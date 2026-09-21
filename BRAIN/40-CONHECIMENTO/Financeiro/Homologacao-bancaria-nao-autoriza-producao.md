---
id: brain-3a02cbeee41af13e0836
type: knowledge
title: Homologação bancária não autoriza produção
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:50:50.519705Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Financeiro/Homologacao-bancaria-nao-autoriza-producao.md#relações
---

# Homologação bancária não autoriza produção

```yaml
categoria: financeiro
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-12
tags: [cresol, homologacao, boletos, remessa, baixa, producao]
```

## Regra

Homologação técnica, pacote local validado, API funcional ou boleto renderizado corretamente não autorizam uso em produção, upload bancário, baixa financeira ou envio externo.

## Aplicação prática

- Manter produção bloqueada por padrão até autorização explícita.
- Separar criação/consulta de título de teste de operações produtivas.
- Exigir procedimento próprio para baixa por API, com validação, rollback e aprovação.
- Registrar no Brain apenas estado, guardrails e evidência sanitizada; payloads, respostas e PDFs oficiais de homologação ficam fora do Git.
- Antes de upload, validar localmente remessa, totais, sequenciais, contrato, carteira, nosso número e documentação oficial.

## Exemplo conectado

Na semana 2026-W28, a API Cresol avançou em homologação, a remessa CNAB400 local foi validada e o boleto PDF foi conferido, mas nenhum upload no portal, envio bancário, baixa por API ou comunicação externa foi autorizado.

## Relações

- [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- [[40-CONHECIMENTO/Financeiro/Retorno-bancario-nao-valida-remessa|Retorno bancário não valida remessa]]
- [[40-CONHECIMENTO/Operacional/Separar-teste-rascunho-e-producao-em-automacoes-externas|Separar teste, rascunho e produção em automações externas]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]

## Complementos reconciliados — lote 10 de 2026-09-21

No teste Cresol histórico, HTTP400 informou Nosso Número já cadastrado antes da obtenção do boleto oficial. Uma colisão exige consultar estado remoto e identificar o título correspondente; não reutilizar ou avançar sequência cegamente. Recibo local/PDF e remessa preparada não comprovam importação ou aceite bancário; homologação permanece separada de produção. Fonte: unidades 3424.

Proposta histórica FBCP: integrar Cresol por adapter atrás do controlador, registrando intenção, autorização, identidade e idempotência. PDF oficial pode existir antes de aceite final e estado remoto pode continuar em processamento. Antes de repetir POST, reconciliar ledger local, referência externa, Nosso Número e estado remoto. CNAB não seria removido por um teste API; mudança de caminho exige provar consulta/ocorrências, rejeição e recuperação, mantendo homologação separada de produção. Fonte: unidades 31588.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch10-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
