import sys,sqlite3,tempfile,unittest
from contextlib import closing
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'skills/life-science-literature-card/scripts';sys.path.insert(0,str(S))
from fill_card_dates import plan

class CardDateTests(unittest.TestCase):
    def test_only_empty_dates_filled_readonly_zotero_then_original_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            v=Path(tmp);(v/'文献笔记').mkdir();db=v/'zotero.sqlite'
            with closing(sqlite3.connect(db)) as conn:
                conn.execute('CREATE TABLE items(key TEXT,dateAdded TEXT)')
                conn.execute("INSERT INTO items VALUES('A','2025-01-15 00:00:00')")
                conn.commit()
            for name,key,added in [('first','A',''),('kept','A','2020-01-01'),('fallback','B','')]:
                (v/'文献笔记'/f'{name}.md').write_text(f'---\nnote_type: literature-card\nzotero_key: {key}\ndate_added: "{added}"\n---\nReader text.\n',encoding='utf-8')
            before={p.name:p.read_bytes() for p in (v/'文献笔记').glob('*.md')};db_before=db.read_bytes()
            rows=plan(v,db,{'文献笔记/fallback.md':'2019-10-01'});byname={Path(r['path']).stem:r for r in rows}
            self.assertEqual(byname['first']['source'],'zotero.items.dateAdded')
            self.assertEqual(byname['kept']['date_added'],'2020-01-01')
            self.assertEqual(byname['fallback']['date_added'],'2019-10-01')
            self.assertEqual(before,{p.name:p.read_bytes() for p in (v/'文献笔记').glob('*.md')})
            self.assertEqual(db_before,db.read_bytes())
    def test_invalid_date_stops_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            v=Path(tmp);(v/'文献笔记').mkdir();p=v/'文献笔记/a.md'
            p.write_text('---\nnote_type: literature-card\ndate_added: "bad-date"\n---\nBody',encoding='utf-8');before=p.read_bytes()
            with self.assertRaises(ValueError):plan(v)
            self.assertEqual(p.read_bytes(),before)
if __name__=='__main__':unittest.main()
