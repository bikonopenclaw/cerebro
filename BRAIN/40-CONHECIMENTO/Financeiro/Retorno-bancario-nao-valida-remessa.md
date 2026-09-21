---
id: brain-7a504005b89f6a90fac0
type: knowledge
title: Retorno bancário não valida remessa
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md#relações
---

# Retorno bancário não valida remessa

```yaml
categoria: financeiro
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [cnab400, cresol, retorno, remessa, conciliacao, boletos]
```

## Princípio

Um arquivo de retorno bancário pode servir como evidência para parser e conciliação, mas não valida layout de remessa nem autoriza inferir próximo nosso número, documento, sequencial ou regra de envio.

## Aplicação prática

- Usar retorno `.ret` apenas para leitura de ocorrências, liquidações e conciliação.
- Sanitizar exemplos antes de qualquer registro no Brain.
- Não versionar `.ret` bruto quando contiver dados sensíveis.
- Não usar retorno como golden case de remessa `.rem`.
- Homologar layout de remessa com documentação oficial e validação bancária antes de qualquer envio real.

## Motivo

Retorno e remessa têm finalidades opostas no fluxo CNAB. Confundir os dois pode gerar boletos/remessas inválidos, sequenciais incorretos ou exposição de dados financeiros.

## Relações

- [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
