---
id: brain-ff506efba7da0ae10837
type: entity
title: SENTINEL, Controller de Operações e SNOC
created: '2026-09-21T19:15:09.943981Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T20:54:07.904960Z'
---

# SENTINEL, Controller de Operações e SNOC

```yaml
nome: Sentinel
papel: controller_operacoes_snoc
status: ativo_capability_registry_controlado_com_mutacao_bloqueada_por_gate
responsavel: Puppet Master
ultima_revisao: 2026-09-19
tags: [sentinel, snoc, operacoes, monitoramento, seguranca, read-only, capability-registry]
```

## Missão

Consolidar a saúde operacional dos clientes, separar sinal de incidente, classificar prioridade e manter evidência, responsável, prazo e estado. Sentinel diagnostica e recomenda; não remedia por conta própria.

## Fontes autorizadas

- NinjaOne por cliente read-only com método `GET` e allowlist interna.
- ARX Backup/Cove pelos métodos JSON-RPC `Login` e `EnumerateAccountStatistics`.
- Excecao ARX mensal estreita e registrada para quatro dispositivos: `GetAccountInfoById`, `QuerySessions` e `QueryErrors`, somente leitura, com periodo, paginacao, identidade, hash e auditoria vinculados a ordem ativa.
- Bitdefender GravityZone pelos métodos de consulta explicitamente permitidos.
- Contexto operacional sanitizado, sem dados fiscais, endereço, telefone ou e-mail financeiro.
- Logs locais autorizados com limite, redação e sem acesso a sessões, mensagens, segredos ou SQLite.

As fontes exatas, clientes permitidos e comandos de validação ficam nos snapshots sanitizados em `BRAIN/60-AGENTES/versionados/workspaces/sentinel/`.

Desde 2026-08-05, a separação canonica ficou registrada assim: Sentinel é o responsável por coleta e consulta em fontes operacionais; Kowalski recebe dados consolidados com fonte, horário UTC, escopo e evidência para interpretar e produzir relatórios no padrão Bikon.

## Limites

- Sem root ou sudo.
- Sem comando remoto, reinício, atualização, isolamento, remediação ou alteração de ativo.
- Sem criar, alterar ou fechar ticket em produção sem aprovação explícita.
- Sem comunicação externa.
- Sem URL, método, caminho ou fonte livre fora das allowlists.
- Sem copiar credencial de outro workspace.
- Sem fallback quando a rota aprovada falhar.
- Sem transformar ausência de evidência em sucesso ou falha confirmada.

## Menor privilégio

- Segredos ficam fora do workspace versionado e devem ter permissão `600`.
- Clientes validam origem, proprietário e permissão antes de usar credencial.
- Saídas contêm somente os campos necessários e sanitizados.
- Auditoria de acesso é append-only e não inclui resposta bruta nem segredo.
- Credenciais compartilhadas são uma segregação operacional, não permissão real do provedor. Essa limitação deve permanecer explícita.

## Revogação

Revogação, rotação, substituição e reativação dependem de autorização do Hebert. Remover arquivo local não revoga acesso no provedor. Depois da revogação, a mesma rota read-only deve comprovar falha; depois da substituição, deve comprovar apenas o escopo permitido. Auditoria e evidências de alteração são preservadas.

Referência: `BRAIN/60-AGENTES/versionados/workspaces/sentinel/access_control/REVOGACAO.md`.

## Governança

- Puppet Master define prioridade, coordena e consolida a decisão.
- Sentinel entrega diagnóstico, severidade, evidência, risco e próxima ação segura.
- Hebert autoriza qualquer mudança real.
- Kowalski interpreta dados coletados pelo Sentinel, produz documento/relatório e preserva o padrão visual Bikon.
- Darth Vader apoia impacto financeiro quando solicitado.
- Robotnik só participa de comunicação educativa ou pública depois da decisão operacional.

## Canário Sentinel v2

Em 2026-07-20, a primeira janela Sentinel v2 entrou em canário read-only com:

- 21 clientes ativos reconciliados;
- janela exata de 24 horas e ciclos de 30 minutos;
- cinco fontes autorizadas e saída sanitizada;
- pausa automática no primeiro P1/P2, falha de fonte, desvio read-only, divergência de escopo ou lacuna de owner/SLA;
- encerramento programado no fim da janela;
- deduplicação, SLA, escalonamento e auditoria append-only.

