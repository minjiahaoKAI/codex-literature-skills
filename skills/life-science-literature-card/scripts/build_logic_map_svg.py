#!/usr/bin/env python3
"""Render a dynamically wrapped 4–6-step reading map, not a causal diagram."""
import argparse,json
from pathlib import Path
from _svg import lines,text,multiline,rect,start,arrow,source_lines,wrap,units as display_units
def build(data):
    steps=data.get('steps',[])
    if not 4<=len(steps)<=6:raise ValueError('steps must contain 4 to 6 items')
    w=1440;colw=420;gap=45;rows=[]
    for step in steps:
        t=lines(step['title'],colw-44,27);d=lines(step.get('detail',''),colw-44,22)
        rows.append((t,d,48+len(t)*37+len(d)*30))
    heights=[max(x[2] for x in rows[:3]),max(x[2] for x in rows[3:])]
    header=lines(data.get('title','文章逻辑地图'),w-100,30)
    top=45+len(header)*41+35;y2=top+heights[0]+70
    concl=data.get('conclusion',{});ct=lines(concl.get('title','结论与边界'),w-160,26);cd=lines(concl.get('detail',''),w-160,22)
    cy=y2+heights[1]+65;ch=44+len(ct)*36+len(cd)*30;src=source_lines(data)
    h=cy+ch+65+len(src)*26
    out=[start(w,h,data.get('title','文章逻辑地图')),multiline(50,45,header,30,'title'),text(50,top-18,'阅读顺序；非因果路径',19,'footer')]
    pos=[]
    for i,(t,d,nh) in enumerate(rows):
        row=i//3;j=i%3;col=j if row==0 else 2-j;x=45+col*(colw+gap);y=top if row==0 else y2
        pos.append((x,y,heights[row]));out.append(rect(x,y,colw,heights[row]));out.append(multiline(x+22,y+40,t,27,'section'));out.append(multiline(x+22,y+40+len(t)*37,d,22))
    for i in range(len(pos)-1):
        x,y,hh=pos[i];xx,yy,h2=pos[i+1]
        if y==yy:
            direction=1 if xx>x else -1;out.append(arrow(x+(colw if direction>0 else 0)+8*direction,y+hh/2,xx+(colw if direction<0 else 0)-8*direction,y+hh/2))
        else:out.append(arrow(x+colw/2,y+hh+8,xx+colw/2,yy-8))
    out+=[rect(50,cy,w-100,ch),multiline(75,cy+35,ct,26,'section'),multiline(75,cy+35+len(ct)*36,cd,22),multiline(50,cy+ch+40,src,19,'footer'),'</svg>']
    return '\n'.join(out)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(build(json.loads(a.input.read_text(encoding='utf-8'))),encoding='utf-8')
if __name__=='__main__':main()
