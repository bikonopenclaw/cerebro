---
id: brain-41161537545a2b7d927a
type: knowledge
title: Governança antes de automação de identidade
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T19:18:32.790773Z'
relationships:
- type: references
  target: BRAIN/70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Governanca-antes-de-automacao-de-identidade.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Governanca-antes-de-automacao-de-identidade.md#relações
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Governanca-antes-de-automacao-de-identidade.md#relações
---

# Governança antes de automação de identidade

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [identidade, entra-id, ad-local, auditoria, governanca, rmm]
```

## Princípio

Antes de automatizar identidade entre diretórios internos e ambientes de clientes, é necessário separar inventário, aprovação, matriz de permissões, regras de ação e trilha de auditoria.

## Aplicação prática

- Começar com fase somente-auditoria.
- Comparar usuários aprovados no Entra ID BIKON com contas/grupos encontrados nos ADs locais dos clientes.
- Reportar divergências antes de qualquer correção.
- Não criar, desativar, remover grupo ou alterar privilégio sem aprovação explícita.
- Ignorar contas não marcadas como gerenciadas pela BIKON, salvo quando houver evidência relevante para relatório.
- Evitar registrar no Brain dumps de AD, inventários brutos, hashes, senhas ou dados sensíveis completos.

## Motivo

Automação de identidade tem alto risco operacional. Uma correção indevida pode remover acesso legítimo, conceder privilégio excessivo ou interferir em contas que pertencem ao cliente.

## Relações

- [[70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES|Matriz de acesso Bikon x clientes AD local]]
- [[40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto|Confirmação antes de ações com impacto]]
- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]

## Complementos reconciliados — lote 6 de 2026-09-21

Na consolidação de CNS, manter a fonte oficial CNJ como autoridade de validação; resultado de busca/Corregedoria auxilia a formar candidato, não prova por si o vínculo final no cadastro. Conferir identidade e escopo contratual antes de gravar; fonte e data fazem parte da evidência. Fonte: unidades 35415.

No piloto de correlação entre NinjaOne, ARX e Bitdefender, ter21clientes cadastrados não provava mapeamento dos IDs de cada fonte: G0 ficou NO-GO e24x7desligado. Matriz candidata deve usar IDs estáveis, ser revisada e ter vínculos de negócio aprovados antes de rotear alerta. A família Corpus/2xxx foi observada como associação operacional por nome, sem vínculo pai/filho formal demonstrado pela API; não promover essa lista a hierarquia canônica nem fazer matching por nome silenciosamente. Fonte: unidades 31503, 36849, 31506.

Proveniência: `BRAIN/99-SISTEMA/brain-v2/reports/coverage-parallel-batch6-20260921.json`. Casos históricos não comprovam estado atual nem autorizam reexecução.
