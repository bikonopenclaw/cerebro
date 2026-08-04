# Brain v2 Proposal Pipeline

Status: foundation candidate.

Agent output is proposal material, not canonical knowledge.

## Required Envelope

Every proposal must contain:

- proposal_id
- producer
- source
- target_note
- operation
- reason
- confidence
- suggested_relations

## States

- pending
- accepted
- rejected
- quarantined
- deferred

## Rules

1. Reprocessing the same proposal must be idempotent.
2. Rejected proposals remain traceable without canonical side effects.
3. Accepted proposals must pass schema, identity, relationship, reachability and manifest checks before write.
4. Canonical writes require explicit approval and exact manifest paths.
