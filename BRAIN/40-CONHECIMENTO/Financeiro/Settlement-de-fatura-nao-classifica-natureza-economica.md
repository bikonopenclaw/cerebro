---
id: brain-fdf700654a18c605c72c
type: knowledge
title: Settlement de fatura nao classifica natureza economica
created: '2026-09-21T19:26:27.377766Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:32:09.804705Z'
---

# Settlement de fatura nao classifica natureza economica

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidacao semanal 2026-W33
confiabilidade: alta
ultima_revisao: 2026-08-16
tags: [financeiro, cartao, settlement, fip, privacidade, pnl]
```

## Principio

Settlement de fatura prova liquidacao de passivo. Match de transferencia ou reembolso prova relacao estrutural de caixa. Nenhum dos dois classifica automaticamente a natureza economica dos itens, nem transforma gasto pessoal em despesa empresarial.

A fatura pode estar reconciliada e ainda assim continuar fora do P&L ate classificacao humana ou fonte autorizada item a item.

## Aplicacao pratica

- Usar settlement para provar que a fatura fechou, nao para aprovar despesas.
- Usar prematch de reembolso para reduzir perguntas, nao para criar batch ou mutacao bancaria.
- Manter itens pessoais em camada privada/quarentenada ate classificacao propria.
- Separar liquidacao de passivo, reembolso, clearing, despesa de negocio e retirada/distribuicao.
- Registrar diferenca zero como reconciliacao de valor, nao como prova de finalidade.

## Exemplo conectado

No FIP CHG-004, a fatura Itau Personnalite `2026-01` fechou com transferencia bancaria de R$ 7.681,79 e diferenca R$ 0,00. Isso provou settlement, mas os 39 itens continuaram exigindo classificacao economica e nao foram promovidos para despesa empresarial.

## Relacoes

- [[50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence|FIP Bikon Financial Intelligence]]
- [[40-CONHECIMENTO/Financeiro/Natureza-economica-provada-antes-de-PnL|Natureza economica provada antes de PnL]]
- [[40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional|Consulta gerencial nao e permissao operacional]]
- [[01-DIARIO/Semanal/2026-W33|Semana 2026-W33]]

## Complementos reconciliados — lote 7 de 2026-09-21

Decisão histórica de Hebert em14/08/2026: transferência Bikon→Hebert deR$6.964,82em13/04/2026corresponde à liquidação integral da fatura Itaú Personnalité2026-04de mesmo valor. Os33itens permaneciam sem classificação econômica por esse aceite. Não criar despesa pelo total ou reimbursementbatch automático; classificação empresarial posterior não cria segunda saída de caixa. Preservar SOURCE_DESCRIPTION; DISPLAY_DESCRIPTION_OVERRIDE só para itens explicitamente enumerados e sem alterar valor/fonte/classificação. A decisão pediu não retomar entrevista e apresentar próximo prematch após persistência/validação. Este registro recupera autoridade/intenção, não comprova que a gravação ocorreu. Fonte: unidades 30765.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
