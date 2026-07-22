#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from runtime_lib import load_yaml

def flatten(registry: dict):
    rows = []
    for kind, providers in sorted(registry.get("providers", {}).items()):
        for provider_id, descriptor in sorted(providers.items()):
            rows.append({"kind": kind, "provider_id": provider_id, **descriptor})
    return rows

def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["list", "preflight", "execute"])
    p.add_argument("--registry", default=str(root/"assets"/"provider-registry.yaml"))
    args = p.parse_args()
    rows = flatten(load_yaml(Path(args.registry).resolve()))
    if args.command == "list":
        print(json.dumps({"providers": rows}, ensure_ascii=False)); return
    if args.command == "execute":
        print(json.dumps({"status": "blocked", "reason": "providerctl não executa providers"}, ensure_ascii=False))
        raise SystemExit(2)
    problems = []
    for row in rows:
        if row.get("external") and row.get("enabled"):
            problems.append(f"provider externo habilitado: {row['kind']}:{row['provider_id']}")
        if any(key.lower() in {"token", "secret", "password", "credential", "endpoint"} for key in row):
            problems.append(f"campo sensível no provider: {row['kind']}:{row['provider_id']}")
    print(json.dumps({"status": "pass" if not problems else "blocked", "problems": problems,
                      "providers": len(rows)}, ensure_ascii=False))
    raise SystemExit(0 if not problems else 2)

if __name__ == "__main__":
    main()
