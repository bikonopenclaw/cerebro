---
id: brain-e8fa11c100610f877915
type: knowledge
title: Proposta nao e contrato congelado
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T20:06:54.602140Z'
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

## Complementos reconciliados — lote 15 de 2026-09-21

Na revisão EP-02A de 28/07, pares run1/run2 eram idênticos, mas os hashes anunciados para freeze e FIM mudaram entre inspeções. Reprodutibilidade entre duas cópias não prova imutabilidade do objeto submetido ao gate. Fixar versão/conjunto por hash, interromper parecer sobre alvo mutável e recomeçar a validação do conjunto efetivamente congelado; não transportar PASS de uma revisão para regeneração posterior. A preimagem semântica continua subordinada à versão normativa correspondente, mesmo quando contagens e hashes internos fecham. Fonte: unidades 9753.

No fluxo histórico da planilha, safe_client havia sobrescrito owner e SLA apesar dos valores explícitos da fonte. Depois do manifesto sanitizado, restava um valor em G6 com a exceção desativada em C6 e J6 vazio. Um campo órfão não deve ativar nem herdar uma exceção; validar condições de aplicabilidade além de presença do valor. A limpeza desse resíduo foi recomendada, mas não era um bloqueador adicional após o aceite do contrato requerido. O checkpoint não comprova configuração atual. Fonte: unidades 41465, 41468, 41471.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

Na revisão documental EP-02 de 28/07, READY_DOCUMENTATION_ONLY foi usado como checkpoint embora o contrato daquele projeto aceitasse apenas READY, BLOCKED ou FAILED. Um rótulo explicativo útil não pode ser introduzido como estado de máquina sem mudança do contrato. A revisão também distinguiu autorização para produzir documento de autorização para alterar a hierarquia normativa do projeto. São regras daquele artefato histórico, não primazia universal de arquivos sobre instruções do usuário; futuras alterações precisam explicitar versão e escopo. O candidato corrigido seguiu revalidação e o EP-02 avançou depois. Fonte: unidades 9720.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
