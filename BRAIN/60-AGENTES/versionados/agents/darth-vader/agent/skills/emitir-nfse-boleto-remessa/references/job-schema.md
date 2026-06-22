# Job JSON, emissão NFS-e + boleto + remessa

Use este schema para qualquer cliente. O exemplo abaixo é ilustrativo, não deve ser hardcoded.

```json
{
  "cliente_slug": "cliente-exemplo",
  "modo": "homologacao",
  "prestador": {
    "nome": "BIKON TECNOLOGIA DA INFORMACAO LTDA",
    "cnpj": "34.191.026/0001-86",
    "municipio": "Vitoria",
    "uf": "ES"
  },
  "tomador": {
    "nome": "CLIENTE LTDA",
    "cnpj": "00.000.000/0001-00",
    "endereco": "RUA EXEMPLO 123 CENTRO",
    "bairro": "CENTRO",
    "cep": "00000000",
    "cidade": "CIDADE",
    "uf": "UF"
  },
  "nfse": {
    "status": "rascunho_preparado",
    "numero_anterior": "opcional",
    "numero_novo": "pendente",
    "competencia": "MM/AAAA ou DD/MM/AAAA",
    "data_emissao_planejada": "DD/MM/AAAA",
    "codigo_tributacao_nacional": "010701",
    "forma_pagamento": "Boleto Cresol",
    "itens": [
      {"descricao": "SERVICO", "quantidade": 1, "valor_unitario": "100,00", "valor_total": "100,00"}
    ],
    "valor_total": "100,00"
  },
  "boleto": {
    "status": "rascunho_preparado",
    "banco": "133",
    "carteira": "009",
    "cooperativa": "01008",
    "agencia": "1008-0",
    "conta": "0027846",
    "conta_dv": "7",
    "numero_documento": "105601",
    "nosso_numero": "1533",
    "data_documento": "DD/MM/AAAA",
    "vencimento": "DD/MM/AAAA",
    "valor": "100,00",
    "juros_mora_dia_centavos": 0,
    "instrucoes": "NÃO RECEBER APÓS O VENCIMENTO."
  },
  "remessa": {
    "layout": "CNAB400",
    "seq_remessa": "0000084",
    "data_gravacao": "DD/MM/AAAA"
  },
  "email": {
    "to": ["financeiro@cliente.com"],
    "cc": [],
    "status": "rascunho_preparado",
    "aprovado_por_hebert": false
  },
  "fontes": [
    "PDF NFS-e anterior",
    "PDF boleto anterior",
    "remessa golden file"
  ]
}
```

## Regras

- `modo` deve ser `homologacao` até aprovação explícita de produção.
- `nfse.numero_novo`, `nfse.chave`, `nfse.pdf` e `nfse.xml` só entram depois de retorno real do emissor/API.
- `boleto.status` pode ser `boleto_emitido_homologacao` quando a skill gerar PDF/linha digitável/código de barras para conferência.
- `boleto_emitido` fica reservado para retorno real do banco/sistema emissor.
- `remessa.seq_remessa` deve seguir sequência real conhecida ou ser explicitamente informada.
- Não usar segunda via com multa/mora como base de cobrança nova.
- Para CNAB400 Cresol, o script atual usa conta Bikon validada: banco 133, carteira 009, cooperativa 01008, conta 27846-7. Se mudar conta, validar de novo.
- `email.to` pode ficar vazio quando o cadastro financeiro tiver e-mails do tomador. O script busca pelo CNPJ/CPF.
- `email.aprovado_por_hebert=true` só pode ser marcado depois de autorização explícita do Hebert para envio externo.
- Sem aprovação, gerar apenas `email-nfse-cliente.eml` para conferência.
