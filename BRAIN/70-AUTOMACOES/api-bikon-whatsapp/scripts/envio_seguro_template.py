#!/usr/bin/env python3
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TEMPLATES = BASE / 'config' / 'templates-aprovados.json'
LOG = BASE / 'logs' / 'envios-template.jsonl'
CLIENT = BASE / 'scripts' / 'bikon_whatsapp_api.py'


def normalizar_numero(n):
    digits = re.sub(r'\D+', '', n or '')
    if len(digits) == 11 and digits.startswith('27'):
        digits = '55' + digits
    if len(digits) == 10 and digits.startswith('27'):
        digits = '55' + digits
    if not digits.startswith('55'):
        raise SystemExit('Número inválido. Use DDD+número ou 55+DDD+número.')
    if len(digits) < 12 or len(digits) > 13:
        raise SystemExit(f'Número inválido após normalização: {digits}')
    return digits


def load_templates():
    return json.loads(TEMPLATES.read_text(encoding='utf-8'))


def append_log(entry):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def main():
    p = argparse.ArgumentParser(description='Rotina segura para envio de templates WhatsApp Bikon')
    p.add_argument('--number', required=True, help='Número destino. Ex: 27993090119 ou 5527993090119')
    p.add_argument('--template', required=True, choices=sorted(load_templates().keys()))
    p.add_argument('--confirm', default='', help='Para enviar de verdade, use exatamente: ENVIAR')
    p.add_argument('--reason', default='', help='Motivo/contexto do envio para auditoria')
    p.add_argument('--force-send', action='store_true', help='Força envio mesmo com atendimento aberto')
    p.add_argument('--verify-contact', action='store_true', help='Pede verificação de contato pela API')
    args = p.parse_args()

    templates = load_templates()
    tpl = templates[args.template]
    number = normalizar_numero(args.number)
    dry_run = args.confirm != 'ENVIAR'

    cmd = [
        str(CLIENT), 'send-template',
        '--number', number,
        '--template-id', tpl['templateId'],
    ]
    if tpl.get('requiresHeaderImage'):
        cmd += ['--header-image-url', tpl['defaultHeaderImageUrl']]
    if args.force_send:
        cmd += ['--force-send']
    if args.verify_contact:
        cmd += ['--verify-contact']

    base_entry = {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'number': number,
        'template': args.template,
        'templateId': tpl['templateId'],
        'language': tpl.get('language'),
        'reason': args.reason,
        'dryRun': dry_run,
        'forceSend': args.force_send,
        'verifyContact': args.verify_contact,
    }

    if dry_run:
        entry = {**base_entry, 'status': 'DRY_RUN', 'message': 'Nada enviado. Use --confirm ENVIAR para disparar.'}
        append_log(entry)
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return

    proc = subprocess.run(cmd, cwd=str(BASE), text=True, capture_output=True)
    try:
        result = json.loads(proc.stdout) if proc.stdout.strip() else None
    except Exception:
        result = {'raw_stdout': proc.stdout[:2000]}
    entry = {**base_entry, 'status': 'SENT' if proc.returncode == 0 else 'ERROR', 'returnCode': proc.returncode, 'result': result}
    if proc.stderr.strip():
        entry['stderr'] = proc.stderr.strip()[:2000]
    append_log(entry)
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    sys.exit(proc.returncode)

if __name__ == '__main__':
    main()
