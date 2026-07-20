#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, mimetypes, os, tempfile, urllib.parse, urllib.request
from pathlib import Path
from runtime_lib import atomic_write_json, safe_name, utc_now

MIME_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
            "video/mp4": ".mp4", "video/webm": ".webm"}

def archive(url: str, dest: Path, allowed_hosts: set[str], max_bytes: int):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("URL precisa ser HTTPS e sem credenciais")
    if allowed_hosts and parsed.hostname not in allowed_hosts:
        raise ValueError("host não autorizado")
    dest.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "BikonAssetArchiver/1.0"})
    h = hashlib.sha256()
    total = 0
    fd, tmp_name = tempfile.mkstemp(prefix=".asset-", dir=dest)
    try:
        with os.fdopen(fd, "wb") as out, urllib.request.urlopen(req, timeout=60) as resp:
            final = urllib.parse.urlparse(resp.geturl())
            if final.scheme != "https" or (allowed_hosts and final.hostname not in allowed_hosts):
                raise ValueError("redirect não autorizado")
            mime = (resp.headers.get_content_type() or "").lower()
            if mime not in MIME_EXT:
                raise ValueError(f"MIME não autorizado: {mime}")
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk: break
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("ativo excede limite")
                h.update(chunk); out.write(chunk)
            out.flush(); os.fsync(out.fileno())
        digest = h.hexdigest()
        target = dest / f"{digest}{MIME_EXT[mime]}"
        os.replace(tmp_name, target)
        meta = {"path": str(target), "sha256": digest, "mime": mime, "size": total,
                "source_url": url, "archived_at": utc_now()}
        atomic_write_json(target.with_suffix(target.suffix + ".json"), meta)
        return meta
    except Exception:
        try: os.unlink(tmp_name)
        except FileNotFoundError: pass
        raise

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--url", required=True); p.add_argument("--dest", required=True)
    p.add_argument("--allowed-host", action="append", default=[])
    p.add_argument("--max-bytes", type=int, default=250_000_000)
    a=p.parse_args()
    print(json.dumps(archive(a.url, Path(a.dest).resolve(), set(a.allowed_host), a.max_bytes), ensure_ascii=False))

if __name__=="__main__":
    main()
