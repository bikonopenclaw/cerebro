#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

DB_DEFAULT = Path('/data/.openclaw/workspace-darth-vader/boletos/db/faturamento.db')
PACOTES_DEFAULT = Path('/data/.openclaw/workspace-darth-vader/boletos/pacotes-emissao')

OCORRENCIAS = {
    '02': 'Entrada confirmada',
    '03': 'Entrada rejeitada',
    '06': 'Liquidação',
    '09': 'Baixa',
    '17': 'Liquidação após baixa ou liquidação de título não registrado',
    '25': 'Protestado e baixado',
    '26': 'Instrução rejeitada',
    '28': 'Débito de tarifas/custas',
}
OCORRENCIAS_PAGAMENTO = {'06', '17'}


def now() -> str:
    return datetime.now().isoformat(timespec='seconds')


def only_digits(v: Any) -> str:
    return re.sub(r'\D+', '', str(v or ''))


def money_to_cents(v: Any) -> int | None:
    if v is None or v == '':
        return None
    if isinstance(v, (int, float)):
        return int(round(float(v) * 100))
    s = str(v).strip()
    if not s:
        return None
    s = s.replace('R$', '').replace(' ', '')
    if ',' in s:
        s = s.replace('.', '').replace(',', '.')
    try:
        return int(round(float(s) * 100))
    except ValueError:
        return None


def cents_to_brl(cents: int | None) -> str:
    if cents is None:
        return '-'
    val = cents / 100
    return f'R$ {val:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def date_br_to_iso(v: Any) -> str | None:
    if not v:
        return None
    s = str(v).strip()
    if re.fullmatch(r'\d{2}/\d{2}/\d{4}', s):
        d, m, y = s.split('/')
        return f'{y}-{m}-{d}'
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return s
    if re.fullmatch(r'\d{6}', s):
        # DDMMAA
        d, m, y = s[:2], s[2:4], s[4:]
        yy = int(y)
        year = 2000 + yy if yy < 80 else 1900 + yy
        return f'{year:04d}-{m}-{d}'
    return s


def cnab_money(line: str, start: int, end: int) -> int:
    raw = line[start-1:end]
    return int(raw.strip() or '0')


def cnab_text(line: str, start: int, end: int) -> str:
    return line[start-1:end].strip()


def cnab_date(line: str, start: int, end: int) -> str | None:
    raw = line[start-1:end]
    if not raw or raw == '000000':
        return None
    return date_br_to_iso(raw)


def connect(db: Path = DB_DEFAULT) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON')
    return con


