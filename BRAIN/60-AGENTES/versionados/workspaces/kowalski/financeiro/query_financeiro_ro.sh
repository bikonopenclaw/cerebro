#!/usr/bin/env bash
set -euo pipefail

DB_URI="file:/var/tmp/openclaw-hermes-financeiro/faturamento.db?mode=ro"

if [ "$#" -gt 0 ]; then
  sqlite3 -readonly "$DB_URI" "$*"
else
  sqlite3 -readonly "$DB_URI"
fi
