#!/usr/bin/env python3
"""Read-only inventory for authorized Brain curation; never declares coverage."""
import argparse,datetime,json,os,stat,time
from pathlib import Path
AGENTS=('main','kowalski','darth-vader','robotnik','sentinel')
PROFILES={'main':'/data/.openclaw','kowalski':'/home/openclaw/.openclaw-kowalski','darth-vader':'/home/openclaw/.openclaw-darth-vader'}
def inventory(days=7,base=Path('/data/.openclaw'),profiles=None):
    profiles=profiles or {k:Path(v) for k,v in PROFILES.items()};cutoff=time.time()-days*86400;rows={};errors=[];surfaces=[]
    for agent in AGENTS:
        workspace=base/('workspace' if agent=='main' else 'workspace-'+agent)
        roots=[('memory',workspace/'memory','shared_workspace'),('memory',workspace/'MEMORY.md','shared_workspace')]
        for profile,root in profiles.items():
            roots.extend([('openclaw_history',root/'agents'/agent/'sessions',profile),('codex_history',root/'agents'/agent/'codex-home'/'sessions',profile)])
        for kind,root,profile in roots:
            if not root.exists():surfaces.append(dict(agent=agent,profile=profile,kind=kind,path=str(root),exists=False));continue
            real=root.resolve();surfaces.append(dict(agent=agent,profile=profile,kind=kind,path=str(root),resolved=str(real),exists=True))
            def walk():
                if real.is_file():yield real;return
                for directory,dirs,files in os.walk(real,followlinks=False):
                    dirs[:]=[d for d in dirs if not (Path(directory)/d).is_symlink()]
                    for f in files:yield Path(directory)/f
            try:
                for p in walk():
                    if p.is_symlink():continue
                    st=p.stat()
                    if not stat.S_ISREG(st.st_mode) or st.st_mtime<cutoff:continue
                    if kind=='memory' and p.suffix.lower()!='.md':continue
                    if kind!='memory' and not (p.name.endswith('.jsonl') or p.name=='sessions.json'):continue
                    key=str(p);r=rows.setdefault(key,dict(path=key,agents=[],profiles=[],kind=kind,size=st.st_size,mtime_ns=st.st_mtime_ns,inode=st.st_ino,coverage='unreviewed',content_read=False))
                    if agent not in r['agents']:r['agents'].append(agent)
                    if profile not in r['profiles']:r['profiles'].append(profile)
            except OSError as e:errors.append(dict(path=str(root),error=type(e).__name__))
    return dict(schema_version='1.0',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),window_days=days,since_epoch=cutoff,coverage_complete=False,scope='Recent local memories and session histories only; older gaps require an explicit earlier window. Stat inventory is not content coverage.',surfaces=surfaces,errors=errors,sources=sorted(rows.values(),key=lambda r:(r['mtime_ns'],r['path'])))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--days',type=int,default=7);p.add_argument('--summary',action='store_true');a=p.parse_args()
    if not 1<=a.days<=3660:p.error('--days must be 1..3660')
    result=inventory(a.days)
    if a.summary:
        result['source_counts']={agent:sum(agent in r['agents'] for r in result['sources']) for agent in AGENTS};result.pop('sources')
    print(json.dumps(result,ensure_ascii=False,indent=2))
