---
id: brain-8b3a4cc164fa24d4f269
type: knowledge
title: Artefatos gerados fora do Brain e Git
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/boletos-malote/README.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md#relações
- type: references
  target: BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md#relações
- type: references
  target: BRAIN/50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213.md
  reason: Relação já declarada pelo autor na seção Relações; conversão de caminho literal para link navegável.
  source: BRAIN/40-CONHECIMENTO/Operacional/Artefatos-gerados-fora-do-Brain-e-Git.md#relações
---

# Artefatos gerados fora do Brain e Git

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-30
tags: [git, brain, snapshots, artefatos, dados-derivados, seguranca, bytecode, validacao]
```

## Regra

Artefatos gerados por execução, homologação, exportação ou rascunho não devem ser tratados como conhecimento permanente do Brain.

O Brain deve registrar decisões, arquitetura, guardrails e estado operacional sanitizado. Bancos locais, exports, drafts, ambientes virtuais, arquivos temporários, respostas de API, PDFs gerados, CSVs, SVGs e estados de ferramenta ficam no workspace operacional ou em cofre local, fora do Git.

## Aplicação prática

- Excluir de snapshots versionados diretórios como `exports/`, `drafts/`, `homologacao-*`, `.venv-*` e estados OpenClaw.
- Excluir arquivos derivados como `*.db`, `*.sqlite`, `*.sqlite3`, WAL/SHM, `*.csv`, `*.svg`, PDFs gerados e payloads brutos.
- Registrar no Brain apenas o resultado sanitizado, a decisão tomada e o guardrail necessário para repetir com segurança.
- Tratar rascunhos editoriais, exports financeiros e artefatos de homologação como evidência operacional temporária, não como memória permanente.
- Em validações Python sobre subtrees protegidos, desabilitar bytecode com `-B`/`PYTHONDONTWRITEBYTECODE=1` e checar untracked antes e depois. Arquivos `.pyc` criados pela própria validação são side effect operacional e podem invalidar a cadeia de custódia.

## Motivo

Dados derivados podem conter informação sensível, envelhecer rápido ou criar ruído no repositório. A memória útil é a interpretação curada: o que foi validado, qual decisão mudou e qual regra deve sobreviver.

## Relações

- [[40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git|Segredos fora do Brain e Git]]
- `BRAIN/60-AGENTES/versionados/`
- [[70-AUTOMACOES/boletos-malote/README|Boletos e malote bancário]]
- [[70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK|Instagram Bikon, Robotnik]]
- [[50-PROJETOS/Em-Andamento/OpenClaw-Provimento-213|OpenClaw - Provimento 213]]
