# Modelo padrão boleto Cresol Bikon

Aprovado por Hebert em 2026-06-17.

Arquivos padrão:
- `modelo-padrao-boleto-cresol-oficial.fr3.xml`: layout oficial Cresol/FastReport.
- `gerar_boleto_cresol_html.aprovado-20260617.py`: gerador aprovado renderizando o XML por coordenadas absolutas.
- `modelo-padrao-boleto-cresol-vazio-aprovado.pdf`: PDF vazio de validação aprovado.

Regra:
- Usar este layout como padrão para boletos Cresol da Bikon.
- Código de barras aprovado com escala final: `barHeight=23.4mm`, `barWidth=0.624mm`, renderizado em `494px x 68px`.
- Não reduzir escala do código de barras nem voltar ao layout genérico sem aprovação explícita do Hebert.

Marcador: BIKON_APPROVED_CRESOL_BOLETO_LAYOUT_OFICIAL_20260617
