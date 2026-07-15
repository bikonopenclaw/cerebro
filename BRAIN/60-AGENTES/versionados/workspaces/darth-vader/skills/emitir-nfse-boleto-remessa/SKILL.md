---
name: emitir-nfse-boleto-remessa
description: Use quando o pedido envolver emissão ou preparação de NFS-e, boleto Cresol, Cresol API e arquivo de remessa bancária em um fluxo único. Orquestra emissão fiscal, boleto oficial ou homologado, remessa CNAB400/CNAB240, retorno/ocorrências e validações, com travas para não afirmar emissão real sem comprovante.
---

# Emitir NFS-e, boleto e remessa

Use esta skill para fluxos como:

- “emita a nota igual ao mês passado, gere boleto e remessa”
- “crie NFS-e, boleto Cresol e arquivo `.rem`”
- “teste emissão de nota/boleto/remessa para homologação”
- “repita a cobrança do cliente X com vencimento Y”
- “emita uma lista/lote de notas com boleto e remessa”
- “gere boleto pela API Cresol”
- “consulte pagamento/ocorrência de boleto Cresol”

## Regra de ouro

Não afirmar que NFS-e ou boleto foram emitidos sem comprovante real.

Estados permitidos:

- `rascunho_preparado`: dados montados, nada emitido.
- `nfse_emitida`: somente com DANFSe/XML/chave retornada pelo emissor.
- `boleto_emitido_homologacao`: PDF/linha digitável/código de barras gerados pela skill para conferência.
- `boleto_registrado_api_homologacao`: título criado no ambiente de homologação da API Cresol.
- `boleto_pdf_api_homologacao`: PDF baixado do ambiente de homologação da API Cresol.
- `boleto_emitido`: somente com PDF/linha digitável/nosso número confirmado pelo sistema/banco.
- `remessa_gerada_homologacao`: arquivo `.rem` para teste, não produção.
- `remessa_validada_homologacao`: arquivo `.rem` validado pelo ambiente de teste do banco.
- `remessa_pronta_producao`: só depois de homologação bancária aprovada pelo Hebert e ordem explícita para produção.
- `ocorrencias_api_importadas`: ocorrências consultadas na API Cresol e registradas no banco local.

## Travas de segurança

- Emissão fiscal real é ação externa. Se não houver acesso/API/sessão do emissor, preparar o rascunho e parar.
- Boleto real pode gerar cobrança. Se não houver retorno do sistema/banco, tratar como boleto de homologação/conferência, mesmo que o PDF esteja correto.
- Remessa bancária pode registrar, alterar, baixar ou protestar títulos. Nunca subir no banco. O Hebert faz a validação ou autoriza explicitamente.
- Cresol API em produção também pode gerar cobrança, alterar vencimento ou baixar título. Só usar produção com aprovação explícita do Hebert.
- Na fase inicial, nunca executar baixa automática pela API. Baixa por API deve ficar bloqueada até homologação e autorização específica.
- Não usar valor de segunda via com multa/mora como valor base de nova cobrança. Para nova emissão, usar valor original da NFS-e, salvo ordem explícita.
- Não inventar número de NFS-e. Se o emissor ainda não retornou número/chave, usar `pendente`.
- Credenciais da Cresol API ficam somente em arquivo secreto local ou cofre, nunca no Git, Brain, SKILL.md, job JSON, relatório ou pacote de emissão.

## Caminhos

- Workspace boleto/remessa: `/data/.openclaw/workspace-darth-vader/boletos`
- Cadastro mestre de clientes ativos: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.json`
- Cadastro tabular: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.csv`
- E-mails financeiros separados: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_emails_financeiro.csv`
- Banco SQLite do cadastro: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.sqlite`
- Inconsistências do cadastro: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/inconsistencias.md`
- Ferramenta de manutenção do cadastro: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/scripts/clientes_tool.py`
- Configuração de e-mail NFS-e Bikon: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/config/email.json`
- Template HTML padrão dos e-mails NFS-e Bikon: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/templates/email_nfse_bikon.html`
- Gerador de rascunho/envio controlado de e-mail NFS-e: `/data/.openclaw/workspace-darth-vader/skills/notaas-nfse/scripts/preparar_email_cliente.py`
- Skill técnica Cresol: `/data/.openclaw/agents/darth-vader/agent/skills/boletos-cresol/SKILL.md`
- Gerador boleto HTML/PDF homologação: `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_boleto_cresol_html.py`
- Gerador CNAB400 homologação: `/data/.openclaw/workspace-darth-vader/boletos/scripts/gerar_remessa_cnab400_cresol.py`
- Pacotes do fluxo: `/data/.openclaw/workspace-darth-vader/boletos/pacotes-emissao`
- Banco local de faturamento: `/data/.openclaw/workspace-darth-vader/boletos/db/faturamento.db`
- Script de banco/conciliação/relatório: `/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/scripts/faturamento_db.py`
- Referência Cresol API: `references/cresol-api-boletos.md`
- Cliente Cresol API homologação: `scripts/cresol_api_client.py`

