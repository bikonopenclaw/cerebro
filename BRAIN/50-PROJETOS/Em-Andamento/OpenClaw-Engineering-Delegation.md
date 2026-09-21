---
id: brain-13c7d8e58ffac16ae29b
type: knowledge
title: OpenClaw Engineering Delegation
created: '2026-09-21T20:06:16.863394Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T20:54:07.904960Z'
---

# OpenClaw Engineering Delegation

```yaml
nome: OpenClaw Engineering Delegation
status: edc_odp_controlled_secret_executor_prepared_installed_validation_fail_closed
responsavel: Puppet Master
inicio: 2026-08-06
fim:
prioridade: alta
ultima_revisao: 2026-08-11
tags: [openclaw, edc, codex, engineering-delegation, sandbox, writable-roots, fail-closed, odp]
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
- Rodada posterior vinculada ao CPIW V4 usou EDC bundle `1dca5fece94fd1a8c3c2bb41917dbd326e1afe07498fae60bbc8613084912049` no commit produtivo CNS `023689`, que passou com `311` operações commitadas, readback `PASS`, `0` DRE/PDF/contato cliente e journal `COMMITTED`.
- A aceitação operacional pós-commit do CNS `023689` falhou em gates do produto/runtime Herald: rota autenticada `023689` ausente e rota controle `024067` com side effect de leitura. Isso deve permanecer separado do resultado de commit de dados AIR/ICD e das evidências EDC.
- Registro de boundary ODP em 2026-08-10 reconciliou artefatos sob caminho canonico `/data/.openclaw/workspace/projects/ODP` e preservou bloqueio por `ROOT_INSTALL_GATE`; nenhuma rota `/data/.openclaw/workspace/projetos/ODP` foi usada ou criada.
- Preparacao do executor controlado de segredo ODP fechou `PASS_READY_FOR_ROOT_INSTALL`, sem instalacao, sudoers mutation, Day 3 promotion, PostgreSQL structural mutation, SQLite ou OpenClaw runtime mutation. Executor SHA-256 `30d79907cd2d3531957d1f755274a9286c843f4215cfe785f4a7d0a44104c909`; sudoers SHA-256 `f6bccc4e59497cce98fcd994536d5be2a04f8df9af6094c6152c24730216a502`; `12/12` testes negativos e Kowalski `PASS_READY_FOR_ROOT_INSTALL`.
- Validacao instalada apos root bridge terminou `FAIL_CLOSED_INSTALLED_STATE_NOT_FULL_FROZEN_ARTIFACT_SET`: executor/sudoers/preflight passaram, mas `EXECUTOR_CONTRACT.json` nao estava instalado no caminho final esperado. Proximo token: `AUTHORIZE_HEBERT_ROOT_INSTALL_ODP_CONTROLLED_SECRET_EXECUTOR_MISSING_CONTRACT_ARTIFACT`.

## Guardrails

- Read-only live delegation nao herda permissao de escrita.
- Writable roots precisam ser declarados por tarefa e validados depois da execucao contra persistencia real.
- Artefatos preliminares de rodada fail-closed nao viram baseline aceito.
- Violacao de boundary deve preservar evidencias ate autorizacao explicita de limpeza ou retry.
- Codex nao deve acessar dados de cliente, Provimento 213 produtivo, rede de tarefa, web/MCP, root, systemd, pacote, permissao ou restart fora do escopo autorizado.
- Preparar artefato root-owned nao equivale a instalar, aceitar ou promover Day 3; cada camada exige gate proprio.
- Validacao instalada deve conferir o conjunto congelado completo, nao apenas binario, sudoers e preflight.

## Proximos passos

- Preservar a separação entre evidência EDC, commit de dados CPIW e aceitação operacional Herald/dashboard.
- Revalidar qualquer novo uso de escrita task-specific com bundle, writable roots e pós-estado persistido explicitamente vinculados.
- Autorizar correção da rota `023689` e da pureza `024067` como trabalho de produto/runtime, não como repetição automática do commit CPIW.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Boundary-de-escrita-em-delegacao-de-engenharia|Boundary de escrita em delegacao de engenharia]]
- [[40-CONHECIMENTO/Operacional/Contrato-de-runtime-reprodutivel|Contrato de runtime reprodutivel]]
- [[40-CONHECIMENTO/Operacional/Validacao-do-caminho-final-instalado|Validacao do caminho final instalado]]

## Complementos reconciliados — lote 16 de 2026-09-21

No EDC v1.2.0, novo binding local corrigiu a referência de controller, mas o ZIP ainda carregava envelope/invocation antigos, inventário com auto-hash obsoleto e README fora da cobertura, além de documentos exigidos pelo validador ausentes. Os 35 testes e validator health PASS não provaram autocontenção do pacote. Revalidar bytes selados, inventário não circular e todos os bindings documento→schema, depois emitir nova versão. O v1.2.1 posterior passou; o registro histórico não mantém o bloqueio antigo aberto. Fonte: unidades 8844.

No primeiro piloto read-only EDC v1.2.1, o autorrelato de Codex trazia invocation_id nulo, enquanto o registro canônico vinculava a execução a EDC-CODEX-INV-0001. Tratar isso como divergência de metadados do autorrelato, sem inventar ausência de execução ou usar o autorrelato como autoridade. A preparação v1.2.2 de escrita era etapa separada: testes e schema não significavam nova invocação nem aprovação de produção. Conferir contrato, invocação e evidência persistida antes de concluir estado atual. Fonte: unidades 8851.

Na revalidação histórica EDC v1.1.2, o ZIP externo tinha a identidade esperada e os inventários de core apontavam à nova baseline, mas três relatórios ainda citavam o ZIP/core anterior. Separar identidade do pacote, identidade do core e escopo temporal do recibo independente; um PASS antigo não pode autenticar bytes novos sem reconciliação explícita. Não exigir que o ZIP contenha seu próprio hash integral: a inconsistência relevante era o vínculo de evidência vigente, não a ausência de uma referência autorrecursiva. O v1.2.2 posteriormente validado supera esse checkpoint; não afirmar defeito ativo. Fonte: unidades 8834.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 22 de 2026-09-21

Na revisão histórica EDC v1.2.3 de 07/08, a reconciliação do CPIW preservou candidato/diff e restaurou fontes canônicas aos hashes pré-invocação; dez diretórios temporários de testes foram removidos, sem residual autorizado como baseline. A simulação validou workspace isolado, contenção de temporários, promoção controlada e rollback, com zero invocações Codex naquela revisão. Isso não apaga a violação anterior nem comprova promoção produtiva. O snapshot ainda aguardava relatório independente final; registrar essa fronteira antes de usar o pacote como evidência atual. Fonte: unidades 8854.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch22-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
