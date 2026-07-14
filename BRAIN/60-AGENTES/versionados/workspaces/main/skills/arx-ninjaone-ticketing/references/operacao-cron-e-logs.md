# Operação, Cron E Logs

## Cron Atual

- Nome: `ATIVO - ARX -> tickets NinjaOne diario 01h15 seg-qui`
- ID: `2c387780-44b2-4ba6-9f67-0ab3d844b75a`
- Agenda: terça a sexta às `01:15 America/Sao_Paulo`, expressão `15 1 * * 2-5`
- Agente: Kowalski
- Executor shell espelhado: `bd9fe2f3-baa7-455b-aeab-6c51e4b9e4d9`, mesma agenda, agente main
- Sábado: `a522de30-a6a0-4690-acff-2984ee9463f4`, às `01:15 America/Sao_Paulo`, expressão `15 1 * * 6`
- Sucesso: silencioso
- Falha: alertar

## Runner

`/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh`

O runner usa lock para evitar execução concorrente.

## Logs

- JSONL de execução: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-log.jsonl`
- Log do runner: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-run.log`

## Validação

Antes de qualquer mudança em produção:

1. Rodar dry-run.
2. Conferir `summary.errors`.
3. Conferir `would_create`, `deduped` e `would_close`.
4. Confirmar que fechamento automático envia mensagem Telegram quando executado.
5. Só então autorizar execução real.

## Reporte

Em sucesso silencioso, não interromper Hebert.

Em falha, reportar em até 3 linhas:

1. O que falhou.
2. Impacto operacional.
3. Próximo passo recomendado.
