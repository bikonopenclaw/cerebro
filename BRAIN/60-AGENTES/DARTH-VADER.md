# Darth Vader

```yaml
categoria: agente_operacional
fonte: sessões operacionais visíveis, configuração de skills em 2026-06-17 e snapshot versionado em 2026-06-25
confiabilidade: alta
ultima_revisao: 2026-06-25
tags: [agente, financeiro, faturamento, nfse, boleto, remessa]
```

## Papel

Agente operacional financeiro usado para tarefas de faturamento, NFS-e, boletos, remessas e conferências cadastrais quando a execução exigir especialização financeira/fiscal.

## Skills e contextos relevantes

- `notaas-nfse`: uso exclusivo da Darth Vader para NFS-e da Bikon, com segredos fora do Brain/Git.
- `emitir-nfse-boleto-remessa`: skill geral relacionada a NFS-e, boletos e remessas.
- `boletos-cresol`: skill técnica relacionada a boletos Cresol.

## Contextos removidos / históricos

- `faturamento-fn-souza`: estrutura inicial criada em 2026-06-17 para o fluxo de faturamento FN Souza, removida do conjunto ativo em 2026-06-25. Não deve ser acionada como skill ativa sem nova autorização explícita e novo escopo operacional.

## Guardrails

- Não emitir NFS-e real sem aprovação explícita.
- Não emitir boleto real sem aprovação explícita.
- Não gerar remessa de produção sem validação e aprovação explícita.
- Não enviar comunicação externa em nome da Bikon sem aprovação explícita.
- Pode preparar rascunhos, estrutura de arquivos, conferências e lista de pendências internas.

## Relações

- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
