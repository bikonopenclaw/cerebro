# OpenClaw RSE

```yaml
nome: OpenClaw RSE
status: production_capacity_governed_lifecycle_repair_m2_staging_active_not_frozen
responsavel: Puppet Master
inicio: 2026-08-18
fim:
prioridade: alta
ultima_revisao: 2026-08-29
tags: [openclaw, rse, execution-foundation, fail-closed, stage4, production, bounded-execution-tree-recovery, capacity-governance, lifecycle, durable-deferral]
```

## Objetivo

Governar a fundacao de execucao RSE do OpenClaw por fases verificaveis, mantendo separacao entre preparacao, validacao independente, instalacao, canary e autoridade de mutacao real.

O Brain registra somente estado consolidado e guardrails. Artefatos, bundles, manifests e evidencias detalhadas permanecem em `projects/RSE/`, fora do Brain/Git.

## Estado consolidado

Stage 4 Phase A foi fechado em 2026-08-18 como `ACCEPTED_FROZEN`.

O fechamento aceita e congela:

- fundacao de execucao OpenClaw Stage 4 Phase A;
- remediacao direcionada P1;
- evidencia de determinismo de app-policy;
- bundle hermetico V3;
- validacao independente Kowalski V3 `PASS`.

Autoridade fonte no fechamento:

- repository HEAD `7b9a9c7516afdb6d141618c871fbe17e02889887`;
- tree `1fbd9dd911607e2576b418a3f8b6d8aa7543029e`;
- digest canonico do child congelado com `103` arquivos: `823a700c704f431b915b577684ba769c323637248c271471d9c926a3419b07d4`.

Estado operacional preservado:

- politica RSE instalada: `SHADOW`;
- live mutation adapters: `INERT`;
- production targets: `0`;
- mutation targets: `0`;
- production/OpenClaw restart atribuivel ao fechamento: `0`;
- Phase B: nao iniciada pela aceitacao Phase A.

## Stage 4 Phase B child

Em 2026-08-18, foi preparado um child Stage 4 Phase B de leitura/execucao como pacote nao produtivo, independentemente enderecavel e pendente de validacao independente.

Estado do child:

- status: `PREPARED_NON_PRODUCTION_PENDING_INDEPENDENT_VALIDATION`;
- classificacao: `NON_PRODUCTION_PREPARATION_ONLY`;
- modo instalado atual permanece `SHADOW`;
- adapters live permanecem `INERT`;
- instalacao e ativacao nao autorizadas;
- producao, systemd, runtime OpenClaw live, Storage Growth Guard, OCOT e SQLite produtivo nao sao mutation targets;
- adaptadores de producao falham fechado;
- testes permitidos apenas offline/fixture/mock/fake runtime/temp SQLite/static;
- next gate: `KOWALSKI_INDEPENDENT_STAGE4_IMPLEMENTATION_VALIDATION`.

Dominios implementados no child preparatorio:

- observation authority and validity;
- memory action decision/offline execution;
- restart action decision/budget/offline execution;
- SQLite eligibility/transaction/offline execution;
- recovery hold and safe mode;
- deterministic action precedence;
- action-scoped authorization validation;
- zero-action and inert canary;
- semantic hash chained action evidence;
- coexistencia com Storage Growth Guard.

## Guardrails

- `AUTHORIZE_RSE_PRODUCTION_ACTIVATION` e apenas envelope de coordenacao de release; sem grant de dominio especifico, memoria, restart e SQLite permanecem inertes.
- Token generico nao autoriza action domain, target, restart, SQLite, memoria ou mutacao cruzada.
- Cada acao exige bindings atuais de politica, manifest, design, runtime, evidence head, nonce, expiracao, revogacao, idempotency key, limite de acao, lock single-writer e rollback/recovery boundary.
- PID ou cgroup observado serve como evidencia hash, nao como autoridade de target.
- Phase B, instalacao, canary e producao exigem gates proprios e validacao independente antes de qualquer mutacao.

## Atualizacao 2026-08-20/21

Evidencia local posterior indicou ativacao produtiva estritamente limitada do RSE:

- `CURRENT_RSE_MODE=PRODUCTION`;
- `LIVE_MUTATION_ADAPTERS=BOUNDED_EXECUTION_TREE_RECOVERY`;
- `ENABLED_MUTATION_DOMAINS=EXECUTION_TREE_RECOVERY`;
- `ACTIVE_EXECUTION_TERMINATION_DEFAULT=FORBIDDEN`;
- `GATEWAY_RESTART_POLICY=ESCALATION_ONLY`;
- `HOST_REBOOT_POLICY=FORBIDDEN`.

A evidencia final de producao registrou:

- manifest final com `179` entradas;
- candidate SHA-256 `31f02863bc249b813f2a346faf7e7bdb474ac41c79b3fcaa3ecadf018b3f2b13`;
- `FINAL_CANDIDATE_VERIFICATION=PASS`;
- `RELEASE_RESIDUES=ZERO`;
- `PREDECESSOR_CANDIDATE_INTEGRITY=PASS`;
- `PRODUCTION_ACTIVATION_AUTHORITY=PASS`;
- `WRITERS=ZERO`;
- `RSE_READER_REAL_V2_RECORD=PASS`, com `19` registros validos e `0` invalidos;
- hash chain `PASS` para canary e producao;
- canary semantic evidence `PASS`;
- `PRODUCTION_NORMAL_CYCLES=3`;
- `PRODUCTION_SIGNALS=0`.

