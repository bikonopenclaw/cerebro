#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path
from runtime_lib import (TRANSITIONS, append_event, atomic_write_json, exclusive_lock,
                         load_json, make_event, require_id, sha256_json, utc_now,
                         verify_event_stream)

def state_paths(root: Path):
    return root/"campaign.json", root/"events.jsonl", root/".campaign.lock"

def init_campaign(args):
    require_id(args.campaign_id,"campaign_id"); require_id(args.asset_id,"asset_id")
    root=Path(args.base).resolve()/args.campaign_id; state_path,events_path,lock_path=state_paths(root)
    with exclusive_lock(lock_path):
        if state_path.exists(): raise SystemExit("campanha já existe")
        for d in ("prompts","generated","renders","release-candidate","approvals","requests","qa","external-actions","assets","governance-decisions","playbooks"):
            (root/d).mkdir(parents=True,exist_ok=True)
        state={"campaign_id":args.campaign_id,"correlation_id":hashlib.sha256(os.urandom(32)).hexdigest(),
               "asset_id":args.asset_id,"asset_version":1,"version":1,"event_version":1,
               "state":"intake","created_at":utc_now(),"updated_at":utc_now(),"actor":args.actor,
               "event_head_hash":""}
        event=append_event(events_path,make_event(state,"init",args.actor,"ok",None,sha256_json(state)))
        state["event_head_hash"]=event["event_hash"]; atomic_write_json(state_path,state)
    print(json.dumps({"root":str(root),"state":state},ensure_ascii=False))

def load_state(root: Path):
    state_path,events_path,lock_path=state_paths(root)
    if not state_path.exists(): raise SystemExit("campaign.json não encontrado")
    return state_path,events_path,lock_path

def transition(args):
    root=Path(args.root).resolve(); state_path,events_path,lock_path=load_state(root)
    with exclusive_lock(lock_path):
        verify_event_stream(events_path); state=load_json(state_path); current=state["state"]; target=args.to
        if target not in TRANSITIONS.get(current,set()): raise SystemExit(f"transição inválida: {current} -> {target}")
        before=sha256_json(state); state["state"]=target; state["version"]+=1; state["event_version"]+=1
        state["updated_at"]=utc_now(); state["actor"]=args.actor
        projected=dict(state); projected["event_head_hash"]=""
        after=sha256_json(projected)
        event=append_event(events_path,make_event(state,"transition",args.actor,"ok",before,after,{"from":current,"to":target,"reason":args.reason}))
        state["event_head_hash"]=event["event_hash"]; atomic_write_json(state_path,state)
    print(json.dumps(state,ensure_ascii=False))

def status(args):
    root=Path(args.root).resolve(); state_path,events_path,_=load_state(root)
    state=load_json(state_path); stream=verify_event_stream(events_path)
    if state.get("event_head_hash")!=stream["head_hash"]: raise SystemExit("projeção diverge do event stream")
    print(json.dumps(state,ensure_ascii=False))

def parser():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    q=s.add_parser("init"); q.add_argument("--base",required=True); q.add_argument("--campaign-id",required=True)
    q.add_argument("--asset-id",required=True); q.add_argument("--actor",required=True); q.set_defaults(func=init_campaign)
    q=s.add_parser("transition"); q.add_argument("--root",required=True); q.add_argument("--to",required=True)
    q.add_argument("--actor",required=True); q.add_argument("--reason",required=True); q.set_defaults(func=transition)
    q=s.add_parser("status"); q.add_argument("--root",required=True); q.set_defaults(func=status)
    return p

if __name__=="__main__":
    a=parser().parse_args(); a.func(a)
