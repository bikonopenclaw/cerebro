---
id: brain-e194d40bcff4caf684f8
type: knowledge
title: Natureza economica provada antes de PnL
created: '2026-09-21T19:15:09.943981Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:18:32.790773Z'
---

# Natureza economica provada antes de PnL

```yaml
categoria: financeiro
fonte: consolidacao FIP Bikon de 2026-08-10/11; CHG-004 de 2026-08-14/15; consolidacao semanal 2026-W33
confiabilidade: alta
ultima_revisao: 2026-08-16
tags: [financeiro, pnl, fip, bikon, competencia, evidencia, go-live, cartao, privacidade]
```

## Regra

Credito bancario, PIX, boleto, fatura de cartao, recorrencia ou similaridade textual nao entram no P&L aprovado por aparencia. Primeiro deve existir natureza economica provada, com vinculo suficiente a cliente, contrato, NFS-e, fatura, titulo, competencia, decisao humana registrada ou evidencia equivalente.

## Aplicacao pratica

- Separar caixa bruto de evento economico.
- Manter recebimentos sem prova como `recebimento a identificar`, `adiantamento`, `clearing`, settlement-only ou pendencia gerencial.
- Tratar pagamento de cartao como liquidacao de passivo ate haver fatura/itemizacao suficiente.
- Tratar settlement de fatura ou match de transferencia como prova de liquidacao/estrutura, nao como classificacao economica automatica dos itens.
- Manter itens de cartao pessoal em camada privada/quarentenada ate decisao humana ou fonte autorizada; relatorio gerencial nao deve expor merchant/descricao sem necessidade.
- Tratar principal de financiamento e transferencias internas fora do P&L, salvo componente economico provado.
- Usar materialidade para priorizar revisao, nao para esconder incerteza.
- Fechar GO-LIVE somente quando pendencias materiais estiverem zeradas ou explicitamente segregadas fora do resultado aprovado.

## Exemplo conectado

No FIP BIKON, a reconstrucao 2025 so foi aceita depois de cruzar titulos, pagadores, datas, valores e decisoes humanas. PIX sem evidencia deterministica ficou bloqueado ate decisao registrada. O residual Mastercard de R$ 39,80 mostrou que a competencia correta precisa vir da evidencia da fatura/ciclo, nao de uma regra superficial sobre o inicio do intervalo.

No FIP CHG-004, Mercado Pago e Itau foram reconciliados em nivel source-native, mas os itens pessoais permaneceram privados e sem classificacao. A confirmacao de uma fatura Itau de R$ 7.681,79 com diferenca R$ 0,00 provou settlement, nao despesa empresarial; os 39 itens seguiram exigindo classificacao economica.

## Relacoes

- [[50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence|FIP Bikon Financial Intelligence]]
- [[40-CONHECIMENTO/Financeiro/Settlement-de-fatura-nao-classifica-natureza-economica|Settlement de fatura nao classifica natureza economica]]
- [[40-CONHECIMENTO/Financeiro/Validacao-source-native-de-PDF-financeiro|Validacao source-native de PDF financeiro]]
- [[40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional|Consulta gerencial nao e permissao operacional]]
- [[40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais|Dados mestres completos em automacoes fiscais]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]

## Complementos reconciliados — lote 6 de 2026-09-21

Caso de planejamento familiar de junho/2026: Hebert pediu que o blueprint cobrisse receitas/despesas e também reservas e investimentos. A taxonomia deve preservar esses conceitos como naturezas distintas, sem transformar automaticamente transferência patrimonial em despesa de consumo. É requisito histórico de desenho, não classificação ou recomendação de investimento para transações atuais. Fonte: unidades 29799.

Na entrevista histórica de cartão, PRIMEBOX aparecia em duas compras parceladas distintas (valores e ciclos diferentes), ambas ainda sem resposta. A decisão humana deve se vincular à identidade da compra/grupo de parcelas; coincidência de estabelecimento não permite reaplicar resposta ou encerrar outra pendência. O exemplo não afirma status financeiro atual nem autoriza classificação. Fonte: unidades 35236.

Na entrada de despesas por foto/documento, tipo de conta/estabelecimento não basta para inferir natureza econômica. Quando a categorização não puder ser sustentada pela fonte, pedir esclarecimento à pessoa que lança. Escopo histórico incluiu contas de água/luz (Sanepar/Copel) e diferentes notas; não torna qualquer compra em um fornecedor pessoal ou empresarial por padrão. Fonte: unidades 29801.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
