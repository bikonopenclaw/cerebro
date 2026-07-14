# Deduplicação E Recuperação

## Deduplicação

Deduplicar por cliente, dispositivo e assinatura do problema.

Estado local:

`/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-state.json`

Não abrir novo ticket enquanto existir problema ativo com mesma assinatura e `ticket_id` registrado.

## Recuperação

Se um cliente/dispositivo com ticket ativo voltar para `Concluído (5)`, considerar recuperado.

Em dry-run:

- mostrar `would_close`;
- não fechar ticket;
- não alterar estado local.

Em produção com `--create`:

- fechar o ticket no NinjaOne como `RESOLVED`;
- enviar confirmação do fechamento para o Hebert no Telegram;
- marcar `active=false` no estado local;
- registrar `resolved_at`, `resolved_status` e `resolved_last_success`.

## Confirmação Obrigatória De Fechamento

Todo fechamento automático real deve enviar mensagem para o Telegram do Hebert com:

- ticket ID;
- cliente;
- dispositivo;
- status ARX atual;
- último backup válido.

Se a confirmação Telegram falhar após o fechamento, registrar erro no log e retornar falha para o cron alertar.

## Logs

Registrar fechamento ou tentativa de fechamento em:

`/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-log.jsonl`
