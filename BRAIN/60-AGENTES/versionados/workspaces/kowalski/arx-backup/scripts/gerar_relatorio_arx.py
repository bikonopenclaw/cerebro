#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-kowalski/arx-backup')
sys.path.insert(0, str(ROOT / 'scripts'))
from arx_client import ArxClient, redact_secrets  # noqa: E402

COLS = [
    'AR', 'AN', 'AL', 'MN', 'PN', 'TS', 'I78',
    'T0', 'T1', 'T3', 'T4', 'T6', 'T7', 'TB', 'TL', 'TQ', 'TJ', 'TO', 'TK',
    'F0', 'F1', 'F3', 'F4', 'F6', 'FL', 'F7', 'FB', 'FJ', 'FO',
    'S0', 'S1', 'S3', 'S4', 'S6', 'SL', 'S7', 'SB', 'SJ', 'SO',
    'Q0', 'Q1', 'Q3', 'Q4', 'Q6', 'QL', 'Q7', 'QB', 'QJ', 'QO',
    'H0', 'H1', 'H3', 'H4', 'H6', 'HL', 'H7', 'HB', 'HJ', 'HO',
    'W0', 'W1', 'W3', 'W4', 'W6', 'WL', 'W7', 'WB', 'WJ', 'WO',
    'AA3135', 'AA3308',
]

STATUS_MAP = {
    '0': 'Indefinido',
    '1': 'Em processo',
    '2': 'Falhou',
    '3': 'Abortado',
    '5': 'Concluído',
    '6': 'Interrompido',
    '7': 'Não iniciado',
    '8': 'Concluído com erros',
    '9': 'Em progresso com falhas',
    '10': 'Acima da cota',
    '11': 'Sem seleção',
    '12': 'Reiniciado',
}

# Legenda oficial Cove: 1 InProcess, 2 Failed, 3 Aborted, 5 Completed,
# 6 Interrupted, 7 NotStarted, 8 CompletedWithErrors, 9 InProgressWithFaults,
# 10 OverQuota, 11 NoSelection, 12 Restarted.
SEVERIDADE = {
    '2': 4,
    '3': 4,
    '9': 4,
    '10': 4,
    '8': 3,
    '6': 3,
    '7': 2,
    '11': 2,
    '1': 1,
    '12': 1,
    '5': 0,
    '0': 1,
}

FONTES = [
    ('F', 'Arquivos e Pastas'),
    ('S', 'System State'),
    ('Q', 'MS SQL'),
    ('H', 'Hyper-V'),
    ('W', 'VMware'),
]


def flatten_settings(row):
    out = {}
    for item in row.get('Settings') or []:
        if isinstance(item, dict):
            out.update(item)
    return out


def ts_to_br(value):
    if not value:
        return '-'
    try:
        n = int(value)
    except (TypeError, ValueError):
        return str(value)
    if n <= 0:
        return '-'
    return datetime.fromtimestamp(n, timezone.utc).strftime('%d/%m/%Y %H:%M UTC')


def fmt_gb(value):
    try:
        n = int(value)
    except (TypeError, ValueError):
        return '-'
    return f'{n / (1024 ** 3):,.1f} GB'.replace(',', 'X').replace('.', ',').replace('X', '.')


def status_label(code):
    if code is None:
        return '-'
    return f"{STATUS_MAP.get(str(code), 'Status desconhecido')} ({code})"


def colorbar_severity(value):
    sev = 0
    for ch in str(value or ''):
        sev = max(sev, SEVERIDADE.get(ch, 1 if ch.strip() else 0))
    return sev


def classificar(row):
    s = flatten_settings(row)
    code = str(s.get('T0', '0'))
    erros = int(s.get('T7') or 0)
    sev = max(SEVERIDADE.get(code, 1), 3 if erros > 0 else 0, colorbar_severity(s.get('TB')))
    for prefix, _nome in FONTES:
        sev = max(sev, SEVERIDADE.get(str(s.get(prefix + '0', '0')), 1), colorbar_severity(s.get(prefix + 'B')))
        try:
            if int(s.get(prefix + '7') or 0) > 0:
                sev = max(sev, 3)
        except ValueError:
            pass
    if sev >= 4:
        return 'Crítico'
    if sev == 3:
        return 'Atenção'
    if sev == 2:
        return 'Aviso'
    return 'OK'


def recomendacao(row):
    s = flatten_settings(row)
    code = str(s.get('T0', '0'))
    erros = int(s.get('T7') or 0)
    if code in {'2', '3', '9', '10'}:
        return 'Verificar falha do backup e abrir tratativa técnica.'
    if code == '8' or erros > 0:
        return 'Validar erros da última sessão e confirmar integridade da próxima execução.'
    if code == '1':
        return 'Acompanhar execução atual até concluir.'
    if code in {'6', '7', '11'}:
        return 'Confirmar agendamento, seleção de dados e próxima execução.'
    return 'Manter monitoramento diário.'


