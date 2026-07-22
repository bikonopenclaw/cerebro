#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from runtime_lib import (append_event, atomic_write_json, exclusive_lock, load_json,
                         require_id, utc_now)

STAGES = {
    "source": {"generated", "selected", "blocked"},
    "generated": {"selected", "blocked"},
    "selected": {"composed", "qa", "blocked"},
    "composed": {"qa", "blocked"},
    "qa": {"release-candidate", "blocked"},
    "release-candidate": {"archived", "blocked"},
    "archived": set(),
    "blocked": set(),
}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def record_path(root: Path, asset_id: str, version: int) -> Path:
    return root / "assets" / asset_id / f"v{version}.json"

def register(args):
    require_id(args.campaign_id, "campaign_id"); require_id(args.asset_id, "asset_id")
    if args.version < 1: raise ValueError("version inválida")
    source = Path(args.path).resolve()
    if not source.is_file(): raise ValueError("asset não encontrado")
    root = Path(args.root).resolve()
    record = record_path(root, args.asset_id, args.version)
    with exclusive_lock(record.with_suffix(".lock")):
        if record.exists(): raise ValueError("asset/version já registrado")
        now = utc_now()
        data = {"asset_id": args.asset_id, "campaign_id": args.campaign_id, "version": args.version,
                "stage": "source", "path": str(source), "sha256": digest(source),
                "size": source.stat().st_size, "mime": args.mime, "created_at": now,
                "updated_at": now, "lineage": []}
        atomic_write_json(record, data)
        event = append_event(root/"events.jsonl", {"correlation_id": args.correlation_id,
            "campaign_id": args.campaign_id, "asset_id": args.asset_id, "event_version": 1,
            "actor": args.actor, "action": "asset-registered", "result": "ok",
            "before_hash": None, "after_hash": data["sha256"], "detail": {"version": args.version, "stage": "source"}})
    print(json.dumps({"record": str(record), "event_id": event["event_id"], "asset": data}, ensure_ascii=False))

def verify_record(data: dict) -> None:
    path = Path(data["path"])
    if not path.is_file(): raise ValueError("asset ausente")
    if path.stat().st_size != data["size"] or digest(path) != data["sha256"]:
        raise ValueError("asset divergiu do registro")

def promote(args):
    root = Path(args.root).resolve()
    record = record_path(root, args.asset_id, args.version)
    with exclusive_lock(record.with_suffix(".lock")):
        data = load_json(record); verify_record(data)
        current = data["stage"]
        if args.to not in STAGES.get(current, set()):
            raise ValueError(f"promoção inválida: {current} -> {args.to}")
        before = data["sha256"]; data["stage"] = args.to; data["updated_at"] = utc_now()
        data["lineage"].append({"from_stage": current, "to_stage": args.to, "actor": args.actor,
                                "timestamp_utc": data["updated_at"], "reason": args.reason})
        atomic_write_json(record, data)
        event = append_event(root/"events.jsonl", {"correlation_id": args.correlation_id,
            "campaign_id": data["campaign_id"], "asset_id": data["asset_id"], "event_version": args.version,
            "actor": args.actor, "action": "asset-promoted", "result": "ok",
            "before_hash": before, "after_hash": data["sha256"],
            "detail": {"from": current, "to": args.to, "version": args.version, "reason": args.reason}})
    print(json.dumps({"event_id": event["event_id"], "asset": data}, ensure_ascii=False))

def status(args):
    data = load_json(record_path(Path(args.root).resolve(), args.asset_id, args.version))
    verify_record(data)
    print(json.dumps(data, ensure_ascii=False))

def parser():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    q=s.add_parser("register")
    for name in ("root","campaign-id","asset-id","correlation-id","actor","path"): q.add_argument("--"+name,required=True)
    q.add_argument("--version",type=int,default=1); q.add_argument("--mime",default="application/octet-stream"); q.set_defaults(func=register)
    q=s.add_parser("promote")
    for name in ("root","asset-id","correlation-id","actor","to","reason"): q.add_argument("--"+name,required=True)
    q.add_argument("--version",type=int,default=1); q.set_defaults(func=promote)
    q=s.add_parser("status"); q.add_argument("--root",required=True); q.add_argument("--asset-id",required=True); q.add_argument("--version",type=int,default=1); q.set_defaults(func=status)
    return p

if __name__=="__main__":
    a=parser().parse_args(); a.func(a)
