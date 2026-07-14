---
name: "kowalski-arx-ticket-recovery"
description: "ARX evita falso negativo e fecha ticket recuperado"
---

# Kowalski, ARX Ticket Recovery

## Objetivo

Evitar ticket NinjaOne falso negativo no monitor ARX Backup e fechar automaticamente tickets quando o backup voltar a concluir.

## Regra operacional

A automação ARX Backup -> NinjaOne deve diferenciar falha atual de falha histórica.

## Abrir ticket

Abrir ticket somente quando a checagem atual indicar problema real:

- status total atual com severidade `Atenção` ou `Crítico`, exceto quando o status atual for `Concluído (5)`;
- fonte atual com status problemático, como `Falhou`, `Abortado`, `Interrompido`, `Concluído com erros`, `Em progresso com falhas` ou `Acima da cota`;
- erro atual em fonte cujo último status não seja `Concluído (5)`.

Falha em histórico de 28 dias (`TB`, `FB`, `SB`, `QB`, `HB`, `WB`) não deve abrir ticket sozinha se depois dela o backup voltou a concluir.

## Não abrir falso negativo

Se houve falha anterior, mas a checagem atual mostra `Concluído (5)`, considerar recuperado e não abrir novo ticket. O histórico pode continuar aparecendo no relatório técnico, mas não deve virar chamado operacional.

## Fechar ticket recuperado

Se já existe ticket ativo no estado local e a próxima checagem mostra que o backup voltou a concluir, fechar o ticket no NinjaOne como `RESOLVED` e marcar o item como inativo em:

`/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-state.json`

Todo fechamento automático real deve enviar confirmação para o Hebert no Telegram. Se a confirmação falhar depois do fechamento, registrar erro e deixar o cron alertar.

## Dry-run e produção

- Dry-run mostra `would_close`, não cria nem fecha ticket real e não altera estado local.
- Produção com `--create` pode criar tickets novos e fechar tickets recuperados.

## Arquivos envolvidos

- Script principal: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py`
- Runner do cron: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh`
- Estado local: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-state.json`
- Logs: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-log.jsonl`

## Validação inicial

Em 2026-07-11, após a mudança:

- dry-run encontrou 11 contas, 1 issue real, 3 tickets recuperados para fechar, 0 erros;
- execução real fechou 3 tickets como `RESOLVED` e não criou ticket novo;
- dry-run pós-fechamento ficou com 1 issue real deduplicada e 0 pendências de fechamento.
