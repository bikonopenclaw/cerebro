#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from runtime_lib import append_event, load_json, read_event_stream, verify_event_stream

def command_append(args):
    value = load_json(Path(args.event).resolve())
    stored = append_event(Path(args.stream).resolve(), value)
    print(json.dumps(stored, ensure_ascii=False))

def command_verify(args):
    print(json.dumps(verify_event_stream(Path(args.stream).resolve()), ensure_ascii=False))

def command_replay(args):
    events = read_event_stream(Path(args.stream).resolve())
    verify_event_stream(Path(args.stream).resolve())
    projection = {"state": None, "events": len(events), "head_hash": events[-1]["event_hash"] if events else ""}
    for event in events:
        detail = event.get("detail", {})
        if event.get("action") == "transition" and isinstance(detail, dict):
            projection["state"] = detail.get("to", projection["state"])
        if event.get("action") == "init":
            projection["state"] = "intake"
    print(json.dumps(projection, ensure_ascii=False))

def parser():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    q = s.add_parser("append"); q.add_argument("--stream", required=True); q.add_argument("--event", required=True); q.set_defaults(func=command_append)
    q = s.add_parser("verify"); q.add_argument("--stream", required=True); q.set_defaults(func=command_verify)
    q = s.add_parser("replay"); q.add_argument("--stream", required=True); q.set_defaults(func=command_replay)
    return p

if __name__ == "__main__":
    args = parser().parse_args()
    args.func(args)
