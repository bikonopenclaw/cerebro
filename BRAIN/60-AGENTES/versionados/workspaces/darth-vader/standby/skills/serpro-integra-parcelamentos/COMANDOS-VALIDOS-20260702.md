# SERPRO PARCSN, comandos válidos e sucessos confirmados

Data: 2026-07-02
Responsável operacional: Darth Vader sob coordenação do Puppet Master
Ambiente: broker local com certificado A1 no Mac do Hebert
Escopo: consultas PARCSN via SERPRO Integra Contador

## Regra de segurança

- Certificado A1 e senha ficam somente no Mac do Hebert.
- Broker local escuta somente em `127.0.0.1`.
- Não colar `access_token`, `jwt_token`, certificado, senha ou retorno fiscal bruto no chat.
- Não chamar `/Emitir` nem `GERARDAS161` sem aprovação explícita.

## Broker local

Rodar no Mac, na pasta do broker:

```bash
python3 serpro_cert_broker.py
```

Teste de saúde/token, sem imprimir token completo:

```bash
bash testar_broker_local.sh
```

Sucesso confirmado em 2026-07-02: broker gerou token localmente e permitiu chamadas SERPRO sem expor certificado.

## Consulta 1, pedidos de parcelamento

Serviço:

```text
POST /Consultar
PARCSN PEDIDOSPARC163
```

Comando válido:

```bash
bash consultar_parcsn_pedidos.sh
```

Regra de payload validada:

```json
"pedidoDados": {
  "idSistema": "PARCSN",
  "idServico": "PEDIDOSPARC163",
  "versaoSistema": "1.0",
  "dados": ""
}
```

Importante: `dados` precisa ser string vazia. Com `{}` o SERPRO retorna erro dizendo que a funcionalidade não requer informação no campo `dados`.

Resultado confirmado:

- HTTP 200.
- Parcelamento nº 1: encerrado a pedido do contribuinte.
- Parcelamento nº 2: em parcelamento.
- Pedido do parcelamento nº 2: 20/01/2026.
- Situação do parcelamento nº 2: 21/01/2026.

## Consulta 2, detalhes do parcelamento

Serviço:

```text
POST /Consultar
PARCSN OBTERPARC164
```

Comando válido:

```bash
NUMERO_PARCELAMENTO=2 bash consultar_parcsn_obter.sh
```

Regra de payload validada:

```json
"pedidoDados": {
  "idSistema": "PARCSN",
  "idServico": "OBTERPARC164",
  "versaoSistema": "1.0",
  "dados": "{\"numeroParcelamento\": 2}"
}
```

Importante: o campo correto é `numeroParcelamento`, não `numero`.

Resultado confirmado:

- HTTP 200.
- Parcelamento nº 2 em parcelamento.
- Valor total consolidado: R$ 34.622,89.
- Quantidade de parcelas: 24.
- Primeira parcela/parcela básica: R$ 1.442,62.
- Demonstrativo confirmou pagamentos de 2026-01, 2026-02 e 2026-03.

## Consulta 3, parcelas disponíveis para gerar

Serviço:

```text
POST /Consultar
PARCSN PARCELASPARAGERAR162
```

Comando válido:

```bash
bash consultar_parcsn_parcelas.sh
```

Regra de payload validada:

```json
"pedidoDados": {
  "idSistema": "PARCSN",
  "idServico": "PARCELASPARAGERAR162",
  "versaoSistema": "1.0",
  "dados": ""
}
```

Importante: este serviço também usa `dados` como string vazia. Enviar `numeroParcelamento` retorna erro `ER_N007`.

Resultado confirmado:

- HTTP 200.
- Parcelas disponíveis em 2026-07-02:
  - 202604, R$ 1.536,24
  - 202605, R$ 1.536,24
  - 202606, R$ 1.536,24

## Informação operacional do Hebert

Hebert informou em 2026-07-02 que essas três parcelas já foram pagas:

- 202604, R$ 1.536,24
- 202605, R$ 1.536,24
- 202606, R$ 1.536,24

Expectativa: baixa/atualização no SERPRO até 03/07/2026.

Próxima ação recomendada: em 03/07/2026, consultar novamente `PARCELASPARAGERAR162` e/ou `OBTERPARC164` para confirmar se as parcelas saíram da lista de disponíveis ou apareceram no demonstrativo de pagamentos.

## Próximo serviço possível, ainda consulta

Antes de qualquer emissão real, se necessário validar baixa/pagamento, usar:

```text
POST /Consultar
PARCSN DETPAGTOPARC165
```

Ainda não validado nesta rodada.

## Emissão bloqueada

Serviço de emissão:

```text
POST /Emitir
PARCSN GERARDAS161
```

Status: bloqueado.

Só pode ser chamado com aprovação explícita citando parcelamento, parcela e valor, conforme `FLUXO-APROVACAO-GERARDAS161.md`.
