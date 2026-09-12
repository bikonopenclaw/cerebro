# Leitura read-only deve provar nao mutacao

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W32 e qualificacao R4 do verificador de midia em 2026-09-11
confiabilidade: alta
ultima_revisao: 2026-09-12
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
- Quando a leitura depende de rede, limitar o worker por identidade, capacidades, `NoNewPrivs`, hostname, porta, metodo e TTL; registrar separadamente requests de leitura e mutacoes do provedor.
- Escrita local de evidencia ou verdict pode ser autorizada sem converter a operacao externa em mutativa, desde que seu escopo seja explicito e os contadores provem zero mutacao no sistema consultado.
- Exigir autorizacao propria para rollback, limpeza, correcao ou retry.

## Exemplo conectado

Na aceitacao operacional do CNS `023689`, a validacao da rota controle CNS `024067` alterou `dashboard-state-v1.json`. Isso invalidou a aceitacao como `FAIL_CLOSED`, apesar de os dados do CNS `023689` estarem commitados corretamente.

Na qualificacao R4 da midia Bikon publicada em 2026-09-10, o verificador protegido recebeu grant de 120 segundos restrito ao CDN exato, operou com capacidades zeradas e `NoNewPrivs=1`, recuperou um unico corpo de imagem e registrou `BYTES_VERIFIED/corresponds=true`. Os contadores separaram a evidencia local permitida de `instagram_mutations=0`.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausencia de evidencia nao e status operacional]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[01-DIARIO/Semanal/2026-W32|Semana 2026-W32]]
- [[01-DIARIO/2026/2026-09-12|Diario 2026-09-12]]
