#!/usr/bin/env python3
"""Install/update staged cards transactionally, preserving protected user content."""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,struct,uuid
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from _frontmatter import split,value,merge,stamp
from validate_ga_briefs import qc_decision

def relative_folder(v):
    n=v.replace('\\','/');p=PurePosixPath(n)
    if not n or n.startswith('/') or ':' in n or any(x in {'.','..'} for x in n.split('/')):raise ValueError('Unsafe vault-relative folder')
    return Path(*p.parts)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def guarded(p,vault):
    if not p.resolve().is_relative_to(vault):raise ValueError('Target leaves selected vault')
    return p
def tree_hash(p):return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file()}
def png_size(p):
    h=p.read_bytes()[:24]
    if len(h)!=24 or h[:8]!=b'\x89PNG\r\n\x1a\n' or h[12:16]!=b'IHDR':raise ValueError('Invalid PNG header')
    return struct.unpack('>II',h[16:24])
def remove_owned(p,vault):
    guarded(p,vault)
    if p.is_dir():shutil.rmtree(p)
    elif p.exists():p.unlink()
def copy_checked(src,dst):
    if src.is_dir():
        shutil.copytree(src,dst)
        if tree_hash(src)!=tree_hash(dst):raise RuntimeError('Directory hash mismatch')
    else:
        shutil.copy2(src,dst)
        if sha(src)!=sha(dst):raise RuntimeError('File hash mismatch')