def init_db(con: sqlite3.Connection) -> None:
    con.executescript('''
    CREATE TABLE IF NOT EXISTS clientes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      documento TEXT UNIQUE,
      nome TEXT,
      email TEXT,
      criado_em TEXT NOT NULL,
      atualizado_em TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS nfse (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente_id INTEGER,
      pacote_path TEXT,
      status TEXT,
      numero TEXT,
      chave TEXT,
      invoice_id TEXT,
      competencia TEXT,
      data_emissao TEXT,
      valor_centavos INTEGER,
      pdf_path TEXT,
      xml_path TEXT,
      payload_path TEXT,
      resultado_path TEXT,
      criado_em TEXT NOT NULL,
      atualizado_em TEXT NOT NULL,
      UNIQUE(numero, chave),
      FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    );

    CREATE TABLE IF NOT EXISTS boletos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente_id INTEGER,
      nfse_id INTEGER,
      pacote_path TEXT,
      status TEXT NOT NULL DEFAULT 'emitido_homologacao',
      banco TEXT,
      carteira TEXT,
      cooperativa TEXT,
      conta TEXT,
      numero_documento TEXT,
      nosso_numero TEXT,
      nosso_numero_formatado TEXT,
      vencimento TEXT,
      valor_original_centavos INTEGER,
      valor_pago_centavos INTEGER,
      juros_mora_centavos INTEGER DEFAULT 0,
      multa_centavos INTEGER DEFAULT 0,
      desconto_centavos INTEGER DEFAULT 0,
      abatimento_centavos INTEGER DEFAULT 0,
      tarifa_centavos INTEGER DEFAULT 0,
      outras_despesas_centavos INTEGER DEFAULT 0,
      outros_creditos_centavos INTEGER DEFAULT 0,
      data_pagamento TEXT,
      data_credito TEXT,
      linha_digitavel TEXT,
      codigo_barras TEXT,
      pdf_path TEXT,
      boleto_input_path TEXT,
      criado_em TEXT NOT NULL,
      atualizado_em TEXT NOT NULL,
      UNIQUE(banco, carteira, cooperativa, conta, nosso_numero),
      FOREIGN KEY(cliente_id) REFERENCES clientes(id),
      FOREIGN KEY(nfse_id) REFERENCES nfse(id)
    );

    CREATE TABLE IF NOT EXISTS remessas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      pacote_path TEXT,
      arquivo_path TEXT UNIQUE,
      layout TEXT,
      banco TEXT,
      seq_remessa TEXT,
      quantidade_titulos INTEGER,
      valor_total_centavos INTEGER,
      status TEXT,
      criado_em TEXT NOT NULL,
      atualizado_em TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS remessa_boletos (
      remessa_id INTEGER NOT NULL,
      boleto_id INTEGER NOT NULL,
      PRIMARY KEY(remessa_id, boleto_id),
      FOREIGN KEY(remessa_id) REFERENCES remessas(id),
      FOREIGN KEY(boleto_id) REFERENCES boletos(id)
    );

    CREATE TABLE IF NOT EXISTS retornos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      arquivo_path TEXT UNIQUE,
      banco TEXT,
      layout TEXT,
      data_arquivo TEXT,
      data_credito TEXT,
      total_detalhes INTEGER,
      total_pagamentos INTEGER,
      total_pago_centavos INTEGER,
      importado_em TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS retorno_ocorrencias (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      retorno_id INTEGER NOT NULL,
      boleto_id INTEGER,
      linha INTEGER,
      ocorrencia_codigo TEXT,
      ocorrencia_descricao TEXT,
      numero_documento TEXT,
      nosso_numero TEXT,
      data_ocorrencia TEXT,
      vencimento TEXT,
      valor_titulo_centavos INTEGER,
      valor_pago_centavos INTEGER,
      juros_mora_centavos INTEGER,
      tarifa_centavos INTEGER,
      outras_despesas_centavos INTEGER,
      abatimento_centavos INTEGER,
      desconto_centavos INTEGER,
      outros_creditos_centavos INTEGER,
      data_credito TEXT,
      conciliado INTEGER NOT NULL DEFAULT 0,
      observacao TEXT,
      criado_em TEXT NOT NULL,
      FOREIGN KEY(retorno_id) REFERENCES retornos(id),
      FOREIGN KEY(boleto_id) REFERENCES boletos(id)
    );
    ''')
    con.commit()


def upsert_cliente(con: sqlite3.Connection, documento: str, nome: str | None, email: str | None = None) -> int:
    doc = only_digits(documento)
    cur = con.execute('SELECT id FROM clientes WHERE documento=?', (doc,)).fetchone()
    ts = now()
    if cur:
        con.execute('UPDATE clientes SET nome=COALESCE(?, nome), email=COALESCE(?, email), atualizado_em=? WHERE id=?', (nome, email, ts, cur['id']))
        return int(cur['id'])
    con.execute('INSERT INTO clientes(documento,nome,email,criado_em,atualizado_em) VALUES(?,?,?,?,?)', (doc, nome, email, ts, ts))
    return int(con.execute('SELECT last_insert_rowid()').fetchone()[0])


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def find_first(pkg: Path, names: list[str]) -> Path | None:
    for name in names:
        p = pkg / name
        if p.exists():
            return p
    return None


