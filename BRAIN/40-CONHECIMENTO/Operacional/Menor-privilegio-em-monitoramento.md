---
id: brain-d03ba676ba34b20e7863
type: knowledge
title: Menor privilégio em monitoramento
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T18:55:38.578515Z'
relationships:
- type: references
  target: BRAIN/60-AGENTES/SENTINEL.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md#relações
- type: references
  target: BRAIN/60-AGENTES/versionados/workspaces/sentinel/access_control/REVOGACAO.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Menor-privilegio-em-monitoramento.md#relações
---

# Menor privilégio em monitoramento

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W29
confiabilidade: alta
ultima_revisao: 2026-07-17
tags: [monitoramento, menor-privilegio, read-only, allowlist, auditoria, revogacao]
```

## Princípio

Monitorar não exige poder de remediar. Agentes de observabilidade devem receber somente a leitura necessária, por clientes tipados e allowlists verificáveis, com saída sanitizada e revogação testável.

## Requisitos

- Fonte e operação explicitamente autorizadas.
- Cliente read-only sem URL, método, comando ou caminho arbitrário.
- Segredo fora do Brain/Git e permissão local restrita.
- Saída mínima, sem resposta bruta, credencial ou dado pessoal desnecessário.
- Auditoria append-only com ator, fonte, operação, horário UTC, resultado, correlação e hash do cliente.
- Falha de auditoria bloqueia a consulta.
- Revogação no provedor seguida de prova pela mesma rota aprovada.

## Limite de credencial compartilhada

Um wrapper read-only reduz risco operacional, mas não transforma uma credencial ampla em credencial de privilégio mínimo. Quando o provedor permitir, a solução correta é criar identidade exclusiva com escopo somente leitura. Até lá, a limitação deve permanecer documentada e revisada.

## Relações

- [[60-AGENTES/SENTINEL|SENTINEL, Controller de Operações e SNOC]]
- [[60-AGENTES/versionados/workspaces/sentinel/access_control/REVOGACAO|Procedimento de revogacao]]
- [[40-CONHECIMENTO/Operacional/Ausencia-de-evidencia-nao-e-status-operacional|Ausência de evidência não é status operacional]]

## Conhecimento recuperado dos históricos — revisão 2026-09-21

Em 01/07/2026, no contexto de dashboard do controle financeiro familiar, Hebert pediu restringir acesso ao IP fixo da empresa. Registrar como requisito de acesso daquele projeto, sujeito a confirmação do endereço e teste efetivo da restrição; a conversa não comprova firewall ou autenticação implementados. Não generalizar o IP observado no servidor como endereço autorizado da empresa. Fonte: unidades 29965.

Hashes e posições constam em `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch3-20260921.json`. Estes registros preservam decisões e aprendizados históricos; não comprovam configuração atual nem reativam operações.
