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
Exemplo 1: Emissão Individual de NFS-e

Demonstra como emitir uma NFS-e individual usando a API Notaas.
"""

import sys
import os

# Adicionar ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import NotaasClient, criar_payload_individual


def exemplo_individual():
    """Emitir NFS-e individual"""
    
    # Criar cliente
    client = NotaasClient.from_env()
    
    # Criar payload usando helper
    payload = criar_payload_individual(
        cnpj="22874038000126",
        nome="INSTITUTO BASE FORTE",
        email="financeiro@institutobaseforte.org.br",
        codigo="171901",
        descricao="Servicos de contabilidade - Imunidade",
        valor=674.40,
        aliquota=0,
        competencia="2026-04"
    )
    
    # Emitir
    print("📤 Emitindo NFS-e individual...")
    result = client.emitir(payload)
    
    if result.success:
        print(f"\n✅ Emissão aceita!")
        print(f"   Invoice ID: {result.invoice_id}")
        print(f"   Status: {result.status}")
        
        # Consultar status
        import time
        time.sleep(5)
        
        status = client.consultar_status(result.invoice_id)
        
        if status.success:
            print(f"\n📊 Status atual: {status.status}")
            
            if status.status == 'issued':
                print(f"   Chave NFSe: {status.chNFSe}")
                
                # Baixar PDF e XML
                pdf = client.baixar_pdf(result.invoice_id)
                xml = client.baixar_xml(result.invoice_id)
                
                if pdf and xml:
                    print(f"\n✅ PDF e XML baixados com sucesso!")
                    print(f"   PDF: {len(pdf)} bytes")
                    print(f"   XML: {len(xml)} bytes")
            elif status.status == 'error':
                print(f"   Erro: {status.error}")
    else:
        print(f"\n❌ Erro: {result.error}")


if __name__ == "__main__":
    exemplo_individual()
