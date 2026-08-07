# OpenClaw Operational Data Platform

```yaml
nome: OpenClaw Operational Data Platform
status: day2_postgresql_foundation_pass_accepted_day3_bloqueado
responsavel: Puppet Master
inicio: 2026-08-05
fim:
prioridade: alta
ultima_revisao: 2026-08-07
tags: [openclaw, odp, postgresql, operational-data, governance, rollback, non-interference]
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
- Proximo token operacional registrado: `DAY_3_ODP_CORE`.

## Guardrails

- Day 2 nao autoriza Day 3, business modules, importacao de operational-data, Provimento 213 ou interacao SQLite.
- Rollback deve distinguir artefatos criados por pacote Ubuntu, artefatos ODP, roles/databases/configuracao/backups ODP e elementos pre-existentes.
- Nunca remover pacote ou artefato pre-existente de cliente sem autorizacao destrutiva explicita.
- Errata em baseline aceito deve ser aditiva, limitada e rastreavel; o pacote imutavel permanece preservado.

## Proximos passos

- Avancar Day 3 somente com autoridade propria `DAY_3_ODP_CORE`.
- Antes de qualquer migracao Provimento 213 para ODP, exigir contratos AIR/CPIW/ICD/DRE, rollback, non-interference e autorizacao atomica.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado|Proposta nao e contrato congelado]]
