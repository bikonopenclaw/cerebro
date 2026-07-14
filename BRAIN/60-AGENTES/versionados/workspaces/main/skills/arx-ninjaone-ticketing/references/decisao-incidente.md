# Decisão De Incidente

## Abrir Ticket

Abrir ticket somente quando a checagem atual indicar problema real:

- status total atual com severidade `Atenção` ou `Crítico`, exceto `Concluído (5)`;
- erro total atual `T7` maior que zero quando o status atual não for `Concluído (5)`;
- fonte atual com status problemático, como `Falhou`, `Abortado`, `Interrompido`, `Concluído com erros`, `Em progresso com falhas` ou `Acima da cota`;
- erro atual em fonte cujo último status não seja `Concluído (5)`.

## Não Abrir Ticket

Não abrir ticket quando:

- o status atual for `Concluído (5)`;
- houver somente falha histórica em `TB`, `FB`, `SB`, `QB`, `HB` ou `WB`;
- o problema já estiver ativo e deduplicado no estado local;
- faltar evidência atual confiável.

## Severidade

- `Crítico`: falha atual, abortado, interrompido, acima da cota, em progresso com falha, erro total atual relevante.
- `Atenção`: alerta atual ou falha pontual que ainda exige acompanhamento.

## Regra Anti-Falso Positivo

Se houve falha anterior, mas a checagem atual mostra `Concluído (5)`, considerar recuperado. O histórico pode aparecer no relatório técnico, mas não deve virar chamado operacional.
