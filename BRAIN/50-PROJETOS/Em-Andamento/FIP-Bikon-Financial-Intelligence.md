# FIP Bikon Financial Intelligence

```yaml
nome: FIP Bikon Financial Intelligence
status: production_private_fcoc16_darth_weekly_operation_active_card_classification_in_progress
responsavel: Puppet Master
inicio: 2026-08-09
fim:
prioridade: alta
ultima_revisao: 2026-08-26
tags: [bikon, financeiro, fip, pnl, forecast, scenario, tailscale, go-live, chg004, intake, archive, darth]
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
- Intake documental produtivo nao deve executar fixture sintetica contra producao. Se isso ocorrer, a neutralizacao precisa registrar estado explicito, rollback logico e trilha append-only, mesmo quando delta canonico e impacto financeiro forem zero.

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

## Atualizacao 2026-08-19

`FIP_DOCUMENT_INTAKE_GATEWAY_V1_0_0=PASS` implantou o gateway permanente de intake documental como primeiro componente de classe em `projects/fip/intake/`:

- workflow privado do Puppet via skill `fip-document-intake-gateway`;
- contratos aceitos de source immutability, idempotencia, document detection, state machine, parser contract, reconciliation gate, canonical promotion, human decision queue, password security e personal card privacy;
- canario produtivo contra fonte Cresol ja ingerida retornou `ALREADY_INGESTED` e delta canonico `0`;
- FCOC ativo evoluiu de `1.5.0` para `1.6.0`, preservando versoes congeladas anteriores;
- `fip-8787.service` permaneceu `active`, HTTP anonimo `/` retornou `401`, dashboard autenticado `/api/dashboard` retornou `200`, caixa oficial seguiu R$ 10.801,39 no cutoff `2026-08-17T20:21:32-03:00`;
- cobertura preservada: Caju `7`, FGTS `12`, INSS `9`, Itau Personnalite `8`, Mercado Pago `8`, Payroll `15`, Santander `8`, Simples `25`, classificacoes de cartao `335` e sessoes de entrevista `6`;
- contadores de seguranca ficaram zerados: mutacao de bytes fonte, senha persistida/logada/argv, residuo temporario de decriptacao, restart do servico FIP, mutacao das portas `8787`/`9213`, card interview e Relatorios Operacionais.

Durante a validacao, uma fixture sintetica `SIMPLES` foi executada por engano contra producao. Ela foi neutralizada no mesmo intake como source `ROLLED_BACK/ARQUIVADO`, tax obligation `ROLLED_BACK`, decision `ROLLED_BACK` e audit append-only; nenhum caixa, cartao, FCOC antigo, Relatorios Operacionais, `8787` ou `9213` foi alterado por essa fixture.

## Atualizacao 2026-08-20

A retomada do FIP Google Drive Archival Storage foi concluida com `PASS`, tratando primeiro o estado interrompido:

- registry canonico `projects/fip/data/fip_archive_registry.sqlite3` reautenticado, com os 3 objetos em `UPLOAD_STARTED` reconciliados contra o Drive;
- como nao havia objeto remoto integro correspondente para esses 3 uploads, eles foram recuperados para `LOCAL_HASHED` antes do processamento, sem repetir exclusao insegura;
- objetos `ARCHIVE_AND_RELEASE` fechados: `356/356`;
- pendentes `ARCHIVE_AND_RELEASE`: `0`;
- validacoes finais: `sqlite integrity_check=ok`, `UPLOAD_STARTED=0`, `no_unverified_local_delete=true` e `active_runtime_local_release_count=0`;
- espaco liberado efetivo na VPS por delta de filesystem: `9.066.463.232` bytes;
- payload logico registrado em release manifest: `9.160.638.953` bytes;
- tamanho final do projeto FIP: de `11.703.546.113` para `2.799.574.529` bytes;
- `reports/backups`: de `8.954.126.977` para `49.053.696` bytes;
- evidencia local: `/data/.openclaw/workspace/projects/fip/reports/fip-drive-archive-v1.0.0/final-archive-report.json`;
- registry final SHA-256: `96edb9ed377d1a0c32c55c0f04cee26e42f91554bb5f96ea7086d7983332d89d`.

Ficaram preservados fora do escopo da retomada objetos `ARCHIVE_KEEP_LOCAL`, `KEEP_LOCAL`, `DEFER_AMBIGUOUS` e 5 `PURGE_REGENERABLE` pequenos. Qualquer limpeza desses grupos exige autorizacao separada.

## Atualizacao 2026-08-23/24

A requalificacao do FIP pelo runtime dedicado da Darth Vader fechou `PASS`, sem reabrir nem redesenhar a Golden Baseline `DARTH_DEDICATED_GATEWAY_V1.0.0`:

- `DARTH_FIP_RUNTIME_AUTHORITY=DEDICATED_DARTH`;
- `DARTH_TO_FIP_REAL_CANARY=PASS_READONLY`;
- `DARTH_FIP_BINDING=PASS`;
- `FIP_DATA_LOSS=0`;
- `FIP_DUPLICATE_PROTECTION=PASS`;
- `DARTH_FIP_TELEGRAM_WORKFLOW=PASS`;
- `FIP_WEEKLY_CLASSIFICATION_MODE=ACTIVE`;
- `FIP_PENDING_QUEUE=READY`;
- `DARTH_FINANCIAL_CLASSIFICATION_READY=PASS`.

Estado financeiro autenticado na requalificacao:

- fontes `48`;
- transacoes `3484`;
- classificadas `2792`;
- transacoes em revisao `692`;
- receita reportada R$ 2.443.859,64;
- despesa reportada R$ 1.418.140,88;
- caixa corrente R$ 10.801,39 reconciliado;
- FCOC ativo `1.6.0 FROZEN`;
- testes automatizados FIP `40/40 PASS`.

O fechamento de integridade financeira gerou um conjunto final de `16` cards operator-facing, total R$ 1.395.651,35, com R$ 500.294,54 potencialmente relevante para P&L e `692` revisoes transacionais restantes. A fila esta pronta para decisao humana via Darth direto, mas nao autoriza classificacao automatica de ambiguidades.

Gates financeiros que permanecem fechados:

- NFS-e agosto/2026: `13` eventos/R$ 48.832,88 aceitos como receita incremental, `6` eventos/R$ 5.783,16 neutralizados como evidencia fiscal duplicada e `8` eventos/R$ 31.741,02 em risco de duplicidade; R$ 37.524,18 nao devem entrar no P&L aceito sem prova ou neutralizacao.
- Recebiveis precisam de composicao por titulo/cliente/NFS-e antes de receita nova.
- Partes relacionadas e reembolsos exigem decisao por padrao, nao inferencia por nome.
- Parcelas de financiamento exigem contrato/cronograma; principal nao e despesa.
- Settlement Mastercard julho permanece fail-closed ate fatura/ciclo correto ou tratamento explicito.

Operacao esperada: Hebert pode trabalhar a fila pelo bot Darth direto; cada decisao financeira precisa ser explicita antes de persistencia/regra. NFS-e, boleto, remessa, pagamento, banco, e-mail externo, novas fontes e mudancas de backend continuam exigindo gates proprios.

## Atualizacao 2026-08-25

FIP avancou em liquidacao estrutural e classificacao de cartoes por decisao humana, preservando gates financeiros:

- Santander statement settlement 2026-04 fechou `SANTANDER_EXACT_SETTLEMENT_CONFIRMATION=PASS`;
- fatura Santander 2026-04: R$ 10.315,46, vencimento 2026-04-18;
- transacao bancaria vinculada: `bank_tx_008797e1f4f3788bd87b7ce6`, 2026-04-22, R$ 10.315,46;
- diferenca: R$ 0,00;
- `57` itens subjacentes preservados como `STILL_REQUIRED`;
- nenhuma classificacao de item, batch de reembolso, FCOC, cursor de entrevista, fato bancario ou caixa corrente foi mutado por esse settlement.

Classificacao recorrente por decisao humana:

- batch 1 fechou `PASS`, classificando `26` itens e criando `6` display overrides, sem regras futuras;
- batch 2 fechou `PASS`, classificando `39` itens adicionais, sem regras futuras;
- total das duas rodadas: `65` itens classificados;
- classificacoes humanas totais passaram de `361` para `400`;
- itens recorrentes atuais passaram de `201` para `162`;
- grupos recorrentes atuais passaram de `39` para `33`;
- itens nao resolvidos passaram de `733` para `694`;
- SQLite `quick_check=ok`;
- contadores de mutacao para bank facts, settlement, FCOC, reimbursement batch, cursor de entrevista e cash anchor ficaram zerados.

Limite: essas decisoes reduzem a fila e melhoram a base economica, mas nao criam regras futuras automaticas. Santander/Amazon/seguros e demais lotes pendentes continuam dependendo de decisao humana explicita.

## Proximos passos

- Operar FIP como baseline privada aceita para consulta executiva, previsao e cenarios da BIKON.
- Tratar novas fontes, regras, exposicoes, imports ou alteracoes de forecast como gates pos-GO-LIVE independentes.
- Coletar/importar documentos para os gaps de confiabilidade do forecast antes de promover `v1.2.0`.
- Usar o gateway de intake documental para novas fontes somente quando o tipo de documento tiver parser/reconciliation gate, protecao de segredo e privacidade de cartao pessoal adequados.
- Sanitizar evidence packs futuros para nao registrar headers de autenticacao nos JSONs de smoke.
- Avancar novos settlements de recebiveis ou Itau somente depois de encerrar o fluxo Mercado Pago autorizado ou receber gate proprio.
- Manter evidencias, backups, prints e exports em `projects/fip/`, fora do Brain/Git.
- Para Santander, aceitar senha/CPF somente por canal local no-echo aprovado; nao receber por Telegram, argv, log, banco ou relatorio.
- Tratar limpeza adicional de objetos fora do escopo do archive como nova unidade autorizada.
- Resolver os `16` cards finais da fila semanal pelo Darth dedicado, sem promover ambiguidades para P&L por inferencia.

## Relacoes

- [[20-EMPRESAS/BIKON/README|BIKON]]
- [[60-AGENTES/DARTH-VADER|Darth Vader]]
- [[40-CONHECIMENTO/Financeiro/Natureza-economica-provada-antes-de-PnL|Natureza economica provada antes de PnL]]
- [[40-CONHECIMENTO/Financeiro/Consulta-gerencial-nao-e-permissao-operacional|Consulta gerencial nao e permissao operacional]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
