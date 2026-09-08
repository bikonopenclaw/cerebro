#!/usr/bin/env python3
"""Only final typography, official logo, crop and export of reconciled photograph."""
from pathlib import Path
import hashlib
import json
import subprocess

SKILL=Path(__file__).resolve().parents[1]
OUT=Path('/data/.openclaw/workspace-robotnik/entregas/piloto-contrato-criativo-v1-20260908')
SOURCE=OUT/'native-candidates/call_r3CVYFM1hEuDwtkhK7G8rMyH.png'
LOGO=SKILL/'assets/Bikon_Horizontal_fundo_preto.png'
FONT=SKILL/'assets/space-grotesk/SpaceGrotesk-wght.ttf'
FINAL=OUT/'piloto-ia-sem-dono-rascunho-final.png'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert sha(SOURCE)=='d1fe2c7dd5dccd71892293276fc7bff51d0f1a12ba2035cf8f0e088ea50cf472'
    assert sha(LOGO)=='7b547dec1c1ec3091eaaa3990ad5e5773bef9e71f17b448aa2598483b72e3a6d'
    assert sha(FONT)=='acad6de1fc93436f5c0f1f4137751ef04f1aea3063e7036535970ffcfbd79f72'
    if FINAL.exists(): raise SystemExit('Final exists: reconcile before any revision')
    args=['/usr/bin/convert',str(SOURCE),'-resize','1080x1424!', '-gravity','center','-extent','1080x1350',
          '-gravity','NorthWest','-font',str(FONT),'-pointsize','78','-strokewidth','3',
          '-stroke','#00B4B9','-fill','#00B4B9','-annotate','+62+82','IA',
          '-stroke','white','-fill','white','-annotate','+158+82','sem dono',
          '-annotate','+62+173','vira bagunça',
          '-stroke','none','-pointsize','30','-fill','white',
          '-annotate','+65+299','Antes de automatizar,',
          '-annotate','+65+340','defina regra, acesso e revisão.',
          '(','-size','1080x260','gradient:transparent-#000000dd',')','-gravity','South','-geometry','+0+0','-composite',
          '(',str(LOGO),'-trim','+repage','-resize','300x',')',
          '-gravity','SouthEast','-geometry','+66+65','-composite',
          '-colorspace','sRGB','-strip','-define','png:exclude-chunk=date,time',str(FINAL)]
    subprocess.run(args,check=True)
    subprocess.run(['/usr/bin/convert',str(FINAL),'-resize','360x450',str(OUT/'piloto-final-mobile-360.png')],check=True)
    caption='''RASCUNHO AGUARDANDO APROVAÇÃO

Legenda sugerida:
IA sem dono vira bagunça.

Quem pode acessar os dados? Qual regra orienta a automação? Quem responde pela decisão? Quem revisa o resultado?

Antes de colocar mais uma ferramenta na operação, deixe essas respostas claras.

Sua empresa governada por IA começa com gente responsável pelo processo.

Quer identificar por onde começar na sua PME? Fale com a Bikon.

#BikonTecnologia #InteligênciaArtificial #GestãoDePME
'''
    (OUT/'legenda-sugerida.txt').write_text(caption)
    manifest={'status':'DRAFT_AWAITING_FORMAL_REVIEW_AND_HUMAN_ACCEPTANCE','source':str(SOURCE),'source_sha256':sha(SOURCE),
              'official_logo':str(LOGO),'official_logo_sha256':sha(LOGO),'font_sha256':sha(FONT),
              'operations':['proportional resize with rounded height','center crop 1080x1350','exact Portuguese typography in Space Grotesk','bottom color finishing for logo contrast','official transparent logo trim and proportional placement','sRGB PNG export'],
              'photographic_scene_replaced':False,'files':[]}
    for p in [FINAL,OUT/'piloto-final-mobile-360.png',OUT/'legenda-sugerida.txt']:
        manifest['files'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
    (OUT/'finalization-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
