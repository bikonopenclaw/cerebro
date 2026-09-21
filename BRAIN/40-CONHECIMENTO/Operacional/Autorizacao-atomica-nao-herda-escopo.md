---
id: brain-bf78a26fa0e02626330e
type: knowledge
title: Autorizacao atomica nao herda escopo
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:08:05.502633Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W31.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Validacao-tecnica-nao-substitui-aceite-humano.md
  reason: Complementa o limite de escopo da autorização com a exigência de aceite aplicável à versão do artefato; não equipara aprovação técnica e humana.
  source: git:2e5f3ed0e3bfcc873f2044df1a3fe80e3097be97:BRAIN/40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo.md; BRAIN/40-CONHECIMENTO/Operacional/Validacao-tecnica-nao-substitui-aceite-humano.md
---

# Autorizacao atomica nao herda escopo

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W31; consolidacao semanal 2026-W37; projeto LinkedIn Robotnik 2026-09-17
confiabilidade: alta
ultima_revisao: 2026-09-18
tags: [approval, checkpoints, escopo, governanca, fail-closed, provimento-213, linkedin, oauth, versao, artefato, publicacao]
```

## Principio

Autorizacao operacional deve ser atomica. Um approval, checkpoint, commit, hash, validacao independente ou publicacao comprova somente o escopo exato que foi autorizado e executado.

Nenhuma evidencia tecnica herda permissao para a proxima etapa.

## Aplicacao pratica

- Separar documento, implementacao, commit, push/publicacao, homologacao, deploy, recorrencia e rollback.
- Usar cada `approval_id` e `execution_id` apenas para a unidade autorizada.
- Tratar ordem terminal como encerrada; falha, timeout ou sucesso parcial nao autorizam reuso.
- Antes de continuar, declarar o novo impacto, os limites e o rollback da proxima unidade.
- Quando faltar evidencia completa, manter bloqueado em vez de reconstruir estado por resumo, memoria ou hash isolado.
- Vincular parecer, aceite e autoridade a identidade logica, versao e bytes exatos do artefato; alteracao posterior abre um novo gate e nao herda o veredito anterior.
- Separar criacao, revisao, entrega, aceite humano, publicacao e readback. Sucesso em uma etapa nao autoriza a seguinte nem retry de um efeito externo ja comprovado.
- Em integrações externas, separar credenciamento do app, associação/verificação da organização, concessão de produto/scope, OAuth, acesso ao segredo, aprovação do payload e publicação. Uma autorização não atravessa essas fronteiras.

## Exemplo conectado

Na semana 2026-W31, o OpenClaw - Provimento 213 teve EPs documentais, commits, hashes, validacoes independentes e publicacao canonica. Esses marcos nao autorizaram provider, target, preflight, restore, contato externo, envio de PDF, deploy ou recorrencia.

Na semana 2026-W37, o marketing Bikon preservou autoridade por versao: o aceite do piloto inicial nao autorizou publicacao; o parecer da V3 do 365 Control nao alcançou a V6; e a publicacao comprovada de 10/09 bloqueou novo `media_publish` mesmo enquanto readback e recibo permaneciam pendentes.

No LinkedIn Robotnik, Hebert autorizou somente o Gate A de credenciamento. A falta de navegador anexável bloqueou a execução antes do portal; o approval não foi interpretado como permissão para OAuth, secret store, scope adicional ou publicação.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[01-DIARIO/Semanal/2026-W31|Semana 2026-W31, cobertura parcial]]
- [[01-DIARIO/Semanal/2026-W37|Semana 2026-W37]]
- [[50-PROJETOS/Em-Andamento/LinkedIn-Robotnik-Publisher|LinkedIn Robotnik Publisher]]

## Conexão revisada em 2026-09-21

[[40-CONHECIMENTO/Operacional/Validacao-tecnica-nao-substitui-aceite-humano|Validacao tecnica nao substitui aceite humano]]: Complementa o limite de escopo da autorização com a exigência de aceite aplicável à versão do artefato; não equipara aprovação técnica e humana.

## Complementos reconciliados — lote 4 de 2026-09-21

No desenho histórico SERPRO, consulta de parcelamento e emissão de DAS eram autorizações distintas. A autorização de emissão deveria identificar serviço, competência/parcela e valor; não expor botão genérico Emitir que contorne essas dimensões. O catálogo histórico de códigos/endpoints não é comprovação de API vigente. Fonte: unidades 38054.

Proveniência e disposições: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch4-20260921.json`. Aplicações históricas permanecem delimitadas pelo período e contrato da fonte.