def coletar():
    client = ArxClient()
    login = client.login()
    partner_id = login['result']['result']['PartnerId']
    query = {
        'PartnerId': partner_id,
        'Filter': '',
        'ExcludedPartners': [],
        'SelectionMode': 'Merged',
        'Labels': [],
        'StartRecordNumber': 0,
        'RecordsCount': 500,
        'OrderBy': 'AR ASC, AN ASC',
        'Columns': COLS,
        'Totals': ['T3', 'T4', 'T7'],
    }
    data = client.call('EnumerateAccountStatistics', {'query': query, 'totalStatistics': {}})
    return redact_secrets(data)


def gerar_markdown(rows):
    agora = datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')
    linhas = []
    linhas.append('# Relatório ARX Backup / Cove')
    linhas.append('')
    linhas.append(f'Gerado em: {agora}')
    linhas.append('')
    total = len(rows)
    counts = {'OK': 0, 'Aviso': 0, 'Atenção': 0, 'Crítico': 0}
    for row in rows:
        counts[classificar(row)] += 1
    linhas.append('## Visão geral')
    linhas.append('')
    linhas.append(f'- Contas monitoradas: {total}')
    linhas.append(f'- OK: {counts["OK"]}')
    linhas.append(f'- Aviso: {counts["Aviso"]}')
    linhas.append(f'- Atenção: {counts["Atenção"]}')
    linhas.append(f'- Crítico: {counts["Crítico"]}')
    linhas.append('')
    linhas.append('## Clientes e dispositivos')
    linhas.append('')
    linhas.append('| Cliente | Dispositivo | Status geral | Erros | Último sucesso | Última conclusão | Selecionado | Processado | Recomendação |')
    linhas.append('|---|---|---:|---:|---:|---:|---:|---:|---|')
    for row in sorted(rows, key=lambda r: (flatten_settings(r).get('AR') or '', flatten_settings(r).get('AN') or '')):
        s = flatten_settings(row)
        linhas.append(
            '| {cliente} | {disp} | {status} | {erros} | {ult_sucesso} | {ult_conc} | {sel} | {proc} | {rec} |'.format(
                cliente=s.get('AR', '-'),
                disp=s.get('AN', '-'),
                status=status_label(s.get('T0')),
                erros=s.get('T7', '0'),
                ult_sucesso=ts_to_br(s.get('TL')),
                ult_conc=ts_to_br(s.get('TO')),
                sel=fmt_gb(s.get('T3')),
                proc=fmt_gb(s.get('T4')),
                rec=recomendacao(row),
            )
        )
    linhas.append('')
    linhas.append('## Detalhe por fonte de dados')
    linhas.append('')
    for row in sorted(rows, key=lambda r: (flatten_settings(r).get('AR') or '', flatten_settings(r).get('AN') or '')):
        s = flatten_settings(row)
        linhas.append(f"### {s.get('AR', '-')} / {s.get('AN', '-')}")
        linhas.append('')
        linhas.append('| Fonte | Status | Erros | Último sucesso |')
        linhas.append('|---|---:|---:|---:|')
        any_source = False
        for prefix, nome in FONTES:
            if f'{prefix}0' in s or f'{prefix}7' in s or f'{prefix}L' in s:
                any_source = True
                linhas.append(f"| {nome} | {status_label(s.get(prefix+'0'))} | {s.get(prefix+'7', '0')} | {ts_to_br(s.get(prefix+'L'))} |")
        if not any_source:
            linhas.append('| Nenhuma fonte detalhada retornada | - | - | - |')
        linhas.append('')
    linhas.append('## Observações')
    linhas.append('')
    linhas.append('- Códigos numéricos de status foram preservados entre parênteses para auditoria.')
    linhas.append('- Arquivos de saída não incluem senha, token ou visa da API.')
    linhas.append('- Este relatório é rascunho técnico interno. Envio para cliente externo exige aprovação explícita.')
    linhas.append('')
    return '\n'.join(linhas)


def main():
    data = coletar()
    rows = data.get('result', {}).get('result') or []
    out_json = ROOT / 'dados' / 'account-statistics-sanitized.json'
    out_md = ROOT / 'relatorios' / f"relatorio-arx-backup-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.md"
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    out_md.write_text(gerar_markdown(rows))
    print(out_md)
    print(f'contas={len(rows)}')


if __name__ == '__main__':
    main()
