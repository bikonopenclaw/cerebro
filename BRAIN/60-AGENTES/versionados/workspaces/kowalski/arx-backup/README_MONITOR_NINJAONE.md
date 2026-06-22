# Monitor ARX Backup -> NinjaOne tickets

## Objetivo

Abrir tickets no NinjaOne automaticamente quando o ARX Backup/Cove indicar backup em Atenção ou Crítico.

## Scripts

- Dry-run: `scripts/monitorar_arx_ninjaone_tickets.py`
- Produção: `scripts/monitorar_arx_ninjaone_tickets.py --create`
- Runner do cron: `scripts/run_monitorar_arx_ninjaone_tickets.sh`

## Cron OpenClaw

- Nome: `ARX Backup diário -> tickets NinjaOne`
- ID: `2c387780-44b2-4ba6-9f67-0ab3d844b75a`
- Agenda: todo dia às `08:15 America/Sao_Paulo`
- Delivery: sem anúncio em sucesso

## Segurança

- Não imprime token.
- Usa OAuth user-context NinjaOne salvo em arquivo local restrito.
- Se o access token expirar, usa refresh token.
- Usa `ticketFormId=1`, formulário `Default`.
- Todos os tickets ARX Backup abrem no cliente interno `00 - Bikon Tech`, por regra definida pelo Hebert.
- Não vincular ticket ao cliente final nem ao node final no NinjaOne. O cliente real vai no título e na descrição.
- Título padrão: `Alerta de ARX Backup - Nome do cliente`.

## Deduplicação

Estado em:

`jobs/arx-ninjaone-ticket-state.json`

A deduplicação evita abrir ticket repetido para o mesmo cliente/dispositivo/problema enquanto o problema continuar ativo.

## Mapa/regra de cliente

Arquivo:

`config/ninjaone-client-map.json`

Regra atual: todos os tickets entram em `00 - Bikon Tech` para triagem interna. Não criar aliases para cliente final sem nova ordem explícita do Hebert.

## Logs

- JSONL de execuções: `jobs/arx-ninjaone-ticket-log.jsonl`
- Log do runner: `jobs/arx-ninjaone-ticket-run.log`

## Validação feita

Dry-run em 2026-06-16:

- Contas ARX verificadas: 10
- Issues detectadas: 4
- Tickets criados: 0 no dry-run
- Cliente padrão: `00 - Bikon Tech`

Execução real em 2026-06-16 criou 4 tickets: `1021`, `1022`, `1023`, `1024`. Próximas execuções usam deduplicação e não devem reabrir os mesmos problemas enquanto continuarem ativos.
