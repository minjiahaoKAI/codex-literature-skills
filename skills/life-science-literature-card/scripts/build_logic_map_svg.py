#!/usr/bin/env python3
"""Render a compact two-row snake article-logic map from a small JSON payload."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from html import escape
from pathlib import Path


PALETTE = [
    ("#E6F6FB", "#56B8CF"),
    ("#EAF2FF", "#82A9F0"),
    ("#F2ECFF", "#AC8BE6"),
    ("#FFF2E8", "#F2AB61"),
    ("#FFF8DF", "#D9B851"),
    ("#EAF8EF", "#72BF91"),
]


def display_units(character: str) -> int:
    """Approximate rendered width: CJK/full-width glyphs use two Latin units."""
    return 2 if unicodedata.east_asian_width(character) in {"W", "F", "A"} else 1


def wrap(text: str, width: int) -> list[str]:
    """Wrap mixed CJK/Latin text by display width, preferring whitespace breaks."""
    paragraphs = str(text).splitlines() or [""]
    output: list[str] = []
    for paragraph in paragraphs:
        remaining = re.sub(r"\s+", " ", paragraph).strip()
        if not remaining:
            output.append("")
            continue
        while sum(display_units(char) for char in remaining) > width:
            used = 0
            cutoff = 0
            last_space = -1
            for index, character in enumerate(remaining):
                next_used = used + display_units(character)
                if next_used > width:
                    break
                used = next_used
                cutoff = index + 1
                if character.isspace():
                    last_space = index
            if last_space > 0:
                cutoff = last_space
            if cutoff == 0:
                cutoff = 1
            output.append(remaining[:cutoff].strip())
            remaining = remaining[cutoff:].strip()
        output.append(remaining)
    return output or [""]


def line(x1: int, y1: int, x2: int, y2: int, marker: bool = True) -> str:
    arrow = ' marker-end="url(#arrow)"' if marker else ""
    return f'<path d="M {x1} {y1} L {x2} {y2}" class="edge"{arrow}/>'


def card(x: int, y: int, fill: str, stroke: str, number: int | str, title: str, detail: str) -> str:
    title_lines = wrap(title, 22)
    detail_lines = wrap(detail, 26)
    if len(title_lines) > 2:
        raise ValueError(f"title is too long for a card: {title!r}")
    if len(detail_lines) > 3:
        raise ValueError(f"detail is too long for a card: {detail!r}")
    title_y = y + 64 - (len(title_lines) - 1) * 15
    detail_y = y + 142 - (len(detail_lines) - 1) * 13
    out = [f'<rect x="{x}" y="{y}" width="400" height="190" rx="28" fill="{fill}" stroke="{stroke}" stroke-width="3" class="node"/>']
    prefix = f"{number:02d}��" if isinstance(number, int) else ""
    for idx, value in enumerate(title_lines):
        line_prefix = prefix if idx == 0 else ""
        out.append(f'<text x="{x + 200}" y="{title_y + idx * 30}" class="title">{line_prefix}{escape(value)}</text>')
    for idx, value in enumerate(detail_lines):
        out.append(f'<text x="{x + 200}" y="{detail_y + idx * 27}" class="detail">{escape(value)}</text>')
    return "\n".join(out)


def build(data: dict) -> str:
    steps = data.get("steps", [])
    if not 4 <= len(steps) <= 6:
        raise ValueError("steps must contain 4 to 6 items")
    conclusion = data.get("conclusion", {})
    positions = [(80, 150), (650, 150), (1220, 150), (1220, 460), (650, 460), (80, 460)]
    nodes = []
    for idx, step in enumerate(steps):
        fill, stroke = PALETTE[idx]
        nodes.append(card(*positions[idx], fill, stroke, idx + 1, step["title"], step["detail"]))
    edges = []
    for idx in range(len(steps) - 1):
        x1, y1 = positions[idx]
        x2, y2 = positions[idx + 1]
        if idx == 2:
            edges.append(line(x1 + 200, y1 + 190, x2 + 200, y2 - 22))
        elif idx == 3:
            edges.append(line(x1 - 22, y1 + 95, x2 + 422, y2 + 95))
        else:
            direction = 1 if x2 > x1 else -1
            edges.append(line(x1 + (400 if direction > 0 else 0) + 22 * direction, y1 + 95, x2 - 22 * direction, y2 + 95))
    last_x, last_y = positions[len(steps) - 1]
    conclusion_fill, conclusion_stroke = "#E0F8F4", "#4ABFB6"
    conclusion_node = card(650, 770, conclusion_fill, conclusion_stroke, "", conclusion.get("title", "���Ľ���"), conclusion.get("detail", ""))
    edges.append(f'<path d="M {last_x + 200} {last_y + 190} C {last_x + 200} 720, 850 720, 850 748" class="edge" marker-end="url(#arrow)"/>')
    title = escape(data.get("title", "ARTICLE LOGIC MAP"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1040" viewBox="0 0 1800 1040" role="img" aria-label="{title}">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#536A88"/></marker>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#5A6D88" flood-opacity="0.16"/></filter>
  <style>.edge{{fill:none;stroke:#536A88;stroke-width:5;stroke-linecap:round}}.node{{filter:url(#shadow)}}.title{{font:700 34px 'Segoe UI','Microsoft YaHei',sans-serif;fill:#1B3858;text-anchor:middle}}.detail{{font:400 27px 'Segoe UI','Microsoft YaHei',sans-serif;fill:#3F5874;text-anchor:middle}}.header{{font:700 30px 'Segoe UI','Microsoft YaHei',sans-serif;letter-spacing:3px;fill:#73829A}}</style>
</defs>
<rect width="1800" height="1040" rx="36" fill="#FBFCFE" stroke="#DCE4ED" stroke-width="2"/>
<text x="80" y="88" class="header">ARTICLE LOGIC MAP �� �����Ķ�·��</text>
{''.join(edges)}
{''.join(nodes)}
{conclusion_node}
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build(data), encoding="utf-8")


if __name__ == "__main__":
    main()
