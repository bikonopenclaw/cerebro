# Brain v2 Graph Audit Spec

Status: foundation candidate.

## Inputs

- Canonical Brain repository HEAD.
- Cognitive metrics exclusion manifest.
- Note schemas.
- Relationship type registry.
- Canonical entry points and MOC policy.

## Checks

1. Inventory closure: every Markdown path has exactly one primary category.
2. Schema validation: required fields and type-specific schema compatibility.
3. Identity validation: no duplicate IDs and no alias collisions.
4. Relationship validation: targets resolve, types are approved, reasons exist.
5. Supersession validation: no cycles in supersession subgraph.
6. Reachability validation: every non-exempt cognitive note is reachable from an approved entry point.
7. Link validation: no new broken internal links introduced by a batch.
8. Metric reproducibility: repeated runs from same HEAD produce the same values.

## Outputs

- Operational Health report.
- Knowledge Health report.
- Broken-link delta.
- Orphan and reachability report.
- Contract pass/fail matrix.

## Fail-Closed Rule

Any integrity contract failure blocks promotion, merge, push and cron reactivation until corrected or explicitly superseded by a new approval.
