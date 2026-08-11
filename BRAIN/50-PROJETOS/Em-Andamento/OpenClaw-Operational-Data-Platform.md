# OpenClaw Operational Data Platform

```yaml
nome: OpenClaw Operational Data Platform
status: day2_pass_accepted_day3_controlled_secret_executor_fail_closed
responsavel: Puppet Master
inicio: 2026-08-05
fim:
prioridade: alta
ultima_revisao: 2026-08-11
tags: [openclaw, odp, postgresql, operational-data, governance, rollback, non-interference, controlled-secret-executor]
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
- Instalacao root parcial posterior validou executor, sudoers e preflight autenticado `module_migrator|odp`, com `16/16` testes negativos; ainda assim terminou `FAIL_CLOSED_INSTALLED_STATE_NOT_FULL_FROZEN_ARTIFACT_SET` porque o contrato congelado nao estava instalado no caminho final esperado.
- Artefato ausente: `/usr/local/share/openclaw/odp-day3-controlled-secret-executor/EXECUTOR_CONTRACT.json`, esperado a partir de `projects/openclaw-engineering-delegation/edc-v1.1.0/prepared/odp-controlled-secret-executor-v1/EXECUTOR_CONTRACT.json`, SHA-256 `15c46d9d3c8200f7b6f07d2edcc0740fedb80266080aa10c1594412856721d7b`, owner/group/mode `root:root 0644`.
- Proximo token operacional registrado para corrigir apenas o contrato ausente: `AUTHORIZE_HEBERT_ROOT_INSTALL_ODP_CONTROLLED_SECRET_EXECUTOR_MISSING_CONTRACT_ARTIFACT`.

## Guardrails

- Day 2 nao autoriza Day 3, business modules, importacao de operational-data, Provimento 213 ou interacao SQLite.
- Preflight autenticado do executor nao autoriza `migrate`; validacao instalada completa precisa passar antes de qualquer promocao Day 3.
- Qualquer correcao do contrato ausente deve ser atomica e limitada ao artefato congelado, sem reinstalar executor, sudoers, segredo ou regenerar artefatos.
- Capacidade sudo ampla pre-existente da conta `openclaw` foi observada como divida de seguranca independente; nao deve ser remediada dentro do escopo ODP sem autorizacao propria.
- Rollback deve distinguir artefatos criados por pacote Ubuntu, artefatos ODP, roles/databases/configuracao/backups ODP e elementos pre-existentes.
- Nunca remover pacote ou artefato pre-existente de cliente sem autorizacao destrutiva explicita.
- Errata em baseline aceito deve ser aditiva, limitada e rastreavel; o pacote imutavel permanece preservado.

## Proximos passos

- Reexecutar validacao instalada somente apos autorizacao e instalacao do contrato congelado ausente.
- Avancar Day 3/migrate somente depois de `PASS_ACCEPTED` do executor instalado e autoridade propria `DAY_3_ODP_CORE`.
- Antes de qualquer migracao Provimento 213 para ODP, exigir contratos AIR/CPIW/ICD/DRE, rollback, non-interference e autorizacao atomica.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado|Proposta nao e contrato congelado]]
