#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
FRX_TEMPLATE = BASE_DIR / 'modelos' / 'modelo-boleto-cresol-oficial.fr3.xml'


def only_digits(v: str) -> str:
    return re.sub(r'\D', '', str(v or ''))


def money_centavos(v) -> int:
    if isinstance(v, int):
        return v
    s = str(v).replace('R$', '').strip()
    if ',' in s:
        s = s.replace('.', '').replace(',', '.')
    return int(round(float(s) * 100))


def fmt_money(v) -> str:
    c = money_centavos(v)
    return f'{c/100:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def parse_date_br(v: str) -> date:
    return datetime.strptime(v, '%d/%m/%Y').date()


def fator_vencimento(venc: str) -> str:
    d = parse_date_br(venc)
    reset = date(2025, 2, 22)
    if d >= reset:
        return str(1000 + (d - reset).days).zfill(4)
    return str((d - date(1997, 10, 7)).days).zfill(4)


def dv_nosso_numero(nosso: str, carteira: str = '09') -> str:
    base = only_digits(carteira)[-2:].zfill(2) + only_digits(nosso).zfill(11)
    weights = [2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(base, weights))
    resto = total % 11
    if resto == 0:
        return '0'
    if resto == 1:
        return 'P'
    return str(11 - resto)


def dv_mod11_barcode(num43: str) -> str:
    total = 0
    weights = list(range(2, 10))
    for i, ch in enumerate(reversed(num43)):
        total += int(ch) * weights[i % len(weights)]
    dig = 11 - (total % 11)
    return '1' if dig in (0, 1) or dig > 9 else str(dig)


def dv_mod10(num: str) -> str:
    total = 0
    mult = 2
    for ch in reversed(num):
        prod = int(ch) * mult
        total += prod if prod < 10 else prod // 10 + prod % 10
        mult = 1 if mult == 2 else 2
    return str((10 - total % 10) % 10)


def campo_livre(d: dict) -> str:
    return (
        only_digits(d['cooperativa'])[-4:].zfill(4)
        + only_digits(d['carteira'])[-2:].zfill(2)
        + only_digits(d['nosso_numero']).zfill(11)
        + only_digits(d['conta']).zfill(7)
        + '0'
    )


def codigo_barras(d: dict) -> str:
    sem_dv = '1339' + fator_vencimento(d['vencimento']) + str(money_centavos(d['valor'])).zfill(10) + campo_livre(d)
    return sem_dv[:4] + dv_mod11_barcode(sem_dv) + sem_dv[4:]


def linha_digitavel(barcode: str) -> str:
    banco_moeda = barcode[:4]
    dv_bar = barcode[4]
    fator_valor = barcode[5:19]
    livre = barcode[19:]
    c1 = banco_moeda + livre[:5]
    c2 = livre[5:15]
    c3 = livre[15:25]
    return f'{c1[:5]}.{c1[5:]}{dv_mod10(c1)} {c2[:5]}.{c2[5:]}{dv_mod10(c2)} {c3[:5]}.{c3[5:]}{dv_mod10(c3)} {dv_bar} {fator_valor}'


def barcode_svg_base64(barcode: str) -> str:
    target = '/tmp/boleto_pdfdeps'
    try:
        from reportlab.graphics.barcode import createBarcodeDrawing
        from reportlab.graphics import renderSVG
        from reportlab.lib.units import mm
    except Exception:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', '--target', target, 'reportlab'])
        sys.path.insert(0, target)
        from reportlab.graphics.barcode import createBarcodeDrawing
        from reportlab.graphics import renderSVG
        from reportlab.lib.units import mm
    drawing = createBarcodeDrawing('I2of5', value=barcode, barHeight=23.4 * mm, barWidth=0.624 * mm, checksum=0, humanReadable=False)
    svg = renderSVG.drawToString(drawing)
    if isinstance(svg, bytes):
        svg = svg.decode('utf-8')
    return base64.b64encode(svg.encode('utf-8')).decode('ascii')


def fr_num(v: str | None, default: float = 0.0) -> float:
    if v is None or v == '':
        return default
    return float(str(v).replace(',', '.'))


def split_agencia(v: str) -> tuple[str, str]:
    s = str(v or '').strip()
    if '-' in s:
        a, dv = s.rsplit('-', 1)
        return only_digits(a), only_digits(dv)
    digs = only_digits(s)
    return digs, '0'


