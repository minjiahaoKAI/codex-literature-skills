"""Conservative multilingual wrapping and unclipped SVG primitives."""
import re,unicodedata
from html import escape
import _style as s
def units(c):return 2 if unicodedata.east_asian_width(c) in {'W','F','A'} else 1
def wrap(text,width=40):
    if width<2:raise ValueError('Wrap width too small')
    result=[]
    for p in str(text).splitlines() or ['']:
        p=re.sub(r'\s+',' ',p).strip()
        while sum(units(c) for c in p)>width:
            n=0;used=0;space=-1
            for i,c in enumerate(p):
                if used+units(c)>width:break
                used+=units(c);n=i+1
                if c==' ':space=i
            if space>0:n=space
            result.append(p[:max(1,n)].strip());p=p[max(1,n):].strip()
        result.append(p)
    return result
def lines(text,width_px,size):return wrap(text,max(2,int(width_px/(size*.55))))
def text(x,y,value,size=24,role='body',status='neutral',anchor='start'):
    return f'<text x="{x:g}" y="{y:g}" {s.text_attrs(size,role,status)} text-anchor="{anchor}">{escape(str(value))}</text>'
def multiline(x,y,values,size=24,role='body',status='neutral',anchor='start'):
    return '\n'.join(text(x,y+i*size*1.35,v,size,role,status,anchor) for i,v in enumerate(values))
def rect(x,y,w,h,fill=None,stroke=None):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="12" fill="{fill or s.PANEL}"'+(f' stroke="{stroke}" stroke-width="1.5"' if stroke else '')+'/>'
def start(w,h,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{escape(title,quote=True)}">'+rect(0,0,w,h,s.BACKGROUND)
def arrow(x1,y1,x2,y2,dashed=False):
    return f'<path d="M{x1:g},{y1:g} L{x2:g},{y2:g}" fill="none" stroke="{s.PRIMARY}" stroke-width="2"'+(' stroke-dasharray="5 5"' if dashed else '')+'/>'
def source_lines(data):
    refs=[]
    def walk(x):
        if isinstance(x,dict):
            if x.get('source'):
                v=x['source'];refs.extend(v if isinstance(v,list) else [str(v)])
            for k,v in x.items():
                if k!='source':walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(data)
    return lines('出处：'+'；'.join(dict.fromkeys(refs)),1120,19)
