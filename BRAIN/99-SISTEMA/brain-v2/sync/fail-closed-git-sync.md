# Fail-Closed Git Sync

Status: accepted policy; implementation gap tracked.

## Required Gates

1. Dedicated worktree must be clean before staging.
2. Every changed path must be listed in the approved execution manifest.
3. `git add -A` and broad staging equivalents are prohibited.
4. Secret scanning must pass before commit or push.
5. Fast-forward safety must be verified before merge or push.
6. Divergence, conflict, unexpected paths or secrets stop the operation.

## Current Gap

As of 2026-08-05, the policy is accepted in Brain v2 and the local Commit Link Gate exists, but the legacy `scripts/sync-github.sh` still performs broad staging with `git add -A`. Treat automatic sync as operationally useful but not fully reconciled with this policy until the script is changed under a separate approval.

## Allowed Staging

Only explicit manifest paths may be staged.

Example pattern:

```sh
git add -- path/from/manifest.md path/from/manifest.yaml
```

## Forbidden Staging

```sh
git add -A
git add .
git commit -a
```

## Rollback

Rollback must preserve evidence, restore baseline or approved commit set, restore cron state, validate repository integrity and produce a rollback report. Retry requires new explicit approval.
