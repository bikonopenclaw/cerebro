---
id: brain-be26739c501dc773919a
type: knowledge
title: Escopo de canais operacionais
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:08:05.502633Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md#relações
- type: references
  target: BRAIN/60-AGENTES/DARTH-VADER.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md#relações
---

# Escopo de canais operacionais

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidações de 2026-06-18 a 2026-06-21 e reparo Relatorios Operacionais em 2026-08-17
confiabilidade: alta
ultima_revisao: 2026-08-18
tags: [canais, telegram, escopo, roteamento, guardrails, faturamento]
```

## Princípio

Canais operacionais precisam de escopo explícito para evitar mistura de assuntos, execução fora de contexto e respostas no local errado.

## Aplicação prática

Para cada grupo, canal ou contexto operacional relevante, registrar:

- finalidade do canal;
- assuntos permitidos;
- assuntos fora de escopo;
- empresa, cliente ou projeto relacionado;
- agente ou skill responsável pela execução;
- owner externo responsavel pela resposta ao canal quando houver workers internos;
- guardrails de aprovação antes de impactos externos;
- caminho do contexto local, quando existir.

## Aprendizado

Separar canais por empresa e tipo de operação reduz risco financeiro, fiscal e reputacional. O agente deve responder considerando o contexto do canal, não apenas a mensagem isolada.

## Relações

- [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]

## Reforço 2026-W26

Além do escopo do canal, a configuração precisa separar grupo permitido de remetente autorizado. A correção do `groupAllowFrom` no Faturamento Bikon mostrou que allowlist de canal e allowlist de autor são camadas independentes; quando o provider mantém estado antigo, reload/restart limpo pode ser necessário para validar a configuração aplicada.

## Reforço 2026-08-18

Quando um canal operacional usa workers internos, o owner externo precisa ser unico e testado. No grupo Relatorios Operacionais, Puppet Master ficou responsavel pela resposta ao Telegram em fluxos com Darth/Kowalski, enquanto os workers retornam resultado interno e ficam bloqueados de `message` externo para evitar duplicidade ou resposta fora de contexto.

## Complementos reconciliados — lote 4 de 2026-09-21

Na consulta assistida SERPRO, o usuário pediu retorno compreensível, com resultado, limitações e próximo passo; diagnóstico técnico do terminal deve sustentar a resposta, não ser transferido ao usuário como única entrega. Isso não autoriza emissão nem oculta erro ou ausência de evidência. Fonte: unidades 38045.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.

## Complementos reconciliados — lote 5 de 2026-09-21

No broker local SERPRO, o usuário preferiu iniciar, consultar e encerrar sob demanda por comando acessível, em vez de deixá-lo sempre aberto. Preservar limite de exposição e controle explícito do ciclo; esta preferência não autoriza túnel público, emissão fiscal ou serviço permanente. Fonte: unidades 37988.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
