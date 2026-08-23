# Producao parcial por dominio nao herda autorizacao

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W34
confiabilidade: alta
ultima_revisao: 2026-08-23
tags: [producao, dominios, approval, rse, escopo, fail-closed]
```

## Principio

Um sistema pode estar em `PRODUCTION` para um dominio especifico sem estar autorizado para todos os dominios tecnicamente disponiveis no mesmo runtime.

Producao parcial precisa declarar o dominio habilitado, os dominios explicitamente excluidos e os gates necessarios para ampliar escopo.

## Aplicacao pratica

- Registrar o dominio produtivo junto do status, nao separado dele.
- Separar leitura, admissao, fila, recuperacao, restart, memoria, banco, terminacao ativa, gateway e adapters.
- Tratar novas superficies live como nova autorizacao, mesmo quando compartilham runtime, servico ou evidencia tecnica.
- Bloquear inferencia de permissao por nomenclatura ampla como `PRODUCTION`, `LIVE`, `PASS` ou `ACCEPTED`.
- Exigir approval, rollback e evidencia propria antes de ampliar dominio mutativo.

## Exemplo conectado

Em 2026-W34, [[50-PROJETOS/Em-Andamento/OpenClaw-RSE|OpenClaw RSE]] foi registrado em producao para `EXECUTION_TREE_RECOVERY` e governanca de capacidade/admissao. Esse estado nao autorizou memoria, restart, SQLite, terminacao ativa, gateway restart, reboot nem adapters adicionais.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente|Capacidade tecnica nao substitui evidencia de ambiente]]
- [[01-DIARIO/Semanal/2026-W34|Semana 2026-W34]]
