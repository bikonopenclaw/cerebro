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
Exemplo 2: Emissão em Lote de NFS-e

Demonstra como emitir múltiplas NFS-e usando batch da API Notaas.
"""

import sys
import os

# Adicionar ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import NotaasClient


def exemplo_lote():
    """Emitir NFS-e em lote"""
    
    # Criar cliente
    client = NotaasClient.from_env()
    
    # Lista de clientes
    clientes = [
        {
            "cnpj": "22874038000126",
            "nome": "INSTITUTO BASE FORTE",
            "email": "financeiro@institutobaseforte.org.br",
            "codigo": "171901",
            "descricao": "Servicos de contabilidade - Nota 1",
            "valor": 500.00,
            "aliquota": 0
        },
        {
            "cnpj": "22874038000126",
            "nome": "INSTITUTO BASE FORTE",
            "email": "financeiro@institutobaseforte.org.br",
            "codigo": "171901",
            "descricao": "Servicos de contabilidade - Nota 2",
            "valor": 600.00,
            "aliquota": 0
        }
    ]
    
    print(f"📤 Emitindo {len(clientes)} NFS-e em lote...")
    
    # Criar payload
    payload = {"items": []}
    for cliente in clientes:
        payload["items"].append({
            "tomador": {
                "cnpj": cliente["cnpj"],
                "nome": cliente["nome"],
                "email": cliente["email"]
            },
            "servico": {
                "codigo": cliente["codigo"],
                "descricao": cliente["descricao"]
            },
            "valores": {
                "total": cliente["valor"],
                "aliquotaIss": cliente["aliquota"]
            }
        })
    
    # Emitir batch
    result = client.emitir_lote(payload["items"])
    
    if result.success:
        print(f"\n✅ Batch aceito!")
        print(f"   Batch ID: {result.invoice_id}")
        print(f"   Status: {result.status}")
        
        # Aguardar processamento
        import time
        print(f"\n⏳ Aguardando processamento...")
        time.sleep(10)
        
        # Consultar status do batch
        status = client.consultar_batch_status(result.invoice_id)
        
        if status.success:
            data = status.data
            print(f"\n📊 Status do batch:")
            print(f"   Total: {data.get('total')}")
            print(f"   Emitidas: {data.get('issued')}")
            print(f"   Erros: {data.get('errors')}")
            print(f"   Status: {data.get('status')}")
            
            # Listar notas emitidas
            for invoice in data.get('invoices', []):
                if invoice.get('status') == 'issued':
                    print(f"\n   ✅ {invoice.get('invoiceId')}: {invoice.get('chNFSe')}")
                else:
                    print(f"\n   ❌ {invoice.get('invoiceId')}: {invoice.get('error')}")
    else:
        print(f"\n❌ Erro: {result.error}")


if __name__ == "__main__":
    exemplo_lote()
