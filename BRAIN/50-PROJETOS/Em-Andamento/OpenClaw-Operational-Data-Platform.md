# OpenClaw Operational Data Platform

```yaml
nome: OpenClaw Operational Data Platform
status: day3_core_pass_accepted_day4_not_executed
responsavel: Puppet Master
inicio: 2026-08-05
fim:
prioridade: alta
ultima_revisao: 2026-08-13
tags: [openclaw, odp, postgresql, operational-data, governance, rollback, non-interference, controlled-secret-executor, day3]
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
- Proximo token operacional registrado: `DAY_4_PROVIMENTO_213_ONBOARDING`.

## Guardrails

- Day 3 nao autoriza Day 4, business modules, importacao de operational-data, Provimento 213 ou interacao SQLite.
- Executor v2 aceito nao autoriza novas migracoes por heranca; cada proxima unidade precisa de token proprio, manifest, rollback e validacao.
- Capacidade sudo ampla pre-existente da conta `openclaw` foi observada como divida de seguranca independente; nao deve ser remediada dentro do escopo ODP sem autorizacao propria.
- Rollback deve distinguir artefatos criados por pacote Ubuntu, artefatos ODP, roles/databases/configuracao/backups ODP e elementos pre-existentes.
- Nunca remover pacote ou artefato pre-existente de cliente sem autorizacao destrutiva explicita.
- Errata em baseline aceito deve ser aditiva, limitada e rastreavel; o pacote imutavel permanece preservado.

## Proximos passos

- Avancar Day 4 somente com autoridade propria `DAY_4_PROVIMENTO_213_ONBOARDING`.
- Antes de qualquer migracao Provimento 213 para ODP, exigir contratos AIR/CPIW/ICD/DRE, rollback, non-interference e autorizacao atomica.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado|Proposta nao e contrato congelado]]
