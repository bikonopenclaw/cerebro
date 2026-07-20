#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shutil
from pathlib import Path

def check(name, ok, detail):
    return {"name":name,"status":"pass" if ok else "blocked","detail":detail}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--mode",choices=["build","production"],default="build")
    a=p.parse_args()
    base=Path(__file__).resolve().parent.parent
    checks=[]
    for rel in ["scripts/runtime_lib.py","scripts/campaignctl.py","scripts/kling_exec.py",
                "scripts/assetctl.py","scripts/qa_media.py",
                "assets/schemas/campaign.schema.json","assets/schemas/operation-request.schema.json",
                "assets/schemas/approval.schema.json","assets/schemas/event.schema.json",
                "assets/schemas/adapter-result.schema.json"]:
        checks.append(check(rel,(base/rel).is_file(),"presente" if (base/rel).is_file() else "ausente"))
    for binary in ["python3","ffprobe","file","chromium"]:
        path=shutil.which(binary); checks.append(check(binary,bool(path),path or "ausente"))
    for rel in ["assets/schemas/campaign.schema.json","assets/schemas/operation-request.schema.json",
                "assets/schemas/approval.schema.json","assets/schemas/event.schema.json",
                "assets/schemas/adapter-result.schema.json","templates/kling-contract.json"]:
        try:
            json.loads((base/rel).read_text()); ok=True; detail="JSON válido"
        except Exception as e:
            ok=False; detail=str(e)
        checks.append(check("parse:"+rel,ok,detail))
    if a.mode=="production":
        kling=shutil.which("kling"); checks.append(check("kling",bool(kling),kling or "ausente"))
        contract=json.loads((base/"templates/kling-contract.json").read_text())
        checks.append(check("kling-contract",contract.get("production_enabled") is True,
                            "habilitado" if contract.get("production_enabled") else "bloqueado"))
        try:
            import yaml
            tm=yaml.safe_load((base/"templates/template-map.yaml").read_text())
            enabled=tm.get("production_enabled") is True and bool(tm.get("formats"))
            checks.append(check("template-map",enabled,"habilitado" if enabled else "bloqueado"))
        except Exception as e:
            checks.append(check("template-map",False,str(e)))
        for env in ["CREATOMATE_API_KEY","BUFFER_ACCESS_TOKEN","BUFFER_PROFILE_ID"]:
            checks.append(check("env:"+env,bool(os.getenv(env)),"presente" if os.getenv(env) else "ausente"))
    status="pass" if all(x["status"]=="pass" for x in checks) else "blocked"
    print(json.dumps({"mode":a.mode,"status":status,"checks":checks},ensure_ascii=False))
    raise SystemExit(0 if status=="pass" else 2)

if __name__=="__main__":
    main()
