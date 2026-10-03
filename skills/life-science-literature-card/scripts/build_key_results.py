#!/usr/bin/env python3
"""Draw 2–8 explicitly reported effects/metrics; never impute intervals."""
import argparse,json,math
from pathlib import Path
import _style as s
from _svg import lines,text,multiline,start,source_lines
def build(data):
    rows=data['rows'];mode=data.get('mode','forest')
    if not 2<=len(rows)<=8:raise ValueError('Expected 2–8 reported results')
    if mode not in {'forest','metrics'}:raise ValueError('Unknown result mode')
    if any(not r.get('source') for r in rows):raise ValueError('Every result needs a source')
    ratio=data.get('effect_scale','HR') in {'HR','OR','RR'}
    if mode=='forest':
        if any(not all(k in r for k in ['estimate','lower','upper']) for r in rows):raise ValueError('Forest rows require reported CIs')
        if any(not r['lower']<=r['estimate']<=r['upper'] for r in rows):raise ValueError('Invalid interval')
        if ratio and any(r['lower']<=0 for r in rows):raise ValueError('Ratio limits must be positive')
        transform=math.log if ratio else float;null=1 if ratio else 0
        lo=min([transform(null)]+[transform(r['lower']) for r in rows]);hi=max([transform(null)]+[transform(r['upper']) for r in rows])
    else:
        if any('estimate' not in r for r in rows):raise ValueError('Metric row needs estimate')
        transform=float;lo=min([0]+[r['estimate'] for r in rows]);hi=max([0]+[r['estimate'] for r in rows])
    span=hi-lo or 1;lo-=span*.12;hi+=span*.12
    X=lambda v:480+(transform(v)-lo)/(hi-lo)*390
    wrapped=[lines(r['label'],390,23) for r in rows];heights=[max(75,28+len(x)*31) for x in wrapped]
    hdr=lines(data.get('title','关键结果'),1100,32);top=65+len(hdr)*44;src=source_lines(data);h=top+sum(heights)+75+len(src)*26
    out=[start(1200,h,data.get('title','关键结果')),multiline(45,45,hdr,32,'title')]
    if mode=='forest':out.append(f'<path d="M{X(null):g},{top-20} V{top+sum(heights):g}" stroke="{s.NULL}" stroke-width="1.5" stroke-dasharray="5 5"/>')
    y=top
    for r,lab,hh in zip(rows,wrapped,heights):
        color=s.NULL if r.get('status') in {'null','unconfirmed','unsupported'} else s.ACCENT
        out.append(multiline(45,y+24,lab,23));yy=y+hh/2
        if mode=='forest':
            a,b=X(r['lower']),X(r['upper']);out.append(f'<path d="M{a:g},{yy:g} H{b:g} M{a:g},{yy-6:g} V{yy+6:g} M{b:g},{yy-6:g} V{yy+6:g}" stroke="{color}" stroke-width="2"/>');value=f"{r['estimate']:g} ({r['lower']:g}–{r['upper']:g})"
        else:
            out.append(f'<path d="M{X(0):g},{yy:g} H{X(r["estimate"]):g}" stroke="{color}" stroke-width="8"/>');value=f"{r['estimate']:g} {r.get('unit','')}"
        out.append(f'<circle cx="{X(r["estimate"]):g}" cy="{yy:g}" r="5" fill="{color}"/>');out.append(text(915,yy+8,value,22,'finding',r.get('status','changed')));y+=hh
    out.extend([text(480,y+32,'对数比例尺度；虚线为无效值' if mode=='forest' and ratio else '线性尺度；仅重绘报告值',18,'footer'),multiline(45,y+65,src,19,'footer'),'</svg>']);return '\n'.join(out)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(build(json.loads(a.input.read_text(encoding='utf-8'))),encoding='utf-8')
if __name__=='__main__':main()
