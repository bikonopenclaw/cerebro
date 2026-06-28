# Retorno bancário não valida remessa

```yaml
categoria: financeiro
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [cnab400, cresol, retorno, remessa, conciliacao, boletos]
```

## Princípio

Um arquivo de retorno bancário pode servir como evidência para parser e conciliação, mas não valida layout de remessa nem autoriza inferir próximo nosso número, documento, sequencial ou regra de envio.

## Aplicação prática

- Usar retorno `.ret` apenas para leitura de ocorrências, liquidações e conciliação.
- Sanitizar exemplos antes de qualquer registro no Brain.
- Não versionar `.ret` bruto quando contiver dados sensíveis.
- Não usar retorno como golden case de remessa `.rem`.
- Homologar layout de remessa com documentação oficial e validação bancária antes de qualquer envio real.

## Motivo

Retorno e remessa têm finalidades opostas no fluxo CNAB. Confundir os dois pode gerar boletos/remessas inválidos, sequenciais incorretos ou exposição de dados financeiros.

## Relações

- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
