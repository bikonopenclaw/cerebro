---
id: brain-8f28ff2c26ed9af615ae
type: state
title: Knowledge Health
created: '2026-09-21T17:53:52Z'
created_semantics: Data de criação deste registro estruturado; não é a data de origem do conteúdo legado.
schema_version: '1.0'
legacy_content_preserved: true
updated: '2026-09-21T17:53:52Z'
relationships:
- type: references
  target: BRAIN/99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive.md
  reason: Explicita a separação entre grafo estrutural, schemas e significado.
  source: git:2e5f3ed0e3bfcc873f2044df1a3fe80e3097be97:BRAIN/99-SISTEMA/brain-v2/tools/brain_link_gate.py
---

# Knowledge Health

Status: accepted baseline on main.

Knowledge Health measures graph and schema quality, not operational readiness.

Formula:

`Knowledge Health = 0.30 * schema_pass_rate + 0.25 * relationship_pass_rate + 0.20 * reachability_rate + 0.15 * link_integrity_rate + 0.10 * identity_integrity_rate`

Definitions:

- `schema_pass_rate = notes_passing_schema / cognitive_notes_tested`
- `relationship_pass_rate = valid_relationships / total_relationships`
- `reachability_rate = reachable_non_exempt_notes / total_non_exempt_cognitive_notes`
- `link_integrity_rate = 1 - (broken_internal_links / total_internal_links)`, capped from 0 to 1
- `identity_integrity_rate = 1` only when duplicate IDs and alias collisions are both zero, otherwise 0

Scope:

- `BRAIN/60-AGENTES/versionados/` is excluded from cognitive reachability because it is operational inventory and snapshot storage.
- Excluded snapshot paths must remain tracked in storage inventory and can still be checked for broken links and secrets.

Thresholds:

- Dry-run baseline: report only.
- Foundation QA pass: Knowledge Health >= 0.85.
- Merge/push pass: no new broken internal links, no new isolated cognitive notes, no reachability regression, no new duplicate IDs, no new alias collisions, and Knowledge Health must not decrease versus baseline.

Forbidden behavior: improving the score through artificial hub links.

Current validation as of 2026-09-20:

- Commit Link Gate: `ok=True`.
- Markdown total: `402`.
- Broken internal links: `0`.
- Uncategorized Markdown: `0`.
- Unreachable cognitive Markdown: `0`.
- Isolated cognitive Markdown: `0`.
- Graph components: `1`.
- Knowledge health estimate: `1`.
- Cognitive Markdown: `209`.
- Reachable cognitive Markdown: `209`.
- `BRAIN/60-AGENTES/versionados/` remains excluded from cognitive reachability and from the Obsidian graph because it is operational inventory/snapshot storage.

## Limitação verificada em 2026-09-21

O código atual de `brain_link_gate.py` atribui constantes 1 a `schema_pass_rate` e `relationship_pass_rate`. Portanto o score histórico acima não mede essas duas dimensões. O lote de reconciliação valida separadamente schemas e relações alteradas; não afirma que todas as notas legadas passaram por validação semântica. Consulte [[99-SISTEMA/brain-v2/governance/semantic-coverage-and-archive|o protocolo de cobertura]].