Essa janela anterior foi posteriormente pausada por `ARX critical=1`, classificado como P2, e preservada no histórico. Ela não comprovou 24 horas sustentadas.

Uma nova janela foi autorizada e iniciou em 2026-07-23 às 14:30:41 UTC, com run ID `b7b4d4ad110ef74744f354f0` e término previsto para 2026-07-24 às 14:30:41 UTC.

Estado reconciliado às 20:03:40 UTC de 2026-07-23:

- `status=active`;
- 12 ciclos executados;
- cinco fontes disponíveis;
- `pause_reason=null`;
- zero P1/P2;
- ARX com `critical=0`, uma conta em atenção e quatro em `other`;
- NinjaOne com 197 alertas agregados;
- Bitdefender com zero incidentes e zero quarentenas.

ARX e NinjaOne permanecem P3 provisórios com confiança baixa enquanto faltarem atribuição única e confirmação de impacto. O padrão de incerteza exige fato, hipótese, severidade, confiança, G1-G5, lacuna, risco, evidência para fechar, freshness/prazo e dono.

O estado `active` da nova janela não autoriza operação 24x7. O parecer depende do encerramento, reconciliação dos ciclos e fechamento dos gates.

## Provimento 213

Em 2026-07-30/31, Sentinel recebeu e avaliou capacidades read-only transferidas do Kowalski para apoiar o OpenClaw - Provimento 213.

Estado consolidado:

- Handover obrigatório inicial ficou bloqueado com `17/25` gaps e paridade `32_PERCENT`, porque WhatsApp/Drive exigiam identidade read-only dedicada e 13 capacidades de management plane não existiam no donor.
- Transferência as-is posterior roteou `7/7` superfícies solicitadas; ARX/Cove falhou inicialmente, depois foi corrigido por cliente Sentinel-owned e passou em uma aceitação read-only fresca.
- Avaliação final do alcance das APIs transferidas executou `27` leituras com sucesso, `0` operações de escrita e `0` mutações externas.
- A superfície transferida melhorou `8/13` domínios de gap, fechou `0` e deixou `5` sem capacidade correspondente: cloud/VM, firewall/roteamento, replicação/snapshot/clone, cleanup/descarte e rollback.
- O registro de alcance read-only foi validado por Kowalski e congelado por checkpoint externo em 2026-07-31.
- A descoberta controlada de provider avaliou AWS, Azure e Google Cloud como rotas tecnicamente qualificadas `5/5`, mas terminou bloqueada por falta de evidência local de conta/tenant/subscription/projeto existente; Sentinel não selecionou provider.
- Sentinel implementou o adaptive evidence interview e dashboard read-only no `prov213-core`; validação independente retornou `PASS`, com `23/23` testes, `48` controles, `77` perguntas, `76` requisitos de evidência e zero side effects externos.
- No primeiro uso controlado, a sessão CNS `024067` ficou `AWAITING_RESPONDENT` com `0` respostas reais e `0` evidências recebidas.
- Na extensão multi-Serventia, Sentinel validou artefatos de apresentação/localização autorados pelo Kowalski e Kowalski validou os artefatos de runtime/estado autorados pelo Sentinel; a suíte ficou `85/85` PASS. Os registros finais autorados pelo Puppet Master ainda exigem validação independente própria.

Limite operacional:

- Sentinel pode diagnosticar e registrar lacunas com leituras sanitizadas, mas não pode ativar source inventory, selecionar target, provisionar, executar preflight, restaurar backup, alterar infraestrutura ou continuar o fluxo sem autorização explícita.
- Próximo passo exato para seleção de provider: `PROVIDE_OR_AUTHORIZE_READ_ONLY_EXISTING_AWS_AZURE_GOOGLE_CLOUD_ACCOUNT_TENANT_SUBSCRIPTION_PROJECT_EVIDENCE_FOR_PROVIDER_SELECTION`.
- Entrevista externa, contato com respondente, envio de PDF, uso operacional de dashboard, provider onboarding, source inventory activation, target selection, provisioning, preflight e restore permanecem bloqueados sem autorização separada.

