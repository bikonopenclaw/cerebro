# ARX Backup diário → tickets NinjaOne

```yaml
categoria: automacao_monitoramento
fonte: execuções cron Kowalski em 2026-06-19, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-29, 2026-07-02 e 2026-07-06; consulta NinjaOne HOST1/Magnitos em 2026-07-06
confiabilidade: media
ultima_revisao: 2026-07-08
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

## Relatórios operacionais observados em 2026-07-06 BRT

ARX Backup:

- 11 contas/dispositivos monitorados: 8 OK, 1 atenção e 2 críticos por recorrência histórica.
- Críticos por recorrência: Shopping Catuaí / `4503-hv-01_3hy73` e Stcoop / `stc-mssql_wq95i`, com tickets NinjaOne existentes reaproveitados.
- Atenção: Ferreira Rocha / `scfr01_1km2s`, também com ticket relacionado existente.
- Guardrail mantido: status total atual concluído não apaga recorrência histórica; não abrir ticket novo quando já houver ticket relacionado para o mesmo problema.

NinjaOne tickets:

- A rotina conseguiu consultar 197 tickets no quadro “Todos os tickets”.
- Ativos no momento do relatório: 30; sem responsável na base: 23; ativos com mais de 24h: 22.
- Limitação técnica persistente: payload disponível não expôs timestamps de resolução/fechamento/primeira resposta; SLA real e fechados do dia não devem ser inventados.

## Limitação observada em servidor de cliente 2026-07-06

Consulta operacional do Kowalski para `HOST1 | Magnitos Granitos` no NinjaOne:

- Device identificado como online, Windows Server 2022 Standard em Dell PowerEdge T150.
- Endpoint de backup/jobs existia, mas não expôs job para o `deviceId 148` nem para a organização identificada.
- Não houve dado/campo/alerta/atividade consultável sobre replicação Hyper-V.
- Custom fields estavam vazios; atividades recentes eram majoritariamente eventos de partição adicionada/removida.

Consequência operacional:

- Não inferir conclusão de backup nem saúde de replicação Hyper-V a partir da ausência de dados no NinjaOne.
- Para validar esses itens, é necessário criar integração, monitor, script ou custom field que grave status explícito no NinjaOne.

## Guardrails

- Não imprimir tokens, segredos ou credenciais em respostas, logs consolidados ou Brain.
- Em caso de erro, relatar de forma curta e apontar o caminho do log operacional.
- Não acionar cliente externo nem enviar e-mail apenas por execução bem-sucedida da rotina.

## Relações

- Agente executor observado: Kowalski.
- Categoria: monitoramento operacional / abertura de tickets.
