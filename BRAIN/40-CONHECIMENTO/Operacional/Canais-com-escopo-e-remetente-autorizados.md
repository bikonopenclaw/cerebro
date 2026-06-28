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

- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Escopo-de-canais-operacionais.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