## Gate de ordem ativa

Em 2026-08-05, o snapshot sanitizado do Sentinel passou a registrar o controlador de ordem ativa em `workspaces/sentinel/orchestration/`.

Regras consolidadas:

- mensagem recebida por sessão é apenas entrada de fila, não autorização técnica;
- toda execução crítica, longa, com GET externo, approval, execution ID, canário, deploy ou alteração exige uma única ordem ativa vinculada a path, SHA-256, approval ID e execution ID;
- antes de credencial, token, GET ou artefato técnico, a rota deve passar por `assert`;
- ordem divergente fecha em `STALE_OR_UNBOUND_ORDER_REJECTED`, sem fallback interpretativo;
- crons não críticos podem ser pausados e restaurados pelo controlador apenas dentro do escopo autorizado.

## Sentinel V2 Goal 1/2

Em 2026-08-21, a auditoria forense e os Goals 1/2 do Sentinel V2 revisaram a diferenca entre capacidade declarada, capacidade real, autoridade de provider e plano de acao controlada.

Goal 1 fechou como `PARTIAL_EXTERNAL_AUTHORITY_BLOCKED`:

- pacote final: `/data/.openclaw/workspace/projects/sentinel/goal1/final/SENTINEL_V2_GOAL1_FOUNDATION_READ_PLANE_20260821T213206Z`;
- manifest SHA-256 `802d2b6847ac8e50e13aefd8923e87b16a4063fe8df35d3eda5e6196730421af`;
- NinjaOne `PASS`;
- ARX/Cove `PASS_WITH_SHARED_CREDENTIAL_LIMITATION`;
- Bitdefender `PASS_WITH_AGGREGATE_IDENTITY_LIMITATION`;
- WhatsApp e Instagram `BLOCKED_EXTERNAL_AUTHORITY`;
- controller final `IDLE`, ticketing produtivo `DISABLED` e contadores mutativos `0`.

Goal 2 Completion fechou como `SENTINEL_V2_GOAL2_RESULT=PASS`:

- pacote final: `/data/.openclaw/workspace/projects/sentinel/goal2/final/SENTINEL_V2_GOAL2_FULL_CAPABILITY_20260821T231003Z`;
- manifest SHA-256 `0ca98716b95724c6c7f5dfdd10fa37952cdf5dc54ffdd9226f952e27418ce801`;
- `TOTAL_REGISTERED_CAPABILITIES=14`;
- `READ_CAPABILITIES=7`;
- `WRITE_ACTION_CAPABILITIES=5`;
- `TICKET_CAPABILITIES=2`;
- recuperacao de capacidades NinjaOne, ARX/Cove, Bitdefender, WhatsApp e Instagram `PASS`;
- provider read parity, provider action parity, ticketing contract, idempotency, negative authority acceptance, secret handover, state ownership, Puppet/Sentinel consumption, Kowalski non-regression, Robotnik non-regression e Golden Baseline `PASS`;
- `00 - Bikon Tech` permanece `CONFLICT`;
- real ticket canary, real action canary, WhatsApp send canary e Instagram publish canary ficaram `NOT_RUN_NO_SAFE_TARGET`;
- `UNAUTHORIZED_MUTATION_COUNT=0`, `REAL_TICKET_MUTATION_COUNT=0`, `REAL_PROVIDER_ACTION_COUNT=0`, `REAL_WHATSAPP_SEND_COUNT=0` e `REAL_INSTAGRAM_PUBLISH_COUNT=0`.

Estado canonico: Sentinel possui modelo controlado de capacidade e contratos para leitura, ticketing e acoes, mas nenhuma mutacao real fica autorizada por inferencia. A primeira execucao real de ticket, provider action, WhatsApp send ou Instagram publish exige alvo seguro, approval proprio, idempotency key, rollback e evidencia.

## Sentinel Phase D Capability Registry

Em 2026-08-26, a Phase D Capability Registry fechou terminalmente como `PASS`, apos tentativas anteriores sem artefato autoritativo e gates de recuperacao que permaneceram nao autoritativos.

Checkpoint autoritativo:

