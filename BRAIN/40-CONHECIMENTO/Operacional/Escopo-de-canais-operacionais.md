# Escopo de canais operacionais

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidações de 2026-06-18 a 2026-06-21
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [canais, telegram, escopo, roteamento, guardrails, faturamento]
```

## Princípio

Canais operacionais precisam de escopo explícito para evitar mistura de assuntos, execução fora de contexto e respostas no local errado.

## Aplicação prática

Para cada grupo, canal ou contexto operacional relevante, registrar:

- finalidade do canal;
- assuntos permitidos;
- assuntos fora de escopo;
- empresa, cliente ou projeto relacionado;
- agente ou skill responsável pela execução;
- guardrails de aprovação antes de impactos externos;
- caminho do contexto local, quando existir.

## Aprendizado

Separar canais por empresa e tipo de operação reduz risco financeiro, fiscal e reputacional. O agente deve responder considerando o contexto do canal, não apenas a mensagem isolada.

## Relações

- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/60-AGENTES/DARTH-VADER.md`

## Reforço 2026-W26

Além do escopo do canal, a configuração precisa separar grupo permitido de remetente autorizado. A correção do `groupAllowFrom` no Faturamento Bikon mostrou que allowlist de canal e allowlist de autor são camadas independentes; quando o provider mantém estado antigo, reload/restart limpo pode ser necessário para validar a configuração aplicada.
