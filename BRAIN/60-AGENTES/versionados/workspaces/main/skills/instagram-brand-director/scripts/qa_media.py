#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, struct, subprocess
from pathlib import Path

def digest(path: Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def image_info(path: Path):
    with path.open("rb") as f:
        head=f.read(32)
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            w,h=struct.unpack(">II",head[16:24]); return {"format":"png","width":w,"height":h}
        if head[:2]==b"\xff\xd8":
            f.seek(2)
            while True:
                b=f.read(1)
                if not b: break
                if b!=b"\xff": continue
                marker=f.read(1)
                while marker==b"\xff": marker=f.read(1)
                if marker in (b"\xd8",b"\xd9"): continue
                raw=f.read(2)
                if len(raw)<2: break
                length=struct.unpack(">H",raw)[0]
                if marker in [bytes([x]) for x in range(0xC0,0xC4)]+[bytes([x]) for x in range(0xC5,0xC8)]+[bytes([x]) for x in range(0xC9,0xCC)]+[bytes([x]) for x in range(0xCD,0xD0)]:
                    data=f.read(5); h,w=struct.unpack(">HH",data[1:5])
                    return {"format":"jpeg","width":w,"height":h}
                f.seek(length-2,1)
    raise ValueError("imagem PNG/JPEG inválida ou não suportada")

def video_info(path: Path):
    ffprobe=shutil.which("ffprobe")
    if not ffprobe: raise ValueError("ffprobe ausente")
    cp=subprocess.run([ffprobe,"-v","error","-show_format","-show_streams","-of","json",str(path)],
                      shell=False,capture_output=True,text=True,timeout=60)
    if cp.returncode: raise ValueError(cp.stderr.strip())
    return {"format":"video","ffprobe":json.loads(cp.stdout)}

def main():
    p=argparse.ArgumentParser(); p.add_argument("path"); p.add_argument("--kind",choices=["image","video"],required=True)
    a=p.parse_args(); path=Path(a.path).resolve()
    if not path.is_file(): raise SystemExit("arquivo não encontrado")
    info=image_info(path) if a.kind=="image" else video_info(path)
    result={"path":str(path),"size":path.stat().st_size,"sha256":digest(path),**info}
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