- terminal gerado em 2026-08-26T00:26:55Z;
- diretorio terminal: `/data/.openclaw/workspace/reports/SENTINEL_PHASE_D_CAPABILITY_REGISTRY_20260826T002655Z/`;
- `PHASE_D_CAPABILITY_REGISTRY=PASS`;
- `PHASE_D_INDEPENDENT_VALIDATION=PASS`;
- `AUTHORITATIVE_TERMINAL_DIRECTORY_COUNT=1`;
- `AUTHORITATIVE_TERMINAL_CHECKPOINT_COUNT=1`;
- `TERMINAL_WRITER_COUNT=1`;
- `PROVIDER_MUTATION_COUNT=0`;
- `SCHEDULE_MUTATION_COUNT=0`;
- `PRODUCTION_MUTATION_COUNT=0`;
- `DUPLICATE_CANONICAL_CAPABILITY_ID_COUNT=0`.

Matriz consolidada:

| Provider | Total | Read | Mutative | Owner gated | Provider-scope blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
| ARX/Cove | 34 | 29 | 5 | 5 | 0 |
| Bitdefender | 24 | 14 | 10 | 10 | 0 |
| Instagram/Meta | 15 | 10 | 5 | 5 | 0 |
| NinjaOne | 188 | 77 | 111 | 111 | 0 |
| WhatsApp | 113 | 55 | 58 | 58 | 0 |

Totais:

- `RAW_PROVIDER_CAPABILITY_COUNT=374`;
- `CANONICAL_CAPABILITY_COUNT=374`;
- `TOTAL_READ_CAPABILITIES=185`;
- `TOTAL_MUTATIVE_CAPABILITIES=189`;
- `TOTAL_IMPLEMENTED_CANONICAL=21`;
- `TOTAL_IMPLEMENTED_DONOR_OR_SHARED_ONLY=8`;
- `TOTAL_PARTIALLY_IMPLEMENTED=5`;
- `TOTAL_NOT_IMPLEMENTED=248`;
- `TOTAL_OWNER_APPROVAL_REQUIRED=189`;
- `TOTAL_BLOCKED_PROVIDER_SCOPE=0`.

Estado canonico: Phase D e um inventario autenticado e validado, nao uma autorizacao de uso. Phase E, ticket real, provider action, WhatsApp send, Instagram publish, criacao/alteracao de webhook, politica, device, contato, documento ou qualquer mutacao permanecem bloqueados ate ordem nova, approval proprio, alvo seguro, idempotency, rollback e evidencia.

## Recuperacao de runtime e mapping, 2026-09-07

A manutencao autorizada do mapping/runtime do Sentinel permaneceu `BLOCKED_FAIL_CLOSED` no precheck, preservando o Goal `416a2f2a-db00-4f09-941d-db7c92f81edd` e a correlacao `sentinel-runtime-recovery-416a2f2a-db00-4f09-941d-db7c92f81edd`.

Evidencia consolidada:

- os executores receberam somente `/data/.openclaw/workspace`; config e state ativos, `/data/.openclaw/workspace-sentinel`, agentDir do Sentinel, SQLite, supervisor, gateway/CLI e bus do systemd nao estavam montados ou acessiveis;
- definir `cwd=/data/.openclaw` nao mudou os mounts do sandbox;
- a indisponibilidade local nao autentica defeito, ausencia ou estado do runtime vivo do Sentinel;
- nao houve backup novo, alteracao de config/binding/unit, restart, root/sudo, nova RUN, PGL, chamada a provider, coleta, ticket ou entrega;
- WhatsApp, ARX, NinjaOne e Bitdefender permaneceram `NOT_STARTED_PRECONDITION_BLOCKED`, sem handoff ao Kowalski;
- root nao foi demonstrado como necessario.

Retomada obrigatoria: usar o mesmo Goal e correlacao numa superficie policy-enforced com visibilidade contemporanea do state/config, workspace Sentinel, SQLite, CLI, supervisor, unit/drop-ins e systemd. O precheck deve recomecar do zero, autenticar o alvo vivo e somente depois permitir backups ou correcao. Nao criar Goal substituto nem reenviar a ordem de coleta por inferencia.

## Fonte historica mensal ARX, 2026-09-09

