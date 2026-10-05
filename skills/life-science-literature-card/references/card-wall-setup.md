# Optional literature card wall setup

Read [card-wall-v2.md](card-wall-v2.md) for view/compatibility details. Resolve the
recipient's Vault and verify Bases is enabled. Install these reusable files:

- `assets/card-wall/Literature_Card_Wall.base` and `.md` in the chosen notes folder;
- `assets/card-wall/literature-card-wall.css` and `assets/literature-note.css` in
  `<vault>/.obsidian/snippets/`.

Compare existing destination files first; retain user changes or choose a new
versioned Base/entry name and update its embed. Never overwrite silently or copy
another user's `.obsidian` configuration. Obtain required filesystem permission.
Enable both snippets in Settings → Appearance and open the Base/entry note.

Check the four views at a normal desktop width: three or four columns, with
journal/year/verdict/summary under the covers. Sparse filters keep normal card
width; use real matching records rather than inventing cards to fill a row.
Check full and legacy
cards, image contain fit, light/dark themes and a narrow note pane. Images use `formula.display_cover`: an existing card_cover takes priority;
otherwise a study-type SVG is shown. Missing or unknown type uses other.svg.
Old cards need no migration.
If a card is absent, inspect note_type, links and indexing first.

Do not claim successful UI installation from filesystem checks alone. If no app
connection is possible, report that limitation and keep a ready staging package.

Copy all bundled `assets/card-wall/placeholders/*.svg` into
`图片资源/literature_card_placeholders/`. No-cover triage installation prepares
these shared files transactionally and skips identical existing copies. Conflicting
files require explicit update and backup. The Base maps the eight paper-type
filenames, falling back to other. These images say 类型占位 and contain no paper
findings; never write a placeholder into card_cover or mark it as generated GA.
Verify real covers take priority and missing/unknown legacy types still display.
