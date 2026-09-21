---
id: brain-da0559fd8fa57b85e42a
type: knowledge
title: Leitura read-only deve provar nao mutacao
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T18:55:38.578515Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md
  reason: 'A restrição de capacidades deve ser acompanhada de prova dos efeitos observados: uma credencial ampla envolvida por um cliente read-only não demonstra menor privilégio.'
  source: git:2e5f3ed0e3bfcc873f2044df1a3fe80e3097be97:BRAIN/40-CONHECIMENTO/Operacional/Leitura-read-only-deve-provar-nao-mutacao.md; BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md
---

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

## Conexão revisada em 2026-09-21

[[40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento|Menor privilegio em monitoramento]]: A restrição de capacidades deve ser acompanhada de prova dos efeitos observados: uma credencial ampla envolvida por um cliente read-only não demonstra menor privilégio.

## Conhecimento recuperado dos históricos — revisão 2026-09-21

No caso histórico NinjaOne de 06/07/2026, o usuário pediu retirar o retorno de JSON completo do script. A proposta seguinte separou remover a produção/gravação desse payload de apagar o custom field já existente no provider. Ajustar saída local não comprova nem autoriza excluir estrutura remota; o escopo da alteração deve ser explícito e o efeito verificado separadamente. Fonte: unidades 34591.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.
