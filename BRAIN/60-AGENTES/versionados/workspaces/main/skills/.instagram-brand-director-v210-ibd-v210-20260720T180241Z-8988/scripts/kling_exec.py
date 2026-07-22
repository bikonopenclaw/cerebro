#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shutil, subprocess
from pathlib import Path
from governance_engine import evaluate, provider_descriptor
from runtime_lib import (append_event, finish_approval_execution, load_json, load_yaml,
                         request_hash, reserve_approval, start_approval_execution, utc_now)

DISCOVERY={"who_am_i","account","tool_list"}
TASK_ID_RE=re.compile(r"^[A-Za-z0-9._:-]{1,200}$")

def load_contract(path: Path) -> dict:
    data=load_json(path)
    if not data.get("production_enabled"): raise ValueError("contrato Kling ainda não está habilitado")
    return data

def build_argv(request: dict,kling: str,contract_path: Path) -> list[str]:
    if request.get("tool")!="kling" or request.get("destination")!="kling": raise ValueError("tool e destination precisam ser kling")
    operation=request.get("operation")
    if operation in DISCOVERY: return [kling,operation]
    if operation=="query_tasks":
        task_id=request.get("parameters",{}).get("task_id","")
        if not TASK_ID_RE.fullmatch(task_id): raise ValueError("task_id inválido")
        return [kling,"query_tasks",task_id]
    contract=load_contract(contract_path); spec=contract.get("operations",{}).get(operation)
    if not isinstance(spec,dict): raise ValueError("operação não autorizada pelo contrato")
    params=request.get("parameters")
    if not isinstance(params,dict): raise ValueError("parameters precisa ser objeto")
    flags=spec.get("flags",{}); positionals=spec.get("positionals",[])
    if not isinstance(flags,dict) or not isinstance(positionals,list): raise ValueError("contrato inválido")
    if len(positionals)!=len(set(positionals)) or set(flags)&set(positionals): raise ValueError("parâmetros duplicados no contrato")
    required=set(spec.get("required",[])); allowed=set(flags)|set(positionals)
    if not required<=allowed: raise ValueError("required fora do contrato")
    missing=required-params.keys()
    if missing: raise ValueError("parâmetros obrigatórios ausentes: "+",".join(sorted(missing)))
    unknown=set(params)-allowed
    if unknown: raise ValueError("parâmetros não autorizados: "+",".join(sorted(unknown)))
    argv=[kling,operation]
    for key in sorted(set(params)-set(positionals)):
        value,flag=params[key],flags[key]
        if not isinstance(flag,str) or not flag.startswith("--"): raise ValueError("flag inválida")
        if isinstance(value,bool):
            if value: argv.append(flag)
        elif isinstance(value,(str,int,float)):
            rendered=str(value)
            if rendered.startswith("--"): raise ValueError(f"valor inválido em {key}")
            argv.extend([flag,rendered])
        elif isinstance(value,list) and all(isinstance(v,str) for v in value):
            if any(v.startswith("--") for v in value): raise ValueError(f"valor inválido em {key}")
            for item in value: argv.extend([flag,item])
        else: raise ValueError(f"tipo inválido em {key}")
    for key in positionals:
        if key not in params: continue
        value=params[key]
        if isinstance(value,bool) or not isinstance(value,(str,int,float)): raise ValueError(f"tipo inválido em {key}")
        rendered=str(value)
        if not rendered.strip() or rendered.startswith("--"): raise ValueError(f"positional inválido em {key}")
        argv.append(rendered)
    return argv

def sanitize(text: str) -> str:
    return re.sub(r"(?i)(token|secret|password|authorization)[=: ]+\S+",r"\1=[REDACTED]",text)

def deny_provider(request: dict, actor: str, reason: str) -> None:
    print(json.dumps({"decision":"deny","actor":actor,"operation":request.get("operation"),
                      "provider_kind":"video","provider_id":"kling-cli",
                      "payload_hash":request_hash(request),"reasons":[reason]},ensure_ascii=False))
    raise SystemExit(2)

