#!/usr/bin/env python3
"""Sincroniza snapshots seguros dos agentes Kowalski, Darth Vader e Robotnik para o Brain.

Não copia segredos, sessões, caches, relatórios finais, binários pesados nem artefatos gerados.
"""
from __future__ import annotations

import datetime as dt
import fnmatch
import os
import shutil
from pathlib import Path

BRAIN = Path('/data/.openclaw/workspace/Brain/BRAIN')
SNAP = BRAIN / '60-AGENTES' / 'versionados'

EXCLUDE_DIRS = {
    '.git', 'sessions', '.openclaw', '__pycache__', '.pytest_cache',
    'node_modules', 'vendor', '.venv', '.pydeps', 'secrets',
}
EXCLUDE_FILE_PATTERNS = [
    '*.pyc', '*.pyo', '*.log', '*.lock',
    '.env', '.env.*', 'auth-profiles.json', 'models.json',
    '*token*', '*Token*', '*secret*', '*Secret*', '*senha*', '*Senha*',
    '*credential*', '*Credential*', '*oauth*', '*OAuth*',
    '*.pdf', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp',
    '*.docx', '*.xlsx', '*.zip', '*.rem', '*.ret',
]


def excluded_file(name: str) -> bool:
    if name == '.env.example':
        return False
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_FILE_PATTERNS)


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
- `sessions/`, `.openclaw/`, `__pycache__/`, `.pytest_cache/`, `node_modules/`, `vendor/`, `.venv/`, `.pydeps/`
- `relatorios/`, `pacotes-emissao/`, `email-rascunhos/`, `dados/`, `jobs/` quando forem artefatos de execução
- Binários e documentos finais: `*.pdf`, `*.png`, `*.jpg`, `*.jpeg`, `*.docx`, `*.xlsx`, `*.rem`, `*.ret`, `*.zip`

## Exceção

Manuais, modelos ou exemplos binários relevantes devem ser guardados fora do snapshot ou substituídos por análise textual/sanitizada.
''', encoding='utf-8')


def main() -> int:
    write_docs()
    for sub in ['agents', 'workspaces']:
        path = SNAP / sub
        if path.exists():
            shutil.rmtree(path)
    (SNAP / 'agents').mkdir(parents=True, exist_ok=True)
    (SNAP / 'workspaces').mkdir(parents=True, exist_ok=True)

    for agent in ['kowalski', 'darth-vader', 'robotnik']:
        copy_tree(Path(f'/data/.openclaw/agents/{agent}/agent'), SNAP / 'agents' / agent / 'agent')

    copy_tree(
        Path('/data/.openclaw/workspace-kowalski'),
        SNAP / 'workspaces' / 'kowalski',
        extra_exclude_dirs={'relatorios', 'dados', 'jobs', 'email-rascunhos', 'inbox'},
        extra_exclude_rel={'identidade-visual/logos', 'identidade-visual/modelos-aprovados', 'identidade-visual/referencias'},
    )
    copy_tree(
        Path('/data/.openclaw/workspace-darth-vader'),
        SNAP / 'workspaces' / 'darth-vader',
        extra_exclude_dirs={'relatorios', 'cadastros'},
        extra_exclude_rel={
            'cadastro-clientes/originais',
            'boletos/exemplos',
            'boletos/manual-cresol',
            'boletos/remessas',
            'boletos/pacotes-emissao',
            'boletos/entradas',
            'boletos/lotes-emissao',
            'skills/serpro-integra-parcelamentos/SEGREDOS.md',
        },
    )
    copy_tree(
        Path('/data/.openclaw/workspace-robotnik'),
        SNAP / 'workspaces' / 'robotnik',
        extra_exclude_dirs={'logs'},
        extra_exclude_rel={'instagram-bikon/secrets', 'instagram-bikon/logs'},
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

## Destino

- BRAIN/60-AGENTES/versionados/

## Política

Snapshot seguro, sem sessões, segredos, tokens, caches, relatórios finais de clientes, binários pesados ou artefatos gerados.
''', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
