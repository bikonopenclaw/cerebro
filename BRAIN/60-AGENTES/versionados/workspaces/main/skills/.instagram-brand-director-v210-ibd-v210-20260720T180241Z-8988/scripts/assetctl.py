#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, tempfile, urllib.parse, urllib.request
from pathlib import Path
from governance_engine import evaluate
from runtime_lib import (append_event, atomic_write_json, finish_approval_execution, load_json,
                         load_yaml, request_hash, reserve_approval, start_approval_execution, utc_now)

MIME_EXT={"image/png":".png","image/jpeg":".jpg","image/webp":".webp","video/mp4":".mp4","video/webm":".webm"}

def validate_url(url: str,allowed_hosts: set[str]):
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!="https" or not parsed.hostname or parsed.username or parsed.password: raise ValueError("URL precisa ser HTTPS e sem credenciais")
    if allowed_hosts and parsed.hostname not in allowed_hosts: raise ValueError("host não autorizado")
    return parsed

def archive(url: str,dest: Path,allowed_hosts: set[str],max_bytes: int):
    validate_url(url,allowed_hosts); dest.mkdir(parents=True,exist_ok=True)
    req=urllib.request.Request(url,headers={"User-Agent":"BikonAssetArchiver/2.1"})
    h=hashlib.sha256(); total=0; fd,tmp_name=tempfile.mkstemp(prefix=".asset-",dir=dest)
    try:
        with os.fdopen(fd,"wb") as out,urllib.request.urlopen(req,timeout=60) as resp:
            final=urllib.parse.urlparse(resp.geturl())
            if final.scheme!="https" or (allowed_hosts and final.hostname not in allowed_hosts): raise ValueError("redirect não autorizado")
            mime=(resp.headers.get_content_type() or "").lower()
            if mime not in MIME_EXT: raise ValueError(f"MIME não autorizado: {mime}")
            while True:
                chunk=resp.read(1024*1024)
                if not chunk: break
                total+=len(chunk)
                if total>max_bytes: raise ValueError("ativo excede limite")
                h.update(chunk); out.write(chunk)
            out.flush(); os.fsync(out.fileno())
        digest=h.hexdigest(); target=dest/f"{digest}{MIME_EXT[mime]}"; os.replace(tmp_name,target)
        meta={"path":str(target),"sha256":digest,"mime":mime,"size":total,"source_url":url,"archived_at":utc_now()}
        atomic_write_json(target.with_suffix(target.suffix+".json"),meta); return meta
    except Exception:
        try: os.unlink(tmp_name)
        except FileNotFoundError: pass
        raise

def main():
    root=Path(__file__).resolve().parent.parent
    p=argparse.ArgumentParser(); p.add_argument("--request",required=True); p.add_argument("--approval")
    p.add_argument("--governance",default=str(root/"templates"/"governance.yaml"))
    p.add_argument("--providers",default=str(root/"assets"/"provider-registry.yaml"))
    p.add_argument("--agents",default=str(root/"assets"/"agent-registry.yaml"))
    p.add_argument("--events"); p.add_argument("--actor",default="Robotnik"); p.add_argument("--execution-id")
    p.add_argument("--dest",required=True); p.add_argument("--allowed-host",action="append",default=[])
    p.add_argument("--max-bytes",type=int,default=250_000_000); p.add_argument("--execute",action="store_true")
    args=p.parse_args(); request=load_json(Path(args.request).resolve())
    if request.get("operation")!="archive_remote" or request.get("tool")!="assetctl": raise SystemExit("request incompatível com assetctl")
    url=str(request.get("parameters",{}).get("url","")); hosts=set(args.allowed_host); validate_url(url,hosts)
    if not args.execute:
        print(json.dumps({"execute":False,"url":url,"payload_hash":request_hash(request)},ensure_ascii=False)); return
    if not args.approval or not args.events or not args.execution_id: raise SystemExit("approval, events e execution-id obrigatórios")
    approval_path=Path(args.approval).resolve(); governance=load_yaml(Path(args.governance).resolve())
    decision=evaluate(request,args.actor,governance,load_yaml(Path(args.agents).resolve()),
                      load_yaml(Path(args.providers).resolve()),root,load_json(approval_path),Path(args.events).resolve())
    if decision["decision"]!="allow": print(json.dumps(decision,ensure_ascii=False)); raise SystemExit(2)
    reserve_approval(approval_path,request,governance,args.execution_id); start_approval_execution(approval_path,args.execution_id)
    outcome="failed"; result={}
    try:
        result=archive(url,Path(args.dest).resolve(),hosts,args.max_bytes); outcome="succeeded"
    except Exception as exc:
        result={"error":str(exc)}; outcome="indeterminate" if isinstance(exc,TimeoutError) else "failed"
    event=append_event(Path(args.events).resolve(),{"correlation_id":request.get("correlation_id",args.execution_id),
        "campaign_id":request["campaign_id"],"asset_id":request["asset_id"],"event_version":request["asset_version"],
        "actor":args.actor,"action":"external-action-result","result":outcome,"before_hash":None,
        "after_hash":request_hash(request),"detail":{"execution_id":args.execution_id,"adapter":"assetctl","result":result}})
    finish_approval_execution(approval_path,args.execution_id,outcome,event["event_id"])
    print(json.dumps({"status":outcome,"event_id":event["event_id"],**result},ensure_ascii=False))
    raise SystemExit(0 if outcome=="succeeded" else 2)

if __name__=="__main__":
    main()
