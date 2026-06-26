# Boletos e malote bancário

Backup e documentação da futura habilidade do Darth Vader para gerar remessa/malote bancário de boletos da Bikon.

Espelho operacional:
`/data/.openclaw/workspace-darth-vader/boletos`

## Estado em 2026-06-26

- Banco identificado nos modelos: Cresol, código 133.
- Há modelo de boleto e template CSV em `modelos/`.
- Há exemplos de remessa em `remessas/exemplos/`.
- A remessa `exemplo-malote-20260614-015740.rem` funciona como referência positiva inicial: header tipo `0`, detalhe tipo `1` e trailer tipo `9`.
- A remessa `exemplo-malote-20260614-0223-133_CNAB400_1008_27846.rem` funciona como referência negativa: possui duas linhas tipo `0`, não possui detalhe nem trailer e deve ser rejeitada por validações futuras.
- Há documentação sanitizada de retorno Cresol CNAB400 em `boletos/retornos/`, sincronizada no snapshot versionado da Darth Vader sem o arquivo `.ret` bruto.
- O retorno analisado confirma estrutura de 3 linhas de 400 posições, registros `0/1/9` e ocorrência `06` como liquidação, servindo apenas para parser/conciliação.

## Pendências antes de uso real

Confirmar com o banco/contrato:

1. layout oficial CNAB 240 ou CNAB 400;
2. convênio/código beneficiário definitivo;
3. regra do nosso número;
4. sequencial da remessa;
5. carteira/modalidade;
6. instruções aceitas pelo banco;
7. validação homologada antes de qualquer envio operacional.

## Guardrail

Não usar os modelos para envio bancário real até concluir homologação com a Cresol e validar os campos obrigatórios do layout oficial.

Retorno `.ret` é referência de conciliação/liquidação, não de geração de remessa `.rem`; não usar retorno para inferir próximo nosso número, número de documento, sequencial de remessa ou regras de emissão.
