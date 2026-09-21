---
id: brain-f6c00041cbcfa4a63c3d
type: entity
title: BIKON
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:50:50.519705Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/LinkedIn-Robotnik-Publisher.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/API-WHATSAPP-BIKON.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/20-EMPRESAS/BIKON/README.md#relações
---

# BIKON

## Identificação

- Nome operacional: Bikon
- Razão social registrada no contexto fiscal: Bikon Tecnologia da Informação Ltda Me
- CNPJ: 34.191.026/0001-86
- Inscrição Municipal: não usar como campo obrigatório na automação Notaas enquanto a API aceitar sem esse dado
- Cidade/UF: Vitória/ES
- Código IBGE: 3205309

## Relações no Brain

- Automação fiscal: [[70-AUTOMACOES/NOTAAS-NFSE|Skill Notaas NFS-e]]
- Cadastro de clientes: `BRAIN/20-EMPRESAS/BIKON/cadastro-clientes/`
- Boletos e malote bancário: `BRAIN/70-AUTOMACOES/boletos-malote/`
- Contexto de grupos de faturamento: [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]
- Grupo relatórios operacionais: [[70-AUTOMACOES/RELATORIOS-OPERACIONAIS-TELEGRAM|Relatórios Operacionais Telegram]]
- Integração de segurança/antivírus em desenho: [[70-AUTOMACOES/BITDEFENDER-GRAVITYZONE|Bitdefender GravityZone - integração Bikon]]
- Governança de acessos Bikon ↔ AD local de clientes: [[70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES|Matriz de acesso Bikon x clientes AD local]]
- Integração Instagram Bikon Robotnik: [[70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK|Instagram Bikon, Robotnik]]
- Projeto LinkedIn Bikon/Robotnik: [[50-PROJETOS/Em-Andamento/LinkedIn-Robotnik-Publisher|LinkedIn Robotnik Publisher]]
- API WhatsApp Bikon: [[70-AUTOMACOES/API-WHATSAPP-BIKON|API WhatsApp Bikon]]
- Migração OpenClaw/Hostinger VPS: [[50-PROJETOS/Planejamento/Migracao-Hostinger-VPS-OpenClaw|Migração Hostinger VPS / OpenClaw]]
- FIP Bikon Financial Intelligence: [[50-PROJETOS/Em-Andamento/FIP-Bikon-Financial-Intelligence|FIP Bikon Financial Intelligence]]

## Histórico relevante

