#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-kowalski/arx-backup')
sys.path.insert(0, str(ROOT / 'scripts'))
from gerar_pacote_clientes_arx import coletar, flatten_settings, row_to_context, md_cliente, html_cliente, print_pdf, slugify

TARGET_CLIENTE = '15 - Cartorio Alzira'
TARGET_DISPOSITIVO = '02-hv-03_49tpe'
MARKER = 'ARX_APPROVED_MODEL:modelo-padrao-relatorio-mensal-arx-backup'
BLOCKED_BRANDS = re.compile(r'\b(Bikon|Cove)\b', re.I)
OUT_REL = ROOT / 'relatorios' / 'por-cliente'
OUT_REL.mkdir(parents=True, exist_ok=True)

def main():
    data = coletar()
    rows = data.get('result', {}).get('result') or []
    matches = []
    for row in rows:
        s = flatten_settings(row)
        if s.get('AR') == TARGET_CLIENTE and s.get('AN') == TARGET_DISPOSITIVO:
            matches.append(row)
    if len(matches) != 1:
        raise SystemExit(f'Alvo nao encontrado de forma unica. matches={len(matches)}')

    row = matches[0]
    ctx = row_to_context(row)
    gerado = datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')
    date_tag = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    slug = slugify(ctx['cliente'])
    base = f'relatorio-arx-{date_tag}-{slug}'
    md_path = OUT_REL / f'{base}.md'
    html_path = OUT_REL / f'{base}.html'
    pdf_path = OUT_REL / f'{base}.pdf'

    md_path.write_text(md_cliente(ctx, gerado), encoding='utf-8')
    html = html_cliente(ctx, gerado)
    html_path.write_text(html, encoding='utf-8')

    html_read = html_path.read_text(encoding='utf-8', errors='ignore')
    if MARKER not in html_read:
        raise SystemExit('BLOQUEADO: marcador do modelo aprovado ausente no HTML')
    html_without_marker = html_read.replace(MARKER, '')
    bad = BLOCKED_BRANDS.findall(html_without_marker)
    if bad:
        raise SystemExit('BLOQUEADO: marca proibida no HTML do cliente: ' + ', '.join(sorted(set(bad))))

    print_pdf(html_path, pdf_path)
    if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
        raise SystemExit('BLOQUEADO: PDF nao gerado corretamente')

    print(json.dumps({
        'ok': True,
        'cliente': ctx['cliente'],
        'dispositivo': ctx['dispositivo'],
        'html': str(html_path),
        'pdf': str(pdf_path),
        'status': ctx['status_bikon'],
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
