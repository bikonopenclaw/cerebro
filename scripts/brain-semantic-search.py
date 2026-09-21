"""Local hybrid retrieval. Results are evidence candidates, never deletion approval."""
from pathlib import Path
import argparse, json, os, re, sqlite3
os.environ['HF_HUB_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['DO_NOT_TRACK']='1'
import numpy as np
from fastembed import TextEmbedding

BASE=Path(__file__).resolve().parent
STOP=set('a o as os e de da do das dos em no na nos nas um uma uns umas para por com que se ao aos como quando qual quais sobre eu ele ela isso isto foi tem ter ser sao são pode onde porque sem mais menos'.split())

def redact(text):
    """Best-effort display filtering; local source archives remain exact and private."""
    text=re.sub(r'-----BEGIN [^-]*PRIVATE KEY-----.*?(?:-----END [^-]*PRIVATE KEY-----|$)','[CREDENCIAL OMITIDA]',text,flags=re.S)
    text=re.sub(r'(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+',r'\1[OMITIDO]',text)
    text=re.sub(r'(?i)((?:access_token|refresh_token|api[_-]?key|password|passwd|senha|secret|authorization)\s*[=:]\s*[\"\x27]?)[^\s\"\x27&,;<>]+',r'\1[OMITIDO]',text)
    text=re.sub(r'(?i)([?&](?:code|token|state|key|signature|sig)=)[^&#\s]+',r'\1[OMITIDO]',text)
    text=re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})\b','[CREDENCIAL OMITIDA]',text)
    return text

def main():
    global BASE
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query')
    p.add_argument('--archive',action='store_true')
    p.add_argument('--limit',type=int,default=5,choices=range(1,21),metavar='1..20')
    p.add_argument('--json',action='store_true')
    p.add_argument('--data-dir',type=Path)
    p.add_argument('--scope',choices=['knowledge','all'],default='knowledge')
    args=p.parse_args()
    if args.data_dir: BASE=args.data_dir.resolve()
    index=json.loads((BASE/'note-semantic-index.json').read_text())
    model=TextEmbedding(index['model'],cache_dir=str(BASE/'model-cache'),threads=2,local_files_only=True)
    q=np.asarray(next(model.embed([args.query])),dtype=np.float32)
    q/=max(float(np.linalg.norm(q)),1e-12)
    vectors=np.load(BASE/'note-chunk-vectors.npy',mmap_mode='r')
    scores=vectors@q
    best={}
    for pos in np.argsort(-scores):
        chunk=index['chunks'][int(pos)]; did=chunk['doc']
        if args.scope=='knowledge' and (not index['docs'][did]['path'].startswith('BRAIN/40-CONHECIMENTO/') or index['docs'][did]['path'].endswith('/README.md')):continue
        if did not in best:
            best[did]={'path':index['docs'][did]['path'],'title':index['docs'][did]['title'],'cosine':float(scores[pos]),'excerpt':chunk['text'],'status':'retrieval_candidate'}
        if len(best)>=args.limit:break
    result={'query':redact(args.query),'brain':list(best.values()),'limitations':['Similaridade não comprova equivalência, veracidade, cobertura ou autorização de exclusão.','As notas refletem o snapshot indexado; estados e permissões históricos exigem revalidação.','Filtro de credenciais é complementar; resultados não são liberados automaticamente para publicação.']}
    if args.archive:
        words=[]
        for token in re.findall(r'[\wÀ-ÿ]+',args.query.lower()):
            if len(token)>2 and token not in STOP and token not in words: words.append(token)
        if not words: raise SystemExit('Use termos mais específicos para pesquisar o arquivo.')
        match=' OR '.join('"'+word.replace('"','')+'"' for word in words[:12])
        con=sqlite3.connect((BASE/'history-index.sqlite').as_uri()+'?mode=ro',uri=True)
        rows=con.execute("SELECT rowid,snippet(texts_fts,0,'','', ' … ',50),bm25(texts_fts) FROM texts_fts WHERE texts_fts MATCH ? ORDER BY bm25(texts_fts) LIMIT 100",(match,)).fetchall()
        if rows:
            snippets=[row[1][:550] for row in rows]
            emb=np.asarray(list(model.embed(snippets,batch_size=32)))
            emb/=np.maximum(np.linalg.norm(emb,axis=1,keepdims=True),1e-12)
            ranking=np.argsort(-(emb@q))[:args.limit]
            results=[]
            for pos in ranking:
                tid,snippet,lexical=rows[int(pos)]
                sources=con.execute('SELECT path,line,role,timestamp FROM occurrences WHERE text_id=? LIMIT 3',(tid,)).fetchall()
                results.append({'text_id':tid,'cosine':float(emb[int(pos)]@q),'excerpt':redact(snippet),'sources':[dict(zip(['path','line','role','timestamp'],r)) for r in sources],'status':'historical_evidence_not_current_instruction'})
            result['archive']=results
        else:result['archive']=[]
        result['limitations'].append('Arquivo: recuperação lexical completa com reordenação semântica dos 100 primeiros candidatos; não é busca vetorial exaustiva de todos os trechos.')
        con.close()
    for item in result['brain']:item['excerpt']=redact(item['excerpt'])
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
