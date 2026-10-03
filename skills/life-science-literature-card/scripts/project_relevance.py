"""Apply calibrated profile gates to reviewed evidence, never keyword similarity.

Each record describes one project. Nonempty evidence contains point, target,
source and limit. The caller must establish source truth and profile fit first.
Use only when the actual profile adopts the calibrated two-level policy.
"""

FIELDS = ('point', 'target', 'source', 'limit')


def supported(evidence):
    return isinstance(evidence, dict) and all(
        isinstance(evidence.get(k), str) and evidence[k].strip() for k in FIELDS
    ) and evidence.get('certain') is True


def assess_project(record):
    theme = supported(record.get('theme'))
    reusable = [kind for kind in ('method', 'narrative')
                if supported(record.get(kind))]
    direct = theme and supported(record.get('current_question'))
    near_term = bool(reusable) and supported(record.get('near_term_reuse'))
    # A record's uncertainty invalidates upgrades without inventing weak matches.
    certain = record.get('certain', True) is True
    strong = certain and theme and (direct or bool(reusable))
    relevance = '强相关' if strong else '中相关' if theme or reusable else '弱相关'
    verdict = '精读' if strong and (direct or near_term) else (
        '略读' if relevance in ('强相关', '中相关') else '存档')
    return {'project_relevance': relevance, 'verdict': verdict,
            'connection_types': (['主题'] if theme else []) +
                [{'method': '方法', 'narrative': '叙事'}[x] for x in reusable],
            'theme_established': theme, 'direct_question_established': direct,
            'near_term_reuse_established': near_term,
            'strong_gate_passed': strong}


def assess(records, profile_present=True):
    if not profile_present:
        return {'project_relevance': '未评估', 'verdict': '',
                'connection_types': [], 'projects': []}
    rows = [dict(assess_project(r), project=r.get('project', '')) for r in records]
    order = {'弱相关': 0, '中相关': 1, '强相关': 2}
    grade = max((r['project_relevance'] for r in rows),
                key=order.get, default='弱相关')
    verdict = '精读' if any(r['verdict'] == '精读' for r in rows) else (
        '略读' if grade in ('强相关', '中相关') else '存档')
    types = [t for t in ('主题', '方法', '叙事')
             if any(t in r['connection_types'] for r in rows)]
    return {'project_relevance': grade, 'verdict': verdict,
            'connection_types': types, 'projects': rows}
