# BI financeiro Bikon

Banco:

`/data/.openclaw/workspace-darth-vader/boletos/db/faturamento.db`

Camada de consulta:

- `vw_financeiro_boletos`: fato principal. Uma linha por boleto/NFS-e.
- `vw_financeiro_contas_receber`: boletos em aberto ou vencidos.
- `vw_financeiro_kpi_mensal`: faturado, recebido, aberto e vencido por mes.
- `vw_financeiro_clientes`: consolidado por cliente.
- `vw_financeiro_remessas`: conferencia entre remessa e boletos vinculados.
- `vw_financeiro_retornos`: ocorrencias de retorno bancario quando importadas.

Atualizar views:

```bash
sqlite3 /data/.openclaw/workspace-darth-vader/boletos/db/faturamento.db < /data/.openclaw/workspace-darth-vader/boletos/bi/views_financeiro.sql
```

Exportar CSVs para PowerBI ou planilha:

```bash
/data/.openclaw/workspace-darth-vader/boletos/bi/exportar_views_csv.sh
```

Proxima evolucao:

- Importar retorno Cresol em `retornos` e `retorno_ocorrencias`.
- Atualizar `boletos.valor_pago_centavos`, `data_pagamento` e `data_credito`.
- Criar tabela de despesas no mesmo banco quando o fluxo de entrada estiver definido.
