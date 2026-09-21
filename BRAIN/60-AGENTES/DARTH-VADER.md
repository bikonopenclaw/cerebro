---
id: brain-bb1cb60bf742a053139d
type: entity
title: Darth Vader
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:32:09.804705Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/60-AGENTES/DARTH-VADER.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/60-AGENTES/DARTH-VADER.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/60-AGENTES/DARTH-VADER.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/60-AGENTES/DARTH-VADER.md#relações
---

# Darth Vader

```yaml
categoria: agente_operacional
fonte: sessões operacionais visíveis, configuração de skills em 2026-06-17, snapshot versionado em 2026-07-11, fechamento/paridade dedicada em 2026-08-23/24 e lote BIKON 4.1 em 2026-08-27
confiabilidade: alta
ultima_revisao: 2026-08-28
tags: [agente, financeiro, faturamento, nfse, boleto, remessa, cresol-api, fip]
```

## Papel

Agente operacional financeiro usado para tarefas de faturamento, NFS-e, boletos, remessas e conferências cadastrais quando a execução exigir especialização financeira/fiscal.

## Skills e contextos relevantes

- `notaas-nfse`: uso exclusivo da Darth Vader para NFS-e da Bikon, com segredos fora do Brain/Git.
- `emitir-nfse-boleto-remessa`: skill geral relacionada a NFS-e, boletos, remessas e API Cresol.
- `boletos-cresol`: skill técnica relacionada a boletos Cresol.

## Contextos removidos / históricos

- `faturamento-fn-souza`: estrutura inicial criada em 2026-06-17 para o fluxo de faturamento FN Souza, removida do conjunto ativo em 2026-06-25. Não deve ser acionada como skill ativa sem nova autorização explícita e novo escopo operacional.

## Guardrails

- Não emitir NFS-e real sem aprovação explícita.
- Não emitir boleto real sem aprovação explícita.
- Não gerar remessa de produção sem validação e aprovação explícita.
- Não usar API Cresol em produção sem aprovação explícita.
- Não executar baixa automática via API Cresol enquanto não houver procedimento próprio aprovado.
- Não enviar comunicação externa em nome da Bikon sem aprovação explícita.
- Pode preparar rascunhos, estrutura de arquivos, conferências e lista de pendências internas.
- Para NFS-e + boleto + remessa em lote, manter produção assistida e cadenciada: dry-run, conferência humana, aprovação explícita, emissão, conferência XML/PDF, depois boleto/remessa e só então comunicação externa.
- Não operar a esteira completa de NFS-e + boleto + remessa + e-mail como fluxo único sem pausas de validação.

## Revisão pré-produção 2026-06-30

Darth Vader registrou revisão segura do fluxo NFS-e + boleto + remessa antes de novo lote em produção. Veredito consolidado: não liberar automação direta da esteira completa; permitir apenas produção assistida, com travas por etapa.

Pontos críticos: cadastro do tomador deve usar identificador único quando houver ambiguidade; `seq_remessa`, `numero_documento` e `nosso_numero` não devem ser inferidos; e-mail externo depende de anexos conferidos e aprovação; upload no portal Cresol exige validação local da remessa e confirmação do Hebert.

## Cresol API, 2026-07-08/09

A skill `emitir-nfse-boleto-remessa` passou a prever a API de boletos Cresol como camada futura para registro de títulos oficiais, PDF oficial, consulta de status, alteração de vencimento e ocorrências.

Estado consolidado:

- Fase 1 documentada com guardrails, mantendo CNAB/remessa como fallback e auditoria.
- Fase 2 criou cliente CLI de homologação, com produção bloqueada por padrão e escrita exigindo `--allow-write`.
- Credenciais ficam somente em arquivo secreto local, fora do Brain/Git/snapshot.
- Testes de homologação validaram autenticação, parâmetros da conta, espécies, listagem de títulos, pagadores e sequenciais.
- Um título controlado de homologação foi criado com autorização explícita do Hebert; o PDF oficial foi baixado para conferência, mas payloads/respostas/PDFs permanecem fora do Git por serem artefatos de execução.

Pendências:

- Consultar evolução de status do título de homologação antes de usar ocorrências/conciliação.
- Confirmar mapeamento definitivo de juros/multa no payload produtivo: Bikon usa multa de 2,00% após vencimento e juros de 1% ao mês proporcional ao dia.

### Rodada homologacao 2026-08-11

Nova rodada Cresol API em homologacao criou o titulo `22394650` para teste BIKON:

