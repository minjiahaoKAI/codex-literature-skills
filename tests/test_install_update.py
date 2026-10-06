import sys,unittest,uuid,shutil,json,struct,subprocess
from pathlib import Path
from unittest.mock import patch
S=Path(__file__).resolve().parents[1]/'skills/life-science-literature-card/scripts';sys.path.insert(0,str(S))
import install_card_to_vault as installer
from _frontmatter import split,value,merge,stamp
from migrate_cards import migrate

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.base=S.parents[2]/'work/test-tmp'/uuid.uuid4().hex;self.base.mkdir(parents=True)
        self.v=self.base/'vault';(self.v/'.obsidian').mkdir(parents=True)
        self.source=self.base/'KEY';self.source.mkdir();(self.source/'paper.md').write_text('Full source')
        self.png=self.base/'cover.png';self.png.write_bytes(b'\x89PNG\r\n\x1a\n'+b'\x00\x00\x00\rIHDR'+struct.pack('>II',200,200))
        self.svg=self.base/'logic.svg';self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.note=self.base/'note.md';self.note.write_text('''---
note_type: literature-card
zotero_key: KEY
pdf_key: PDF
card_cover: "[[图片资源/literature_cards/cover.png]]"
card_logic_map: "[[图片资源/literature_cards/logic.svg]]"
card_summary: "Conclusion"
source_status: local_zotero_pdf_mineru_extract
mineru_mode: extract
cssclasses: [literature-note]
read_stage: reading
zotero_annotations: partial
custom_field: "Keep me"
---
%% generated:start %%
Original text ![[图片资源/literature_cards/cover.png|1000]]
%% generated:end %%
## My reading
User edits outside generated region
''',encoding='utf-8')
        self.args=installer.parser().parse_args(['--vault',str(self.v),'--note',str(self.note),'--graphical-abstract',str(self.png),'--logic-map',str(self.svg),'--mineru-directory',str(self.source)])
    def tearDown(self):
        self.assertTrue(self.base.resolve().is_relative_to((S.parents[2]/'work/test-tmp').resolve()));shutil.rmtree(self.base)
    def test_skip_and_update_preserve_reading_and_user_text(self):
        installer.run(self.args);dest=self.v/'文献笔记/note.md';before=dest.read_text(encoding='utf-8')
        self.args.skip_existing=True;self.assertEqual(installer.run(self.args)['status'],'skipped');self.args.skip_existing=False
        self.note.write_text(self.note.read_text(encoding='utf-8').replace('Original text','New evidence').replace('read_stage: reading','read_stage: initial_card'),encoding='utf-8')
        self.args.update=True;r=installer.run(self.args);after=dest.read_text(encoding='utf-8')
        self.assertEqual(r['status'],'updated');self.assertIn('New evidence',after);self.assertIn('User edits outside',after);self.assertIn('read_stage: reading',after);self.assertIn('custom_field: "Keep me"',after)
        self.assertTrue(Path(r['backup']).exists())
    def test_unprotected_manual_change_conflicts(self):
        installer.run(self.args);dest=self.v/'文献笔记/note.md';dest.write_text(dest.read_text(encoding='utf-8').replace('Original text','Hand-edited prose'),encoding='utf-8');self.args.update=True
        with self.assertRaises(ValueError):installer.run(self.args)
    def test_update_with_new_cover_filename_backs_up_old_cover(self):
        installer.run(self.args);old=(self.v/'图片资源/literature_cards/cover.png').read_bytes()
        new=self.base/'new_cover.png';new.write_bytes(self.png.read_bytes());self.args.graphical_abstract=new
        self.note.write_text(self.note.read_text(encoding='utf-8').replace('cover.png','new_cover.png'),encoding='utf-8');self.args.update=True
        result=installer.run(self.args);backup=Path(result['backup'])
        self.assertEqual((backup/'图片资源/literature_cards/cover.png').read_bytes(),old)
        self.assertTrue((backup/'文献笔记/note.md').exists())
    def test_replace_failure_rolls_back_note(self):
        installer.run(self.args);dest=self.v/'文献笔记/note.md';before=dest.read_bytes();self.args.update=True
        old_png=(self.v/'图片资源/literature_cards/cover.png').read_bytes();self.png.write_bytes(self.png.read_bytes()+b'updated')
        real=installer.os.replace
        def fail_note(src,dst):
            if Path(dst)==dest:raise OSError('simulated replace failure')
            return real(src,dst)
        with patch.object(installer.os,'replace',side_effect=fail_note):
            with self.assertRaises(OSError):installer.run(self.args)
        self.assertEqual(dest.read_bytes(),before)
        self.assertEqual((self.v/'图片资源/literature_cards/cover.png').read_bytes(),old_png)
    def test_metadata_migration_body_is_identical(self):
        old=self.note.read_text(encoding='utf-8');new,missing=migrate(old);self.assertTrue(missing);self.assertEqual(split(old)[1],split(new)[1]);self.assertEqual(value(split(new)[0],'ga_qc'),'unverified')
    def test_quoted_emphasis_migrates_but_real_yaml_references_are_refused(self):
        old=self.note.read_text(encoding='utf-8').replace('"Conclusion"','"*Lactobacillus crispatus* and literal <<: *alias"')
        new,missing=migrate(old)
        self.assertTrue(missing);self.assertEqual(split(new)[1],split(old)[1])
        self.assertEqual(split(new)[0]['card_summary'],split(old)[0]['card_summary'])
        for scalar in ['&anchor "value"','*alias','["literal", *alias]']:
            with self.assertRaises(ValueError):split(old.replace('custom_field: "Keep me"','custom_field: '+scalar))
    def test_no_cover_triage_installs_shared_assets_without_fabricating_cover(self):
        import hashlib
        tx=self.note.read_text(encoding='utf-8').replace('[[图片资源/literature_cards/cover.png]]','').replace('[[图片资源/literature_cards/logic.svg]]','').replace(' ![[图片资源/literature_cards/cover.png|1000]]','')
        tx=tx.replace('note_type: literature-card','note_type: literature-card\ncard_tier: triage\nga_attempts: 0\nga_qc: not_generated\nimage_mode: disabled')
        self.note.write_text(tx,encoding='utf-8');report=self.base/'numbers.json';report.write_text(json.dumps({'status':'pass','not_found':0,'card_sha256':hashlib.sha256(self.note.read_bytes()).hexdigest()}))
        self.args.number_report=report;self.args.number_source=self.source/'paper.md';self.args.graphical_abstract=None;self.args.logic_map=None
        self.args.dry_run=True;plan=installer.run(self.args);self.assertEqual(plan['status'],'ready');self.assertFalse((self.v/'图片资源').exists())
        self.args.dry_run=False;installer.run(self.args);fm,body=split((self.v/'文献笔记/note.md').read_text(encoding='utf-8'))
        self.assertEqual(value(fm,'card_cover'),'');self.assertEqual(value(fm,'ga_qc'),'not_generated');self.assertNotIn('literature_card_placeholders',body)
        from build_card_placeholders import TYPES
        self.assertEqual(len(list((self.v/'图片资源/literature_card_placeholders').glob('*.svg'))),len(TYPES))
    def test_path_escape_refused(self):
        self.args.notes_folder='../outside'
        with self.assertRaises(ValueError):installer.run(self.args)
    def test_cover_only_preserves_body_and_width_embed(self):
        old=stamp(self.note.read_text(encoding='utf-8'));new=old.replace('cover.png','new.png')
        merged=merge(old,new,True);self.assertIn('new.png|1000',merged);self.assertIn('User edits outside',merged)
    def test_batch_failure_does_not_prevent_later_install(self):
        manifest=self.base/'batch.json';manifest.write_text(json.dumps({'cards':[{'note':'missing.md'},{'note':self.note.name}]}),encoding='utf-8')
        cmd=[sys.executable,str(S/'install_card_to_vault.py'),'--vault',str(self.v),'--batch',str(manifest),'--graphical-abstract',str(self.png),'--logic-map',str(self.svg),'--mineru-directory',str(self.source)]
        p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');r=json.loads(p.stdout)
        self.assertEqual(p.returncode,1);self.assertEqual([x['status'] for x in r['results']],['failed','created'])
    def test_unknown_property_is_not_overwritten(self):
        old=stamp(self.note.read_text(encoding='utf-8'));new=old.replace('Keep me','New accidental value')
        self.assertIn('custom_field: "Keep me"',merge(old,new))
    def test_profile_fields_refresh_without_resetting_user_projects(self):
        old=self.note.read_text(encoding='utf-8').replace('custom_field:', 'projects: ["[[User project]]"]\nproject_relevance: "未评估"\nconnection_types: []\nverdict_reason: "Not assessed"\nverdict: "略读"\ncustom_field:')
        new=old.replace('"未评估"','"中相关"').replace('connection_types: []','connection_types: ["方法"]').replace('"Not assessed"','"A concrete method match"').replace('"[[User project]]"','"[[Proposed project]]"')
        fm,body=split(merge(stamp(old),new))
        self.assertEqual(value(fm,'project_relevance'),'中相关');self.assertEqual(value(fm,'connection_types'), '["方法"]')
        self.assertEqual(value(fm,'verdict_reason'),'A concrete method match');self.assertIn('User project',fm['projects']);self.assertIn('User edits outside',body)
    def test_legacy_card_can_receive_optional_profile_fields(self):
        old=stamp(self.note.read_text(encoding='utf-8'))
        new=old.replace('custom_field:', 'project_relevance: "中相关"\nconnection_types: ["叙事"]\nverdict_reason: "Evidence organization worth learning"\ncustom_field:')
        fm,_=split(merge(old,new));self.assertEqual(value(fm,'project_relevance'),'中相关')
        self.assertEqual(value(fm,'read_stage'),'reading');self.assertEqual(value(fm,'custom_field'),'Keep me')
if __name__=='__main__':unittest.main()
