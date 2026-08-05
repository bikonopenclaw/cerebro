#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from urllib import parse, request, error

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / 'config' / '.env'


def load_env(path=ENV_PATH):
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key, value.strip().strip('"'))


def get_token():
    client_id = os.getenv('NINJAONE_CLIENT_ID')
    client_secret = os.getenv('NINJAONE_CLIENT_SECRET')
    token_url = os.getenv('NINJAONE_TOKEN_URL', 'https://bikon.rmmservice.com/ws/oauth/token')
    scopes = os.getenv('NINJAONE_SCOPES', 'monitoring management')
    if not client_id or not client_secret:
        raise SystemExit('Faltam NINJAONE_CLIENT_ID e/ou NINJAONE_CLIENT_SECRET')
    body = parse.urlencode({
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scopes,
    }).encode()
    req = request.Request(token_url, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'}, method='POST')
    with request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    token = payload.get('access_token')
    if not token:
        raise SystemExit('Resposta sem access_token')
    return token


def api_get(path, token):
    base = os.getenv('NINJAONE_API_BASE', 'https://bikon.rmmservice.com/v2').rstrip('/')
    url = f'{base}/{path.lstrip("/")}'
    req = request.Request(url, headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'}, method='GET')
    with request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode()
    return json.loads(text) if text else None


def main():
    load_env()
    if len(sys.argv) < 2:
        print('Uso: ninjaone_client.py <organizations|organizations-detailed|devices|devices-detailed|alerts|activities|policies>')
        sys.exit(2)
    allowed = {'organizations', 'organizations-detailed', 'devices', 'devices-detailed', 'alerts', 'activities', 'policies'}
    endpoint = sys.argv[1]
    if endpoint not in allowed:
        raise SystemExit(f'Endpoint não permitido neste helper: {endpoint}')
    token = get_token()
    data = api_get(endpoint, token)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except error.HTTPError as exc:
        print(f'HTTP {exc.code}', file=sys.stderr)
        print(exc.read().decode(errors='replace')[:1000], file=sys.stderr)
        sys.exit(1)
