# ARX Backup diário → tickets NinjaOne

```yaml
categoria: automacao_monitoramento
fonte: execuções cron Kowalski em 2026-06-19, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-29 e 2026-07-02
confiabilidade: media
ultima_revisao: 2026-07-03
tags: [arx, backup, ninjaone, tickets, monitoramento, kowalski]
```

## Finalidade

Automação diária para monitorar situações de backup ARX e refletir issues em tickets NinjaOne, com deduplicação para evitar tickets repetidos.

## Execução registrada

- Script: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh`
- Log operacional: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-run.log`
- Última execução observada: 2026-06-29.
- Resultado: sucesso.
- Resumo detalhado conhecido da execução de 2026-06-29: 10 backups verificados, 3 ocorrências, 1 ticket criado (#1131), 2 tickets existentes reaproveitados, 0 erros.
- Resumo histórico conhecido da execução de 2026-06-19: 10 checados, 3 issues, 0 tickets criados, 3 deduplicados, 0 erros.


## Limitação observada em relatório NinjaOne 2026-07-02

Na rotina de resumo diário de tickets NinjaOne, a autenticação, o status de ticket e o formulário padrão responderam, mas a listagem de tickets não ficou disponível pelos endpoints testados.

Consequência operacional:

- KPIs de chamados abertos, novos, fechados, vencidos, responsável, prioridade e tempos não devem ser inferidos sem endpoint/permissão oficial de leitura/listagem.
- Próximo passo técnico: validar endpoint e permissões oficiais de listagem de tickets antes de consolidar relatório completo.

## Guardrails

- Não imprimir tokens, segredos ou credenciais em respostas, logs consolidados ou Brain.
- Em caso de erro, relatar de forma curta e apontar o caminho do log operacional.
- Não acionar cliente externo nem enviar e-mail apenas por execução bem-sucedida da rotina.

## Relações

- Agente executor observado: Kowalski.
- Categoria: monitoramento operacional / abertura de tickets.
