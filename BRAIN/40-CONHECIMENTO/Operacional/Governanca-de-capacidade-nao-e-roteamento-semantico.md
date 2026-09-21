---
id: brain-90b77686aab6da8f4b6c
type: knowledge
title: Governanca de capacidade nao e roteamento semantico
created: '2026-09-21T18:53:54.531182Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T18:55:38.578515Z'
---

# Governanca de capacidade nao e roteamento semantico

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W34
confiabilidade: alta
ultima_revisao: 2026-08-23
tags: [capacidade, roteamento, rse, puppet, admissao, governanca]
```

## Principio

Governanca de capacidade decide se uma execucao cabe agora, deve esperar ou deve ser rejeitada por pressao operacional. Ela nao decide a intencao da tarefa nem reclassifica seu significado.

A autoridade de classificacao semantica deve permanecer separada da autoridade de admissao por recursos.

## Aplicacao pratica

- Puppet ou owner equivalente classifica intencao, risco, foreground/background e escopo.
- RSE ou camada de capacidade consome perfil de recurso e decide admissao, deferral, fila, pressao e reserva atomica.
- Pressao operacional pode bloquear trabalho caro, mas nao deve transformar tarefa, dominio ou autorizacao.
- Uma decisao de capacidade `PASS` nao amplia permissoes mutativas nem substitui approval de superficie.
- Logs devem registrar classificacao recebida, decisao de capacidade e razao de deferral/rejeicao sem reinterpretar o pedido.

## Exemplo conectado

Em 2026-W34, [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]] fechou Capacity-Aware Execution Governance v1 como `PASS`. O contrato canonico preservou Puppet como dono de intencao/classificacao e RSE como autoridade de admissao, fila, pressao, headroom e reserva atomica.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Producao-parcial-por-dominio-nao-herda-autorizacao|Producao parcial por dominio nao herda autorizacao]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]]
- [[01-DIARIO/Semanal/2026-W34|Semana 2026-W34]]

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Correção histórica de 18/07/2026: Hebert rejeitou tratar UNUS como nome de processo; UNUS identifica um cliente. Em memória e roteamento, separar identidade da entidade (cliente/organização) do procedimento, capacidade ou workflow que a atende. Uma coincidência de nome em tarefa ou artefato não cria um processo institucional e não deve originar vínculo semântico desse tipo sem evidência. Fonte: unidades 36976.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.
