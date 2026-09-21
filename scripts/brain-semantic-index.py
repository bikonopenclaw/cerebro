from pathlib import Path
import argparse, hashlib, json, os, re
os.environ['HF_HUB_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['DO_NOT_TRACK']='1'
import numpy as np
from fastembed import TextEmbedding
from tokenizers import Tokenizer

base=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Build an offline semantic index from a Brain snapshot; keep output outside Git.')
parser.add_argument('--root',type=Path,default=base/'candidate')
parser.add_argument('--data-dir',type=Path,default=base)
args=parser.parse_args()
base=args.data_dir.resolve()
root=args.root.resolve()
model=TextEmbedding('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',cache_dir=str(base/'model-cache'),threads=2,local_files_only=True)
tokenizer=Tokenizer.from_file(str(next((base/'model-cache').rglob('tokenizer.json'))))
tokenizer.no_truncation()
files={p.relative_to(root).as_posix():p.read_text() for p in (root/'BRAIN').rglob('*.md')}
docs=[]; chunks=[]
for name,text in sorted(files.items()):
    if not name.startswith('BRAIN/') or not name.endswith('.md'): continue
    if '/versionados/' in name or '/reports/' in name: continue
    title=next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')),Path(name).stem)
    body=re.sub(r'\A---\n.*?\n---\n','',text,flags=re.S)
    clean=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',r'\2',body)
    clean=re.sub(r'\[\[([^\]]+)\]\]',r'\1',clean)
    ids=tokenizer.encode(clean,add_special_tokens=False).ids
    docid=len(docs)
    docs.append({'path':name,'title':title,'sha256':hashlib.sha256(text.encode()).hexdigest(),'first_chunk':len(chunks)})
    for start in range(0,len(ids),80):
        value=tokenizer.decode(ids[start:start+100],skip_special_tokens=True)
        chunks.append({'doc':docid,'token_start':start,'text':value})
        if start+100>=len(ids): break
    docs[-1]['chunks']=len(chunks)-docs[-1]['first_chunk']

print(f'Embedding {len(docs)} notes / {len(chunks)} chunks locally',flush=True)
vectors=[]
for i,v in enumerate(model.embed([c['text'] for c in chunks],batch_size=32)):
    vectors.append(v)
    if (i+1)%500==0: print(f'Embedded {i+1}/{len(chunks)}',flush=True)
matrix=np.asarray(vectors,dtype=np.float32)
matrix/=np.maximum(np.linalg.norm(matrix,axis=1,keepdims=True),1e-12)
means=np.asarray([matrix[d['first_chunk']:d['first_chunk']+d['chunks']].mean(axis=0) for d in docs])
means/=np.maximum(np.linalg.norm(means,axis=1,keepdims=True),1e-12)
np.save(base/'note-chunk-vectors.npy',matrix)
np.save(base/'note-vectors.npy',means)
(base/'note-semantic-index.json').write_text(json.dumps({'model':'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2','fastembed_version':'0.8.0','pooling':'mean','dimension':384,'chunk_tokens':100,'chunk_stride':80,'docs':docs,'chunks':chunks},ensure_ascii=False))
eligible=[i for i,d in enumerate(docs) if d['path'].startswith('BRAIN/40-CONHECIMENTO/') and not d['path'].endswith('/README.md')]
pairs=[]
for pos,i in enumerate(eligible):
    for j in eligible[pos+1:]:
        pairs.append({'left':docs[i]['path'],'right':docs[j]['path'],'cosine':float(means[i]@means[j]),'status':'candidate_not_approved'})
pairs.sort(key=lambda x:-x['cosine'])
(base/'semantic-link-candidates.json').write_text(json.dumps(pairs[:40],ensure_ascii=False,indent=2))
for p in pairs[:12]: print(round(p['cosine'],3),Path(p['left']).stem,'<->',Path(p['right']).stem)