## Workflow obrigatório

1. Buscar tomador/pagador no cadastro mestre de clientes ativos antes de montar NFS-e/boleto.
2. Se o cadastro tiver inconsistência crítica para o cliente, parar e pedir correção ao Hebert antes de emitir.
3. Se o cliente tiver mais de um e-mail financeiro, preservar todos no job/rascunho/envio.
4. Extrair dados da NFS-e anterior e do boleto anterior quando aplicável.
5. Montar um job JSON do novo ciclo em `pacotes-emissao/YYYYMMDD-cliente/`.
6. Validar dados mínimos:
   - prestador
   - tomador
   - serviços/itens
   - valor original
   - vencimento
   - documento
   - nosso número ou regra para próximo número
   - pagador
   - conta/carteira/cooperativa Cresol
7. Separar o fluxo em 3 blocos:
   - NFS-e
   - boleto
   - remessa/API bancária
8. Se não houver acesso ao emissor fiscal, marcar NFS-e como `rascunho_preparado` e listar exatamente o que falta para emitir.
9. Se houver Cresol API disponível, usar primeiro ambiente de homologação. Ler `references/cresol-api-boletos.md` antes de montar payload ou interpretar retorno.
10. Se não houver acesso ao sistema/API do boleto/banco, gerar apenas boleto/remessa de homologação local, mantendo boleto como `boleto_emitido_homologacao` ou `rascunho_preparado`, conforme evidência.
11. Gerar boleto PDF limpo para conferência, com linha digitável, código de barras e nosso número calculados.
12. Quando a API Cresol retornar título/PDF oficial, registrar status próprio no pacote e no banco local, sem apagar o PDF local de conferência.
13. Gerar `.rem` somente com dados coerentes e validar linha de 400 caracteres, header/detalhe/trailer e CRLF.
14. Se Hebert informar que a remessa validou no banco, atualizar o pacote/status para `remessa_validada_homologacao`; não considerar produção automaticamente.
15. Preparar e-mail automático para o cliente quando a NFS-e real tiver PDF/XML baixados:
   - usar e-mails financeiros do cadastro mestre ou `tomador.email`/`email.to` do job
   - anexar DANFSe PDF, XML da NFS-e e boleto PDF quando houver
   - usar PDF oficial da API Cresol quando disponível e validado
   - usar o template HTML padrão Bikon e fallback texto simples
   - gerar `email-nfse-cliente.eml` e `email-nfse-cliente.json` no pacote
   - envio real para cliente externo exige autorização explícita do Hebert e `job.email.aprovado_por_hebert=true`
   - se faltar e-mail financeiro, bloquear envio e marcar pendência cadastral
   - em teste controlado, enviar apenas para destinatário explícito, sem buscar cadastro do cliente
16. Registrar o pacote no banco local de faturamento quando houver NFS-e, boleto, retorno de API ou remessa gerados/importados.
17. Entregar ao Hebert:
   - status da NFS-e
   - status do boleto
   - status da remessa/API bancária
   - status do e-mail ao cliente
   - status do registro no banco de faturamento
   - arquivos gerados
   - pendências objetivas

## Cresol API, fase 1

Fase 1 é documentação e desenho de uso. Não chama serviço externo.

Escopo permitido na fase 1:

- Guardar referência técnica da API em `references/cresol-api-boletos.md`.
- Definir estados, travas e ponto de encaixe no workflow.
- Planejar cliente de homologação para fase 2.
- Definir que credenciais ficam fora da skill e fora do Git.

Escopo bloqueado na fase 1:

- Autenticar na Cresol API.
- Criar título real ou de homologação.
- Alterar vencimento.
- Dar baixa.
- Enviar boleto a cliente.
- Trocar CNAB/remessa pelo uso da API.

## Cresol API, fase 2

