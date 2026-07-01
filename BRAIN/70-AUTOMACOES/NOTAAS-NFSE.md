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
- Se houver duas ou mais NFS-e para o mesmo `cliente_id`, CPF, CNPJ ou documento de cliente, enviar um único e-mail para esse cliente.
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