- 2026-09-17/18: preparado o `LinkedIn Robotnik Publisher` para a Página Bikon, somente pela API oficial e com `w_organization_social`. Mock/testes locais e genesis PGL passaram; o Gate A parou antes do portal por falta do Chrome autenticado anexável. Nenhum app, OAuth, segredo ou post foi criado, e publicação continua sujeita a aprovação própria por conteúdo.
- 2026-09-14: a V12 do piloto 365 Control foi aceita por Hebert como arte final (`ARTWORK_ACCEPTED`), sem autoridade herdada de publicação. Nos jobs semanais de carrossel e Reel, o pedido humano de maior variedade criativa foi persistido sem apagar os reviews dos bytes anteriores; novas versões com situações, pessoas, enquadramentos e mensagens distintas chegaram a `REVIEW_COMPLETE / APPROVED_FOR_TECHNICAL_DELIVERY` e foram entregues privadamente. `approval` e `publication` continuaram nulos, e publicação, agendamento e impulsionamento permaneceram bloqueados.
- 2026-09-12: o piloto "365 Control" evoluiu por iteracoes controladas. A V3 recebeu revisao tecnica do Kowalski; depois Hebert pediu uma alternativa menos sombria. A opcao C corrigida chegou a V6 e foi entregue apenas como previa, ainda sem revalidacao porque `review_prepare` permaneceu falhando. Nao houve publicacao nem agendamento.
- 2026-09-11: o readback da peca publicada em 10/09 foi recuperado por verificador confinado com grant de 120 segundos restrito ao hostname/porta exatos. O estado chegou a `BYTES_VERIFIED`, o parecer visual registrou correspondencia entre o JPEG submetido e o publicado, e `instagram_mutations=0`; isso nao autoriza nova publicacao.
- 2026-09-11: duas novas opcoes A/B da campanha de IA foram recuperadas por handoff de escopo exato para o workspace do Kowalski, revisadas nos mesmos bytes e entregues privadamente pelo Robotnik como documentos Telegram `messageId 871` e `873`. Ambas ficaram `APROVADO_COM_RESSALVA` para rascunho; A precisa de recomposicao/legenda nova antes de aceite artistico ou publicacao. Visualizacao/aprovacao humana seguem pendentes e nenhuma mutacao Instagram ocorreu.
- 2026-09-10: Hebert aprovou no Telegram `messageId 860` a publicação da peça "IA governada para PME". Robotnik executou um único `media_publish`; o Graph confirmou `bikontech`, `IMAGE/FEED`, legenda pública e permalink `https://www.instagram.com/p/DdFkfePleea/` (`media_id 18619098217050385`). O job foi preservado sem republicacao; em 11/09 o readback chegou a `BYTES_VERIFIED` por rota confinada, ainda sem herdar autoridade para novo efeito externo.
- 2026-09-08/09: marketing Bikon passou a ter `content-production-contract` v1 como unica direcao criativa ativa, com geracao principal por `image_gen.imagegen`, finalizacao deterministica e revisao dos mesmos bytes pelo Kowalski. O piloto final foi entregue no Telegram `messageId 794` e aceito por Hebert como `HUMAN_ACCEPTED / COMPLETE`; o aceite nao autoriza Instagram, staging, agendamento ou publicacao.
- 2026-09-08/09: a cadeia mensal ARX foi reparada para aquisicao historica nativa e gerou artefatos de agosto `VALIDATED_NO_SEND` para Alzira, Camburi, Capixaba e Vila Velha. Tres execucoes historicas sao `CONFIRMED_NOT_SUBMITTED`, Capixaba permanece `UNKNOWN`, e os ciclos naturais corrigidos ainda aguardam observacao.
- 2026-08-28: snapshot read-only de NFS-e de agosto registrou 29 notas, 23 validas e 6 canceladas, com bruto R$ 88.155,06, cancelado R$ 35.211,55 e liquido R$ 52.943,51. O cancelamento da NFS-e `214`/boleto `105609` parou sem mutacao por falta de motivo fiscal e de rota CNAB400 validada para ocorrencia `02`. Em homologacao Cresol, boleto/remessa NN `358` foram preparados localmente sem importacao, envio ou registro externo.
- 2026-08-27: lote 4.1 concluido apos aprovacao explicita de competencia `08/2026`, emissao em `27/08/2026` e gravacao da remessa 094 em `27/08/2026`: NFS-e `246` e `247`, R$ 899,00 cada; dois boletos locais; remessa CNAB400 local com dois titulos/R$ 1.798,00; e-mails apenas em rascunho, remessa nao transmitida e sem confirmacao de registro bancario.
- 2026-08-26/27: CNS `02.133-7`/`021337` do Cartorio do I Oficio de Alfredo Chaves ratificado pelo Owner; JSON, CSV e SQLite do cadastro permaneceram consistentes, com CNS unico e `integrity_check=ok`. Cards cadastrais validados de Alfredo Chaves e Donna Industria de Madeiras foram entregues sem refacao dos dados.
- 2026-08-20: FIP Google Drive Archival Storage foi concluido com `PASS`: `356/356` objetos `ARCHIVE_AND_RELEASE` fechados, `0` pendentes, `UPLOAD_STARTED=0`, `sqlite integrity_check=ok`, liberacao efetiva de `9.066.463.232` bytes na VPS e registry final SHA-256 `96edb9ed377d1a0c32c55c0f04cee26e42f91554bb5f96ea7086d7983332d89d`. Objetos fora do escopo (`ARCHIVE_KEEP_LOCAL`, `KEEP_LOCAL`, `DEFER_AMBIGUOUS` e 5 `PURGE_REGENERABLE`) foram preservados.
- 2026-08-19: FIP implantou gateway privado de intake documental `v1.0.0` como componente permanente e elevou FCOC ativo para `1.6.0`, com canario produtivo Cresol `ALREADY_INGESTED`/delta `0`, caixa oficial ainda R$ 10.801,39, `fip-8787.service` ativo e portas `8787`/`9213` sem mutacao. Relatorios Operacionais recebeu alias-router para Puppet/Kowalski/Darth preservando Puppet como owner externo e workers sem envio externo direto.
- 2026-08-18: FIP atualizou caixa Cresol corrente para R$ 10.801,39 em 2026-08-17T20:21:32-03:00, reconciliado por extrato oficial com diferenca R$ 0,00. Limite de credito R$ 30.000,00 e saldo disponivel R$ 40.801,39 nao foram tratados como caixa. O backend `8787` ficou sob `fip-8787.service` e a rota Relatorios Operacionais para cenarios FIP passou a responder via Puppet, com Darth/Kowalski apenas como workers internos.
- 2026-08-15: FIP CHG-004 ampliou a base financeira 2026 da BIKON: `546` transacoes bancarias canonicas 2026, carteira Cresol com 231 titulos/24 clientes e R$ 170.331,83 em 16 titulos abertos vencidos, Grupo Unus canonico com 8 CNPJs aprovados e 98,80% da carteira aberta medida, Caju/folha/impostos estruturados e cartoes pessoais preservados em quarentena privada sem classificacao automatica.
- 2026-08-12: FIP `v1.1.0` congelado com tesouraria/caixa: saldo oficial Cresol de 2026-08-11 R$ 17.001,68 reconciliado com diferenca R$ 0,00, forecast 30d R$ 38.629,45 e primeiro caixa negativo projetado em 2026-08-20; `v1.2.0` ficou candidato nao congelado porque a cobertura documental material do forecast ficou abaixo de 80%.
- 2026-08-11: rodada Cresol API em homologacao criou titulo `22394650`, nosso numero `09/00000000357-6`, valor R$ 1,00, vencimento 2026-08-18, PDF oficial e remessa CNAB400 local validada; sem producao, sem upload no portal/banco, sem baixa e sem envio a cliente.
- 2026-08-10/11: FIP Bikon Financial Intelligence atingiu `FIP_PRODUCTION_GO_LIVE=PASS` para fronteira privada/controlada. Totais aceitos: receita canonica R$ 2.443.859,64, despesa R$ 1.418.140,88, resultado R$ 1.025.718,76, `1438` transacoes bancarias canonicas e pendencias materiais `0`/R$ 0,00. Acesso produtivo ficou em `127.0.0.1:8787` e rota Tailscale tailnet-only `https://srv1811702.tail34aee8.ts.net:8787/`, sem Funnel/public Internet para `8787`.
- 2026-08-03: faturamento agosto/2026 remessa 093 executado em produção assistida: 27 NFS-e autorizadas, 27 boletos locais, 18 e-mails enviados com cópia para `financeiro@bikon.com.br`, total R$ 86.357,06; remessa CNAB400 local gerada sem transmissão bancária consolidada.
- 2026-08-03: dashboard Provimento 213 do CNS `024067` entrou em produção focada com identidade Bikon/PT-BR e exportação PDF autenticada via Tailscale; token antigo revogado e sem token permanente na URL.
- 2026-08-03: crons dos relatórios operacionais diários antecipados para janela 07:45-07:48 e instrução diária do Kowalski para 07:59, timezone `America/Sao_Paulo`.
- 2026-07-20: conjunto Instagram Bikon v4 aprovado como canônico; cinco fundos Kling consumiram 10 créditos autorizados e nenhuma publicação ocorreu.
- 2026-07-20: Instagram Brand Director v2.1.0 implantada por corte atômico com backup, rollback e recibo append-only; Produção Assistida iniciada e lifecycle da proposta ainda `pending`.
- 2026-07-20: snapshot `feed-base-a v1` congelado com sete arquivos e Brand QA pré-geração `PASS`; manifesto `474e9af2…`, request `5d721862…` e payload `2be351a0…`. Render, Portão C, Kling e publicação permanecem bloqueados.
- 2026-07-20: SSI e SFT adotados como indicadores oficiais da Produção Assistida. Valores iniciais: SSI 50% e SFT 68,985 segundos.
- 2026-07-20: pacote conferido com 28 PDFs das NFS-e 191 a 218, total de R$ 88.403,87, entregue sem nova emissão ou cancelamento.
- 2026-07-17: aprovada a arquitetura de produção Instagram com Robotnik na preparação, Puppet Master na coordenação, Hebert nos portões de gasto/ação externa, Kling para mídia bruta, Creatomate para composição e Buffer como único publicador.
- 2026-07-17: contrato Kling CLI 0.1.3 limitado a `text_to_image`, adapter corrigido e nove testes aprovados sem geração ou consumo; brand pack oficial e template Creatomate 1080 × 1350 validados, com camadas produtivas e Buffer ainda pendentes.
- 2026-07-09: integração Instagram Bikon/Robotnik configurada em modo `draft` com Meta Graph API, token em segredo local, publicação bloqueada e crons editoriais criados para pautas diárias/semanais com aprovação humana.
- 2026-07-09: definido Kowalski como guardião visual de materiais públicos ou semi-públicos Bikon com arte/layout, enquanto Robotnik permanece dono de pauta, copy e campanha.
- 2026-07-09: pacote local de homologação Cresol gerado com remessa CNAB400 validada e boleto PDF conferido; nenhum upload no portal, envio ao banco ou e-mail externo foi feito.
- 2026-07-07: VPS de destino da migração OpenClaw foi limpa antes do replanejamento; manter arquitetura final com usuário `openclaw` como dono e sem resíduos de `root`, `u4s` ou gateway duplicado.
- 2026-06-26: API WhatsApp Bikon validada via `api.bikon.tech`, canal Atendimento Bikon registrado como `REGISTERED`, template `retomar_solicitacao` confirmado e rotina segura criada com token fora do Brain/Git.
- 2026-06-26: verificação de segurança da Meta aprovada para retomada da integração Instagram Bikon Robotnik; publicação real permanece bloqueada até configuração segura, testes e aprovação explícita.
- 2026-06-26: regra de faturamento atualizada para copiar `financeiro@bikon.com.br` em todo e-mail de NFS-e/boleto enviado a cliente.
- 2026-06-24: iniciada governança de acessos Bikon ↔ AD local de clientes, com matriz mestre em Google Sheets para listar usuários Bikon aprovados no Entra ID, clientes, servidores, permissões e regras de auditoria antes de qualquer automação.
- 2026-06-23: reforçado padrão visual premium Bikon para relatórios técnicos externos, com fundo suave dentro da paleta, sem cabeçalhos/rodapés automáticos e sem metadados de impressão/navegador.
- 2026-06-22: validado envio de e-mail NFS-e via `fatura@bikontecnologia.com.br`, template HTML padrão Bikon e agrupamento de duas ou mais NFS-e por cliente em um único e-mail com todos os PDFs/XMLs e boletos.
- 2026-06-22: criado grupo Telegram `relatórios operacionais` para consultas e relatórios do Kowalski, sem bot separado e sem alteração de estrutura operacional do agente.
- 2026-06-20: definido padrão operacional de NFS-e com tomador completo; quando o cadastro mestre tiver endereço, o payload Notaas deve incluir endereço completo e não apenas documento, nome e e-mail.
- 2026-06-19: gerado relatório executivo Bitdefender com 21 clientes, 785 licenças, 651 slots usados, 759 dispositivos, 647 gerenciados e 112 não gerenciados; caminhos registrados sem segredos.
- 2026-06-19: desenhada oportunidade de integração Bitdefender GravityZone para inventário, status de endpoints, incidentes e relatórios por cliente; sem credenciais registradas e sem execução externa.
- 2026-06-17: grupo Telegram `Faturamento Bikon` (`telegram:-5561224828`) restringido para tratar apenas de faturamento da Bikon: NFS-e, boletos, remessa/retorno e conferência cadastral diretamente ligada ao faturamento.
- 2026-06-12: skill Notaas NFS-e configurada para Bikon, com segredos mantidos fora do Brain/Git e emissão/cancelamento real protegidos por confirmação explícita.
- 2026-06-14: criado backup operacional de cadastro de clientes e documentação inicial para futura geração de boletos/remessa bancária.

