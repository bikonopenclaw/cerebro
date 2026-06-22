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
Cancelar NFS-e via API Notaas

Uso:
    python3 cancelar_nota.py --invoice-id "xxx" --motivo "Justificativa"
"""

import sys
import argparse
import dotenv
from core import NotaasClient

dotenv.load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='Cancelar NFS-e')
    parser.add_argument('--invoice-id', required=True, help='Invoice ID da nota')
    parser.add_argument('--motivo', required=True, help='Justificativa do cancelamento')
    parser.add_argument('--poll', action='store_true', help='Aguardar status após cancelamento')
    parser.add_argument('--poll-delay', type=int, default=3, help='Delay entre polls')
    parser.add_argument('--dry-run', '--teste', action='store_true', help='Mostra a solicitação, mas NÃO envia para a API')
    parser.add_argument('--confirmar-cancelamento', action='store_true', help='Obrigatório para cancelamento real')
    
    args = parser.parse_args()
    
    print(f"\n🚫 Solicitação de cancelamento NFS-e: {args.invoice_id}")
    print(f"   Motivo: {args.motivo}")
    
    if args.dry_run:
        print("\n🧪 DRY-RUN ativo. Nenhuma requisição será enviada para a API.")
        return 0

    if not args.confirmar_cancelamento:
        print("\n❌ Bloqueado: cancelamento real exige --confirmar-cancelamento.")
        print("Use --dry-run para simular sem enviar para a API.")
        return 2

    print("\n⚠️ CANCELAMENTO REAL confirmado. Enviando para a API Notaas.")
    client = NotaasClient.from_env()
    result = client.cancelar(args.invoice_id, args.motivo)
    
    if result.success:
        print(f"\n✅ Cancelamento solicitado!")
        print(f"   Status: {result.status}")
        
        if args.poll:
            import time
            time.sleep(args.poll_delay)
            
            status = client.consultar_status(args.invoice_id)
            
            if status.success and status.status == 'cancelled':
                print(f"\n✅ Nota cancelada com sucesso!")
                return 0
            else:
                print(f"\n⏳ Status atual: {status.status}")
                return 1
        return 0
    else:
        print(f"\n❌ Erro no cancelamento!")
        print(f"   {result.error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
