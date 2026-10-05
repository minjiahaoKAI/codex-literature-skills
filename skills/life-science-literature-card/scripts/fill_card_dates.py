#!/usr/bin/env python3
"""Fill empty date_added from read-only Zotero metadata, then file creation date."""
import argparse,json,sqlite3,shutil,uuid
from contextlib import closing
from pathlib import Path
from datetime import date,datetime,timezone
from _frontmatter import split,value,field,join

def zotero_dates(db):
    if not db:return {}
    uri=db.resolve().as_uri()+'?mode=ro'
    with closing(sqlite3.connect(uri,uri=True)) as conn:
        records={}
        for key,added in conn.execute('SELECT key,dateAdded FROM items'):
            records.setdefault(key,[]).append(added)
    # Ambiguous library identities cannot determine a reliable timestamp.
    return {k:v[0] for k,v in records.items() if len(v)==1}

def added_date(raw):
    parsed=datetime.fromisoformat(raw.replace('Z','+00:00'))
    if parsed.tzinfo is None:parsed=parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone().date().isoformat()

def plan(vault,db=None,fallback=None):
    vault=vault.resolve();dates=zotero_dates(db);rows=[]
    for p in (vault/'文献笔记').rglob('*.md'):
        if '_backup' in p.parts:continue
        if not p.resolve().is_relative_to(vault):raise ValueError('Note leaves selected Vault')
        fm,body=split(p.read_text(encoding='utf-8'))
        if value(fm,'note_type')!='literature-card':continue
        old=value(fm,'date_added');rel=p.relative_to(vault).as_posix()
        if old:
            date.fromisoformat(old)
            rows.append({'path':rel,'status':'unchanged','date_added':old});continue
        key=value(fm,'zotero_key');raw=dates.get(key)
        if raw:new=added_date(raw);source='zotero.items.dateAdded';original=raw
        else:
            if fallback and rel in fallback:new=fallback[rel];source='original_file_creation';original=new
            else:
                stat=p.stat();timestamp=getattr(stat,'st_birthtime',None)
                if timestamp is None:raise ValueError('Creation time unavailable; supply original file dates for '+rel)
                new=datetime.fromtimestamp(timestamp).date().isoformat();source='file_creation';original=str(timestamp)
        date.fromisoformat(new);fm['date_added']=field('date_added',new)
        rows.append({'path':rel,'status':'planned','zotero_key':key,'date_added':new,'source':source,'source_value':original,'new_text':join(fm,body)})
    return rows

def main():
    from _cli_io import utf8_stdio
    utf8_stdio();p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--vault',required=True,type=Path);p.add_argument('--zotero-db',type=Path)
    p.add_argument('--fallback-file-dates',type=Path,help='Original creation dates keyed by Vault-relative path, for copied test Vaults')
    p.add_argument('--report',required=True,type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args()
    rows=plan(a.vault,a.zotero_db,json.loads(a.fallback_file_dates.read_text(encoding='utf-8')) if a.fallback_file_dates else None)
    backup=a.vault/'文献笔记/_backup'/('date-added-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    for row in rows:
        text=row.pop('new_text',None)
        if text and a.apply:
            path=a.vault/row['path'];dest=backup/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
            path.write_text(text,encoding='utf-8');row['status']='updated'
    report={'mode':'apply' if a.apply else 'dry-run','cards':len(rows),'filled':sum(r['status'] in {'planned','updated'} for r in rows),'rows':rows}
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False))
if __name__=='__main__':main()
