# Artefatos gerados fora do Brain e Git

```yaml
categoria: operacional
tipo: guardrail
fonte: consolidação semanal 2026-W28
confiabilidade: alta
ultima_revisao: 2026-07-12
tags: [git, brain, snapshots, artefatos, dados-derivados, seguranca]
```

## Regra

Artefatos gerados por execução, homologação, exportação ou rascunho não devem ser tratados como conhecimento permanente do Brain.

O Brain deve registrar decisões, arquitetura, guardrails e estado operacional sanitizado. Bancos locais, exports, drafts, ambientes virtuais, arquivos temporários, respostas de API, PDFs gerados, CSVs, SVGs e estados de ferramenta ficam no workspace operacional ou em cofre local, fora do Git.

## Aplicação prática

- Excluir de snapshots versionados diretórios como `exports/`, `drafts/`, `homologacao-*`, `.venv-*` e estados OpenClaw.
- Excluir arquivos derivados como `*.db`, `*.sqlite`, `*.sqlite3`, WAL/SHM, `*.csv`, `*.svg`, PDFs gerados e payloads brutos.
- Registrar no Brain apenas o resultado sanitizado, a decisão tomada e o guardrail necessário para repetir com segurança.
- Tratar rascunhos editoriais, exports financeiros e artefatos de homologação como evidência operacional temporária, não como memória permanente.

## Motivo

Dados derivados podem conter informação sensível, envelhecer rápido ou criar ruído no repositório. A memória útil é a interpretação curada: o que foi validado, qual decisão mudou e qual regra deve sobreviver.

## Relações

- `BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md`
- `BRAIN/60-AGENTES/versionados/`
- `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- `BRAIN/70-AUTOMACOES/INSTAGRAM-BIKON-ROBOTNIK.md`
