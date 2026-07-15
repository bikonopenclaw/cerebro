# Checklist de validação

## Antes de emitir NFS-e

- Confirmar tomador, CNPJ e endereço.
- Confirmar competência e data de emissão.
- Confirmar itens e valores.
- Confirmar código de tributação e município de incidência.
- Confirmar se há retenção de ISSQN ou tributos federais.
- Confirmar forma de pagamento.

## Antes de emitir boleto

- Usar valor original da nova NFS-e, não valor atualizado de segunda via.
- Confirmar vencimento.
- Confirmar documento e nosso número.
- Calcular DV do nosso número.
- Confirmar multa/mora/instruções.

## Antes de gerar remessa

- Confirmar layout CNAB400 ou CNAB240.
- Confirmar sequencial de remessa.
- Validar 400 caracteres por linha para CNAB400.
- Validar header `0`, detalhe `1`, trailer `9`.
- Comparar com golden file real quando possível.

## Entrega

Nunca dizer “emitido” se está apenas rascunhado.
Use:

- “NFS-e: rascunho preparado, emissão real pendente.”
- “Boleto: rascunho preparado, PDF/registro real pendente.”
- “Remessa: gerada para homologação.”
