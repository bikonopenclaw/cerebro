#!/usr/bin/env bash
set -euo pipefail

ROOT="/data/.openclaw/workspace-kowalski/bitdefender-gravityzone"
SCRIPT="$ROOT/scripts/criar_bitdefender_ninja_tickets_fase1.py"
LOCK="$ROOT/jobs/bitdefender-ninja-ticket-monitor.lock"
LOG="$ROOT/jobs/bitdefender-ninja-ticket-run.log"

mkdir -p "$ROOT/jobs"

{
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Iniciando Bitdefender -> Ninja Fase 1"
  flock -n 9 || { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Já existe execução em andamento. Saindo."; exit 0; }
  python3 "$SCRIPT" --live --execute --auto-close
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Bitdefender -> Ninja Fase 1 concluído"
} 9>"$LOCK" >>"$LOG" 2>&1
