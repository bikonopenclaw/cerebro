#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/data/.openclaw/workspace/Brain"
cd "$REPO_DIR"

# Evita rodar fora de um repo Git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERRO: $REPO_DIR não é um repositório Git"
  exit 1
fi

# Garante que origin existe
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "ERRO: remoto origin não configurado"
  exit 1
fi

# Atualiza refs remotas sem quebrar se rede falhar momentaneamente
git fetch origin main --quiet || true

# Se houver mudanças locais, commita
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "Sync automático do Brain $(date '+%Y-%m-%d %H:%M:%S %Z')"
else
  echo "Sem mudanças locais para commit."
fi

# Só tenta push se branch local estiver à frente ou tiver commit novo
git push origin main
