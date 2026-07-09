#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_SECRET = Path('/data/.openclaw/secrets/cresol-api.env')

ENVIRONMENTS = {
    'homologacao': {
        'api_base': 'https://api-dev.governarti.com.br',
        'auth_url': 'https://auth-dev.governarti.com.br/auth/realms/cresol/protocol/openid-connect/token',
    },
    'producao': {
        'api_base': 'https://cresolapi.governarti.com.br',
        'auth_url': 'https://cresolauth.governarti.com.br/auth/realms/cresol/protocol/openid-connect/token',
    },
}


class CresolApiError(RuntimeError):
    pass


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def env_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise CresolApiError(f'credencial ausente: {name}')
    return value


def request_json_or_bytes(
    method: str,
    url: str,
    *,
    token: str | None = None,
    params: dict[str, Any] | None = None,
    body: Any = None,
    accept: str = 'application/json',
) -> tuple[Any, str]:
    if params:
        clean = {k: v for k, v in params.items() if v not in (None, '')}
        if clean:
            url = f'{url}?{urllib.parse.urlencode(clean)}'

    data = None
    headers = {'Accept': accept}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            content_type = resp.headers.get('content-type', '')
            payload = resp.read()
            if 'application/json' in content_type:
                return json.loads(payload.decode('utf-8')), content_type
            return payload, content_type
    except urllib.error.HTTPError as exc:
        details = exc.read().decode('utf-8', errors='replace')
        raise CresolApiError(f'HTTP {exc.code} em {method} {url}: {details[:500]}') from exc
    except urllib.error.URLError as exc:
        raise CresolApiError(f'falha de rede em {method} {url}: {exc}') from exc


def get_token(auth_url: str) -> str:
    form = {
        'username': env_required('CRESOL_API_USERNAME'),
        'password': env_required('CRESOL_API_PASSWORD'),
        'grant_type': os.environ.get('CRESOL_API_GRANT_TYPE', 'password'),
        'client_id': os.environ.get('CRESOL_API_CLIENT_ID', 'cresolApi'),
        'scope': os.environ.get('CRESOL_API_SCOPE', 'read'),
        'client_secret': env_required('CRESOL_API_CLIENT_SECRET'),
    }
    data = urllib.parse.urlencode(form).encode('utf-8')
    req = urllib.request.Request(
        auth_url,
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode('utf-8', errors='replace')
        raise CresolApiError(f'falha ao autenticar: HTTP {exc.code}: {details[:500]}') from exc
    token = payload.get('access_token')
    if not token:
        raise CresolApiError('resposta de autenticação sem access_token')
    return token


def api_url(base: str, path: str) -> str:
    return base.rstrip('/') + '/' + path.lstrip('/')


def load_payload(path: str | None) -> Any:
    if not path:
        raise CresolApiError('informe --payload para esta operação')
    return json.loads(Path(path).read_text(encoding='utf-8'))


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def write_bytes(path: str, data: bytes) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)