def run(args):
    vault=args.vault.resolve()
    if not vault.is_dir() or not (vault/'.obsidian').is_dir():raise ValueError('Not an Obsidian vault')
    if not args.note or not args.note.is_file():raise ValueError('Missing staged note')
    text=args.note.read_text(encoding='utf-8')
    if '\ufffd' in text:raise ValueError('Replacement character in note')
    fm,_=split(text);key=value(fm,'zotero_key')
    if not key or '/' in key or '\\' in key or ':' in key or key in {'.','..'}:raise ValueError('Invalid Zotero/source key')
    if value(fm,'note_type')!='literature-card':raise ValueError('Not a literature card')
    for k in ['card_cover','card_summary','card_logic_map','source_status','mineru_mode','pdf_key','cssclasses']:
        if k not in fm:raise ValueError('Missing field '+k)
    nf=relative_folder(args.notes_folder);af=relative_folder(args.assets_folder)
    existing=[]
    note_root=guarded(vault/nf,vault)
    if note_root.exists():
        for p in note_root.rglob('*.md'):
            try:
                ef,_=split(p.read_text(encoding='utf-8'))
                if value(ef,'zotero_key')==key and value(ef,'note_type')=='literature-card':existing.append(p)
            except ValueError:continue
    if len(existing)>1:raise ValueError('Multiple cards share identity in this notes folder')
    if existing and args.skip_existing:return dict(status='skipped',zotero_key=key)
    if existing and not args.update:raise FileExistsError('Card already exists; use explicit --update or --skip-existing')
    if args.cover_only and (not args.update or not existing):raise ValueError('--cover-only needs an existing card and --update')
    target_note=existing[0] if existing else guarded(vault/nf/args.note.name,vault)
    if target_note.exists() and not existing:raise FileExistsError('Filename belongs to another note')
    old_assets=[]
    if existing:
        oldtext=target_note.read_text(encoding='utf-8');oldfm,_=split(oldtext)
        for field_name in ['card_cover','card_logic_map']:
            link=value(oldfm,field_name)
            if link and not link.startswith(('http://','https://')):
                path=link.removeprefix('[[').removesuffix(']]').split('|',1)[0]
                old_assets.append(guarded(vault/relative_folder(path),vault))
        text=merge(oldtext,text,args.cover_only)
    else:text=stamp(text)
    fm,_=split(text);tier=value(fm,'card_tier','full');cover=value(fm,'card_cover');logic=value(fm,'card_logic_map')
    v2='card_tier' in fm
    if tier=='full' and not args.cover_only and (not cover or not logic):raise ValueError('Full card requires cover and logic map')
    if cover and value(fm,'ga_qc')=='failed':raise ValueError('Hard-failed cover cannot be installed')
    if v2:
        if not args.number_report or not args.number_report.is_file():raise ValueError('v2 requires numeric verification report')
        report=json.loads(args.number_report.read_text(encoding='utf-8'))
        if report.get('status')!='pass' or report.get('not_found')!=0:raise ValueError('Unresolved scientific numbers')
        if report.get('card_sha256')!=sha(args.note):raise ValueError('Numeric report is stale or lacks note hash')
        if cover:
            if not args.qc or not args.visual_brief:raise ValueError('Generated v2 cover requires QC and visual brief')
            raw_qc=json.loads(args.qc.read_text(encoding='utf-8'))
            if not args.graphical_abstract or raw_qc.get('image_sha256')!=sha(args.graphical_abstract):raise ValueError('QC is stale or lacks selected PNG hash')
            decision=qc_decision(json.loads(args.visual_brief.read_text(encoding='utf-8')),raw_qc)
            if decision['ga_qc']=='failed':raise ValueError('Cover fails hard gates')
    source=args.source_directory or args.mineru_directory
    if tier=='full' and not args.cover_only and (not source or not source.is_dir()):raise ValueError('Full card requires extracted source directory')
    if source and source.name!=key:raise ValueError('Source directory name must match Zotero key')
    source_folder=relative_folder(args.sources_folder if tier=='full' else args.triage_sources_folder)
    mapping=[];staged={}
    # No-cover triage uses shared gallery resources; do not set card_cover.
    if tier=='triage' and not cover:
        from build_card_placeholders import ASSETS,TYPES,VAULT_FOLDER
        for name in TYPES:
            placeholder=ASSETS/(name+'.svg')
            if not placeholder.is_file():raise ValueError('Missing shared placeholder '+name)
            ET.parse(placeholder)
            target=guarded(vault/relative_folder(VAULT_FOLDER)/placeholder.name,vault)
            mapping.append((placeholder,target));staged[target]=placeholder
    if source:
        if not any(p.suffix=='.md' and p.stat().st_size for p in source.rglob('*') if p.is_file()):raise ValueError('Source directory has no readable Markdown')
        starget=guarded(vault/source_folder/key,vault)
        if source.resolve()==starget.resolve():raise ValueError('Stage outside the target source directory')
        mapping.append((source,starget));staged[starget]=source
    # Cover/map plus other embedded helper SVGs referenced by this card.
    local_files={}
    for p in [args.graphical_abstract,args.logic_map]:
        if p:local_files[p.name]=p
    if args.assets_directory:
        local_files.update({p.name:p for p in args.assets_directory.iterdir() if p.is_file()})
    links=set(re.findall(r'!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]',text))
    for link in [cover,logic]:
        if link:links.add(link.removeprefix('[[').removesuffix(']]').split('|',1)[0])
    for link in links:
        lp=relative_folder(link.split('#',1)[0]);target=guarded(vault/lp,vault)
        if lp.parts[:len(af.parts)]==af.parts:
            src=local_files.get(lp.name)
            if src:
                if not src.is_file() or not src.stat().st_size:raise ValueError('Missing visual asset')
                if src.suffix.lower()=='.svg':
                    tx=src.read_text(encoding='utf-8')
                    if '\ufffd' in tx:raise ValueError('Corrupt SVG')
                    ET.fromstring(tx)
                if src.suffix.lower()=='.png' and min(png_size(src))<100:raise ValueError('Implausibly small PNG')
                mapping.append((src,target));staged[target]=src
            elif not target.is_file():raise ValueError('Missing embedded asset '+link)
        elif source and target.is_relative_to(vault/source_folder/key):
            if not (source/target.relative_to(vault/source_folder/key)).is_file():raise ValueError('Missing source image '+link)
        elif not target.is_file():raise ValueError('Unresolved embed '+link)
    # Keep source originals and merge only during an explicitly authorized update.
    plan=[]
    for src,target in mapping:
        if target.exists():
            equal=tree_hash(src)==tree_hash(target) if src.is_dir() else sha(src)==sha(target)
            if equal:continue
            if not args.update:raise FileExistsError('Different existing asset/source; explicit update required')
        plan.append((src,target))
    if args.dry_run:return dict(status='ready',zotero_key=key,action='update' if existing else 'create',note=str(target_note),targets=[str(t) for _,t in plan],protected_merge=bool(existing))
    uid=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    backup=guarded(vault/nf/'_backup'/uid,vault);temps=[];backups={};changed=[];created=[]
    try:
        # An upgrade often uses a new cover filename. Back up the old linked
        # image/map even when neither is a replacement target in this plan.
        all_targets=list(dict.fromkeys([target_note]+[t for _,t in plan]+old_assets))
        for target in all_targets:
            guarded(target,vault)
            if target.exists():
                b=backup/target.relative_to(vault);b.parent.mkdir(parents=True,exist_ok=True);copy_checked(target,b);backups[target]=b
        for src,target in plan:
            target.parent.mkdir(parents=True,exist_ok=True);tmp=guarded(target.with_name(target.name+'.codex-tmp-'+uid),vault);temps.append(tmp)
            if src.is_dir() and target.exists():
                copy_checked(target,tmp)
                for f in src.rglob('*'):
                    if f.is_file():
                        dest=tmp/f.relative_to(src);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
                        if sha(f)!=sha(dest):raise RuntimeError('Merged source hash mismatch')
            else:copy_checked(src,tmp)
        target_note.parent.mkdir(parents=True,exist_ok=True);ntmp=guarded(target_note.with_name(target_note.name+'.codex-tmp-'+uid),vault);ntmp.write_text(text,encoding='utf-8');temps.append(ntmp)
        operations=list(zip(temps[:-1],[t for _,t in plan]))+[(ntmp,target_note)]
        for tmp,target in operations:
            existed=target.exists()
            if target.is_dir():
                hold=guarded(target.with_name(target.name+'.codex-old-'+uid),vault);target.rename(hold);temps.append(hold)
                changed.append(target);tmp.rename(target)
            else:
                changed.append(target);os.replace(tmp,target)
            if not existed:created.append(target)
            os.utime(target,None)
        for p in temps:
            if p.exists():remove_owned(p,vault)
        if backups:
            (backup/'manifest.json').write_text(json.dumps({'zotero_key':key,'targets':[str(t.relative_to(vault)) for t in backups]},ensure_ascii=False,indent=2),encoding='utf-8')
        return dict(status='updated' if existing else 'created',note=str(target_note),zotero_key=key,backup=str(backup) if backups else None,visual_render_verification='required_in_obsidian')
    except Exception:
        for t in reversed(changed):
            if t in backups:
                if t.exists():remove_owned(t,vault)
                copy_checked(backups[t],t)
            elif t in created and t.exists():remove_owned(t,vault)
        for p in temps:
            if p.exists():remove_owned(p,vault)
        raise

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--vault',type=Path,required=True)
    for n in ['note','graphical-abstract','logic-map','mineru-directory','source-directory','assets-directory','number-report','qc','visual-brief','batch']:p.add_argument('--'+n,type=Path)
    p.add_argument('--notes-folder',default='文献笔记');p.add_argument('--assets-folder',default='图片资源/literature_cards');p.add_argument('--sources-folder',default='sources/mineru');p.add_argument('--triage-sources-folder',default='sources/literature')
    for n in ['dry-run','update','skip-existing','cover-only']:p.add_argument('--'+n,action='store_true')
    return p
def main():
    from _cli_io import utf8_stdio
    utf8_stdio()
    p=parser();a=p.parse_args()
    if not a.batch:
        try:r=run(a)
        except Exception as e:print(json.dumps({'status':'failed','error':str(e)},ensure_ascii=False));raise SystemExit(1)
        print(json.dumps(r,ensure_ascii=False,indent=2));return
    manifest=json.loads(a.batch.read_text(encoding='utf-8'));rows=manifest.get('cards',manifest) if isinstance(manifest,dict) else manifest
    results=[];paths={'note','graphical_abstract','logic_map','mineru_directory','source_directory','assets_directory','number_report','qc','visual_brief'}
    for i,row in enumerate(rows):
        opts=vars(a).copy()
        for k,v in row.items():
            if k not in opts:continue
            opts[k]=(a.batch.parent/Path(v)).resolve() if k in paths and v else v
        try:r=run(argparse.Namespace(**opts))
        except Exception as e:r={'status':'failed','error':str(e)}
        results.append({'index':i,**r})
    print(json.dumps({'results':results,'failed':sum(x['status']=='failed' for x in results)},ensure_ascii=False,indent=2))
    if any(x['status']=='failed' for x in results):raise SystemExit(1)
if __name__=='__main__':main()
