# Brain v2 Governance

Status: foundation candidate in isolated worktree.

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
