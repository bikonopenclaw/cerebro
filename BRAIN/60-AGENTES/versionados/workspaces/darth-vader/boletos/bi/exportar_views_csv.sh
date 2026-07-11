#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="${BASE_DIR}/../db/faturamento.db"
OUT_DIR="${BASE_DIR}/exports"

mkdir -p "${OUT_DIR}"

sqlite3 "${DB_PATH}" <<SQL
.headers on
.mode csv
.once ${OUT_DIR}/financeiro_boletos.csv
SELECT * FROM vw_financeiro_boletos;
.once ${OUT_DIR}/financeiro_contas_receber.csv
SELECT * FROM vw_financeiro_contas_receber;
.once ${OUT_DIR}/financeiro_kpi_mensal.csv
SELECT * FROM vw_financeiro_kpi_mensal;
.once ${OUT_DIR}/financeiro_clientes.csv
SELECT * FROM vw_financeiro_clientes;
.once ${OUT_DIR}/financeiro_remessas.csv
SELECT * FROM vw_financeiro_remessas;
.once ${OUT_DIR}/financeiro_retornos.csv
SELECT * FROM vw_financeiro_retornos;
SQL

echo "CSV exports written to ${OUT_DIR}"
