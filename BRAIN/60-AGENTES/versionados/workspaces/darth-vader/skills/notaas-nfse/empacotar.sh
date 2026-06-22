#!/bin/bash
# Script de Empacotamento - NOTAAS NFSE Skill
# Cria pacote ZIP limpo para distribuição
#
# Uso: ./empacotar.sh

set -e

CORES='\033[0;36m'
VERDE='\033[0;32m'
AMARELO='\033[0;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_NAME=$(basename "${SCRIPT_DIR}")
PACOTE_DIR="/tmp/${SKILL_NAME}-pacote"
ZIP_FILE="/tmp/${SKILL_NAME}.zip"

echo -e "${CORES}"
echo "========================================"
echo "📦 EMPACOTAMENTO - ${SKILL_NAME}"
echo "========================================"
echo -e "${NC}"

# Limpar pacote anterior
echo -e "${AMARELO}Limpando...${NC}"
rm -rf "${PACOTE_DIR}"
rm -f "${ZIP_FILE}"
mkdir -p "${PACOTE_DIR}"
echo -e "${VERDE}✅ Limpo${NC}"
echo

# Copiar arquivos (excluindo dados sensíveis)
echo -e "${AMARELO}Copiando arquivos...${NC}"

rsync -av \
  --exclude 'config/' \
  --exclude 'data/' \
  --exclude '.env' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.git/' \
  --exclude 'logs/' \
  --exclude '*.log' \
  --exclude 'node_modules/' \
  "${SCRIPT_DIR}/" \
  "${PACOTE_DIR}/"

echo -e "${VERDE}✅ Arquivos copiados${NC}"
echo

# Criar ZIP
echo -e "${AMARELO}Criando pacote ZIP...${NC}"
cd /tmp
zip -r "${ZIP_FILE}" "${SKILL_NAME}-pacote/" -q
echo -e "${VERDE}✅ Pacote criado: ${ZIP_FILE}${NC}"
echo

# Mostrar informações
TAMANHO=$(du -h "${ZIP_FILE}" | cut -f1)
ARQUIVOS=$(find "${PACOTE_DIR}" -type f | wc -l)

echo -e "${CORES}========================================${NC}"
echo -e "${VERDE}✅ PACOTE PRONTO!${NC}"
echo -e "${CORES}========================================${NC}"
echo
echo "📦 Arquivo: ${ZIP_FILE}"
echo "📊 Tamanho: ${TAMANHO}"
echo "📁 Arquivos: ${ARQUIVOS}"
echo
echo "📋 Para instalar em outra instância:"
echo "   1. Copiar ${ZIP_FILE} para nova instância"
echo "   2. unzip ${ZIP_FILE} -d ~/.openclaw/workspace/skills/"
echo "   3. cd ~/.openclaw/workspace/skills/${SKILL_NAME}"
echo "   4. ./instalar.sh"
echo

# Opcional: copiar para diretório atual
read -p "Copiar pacote para o diretório atual? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    cp "${ZIP_FILE}" "${SCRIPT_DIR}/"
    echo -e "${VERDE}✅ Pacote copiado para: ${SCRIPT_DIR}/${SKILL_NAME}.zip${NC}"
fi

# Limpar
rm -rf "${PACOTE_DIR}"
