---
id: brain-fbd5bebde43f9b4077a9
type: state
title: ARX Backup diário → tickets NinjaOne
created: '2026-09-21T18:53:54.531182Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:08:05.502633Z'
---

# ARX Backup diário → tickets NinjaOne

```yaml
categoria: automacao_monitoramento
fonte: execuções cron Kowalski em 2026-06-19, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26, 2026-06-29, 2026-07-02, 2026-07-06, relatorios operacionais ate 2026-08-12, checkpoints de reativacao em 2026-08-24/25, relatorios Cartorio Gerusa em 2026-08-26, qualificacao/ciclo ARX de 2026-09-08 a 2026-09-10, fechamento semanal entregue em 2026-09-14, ciclo diario de 2026-09-15 e requests mensais/qualificacao nativa reconciliadas em 2026-09-16/19
confiabilidade: alta
ultima_revisao: 2026-09-19
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
- Naquele checkpoint, o escopo permaneceu congelado sem criar novo sucessor: faltavam binding numerico `PartnerId/AccountId` aprovado pelo proprietario e decisao sobre a permissao nativa Sentinel-only preparada para `api.backup.management`. Nome de exibicao nao autoriza esse binding e snapshot corrente nao substitui historico completo de agosto.

## Rework mensal 2111 e esgotamento de evidencia, 2026-09-16/17

- Depois da autorizacao e do binding numerico autenticado, a request duravel `DW-12bc23c0ea0b5e4ec41480df` consultou a conta `5452047` sob o partner `2944584`, produziu PDF e passou QA. A leitura mensal retornou zero registros e nao sustentou volume, falhas, taxa de sucesso ou pontos de recuperacao; o proprietario rejeitou o artefato por nao mostrar os backups realizados.
- O predecessor ficou preservado como `REWORK_REQUIRED / OWNER_REJECTED`, sem apagar o sucesso tecnico anterior. O sucessor `DW-378186a1a4d61eb0b026fa6a` manteve a linhagem e executou recuperacao limitada da mesma request, sem envio externo nem mutacao do provider.
- A resolucao reutilizou evidencia valida e esgotou as hipoteses causais autorizadas: historico primario, host alternativo autenticado, auditoria nativa e descritores de retencao. Uma leitura falha preservou o recibo original e bloqueou retry identico automatico.
- O terminal canonico do sucessor foi `TERMINAL_INTERNAL_FAILURE / EVIDENCE_INSUFFICIENT`, com primeiro rompimento na etapa `collect`. Nao produzir novo PDF nem repetir consulta identica: retomada depende de nova fonte causal capaz de provar as sessoes de agosto ou de nova decisao explicita do proprietario sobre uma saida honesta com a lacuna declarada.

## Política de dados disponíveis e relatórios concluídos, 2026-09-17/18

- Um novo pedido literal por “dados disponíveis” não reabre o predecessor de agosto nem herda seu contexto. Ele ativa, apenas para a request nova, `AVAILABLE_AUTHENTICATED_DATA_V1`: observações autenticadas podem compor produto honesto quando datas reais, cobertura e limitações estiverem explícitas.
- Alfredo Chaves, Cartório Capixaba, Cartório Camburi e Cartório Vila Velha concluíram requests novas com PDF autenticado, QA `PASS`, delivery privado `ACKNOWLEDGED`, `customer_delivery=false` e `provider_mutation=false`.
- Alfredo Chaves usou `31` sessões retidas autenticadas, deixando claro que a cobertura não prova o mês inteiro. Capixaba e Camburi usaram `190` registros autenticados cada; Vila Velha usou `134` registros, dos quais `122` execuções, `121` sucessos, `1` com erro e `12` skips.
- Métrica válida continua limitada ao recorte temporal e à evidência de origem. “Dados disponíveis” não permite omitir lacunas, converter ausência em zero nem generalizar observação parcial para todo o mês.

## Requalificacao nativa e revisoes mensais, 2026-09-18/19

- O preflight no runtime Sentinel confirmou namespace, adapter e referencia de segredo legiveis, com `SECRET_VALUE_EXPOSURE_COUNT=0`. O inspect isolado por `bubblewrap` falhou por indisponibilidade de namespace nao privilegiado e nao foi contornado por repeticao ou alteracao de permissao.
- A primeira qualificacao in-process preservou o recibo e fechou em `PROVIDER_ATTEMPT_RECONCILIATION_REQUIRED`; uma descoberta autenticada posterior identificou cinco contas configuradas. A qualificacao v2, com input e codigo vinculados por hash, encerrou o ciclo logico `2026-09-17` em `SUCCESS / PASS`, sem envio, ticket ou mutacao.
- O pedido Alzira terminou `SUCCESS`, QA `PASS` e delivery privado `ACKNOWLEDGED`, usando `192` execucoes autenticadas do recorte de setembro: `191` sucessos, `1` falha e taxa de `99,4792%`. Houve uma recuperacao causal depois de falha no QA visual.
- O pedido Cartorio Capixaba terminou `SUCCESS`, QA `PASS` e delivery privado `ACKNOWLEDGED`, com `190` execucoes autenticadas e `100%` de sucesso no recorte observado. Cinco recuperacoes causais preservaram a mesma request, as versoes anteriores e os recibos enquanto corrigiam contrato/prova visual e revisoes de apresentacao.
- No Capixaba, a versao final entregue separou o placar verde `SEM FALHAS NO RECORTE · 01–08/09` da posicao historica de armazenamento em vermelho. Essa correcao de negocio nao alterou a evidencia do provider e nao converteu o terminal tecnico em aceite de negocio automatico.

## Guardrails

- Não imprimir tokens, segredos ou credenciais em respostas, logs consolidados ou Brain.
- Em caso de erro, relatar de forma curta e apontar o caminho do log operacional.
- Não acionar cliente externo nem enviar e-mail apenas por execução bem-sucedida da rotina.
- Resultado de entrega `UNKNOWN` deve bloquear retry ate reconciliacao confiavel ou nova autorizacao especifica; regenerar o anexo nao contorna a identidade logica cliente/competencia.
- Timeout de ACK/start em ordem ad-hoc deve fechar a mesma identidade terminalmente; nao autoriza criar sucessor nem acessar provider por rota alternativa.
- PDF valido e QA aprovado nao compensam evidencia mensal insuficiente nem aceite negativo do proprietario; produto, suficiência factual e aceite sao gates separados.
- A política `AVAILABLE_AUTHENTICATED_DATA_V1` é exceção explícita por request, não relaxamento global do gate de performance mensal.
- Apresentacao corrigida dentro da mesma request deve preservar artefatos/recibos anteriores, usar revisionamento imutavel e impedir replay do mesmo input depois da barreira de efeitos.

## Relações

- Agente executor observado: Kowalski.
- Categoria: monitoramento operacional / abertura de tickets.

## Conhecimento recuperado dos históricos — revisão 2026-09-21

No fluxo histórico de e-mail ARX, Hebert pediu uma cópia oculta para a caixa funcional de backup da Bikon. Preservar a exigência de BCC no contrato de entrega aplicável, mantendo destinatário exato na configuração operacional e revalidando a regra vigente antes de enviar; isso não autoriza envios adicionais. Fonte: unidades 36273.

Na configuração histórica dos envios ARX, Hebert pediu criação sequencial por cliente. Cada agendamento deve vincular cliente inequívoco, período, dia/horário, destinatários, modelo validado e regra de cópia; validar o primeiro antes de passar ao próximo. Esta recuperação não reativa agendas antigas nem autoriza novos destinatários. Fonte: unidades 36294.

No episódio de aprovação do modelo diário ARX, Hebert pediu guardar o modelo aprovado para reutilização pelo Kowalski. A versão submetida havia retirado a seção de seleção protegida quando não havia lista explícita das pastas. A regra durável é separar modelo aprovado de artefato em validação e não preencher seleção de backup por inferência; recuperar a versão vigente por identidade verificável antes de reutilizar. Fonte: unidades 36366.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.

## Complementos reconciliados — lote 4 de 2026-09-21

No caso histórico do ARX, foi removida a barra sempre verde: cores/severidade devem representar dados reais da fonte, inclusive falhas. O relato identificava TB como janela rolante de 28 dias e outros campos por fonte; validar esses campos no schema consultado. Uma barra rolante correta ainda não prova cobertura integral de mês-calendário. Fonte: unidades 36333, 36327.

Escopo histórico solicitado para ARX Backup: relatórios em português do Brasil, separados por cliente, com capacidade de preparar e-mail ou job de envio limitada a esse produto. Preparação e envio real continuam etapas distintas; destinatário, modelo e autorização devem ser validados pelo contrato aplicável. Fonte: unidades 36267, 32001.

No gerador histórico NinjaOne, um alerta vinculado a dispositivo precisou ser relacionado ao cadastro do dispositivo para chegar à organização/cliente. Antes de agregar alertas por cliente, validar as chaves e cardinalidade do schema efetivamente consultado; não supor que o evento traz diretamente organizationId. Sem vínculo inequívoco, manter o alerta não atribuído em vez de inventar cliente. Fonte: unidades 31926.

Na padronização histórica de quatro crons mensais ARX, a alteração autorizada foi somente assunto e corpo do email. Agenda, destinatários e BCC deveriam permanecer preservados; uniformizar apresentação não autoriza mudar distribuição ou criar novos envios. Fonte: unidades 36308.

No desenho histórico ARX, relatório diário significa recorte de backup das últimas 24 horas e usa modelo próprio; não é o resumo de tarefas realizadas pelo agente. Diário e mensal exigem fonte, período e aprovação correspondentes, sem reaproveitar o nome de um para afirmar cobertura do outro. Fonte: unidades 36347.

No ciclo inicial de ARX→NinjaOne, o usuário pediu centralizar tickets em 00 - Bikon Tech, com cliente no título, evitando remapear automaticamente para organização final do cliente. Registrar como decisão histórica de roteamento, sujeita ao contrato vigente; não migrar tickets nem conceder autorização de criação em massa. Fonte: unidades 36443.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.

## Complementos reconciliados — lote 5 de 2026-09-21

Na integração de 15/06/2026, ARX/Cove foi identificado como JSON-RPC: login com partner/usuário/credencial retornava uma sessão visa; chamadas usavam query e Columns, e a estrutura observada incluía result.result.Settings. A presença de segredo em respostas exigia saneamento antes de guardar evidência. São observações daquele conector, não contrato atual garantido; não registrar visa, senhas ou inventário bruto no Brain. Fonte: unidades 32017, 32080.

O checkpoint de 15/06/2026 consolidou relatórios em português brasileiro e separados por cliente, templates aprovados como referência, preparação de e-mails sem disparo automático, separação CNAB400/CNAB240 e conector ARX/Cove JSON-RPC. Falhas de autenticação e bloqueio de comunicação descritos ali eram estado transitório; não reexecutar tentativas de credenciais, restaurar configurações ou tomar listas de arquivos modificados como prova do runtime atual. Os detalhes de custódia permanecem apenas como caminhos lógicos, sem segredos. Fonte: unidades 32059.

No desenho dos relatórios ARX de 16/06/2026, o BCC padrão solicitado era backup@bikon.com.br, enquanto o contato apresentado ao cliente era backup@arxcore.com.br. Preparação de job distinguia cliente, dia/horário e destinatários. Preservar essa separação entre identidade pública e cópia interna, sem confundir documentação histórica com configuração de envio vigente ou autorização de novos disparos. Fonte: unidades 36274, 36295, 36310.

Em 16/06/2026 foram relatados agendamentos mensais ARX separados para Alzira, Camburi, Capixaba e Vila Velha, dia 1 às 08:00 GMT-3. Esse é o desenho inicial: disponibilidade da agenda e execução posterior exigem recibos próprios e configuração autenticada; não reativar jobs antigos por esta memória. Fonte: unidades 36298, 36301, 36304, 36307.

Na implantação ARX→NinjaOne de 16/06/2026, o usuário pediu centralizar os alertas na organização interna 00 - Bikon Tech enquanto nomes/clientes não estavam mapeados com segurança. O título final foi corrigido para Alerta de ARX Backup - Nome do cliente, após erro AARX. Esse fallback era específico daquele desenho; não substitui vínculo estável aprovado entre cliente, ativo e fonte, nem autoriza hoje abrir tickets na organização errada. Fonte: unidades 36430, 36439, 36445, 36454.

No dry-run inicial de ticketing ARX, o prefixo numérico15 produziu associação incorreta entre Vila Velha e RI Marabá. Resolver identidade por cadastro/ID canônico ou mapeamento explícito validado; prefixo ou nome parecido não confirma cliente e não autoriza ticket na organização presumida. Fonte: unidades 36428.

Na ativação histórica ARX, criar o cron não autorizou forçar execução imediata dos tickets detectados. Configuração, primeira execução real e abertura de tickets são ações distintas; manter autorização específica e deduplicação. Horário08:15 daquele episódio não é grade vigente. Fonte: unidades 36434.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
