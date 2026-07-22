#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json, os, re, shutil
from pathlib import Path
try:
    import yaml
except Exception:
    yaml=None

REQUIRED=[
"SKILL.md","assets/production-manifest.yaml","assets/approval-record.yaml","assets/agent-registry.yaml","assets/provider-registry.yaml",
"assets/schemas/campaign.schema.json","assets/schemas/operation-request.schema.json","assets/schemas/approval.schema.json",
"assets/schemas/event.schema.json","assets/schemas/adapter-result.schema.json","assets/schemas/provider.schema.json",
"assets/schemas/asset.schema.json","assets/schemas/governance-decision.schema.json","assets/schemas/playbook-run.schema.json",
"scripts/runtime_lib.py","scripts/event_store.py","scripts/campaignctl.py","scripts/approvalctl.py","scripts/governance_engine.py",
"scripts/providerctl.py","scripts/asset_pipeline.py","scripts/kling_exec.py","scripts/assetctl.py","scripts/qa_media.py",
"scripts/preflight.py","scripts/validate_skill.py","templates/governance.yaml","templates/kling-contract.json",
"templates/template-map.yaml","templates/publishing-contract.yaml",
"references/architecture-v2.1.md","references/provider-system.md","references/event-sourcing.md",
"references/asset-pipeline.md","references/governance-engine.md","references/playbooks-and-roles.md",
"references/compatibility-report.md","references/migration-v2.0.1-to-v2.1.0.md",
"references/playbooks/intake-to-release.md","references/playbooks/qa.md",
"references/playbooks/external-action.md"]
LEGACY={
"creatomate":r"\bcreatomate\b","buffer":r"\bbuffer\b","elevenlabs":r"\belevenlabs\b",
"cloudflare r2":r"\bcloudflare\s+r2\b","figma":r"\bfigma\b","remotion":r"\bremotion\b",
"exa":r"\bexa\b","firecrawl":r"\bfirecrawl\b","hermes":r"\bhermes\b"}

def check(name,ok,detail): return {"name":name,"status":"pass" if ok else "blocked","detail":detail}
def binary(name):
    path=shutil.which(name); return check("binary:"+name,bool(path),path or "ausente")

def parse_files(base,checks):
    for rel in REQUIRED:
        p=base/rel; checks.append(check("file:"+rel,p.is_file(),"presente" if p.is_file() else "ausente"))
    for p in sorted((base/"assets"/"schemas").glob("*.json"))+sorted((base/"templates").glob("*.json")):
        try: json.loads(p.read_text(encoding="utf-8")); ok=True; detail="JSON válido"
        except Exception as e: ok=False; detail=str(e)
        checks.append(check("parse:"+str(p.relative_to(base)),ok,detail))
    yaml_files=sorted((base/"assets").glob("*.yaml"))+sorted((base/"templates").glob("*.yaml"))
    for p in yaml_files:
        try:
            if yaml is None: raise ValueError("PyYAML ausente")
            value=yaml.safe_load(p.read_text(encoding="utf-8"))
            if not isinstance(value,dict): raise ValueError("mapa YAML obrigatório")
            ok=True; detail="YAML válido"
        except Exception as e: ok=False; detail=str(e)
        checks.append(check("parse:"+str(p.relative_to(base)),ok,detail))
    for p in sorted((base/"scripts").rglob("*.py")):
        try: ast.parse(p.read_text(encoding="utf-8")); ok=True; detail="Python válido"
        except Exception as e: ok=False; detail=str(e)
        checks.append(check("syntax:"+str(p.relative_to(base)),ok,detail))

def registries(base,checks):
    try:
        providers=yaml.safe_load((base/"assets/provider-registry.yaml").read_text(encoding="utf-8"))
        kinds=set(providers.get("provider_kinds",[])); expected={"image","video","tts","storage","publication","search"}
        checks.append(check("providers:kinds",kinds==expected,",".join(sorted(kinds))))
        external_enabled=[]
        for kind,values in providers.get("providers",{}).items():
            for provider_id,item in values.items():
                if item.get("external") and item.get("enabled"): external_enabled.append(f"{kind}:{provider_id}")
        checks.append(check("providers:external-default-disabled",not external_enabled,",".join(external_enabled) or "todos bloqueados"))
    except Exception as e: checks.append(check("providers:registry",False,str(e)))
    try:
        agents=yaml.safe_load((base/"assets/agent-registry.yaml").read_text(encoding="utf-8")).get("agents",{})
        for key in ("skipper","rico","private"):
            checks.append(check("agent:"+key+":disabled",agents.get(key,{}).get("enabled") is False,"desabilitado por padrão"))
        for key in ("puppet_master","robotnik","kowalski"):
            checks.append(check("agent:"+key+":canonical",agents.get(key,{}).get("enabled") is True and agents.get(key,{}).get("canonical") is True,"canônico"))
    except Exception as e: checks.append(check("agents:registry",False,str(e)))

