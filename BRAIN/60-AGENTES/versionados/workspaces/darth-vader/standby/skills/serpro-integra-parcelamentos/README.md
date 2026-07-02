# Skill futura — SERPRO Integra Contador / Integra Parcelamentos

## Objetivo
Automatizar controle, consulta e geração assistida de guias de parcelamento do Simples Nacional para a Bikon, usando a API oficial SERPRO Integra Contador, módulo Integra Parcelamentos.

Escopo inicial: **PARCSN — Parcelamento do Simples Nacional comum**.


## Dados confirmados até agora

- Integra Contador: **ainda não contratado**.
- Certificado digital disponível: **A1**.
- Escopo inicial: **somente Bikon**.
- CNPJ inicial: **34.191.026/0001-86**.
- Hebert informou que é **controlador do CNPJ**.
- Geração automática de DAS: **desativada** até validação completa.
- Qualquer geração real de guia exige **confirmação explícita antes da chamada ao `GERARDAS161`**.

Fora de escopo nesta fase:
- contratação automática do SERPRO;
- acesso ao e-CAC;
- emissão real de guias sem aprovação;
- uso de credenciais/certificados sem autorização explícita;
- PGDAS-D mensal, salvo integração futura.

## Dependências que precisam do Hebert

1. Contratação SERPRO
- Status atual: **não contratado**.
- Hebert precisa contratar o produto **Integra Contador**.
- Confirmar habilitação do módulo **Integra Parcelamentos**.
- Obter dados de acesso/API: client id, client secret, consumer key/secret ou equivalente conforme contrato SERPRO.
- Confirmar ambiente disponível: homologação e/ou produção.

2. Certificado digital
- Confirmado: certificado digital **A1**.
- Guardar o A1 em cofre/secret manager; senha fora do código e fora do repositório.
- Não copiar certificado para workspace sem autorização explícita do Hebert.

3. Procuração e-CAC
- Cada empresa consultada/gerenciada precisa conceder procuração eletrônica no e-CAC para a Bikon/contador autorizado.
- A procuração precisa cobrir serviços relacionados a Simples Nacional / parcelamentos / geração de DAS, conforme exigência da Receita/SERPRO.
- Sem procuração, a API pode autenticar mas negar dados do contribuinte.

4. Dados das empresas
- Escopo inicial confirmado: **Bikon — CNPJ 34.191.026/0001-86**.
- Controlador informado: **Hebert**.
- Razão social / nome fantasia precisa ser confirmada no cadastro final, sem consulta externa nesta etapa.
- Responsável interno.
- Regime: Simples Nacional.
- Situação atual do parcelamento, se conhecida.
- Dia preferido para rotina mensal.
- Canal de aviso ao cliente/responsável.

## Fluxo técnico de autenticação

Fluxo previsto, a validar na documentação contratada do SERPRO:

1. Assinar/autenticar requisição usando credenciais da aplicação SERPRO.
2. Usar certificado digital para representar o procurador/contribuinte autorizado.
3. Obter token OAuth/JWT de acesso.
4. Enviar chamadas à API com:
   - token bearer;
   - headers exigidos pelo SERPRO;
   - identificação do contribuinte alvo, quando aplicável;
   - certificado/assinatura quando exigido.
5. Renovar token antes de expirar.
6. Registrar logs sem vazar segredo, certificado, token ou dados sensíveis.

## Serviços PARCSN mapeados

### GERARDAS161
Geração de DAS de parcela do parcelamento.

Uso provável:
- gerar guia/parcela do mês;
- obter código de barras/linha digitável/PDF se retornado pela API;
- registrar vencimento e valor.

### PARCELASPARAGERAR162
Consulta de parcelas disponíveis para geração.

Uso provável:
- rotina mensal;
- descobrir quais parcelas estão abertas;
- evitar gerar guia duplicada.

### PEDIDOSPARC163
Consulta/listagem de pedidos de parcelamento.

Uso provável:
- identificar parcelamento ativo;
- guardar número do pedido;
- acompanhar status.

### OBTERPARC164
Obter detalhes de um parcelamento.

Uso provável:
- detalhar quantidade de parcelas;
- situação do parcelamento;
- valores e datas.

### DETPAGTOPARC165
Detalhamento de pagamento do parcelamento.

Uso provável:
- conciliar parcela paga;
- atualizar status local;
- alimentar relatório financeiro.

## Dados mínimos por empresa

```json
{
  "cnpj": "34191026000186",
  "razao_social": "BIKON TECNOLOGIA DA INFORMACAO LTDA ME",
  "responsavel": "Hebert",
  "tem_procuracao_ecac": false,
  "procuracao_validade": null,
  "parcelamento": {
    "tipo": "PARCSN",
    "numero_pedido": null,
    "status": "desconhecido"
  },
  "rotina": {
    "dia_consulta_mensal": 5,
    "gerar_guia_automaticamente": false,
    "exige_confirmacao_antes_de_gerar": true
  }
}
```

## Modelo de armazenamento

