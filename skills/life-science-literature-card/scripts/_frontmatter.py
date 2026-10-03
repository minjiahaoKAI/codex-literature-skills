"""Lossless top-level frontmatter edits; not a general YAML parser."""
import json,re,hashlib
KEY=re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):(?:\s|$)')
GEN_START='%% generated:start %%'
GEN_END='%% generated:end %%'
USER=re.compile(r'%% user:start %%.*?%% user:end %%',re.S)
PRESERVE={'read_stage','zotero_annotations','projects','priority','date_added'}
AUTOMATED={'title','short_title','authors','year','journal','doi','url','zotero_key','pdf_key','mineru_source','source_status','mineru_mode','graphical_abstract','image_mode','card_cover','card_logic_map','card_summary','note_type','topics','methods','cssclasses','tags','last_literature_update','created_by','study_type','study_modifiers','publication_stage','design_summary','verdict','key_result','card_tier','ga_prompt_version','ga_attempts','ga_qc','generation_elapsed_seconds','generation_log','generated_content_sha256'}

AUTOMATED.update({'project_relevance','connection_types','verdict_reason'})

def split(text):
    if not text.startswith('---\n'):raise ValueError('Missing frontmatter')
    pos=text.find('\n---',4)
    if pos<0:raise ValueError('Unclosed frontmatter')
    raw=text[4:pos];end=pos+4
    if text[end:end+1]=='\n':end+=1
    blocks={};key=None
    for line in raw.splitlines(keepends=True):
        m=KEY.match(line)
        if m:
            key=m[1]
            if key in blocks:raise ValueError('Duplicate frontmatter key '+key)
            blocks[key]=line
        elif key:blocks[key]+=line
        elif line.strip():raise ValueError('Unsupported frontmatter preamble')
    for block in blocks.values():
        # Anchors/aliases cannot be safely merged by a stdlib subset parser.
        if re.search(r'(?:^|\s)[&*][A-Za-z_]',block) or '<<:' in block:raise ValueError('YAML anchors/aliases require manual review')
    return blocks,text[end:]

def value(blocks,name,default=''):
    if name not in blocks:return default
    raw=blocks[name].split(':',1)[1].strip()
    if '\n' in raw:return default
    if raw.startswith('"'):
        try:return json.loads(raw)
        except json.JSONDecodeError:raise ValueError('Unsupported quoted YAML scalar '+name)
    if raw.startswith("'") and raw.endswith("'"):return raw[1:-1].replace("''", "'")
    if raw in {'','null','~'}:return default
    return raw
def field(name,val):return name+': '+json.dumps(val,ensure_ascii=False)+'\n'
def join(blocks,body):return '---\n'+''.join(v if v.endswith('\n') else v+'\n' for v in blocks.values())+'---\n'+body
def generated(text):
    if text.count(GEN_START)!=1 or text.count(GEN_END)!=1:raise ValueError('Need exactly one generated region; legacy note needs manual adoption')
    a=text.index(GEN_START)+len(GEN_START);b=text.index(GEN_END)
    if b<a:raise ValueError('Invalid generated markers')
    return a,b,text[a:b]
def content_hash(body):
    _,_,region=generated(body)
    return hashlib.sha256(USER.sub('%% protected user region %%',region).encode('utf-8')).hexdigest()
def stamp(text):
    blocks,body=split(text)
    if GEN_START in body:blocks['generated_content_sha256']=field('generated_content_sha256',content_hash(body))
    return join(blocks,body)
def merge(old,new,cover_only=False):
    oldfm,oldbody=split(old);newfm,newbody=split(new)
    if value(oldfm,'zotero_key')!=value(newfm,'zotero_key'):raise ValueError('Zotero identity mismatch')
    if cover_only:
        allowed={'card_cover','ga_prompt_version','ga_attempts','ga_qc','graphical_abstract','image_mode','generation_elapsed_seconds','generation_log','last_literature_update'}
        oldcover=value(oldfm,'card_cover');newcover=value(newfm,'card_cover')
        if not oldcover or not newcover:raise ValueError('Cover-only update requires old/new cover links')
        oldpath=oldcover.removeprefix('[[').removesuffix(']]').split('|',1)[0]
        newpath=newcover.removeprefix('[[').removesuffix(']]').split('|',1)[0]
        body=re.sub(r'(!?\[\[)'+re.escape(oldpath)+r'(?=[|\]])',lambda m:m[1]+newpath,oldbody)
        merged=dict(oldfm)
        for k in allowed:
            if k in newfm:merged[k]=newfm[k]
        prior_hash=value(oldfm,'generated_content_sha256')
        if GEN_START in oldbody and prior_hash==content_hash(oldbody):return stamp(join(merged,body))
        return join(merged,body)
    if value(oldfm,'card_tier')=='full' and value(newfm,'card_tier')=='triage':raise ValueError('Refusing full-to-triage downgrade')
    a,b,oldregion=generated(oldbody);_,_,newregion=generated(newbody)
    oldhash=value(oldfm,'generated_content_sha256')
    if not oldhash or oldhash!=content_hash(oldbody):raise ValueError('Generated text modified or no baseline hash; manual merge required')
    users=USER.findall(oldregion)
    if users:
        if len(USER.findall(newregion))!=len(users):raise ValueError('User-region structure changed')
        it=iter(users);newregion=USER.sub(lambda _:next(it),newregion)
    body=oldbody[:a]+newregion+oldbody[b:]
    merged=dict(oldfm)
    for k,v in newfm.items():
        if k not in PRESERVE and (k in AUTOMATED or k not in merged):merged[k]=v
    return stamp(join(merged,body))
