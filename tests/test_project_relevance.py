import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'skills/life-science-literature-card/scripts'))
from project_relevance import assess, assess_project


def evidence(**changes):
    return dict(point='Concrete operation', target='Named project task',
                source='Methods section', limit='Known transfer limit',
                certain=True, **changes)


class RelevanceTests(unittest.TestCase):
    def test_method_and_narrative_without_theme_cannot_upgrade(self):
        r = assess_project(dict(method=evidence(), narrative=evidence(),
                                current_question=evidence(), near_term_reuse=evidence()))
        self.assertEqual((r['project_relevance'], r['verdict']), ('中相关', '略读'))
        self.assertFalse(r['direct_question_established'])

    def test_strong_does_not_automatically_mean_close_reading(self):
        r = assess_project(dict(theme=evidence(), method=evidence()))
        self.assertEqual((r['project_relevance'], r['verdict']), ('强相关', '略读'))

    def test_direct_current_question_or_supported_near_term_can_qualify(self):
        for extra in [dict(current_question=evidence()),
                      dict(method=evidence(), near_term_reuse=evidence())]:
            self.assertEqual(assess_project(dict(theme=evidence(), **extra))['verdict'], '精读')

    def test_generic_praise_missing_target_does_not_qualify(self):
        r = assess_project(dict(method={'point': 'Rigorous methods', 'certain': True},
                                narrative={'point': 'Clear story', 'certain': True}))
        self.assertEqual((r['project_relevance'], r['verdict']), ('弱相关', '存档'))

    def test_uncertain_evidence_does_not_upgrade(self):
        m = evidence();m['certain'] = False
        r = assess_project(dict(theme=evidence(), method=m, near_term_reuse=evidence()))
        self.assertEqual((r['project_relevance'], r['verdict']), ('中相关', '略读'))
        self.assertEqual(assess_project(dict(theme=evidence(), method=evidence(),
                                            current_question=evidence(), certain=False))['verdict'], '略读')

    def test_matches_on_different_projects_do_not_combine_into_strong(self):
        r = assess([dict(project='A', theme=evidence()),
                    dict(project='B', method=evidence(), narrative=evidence())])
        self.assertEqual((r['project_relevance'], r['verdict']), ('中相关', '略读'))

    def test_missing_profile_is_unassessed_and_batch_has_no_quota(self):
        self.assertEqual(assess([], False)['project_relevance'], '未评估')
        for _ in range(6):
            self.assertEqual(assess([dict(theme=evidence(), current_question=evidence())])['verdict'], '精读')


if __name__ == '__main__':
    unittest.main()
