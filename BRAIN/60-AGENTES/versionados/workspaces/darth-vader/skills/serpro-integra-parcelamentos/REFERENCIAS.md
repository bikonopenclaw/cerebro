# Referências válidas — SERPRO Integra Contador / Parcelamento Simples Nacional

Última atualização: 2026-06-18
Escopo: automação de controle e emissão assistida de DAS de parcelamento do Simples Nacional da Bikon Tecnologia.

## 1. Contrato Bikon / SERPRO

### Contrato recebido
- Arquivo original: `/data/.openclaw/media/inbound/contrato-num-540190---7018163b-eee9-4161-b1be-f88095ffe11e.pdf`
- Texto extraído: `/data/.openclaw/workspace/serpro-integra-contador-contrato-540190-extraido.txt`
- Resumo operacional: `/data/.openclaw/workspace/serpro-integra-contador-contrato-540190-resumo.md`

### Dados confirmados
- Cliente: BIKON TECNOLOGIA DA INFORMACAO LTDA
- CNPJ: 34.191.026/0001-86
- Pedido/contrato SERPRO: 540190
- Serviço: Integra Contador
- Data de assinatura/registro: 18/06/2026
- Vigência exibida no registro: 18/06/2026 a 18/06/2031
- Cláusula contratual de vigência: prazo indeterminado a partir da celebração

### Preços encontrados no contrato
Consulta:
- Faixa 01, 1 a 300 requisições: R$ 0,2400 por requisição
- Faixas maiores reduzem progressivamente até R$ 0,0600 por requisição acima de 30.000

Declaração:
- Faixa 01, 1 a 100 requisições: R$ 0,4000 por requisição
- Faixas maiores reduzem progressivamente até R$ 0,1200 por requisição acima de 10.000

Emissão:
- Faixa 01, 1 a 500 requisições: R$ 0,3200 por requisição
- Faixas maiores reduzem progressivamente até R$ 0,0800 por requisição acima de 50.000

Cobrança:
- Mensal por consumo.
- Período de consumo: dia 21 do mês anterior ao dia 20 do mês de referência.
- NF até o último dia útil do mês.
- Pagamento em até 30 dias corridos da emissão da NF.

## 2. Documentação oficial SERPRO

### Página geral da API Integra Contador
URL: https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/

Uso futuro:
- Introdução do produto.
- Explica que o Integra Contador é contratado na Loja SERPRO.
- Explica uso com certificado digital e-CNPJ.
- Explica necessidade de procuração digital no e-CAC quando o autor do pedido não for o próprio contribuinte.

Trecho relevante validado:
- “O Integra Contador é uma plataforma de serviços (APIs), disponibilizada aos clientes que obtiverem credenciais de acesso, mediante contratação junto à loja Serpro, utilizando certificado digital e-CNPJ.”
- Serviços com procuração exigem permissão no e-CAC.

### Loja SERPRO, produto Integra Contador
URL: https://loja.serpro.gov.br/integra-contador/product/integracontador

Uso futuro:
- Página comercial do produto.
- Contratação e gestão do produto.
- Conferência de preço/tabela vigente, pois o contrato referencia a página do produto e a Área do Cliente.

### Catálogo de Serviços do Integra Contador
URL: https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/pt/catalogo_de_servicos/

Uso futuro:
- Confirmar `idSistema`, `idServico`, tipo e situação de cada serviço.
- Fonte oficial para mapear chamadas disponíveis.

Serviços úteis identificados:

#### Integra-SN / PGDASD
- `PGDASD TRANSDECLARACAO11`: entregar declaração mensal.
- `PGDASD GERARDAS12`: gerar DAS mensal.
- `PGDASD CONSDECLARACAO13`: consultar declarações transmitidas.
- `PGDASD CONSULTIMADECREC14`: consultar última declaração/recibo transmitida.
- `PGDASD CONSDECREC15`: consultar declaração/recibo.
- `PGDASD CONSEXTRATO16`: consultar extrato do DAS.
- `PGDASD GERARDASCOBRANCA17`: gerar DAS referente a período no sistema de cobrança da RFB.
- `PGDASD GERARDASPROCESSO18`: gerar DAS referente a processo no sistema de cobrança da RFB.
- `PGDASD GERARDASAVULSO19`: gerar DAS avulso.

Observação:
- PGDASD é útil para DAS mensal e extratos, mas o foco desta skill é parcelamento.

#### Integra-Parcelamentos / PARCSN
Sistema: `PARCSN`, Parcelamento do Simples Nacional ordinário.