Este estado nao autoriza dominios adicionais. Memoria, restart, SQLite, terminacao ativa, gateway restart, reboot, novos adapters live e qualquer mutacao fora de `EXECUTION_TREE_RECOVERY` continuam exigindo approvals e gates proprios.

## Capacity-Aware Execution Governance v1

Em 2026-08-22, o RSE Capacity-Aware Execution Governance v1 fechou `PASS` em producao.

Evidencia consolidada:

- pacote successor: `/data/.openclaw/workspace/projects/RSE/openclaw-rse-execution-pack-v1.0.0/rse-capacity-aware-execution-governance-v1-production-successor-20260822T003248Z`;
- evidencia de producao: `/data/.openclaw/workspace/projects/RSE/rse-capacity-governance-v1-production-evidence-20260822T004212Z`;
- predecessor SHA-256 `31f02863bc249b813f2a346faf7e7bdb474ac41c79b3fcaa3ecadf018b3f2b13`;
- successor SHA-256 `5c72cb05f796434cdd8aff9240c1ee5de69246e3dadac5c73f0e5d2c37a11336`;
- installed implementation manifest SHA-256 `20ed7430d27ce2a41c4d244bc49ed7c9c4317421966df0191673bd8d98509106`;
- evidence manifest `37` entradas, SHA-256 `4aae90089b30cae124130711d91850b9fdec5146820104c1903e62334b0afcaf`;
- `EXISTING_PUPPET_TASK_CLASSIFIER_INTEGRATION=PASS`;
- `EXECUTION_RESOURCE_PROFILING=PASS`;
- `HISTORICAL_RESOURCE_MODEL=PASS`;
- `DYNAMIC_HOST_CAPACITY_MODEL=PASS`;
- `PLATFORM_RESERVE_MODEL=PASS`;
- `DYNAMIC_SAFETY_HEADROOM=PASS`;
- `CAPACITY_AWARE_ADMISSION_CONTROL=PASS`;
- `FIXED_CONCURRENCY_LIMIT=NONE`;
- `DEFERRED_EXECUTION_QUEUE=PASS`;
- `AUTOMATIC_REEVALUATION=PASS`;
- `FAIRNESS_AGING=PASS`;
- `PRESSURE_ADMISSION_FREEZE=PASS`;
- `RUNTIME_PRESSURE_GOVERNANCE=PASS`;
- `ORPHAN_PROCESS_TREE_RECOVERY=PASS`;
- `REGISTRY_COVERAGE_ALL_MANAGED_EXECUTIONS=PASS`;
- `UNREGISTERED_MANAGED_EXECUTION_SCOPE_COUNT=0`;
- `SIGNAL_AUTHORITY_ABORT_NONFATAL=PASS`;
- `RSE_SELF_SURVIVAL_UNDER_PRESSURE=PASS`;
- `HARDWARE_ADAPTIVITY_8G/16G/32G=PASS`;
- `NO_CONCURRENCY_CONFIGURATION_CHANGE_BETWEEN_HOST_SIZES=PASS`;
- `PUPPET_TELEGRAM_RESPONSIVENESS=PASS`;
- `CONTROLLED_PRODUCTION_CANARY=PASS`;
- `CANARY_PRODUCTION_TARGETS_SELECTED=ZERO`;
- `CANARY_PRODUCTION_TARGETS_SIGNALED=ZERO`;
- `RSE_TIMER_ACTIVE=YES`;
- `RSE_CONTROLLER_HEALTH=PASS`;
- `P0_BLOCKERS=0`;
- `P1_BLOCKERS=0`;
- `ROLLBACK_READY=YES`;
- `ROLLBACK_RESULT=PASS`;
- `UNRELATED_PRODUCTION_MUTATIONS=ZERO`;
- `PRODUCTION_SQLITE_UNINTENDED_MUTATIONS=ZERO`;
- `UNRELATED_PROCESS_SIGNALS=ZERO`.

Contrato canonico: Puppet continua dono de intencao, classificacao e colocacao foreground/background. RSE nao reclassifica a tarefa; ele consome o perfil de recurso e governa admissao, fila, pressao, reserva atomica e capacidade. A terminacao ativa segue proibida por padrao; pressao congela admissoes caras e preserva trabalho legitimamente em execucao.

## Incidente de lifecycle e Checkpoint B1, 2026-08-27/28

A qualificacao do onboarding ODP provou um defeito estrutural fora do workload de negocio:

- o child pode ser criado antes da decisao de admissao RSE;
- o caller fica bloqueado em `rse-capacity --wait` durante uma deferral;
- a sessao/registry pode terminar enquanto a admissao ou o processo fisico continua vivo;
- perfis equivalentes do workload ODP oscilaram entre aproximadamente 805 MB e 5,77 GB, e uma execucao admitida sob o perfil menor chegou a aproximadamente 6,95 GB;
- houve evidencia de registry terminal enquanto o cgroup ainda produzia heartbeat.

