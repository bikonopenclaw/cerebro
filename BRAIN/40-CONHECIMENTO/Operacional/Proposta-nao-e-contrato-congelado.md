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

- `BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md`
- `BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md`
- `BRAIN/01-DIARIO/Semanal/2026-W31.md`
