#!/usr/bin/env python3
"""Assemble the approved fixed style and a source-validated visual brief."""
import argparse,json,re
from pathlib import Path
from validate_ga_briefs import validate

def build(story,visual,evidence=None,feedback=''):
    validate(story,visual,evidence)
    style=(Path(__file__).resolve().parents[1]/'references/graphical-abstract/house-style.md').read_text(encoding='utf-8')
    fixed=re.search(r'<!-- prompt:start -->\s*(.*?)\s*<!-- prompt:end -->',style,re.S).group(1)
    out=['# Graphical abstract · house-style-v1','',fixed,'',f"Scope: {story['card_tier']}; {story['paper_type']}; {story['complexity']}; shape {story['finding_shape']}.",
         'Story: '+story['one_line_story'],'Key concept: '+story['key_concept_plain'],
         'Layout: '+visual['layout'],'Focal point: '+visual.get('focal_point','central findings'),
         'MUST NOT SHOW: '+'; '.join(story['must_not_show']),
         'Exact label inventory (no added text; preserve all letters, numbers and symbols):']
    for x in visual['labels']:out.append(f"{x['id']} [{x['role']}; {x.get('status','neutral')}]: {x['text']}")
    out+=['','Panel instructions:']
    for p in visual['panels']:
        out.append(f"{p['id']} at {p['position']}: {p['description']}; labels {', '.join(p['label_ids'])}.")
        for i in p.get('icons',[]):out.append(f"  Labeled icon: {i['name']}, next to label {i['label_id']}.")
    out+=['','Allowed connectors only:']
    for c in visual.get('connectors',[]):
        out.append(f"{c['from']} → {c['to']}: {c['semantic']}, {c['style']}. No additional arrow caption.")
        if c.get('label'):out.append('Planning note only, NOT visible text: '+c['label'])
    if not visual.get('connectors'):out.append('No relational arrows between panels. Direction arrows already appear only in exact finding labels.')
    out+=['','No invented data or tissues. Show every inventory label once, including any connector annotations; do not render planning notes, extra icon sublabels or repeated labels. No organ glyph for a diagnosis when that organ was not measured. No grids, bars or curves invented to depict a result.']
    if feedback:out+=['','User feedback within approved scientific/style boundaries:',feedback]
    return '\n'.join(out)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['story','visual','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--evidence',type=Path);p.add_argument('--feedback',type=Path);a=p.parse_args()
    load=lambda f:json.loads(f.read_text(encoding='utf-8'))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(build(load(a.story),load(a.visual),load(a.evidence) if a.evidence else None,a.feedback.read_text(encoding='utf-8') if a.feedback and a.feedback.exists() else ''),encoding='utf-8')
if __name__=='__main__':main()
