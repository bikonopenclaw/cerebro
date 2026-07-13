#!/usr/bin/env python3
"""Monitora ARX Backup e abre tickets NinjaOne quando houver erro real.

Modo padrão é dry-run. Use --create para criar tickets reais.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib import parse, request, error

ROOT = Path('/data/.openclaw/workspace-kowalski/arx-backup')
NINJA_ROOT = Path('/data/.openclaw/workspace-kowalski/ninjaone')
STATE_PATH = ROOT / 'jobs' / 'arx-ninjaone-ticket-state.json'
LOG_PATH = ROOT / 'jobs' / 'arx-ninjaone-ticket-log.jsonl'
CLIENT_MAP_PATH = ROOT / 'config' / 'ninjaone-client-map.json'
TOKEN_PATH = NINJA_ROOT / 'config' / 'oauth-user-context-token.json'
NINJA_ENV = NINJA_ROOT / 'config' / '.env'
DEFAULT_NINJA_CLIENT_ID = 1  # 00 - Bikon Tech. Regra operacional: todo alerta ARX abre aqui para triagem interna.

sys.path.insert(0, str(ROOT / 'scripts'))
from gerar_relatorio_arx import (  # noqa: E402
    coletar,
    flatten_settings,
    status_label,
    classificar,
    recomendacao,
    ts_to_br,
    FONTES,
)


def load_env(path: Path = NINJA_ENV) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(value: str | None) -> str:
    value = value or ''
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()


def only_digits_prefix(value: str) -> str | None:
    m = re.match(r'\s*(\d+)', value or '')
    return m.group(1) if m else None


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    try:
        os.chmod(path, 0o600)
    except PermissionError:
        pass


def append_log(record: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': now_iso(), **record}, ensure_ascii=False) + '\n')


def refresh_user_token() -> dict:
    load_env()
    token = read_json(TOKEN_PATH, {})
    refresh_token = token.get('refresh_token')
    if not refresh_token:
        raise RuntimeError('NinjaOne user-context token sem refresh_token. Refaça OAuth.')
    client_id = os.getenv('NINJAONE_USER_CLIENT_ID')
    client_secret = os.getenv('NINJAONE_USER_CLIENT_SECRET')
    token_url = os.getenv('NINJAONE_TOKEN_URL', 'https://bikon.rmmservice.com/ws/oauth/token')
    if not client_id or not client_secret:
        raise RuntimeError('Faltam NINJAONE_USER_CLIENT_ID/SECRET no .env')
    body = parse.urlencode({
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
    }).encode()
    req = request.Request(token_url, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}, method='POST')
    with request.urlopen(req, timeout=30) as resp:
        new_token = json.loads(resp.read().decode())
    if 'refresh_token' not in new_token:
        new_token['refresh_token'] = refresh_token
    new_token['obtained_at'] = now_iso()
    write_json(TOKEN_PATH, new_token)
    return new_token


def user_token() -> str:
    token = read_json(TOKEN_PATH, {})
    if not token.get('access_token'):
        token = refresh_user_token()
    return token['access_token']


def ninja_request(path: str, method: str = 'GET', payload: dict | None = None, retry: bool = True):
    base = os.getenv('NINJAONE_API_BASE', 'https://bikon.rmmservice.com/v2').rstrip('/')
    token = user_token()
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    if payload is not None:
        headers['Content-Type'] = 'application/json'
    req = request.Request(f'{base}/{path.lstrip("/")}', data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode(errors='replace')
            return json.loads(text) if text else None
    except error.HTTPError as exc:
        body = exc.read().decode(errors='replace')
        if exc.code == 401 and retry:
            refresh_user_token()
            return ninja_request(path, method, payload, retry=False)
        raise RuntimeError(f'NinjaOne HTTP {exc.code} em {method} {path}: {body[:1000]}')


def load_ninja_inventory():
    load_env()
    orgs = ninja_request('organizations') or []
    devices = ninja_request('devices') or []
    org_by_id = {int(o['id']): o for o in orgs if 'id' in o}
    devices_by_org: dict[int, list[dict]] = {}
    for d in devices:
        oid = d.get('organizationId')
        if oid is not None:
            devices_by_org.setdefault(int(oid), []).append(d)
    return orgs, org_by_id, devices_by_org


def match_org(cliente: str, orgs: list[dict], client_map: dict | None = None) -> dict | None:
    client_map = client_map or {}
    aliases = client_map.get('aliases') or {}
    alias_id = aliases.get(cliente)
    if alias_id is not None:
        for o in orgs:
            if int(o.get('id')) == int(alias_id):
                return o
    c_norm = norm(cliente)
    c_prefix = only_digits_prefix(cliente)
    c_tokens = set(c_norm.split())
    weak_tokens = {'cartorio', 'oficio', 'oficios', 'notas', 'ri'}
    c_meaningful = c_tokens - weak_tokens - ({c_prefix} if c_prefix else set())

    best = None
    best_score = 0
    for o in orgs:
        o_name = o.get('name', '')
        o_norm = norm(o_name)
        o_prefix = only_digits_prefix(o_name)
        o_tokens = set(o_norm.split())
        o_meaningful = o_tokens - weak_tokens - ({o_prefix} if o_prefix else set())
        overlap = len(c_meaningful & o_meaningful)
        score = overlap * 3
        if c_norm and (c_norm in o_norm or o_norm in c_norm):
            score += 8
        # Prefix only helps when it is specific, e.g. 4503, or when there is meaningful token overlap.
        if c_prefix and o_prefix == c_prefix and (len(c_prefix) >= 4 or overlap > 0):
            score += 2
        if score > best_score:
            best_score = score
            best = o
    return best if best_score >= 3 else None


def match_device(settings: dict, org: dict | None, devices_by_org: dict[int, list[dict]]) -> dict | None:
    if not org:
        return None
    candidates = devices_by_org.get(int(org['id']), [])
    names = [settings.get('MN'), settings.get('AN'), (settings.get('AN') or '').split('_')[0]]
    nset = [norm(x) for x in names if x]
    for d in candidates:
        d_names = [d.get('systemName'), d.get('dnsName')]
        d_norms = [norm(x.split('.')[0] if isinstance(x, str) else x) for x in d_names if x]
        for a in nset:
            for b in d_norms:
                if a and b and (a == b or a in b or b in a):
                    return d
    return None


def status_code_severity(code: str | None) -> int:
    critical = {'2', '3', '9', '10'}
    attention = {'6', '8'}
    if str(code) in critical:
        return 4
    if str(code) in attention:
        return 3
    return 0


def int_or_zero(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def status_is_completed(code: str | None) -> bool:
    return str(code) == '5'


def current_status_has_issue(code: str | None, errors) -> bool:
    # Historical errors can remain in counters after a later successful run.
    # If the latest status is Completed, treat the backup as recovered.
    if status_is_completed(code):
        return False
    return status_code_severity(code) >= 3 or int_or_zero(errors) > 0


def source_failures(s: dict) -> list[dict]:
    failures = []
    for prefix, nome in FONTES:
        code = str(s.get(prefix + '0', ''))
        err = int_or_zero(s.get(prefix + '7'))
        if current_status_has_issue(code, err):
            failures.append({
                'fonte': nome,
                'status': status_label(code),
                'erros': err,
                'ultimo_sucesso': ts_to_br(s.get(prefix + 'L')),
                'ultima_conclusao': ts_to_br(s.get(prefix + 'O')),
            })
    return failures


def should_ticket(row) -> bool:
    s = flatten_settings(row)
    if current_status_has_issue(s.get('T0'), s.get('T7')):
        return True
    return bool(source_failures(s))


def issue_signature(s: dict, failures: list[dict]) -> str:
    # Stable enough to avoid duplicates for same affected device while issue persists.
    parts = [str(s.get('T0', '')), 'sources=' + ','.join(f['fonte'] for f in failures)]
    return '|'.join(parts)


def ticket_subject(status: str, cliente: str, dispositivo: str) -> str:
    return f'Alerta de ARX Backup - {cliente}'[:250]


def ticket_payload(row, org: dict | None, device: dict | None, failures: list[dict]) -> dict:
    s = flatten_settings(row)
    status = classificar(row)
    cliente = s.get('AR', '-')
    dispositivo = s.get('AN', '-')
    mn = s.get('MN', '-')
    source_lines = '\n'.join(
        f"- {f['fonte']}: {f['status']}, erros={f['erros']}, último sucesso={f['ultimo_sucesso']}, última conclusão={f['ultima_conclusao']}"
        for f in failures
    ) or '- Nenhuma fonte específica retornada, verificar status total.'
    body = f"""Alerta automático ARX Backup.

