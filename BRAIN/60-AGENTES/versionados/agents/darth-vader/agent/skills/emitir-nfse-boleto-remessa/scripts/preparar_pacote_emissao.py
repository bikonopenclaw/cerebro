#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-darth-vader/boletos')
PACOTES = ROOT / 'pacotes-emissao'
REMESSA_GENERATOR = ROOT / 'scripts' / 'gerar_remessa_cnab400_cresol.py'
BOLETO_GENERATOR = ROOT / 'scripts' / 'gerar_boleto_cresol_html.py'
EMAIL_GENERATOR = Path('/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_email_cliente.py')


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'cliente'


def require(data: dict, path: str):
    cur = data
    for part in path.split('.'):
        if not isinstance(cur, dict) or part not in cur or cur[part] in (None, ''):
            raise SystemExit(f'Campo obrigatório ausente: {path}')
        cur = cur[part]
    return cur


def validate_job(job: dict) -> list[str]:
    errors = []
    for path in [
        'cliente_slug', 'modo',
        'prestador.nome', 'prestador.cnpj',
        'tomador.nome', 'tomador.cnpj', 'tomador.endereco', 'tomador.cep',
        'nfse.status', 'nfse.valor_total',
        'boleto.status', 'boleto.numero_documento', 'boleto.nosso_numero', 'boleto.vencimento', 'boleto.valor',
        'boleto.banco', 'boleto.carteira', 'boleto.cooperativa', 'boleto.conta', 'boleto.conta_dv',
        'remessa.layout', 'remessa.seq_remessa', 'remessa.data_gravacao',
    ]:
        try:
            require(job, path)
        except SystemExit as exc:
            errors.append(str(exc))
    if job.get('modo') != 'homologacao':
        errors.append('modo deve ser homologacao até aprovação explícita de produção')
    if job.get('remessa', {}).get('layout') != 'CNAB400':
        errors.append('script atual só gera CNAB400')
    return errors


def build_remessa_input(job: dict) -> dict:
    tomador = job['tomador']
    boleto = job['boleto']
    remessa = job['remessa']
    return {
        'observacao': 'Gerado pela skill emitir-nfse-boleto-remessa. Homologação até validação bancária.',
        'data_gravacao': remessa['data_gravacao'],
        'seq_remessa': remessa['seq_remessa'],
        'titulos': [{
            'numero_documento': boleto['numero_documento'],
            'nosso_numero': boleto['nosso_numero'],
            'data_emissao': job['nfse'].get('data_emissao_planejada') or remessa['data_gravacao'],
            'vencimento': boleto['vencimento'],
            'valor': boleto['valor'],
            'juros_mora_dia_centavos': boleto.get('juros_mora_dia_centavos'),
            'pagador_nome': tomador['nome'],
            'pagador_cnpj': tomador['cnpj'],
            'pagador_endereco': tomador['endereco'],
            'pagador_bairro': tomador.get('bairro', ''),
            'pagador_cep': tomador['cep'],
            'pagador_cidade': tomador.get('cidade', ''),
            'pagador_uf': tomador.get('uf', ''),
        }],
    }


def build_boleto_input(job: dict) -> dict:
    prestador = job['prestador']
    tomador = job['tomador']
    boleto = job['boleto']
    nfse = job.get('nfse', {})
    return {
        'beneficiario_nome': prestador['nome'],
        'beneficiario_cnpj': prestador['cnpj'],
        'pagador_nome': tomador['nome'],
        'pagador_cnpj': tomador['cnpj'],
        'pagador_endereco': tomador['endereco'],
        'pagador_cep': tomador['cep'],
        'pagador_cidade': tomador.get('cidade', ''),
        'pagador_uf': tomador.get('uf', ''),
        'banco': boleto.get('banco', '133'),
        'agencia': boleto.get('agencia') or f"{boleto['cooperativa']}-0",
        'cooperativa': boleto['cooperativa'],
        'conta': boleto['conta'],
        'conta_dv': boleto['conta_dv'],
        'carteira': boleto['carteira'],
        'numero_documento': boleto['numero_documento'],
        'nosso_numero': boleto['nosso_numero'],
        'data_documento': boleto.get('data_documento') or nfse.get('data_emissao_planejada') or job['remessa']['data_gravacao'],
        'vencimento': boleto['vencimento'],
        'valor': boleto['valor'],
        'nfse_numero': nfse.get('numero') or nfse.get('numero_novo') or '',
        'nfse_chave': nfse.get('chave') or '',
        'instrucoes': boleto.get('instrucoes', 'NÃO RECEBER APÓS O VENCIMENTO.'),
    }


