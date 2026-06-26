#!/usr/bin/env python3
import argparse, base64, json, os, sys, urllib.parse, urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / 'secrets' / '.env'
DEFAULT_BASE = 'https://api.bikon.tech'

def load_env():
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding='utf-8').splitlines():
            line=line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k,v=line.split('=',1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def token():
    t=os.environ.get('BIKON_API_TOKEN') or os.environ.get('ACCESS_TOKEN')
    if not t:
        raise SystemExit(f'Falta BIKON_API_TOKEN em {ENV_PATH}')
    return t

def base_url():
    return (os.environ.get('BIKON_API_BASE') or DEFAULT_BASE).rstrip('/')

def request(method, path, body=None, query=None):
    url = base_url() + path
    if query:
        clean={k:v for k,v in query.items() if v is not None}
        if clean:
            url += '?' + urllib.parse.urlencode(clean)
    data = None
    headers = {
        'access-token': token(),
        'Accept': 'application/json',
        # Cloudflare da api.bikon.tech bloqueia user-agent padrão do Python.
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
    }
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode('utf-8', errors='replace')
            try:
                parsed=json.loads(raw) if raw else None
            except json.JSONDecodeError:
                parsed=raw
            return {'ok': 200 <= r.status < 300, 'status': r.status, 'data': parsed}
    except urllib.error.HTTPError as e:
        raw=e.read().decode('utf-8', errors='replace')
        try:
            parsed=json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed=raw
        return {'ok': False, 'status': e.code, 'data': parsed}

def print_result(res):
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if not res.get('ok'):
        sys.exit(1)

def cmd_channel(args): print_result(request('GET','/core/v2/api/channel', query={'channelId': args.channel_id}))
def cmd_status(args): print_result(request('GET','/core/v2/api/channel/status', query={'channelId': args.channel_id}))

def cmd_send_text(args):
    body={
        'number': args.number,
        'contactId': args.contact_id,
        'message': args.message,
        'isWhisper': args.whisper,
        'forceSend': args.force_send,
        'verifyContact': args.verify_contact,
        'delayInSeconds': args.delay,
        'linkPreview': args.link_preview,
    }
    print_result(request('POST','/core/v2/api/chats/send-text', body={k:v for k,v in body.items() if v is not None}))

def cmd_send_media(args):
    body={
        'number': args.number,
        'contactId': args.contact_id,
        'forceSend': args.force_send,
        'verifyContact': args.verify_contact,
        'linkUrl': args.link_url,
        'extension': args.extension,
        'fileName': args.file_name,
        'caption': args.caption,
        'delayInSeconds': args.delay,
        'isWhisper': args.whisper,
    }
    if args.file:
        p=Path(args.file)
        body['base64']=base64.b64encode(p.read_bytes()).decode('ascii')
        body['fileName']=body.get('fileName') or p.name
        body['extension']=body.get('extension') or p.suffix.lstrip('.')
    print_result(request('POST','/core/v2/api/chats/send-media', body={k:v for k,v in body.items() if v is not None}))

def cmd_send_template(args):
    components = None
    if args.header_image_url:
        components = [{
            'type': 'header',
            'parameters': [{
                'type': 'image',
                'image': {'link': args.header_image_url}
            }]
        }]
    body={
        'number': args.number,
        'contactId': args.contact_id,
        'templateId': args.template_id,
        'templateComponents': components,
        'forceSend': args.force_send,
        'verifyContact': args.verify_contact,
        'useMmLiteApi': args.use_mm_lite_api,
    }
    print_result(request('POST','/core/v2/api/chats/send-template', body={k:v for k,v in body.items() if v is not None}))


def cmd_create_chat(args):
    body={
        'number': args.number or '',
        'contactId': args.contact_id or '',
        'message': args.message,
        'sectorId': args.sector_id,
        'userId': args.user_id,
        'templateId': args.template_id,
    }
    print_result(request('POST','/core/v2/api/chats/create-new', body={k:v for k,v in body.items() if v is not None}))

def cmd_list_chats(args):
    body={
        'page': args.page,
        'typeChat': args.type_chat,
        'status': args.status,
        'number': args.number,
        'contactId': args.contact_id,
        'sectorId': args.sector_id,
        'userId': args.user_id,
        'protocol': args.protocol,
    }
    print_result(request('POST','/core/v2/api/chats/list', body={k:v for k,v in body.items() if v is not None}))

def cmd_contact_number(args): print_result(request('GET', f'/core/v2/api/contacts/number/{urllib.parse.quote(args.number, safe="")}'))

def cmd_create_contact(args):
    body={'number':args.number, 'nickName':args.name, 'email':args.email, 'observation':args.observation, 'updateIfExists':args.update_if_exists}
    print_result(request('POST','/core/v2/api/contacts', body={k:v for k,v in body.items() if v is not None}))

def main():
    load_env()
    p=argparse.ArgumentParser(description='Client CLI da API WhatsApp Bikon')
    sub=p.add_subparsers(required=True)
    s=sub.add_parser('channel'); s.add_argument('--channel-id'); s.set_defaults(func=cmd_channel)
    s=sub.add_parser('status'); s.add_argument('--channel-id'); s.set_defaults(func=cmd_status)
    s=sub.add_parser('send-text'); s.add_argument('--number'); s.add_argument('--contact-id'); s.add_argument('--message', required=True); s.add_argument('--whisper', action='store_true'); s.add_argument('--force-send', action='store_true', default=False); s.add_argument('--verify-contact', action='store_true', default=False); s.add_argument('--delay', type=int); s.add_argument('--link-preview', action='store_true'); s.set_defaults(func=cmd_send_text)
    s=sub.add_parser('send-media'); s.add_argument('--number'); s.add_argument('--contact-id'); s.add_argument('--file'); s.add_argument('--link-url'); s.add_argument('--extension'); s.add_argument('--file-name'); s.add_argument('--caption'); s.add_argument('--force-send', action='store_true', default=False); s.add_argument('--verify-contact', action='store_true', default=False); s.add_argument('--whisper', action='store_true'); s.add_argument('--delay', type=int); s.set_defaults(func=cmd_send_media)
    s=sub.add_parser('send-template'); s.add_argument('--number'); s.add_argument('--contact-id'); s.add_argument('--template-id', required=True); s.add_argument('--header-image-url'); s.add_argument('--force-send', action='store_true', default=False); s.add_argument('--verify-contact', action='store_true', default=False); s.add_argument('--use-mm-lite-api', action='store_true'); s.set_defaults(func=cmd_send_template)
    s=sub.add_parser('create-chat'); s.add_argument('--number'); s.add_argument('--contact-id'); s.add_argument('--message'); s.add_argument('--sector-id'); s.add_argument('--user-id'); s.add_argument('--template-id'); s.set_defaults(func=cmd_create_chat)
    s=sub.add_parser('list-chats'); s.add_argument('--page', type=int, default=1); s.add_argument('--type-chat', type=int, default=2); s.add_argument('--status', type=int, default=2); s.add_argument('--number'); s.add_argument('--contact-id'); s.add_argument('--sector-id'); s.add_argument('--user-id'); s.add_argument('--protocol'); s.set_defaults(func=cmd_list_chats)
    s=sub.add_parser('contact-number'); s.add_argument('number'); s.set_defaults(func=cmd_contact_number)
    s=sub.add_parser('create-contact'); s.add_argument('--number', required=True); s.add_argument('--name'); s.add_argument('--email'); s.add_argument('--observation'); s.add_argument('--update-if-exists', action='store_true'); s.set_defaults(func=cmd_create_contact)
    args=p.parse_args(); args.func(args)
if __name__ == '__main__': main()
