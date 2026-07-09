# Cresol API, boletos

Fonte inicial: anexo `API_Cresol---4f2b8a39-5fb7-4450-baa5-7bffa4814537.rtf`, recebido em 2026-07-08.

## Objetivo

Usar a API de boletos Cresol como camada futura para registrar títulos oficiais, baixar PDF oficial, consultar títulos, alterar vencimento e importar ocorrências para conciliação.

Esta referência é fase 1. Ela documenta a API e define guardrails. Não autoriza chamada externa.

## Ambientes

Swagger homologação:

```text
https://api-dev.governarti.com.br/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config#/
```

Swagger produção:

```text
https://cresolapi.governarti.com.br/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config
```

Servidor homologação:

```text
https://api-dev.governarti.com.br
```

Servidor produção:

```text
https://cresolapi.governarti.com.br
```

## Paths confirmados no OpenAPI

Em 2026-07-08, o Swagger de produção respondeu em `/v3/api-docs` e confirmou estes paths. A base de homologação respondeu `401 Unauthorized` para os mesmos paths, indicando que os endpoints existem, mesmo com `/v3/api-docs` retornando 404 no ambiente dev.

- `GET /especies`
- `GET /grupos-pagadores`
- `GET /ocorrencias/sequenciais`
- `GET /ocorrencias/{sequencial}`
- `GET /pagadores`
- `POST /pagadores`
- `GET /pagadores/{id}`
- `PUT /pagadores/{id}`
- `DELETE /pagadores/{id}`
- `GET /parametros-conta`
- `GET /titulos`
- `POST /titulos`
- `GET /titulos/{id}`
- `PUT /titulos/{id}`
- `GET /titulos/pdf/{id}`
- `PUT /titulos/{id}/operacao/baixar`

Query params confirmados:

- `GET /titulos`: `page`, `size`, `status`, `dt_vencimento_ini`, `dt_vencimento_fim`, `dt_processamento_ini`, `dt_processamento_fim`.
- `GET /pagadores`: `page`, `size`, `nomePagador`.
- `GET /titulos/pdf/{id}`: `formato`, `capa`, `nr_parcela_inicial`, `nr_parcela_final`.
- `GET /ocorrencias/sequenciais`: `dateStart`, `dateEnd`.

## Autenticação

A API usa OAuth 2.0 com Bearer Token.

Endpoint homologação:

```text
POST https://auth-dev.governarti.com.br/auth/realms/cresol/protocol/openid-connect/token
```

Endpoint produção:

```text
POST https://cresolauth.governarti.com.br/auth/realms/cresol/protocol/openid-connect/token
```

Content-Type:

```text
application/x-www-form-urlencoded
```

Campos esperados:

- `username`: login do sistema.
- `password`: CPF/CNPJ em homologação ou senha de acesso em produção, conforme documentação recebida.
- `grant_type`: `password`.
- `client_id`: `cresolApi`.
- `scope`: `read`.
- `client_secret`: deve ser tratado como segredo, mesmo que conste no documento. Não salvar em skill, Git, Brain, job JSON ou relatório.

O retorno inclui:

- `access_token`
- `expires_in`: 300 segundos
- `refresh_expires_in`: 1800 segundos
- `refresh_token`
- `token_type`: bearer
- `scope`

Regra operacional: capturar `access_token` e usar em `Authorization: Bearer <token>` nas chamadas protegidas. Renovar token quando expirar.

## Títulos de cobrança

A API permite:

- Criar títulos em lote via `POST titulos`.
- Consultar títulos por status via `GET titulos`, por exemplo `status=EM_ABERTO`.
- Consultar título por ID via `GET titulos/{id}`.
- Baixar PDF oficial via `GET titulos/pdf/{id}`.
- Atualizar vencimento de título em aberto via `PUT titulos/{id}` com `dtVencimento`.
- Baixar título via endpoint de baixa.

Payload base para criação de título é array de objetos JSON, mesmo para um único título.

Campos observados no documento:

