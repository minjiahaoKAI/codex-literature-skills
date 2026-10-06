"""Approved white/gray house style v2, shared by stdlib SVG helpers."""
from html import escape
VERSION='house-style-v2'
BACKGROUND='#FFFFFF'
PANEL='#FAFAFA'
PRIMARY='#6F99B5'
AUXILIARY='#7FA590'
ACCENT='#AE879F'
NULL='#8A9099'
TEXT='#454545'
SECONDARY='#747474'
FONT_FAMILY="'Microsoft YaHei','Noto Sans CJK SC','Segoe UI',sans-serif"
FONT_RATIO={'title':.05,'finding':.03,'section':.025,'method':.021,'body':.021,'footer':.021}
FONT_WEIGHT={'title':600,'finding':600,'section':500,'method':400,'body':400,'footer':400}
TITLE_MAX_WIDTH_RATIO=.75
PALETTE=[(PANEL,PRIMARY)]*6
def color(role='body',status='neutral'):
    if status in {'null','nonsignificant','unconfirmed','unsupported'}:return NULL
    if role=='finding' and status in {'changed','associated','supported'}:return ACCENT
    if role=='section':return PRIMARY
    if role in {'method','footer'}:return SECONDARY
    return TEXT
def text_attrs(size,role='body',status='neutral'):
    return f'font-family="{escape(FONT_FAMILY,quote=True)}" font-size="{size:g}" font-weight="{FONT_WEIGHT[role]}" fill="{color(role,status)}"'
def svg_text_attrs(height,role,status='neutral'):return text_attrs(height*FONT_RATIO[role],role,status)
