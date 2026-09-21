---
id: brain-6b68b846fff4c439dfe6
type: state
title: Skill Notaas NFS-e
created: '2026-09-21T19:00:06.782473Z'
created_semantics: Data de registro estruturado, não data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
updated: '2026-09-21T19:50:50.519705Z'
---

# Skill Notaas NFS-e

## Status

Instalada com hardening em 2026-06-12.

## Locais

- Skill exclusiva Darth Vader: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse`
- Auditoria: `/data/.openclaw/workspace/audits/notaas-nfse/AUDITORIA.md`
- Instalação: `/data/.openclaw/workspace/audits/notaas-nfse/INSTALACAO.md`

## Finalidade

Emitir, consultar, baixar e cancelar NFS-e via API Notaas.

## Guardrails aplicados

- `--dry-run` e alias `--teste` para simulação sem chamada à API.
- Emissão real exige `--confirmar-emissao`.
- Cancelamento real exige `--confirmar-cancelamento`.
- Dependências instaladas em `vendor/`, sem mexer no Python global.
- `.env` com permissão `600`.
- `.env.example` criado.
- `scripts/cadastrar_cliente.py` criado.
- `SKILL.md` corrigido com frontmatter obrigatório.

## Validação

- Skill visível no OpenClaw: `openclaw skills info notaas-nfse` retorna `Ready`.
- `emitir_nota.py --dry-run` validado sem envio.
- `emitir_lote.py --dry-run` validado sem envio.
- `cancelar_nota.py --dry-run` validado sem envio.
- Operação real sem confirmação é bloqueada.

## Configuração

Configurada em 2026-06-12 para Bikon Tecnologia da Informação Ltda Me.

Dados não sensíveis registrados:

- CNPJ: 34.191.026/0001-86
- Cidade/UF: Vitória/ES
- Código IBGE: 3205309

Decisão de 2026-06-22: manter a configuração da Bikon sem inscrição municipal. Houve erro ao tentar usar/preencher IM; ausência de IM não deve bloquear emissão enquanto a API Notaas aceitar sem esse campo.

A API key foi armazenada apenas nos arquivos locais `.env` e `config/empresa.json`, com permissão `600`. Não registrar segredo no Brain nem no Git.

## Regra operacional

Qualquer emissão ou cancelamento real de NFS-e deve ser previamente autorizado pelo Hebert/Puppet Master, por envolver obrigação fiscal.

Envio de e-mail para cliente externo também exige autorização explícita, mesmo quando o SMTP estiver validado e o rascunho estiver pronto.

Atualização 2026-07-01: em lote com boleto/remessa, NFS-e deve ser etapa separada. Primeiro dry-run e conferência de cadastro/valor/competência; depois aprovação explícita; depois emissão; depois conferência de XML/PDF. Boleto/remessa e e-mail só avançam após essa conferência.

Atualização 2026-08-03: o lote de faturamento Bikon agosto/2026 remessa 093 emitiu `27` NFS-e em produção, com PDF/XML locais, totalizando R$ 86.357,06. Os e-mails externos foram enviados depois da preparação/conferência, com `18` mensagens agrupadas por cliente e copia para `financeiro@bikon.com.br`. O evento confirma o uso operacional assistido da skill, mas não autoriza automação cega para lotes futuros.

Atualizacao 2026-08-27: lote BIKON 4.1 emitiu as NFS-e `246` e `247`, R$ 899,00 cada, somente depois de autorizacoes explicitas para competencia `08/2026` e emissao em `27/08/2026`. PDFs/XMLs, boletos, remessa 094 e rascunhos foram empacotados localmente. E-mails nao foram enviados, a remessa nao foi transmitida e nao existe confirmacao de registro bancario. A divergencia original reforca que emissao, competencia, data de gravacao da remessa, envio de e-mail e transmissao bancaria sao superficies materiais separadas.

Baseline FBCP 2026-08-03: a revisão read-only `FBCP_PHASE_0_READ_ONLY_BASELINE_FREEZE=PASS` congelou hashes, SQLite em modo immutable e superfícies de mutação sem chamar Notaas, Cresol, SMTP, transmissão de remessa ou emissão nova. Riscos P0 para a skill Notaas: competência default fixa `2026-04` em emissão individual/payload helper, uso de `float` para valores e retry sem ledger idempotente. Próxima autorização recomendada antes de evoluir produção: `AUTHORIZE_FBCP_P0_COMPETENCE_AND_MONEY_HARDENING_ONLY`.

## Padrão Bikon para dados do tomador

Atualizado em 2026-06-19/20 após lote de homologação sair sem endereço porque o script descartava `tomador.endereco`.

Para emissões da Bikon, a NFS-e deve usar todos os dados disponíveis no cadastro mestre do cliente:

- CPF ou CNPJ conforme documento.
- Nome/razão social do cadastro.
- E-mail financeiro quando existir.
- Endereço completo sempre que disponível: logradouro, número, complemento, bairro, cidade, UF e CEP.
- Não emitir lote usando só documento, nome e e-mail quando o cadastro tiver endereço.
- Se endereço estiver ausente ou ambíguo, marcar pendência antes da emissão.
- Quando houver risco de homônimos ou múltiplos cadastros, usar `cliente_id`/cadastro único e conferir CPF/CNPJ, nome, cidade, UF, CEP e endereço completo antes de emitir.

Correção aplicada na skill da Darth Vader em `core/client.py` e `scripts/emitir_lote.py` para preservar endereço quando disponível.

## Exclusividade

Em 2026-06-12, a skill foi restringida para uso exclusivo da Darth Vader.

Validação realizada:

- `openclaw skills check --agent darth-vader` mostra `notaas-nfse`.
- `openclaw skills check --agent main` não mostra `notaas-nfse`.
- `openclaw skills check --agent kowalski` não mostra `notaas-nfse`.

A skill foi removida dos diretórios globais/main e mantida apenas no workspace da Darth Vader.

## E-mail automático Bikon

Atualizado em 2026-06-22.

Remetente padrão:

- Caixa: `fatura@bikontecnologia.com.br`
- Nome exibido: `Faturamento Bikon`
- Reply-to: `fatura@bikontecnologia.com.br`

SMTP validado:

- Provedor: DreamHost
- Host: `smtp.dreamhost.com`
- Porta válida: `465` com SSL/TLS
- Porta `587` STARTTLS falhou com autenticação `535` e não deve ser usada como padrão.

Segredo local:

- Arquivo: `/data/.openclaw/secrets/email-dreamhost/fatura-bikon.env`
- Permissão: `600`
- Não registrar senha no Brain nem no Git.

Validações realizadas:

- Login SMTP validado sem envio externo.
- IMAP/Himalaya validado listando pastas da conta `fatura-bikon`.
- E-mail teste enviado para `hebert.mattedi@bikon.com.br` e confirmado pelo Hebert como entregue na caixa de entrada.

## Template HTML padrão

Atualizado em 2026-06-22.

Arquivos:

- Template ativo: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/templates/email_nfse_bikon.html`
- Configuração: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/config/email.json`
- Script de preparo/envio controlado: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_email_cliente.py`

