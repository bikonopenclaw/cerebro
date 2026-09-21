---
id: brain-b0d009e977ec010322b2
type: knowledge
title: Capacidade tecnica nao substitui evidencia de ambiente
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T20:06:54.602140Z'
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

## Complementos reconciliados — lote 5 de 2026-09-21

No desenho de 18/06/2026, a conta DreamHost foi separada da integração Gmail/Google Workspace: deveria usar rota IMAP/SMTP apropriada, com permissão de leitura/envio definida para aquela conta. Ter token gmail.send não demonstra acesso a uma caixa DreamHost. Hosts/portas e credenciais devem ser confirmados na configuração e documentação atuais antes de conectar. Fonte: unidades 34711.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.

## Complementos reconciliados — lote 15 de 2026-09-21

O status agregado ARX expunha contagens sanitizadas, suficientes para indicar atenção, mas insuficientes para explicar a causa de um cliente específico. Antes de usar uma consulta autorizada para responder outra pergunta, verificar se o contrato retorna a informação necessária; não inferir diagnóstico a partir de contagem nem abrir payloads brutos como atalho. Uma extensão apropriada pode fornecer categorias agregadas de causa, com escopo e minimização explícitos, antes da execução correspondente. Fonte: unidades 36770.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch15-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