Sob autorizacao estreita, Sentinel passou a adquirir a populacao historica mensal dos quatro dispositivos ARX ja definidos, sem ampliar para outros clientes ou metodos mutativos.

- Aquisicao usa endpoint nativo de historico autenticado, paginas sequenciais, resposta terminal, IDs unicos, limites de tempo e identidade de conta/dispositivo; `QueryErrors` reconcilia as sessoes com erro.
- Evidencia imutavel e contrato de fonte ficam separados dos artefatos de Kowalski. O workflow mensal falha fechado antes do render se periodo, cliente, hashes, paginacao, lacunas ou classificacao nao fecharem.
- Agosto foi recuperado para Alzira, Camburi, Capixaba e Vila Velha; consultas de setembro preservam somente intervalo decorrido e nao qualificam o mes ainda aberto.
- A ausencia de sessoes de Vila Velha em 07/09 permanece lacuna operacional nao classificada: nao prova sucesso, falha nem destruicao de fonte.
- A autorizacao de History nao inclui restore, Recovery Verification ativo, alteracao de backup, envio de relatorio, ampliacao de cliente ou mutacao do provider.

## Requalificacao do ciclo diario ARX, 2026-09-18

- O preflight do runtime real passou com adapter, namespace e referencia de segredo visiveis e contagem zero de exposicao de valor secreto.
- O inspect por isolamento `bubblewrap` foi bloqueado pelo host por ausencia de namespace nao privilegiado. A negativa foi preservada sem alterar permissao ou improvisar fallback.
- Uma primeira qualificacao in-process fechou em `PROVIDER_ATTEMPT_RECONCILIATION_REQUIRED`, mantendo o recibo original e proibindo retry identico automatico.
- Descoberta autenticada read-only posterior encontrou cinco contas configuradas. A qualificacao v2 vinculada por hashes encerrou o ciclo logico `2026-09-17` em `SUCCESS / PASS`, com validacao obrigatoria `PASS`.
- O marco prova a rota nativa de leitura e a producao do artefato do ciclo; nao autoriza ticket, envio, mutacao de provider, cron novo ou ampliacao de escopo.

## Binding ad-hoc ARX e request 2111, 2026-09-15/16

- Ordens ad-hoc ARX/Cove passaram a exigir ativacao unica pelo Puppet e dispatch do coletor canonico com os bindings exatos da ordem ativa. O coletor executa preflight no namespace Sentinel e persiste ACK/start da mesma identidade; mensagens conversacionais nao substituem essas transicoes.
- ACK e start possuem limites de `120` segundos, observados por watchdog independente a cada `30` segundos. Timeout persiste falha terminal e bloqueia a request supervisionada, sem criar sucessor ou chamar provider.
- No request mensal de `2111-Cartorio Alfredo Chaves` para agosto/2026, o caminho hardcoded para credencial fora do workspace Sentinel foi substituido pelo cofre compartilhado aprovado, preservando segredo fora de logs/Brain e validando o loader em `7/7` testes fail-closed.
- A request reconciliada terminou `FAIL_CLOSED_EXTERNAL_OWNER_GATE`, com `0` provider requests, `0` mutacoes e `0` envios. Naquele checkpoint, ficou congelada ate binding numerico `PartnerId/AccountId` aprovado pelo proprietario e decisao sobre permissao nativa Sentinel-only; display name ou inferencia nao sao binding de provider.

## Rework ARX 2111 e terminal de evidencia, 2026-09-16/17

- Com binding numerico e permissao autenticados posteriormente, Sentinel consultou read-only a conta `5452047` do partner `2944584`, preservando recibos de provider e zero mutacao. A resposta mensal nao retornou sessoes suficientes para comprovar os backups de agosto.
- O artefato inicial passou QA, mas foi rejeitado pelo proprietario por insuficiencia do conteudo de negocio. O sucessor duravel preservou a linhagem e ampliou somente a busca causal autorizada, reutilizando resultados validos e evitando leitura duplicada.
- Historico primario, host alternativo, auditoria nativa e retencao foram esgotados sob recuperacao limitada. O resultado terminal foi `EVIDENCE_INSUFFICIENT / PERMANENT_INTERNAL_FAILURE`; nenhuma rota deve converter ausencia de sessoes retornadas em ausencia de backup, sucesso mensal ou autorizacao para novo PDF.
- Falha de uma leitura adicional preserva o recibo original e exige reconciliacao antes de qualquer nova tentativa. Retry identico automatico e proibido depois do terminal permanente.

