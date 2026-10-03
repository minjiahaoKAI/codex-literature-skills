#!/usr/bin/env python3
"""Persist per-card elapsed time and enforce hard-error-only cover retries."""
from __future__ import annotations
import argparse,json,hashlib
import shutil
from datetime import datetime,timezone
from pathlib import Path
from validate_ga_briefs import qc_decision

def now():return datetime.now(timezone.utc).isoformat()
def elapsed(a,b):return round((datetime.fromisoformat(b)-datetime.fromisoformat(a)).total_seconds(),3)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def start(key,tier,operation='create'):
    return dict(schema_version='2.0',key=key,card_tier=tier,operation=operation,started_at=now(),finished_at=None,
        total_elapsed_seconds=None,ga_attempts=0,attempts=[],prompt_version='house-style-v1',feedback=None,style_references=[])
def begin_attempt(log,prompt):
    n=len(log['attempts'])
    if log.get('finished_at'):raise ValueError('Operation already finished')
    if n>=3:raise ValueError('Three-call maximum reached')
    if n:
        prior=log['attempts'][-1]
        if not prior.get('finished_at'):raise ValueError('Prior call is not reviewed')
        if not prior.get('qc',{}).get('hard_failures'):raise ValueError('Soft deviations do not authorize regeneration')
    archived=prompt.with_name(prompt.stem+f'_attempt_{n+1}'+prompt.suffix)
    if archived.exists() and digest(archived)!=digest(prompt):raise FileExistsError('Attempt prompt archive already contains different text')
    if not archived.exists():shutil.copy2(prompt,archived)
    log['attempts'].append(dict(number=n+1,started_at=now(),finished_at=None,prompt_sha256=digest(archived),prompt=str(archived),source_prompt=str(prompt),qc=None))
    log['ga_attempts']=n+1
    return log
def review(log,image,visual,qc):
    if not log['attempts'] or log['attempts'][-1].get('finished_at'):raise ValueError('No pending generation')
    item=log['attempts'][-1];end=now();item.update(finished_at=end,elapsed_seconds=elapsed(item['started_at'],end),
        image=str(image),image_sha256=digest(image),qc=qc_decision(visual,qc))
    return log
def finish(log,selected_attempt=None):
    passing=[a for a in log['attempts'] if a.get('qc',{}).get('ga_qc') in {'passed','passed_with_issues'}]
    if log['attempts'] and not passing:raise ValueError('No hard-passing cover; publication remains blocked')
    if log['attempts'] and not log['attempts'][-1].get('finished_at'):raise ValueError('Pending call')
    chosen=next((a for a in passing if a['number']==selected_attempt),None) if selected_attempt else (passing[-1] if passing else None)
    if passing and chosen is None:raise ValueError('Selected attempt does not pass hard gates')
    log['finished_at']=now();log['total_elapsed_seconds']=elapsed(log['started_at'],log['finished_at'])
    log['selected_attempt']=chosen['number'] if chosen else None;log['ga_qc']=chosen['qc']['ga_qc'] if chosen else 'not_generated'
    return log
def main():
    from _cli_io import utf8_stdio
    utf8_stdio()
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['start','attempt','review','finish','summary']);p.add_argument('--log',type=Path);p.add_argument('--key');p.add_argument('--tier',choices=['full','triage']);p.add_argument('--operation',default='create');p.add_argument('--prompt',type=Path);p.add_argument('--image',type=Path);p.add_argument('--visual',type=Path);p.add_argument('--qc',type=Path);p.add_argument('--logs',type=Path,nargs='*');a=p.parse_args()
    load=lambda f:json.loads(f.read_text(encoding='utf-8'))
    if a.action=='summary':
        rows=[load(x) for x in a.logs or []];complete=[r for r in rows if r.get('total_elapsed_seconds') is not None]
        print(json.dumps(dict(cards=len(complete),mean_elapsed_seconds=sum(r['total_elapsed_seconds'] for r in complete)/len(complete) if complete else None,ga_calls=sum(r['ga_attempts'] for r in complete)),indent=2));return
    if not a.log:p.error('--log required')
    if a.action=='start':
        if a.log.exists():raise FileExistsError('Log exists; resume instead of resetting attempts')
        if not a.key or not a.tier:p.error('--key and --tier required')
        log=start(a.key,a.tier,a.operation)
    else:
        log=load(a.log)
        if a.action=='attempt':begin_attempt(log,a.prompt)
        elif a.action=='review':review(log,a.image,load(a.visual),load(a.qc))
        else:finish(log)
    a.log.parent.mkdir(parents=True,exist_ok=True);a.log.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(action=a.action,ga_attempts=log['ga_attempts'],finished=bool(log['finished_at'])),ensure_ascii=False))
if __name__=='__main__':main()