def owner_ready(base):
    try:
        g=yaml.safe_load((base/"templates/governance.yaml").read_text(encoding="utf-8")); o=g.get("owner",{})
        ok=g.get("external_action_lock") is True and o.get("role")=="proprietário" and all(str(o.get(k,"")).strip() for k in ("id","channel","chat_id"))
        return ok,"configurado" if ok else "identidade ou lock incompleto"
    except Exception as e: return False,str(e)

def format_enabled(base,kind):
    try:
        tm=yaml.safe_load((base/"templates/template-map.yaml").read_text(encoding="utf-8")); values=tm.get("formats",{}).get(kind,{})
        ok=tm.get("production_enabled") is True and isinstance(values,dict) and bool(values)
        return ok,"habilitado" if ok else f"formato {kind} não configurado"
    except Exception as e: return False,str(e)

def build_checks(base:Path,mode:str,operation:str):
    checks=[]; parse_files(base,checks); registries(base,checks)
    operational=[base/"SKILL.md",*sorted((base/"references").rglob("*.md")),base/"assets/production-manifest.yaml"]
    for p in operational:
        text=p.read_text(encoding="utf-8").lower()
        for term,pattern in LEGACY.items():
            found=re.search(pattern,text,re.I) is not None
            checks.append(check("legacy:"+term+":"+str(p.relative_to(base)),not found,"dependência legada" if found else "ausente"))
    if mode=="build": return checks
    checks.append(binary("python3")); ok,detail=owner_ready(base); checks.append(check("owner-binding",ok,detail))
    if operation=="generation":
        checks.append(binary("kling"))
        try:
            c=json.loads((base/"templates/kling-contract.json").read_text()); ok=c.get("production_enabled") is True and bool(c.get("operations")); detail="contrato válido" if ok else "bloqueado"
        except Exception as e: ok=False; detail=str(e)
        checks.append(check("kling-contract",ok,detail))
        checks.append(check("provider:video:kling-cli",False,"provider externo desabilitado por padrão"))
    if operation in ("static","composition"):
        image_tool=shutil.which("magick") or shutil.which("convert")
        checks.append(check("imagemagick",bool(image_tool),image_tool or "ausente"))
        ok,detail=format_enabled(base,"static"); checks.append(check("templates:static",ok,detail))
    if operation in ("video","composition"):
        checks.extend([binary("ffmpeg"),binary("ffprobe")]); ok,detail=format_enabled(base,"video"); checks.append(check("templates:video",ok,detail))
    if operation in ("motion","composition"):
        checks.extend([binary("node"),binary("npx")]); raw=os.environ.get("MOTION_CANVAS_PROJECT_DIR","").strip()
        project=Path(raw).expanduser() if raw else Path("/nonexistent"); package=project/"package.json"; ok=bool(raw) and package.is_file()
        if ok:
            try: ok="motion-canvas" in package.read_text(encoding="utf-8").lower()
            except Exception: ok=False
        checks.append(check("motion-canvas-project",ok,str(project) if ok else "ausente ou inválido"))
        enabled,detail=format_enabled(base,"motion"); checks.append(check("templates:motion",enabled,detail))
    if operation=="publish":
        try:
            pc=yaml.safe_load((base/"templates/publishing-contract.yaml").read_text(encoding="utf-8")); adapter=Path(str(pc.get("adapter_path",""))).expanduser()
            ok=pc.get("production_enabled") is True and adapter.is_file(); detail=str(adapter) if ok else "adapter de publicação bloqueado"
        except Exception as e: ok=False; detail=str(e)
        checks.append(check("publishing-adapter",ok,detail))
        checks.append(check("provider:publication:instagram",False,"provider externo desabilitado por padrão"))
        checks.append(check("env:INSTAGRAM_ACCESS_TOKEN",bool(os.getenv("INSTAGRAM_ACCESS_TOKEN")),"presente" if os.getenv("INSTAGRAM_ACCESS_TOKEN") else "ausente"))
    return checks

def main():
    p=argparse.ArgumentParser(); p.add_argument("--mode",choices=["build","production"],default="build")
    p.add_argument("--operation",choices=["advisory","generation","static","motion","video","composition","manual-handoff","publish"],default="advisory")
    a=p.parse_args(); base=Path(__file__).resolve().parent.parent; checks=build_checks(base,a.mode,a.operation)
    status="pass" if all(x["status"]=="pass" for x in checks) else "blocked"
    print(json.dumps({"mode":a.mode,"operation":a.operation,"status":status,"checks":checks},ensure_ascii=False))
    raise SystemExit(0 if status=="pass" else 2)

if __name__=="__main__": main()
