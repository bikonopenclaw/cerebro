# Banco de faturamento e conciliação bancária

## Objetivo

Manter um banco local auditável com NFS-e, boletos, remessas e retornos bancários para gerar relatórios e controlar pagamentos.

Banco padrão:

```text
/data/.openclaw/workspace-darth-vader/boletos/db/faturamento.db
```

Script:

```text
/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/scripts/faturamento_db.py
```

## Regra operacional

- O banco é controle interno Bikon.
- Registrar pacote local não significa que NFS-e, boleto ou remessa foram emitidos em produção.
- Baixa por retorno bancário atualiza o **controle interno** do boleto.
- Nunca alterar banco, remessa, NFS-e, boleto ou envio externo sem aprovação explícita do Hebert quando isso mudar estado real fora do controle local.
- Importar retorno recebido do banco é permitido quando Hebert envia o arquivo para conciliação.

## Comandos

Inicializar banco:

```bash
python3 scripts/faturamento_db.py init
```

Registrar um pacote de emissão no banco:

```bash
python3 scripts/faturamento_db.py registrar-pacote --pacote /caminho/do/pacote
```

Sincronizar todos os pacotes existentes:

```bash
python3 scripts/faturamento_db.py sincronizar-pacotes
```

Importar retorno CNAB400 Cresol:

```bash
python3 scripts/faturamento_db.py importar-retorno --arquivo /caminho/arquivo.ret
```

Gerar relatório em Markdown:

```bash
python3 scripts/faturamento_db.py relatorio --output /data/.openclaw/workspace-darth-vader/boletos/relatorios/faturamento.md
```

Gerar relatório CSV:

```bash
python3 scripts/faturamento_db.py relatorio --formato csv --output /data/.openclaw/workspace-darth-vader/boletos/relatorios/faturamento.csv
```

## Tabelas principais

- `clientes`: tomadores/pagadores.
- `nfse`: notas fiscais de serviço emitidas, rascunhadas ou importadas dos pacotes.
- `boletos`: boletos gerados/registrados no controle, com valor original e campos de pagamento.
- `remessas`: arquivos de remessa gerados.
- `remessa_boletos`: vínculo entre remessa e boleto.
- `retornos`: arquivos de retorno importados.
- `retorno_ocorrencias`: cada ocorrência/título dentro do retorno.

## Campos financeiros importantes do boleto

O boleto preserva o valor original e separa o que voltou no banco:

- `valor_original_centavos`: valor emitido/cobrado originalmente.
- `valor_pago_centavos`: valor efetivamente pago no retorno.
- `juros_mora_centavos`: juros/mora retornados pelo banco.
- `tarifa_centavos`: tarifa/custa bancária.
- `desconto_centavos`: desconto concedido.
- `abatimento_centavos`: abatimento concedido.
- `outras_despesas_centavos`: despesas adicionais.
- `outros_creditos_centavos`: créditos adicionais.
- `data_pagamento`: data da ocorrência/liquidação.
- `data_credito`: data de crédito informada pelo retorno.

Isso permite consultar pagamentos acima ou abaixo do valor original sem destruir o histórico da cobrança.

## Retorno CNAB400 Cresol

Parser inicial usa layout de retorno CNAB400 Cresol 133 já mapeado em:

```text
/data/.openclaw/workspace-darth-vader/boletos/manual-cresol/mapa-retorno-cnab400-cresol-133.json
```

Ocorrências que baixam pagamento:

- `06`: Liquidação.
- `17`: Liquidação após baixa ou liquidação de título não registrado.

Ocorrências que alteram status sem pagamento:

- `03`: Entrada rejeitada.
- `09`: Baixa.
- `26`: Instrução rejeitada.

## Conciliação

A conciliação tenta localizar boleto por:

1. `nosso_numero` do retorno.
2. `numero_documento`, se `nosso_numero` não localizar.

Se encontrar boleto e a ocorrência for pagamento, atualiza:

- `status='pago'`
- `valor_pago_centavos`
- juros/mora
- tarifa
- desconto
- abatimento
- data de pagamento
- data de crédito

Se não encontrar, registra ocorrência em `retorno_ocorrencias` com `conciliado=0` e observação `Boleto não encontrado no banco local`.

## Relatórios esperados

O relatório deve permitir responder:

- Quais NFS-e foram emitidas no período.
- Quais boletos existem e seu status.
- Quais remessas levaram quais boletos.
- Quais boletos foram pagos.
- Quais pagamentos vieram com juros/mora/multa ou valor diferente do original.
- Quais ocorrências de retorno não conciliam com boletos registrados.

## Integração com pacote de emissão

`preparar_pacote_emissao.py` registra automaticamente o pacote no banco ao final do fluxo, quando `faturamento_db.py` existir.

Se o pacote tiver NFS-e, boleto ou remessa real/homologação, o registro é feito com status coerente com os metadados disponíveis. O status fiscal/bancário real depende de comprovante e validações externas.
