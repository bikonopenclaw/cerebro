# CHANGELOG.md

## 2026-06-12

- Criada estrutura Brain Enterprise v1.0.
- Criadas subpastas oficiais.
- Criados arquivos obrigatórios em `99-SISTEMA`.
- Registrada regra operacional em `CONFIG.md`.

## 2026-06-12, decisão arquitetural

- Confirmado que o Brain não será agente.
- Brain definido como repositório vivo de conhecimento.
- Puppet Master permanece responsável pela administração do Brain.
- Criada rotina diária de consolidação silenciosa.
- Criado dashboard inicial de status do Brain.

## 2026-06-12, consolidação diária

- Criado diário consolidado em `BRAIN/01-DIARIO/2026/2026-06-12.md`.
- Registrada automação `BRAIN/70-AUTOMACOES/CONSOLIDACAO-DIARIA-SILENCIOSA.md`.
- Atualizados indicadores de saúde após criação da rotina e dashboard inicial.

## 2026-06-12, filosofia cognitiva

- Criado `BRAIN/99-SISTEMA/FILOSOFIA.md`.
- Registrados princípios: memória maior que armazenamento, contexto maior que fato, conhecimento conectado, relevância conquistada e esquecimento saudável.
- Criada pasta `BRAIN/99-ARQUIVO` para redução de prioridade sem apagar conhecimento.
- Atualizados `CONFIG.md`, `INDEX.md`, `ROTINA-CONSOLIDACAO.md` e `HEALTH.md`.

## 2026-06-12, sync GitHub 4x ao dia

- Criado script `scripts/sync-github.sh`.
- Script faz commit apenas quando há mudanças locais.
- Script envia `main` para `origin/main`.
- Automação programada para 06:00, 12:00, 18:00 e 23:00 BRT.

## 2026-06-12, skill Notaas NFS-e

- Auditada skill Notaas NFS-e v2.0.
- Corrigidos problemas de instalação, dry-run e frontmatter.
- Instalada skill em `/data/.openclaw/workspace/skills/notaas-nfse` e `/data/.openclaw/skills/notaas-nfse`.
- Registrados guardrails para impedir emissão/cancelamento fiscal sem confirmação explícita.
