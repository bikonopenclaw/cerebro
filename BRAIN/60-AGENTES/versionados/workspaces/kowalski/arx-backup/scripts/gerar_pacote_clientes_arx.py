#!/usr/bin/env python3
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace-kowalski/arx-backup')
sys.path.insert(0, str(ROOT / 'scripts'))
from gerar_relatorio_arx import (  # noqa: E402
    coletar,
    flatten_settings,
    ts_to_br,
    fmt_gb,
    status_label,
    classificar,
    recomendacao,
    FONTES,
)

OUT_REL = ROOT / 'relatorios' / 'por-cliente'
OUT_MAIL = ROOT / 'email-rascunhos'
OUT_PACK = ROOT / 'pacotes'
MEDIA_OUT = Path('/data/.openclaw/media/outbound')
APPROVED_TEMPLATE = Path('/data/.openclaw/agents/kowalski/agent/skills/arx-backup/assets/modelos-aprovados/modelo-padrao-relatorio-mensal-arx-backup.html')
APPROVED_LOGO = Path('/data/.openclaw/agents/kowalski/agent/skills/arx-backup/assets/arx-backup-logo-transparent.png')
APPROVED_MODEL_MARKER = 'data-arx-approved-model="modelo-padrao-relatorio-mensal-arx-backup"'

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: Arial, Helvetica, sans-serif; color: #17202a; font-size: 11.5px; line-height: 1.42; }
h1 { color: #0b3d5c; font-size: 22px; margin: 0 0 4px; }
h2 { color: #0b3d5c; font-size: 16px; margin: 18px 0 8px; border-bottom: 1px solid #d9e2ec; padding-bottom: 4px; }
h3 { color: #243b53; font-size: 13px; margin: 14px 0 6px; }
.header { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #0b3d5c; padding-bottom: 10px; margin-bottom: 16px; }
.brand { font-weight: 700; font-size: 15px; color: #0b3d5c; }
.meta { text-align: right; color: #52606d; font-size: 10px; }
.badge { display: inline-block; padding: 5px 10px; border-radius: 999px; font-weight: 700; font-size: 12px; }
.badge.OK { background: #e3fcef; color: #0f7b45; }
.badge.Aviso { background: #fffbea; color: #8a6d1d; }
.badge.Atenção { background: #fff3cd; color: #856404; }
.badge.Crítico { background: #fdecea; color: #b42318; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 12px 0 16px; }
.card { border: 1px solid #d9e2ec; border-radius: 8px; padding: 9px; background: #f8fafc; }
.card .label { color: #52606d; font-size: 9.5px; text-transform: uppercase; }
.card .value { font-size: 13px; font-weight: 700; margin-top: 3px; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 14px; }
th, td { border: 1px solid #d9e2ec; padding: 6px 7px; vertical-align: top; }
th { background: #f1f5f9; color: #243b53; text-align: left; font-size: 10px; }
.footer { margin-top: 18px; padding-top: 8px; border-top: 1px solid #d9e2ec; color: #52606d; font-size: 9.5px; }
.page-break { page-break-after: always; }
.small { color: #52606d; font-size: 10px; }
"""


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9áàâãéêíóôõúçñ]+', '-', s, flags=re.I)
    s = s.strip('-')
    return s[:80] or 'cliente'


def row_to_context(row):
    s = flatten_settings(row)
    cliente = s.get('AR') or f"Cliente {row.get('PartnerId')}"
    dispositivo = s.get('AN') or '-'
    status_bikon = classificar(row)
    return {
        'row': row,
        'settings': s,
        'cliente': cliente,
        'dispositivo': dispositivo,
        'status_bikon': status_bikon,
        'status_cove': status_label(s.get('T0')),
        'erros': s.get('T7', '0'),
        'ultimo_sucesso': ts_to_br(s.get('TL')),
        'ultima_conclusao': ts_to_br(s.get('TO')),
        'historico_28d': s.get('TB', ''),
        'selecionado': fmt_gb(s.get('T3')),
        'processado': fmt_gb(s.get('T4')),
        'recomendacao': recomendacao(row),
    }


def br_date_only(value):
    if not value or value == '-':
        return '-'
    return value.replace(' UTC', ' GMT-3')


def status_mes(ctx):
    if ctx['status_bikon'] == 'OK':
        return 'VERDE', 'todos os dados monitorados no período estão protegidos e recuperáveis dentro da política de retenção apresentada.', 'linear-gradient(135deg,#34c759,#1f9d55)', '#00170b'
    if ctx['status_bikon'] == 'Crítico':
        return 'CRÍTICO', 'há falhas ou atraso relevante que exigem acompanhamento técnico para reduzir risco operacional.', 'linear-gradient(135deg,#ff453a,#b42318)', '#ffffff'
    return 'ATENÇÃO', 'há ponto de acompanhamento operacional no período e o histórico deve ser acompanhado pela equipe técnica.', 'linear-gradient(135deg,#ffd60a,#c88700)', '#201400'


def colorbar_segments(value):
    raw = ''.join(ch for ch in str(value or '') if ch.strip())[:28]
    if not raw:
        raw = '0' * 28
    if len(raw) < 28:
        raw = raw.rjust(28, '0')
    cls_map = {
        '5': 'ok',
        '1': 'warn', '7': 'warn', '8': 'warn', '6': 'warn', '0': 'none',
        '2': 'fail', '3': 'fail', '9': 'fail', 'A': 'fail', 'a': 'fail',
    }
    title_map = {
        '5': 'Concluído', '1': 'Em processo', '2': 'Falhou', '3': 'Abortado',
        '6': 'Interrompido', '7': 'Não iniciado', '8': 'Concluído com erros',
        '9': 'Em progresso com falhas', '0': 'Sem dado', 'A': 'Acima da cota', 'a': 'Acima da cota',
    }
    return ''.join(f'<span class="seg {cls_map.get(ch, "warn")}" title="Dia {i}: {escape(title_map.get(ch, "Status " + ch))}"></span>' for i, ch in enumerate(raw, 1))


def colorbar_summary(value):
    raw = ''.join(ch for ch in str(value or '') if ch.strip())[:28]
    if not raw:
        return 'Histórico diário não retornado pela API.'
    falhas = sum(1 for ch in raw if ch in {'2', '3', '9', 'A', 'a'})
    alertas = sum(1 for ch in raw if ch in {'1', '6', '7', '8', '0'})
    ok = sum(1 for ch in raw if ch == '5')
    return f'Últimos 28 dias: {ok} dia(s) concluído(s), {alertas} dia(s) com alerta/erro parcial e {falhas} dia(s) com falha crítica.'


def fontes_protegidas(ctx):
    s = ctx['settings']
    nomes = []
    for prefix, nome in FONTES:
        if f'{prefix}0' in s or f'{prefix}7' in s or f'{prefix}L' in s:
            nomes.append(nome)
    return '<br>'.join(escape(n) for n in nomes[:4]) or 'Fontes monitoradas'


def replace_once(html, old, new):
    if old not in html:
        return html
    return html.replace(old, new, 1)


def load_approved_template():
    html = APPROVED_TEMPLATE.read_text(encoding='utf-8')
    pattern = r'(<img class="arx" src=")data:image/png;base64,[^"]+("[^>]*>)'
    html, replacements = re.subn(
        pattern,
        lambda match: f'{match.group(1)}{APPROVED_LOGO.as_uri()}{match.group(2)}',
        html,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError('Logo oficial ARX não encontrado no template aprovado.')
    return html


def html_cliente(ctx, gerado):
    """Gera relatório usando o HTML aprovado pelo Hebert como base visual."""
    s = ctx['settings']
    html = load_approved_template()
    status_nome, status_texto, status_bg, status_fg = status_mes(ctx)
    cliente = ctx['cliente']
    dispositivo = ctx['dispositivo']
    computador = s.get('AN', dispositivo).split('_')[0].upper() if s.get('AN') else dispositivo
    emissao = datetime.now(timezone.utc).strftime('%d/%m/%Y')
    ultimo = br_date_only(ctx['ultimo_sucesso'])
    erros = ctx['erros']
    selecionado = ctx['selecionado']
    processado = ctx['processado']
    fontes = fontes_protegidas(ctx)
    falhas_texto = 'Nenhuma falha em aberto no período.' if str(erros) in {'0', '0.0', '-'} else f'{escape(str(erros))} falha(s) registradas para acompanhamento técnico.'
    taxa = '100.0%' if str(erros) in {'0', '0.0', '-'} else 'Em acompanhamento'
    meta_taxa = '≥ 99% ✔' if str(erros) in {'0', '0.0', '-'} else 'Verificar operação'

    replacements = {
        '<title>Relatório Mensal ARX Backup Alzira</title>': f'<title>Relatório Mensal ARX Backup - {escape(cliente)}</title>',
        'Cliente: <b>02 - Cartório Alzira</b> · Período: últimos 28 dias · Emissão: 15/06/2026 · Fuso horário: GMT-3': f'Cliente: <b>{escape(cliente)}</b> · Período: mês de referência · Emissão: {escape(emissao)} · Fuso horário: GMT-3',
        '<div class="status-left">VERDE</div>': f'<div class="status-left" style="background:{escape(status_bg)};color:{escape(status_fg)}">{escape(status_nome)}</div>',
        '<b>Status do mês:</b> todos os dados monitorados no período estão protegidos e recuperáveis dentro da política de retenção apresentada.': f'<b>Status do mês:</b> {escape(status_texto)}',
        '<div class="label">Cliente</div><div class="value">02 - Cartório Alzira</div>': f'<div class="label">Cliente</div><div class="value">{escape(cliente)}</div>',
        '<div class="label">Dispositivo</div><div class="value">02-hv-03_49tpe</div>': f'<div class="label">Dispositivo</div><div class="value">{escape(dispositivo)}</div>',
        '<div class="label">Computador</div><div class="value">02-HV-03</div>': f'<div class="label">Computador</div><div class="value">{escape(computador)}</div>',
        '<div class="label">Último backup válido</div><div class="value">15/06/2026 14:11 GMT-3</div>': f'<div class="label">Último backup válido</div><div class="value">{escape(ultimo)}</div>',
        '<tr><td>Cobertura de proteção</td><td>1 de 1 equipamento monitorado</td><td>100%</td></tr>': '<tr><td>Cobertura de proteção</td><td>1 equipamento monitorado</td><td>Monitorado</td></tr>',
        '<tr><td>Taxa de sucesso dos backups no período</td><td>100.0%</td><td>≥ 99% ✔</td></tr>': f'<tr><td>Taxa de sucesso dos backups no período</td><td>{escape(taxa)}</td><td>{escape(meta_taxa)}</td></tr>',
        '<tr><td>Falhas registradas no período</td><td>0</td><td>0 em aberto</td></tr>': f'<tr><td>Falhas registradas no período</td><td>{escape(str(erros))}</td><td>{escape(falhas_texto)}</td></tr>',
        '<tr><td>Último backup válido</td><td>15/06/2026 14:11 GMT-3</td><td>Atualizado ✔</td></tr>': f'<tr><td>Último backup válido</td><td>{escape(ultimo)}</td><td>Monitorado</td></tr>',
        '<tr><td>Volume total selecionado para proteção</td><td>0,98 TB</td><td>Monitorado</td></tr>': f'<tr><td>Volume total selecionado para proteção</td><td>{escape(selecionado)}</td><td>Monitorado</td></tr>',
        '<tr><td>Armazenamento usado</td><td>1,12 TB</td><td>Monitorado</td></tr>': f'<tr><td>Armazenamento usado</td><td>{escape(processado)}</td><td>Monitorado</td></tr>',
        '<b>Servidor</b>02-HV-03<br><span class="small">Dispositivo: 02-hv-03_49tpe</span>': f'<b>Servidor</b>{escape(computador)}<br><span class="small">Dispositivo: {escape(dispositivo)}</span>',
        '<b>Fontes protegidas</b>Arquivos e Pastas<br>System State': f'<b>Fontes protegidas</b>{fontes}',
        '<li>Os dados do servidor monitorado foram protegidos ao longo do período.</li><li>Não há falhas em aberto no relatório mensal deste cliente.</li><li>A política de retenção de 90 dias está registrada para as fontes apresentadas.</li><li>O histórico disponível para este dispositivo inicia em 27/04/2026 01:26 GMT-3.</li>': f'<li>O ambiente monitorado do cliente {escape(cliente)} foi consolidado neste relatório mensal.</li><li>{escape(falhas_texto)}</li><li>O último backup válido registrado foi {escape(ultimo)}.</li><li>Os volumes monitorados somam {escape(selecionado)} selecionados e {escape(processado)} processados.</li>',
        '<tr><td>Falhas em aberto</td><td>Nenhuma falha em aberto no período.</td></tr>': f'<tr><td>Falhas em aberto</td><td>{escape(falhas_texto)}</td></tr>',
        '<tr><td>Volume de dados</td><td>0,98 TB selecionados e 1,12 TB armazenados.</td></tr>': f'<tr><td>Volume de dados</td><td>{escape(selecionado)} selecionados e {escape(processado)} processados.</td></tr>',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    html = html.replace('.ok { background:#34c759; } .warn { background:#f0b429; }', '.ok { background:#34c759; } .warn { background:#f0b429; } .fail { background:#ff453a; box-shadow:0 0 5px rgba(255,69,58,.45); } .none { background:#69727d; box-shadow:none; opacity:.7; }')
    html = re.sub(r'<div class="bar"><span class="seg ok"></span>.*?</div><div class="note">Cada barra representa um dia do período\. Verde indica rotina concluída\.</div>', f'<div class="bar">{colorbar_segments(ctx["historico_28d"])}</div><div class="note">{escape(colorbar_summary(ctx["historico_28d"]))}</div>', html, flags=re.S)
    html = html.replace('<body>', f'<body {APPROVED_MODEL_MARKER}>', 1)
    html += '\n<!-- ARX_APPROVED_MODEL:modelo-padrao-relatorio-mensal-arx-backup -->\n'
    return html


def md_cliente(ctx, gerado):
    s = ctx['settings']
    lines = [
        f"# Relatório Mensal ARX Backup, {ctx['cliente']}", '',
        f"Gerado em: {gerado}", '',
        f"Status Bikon: {ctx['status_bikon']}",
        f"Status Cove: {ctx['status_cove']}", '',
        '## Resumo executivo', '',
        f"O backup do dispositivo **{ctx['dispositivo']}** está com status **{ctx['status_cove']}**.", '',
        f"**Ação recomendada:** {ctx['recomendacao']}", '',
        '## Indicadores', '',
        f"- Dispositivo: {ctx['dispositivo']}",
        f"- Política/Produto: {s.get('PN','-')}",
        f"- Erros: {ctx['erros']}",
        f"- Último sucesso: {ctx['ultimo_sucesso']}",
        f"- Última conclusão: {ctx['ultima_conclusao']}",
        f"- Dados selecionados: {ctx['selecionado']}",
        f"- Dados processados: {ctx['processado']}", '',
        '## Detalhe por fonte', '',
        '| Fonte | Status | Erros | Último sucesso |', '|---|---:|---:|---:|'
    ]
    any_source = False
    for prefix, nome in FONTES:
        if f'{prefix}0' in s or f'{prefix}7' in s or f'{prefix}L' in s:
            any_source = True
            lines.append(f"| {nome} | {status_label(s.get(prefix+'0'))} | {s.get(prefix+'7','0')} | {ts_to_br(s.get(prefix+'L'))} |")
    if not any_source:
        lines.append('| Nenhuma fonte detalhada retornada | - | - | - |')
    lines += ['', '## Observações', '', '- Relatório mensal no padrão visual ARX Backup.', '- Envio externo depende de aprovação explícita.']
    return '\n'.join(lines) + '\n'


def email_draft(ctx, pdf_name):
    principal = ctx['recomendacao']
    return f"""status: aguardando_aprovacao
cliente: {ctx['cliente']}
anexo: {pdf_name}
assunto: Relatório Mensal ARX Backup - mês/ano

Olá.

Segue o relatório mensal ARX Backup.

Status geral: {ctx['status_bikon']}
Ponto de acompanhamento: {principal}

Qualquer dúvida, estamos à disposição.

ARX Backup
backup@arxcore.com.br
"""


def print_pdf(html_path, pdf_path):
    subprocess.run([
        'chromium', '--headless', '--no-sandbox', '--disable-gpu',
        f'--print-to-pdf={pdf_path}', f'file://{html_path}'
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    OUT_REL.mkdir(parents=True, exist_ok=True)
    OUT_MAIL.mkdir(parents=True, exist_ok=True)
    OUT_PACK.mkdir(parents=True, exist_ok=True)
    MEDIA_OUT.mkdir(parents=True, exist_ok=True)

    data = coletar()
    rows = data.get('result', {}).get('result') or []
    gerado = datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')
    date_tag = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    pdfs = []
    html_parts = []
    for row in sorted(rows, key=lambda r: (flatten_settings(r).get('AR') or '', flatten_settings(r).get('AN') or '')):
        ctx = row_to_context(row)
        slug = slugify(ctx['cliente'])
        base = f"relatorio-arx-{date_tag}-{slug}"
        md_path = OUT_REL / f'{base}.md'
        html_path = OUT_REL / f'{base}.html'
        pdf_path = OUT_REL / f'{base}.pdf'
        email_path = OUT_MAIL / f'email-{date_tag}-{slug}.md'
        md_path.write_text(md_cliente(ctx, gerado))
        html = html_cliente(ctx, gerado)
        html_path.write_text(html)
        print_pdf(html_path, pdf_path)
        email_path.write_text(email_draft(ctx, pdf_path.name))
        pdfs.append(pdf_path)
        html_parts.append(html.replace('</body></html>', '<div class="page-break"></div></body></html>'))

    # PDF consolidado para conferência rápida
    combined_html = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Relatórios ARX Backup por cliente</title><style>' + CSS + '</style></head><body>'
    body_parts = []
    for p in sorted(OUT_REL.glob(f'relatorio-arx-{date_tag}-*.html')):
        txt = p.read_text()
        match = re.search(r'<body[^>]*>(.*)</body>', txt, re.S)
        if not match:
            raise RuntimeError(f'HTML sem body reconhecível: {p}')
        body = match.group(1)
        body_parts.append(body + '<div class="page-break"></div>')
    combined_html += ''.join(body_parts) + '</body></html>'
    combined_html_path = OUT_REL / f'relatorios-arx-por-cliente-{date_tag}.html'
    combined_pdf_path = OUT_REL / f'relatorios-arx-por-cliente-{date_tag}.pdf'
    combined_html_path.write_text(combined_html)
    print_pdf(combined_html_path, combined_pdf_path)

    zip_path = OUT_PACK / f'pacote-arx-backup-clientes-{date_tag}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in pdfs:
            z.write(p, arcname=f'pdfs/{p.name}')
        for p in sorted(OUT_MAIL.glob(f'email-{date_tag}-*.md')):
            z.write(p, arcname=f'emails/{p.name}')
        z.write(combined_pdf_path, arcname=combined_pdf_path.name)

    media_pdf = MEDIA_OUT / combined_pdf_path.name
    media_zip = MEDIA_OUT / zip_path.name
    media_pdf.write_bytes(combined_pdf_path.read_bytes())
    media_zip.write_bytes(zip_path.read_bytes())

    print(json.dumps({
        'clientes': len(rows),
        'pdf_consolidado': str(media_pdf),
        'zip_pacote': str(media_zip),
        'pasta_relatorios': str(OUT_REL),
        'pasta_emails': str(OUT_MAIL),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
