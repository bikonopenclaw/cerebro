#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import csv
import json
import os
import re
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path
from string import Formatter

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / 'config' / 'email.json'
DEFAULT_SECRET_ENV = Path('/data/.openclaw/secrets/email-dreamhost/fatura-bikon.env')
CADASTRO_EMAILS = Path('/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_emails_financeiro.csv')


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('\"', "'"):
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def clean_doc(value: str) -> str:
    return re.sub(r'\D', '', value or '')


def split_emails(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        raw = value
    else:
        raw = re.split(r'[;,\s]+', str(value))
    out = []
    for item in raw:
        email = str(item).strip().strip(',;')
        if email and '@' in email and email not in out:
            out.append(email)
    return out


def lookup_finance_emails(job: dict) -> list[str]:
    tomador = job.get('tomador', {})
    emails = []
    emails += split_emails(tomador.get('email'))
    emails += split_emails(job.get('email', {}).get('to'))
    doc = clean_doc(tomador.get('cnpj') or tomador.get('cpf') or tomador.get('documento') or '')
    if doc and CADASTRO_EMAILS.exists():
        with CADASTRO_EMAILS.open(newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                if clean_doc(row.get('cpf_cnpj', '')) == doc:
                    emails += split_emails(row.get('email'))
    dedup = []
    for email in emails:
        if email not in dedup:
            dedup.append(email)
    return dedup


def first_existing(paths: list[str]) -> str | None:
    for p in paths:
        if p and Path(p).exists():
            return p
    return None


def infer_attachments(job: dict, explicit: list[str]) -> list[str]:
    nfse = job.get('nfse', {})
    boleto = job.get('boleto', {})
    paths = []
    paths += explicit
    paths += [nfse.get('pdf'), nfse.get('xml'), boleto.get('pdf')]
    for doc in nfse.get('documentos', []) or []:
        paths += [doc.get('pdf'), doc.get('xml'), doc.get('boleto_pdf')]
        if isinstance(doc.get('boleto'), dict):
            paths.append(doc['boleto'].get('pdf'))
    out = []
    for item in paths:
        if not item:
            continue
        path = str(Path(item))
        if Path(path).exists() and path not in out:
            out.append(path)
    return out


def format_template(template: str, values: dict) -> str:
    safe = {k: ('' if v is None else v) for k, v in values.items()}
    for _, field, _, _ in Formatter().parse(template):
        if field and field not in safe:
            safe[field] = ''
    return template.format(**safe)


def format_template_html(template: str, values: dict) -> str:
    safe = {k: html.escape('' if v is None else str(v), quote=True) for k, v in values.items()}
    if 'documentos_html' in values:
        safe['documentos_html'] = values.get('documentos_html') or ''
    for _, field, _, _ in Formatter().parse(template):
        if field and field not in safe:
            safe[field] = ''
    return template.format(**safe)


def load_html_template(config: dict) -> str | None:
    rel = config.get('html_template_path')
    if not rel:
        return None
    path = Path(rel)
    if not path.is_absolute():
        path = SKILL_ROOT / path
    if not path.exists():
        raise SystemExit(f'Template HTML não encontrado: {path}')
    return path.read_text(encoding='utf-8')


def parse_brl(value) -> float:
    if value in (None, ''):
        return 0.0
    text = str(value).strip().replace('R$', '').replace(' ', '')
    if ',' in text:
        text = text.replace('.', '').replace(',', '.')
    try:
        return float(text)
    except ValueError:
        return 0.0


def format_brl(value: float) -> str:
    return f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def attachment_kind(path: str) -> str:
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()
    if suffix == '.xml':
        return 'nfse_xml'
    if suffix == '.pdf' and any(token in name for token in ('boleto', 'bol-')):
        return 'boleto_pdf'
    if suffix == '.pdf':
        return 'nfse_pdf'
    return 'outro'


def has_existing_path(value) -> bool:
    return bool(value) and Path(str(value)).exists()


def build_documentos(job: dict) -> tuple[list[dict], str, str]:
    nfse = job.get('nfse', {})
    docs = nfse.get('documentos') or []
    if not docs:
        docs = [{
            'numero': nfse.get('numero') or nfse.get('numero_novo') or 'pendente',
            'chave': nfse.get('chave') or '',
            'valor_total': nfse.get('valor_total') or job.get('boleto', {}).get('valor', ''),
            'boleto_numero': job.get('boleto', {}).get('numero_documento', ''),
            'boleto_vencimento': job.get('boleto', {}).get('vencimento', ''),
        }]
    normalized = []
    for idx, doc in enumerate(docs, 1):
        boleto = doc.get('boleto') if isinstance(doc.get('boleto'), dict) else {}
        normalized.append({
            'idx': idx,
            'numero': doc.get('numero') or doc.get('numero_nfse') or doc.get('numero_novo') or 'pendente',
            'chave': doc.get('chave') or doc.get('chave_nfse') or '',
            'valor_total': doc.get('valor_total') or doc.get('valor') or boleto.get('valor') or '',
            'boleto_numero': doc.get('boleto_numero') or boleto.get('numero_documento') or '',
            'boleto_vencimento': doc.get('boleto_vencimento') or boleto.get('vencimento') or '',
        })
    lines = []
    rows = []
    for doc in normalized:
        boleto_txt = f" | boleto {doc['boleto_numero']} venc. {doc['boleto_vencimento']}" if doc.get('boleto_numero') else ''
        lines.append(f"- NFS-e {doc['numero']} | chave {doc['chave']} | valor R$ {doc['valor_total']}{boleto_txt}")
        rows.append(
            '<tr>'
            f'<td style="padding:12px 14px;border-bottom:1px solid #d7eef1;color:#17202b;font-size:13px;line-height:18px;font-weight:800;">{html.escape(str(doc["numero"]))}</td>'
            f'<td style="padding:12px 14px;border-bottom:1px solid #d7eef1;color:#17202b;font-size:13px;line-height:18px;font-weight:800;">R$ {html.escape(str(doc["valor_total"]))}</td>'
            f'<td style="padding:12px 14px;border-bottom:1px solid #d7eef1;color:#17202b;font-size:12px;line-height:17px;word-break:break-word;">{html.escape(str(doc["chave"]))}</td>'
            f'<td style="padding:12px 14px;border-bottom:1px solid #d7eef1;color:#17202b;font-size:12px;line-height:17px;font-weight:700;">{html.escape(str(doc.get("boleto_numero") or ""))}</td>'
            '</tr>'
        )
    documentos_texto = '\n'.join(lines)
    if len(normalized) <= 1:
        documentos_html = ''
    else:
        documentos_html = (
            '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;border-collapse:separate;border-spacing:0;margin:0 0 22px 0;background:#ffffff;border:1px solid #d7eef1;border-radius:18px;overflow:hidden;">'
            '<tr><td colspan="4" style="padding:15px 18px;background:#0a2830;color:#ffffff;font-size:13px;line-height:18px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;">Documentos deste envio</td></tr>'
            '<tr>'
            '<td style="padding:11px 14px;background:#f5fbfc;border-bottom:1px solid #d7eef1;color:#60737b;font-size:11px;font-weight:800;text-transform:uppercase;">NFS-e</td>'
            '<td style="padding:11px 14px;background:#f5fbfc;border-bottom:1px solid #d7eef1;color:#60737b;font-size:11px;font-weight:800;text-transform:uppercase;">Valor</td>'
            '<td style="padding:11px 14px;background:#f5fbfc;border-bottom:1px solid #d7eef1;color:#60737b;font-size:11px;font-weight:800;text-transform:uppercase;">Chave</td>'
            '<td style="padding:11px 14px;background:#f5fbfc;border-bottom:1px solid #d7eef1;color:#60737b;font-size:11px;font-weight:800;text-transform:uppercase;">Boleto</td>'
            '</tr>' + ''.join(rows) + '</table>'
        )
    return normalized, documentos_texto, documentos_html


def validate_required_attachments(job: dict, attachments: list[str]) -> tuple[list[str], list[str]]:
    """Retorna erros bloqueantes e avisos do checklist de envio externo."""
    errors: list[str] = []
    warnings: list[str] = []
    nfse = job.get('nfse', {})
    boleto = job.get('boleto', {})
    docs = nfse.get('documentos') or []

    if docs:
        for idx, doc in enumerate(docs, 1):
            numero = doc.get('numero') or doc.get('numero_nfse') or doc.get('numero_novo') or f'#{idx}'
            boleto_doc = doc.get('boleto') if isinstance(doc.get('boleto'), dict) else {}
            if not has_existing_path(doc.get('pdf')):
                errors.append(f'NFS-e {numero}: PDF ausente ou caminho inválido.')
            if not has_existing_path(doc.get('xml')):
                errors.append(f'NFS-e {numero}: XML ausente ou caminho inválido.')
            boleto_indicado = bool(doc.get('boleto_pdf') or doc.get('boleto_numero') or boleto_doc.get('numero_documento'))
            if boleto_indicado and not (has_existing_path(doc.get('boleto_pdf')) or has_existing_path(boleto_doc.get('pdf'))):
                errors.append(f'NFS-e {numero}: boleto indicado, mas PDF do boleto ausente ou inválido.')
    else:
        numero = nfse.get('numero') or nfse.get('numero_novo') or 'pendente'
        if not has_existing_path(nfse.get('pdf')) and not any(attachment_kind(p) == 'nfse_pdf' for p in attachments):
            errors.append(f'NFS-e {numero}: PDF ausente ou caminho inválido.')
        if not has_existing_path(nfse.get('xml')) and not any(attachment_kind(p) == 'nfse_xml' for p in attachments):
            errors.append(f'NFS-e {numero}: XML ausente ou caminho inválido.')
        boleto_indicado = bool(boleto.get('pdf') or boleto.get('numero_documento') or boleto.get('nosso_numero'))
        if boleto_indicado and not (has_existing_path(boleto.get('pdf')) or any(attachment_kind(p) == 'boleto_pdf' for p in attachments)):
            errors.append(f'NFS-e {numero}: boleto indicado, mas PDF do boleto ausente ou inválido.')

    kinds = [attachment_kind(p) for p in attachments]
    if 'outro' in kinds:
        warnings.append('Há anexos não classificados como PDF NFS-e, XML ou boleto. Conferir manualmente.')
    return errors, warnings


def build_checklist(job: dict, config: dict, msg: EmailMessage, attachments: list[str], to: list[str], cc: list[str], confirmar_envio: bool) -> dict:
    documentos, _, _ = build_documentos(job)
    total = sum(parse_brl(doc.get('valor_total')) for doc in documentos)
    attachment_errors, warnings = validate_required_attachments(job, attachments)
    approval_required = bool(config.get('approval_required', True))
    approved = bool(job.get('email', {}).get('aprovado_por_hebert'))
    errors = list(attachment_errors)
    if confirmar_envio and approval_required and not approved:
        errors.append('Envio externo exige job.email.aprovado_por_hebert=true.')
    if confirmar_envio and not to:
        errors.append('Envio externo sem destinatário final.')
    if confirmar_envio and not attachments:
        errors.append('Envio externo sem anexos.')
    return {
        'status': 'liberado_para_envio' if confirmar_envio and not errors else ('bloqueado_para_envio' if confirmar_envio else ('rascunho_com_pendencias' if errors else 'rascunho_conferivel')),
        'confirmar_envio_solicitado': confirmar_envio,
        'approval_required': approval_required,
        'aprovado_por_hebert': approved,
        'from': str(msg.get('From', '')),
        'reply_to': str(msg.get('Reply-To', '')),
        'to': to,
        'cc': cc,
        'subject': str(msg.get('Subject', '')),
        'cliente': job.get('tomador', {}).get('nome', ''),
        'documentos': documentos,
        'total_notas': len(documentos),
        'valor_total_calculado': format_brl(total) if total else '',
        'attachments': [{'path': p, 'filename': Path(p).name, 'kind': attachment_kind(p)} for p in attachments],
        'errors': errors,
        'warnings': warnings,
    }


def write_checklist(out_dir: Path, checklist: dict) -> tuple[Path, Path]:
    json_path = out_dir / 'checklist-envio-nfse.json'
    md_path = out_dir / 'checklist-envio-nfse.md'
    json_path.write_text(json.dumps(checklist, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    docs = checklist.get('documentos') or []
    attachments = checklist.get('attachments') or []
    errors = checklist.get('errors') or []
    warnings = checklist.get('warnings') or []
    lines = [
        '# Checklist envio NFS-e',
        '',
        f"Status: {checklist.get('status')}",
        f"Cliente: {checklist.get('cliente') or '-'}",
        f"Remetente: {checklist.get('from') or '-'}",
        f"Reply-to: {checklist.get('reply_to') or '-'}",
        f"Destinatário: {', '.join(checklist.get('to') or []) or '-'}",
        f"Cc: {', '.join(checklist.get('cc') or []) or '-'}",
        f"Assunto: {checklist.get('subject') or '-'}",
        f"Notas: {checklist.get('total_notas')}",
        f"Total calculado: R$ {checklist.get('valor_total_calculado') or '-'}",
        f"Aprovação Hebert: {'sim' if checklist.get('aprovado_por_hebert') else 'não'}",
        '',
        '## Documentos',
        '',
    ]
    lines += [
        f"- NFS-e {doc.get('numero')} | chave {doc.get('chave') or '-'} | valor R$ {doc.get('valor_total') or '-'} | boleto {doc.get('boleto_numero') or '-'}"
        for doc in docs
    ] or ['- Nenhum documento normalizado.']
    lines += ['', '## Anexos', '']
    lines += [f"- [{item.get('kind')}] {item.get('filename')}" for item in attachments] or ['- Nenhum anexo.']
    lines += ['', '## Bloqueios', '']
    lines += [f"- {e}" for e in errors] or ['- Nenhum bloqueio.']
    lines += ['', '## Avisos', '']
    lines += [f"- {w}" for w in warnings] or ['- Nenhum aviso.']
    lines.append('')
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    return json_path, md_path


def build_message(job: dict, config: dict, attachments: list[str], to: list[str], cc: list[str]) -> EmailMessage:
    tomador = job.get('tomador', {})
    nfse = job.get('nfse', {})
    documentos, documentos_texto, documentos_html = build_documentos(job)
    if len(documentos) > 1:
        total = sum(parse_brl(doc.get('valor_total')) for doc in documentos)
        valor_total = format_brl(total)
        numero_nfse = ', '.join(str(doc.get('numero') or 'pendente') for doc in documentos)
        chave_nfse = 'Conforme tabela de documentos abaixo'
    else:
        doc0 = documentos[0] if documentos else {}
        boleto0 = doc0.get('boleto') if isinstance(doc0.get('boleto'), dict) else {}
        valor_total = (
            nfse.get('valor_total')
            or job.get('boleto', {}).get('valor')
            or doc0.get('valor_total')
            or doc0.get('valor')
            or boleto0.get('valor')
            or ''
        )
        numero_nfse = nfse.get('numero') or nfse.get('numero_novo') or doc0.get('numero') or 'pendente'
        chave_nfse = nfse.get('chave') or doc0.get('chave') or ''
    values = {
        'cliente_nome': tomador.get('nome', ''),
        'competencia': nfse.get('competencia', ''),
        'valor_total': valor_total,
        'numero_nfse': numero_nfse,
        'chave_nfse': chave_nfse,
        'documentos_texto': documentos_texto,
        'documentos_html': documentos_html,
        'total_notas': str(len(documentos)),
        'data_envio': datetime.now().strftime('%d/%m/%Y'),
        'ano': datetime.now().strftime('%Y'),
    }
    msg = EmailMessage()
    msg['Message-ID'] = make_msgid(domain='bikon.com.br')
    msg['Date'] = datetime.now().astimezone().strftime('%a, %d %b %Y %H:%M:%S %z')
    msg['From'] = formataddr((config.get('sender_name', 'Bikon Tecnologia'), config.get('from_email', 'administrativo@bikon.com.br')))
    msg['To'] = ', '.join(to)
    if cc:
        msg['Cc'] = ', '.join(cc)
    if config.get('reply_to'):
        msg['Reply-To'] = config['reply_to']
    msg['Subject'] = format_template(config.get('subject_template', 'NFS-e Bikon Tecnologia - {cliente_nome}'), values)
    text_body = format_template(config.get('body_template', ''), values)
    msg.set_content(text_body)
    html_template = load_html_template(config)
    if html_template:
        msg.add_alternative(format_template_html(html_template, values), subtype='html')
    for path in attachments:
        p = Path(path)
        maintype, subtype = ('application', 'octet-stream')
        if p.suffix.lower() == '.pdf':
            subtype = 'pdf'
        elif p.suffix.lower() == '.xml':
            subtype = 'xml'
        msg.add_attachment(p.read_bytes(), maintype=maintype, subtype=subtype, filename=p.name)
    return msg


def send_smtp(msg: EmailMessage):
    load_env_file(DEFAULT_SECRET_ENV)
    host = os.getenv('SMTP_HOST')
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    port = int(os.getenv('SMTP_PORT', '587'))
    security = (os.getenv('SMTP_SECURITY') or '').upper().replace('-', '_').replace('/', '_')
    if not host or not user or not password:
        raise SystemExit('SMTP não configurado: defina SMTP_HOST, SMTP_USER e SMTP_PASSWORD.')
    context = ssl.create_default_context()
    if port == 465 or security in {'SSL', 'TLS', 'SSL_TLS'}:
        with smtplib.SMTP_SSL(host, port, timeout=30, context=context) as server:
            server.login(user, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.starttls(context=context)
            server.login(user, password)
            server.send_message(msg)


def main() -> int:
    ap = argparse.ArgumentParser(description='Prepara e-mail de envio de NFS-e para cliente Bikon')
    ap.add_argument('--job', required=True, help='Job JSON do pacote')
    ap.add_argument('--anexo', action='append', default=[], help='Anexo adicional, repetir se necessário')
    ap.add_argument('--to', action='append', default=[], help='Destinatário manual, repetir se necessário')
    ap.add_argument('--cc', action='append', default=[], help='Cópia manual, repetir se necessário')
    ap.add_argument('--out-dir', help='Diretório de saída do rascunho')
    ap.add_argument('--confirmar-envio', action='store_true', help='Envia por SMTP. Exige autorização explícita e SMTP configurado')
    args = ap.parse_args()

    config = load_json(CONFIG_PATH)
    if not config.get('enabled', True):
        raise SystemExit('Envio de e-mail desabilitado em config/email.json')

    job_path = Path(args.job)
    job = load_json(job_path)
    explicit_to = split_emails(args.to)
    job_to = split_emails(job.get('email', {}).get('to'))
    if explicit_to:
        to = explicit_to
    elif str(job.get('modo', '')).startswith('teste') and job_to:
        # Em teste controlado, nunca buscar cadastro financeiro automaticamente.
        # Evita disparo externo acidental ao usar dados reais de cliente como base.
        to = job_to
    else:
        to = lookup_finance_emails(job)
    cc = split_emails(args.cc) + split_emails(config.get('default_cc'))
    if not to:
        raise SystemExit('Nenhum e-mail financeiro encontrado para o tomador. Corrija cadastro ou use --to.')

    attachments = infer_attachments(job, args.anexo)
    if not attachments:
        raise SystemExit('Nenhum anexo encontrado. Informe --anexo ou preencha nfse.pdf/nfse.xml no job.')

    msg = build_message(job, config, attachments, to, cc)
    out_dir = Path(args.out_dir) if args.out_dir else job_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    eml = out_dir / 'email-nfse-cliente.eml'
    meta = out_dir / 'email-nfse-cliente.json'
    eml.write_bytes(bytes(msg))

    checklist = build_checklist(job, config, msg, attachments, to, cc, args.confirmar_envio)
    checklist_json, checklist_md = write_checklist(out_dir, checklist)

    status = 'rascunho_preparado'
    if args.confirmar_envio:
        if checklist.get('errors'):
            raise SystemExit('Bloqueado pelo checklist de envio externo: ' + '; '.join(checklist['errors']))
        send_smtp(msg)
        status = 'enviado'

    payload = {
        'status': status,
        'to': to,
        'cc': cc,
        'subject': msg['Subject'],
        'eml': str(eml),
        'attachments': attachments,
        'approval_required': config.get('approval_required', True),
        'checklist_json': str(checklist_json),
        'checklist_md': str(checklist_md),
        'checklist_status': checklist.get('status'),
        'checklist_errors': checklist.get('errors'),
        'checklist_warnings': checklist.get('warnings'),
    }
    meta.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
