#!/usr/bin/env python3
"""Create a sourced cohort, RCT or pipeline study-design SVG."""
import argparse,json
from pathlib import Path
from _svg import lines,multiline,rect,start,arrow,source_lines
def build(data):
    template=data['template']
    if template not in {'cohort','rct','pipeline'}:raise ValueError('Unknown design template')
    nodes=data['nodes']
    if not 2<=len(nodes)<=10:raise ValueError('Design needs 2–10 nodes')
    for n in nodes:
        if not n.get('source'):raise ValueError('Every design node needs a source')
        for v in n.get('numbers',[]):
            if not v.get('source'):raise ValueError('Unsourced design number')
    if template=='rct' and data.get('arms'):
        arms=data['arms']
        if len(arms)!=2 or any(not a.get('source') for a in arms):raise ValueError('RCT needs two sourced arms/sequences')
        # Recruitment/randomization above parallel conditions; analysis below.
        prep=nodes[:-1];end=nodes[-1]
        arm_blocks=[(lines(a['title'],475,27),lines(a.get('text',''),475,23)) for a in arms]
        arm_h=max(50+len(t)*37+len(d)*32 for t,d in arm_blocks)
        header=lines(data.get('title','随机试验设计'),1100,32);y=60+len(header)*43
        chunks=[]
        for n in prep:
            t=lines(n['title'],1020,27);d=lines(n.get('text',''),1020,23);hh=44+len(t)*37+len(d)*32
            chunks.extend([rect(55,y,1090,hh),multiline(78,y+35,t,27,'section'),multiline(78,y+35+len(t)*37,d,23)])
            y+=hh+35
        for i,(t,d) in enumerate(arm_blocks):
            x=55+i*580;chunks.extend([arrow(600,y-30,x+255,y-5),rect(x,y,510,arm_h),multiline(x+20,y+35,t,27,'section'),multiline(x+20,y+35+len(t)*37,d,23)])
        y+=arm_h+45
        for x in [310,890]:chunks.append(arrow(x,y-40,600,y-5))
        et=lines(end['title'],1020,27);ed=lines(end.get('text',''),1020,23);eh=44+len(et)*37+len(ed)*32
        chunks.extend([rect(55,y,1090,eh),multiline(78,y+35,et,27,'section'),multiline(78,y+35+len(et)*37,ed,23)])
        src=source_lines(data);h=y+eh+65+len(src)*26
        return '\n'.join([start(1200,h,data.get('title','随机试验设计')),multiline(50,45,header,32,'title'),*chunks,multiline(55,y+eh+40,src,19,'footer'),'</svg>'])
    w=1200;header=lines(data.get('title','研究设计'),1100,32);top=50+len(header)*43+20
    blocks=[]
    for n in nodes:
        t=lines(n['title'],1020,27);d=lines(n.get('text',''),1020,23);hh=44+len(t)*37+len(d)*32;blocks.append((t,d,hh))
    src=source_lines(data);h=top+sum(b[2]+35 for b in blocks)+40+len(src)*27
    out=[start(w,h,data.get('title','研究设计')),multiline(50,45,header,32,'title')];y=top
    for i,(t,d,hh) in enumerate(blocks):
        out.extend([rect(55,y,1090,hh),multiline(78,y+35,t,27,'section'),multiline(78,y+35+len(t)*37,d,23)])
        if i<len(blocks)-1:out.append(arrow(600,y+hh+4,600,y+hh+30,template=='cohort'))
        y+=hh+35
    out.extend([multiline(55,y+10,src,19,'footer'),'</svg>']);return '\n'.join(out)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(build(json.loads(a.input.read_text(encoding='utf-8'))),encoding='utf-8')
if __name__=='__main__':main()
