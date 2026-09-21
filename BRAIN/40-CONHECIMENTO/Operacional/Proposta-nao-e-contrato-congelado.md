---
id: brain-e8fa11c100610f877915
type: knowledge
title: Proposta nao e contrato congelado
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W31.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Proposta-nao-e-contrato-congelado.md#relações
---

# Proposta nao e contrato congelado

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [documentacao, contratos, freeze, validacao, cadeia-de-custodia]
```

## Principio

Documento proposto preserva contexto e intencao, mas nao cria autoridade operacional. Arquivos marcados como `PROPOSED_NOT_FROZEN`, `PROPOSED_PENDING_INDEPENDENT_VALIDATION` ou equivalente devem continuar como proposta ate passarem por unidade documental, freeze e validacao proprios.

## Aplicacao pratica

- Preservar o sufixo de proposta no nome e no texto.
- Nao usar proposta como fonte canonica para implementacao, target, deploy, restore, contato externo ou recorrencia.
- Promover somente por fluxo explicito: escopo documental, diff, hash, validacao independente, commit/checkpoint e Approval quando exigido.
- Se a implementacao depender da proposta, bloquear e pedir autorizacao para congelamento documental antes de executar.

## Exemplo conectado

Na semana 2026-W31, documentos como `Serventia_Identity_Contract_v1_PROPOSED_NOT_FROZEN.md`, `CNS_Format_Source_Resolution_Record_v1_PROPOSED_NOT_FROZEN.md` e registros multi-Serventia pendentes foram tratados como propostas, nao contratos canonicos.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[01-DIARIO/Semanal/2026-W31|Semana 2026-W31, cobertura parcial]]