- `nossoNumero`
- `idEspecie`
- `tipoPagador`
- `docPagador`
- `pagadorNome`
- `pagadorEndereco`
- `pagadorEnderecoNumero`
- `pagadorBairro`
- `pagadorCep`
- `pagadorCidade`
- `pagadorUf`
- `numeroDocumento`
- `dtVencimento`
- `dtDocumento`
- `valorNominal`

Pendência de fase 2: confirmar paths exatos no Swagger, porque o RTF recebido omitiu/ocultou parte das URLs dos endpoints.

## Pagadores

A API permite:

- Listar pagadores.
- Consultar pagador por ID.
- Cadastrar pagador.
- Atualizar pagador.
- Excluir pagador, somente quando não houver título emitido para ele.

Observação: o documento informa que o pagador pode ser cadastrado automaticamente na primeira geração de título.

Regra operacional: cadastro mestre local da Bikon continua sendo fonte principal. API Cresol não substitui cadastro local sem rotina explícita de sincronização.

## Ocorrências e sequenciais

A API permite consultar sequenciais de ocorrência e detalhes das ocorrências.

Endpoint conceitual de sequenciais:

- Parâmetros: `dateStart` e `dateEnd`, exemplo `?dateStart=2025-09-16&dateEnd=2025-09-16`.
- Retorno contém `nrSequencial`, `dtOcorrenciaInicial`, `dtOcorrenciaFinal`.

Endpoint conceitual de ocorrências:

- Parâmetro: ID/número do sequencial.
- Retorno contém ocorrências com campos como:
  - `id`
  - `idParcela`
  - `tipo`
  - `valor`
  - `codigoOcorrencia`
  - `descricaoOcorrencia`
  - `dtOcorrencia`
  - `motivo`

Calendário informado:

- Terça-feira: ocorrências de sábado, domingo e segunda.
- Quarta-feira: ocorrências de terça.
- Quinta-feira: ocorrências de quarta.
- Sexta-feira: ocorrências de quinta.
- Segunda-feira: ocorrências de sexta.

Regra operacional: ocorrências de API podem alimentar o banco local de faturamento como fonte adicional ao retorno CNAB. Não alterar banco externo nem baixar título automaticamente.

## Juros e multa

Campos citados:

- `cdTipoJuros`: valores permitidos `[0, 1, 3]`.
  - `0`: valor fixo.
  - `1`: valor percentual.
  - `3`: isento.
- `cdTipoMulta`: valores permitidos `[1, 0, 5]`.
  - `1`: valor fixo.
  - `0`: valor percentual.
  - `5`: isento.

Observação do documento: para isentar multa/juros, não é obrigatório informar os campos.

Regra Bikon atual: multa de 2,00% após vencimento e juros de mora diário calculado como 1% ao mês proporcional ao dia. Antes de chamar API, mapear essa regra para os códigos aceitos pelo Swagger.

## Guardrails

- Produção bloqueada até autorização explícita do Hebert.
- Baixa via API bloqueada até procedimento próprio e autorização explícita.
- Alteração de vencimento é ação externa e exige autorização explícita quando for produção.
- Credenciais ficam fora da skill, fora do Git e fora do Brain.
- O PDF oficial da API não elimina a necessidade de validar valor, vencimento, pagador e nosso número contra NFS-e/job.
- CNAB/remessa permanece como fallback e trilha de auditoria até a API ser homologada.

## Fase 2 sugerida

Criar cliente de homologação `cresol_api_client.py` com funções:

- `get_token()`
- `listar_titulos(status)`
- `criar_titulos(payload_array)`
- `consultar_titulo(id)`
- `baixar_pdf_titulo(id, destino)`
- `listar_sequenciais(date_start, date_end)`
- `listar_ocorrencias(sequencial_id)`

A fase 2 deve usar somente homologação e payload fictício/controlado até aprovação do Hebert.

## Cliente CLI criado

Script:

```text
scripts/cresol_api_client.py
```

Credenciais esperadas fora da skill:

```text
/data/.openclaw/secrets/cresol-api.env
```

Variáveis:

- `CRESOL_API_USERNAME`
- `CRESOL_API_PASSWORD`
- `CRESOL_API_CLIENT_ID`
- `CRESOL_API_CLIENT_SECRET`
- `CRESOL_API_SCOPE`

Comandos seguros de leitura:

```bash
python3 scripts/cresol_api_client.py token-test
python3 scripts/cresol_api_client.py parametros-conta
python3 scripts/cresol_api_client.py especies
python3 scripts/cresol_api_client.py titulos --status EM_ABERTO
python3 scripts/cresol_api_client.py pagadores --nome NOME
python3 scripts/cresol_api_client.py sequenciais --date-start AAAA-MM-DD --date-end AAAA-MM-DD
python3 scripts/cresol_api_client.py ocorrencias --sequencial 123
```

Comandos de escrita exigem `--allow-write`. Produção exige também `--env producao --allow-producao`.

## Validação de homologação, 2026-07-08

Credenciais de homologação foram salvas fora da skill em:

```text
/data/.openclaw/secrets/cresol-api.env
```

Permissão validada: `600`.

Testes executados em homologação:

- `token-test`: OK.
- `parametros-conta`: OK.
- `especies`: OK.
- `titulos --status EM_ABERTO --size 5`: OK, retornou lista vazia.
- `pagadores --size 3`: OK, retornou cadastro paginado.
- `sequenciais --date-start 2026-07-08 --date-end 2026-07-08`: OK, retornou lista vazia.

Observação operacional: chamadas paralelas de autenticação podem retornar HTTP 500 no servidor de homologação. Usar chamadas sequenciais e, na próxima evolução, reaproveitar token até expirar.

Parâmetros de conta observados em homologação:

- `nrFormatoJuros`: `1`
- `nrJurosDia`: `2.0`
- `nrFormatoMulta`: `0`
- `nrPorcentagemMulta`: `1.0`
- `fgNegativacao`: `0`
- `fgProtesto`: `0`
- `fgPixAtivado`: `false`

Alerta resolvido em 2026-07-08: Hebert definiu usar juros de 1% e multa de 2%. Para manter coerência com a regra operacional já existente na skill, interpretar juros como 1% ao mês proporcional ao dia, e multa como 2,00% após vencimento. Esta regra deve prevalecer no payload mesmo quando os parâmetros retornados pela conta de homologação divergirem.

## Título de teste em homologação, 2026-07-08

Autorização de Hebert recebida em 2026-07-08 para criar um título de teste em homologação.

Payload salvo em:

```text
/data/.openclaw/workspace-darth-vader/boletos/api-homologacao/payload-titulo-teste-20260708.json
```

Primeira tentativa rejeitada corretamente pela API:

- `numeroDocumento` maior que 15 caracteres.

Payload ajustado para `numeroDocumento=TST260708001`.

Resultado da criação:

- `id`: `22389619`
- `nossoNumero`: `352`
- `dvNossoNumero`: `5`
- `numeroDocumento`: `TST260708001`
- `status`: `EM_PROCESSAMENTO`
- `valorNominal`: `1.0`
- `dtVencimento`: `2026-07-15`
- `linhaDigitavel`: `13391.00800 90000.000035 52002.784602 1 15080000000100`

Arquivos salvos:

```text
/data/.openclaw/workspace-darth-vader/boletos/api-homologacao/resultado-criar-titulo-teste-20260708.json
/data/.openclaw/workspace-darth-vader/boletos/api-homologacao/consulta-titulo-teste-20260708-22389619.json
/data/.openclaw/workspace-darth-vader/boletos/api-homologacao/baixar-pdf-titulo-teste-20260708-22389619.json
/data/.openclaw/workspace-darth-vader/boletos/api-homologacao/titulo-teste-20260708-22389619.pdf
```

PDF oficial baixado com sucesso:

- Content-Type: `application/pdf`
- Tamanho: `15920` bytes

Próxima etapa recomendada: consultar o título novamente após processamento para verificar transição de status, e só depois testar ocorrências/sequenciais vinculados.