def scan_files(pkg: Path) -> dict[str, Path | None]:
    return {
        'job': find_first(pkg, ['job.json']),
        'boleto_input': find_first(pkg, ['boleto-input.json']),
        'resumo_nfse': find_first(pkg, ['resumo-emissao.json']),
        'resultado_boleto': next(pkg.glob('**/resultado-boleto*.json'), None),
        'resultado_remessa': next(pkg.glob('**/resultado-remessa*.json'), None),
        'payload_nfse': next(pkg.glob('**/payload*.json'), None),
        'resultado_nfse': next(pkg.glob('**/resultado-emissao.json'), None),
    }


def register_package(con: sqlite3.Connection, pkg: Path) -> dict:
    init_db(con)
    pkg = pkg.resolve()
    files = scan_files(pkg)
    job = load_json(files['job']) if files['job'] else {}
    boleto_input = load_json(files['boleto_input']) if files['boleto_input'] else {}
    resumo_nfse = load_json(files['resumo_nfse']) if files['resumo_nfse'] else {}
    resultado_boleto = load_json(files['resultado_boleto']) if files['resultado_boleto'] else {}
    resultado_remessa = load_json(files['resultado_remessa']) if files['resultado_remessa'] else {}

    tomador = job.get('tomador') or {}
    nome = tomador.get('nome') or boleto_input.get('pagador_nome') or job.get('cliente_slug') or pkg.name
    documento = tomador.get('cnpj') or tomador.get('cpf') or boleto_input.get('pagador_cnpj') or 'sem-documento-' + pkg.name
    email = None
    if isinstance(job.get('email'), dict):
        tos = job['email'].get('to') or []
        email = ','.join(tos) if isinstance(tos, list) else str(tos)
    cliente_id = upsert_cliente(con, documento, nome, email)

    ts = now()
    nfse_id = None
    nfse = job.get('nfse') or {}
    nfse_num = resumo_nfse.get('nNFSe_xml') or resumo_nfse.get('numero') or nfse.get('numero') or nfse.get('numero_novo')
    nfse_chave = resumo_nfse.get('chNFSe') or nfse.get('chave')
    if nfse_num or nfse_chave or nfse.get('valor_total'):
        valor_nfse = money_to_cents(nfse.get('valor_total') or boleto_input.get('valor'))
        row = con.execute('SELECT id FROM nfse WHERE (numero=? AND COALESCE(chave, "")=COALESCE(?, "")) OR (chave IS NOT NULL AND chave=?)', (nfse_num, nfse_chave, nfse_chave)).fetchone()
        fields = (cliente_id, str(pkg), resumo_nfse.get('status') or nfse.get('status'), nfse_num, nfse_chave, resumo_nfse.get('invoiceId'), resumo_nfse.get('competencia_xml') or nfse.get('competencia'), nfse.get('data_emissao_planejada'), valor_nfse, resumo_nfse.get('pdf') or nfse.get('pdf'), resumo_nfse.get('xml') or nfse.get('xml'), str(files['payload_nfse']) if files['payload_nfse'] else None, str(files['resultado_nfse']) if files['resultado_nfse'] else None, ts)
        if row:
            nfse_id = int(row['id'])
            con.execute('''UPDATE nfse SET cliente_id=?, pacote_path=?, status=?, numero=?, chave=?, invoice_id=?, competencia=?, data_emissao=?, valor_centavos=?, pdf_path=?, xml_path=?, payload_path=?, resultado_path=?, atualizado_em=? WHERE id=?''', (*fields, nfse_id))
        else:
            con.execute('''INSERT INTO nfse(cliente_id,pacote_path,status,numero,chave,invoice_id,competencia,data_emissao,value_centavos,pdf_path,xml_path,payload_path,resultado_path,criado_em,atualizado_em)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''.replace('value_centavos', 'valor_centavos'), (*fields, ts))
            nfse_id = int(con.execute('SELECT last_insert_rowid()').fetchone()[0])

    boleto_id = None
    if boleto_input or resultado_boleto:
        banco = boleto_input.get('banco', '133')
        carteira = boleto_input.get('carteira')
        coop = boleto_input.get('cooperativa')
        conta = boleto_input.get('conta')
        nosso = boleto_input.get('nosso_numero') or re.sub(r'\D+', '', resultado_boleto.get('nosso_numero_formatado', ''))[-11:].lstrip('0')
        row = con.execute('SELECT id FROM boletos WHERE banco=? AND carteira=? AND cooperativa=? AND conta=? AND nosso_numero=?', (banco, carteira, coop, conta, nosso)).fetchone()
        fields = (
            cliente_id, nfse_id, str(pkg), 'emitido_homologacao', banco, carteira, coop, conta,
            boleto_input.get('numero_documento'), nosso, resultado_boleto.get('nosso_numero_formatado'), date_br_to_iso(boleto_input.get('vencimento')),
            money_to_cents(boleto_input.get('valor')), resultado_boleto.get('linha_digitavel'), resultado_boleto.get('codigo_barras'),
            resultado_boleto.get('pdf'), str(files['boleto_input']) if files['boleto_input'] else None, ts
        )
        if row:
            boleto_id = int(row['id'])
            con.execute('''UPDATE boletos SET cliente_id=?, nfse_id=?, pacote_path=?, status=COALESCE(status,?), banco=?, carteira=?, cooperativa=?, conta=?, numero_documento=?, nosso_numero=?, nosso_numero_formatado=?, vencimento=?, valor_original_centavos=?, linha_digitavel=?, codigo_barras=?, pdf_path=?, boleto_input_path=?, atualizado_em=? WHERE id=?''', (*fields, boleto_id))
        else:
            con.execute('''INSERT INTO boletos(cliente_id,nfse_id,pacote_path,status,banco,carteira,cooperativa,conta,numero_documento,nosso_numero,nosso_numero_formatado,vencimento,valor_original_centavos,linha_digitavel,codigo_barras,pdf_path,boleto_input_path,criado_em,atualizado_em)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (*fields, ts))
            boleto_id = int(con.execute('SELECT last_insert_rowid()').fetchone()[0])

    remessa_id = None
    if resultado_remessa:
        arquivo = resultado_remessa.get('arquivo')
        row = con.execute('SELECT id FROM remessas WHERE arquivo_path=?', (arquivo,)).fetchone()
        fields = (str(pkg), arquivo, 'CNAB400', '133', resultado_remessa.get('seq_remessa'), resultado_remessa.get('titulos'), resultado_remessa.get('valor_total_centavos'), 'gerada_homologacao', ts)
        if row:
            remessa_id = int(row['id'])
            con.execute('''UPDATE remessas SET pacote_path=?, arquivo_path=?, layout=?, banco=?, seq_remessa=?, quantidade_titulos=?, valor_total_centavos=?, status=?, atualizado_em=? WHERE id=?''', (*fields, remessa_id))
        else:
            con.execute('''INSERT INTO remessas(pacote_path,arquivo_path,layout,banco,seq_remessa,quantidade_titulos,valor_total_centavos,status,criado_em,atualizado_em) VALUES(?,?,?,?,?,?,?,?,?,?)''', (*fields, ts))
            remessa_id = int(con.execute('SELECT last_insert_rowid()').fetchone()[0])
        if remessa_id and boleto_id:
            con.execute('INSERT OR IGNORE INTO remessa_boletos(remessa_id,boleto_id) VALUES(?,?)', (remessa_id, boleto_id))

    con.commit()
    return {'pacote': str(pkg), 'cliente_id': cliente_id, 'nfse_id': nfse_id, 'boleto_id': boleto_id, 'remessa_id': remessa_id}