Regras:

- E-mail deve ser multipart: texto simples + HTML.
- Template usa identidade visual Bikon, paleta Bikon e logo embutido/base64, sem imagem externa obrigatória.
- Campos do corpo devem incluir número da NFS-e e chave quando presentes no job.
- Se a nota tiver boleto, o boleto PDF deve ir anexado junto com DANFSe PDF e XML.
- Testes com dados reais de cliente devem usar destinatário explícito e não buscar cadastro automaticamente.

## Agrupamento por cliente

Validado pelo Hebert em 2026-06-22.

Regra oficial para envio em lote:

- Todo e-mail de NFS-e/boleto para cliente deve copiar `financeiro@bikon.com.br`.
- Agrupar duas ou mais NFS-e pelo mesmo `cliente_id` comprovado. A formulação inicial que também permitia agrupar apenas por CPF/CNPJ/documento foi superada pela correção registrada abaixo: unidades diferentes do mesmo documento, como Celi Aracruz e Celi João Neiva, não devem ser misturadas. Essa regra de agrupamento não concede autorização de envio.
- O corpo do e-mail deve listar cada NFS-e com número, chave, valor e boleto relacionado.
- Anexos devem incluir todos os PDFs/XMLs das NFS-e e todos os boletos PDF daquele cliente.
- Um e-mail por cliente, mesmo que existam duas ou mais notas e boletos no mesmo envio.

Ferramenta criada:

- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_emails_lote_clientes.py`

Teste validado:

- Cliente: Alzira Maria Viana.
- NFS-e de homologação: números `5` e `7`.
- Chaves: `32053092234191026000186000000000000526069998018858` e `32053092234191026000186000000000000726062822079919`.
- Boletos: `105602/1534` e `105603/1535`.
- Total: R$ 3.474,73.
- Envio teste agrupado para `hebert.mattedi@bikon.com.br` validado pelo Hebert.

## Trava automática de checklist antes do envio externo

Implementada em 2026-06-22 no script:

- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_email_cliente.py`

