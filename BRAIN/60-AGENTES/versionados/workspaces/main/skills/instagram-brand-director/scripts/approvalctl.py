#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from runtime_lib import (append_event, atomic_write_json, canonical_bytes, consume_approval,
                         exclusive_lock, finish_approval_execution, load_json, load_yaml,
                         request_hash, require_id, reserve_approval, start_approval_execution,
                         utc_now, validate_approval, validate_owner_event)

def emit(events: str | None, request: dict, approval: dict, action: str, result: str, actor: str, detail: dict):
    if not events: return None
    return append_event(Path(events).resolve(), {
        "correlation_id": str(request.get("correlation_id", approval.get("approval_id", ""))),
        "campaign_id": request["campaign_id"], "asset_id": request["asset_id"],
        "event_version": request["asset_version"], "actor": actor, "action": action,
        "result": result, "before_hash": None, "after_hash": request_hash(request),
        "detail": detail,
    })

def record(args):
    request = load_json(Path(args.request).resolve())
    governance = load_yaml(Path(args.governance).resolve())
    event = load_json(Path(args.owner_event).resolve())
    validate_owner_event(event, governance)
    for key in ("campaign_id", "asset_id", "operation", "destination"):
        require_id(str(request.get(key, "")), key)
    version = request.get("asset_version")
    if not isinstance(version, int) or version < 1: raise ValueError("asset_version inválida")
    digest = request_hash(request); approved = datetime.now(timezone.utc)
    ttl = min(max(args.ttl_minutes, 1), 1440); owner = governance["owner"]
    approval = {
        "approval_id": hashlib.sha256(canonical_bytes(event) + digest.encode()).hexdigest(),
        "status": "approved", "campaign_id": request["campaign_id"], "asset_id": request["asset_id"],
        "asset_version": version, "action": request["operation"], "destination": request["destination"],
        "provider_kind": request.get("provider_kind", ""), "provider_id": request.get("provider_id", ""),
        "payload_hash": digest, "approved_by_role": "proprietário", "approved_by_id": str(owner["id"]),
        "approved_channel": owner["channel"], "approved_chat_id": str(owner["chat_id"]),
        "approved_by_reference": str(event["message_id"]),
        "owner_message_hash": hashlib.sha256(str(event["text"]).encode("utf-8")).hexdigest(),
        "approved_at": approved.isoformat().replace("+00:00", "Z"),
        "expires_at": (approved + timedelta(minutes=ttl)).isoformat().replace("+00:00", "Z"),
        "revoked_at": None, "reserved_at": None, "execution_id": "",
        "execution_started_at": None, "completed_at": None, "outcome": None,
        "result_event_id": "", "consumed_at": None, "notes": args.notes,
    }
    out = Path(args.output).resolve()
    with exclusive_lock(out.with_name(out.name + ".lock")):
        if out.exists(): raise SystemExit("approval já existe")
        atomic_write_json(out, approval)
    stored = emit(args.events, request, approval, "approval-recorded", "ok", args.actor,
                  {"approval_id": approval["approval_id"]})
    print(json.dumps({"approval": str(out), "approval_id": approval["approval_id"],
                      "payload_hash": digest, "event_id": stored["event_id"] if stored else None}, ensure_ascii=False))

def verify(args):
    request=load_json(Path(args.request).resolve()); approval=load_json(Path(args.approval).resolve())
    validate_approval(request,approval,load_yaml(Path(args.governance).resolve()))
    print(json.dumps({"valid":True,"approval_id":approval["approval_id"],"payload_hash":request_hash(request)},ensure_ascii=False))

def consume(args):
    request=load_json(Path(args.request).resolve()); governance=load_yaml(Path(args.governance).resolve())
    approval=consume_approval(Path(args.approval).resolve(),request,governance)
    stored=emit(args.events,request,approval,"approval-consumed-legacy","ok",args.actor,{"approval_id":approval["approval_id"]})
    print(json.dumps({"consumed":True,"approval_id":approval["approval_id"],"consumed_at":approval["consumed_at"],
                      "event_id":stored["event_id"] if stored else None},ensure_ascii=False))

