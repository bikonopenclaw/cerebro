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
Setup Interativo - Configuração Inicial da Skill NOTAAS NFSE

Este script coleta os dados da empresa e configura a skill para uso.
Executar no primeiro uso em qualquer instância OpenClaw.

Uso: python3 scripts/setup.py
"""

import json
import os
import sys
import re
from pathlib import Path

# Cores para terminal
CORES = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'verde': '\033[92m',
    'amarelo': '\033[93m',
    'azul': '\033[94m',
    'vermelho': '\033[91m',
    'ciano': '\033[96m'
}

def limpar_terminal():
    os.system('clear' if os.name != 'nt' else 'cls')

def imprimir_cabecalho():
    print(f"{CORES['ciano']}")
    print("=" * 70)
    print(f"{CORES['bold']}🧠 SETUP INICIAL - SKILL NOTAAS NFSE{CORES['reset']}")
    print(f"{CORES['ciano']}=" * 70)
    print(f"{CORES['reset']}")
    print("Este script vai configurar a skill para sua empresa.")
    print("Você precisa de uma conta ativa na plataforma Notaas.")
    print()

def validar_cnpj(cnpj):
    """Valida formato do CNPJ"""
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    if len(cnpj) != 14:
        return False
    return True

def validar_api_key(api_key):
    """Valida formato da API Key"""
    if not api_key.startswith('ntaas_'):
        return False
    return len(api_key) >= 20

def obter_dados_empresa():
    """Coleta dados da empresa via input interativo"""
    print(f"{CORES['bold']}📋 DADOS DA EMPRESA{CORES['reset']}")
    print("-" * 50)
    print()
    
    dados = {}
    
    # Razão Social
    while True:
        nome = input(f"{CORES['amarelo']}Razão Social da Empresa:{CORES['reset']} ").strip()
        if nome:
            dados['nome'] = nome.upper()
            break
        print(f"{CORES['vermelho']}❌ Campo obrigatório!{CORES['reset']}")
    
    # Nome Fantasia (opcional)
    fantasia = input(f"{CORES['amarelo']}Nome Fantasia (opcional):{CORES['reset']} ").strip()
    dados['fantasia'] = fantasia.upper() if fantasia else ''
    
    # CNPJ
    while True:
        cnpj = input(f"{CORES['amarelo']}CNPJ (apenas números):{CORES['reset']} ").strip()
        if validar_cnpj(cnpj):
            dados['cnpj'] = cnpj
            # Formatar para exibição
            cnpj_fmt = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
            print(f"{CORES['verde']}✅ CNPJ válido: {cnpj_fmt}{CORES['reset']}")
            break
        print(f"{CORES['vermelho']}❌ CNPJ inválido! Deve ter 14 dígitos.{CORES['reset']}")
    
    # Inscrição Municipal
    while True:
        im = input(f"{CORES['amarelo']}Inscrição Municipal (ou Enter se não tiver):{CORES['reset']} ").strip()
        if im or im == '':
            dados['inscricao_municipal'] = im
            break
    
    # Cidade
    cidade = input(f"{CORES['amarelo']}Cidade:{CORES['reset']} ").strip()
    dados['cidade'] = cidade.upper()
    
    # UF
    while True:
        uf = input(f"{CORES['amarelo']}UF (2 letras):{CORES['reset']} ").strip().upper()
        if len(uf) == 2:
            dados['uf'] = uf
            break
        print(f"{CORES['vermelho']}❌ UF deve ter 2 letras!{CORES['reset']}")
    
    # Código IBGE (opcional, pode buscar depois)
    ibge = input(f"{CORES['amarelo']}Código IBGE da Cidade (opcional):{CORES['reset']} ").strip()
    dados['ibge'] = ibge
    
    print()
    return dados

def obter_dados_notaas():
    """Coleta dados de acesso à Notaas"""
    print(f"{CORES['bold']}🔐 DADOS DE ACESSO - NOTAAS{CORES['reset']}")
    print("-" * 50)
    print()
    print("Obtenha sua API Key em: https://platform.notaas.com.br")
    print("Configurações → API → Gerar Chave")
    print()
    
    dados = {}
    
    # API Key
    while True:
        api_key = input(f"{CORES['amarelo']}API Key da Notaas:{CORES['reset']} ").strip()
        if validar_api_key(api_key):
            dados['api_key'] = api_key
            print(f"{CORES['verde']}✅ API Key válida{CORES['reset']}")
            break
        print(f"{CORES['vermelho']}❌ API Key inválida! Deve começar com 'ntaas_' e ter 20+ caracteres.{CORES['reset']}")
    
    # Ambiente
    print()
    print("Selecione o ambiente:")
    print("  1) Produção (recomendado)")
    print("  2) Homologação (testes)")
    
    while True:
        opcao = input(f"{CORES['amarelo']}Opção (1 ou 2):{CORES['reset']} ").strip()
        if opcao == '1':
            dados['ambiente'] = 'producao'
            dados['base_url'] = 'https://platform.notaas.com.br/api/v1'
            break
        elif opcao == '2':
            dados['ambiente'] = 'homologacao'
            dados['base_url'] = 'https://platform.notaas.com.br/api/v1'  # Mesma URL
            break
        print(f"{CORES['vermelho']}❌ Opção inválida!{CORES['reset']}")
    
    print()
    return dados

def salvar_configuracao(empresa, notaas):
    """Salva configuração nos arquivos apropriados"""
    print(f"{CORES['bold']}💾 SALVANDO CONFIGURAÇÃO...{CORES['reset']}")
    print()
    
    # Criar diretório config se não existir
    config_dir = Path(__file__).parent.parent / 'config'
    config_dir.mkdir(exist_ok=True)
    
    # Salvar config da empresa
    config_empresa = {
        'empresa': empresa,
        'notaas': notaas,
        'data_configuracao': __import__('datetime').datetime.now().isoformat(),
        'versao_skill': '2.0.0'
    }
    
    config_path = config_dir / 'empresa.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_empresa, f, indent=2, ensure_ascii=False)
    
    print(f"{CORES['verde']}✅ Config salva em: {config_path}{CORES['reset']}")
    
    # Criar .env
    env_path = Path(__file__).parent.parent / '.env'
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(f"NOTAAS_API_KEY={notaas['api_key']}\n")
        f.write(f"NOTAAS_BASE_URL={notaas['base_url']}\n")
        f.write(f"EMPRESA_CNPJ={empresa['cnpj']}\n")
        f.write(f"EMPRESA_NOME={empresa['nome']}\n")
    
    print(f"{CORES['verde']}✅ .env criado em: {env_path}{CORES['reset']}")
    
    # Criar base de clientes vazia se não existir
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    clientes_path = data_dir / 'clientes.json'
    if not clientes_path.exists():
        with open(clientes_path, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        print(f"{CORES['verde']}✅ Base de clientes criada: {clientes_path}{CORES['reset']}")
    
    # Criar histórico vazio
    historico_path = data_dir / 'historico.json'
    if not historico_path.exists():
        with open(historico_path, 'w', encoding='utf-8') as f:
            json.dump({'emissoes': []}, f, indent=2, ensure_ascii=False)
        print(f"{CORES['verde']}✅ Histórico criado: {historico_path}{CORES['reset']}")
    
    print()

def imprimir_resumo(empresa, notaas):
    """Imprime resumo da configuração"""
    print(f"{CORES['bold']}📊 RESUMO DA CONFIGURAÇÃO{CORES['reset']}")
    print("=" * 50)
    print()
    print(f"{CORES['bold']}EMPRESA:{CORES['reset']}")
    print(f"  • Razão Social: {empresa['nome']}")
    if empresa.get('fantasia'):
        print(f"  • Fantasia: {empresa['fantasia']}")
    print(f"  • CNPJ: {empresa['cnpj']}")
    if empresa.get('inscricao_municipal'):
        print(f"  • Inscrição Municipal: {empresa['inscricao_municipal']}")
    print(f"  • Cidade/UF: {empresa['cidade']}/{empresa['uf']}")
    if empresa.get('ibge'):
        print(f"  • IBGE: {empresa['ibge']}")
    print()
    print(f"{CORES['bold']}NOTAAS:{CORES['reset']}")
    print(f"  • API Key: {notaas['api_key'][:10]}...{notaas['api_key'][-4:]}")
    print(f"  • Ambiente: {notaas['ambiente']}")
    print(f"  • Base URL: {notaas['base_url']}")
    print()

def proximos_passos():
    """Imprime próximos passos"""
    print(f"{CORES['bold']}🎯 PRÓXIMOS PASSOS:{CORES['reset']}")
    print("=" * 50)
    print()
    print("1. Cadastrar clientes:")
    print(f"   {CORES['ciano']}python3 scripts/cadastrar_cliente.py --help{CORES['reset']}")
    print()
    print("2. Simular emissão sem enviar para API:")
    print(f"   {CORES['ciano']}python3 scripts/emitir_nota.py --dry-run --cnpj 00.000.000/0001-00 --nome TESTE --email teste@exemplo.com --codigo 171901 --descricao Teste --valor 1000{CORES['reset']}")
    print()
    print("3. Emitir nota real, somente com confirmação explícita:")
    print(f"   {CORES['ciano']}python3 scripts/emitir_nota.py --confirmar-emissao --cnpj 00.000.000/0001-00 --nome TESTE --email teste@exemplo.com --codigo 171901 --descricao Teste --valor 1000{CORES['reset']}")
    print()
    print("4. Documentação completa:")
    print(f"   {CORES['ciano']}cat SKILL.md{CORES['reset']}")
    print()
    print(f"{CORES['verde']}✅ SETUP CONCLUÍDO!{CORES['reset']}")
    print()

def main():
    """Função principal"""
    limpar_terminal()
    imprimir_cabecalho()
    
    # Coletar dados
    empresa = obter_dados_empresa()
    print()
    notaas = obter_dados_notaas()
    print()
    
    # Confirmar
    imprimir_resumo(empresa, notaas)
    
    confirmar = input(f"{CORES['amarelo']}Confirmar configuração? (s/n):{CORES['reset']} ").strip().lower()
    if confirmar != 's':
        print(f"{CORES['vermelho']}❌ Configuração cancelada.{CORES['reset']}")
        sys.exit(1)
    
    # Salvar
    salvar_configuracao(empresa, notaas)
    
    # Próximos passos
    proximos_passos()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{CORES['vermelho']}❌ Setup cancelado pelo usuário.{CORES['reset']}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{CORES['vermelho']}❌ Erro: {e}{CORES['reset']}")
        sys.exit(1)
