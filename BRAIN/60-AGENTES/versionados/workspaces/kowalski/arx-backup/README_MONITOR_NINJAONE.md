# Monitor ARX Backup -> NinjaOne tickets

## Objetivo

Abrir tickets no NinjaOne automaticamente quando o ARX Backup/Cove indicar backup em Atenção ou Crítico.
Evitar falso negativo: se houve falha no histórico, mas a checagem atual mostra backup concluído, não abre ticket.
Se havia ticket ativo e a checagem atual mostra recuperação, fecha o ticket no NinjaOne como `RESOLVED`.

## Scripts

- Dry-run: `scripts/monitorar_arx_ninjaone_tickets.py`
- Produção: `scripts/monitorar_arx_ninjaone_tickets.py --create`
- Runner do cron: `scripts/run_monitorar_arx_ninjaone_tickets.sh`

## Cron OpenClaw

- Nome: `ATIVO - ARX -> tickets NinjaOne diario 01h15 seg-qui`
- ID: `2c387780-44b2-4ba6-9f67-0ab3d844b75a`
- Agenda: terça a sexta às `01:15 America/Sao_Paulo`, expressão `15 1 * * 2-5`
- Executor shell espelhado: `bd9fe2f3-baa7-455b-aeab-6c51e4b9e4d9`, mesma agenda, agente main
- Sábado: `a522de30-a6a0-4690-acff-2984ee9463f4`, às `01:15 America/Sao_Paulo`, expressão `15 1 * * 6`
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

## Regra de recuperação

- Ticket só deve existir enquanto a falha atual persistir.
- Falha histórica em `TB`, `FB`, `SB`, `QB`, `HB` ou `WB` não basta para abrir ticket se o status atual já voltou para `Concluído (5)`.
- Quando um cliente/dispositivo com ticket ativo volta para `Concluído (5)`, o monitor fecha o ticket como `RESOLVED` e marca o item como inativo no estado local.
- Todo fechamento automático real deve enviar confirmação para o Hebert no Telegram.
- Se a confirmação Telegram falhar depois do fechamento, o monitor registra erro e deixa o cron alertar.
- Dry-run mostra `would_close`; produção com `--create` executa o fechamento real.

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
