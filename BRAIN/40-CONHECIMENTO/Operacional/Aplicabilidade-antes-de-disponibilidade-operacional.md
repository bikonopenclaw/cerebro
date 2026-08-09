# Aplicabilidade antes de disponibilidade operacional

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidacao semanal 2026-W32
confiabilidade: alta
ultima_revisao: 2026-08-09
tags: [provider, aplicabilidade, evidencia, provimento-213, fail-closed]
```

## Principio

Disponibilidade tecnica de uma plataforma, provider, API ou rota nao prova que ela se aplica ao ciclo operacional atual.

Uma pergunta, decisao ou execucao especifica sobre provider so e elegivel quando existir uma destas evidencias:

- provider selecionado por unidade autorizada;
- arquitetura aprovada que mandate o provider;
- controle regulatorio aplicavel que exija aquele provider;
- dependencia operacional ja aprovada que torne o provider necessario.

## Aplicacao pratica

- Separar capacidade oficial de aplicabilidade canonica.
- Nao perguntar por AWS/Azure/GCP apenas porque eles tecnicamente cobrem gaps.
- Nao transformar rota, tenant, subscription, conta ou projeto possivel em caminho operacional sem owner, permissao e trilha de auditoria.
- Se a aplicabilidade nao estiver provada, manter `FAIL_CLOSED` e selecionar pergunta neutra ou bloqueada por respondente/canal autorizado.

## Exemplo conectado

Em 2026-08-03, a pergunta `Q-PROVIDER-001` do Provimento 213 foi entregue e depois colocada em quarentena porque confundiu disponibilidade de provider com aplicabilidade do provider ao ciclo. A regra corrigida exige provider selecionado, mandatado, requerido por controle aplicavel ou necessario para dependencia ja aprovada.

## Relacoes

- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
- [[40-CONHECIMENTO/Operacional/Capacidade-tecnica-nao-substitui-evidencia-de-ambiente|Capacidade tecnica nao substitui evidencia de ambiente]]
- [[40-CONHECIMENTO/Operacional/Autorizacao-atomica-nao-herda-escopo|Autorizacao atomica nao herda escopo]]
- [[01-DIARIO/Semanal/2026-W32|Semana 2026-W32]]