Serviços principais para esta skill:
- `PARCSN GERARDAS161`: gerar DAS de parcela do parcelamento.
- `PARCSN PARCELASPARAGERAR162`: consultar parcelas disponíveis para geração.
- `PARCSN PEDIDOSPARC163`: consultar pedidos de parcelamento.
- `PARCSN OBTERPARC164`: obter detalhes de parcelamento.
- `PARCSN DETPAGTOPARC165`: consultar detalhes de pagamento de parcela.

### Integra Parcelamentos, contexto
URL: https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/pt/solucoes/integra-parcelamento/

Uso futuro:
- Fonte oficial sobre a solução Integra Parcelamentos.
- Confirma sistemas disponíveis: PARCSN, PARCSN-ESP, PERTSN, RELPSN, PARCMEI, PARCMEI-ESP, PERTMEI, RELPMEI.

Trecho relevante validado:
- “É uma solução integrada ao sistema de Parcelamentos do Simples Nacional e MEI.”
- Permite parcelamento/reparcelamento de débitos apurados pelo Simples Nacional vencidos e em cobrança na RFB.

### Serviços x Procurações
URL: https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/pt/servicos_vs_procuracoes/

Uso futuro:
- Verificar quais serviços exigem procuração eletrônica e-CAC.
- Validar códigos de procuração necessários quando o autor do pedido não for o próprio contribuinte.

Procurações relacionadas ao PARCSN:
- `00076`: Parcelamento de Débitos do Simples Nacional.
- `00188`: Solicitar, acompanhar e emitir DAS de parcelamento.

Serviços PARCSN vinculados às procurações acima:
- `GERARDAS161`
- `PARCELASPARAGERAR162`
- `PEDIDOSPARC163`
- `OBTERPARC164`
- `DETPAGTOPARC165`

## 3. Fontes oficiais Receita / Gov.br sobre regra de negócio

### Parcelar dívidas do Simples Nacional
URL: https://www.gov.br/pt-br/servicos/parcelar-imposto-simples

Uso futuro:
- Regras gerais do parcelamento.
- Limite de parcelas.
- Valor mínimo.
- Validação pela primeira parcela.
- Rescisão por inadimplência.

Pontos validados:
- Parcelamento pode ser feito em até 60 vezes.
- Parcela mínima de R$ 300,00 no âmbito RFB.
- Aprovação depende do pagamento da primeira parcela.
- Pode rescindir se faltar pagamento de 3 parcelas, seguidas ou não, ou da última parcela se as demais estiverem pagas.
- Débitos ainda não inscritos em Dívida Ativa ficam na Receita Federal.
- Débitos inscritos em Dívida Ativa vão para PGFN.

### Perguntas e Respostas, Receita Federal, Parcelamento Simples Nacional
URL: https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/pagamentos-e-parcelamentos/parcelamento-simples-nacional/perguntas-e-respostas

Uso futuro:
- Regras operacionais detalhadas.
- Quando solicitar.
- Quem é o ente responsável.
- Como emitir DAS de parcela.
- Juros/Selic.

Pontos validados:
- Pedido pode ser feito no Portal do Simples Nacional ou e-CAC, serviço “Parcelamento, Simples Nacional”.
- Acesso por certificado digital ou código de acesso no Portal do Simples.
- Acesso e-CAC por certificado digital/Gov.br.
- Máximo 60 parcelas e mínimo 2.
- Parcela mínima R$ 300,00.
- Demais parcelas vencem até o último dia útil de cada mês.
- Parcela mensal recebe Selic acumulada a partir do mês seguinte à consolidação, mais 1% no mês do pagamento.
- DAS da parcela é emitido no serviço “Parcelamento, Simples Nacional”, função “Emissão de Parcela”.

### PGFN, emissão de DAS para dívida ativa
URL: https://www.gov.br/pgfn/pt-br/servicos/orientacoes-contribuintes/emissao-de-das

Uso futuro:
- Quando o débito de Simples Nacional estiver inscrito em Dívida Ativa da União.
- Este fluxo não é o foco inicial da skill PARCSN/RFB.

Pontos validados:
- Emissão pelo REGULARIZE.
- Permite DAS integral ou parcial de débitos de Simples Nacional inscritos em dívida ativa.
- Exige CPF/CNPJ do contribuinte devedor e número da inscrição.

## 4. Regra técnica decidida para a skill

### Modo inicial
- Rodar em modo consulta/leitura.
- Não gerar DAS real automaticamente.
- Toda chamada `GERARDAS161` exige confirmação explícita do Hebert.

### CNPJ inicial
- Bikon Tecnologia: 34.191.026/0001-86.

### Certificado
- Certificado A1.
- Nunca salvar senha/certificado em Markdown, Git, chat ou print.
- Salvar depois em cofre/local seguro definido.

### Procuração
- Como contratante e contribuinte inicial são a própria Bikon, testar primeiro sem procuração de terceiro.
- Se a API negar permissão, validar e-CAC para os serviços `00076` e `00188`.

