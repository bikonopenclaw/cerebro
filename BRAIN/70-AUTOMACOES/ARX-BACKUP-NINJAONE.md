# ARX Backup diário → tickets NinjaOne

```yaml
categoria: automacao_monitoramento
fonte: execuções cron Kowalski em 2026-06-19, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-29, 2026-07-02, 2026-07-06, relatorios operacionais ate 2026-08-12, checkpoints de reativacao em 2026-08-24/25, relatorios Cartorio Gerusa em 2026-08-26, qualificacao/ciclo ARX de 2026-09-08 a 2026-09-10, fechamento semanal entregue em 2026-09-14, ciclo diario de 2026-09-15 e request mensal 2111 reconciliado em 2026-09-16
confiabilidade: alta
ultima_revisao: 2026-09-16
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

## Qualificacao da cadeia ARX em 2026-09-08/09

A investigacao separou coleta, render, transporte e leitura humana e preservou o owner canonico: Sentinel coleta/evidencia, Kowalski produz e entrega relatorios, Puppet Master governa autoridade. O job original `879289fc-12e3-44c3-984b-9c7e4fb39221` continua `FAILED` e inativo; nao foi reaberto nem reclassificado como sucesso.

### Diario e Telegram

- A coleta diaria anterior ocorreu em 08/09 03:30 UTC e a entrega no grupo ocorreu em 08/09 10:46:01 UTC, ACK Telegram `messageId 1687` pela conta Kowalski.
- O corpo entregue continha wrappers de stdout/stderr e diagnosticos internos. Foram instalados binding por hashes da evidencia/coleta, validacao de identidade/data/contagens e saida limpa; entrega ja confirmada e suprimida por `NO_REPLY` para impedir duplicata.
- Resultados desconhecidos agora persistem recibo privado `UNKNOWN / UNRESOLVED / HOLD_RECONCILE_BEFORE_RETRY` e retornam hold silencioso, impedindo que callback de falha crie retry ou notificacao enganosa.
- O fluxo corrigido ainda precisa de observacao no ciclo natural: coleta diaria em 09/09 03:30 UTC e entrega em 09/09 10:46 UTC. Teste instalado/no-send nao equivale a entrega natural aceita.
- O ciclo referente a 09/09 produziu artefato em 10/09 03:30 UTC e passou validacao em 10/09 10:46 UTC: 12 contas, 10 clientes, 8 OK, 1 atencao, 0 critico e 3 outros. A validacao registrou `delivery=NOT_REQUESTED`; portanto prova coleta/render validos, nao transporte ou leitura humana, e nao fecha a observacao ponta a ponta.

### Mensal e e-mail

- O source contract anterior expunha apenas estatistica corrente e nao provava um mes-calendario. Foi instalada aquisicao historica nativa, limitada aos quatro dispositivos autorizados, com `GetAccountInfoById`, `QuerySessions` e `QueryErrors`, paginacao exaurida, IDs/periodo/identidade validados e evidencia imutavel.
- Os quatro crons mensais preservaram IDs, horarios de 01/10, timezone, remetente, destinos e owner Kowalski; nao foi criado cron novo nem alterada a rotina diaria/semanal.
- Agosto foi recuperado e renderizado no template aprovado, com Markdown/HTML/PDF idempotentes e `VALIDATED_NO_SEND`: Alzira 744 sessoes registradas/744 sucesso; Camburi 744 registradas, 734 sucesso, 1 com erros e 9 puladas; Capixaba 744 registradas, 742 sucesso, 1 falha e 1 pulada; Vila Velha 743 registradas, 707 sucesso, 1 falha, 1 com erros e 34 puladas.
- Alzira, Camburi e Vila Velha estao `CONFIRMED_NOT_SUBMITTED` apenas nas execucoes historicas autenticadas. Capixaba permanece `UNKNOWN`; um PDF valido ou credencial SMTP de saida nao prova o efeito anterior e nao autoriza retry.
- Nenhum catch-up, SMTP ou Telegram foi enviado na qualificacao. O ciclo mensal natural continua pendente por cliente em 01/10; Vila Velha tambem mantem gate de cobertura aberto porque a consulta nativa nao retornou sessoes em 07/09.

### Regra de evidencia temporal

- Primeiro/ultimo timestamp, nome de arquivo, ACK de transporte ou barra rolante de 28 dias nao provam cobertura mensal.
- Fechamento exige populacao vinculada ao cliente e periodo, paginacao terminal, IDs unicos, dias/lacunas explicitados, classificacoes sem mistura e separacao entre metricas do mes e observacao corrente de retencao/storage.
- Artefato valido, submissao SMTP, aceite do provider, entrega na caixa e leitura humana permanecem estados distintos.

## Fechamento semanal de 2026-09-11 entregue em 2026-09-14

- A fotografia corrente coletada em 12/09 00:36:41 BRT registrou 12 contas de 10 clientes: 9 OK, 1 em atencao, 0 criticas e 2 nao classificadas. Ela foi apresentada explicitamente como snapshot corrente, nao como historico nativo da sexta-feira.
- Nos quatro snapshots historicos disponiveis de 07/09 a 10/09 houve 48 contas-snapshot: 34 OK, 4 em atencao, 0 criticas e 10 nao classificadas. A fonte nao expos eventos completos por job nem o placar historico nativo de 11/09.
- A atencao recorrente foi atribuida a `16 Ferreira Rocha / servidor_2j3wv` de 08/09 a 10/09 e no snapshot corrente; o ultimo backup valido recente reduziu risco imediato, mas nao provou operacao saudavel durante toda a semana.
- Proxima validacao segura: confirmar se o contador de erro do ativo zera em coleta posterior, classificar as duas contas ainda nao classificadas e correlacionar com ticket NinjaOne somente quando a evidencia expuser o vinculo ARX.

## Ciclo diario referente a 2026-09-14

- A coleta autenticada read-only gerada em 15/09 00:30:03 BRT registrou `11` contas de `10` clientes: `10` OK, `1` em atencao, `0` criticas e `0` outras.
- O artefato passou validacao, mas o recibo preservou `delivery=NOT_REQUESTED`; portanto prova coleta/render, nao transporte nem leitura humana.
- O resumo agregado nao expos eventos completos do periodo nem ultimo backup valido por conta. O placar e fotografia corrente e nao deve ser convertido em total de backups executados no dia.

## Relatorio mensal 2111 Alfredo Chaves, 2026-09-15/16

- O pedido referente a agosto/2026 preservou a janela exata de `2026-08-01T03:00:00Z` a `2026-09-01T03:00:00Z` exclusiva, em `America/Sao_Paulo`, mas nao produziu relatorio mensal.
- Tentativas sucessivas falharam fechadas antes de dados validos por invisibilidade do workspace/controlador Sentinel, binding `supersedes` defasado, ausencia do cliente no mapping mensal e credencial inacessivel na rota anterior.
- O caminho hardcoded da credencial foi removido em favor do cofre compartilhado aprovado, com arquivo regular, ownership esperado e modo `600`; os testes fail-closed passaram `7/7`, sem expor o valor secreto.
- A reconciliacao terminal manteve a request canonica como `FAIL_CLOSED_EXTERNAL_OWNER_GATE`: `0` chamadas ao provider, `0` mutacoes, `0` envios externos, `0` evidencia mensal Sentinel e `0` PDF Kowalski.
- O escopo permanece congelado sem criar novo sucessor: faltam binding numerico `PartnerId/AccountId` aprovado pelo proprietario e decisao sobre a permissao nativa Sentinel-only preparada para `api.backup.management`. Nome de exibicao nao autoriza esse binding e snapshot corrente nao substitui historico completo de agosto.

## Guardrails

- Não imprimir tokens, segredos ou credenciais em respostas, logs consolidados ou Brain.
- Em caso de erro, relatar de forma curta e apontar o caminho do log operacional.
- Não acionar cliente externo nem enviar e-mail apenas por execução bem-sucedida da rotina.
- Resultado de entrega `UNKNOWN` deve bloquear retry ate reconciliacao confiavel ou nova autorizacao especifica; regenerar o anexo nao contorna a identidade logica cliente/competencia.
- Timeout de ACK/start em ordem ad-hoc deve fechar a mesma identidade terminalmente; nao autoriza criar sucessor nem acessar provider por rota alternativa.

## Relações

- Agente executor observado: Kowalski.
- Categoria: monitoramento operacional / abertura de tickets.