def parse_return_file(path: Path) -> tuple[dict, list[dict]]:
    raw_lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    lines = [ln.rstrip('\r\n') for ln in raw_lines if ln.strip()]
    header = {}
    detalhes = []
    for idx, line in enumerate(lines, 1):
        if len(line) < 400:
            line = line.ljust(400)
        tipo = line[0]
        if tipo == '0':
            header = {
                'data_arquivo': cnab_date(line, 95, 100),
                'data_credito': cnab_date(line, 380, 385),
                'banco': cnab_text(line, 77, 79),
            }
        elif tipo == '1':
            occ = cnab_text(line, 109, 110)
            detalhes.append({
                'linha': idx,
                'ocorrencia_codigo': occ,
                'ocorrencia_descricao': OCORRENCIAS.get(occ, 'Ocorrência não mapeada'),
                'nosso_numero': cnab_text(line, 71, 81).lstrip('0') or cnab_text(line, 71, 81),
                'nosso_numero_dv': cnab_text(line, 82, 82),
                'numero_documento': cnab_text(line, 117, 126),
                'data_ocorrencia': cnab_date(line, 111, 116),
                'vencimento': cnab_date(line, 147, 152),
                'valor_titulo_centavos': cnab_money(line, 153, 165),
                'tarifa_centavos': cnab_money(line, 176, 188),
                'outras_despesas_centavos': cnab_money(line, 189, 201),
                'juros_operacao_centavos': cnab_money(line, 202, 214),
                'abatimento_centavos': cnab_money(line, 228, 240),
                'desconto_centavos': cnab_money(line, 241, 253),
                'valor_pago_centavos': cnab_money(line, 254, 266),
                'juros_mora_centavos': cnab_money(line, 267, 279),
                'outros_creditos_centavos': cnab_money(line, 280, 292),
                'data_credito': cnab_date(line, 296, 301),
            })
    return header, detalhes


