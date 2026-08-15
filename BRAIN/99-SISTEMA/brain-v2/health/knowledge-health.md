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

Current validation as of 2026-08-15:

- Commit Link Gate: `ok=True`.
- Markdown total: `353`.
- Broken internal links: `0`.
- Uncategorized Markdown: `0`.
- Unreachable cognitive Markdown: `0`.
- Isolated cognitive Markdown: `0`.
- Graph components: `1`.
- Knowledge health estimate: `1`.
- Cognitive Markdown: `166`.
- Reachable cognitive Markdown: `166`.
- `BRAIN/60-AGENTES/versionados/` remains excluded from cognitive reachability and from the Obsidian graph because it is operational inventory/snapshot storage.
