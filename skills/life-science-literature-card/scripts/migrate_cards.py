#!/usr/bin/env python3
"""Opt-in metadata-only migration, automatic backup; never rewrite card bodies."""
import argparse,json,shutil,uuid
from datetime import datetime,timezone
from pathlib import Path
from _frontmatter import split,value,field,join

def migrate(text):
    fm,body=split(text)
    if value(fm,'note_type')!='literature-card':return text,[]
    defaults={'study_type':'other','design_summary':'','verdict':'','key_result':'','date_added':'',
              'card_tier':'full' if value(fm,'mineru_source') else 'triage','ga_prompt_version':'legacy',
              'ga_attempts':None,'ga_qc':'unverified','generation_elapsed_seconds':None,'generation_log':''}
    missing=[k for k in defaults if k not in fm]
    for k in missing:fm[k]=field(k,defaults[k])
    return join(fm,body),missing
def main():
    from _cli_io import utf8_stdio
    utf8_stdio()
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--folder',type=Path,required=True);p.add_argument('--dry-run',action='store_true');a=p.parse_args();root=a.folder.resolve();rows=[]
    if not root.is_dir():raise ValueError('Missing note folder')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    for f in root.rglob('*.md'):
        if '_backup' in f.relative_to(root).parts:continue
        if not f.resolve().is_relative_to(root):raise ValueError('Symlink leaves notes folder')
        try:
            new,missing=migrate(f.read_text(encoding='utf-8'))
            if missing and not a.dry_run:
                backup=root/'_backup'/stamp/f.relative_to(root);backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,backup)
                f.write_text(new,encoding='utf-8')
            rows.append({'file':f.name,'missing':missing,'status':'planned' if missing and a.dry_run else 'updated' if missing else 'unchanged'})
        except ValueError as e:rows.append({'file':f.name,'status':'conflict','error':str(e)})
    print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
