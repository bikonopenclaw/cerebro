# OpenClaw Engineering Delegation

```yaml
nome: OpenClaw Engineering Delegation
status: edc_live_read_only_validado_task_specific_write_alinhado_boundary_repair_pendente
responsavel: Puppet Master
inicio: 2026-08-06
fim:
prioridade: alta
ultima_revisao: 2026-08-07
tags: [openclaw, edc, codex, engineering-delegation, sandbox, writable-roots, fail-closed]
```

## Objetivo

Governar delegacao de engenharia para Codex CLI como ferramenta controlada pelo Puppet Master, com autorizacao atomica, contrato de runtime, isolamento de sandbox, evidencia append-only, validação independente e fail-closed antes de qualquer mutacao nao autorizada.

O EDC nao transforma Codex em agente autonomo e nao concede acesso permanente a producao, dados sensiveis, clientes, root, systemd, rede de tarefa ou escrita fora de boundary explicito.

## Estado consolidado

- EDC v1.1.0: primeira homologacao falhou fechado por `5` mismatches schema/documento e uma acao proibida de permissao; estados permaneceram inativos.
- EDC v1.1.0 schema alignment: `PASS`, com JSON Schema Draft 2020-12, politica semantica e `21/21` testes PASS.
- EDC v1.1.1: runtime contract e activation-readiness `PASS`; profile/registry/receipt ainda ficaram `FROZEN_NOT_ACTIVE` ou homologacao inativa.
- EDC v1.1.2: ativacao real do perfil read-only `PASS`, sem invocar Codex; active state bundle `cb1628139ee080833aef2f658f7b4f98a238cac024b4e526960a08ffc37e6c50`.
- EDC v1.2.0: primeira tentativa de piloto Zone A read-only falhou fechado antes de Codex por revalidacao Kowalski do pacote pre-pilot.
- EDC v1.2.1: correcao unica de binding no pacote pre-pilot `PASS`, sem invocar Codex e sem live delegation.
- Reautenticacao Codex: transicao `API_KEY -> CHATGPT_ACCOUNT_OAUTH` validada, sem divulgar metadados de conta e sem retry de piloto nessa unidade.
- Sandbox Codex: diagnostico identificou restricao AppArmor/bwrap; reparo root-assisted posterior instalou e validou `bubblewrap`, perfis AppArmor e `codex sandbox /usr/bin/true` com exit `0`.
- Primeiro piloto live Zone A read-only v1.2.1: `PASS`, thread `019fd8f1-23a2-7f93-a6e4-2b1080b2dc84`, invocation `EDC-CODEX-INV-0001`, Codex leu exatamente dois targets autorizados, writes `0`, task network `0`, web/MCP `0`, dados sensiveis/clientes/producao/root/systemd/restart `0`.
- Runtime-state apos piloto: bundle `59bf0c68aa8c09e7dd907c8dffe7d4bd1a0ec31fa160529e258b22786178fe33`.
- Primeira tentativa de engineering write para CPIW V4 falhou antes de Codex porque o EDC ativo ainda nao tinha ramo conforme para `TASK_SPECIFIC_ENGINEERING_DELEGATION` com writable roots explicitos.
- EDC v1.2.2 alinhou schema, controller, writable-root validator, fixtures task-specific, regressao read-only e simulacao do gate Provimento; `56` testes PASS e Kowalski `PASS`. Runtime-state ativo: bundle `4fbd8a16f98009b9e5aacc4b86a2087fea1c5f423b6b0ad8aab6fea1ecdea75d`.
- Tentativa seguinte de apply adapter CPIW V4 executou Codex uma vez, mas terminou `FAIL_CLOSED` por `CODEX_WRITE_BOUNDARY_VIOLATION_OUTSIDE_AUTHORIZED_WRITABLE_ROOTS`: `3` escritas dentro dos roots autorizados e `54` arquivos fora do boundary. O baseline do adapter nao foi aceito.

## Guardrails

- Read-only live delegation nao herda permissao de escrita.
- Writable roots precisam ser declarados por tarefa e validados depois da execucao contra persistencia real.
- Artefatos preliminares de rodada fail-closed nao viram baseline aceito.
- Violacao de boundary deve preservar evidencias ate autorizacao explicita de limpeza ou retry.
- Codex nao deve acessar dados de cliente, Provimento 213 produtivo, rede de tarefa, web/MCP, root, systemd, pacote, permissao ou restart fora do escopo autorizado.

## Proximos passos

- Corrigir enforcement de boundary para escrita task-specific somente com autorizacao propria.
- Revalidar EDC apos a correcao sem executar tarefa CPIW na mesma unidade, se esse for o escopo autorizado.
- Autorizar novamente o apply adapter CPIW V4 apenas quando boundary, bundle EDC e baseline estiverem congelados e vinculados ao preview hash CPIW.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Boundary-de-escrita-em-delegacao-de-engenharia|Boundary de escrita em delegacao de engenharia]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado|Validacao do caminho final instalado]]
