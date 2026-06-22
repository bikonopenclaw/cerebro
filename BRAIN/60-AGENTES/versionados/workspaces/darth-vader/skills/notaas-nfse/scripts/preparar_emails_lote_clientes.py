#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

SCRIPT_EMAIL = Path(__file__).resolve().parent / 'preparar_email_cliente.py'


def clean_doc(value: str) -> str:
    return re.sub(r'\D', '', value or '')


def load_jobs(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'jobs' in data:
        data = data['jobs']
    if not isinstance(data, list):
        raise SystemExit('Entrada deve ser uma lista de jobs ou objeto com chave jobs.')
    return data


def group_key(job: dict) -> str:
    tomador = job.get('tomador', {})
    return (
        str(job.get('cliente_id') or tomador.get('cliente_id') or '').strip()
        or clean_doc(tomador.get('cnpj') or tomador.get('cpf') or tomador.get('documento') or '')
        or str(job.get('cliente_slug') or tomador.get('nome') or 'cliente-sem-id').lower()
    )


def doc_from_job(job: dict) -> list[dict]:
    nfse = job.get('nfse', {})
    if nfse.get('documentos'):
        return nfse['documentos']
    boleto = job.get('boleto', {})
    return [{
        'numero': nfse.get('numero') or nfse.get('numero_novo') or 'pendente',
        'chave': nfse.get('chave') or '',
        'valor_total': nfse.get('valor_total') or boleto.get('valor') or '',
        'pdf': nfse.get('pdf'),
        'xml': nfse.get('xml'),
        'boleto_pdf': boleto.get('pdf'),
        'boleto': {
            'numero_documento': boleto.get('numero_documento') or '',
            'nosso_numero': boleto.get('nosso_numero') or '',
            'vencimento': boleto.get('vencimento') or '',
            'valor': boleto.get('valor') or nfse.get('valor_total') or '',
        }
    }]


def combine_group(jobs: list[dict]) -> dict:
    base = deepcopy(jobs[0])
    docs = []
    for job in jobs:
        docs.extend(doc_from_job(job))
    base.setdefault('nfse', {})
    base['nfse'].pop('pdf', None)
    base['nfse'].pop('xml', None)
    base['nfse']['documentos'] = docs
    base['nfse']['numero'] = ', '.join(str(d.get('numero') or 'pendente') for d in docs)
    base['nfse']['chave'] = 'Conforme lista de documentos'
    base.setdefault('email', {})
    base['email']['agrupado_por_cliente'] = True
    base['email']['total_documentos'] = len(docs)
    return base


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'cliente'


def main() -> int:
    ap = argparse.ArgumentParser(description='Agrupa NFS-e por cliente e prepara um e-mail por cliente')
    ap.add_argument('--jobs-json', required=True, help='JSON com lista de jobs')
    ap.add_argument('--out-dir', required=True, help='Diretório de saída')
    ap.add_argument('--to', action='append', default=[], help='Destinatário explícito para teste, repetir se necessário')
    ap.add_argument('--confirmar-envio', action='store_true', help='Envia e-mails aprovados')
    args = ap.parse_args()

    jobs = load_jobs(Path(args.jobs_json))
    groups: dict[str, list[dict]] = {}
    for job in jobs:
        groups.setdefault(group_key(job), []).append(job)

    out_root = Path(args.out_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    results = []
    for key, group_jobs in groups.items():
        combined = combine_group(group_jobs)
        group_dir = out_root / slug(key)
        group_dir.mkdir(parents=True, exist_ok=True)
        job_path = group_dir / 'job-email-agrupado.json'
        job_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        cmd = [sys.executable, str(SCRIPT_EMAIL), '--job', str(job_path), '--out-dir', str(group_dir)]
        for to in args.to:
            cmd += ['--to', to]
        if args.confirmar_envio:
            cmd.append('--confirmar-envio')
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        item = {'cliente_key': key, 'jobs': len(group_jobs), 'job_agrupado': str(job_path), 'returncode': proc.returncode}
        if proc.returncode == 0:
            item['email'] = json.loads(proc.stdout)
        else:
            item['error'] = proc.stderr.strip() or proc.stdout.strip()
        results.append(item)

    print(json.dumps({'groups': len(groups), 'results': results}, ensure_ascii=False, indent=2))
    return 1 if any(r['returncode'] != 0 for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(main())
