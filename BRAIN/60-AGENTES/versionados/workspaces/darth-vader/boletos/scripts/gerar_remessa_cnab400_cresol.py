#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-darth-vader/boletos')
OUT_DIR = ROOT / 'remessas' / 'homologacao'


def ascii_upper(s: str) -> str:
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^A-Za-z0-9 /.,&-]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().upper()


def a(value: str, size: int) -> str:
    return ascii_upper(value)[:size].ljust(size)


def n(value, size: int) -> str:
    return re.sub(r'\D', '', str(value))[-size:].zfill(size)


def money_centavos(value: str | int) -> int:
    if isinstance(value, int):
        return value
    clean = str(value).strip().replace('R$', '').replace('.', '').replace(',', '.')
    return int(round(float(clean) * 100))


def ddmmaa(date_br: str) -> str:
    if re.match(r'^\d{6}$', date_br):
        return date_br
    dt = datetime.strptime(date_br, '%d/%m/%Y')
    return dt.strftime('%d%m%y')


def dv_nosso_numero(nosso: int | str, carteira: str = '09') -> str:
    base = n(carteira, 2) + n(nosso, 11)
    weights = [2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(base, weights))
    resto = total % 11
    if resto == 0:
        return '0'
    if resto == 1:
        return 'P'
    return str(11 - resto)


def set_field(line: list[str], start: int, end: int, value: str) -> None:
    # start/end are 1-based inclusive.
    value = str(value)
    size = end - start + 1
    if len(value) != size:
        raise ValueError(f'Campo {start}-{end} esperava {size}, recebeu {len(value)}: {value!r}')
    line[start - 1:end] = list(value)


def header(data_gravacao: str, seq_remessa: str) -> str:
    line = list(' ' * 400)
    set_field(line, 1, 1, '0')
    set_field(line, 2, 2, '1')
    set_field(line, 3, 9, 'REMESSA')
    set_field(line, 10, 11, '01')
    set_field(line, 12, 26, 'COBRANCA'.ljust(15))
    set_field(line, 27, 46, '00000000000000027846')
    set_field(line, 47, 76, a('BIKON TECNOLOGIA DA INFORMACAO', 30))
    set_field(line, 77, 79, '133')
    set_field(line, 80, 94, 'CRESOL'.ljust(15))
    set_field(line, 95, 100, ddmmaa(data_gravacao))
    set_field(line, 111, 117, n(seq_remessa, 7))
    set_field(line, 395, 400, '000001')
    return ''.join(line)


def detalhe(d: dict, seq_registro: int) -> str:
    line = list(' ' * 400)
    valor = money_centavos(d['valor'])
    mora = d.get('juros_mora_dia_centavos')
    if mora is None:
        # Padrão Bikon: juros de mora de 1% ao mês, proporcional ao dia.
        # Fórmula: valor * 0,01 / 30 = valor / 3000, arredondado em centavos.
        mora = round(valor / 3000)
    nosso = int(d['nosso_numero'])
    set_field(line, 1, 1, '1')
    set_field(line, 21, 37, '00090100800278467')
    set_field(line, 38, 62, a(d['numero_documento'], 25))
    set_field(line, 66, 66, '2')
    set_field(line, 67, 70, '0200')
    set_field(line, 71, 81, n(nosso, 11))
    set_field(line, 82, 82, dv_nosso_numero(nosso))
    set_field(line, 93, 93, '2')
    # Posição 106 vem como '2' nos golden files reais Cresol da Bikon.
    set_field(line, 106, 106, '2')
    set_field(line, 109, 110, '01')
    set_field(line, 111, 120, a(d['numero_documento'], 10))
    set_field(line, 121, 126, ddmmaa(d['vencimento']))
    set_field(line, 127, 139, n(valor, 13))
    set_field(line, 148, 149, '02')
    set_field(line, 151, 156, ddmmaa(d['data_emissao']))
    set_field(line, 161, 173, n(mora, 13))
    set_field(line, 174, 179, '000000')
    set_field(line, 180, 192, '0000000000000')
    set_field(line, 193, 205, '0000000000000')
    set_field(line, 206, 218, '0000000000000')
    pagador_doc = re.sub(r'\D', '', str(d['pagador_cnpj']))
    # Tipo de inscrição do pagador: 01 = CPF, 02 = CNPJ.
    # O campo número tem 14 posições; CPF vai alinhado à direita com zeros à esquerda.
    tipo_inscricao = '01' if len(pagador_doc) == 11 else '02'
    set_field(line, 219, 220, tipo_inscricao)
    set_field(line, 221, 234, n(pagador_doc, 14))
    set_field(line, 235, 274, a(d['pagador_nome'], 40))
    set_field(line, 275, 314, a(d['pagador_endereco'], 40))
    set_field(line, 315, 326, a(d.get('pagador_bairro', ''), 12))
    set_field(line, 327, 334, n(d['pagador_cep'], 8))
    set_field(line, 335, 349, a(d.get('pagador_cidade', ''), 15))
    set_field(line, 350, 351, a(d.get('pagador_uf', ''), 2))
    set_field(line, 395, 400, n(seq_registro, 6))
    return ''.join(line)


def trailer(seq_final: int) -> str:
    line = list(' ' * 400)
    set_field(line, 1, 1, '9')
    set_field(line, 395, 400, n(seq_final, 6))
    return ''.join(line)


def validar(lines: list[str]) -> list[str]:
    erros = []
    if len(lines) < 3:
        erros.append('Arquivo precisa ter header, detalhe e trailer')
    for i, line in enumerate(lines, 1):
        if len(line) != 400:
            erros.append(f'Linha {i} tem {len(line)} caracteres, esperado 400')
    if lines and lines[0][0] != '0': erros.append('Header não começa com 0')
    if len(lines) > 1 and not all(l[0] == '1' for l in lines[1:-1]): erros.append('Detalhes não começam com 1')
    if lines and lines[-1][0] != '9': erros.append('Trailer não começa com 9')
    return erros


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output')
    args = p.parse_args()
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    seq_remessa = data['seq_remessa']
    lines = [header(data['data_gravacao'], seq_remessa)]
    for idx, titulo in enumerate(data['titulos'], 2):
        lines.append(detalhe(titulo, idx))
    lines.append(trailer(len(lines) + 1))
    erros = validar(lines)
    if erros:
        raise SystemExit('\n'.join(erros))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.output) if args.output else OUT_DIR / f"cb{datetime.now().strftime('%d%m%H%M')}-homologacao.rem"
    out.write_bytes(('\r\n'.join(lines) + '\r\n').encode('latin1'))
    meta = {
        'arquivo': str(out),
        'linhas': len(lines),
        'tamanho_linhas': [len(x) for x in lines],
        'seq_remessa': seq_remessa,
        'titulos': len(data['titulos']),
        'valor_total_centavos': sum(money_centavos(t['valor']) for t in data['titulos']),
        'erros_validacao': erros,
    }
    print(json.dumps(meta, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
