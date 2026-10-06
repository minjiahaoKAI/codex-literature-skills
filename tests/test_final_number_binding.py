"""Regression: passing input reports must not authorize unverified merged notes."""
import hashlib,json,subprocess,sys,unittest,uuid,shutil
from pathlib import Path
from unittest.mock import patch

S=Path(__file__).resolve().parents[1]/'skills/life-science-literature-card/scripts'
sys.path.insert(0,str(S))
import install_card_to_vault as installer

class FinalNumberBindingTests(unittest.TestCase):
    def setUp(self):
        self.base=S.parents[2]/'work/test-tmp'/uuid.uuid4().hex
        self.v=self.base/'vault';(self.v/'.obsidian').mkdir(parents=True)
        self.source=self.base/'source.md';self.source.write_text('HR 0.84. Range 50.9% versus 43.3%.',encoding='utf-8')
        self.note=self.base/'card.md'
        self.note.write_text('''---
note_type: literature-card
card_tier: triage
zotero_key: KEY
pdf_key: PDF
card_cover: ""
card_logic_map: ""
card_summary: "Conclusion"
source_status: abstract_only
mineru_mode: none
cssclasses: [literature-note]
ga_qc: not_generated
read_stage: reading
---
%% generated:start %%
结果 HR 0.84。
%% generated:end %%
## My reading
Protected reading notes.
''',encoding='utf-8')
        self.report=self.base/'numbers.json'
        self.args=installer.parser().parse_args(['--vault',str(self.v),'--note',str(self.note),'--number-report',str(self.report)])
        self.generate_report()

    def tearDown(self):
        self.assertTrue(self.base.resolve().is_relative_to((S.parents[2]/'work/test-tmp').resolve()))
        shutil.rmtree(self.base)

    def generate_report(self,ledger=None):
        cmd=[sys.executable,'-B',str(S/'verify_card_numbers.py'),'--source',str(self.source),'--card',str(self.note),'--output',str(self.report)]
        if ledger:cmd+=['--ledger',str(ledger)]
        result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def destination(self):return self.v/'文献笔记/card.md'

    def add_protected_text(self,text):
        dest=self.destination();dest.write_text(dest.read_text(encoding='utf-8')+'\n'+text,encoding='utf-8')
        self.args.update=True

    def snapshot(self):return installer.tree_hash(self.v)

    def test_unmatched_retained_number_blocks_dry_run_and_write_without_mutation(self):
        installer.run(self.args);self.add_protected_text('Retained effect 99.9.')
        before=self.snapshot()
        for dry_run in [True,False]:
            with self.subTest(dry_run=dry_run):
                self.args.dry_run=dry_run
                with self.assertRaisesRegex(ValueError,'Final merged note failed.*1 unmatched'):
                    installer.run(self.args)
                self.assertEqual(self.snapshot(),before)

    def test_supported_retained_number_checked_and_written_hash_matches(self):
        first=installer.run(self.args)
        self.assertEqual(first['final_number_verification']['card_sha256'],installer.sha(self.destination()))
        self.add_protected_text('Retained range 50.9%.')
        self.note.write_text(self.note.read_text(encoding='utf-8').replace('结果 HR','更新结果 HR').replace('read_stage: reading','read_stage: initial_card'),encoding='utf-8')
        self.generate_report();self.args.dry_run=True
        before=self.snapshot();plan=installer.run(self.args);self.assertEqual(self.snapshot(),before)
        self.assertEqual(plan['final_number_verification']['quantities'],2)
        self.args.dry_run=False;result=installer.run(self.args)
        self.assertEqual(result['final_number_verification'],plan['final_number_verification'])
        self.assertEqual(result['final_number_verification']['card_sha256'],installer.sha(self.destination()))
        final=self.destination().read_bytes();self.assertNotIn(b'\r\n',final)
        self.assertIn('Retained range 50.9%',final.decode('utf-8'))
        self.assertIn('read_stage: reading',final.decode('utf-8'))

    def test_source_backed_derivation_survives_merge_recheck(self):
        ledger=self.base/'ledger.json'
        ledger.write_text(json.dumps({'claims':[{'id':'delta','value':7.6,'locator':'Results','excerpt':'Range 50.9% versus 43.3%.','derivation':{'operation':'subtract','operands':[50.9,43.3]}}]}),encoding='utf-8')
        self.generate_report(ledger)
        report=json.loads(self.report.read_text(encoding='utf-8'))
        self.assertEqual(report['source_file'],str(self.source.resolve()))
        self.assertEqual(report['ledger_file'],str(ledger.resolve()))
        installer.run(self.args);self.add_protected_text('增加7.6个百分点。')
        result=installer.run(self.args)
        self.assertEqual(result['final_number_verification']['counts']['derived_verified'],1)
        self.assertEqual(result['final_number_verification']['card_sha256'],installer.sha(self.destination()))

    def test_invalid_derivation_rejected_before_writes(self):
        ledger=self.base/'ledger.json'
        ledger.write_text(json.dumps({'claims':[{'id':'delta','value':9.6,'locator':'Results','excerpt':'Range 50.9% versus 43.3%.','derivation':{'operation':'subtract','operands':[50.9,43.3]}}]}),encoding='utf-8')
        self.args.number_ledger=ledger;before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'1 derivation errors'):installer.run(self.args)
        self.assertEqual(self.snapshot(),before)

    def test_legacy_report_requires_explicit_source_and_then_works(self):
        report=json.loads(self.report.read_text(encoding='utf-8'));report.pop('source_file');report.pop('ledger_file')
        self.report.write_text(json.dumps(report),encoding='utf-8');before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'--number-source'):installer.run(self.args)
        self.assertEqual(self.snapshot(),before)
        self.args.number_source=self.source
        self.assertEqual(installer.run(self.args)['status'],'created')

    def test_stale_incoming_report_still_rejected(self):
        self.note.write_text(self.note.read_text(encoding='utf-8')+'Changed text',encoding='utf-8')
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'stale'):installer.run(self.args)
        self.assertEqual(self.snapshot(),before)

    def test_cover_only_verifies_retained_body_instead_of_incoming_body(self):
        # Legacy covered card upgraded through cover-only retains its old body.
        from _frontmatter import stamp
        import struct
        image=self.base/'cover.png'
        image.write_bytes(b'\x89PNG\r\n\x1a\n'+b'\x00\x00\x00\rIHDR'+struct.pack('>II',200,200))
        old=self.note.read_text(encoding='utf-8').replace('card_tier: triage','card_tier: full').replace('card_cover: ""','card_cover: "[[图片资源/literature_cards/cover.png]]"')
        dest=self.destination();dest.parent.mkdir(parents=True);dest.write_text(stamp(old)+'\nRetained effect 99.9.',encoding='utf-8')
        self.note.write_text(old,encoding='utf-8');self.generate_report()
        self.args.update=True;self.args.cover_only=True;self.args.graphical_abstract=image
        self.args.qc=self.base/'qc.json';self.args.qc.write_text(json.dumps({'image_sha256':installer.sha(image)}),encoding='utf-8')
        self.args.visual_brief=self.base/'visual.json';self.args.visual_brief.write_text('{}',encoding='utf-8')
        before=self.snapshot()
        with patch.object(installer,'qc_decision',return_value={'ga_qc':'passed'}):
            with self.assertRaisesRegex(ValueError,'Final merged note failed.*1 unmatched'):installer.run(self.args)
        self.assertEqual(self.snapshot(),before)

if __name__=='__main__':unittest.main()
