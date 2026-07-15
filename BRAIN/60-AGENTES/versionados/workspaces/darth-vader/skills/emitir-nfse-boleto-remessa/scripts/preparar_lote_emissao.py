#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-darth-vader/boletos')
LOTES = ROOT / 'lotes-emissao'
PREPARAR = Path(__file__).resolve().parent / 'preparar_pacote_emissao.py'

PRESTADOR_PADRAO = {
    'nome': 'BIKON TECNOLOGIA DA INFORMACAO LTDA',
    'cnpj': '34.191.026/0001-86',
    'municipio': 'Vitoria',
    'uf': 'ES',
}




def money_centavos(value) -> int:
    clean_value = str(value).strip().replace('R$', '').replace('.', '').replace(',', '.')
    return int(round(float(clean_value) * 100))


def juros_mora_dia_centavos(valor) -> int:
    # Padrão Bikon: juros de mora de 1% ao mês, proporcional ao dia.
    return round(money_centavos(valor) / 3000)


def fmt_money_centavos(cents: int) -> str:
    return f'{cents / 100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def instrucoes_boleto_padrao(valor) -> str:
    juros = fmt_money_centavos(juros_mora_dia_centavos(valor))
    return (
        'Após o vencimento cobrar multa de 2,00%.\n'
        f'Após o vencimento cobrar juros de R$ {juros} ao dia.'
    )

def clean(v):
    return (v or '').strip()


def row_to_job(row: dict) -> dict:
    valor = clean(row.get('valor_total'))
    data_emissao = clean(row.get('data_emissao'))
    return {
        'cliente_slug': clean(row.get('cliente_slug')),
        'modo': 'homologacao',
        'prestador': PRESTADOR_PADRAO,
        'tomador': {
            'nome': clean(row.get('tomador_nome')),
            'cnpj': clean(row.get('tomador_cnpj')),
            'endereco': clean(row.get('tomador_endereco')),
            'bairro': clean(row.get('tomador_bairro')),
            'cep': clean(row.get('tomador_cep')),
            'cidade': clean(row.get('tomador_cidade')),
            'uf': clean(row.get('tomador_uf')),
            'email': clean(row.get('email_tomador')),
        },
        'nfse': {
            'status': 'rascunho_preparado',
            'numero_anterior': clean(row.get('numero_nfse_anterior')),
            'numero_novo': 'pendente',
            'competencia': clean(row.get('competencia')),
            'data_emissao_planejada': data_emissao,
            'codigo_tributacao_nacional': clean(row.get('codigo_tributacao')),
            'forma_pagamento': clean(row.get('forma_pagamento')) or 'Boleto Cresol',
            'itens': [{'descricao': clean(row.get('descricao_servico')), 'quantidade': 1, 'valor_unitario': valor, 'valor_total': valor}],
            'valor_total': valor,
        },
        'boleto': {
            'status': 'rascunho_preparado',
            'banco': '133',
            'carteira': clean(row.get('carteira')) or '009',
            'cooperativa': clean(row.get('cooperativa')) or '01008',
            'agencia': clean(row.get('agencia')) or '1008-0',
            'conta': clean(row.get('conta')) or '0027846',
            'conta_dv': clean(row.get('conta_dv')) or '7',
            'numero_documento': clean(row.get('numero_documento')),
            'nosso_numero': clean(row.get('nosso_numero')),
            'data_documento': clean(row.get('data_documento')) or data_emissao,
            'vencimento': clean(row.get('vencimento')),
            'valor': valor,
            'juros_mora_dia_centavos': int(clean(row.get('juros_mora_dia_centavos')) or juros_mora_dia_centavos(valor)),
            'instrucoes': instrucoes_boleto_padrao(valor),
        },
        'remessa': {
            'layout': 'CNAB400',
            'seq_remessa': clean(row.get('seq_remessa')),
            'data_gravacao': clean(row.get('data_gravacao')) or data_emissao,
        },
        'fontes': ['lista de emissão em lote'],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description='Prepara lote de NFS-e + boleto + remessa')
    ap.add_argument('--csv', required=True, help='CSV de entrada')
    args = ap.parse_args()

    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    lote_dir = LOTES / stamp
    jobs_dir = lote_dir / 'jobs'
    jobs_dir.mkdir(parents=True, exist_ok=True)

    results = []
    with open(args.csv, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            job = row_to_job(row)
            job_path = jobs_dir / f'{idx:03d}-{job.get("cliente_slug") or "cliente"}.json'
            job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            proc = subprocess.run([sys.executable, str(PREPARAR), '--job', str(job_path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            item = {'linha': idx, 'job': str(job_path), 'returncode': proc.returncode}
            if proc.returncode == 0:
                item.update(json.loads(proc.stdout))
            else:
                item['error'] = proc.stderr.strip() or proc.stdout.strip()
            results.append(item)

    status = lote_dir / 'status-lote.md'
    ok = [r for r in results if r['returncode'] == 0]
    fail = [r for r in results if r['returncode'] != 0]
    lines = [
        '# Status lote NFS-e + boleto + remessa', '',
        f'Gerado em: {datetime.now().isoformat(timespec="seconds")}',
        f'- Total: {len(results)}',
        f'- OK: {len(ok)}',
        f'- Falha: {len(fail)}', '',
        '## Itens', ''
    ]
    for r in results:
        if r['returncode'] == 0:
            lines.append(f"- Linha {r['linha']}: OK, pacote `{r.get('pacote')}`, boleto `{r.get('boleto_pdf')}`, remessa `{r.get('remessa')}`")
        else:
            lines.append(f"- Linha {r['linha']}: FALHA, {r.get('error')}")
    status.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    result = {'lote': str(lote_dir), 'status': str(status), 'total': len(results), 'ok': len(ok), 'falha': len(fail), 'items': results}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