- nosso numero: `09/00000000357-6`;
- valor: R$ 1,00;
- vencimento: 2026-08-18;
- status consultado: `EM_PROCESSAMENTO`;
- PDF oficial baixado via API, SHA-256 `7bb77b5480623ac7b0505a5fefbd0b977a0fb311b1e45ff21de7f8e99b309066`;
- remessa CNAB400 local `cb110857-titulo-22394650-homologacao.rem`, sequencial `2394650`, 3 linhas de 400 posicoes, tipos `0/1/9`, valor total R$ 1,00, validacao estrutural OK e SHA-256 `5602b5efeec58a1e033d2a77cee36644901d15b394ddcdf328848227c76ac2e8`;
- nenhum uso de producao, upload de remessa, baixa ou envio a cliente.

## BI financeiro Bikon, 2026-07-10/11

A workspace da Darth Vader passou a manter camada BI sobre o SQLite financeiro de boletos/NFS-e da Bikon, com views para:

- boletos;
- contas a receber;
- KPIs mensais;
- clientes;
- remessas;
- retornos.

Essa camada serve para consulta gerencial, relatório e conferência. Exports CSV gerados a partir dessas views são dados derivados/sensíveis e não devem ser versionados no Brain/Git.

Kowalski pode consultar a base em modo somente leitura para relatórios. Escrita, alteração de schema, importação de retorno, baixa, pagamento, NFS-e, boleto e remessa continuam exclusivamente com Darth Vader.

## Lote Bikon agosto/2026, remessa 093

Em 2026-08-03, Darth Vader executou produção assistida do lote agosto/2026:

- `27` NFS-e autorizadas em produção, com PDF/XML locais.
- `27` boletos gerados localmente e vinculados às NFS-e.
- `1` remessa CNAB400 local `remessa-093-010826-producao.rem`, SHA-256 `b4616a39ed4c89adb04bab60461c93e8df2dab33c022b4807210809592e56141`.
- Total do lote: R$ 86.357,06.
- `18` e-mails enviados, agrupados por cliente, todos com `financeiro@bikon.com.br` em cópia, status local `sent_all`.
- A remessa bancária foi preparada, mas não há registro consolidado de transmissão ao banco nesta etapa.

## Baseline FBCP, 2026-08-03

Foi concluída a Fase 0 read-only do FBCP com inventário, hashes, leitura SQLite immutable, mapa de mutações e riscos P0, sem chamada Notaas, Cresol, SMTP, remessa, emissão, boleto ou alteração operacional.

Riscos P0 que afetam a governança da Darth Vader:

- competência default fixa em partes da skill Notaas;
- valores tratados como `float` em CLI/helper/e-mail/CNAB;
- retry Notaas sem ledger idempotente;
- aprovação como flag booleana/reutilizável, sem manifest/hash de payload/anexos/destinatários;
- nosso número sem reserva transacional prévia;
- validador CNAB estrutural incompleto;
- envio SMTP sem outbox transacional/recibo forte;
- fronteira homologação/produção baseada em flags e nomes de pasta.

Próxima autorização recomendada: `AUTHORIZE_FBCP_P0_COMPETENCE_AND_MONEY_HARDENING_ONLY`.

## Lote BIKON 4.1, remessa 094

Em 2026-08-27, Darth Vader concluiu o lote assistido depois de tres gates materiais separados: data real de emissao, competencia e data de gravacao da remessa.

- NFS-e `246`, Alfredo Chaves Cartorio do I Oficio, R$ 899,00;
- NFS-e `247`, Donna Industria de Madeiras Ltda, R$ 899,00;
- competencia `08/2026`, emissao `27/08/2026`, vencimento `05/09/2026`, servico `010701`;
- boletos locais de conferencia: documentos `105659` e `105660`, nossos numeros `009/00000001591-4` e `009/00000001592-2`;
- remessa CNAB400 094 local: quatro linhas de 400 caracteres, dois titulos, total R$ 1.798,00, gravacao em 27/08/2026;
- pack validado em `/data/.openclaw/workspace-darth-vader/boletos/lotes-emissao/pack-final-lote-4.1-remessa-094-20260827.tar.gz`.

Estado externo: e-mails apenas em rascunho, sem envio; remessa nao transmitida; boletos sem confirmacao de registro bancario. Envio de e-mail e qualquer registro/transmissao bancaria continuam exigindo autorizacoes proprias.

## FIP Bikon Financial Intelligence, 2026-08-10/11