## Forense passivo Darth 409, 2026-08-23

Sentinel executou investigacao local read-only do conflito Telegram 409 do Darth sem `getUpdates`, canary artificial, restart/stop, token/header/env, root/sudo ou mutacao de producao.

Resultado:

- `DARTH_PASSIVE_409_OBSERVER_RESULT=PASS_NO_LOCAL_DUPLICATE_AT_CONFLICT`;
- 409 genuino capturado em 2026-08-23T19:56:58Z;
- runtime canonico local no conflito: `openclaw-gateway-darth-vader.service`;
- nenhum quarto PID/unit/cgroup local apareceu como poller duplicado;
- Main/Puppet e Kowalski tinham conexoes ao endpoint Telegram comum, mas com providers distintos e sem autoridade sobre a credencial Darth;
- classificacao terminal antes da rotacao: `DARTH_TELEGRAM_DUPLICATE_POLLER_ORIGIN=EXTERNAL_OR_NON_LOCAL_UNRESOLVED`.

A remediacao exigiu acao owner-exclusive fora do Sentinel: rotacao do token no BotFather e binding seguro do novo tokenfile canonico. Sentinel nao deve pedir, receber, imprimir ou transportar token por chat.

## Critério de pronto

Uma ocorrência só está consolidada quando possui fonte, recência, impacto, severidade, responsável, prazo, estado e evidência. Encerramento exige nova coleta que comprove resolução quando o estado depende de ferramenta operacional.

## Complementos reconciliados — lote 6 de 2026-09-21

Na preparação Sentinel de julho/2026, lista de 21 clientes, responsáveis e SLA não bastava para liberar operação: faltavam vínculos dos IDs NinjaOne/ARX/Bitdefender com client_id e cobertura esperada. IDs técnicos e evidência são preparados pelo agente; o usuário decide fontes esperadas, mínimos/exceção e aprovação do vínculo. Interface de aprovação não deve transferir 24 colunas técnicas ao usuário. Cadastro completo não prova cobertura real 24x7. Fonte: unidades 31504, 31513.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

No desenho inicial read-only do Sentinel, responsável significa humano ou função Bikon que assume o incidente; o agente detecta e escala. SLA de reconhecimento/escalonamento não é disponibilidade da rede. Janela de manutenção pertence à intervenção planejada e não deve bloquear leitura pura; prazos exemplificados não são contratos aprovados. Fonte: unidades 36206.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

Contrato OAS3 deve ser autenticado nos bytes do YAML/JSON local, com proveniência ao pacote autorizado, paths/operações/schemas e refs resolvíveis offline. Hash de Markdown da autorização não identifica OAS3. Zero candidato ou múltiplos sem identidade inequívoca bloqueiam; não reconstruir do HTML nem escolher outro parseável. Approval deve vincular execução, caminho, hash, finalidade, uso único/expiração; descrever uma API não autoriza chamá-la. Fonte: unidades 33680.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

Uma baseline pode servir ao desenho de supervisor/modelo/isolamento sem provar equivalência funcional. Na preparação Sentinel, PDF/dossiê/QA visual não substituíam ciclos reais de alerta NinjaOne, agregado ARX e decisão Bitdefender. Comparar os mesmos inputs sanitizados, preservando decisões materiais, pause state e findings; diferenças editoriais não bloqueiam, divergências operacionais devem ser classificadas. Não copiar credenciais, transcritos, identidade ou permissões amplas do donor. Fonte: unidades 33617, 8582.

O manifesto histórico de contexto operacional Sentinel usava client_id exato para associar exceções, separava owners/SLA padrão de overrides por cliente e registrava fonte, data de alteração, exportação e hash. Naquela planilha, C=Não selecionava padrão e C=Sim override; o nome genérico do campo inheritance_flag não deve inverter essa regra. Revalidar planilha/schema antes de reutilizar; manutenção estava opcional e não configurada naquele snapshot. Fonte: unidades 29740.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 12 de 2026-09-21