Fase 2 cria e valida o cliente de homologação, sem produção.

Escopo permitido na fase 2:

- Confirmar paths no Swagger/OpenAPI.
- Criar cliente CLI em `scripts/cresol_api_client.py`.
- Testar autenticação em homologação quando Hebert fornecer credencial por canal seguro.
- Testar consultas somente leitura: parâmetros da conta, espécies, títulos, pagadores, sequenciais e ocorrências.
- Baixar PDF oficial somente de título de homologação/controlado.

Escopo bloqueado na fase 2:

- Produção sem flag explícita e nova autorização do Hebert.
- Criar título sem `--allow-write`.
- Alterar vencimento sem `--allow-write`.
- Baixar título por API. Esta operação permanece bloqueada no cliente inicial.
- Enviar boleto para cliente externo.

## Lote como padrão operacional

O padrão definido pelo Hebert é entregar uma lista de notas para emitir em lote. Quando receber lista/planilha/CSV:

1. Ler `references/lote-schema.md`.
2. Converter cada linha em job individual.
3. Rodar o script de lote.
4. Entregar `status-lote.md`, boletos/remessas gerados e pendências por linha.

Para processar CSV:

```bash
/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/scripts/preparar_lote_emissao.py --csv /caminho/lote.csv
```

## Script auxiliar

Para criar pacote operacional e remessa a partir de JSON:

```bash
/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/scripts/preparar_pacote_emissao.py --job /caminho/job.json
```

Leia `references/job-schema.md` quando precisar montar ou validar o JSON.
Leia `references/lote-schema.md` quando o Hebert entregar uma lista de notas para emitir em lote.
Leia `references/modelo-geral-validado.md` quando for repetir o fluxo completo ou alterar scripts. O caso Unus é golden case validado, mas o modelo é geral e parametrizado por job.
Leia `references/faturamento-db-retorno.md` quando o pedido envolver banco de faturamento, relatório financeiro de NFS-e/boleto/remessa, importação de retorno bancário, conciliação, baixa de boleto, juros, multa, valor pago ou divergência entre valor original e valor recebido.
Leia `references/cresol-api-boletos.md` quando o pedido envolver API Cresol, título oficial, PDF oficial, alteração de vencimento, baixa via API, pagadores, sequenciais ou ocorrências.

## Banco de faturamento e retorno bancário

A skill deve manter controle interno de NFS-e, boletos, remessas e retornos bancários em SQLite.

Regras:

- Registrar pacote de emissão no banco local ao final do preparo/geração.
- Preservar valor original do boleto e registrar separadamente valor pago, juros/mora, tarifa, desconto, abatimento, outros créditos e data de crédito.
- Quando Hebert enviar arquivo de retorno do banco, importar o arquivo e conciliar contra boletos registrados.
- Para Cresol CNAB400, usar o parser do `faturamento_db.py` e o mapa de retorno Cresol já salvo em `boletos/manual-cresol`.
- Quando houver ocorrências da Cresol API, importar como fonte bancária adicional e manter rastreabilidade do sequencial consultado.
- Baixa por retorno ou ocorrência atualiza o controle local; não altera banco externo nem sistema fiscal.
- Baixa via API é operação externa e deve permanecer bloqueada até autorização explícita e procedimento próprio.
- Se uma ocorrência de retorno/API não encontrar boleto correspondente, registrar como não conciliada e reportar.

Comandos principais:

```bash
python3 scripts/faturamento_db.py init
python3 scripts/faturamento_db.py registrar-pacote --pacote /caminho/pacote
python3 scripts/faturamento_db.py sincronizar-pacotes
python3 scripts/faturamento_db.py importar-retorno --arquivo /caminho/retorno.ret
python3 scripts/faturamento_db.py relatorio --output /caminho/relatorio.md
```

## Integração com boletos-cresol

Quando o pedido envolver Cresol/CNAB, use também a skill `boletos-cresol` para detalhes de layout, cálculo de DV, validação e restrições bancárias.

Quando o pedido envolver Cresol API, use esta skill como orquestradora e a referência `references/cresol-api-boletos.md` como fonte técnica inicial. CNAB continua como fallback, auditoria e caminho de homologação até a API estar validada.

## Resposta padrão para o Hebert

Sempre responder em 3 linhas:

1. O que foi pedido.
2. O que foi entregue, separando NFS-e, boleto e remessa/API bancária.
3. Próximo passo sugerido ou bloqueio real.
