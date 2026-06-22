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
Emitir NFS-e em lote via API Notaas

Uso:
    python3 emitir_lote.py --clientes data/clientes.json --batch-size 2
"""

import os
import sys
import json
import argparse
import dotenv
from core import NotaasClient, montar_tomador

dotenv.load_dotenv()


def carregar_clientes(path: str) -> list:
    """Carrega lista de clientes do JSON"""
    with open(path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Emitir NFS-e em lote')
    parser.add_argument('--clientes', required=True, help='Arquivo JSON com clientes')
    parser.add_argument('--batch-size', type=int, default=2, help='Tamanho do batch')
    parser.add_argument('--poll', action='store_true', help='Aguardar status')
    parser.add_argument('--poll-delay', type=int, default=5, help='Delay entre polls')
    parser.add_argument('--max-polls', type=int, default=30, help='Máximo de polls')
    parser.add_argument('--dry-run', '--teste', action='store_true', help='Monta os batches, mas NÃO envia para a API')
    parser.add_argument('--confirmar-emissao', action='store_true', help='Obrigatório para emissão real em lote')
    
    args = parser.parse_args()
    
    # Carregar clientes
    clientes = carregar_clientes(args.clientes)
    print(f"📋 {len(clientes)} clientes carregados")
    
    if args.dry_run:
        print("🧪 DRY-RUN ativo. Nenhuma requisição será enviada para a API.")

    if not args.dry_run and not args.confirmar_emissao:
        print("❌ Bloqueado: emissão real em lote exige --confirmar-emissao.")
        print("Use --dry-run para simular sem enviar para a API.")
        return 2

    client = None if args.dry_run else NotaasClient.from_env()
    
    # Processar em batches
    total_emitidas = 0
    total_erros = 0
    
    for i in range(0, len(clientes), args.batch_size):
        batch_clientes = clientes[i:i + args.batch_size]
        print(f"\n📤 Batch {i//args.batch_size + 1}: {len(batch_clientes)} notas")
        
        # Criar payload
        payload = {"items": []}
        for cliente in batch_clientes:
            documento = cliente.get('documento') or cliente.get('cpf') or cliente.get('cnpj')
            payload["items"].append({
                "tomador": montar_tomador(documento, cliente['nome'], cliente.get('email', ''), cliente.get('endereco')),
                "servico": {
                    "codigo": cliente['codigo'],
                    "descricao": cliente['descricao']
                },
                "valores": {
                    "total": cliente['valor'],
                    "aliquotaIss": cliente.get('aliquota', 0)
                }
            })
        
        if args.dry_run:
            print(f"   DRY-RUN: batch montado com {len(payload['items'])} notas.")
            continue

        print("   ⚠️ EMISSÃO REAL EM LOTE confirmada. Enviando para a API Notaas.")
        result = client.emitir_lote(payload['items'])
        
        if result.success:
            print(f"   Batch aceito - ID: {result.invoice_id}")
            
            if args.poll:
                import time
                for j in range(args.max_polls):
                    time.sleep(args.poll_delay)
                    
                    status = client.consultar_batch_status(result.invoice_id)
                    
                    if status.success:
                        data = status.data
                        issued = data.get('issued', 0)
                        errors = data.get('errors', 0)
                        total = data.get('total', 0)
                        
                        print(f"   Status: {issued}/{total} emitidas, {errors} erros")
                        
                        if data.get('status') in ['completed', 'partial']:
                            total_emitidas += issued
                            total_erros += errors
                            break
        else:
            print(f"   ❌ Erro: {result.error}")
            total_erros += len(batch_clientes)
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   Emitidas: {total_emitidas}")
    print(f"   Erros: {total_erros}")
    print(f"   Total: {len(clientes)}")
    
    return 0 if total_erros == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