O FIP virou projeto financeiro proprio da BIKON e nao substitui a responsabilidade operacional da Darth Vader por NFS-e, boletos, remessas, baixas e comunicacao externa.

Estado consolidado:

- `FIP_PRODUCTION_GO_LIVE=PASS` em fronteira privada/controlada.
- Totais aceitos: receita canonica R$ 2.443.859,64, despesa R$ 1.418.140,88, resultado R$ 1.025.718,76; 2025 resultado R$ 812.106,17; 2026-current resultado R$ 213.612,59.
- `1438` transacoes bancarias canonicas, pendencias materiais `0`/R$ 0,00, backup/rollback `PASS`, validacao desktop/mobile `PASS`.
- App produtivo em `127.0.0.1:8787` com rota Tailscale tailnet-only, autenticacao obrigatoria e porta `9213` intocada.

Guardrail financeiro reforcado: o FIP separa caixa bruto de evento economico. Credito bancario, PIX, boleto ou cartao so entram no P&L aprovado com evidencia de natureza economica, competencia e vinculo suficiente; caso contrario ficam em clearing, settlement-only ou pendencia gerencial.

## FIP CHG-004, 2026-08-14/15

Darth Vader atuou como autoridade financeira/read-only em pontos de validacao do CHG-004. Estado consolidado:

- backend canonico 2026 aplicado no FIP com schema aditivo e sem substituir a responsabilidade operacional da Darth Vader por NFS-e, boletos, remessas, baixas e e-mails;
- fechamento estrutural `PASS`, com politica F N Souza/Felipe assumida por Bikon sob autoridade Hebert, Caju/folha/Cresol estruturados e FGTS/INSS/settlements parciais onde a fonte nao permitiu comparacao plena;
- carteira Cresol 2026 consolidada para consulta gerencial, com baixas manuais segregadas e sem caixa sintetico;
- Grupo Unus aceito por decisao humana com 8 CNPJs, sem inferencia por nome;
- cartoes pessoais Mercado Pago/Itau mantidos em quarentena privada; settlement ou prematch de reembolso nao autoriza classificacao economica automatica.

Risco residual observado: um evidence JSON de smoke registrou header de autenticacao. Isso nao altera o veredito financeiro, mas deve ser sanitizado em proxima janela aprovada.

## FIP/FCOC e Relatorios Operacionais, 2026-08-17/18

Darth Vader passou a atuar como worker interno em cenarios FIP solicitados pelo grupo Relatorios Operacionais, com Puppet Master como unico owner externo:

- active FCOC validado como `1.5.0 FROZEN`, com bootstrap/cold-start para compromissos de socios, clearing Felipe/Claude/notebook e regra de nao criar caixa sintetico;
- acesso ao backend FIP canonico `127.0.0.1:8787` validado em leitura/autenticacao, com app supervisionado por `fip-8787.service`;
- parecer do cenario Grupo Unus indicou consistencia aritmetica, sem erro material e baixo risco de dupla contagem se o valor reduzido R$ 24.000,00 substituir, e nao somar, os R$ 42.942,42 canonicos;
- em rotas do grupo, Darth nao deve usar `message` externo diretamente; resultado financeiro volta ao Puppet, que responde uma unica vez no Telegram.

## Gateway dedicado e paridade funcional, 2026-08-23/24

Darth Vader fechou a extracao para runtime Telegram dedicado com aceite de producao e Golden Baseline:

- `DARTH_DEDICATED_GATEWAY_GOAL_RESULT=PASS`;
- `DARTH_GOLDEN_BASELINE_VERSION=DARTH_DEDICATED_GATEWAY_V1.0.0`;
- servico canonico `openclaw-gateway-darth-vader.service`, porta `18840`, runtime unico e `PUPPET_HOSTS_DARTH=NO`;
- aceite Telegram direto pos-rotacao `PASS`, single-writer `PASS` e conflitos 409 pos-rotacao `0`;
- Puppet continua podendo delegar para Darth, mas nao hospeda mais o bot/rota Darth;
- Storage Guard, RSE, PGL e regressao de gateways relacionados fecharam `PASS`;
- rollback boundary validado em `/data/.openclaw/backups/darth-dedicated-gateway-final-boundary-20260823T224831Z`, sem copiar segredo.

Antes do aceite final, a investigacao passiva do conflito Telegram 409 provou `PASS_NO_LOCAL_DUPLICATE_AT_CONFLICT`; a origem ficou `EXTERNAL_OR_NON_LOCAL_UNRESOLVED` ate rotacao owner-exclusive do token pelo Hebert/BotFather. O novo segredo foi vinculado somente pelo tokenfile canonico e nao deve ser transportado por chat.