Sugestão inicial em Postgres ou SQLite local enquanto protótipo.

### Tabela `empresas`
- id
- cnpj
- razao_social
- responsavel
- ativo
- tem_procuracao_ecac
- procuracao_validade
- created_at
- updated_at

### Tabela `parcelamentos`
- id
- empresa_id
- tipo: PARCSN
- numero_pedido
- status
- data_adesao
- quantidade_parcelas
- fonte_ultima_consulta
- raw_response_json criptografado/opcional
- created_at
- updated_at

### Tabela `parcelas`
- id
- parcelamento_id
- numero_parcela
- competencia
- vencimento
- valor_principal
- multa
- juros
- valor_total
- status: disponivel, gerada, paga, vencida, erro
- codigo_receita/opcional
- linha_digitavel/opcional criptografada
- codigo_barras/opcional criptografado
- pdf_path/opcional
- xml_json_path/opcional
- serpro_request_id/opcional
- created_at
- updated_at

### Tabela `eventos`
- id
- empresa_id
- parcelamento_id
- parcela_id
- tipo_evento
- mensagem
- payload_resumido
- created_at

## Rotina mensal sugerida

1. Rodar consulta mensal por empresa ativa.
2. Verificar procuração válida e credenciais disponíveis.
3. Consultar pedidos com `PEDIDOSPARC163`.
4. Para parcelamento ativo, consultar detalhes com `OBTERPARC164`.
5. Consultar parcelas disponíveis com `PARCELASPARAGERAR162`.
6. Comparar com banco local para evitar duplicidade.
7. Se houver parcela disponível:
   - registrar status `disponivel`;
   - alertar responsável;
   - só gerar DAS com `GERARDAS161` mediante regra configurada ou confirmação explícita.
8. Após geração, salvar vencimento, valor, identificadores e arquivo retornado.
9. Consultar pagamentos com `DETPAGTOPARC165` para conciliação.
10. Gerar relatório mensal: aberto, gerado, pago, vencido, erro.

## Segurança e guardrails

- Nunca salvar certificado A1 em texto puro.
- Nunca versionar `.env`, certificado, senha, token ou retorno fiscal completo com dados sensíveis.
- Usar cofre/secret manager quando disponível.
- Separar ambiente homologação e produção.
- Produção exige confirmação explícita para geração real de guia até o fluxo estar auditado.
- Idempotência obrigatória: antes de gerar, consultar se a parcela já foi gerada.
- Logar request id, horário, serviço chamado e CNPJ mascarado.
- Mascarar CNPJ/CPF em logs externos.
- Controle de permissões: só agente financeiro autorizado pode gerar guia.
- Backups criptografados para banco local.
- Alertas para vencimento próximo e falhas de API.

## Estrutura futura da skill

```text
serpro-integra-parcelamentos/
├── README.md
├── config.example.json
├── core/
│   ├── auth.py
│   ├── client.py
│   ├── parcsn.py
│   └── storage.py
├── scripts/
│   ├── setup.py
│   ├── consultar_parcelamentos.py
│   ├── gerar_das_parcela.py
│   └── rotina_mensal.py
├── data/
│   └── .gitkeep
└── tests/
    └── fixtures/
```

## Checklist próximo — contratação/habilitação SERPRO

Nada abaixo deve ser executado pelo agente sem ordem explícita. É checklist para o Hebert/Bikon.

1. Contratar o produto **SERPRO Integra Contador**.
2. Confirmar que o módulo **Integra Parcelamentos** está habilitado no contrato.
3. Confirmar acesso aos serviços **PARCSN**:
   - `GERARDAS161`;
   - `PARCELASPARAGERAR162`;
   - `PEDIDOSPARC163`;
   - `OBTERPARC164`;
   - `DETPAGTOPARC165`.
4. Solicitar/obter credenciais da aplicação SERPRO, sem enviar por chat aberto:
   - client id / consumer key;
   - client secret / consumer secret;
   - URLs de homologação e produção;
   - escopos autorizados.
5. Validar certificado **A1** que será usado:
   - titular;
   - validade;
   - senha armazenada em cofre;
   - permissão para uso automatizado.
6. Conferir se o CNPJ **34.191.026/0001-86** possui poderes/procurações necessárias no e-CAC para os serviços de parcelamento do Simples.
7. Definir ambiente inicial: recomendação é começar por **homologação**, se disponível.
8. Definir política operacional:
   - consulta automática mensal permitida;
   - geração automática desativada;
   - geração de DAS somente com confirmação explícita do Hebert.
9. Depois disso, criar `.env`/secret store real a partir de `config.example.json`, sem versionar segredo.

## Próximo passo técnico

Com SERPRO contratado e credenciais separadas em cofre, implementar primeiro só consulta:
1. autenticação;
2. `PEDIDOSPARC163`;
3. `OBTERPARC164`;
4. `PARCELASPARAGERAR162`;
5. persistência local;
6. relatório de conferência.

Só depois liberar `GERARDAS161`, ainda com confirmação manual obrigatória.
