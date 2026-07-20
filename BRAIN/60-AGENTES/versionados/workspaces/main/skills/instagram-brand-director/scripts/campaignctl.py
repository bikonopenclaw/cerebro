#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from runtime_lib import (TRANSITIONS, append_jsonl, atomic_write_json, exclusive_lock,
                         load_json, make_event, request_hash, require_id, sha256_json,
                         utc_now, validate_approval)

def state_paths(root: Path):
    return root / "campaign.json", root / "events.jsonl", root / ".campaign.lock"

def init_campaign(args):
    require_id(args.campaign_id, "campaign_id")
    require_id(args.asset_id, "asset_id")
    root = Path(args.base).resolve() / args.campaign_id
    state_path, events_path, lock_path = state_paths(root)
    with exclusive_lock(lock_path):
        if state_path.exists():
            raise SystemExit("campanha já existe")
        for d in ("prompts", "generated", "renders", "approvals", "requests", "qa"):
            (root / d).mkdir(parents=True, exist_ok=True)
        state = {
            "campaign_id": args.campaign_id,
            "correlation_id": hashlib.sha256(os.urandom(32)).hexdigest(),
            "asset_id": args.asset_id,
            "version": 1,
            "event_version": 1,
            "state": "intake",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "actor": args.actor,
        }
        atomic_write_json(state_path, state)
        append_jsonl(events_path, make_event(state, "init", args.actor, "ok", None, sha256_json(state)))
    print(json.dumps({"root": str(root), "state": state}, ensure_ascii=False))

def load_state(root: Path):
    state_path, events_path, lock_path = state_paths(root)
    if not state_path.exists():
        raise SystemExit("campaign.json não encontrado")
    return state_path, events_path, lock_path

def transition(args):
    root = Path(args.root).resolve()
    state_path, events_path, lock_path = load_state(root)
    with exclusive_lock(lock_path):
        state = load_json(state_path)
        current = state["state"]
        target = args.to
        if target not in TRANSITIONS.get(current, set()):
            raise SystemExit(f"transição inválida: {current} -> {target}")
        before = sha256_json(state)
        state["state"] = target
        state["version"] += 1
        state["event_version"] += 1
        state["updated_at"] = utc_now()
        state["actor"] = args.actor
        after = sha256_json(state)
        atomic_write_json(state_path, state)
        append_jsonl(events_path, make_event(state, "transition", args.actor, "ok", before, after,
                                              {"from": current, "to": target, "reason": args.reason}))
    print(json.dumps(state, ensure_ascii=False))

def approve(args):
    root = Path(args.root).resolve()
    state_path, events_path, lock_path = load_state(root)
    request = load_json(Path(args.request).resolve())
    with exclusive_lock(lock_path):
        state = load_json(state_path)
        for key in ("campaign_id", "asset_id"):
            if request.get(key) != state.get(key):
                raise SystemExit(f"request diverge em {key}")
        operation = require_id(request.get("operation", ""), "operation")
        digest = request_hash(request)
        approved = datetime.now(timezone.utc)
        approval = {
            "campaign_id": state["campaign_id"],
            "asset_id": state["asset_id"],
            "operation": operation,
            "request_hash": digest,
            "approved_by": args.approver,
            "chat_id": args.chat_id,
            "message_id": args.message_id,
            "approved_at": approved.isoformat().replace("+00:00", "Z"),
            "expires_at": (approved + timedelta(minutes=args.ttl_minutes)).isoformat().replace("+00:00", "Z"),
            "used_at": None,
            "notes": args.notes,
        }
        path = root / "approvals" / f"{operation}-{digest}.json"
        atomic_write_json(path, approval)
        state["event_version"] += 1
        state["updated_at"] = utc_now()
        atomic_write_json(state_path, state)
        append_jsonl(events_path, make_event(state, "approve", args.approver, "ok", None, sha256_json(approval),
                                              {"operation": operation, "request_hash": digest,
                                               "message_id": args.message_id}))
    print(json.dumps({"approval": str(path), "request_hash": digest}, ensure_ascii=False))

def verify(args):
    request = load_json(Path(args.request).resolve())
    approval = load_json(Path(args.approval).resolve())
    validate_approval(request, approval)
    print(json.dumps({"valid": True, "request_hash": request_hash(request)}, ensure_ascii=False))

def status(args):
    root = Path(args.root).resolve()
    state_path, _, _ = load_state(root)
    print(json.dumps(load_json(state_path), ensure_ascii=False))

def parser():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    q = s.add_parser("init")
    q.add_argument("--base", required=True); q.add_argument("--campaign-id", required=True)
    q.add_argument("--asset-id", required=True); q.add_argument("--actor", required=True)
    q.set_defaults(func=init_campaign)
    q = s.add_parser("transition")
    q.add_argument("--root", required=True); q.add_argument("--to", required=True)
    q.add_argument("--actor", required=True); q.add_argument("--reason", required=True)
    q.set_defaults(func=transition)
    q = s.add_parser("approve")
    q.add_argument("--root", required=True); q.add_argument("--request", required=True)
    q.add_argument("--approver", required=True); q.add_argument("--chat-id", required=True)
    q.add_argument("--message-id", required=True); q.add_argument("--ttl-minutes", type=int, default=60)
    q.add_argument("--notes", default="")
    q.set_defaults(func=approve)
    q = s.add_parser("verify")
    q.add_argument("--request", required=True); q.add_argument("--approval", required=True)
    q.set_defaults(func=verify)
    q = s.add_parser("status")
    q.add_argument("--root", required=True); q.set_defaults(func=status)
    return p

if __name__ == "__main__":
    a = parser().parse_args()
    a.func(a)