Cliente ARX: {cliente}
Dispositivo ARX: {dispositivo}
Computador: {mn}
Status operacional: {status}
Status total: {status_label(s.get('T0'))}
Erros totais: {s.get('T7', '0')}
Último backup válido: {ts_to_br(s.get('TL'))}
Última conclusão: {ts_to_br(s.get('TO'))}
Histórico 28 dias (TB): {s.get('TB', '-')}

Fontes com alerta/falha:
{source_lines}

Ação sugerida: {recomendacao(row)}

Deduplicação: este ticket é aberto apenas uma vez por cliente/dispositivo enquanto o problema permanecer ativo.
"""
    severity = 'CRITICAL' if status == 'Crítico' else 'MAJOR'
    priority = 'HIGH' if status == 'Crítico' else 'MEDIUM'
    payload = {
        'subject': ticket_subject(status, cliente, dispositivo),
        'description': {
            'body': body,
            'public': False,
            'timeTracked': 0,
            'htmlBody': '<pre>' + body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + '</pre>',
            'duplicateInIncidents': False,
        },
        'type': 'INCIDENT' if status == 'Crítico' else 'TASK',
        'status': 'NEW',
        'clientId': DEFAULT_NINJA_CLIENT_ID,
        'ticketFormId': 1,
        'severity': severity,
        'priority': priority,
        'tags': ['openclaw', 'arx-backup', 'backup-alerta'],
    }
    return payload


def status_name(ticket: dict | None) -> str:
    status = (ticket or {}).get('status')
    if isinstance(status, dict):
        return str(status.get('name') or '').upper()
    return str(status or '').upper()


def ticket_is_closed(ticket: dict | None) -> bool:
    return status_name(ticket) in {'RESOLVED', 'CLOSED'}


def resolve_ticket(ticket_id: int | str | None) -> dict:
    if not ticket_id:
        raise RuntimeError('Sem ticket_id para fechar no NinjaOne')
    ticket = ninja_request(f'ticketing/ticket/{ticket_id}')
    if ticket_is_closed(ticket):
        return {'ticket_id': ticket_id, 'status': status_name(ticket), 'already_closed': True}

    # NinjaOne Public API exposes PUT /v2/ticketing/ticket/{ticketId} for update.
    # The update endpoint expects a ticket-shaped payload. Keep existing fields and only
    # change status so we do not overwrite assignment, client, priority, severity or tags.
    full_payload = {
        'subject': ticket.get('subject'),
        'clientId': ticket.get('clientId'),
        'ticketFormId': ticket.get('ticketFormId'),
        'type': ticket.get('type'),
        'status': 'RESOLVED',
        'severity': ticket.get('severity'),
        'priority': ticket.get('priority'),
        'tags': ticket.get('tags') or [],
    }
    for optional_key in ('nodeId', 'locationId', 'assignedAppUserId', 'requesterUid', 'followupTime', 'version'):
        if ticket.get(optional_key) is not None:
            full_payload[optional_key] = ticket.get(optional_key)

    attempts = [
        full_payload,
        {'status': 'RESOLVED'},
        {'statusId': 5000},
    ]
    errors = []
    for payload in attempts:
        try:
            ninja_request(f'ticketing/ticket/{ticket_id}', method='PUT', payload=payload)
            updated = ninja_request(f'ticketing/ticket/{ticket_id}')
            return {'ticket_id': ticket_id, 'status': status_name(updated), 'already_closed': False}
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError(f'Nao consegui fechar ticket {ticket_id}: ' + ' | '.join(errors[-2:]))


def recovery_action(cliente: str, dispositivo: str, existing: dict, s: dict, args) -> dict:
    action = {
        'action': 'would_close' if not args.create else 'close',
        'cliente': cliente,
        'dispositivo': dispositivo,
        'ticket_id': existing.get('ticket_id'),
        'status_atual': status_label(s.get('T0')),
        'ultimo_sucesso': ts_to_br(s.get('TL')),
        'ultima_conclusao': ts_to_br(s.get('TO')),
    }
    if args.create:
        close_result = resolve_ticket(existing.get('ticket_id'))
        action.update(close_result)
    return action


def main() -> int:
    parser = argparse.ArgumentParser(description='Monitora ARX Backup e cria tickets NinjaOne com deduplicação')
    parser.add_argument('--create', action='store_true', help='Cria tickets reais. Sem isso, roda em dry-run.')
    parser.add_argument('--include-attention', action='store_true', default=True, help='Inclui Atenção além de Crítico (padrão ligado).')
    parser.add_argument('--reset-state', action='store_true', help='Zera estado de deduplicação antes de rodar.')
    args = parser.parse_args()

    if args.reset_state and STATE_PATH.exists():
        STATE_PATH.unlink()

    state = read_json(STATE_PATH, {'issues': {}})
    issues = state.setdefault('issues', {})

    data = coletar()
    rows = data.get('result', {}).get('result') or []
    # Regra operacional atual: todos os tickets ARX abrem no cliente interno 00 - Bikon Tech.
    # Não tentamos mapear organização/dispositivo final no NinjaOne para evitar chamado no cliente errado.
    summary = {'mode': 'create' if args.create else 'dry-run', 'checked': len(rows), 'issues': 0, 'created': 0, 'deduped': 0, 'resolved': 0, 'closed': 0, 'errors': []}
    active_keys = set()
    actions = []

    for row in rows:
        s = flatten_settings(row)
        cliente = s.get('AR', '-')
        dispositivo = s.get('AN', '-')
        key = norm(cliente + '|' + dispositivo)
        if not key:
            continue
        if not should_ticket(row):
            if key in issues and issues[key].get('active'):
                existing = issues[key]
                try:
                    action = recovery_action(cliente, dispositivo, existing, s, args)
                    if args.create:
                        existing['active'] = False
                        existing['resolved_at'] = now_iso()
                        existing['resolved_status'] = status_label(s.get('T0'))
                        existing['resolved_last_success'] = ts_to_br(s.get('TL'))
                        summary['closed'] += 1
                    summary['resolved'] += 1
                    actions.append(action)
                except Exception as exc:
                    action = {
                        'action': 'close_error',
                        'cliente': cliente,
                        'dispositivo': dispositivo,
                        'ticket_id': existing.get('ticket_id'),
                        'error': str(exc),
                    }
                    summary['errors'].append(action)
                    append_log({'event': 'ticket_close_error', **action})
            continue

        status = classificar(row)
        if status == 'Aviso':
            continue
        failures = source_failures(s)
        sig = issue_signature(s, failures)
        active_keys.add(key)
        summary['issues'] += 1

        existing = issues.get(key)
        if existing and existing.get('active') and existing.get('signature') == sig and existing.get('ticket_id'):
            summary['deduped'] += 1
            actions.append({'action': 'deduped', 'cliente': cliente, 'dispositivo': dispositivo, 'ticket_id': existing.get('ticket_id'), 'status': status})
            if args.create:
                existing['last_seen_at'] = now_iso()
            continue

        org = None
        device = None
        payload = ticket_payload(row, org, device, failures)

        action = {
            'action': 'would_create' if not args.create else 'create',
            'cliente': cliente,
            'dispositivo': dispositivo,
            'status': status,
            'org': '00 - Bikon Tech',
            'clientId': payload.get('clientId'),
            'nodeId': payload.get('nodeId'),
            'subject': payload['subject'],
        }

        if args.create:
            try:
                created = ninja_request('ticketing/ticket', method='POST', payload=payload)
                ticket_id = created.get('id') if isinstance(created, dict) else None
                action['ticket_id'] = ticket_id
                issues[key] = {
                    'active': True,
                    'signature': sig,
                    'ticket_id': ticket_id,
                    'cliente': cliente,
                    'dispositivo': dispositivo,
                    'status': status,
                    'created_at': now_iso(),
                    'last_seen_at': now_iso(),
                    'subject': payload['subject'],
                }
                summary['created'] += 1
            except Exception as exc:
                action['error'] = str(exc)
                summary['errors'].append(action)
                append_log({'event': 'ticket_create_error', **action})
        else:
            # Mark nothing in dry-run.
            pass
        actions.append(action)

    if args.create:
        state['updated_at'] = now_iso()
        write_json(STATE_PATH, state)
    append_log({'event': 'run', 'summary': summary, 'actions': actions})
    print(json.dumps({'summary': summary, 'actions': actions}, ensure_ascii=False, indent=2))
    return 1 if summary['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