def split_endereco(s: str) -> dict:
    parts = [p.strip() for p in str(s or '').split(',')]
    rua = parts[0] if parts else ''
    numero = parts[1] if len(parts) > 1 else ''
    complemento = ''
    bairro = parts[2] if len(parts) > 2 else ''
    if len(parts) > 3:
        complemento = ' '.join(parts[2:-1])
        bairro = parts[-1]
    return {'SACADO_RUA': rua, 'SACADO_NUMERO': numero, 'SACADO_COMPLEMENTO': complemento, 'SACADO_BAIRRO': bairro}


def png_from_propdata(prop: str) -> str:
    # FastReport salva metadados antes da assinatura PNG.
    idx = prop.find('89504E470D0A1A0A')
    if idx < 0:
        return ''
    return base64.b64encode(bytes.fromhex(prop[idx:])).decode('ascii')


def boleto_fields(d: dict, barcode: str, linha: str) -> dict:
    ag, ag_dv = split_agencia(d.get('agencia') or d.get('cooperativa') or '')
    end = split_endereco(d.get('pagador_endereco', ''))
    carteira = only_digits(d.get('carteira', '09')) or '09'
    nosso_base = only_digits(d.get('nosso_numero', '')).zfill(11)
    nosso_dv = d.get('digito_nosso_numero') or dv_nosso_numero(nosso_base, carteira)
    conta = only_digits(d.get('conta', ''))
    fields = {
        'CODIGO_BANCO': '133-3',
        'LINHA_DIGITAVEL': linha,
        'CODIGO_BARRAS': barcode,
        'NOME_CEDENTE': d.get('beneficiario_nome', ''),
        'CNPJ_CEDENTE': d.get('beneficiario_cnpj', ''),
        'AGENCIA': ag,
        'DIGITO_AGENCIA': ag_dv,
        'CONTA': conta.lstrip('0') or conta,
        'DIGITO_CONTA': d.get('conta_dv', ''),
        'CARTEIRA': carteira,
        'NOSSO_NUMERO': nosso_base,
        'DIGITO_NOSSO_NUMERO': nosso_dv,
        'NUMERO_DOCUMENTO': d.get('numero_documento', ''),
        'DATA_DOCUMENTO': d.get('data_documento', ''),
        'DATA_PROCESSAMENTO': d.get('data_processamento') or d.get('data_documento', ''),
        'DATA_VENCIMENTO': d.get('vencimento', ''),
        'VALOR_DOCUMENTO': fmt_money(d.get('valor', 0)),
        'SACADO_NOME': d.get('pagador_nome', ''),
        'SACADO_CPF_CNPJ': d.get('pagador_cnpj', ''),
        'SACADO_CEP': d.get('pagador_cep', ''),
        'SACADO_CIDADE': d.get('pagador_cidade', ''),
        'SACADO_ESTADO': d.get('pagador_uf', ''),
        'PARCELA': d.get('parcela', ''),
        'INSTRUCOES': d.get('instrucoes', 'NÃO RECEBER APÓS O VENCIMENTO.'),
    }
    fields.update(end)
    return fields


def replace_expr(text: str, fields: dict) -> str:
    out = text or ''
    out = out.replace('[GetConta]', f"{fields['AGENCIA']}-{fields['DIGITO_AGENCIA']}/{fields['CONTA']}-{fields['DIGITO_CONTA']}")
    out = out.replace('[GetNossoNumero]', f"{fields['CARTEIRA']}/{fields['NOSSO_NUMERO']}-{fields['DIGITO_NOSSO_NUMERO']}")
    out = out.replace('[MemoInstrucoes.Lines.Text]', '')

    def repl(m):
        return str(fields.get(m.group(1), ''))

    out = re.sub(r'\[Boleto\."([^"]+)"\]', repl, out)
    return out


