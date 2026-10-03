import sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'skills/life-science-literature-card/scripts';sys.path.insert(0,str(S))
from verify_card_numbers import verify
import build_logic_map_svg as logic
import build_key_results as results

class NumbersAndSVGTests(unittest.TestCase):
    def test_spaced_mineru_math_and_attached_hr(self):
        src=r'Glucose $7 . 4$, range $5 0 . 9\%$ versus $4 3 . 3\%$, $p=0 . 0 3 6$. HR 0.84.'
        card='血糖7.4；范围50.9对43.3；p=0.036；HR0.84。DOI：10.1002/advs.76217。'
        r=verify(src,[('card','md',card)])
        self.assertEqual(r['not_found'],0)
        self.assertEqual(r['quantities'],5)
        self.assertEqual(verify('Values 5 0 9',[('card','md','效应50.9')])['status'],'fail')
    def test_spaced_math_derivation_still_checks_operands(self):
        src=r'Range $5 0 . 9\%$ versus $4 3 . 3\%$.'
        ledger={'claims':[{'id':'delta','value':7.6,'locator':'Fig 2E','excerpt':src,'derivation':{'operation':'subtract','operands':[50.9,43.3]}}]}
        self.assertEqual(verify(src,[('card','md','增加7.6个百分点')],ledger)['status'],'pass')
        ledger['claims'][0]['value']=9.6
        self.assertEqual(verify(src,[('card','md','增加9.6个百分点')],ledger)['status'],'fail')
    def test_thousands_ci_and_metadata_not_scientific(self):
        src='Sample n=89,309. HR 0.84, 95% CI 0.81-0.87.'
        card='---\nyear: 2026\ndoi: 10.1000/1234\n---\n样本89309，HR 0.84（95%CI 0.81–0.87）。〔Fig 4〕'
        r=verify(src,[('card','md',card)]);self.assertEqual(r['not_found'],0);self.assertIn('matched_normalized',r['counts'])
    def test_false_number_and_wrong_arithmetic_fail(self):
        src='Range time 50.9% versus 43.3%.'
        ledger={'claims':[{'id':'delta','value':7.6,'locator':'Results','excerpt':src,'derivation':{'operation':'subtract','operands':[50.9,43.3]}}]}
        self.assertEqual(verify(src,[('card','md','增加7.6个百分点')],ledger)['status'],'pass')
        ledger['claims'][0]['value']=9.6
        self.assertEqual(verify(src,[('card','md','增加9.6个百分点')],ledger)['status'],'fail')
        self.assertEqual(verify(src,[('card','md','HR 0.17')])['not_found'],1)
    def test_fake_operand_passage_cannot_authorize_derived_value(self):
        ledger={'claims':[{'id':'x','value':3,'locator':'Results','excerpt':'Values 5 and 2','derivation':{'operation':'subtract','operands':[5,2]}}]}
        self.assertEqual(verify('Values 8 and 1',[('card','md','效应3')],ledger)['status'],'fail')
    def test_long_map_wraps_and_grows_without_truncation(self):
        d={'steps':[{'title':'较长的中文研究问题以及 mixed English methodology '*4,'detail':'数据与结果需要保留原文的限定条件。'*12} for _ in range(6)]}
        root=ET.fromstring(logic.build(d));self.assertGreater(float(root.attrib['height']),1040)
        self.assertEqual(len(root.findall('.//{http://www.w3.org/2000/svg}text'))>60,True)
    def test_ratio_forest_rejects_invalid_ci(self):
        d={'mode':'forest','rows':[{'label':'A','estimate':.8,'lower':0,'upper':1,'source':['Fig 1']},{'label':'B','estimate':.9,'lower':.8,'upper':1,'source':['Fig 1']}]}
        with self.assertRaises(ValueError):results.build(d)
        d['rows'][0]['lower']=.6;ET.fromstring(results.build(d))
if __name__=='__main__':unittest.main()
