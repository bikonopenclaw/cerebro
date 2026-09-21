---
id: brain-a2c0ca05e5b1af111694
type: knowledge
title: Dados mestres completos em automações fiscais
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:08:05.502633Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais.md#relações
- type: references
  target: BRAIN/20-EMPRESAS/BIKON/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Dados-mestres-completos-em-automacoes-fiscais.md#relações
---

# Dados mestres completos em automações fiscais

```yaml
categoria: financeiro_fiscal
tipo: aprendizado_permanente
fonte: consolidação de 2026-06-20 e revisão semanal 2026-W25
confiabilidade: alta
ultima_revisao: 2026-06-21
tags: [nfse, cadastro, tomador, dados-mestres, automacao-fiscal, bikon]
```

## Princípio

Automações fiscais devem preservar integralmente os dados disponíveis no cadastro mestre. Usar apenas os campos mínimos aceitos por uma API pode gerar documento incompleto, retrabalho ou risco operacional.

## Aplicação prática

Em emissões de NFS-e da BIKON:

- usar CPF/CNPJ conforme cadastro;
- usar nome ou razão social do cadastro;
- usar e-mail financeiro quando existir;
- incluir endereço completo quando disponível: logradouro, número, complemento, bairro, cidade, UF e CEP;
- não emitir lote apenas com documento, nome e e-mail quando o cadastro possuir endereço;
- se endereço estiver ausente ou ambíguo, marcar pendência antes da emissão.

## Aprendizado

Payload fiscal não deve ser reduzido ao mínimo técnico aceito pela API. A fonte de verdade é o cadastro mestre; a automação deve carregar todos os campos confiáveis para reduzir risco de inconsistência.

## Relações

- [[70-AUTOMACOES/NOTAAS-NFSE|Skill Notaas NFS-e]]
- [[20-EMPRESAS/BIKON/README|BIKON]]
- [[70-AUTOMACOES/FATURAMENTO-TELEGRAM|Grupos Telegram de faturamento]]

## Complementos reconciliados — lote 5 de 2026-09-21

No teste fiscal/Cresol de 16/06/2026, um boleto de segunda via já incluía multa/mora. O relato separou esse valor atualizado do principal da NFS-e usado na nova preparação. A lição é identificar origem e natureza do valor antes de reutilizar documento: segunda via atualizada não é, por si, base para criar nova obrigação. Cada emissão continua exigindo fonte fiscal, escopo e aprovação aplicáveis. Fonte: unidades 36469.

No saneamento de teste do faturamento em 03/07/2026, um pacote de simulação reutilizou nfse_id existente pela regra de deduplicação. A limpeza foi limitada ao objeto de teste e pacote físico, sem apagar NFS-e/cliente presumindo exclusividade. Antes de descartar fixture, confirmar referências e identidade compartilhada; nome teste ou pasta temporária não garante que todos os registros associados sejam descartáveis. Fonte: unidades 38104.

No diagnóstico NotaAS de 13/06/2026, removerInscrição Estadual não resolvia necessariamente rejeição referente àInscrição Municipal. Identificar campo e entidade exatos indicados pela fonte antes de alterar cadastro, evitando tratar siglas IE/IM como equivalentes. A decisão posterior da Bikon sobre enviar IM é específica daquele fluxo e não regra fiscal geral. Fonte: unidades 29008.

Em 17/06/2026, Hebert corrigiu a cidade do cadastro Nicole Debus Advocacia de CACAVEL para CASCAVEL. O relato de execução afirmou atualização coerente de JSON, CSV e SQLite. A lição é reconciliar representações do cadastro após correção de dado mestre; essa evidência histórica não substitui conferência da base vigente nem autoriza emitir a partir de cópia antiga. Fonte: unidades 30856.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch5-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