## Guardrails

- Não registrar API keys, credenciais bancárias, tokens, arquivos sensíveis sem necessidade ou dados fiscais sigilosos no Brain.
- Qualquer emissão/cancelamento fiscal real exige autorização explícita do Hebert/Puppet Master.
- Qualquer envio externo de NFS-e, boleto ou e-mail financeiro para cliente exige aprovação explícita.
- Todo e-mail de NFS-e/boleto enviado a cliente deve copiar `financeiro@bikon.com.br`.
- NFS-e da Bikon deve usar dados completos do tomador quando disponíveis no cadastro mestre, incluindo endereço completo.
- Qualquer geração de remessa bancária real deve ser validada contra layout oficial do banco antes de uso operacional.
- Qualquer chamada real à API GravityZone ou armazenamento de chave exige autorização explícita do Hebert e cofre local fora do Git.
- Qualquer automação sobre contas de AD local de clientes deve começar em modo auditoria; criação, desativação, remoção de grupos ou alteração de privilégio exige aprovação explícita e escopo validado.
- Relatórios técnicos externos devem sair com acabamento visual premium Bikon, sem caminhos internos, metadados automáticos, paginação feia ou aparência de HTML impresso.
- Materiais públicos ou semi-públicos com logo, paleta, layout ou identidade Bikon devem passar por revisão visual do Kowalski antes da peça final; isso não substitui aprovação explícita para publicação ou envio externo.
- No marketing Bikon, estrategia, geracao, finalizacao, revisao, entrega e publicacao sao aprovacoes independentes. `content-production-contract` v1 e a autoridade criativa ativa; `image_gen.imagegen` e a rota visual principal. Nenhum publicador esta autorizado por inferencia a partir do aceite de uma arte.
- Depois de `media_publish` comprovado, falha de readback, cleanup ou recibo nao autoriza repetir a publicação; preservar o media ID e retomar apenas o fechamento do mesmo job.
- Brand QA pré-geração aprova somente o snapshot e o hash apresentados. Não autoriza Portão C, Kling, render, upload ou publicação; qualquer alteração de byte exige nova submissão.
- FIP e dashboards financeiros privados nao autorizam emissao fiscal, boleto, remessa, baixa bancaria ou comunicacao externa; eles sao base executiva/gerencial ate haver Approval proprio para efeitos operacionais.
- FIP em `8787` deve permanecer privado/autenticado; nao expor via Internet publica, segredo em URL ou relatorio.
- Forecast FIP com cobertura documental parcial deve permanecer como candidato/partial pass; nao usar projecoes para decisao operacional irreversivel sem explicitar confianca, materialidade e lacunas.
- FIP CHG-004 e carteira Cresol sao base gerencial/canonica interna; cobranca, baixa bancaria, classificacao de cartao pessoal, reembolso, P&L definitivo, envio externo ou comunicacao com cliente continuam exigindo Approval proprio.
- Limite de credito bancario e saldo disponivel nao sao caixa; forecasts devem usar apenas saldo oficial reconciliado como autoridade corrente.
- Novas evidencias documentais no FIP devem entrar pelo intake gateway somente com parser/reconciliation gate, idempotencia, protecao de senha e privacidade de cartao pessoal preservadas.
- Limpeza adicional de arquivos FIP fora do escopo `ARCHIVE_AND_RELEASE` exige autorizacao propria e prova de destino/rollback; conclusao do archive nao autoriza purge por heranca.

## Complementos reconciliados — lote 10 de 2026-09-21

Briefing histórico posicionou Bikon como parceira operacional B2B de infraestrutura/rede/SNOC/backup, evitando suporte genérico e linguagem institucional vazia. Público proposto: empresas a partir de5dispositivos com dependência real de rede. Copy pública deveria chamar Hebert de fundador/sócio-administrador e evitar travessão. A formulação de reduzir dependência do dono em90dias era proposta daquele briefing, não garantia validada; a persona Captain era desenho, não agente operacional comprovado. Fonte: unidades 3493.

Perfil histórico de Hebert: sócio-administrador/CFO com apoio operacional; Bikon em reorganização de processos com equipe de3pessoas. Prioridades declaradas naquela janela: Provimento213, NFS-e/caixa gerencial e equipe enxuta; metas então propostas eram R$1,5milhão/ano e30clientes em12meses, e equipe10/R$6milhões/ano em3anos. Preferia respostas curtas/numeradas e reduzir tarefas manuais/relatórios dispersos. Horário8–18dias úteis e contato fora só emergência eram regra geral histórica, conciliada com autorização posterior de follow-ups prometidos sem essa limitação. Não tratar metas antigas como previsão atual. Fonte: unidades 34183.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