def find_boleto_for_occ(con: sqlite3.Connection, occ: dict) -> sqlite3.Row | None:
    nosso = str(occ.get('nosso_numero') or '').lstrip('0')
    doc = str(occ.get('numero_documento') or '').strip()
    row = con.execute('SELECT * FROM boletos WHERE nosso_numero=?', (nosso,)).fetchone()
    if row:
        return row
    if doc:
        return con.execute('SELECT * FROM boletos WHERE numero_documento=?', (doc,)).fetchone()
    return None


def import_return(con: sqlite3.Connection, path: Path) -> dict:
    init_db(con)
    path = path.resolve()
    header, detalhes = parse_return_file(path)
    ts = now()
    total_pago = sum(d['valor_pago_centavos'] for d in detalhes if d['ocorrencia_codigo'] in OCORRENCIAS_PAGAMENTO)
    total_pgtos = sum(1 for d in detalhes if d['ocorrencia_codigo'] in OCORRENCIAS_PAGAMENTO)
    row = con.execute('SELECT id FROM retornos WHERE arquivo_path=?', (str(path),)).fetchone()
    if row:
        retorno_id = int(row['id'])
        con.execute('DELETE FROM retorno_ocorrencias WHERE retorno_id=?', (retorno_id,))
        con.execute('''UPDATE retornos SET banco=?, layout=?, data_arquivo=?, data_credito=?, total_detalhes=?, total_pagamentos=?, total_pago_centavos=?, importado_em=? WHERE id=?''', (header.get('banco') or '133', 'CNAB400', header.get('data_arquivo'), header.get('data_credito'), len(detalhes), total_pgtos, total_pago, ts, retorno_id))
    else:
        con.execute('''INSERT INTO retornos(arquivo_path,banco,layout,data_arquivo,data_credito,total_detalhes,total_pagamentos,total_pago_centavos,importado_em) VALUES(?,?,?,?,?,?,?,?,?)''', (str(path), header.get('banco') or '133', 'CNAB400', header.get('data_arquivo'), header.get('data_credito'), len(detalhes), total_pgtos, total_pago, ts))
        retorno_id = int(con.execute('SELECT last_insert_rowid()').fetchone()[0])

    conciliados = 0
    pagamentos = 0
    for d in detalhes:
        boleto = find_boleto_for_occ(con, d)
        boleto_id = int(boleto['id']) if boleto else None
        conciliado = 1 if boleto else 0
        if boleto:
            conciliados += 1
        if boleto and d['ocorrencia_codigo'] in OCORRENCIAS_PAGAMENTO:
            pagamentos += 1
            con.execute('''UPDATE boletos SET status='pago', valor_pago_centavos=?, juros_mora_centavos=?, tarifa_centavos=?, outras_despesas_centavos=?, abatimento_centavos=?, desconto_centavos=?, outros_creditos_centavos=?, data_pagamento=?, data_credito=?, atualizado_em=? WHERE id=?''', (
                d['valor_pago_centavos'],
                d['juros_mora_centavos'] + d['juros_operacao_centavos'],
                d['tarifa_centavos'],
                d['outras_despesas_centavos'],
                d['abatimento_centavos'],
                d['desconto_centavos'],
                d['outros_creditos_centavos'],
                d['data_ocorrencia'],
                d['data_credito'],
                ts,
                boleto_id,
            ))
        elif boleto and d['ocorrencia_codigo'] in {'03', '26'}:
            con.execute('UPDATE boletos SET status=?, atualizado_em=? WHERE id=?', ('rejeitado_retorno', ts, boleto_id))
        elif boleto and d['ocorrencia_codigo'] == '09':
            con.execute('UPDATE boletos SET status=?, atualizado_em=? WHERE id=?', ('baixado_sem_pagamento', ts, boleto_id))

        con.execute('''INSERT INTO retorno_ocorrencias(retorno_id,boleto_id,linha,ocorrencia_codigo,ocorrencia_descricao,numero_documento,nosso_numero,data_ocorrencia,vencimento,valor_titulo_centavos,valor_pago_centavos,juros_mora_centavos,tarifa_centavos,outras_despesas_centavos,abatimento_centavos,desconto_centavos,outros_creditos_centavos,data_credito,conciliado,observacao,criado_em)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
            retorno_id, boleto_id, d['linha'], d['ocorrencia_codigo'], d['ocorrencia_descricao'], d['numero_documento'], d['nosso_numero'], d['data_ocorrencia'], d['vencimento'], d['valor_titulo_centavos'], d['valor_pago_centavos'], d['juros_mora_centavos'] + d['juros_operacao_centavos'], d['tarifa_centavos'], d['outras_despesas_centavos'], d['abatimento_centavos'], d['desconto_centavos'], d['outros_creditos_centavos'], d['data_credito'], conciliado, None if boleto else 'Boleto não encontrado no banco local', ts,
        ))
    con.commit()
    return {'retorno_id': retorno_id, 'arquivo': str(path), 'detalhes': len(detalhes), 'conciliados': conciliados, 'pagamentos_baixados': pagamentos, 'total_pago_centavos': total_pago}


def sync_packages(con: sqlite3.Connection, root: Path) -> list[dict]:
    results = []
    for pkg in sorted(root.iterdir() if root.exists() else []):
        if pkg.is_dir() and any((pkg / f).exists() for f in ['job.json', 'boleto-input.json', 'resumo-emissao.json']):
            try:
                results.append(register_package(con, pkg))
            except Exception as exc:
                results.append({'pacote': str(pkg), 'erro': str(exc)})
    return results


def report(con: sqlite3.Connection, output: str = 'md') -> str:
    init_db(con)
    rows = con.execute('''SELECT b.*, c.nome AS cliente_nome, c.documento AS cliente_documento, n.numero AS nfse_numero
                          FROM boletos b LEFT JOIN clientes c ON c.id=b.cliente_id LEFT JOIN nfse n ON n.id=b.nfse_id
                          ORDER BY COALESCE(b.vencimento,'9999-99-99'), b.id''').fetchall()
    total_original = sum(r['valor_original_centavos'] or 0 for r in rows)
    total_pago = sum(r['valor_pago_centavos'] or 0 for r in rows)
    abertos = [r for r in rows if r['status'] not in ('pago', 'baixado_sem_pagamento')]
    if output == 'csv':
        import io
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(['cliente','documento','nfse','nosso_numero','numero_documento','vencimento','status','valor_original','valor_pago','juros_mora','tarifa','desconto','data_pagamento','data_credito'])
        for r in rows:
            w.writerow([r['cliente_nome'], r['cliente_documento'], r['nfse_numero'], r['nosso_numero'], r['numero_documento'], r['vencimento'], r['status'], cents_to_brl(r['valor_original_centavos']), cents_to_brl(r['valor_pago_centavos']), cents_to_brl(r['juros_mora_centavos']), cents_to_brl(r['tarifa_centavos']), cents_to_brl(r['desconto_centavos']), r['data_pagamento'], r['data_credito']])
        return buf.getvalue()
    lines = [
        '# Relatório de faturamento, NFS-e, boletos e retornos', '',
        f'Gerado em: {now()}', '',
        '## Placar', '',
        f'- Boletos registrados: {len(rows)}',
        f'- Boletos em aberto/pendentes: {len(abertos)}',
        f'- Valor original registrado: {cents_to_brl(total_original)}',
        f'- Valor pago/baixado: {cents_to_brl(total_pago)}', '',
        '## Boletos', '',
        '| Cliente | NFS-e | Nosso número | Documento | Vencimento | Status | Original | Pago | Juros/mora | Data pagamento |',
        '|---|---:|---:|---:|---:|---|---:|---:|---:|---:|',
    ]
    for r in rows:
        lines.append(f"| {r['cliente_nome'] or '-'} | {r['nfse_numero'] or '-'} | {r['nosso_numero'] or '-'} | {r['numero_documento'] or '-'} | {r['vencimento'] or '-'} | {r['status']} | {cents_to_brl(r['valor_original_centavos'])} | {cents_to_brl(r['valor_pago_centavos'])} | {cents_to_brl(r['juros_mora_centavos'])} | {r['data_pagamento'] or '-'} |")
    return '\n'.join(lines) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description='Banco local de faturamento Bikon: NFS-e, boletos, remessas e retornos')
    ap.add_argument('--db', default=str(DB_DEFAULT))
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('init')
    sp = sub.add_parser('registrar-pacote')
    sp.add_argument('--pacote', required=True)
    sp = sub.add_parser('sincronizar-pacotes')
    sp.add_argument('--root', default=str(PACOTES_DEFAULT))
    sp = sub.add_parser('importar-retorno')
    sp.add_argument('--arquivo', required=True)
    sp = sub.add_parser('relatorio')
    sp.add_argument('--formato', choices=['md','csv'], default='md')
    sp.add_argument('--output')
    args = ap.parse_args()

    con = connect(Path(args.db))
    if args.cmd == 'init':
        init_db(con)
        print(json.dumps({'ok': True, 'db': str(Path(args.db))}, ensure_ascii=False, indent=2))
    elif args.cmd == 'registrar-pacote':
        print(json.dumps(register_package(con, Path(args.pacote)), ensure_ascii=False, indent=2))
    elif args.cmd == 'sincronizar-pacotes':
        print(json.dumps(sync_packages(con, Path(args.root)), ensure_ascii=False, indent=2))
    elif args.cmd == 'importar-retorno':
        print(json.dumps(import_return(con, Path(args.arquivo)), ensure_ascii=False, indent=2))
    elif args.cmd == 'relatorio':
        text = report(con, args.formato)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(text, encoding='utf-8')
            print(json.dumps({'ok': True, 'output': args.output}, ensure_ascii=False, indent=2))
        else:
            print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
