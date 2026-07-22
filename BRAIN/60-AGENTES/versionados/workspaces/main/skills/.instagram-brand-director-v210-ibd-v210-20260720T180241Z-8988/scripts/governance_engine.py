#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from runtime_lib import (load_json, load_yaml, request_hash, utc_now,
                         validate_approval, verify_event_stream)

def actor_key(value: str) -> str:
    return value.strip().lower().replace(" ", "_")

def provider_descriptor(registry: dict, kind: str, provider_id: str) -> dict | None:
    group = registry.get("providers", {}).get(kind, {})
    value = group.get(provider_id) if isinstance(group, dict) else None
    return value if isinstance(value, dict) else None

def evaluate(request: dict, actor: str, governance: dict, agents: dict,
             providers: dict, base: Path, approval: dict | None = None,
             event_stream: Path | None = None) -> dict:
    reasons = []
    digest = request_hash(request)
    key = actor_key(actor)
    agent = agents.get("agents", {}).get(key)
    if not isinstance(agent, dict) or agent.get("enabled") is not True:
        reasons.append("actor-disabled-or-unknown")
    kind = str(request.get("provider_kind", ""))
    provider_id = str(request.get("provider_id", ""))
    descriptor = provider_descriptor(providers, kind, provider_id)
    if descriptor is None:
        reasons.append("provider-unknown")
    else:
        if descriptor.get("enabled") is not True:
            reasons.append("provider-disabled")
        adapter = str(descriptor.get("adapter_path", "")).strip()
        if adapter and not (base / adapter).is_file():
            reasons.append("provider-adapter-missing")
    if event_stream is not None:
        try:
            verify_event_stream(event_stream)
        except Exception:
            reasons.append("event-stream-invalid")
    external = bool(descriptor and descriptor.get("external") is True)
    if external:
        if approval is None:
            reasons.append("owner-approval-required")
        else:
            try:
                validate_approval(request, approval, governance)
            except Exception:
                reasons.append("owner-approval-invalid")
    decision = "deny" if reasons else "allow"
    material = {"actor": actor, "operation": request.get("operation"), "provider_kind": kind,
                "provider_id": provider_id, "payload_hash": digest, "decision": decision,
                "reasons": sorted(set(reasons))}
    return {
        "decision_id": hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest(),
        "timestamp_utc": utc_now(),
        **material,
    }

def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser()
    p.add_argument("--request", required=True); p.add_argument("--actor", required=True)
    p.add_argument("--approval"); p.add_argument("--event-stream")
    p.add_argument("--governance", default=str(root/"templates"/"governance.yaml"))
    p.add_argument("--agents", default=str(root/"assets"/"agent-registry.yaml"))
    p.add_argument("--providers", default=str(root/"assets"/"provider-registry.yaml"))
    args = p.parse_args()
    request = load_json(Path(args.request).resolve())
    approval = load_json(Path(args.approval).resolve()) if args.approval else None
    result = evaluate(request, args.actor, load_yaml(Path(args.governance).resolve()),
                      load_yaml(Path(args.agents).resolve()), load_yaml(Path(args.providers).resolve()),
                      root, approval, Path(args.event_stream).resolve() if args.event_stream else None)
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["decision"] == "allow" else 2)

if __name__ == "__main__":
    main()
