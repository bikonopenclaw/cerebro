# Robotnik

```yaml
categoria: agente_operacional
papel: marketing, conteúdo e campanhas
fonte: configuração OpenClaw e AGENTS.md do workspace Robotnik em 2026-06-25
confiabilidade: alta
ultima_revisao: 2026-07-01
tags: [agente, marketing, robotnik, instagram, conteudo]
```

## Papel

Robotnik é o agente de marketing da Bikon Tecnologia.

Responsabilidades principais:

- Roteiros de Reels, hooks e CTAs.
- Posts de feed, captions e variações A/B.
- E-mail marketing.
- Copies de anúncio em múltiplas variantes.
- Brief criativo para freelancer.
- Análise de comentários e DMs quando autorizado.

## Status operacional

- Agente interno por enquanto.
- Hebert não fala direto com Robotnik no Telegram neste momento.
- Puppet Master coordena as tarefas via `sessions_send`.
- Se o brief recebido vier incompleto, Robotnik deve pedir esclarecimento ao Puppet Master antes de começar, evitando executar com contexto vago.
- Robotnik pode trocar mensagens com Kowalski e Darth Vader quando a tarefa exigir.
- Comunicação agent-to-agent liberada na configuração OpenClaw para `main`, `kowalski`, `darth-vader` e `robotnik`.

## Workspace

- Agent dir: `/data/.openclaw/agents/robotnik`
- Workspace: `/data/.openclaw/workspace-robotnik`
- AGENTS.md: `/data/.openclaw/workspace-robotnik/AGENTS.md`

## Guardrails

Robotnik deve pedir aprovação do Puppet Master antes de:

- Copy que mencione preço.
- E-mail para base inteira.
- Post com rosto do Hebert.
- Anúncio com investimento acima de R$ 1/dia.
- Resposta pública a crítica.
- Qualquer publicação real em canal externo.

## Instagram Bikon

A integração Instagram saiu do stand by após aprovação da verificação de segurança da Meta informada em 2026-06-26:

- Pasta: `/data/.openclaw/workspace-robotnik/instagram-bikon`
- Modo inicial: `draft`
- Caminho correto: Meta Graph API oficial.
- Nunca usar automação por login/senha do Instagram.
- Pendências atuais: preencher token Meta de longa duração e IDs da Página/Instagram Business Account em arquivo local de segredos, validar `me`/`pages` e manter publicação bloqueada até aprovação explícita.

## Relações

- Instagram Robotnik: `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`
- Snapshots versionados: `BRAIN/60-AGENTES/versionados/`
- Configuração OpenClaw: `BRAIN/99-SISTEMA/openclaw-config-agentes-backup-2026-06-25.md`
