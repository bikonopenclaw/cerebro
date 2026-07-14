# Payload NinjaOne

## Cliente De Destino

Todos os tickets ARX Backup devem abrir no cliente interno NinjaOne `00 - Bikon Tech` (`clientId=1`).

Nunca abrir automaticamente no cliente final.

## Node

Não vincular `nodeId` do cliente final sem nova ordem explícita do Hebert.

## Formulário

Usar `ticketFormId=1`, formulário `Default`, enquanto não houver nova regra aprovada.

## Título

Usar:

`Alerta de ARX Backup - Nome do cliente`

## Corpo Mínimo

Incluir:

- cliente real ARX;
- dispositivo ARX;
- computador;
- status operacional;
- status total;
- erros totais;
- último backup válido;
- última conclusão;
- histórico `TB` dos últimos 28 dias;
- fontes com alerta/falha;
- ação sugerida;
- nota de deduplicação.

## Tags

Usar tags operacionais:

- `openclaw`
- `arx-backup`
- `backup-alerta`

## Prioridade E Severidade

- `Crítico`: `severity=CRITICAL`, `priority=HIGH`, `type=INCIDENT`.
- `Atenção`: `severity=MAJOR`, `priority=MEDIUM`, `type=TASK`.
