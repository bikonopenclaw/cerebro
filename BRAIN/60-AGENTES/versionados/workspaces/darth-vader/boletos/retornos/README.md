# Retornos bancários Cresol

Pasta para exemplos e futura rotina de parser/conciliação de arquivos de retorno bancário.

## Exemplo válido disponível

- Arquivo: `exemplos/retorno-cresol-20260619.ret`
- Análise: `exemplos/analise-retorno-cresol-20260619.md`
- Banco: Cresol `133`
- Layout: CNAB400 retorno `.ret`
- Estrutura validada: 3 linhas de 400 posições, registros `0` header, `1` detalhe e `9` trailer.
- Ocorrência validada: `06` = liquidação.
- Documento: `105601`
- Nosso número em retorno: `00000001533-7`
- Valor: `R$ 2.260,00`
- Vencimento: `19/06/2026`
- Data da ocorrência: `19/06/2026`
- Data de crédito no detalhe: `22/06/2026`

## Uso permitido

Usar este arquivo como exemplo válido para:

1. parser de retorno CNAB400 Cresol;
2. conciliação de liquidação bancária;
3. validação de linhas com 400 posições;
4. mapeamento de ocorrência `06` como título liquidado;
5. testes de leitura de carteira, cooperativa, conta, documento, nosso número, vencimento, valor, data de ocorrência e data de crédito.

## Trava operacional

Este arquivo é **retorno `.ret`**, não remessa `.rem`.

Não usar este retorno para:

- gerar remessa;
- validar layout de remessa;
- inferir próximo nosso número;
- inferir número de documento;
- inferir sequencial de remessa;
- criar regra operacional para novos boletos.

Nosso número, número de documento e sequencial de remessa só podem ser gerados por regra aprovada separada.