Na matriz G0 de19/07, havia280célulasPENDENTE, mas o conjunto autorizado de decisão tinha52. Formatação limitada não alterou valores/fórmulas. As17decisõesARX REVISAR tornaram-se não bloqueantes paraG0 por regra expressa, sem equivaler aAPROVAR nem autorizar uso fora do gate. Hashes lógicos de21linhas precisaram ser recalculados após edição manual. G0PASS e0bloqueios de matriz não comprovaram prontidão de produção recorrente: runbook, credenciais, janela, duplicação efalse-green ainda eram questões próprias. Estado histórico não redefine política atual. Fonte: unidades 8721.

Na proposta histórica SentinelR3, incidenteP1/P2 atribuído pausava; agregado crítico sem atribuição suficiente provocava protective_hold_unresolved_critical imediato com severidade nula; agregado não crítico incompleto era dívida de evidência. Timeout dessa dívida (480min no desenho) não se convertia artificialmente emP2. Agente, motor determinístico e Puppet eram camadas distintas: build isolado podia avançar, mas implantação exigia política restrita, envelope sanitizado e prova de runtime. Aceiteoffline não equivalia à homologação real. Não ativar estados/prazos pela nota histórica. Fonte: unidades 37018.

No piloto read-only de19/07/2026, a fonte local indicava owner/SLA ausentes para21/21, embora a planilha validada tivesse21 completos (13padrão/8exceções). A inspeção encontrou safe_client forçando not_configured, portanto ausência na projeção não demonstrava ausência na origem. Rodada parou antes de APIs externas; reconciliação requeria vínculo porclient_id/proveniência, sem inferir janela de manutenção. Situação histórica, não diagnóstico atual nem autoridade para editar clientes. Fonte: unidades 41456.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 13 de 2026-09-21

Na preparação SentinelR4, equivalência parcial permitia offline/shadow condicionado, não canário. Advisory-only deveria provar recomendação determinística de owner/destino sem reassignment real. Divergência P2/continue exigia distinguir semântica do campo, elegibilidade no evento, mudança intencional de política ou erro do resumo. Medir duração/overlap/processo residual contra deadline configurado sem inventar limite. O shadow histórico limitava-se a2ciclos ou30min e terminava antes de canário; autorização antiga não é vigente. Fonte: unidades 33623.

Consolidar junto41456: planilha histórica diretamente lida confirmava padrão e8exceções, enquanto safe_client anulava owner/SLA na projeção. Autoridade está no mapeamento porclient_id e proveniência, não em nome/default inferido do resumo. Janela de manutenção vazia era opcional somente para aquele piloto read-only. Fonte: unidades 41459.

Goal5B histórico teve bloqueio por descoberta rootcrontab, depois superado por evidência humanaPASS_EMPTY. Criou15sucessores para17agendas, consolidando2paresARXduplicados. Mutativos/comunicação tiveram predecessores desativados antes de ativar sucessores; auditoria pós-corte relatou old_active0/new_inactive0/duplicatas0. Validador legado falhou por esperarjobs.json quando autoridade eraSQLite: isso não invalida por si o cutover. O trecho ainda pendia pacote/baseline final; não presume estado atual nem requer repetir rootgate antigo. Fonte: unidades 31205.

Fechamento da equivalência classificou P2+continue de Kowalski como SEMANTIC_MAPPING_DIFFERENCE: continue significava rotina sem falha, não decisãoSNOC de não pausar. Sentinel mantém pausa individualP2atribuível; não comparar os enums diretamente nem descartar findings corretos. Aceite histórico PASS_WITH_INTENTIONAL_SEMANTIC_MAPPING preservava advisory-only/semcopiarpermissões e não liberava canário. Consolidar com33623 como evolução resolvida, não pendência atual. Fonte: unidades 8591.

Consolidar com41456/41459: safe_client anulava campos daorigem; aguardo de decisão era checkpoint histórico, não determinação vigente nem prova de owner/SLA ausentes hoje. Fonte: unidades 41462.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch13-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 14 de 2026-09-21