def main() -> int:
    ap = argparse.ArgumentParser(description='Cliente seguro da Cresol API para homologação de boletos')
    ap.add_argument('command', choices=[
        'token-test',
        'parametros-conta',
        'especies',
        'titulos',
        'titulo',
        'baixar-pdf',
        'pagadores',
        'pagador',
        'sequenciais',
        'ocorrencias',
        'criar-titulos',
        'atualizar-titulo',
        'baixar-titulo',
    ])
    ap.add_argument('--env', choices=sorted(ENVIRONMENTS), default='homologacao')
    ap.add_argument('--secret-file', default=str(DEFAULT_SECRET))
    ap.add_argument('--api-base')
    ap.add_argument('--auth-url')
    ap.add_argument('--allow-producao', action='store_true')
    ap.add_argument('--allow-write', action='store_true')
    ap.add_argument('--id')
    ap.add_argument('--status')
    ap.add_argument('--page')
    ap.add_argument('--size')
    ap.add_argument('--nome')
    ap.add_argument('--date-start')
    ap.add_argument('--date-end')
    ap.add_argument('--sequencial')
    ap.add_argument('--payload')
    ap.add_argument('--output')
    args = ap.parse_args()

    if args.env == 'producao' and not args.allow_producao:
        raise SystemExit('produção bloqueada: use --allow-producao somente com autorização explícita do Hebert')

    write_commands = {'criar-titulos', 'atualizar-titulo'}
    if args.command in write_commands and not args.allow_write:
        raise SystemExit(f'{args.command} bloqueado: use --allow-write somente em homologação/controlado')
    if args.command == 'baixar-titulo':
        raise SystemExit('baixa via API bloqueada nesta fase')

    load_env(Path(args.secret_file))
    env = ENVIRONMENTS[args.env]
    base = args.api_base or env['api_base']
    auth_url = args.auth_url or env['auth_url']

    try:
        token = get_token(auth_url)
        if args.command == 'token-test':
            print_json({'status': 'ok', 'env': args.env, 'api_base': base, 'token_obtido': True})
            return 0

        if args.command == 'parametros-conta':
            data, _ = request_json_or_bytes('GET', api_url(base, '/parametros-conta'), token=token)
            print_json(data)
            return 0
        if args.command == 'especies':
            data, _ = request_json_or_bytes('GET', api_url(base, '/especies'), token=token)
            print_json(data)
            return 0
        if args.command == 'titulos':
            data, _ = request_json_or_bytes('GET', api_url(base, '/titulos'), token=token, params={
                'page': args.page,
                'size': args.size,
                'status': args.status,
            })
            print_json(data)
            return 0
        if args.command == 'titulo':
            if not args.id:
                raise CresolApiError('informe --id')
            data, _ = request_json_or_bytes('GET', api_url(base, f'/titulos/{args.id}'), token=token)
            print_json(data)
            return 0
        if args.command == 'baixar-pdf':
            if not args.id:
                raise CresolApiError('informe --id')
            if not args.output:
                raise CresolApiError('informe --output')
            data, content_type = request_json_or_bytes('GET', api_url(base, f'/titulos/pdf/{args.id}'), token=token, accept='application/pdf')
            if isinstance(data, bytes):
                write_bytes(args.output, data)
                print_json({'status': 'ok', 'output': args.output, 'content_type': content_type, 'bytes': len(data)})
            else:
                print_json(data)
            return 0
        if args.command == 'pagadores':
            data, _ = request_json_or_bytes('GET', api_url(base, '/pagadores'), token=token, params={
                'page': args.page,
                'size': args.size,
                'nomePagador': args.nome,
            })
            print_json(data)
            return 0
        if args.command == 'pagador':
            if not args.id:
                raise CresolApiError('informe --id')
            data, _ = request_json_or_bytes('GET', api_url(base, f'/pagadores/{args.id}'), token=token)
            print_json(data)
            return 0
        if args.command == 'sequenciais':
            data, _ = request_json_or_bytes('GET', api_url(base, '/ocorrencias/sequenciais'), token=token, params={
                'dateStart': args.date_start,
                'dateEnd': args.date_end,
            })
            print_json(data)
            return 0
        if args.command == 'ocorrencias':
            if not args.sequencial:
                raise CresolApiError('informe --sequencial')
            data, _ = request_json_or_bytes('GET', api_url(base, f'/ocorrencias/{args.sequencial}'), token=token)
            print_json(data)
            return 0
        if args.command == 'criar-titulos':
            payload = load_payload(args.payload)
            data, _ = request_json_or_bytes('POST', api_url(base, '/titulos'), token=token, body=payload)
            print_json(data)
            return 0
        if args.command == 'atualizar-titulo':
            if not args.id:
                raise CresolApiError('informe --id')
            payload = load_payload(args.payload)
            data, _ = request_json_or_bytes('PUT', api_url(base, f'/titulos/{args.id}'), token=token, body=payload)
            print_json(data)
            return 0

        raise CresolApiError(f'comando não tratado: {args.command}')
    except CresolApiError as exc:
        print(json.dumps({'status': 'erro', 'erro': str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
