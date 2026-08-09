# Leitura read-only deve provar nao mutacao

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W32
confiabilidade: alta
ultima_revisao: 2026-08-09
tags: [read-only, validacao, side-effect, dashboard, fail-closed]
```

## Principio

Validacao read-only so e aceitavel quando a leitura tambem prova ausencia de mutacao persistida.

`GET`, consulta, dashboard, exportacao ou readback nao devem ser aceitos como leitura pura se alterarem arquivo de estado, cache canonico, journal, contador, token, lock ou qualquer artefato persistido fora do escopo autorizado.

## Aplicacao pratica

- Medir hashes antes e depois das rotas de comparacao.
- Incluir controle negativo: uma rota conhecida deve permanecer byte-identica quando usada apenas para validar outra.
- Tratar side effect em leitura como falha de aceitacao, mesmo quando o alvo principal parece correto.
- Separar cache derivado descartavel de estado canonico persistido; se nao houver separacao clara, falhar fechado.
- Exigir autorizacao propria para rollback, limpeza, correcao ou retry.

## Exemplo conectado

Na aceitacao operacional do CNS `023689`, a validacao da rota controle CNS `024067` alterou `dashboard-state-v1.json`. Isso invalidou a aceitacao como `FAIL_CLOSED`, apesar de os dados do CNS `023689` estarem commitados corretamente.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausencia de evidencia nao e status operacional]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[01-DIARIO/Semanal/2026-W32|Semana 2026-W32]]
