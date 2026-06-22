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
Emitir NFS-e individual via API Notaas

Uso:
    # Pessoa jurídica
    python3 emitir_nota.py --documento "22874038000126" --nome "INSTITUTO BASE FORTE" \
        --email "financeiro@institutobaseforte.org.br" --codigo "171901" \
        --descricao "Servicos de contabilidade" --valor 674.40 --aliquota 0

    # Pessoa física
    python3 emitir_nota.py --documento "10301594759" --nome "Hebert Dummer Mattedi" \
        --email "hebertmattedi@gmail.com" --codigo "010701" \
        --descricao "serviço de infraestrutura de rede" --valor 1.00 --aliquota 5
"""

import os
import sys
import argparse
import json
import dotenv
from core import NotaasClient, criar_payload_individual

# Carregar variáveis de ambiente
dotenv.load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='Emitir NFS-e individual')
    parser.add_argument('--documento', help='CPF ou CNPJ do tomador, detectado automaticamente')
    parser.add_argument('--cpf', help='CPF do tomador pessoa física')
    parser.add_argument('--cnpj', help='CNPJ do tomador pessoa jurídica, mantido por compatibilidade')
    parser.add_argument('--nome', required=True, help='Nome/Razão social')
    parser.add_argument('--email', default='', help='Email do tomador, opcional quando a API aceitar emissão sem e-mail')
    parser.add_argument('--codigo', required=True, help='Código LC 116')
    parser.add_argument('--descricao', required=True, help='Descrição do serviço')
    parser.add_argument('--valor', type=float, required=True, help='Valor total')
    parser.add_argument('--aliquota', type=float, default=0, help='Alíquota ISS')
    parser.add_argument('--competencia', default='2026-04', help='Competência (YYYY-MM)')
    parser.add_argument('--poll', action='store_true', help='Aguardar status após emissão')
    parser.add_argument('--poll-delay', type=int, default=5, help='Delay entre polls (segundos)')
    parser.add_argument('--max-polls', type=int, default=20, help='Máximo de polls')
    parser.add_argument('--dry-run', '--teste', action='store_true', help='Monta e valida o payload, mas NÃO envia para a API')
    parser.add_argument('--confirmar-emissao', action='store_true', help='Obrigatório para emissão real')
    
    args = parser.parse_args()
    documento = args.documento or args.cpf or args.cnpj
    if not documento:
        parser.error('informe --documento, --cpf ou --cnpj')
    doc_digits = ''.join(ch for ch in documento if ch.isdigit())
    if len(doc_digits) == 11:
        doc_label = 'CPF'
    elif len(doc_digits) == 14:
        doc_label = 'CNPJ'
    else:
        parser.error('documento inválido: CPF deve ter 11 dígitos e CNPJ 14 dígitos')
    
    # Criar payload
    payload = criar_payload_individual(
        documento=documento,
        nome=args.nome,
        email=args.email,
        codigo=args.codigo,
        descricao=args.descricao,
        valor=args.valor,
        aliquota=args.aliquota,
        competencia=args.competencia
    )
    
    print(f"\n📄 Preparando NFS-e para: {args.nome}")
    print(f"   {doc_label}: {doc_digits}")
    print(f"   Valor: R$ {args.valor:.2f}")
    print(f"   Código LC 116: {args.codigo}")
    print(f"   Alíquota ISS: {args.aliquota}%")
    
    if args.dry_run:
        print("\n🧪 DRY-RUN ativo. Nenhuma requisição será enviada para a API.")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    if not args.confirmar_emissao:
        print("\n❌ Bloqueado: emissão real exige --confirmar-emissao.")
        print("Use --dry-run para simular sem enviar para a API.")
        return 2

    print("\n⚠️ EMISSÃO REAL confirmada. Enviando para a API Notaas.")
    client = NotaasClient.from_env()
    result = client.emitir(payload)
    
    if result.success:
        print(f"\n✅ Emissão aceita!")
        print(f"   Invoice ID: {result.invoice_id}")
        print(f"   Status: {result.status}")
        
        # Polling se solicitado
        if args.poll:
            print(f"\n⏳ Aguardando processamento...")
            
            for i in range(args.max_polls):
                import time
                time.sleep(args.poll_delay)
                
                status_result = client.consultar_status(result.invoice_id)
                
                if status_result.success:
                    status = status_result.status
                    
                    if status == 'issued':
                        print(f"\n✅ NFS-e emitida com sucesso!")
                        print(f"   Chave: {status_result.chNFSe}")
                        print(f"   Status: {status}")
                        return 0
                    elif status == 'error':
                        print(f"\n❌ Erro na emissão!")
                        print(f"   Erro: {status_result.error}")
                        return 1
                    else:
                        print(f"   Status: {status}...")
                else:
                    print(f"   Erro na consulta: {status_result.error}")
            
            print(f"\n⚠️ Timeout após {args.max_polls} tentativas")
            return 1
    else:
        print(f"\n❌ Erro na emissão!")
        print(f"   {result.error}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
