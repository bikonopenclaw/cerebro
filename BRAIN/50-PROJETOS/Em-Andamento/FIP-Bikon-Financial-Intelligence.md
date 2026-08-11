# FIP Bikon Financial Intelligence

```yaml
nome: FIP Bikon Financial Intelligence
status: production_go_live_pass_private_tailnet
responsavel: Puppet Master
inicio: 2026-08-09
fim:
prioridade: alta
ultima_revisao: 2026-08-11
tags: [bikon, financeiro, fip, pnl, forecast, scenario, tailscale, go-live]
```

## Objetivo

Implantar uma base executiva financeira da BIKON para P&L canonico, forecast e cenarios, com origem bancaria/economica reconciliada, autenticacao, rollback, regressao financeira e exposicao restrita a fronteira privada.

O Brain registra estado consolidado, decisoes e guardrails. Bancos, exports, prints, backups, credenciais e evidencias detalhadas permanecem em `projects/fip/`, fora do Brain/Git.

## Estado consolidado

- FIP passou por arquitetura BAFT e base de fontes bancarias canonicas antes de GO-LIVE; fonte operacional consolidada manteve `1438` cash transactions canonicas.
- A reconstrucao 2025 rejeitou conversao generica de recebimento bancario em receita: o XLSX `1786384694059.xlsx` foi tratado como `TITLE_RECEIVABLE_MAP`, com `480` registros validos, `303` title records casados, `92` recebimentos de cobranca propria, R$ 967.991,33 reconstruidos e anti-double-revenue `PASS`.
- A etapa residual resolveu `5` recebimentos de cobranca propria/R$ 95.947,89 e manteve PIX sem vinculo deterministico como decisao humana ate receber evidencias suficientes.
- A decisao humana final dos PIX fechou `FIP_FINAL_FINANCIAL_INTEGRITY=PASS`: `7` cards PIX resolvidos, R$ 18.121,45 de nova receita de servico, R$ 1.500,00 Boss Paper mantido como settlement-only, pendencias materiais `0`/R$ 0,00 e cash count preservado em `1438`.
- Primeiro gate de GO-LIVE falhou fechado por divergencia exata de R$ 39,80 no `FIP_FINANCIAL_REGRESSION_LOCK`; a causa foi evento residual Mastercard da fatura `02-2026.pdf` classificado no ano errado por bug de intervalo temporal.
- Reconciliacao exata do residual R$ 39,80 fechou `FIP_PRODUCTION_GO_LIVE=PASS` em 2026-08-10. Totais finais aceitos: receita canonica R$ 2.443.859,64, despesa R$ 1.418.140,88, resultado R$ 1.025.718,76; 2025 receita R$ 1.171.645,03, despesa R$ 359.538,86, resultado R$ 812.106,17; 2026-current receita R$ 1.272.214,61, despesa R$ 1.058.602,02, resultado R$ 213.612,59.
- Estado tecnico final: DB produtivo SHA-256 `13854b791edeeaf253d872401eb16f2533f897dd3c47efc918b64336edff59fd`, manifest de aplicacao `ebd973bec08694a250883c431bdf85997ea6fcc0ee2acf45381f747a45e450e8`, export canonico `1c1ef38f1b8ffa32a689e7d930174d0ca96fddfdd5cde6d0a8b0152a86563450`, source-set `23a9c837af99dfe52ef82eb63114f60a23dbafdbd52d98499361f5a177a57bd3`.
- Seguranca/operacao: app em `127.0.0.1:8787`, anonimo dashboard/API `401`, autenticado API `200`, cookie `HttpOnly; SameSite=Lax; Max-Age=43200`; `Secure` documentado como indisponivel no transporte HTTP local.
- Backup/rollback: backup final `FIP_PRODUCTION_BACKUP_20260810T195743Z.tar.gz`, SHA-256 `5d0638a9306b639593662538b3b7d0895aef15c87bebb0f082c10236a9b902f8`, validacao de restore isolado e equivalencia `PASS`.
- Validacao visual: desktop e mobile `PASS`; testes automatizados `PASS`; Scenario Studio consumiu baseline canonica sem mutar actuals.
- Mudanca pos-GO-LIVE em 2026-08-10 criou rota Tailscale tailnet-only `https://srv1811702.tail34aee8.ts.net:8787/`, proxy para `127.0.0.1:8787`, sem Funnel/public Internet na porta `8787`; hash do DB permaneceu inalterado e porta `9213` ficou intocada.

## Guardrails

- Nao transformar credito bancario, PIX, boleto, fatura de cartao ou recorrencia em receita/despesa definitiva sem evidencia economica suficiente.
- Receitas exigem vinculo a NFS-e, contrato, fatura, titulo, carteira de cobranca, decisao humana registrada ou evidencia equivalente.
- Pagamento de cartao e liquidacao de boleto podem ser settlement/passivo/clearing; P&L usa eventos economicos, nao o caixa bruto por aparencia.
- GO-LIVE financeiro exige regressao de totais, backup, rollback provado, autenticacao, boundary de rede e validacao visual.
- A porta `8787` permanece em fronteira privada/controlada; nao publicar senha, token ou segredo em URL, relatorio ou Brain.
- Porta `9213` e outros apps nao devem ser alterados por mudancas FIP sem autorizacao propria.
- Toda alteracao pos-GO-LIVE deve ter backup, rollback, regressao financeira, smoke autenticado/anonimo e validacao de que DB/actuals mudaram apenas quando explicitamente autorizado.

## Proximos passos

- Operar FIP como baseline privada aceita para consulta executiva, previsao e cenarios da BIKON.
- Tratar novas fontes, regras, exposicoes, imports ou alteracoes de forecast como gates pos-GO-LIVE independentes.
- Manter evidencias, backups, prints e exports em `projects/fip/`, fora do Brain/Git.

## Relacoes

- [[20-EMPRESAS/BIKON/README|BIKON]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]
- [[40-CONHECIMENTO/Financeiro/Natureza-economica-provada-antes-de-PnL|Natureza economica provada antes de PnL]]
- [[40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional|Consulta gerencial nao e permissao operacional]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
