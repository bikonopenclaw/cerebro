#!/usr/bin/env python3
import json
import os
import sys
from urllib import parse, request, error

CLIENT_ID = os.getenv('NINJAONE_CLIENT_ID')
CLIENT_SECRET = os.getenv('NINJAONE_CLIENT_SECRET')
TOKEN_URL = os.getenv('NINJAONE_TOKEN_URL', 'https://app.ninjaone.com/ws/oauth/token')
API_BASE = os.getenv('NINJAONE_API_BASE', 'https://app.ninjaone.com/v2')
SCOPES = os.getenv('NINJAONE_SCOPES', 'monitoring management')

if not CLIENT_ID or not CLIENT_SECRET:
    print('Faltam NINJAONE_CLIENT_ID e/ou NINJAONE_CLIENT_SECRET no ambiente.', file=sys.stderr)
    sys.exit(2)

body = parse.urlencode({
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': SCOPES,
}).encode()

try:
    req = request.Request(
        TOKEN_URL,
        data=body,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )
    with request.urlopen(req, timeout=30) as resp:
        token_status = resp.status
        token_payload = resp.read().decode()
except error.HTTPError as exc:
    print('token_status=', exc.code)
    print(exc.read().decode()[:1000], file=sys.stderr)
    sys.exit(1)

print('token_status=', token_status)
try:
    token = json.loads(token_payload).get('access_token')
except json.JSONDecodeError:
    print('Resposta de token não é JSON válido.', file=sys.stderr)
    sys.exit(1)

if not token:
    print('Resposta sem access_token.', file=sys.stderr)
    sys.exit(1)

try:
    req = request.Request(
        f'{API_BASE}/organizations',
        headers={'Authorization': f'Bearer {token}'},
        method='GET',
    )
    with request.urlopen(req, timeout=30) as resp:
        org_status = resp.status
        org_payload = resp.read().decode()
except error.HTTPError as exc:
    print('organizations_status=', exc.code)
    print(exc.read().decode()[:1000])
    sys.exit(1)

print('organizations_status=', org_status)
print(org_payload[:1000])
