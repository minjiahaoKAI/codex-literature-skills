#!/usr/bin/env python3
"""Stdlib package/frontmatter/link/import validation without installing PyYAML."""
import argparse,ast,json,re,sys
from pathlib import Path
from _frontmatter import split,value
from _cli_io import utf8_stdio

def validate(root):
    errors=[];entry=root/'SKILL.md';text=entry.read_text(encoding='utf-8');fm,body=split(text)
    name=value(fm,'name');description=value(fm,'description')
    if not re.fullmatch('[a-z0-9-]{1,64}',name):errors.append('Invalid skill name')
    if not description or len(description)>1024:errors.append('Invalid description')
    if len(text.splitlines())>250:errors.append('SKILL.md exceeds 250 lines')
    if 'TODO' in text or '[INSERT' in text:errors.append('Unfinished scaffold')
    local={p.stem for p in (root/'scripts').glob('*.py')};imports=set();links=0
    for f in root.rglob('*'):
        if not f.is_file() or '__pycache__' in f.parts or 'style-refs' in f.parts:continue
        if f.suffix in {'.md','.py','.json','.yaml','.css','.base'}:
            t=f.read_text(encoding='utf-8')
            if '\ufffd' in t:errors.append('Replacement character: '+str(f.relative_to(root)))
            if f.suffix=='.json':json.loads(t)
            if f.suffix=='.py':
                tree=ast.parse(t)
                for n in ast.walk(tree):
                    names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.module else []
                    for name in names:
                        top=name.split('.')[0];imports.add(top)
                        if top not in sys.stdlib_module_names and top not in local:errors.append('Non-stdlib runtime dependency '+top)
            if f.suffix=='.md':
                for target in re.findall(r'\]\(([^)]+)\)',t):
                    if '://' in target or target.startswith('#') or '<' in target:continue
                    target=target.split('#',1)[0]
                    if target:
                        links+=1
                        if not (f.parent/target).exists():errors.append('Broken local link '+str(f.relative_to(root))+': '+target)
    return {'status':'pass' if not errors else 'fail','skill_lines':len(text.splitlines()),'local_links':links,'runtime_imports':sorted(imports),'errors':errors}
def main():
    utf8_stdio();p=argparse.ArgumentParser();p.add_argument('skill',type=Path);a=p.parse_args();r=validate(a.skill);print(json.dumps(r,ensure_ascii=False,indent=2))
    if r['status']=='fail':raise SystemExit(1)
if __name__=='__main__':main()
