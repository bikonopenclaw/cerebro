#!/usr/bin/env python3

# Local skill path and vendored dependencies
import sys as _sys
from pathlib import Path as _Path
_skill_root = _Path(__file__).resolve().parent.parent
_vendor = _skill_root / 'vendor'
for _p in (_skill_root, _vendor):
    if _p.exists() and str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

"""
Cancelar NFS-e via API Notaas, com guardrail Bikon.

Uso seguro:
    python3 cancelar_nota.py --invoice-id "xxx" --motivo "Justificativa" --dry-run
    python3 cancelar_nota.py --invoice-id "xxx" --motivo "Justificativa" --confirmar-cancelamento --poll --out-dir pacote/cancelamento
"""

import sys
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import dotenv
from core import NotaasClient

# Carrega o .env da skill mesmo quando o script roda fora do diretório da skill.
dotenv.load_dotenv(_skill_root / '.env')


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(description='Cancelar NFS-e')
    parser.add_argument('--invoice-id', required=True, help='Invoice ID da nota')
    parser.add_argument('--motivo', required=True, help='Justificativa do cancelamento, max 255 caracteres')
    parser.add_argument('--poll', action='store_true', help='Aguardar status após cancelamento')
    parser.add_argument('--poll-delay', type=int, default=5, help='Delay entre polls')
    parser.add_argument('--max-polls', type=int, default=60, help='Máximo de polls até cancelled/error')
    parser.add_argument('--out-dir', help='Diretório para salvar resultado e XML de cancelamento')
    parser.add_argument('--dry-run', '--teste', action='store_true', help='Mostra a solicitação, mas NÃO envia para a API')
    parser.add_argument('--confirmar-cancelamento', action='store_true', help='Obrigatório para cancelamento real')
    args = parser.parse_args()

    if len(args.motivo) > 255:
        parser.error('motivo deve ter no máximo 255 caracteres, conforme documentação Notaas')

    out_dir = Path(args.out_dir) if args.out_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        'invoiceId': args.invoice_id,
        'motivo': args.motivo,
    }
    result_doc = {
        'started_at': now_iso(),
        'payload_cancelamento': payload,
        'dry_run': args.dry_run,
        'cancelamento': None,
        'polls': [],
        'xml_cancelamento': None,
    }

    print(f"\n🚫 Solicitação de cancelamento NFS-e: {args.invoice_id}")
    print(f"   Motivo: {args.motivo}")

    if args.dry_run:
        print("\n🧪 DRY-RUN ativo. Nenhuma requisição será enviada para a API.")
        if out_dir:
            (out_dir / 'resultado-cancelamento-dry-run.json').write_text(json.dumps(result_doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return 0

    if not args.confirmar_cancelamento:
        print("\n❌ Bloqueado: cancelamento real exige --confirmar-cancelamento.")
        print("Use --dry-run para simular sem enviar para a API.")
        return 2

    print("\n⚠️ CANCELAMENTO REAL confirmado. Enviando para a API Notaas.")
    client = NotaasClient.from_env()
    result = client.cancelar(args.invoice_id, args.motivo)
    result_doc['cancelamento'] = {
        'success': result.success,
        'invoice_id': result.invoice_id,
        'status': result.status,
        'error': result.error,
        'data': result.data,
    }

    if not result.success:
        if out_dir:
            (out_dir / 'resultado-cancelamento.json').write_text(json.dumps(result_doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print("\n❌ Erro no cancelamento!")
        print(f"   {result.error}")
        return 1

    print("\n✅ Cancelamento solicitado!")
    print(f"   Status: {result.status}")

    final_status = result.status
    if args.poll:
        for attempt in range(1, args.max_polls + 1):
            time.sleep(args.poll_delay)
            status = client.consultar_status(args.invoice_id)
            poll = {
                'attempt': attempt,
                'success': status.success,
                'status': status.status,
                'chNFSe': status.chNFSe,
                'error': status.error,
                'data': status.data,
                'at': now_iso(),
            }
            result_doc['polls'].append(poll)
            final_status = status.status
            print(f"   Poll {attempt}: {status.status}")
            if status.success and status.status in {'cancelled', 'error'}:
                break

    if final_status == 'cancelled':
        xml = client.baixar_xml(args.invoice_id, tipo='cancel')
        if xml and out_dir:
            xml_path = out_dir / f'cancelamento-{args.invoice_id}.xml'
            xml_path.write_bytes(xml)
            result_doc['xml_cancelamento'] = str(xml_path)
            print(f"\n✅ XML de cancelamento salvo: {xml_path}")
        elif out_dir:
            print("\n⚠️ Nota cancelada, mas XML de cancelamento ainda não disponível pela API.")
        print("\n✅ Nota cancelada com sucesso!")
    elif args.poll:
        print(f"\n⚠️ Cancelamento solicitado, mas status final observado: {final_status}")

    if out_dir:
        (out_dir / 'resultado-cancelamento.json').write_text(json.dumps(result_doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return 0 if final_status == 'cancelled' or not args.poll else 1


if __name__ == "__main__":
    sys.exit(main())
