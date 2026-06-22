#!/usr/bin/env bash
set -euo pipefail

ROOT="/data/.openclaw/workspace-kowalski/arx-backup"
SCRIPT="$ROOT/scripts/monitorar_arx_ninjaone_tickets.py"
LOCK="$ROOT/jobs/arx-ninjaone-ticket-monitor.lock"
LOG="$ROOT/jobs/arx-ninjaone-ticket-run.log"

mkdir -p "$ROOT/jobs"

{
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Iniciando monitor ARX -> NinjaOne"
  flock -n 9 || { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Já existe execução em andamento. Saindo."; exit 0; }
  python3 "$SCRIPT" --create
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Monitor concluído"
} 9>"$LOCK" >>"$LOG" 2>&1
