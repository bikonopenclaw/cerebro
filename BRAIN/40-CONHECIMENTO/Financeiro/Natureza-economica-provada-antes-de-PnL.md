# Natureza economica provada antes de PnL

```yaml
categoria: financeiro
fonte: consolidacao FIP Bikon de 2026-08-10/11; CHG-004 de 2026-08-14/15
confiabilidade: alta
ultima_revisao: 2026-08-15
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
- [[40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional|Consulta gerencial nao e permissao operacional]]
- [[40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais|Dados mestres completos em automacoes fiscais]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]
