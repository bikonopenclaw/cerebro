# OpenClaw Operational Data Platform

```yaml
nome: OpenClaw Operational Data Platform
status: day4_checkpoint_l_preserved_rse_cancelled_b1_workspace_preserved
responsavel: Puppet Master
inicio: 2026-08-05
fim:
prioridade: alta
ultima_revisao: 2026-08-31
tags: [openclaw, odp, postgresql, operational-data, governance, rollback, non-interference, controlled-secret-executor, day3, day4, production-onboarding, rse-decommissioned]
```

## Objetivo

Implantar uma fundacao governada de dados operacionais em PostgreSQL para OpenClaw, separada de SQLite interno, runtime OpenClaw existente e migracoes do Provimento 213.

O Brain registra apenas estado consolidado e guardrails. Evidencias, pacotes, manifests e artefatos autoritativos permanecem em `projects/ODP/`, fora do Brain/Git.

## Estado consolidado

- Phase 0/0A estabeleceu arquitetura, authority chain e Execution Pack ODP v1.0.0, sem autorizar instalacao PostgreSQL ou mutacao produtiva.
- Day 1 Foundation Freeze final fechou `PASS`: firewall final PASS, PostgreSQL `5432` nao exposto, inventario user-service OpenClaw PASS, SQLite interaction `NONE_PASS`, AIR/ICD/DRE deferidos como dependencia bloqueante para Day 4, mutacoes proibidas `0`.
- Pacote Day 1 final: `DAY1_FOUNDATION_FREEZE_FINAL_CLOSURE_20260806T183647Z.tar.gz`, SHA-256 `2ee20437112415c9c1095913cc6743a876ea15aea1e11d7f6f808018bf91fd32`.
- Day 2 PostgreSQL Foundation foi aceito como `PASS_ACCEPTED`: PostgreSQL `16.14`, cluster `16/main`, service `active/running`, checksums `on`, listener apenas em `127.0.0.1:5432` e `[::1]:5432`, sem listener publico.
- Banco ODP: database `odp`, owner `platform_owner`, encoding `UTF8`, `public_create=false`.
- Validacoes Day 2: backup PASS, restore PASS, OpenClaw non-interference PASS e SQLite non-interference PASS.
- Day 2 Completion Pack v1.0.0: SHA-256 `c79fc107ecba5c5f1c0e3e217555ed44b10fc7b47db394691dc31a19ee026ad9`.
- Errata Day 2 v1.0.1: `PASS_ACCEPTED`, escopo `SECRET_ROOT_OWNERSHIP_DOCUMENTATION_ONLY`; corrigiu apenas a documentacao de ownership do secret root pre-existente.
- Regra canonica de segredo ODP: `/data/.openclaw/secrets` e pre-existente e preservado; ownership/control ODP comeca em `/data/.openclaw/secrets/odp` e `/data/.openclaw/secrets/odp/postgresql`. Valores de segredo nao entram em Git, reports, manifests, packs, logs ou saida Codex.
- Preparacao do executor controlado de segredo para Day 3 fechou `PASS_READY_FOR_ROOT_INSTALL`: executor SHA-256 `30d79907cd2d3531957d1f755274a9286c843f4215cfe785f4a7d0a44104c909`, sudoers SHA-256 `f6bccc4e59497cce98fcd994536d5be2a04f8df9af6094c6152c24730216a502`, `12/12` testes negativos, secret leak scan `PASS`, mutacoes de sistema `0`.
- Instalacao root parcial posterior validou executor, sudoers e preflight autenticado `module_migrator|odp`, com `16/16` testes negativos; a primeira validacao instalada terminou `FAIL_CLOSED_INSTALLED_STATE_NOT_FULL_FROZEN_ARTIFACT_SET` porque o contrato congelado nao estava instalado no caminho final esperado.
- Day 3 foi corrigido e aceito como `PASS_ACCEPTED`: executor v2 final `PASS`, `platform_admin -> platform_owner`, preflight `PASS`, migracoes `0000_bootstrap.sql`, `0001_core_metadata.sql` e `0002_observability.sql` aplicadas, ledger `PASS_0000_0001_0002`, drift `0`, checksums `3/3`, Kowalski `PASS_ACCEPTED`, `0` business modules, `0` mutacoes no runtime OpenClaw, `0` interacoes SQLite e `0` exposicao de segredo.
- Day 3 Completion Pack v1.0.0: `DAY3_COMPLETION_PACK_v1.0.0.tar.gz`; pacote final `ODP_DAY3_CORE_FINAL_ACCEPTANCE_PASS_20260811T124410Z.tar.gz`.
- Day 4 foi autorizado como `DAY_4_PROVIMENTO_213_ONBOARDING`, mas falhou fechado antes de qualquer continuacao por exposicao P0 recuperavel de credenciais OpenClaw runtime durante discovery de ambiente.
- Incidente Day 4 em 2026-08-21: comando de preflight nao delimitado `env | sort | rg -i 'PG|POSTGRES|ODP|CRC|DATABASE|DB|OPENCLAW'` expôs referencias logicas de credenciais OpenClaw runtime no stdout/tool result/transcripts. Referencias afetadas: `OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_REMOTE_TOKEN` e `OPENCLAW_HOOKS_TOKEN`. Plaintext nao deve ser registrado no Brain.
- Pacote de recuperacao: `/data/.openclaw/workspace/projects/ODP/reports/day4-secret-exposure-recovery-20260821T152254Z.tar.gz`, SHA-256 `6071d6d7a8c098aadd7b70e4a72d392e368c30706cbb592d1732e1c851b30a8b`.
- Estado Day 4: `RECOVERABLE_P0_SECRET_EXPOSURE_PENDING_OPENCLAW_RUNTIME_SECRET_ROTATION`, `DAY4_CONTINUATION=NOT_CONTINUED`, `DAY4_COMPLETION_PACK` nao executado, implementacao/testes/promocao/validacao Kowalski/estabilidade nao executados.
- Integridade preservada por nao mutacao: ODP production DB `NOT_TOUCHED`, CRC authority `PRESERVED_BY_NON_MUTATION`, EDC `PRESERVED_BY_NON_MUTATION`, Day 2/Day 3 authority `PRESERVED_BY_NON_MUTATION`, OpenClaw runtime state nao mutado pelo child, SQLite sem interacao.
- Proximo token operacional registrado: `OPENCLAW_RUNTIME_ROTATION_BRIDGE_THEN_CONTINUE_SAME_DAY_4_PROVIMENTO_213_ONBOARDING_AUTHORITY`.