def reserve(args):
    request=load_json(Path(args.request).resolve()); governance=load_yaml(Path(args.governance).resolve())
    approval=reserve_approval(Path(args.approval).resolve(),request,governance,args.execution_id)
    stored=emit(args.events,request,approval,"approval-reserved","ok",args.actor,{"approval_id":approval["approval_id"],"execution_id":args.execution_id})
    print(json.dumps({"reserved":True,"approval_id":approval["approval_id"],"execution_id":args.execution_id,
                      "event_id":stored["event_id"] if stored else None},ensure_ascii=False))

def start(args):
    request=load_json(Path(args.request).resolve())
    approval=start_approval_execution(Path(args.approval).resolve(),args.execution_id)
    stored=emit(args.events,request,approval,"external-action-started","executing",args.actor,{"approval_id":approval["approval_id"],"execution_id":args.execution_id})
    print(json.dumps({"executing":True,"approval_id":approval["approval_id"],"execution_id":args.execution_id,
                      "event_id":stored["event_id"] if stored else None},ensure_ascii=False))

def finish(args):
    request=load_json(Path(args.request).resolve()); approval_path=Path(args.approval).resolve()
    current=load_json(approval_path)
    stored=emit(args.events,request,current,"external-action-result",args.outcome,args.actor,
                {"approval_id":current["approval_id"],"execution_id":args.execution_id,"evidence":args.evidence})
    if stored is None: raise ValueError("--events obrigatório para concluir execução")
    approval=finish_approval_execution(approval_path,args.execution_id,args.outcome,stored["event_id"])
    print(json.dumps({"completed":True,"approval_id":approval["approval_id"],"outcome":args.outcome,
                      "event_id":stored["event_id"]},ensure_ascii=False))

def revoke(args):
    path=Path(args.approval).resolve()
    with exclusive_lock(path.with_name(path.name+".lock")):
        approval=load_json(path)
        if approval.get("status") not in {"pending","approved"}: raise SystemExit("approval não pode ser revogado neste estado")
        approval["revoked_at"]=utc_now(); approval["status"]="revoked"; atomic_write_json(path,approval)
    print(json.dumps({"revoked":True,"approval_id":approval["approval_id"]},ensure_ascii=False))

def common(q, governance=True):
    q.add_argument("--request",required=True); q.add_argument("--approval",required=True)
    if governance: q.add_argument("--governance",required=True)
    q.add_argument("--events"); q.add_argument("--actor",default="Puppet Master")

def parser():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    q=s.add_parser("record"); q.add_argument("--request",required=True); q.add_argument("--owner-event",required=True)
    q.add_argument("--governance",required=True); q.add_argument("--output",required=True)
    q.add_argument("--ttl-minutes",type=int,default=60); q.add_argument("--notes",default="")
    q.add_argument("--events"); q.add_argument("--actor",default="Puppet Master"); q.set_defaults(func=record)
    q=s.add_parser("verify"); common(q); q.set_defaults(func=verify)
    q=s.add_parser("consume"); common(q); q.set_defaults(func=consume)
    q=s.add_parser("reserve"); common(q); q.add_argument("--execution-id",required=True); q.set_defaults(func=reserve)
    q=s.add_parser("start"); common(q,governance=False); q.add_argument("--execution-id",required=True); q.set_defaults(func=start)
    q=s.add_parser("finish"); common(q,governance=False); q.add_argument("--execution-id",required=True)
    q.add_argument("--outcome",choices=["succeeded","failed","indeterminate"],required=True); q.add_argument("--evidence",default=""); q.set_defaults(func=finish)
    q=s.add_parser("revoke"); q.add_argument("--approval",required=True); q.set_defaults(func=revoke)
    return p

if __name__=="__main__":
    a=parser().parse_args(); a.func(a)
