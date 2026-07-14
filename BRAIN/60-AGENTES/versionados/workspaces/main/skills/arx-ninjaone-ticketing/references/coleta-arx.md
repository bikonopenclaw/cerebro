# Coleta ARX

## Fonte

Usar a integração JSON-RPC Cove/ARX Backup já validada pelo workspace ARX.

## Campos usados na decisão

- `T0`: status total atual.
- `T7`: erros totais atuais.
- `TL`: último backup válido.
- `TO`: última conclusão.
- `TB`: histórico total dos últimos 28 dias.
- `FB`, `SB`, `QB`, `HB`, `WB`: histórico por fonte.
- Status por fonte: código atual de cada fonte protegida.
- Erros por fonte: contador atual por fonte.

## Separação crítica

Dado atual decide ticket. Histórico decide relatório e contexto.

Falha histórica em `TB`, `FB`, `SB`, `QB`, `HB` ou `WB` não abre ticket sozinha quando o status atual voltou para `Concluído (5)`.

## Saídas úteis

- Cliente ARX.
- Dispositivo ARX.
- Nome da máquina.
- Status operacional.
- Fonte afetada.
- Último sucesso.
- Última conclusão.
- Histórico 28 dias.