## 5. Checklist quando as credenciais estiverem disponíveis

1. Confirmar liberação do contrato na Área do Cliente SERPRO.
2. Obter credenciais de API sem colar secrets no chat.
3. Salvar secrets em arquivo seguro ou secret manager.
4. Salvar certificado A1 em local seguro fora do repositório.
5. Implementar autenticação.
6. Testar chamada de consulta simples.
7. Testar `PEDIDOSPARC163` para o CNPJ da Bikon.
8. Testar `OBTERPARC164` se houver parcelamento ativo.
9. Testar `PARCELASPARAGERAR162`.
10. Persistir resultado local.
11. Só liberar `GERARDAS161` depois de confirmação explícita.

## 6. Arquivos locais relacionados

- Especificação principal: `/data/.openclaw/workspace-darth-vader/skills/serpro-integra-parcelamentos/README.md`
- Configuração exemplo: `/data/.openclaw/workspace-darth-vader/skills/serpro-integra-parcelamentos/config.example.json`
- Este arquivo: `/data/.openclaw/workspace-darth-vader/skills/serpro-integra-parcelamentos/REFERENCIAS.md`

## 7. API Reference oficial, Produção

URL da página:
https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/pt/chamadas/api_reference/

Arquivo OpenAPI/YAML usado pela página:
https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/pt/chamadas/api_reference/api-integra-contador-sp.yaml

Cópia local salva para consulta futura:
`/data/.openclaw/workspace-darth-vader/skills/serpro-integra-parcelamentos/api-integra-contador-sp.yaml`

Última atualização exibida pela página: 13/03/2026.

### Base URL de produção
```text
https://gateway.apiserpro.serpro.gov.br/integra-contador/v1
```

### Endpoints genéricos disponíveis
A API Reference não cria um endpoint separado por serviço fiscal. Ela usa endpoints genéricos por tipo de operação. O serviço fiscal real é definido no corpo da requisição, dentro de `pedidoDados.idSistema` e `pedidoDados.idServico`.

Endpoints:
- `POST /Apoiar`: serviços auxiliares de suporte.
- `POST /Consultar`: envio de pedido de dados do tipo consulta.
- `POST /Declarar`: entrega/transmissão de declaração.
- `POST /Emitir`: emissão/geração de documento de arrecadação.
- `POST /Monitorar`: serviços auxiliares de monitoração de eventos.

Para esta skill PARCSN:
- Consultas de parcelamento usam `POST /Consultar`.
- Geração de DAS usa `POST /Emitir`.

### Autenticação e headers
Header obrigatório em todas as requisições:
```text
jwt_token: <token>
```

Descrição oficial:
- `jwt_token` é obrigatório e deve ser informado em todas as requisições.
- Esse token é obtido do serviço `/Authenticate` do SAPI.

Header opcional:
```text
autenticar_procurador_token: <token>
```

Uso:
- Informar quando um procurador assinou XML autorizando o contratante a utilizar em seu nome.
- A documentação referencia o serviço `ENVIOXMLASSINADO81` para esse fluxo.
- Para Bikon usando o próprio CNPJ como contratante/contribuinte, testar primeiro sem esse header.
- Se houver contador/terceiro, provavelmente precisará de procuração e esse token.

A especificação também informa `securitySchemes.bearerAuth` tipo HTTP bearer. Na implementação, considerar que pode haver dois níveis:
- autenticação de gateway/aplicação SERPRO;
- `jwt_token` exigido pela API Integra Contador.

Validar no primeiro teste real com credenciais.

### Estrutura do corpo JSON
Schema principal: `DadosEntrada`.

```json
{
  "contratante": {
    "numero": "34191026000186",
    "tipo": 2
  },
  "autorPedidoDados": {
    "numero": "34191026000186",
    "tipo": 2
  },
  "contribuinte": {
    "numero": "34191026000186",
    "tipo": 2
  },
  "pedidoDados": {
    "idSistema": "PARCSN",
    "idServico": "PEDIDOSPARC163",
    "versaoSistema": "1.0",
    "dados": "{}"
  }
}
```

Campos:
- `contratante`: identificação de quem contratou o Integra Contador.
- `autorPedidoDados`: identificação de quem está solicitando os dados.
- `contribuinte`: identificação do contribuinte alvo.
- `pedidoDados`: pedido específico para o sistema/serviço fiscal.

### Identificação, TipoNi
Schema `Identificacao`:
```json
{
  "numero": "string",
  "tipo": 1
}
```

Schema `TipoNi`:
- `1`: pessoa física, CPF.
- `2`: pessoa jurídica, CNPJ.

Para a Bikon:
```json
{
  "numero": "34191026000186",
  "tipo": 2
}
```

