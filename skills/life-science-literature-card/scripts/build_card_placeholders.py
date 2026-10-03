#!/usr/bin/env python3
"""Shared study-type SVGs; these are gallery placeholders, never paper results."""
from pathlib import Path
from html import escape
import argparse
import _style as st

TYPES={
    'observational-cohort':('观察性队列','<circle cx="125" cy="115" r="15"/><circle cx="180" cy="115" r="15"/><circle cx="235" cy="115" r="15"/><path d="M110 155v35m55-35v35m55-35v35M110 210h140m-12-10 12 10-12 10"/>'),
    'rct':('随机试验','<path d="M180 90v45m0 0-60 40m60-40 60 40M120 175v40m120-40v40"/><rect x="100" y="215" width="40" height="25" rx="5"/><rect x="220" y="215" width="40" height="25" rx="5"/>'),
    'prediction-model':('预测模型','<rect x="110" y="95" width="45" height="35" rx="5"/><rect x="110" y="155" width="45" height="35" rx="5"/><path d="M155 112h30v60h25m-55 0h55"/><rect x="210" y="150" width="50" height="45" rx="5"/>'),
    'genetic-mr':('遗传与 MR','<path d="M135 85c100 35-10 90 90 125M225 85c-100 35 10 90-90 125M155 100h50m-70 40h90m-70 40h50"/>'),
    'basic-mechanism':('机制研究','<circle cx="180" cy="150" r="65"/><circle cx="180" cy="150" r="22"/><path d="M115 150h25m80 0h25M180 85v25m0 80v25"/>'),
    'neuroimaging':('神经影像','<rect x="110" y="95" width="140" height="110" rx="8"/><circle cx="180" cy="150" r="32"/><path d="M160 210v25m40-25v25M145 235h70"/>'),
    'systematic-review-meta':('系统综述与荟萃','<rect x="115" y="95" width="85" height="110" rx="5"/><path d="M140 120h35m-35 25h35m-35 25h35"/><rect x="205" y="130" width="45" height="75" rx="5"/>'),
    'other':('其他／未分类','<rect x="130" y="85" width="100" height="140" rx="6"/><path d="M150 120h60m-60 30h60m-60 30h40"/>'),
}
ASSETS=Path(__file__).resolve().parents[1]/'assets/card-wall/placeholders'
VAULT_FOLDER='图片资源/literature_card_placeholders'

def svg(label,icon):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400" viewBox="0 0 640 400" role="img" aria-label="{escape(label)} 类型占位">
<rect width="640" height="400" fill="{st.BACKGROUND}"/>
<rect x="28" y="28" width="584" height="344" rx="14" fill="{st.PANEL}"/>
<g fill="none" stroke="{st.PRIMARY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
<text x="320" y="165" {st.text_attrs(32,'title')}>{escape(label)}</text>
<text x="320" y="205" {st.text_attrs(22,'body')}>类型占位</text>
<text x="320" y="238" {st.text_attrs(18,'body')}>专属封面在完整卡中生成</text>
</svg>'''

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ASSETS);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    for key,(label,icon) in TYPES.items():(a.output/(key+'.svg')).write_text(svg(label,icon),encoding='utf-8')
if __name__=='__main__':main()
