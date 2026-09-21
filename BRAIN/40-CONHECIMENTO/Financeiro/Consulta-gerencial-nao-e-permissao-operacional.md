---
id: brain-0e82d17a3d791cc73817
type: knowledge
title: Consulta gerencial não é permissão operacional
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional.md#relações
- type: references
  target: BRAIN/60-AGENTES/DARTH-VADER.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional.md#relações
- type: references
  target: BRAIN/60-AGENTES/KOWALSKI.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional.md#relações
---

# Consulta gerencial não é permissão operacional

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-12
tags: [financeiro, permissoes, relatorios, sqlite, kowalski, darth-vader]
```

## Regra

Acesso de leitura para relatório, BI ou conferência não concede permissão para escrever, baixar, importar retorno, emitir NFS-e, gerar boleto, gerar remessa ou comunicar cliente.

## Aplicação prática

- Separar claramente consumidor gerencial de dono operacional do fluxo.
- Conceder somente leitura para relatórios quando a tarefa for análise ou conferência.
- Manter escrita, baixa, importação e efeitos fiscais/bancários com o agente ou processo responsável.
- Validar permissões técnicas, não apenas intenção operacional.

## Exemplo conectado

Kowalski recebeu acesso somente leitura à base financeira gerencial da BIKON para relatórios e conferências. Darth Vader continua responsável por escrita, importação de retorno, baixa, NFS-e, boleto e remessa.

## Relações

- [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]
- [[60-AGENTES/KOWALSKI|Kowalski]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
