#!/usr/bin/env python3
import argparse, json, os, urllib.parse, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ENV = BASE / "secrets" / "instagram-bikon.env"

def load_env():
    if ENV.exists():
        for line in ENV.read_text(encoding="utf-8").splitlines():
            line=line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k,v=line.split("=",1)
            os.environ.setdefault(k.strip(), v.strip())

def need(name):
    v=os.environ.get(name)
    if not v:
        raise SystemExit(f"Falta {name} em {ENV}")
    return v

def graph(path, method="GET", params=None):
    version=os.environ.get("META_GRAPH_VERSION","v24.0")
    token=need("META_ACCESS_TOKEN")
    params=dict(params or {})
    params["access_token"]=token
    url=f"https://graph.facebook.com/{version}/{path.lstrip("/")}"
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
        req=urllib.request.Request(url)
    else:
        data=urllib.parse.urlencode(params).encode()
        req=urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body=e.read().decode(errors="replace")
        raise SystemExit(f"Graph API erro {e.code}: {body}")

def cmd_me(args):
    print(json.dumps(graph("/me", params={"fields":"id,name"}), ensure_ascii=False, indent=2))

def cmd_pages(args):
    print(json.dumps(graph("/me/accounts", params={"fields":"id,name,instagram_business_account{id,username,name}"}), ensure_ascii=False, indent=2))

def cmd_create(args):
    ig=args.ig_id or need("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    params={"caption": args.caption}
    if args.image_url:
        params["image_url"]=args.image_url
    if args.video_url:
        params["media_type"]=args.media_type or "REELS"
        params["video_url"]=args.video_url
    if not args.image_url and not args.video_url:
        raise SystemExit("Informe --image-url ou --video-url")
    print(json.dumps(graph(f"/{ig}/media", method="POST", params=params), ensure_ascii=False, indent=2))

def cmd_status(args):
    print(json.dumps(graph(f"/{args.creation_id}", params={"fields":"id,status_code,status"}), ensure_ascii=False, indent=2))

def cmd_publish(args):
    mode=os.environ.get("ROBOTNIK_INSTAGRAM_MODE","draft").lower()
    if mode != "publish" and not args.force:
        raise SystemExit("Modo seguro ativo: ROBOTNIK_INSTAGRAM_MODE=draft. Use --force só com aprovação explícita.")
    ig=args.ig_id or need("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    print(json.dumps(graph(f"/{ig}/media_publish", method="POST", params={"creation_id":args.creation_id}), ensure_ascii=False, indent=2))

def main():
    load_env()
    p=argparse.ArgumentParser(description="Meta Graph API, Instagram Bikon")
    sub=p.add_subparsers(required=True)
    s=sub.add_parser("me"); s.set_defaults(func=cmd_me)
    s=sub.add_parser("pages"); s.set_defaults(func=cmd_pages)
    s=sub.add_parser("create-container"); s.add_argument("--ig-id"); s.add_argument("--caption", required=True); s.add_argument("--image-url"); s.add_argument("--video-url"); s.add_argument("--media-type"); s.set_defaults(func=cmd_create)
    s=sub.add_parser("container-status"); s.add_argument("creation_id"); s.set_defaults(func=cmd_status)
    s=sub.add_parser("publish"); s.add_argument("creation_id"); s.add_argument("--ig-id"); s.add_argument("--force", action="store_true"); s.set_defaults(func=cmd_publish)
    args=p.parse_args(); args.func(args)
if __name__ == "__main__": main()