## Atualizacao Day 4 e pipeline de onboarding, 2026-08-27/28

- A recuperacao e os gates posteriores preservaram Day 4 no Checkpoint L com `311/311` testes, candidato `17/17`, PGL `PASS`, Kowalski `PASS` e mutacoes de producao `0`.
- O objetivo corrente e provar `ODP_PRODUCTION_ONBOARDING_PIPELINE=PASS_ACCEPTED`, com Provimento 213 como primeiro workload real, sem reconstruir trabalho autenticado do Checkpoint L.
- A execucao foi bloqueada antes do canario por defeito estrutural do lifecycle OpenClaw/RSE/EDC: child criado antes da admissao, deferral bloqueando caller em `--wait`, perda de sessao com admissao viva, perfis de memoria inconsistentes e registry terminal enquanto cgroup permanecia ativo.
- O reparo B1 foi autorizado fora do caminho quebrado, em clone isolado e unit `systemd --user`, sem RSE, deploy ou mutacao ODP/EDC de producao. Na janela desta consolidacao, terminou com patch/testes parciais, mas sem manifesto/pacote final e sem aceite; `B1_INCOMPLETE_PENDING_RECONCILIATION`.
- Em 2026-08-28/29, o bootstrap M2 do reparo de lifecycle avancou somente em staging. O B1 continuou preservado no mesmo HEAD e sem mutacao; como o M2 ainda tinha dois P0 abertos e bytes em mudanca, ele nao liberou B2, canario ODP nem retomada do onboarding.
- Nenhum canario produtivo, onboarding Provimento 213, reexecucao idempotente, teste de falha, escala ou rollback de qualificacao foi concluido por esta rodada.

## Guardrails

- Day 3 nao autoriza Day 4, business modules, importacao de operational-data, Provimento 213 ou interacao SQLite.
- Executor v2 aceito nao autoriza novas migracoes por heranca; cada proxima unidade precisa de token proprio, manifest, rollback e validacao.
- Capacidade sudo ampla pre-existente da conta `openclaw` foi observada como divida de seguranca independente; nao deve ser remediada dentro do escopo ODP sem autorizacao propria.
- Rollback deve distinguir artefatos criados por pacote Ubuntu, artefatos ODP, roles/databases/configuracao/backups ODP e elementos pre-existentes.
- Nunca remover pacote ou artefato pre-existente de cliente sem autorizacao destrutiva explicita.
- Errata em baseline aceito deve ser aditiva, limitada e rastreavel; o pacote imutavel permanece preservado.
- Discovery de ambiente nao pode despejar `env` em stdout com filtro amplo. Preflight seguro deve usar allowlist de nomes, metadata/hash ou probes que provem ausencia de segredo antes de imprimir qualquer saida.
- Exposicao de segredo em transcript/evidence exige fail-closed, inventario de superficies, rotacao/revogacao de runtime, validacao de credencial nova sem stdout secreto, invalidez da antiga onde testavel e suite negativa com exposicao pos-recuperacao zerada antes de retomar a autoridade original.

## Proximos passos

- Preservar o Checkpoint L e o workspace B1 incompleto em `/data/.openclaw/workspace/projects/ODP/preserved/odp-b1-bootstrap-20260827T235127Z`; ODP nao aguarda nem invoca RSE. Qualquer reconciliacao B1 ou boundary B2 exige nova autoridade ODP propria.
- RSE foi permanentemente cancelado e desinstalado. Uma retomada ODP nao pode depender de RSE nem interpretar artefatos historicos RSE como autoridade ativa.
- Antes de qualquer migracao Provimento 213 para ODP, exigir contratos AIR/CPIW/ICD/DRE, rollback, non-interference e autorizacao atomica.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado|Proposta nao e contrato congelado]]
