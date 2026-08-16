# Validacao source-native de PDF financeiro

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidacao semanal 2026-W33
confiabilidade: alta
ultima_revisao: 2026-08-16
tags: [financeiro, pdf, extracao, evidencia, fip, cartao]
```

## Principio

Quando um PDF financeiro alimenta decisao material, a extracao precisa preservar layout, colunas, coordenadas, encoding e totalizadores da fonte. Parser generico que mistura linhas ou colunas nao e detalhe tecnico: ele pode contaminar a fila de classificacao, P&L, settlement ou entrevista.

Se a fonte e PDF estruturado, a validacao source-native pode ser requisito financeiro.

## Aplicacao pratica

- Reconciliar totais da fatura ou demonstrativo antes de usar itens extraidos.
- Validar paginas, bounding boxes, colunas, datas, valores e sinais quando houver risco de mistura.
- Marcar fila antiga como invalida quando parser anterior contaminou itens.
- Nao promover entrevista, classificacao ou P&L com base em itens cuja origem/layout nao foi provada.
- Guardar apenas estado consolidado e sanitizado no Brain; PDFs e artefatos brutos ficam fora do Git.

## Exemplo conectado

No FIP CHG-004, Mercado Pago precisou reparar a fila porque o parser antigo contaminou janeiro como linha malformada. Itau Personnalite foi validado source-native por coordenadas bbox antes da entrevista, preservando 282 itens privados como fila reparada, sem classificacao automatica.

## Relacoes

- [[50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence|FIP Bikon Financial Intelligence]]
- [[40-CONHECIMENTO/Financeiro/Natureza-economica-provada-antes-de-PnL|Natureza economica provada antes de PnL]]
- [[40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git|Artefatos gerados fora do Brain e Git]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]
