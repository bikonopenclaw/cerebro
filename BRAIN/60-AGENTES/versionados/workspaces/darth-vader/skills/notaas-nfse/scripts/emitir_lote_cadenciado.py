#!/usr/bin/env python3
from __future__ import annotations

# Local skill path and vendored dependencies
import sys as _sys
from pathlib import Path as _Path
_skill_root = _Path(__file__).resolve().parent.parent
_vendor = _skill_root / 'vendor'
for _p in (_skill_root, _vendor):
    if _p.exists() and str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import dotenv
from core import NotaasClient

DEFAULT_INTERVAL_SECONDS = 60


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_items(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get('items'), list):
        return data['items']
    raise SystemExit('Arquivo deve ser uma lista JSON ou objeto com chave items.')


def public_payload(item: dict) -> dict:
    # Remove metadados locais antes de enviar para a Notaas.
    return {k: v for k, v in item.items() if k not in {'controle_bikon', 'email', '_local'}}


def item_key(item: dict, idx: int) -> str:
    ctrl = item.get('controle_bikon') or {}
    return str(ctrl.get('ordem') or item.get('id') or idx)


def save_state(path: Path, state: dict) -> None:
    state['updated_at'] = now_iso()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def baixar_documentos(client: NotaasClient, invoice_id: str, out_dir: Path, prefix: str) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {'pdf': None, 'xml': None}
    pdf = client.baixar_pdf(invoice_id)
    if pdf:
        p = out_dir / f'{prefix}-nfse-{invoice_id}.pdf'
        p.write_bytes(pdf)
        result['pdf'] = str(p)
    xml = client.baixar_xml(invoice_id)
    if xml:
        p = out_dir / f'{prefix}-nfse-{invoice_id}.xml'
        p.write_bytes(xml)
        result['xml'] = str(p)
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description='Emite lote NFS-e Bikon de forma cadenciada: 1 nota por vez, ciclo mínimo de 60s entre início de uma nota e início da próxima.')
    ap.add_argument('--items', required=True, help='JSON com lista de payloads ou objeto {items:[...]}')
    ap.add_argument('--out-dir', required=True, help='Diretório para resultado e arquivos XML/PDF')
    ap.add_argument('--interval-seconds', type=int, default=DEFAULT_INTERVAL_SECONDS, help='Intervalo mínimo entre uma nota e outra. Padrão Bikon: 60s')
    ap.add_argument('--max-status-polls', type=int, default=30, help='Tentativas de status por nota')
    ap.add_argument('--status-delay', type=int, default=5, help='Segundos entre consultas de status')
    ap.add_argument('--max-document-polls', type=int, default=30, help='Tentativas para baixar PDF+XML antes de ir para próxima nota')
    ap.add_argument('--document-delay', type=int, default=10, help='Segundos entre tentativas de baixar PDF/XML')
    ap.add_argument('--dry-run', '--teste', action='store_true', help='Valida/gera estado sem chamar API')
    ap.add_argument('--confirmar-emissao', action='store_true', help='Obrigatório para emissão real')
    args = ap.parse_args()

    if args.interval_seconds < DEFAULT_INTERVAL_SECONDS and not args.dry_run:
        raise SystemExit(f'Bloqueado: padrão Bikon exige intervalo mínimo de {DEFAULT_INTERVAL_SECONDS}s entre notas.')
    if not args.dry_run and not args.confirmar_emissao:
        raise SystemExit('Bloqueado: emissão real exige --confirmar-emissao. Use --dry-run para simular.')

    dotenv.load_dotenv(_skill_root / '.env')
    items = load_items(Path(args.items))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    files_dir = out_dir / 'nfse-arquivos'
    state_path = out_dir / 'resultado-emissao-cadenciada.json'

    if state_path.exists():
        state = json.loads(state_path.read_text(encoding='utf-8'))
    else:
        state = {'status': 'running', 'started_at': now_iso(), 'items': []}

    done = {str(x.get('key')) for x in state.get('items', []) if (x.get('final') or {}).get('status') == 'issued' and x.get('downloads', {}).get('pdf') and x.get('downloads', {}).get('xml')}
    client = None if args.dry_run else NotaasClient.from_env()

    for idx, item in enumerate(items, 1):
        key = item_key(item, idx)
        prefix = str(key).zfill(2) if str(key).isdigit() else str(idx).zfill(2)
        if key in done:
            print(f'[{prefix}] já concluída, pulando', flush=True)
            continue

        entry = {
            'key': key,
            'index': idx,
            'controle_bikon': item.get('controle_bikon'),
            'started_at': now_iso(),
            'payload_enviado': public_payload(item),
            'emissao': None,
            'polls': [],
            'downloads': {},
            'final': None,
        }
        state['items'] = [x for x in state.get('items', []) if str(x.get('key')) != key]
        state['items'].append(entry)
        save_state(state_path, state)

        if args.dry_run:
            entry['final'] = {'status': 'dry_run'}
            save_state(state_path, state)
            print(f'[{prefix}] dry-run ok', flush=True)
            continue

        cycle_started = time.monotonic()
        print(f'[{prefix}] emitindo nota {idx}/{len(items)}', flush=True)
        res = client.emitir(public_payload(item))
        entry['emissao'] = {'success': res.success, 'invoice_id': res.invoice_id, 'status': res.status, 'error': res.error, 'data': res.data}
        save_state(state_path, state)
        if not res.success:
            entry['final'] = entry['emissao']
            save_state(state_path, state)
            state['status'] = 'partial_error'
            save_state(state_path, state)
            raise SystemExit(f'Erro na emissão do item {key}: {res.error}')

        final = None
        for attempt in range(1, args.max_status_polls + 1):
            time.sleep(args.status_delay)
            st = client.consultar_status(res.invoice_id)
            poll = {'attempt': attempt, 'success': st.success, 'invoice_id': st.invoice_id, 'status': st.status, 'chNFSe': st.chNFSe, 'error': st.error, 'data': st.data}
            entry['polls'].append(poll)
            save_state(state_path, state)
            if st.success and st.status in {'issued', 'error', 'cancelled'}:
                final = poll
                break
        entry['final'] = final or (entry['polls'][-1] if entry['polls'] else entry['emissao'])
        save_state(state_path, state)
        if entry['final'].get('status') != 'issued':
            state['status'] = 'partial_error'
            save_state(state_path, state)
            raise SystemExit(f'Item {key} não ficou issued: {entry["final"]}')

        for attempt in range(1, args.max_document_polls + 1):
            downloads = baixar_documentos(client, res.invoice_id, files_dir, prefix)
            entry['downloads'].update({k: v or entry['downloads'].get(k) for k, v in downloads.items()})
            entry.setdefault('document_polls', []).append({'attempt': attempt, 'pdf': bool(entry['downloads'].get('pdf')), 'xml': bool(entry['downloads'].get('xml')), 'at': now_iso()})
            save_state(state_path, state)
            if entry['downloads'].get('pdf') and entry['downloads'].get('xml'):
                break
            time.sleep(args.document_delay)
        if not (entry['downloads'].get('pdf') and entry['downloads'].get('xml')):
            state['status'] = 'waiting_documents_failed'
            save_state(state_path, state)
            raise SystemExit(f'Item {key} emitido, mas PDF/XML não ficaram prontos dentro do limite. Não avançar para a próxima nota.')

        print(f'[{prefix}] issued + PDF/XML ok', flush=True)
        if idx < len(items):
            elapsed = time.monotonic() - cycle_started
            wait_seconds = max(0, args.interval_seconds - elapsed)
            print(f'[{prefix}] ciclo levou {elapsed:.1f}s; aguardando {wait_seconds:.1f}s para completar janela de {args.interval_seconds}s antes da próxima nota', flush=True)
            if wait_seconds:
                time.sleep(wait_seconds)

    statuses = [x.get('final', {}).get('status') for x in state.get('items', [])]
    state['status'] = 'completed' if len(state.get('items', [])) == len(items) and all(s in {'issued', 'dry_run'} for s in statuses) else 'partial'
    state['finished_at'] = now_iso()
    state['summary'] = {
        'total': len(items),
        'processed': len(state.get('items', [])),
        'issued': sum(1 for s in statuses if s == 'issued'),
        'dry_run': sum(1 for s in statuses if s == 'dry_run'),
        'interval_seconds': args.interval_seconds,
    }
    save_state(state_path, state)
    print(json.dumps(state['summary'], ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