Consequencia: fila RSE, child/subagent, execution registry e processo/cgroup nao possuem hoje uma unica verdade canonica de lifecycle. O reparo precisa estabelecer admission-before-child, deferral duravel sem espera no gateway, execution ID estavel, ativacao exatamente uma vez e proibicao de terminal enquanto o cgroup canonico estiver vivo.

Contencao preservada com verdade historica:

- admissao `0705a63f-2759-4a53-b5fb-561e4913a2e9`: `RECONCILED_STALE`, motivo `DEFERRED_REQUEST_LEASE_EXPIRED`; processo e cgroup ja ausentes;
- uma tentativa de contencao pelo caminho antigo criou a admissao tecnica `8dbc88f6-126e-4de4-ada0-8014f83153c4`, confirmando a dependencia circular e proibindo novo retry pelo mesmo mecanismo;
- restore point foi reautenticado antes do B1.

O B1 foi autorizado somente como construcao/staging em clone user-owned autenticado e unit transitoria `systemd --user`, sem RSE admission, `rse-capacity --wait`, deploy, `/opt`, runtime live ou mutacao ODP/EDC de producao. A unit terminou em 2026-08-28 com patch e testes parciais, mas sem package manifest, suite integral ou fechamento B1. Estado canonico nesta consolidacao: `B1_INCOMPLETE_PENDING_RECONCILIATION`, nao deployavel e nao aceito.

## Bootstrap de reparo M2 em staging, 2026-08-28/29

A retomada confirmou que o proprio caminho de isolamento podia reproduzir a falha que deveria corrigir:

- `sessions_spawn` aplicou perfil de aproximadamente 5,77 GB contra capacidade liberavel de aproximadamente 4,47 GB;
- a tentativa terminou com zero spawn, zero bootstrap e zero workload, e a admissao foi cancelada sem orfao;
- o B1 permaneceu no HEAD `7b9a9c7516afdb6d141618c871fbe17e02889887`, com 17 arquivos modificados e 10 nao rastreados, sem promocao ou deploy.

A causa da interrupcao de uma continuacao direta foi classificada como `PARENT_OPENCLAW_EXECUTION_SCOPE_TEARDOWN`, nao como OOM, reboot, timeout ou falha comprovada do patch. A execucao passou entao para um tmux persistente, mas a auditoria posterior corrigiu a identidade operacional: o executor real e o tmux root-owned `rse-m2`, dentro de `session-3.scope`; o nome `rse-bootstrap-final` e os limites reportados de 2 GB, 75% CPU e 48 processos nao estavam aplicados ao processo real.

Evidencia de progresso em staging no corte desta consolidacao:

- qualificacao A-N `14/14 PASS`;
- invariantes `18/18 PASS`;
- upgrade compatibility `1/1 PASS`;
- Node/E2E `13/13 PASS`;
- regressao predecessora `432 PASS`;
- suite CAS adicional `21 PASS`;
- manifest global intermediario `fe08162d4bf0ad1ffefc4c710ebe7d39cc58ffea28229cbad7b7a4b040f1bcce`.

Esse resultado ainda nao e terminal. Auditoria posterior encontrou dois P0 abertos: processos escapando do slice canonico e fechamento do client dedicado antes do estado terminal. Os bytes continuavam mudando no corte; portanto nao existe freeze final, pacote imutavel aceito, SHA do pacote, rollback byte-exato, auditoria independente fechada, preflight root ou primeiro comando root. Producao permanece em quarentena, sem deploy/root comprovado e sem mutacao do B1 ou de ODP/EDC de producao.

## Proximos passos

- Manter dominios mutativos restritos a `EXECUTION_TREE_RECOVERY`, embora as capacidades de admissao/capacidade/fila/pressao ja estejam produtivas.
- Exigir approval especifico antes de habilitar memoria, restart, SQLite, terminacao ativa, gateway restart, reboot ou qualquer novo adapter live.
- Reconciliar os artefatos parciais do B1 sem promover ou repetir cegamente; exigir manifest SHA-256, testes unitarios/integracao/staging completos e prova de todos os invariantes antes de solicitar deploy B2.
- No M2, fechar os dois P0 de containment/terminalidade, autenticar o cgroup e o envelope de recursos realmente usados, repetir a qualificacao central serial nos bytes finais e somente depois congelar pacote, manifest e rollback.
- Preservar a admissao P1 `f3c9c0bf-07f9-4c53-8257-92c810249e29` sem retry concorrente ate o reparo do lifecycle ser aceito e implantado por boundary proprio.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Engineering-Delegation|OpenClaw Engineering Delegation]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Leitura-read-only-deve-provar-nao-mutacao|Leitura read-only deve provar nao mutacao]]
- [[40-CONHECIMENTO/Operacional/Pacote-selado-auto-reprodutivel-antes-de-privilegio-operacional|Pacote selado auto-reprodutivel antes de privilegio operacional]]
