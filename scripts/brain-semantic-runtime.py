#!/usr/bin/env python3
"""Persistent local Brain retrieval with incremental, atomic index refresh."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,json,os,re,shutil,sys,tempfile,types
from importlib.metadata import version
os.environ.update(HF_HUB_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',DO_NOT_TRACK='1',TOKENIZERS_PARALLELISM='false')
sys.dont_write_bytecode=True
import numpy as np
from fastembed import TextEmbedding
from tokenizers import Tokenizer
import yaml

MODEL='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
ALGORITHM={'model':MODEL,'fastembed_version':'0.8.0','pooling':'mean','dimension':384,'chunk_tokens':100,'chunk_stride':80}
EXCLUDED=('/versionados/','/evidence/','/exports/','/relatorios/','/reports/','/runtime/','/snapshots/')

def sha(data):return hashlib.sha256(data).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def redact(text):
    text=re.sub(r'-----BEGIN [^-]*PRIVATE KEY-----.*?(?:-----END [^-]*PRIVATE KEY-----|$)','[CREDENCIAL OMITIDA]',text,flags=re.S)
    text=re.sub(r'(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+',r'\1[OMITIDO]',text)
    text=re.sub(r'(?i)((?:access_token|refresh_token|api[_-]?key|password|passwd|senha|secret|authorization)\s*[=:]\s*[\"\x27]?)[^\s\"\x27&,;<>]+',r'\1[OMITIDO]',text)
    text=re.sub(r'(?i)([?&](?:code|token|state|key|signature|sig)=)[^&#\s]+',r'\1[OMITIDO]',text)
    return re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})\b','[CREDENCIAL OMITIDA]',text)

def source_snapshot(root):
    files={}
    for p in sorted((root/'BRAIN').rglob('*.md')):
        name=p.relative_to(root).as_posix()
        if any(part in name for part in EXCLUDED):continue
        if p.is_symlink() or not p.resolve().is_relative_to(root):raise RuntimeError('Unexpected source symlink: '+name)
        raw=p.read_bytes();files[name]={'sha256':sha(raw),'text':raw.decode('utf-8')}
    if not files:raise RuntimeError('Brain source is empty; refusing to replace index')
    digest=sha(json.dumps([(k,v['sha256']) for k,v in files.items()],ensure_ascii=False).encode())
    return files,digest

def declared_links(text,name,known):
    """Resolve only authored wikilinks; never infer a semantic relationship type."""
    found=[];seen=set()
    for raw in re.findall(r'\[\[([^\]]+)\]\]',text):
        target=raw.split('|',1)[0].split('#',1)[0].strip()
        if not target or '://' in target:continue
        stem=target.removesuffix('.md');options=[stem+'.md', 'BRAIN/'+stem+'.md', str(Path(name).parent/(stem+'.md'))]
        matches=[x for x in options if x in known]
        if not matches and '/' not in stem:matches=[x for x in known if Path(x).stem==stem]
        matches=list(dict.fromkeys(matches))
        if len(matches)==1 and matches[0] not in seen:
            seen.add(matches[0]);found.append({'target':matches[0],'basis':'explicit_wikilink_in_source'})
    return found

def readonly_embedding(model_dir):
    """Use the pinned encoder with an isolated, non-creating cache resolver.

    FastEmbed 0.8.0 calls mkdir even for an existing cache. Clone only its
    constructor globals for this instance; never monkeypatch installed modules.
    Model selection, tokenization, pooling and inference remain FastEmbed's.
    """
    from fastembed.text.onnx_embedding import OnnxTextEmbedding
    if version('fastembed')!=ALGORITHM['fastembed_version']:
        raise RuntimeError('Read-only encoder requires the indexed FastEmbed version')
    selected=next((cls for cls in TextEmbedding.EMBEDDINGS_REGISTRY
                   if any(MODEL.lower()==d.model.lower() for d in cls._list_supported_models())),None)
    if selected is None or selected.__init__ is not OnnxTextEmbedding.__init__:
        raise RuntimeError('Unsupported read-only encoder constructor; no fallback writes allowed')
    model_dir=Path(model_dir).resolve()
    if not model_dir.is_dir():raise RuntimeError('Local model is missing; read-only search cannot download it')
    def existing_cache(cache_dir=None):
        if cache_dir is None or Path(cache_dir).resolve()!=model_dir:
            raise RuntimeError('Unexpected read-only model cache path')
        return model_dir
    original=OnnxTextEmbedding.__init__
    initializer=types.FunctionType(original.__code__,
        {**original.__globals__,'define_cache_dir':existing_cache},
        original.__name__,original.__defaults__,original.__closure__)
    initializer.__kwdefaults__=original.__kwdefaults__
    encoder=type('ReadOnlyEmbedding',(selected,),{'__init__':initializer})
    return encoder(model_name=MODEL,specific_model_path=str(model_dir),cache_dir=str(model_dir),
                   threads=2,local_files_only=True,providers=['CPUExecutionProvider'])

class Runtime:
    def __init__(self,config,read_only=False):
        self.root=Path(config['brain_root']).resolve();self.data=Path(config['data_dir']).resolve()
        self.model_dir=Path(config['model_dir']).resolve();self.config=config;self._model=None;self.read_only=read_only
        if self.data.is_relative_to(self.root):raise RuntimeError('Derived index must stay outside the Brain repository')
        if self.read_only:
            if not self.data.is_dir():raise RuntimeError('Index directory is missing; run an authorized refresh first')
        else:self.data.mkdir(parents=True,exist_ok=True,mode=0o700)
    @property
    def model(self):
        if self._model is None:
            if self.read_only:self._model=readonly_embedding(self.model_dir)
            else:self._model=TextEmbedding(MODEL,specific_model_path=str(self.model_dir),cache_dir=str(self.data/'model-cache'),
                                      threads=2,local_files_only=True,providers=['CPUExecutionProvider'])
        return self._model
    def current(self):
        p=self.data/'CURRENT'
        if not p.exists():return None,None,None
        name=p.read_text().strip()
        if not re.fullmatch(r'gen-[a-f0-9]{20}',name):raise RuntimeError('Invalid index generation pointer')
        folder=self.data/name
        index=json.loads((folder/'index.json').read_text())
        vectors=np.load(folder/'vectors.npy',mmap_mode='r',allow_pickle=False)
        if vectors.shape!=(len(index['chunks']),384):raise RuntimeError('Index/vector shape mismatch')
        return index,vectors,folder
    def refresh(self):
        if self.read_only:raise RuntimeError('Refresh is disabled for read-only search')
        with (self.data/'index.lock').open('a') as lock:
            try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise RuntimeError('Index refresh already in progress; retry after it completes')
            files,digest=source_snapshot(self.root)
            old,vectors,oldfolder=self.current()
            if old and old.get('source_digest')==digest and all(old.get(k)==v for k,v in ALGORITHM.items()):
                return old,vectors,{'updated':False,'changed_notes':0,'reused_notes':len(files)}
            olddocs={d['path']:d for d in old['docs']} if old and all(old.get(k)==v for k,v in ALGORITHM.items()) else {}
            tokenizer=Tokenizer.from_file(str(self.model_dir/'tokenizer.json'));tokenizer.no_truncation()
            docs=[];chunks=[];blocks=[];reused=changed=0
            for name,value in files.items():
                did=len(docs);text=value['text'];previous=olddocs.get(name)
                title=next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')),Path(name).stem)
                meta={}
                if text.startswith('---\n'):
                    meta=yaml.safe_load(text.split('---',2)[1]) or {}
                doc={'path':name,'title':title,'sha256':value['sha256'],'first_chunk':len(chunks),
                     'relationships':meta.get('relationships',[]),'updated':str(meta.get('updated',''))}
                if previous and previous['sha256']==value['sha256']:
                    start=previous['first_chunk'];end=start+previous['chunks']
                    local=[{**c,'doc':did} for c in old['chunks'][start:end]]
                    block=np.asarray(vectors[start:end]);reused+=1
                else:
                    body=re.sub(r'\A---\n.*?\n---\n','',text,flags=re.S)
                    body=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',r'\2',body)
                    body=re.sub(r'\[\[([^\]]+)\]\]',r'\1',body)
                    ids=tokenizer.encode(body,add_special_tokens=False).ids;local=[]
                    for start in range(0,len(ids),80):
                        local.append({'doc':did,'token_start':start,'text':tokenizer.decode(ids[start:start+100],skip_special_tokens=True)})
                        if start+100>=len(ids):break
                    if not local:local=[{'doc':did,'token_start':0,'text':title}]
                    block=np.asarray(list(self.model.embed([c['text'] for c in local],batch_size=32)),dtype=np.float32)
                    block/=np.maximum(np.linalg.norm(block,axis=1,keepdims=True),1e-12)
                    changed+=1
                doc['chunks']=len(local);docs.append(doc);chunks+=local;blocks.append(block)
            if source_snapshot(self.root)[1]!=digest:raise RuntimeError('Brain changed during indexing; no new generation published')
            matrix=np.concatenate(blocks).astype(np.float32,copy=False)
            index={**ALGORITHM,'source_digest':digest,'indexed_at':now(),'docs':docs,'chunks':chunks}
            generation_key=sha((digest+json.dumps(ALGORITHM,sort_keys=True)).encode())
            name='gen-'+generation_key[:20];destination=self.data/name
            temp=Path(tempfile.mkdtemp(prefix='.build-',dir=self.data))
            try:
                (temp/'index.json').write_text(json.dumps(index,ensure_ascii=False))
                np.save(temp/'vectors.npy',matrix,allow_pickle=False)
                if destination.exists():
                    # A complete generation with the same source digest is reusable; verify exact metadata.
                    existing=json.loads((destination/'index.json').read_text())
                    if existing['source_digest']!=digest or any(existing.get(k)!=v for k,v in ALGORITHM.items()):raise RuntimeError('Generation collision')
                    shutil.rmtree(temp)
                else:os.replace(temp,destination)
                pointer=self.data/'CURRENT.next';pointer.write_text(name+'\n');os.replace(pointer,self.data/'CURRENT')
            finally:
                if temp.exists():shutil.rmtree(temp)
            keep={destination,oldfolder}
            for p in self.data.glob('gen-*'):
                if p not in keep and re.fullmatch(r'gen-[a-f0-9]{20}',p.name) and p.is_dir() and not p.is_symlink():shutil.rmtree(p)
            return index,matrix,{'updated':True,'changed_notes':changed,'reused_notes':reused}
    def search(self,query,limit=5,scope='knowledge'):
        if self.read_only:
            index,vectors,_=self.current()
            if index is None:raise RuntimeError('Index is not ready; run an authorized refresh first')
            if any(index.get(k)!=v for k,v in ALGORITHM.items()):
                raise RuntimeError('Index algorithm is incompatible; run an authorized refresh first')
            if source_snapshot(self.root)[1]!=index.get('source_digest'):
                raise RuntimeError('Index is stale; run an authorized refresh first')
            refresh={'updated':False,'changed_notes':0,'reused_notes':len(index['docs']),'mode':'read_only'}
        else:index,vectors,refresh=self.refresh()
        q=np.asarray(next(self.model.embed([query])),dtype=np.float32);q/=max(float(np.linalg.norm(q)),1e-12)
        scores=vectors@q;seen=set();results=[];known={d['path'] for d in index['docs']}
        for pos in np.argsort(-scores):
            chunk=index['chunks'][int(pos)];doc=index['docs'][chunk['doc']]
            if scope=='knowledge' and (not doc['path'].startswith('BRAIN/40-CONHECIMENTO/') or doc['path'].endswith('/README.md')):continue
            if doc['path'] in seen:continue
            seen.add(doc['path']);score=float(scores[pos])
            raw=(self.root/doc['path']).read_bytes()
            if sha(raw)!=doc['sha256']:raise RuntimeError('Result source changed; retry')
            results.append({'path':doc['path'],'title':doc['title'],'source_sha256':doc['sha256'],'cosine':score,
                            'match_strength':'weak' if score<0.35 else 'candidate','excerpt':redact(chunk['text']),
                            'relationships':doc.get('relationships',[])[:6], 'source_updated':doc.get('updated',''),
                            'declared_links':declared_links(raw.decode('utf-8'),doc['path'],known)[:12]})
            if len(results)>=limit:break
        if source_snapshot(self.root)[1]!=index['source_digest']:raise RuntimeError('Source changed during search; retry against the new snapshot')
        return {'query':redact(query),'scope':scope,'index_at':index['indexed_at'],'source_digest':index['source_digest'],
                'refresh':refresh,'results':results,'raw_history_access':False,
                'limitations':['Similaridade sugere leitura; não prova equivalência, cobertura, autorização nem estado atual.',
                               'Consulta somente o Brain consolidado. Históricos brutos não integram este índice; sua retenção segue os recibos de cobertura.',
                               'Filtro de credenciais é complementar; não publicar resultados brutos automaticamente.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path,required=True)
    mode=p.add_mutually_exclusive_group()
    mode.add_argument('--refresh-only',action='store_true')
    mode.add_argument('--no-refresh',action='store_true',help='Search the existing index without locks, cache creation or writes; fail if missing or stale')
    p.add_argument('--scope',choices=['knowledge','all'],default='knowledge')
    p.add_argument('--limit',type=int,choices=range(1,11),default=5,metavar='1..10');p.add_argument('query',nargs='?')
    a=p.parse_args()
    if not a.refresh_only and not a.query:p.error('Provide a question or --refresh-only')
    try:
        runtime=Runtime(json.loads(a.config.read_text()),read_only=a.no_refresh)
        if a.refresh_only:
            idx,_,info=runtime.refresh();result={'status':'ready','notes':len(idx['docs']),'chunks':len(idx['chunks']),**info}
        else:result=runtime.search(a.query,a.limit,a.scope)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except Exception as e:
        print(json.dumps({'status':'not_ready','error':redact(str(e)),'results':[]},ensure_ascii=False))
        raise SystemExit(1)

if __name__=='__main__':main()
