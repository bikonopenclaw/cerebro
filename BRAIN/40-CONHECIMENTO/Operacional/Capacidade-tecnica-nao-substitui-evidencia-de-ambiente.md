---
id: brain-b0d009e977ec010322b2
type: knowledge
title: Capacidade tecnica nao substitui evidencia de ambiente
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente.md#relações
- type: references
  target: BRAIN/01-DIARIO/Semanal/2026-W31.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente.md#relações
---

# Capacidade tecnica nao substitui evidencia de ambiente

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidacao semanal 2026-W31
confiabilidade: alta
ultima_revisao: 2026-08-02
tags: [provider, cloud, evidencia, management-plane, read-only, selecao]
```

## Principio

Um provedor pode ter capacidade tecnica oficial para resolver um problema e ainda assim nao estar operacionalmente disponivel para o caso concreto. Se faltam conta, tenant, subscription, projeto, dono aprovado, permissao e trilha de auditoria, a capacidade permanece teorica.

## Aplicacao pratica

- Separar matriz de capacidade de evidencia de ambiente existente.
- Antes de selecionar provider, confirmar por leitura autorizada a existencia do ambiente e seu owner.
- Registrar gaps como `sem superficie disponivel` ou `parcialmente coberto`, sem completar por inferencia.
- Nao escolher por empate aparente quando o bloqueio real e falta de evidencia local.
- Manter credenciais, IDs sensiveis e inventarios brutos fora do Brain/Git; registrar apenas estado sanitizado.

## Exemplo conectado

Na semana 2026-W31, AWS, Azure e Google Cloud cobriam tecnicamente os gaps de cloud/VM, firewall/roteamento, replicacao/snapshot/clone, cleanup/descarte e rollback. Ainda assim, nenhum provider foi selecionado porque nao havia evidencia local de conta, tenant, subscription ou projeto existente e aprovado.

## Relacoes

- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausência de evidência não é status operacional]]
- [[40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento|Menor privilégio em monitoramento]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[01-DIARIO/Semanal/2026-W31|Semana 2026-W31, cobertura parcial]]
