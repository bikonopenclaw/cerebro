---
categoria: operacional
fonte: consolidacao diaria 2026-08-13, a partir do gate Provimento 213 false 100% KPI de 2026-08-12
confiabilidade: alta
ultima_revisao: 2026-08-13
tags: [metricas, kpi, relatorios, provimento-213, qualidade, semantica]
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
