#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json, re, sys
from pathlib import Path
try:
    import yaml
except Exception:
    yaml=None

EXPECTED_NAME="instagram-brand-director"; EXPECTED_VERSION="2.1.0"
REQUIRED=[
"SKILL.md","assets/production-manifest.yaml","assets/approval-record.yaml","assets/agent-registry.yaml","assets/provider-registry.yaml",
"assets/schemas/campaign.schema.json","assets/schemas/operation-request.schema.json","assets/schemas/approval.schema.json",
"assets/schemas/event.schema.json","assets/schemas/adapter-result.schema.json","assets/schemas/provider.schema.json",
"assets/schemas/asset.schema.json","assets/schemas/governance-decision.schema.json","assets/schemas/playbook-run.schema.json",
"references/architecture-v2.1.md","references/provider-system.md","references/event-sourcing.md","references/asset-pipeline.md",
"references/governance-engine.md","references/playbooks-and-roles.md","references/acceptance-matrix.md",
"references/compatibility-report.md","references/migration-v2.0.1-to-v2.1.0.md",
"scripts/runtime_lib.py","scripts/event_store.py","scripts/campaignctl.py","scripts/approvalctl.py","scripts/governance_engine.py",
"scripts/providerctl.py","scripts/asset_pipeline.py","scripts/kling_exec.py","scripts/assetctl.py","scripts/qa_media.py",
"scripts/preflight.py","scripts/validate_skill.py","scripts/tests/test_runtime.py","scripts/tests/test_preflight.py",
"scripts/tests/test_event_store.py","scripts/tests/test_governance_engine.py","scripts/tests/test_asset_pipeline.py",
"scripts/tests/test_compatibility.py","templates/governance.yaml","templates/kling-contract.json",
"templates/template-map.yaml","templates/publishing-contract.yaml"]
ALLOWED_FRONTMATTER={"name","description"}

def main():
    p=argparse.ArgumentParser(); p.add_argument("root",nargs="?",default="."); root=Path(p.parse_args().root).resolve(); errors=[]
    for rel in REQUIRED:
        if not (root/rel).is_file(): errors.append("arquivo obrigatório ausente: "+rel)
    skill=(root/"SKILL.md").read_text(encoding="utf-8") if (root/"SKILL.md").is_file() else ""
    m=re.match(r"\A---\s*\n(.*?)\n---\s*\n",skill,re.S)
    if not m: errors.append("frontmatter ausente")
    else:
        try:
            if yaml is None: raise ValueError("PyYAML ausente")
            fm=yaml.safe_load(m.group(1))
            if not isinstance(fm,dict): raise ValueError("frontmatter não é mapa")
            extra=set(fm)-ALLOWED_FRONTMATTER
            if extra: errors.append("chaves não aceitas no frontmatter: "+",".join(sorted(extra)))
            if fm.get("name")!=EXPECTED_NAME: errors.append("name inválido")
            if not str(fm.get("description","")).strip(): errors.append("description ausente")
        except Exception as e: errors.append("frontmatter inválido: "+str(e))
    if f"Instagram Brand Director {EXPECTED_VERSION}" not in skill: errors.append("versão não encontrada no título")
    for ref in re.findall(r"\{baseDir\}/([^\x60\s]+)",skill):
        if not (root/ref).exists(): errors.append("referência inexistente: "+ref)
    for pth in sorted((root/"scripts").rglob("*.py")):
        try: ast.parse(pth.read_text(encoding="utf-8"))
        except Exception as e: errors.append(f"Python inválido em {pth.name}: {e}")
    for pth in sorted((root/"assets"/"schemas").glob("*.json"))+sorted((root/"templates").glob("*.json")):
        try: json.loads(pth.read_text(encoding="utf-8"))
        except Exception as e: errors.append(f"JSON inválido em {pth.name}: {e}")
    if yaml is not None:
        for pth in sorted((root/"assets").glob("*.yaml"))+sorted((root/"templates").glob("*.yaml")):
            try:
                if not isinstance(yaml.safe_load(pth.read_text(encoding="utf-8")),dict): raise ValueError("mapa obrigatório")
            except Exception as e: errors.append(f"YAML inválido em {pth.relative_to(root)}: {e}")
        try:
            providers=yaml.safe_load((root/"assets/provider-registry.yaml").read_text(encoding="utf-8"))
            if set(providers.get("provider_kinds",[]))!={"image","video","tts","storage","publication","search"}: errors.append("tipos de provider inválidos")
            for kind,items in providers.get("providers",{}).items():
                for provider_id,item in items.items():
                    if item.get("external") and item.get("enabled"): errors.append(f"provider externo habilitado: {kind}:{provider_id}")
            agents=yaml.safe_load((root/"assets/agent-registry.yaml").read_text(encoding="utf-8")).get("agents",{})
            for key in ("skipper","rico","private"):
                if agents.get(key,{}).get("enabled") is not False: errors.append(f"agente opcional habilitado: {key}")
        except Exception as e: errors.append("registry inválido: "+str(e))
    manifest=(root/"assets/production-manifest.yaml").read_text(encoding="utf-8")
    for item in ('skill_version: "2.1.0"','external_action_lock: true','status: "not-submitted"'):
        if item not in manifest: errors.append("manifesto sem campo: "+item)
    if list(root.rglob("*.pyc")): errors.append("arquivos compilados não permitidos")
    if errors:
        for e in errors: print("ERRO:",e)
        return 1
    print(f"OK: {EXPECTED_NAME} v{EXPECTED_VERSION} validada em {root}")
    return 0

if __name__=="__main__": sys.exit(main())
