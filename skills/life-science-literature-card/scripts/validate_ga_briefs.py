#!/usr/bin/env python3
"""Validate GA facts, label references, complexity and evidence-map coverage."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

TYPES={'observational-cohort','rct','neuroimaging','prediction-model','genetic-mr','systematic-review-meta','basic-mechanism','other'}
SHAPES={'contrast','gradient','trajectory','mechanism_chain','risk_stratification','null_result','mixed','protocol'}
HARD_CHECKS=('literal_text','numbers','direction','evidence_type','association_as_cause','unmeasured_organs','cartoon_elements')

def refs(value, sources, where):
    if not isinstance(value,list) or not value or any(x not in sources for x in value):
        raise ValueError(f'{where}: missing/unknown source IDs')

def validate(story,visual,evidence=None):
    for k in ('schema_version','paper_type','card_tier','complexity','one_line_story','key_concept_plain','finding_shape','sources','main_findings','must_not_show','numbers_allowed'):
        if k not in story:raise ValueError(f'story missing {k}')
    if story['paper_type'] not in TYPES or story['card_tier'] not in {'full','triage'}:raise ValueError('Invalid paper type/tier')
    if story['complexity'] not in {'simple','complex'} or story['finding_shape'] not in SHAPES:raise ValueError('Invalid complexity/shape')
    sources=story['sources']
    if not sources or any(not x.get('locator') for x in sources.values()):raise ValueError('Sources need locators')
    claims={x['id']:x for x in story['main_findings']}
    if len(claims)!=len(story['main_findings']):raise ValueError('Duplicate claim ID')
    for x in claims.values():
        refs(x.get('source'),sources,'finding '+x['id'])
        if x['relation'] not in {'association','causal_evidence','prediction','mechanism','planned'}:raise ValueError('Invalid relation')
        if x['direction'] not in {'increase','decrease','no_difference','mixed','uncertain','not_applicable'}:raise ValueError('Invalid direction')
        if x.get('status') not in {'changed','associated','supported','null','unconfirmed','unsupported','planned','neutral'}:raise ValueError('Invalid finding status')
    if story.get('publication_stage')=='protocol' and claims:raise ValueError('Protocol cannot have observed findings')
    if not isinstance(story['must_not_show'],list):raise ValueError('must_not_show must be a list')
    if len(story.get('outcomes_named',[]))>5:raise ValueError('At most five named cover outcomes')
    for x in story.get('outcomes_named',[]):refs(x.get('source'),sources,'named outcome')
    shape=story['finding_shape']
    shape_fields={'contrast':'hero_contrast','gradient':'hero_contrast','trajectory':'trajectories','mechanism_chain':'mechanism_chain','risk_stratification':'risk_strata','null_result':'null_comparison'}
    if story['complexity']=='simple' and shape in shape_fields and not story.get(shape_fields[shape]):raise ValueError('Missing finding-shape structure')
    if story['complexity']=='complex' and story['card_tier']=='full':
        if evidence is None:raise ValueError('Complex full paper requires evidence_map')
        required={'paper_title_claim','primary_endpoint','main_figures','modules','integrated_conclusion','tension','sources'}
        if not required<=evidence.keys():raise ValueError('Incomplete evidence map')
        modules={m['id']:m for m in evidence['modules']}
        if len(modules)!=len(evidence['modules']):raise ValueError('Duplicate evidence module')
        for f in evidence['main_figures']:
            if not any(m['figure']==f for m in modules.values()):raise ValueError('Missing main figure '+f)
        for m in modules.values():
            refs(m.get('source'),evidence['sources'],'module '+m['id'])
            if m['evidence_strength'] not in {'primary','secondary','exploratory'}:raise ValueError('Invalid evidence strength')
        selected=story.get('selected_modules',[])
        if not selected or any(not m.get('why') or any(i not in modules for i in m['ids']) for m in selected):raise ValueError('Invalid module selection')
    labels={x['id']:x for x in visual['labels']}
    if len(labels)!=len(visual['labels']):raise ValueError('Duplicate planned label')
    if len(labels)>visual.get('label_budget',24 if visual['layout']=='complex' else 16):raise ValueError('Label budget exceeded')
    for x in labels.values():
        if not x['text'] or '\ufffd' in x['text']:raise ValueError('Empty/corrupt label')
        refs(x.get('source'),sources,'label '+x['id'])
        if x['role'] not in {'title','finding','section','method','body','footer'}:raise ValueError('Invalid text role')
        if any(c not in claims for c in x.get('claim_ids',[])):raise ValueError('Unknown label claim')
    nums={x['id']:x for x in story['numbers_allowed']}
    if len(nums)!=len(story['numbers_allowed']):raise ValueError('Duplicate numeric ID')
    for x in nums.values():refs(x.get('source'),sources,'number '+x['id'])
    for x in visual.get('numbers_in_image',[]):
        if x['number_id'] not in nums or x['label_id'] not in labels:raise ValueError('Unknown displayed number')
    if story['card_tier']=='triage' and visual.get('numbers_in_image'):raise ValueError('Triage cover must omit scientific numbers')
    panel_ids={p['id'] for p in visual['panels']}
    central={p['id'] for p in visual['panels'] if p.get('kind')=='evidence'}
    for p in visual['panels']:
        if any(i not in labels for i in p['label_ids']):raise ValueError('Unknown panel label')
        for icon in p.get('icons',[]):
            if icon.get('label_id') not in p['label_ids']:raise ValueError('Unlabeled semantic icon')
            refs(icon.get('source'),sources,'icon '+icon['name'])
    for c in visual.get('connectors',[]):
        if c['from'] in central and c['to'] in central and visual['layout']=='complex':raise ValueError('Arrow between parallel evidence modules')
        if c['semantic'] not in {'workflow','temporal','association','causal_evidence','hypothesis'}:raise ValueError('Unknown connector meaning')
        refs(c.get('source'),sources,'connector')
        if c['semantic'] in {'association','hypothesis'} and c['style']!='dashed':raise ValueError('Uncertain link must be dashed')
    if visual.get('text_overlay'):raise ValueError('Text overlay is not enabled')
    return {'status':'pass','labels':len(labels),'claims':len(claims),'evidence_map_required':story['complexity']=='complex' and story['card_tier']=='full'}

def qc_decision(visual,qc):
    planned={x['id']:x['text'] for x in visual['labels']}
    actual={};duplicates=[]
    for x in qc.get('transcription',[]):
        if x['id'] in actual:duplicates.append(x['id'])
        actual[x['id']]=x['text']
    text_ok=actual==planned and not duplicates and not qc.get('unplanned_text',[])
    checks=dict(qc.get('hard_checks',{}))
    checks['literal_text']='pass' if text_ok and checks.get('literal_text')=='pass' else 'fail'
    unresolved=[k for k in HARD_CHECKS if checks.get(k)!='pass']
    actual_failures=[k for k in HARD_CHECKS if checks.get(k)=='fail']
    soft=qc.get('soft_observations',[])
    return {'ga_qc':'failed' if unresolved else 'passed_with_issues' if soft else 'passed',
            'hard_unresolved':unresolved,'hard_failures':actual_failures,'hard_checks':checks,'soft_observations':soft,
            'review_method':qc.get('review_method','unspecified')}

def main():
    from _cli_io import utf8_stdio
    utf8_stdio()
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--story',type=Path,required=True);p.add_argument('--visual',type=Path,required=True);p.add_argument('--evidence',type=Path);p.add_argument('--qc',type=Path)
    a=p.parse_args();load=lambda f:json.loads(f.read_text(encoding='utf-8'))
    v=load(a.visual);r=validate(load(a.story),v,load(a.evidence) if a.evidence else None)
    if a.qc:r['qc']=qc_decision(v,load(a.qc))
    print(json.dumps(r,ensure_ascii=False,indent=2))
    if a.qc and r['qc']['ga_qc']=='failed':raise SystemExit(1)
if __name__=='__main__':main()
