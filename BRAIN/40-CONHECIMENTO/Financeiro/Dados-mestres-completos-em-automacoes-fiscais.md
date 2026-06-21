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

- `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- `BRAIN/20-EMPRESAS/BIKON/README.md`
- `BRAIN/70-AUTOMACOES/FATURAMENTO-TELEGRAM.md`
