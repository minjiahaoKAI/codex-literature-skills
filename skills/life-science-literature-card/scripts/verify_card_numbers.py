#!/usr/bin/env python3
"""Find scientific numeric tokens in sources, with checked derivation records.

A textual match is a candidate, not proof of group/endpoint/model correctness.
Source locators and semantic manual review remain required.
"""
from __future__ import annotations
import argparse,json,re,unicodedata,hashlib
from collections import Counter
from decimal import Decimal,InvalidOperation
from pathlib import Path

TOKEN=re.compile(r'(?<![A-Za-z0-9_])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?(?![A-Za-z0-9_])')
SKIP_KEYS={'id','schema_version','source','sources','source_refs','locator','excerpt','file_sha256','sha256','doi','url','year','zotero_key','pdf_key','date_added','ga_attempts','ga_prompt_version','generation_elapsed_seconds','ga_qc','style','font_height_ratios','palette','max_labels','label_budget','content_area_target','title_max_width_ratio','order','position','template','number_id','label_id','claim_ids','label_ids','selected_modules','omissions','main_figures','figure','level','reference_images','reference_role'}

def normalize(text):
    t=unicodedata.normalize('NFKC',str(text)).replace('−','-').replace('–',' ').replace('—',' ')
    t=re.sub(r'\\(?:mathrm|text|operatorname|mathbf)\{([^{}]*)\}',r'\1',t)
    t=t.replace('$','').replace('{','').replace('}','').replace('\\,','').replace('\\%','%')
    t=re.sub(r'(?<=\d)\s*,\s*(?=\d{3}(?:\D|$))',',',t)
    return t
def key(v):
    try:return str(Decimal(str(v).replace(',','').replace('−','-').lstrip('+')).normalize())
    except InvalidOperation:raise ValueError('Invalid numeric token '+str(v))
def tokens(t):return [(m.group(),key(m.group()),m.start()) for m in TOKEN.finditer(normalize(t))]
def strip_nonresults(t):
    t=re.sub(r'^---\s*\n.*?\n---\s*\n','',t,flags=re.S)
    t=re.sub(r'!?\[\[.*?\]\]|!\[.*?\]\(.*?\)|https?://\S+|zotero://\S+','',t)
    t=re.sub(r'〔.*?〕|\b(?:Fig(?:ure)?|Table|Supplementary Fig(?:ure)?)\.?\s*\d+[A-Za-z]?','',t)
    t=re.sub(r'^\s*\d+\.\s+','',t,flags=re.M)
    t=re.sub(r'\[!step\].*?\d+[｜|]','[!step]',t)
    return t
def json_strings(obj,path=''):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k not in SKIP_KEYS:yield from json_strings(v,path+'.'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):yield from json_strings(v,path+f'[{i}]')
    elif isinstance(obj,(str,int,float)) and not isinstance(obj,bool):yield path,str(obj)

def verified_derivations(ledger,source):
    verified={};errors=[];norm=re.sub(r'\s+','',normalize(source))
    for c in (ledger or {}).get('claims',[]):
        if not c.get('derivation'):continue
        d=c['derivation'];excerpt=c.get('excerpt','');exnorm=re.sub(r'\s+','',normalize(excerpt));ts={k for _,k,_ in tokens(excerpt)}
        operands=[Decimal(str(x)) for x in d['operands']]
        if not excerpt or exnorm not in norm or not c.get('locator') or any(key(x) not in ts for x in operands):errors.append(c['id']+': operands/source passage not verified');continue
        op=d['operation']
        if op=='subtract' and len(operands)==2:value=operands[0]-operands[1]
        elif op=='add':value=sum(operands)
        elif op=='divide' and len(operands)==2 and operands[1]:value=operands[0]/operands[1]
        elif op=='multiply' and len(operands)==2:value=operands[0]*operands[1]
        else:errors.append(c['id']+': unsupported derivation');continue
        if key(value)!=key(c['value']):errors.append(c['id']+': incorrect derived value');continue
        verified[key(value)]=dict(claim_id=c['id'],locator=c['locator'],formula=d,unit=c.get('unit',''))
    return verified,errors

def verify(source,artifacts,ledger=None):
    source_tokens=tokens(source);index={}
    nsource=normalize(source)
    for raw,k,pos in source_tokens:
        index.setdefault(k,[]).append(dict(token=raw,context=nsource[max(0,pos-80):pos+110]))
    derived,errors=verified_derivations(ledger,source);rows=[]
    for name,kind,content in artifacts:
        fields=json_strings(content) if kind=='json' else [('',strip_nonresults(content))]
        for path,value in fields:
            val=strip_nonresults(value)
            for raw,k,pos in tokens(val):
                matches=index.get(k,[])
                status='derived_verified' if k in derived else 'matched_exact' if any(m['token']==raw for m in matches) else 'matched_normalized' if matches else 'not_found'
                rows.append(dict(artifact=name,field=path,value=raw,normalized=k,status=status,
                    artifact_context=normalize(val)[max(0,pos-45):pos+65],source_candidates=matches[:3],derivation=derived.get(k),
                    semantic_review='required: verify endpoint, group, unit, direction and adjustment; same number alone does not establish meaning'))
    return dict(status='pass' if not errors and all(r['status']!='not_found' for r in rows) else 'fail',
        source_sha256=hashlib.sha256(source.encode('utf-8')).hexdigest(),quantities=len(rows),not_found=sum(r['status']=='not_found' for r in rows),
        counts=dict(Counter(r['status'] for r in rows)),derivation_errors=errors,checks=rows,
        limitation='Textual/normalized matching and source-checked arithmetic; scientific semantic correctness requires the separate review.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--card',type=Path,required=True);p.add_argument('--story',type=Path);p.add_argument('--visual',type=Path);p.add_argument('--aux',nargs='*',type=Path,default=[]);p.add_argument('--ledger',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    paths=[x for x in [a.story,a.visual,*a.aux] if x]
    artifacts=[(str(a.card),'md',a.card.read_text(encoding='utf-8'))]+[(str(x),'json',json.loads(x.read_text(encoding='utf-8'))) for x in paths]
    r=verify(a.source.read_text(encoding='utf-8'),artifacts,json.loads(a.ledger.read_text(encoding='utf-8')) if a.ledger else None)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:r[k] for k in ['status','quantities','not_found','counts']},ensure_ascii=False))
    if r['status']!='pass':raise SystemExit(1)
if __name__=='__main__':main()
