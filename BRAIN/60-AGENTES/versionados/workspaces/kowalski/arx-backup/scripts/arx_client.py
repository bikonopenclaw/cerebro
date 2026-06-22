#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from urllib import request, error

ROOT = Path('/data/.openclaw/workspace-kowalski/arx-backup')
ENV_PATH = ROOT / 'config' / '.env'


def load_env(path=ENV_PATH):
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k, v.strip().strip('"'))


class ArxClient:
    def __init__(self):
        load_env()
        self.url = os.getenv('ARX_BACKUP_JSONRPC_URL', 'https://api.backup.management/jsonapi')
        self.visa = None
        self._id = 0

    def call(self, method, params=None, visa=True):
        self._id += 1
        payload = {
            'jsonrpc': '2.0',
            'id': str(self._id),
            'method': method,
            'params': params or {},
        }
        if visa and self.visa:
            payload['visa'] = self.visa
        body = json.dumps(payload).encode()
        req = request.Request(
            self.url,
            data=body,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            method='POST',
        )
        with request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        if 'visa' in data:
            self.visa = data['visa']
        if data.get('error'):
            raise RuntimeError(json.dumps(data['error'], ensure_ascii=False))
        return data

    def login(self):
        partner = os.getenv('ARX_BACKUP_PARTNER')
        username = os.getenv('ARX_BACKUP_USERNAME')
        password = os.getenv('ARX_BACKUP_PASSWORD') or os.getenv('ARX_BACKUP_TOKEN')
        missing = [k for k, v in {'ARX_BACKUP_PARTNER': partner, 'ARX_BACKUP_USERNAME': username, 'ARX_BACKUP_PASSWORD/TOKEN': password}.items() if not v]
        if missing:
            raise SystemExit('Faltam credenciais: ' + ', '.join(missing))
        return self.call('Login', {'partner': partner, 'username': username, 'password': password}, visa=False)

    def get_partner_info(self):
        return self.call('GetPartnerInfo', {})

    def enumerate_accounts(self, partner_id):
        return self.call('EnumerateAccounts', {'partnerId': int(partner_id)})


def redact_secrets(obj):
    if isinstance(obj, dict):
        return {k: ('<redacted>' if k.lower() in {'password', 'token', 'visa'} else redact_secrets(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_secrets(v) for v in obj]
    return obj


def main():
    client = ArxClient()
    if len(sys.argv) < 2:
        print('Uso: arx_client.py login|get-partner-info|enumerate-accounts <partnerId>')
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == 'login':
        data = client.login()
    elif cmd == 'get-partner-info':
        client.login()
        data = client.get_partner_info()
    elif cmd == 'enumerate-accounts':
        if len(sys.argv) < 3:
            raise SystemExit('Informe partnerId')
        client.login()
        data = client.enumerate_accounts(sys.argv[2])
    else:
        raise SystemExit('Comando inválido')
    # Reduz risco de vazar visa, token ou senha de agentes na saída padrão.
    data = redact_secrets(data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except error.HTTPError as exc:
        print(f'HTTP {exc.code}', file=sys.stderr)
        print(exc.read().decode(errors='replace')[:1000], file=sys.stderr)
        sys.exit(1)
