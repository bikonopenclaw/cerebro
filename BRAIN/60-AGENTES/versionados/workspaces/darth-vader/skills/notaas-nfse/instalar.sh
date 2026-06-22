#!/bin/bash
# Script de Instalação - NOTAAS NFSE Skill
# Uso: ./instalar.sh

set -e

CORES='\033[0;36m'
VERDE='\033[0;32m'
AMARELO='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${CORES}"
echo "========================================"
echo "🧠 INSTALAÇÃO - NOTAAS NFSE"
echo "========================================"
echo -e "${NC}"

# Detectar diretório da skill
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_DIR="${SCRIPT_DIR}"

echo -e "${AMARELO}📁 Diretório da skill:${NC} ${SKILL_DIR}"
echo

# Verificar Python
echo -e "${AMARELO}Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "❌ Python 3 não encontrado!"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${VERDE}✅ Python ${PYTHON_VERSION} encontrado${NC}"
echo

# Instalar dependências
echo -e "${AMARELO}Instalando dependências...${NC}"
if [ -f "${SKILL_DIR}/requirements.txt" ]; then
    pip3 install -r "${SKILL_DIR}/requirements.txt" -q
    echo -e "${VERDE}✅ Dependências instaladas${NC}"
else
    echo -e "⚠️  requirements.txt não encontrado"
fi
echo

# Criar diretórios necessários
echo -e "${AMARELO}Criando diretórios...${NC}"
mkdir -p "${SKILL_DIR}/config"
mkdir -p "${SKILL_DIR}/data"
mkdir -p "${SKILL_DIR}/logs"
echo -e "${VERDE}✅ Diretórios criados${NC}"
echo

# Verificar se já existe configuração
if [ -f "${SKILL_DIR}/config/empresa.json" ]; then
    echo -e "${AMARELO}⚠️  Configuração já existe!${NC}"
    echo "Deseja reconfigurar? (s/n)"
    read -r resposta
    if [ "$resposta" != "s" ]; then
        echo -e "${VERDE}✅ Instalação concluída (configuração mantida)${NC}"
        exit 0
    fi
fi

# Copiar .env.example se não existir
if [ ! -f "${SKILL_DIR}/.env" ]; then
    echo -e "${AMARELO}Criando .env...${NC}"
    if [ -f "${SKILL_DIR}/.env.example" ]; then
        cp "${SKILL_DIR}/.env.example" "${SKILL_DIR}/.env"
    else
        touch "${SKILL_DIR}/.env"
    fi
    chmod 600 "${SKILL_DIR}/.env" || true
    echo -e "${VERDE}✅ .env criado${NC}"
    echo
fi

# Rodar setup interativo
echo -e "${AMARELO}Iniciando setup interativo...${NC}"
echo -e "${CORES}========================================${NC}"
echo

python3 "${SKILL_DIR}/scripts/setup.py"

echo
echo -e "${CORES}========================================${NC}"
echo -e "${VERDE}✅ INSTALAÇÃO CONCLUÍDA!${NC}"
echo -e "${CORES}========================================${NC}"
echo
echo "Próximos passos:"
echo "  1. Cadastrar clientes: python3 scripts/cadastrar_cliente.py"
echo "  2. Testar emissão: python3 scripts/emitir_nota.py --dry-run --cnpj 00.000.000/0001-00 --nome TESTE --email teste@exemplo.com --codigo 171901 --descricao Teste --valor 1000"
echo "  3. Ver docs: cat README.md"
echo