Arquivos gerados a cada preparo de e-mail:

- `checklist-envio-nfse.json`
- `checklist-envio-nfse.md`

Comportamento:

- Preparar rascunho sem `--confirmar-envio` gera checklist e `.eml`, mesmo quando houver pendência, para conferência.
- Envio SMTP com `--confirmar-envio` só passa se o checklist não tiver bloqueios.
- Se `config/email.json` mantiver `approval_required=true`, envio externo exige `job.email.aprovado_por_hebert=true`.
- Se faltar PDF da NFS-e, XML da NFS-e ou boleto PDF quando houver boleto indicado, o envio externo é bloqueado.
- PDF Notaas pode atrasar ou falhar; XML é o artefato técnico confiável imediato, mas e-mail externo só deve sair quando PDF e XML estiverem conferidos.
- O checklist lista remetente, reply-to, destinatários, assunto, cliente, quantidade de notas, total calculado, documentos, anexos, bloqueios e avisos.

Validação feita:

- Rascunho de teste gerou checklist com status `rascunho_conferivel`.
- Tentativa de envio com `--confirmar-envio` sem `job.email.aprovado_por_hebert=true` retornou bloqueio e status `bloqueado_para_envio`.
- Checklist com aprovação simulada e todos os anexos retornou `liberado_para_envio`, sem disparar SMTP no teste.

## Atualização 2026-07-01, lote Remessa 092 e padrão mensal

Hebert aprovou e validou novas regras operacionais para emissão mensal de NFS-e, boletos, remessa e e-mails.

### Emissão de lote NFS-e

Padrão Bikon daqui para frente:

- Não usar batch cego da Notaas em produção.
- Emitir lote de forma cadenciada: 1 NFS-e por vez.
- O ciclo mínimo é de 60 segundos entre o início de uma nota e o início da próxima.
- Dentro desses 60 segundos entram: `POST /emitir`, polling até `issued`, download e confirmação de XML + PDF.
- Se o ciclo terminar antes de 60 segundos, aguardar apenas o saldo restante.
- Se a Notaas demorar mais de 60 segundos, avançar assim que XML+PDF estiverem prontos, sem espera extra.
- Se PDF ou XML não ficarem prontos dentro do limite de tentativas, parar o lote e não avançar para a próxima nota.

Implementação:

- Script: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/emitir_lote_cadenciado.py`
- Documentação: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/SKILL.md`
- Dry-run validado com o payload do lote Remessa 092.

### Documentação oficial Notaas incorporada

Fonte oficial registrada:

- https://docs.notaas.com.br

Referência operacional Bikon criada:

- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/references/notaas-emissao-cancelamento-bikon.md`

Pontos incorporados:

- Emissão é assíncrona via `POST /emitir`, retorno `202` com `invoiceId`, e polling em `GET /invoices/{id}/status` até `issued` ou `error`.
- XML: `GET /invoices/{id}/xml`; XML de cancelamento: `GET /invoices/{id}/xml?type=cancel`.
- PDF: `GET /invoices/{id}/pdf`; pode retornar temporariamente `503`/`429` mesmo com nota `issued`, como ocorreu no lote 092.
- Webhook `nfse.documents_ready` pode vir parcial: XML pronto e `pdfUrl: null`; pode completar até 10 minutos depois.
- Checklist de e-mail deve validar PDF/XML existentes localmente, não apenas status `issued`.

### Cancelamento NFS-e

Cancelamento é operação fiscal real e exige autorização explícita do Hebert.

Regras:

- Fazer dry-run antes.
- Conferir `invoiceId`, número da NFS-e, cliente, valor, motivo e impacto em boleto/remessa/e-mail.
- Cancelamento real usa `--confirmar-cancelamento`.
- Script agora suporta polling até `cancelled`/`error`, `--max-polls`, `--out-dir` e tentativa de baixar XML de cancelamento.
- Cancelar e reemitir são aprovações separadas.

Script atualizado:

- `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/cancelar_nota.py`

### Regras de boleto e e-mail ajustadas no lote 092

- Para cada NFS-e emitida, gerar exatamente 1 boleto.
- Para todos os boletos do lote, gerar apenas 1 arquivo de remessa CNAB400.
- E-mail ao cliente deve conter NFS-e + boleto.
- Quando houver mais de uma NFS-e + boleto para o mesmo `cliente_id`, enviar apenas 1 e-mail agrupado.
- Agrupar por `cliente_id`, não só CPF/CNPJ, para evitar misturar unidades diferentes do mesmo documento, como Celi Aracruz e Celi João Neiva.
- CC obrigatório em todos os e-mails: `financeiro@bikon.com.br`.
- Correção aplicada: clientes com apenas uma nota agora também preenchem o valor do e-mail usando `nfse.documentos[0].valor_total` quando necessário.
- Correção aplicada no boleto: PDFs gerados pelo Chromium devem usar `--no-pdf-header-footer`; Hebert quer somente o corpo do boleto, sem cabeçalho/rodapé de impressão.

### Resultado operacional do lote Remessa 092

- 28 NFS-e emitidas.
- 28 XMLs baixados.
- 28 PDFs obtidos, alguns via retries e um PDF enviado manualmente pelo Hebert.
- 28 boletos gerados.
- 1 remessa CNAB400 gerada e enviada ao Hebert para registro dos boletos.
- 18 e-mails enviados, agrupados por cadastro, cobrindo 28 NFS-e + 28 boletos.
- Erros de envio: 0.
- `financeiro@bikon.com.br` copiado em todos os e-mails.

## Atualizacao 2026-08-28

- Consulta read-only da competencia agosto/2026 encontrou 29 NFS-e: 23 emitidas e 6 canceladas (`235`, `240`, `242`, `243`, `244` e `245`), sem duplicidade.
- Totais do snapshot: bruto R$ 88.155,06, cancelado R$ 35.211,55 e liquido valido R$ 52.943,51. PDF/CSV de entrega permanecem fora do Brain/Git.
- O cancelamento solicitado da NFS-e `214`, R$ 2.046,81, foi interrompido no preflight sem mutacao. A nota continuava `issued` e o boleto relacionado `105609`, nosso numero `1541`, continuava `emitido_producao`, sem baixa.
- Bloqueios: motivo fiscal obrigatorio nao informado e gerador CNAB400 aprovado fixo na ocorrencia `01`, enquanto a baixa exige ocorrencia `02`. Cancelar a nota isoladamente criaria inconsistencia fiscal/bancaria.
- Retomar somente com motivo fiscal e uma rota CNAB de baixa `02` validada e explicitamente autorizada; cancelamento da nota, baixa/remessa e eventual mudanca de script/metodo sao gates separados.

## Complementos reconciliados — lote 4 de 2026-09-21

O fluxo assistido recebe lista de notas/itens, cruza cadastro e gera resultados/status por item. Entrada em lote não elimina aprovação fiscal nem conferência de NFS-e, boleto e remessa; o caso Unus não deve ficar hardcoded. Fonte: unidades 36551.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.

## Complementos reconciliados — lote 7 de 2026-09-21

Diagnóstico histórico FBCP: a skill assistida não deve ser fonte única de autoridade financeira. Além de competência atual, centavos/Decimal e retry protegido, desenho exige identidade canônica billing_operation_id/external_reference, autorização vinculada a operação/hash/validade, journal de transições e outbox de email com hashMIME/recibo. Flag booleana reutilizável não prova autorização dessa operação e timeout dePOSTnão permite retry cego. Implementação por etapas e baseline; não alegar esses componentes instalados só por constarem da proposta. Fonte: unidades 31587.

O histórico distinguiu chave de projeto Notaas usada em emissão/consulta de token de organização para gestão de certificados. Nenhum desses fatos comprova possibilidade de exportar A1 para SERPRO; usar certificado sob controle do titular e verificar capacidades do endpoint, sem prometer exportação de segredo. Fonte: unidades 34733.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch7-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 8 de 2026-09-21

No lote Bikon agosto/2026 de 27 notas, Hebert esclareceu que diferenças entre soma e total eram descontos concedidos e que os sufixos aracruz/joão neiva identificavam qual cadastro/endereço Celi usar, com os dados mestres completos na emissão. Isso resolve aquele lote e não autoriza tratar qualquer divergência futura como desconto. Preparar notas, boletos/remessa e rascunhos é distinto de enviar/transmitir. Fonte: unidades 3398, 3401.

Hebert aceitou provisoriamente layoutv5 como padrão apesar de insatisfação estética, e pediu descartar simulações e carregar o faturamento de julho na base recém-criada. O trecho registra pedido/autorização daquela etapa, não prova exclusão/importação concluídas nem autorização vigente para limpar dados atuais. Não promover aceitável por enquanto a aprovação definitiva de qualidade. Fonte: unidades 38135.

NFS-e180 Unus, competência junho/2026 e totalR$18.004,19, foi lida como documento de referência para preparar fluxo seguinte de NFS-e/boleto/remessa Cresol. Era NFS-e de serviço, não DANFE de produto. Não registrar novamente receita, pagamento ou quitação apenas por essa leitura, nem copiar a chave fiscal ao Brain. Comprovante/documento mestre permanecem autoridade operacional. Fonte: unidades 36464.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch8-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 10 de 2026-09-21

No segundo lote de produção de01/07/2026, Hebert confirmou que diferenças entre soma dos itens e total refletiam descontos já conferidos; isso não autorizava emissão imediata. A pré-validação precisava distinguir Celi Aracruz e Celi JoãoNeiva por cliente_id/endereço, não fundir por nome/CPF. Aceitação de desconto nesse lote não é regra genérica para ignorar divergência de totais em lotes futuros. Fonte: unidades 3565.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 11 de 2026-09-21

Em13/06/2026, a tentativa fiscal real de valorR$1,00 teve timeout apósPOST Notaas; não retornaram invoice_id, número, código verificador ouPDF/XML. O resultado comunicado foi INDETERMINADO, com orientação de conferir provider antes de repetir para não duplicar emissão. Isso é estado histórico, não prova de pendência atual nem autorização de retry. Relatório referenciado: workspace-darth-vader/relatorios/status_emissao_nfse_hebert_mattedi_2026-06-13.md. Fonte: unidades 3519, 3501, 3510.

Pedido histórico de NFS-e real deR$1,00 para Hebert em13/06, serviço de infraestrutura de rede010701, município de prestaçãoVitória/ES eISS5%; houve preparação/dry-run com gate final e posterior timeoutINDETERMINADO. As instruções fiscais do pedido são históricas, não validação tributária vigente. Não conservar CPF/endereço nos resumos do Brain; consulta operacional deve usar cadastro protegido e evidência original autorizada. Fonte: unidades 29391.

Em26/06/2026, Hebert autorizou uma únicaNFS-e real para Celi/Aracruz, R$585,00, competênciajunho/2026, serviço gerenciamento/controladoria/monitoramento de recursos de rede010701, prestaçãoVitória/ES,ISS5%. CSVRemessa091260626 indicava data desejada22/06, boleto comvencimento30/06 e próximo documento105602/últimonossonúmero1533-7. A delegação vedava lote, e-mailcliente, boleto/remessa e cancelamento naquele passo. Isso preserva pedido e limites; não prova emissão, númeroNFS-e189 ou envio. Cadastro pessoal deve ficar na fonte operacional protegida, não neste resumo. Fonte: unidades 31443, 3552.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch11-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 12 de 2026-09-21

O formulário histórico do pedidoR$1 deHebert especificava competência2026-06 eISS5%retido, além do serviço010701 eVitória/ES. Preservar como instrução do pedido daépoca, sem validar o enquadramento fiscalatual ou inferir emissão; a tentativa terminouINDETERMINADA após timeout e exigia conferência antes de retry. E-mail/CPF não precisam ser duplicados na memória. Fonte: unidades 29388.

Uma solicitação histórica separada pediu NFS-e paraCeliCabral deJoãoNeiva,R$585, com boleto vencendo30/06 e arquivo de remessa. Esse pedido não é equivalente à delegaçãoAracruz preservada em31443/3552, que tinha escopo restrito. Manter identidades e escopos separados; nenhum dos pedidos isolados comprova emissão/transmissão. O cadastro mestre deve distinguir cliente_id/endereço sem repetir dados pessoais noBrain. Fonte: unidades 36972.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch12-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 14 de 2026-09-21

Em03/08/2026, um recibo do lote fiscal relatou autorização da posição01 após retentativa (invoice254af27a-8f4c-4f51-a2ec-291c668daebb), posições01–07 emitidas com PDF/XML, e interrupção na posição08 (invoicefcc65f27-a93b-4736-b381-774766878a98) por resposta nãoJSON HTTP503 do SNNFSE, sem número/chave/PDF/XML para essa tentativa. Envio externo permanecia bloqueado. Posição do lote não é número oficial deNFS-e; erro de resposta não prova inexistência de emissão remota. Conferir esses identificadores no registro/provider antes de qualquer retry autorizado. A chave fiscal e os documentos operacionais permanecem fora desta memória cognitiva e do escopo de exclusão de históricos. Fonte: unidades 3405.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch14-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
