# FIP Bikon Financial Intelligence

```yaml
nome: FIP Bikon Financial Intelligence
status: production_private_fcoc15_systemd_current_cash_pass
responsavel: Puppet Master
inicio: 2026-08-09
fim:
prioridade: alta
ultima_revisao: 2026-08-18
tags: [bikon, financeiro, fip, pnl, forecast, scenario, tailscale, go-live, chg004]
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

## Atualizacao 2026-08-12

`FIP_CHG_002_TREASURY_CASH_INTELLIGENCE=PASS` promoveu o FIP para `v1.1.0 FROZEN_PASS` com modelo de tesouraria e caixa:

- conta Cresol principal inventariada: agencia `1708`, conta mascarada `***846-7`, BRL, ativa;
- anchors oficiais aceitos do app Cresol: fechamento 2026-08-10 R$ 17.788,22 e fechamento 2026-08-11 R$ 17.001,68;
- saldo calculado FIP em 2026-08-11: R$ 17.001,68, diferenca atual R$ 0,00 e `CURRENT_CASH_AUTHORITY=PASS`;
- ledger diario 2026-08-11: abertura R$ 17.788,22, entrada R$ 1.800,00, saida R$ 2.586,54, fechamento R$ 17.001,68;
- forecast CHG-002 projetou primeiro caixa negativo em 2026-08-20 no cenario base e necessidade adicional de capital de R$ 13.553,93;
- P&L canonico, transacoes bancarias e actuals permaneceram sem regressao; porta `8787` continuou em loopback/Tailscale e porta `9213` ficou intocada.

`FIP_CHG_003_CASH_FORECAST_RELIABILITY` passou tecnicamente, mas nao virou baseline congelada:

- testes automatizados `17/17`, API autenticada `200`, API anonima `401`, validacao desktop/mobile `PASS` e regressoes de tabelas protegidas `PASS`;
- ponte 30 dias fechou exatamente: R$ 17.001,68 + R$ 81.855,10 - R$ 60.227,33 = R$ 38.629,45;
- menor caixa projetado: -R$ 12.384,86 em 2026-09-03; primeiro negativo: 2026-08-20;
- cobertura documental material ficou parcial: entradas confirmadas 38%, saidas confirmadas 0%, abaixo da meta de 80%;
- `FIP v1.2.0` ficou como candidato `NOT_FROZEN`, dependente de evidencias materiais de SIMPLES, Mastercard, TiFLux, folha/pro-labore e Bitrix24 antes de promocao.

## Atualizacao 2026-08-14/15

`FIP-CHG-004-FINANCIAL-CANONICAL-BACKEND-FOUNDATION` ampliou o FIP para backend canonico 2026, preservando a producao privada e sem reescrever tabelas legadas:

- evidence set 2026 validado por ZIP SHA-256 `0a2a4a03c8080ef636d91c80df9841d3377e5661a4001080bc464259896483a7` e `MANIFEST.sha256` `066d306259a66b5881c59d652b4afd734b557080a29b6d2cb181ec86bdd9683a`;
- schema aditivo criado/preservado para registry de fontes, entidades legais, banco 2026, reconciliacao bancaria, cartoes, entrevistas, reembolso, folha, Caju, impostos, grupos, contratos, recebiveis e invariantes;
- banco 2026: `546` transacoes unicas, entrada R$ 715.914,41, saida R$ 700.271,90, `177` anchors de saldo, `14` overlaps deduplicados e `0` conflitos;
- cartoes pessoais: Mercado Pago e Itau permanecem em quarentena privada, sem expor merchant/descricao em relatorio, com `0` classificacoes automaticas e `0` despesa/reembolso criado;
- backend geral ficou `PARTIAL_PASS` porque Caju, cartoes, folha/impostos e membership/contratos exigiam evidencias ou decisoes adicionais antes de promocao canonica.

`FIP_CHG_004_STRUCTURAL_CANONICAL_CLOSURE=PASS` fechou parte dessas lacunas sob decisao humana e fontes reconciliadas:

- politica F N Souza/Felipe: `RELATED_PARTY_OBLIGATION_ASSUMED_BY_BIKON`, autoridade Hebert, 5 obrigacoes e R$ 607,96 pagos/assumidos com Bikon cash, sem criar recebivel contra Felipe;
- 7 faturas Cresol processadas e plenamente reconciliadas como statements, com double-cost invariants zerados;
- Caju recuperado: 7 documentos, R$ 9.996,00 alimentacao, R$ 3.650,00 mobilidade, split por funcionario ainda pendente em 7 lotes, sem alocacao inventada;
- folha enriquecida com 15 periodos/documentos e 5 identidades de funcionarios;
- FGTS/INSS/payroll-tax crosswalk e bank settlement linking ficaram `PARTIAL_PASS` por limitacao documental/comparabilidade, nao por parser defect.

`FIP_CHG_004_CRESOL_RECEIVABLE_PORTFOLIO_INCREMENTAL=PASS` criou backend de carteira Cresol:

- 231 titulos 2026, 24 clientes, 16 titulos abertos vencidos somando R$ 170.331,83;
- 200 titulos liquidados somando R$ 519.324,42, 12 baixas manuais pre-maio/R$ 54.708,69 tratadas como politica de write-off, sem caixa sintetico;
- metodologia de settlement exige data de pagamento, proximo dia util, soma exata de lote e token bancario `credito titulos cobranca propria`, nunca match por valor isolado;
- permanecem 13 titulos liquidados sem prova bancaria de lote e 7 grupos de credito bancario sem match ao XLSX, por ausencia de referencia titulo-a-titulo no extrato.

Grupo Unus foi congelado como membership canonico por decisao de Hebert, sem inferencia por nome:

- 8 CNPJs ativos aprovados: INTESS, TAG Assistencia, Cooperativa de Trabalho dos Proprietario, TDK Corretora, UNUS Holding, TK Reguladora, BR Center Truck e TK Assistencia;
- recorte 2026: 74 titulos/R$ 546.827,05; 15 abertos vencidos/R$ 168.285,02; 51 liquidados/R$ 317.954,87; 7 baixas manuais/R$ 50.942,96;
- Grupo Unus representa 98,80% da carteira aberta atual medida no FIP.

Filas de cartoes pessoais:

- Mercado Pago: parser antigo contaminou janeiro como uma linha; reparo source-native reconciliou 7 faturas, substituiu 276 linhas antigas por 324 itens privados quarentenados, com primeira entrevista valida em `01 janeiro.pdf` e 65 itens.
- Itau Personnalite: validacao source-native por coordenadas bbox reconciliou 8 faturas, marcou a fila atual como `INVALID_REPAIRED` e identificou 282 itens privados para fila reparada; entrevista Itau vem depois de Mercado Pago.
- Prematch de reembolso pausou a entrevista Mercado Pago: 82 transferencias Bikon -> Hebert em 2026/R$ 193.525,56, 22 conhecidas como nao reembolso/R$ 68.457,97, 60 candidatas/R$ 125.067,59, sem classificar itens, criar batches ou mutar banco.
- Confirmacao restrita de settlement da fatura Itau `2026-01` registrou transferencia R$ 7.681,79 contra fatura R$ 7.681,79, diferenca R$ 0,00, preservando 39 itens pendentes de classificacao economica.

## Guardrails

- Nao transformar credito bancario, PIX, boleto, fatura de cartao ou recorrencia em receita/despesa definitiva sem evidencia economica suficiente.
- Receitas exigem vinculo a NFS-e, contrato, fatura, titulo, carteira de cobranca, decisao humana registrada ou evidencia equivalente.
- Pagamento de cartao e liquidacao de boleto podem ser settlement/passivo/clearing; P&L usa eventos economicos, nao o caixa bruto por aparencia.
- GO-LIVE financeiro exige regressao de totais, backup, rollback provado, autenticacao, boundary de rede e validacao visual.
- A porta `8787` permanece em fronteira privada/controlada; nao publicar senha, token ou segredo em URL, relatorio ou Brain.
- Porta `9213` e outros apps nao devem ser alterados por mudancas FIP sem autorizacao propria.
- Toda alteracao pos-GO-LIVE deve ter backup, rollback, regressao financeira, smoke autenticado/anonimo e validacao de que DB/actuals mudaram apenas quando explicitamente autorizado.
- Forecast e cenario nao devem inflar confianca quando a cobertura documental material estiver abaixo do alvo; promover apenas como candidato/partial pass ate receber evidencias suficientes.
- CHG-004 nao autoriza classificar cartao pessoal por inferencia: settlement de fatura, match de transferencia ou fila reconciliada provam estrutura/liquidacao, nao natureza economica dos itens.
- Estados de elegibilidade canonica e motivos de bloqueio devem ser colunas/flags separados; consultas por texto como `LIKE '%CANONICAL%'` nao devem virar criterio financeiro.
- Carteira Cresol, Grupo Unus e prematches de reembolso sao bases gerenciais/estruturais ate haver autorizacao propria para cobranca, baixa, classificacao, P&L ou comunicacao externa.

## Atualizacao 2026-08-17/18

FIP evoluiu a camada semantica e operacional sem ampliar permissoes externas:

- FCOC ativo passou a `1.5.0 FROZEN`, preservando artefatos anteriores e adicionando semanticas de compromissos mensais de socios, partner clearing, Claude/Anthropic, cronogramas Kepler/Amauri/notebook e a correcao de que notebook/Freire e reembolso de Felipe para a Bikon, sem caixa sintetico;
- compromissos mensais registrados: Felipe R$ 16.349,00/mes, com R$ 6.898,70 dia 05 e R$ 9.450,30 dia 15 para Camila como destinataria operacional; Hebert R$ 9.780,00/mes apenas em nivel de cenario enquanto data de pagamento exige confirmacao humana;
- clearing Felipe: Claude bruto R$ 1.100,00, parte Felipe R$ 569,00, custo liquido Bikon R$ 531,00; notebook/Freire corrige setembro-novembro para R$ 1.069,00/mes em favor da Bikon e, de dezembro em diante, R$ 569,00/mes enquanto Claude permanecer ativo;
- entrevista Mercado Pago janeiro-julho foi retomada e ficou com `0` pendencias, `335` classificacoes totais de cartao no backend; Mercado Pago tem 251 `BUSINESS_DIRECT`/R$ 26.683,17 e 73 `PERSONAL_PRIVATE`/R$ 6.160,59; Itau Personnalite permanece `READY_NOT_STARTED_SOURCE_RECONCILED` com 271 itens pendentes;
- reconciliacao incremental Cresol registrou extrato oficial de 2026-08-17T20:21:32-03:00, 31 linhas parseadas, 6 novos fatos bancarios, 25 identicos ja existentes, 2 fatos existentes linkados ao novo cutoff, diferenca R$ 0,00 e saldo oficial corrente R$ 10.801,39; limite de credito R$ 30.000,00 e saldo disponivel R$ 40.801,39 nao foram promovidos a caixa;
- backend `8787` passou para `fip-8787.service` em `systemd --user`, com MainPID como autoridade canonica, autorestart validado, hardening minimo, `127.0.0.1:8787` privado/autenticado, Tailscale tailnet-only e porta `9213` intocada;
- cenario Grupo Unus para Relatorios Operacionais reduziu os eventos futuros ativos de R$ 42.942,42/mes para R$ 24.000,00/mes por fator proporcional `0.55888792`, substituindo o valor canonico no cenario e sem mutar actuals; receita cenario R$ 85.143,84 e Simples R$ 11.745,95/mes foram calculados com perfil canonico, nao com fallback de 6%;
- tentativa de fechamento documental Santander/MP agosto validou pacote, mas falhou fechado porque Santander exige CPF/senha e nao havia canal local no-echo aprovado; Mercado Pago agosto foi apenas parseado read-only, com total R$ 4.987,28, vencimento 2026-08-20 e diferenca R$ 0,00, sem ingestao produtiva.

## Proximos passos

- Operar FIP como baseline privada aceita para consulta executiva, previsao e cenarios da BIKON.
- Tratar novas fontes, regras, exposicoes, imports ou alteracoes de forecast como gates pos-GO-LIVE independentes.
- Coletar/importar documentos para os gaps de confiabilidade do forecast antes de promover `v1.2.0`.
- Iniciar a entrevista Mercado Pago apenas com autorizacao atomica `START_FIP_PERSONAL_CARD_CLASSIFICATION_INTERVIEW_MERCADO_PAGO_REPAIRED_QUEUE`.
- Sanitizar evidence packs futuros para nao registrar headers de autenticacao nos JSONs de smoke.
- Avancar novos settlements de recebiveis ou Itau somente depois de encerrar o fluxo Mercado Pago autorizado ou receber gate proprio.
- Manter evidencias, backups, prints e exports em `projects/fip/`, fora do Brain/Git.
- Para Santander, aceitar senha/CPF somente por canal local no-echo aprovado; nao receber por Telegram, argv, log, banco ou relatorio.

## Relacoes

- [[20-EMPRESAS/BIKON/README|BIKON]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]
- [[40-CONHECIMENTO/Financeiro/Natureza-economica-provada-antes-de-PnL|Natureza economica provada antes de PnL]]
- [[40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional|Consulta gerencial nao e permissao operacional]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
