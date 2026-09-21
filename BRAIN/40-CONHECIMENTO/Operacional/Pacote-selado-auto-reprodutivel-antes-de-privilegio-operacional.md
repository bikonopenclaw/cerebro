---
id: brain-be7d87681eef2b3bcc3a
type: knowledge
title: Pacote selado auto-reprodutivel antes de privilegio operacional
created: '2026-09-21T19:31:17.466455Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:32:09.804705Z'
---

# Pacote selado auto-reprodutivel antes de privilegio operacional

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W33 e Portal 213 Stage 1B R2.3/R2.4
confiabilidade: alta
ultima_revisao: 2026-08-20
tags: [pacote, hash, rollback, preflight, root, producao, provimento-213, checkpoint]
```

## Principio

Antes de qualquer etapa com privilegio operacional, o pacote selado precisa provar que e auto-reprodutivel a partir dos proprios bytes. Narrativa, runbook, manifesto ou marcador `PASS` nao bastam se o artefato nao exercita controller, plano, hashes, preflight, canary, ledger e rollback de forma verificavel.

O pacote preparatorio deve falhar antes da ativacao real, nao durante ela.

## Aplicacao pratica

- Validar o hash esperado do pacote e recalcular planos a partir dos bytes selados.
- Exercitar o mesmo engine transacional em backend fake e, quando autorizado, live.
- Testar rollback, preflight, canary e ataques/adversarial cases sem mutacao real quando o escopo for preparatorio.
- Em scripts que poderao rodar com privilegio, exercitar sinais durante rollback, reentrada de fail/rollback, verificacao final de systemd, residuos de segredo temporario, diretorios pais criados na rodada e classificacao real de pacote interrompido.
- Bloquear root, servico, Telegram, DNS/TLS/proxy e producao se o artefato nao for aceito pelo proprio controller.
- Tratar correcao do pacote como nova unidade versionada, com novo hash e nova validacao.

## Exemplo conectado

No Portal 213, o Stage 1A.3 supersedido falhou porque o artefato selado nao era aceito pelo proprio controller como delivery bundle e divergia da matriz de rollback. O Stage 1A.3-R1 corrigiu o controller transacional futuro, validou hashes, plano, release binding e rollback offline/read-only, mas continuou sem autorizar Stage 1B/1C ou ativacao real.

Em 2026-08-19, o Portal 213 Stage 1B R2.3 reforcou o mesmo principio em formato de comando local canary root: o artefato novo foi validado por diff exato, `bash -n`, compilacao de heredocs Python, fixtures de sinais, rollback systemd, pais `/opt`, apt parcial, evidence path e segredo temporario, com root/sudo/systemctl/apt/producao `0`. O `PASS` continua preparatorio e nao autoriza execucao real.

Em 2026-08-20, a rota R2.4 tornou explicito que um pacote com prerequisito instalado ainda precisa de reconciliacao read-only autenticada antes de canary: execucoes orfas nao sao `PASS`, e Checkpoint 2 so pode iniciar depois de Checkpoint 1 retornar classificacao, evidence path e manifest SHA.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado|Validacao do caminho final instalado]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]

## Complementos reconciliados — lote 8 de 2026-09-21

Em scripts privilegiados, mantenha o descritor retornado por mkstemp; não combine arquivo já criado com nova abertura O_EXCL do mesmo caminho. Rollback só remove recursos criados/iniciados pela própria execução, com flags por recurso e sem agir após preflight sem mutação. Verifique hash por caminho exato, não presença em lista; processo/listener inalterado não prova teste funcional Telegram. Fonte revisada e cópia privilegiada executada devem manter identidade de bytes. Fonte: unidades 30533.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
