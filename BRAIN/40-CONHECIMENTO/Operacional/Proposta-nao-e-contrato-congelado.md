---
id: brain-e8fa11c100610f877915
type: knowledge
title: Proposta nao e contrato congelado
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-10-18T06:00:00Z'
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
- type: references
  target: BRAIN/01-DIARIO/2026/2026-10-15.md
  reason: Caso recente em que um documento dito oficial permanecia em formação e misturava regras vigentes, propostas e estados não normalizados.
  source: cron:d95bbe73-24d9-4e2b-ba57-0032082bb54b
- type: derived_from
  target: BRAIN/01-DIARIO/Semanal/2026-W42.md
  reason: Consolida o padrão de que riqueza e detalhamento documental não substituem versão, estado e autoridade executáveis.
  source: BRAIN/99-SISTEMA/brain-v2/reports/coverage-2026-10-18-weekly.json
---

# Proposta nao e contrato congelado

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W31; revisão documental local de 2026-10-11; consolidação semanal 2026-W42
confiabilidade: alta
ultima_revisao: 2026-10-18
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
- [[01-DIARIO/2026/2026-10-15|Diário 2026-10-15 — contrato de tráfego em formação]]

## Documento oficial ainda em formação — 11/10/2026

Um documento pode ser oficial como acervo de estudo e, ao mesmo tempo, não estar apto a governar execução. No contrato de tráfego v0.65 encaminhado para análise, o próprio cabeçalho dizia `Em formação`; a leitura local encontrou 450 definições de regra, 449 IDs únicos e duas regras diferentes com o ID `R-META-243`. A ordem dos capítulos também não era estável: depois de 1–10 surgiam outro 8, 12, 13, 14 e 11.

O corpo misturava regras validadas, propostas, estados fora da taxonomia declarada e itens sem estado. Por isso, chamar o arquivo de fonte oficial não cria uma visão executável inequívoca nem autorização para publicar, alterar orçamento, segmentação, tracking, site, dados pessoais ou identidade de terceiros.

Antes de automação, separar política vigente, estudo, catálogo ativo, changelog e auditoria; normalizar IDs e estados; resolver conflitos de fórmula e escopo; materializar as evidências referenciadas; definir objetivo e owner; fazer revisão jurídica/regulatória; e congelar a versão efetivamente aprovada por hash. A solicitação de Hebert foi análise de conteúdo primeiro e encaixe secundário, não adoção do contrato pela BIKON.

## Riqueza documental não substitui contrato executável — semana 2026-W42

Um acervo volumoso, detalhado ou chamado de oficial pode ser excelente para pesquisa e ainda ser inadequado como instrução de produção. A revisão semanal combinou o estado `Em formação`, IDs conflitantes, ordem instável de capítulos e taxonomia misturada com a ausência de aceite ou adoção pela BIKON. Quantidade de regras não resolve qual versão vigora, quem possui autoridade nem quais estados são executáveis.

Antes de promover esse tipo de fonte, exigir separação entre política vigente, propostas, catálogo, changelog e auditoria; resolver conflitos; definir owner e alçadas; materializar evidências; e congelar a versão aprovada por hash. Analisar, transportar ou resumir o documento não autoriza publicação, orçamento, dados pessoais, identidade de terceiros ou promessa comercial. Síntese em [[01-DIARIO/Semanal/2026-W42|W42]].

## Complementos reconciliados — lote 15 de 2026-09-21

Na revisão EP-02A de 28/07, pares run1/run2 eram idênticos, mas os hashes anunciados para freeze e FIM mudaram entre inspeções. Reprodutibilidade entre duas cópias não prova imutabilidade do objeto submetido ao gate. Fixar versão/conjunto por hash, interromper parecer sobre alvo mutável e recomeçar a validação do conjunto efetivamente congelado; não transportar PASS de uma revisão para regeneração posterior. A preimagem semântica continua subordinada à versão normativa correspondente, mesmo quando contagens e hashes internos fecham. Fonte: unidades 9753.

No fluxo histórico da planilha, safe_client havia sobrescrito owner e SLA apesar dos valores explícitos da fonte. Depois do manifesto sanitizado, restava um valor em G6 com a exceção desativada em C6 e J6 vazio. Um campo órfão não deve ativar nem herdar uma exceção; validar condições de aplicabilidade além de presença do valor. A limpeza desse resíduo foi recomendada, mas não era um bloqueador adicional após o aceite do contrato requerido. O checkpoint não comprova configuração atual. Fonte: unidades 41465, 41468, 41471.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 16 de 2026-09-21

Na revisão documental EP-02 de 28/07, READY_DOCUMENTATION_ONLY foi usado como checkpoint embora o contrato daquele projeto aceitasse apenas READY, BLOCKED ou FAILED. Um rótulo explicativo útil não pode ser introduzido como estado de máquina sem mudança do contrato. A revisão também distinguiu autorização para produzir documento de autorização para alterar a hierarquia normativa do projeto. São regras daquele artefato histórico, não primazia universal de arquivos sobre instruções do usuário; futuras alterações precisam explicitar versão e escopo. O candidato corrigido seguiu revalidação e o EP-02 avançou depois. Fonte: unidades 9720.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch16-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
