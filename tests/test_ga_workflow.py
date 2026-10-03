import importlib.util,sys,shutil,uuid,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'skills/life-science-literature-card/scripts'
sys.path.insert(0,str(S))
import ga_workflow as workflow
from validate_ga_briefs import qc_decision,HARD_CHECKS

class CoverBudgetTests(unittest.TestCase):
    def setUp(self):
        base=S.parents[2]/'work/test-tmp';base.mkdir(parents=True,exist_ok=True)
        self.tmp=base/uuid.uuid4().hex;self.tmp.mkdir();self.p=self.tmp/'prompt.md';self.p.write_text('prompt')
        self.im=self.tmp/'image.png';self.im.write_bytes(b'fixture')
        self.v={'labels':[{'id':'x','text':'Exact'}]}
        self.q={'transcription':[{'id':'x','text':'Exact'}],'hard_checks':dict.fromkeys(HARD_CHECKS,'pass'),'soft_observations':['large type']}
    def tearDown(self):
        self.assertTrue(self.tmp.resolve().is_relative_to((S.parents[2]/'work/test-tmp').resolve()))
        shutil.rmtree(self.tmp)
    def test_soft_deviation_passes_and_cannot_spend_retry(self):
        l=workflow.start('KEY','full');workflow.begin_attempt(l,self.p);workflow.review(l,self.im,self.v,self.q)
        self.assertEqual(l['attempts'][0]['qc']['ga_qc'],'passed_with_issues')
        with self.assertRaises(ValueError):workflow.begin_attempt(l,self.p)
        workflow.finish(l);self.assertGreaterEqual(l['total_elapsed_seconds'],0)
    def test_third_only_after_hard_failure_and_fourth_refused(self):
        l=workflow.start('KEY','full');bad={**self.q,'transcription':[{'id':'x','text':'Wrong'}]}
        for n in range(3):workflow.begin_attempt(l,self.p);workflow.review(l,self.im,self.v,bad)
        self.assertEqual(l['ga_attempts'],3)
        with self.assertRaises(ValueError):workflow.begin_attempt(l,self.p)
        with self.assertRaises(ValueError):workflow.finish(l)
    def test_extra_and_duplicate_visible_text_fail(self):
        q={**self.q,'unplanned_text':['Invented organ']};self.assertEqual(qc_decision(self.v,q)['ga_qc'],'failed')
        q={**self.q,'transcription':self.q['transcription']*2};self.assertEqual(qc_decision(self.v,q)['ga_qc'],'failed')
    def test_missing_science_check_is_not_a_pass(self):
        q={**self.q,'hard_checks':{'literal_text':'pass'}};self.assertEqual(qc_decision(self.v,q)['ga_qc'],'failed')
    def test_attempt_archives_prompt_before_retry_overwrites_it(self):
        l=workflow.start('KEY','full');workflow.begin_attempt(l,self.p)
        first=Path(l['attempts'][0]['prompt']);self.assertEqual(first.read_text(),'prompt')
        bad={**self.q,'transcription':[{'id':'x','text':'Wrong'}]};workflow.review(l,self.im,self.v,bad)
        self.p.write_text('corrective prompt');workflow.begin_attempt(l,self.p)
        self.assertEqual(first.read_text(),'prompt')
        self.assertNotEqual(l['attempts'][0]['prompt_sha256'],l['attempts'][1]['prompt_sha256'])
if __name__=='__main__':unittest.main()