A auditoria de paridade funcional em 2026-08-24 fechou `DARTH_FULL_FUNCTIONAL_PARITY=PASS`, pacote SHA-256 `b21a1fbfa42035ed96a0ffda4c96ab4865e1c6852667e709460f4617c3c951cc` e `NEW_DARTH_GOLDEN_BASELINE_REQUIRED=NO`. Capacidades legitimas de predecessor permaneceram cobertas por Darth dedicado ou servicos compartilhados canonicos: NFS-e, boletos/remessa, conciliacao assistida, FIP, BI financeiro, reporting, input documental suportado, interface Telegram direta e delegacao Puppet. O item `DARTH_GATEWAY_LOCAL_COMMAND_TOKEN_BINDING=NON_BLOCKING_REVIEW_ITEM` deve ser tratado como revisao tecnica sem bloquear operacao aceita, salvo se virar falha operacional provada.

## Relações

- [[70-AUTOMACOES/NOTAAS-NFSE|Skill Notaas NFS-e]]
- [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]
- [[50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence|FIP Bikon Financial Intelligence]]

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Preferência de tratamento registrada por Hebert: referir-se ao agente Darth Vader no masculino (ele). Fonte: unidades 29025.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.

## Complementos reconciliados — lote 4 de 2026-09-21

No início da proposta de integração SERPRO/PARCSN, o escopo informado por Hebert era somente a própria Bikon, com certificado A1 e contratação Integra Contador ainda pendente. Não estender para terceiros ou inferir procuração/contrato ativo a partir dessa declaração histórica. A recuperação não contrata serviço nem autoriza emissão de guias. Fonte: unidades 34611.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.

## Complementos reconciliados — lote 5 de 2026-09-21

Na preparação SERPRO de 18/06/2026, o controle proposto separava cadastro do parcelamento, parcelas por competência e alertas: valor previsto, guia emitida, pagamento e comprovante são campos distintos. Valor de parcela pode variar e pagamento exige evidência, não mera previsão. Limites legais, prazos e gatilhos de rescisão mencionados no diálogo eram referências históricas e precisam da fonte oficial atual; não preservá-los como regra universal nem executar emissão automática pelo calendário sugerido. Fonte: unidades 34603.

O projeto SERPRO registrou contrato/pedido 540190 da Bikon, datado 18/06/2026, e cobrança por requisição, com referências técnicas na skill em standby. O resumo daquela data citou faixas iniciais de R$ 0,24 consulta, R$ 0,32 emissão e R$ 0,40 declaração, além de prazo de liberação até 10 dias. Esses números são relato histórico do contrato, não preços atuais validados; qualquer novo consumo/contratação depende de contrato e escopo vigentes. Fonte: unidades 34618, 34621, 34627.

Em 18/06/2026, Hebert colocou SERPRO em standby até encontrar forma segura de operar sem entregar seu certificado. A retomada experimental local em02/07 não apagou esse limite de custódia nem liberou emissão fiscal. Arquivo da skill existir ou estar versionado não significa serviço produtivo ativo. Fonte: unidades 34657.

Em 02/07/2026, Hebert determinou que a skill SERPRO ficasse somente no workspace de Darth Vader em standby, para retomada posterior. No mesmo saneamento, ressaltou que Notaas e a esteira notas/boletos/remessa/e-mail eram operação principal e não poderiam ser removidas por parecerem resíduo. Essa decisão histórica exige separar material em espera de dependências realmente usadas antes de limpar skills. Fonte: unidades 35644.

Checkpoint histórico de 02/07/2026: o kit Controle Financeiro Familiar fase4 foi descrito como pacote de instalação limpo, com SQLite/categorias, bot Telegram, OCR Apple Vision/Tesseract, dashboard local, aprovação de pendências, limites de upload e allowlist de chat fail-closed. Banco, uploads, pending, caches e .env real foram excluídos do pacote. Era candidato a teste local controlado, não prova de produção nem identidade automática com o FIP posterior. Fonte: unidades 35695.

No experimento SERPRO de 02/07/2026, PEDIDOSPARC163 e PARCELASPARAGERAR162 responderam com pedidoDados.dados como string vazia; objeto vazio/null tiveram erro. OBTERPARC164 exigiu numeroParcelamento, não numero. Também houve erro local de construção JSON antes da requisição; distinguir rejeição do provider de falha do script. O teste evitou disparar múltiplos payloads por tentativa porque chamadas poderiam ser cobradas. Estas são observações históricas do PARCSN, a conferir no contrato atual antes de nova chamada; não liberam emissão. Fonte: unidades 35746, 35749, 35752, 35755, 35758, 35761, 35770.

