---
name: "kowalski-arx-ticket-recovery"
description: "Alias seguro para ARX NinjaOne canonico"
---

# Kowalski ARX Ticket Recovery

## Decisao operacional

Esta skill nao e mais a fonte operacional principal do fluxo ARX Backup -> NinjaOne.

Ao acionar este tema, usar a skill canonica:

`/data/.openclaw/workspace/skills/arx-ninjaone-ticketing/SKILL.md`

## Por que esta skill continua existindo

Manter este alias evita perda de gatilho historico. Pedidos antigos como `ARX ticket recovery`, `falso negativo ARX`, `fechar ticket recuperado` ou `Kowalski ARX ticket` ainda devem cair no fluxo correto.

## Redirecionamento obrigatorio

1. Ler e seguir `arx-ninjaone-ticketing/SKILL.md`.
2. Para decisao de abrir ou nao abrir ticket, usar `arx-ninjaone-ticketing/references/decisao-incidente.md`.
3. Para deduplicacao, fechamento recuperado e confirmacao Telegram, usar `arx-ninjaone-ticketing/references/deduplicacao-e-recuperacao.md`.
4. Para cron, runner e logs, usar `arx-ninjaone-ticketing/references/operacao-cron-e-logs.md`.
5. Nao executar regra propria desta skill sem conferir a canonica.

## Funcionalidade preservada

A funcionalidade original fica preservada na skill canonica:

- nao abrir ticket por falha historica quando a checagem atual voltou para `Concluido (5)`;
- abrir ticket somente quando houver problema atual real;
- deduplicar por cliente, dispositivo e assinatura do problema;
- fechar ticket recuperado como `RESOLVED`;
- marcar o item como inativo no estado local;
- enviar confirmacao de fechamento automatico para o Hebert no Telegram;
- registrar fechamento, falha de confirmacao e estado local nos logs.

## Historico de validacao preservado

Em 2026-07-11, apos a mudanca de recuperacao:

- dry-run encontrou 11 contas, 1 issue real, 3 tickets recuperados para fechar, 0 erros;
- execucao real fechou 3 tickets como `RESOLVED` e nao criou ticket novo;
- dry-run pos-fechamento ficou com 1 issue real deduplicada e 0 pendencias de fechamento.

## Travas

- Nao alterar script, cron, token, config, estado local ou integracao NinjaOne sem aprovacao explicita do Hebert.
- Nao rodar `--create` manual fora do cron ja aprovado sem aprovacao.
- Nao criar ticket de teste real.
- Nao fechar ticket real manualmente.
- Se houver conflito entre esta skill e `arx-ninjaone-ticketing`, a canonica vence.
