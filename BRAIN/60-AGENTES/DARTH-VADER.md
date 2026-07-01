# Darth Vader

```yaml
categoria: agente_operacional
fonte: sessões operacionais visíveis, configuração de skills em 2026-06-17 e snapshot versionado em 2026-06-25
confiabilidade: alta
ultima_revisao: 2026-07-01
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
- Para NFS-e + boleto + remessa em lote, manter produção assistida e cadenciada: dry-run, conferência humana, aprovação explícita, emissão, conferência XML/PDF, depois boleto/remessa e só então comunicação externa.
- Não operar a esteira completa de NFS-e + boleto + remessa + e-mail como fluxo único sem pausas de validação.

## Revisão pré-produção 2026-06-30

Darth Vader registrou revisão segura do fluxo NFS-e + boleto + remessa antes de novo lote em produção. Veredito consolidado: não liberar automação direta da esteira completa; permitir apenas produção assistida, com travas por etapa.

Pontos críticos: cadastro do tomador deve usar identificador único quando houver ambiguidade; `seq_remessa`, `numero_documento` e `nosso_numero` não devem ser inferidos; e-mail externo depende de anexos conferidos e aprovação; upload no portal Cresol exige validação local da remessa e confirmação do Hebert.

## Relações

- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
