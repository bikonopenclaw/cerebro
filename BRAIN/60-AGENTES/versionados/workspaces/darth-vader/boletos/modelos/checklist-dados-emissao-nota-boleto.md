# Checklist padrão, emissão de NFS-e + boleto Cresol

Status: rascunho para validação do Hebert
Uso: padrão mínimo de dados para o Darth Vader aceitar pedidos de emissão.

## Regra geral de bloqueio

Sem os campos obrigatórios abaixo, o agente deve parar e pedir complemento.

Não emitir nota, boleto, registrar cobrança, gerar remessa definitiva ou enviar arquivo ao banco sem aprovação explícita.

---

# 1. Dados do cliente/tomador, obrigatórios

- Razão social ou nome completo
- CPF ou CNPJ
- Inscrição municipal, se aplicável
- Inscrição estadual, se aplicável
- E-mail financeiro do cliente
- Telefone, se disponível
- Endereço completo:
  - Logradouro
  - Número
  - Complemento, se houver
  - Bairro
  - Cidade
  - UF
  - CEP

## Validações

- CPF/CNPJ com dígito válido
- CEP com 8 dígitos
- UF com 2 letras
- E-mail em formato válido
- Cidade compatível com UF quando possível

---

# 2. Dados da nota fiscal de serviço, obrigatórios

- Cliente/tomador
- Data de emissão desejada
- Competência, mês/ano do serviço
- Descrição do serviço
- Valor total da nota
- Município de prestação do serviço
- Código de serviço municipal ou item da lista de serviço
- Alíquota de ISS, se aplicável
- Retenções, quando houver:
  - ISS retido
  - INSS
  - IRRF
  - CSLL
  - PIS
  - COFINS
- Condição de pagamento
- Observações adicionais da nota, se houver

## Validações

- Valor maior que zero
- Competência informada
- Descrição clara e compatível com serviço prestado
- Código de serviço informado antes de emissão real
- Retenções explicitamente marcadas como `sim`, `não` ou `não se aplica`

## Campo de segurança

Antes de emitir NFS-e real, exigir confirmação:

`CONFIRMO EMISSÃO DA NOTA`

---

# 3. Dados do boleto Cresol, obrigatórios

- Cliente/pagador
- Número do documento, preferencialmente número da nota ou referência interna
- Valor do boleto
- Data de vencimento
- Data de emissão
- Nosso número ou autorização para gerar próximo nosso número
- Carteira Cresol
- Cooperativa
- Conta corrente com dígito
- Espécie do título
- Aceite, normalmente branco/não
- Ocorrência CNAB, normalmente `01` para entrada/remessa
- Condição de emissão da papeleta, normalmente `2`, cliente emite e banco processa
- Multa:
  - Tem multa? sim/não
  - Percentual de multa
- Juros/mora:
  - Tem juros? sim/não
  - Percentual mensal ou valor diário
- Desconto, se houver:
  - Data limite
  - Valor
- Abatimento, se houver
- Instrução de protesto/baixa, se houver

## Validações

- Valor maior que zero
- Vencimento em data futura ou explicitamente autorizado se vencido
- CPF/CNPJ do pagador válido
- CEP do pagador válido
- Nosso número com 11 dígitos e DV validado, ou gerar DV pela regra Cresol
- Campo beneficiário CNAB400 = zero + carteira + cooperativa + conta + DV
- Juros/mora calculado em centavos conforme regra definida
- Multa `0200` para 2,00%, se aplicável
- Desconto, IOF e abatimento zerados quando não houver

## Campo de segurança

Antes de gerar boleto/remessa real, exigir confirmação:

`CONFIRMO GERAÇÃO DO BOLETO/REMESSA`

---

# 4. Dados da remessa CNAB400 Cresol, obrigatórios

- Sequencial da remessa
- Data de gravação do arquivo
- Lista de boletos/títulos incluídos
- Quantidade total de títulos
- Valor total dos títulos
- Nome do arquivo `.rem`
- Modo do arquivo:
  - rascunho
  - homologação
  - produção

## Validações CNAB400

- Cada linha com 400 caracteres
- Header tipo `0`
- Detalhes tipo `1`
- Trailer tipo `9`
- Sequencial de registro correto:
  - Header `000001`
  - Primeiro detalhe `000002`
  - Trailer = quantidade total de linhas
- Pelo menos 1 detalhe
- Banco `133`
- Literal `REMESSA`
- Serviço `COBRANCA`
- Ocorrência `01` para entrada normal
- Comparar campos fixos com golden files:
  - `cb010601.rem`
  - `cb110501.rem`

## Campo de segurança

Antes de enviar ao portal do banco, exigir confirmação:

`CONFIRMO ENVIO AO PORTAL CRESOL`

---

# 5. Formato padrão aceito para pedido de emissão

```yaml
cliente:
  razao_social: ""
  cpf_cnpj: ""
  email: ""
  telefone: ""
  endereco:
    logradouro: ""
    numero: ""
    complemento: ""
    bairro: ""
    cidade: ""
    uf: ""
    cep: ""

nota:
  emitir: true
  data_emissao: "DD/MM/AAAA"
  competencia: "MM/AAAA"
  descricao_servico: ""
  municipio_prestacao: ""
  codigo_servico: ""
  valor_total: 0.00
  iss_retido: "sim|não|não se aplica"
  retencoes:
    inss: 0.00
    irrf: 0.00
    csll: 0.00
    pis: 0.00
    cofins: 0.00
  observacoes: ""

boleto:
  gerar: true
  numero_documento: ""
  valor: 0.00
  data_emissao: "DD/MM/AAAA"
  vencimento: "DD/MM/AAAA"
  nosso_numero: "gerar|informar número"
  carteira: "009"
  cooperativa: "01008"
  conta: "0027846"
  conta_dv: "7"
  especie: "02"
  aceite: ""
  ocorrencia: "01"
  condicao_emissao_papeleta: "2"
  multa_percentual: 2.00
  juros_percentual_mes: 1.00
  desconto:
    data_limite: ""
    valor: 0.00
  abatimento: 0.00
  protesto_instrucao: ""

remessa:
  gerar: true
  modo: "rascunho|homologação|produção"
  sequencial_remessa: ""
  nome_arquivo: ""
```

---

# 6. Decisão de fluxo

## Pode avançar para rascunho

- Todos os campos obrigatórios preenchidos
- Dados passaram nas validações locais
- Modo marcado como `rascunho` ou `homologação`

## Não pode avançar

- CPF/CNPJ inválido
- Endereço incompleto
- Valor zerado ou negativo
- Vencimento ausente
- Retenções da nota não informadas
- Nosso número ausente sem autorização para gerar
- Sequencial de remessa ausente
- Pedido sem confirmação explícita para emissão real

## Pode gerar arquivo para validação no portal

Somente se:

- Modo = `homologação`
- Remessa validada localmente
- Conferida contra golden files
- Hebert confirmar envio/teste no portal

---

# 7. Pendências para tornar obrigatório na skill

- Hebert validar este checklist
- Definir se NFS-e será emitida por sistema/API específico ou apenas preparada
- Definir padrão de descrição dos serviços Bikon
- Definir regra oficial de juros/mora mensal
- Definir origem e controle do próximo nosso número
- Definir se sequencial de remessa será manual ou controlado em arquivo local