def render_from_frx(fields: dict, barcode: str) -> str:
    root = ET.parse(FRX_TEMPLATE).getroot()
    page = root.find('.//TfrxReportPage')
    master = root.find('.//TfrxMasterData')
    width = fr_num(master.attrib.get('Width'), 718.1107)
    height = fr_num(master.attrib.get('Height'), 1025.67718)
    barcode64 = barcode_svg_base64(barcode)

    css = f'''
@page {{ size: A4; margin: {fr_num(page.attrib.get('TopMargin'), 10)}mm {fr_num(page.attrib.get('RightMargin'), 10)}mm {fr_num(page.attrib.get('BottomMargin'), 10)}mm {fr_num(page.attrib.get('LeftMargin'), 10)}mm; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:white; color:#000; }}
.page {{ position:relative; width:{width}px; height:{height}px; overflow:hidden; font-family: Verdana, Arial, sans-serif; }}
.memo {{ position:absolute; white-space:pre-wrap; overflow:hidden; line-height:1.05; padding:0; }}
.line {{ position:absolute; border-color:#000; }}
.logo {{ position:absolute; object-fit:contain; }}
.barcode {{ position:absolute; object-fit:fill; }}
'''
    items: list[str] = []

    for pic in root.findall('.//TfrxPictureView'):
        png64 = png_from_propdata(pic.attrib.get('Picture.PropData', ''))
        if not png64:
            continue
        style = f"left:{fr_num(pic.attrib.get('Left'))}px;top:{fr_num(pic.attrib.get('Top'))}px;width:{fr_num(pic.attrib.get('Width'))}px;height:{fr_num(pic.attrib.get('Height'))}px;"
        items.append(f'<img class="logo" style="{style}" src="data:image/png;base64,{png64}">')

    for line in root.findall('.//TfrxLineView'):
        left, top = fr_num(line.attrib.get('Left')), fr_num(line.attrib.get('Top'))
        w, h = fr_num(line.attrib.get('Width')), fr_num(line.attrib.get('Height'))
        bw = fr_num(line.attrib.get('Frame.Width'), 1)
        style_name = line.attrib.get('Frame.Style')
        border_style = 'dotted' if style_name == 'fsDot' else 'solid'
        if abs(h) < 0.01:
            style = f'left:{left}px;top:{top}px;width:{w}px;height:0;border-top:{bw}px {border_style} #000;'
        elif abs(w) < 0.01:
            style = f'left:{left}px;top:{top}px;width:0;height:{h}px;border-left:{bw}px {border_style} #000;'
        else:
            style = f'left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-top:{bw}px {border_style} #000;'
        items.append(f'<div class="line" style="{style}"></div>')

    for bc in root.findall('.//TfrxBarCodeView'):
        left, top = fr_num(bc.attrib.get('Left')), fr_num(bc.attrib.get('Top'))
        # FastReport expande o Interleaved 2 of 5 conforme conteúdo; Width=64 no XML não representa a largura impressa final.
        # Escala ajustada para ficar mais próximo do boleto oficial impresso.
        style = f'left:{left}px;top:{top}px;width:494px;height:68px;'
        items.append(f'<img class="barcode" style="{style}" src="data:image/svg+xml;base64,{barcode64}">')

    for memo in root.findall('.//TfrxMemoView'):
        text = replace_expr(memo.attrib.get('Text', ''), fields)
        left, top = fr_num(memo.attrib.get('Left')), fr_num(memo.attrib.get('Top'))
        w, h = fr_num(memo.attrib.get('Width')), fr_num(memo.attrib.get('Height'))
        font = memo.attrib.get('Font.Name', 'Verdana')
        size = abs(int(fr_num(memo.attrib.get('Font.Height'), -10)))
        weight = '700' if memo.attrib.get('Font.Style') == '1' else '400'
        align = {'haRight': 'right', 'haCenter': 'center'}.get(memo.attrib.get('HAlign'), 'left')
        valign = memo.attrib.get('VAlign')
        display = 'flex;align-items:center;' if valign == 'vaCenter' else ''
        style = f'left:{left}px;top:{top}px;width:{w}px;height:{h}px;font-family:{font}, Arial, sans-serif;font-size:{size}px;font-weight:{weight};text-align:{align};{display}'
        items.append(f'<div class="memo" style="{style}">{html.escape(text)}</div>')

    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="page">{"".join(items)}</div></body></html>'


def gerar(d: dict, html_out: Path, pdf_out: Path | None = None) -> dict:
    barcode = codigo_barras(d)
    linha = linha_digitavel(barcode)
    fields = boleto_fields(d, barcode, linha)
    rendered = render_from_frx(fields, barcode)
    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(rendered, encoding='utf-8')

    if pdf_out:
        subprocess.check_call(['chromium', '--headless', '--no-sandbox', '--disable-gpu', f'--print-to-pdf={pdf_out}', html_out.resolve().as_uri()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return {
        'html': str(html_out),
        'pdf': str(pdf_out) if pdf_out else None,
        'codigo_barras': barcode,
        'linha_digitavel': linha,
        'nosso_numero_formatado': f"{fields['CARTEIRA']}/{fields['NOSSO_NUMERO']}-{fields['DIGITO_NOSSO_NUMERO']}",
        'layout': str(FRX_TEMPLATE),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--html-output')
    ap.add_argument('--pdf-output')
    args = ap.parse_args()
    d = json.loads(Path(args.input).read_text(encoding='utf-8'))
    html_out = Path(args.html_output or Path(args.pdf_output).with_suffix('.html'))
    meta = gerar(d, html_out, Path(args.pdf_output) if args.pdf_output else None)
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
