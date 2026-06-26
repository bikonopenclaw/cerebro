# Análise retorno Cresol CNAB400 2026-06-19

Arquivo recebido: `/data/.openclaw/media/inbound/133_1008_27846_27846_20260619_27846-7.ret---f7a016ff-3fea-4976-8559-467c23e8e3d9.txt`

## Tipo de arquivo

- Tipo: retorno bancário `.ret`, não remessa `.rem`.
- Banco: Cresol `133`.
- Layout: CNAB400.
- Estrutura validada: 3 linhas de 400 posições.
- Registros: `0` header, `1` detalhe, `9` trailer.

## Header, registro 0

- Identificação: `02RETORNO`.
- Serviço: `01 COBRANCA`.
- Código empresa/conta cooperado: `00000000000000027846`.
- Empresa: `BIKON TECNOLOGIA DA INFORMACAO`.
- Banco: `133`.
- Nome banco: `CRESOL`.
- Data gravação: `20/06/2026`.
- Número aviso bancário: `01383`.
- Data crédito no header: `20/06/2026`.
- Sequencial do registro: `000001`.

## Detalhe, registro 1

- Tipo inscrição empresa: `02`, CNPJ.
- CNPJ Bikon: `34.191.026/0001-86`.
- Carteira: `009`.
- Cooperativa: `01008`.
- Conta: `0027846`.
- Dígito conta: `7`.
- Controle participante/documento: `105601`.
- Nosso número no banco: `00000001533`.
- DV nosso número: `7`.
- Ocorrência: `06`, liquidação.
- Data ocorrência: `19/06/2026`.
- Número documento: `105601`.
- Vencimento: `19/06/2026`.
- Valor do título: `R$ 2.260,00`.
- Banco cobrador: `203`.
- Agência cobradora: `07349`.
- Valor pago/creditado identificado: `R$ 2.260,00`.
- Data crédito no detalhe: `22/06/2026`.
- Sequencial do registro: `000002`.

## Trailer, registro 9

- Banco: `133`.
- Sequencial do registro: `000003`.

## O que este arquivo permite reaproveitar

- Confirmar credenciais bancárias da Bikon no retorno: carteira `009`, cooperativa `01008`, conta `0027846-7`.
- Confirmar formato do nosso número em retorno: base 11 dígitos + DV separado.
- Confirmar ocorrência `06` como liquidação.
- Confirmar que o retorno usa registros 0/1/9 com linhas de 400 posições.
- Usar como exemplo válido para parser/conciliação de retorno Cresol CNAB400.

## O que este arquivo não fecha sozinho

- Não é remessa, então não confirma todas as posições exigidas para geração de `.rem`.
- Não deve ser usado para inventar próximo nosso número, número de documento ou sequencial de remessa sem regra aprovada.
- Não substitui manual de remessa ou validação bancária em produção.
