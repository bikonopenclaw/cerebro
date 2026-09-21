---
categoria: operacional
fonte: consolidacao diaria 2026-08-13, a partir do gate Provimento 213 false 100% KPI de 2026-08-12
confiabilidade: alta
ultima_revisao: 2026-08-13
tags:
- metricas
- kpi
- relatorios
- provimento-213
- qualidade
- semantica
updated: '2026-09-21T19:50:50.519705Z'
id: brain-753db6fa62413010ae52
type: knowledge
title: Contagem não é percentual de conclusão
created: '2026-09-21T19:46:23.314357Z'
created_semantics: Data de registro estruturado; data de origem permanece em ultima_revisao legado.
schema_version: '1.0'
legacy_content_preserved: true
relationships: []
---

# Contagem nao e percentual de conclusao

## Principio

Uma contagem simples nao deve ser convertida em percentual de conclusao sem denominador canonico e significado operacional provado.

## Regra

- `47/47` pode significar cobertura de entrevista quando o universo da entrevista esta definido.
- `69 evidencias`, `18 registros de conformidade` ou `4 adequacoes` sao contagens, nao provas automaticas de 100%.
- Contagem sem denominador semantico deve ser renderizada como contagem, inventario ou item em reconciliacao.
- Denominador ausente nao pode ser inventado a partir da propria contagem.
- Quando houver conflito de versao do universo, como `47` controles atuais versus `48` historicos, o conflito deve ser preservado e rotulado.

## Aplicacao

No Provimento 213, o PDF da Alzira exibiu metricas de evidencias, conformidade e adequacoes como `100%` porque contagens foram tratadas como razoes. A correcao separou:

- cobertura da entrevista;
- evidencias cadastradas;
- distribuicao de conformidade;
- registros de remediacao;
- pendencias documentais;
- conflito historico/canonico.

## Guardrail

Relatorio, dashboard, Mini App, PDF ou KPI operacional deve carregar contrato semantico explicito para cada metrica: tipo de valor, numerador, denominador, fonte, autoridade do denominador e estado de reconciliacao.

## Relacionamentos

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Commit-de-estado-nao-e-aceitacao-operacional|Commit de estado nao e aceitacao operacional]]
- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausencia de evidencia nao e status operacional]]

## Complementos reconciliados — lote 10 de 2026-09-21

No shadow histórico, resultado observado não podia alterar rota ativa. UNKNOWN era excluído da concordância mas reduzia cobertura: comparáveis=MATCH+OVER+UNDER; concordância=MATCH/comparáveis; cobertura=comparáveis/total, denominador zero explicitamente tratado. Falha/timeout não é acordo. Persistência precisava deduplicar execution_id em primário+fallback; duplicata conflitante ou JSON truncado tornava relatório incompleto/erro, sem métricas de sucesso enganadoras. Timeout de worker isolado precisava provar ausência de processos residuais; estes relatos de teste não comprovam ativação real. Fonte: unidades 34546, 34558.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