### PedidoDados
Schema:
```json
{
  "idSistema": "string",
  "idServico": "string",
  "versaoSistema": "string",
  "dados": "string"
}
```

Ponto importante:
- `dados` é string, não objeto JSON direto.
- Quando o serviço exigir parâmetros, serializar o JSON interno como string.
- Quando não houver parâmetros, testar com `"{}"` ou conforme exemplo específico do serviço.

### Responses e erros
Responses previstos na especificação:
- `200`: Success.
- `400`: Bad Request.
- `401`: Unauthorized.
- `403`: Forbidden.
- `404`: Not Found.
- `500`: Server Error.

Schema de erro `ProblemDetails`:
```json
{
  "type": "string",
  "title": "string",
  "status": 400,
  "detail": "string",
  "instance": "string"
}
```

Tratamento recomendado na skill:
- `400`: erro de payload, idSistema/idServico, versão ou dados internos.
- `401`: token inválido/expirado ou autenticação incompleta.
- `403`: sem permissão/procuração/serviço não autorizado.
- `404`: endpoint ou serviço não encontrado, validar base URL e serviço.
- `500`: erro SERPRO, registrar request e tentar novamente depois.

### Mapeamento PARCSN para endpoints genéricos

Serviços de consulta, usar `POST /Consultar`:
- `PARCSN PEDIDOSPARC163`: consultar pedidos de parcelamento.
- `PARCSN OBTERPARC164`: obter detalhes de parcelamento.
- `PARCSN PARCELASPARAGERAR162`: consultar parcelas disponíveis para geração.
- `PARCSN DETPAGTOPARC165`: consultar detalhes de pagamento de parcela.

Serviço de emissão, usar `POST /Emitir`:
- `PARCSN GERARDAS161`: gerar DAS de parcela do parcelamento.

### Exemplo base para consulta PARCSN
```json
{
  "contratante": {"numero": "34191026000186", "tipo": 2},
  "autorPedidoDados": {"numero": "34191026000186", "tipo": 2},
  "contribuinte": {"numero": "34191026000186", "tipo": 2},
  "pedidoDados": {
    "idSistema": "PARCSN",
    "idServico": "PEDIDOSPARC163",
    "versaoSistema": "1.0",
    "dados": "{}"
  }
}
```

### Regras de implementação derivadas da referência
1. Criar cliente genérico com método `postar(tipo_operacao, dados_entrada)` onde `tipo_operacao` resolve para `/Consultar`, `/Emitir`, etc.
2. Nunca montar URL por serviço fiscal. O serviço vai no `pedidoDados`.
3. Validar sempre `tipo=2` para CNPJ.
4. Guardar payload e resposta com CNPJ mascarado em logs.
5. Tratar `403` como provável falta de autorização/procuração/serviço não habilitado.
6. Tratar `401` como token expirado ou fluxo de autenticação incompleto.
7. Bloquear `POST /Emitir` em produção até confirmação explícita do Hebert.

## 8. Autenticação real, Quick Start SERPRO

URL:
https://apicenter.estaleiro.serpro.gov.br/documentacao/api-integra-contador/pt/quick_start/

### Fluxo correto de autenticação
A API usa OAuth2, mas para o Integra Contador o token completo deve ser obtido no endpoint SAPI com certificado digital e-CNPJ.

Endpoint oficial:
```text
POST https://autenticacao.sapi.serpro.gov.br/authenticate
```

Headers:
```text
Authorization: Basic base64(consumerKey:consumerSecret)
Role-Type: TERCEIROS
Content-Type: application/x-www-form-urlencoded
```

Body:
```text
grant_type=client_credentials
```

Certificado:
- Obrigatório informar certificado digital e-CNPJ válido ICP-Brasil.
- Em curl, usar `--cert-type P12` e `--cert arquivo_certificado.p12:senha_certificado`.
- Certificado deve ser o mesmo utilizado na contratação do produto.

Retorno esperado:
```json
{
  "expires_in": 2008,
  "scope": "default",
  "token_type": "Bearer",
  "access_token": "...",
  "jwt_token": "..."
}
```

Uso posterior nas chamadas Integra Contador:
```text
Authorization: Bearer <access_token>
jwt_token: <jwt_token>
Content-Type: application/json
```

### Observação do teste em 2026-06-18
- Credenciais Basic recebidas do Hebert foram salvas no `.env` seguro.
- Teste simples em `https://gateway.apiserpro.serpro.gov.br/token` retornou HTTP 200 e token, mas esse endpoint não é o fluxo completo recomendado para Integra Contador, pois a documentação exige também `jwt_token` via SAPI + certificado.
- Próximo bloqueio técnico: salvar certificado A1 `.pfx/.p12` e senha no cofre local para testar `https://autenticacao.sapi.serpro.gov.br/authenticate`.