def write_status(pkg: Path, job: dict, boleto_meta: dict | None, remessa_meta: dict | None, email_meta: dict | None, errors: list[str]) -> Path:
    nfse_status = job.get('nfse', {}).get('status', 'pendente')
    boleto_status = job.get('boleto', {}).get('status', 'pendente')
    remessa_status = 'erro_validacao' if errors else 'remessa_gerada_homologacao'
    out = pkg / 'status-emissao.md'
    out.write_text('\n'.join([
        '# Status do pacote NFS-e + boleto + remessa',
        '',
        f"Gerado em: {datetime.now().isoformat(timespec='seconds')}",
        '',
        f"- Cliente: {job.get('tomador', {}).get('nome', '-')}",
        f"- Modo: {job.get('modo', '-')}",
        f"- NFS-e: {nfse_status}",
        f"- Boleto: {boleto_status}",
        f"- Remessa: {remessa_status}",
        f"- E-mail cliente: {email_meta.get('status') if email_meta else 'não preparado'}",
        '',
        '## Arquivos',
        '',
        f"- Job original: `{pkg / 'job.json'}`",
        f"- Entrada boleto: `{pkg / 'boleto-input.json'}`",
        f"- Boleto PDF: `{boleto_meta.get('pdf') if boleto_meta else '-'}`",
        f"- Linha digitável: `{boleto_meta.get('linha_digitavel') if boleto_meta else '-'}`",
        f"- Entrada remessa: `{pkg / 'remessa-input.json'}`",
        f"- Remessa: `{remessa_meta.get('arquivo') if remessa_meta else '-'}`",
        f"- E-mail cliente: `{email_meta.get('eml') if email_meta else '-'}`",
        '',
        '## Pendências',
        '',
        '- Emitir NFS-e real no emissor fiscal e anexar DANFSe/XML/chave.' if nfse_status != 'nfse_emitida' else '- NFS-e real já marcada como emitida no job.',
        '- Boleto PDF gerado para homologação/conferência; registro bancário real depende da validação/aceite do banco.' if boleto_meta else '- Emitir/registrar boleto real e anexar PDF/linha digitável.',
        '- Validar remessa no ambiente de teste do banco antes de qualquer produção.',
        '- Conferir/aprovar envio do e-mail ao cliente antes de qualquer disparo externo.' if email_meta else '- Preparar e-mail ao cliente quando NFS-e PDF/XML estiverem disponíveis.',
        '',
        '## Erros de validação',
        '',
        *(f'- {e}' for e in errors),
        ''
    ]), encoding='utf-8')
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description='Prepara pacote NFS-e + boleto + remessa Cresol')
    ap.add_argument('--job', required=True, help='Caminho do job JSON')
    args = ap.parse_args()

    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding='utf-8'))
    errors = validate_job(job)

    slug = slugify(job.get('cliente_slug') or job.get('tomador', {}).get('nome', 'cliente'))
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    pkg = PACOTES / f'{stamp}-{slug}'
    pkg.mkdir(parents=True, exist_ok=True)
    shutil.copy2(job_path, pkg / 'job.json')

    boleto_meta = None
    remessa_meta = None
    if not errors:
        boleto_input = build_boleto_input(job)
        boleto_input_path = pkg / 'boleto-input.json'
        boleto_input_path.write_text(json.dumps(boleto_input, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        boleto_pdf = pkg / f"{stamp}-{slug}-boleto.pdf"
        boleto_html = pkg / f"{stamp}-{slug}-boleto.html"
        proc_boleto = subprocess.run(
            [sys.executable, str(BOLETO_GENERATOR), '--input', str(boleto_input_path), '--html-output', str(boleto_html), '--pdf-output', str(boleto_pdf)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc_boleto.returncode != 0:
            errors.append(proc_boleto.stderr.strip() or proc_boleto.stdout.strip() or 'falha ao gerar boleto')
        else:
            boleto_meta = json.loads(proc_boleto.stdout)

        remessa_input = build_remessa_input(job)
        remessa_input_path = pkg / 'remessa-input.json'
        remessa_input_path.write_text(json.dumps(remessa_input, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        remessa_out = pkg / f"{stamp}-{slug}.rem"
        proc = subprocess.run(
            [sys.executable, str(REMESSA_GENERATOR), '--input', str(remessa_input_path), '--output', str(remessa_out)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            errors.append(proc.stderr.strip() or proc.stdout.strip() or 'falha ao gerar remessa')
        else:
            remessa_meta = json.loads(proc.stdout)
    else:
        (pkg / 'boleto-input.json').write_text('{}\n', encoding='utf-8')
        (pkg / 'remessa-input.json').write_text('{}\n', encoding='utf-8')

    email_meta = None
    nfse = job.get('nfse', {})
    email_attachments = [p for p in [nfse.get('pdf'), nfse.get('xml')] if p]
    if boleto_meta and boleto_meta.get('pdf'):
        email_attachments.append(boleto_meta['pdf'])
    if email_attachments and EMAIL_GENERATOR.exists():
        cmd = [sys.executable, str(EMAIL_GENERATOR), '--job', str(pkg / 'job.json'), '--out-dir', str(pkg)]
        for attach in email_attachments:
            cmd += ['--anexo', str(attach)]
        proc_email = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc_email.returncode != 0:
            errors.append(proc_email.stderr.strip() or proc_email.stdout.strip() or 'falha ao preparar e-mail ao cliente')
        else:
            email_meta = json.loads(proc_email.stdout)

    status = write_status(pkg, job, boleto_meta, remessa_meta, email_meta, errors)
    result = {
        'pacote': str(pkg),
        'status': str(status),
        'boleto_pdf': boleto_meta.get('pdf') if boleto_meta else None,
        'linha_digitavel': boleto_meta.get('linha_digitavel') if boleto_meta else None,
        'remessa': remessa_meta.get('arquivo') if remessa_meta else None,
        'email_cliente': email_meta,
        'errors': errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