No fluxo SERPRO em standby documentado em 02/07/2026, GERARDAS161 permaneceu bloqueado até aprovação específica que identificasse serviço, parcelamento, competência/parcela e valor. Uma eventual primeira emissão seria limitada à unidade aprovada; consultas de pedidos/parcelas não herdavam permissão para /Emitir. Disponibilidade de parcela na consulta não comprova dívida não paga e exige conferência antes de emissão. Fonte: unidades 35776.

O checkpoint SERPRO de 02/07/2026 preserva: skill em standby exclusiva de Darth, Notaas produtivo preservado no saneamento, broker loopback sob custódia do titular, consulta antes de emissão, segredos fora do chat/Git e teste controlado por potencial cobrança. PEDIDOSPARC163 com dados vazio foi o primeiro sucesso; OBTERPARC164 estava em construção e o campo numero foi depois corrigido para numeroParcelamento. Caminhos e próximos passos do resumo são históricos, não autoridade para reativar serviço ou emitir. Fonte: unidades 35782.

Em 03/07/2026, o experimento SERPRO foi mantido no fluxo local solicitado por Hebert após tentativa de túnel para endereço interno inacessível. O controle local agrupava iniciar/parar/testar broker e consultas de pedidos, parcelas e detalhe; DETPAGTOPARC165 era experimental, GERARDAS161 bloqueado. Diagnóstico distinguiu caminho certificado com hífen/underscore e arquivo .env efetivamente lido. A rotina de baixa comparava parcelas disponíveis com demonstrativo, mas presença na API só documenta o estado daquela fonte naquele instante, não nega pagamento externo. Redigir dados para saída não deve corromper o JSON usado no cálculo/parsing; preservar estrutura interna e produzir resumo sanitizado separado. Fonte: unidades 37966, 37981, 37990, 38011, 38026, 38044, 38050, 38062.

Preferência de tratamento registrada por Hebert: Darth Vader e Kowalski no masculino; usar ele/dele para Darth Vader. Trata-se de convenção de comunicação dos agentes, sem alterar papel, permissão ou roteamento. Fonte: unidades 29027.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 6 de 2026-09-21

O protótipo de controle financeiro familiar foi desenhado como aplicativo local/offline Flask + SQLite, dashboard lendo o mesmo banco, entrada manual e posterior bot Telegram com recepção de documentos/OCR local e confirmação humana. A fase inicial citava 46 categorias. Esse registro descreve o protótipo histórico, não migração concluída nem arquitetura produtiva vigente. Fonte: unidades 29827, 29833, 29836, 29950.

Para ingestão financeira local, explorar QR estruturado antes de OCR, preservar evidência e exigir revisão humana antes de persistir classificação. O desenho histórico fechava o bot por padrão, limitava tamanho de arquivo, tirava OCR do event loop e mostrava erros operacionais. Avaliação antiga de Apple Vision/Tesseract não é ranking atual nem autorização para enviar dados a serviços externos. Fonte: unidades 29983, 30004.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 7 de 2026-09-21

Desenho histórico da conciliação assistida: separar analisar, entrevistar, propor regra e gravar definitivo. Movimento desconhecido entra em exceção com ID estável, evidência, regra candidata, dado ausente e risco. Resposta humana deve distinguir aplicação só ao movimento de regra futura. Confiança alta não autoriza gravação definitiva. Fechamento informa classificados, pendentes, regras propostas e bloqueios; conectar à autoridade atual FIP sem criar banco paralelo. Fonte: unidades 35376, 37500.

No blueprint histórico Controle Financeiro Familiar, compra contém cabeçalho e itens categorizados ligados à evidência. Orçamento com ciclo dia5→dia4e lista de compras assistida com baixa eram expansões planejadas, não funcionalidades comprovadas. Preservar essa distinção de escopo e estágio; não confundir o protótipo familiar com o FIP corporativo posterior. Fonte: unidades 29796.

No blueprint familiar histórico, reservas e investimentos foram propostos como movimentos patrimoniais: podem afetar caixa/orçamento sem constituir despesa de consumo. A visão de lançamento deve distinguir caixa, competência, conta, categoria, responsável e conciliação. Trata-se de modelagem proposta, não prova de módulo implementado. Fonte: unidades 29810.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
