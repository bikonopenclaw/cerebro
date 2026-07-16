#!/usr/bin/env python3
"""Sincroniza snapshots seguros dos agentes Kowalski, Darth Vader e Robotnik para o Brain.

Não copia segredos, sessões, caches, relatórios finais, binários pesados nem artefatos gerados.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import fnmatch
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

BRAIN = Path('/data/.openclaw/workspace/Brain/BRAIN')
SNAP = BRAIN / '60-AGENTES' / 'versionados'

CHECK_IGNORE = {'MANIFEST.md'}
MAX_DIFF_LINES = 240
SECRET_PATTERNS = (
    ('private-key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
    ('github-token', re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b')),
    ('aws-access-key', re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
    ('jwt', re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b')),
)
SECRET_ASSIGNMENT = re.compile(
    r'(?i)[\"\']?\b(api[_-]?key|access[_-]?token|refresh[_-]?token|secret|password|senha)\b[\"\']?'
    r'\s*[:=]\s*[\"\']([^\"\']{12,})[\"\']'
)
SAFE_VALUE_MARKERS = {
    'definir', 'example', 'exemplo', 'placeholder', 'redacted',
    'changeme', 'your_', 'sua_', 'seu_', 'preencher', 'substituir',
    'trocar', 'dummy', 'fake', 'teste', 'aqui', '<', '${', 'fora_do_git',
}

EXCLUDE_DIRS = {
    '.git', 'sessions', '.openclaw', '__pycache__', '.pytest_cache',
    'node_modules', 'vendor', '.venv', '.pydeps', 'secrets',
    'exports', 'drafts',
}
EXCLUDE_DIR_PREFIXES = (
    '.venv-',
    'homologacao-',
)
EXCLUDE_FILE_PATTERNS = [
    '*.pyc', '*.pyo', '*.log', '*.lock',
    '*.sqlite', '*.sqlite3', '*.sqlite-shm', '*.sqlite-wal', '*.db',
    'openclaw-workspace-state.json',
    '.env', '.env.*', 'auth-profiles.json', 'models.json',
    '*token*', '*Token*', '*secret*', '*Secret*',
    '*segredo*', '*Segredo*', '*SEGREDO*', '*senha*', '*Senha*',
    '*credential*', '*Credential*', '*oauth*', '*OAuth*',
    '*.pdf', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp', '*.svg',
    '*.csv',
    '*.docx', '*.xlsx', '*.zip', '*.rem', '*.ret',
]


def excluded_file(name: str) -> bool:
    if name == '.env.example':
        return False
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_FILE_PATTERNS)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def file_map(root: Path) -> dict[str, Path]:
    return {
        str(path.relative_to(root)): path
        for path in root.rglob('*')
        if path.is_file() and str(path.relative_to(root)) not in CHECK_IGNORE
    }


def finding_fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]


def scan_text_secrets(rel: str, text: str) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    for label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append((rel, label, finding_fingerprint(match.group(0))))
    for match in SECRET_ASSIGNMENT.finditer(text):
        value = match.group(2).lower()
        if not any(marker in value for marker in SAFE_VALUE_MARKERS):
            findings.append((
                rel,
                f'assignment:{match.group(1).lower()}',
                finding_fingerprint(match.group(2)),
            ))
    return findings


def scan_secrets(root: Path) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    for rel, path in file_map(root).items():
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text_secrets(rel, text))
    return sorted(set(findings))


def git_worktree_check(repo: Path) -> tuple[
    list[tuple[str, str]], list[str], set[tuple[str, str, str]], set[tuple[str, str, str]]
]:
    status_raw = subprocess.run(
        ['git', '-C', str(repo), 'status', '--porcelain=v1', '-z', '--untracked-files=all'],
        check=True,
        capture_output=True,
    ).stdout
    changes: list[tuple[str, str]] = []
    new_findings: set[tuple[str, str, str]] = set()
    baseline_findings: set[tuple[str, str, str]] = set()

    for entry in status_raw.split(b'\0'):
        if not entry:
            continue
        status = entry[:2].decode('utf-8', errors='replace')
        rel = entry[3:].decode('utf-8', errors='surrogateescape')
        changes.append((status, rel))
        path = repo / rel
        if not path.is_file():
            continue
        try:
            current_text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        current = set(scan_text_secrets(rel, current_text))
        previous = subprocess.run(
            ['git', '-C', str(repo), 'show', f'HEAD:{rel}'],
            capture_output=True,
        )
        if previous.returncode == 0:
            try:
                previous_text = previous.stdout.decode('utf-8')
            except UnicodeDecodeError:
                previous_text = ''
            baseline = set(scan_text_secrets(rel, previous_text))
        else:
            baseline = set()
        new_findings.update(current - baseline)
        baseline_findings.update(current & baseline)

    tracked_diff = subprocess.run(
        ['git', '-C', str(repo), 'diff', '--no-ext-diff', '--unified=3', 'HEAD', '--'],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines(keepends=True)
    diff_lines = tracked_diff[:MAX_DIFF_LINES]
    tracked_paths = {line[4:] for line in tracked_diff if line.startswith('+++ b/')}
    for status, rel in changes:
        if '?' in status and rel not in tracked_paths and len(diff_lines) < MAX_DIFF_LINES:
            diff_lines.append(f'A {rel} (arquivo não rastreado; conteúdo omitido)\n')

    return sorted(changes), diff_lines, new_findings, baseline_findings


def compare_snapshots(current: Path, candidate: Path) -> tuple[list[tuple[str, str]], list[str]]:
    old = file_map(current)
    new = file_map(candidate)
    changes: list[tuple[str, str]] = []
    diff_lines: list[str] = []

    for rel in sorted(old.keys() | new.keys()):
        if rel not in old:
            status = 'A'
        elif rel not in new:
            status = 'D'
        elif sha256(old[rel]) != sha256(new[rel]):
            status = 'M'
        else:
            continue
        changes.append((status, rel))

        if len(diff_lines) >= MAX_DIFF_LINES:
            continue
        try:
            before = old[rel].read_text(encoding='utf-8').splitlines(keepends=True) if rel in old else []
            after = new[rel].read_text(encoding='utf-8').splitlines(keepends=True) if rel in new else []
        except UnicodeDecodeError:
            diff_lines.append(f'{status} {rel} (arquivo não textual)\n')
            continue
        remaining = MAX_DIFF_LINES - len(diff_lines)
        file_diff = list(difflib.unified_diff(
            before,
            after,
            fromfile=f'a/{rel}',
            tofile=f'b/{rel}',
            n=3,
        ))
        diff_lines.extend(file_diff[:remaining])

    return changes, diff_lines


def copy_tree(src: Path, dst: Path, *, extra_exclude_dirs=(), extra_exclude_rel=()) -> None:
    extra_exclude_dirs = set(extra_exclude_dirs)
    extra_exclude_rel = {Path(x) for x in extra_exclude_rel}
    for root, dirs, files in os.walk(src):
        rootp = Path(root)
        rel = rootp.relative_to(src)
        if any(rel == x or x in rel.parents for x in extra_exclude_rel):
            continue
        dirs[:] = [
            d for d in dirs
            if d not in EXCLUDE_DIRS
            and d not in extra_exclude_dirs
            and not any(d.startswith(prefix) for prefix in EXCLUDE_DIR_PREFIXES)
            and not d.startswith('tmp-')
            and not d.startswith('tmp_')
            and d not in {'tmp', 'temp'}
            and rel / d not in extra_exclude_rel
        ]
        target_dir = dst / rel
        target_dir.mkdir(parents=True, exist_ok=True)
        for filename in files:
            if excluded_file(filename):
                continue
            rfile = rel / filename
            if any(rfile == x or x in rfile.parents for x in extra_exclude_rel):
                continue
            shutil.copy2(rootp / filename, target_dir / filename)


def write_docs() -> None:
    SNAP.mkdir(parents=True, exist_ok=True)
    (SNAP / 'README.md').write_text('''# Agentes versionados no Brain

Este diretório guarda snapshots controlados do código-fonte operacional dos agentes Kowalski, Darth Vader e Robotnik.

## Objetivo

- Trazer skills, scripts, documentação operacional e configuração não sensível dos agentes para o Git do Brain.
- Permitir auditoria, diff e rollback básico das mudanças importantes.
- Evitar depender apenas dos workspaces vivos dos agentes, que não são repositórios Git próprios.

## O que entra

- `agents/<agente>/agent`: definição e skills instaladas do agente.
- `workspaces/<agente>/`: arquivos operacionais de código, skills, scripts, docs, templates e exemplos não sensíveis.
- `workspaces/main/skills`: skills globais aprovadas do workspace principal.
- Manifesto com data, origem e regras de exclusão.

## O que não entra

- `.env`, `.env.*`, tokens OAuth, credenciais, segredos, senhas e chaves.
- Sessões, caches, `__pycache__`, `.openclaw`, logs, locks e artefatos temporários.
- Relatórios finais de clientes, PDFs, imagens, documentos binários e pacotes gerados.
- Dados brutos sensíveis de clientes ou respostas completas de APIs.

## Regra

Se um arquivo for necessário para entender ou reconstruir uma automação, ele deve entrar sanitizado ou como `.example`.
Se expõe segredo, cliente ou artefato operacional final, fica fora do Git.
''', encoding='utf-8')
    (SNAP / '.versionamento-rules.md').write_text('''# Regras de versionamento dos agentes

## Inclui

- Markdown operacional: `*.md`
- Código: `*.py`, `*.js`, `*.sh`, `*.sql`
- Configuração segura: `*.example`, `.gitignore`, schemas e JSON/YAML sem segredo
- Templates: `*.html`, `*.txt`, `*.xml`, `*.fr3.xml`

## Exclui

- `.env*`, exceto `.env.example`
- Arquivos com `token`, `secret`, `senha`, `credential`, `oauth` no nome
- `sessions/`, `.openclaw/`, `__pycache__/`, `.pytest_cache/`, `node_modules/`, `vendor/`, `.venv/`, `.venv-*`, `.pydeps/`
- bancos/estado/caches locais: `*.sqlite`, `*.sqlite-shm`, `*.sqlite-wal`, `*.db`, `openclaw-workspace-state.json`
- `relatorios/`, `pacotes-emissao/`, `email-rascunhos/`, `dados/`, `jobs/`, `api-homologacao/`, `homologacao-*` quando forem artefatos de execução
- Dados exportados e rascunhos gerados: `exports/`, `drafts/`, `*.csv`
- Binários, imagens e documentos finais: `*.pdf`, `*.png`, `*.jpg`, `*.jpeg`, `*.svg`, `*.docx`, `*.xlsx`, `*.rem`, `*.ret`, `*.zip`

## Exceção

Manuais, modelos ou exemplos binários relevantes devem ser guardados fora do snapshot ou substituídos por análise textual/sanitizada.
''', encoding='utf-8')


def sync_snapshot() -> int:
    write_docs()
    for sub in ['agents', 'workspaces']:
        path = SNAP / sub
        if path.exists():
            shutil.rmtree(path)
    (SNAP / 'agents').mkdir(parents=True, exist_ok=True)
    (SNAP / 'workspaces').mkdir(parents=True, exist_ok=True)

    for agent in ['kowalski', 'darth-vader', 'robotnik', 'sentinel']:
        copy_tree(Path(f'/data/.openclaw/agents/{agent}/agent'), SNAP / 'agents' / agent / 'agent')

    copy_tree(
        Path('/data/.openclaw/workspace-kowalski'),
        SNAP / 'workspaces' / 'kowalski',
        extra_exclude_dirs={
            'relatorios', 'dados', 'jobs', 'email-rascunhos', 'inbox',
            'backups', 'logs',
        },
        extra_exclude_rel={
            'identidade-visual/logos',
            'identidade-visual/modelos-aprovados',
            'identidade-visual/referencias',
            'media/inbound',
        },
    )
    copy_tree(
        Path('/data/.openclaw/workspace-darth-vader'),
        SNAP / 'workspaces' / 'darth-vader',
        extra_exclude_dirs={'relatorios', 'cadastros', 'backups', 'logs'},
        extra_exclude_rel={
            'cadastro-clientes/originais',
            'boletos/exemplos',
            'boletos/manual-cresol',
            'boletos/remessas',
            'boletos/api-homologacao',
            'boletos/pacotes-emissao',
            'boletos/entradas',
            'boletos/lotes-emissao',
            'media/inbound',
            'skills/serpro-integra-parcelamentos/SEGREDOS.md',
        },
    )
    copy_tree(
        Path('/data/.openclaw/workspace-robotnik'),
        SNAP / 'workspaces' / 'robotnik',
        extra_exclude_dirs={'backups', 'logs'},
        extra_exclude_rel={
            'instagram-bikon/secrets',
            'instagram-bikon/logs',
            'media/inbound',
        },
    )
    copy_tree(
        Path('/data/.openclaw/workspace-sentinel'),
        SNAP / 'workspaces' / 'sentinel',
        extra_exclude_dirs={'backups', 'logs'},
        extra_exclude_rel={'media/inbound'},
    )
    copy_tree(
        Path('/data/.openclaw/workspace/skills'),
        SNAP / 'workspaces' / 'main' / 'skills',
        extra_exclude_dirs={'_quarantine'},
    )

    # Remove configs reais e substitui por exemplo seguro quando necessário.
    for path in [
        SNAP / 'workspaces/darth-vader/skills/notaas-nfse/config/empresa.json',
        SNAP / 'workspaces/darth-vader/skills/notaas-nfse/config/empresa.json.bak-sem-im-20260613210903',
    ]:
        path.unlink(missing_ok=True)
    cfg = SNAP / 'workspaces/darth-vader/skills/notaas-nfse/config/empresa.example.json'
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text('''{
  "empresa": {
    "nome": "Bikon Tecnologia da Informação Ltda Me",
    "cnpj": "34.191.026/0001-86",
    "cidade_ibge": "3205309",
    "cidade_uf": "Vitória/ES"
  },
  "notaas": {
    "api_key": "DEFINIR_EM_ARQUIVO_LOCAL_FORA_DO_GIT",
    "base_url": "https://platform.notaas.com.br/api/v1"
  }
}
''', encoding='utf-8')

    # Limpeza extra de artefatos de documento expandido.
    shutil.rmtree(SNAP / 'workspaces/kowalski/arx-backup/modelo-anexo-inspecao/unzipped', ignore_errors=True)
    (SNAP / 'workspaces/kowalski/arx-backup/modelo-anexo-inspecao/texto-extraido.txt').unlink(missing_ok=True)

    (SNAP / 'MANIFEST.md').write_text(f'''# Manifesto dos snapshots dos agentes

Gerado em: {dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()}

## Origens

- Kowalski agent: /data/.openclaw/agents/kowalski/agent
- Kowalski workspace: /data/.openclaw/workspace-kowalski
- Darth Vader agent: /data/.openclaw/agents/darth-vader/agent
- Darth Vader workspace: /data/.openclaw/workspace-darth-vader
- Robotnik agent: /data/.openclaw/agents/robotnik/agent
- Robotnik workspace: /data/.openclaw/workspace-robotnik
- Sentinel agent: /data/.openclaw/agents/sentinel/agent
- Sentinel workspace: /data/.openclaw/workspace-sentinel
- Main workspace skills: /data/.openclaw/workspace/skills

## Destino

- BRAIN/60-AGENTES/versionados/

## Política

Snapshot seguro, sem sessões, segredos, tokens, caches, relatórios finais de clientes, binários pesados ou artefatos gerados.
''', encoding='utf-8')
    return 0


def check_snapshot() -> int:
    global SNAP
    current = SNAP
    with tempfile.TemporaryDirectory(prefix='brain-agent-check-') as tmp:
        candidate = Path(tmp) / 'versionados'
        SNAP = candidate
        try:
            sync_snapshot()
        finally:
            SNAP = current

        current_findings = set(scan_secrets(current))
        candidate_findings = set(scan_secrets(candidate))
        snapshot_new_findings = candidate_findings - current_findings
        snapshot_baseline_findings = candidate_findings & current_findings
        snapshot_changes, snapshot_diff_lines = compare_snapshots(current, candidate)
        repo_changes, repo_diff_lines, repo_new_findings, repo_baseline_findings = git_worktree_check(BRAIN.parent)
        new_findings = sorted(snapshot_new_findings | repo_new_findings)
        baseline_findings = sorted(snapshot_baseline_findings | repo_baseline_findings)

        if new_findings:
            print('CHECK_RESULT=BLOCKED_SECRETS')
            print(f'NEW_SECRET_FINDINGS={len(new_findings)}')
            print(f'BASELINE_CANDIDATES={len(baseline_findings)}')
            for rel, label, _fingerprint in new_findings:
                print(f'SECRET\t{label}\t{rel}')
            return 2

        if not snapshot_changes and not repo_changes:
            print('CHECK_RESULT=CLEAN')
            print('SNAPSHOT_CHANGES=0')
            print('REPO_CHANGES=0')
            print(f'BASELINE_CANDIDATES={len(baseline_findings)}')
            return 0

        print('CHECK_RESULT=CHANGES')
        print(f'SNAPSHOT_CHANGES={len(snapshot_changes)}')
        print(f'REPO_CHANGES={len(repo_changes)}')
        print(f'BASELINE_CANDIDATES={len(baseline_findings)}')
        for status, rel in snapshot_changes:
            print(f'SNAPSHOT_{status}\t{rel}')
        for status, rel in repo_changes:
            print(f'REPO_{status}\t{rel}')
        print('SNAPSHOT_DIFF_BEGIN')
        for line in snapshot_diff_lines:
            print(line, end='' if line.endswith('\n') else '\n')
        if len(snapshot_diff_lines) >= MAX_DIFF_LINES:
            print(f'SNAPSHOT_DIFF_TRUNCATED_AT={MAX_DIFF_LINES}')
        print('SNAPSHOT_DIFF_END')
        print('REPO_DIFF_BEGIN')
        for line in repo_diff_lines:
            print(line, end='' if line.endswith('\n') else '\n')
        if len(repo_diff_lines) >= MAX_DIFF_LINES:
            print(f'REPO_DIFF_TRUNCATED_AT={MAX_DIFF_LINES}')
        print('REPO_DIFF_END')
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--check',
        action='store_true',
        help='Compara snapshot sanitizado em diretório temporário, sem alterar o Brain.',
    )
    args = parser.parse_args()
    return check_snapshot() if args.check else sync_snapshot()


if __name__ == '__main__':
    raise SystemExit(main())
