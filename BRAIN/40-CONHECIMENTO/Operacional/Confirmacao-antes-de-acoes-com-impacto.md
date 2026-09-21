---
id: brain-1aaee8dea1ff664edcb0
type: knowledge
title: Confirmação antes de ações com impacto
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:18:32.790773Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/BITDEFENDER-GRAVITYZONE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md#relações
- type: references
  target: BRAIN/99-SISTEMA/MEMORY.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md#relações
---

# Confirmação antes de ações com impacto

```yaml
categoria: operacional
tipo: guardrail
fonte: orientação de Hebert em 2026-06-18/19
confiabilidade: alta
ultima_revisao: 2026-07-28
tags: [guardrails, confirmacao, telegram, execucao, mensagens, follow-up, seguranca-operacional, approval, checkpoints]
```

## Regra

Antes de iniciar ações que gerem envio, alteração, criação ou execução fora da conversa atual, avisar Hebert e obter confirmação quando o impacto não estiver previamente autorizado.

## Inclui

- Enviar ou repostar mensagens em grupos/canais.
- Acionar agentes para execução com efeito externo.
- Alterar arquivos, configurações ou recursos operacionais fora de uma rotina já autorizada.
- Criar integrações, chaves, recursos, jobs ou artefatos com impacto operacional.
- Disparar comunicação externa, emissão fiscal, boleto, remessa, webhook ou chamada real a API sensível.

## Exceções

- Pesquisas simples e levantamento de informação sem impacto externo.
- Rotinas silenciosas já autorizadas, como a consolidação diária do Brain, desde que respeitem suas próprias restrições.
- Preparos internos reversíveis em rascunho, quando não enviem, publiquem, acionem terceiros ou exponham dados sensíveis.

## Motivo

A regra reduz risco de execução fora de contexto, postagem no canal errado, alteração indesejada e exposição acidental de informação sensível.

## Relações

- [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]
- [[70-AUTOMACOES/BITDEFENDER-GRAVITYZONE|Bitdefender GravityZone - integração Bikon]]
- [[99-SISTEMA/MEMORY|MEMORY.md]]

## Reforço 2026-W26

A regra foi reforçada por novos fluxos com impacto externo: envio de NFS-e/boleto por e-mail, disparos WhatsApp via API oficial, publicação Instagram via Meta Graph API e automações de acesso em AD local. Em todos os casos, preparação interna e dry-run são aceitáveis; envio, publicação, emissão, remessa ou alteração real permanecem dependentes de aprovação explícita quando não houver autorização prévia.

## Follow-up prometido

Em 2026-07-13, Hebert determinou uma regra operacional adicional: quando o Puppet Master prometer retorno futuro sem resposta imediata, deve agendar follow-up no Telegram antes de encerrar a interação. Essa regra reduz perda de acompanhamento em execuções delegadas a agentes e vale especialmente para tarefas com Kowalski/Darth Vader/Robotnik que dependam de retorno posterior.

## Checkpoints e Approval

Em 2026-07-28, no contexto OpenClaw - Provimento 213, a regra foi reforçada para projetos governados por checkpoint: Git commit, hash de artefato, checkpoint e Approval humano são evidências distintas. Nenhum deles substitui os demais nem autoriza continuidade implícita.

Resumo de índice, memória de agente, commit ou hash não podem reconstruir checkpoint ausente. Se um registro completo obrigatório estiver ausente, a cadeia permanece bloqueada até o Owner fornecer a evidência original.

## Complementos reconciliados — lote 6 de 2026-09-21

Nos episódios de entrega via Drive, a disponibilidade de uma interface/plugin no Codex não significava que o usuário havia recebido autorização no Telegram ou que o runtime institucional estava conectado. Não deslocar o fluxo para navegador/computador pessoal nem trocar integração silenciosamente. Respeitar o canal/ambiente autorizado da solicitação atual; uma aceitação técnica em outra superfície não transfere permissão. Fonte: unidades 29547, 36213.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
