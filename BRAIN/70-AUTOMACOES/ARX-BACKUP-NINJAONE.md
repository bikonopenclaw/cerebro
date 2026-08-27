# ARX Backup diário → tickets NinjaOne

```yaml
categoria: automacao_monitoramento
fonte: execuções cron Kowalski em 2026-06-19, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-29, 2026-07-02, 2026-07-06, relatorios operacionais ate 2026-08-12, checkpoints de reativacao em 2026-08-24/25 e relatorios Cartorio Gerusa em 2026-08-26
confiabilidade: alta
ultima_revisao: 2026-08-27
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

## Relatorio operacional 2026-08-12

Resumo agregado read-only referente a 2026-08-11 BRT:

- 11 contas/dispositivos monitorados.
- Classificacao operacional: 9 OK, 2 atencao, 0 critico.
- Status atual da API: 9 concluidos e 2 em processo.
- Ultimo backup valido em 2026-08-11: 6/11; apos a virada para 2026-08-12: 5/11.
- Atencoes: `16 Ferreira Rocha / servidor_2j3wv` com ticket NinjaOne `#1692` ativo; `15 - RI Maraba / 15-hv-03_fpjsk`; acompanhamento de `11 - Grupo Unus / hv-01_qbcsz`.
- Nenhum job com falha critica atual retornado pela API.

Guardrail: acompanhar jobs em processo/atencao/recorrencia e reavaliar pelo fluxo autorizado de tickets; nao alterar backup, job, politica, script ou ticket sem autorizacao explicita.

## Reativacao controlada 2026-08-24/25

Hebert pediu retorno da abertura de tickets ARX -> NinjaOne e depois autorizou o passo seguinte como `Ok reautorizar ninjaone e canary 1 ticket`. Registrar isso como autorizacao estreita para reautorizar NinjaOne e executar somente um canario real de ticket quando houver issue ARX real atual ou fixture controlada explicitamente aprovada; nao e autorizacao para bulk create.

Responsabilidade canonica atual:

- Sentinel: coleta/read-plane operacional;
- Kowalski: producao de relatorios e operacao ARX Backup -> NinjaOne ticketing;
- Puppet Master: controle, aprovacao e orquestracao.

Arquivos canonicos ativos:

- Skill: `/data/.openclaw/workspace/skills/arx-ninjaone-ticketing/SKILL.md`.
- Runner: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/run_monitorar_arx_ninjaone_tickets.sh`.
- Script: `/data/.openclaw/workspace-kowalski/arx-backup/scripts/monitorar_arx_ninjaone_tickets.py`.
- State: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-state.json`.
- JSONL log: `/data/.openclaw/workspace-kowalski/arx-backup/jobs/arx-ninjaone-ticket-log.jsonl`.

Evidencia local no checkpoint:

- Ultimo monitor ARX observado: `2026-08-24T23:34:02Z`, modo `dry-run`, `13` checados, issues `0`, created/deduped/resolved/closed `0`, errors `[]`.
- State ainda mostrava issues anteriores inativas, atualizado em `2026-08-22T04:15:22Z`.
- Nao havia issue ARX real atual segura para provar criacao de canario no momento do checkpoint.
- Tentativas create-mode anteriores de 2026-08-18 a 2026-08-22 para `16 Ferreira Rocha` / `servidor_2j3wv` falharam com NinjaOne `HTTP Error 400: Bad Request`; ticket anterior `1692` do mesmo device foi resolvido em 2026-08-15 apos recuperacao.

NinjaOne/RMM canonico:

- URL canonica corrigida: `https://rmm.bikon.com.br`.
- OAuth pendente regenerado com `auth_base=https://rmm.bikon.com.br/ws/oauth/authorize`, `token_url=https://rmm.bikon.com.br/ws/oauth/token`, `api_base=https://rmm.bikon.com.br/v2`, redirect `http://localhost:8756/callback/` e scope `monitoring management offline_access`.
- O token anterior predatava a correcao; nao assumir user-context auth valido ate completar a reautorizacao.

Estado de cron no checkpoint:

- Crons de relatorio NinjaOne sob Kowalski estavam habilitados na janela 07:45-07:48 America/Sao_Paulo.
- Crons de abertura ARX -> NinjaOne ainda estavam desabilitados no DB local: diario `f2b954f0-1c38-46d0-acde-796d3898093f` e semanal `cd7bfa61-30ca-458f-9f62-2679726dfc09`.
- Antes de reabilitar producao, verificar ownership/target conforme o novo modelo de responsabilidade.

Proxima retomada segura: concluir OAuth em `https://rmm.bikon.com.br`, rodar dry-run, inspecionar `summary.errors` e executar no maximo um ticket real canario se houver issue real atual. Registrar ticket id e impedir abertura em massa ate revisao do resultado.

## Relatorios Cartorio Gerusa em 2026-08-26

- Relatorio consolidado junho-agosto/2026 concluido em tres paginas A4, revisado visualmente, sem JavaScript, caminhos locais, nomes de agentes, segredos ou texto tecnico indevido.
- Relatorio mensal de agosto/2026 foi mantido como parcial ate 26/08, com classificacao `ATENCAO`, sem inferir fechamento mensal ou taxa de sucesso ausente na fonte.
- Snapshot parcial de agosto: `5` jobs concluidos, `0` erros ativos, `1.550,7 GB` selecionados e `1.165,6 GB` processados.
- Historico recente: `28` registros, sendo `27` concluidos e `1` concluido com erros; a ocorrencia foi tratada como recuperada, sem inventar data nao retornada pela fonte.
- Os PDFs finais permanecem fora do Brain/Git; a versao consolidada correta substitui o rascunho mensal como entrega, sem apagar o historico parcial.

## Guardrails

- Não imprimir tokens, segredos ou credenciais em respostas, logs consolidados ou Brain.
- Em caso de erro, relatar de forma curta e apontar o caminho do log operacional.
- Não acionar cliente externo nem enviar e-mail apenas por execução bem-sucedida da rotina.

## Relações

- Agente executor observado: Kowalski.
- Categoria: monitoramento operacional / abertura de tickets.
