# Brain v2 Governance

Status: accepted on main.

Brain v2 separates canonical knowledge from evidence, events, transient state, decisions, proposals and operational snapshots. The foundation blocks new knowledge debt before legacy migration starts.

## Authority

- Hebert is the only execution approver for gates, merge, push, rollback and cron reactivation.
- Agents may produce proposals and evidence, but direct canonical writes are prohibited outside the approved governor path.
- Approval for one gate does not authorize another gate.

## Canonical Flow

1. Capture raw input as evidence, event or proposal.
2. Validate proposal envelope and source.
3. Apply schema and relationship checks.
4. Stage exact manifest paths only.
5. Publish separate Operational Health and Knowledge Health.
6. Stop on any contract failure.

## Foundation Scope

This foundation adds governance rules, schemas, relationship types, MOC reachability policy, proposal handling, metric exclusions, health definitions and fail-closed sync rules. It does not perform full legacy migration.

Cutover status as of 2026-08-04:

- Foundation commit: `ef724a98800ab9a0d408e34596b4dfbb51234f55`.
- Phase 11B commit: `153129b52ae093c42bb106006de18b78a7ab7dbe`.
- Current accepted baseline: 0 broken internal links, 0 uncategorized Markdown, 0 duplicate IDs, 0 duplicate aliases.

## Phase 11B Scope

Phase 11B starts the missing reintegration layer after the foundation cutover. It adds real entry points, resolves obvious legacy wikilinks to canonical paths and introduces a local Commit Link Gate so future commits can be checked against accepted knowledge debt instead of silently adding new orphan notes.

The first batch links legacy diary notes through `BRAIN/01-DIARIO/README.md` without moving historical files.

## Active Constraint

The local Commit Link Gate exists as a validation tool and baseline. Automatic Git sync still needs a separate reconciliation step before it can be considered fully fail-closed for staging and commit.

## Phase 11C Graph Gate

Phase 11C closes the gap between "no broken links" and "healthy Obsidian graph". The Commit Link Gate now measures cognitive reachability, isolated cognitive notes and graph components.

`BRAIN/60-AGENTES/versionados/` remains preserved as operational inventory, but is excluded from cognitive reachability and from the Obsidian graph through `.obsidian/app.json`.

Canonical MOCs by area connect empresas, conhecimento, projetos, agentes, automacoes, dashboards and sistema without moving historical notes or linking snapshots as if they were knowledge.
