---
id: brain-a99fd14c965ed57d037f
type: knowledge
title: Canais com escopo e remetente autorizados
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:50:50.519705Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Canais-com-escopo-e-remetente-autorizados.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Canais-com-escopo-e-remetente-autorizados.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Canais-com-escopo-e-remetente-autorizados.md#relações
---

# Canais com escopo e remetente autorizados

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [telegram, canais, allowlist, remetente, escopo, gateway]
```

## Princípio

Em canais operacionais, grupo permitido e remetente autorizado são dimensões diferentes de segurança. O agente precisa validar ambos para evitar resposta no contexto certo para a pessoa errada, ou resposta de pessoa certa no grupo errado.

## Aplicação prática

- Registrar o ID do grupo/canal permitido separadamente do ID do remetente autorizado.
- `groupAllowFrom` deve representar remetentes autorizados, não o ID do grupo.
- Após corrigir allowlist ou configuração de provider/canal, considerar reload/restart limpo quando o comportamento antigo persistir.
- Manter escopo permitido, fora de escopo, roteamento e guardrails documentados no Brain.

## Relações

- [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]
- [[40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais|Escopo de canais operacionais]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]

## Conhecimento recuperado dos históricos — revisão 2026-09-21

No episódio histórico de configuração de grupos, a abertura consultiva foi limitada a grupos aprovados nominalmente; não autorizou wildcard para qualquer grupo nem abertura do faturamento. Permissão consultiva e autoridade para efeitos financeiros continuam distintas; a configuração vigente deve ser revalidada antes de reutilizar o exemplo. Fonte: unidades 31800.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.

## Complementos reconciliados — lote 10 de 2026-09-21

No piloto Portal213, imagem do BotFather mostrava direitos padrão para futuras adições, mas BotAPI no canal existente retornava can_edit_messages=false apesar de administrator e can_post_messages=true. Conferir permissão efetiva no canal e identidade numérica antes da ação; título, username, papel amplo e screenshot de defaults não provam capacidade específica. Após ajuste houve card próprio publicado/fixado e validação sanitizada, sem autorização de publicação cliente ou edição de mensagens alheias. Fonte: unidades 37104.

Pedido histórico de Hebert limitou a dispensa de menção a um grupo em que conversava sozinho com o bot. O ID do grupo e a alteração efetiva não estão comprovados nesta unidade. Preservar a intenção contextual; não converter o pedido em requireMention=false global nem ampliar remetentes autorizados. Fonte: unidades 34333.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
