# Modelo de boleto e base para malote bancário

Criado a partir do arquivo `exemplo-boleto-20260614-014941.pdf`.

Banco identificado: Cresol, código 133.

Arquivos:
- `modelo-boleto-cresol.json`: estrutura completa com campos extraídos e campos necessários para remessa.
- `template-boletos-cresol.csv`: planilha-base para cadastrar títulos futuros.

Atenção:
Este modelo ainda NÃO gera CNAB. Para gerar malote/remessa, falta confirmar com o banco:
1. layout CNAB 240 ou CNAB 400,
2. convênio/código beneficiário definitivo,
3. regra do nosso número,
4. sequencial da remessa,
5. carteira/modalidade,
6. instruções aceitas pelo banco.