A decisão humana “Sentinel coleta tudo” já aparece em 26/07/2026, seguida de confirmação interagente: coleta/consulta exclusiva nas fontes operacionais autorizadas pelo Sentinel, handoff ao Kowalski com fonte, horário UTC, escopo e evidência sanitizada para interpretar/formatar. Não manter coleta paralela no Kowalski nem inferir novas permissões de fontes; Puppet acompanha mudanças de prioridade, gate ou risco. A menção canônica a 05/08 registra consolidação posterior, não necessariamente a primeira decisão. Fonte: unidades 33693.

Na correção ARX de 17/07, status passou a emitir somente ok, accounts, clients, current_status, write_methods_exposed e audit; audit continha correlation, timestamp_utc e client_sha256 obtidos após append-only bem-sucedido. Redigir campos de um payload bruto não substitui allowlist explícita de saída. A única leitura retornou 11 contas/10 clientes/attention=1, escrita indisponível: corrigir sanitização não resolve a ocorrência operacional. Consulta direcionada posterior foi autorizada separadamente, sem herdar ticket, remediação ou avanço de fase. Counts e estado são históricos. Fonte: unidades 36768.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch14-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

Após o fechamento da diferença continue/pause como SEMANTIC_MAPPING_DIFFERENCE, a fonte 8595 registra uma ordem executiva posterior e distinta: shadow advisory-only por até dois ciclos ou 30 minutos, e canário por um ciclo ou 15 minutos somente após SHADOW_PASS ou PASS com diferença intencional. Kowalski permanecia referência, sem copiar identidade/permissões; ações externas continuavam proibidas. Essa autorização condicional não comprova execução dos ciclos e não elimina SOURCE_SCHEMA_READY para o adapter definitivo. A nota da unidade 8591 descreve o gate anterior, sem autorização de canário; reconciliar pela cronologia, não como contradição a resolver apagando restrições. Fonte: unidades 8595.

Em 19/07, a implementação já aplicada do mapa operacional foi inspecionada: 21 IDs exatos, 13 owners padrão e 8 overrides por aliases, SLA completo, modo 0600 e ausência de PII. A associação usou client_id, sem alterar cadastro mestre; o defeito estava na apresentação safe_client. Manutenção permaneceu opcional e G6 órfão fora do piloto. A existência do patch não bastou: foi necessária validação contra manifesto em memória antes de nova rodada. Este fechamento supera a pendência de reconciliação anterior, mas não comprova execução do piloto seguinte nem produção 24x7. Fonte: unidades 41480.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 18 de 2026-09-21

Na auditoria interna de 19/07, owner/SLA estavam completos para 21/21 clientes (13 padrão e 8 exceções), enquanto o vínculo determinístico completo entre client_id e as três plataformas era 0/21 nas fontes autorizadas inspecionadas. Havia 21 valores fiscais preenchidos, mas somente 20 únicos; nem nome nem esse campo podiam funcionar como chave universal. ninjaone-client-map.json era política de encaminhar ARX à triagem interna Bikon, não cadastro de organizações de clientes. Atribuição pontual de um incidente não prova crosswalk geral. Manutenção continuava opcional, e célula órfã G6 não deveria ser promovida por inferência. Esse é resultado delimitado às fontes/data, não afirmação de inexistência global ou estado atual. Fonte: unidades 8649.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch18-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 21 de 2026-09-21

A lista histórica de clientes vinculados operacionalmente à Corpus não se limitava à organização Corpus Soluções (ID 16). Os caches de junho/julho distinguiam Rio Novo do Sul (ID 44; código 2015 depois 2102), Presidente Kennedy (ID 46; 2017 depois 2106) e João Neiva (ID 51). Essa associação por conhecimento/cache não prova hierarquia formal pai-filho da API nem cadastro atual. Em consulta separada de 18/08/2026 às 20:03:51Z, o relato registrou 659 dispositivos, maior ID 719 e 69 IDs de 651 a 719, com created exposto e zero mutações: quantidade de dispositivos, maior identificador e data real de criação são medidas distintas. O bloqueio anterior por falta de ordem foi superado por uma ordem read-only específica, sem ampliar autoridade operacional por memória. Fonte: unidades 36844.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch21-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