def main(cli_args=None,runner=None,which=None):
    root=Path(__file__).resolve().parent.parent
    p=argparse.ArgumentParser(); p.add_argument("--request",required=True); p.add_argument("--approval")
    p.add_argument("--governance",default=str(root/"templates"/"governance.yaml"))
    p.add_argument("--providers",default=str(root/"assets"/"provider-registry.yaml"))
    p.add_argument("--agents",default=str(root/"assets"/"agent-registry.yaml"))
    p.add_argument("--contract",default=str(root/"templates"/"kling-contract.json"))
    p.add_argument("--events"); p.add_argument("--actor",default="Robotnik"); p.add_argument("--execution-id")
    p.add_argument("--execute",action="store_true"); p.add_argument("--timeout",type=int,default=120)
    args=p.parse_args(cli_args); request=load_json(Path(args.request).resolve())
    which=which or shutil.which; runner=runner or subprocess.run
    kling=which("kling") or "/usr/bin/kling-not-installed"
    contract_path=Path(args.contract).resolve()
    argv=build_argv(request,kling,contract_path)
    mutation=request.get("operation") not in DISCOVERY|{"query_tasks"}
    if not args.execute:
        print(json.dumps({"execute":False,"argv":argv,"payload_hash":request_hash(request)},ensure_ascii=False)); return
    load_contract(contract_path)
    providers=load_yaml(Path(args.providers).resolve())
    descriptor=provider_descriptor(providers,"video","kling-cli")
    if descriptor is None: deny_provider(request,args.actor,"provider-unknown")
    if descriptor.get("enabled") is not True: deny_provider(request,args.actor,"provider-disabled")
    if descriptor.get("external") is not True: deny_provider(request,args.actor,"provider-contract-invalid")
    adapter=str(descriptor.get("adapter_path","")).strip()
    if adapter!="scripts/kling_exec.py" or not (root/adapter).is_file():
        deny_provider(request,args.actor,"provider-adapter-invalid")
    if mutation and (not args.approval or not args.events or not args.execution_id):
        raise SystemExit("approval, events e execution-id obrigatórios")
    approval_path=Path(args.approval).resolve() if args.approval else None
    approval=load_json(approval_path) if approval_path else None
    decision=evaluate(request,args.actor,load_yaml(Path(args.governance).resolve()),
                      load_yaml(Path(args.agents).resolve()),providers,
                      root,approval,Path(args.events).resolve() if args.events else None)
    if decision["decision"]!="allow":
        print(json.dumps(decision,ensure_ascii=False)); raise SystemExit(2)
    if not which("kling"): raise SystemExit("kling não encontrado")
    if mutation:
        reserve_approval(approval_path,request,load_yaml(Path(args.governance).resolve()),args.execution_id)
        start_approval_execution(approval_path,args.execution_id)
    outcome="failed"; result={}
    try:
        cp=runner(argv,shell=False,capture_output=True,text=True,timeout=args.timeout)
        outcome="succeeded" if cp.returncode==0 else "failed"
        result={"operation":request["operation"],"request_hash":request_hash(request),"status":outcome,
                "timestamp_utc":utc_now(),"returncode":cp.returncode,
                "stdout":sanitize(cp.stdout),"stderr":sanitize(cp.stderr)}
    except subprocess.TimeoutExpired as exc:
        outcome="indeterminate"
        result={"operation":request["operation"],"request_hash":request_hash(request),"status":outcome,
                "timestamp_utc":utc_now(),"returncode":None,"stdout":sanitize(exc.stdout or ""),"stderr":"timeout"}
    if mutation:
        event=append_event(Path(args.events).resolve(),{"correlation_id":request.get("correlation_id",args.execution_id),
            "campaign_id":request["campaign_id"],"asset_id":request["asset_id"],"event_version":request["asset_version"],
            "actor":args.actor,"action":"external-action-result","result":outcome,"before_hash":None,
            "after_hash":request_hash(request),"detail":{"execution_id":args.execution_id,"adapter":"kling","result":result}})
        finish_approval_execution(approval_path,args.execution_id,outcome,event["event_id"])
        result["event_id"]=event["event_id"]
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(0 if outcome=="succeeded" else 2)

if __name__=="__main__":
    main()
