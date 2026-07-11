# Acesso financeiro read-only

## Finalidade

Kowalski pode consultar a base financeira gerencial criada pelo Darth Vader para montar relatórios, conferências e visões consolidadas.

## Fonte de verdade

- Dono operacional: Darth Vader.
- Banco original: `/data/.openclaw/workspace-darth-vader/boletos/db/faturamento.db`.
- Acesso compartilhado para Hermes: `/var/tmp/openclaw-hermes-financeiro/faturamento.db`.

O caminho em `/var/tmp/openclaw-hermes-financeiro/faturamento.db` é um hard link para o mesmo arquivo SQLite, não uma cópia exportada.

## Regra obrigatória

- Kowalski só consulta.
- Não criar tabela.
- Não alterar schema.
- Não importar retorno bancário.
- Não atualizar baixa, pagamento, boleto, NFS-e ou remessa.
- Escrita, baixa e conciliação continuam com Darth Vader.

## Consulta segura

Use sempre SQLite em modo read-only:

```bash
sqlite3 'file:/var/tmp/openclaw-hermes-financeiro/faturamento.db?mode=ro'
```

Helper:

```bash
/data/.openclaw/workspace-kowalski/financeiro/query_financeiro_ro.sh "select count(*) from vw_financeiro_boletos;"
```

## Views liberadas

- `vw_financeiro_boletos`
- `vw_financeiro_contas_receber`
- `vw_financeiro_kpi_mensal`
- `vw_financeiro_clientes`
- `vw_financeiro_remessas`
- `vw_financeiro_retornos`
