# Card wall v2.1

Install the bundled Base/entry note and both CSS snippets through an authorized
copy, comparing existing files first. Do not copy a Vault's other settings.
Enable Bases and snippets in Obsidian. The companion entry embeds the “全部” view;
update an old `#Literature Cards` embed when choosing to replace that entry.

Four views: 全部 sorts by date_added descending, falling back to file.ctime for
legacy cards; 待精读 filters 精读 and unfinished read_stage; 按课题 groups by the
project combination (no promise of simultaneous membership in multiple groups);
本周新增 means Monday through now in Obsidian's local timezone, not rolling seven
days. Legacy verdict/type display 未评估/未分类. No migration required. Backups
are excluded. Card imageFit is contain and target H/W ratio is 0.625 for 16:10
covers; verify actual native rendered dimensions in the acceptance Vault.

Each native Cards view uses `cardSize: 260`, targeting three or four columns at
normal desktop widths. Sparse views retain that size instead of stretching a
single cover. Grouped views may have fewer items per group. Below the cover show
only journal, year, verdict and card_summary (at most two lines). Other properties
remain available through the view's property settings; CSS does not hide them.
At native size inspect cover labels/science; at thumbnail size inspect only
structure. CSS is scoped
to literature-note or the Literature_Card_Wall tab and supports light/dark and
responsive grids. Full-card cover height is capped to keep the verdict visible
on the first screen.

For empty `date_added`, dry-run `scripts/fill_card_dates.py` against the selected
Vault and a read-only Zotero database. Prefer Zotero's added timestamp; otherwise
use the original note creation date. When checking a copied Vault, supply original
creation dates with `--fallback-file-dates`. Preserve existing dates. Apply only
within authorized scope; the helper backs up each changed note.

If a card is missing, check note_type, card_cover path, indexing and note folder
before changing the Base. Filesystem checks and browser simulations do not prove
Obsidian UI acceptance; record the app render separately.

Official references: [Bases syntax](https://obsidian.md/help/bases/syntax),
[functions](https://obsidian.md/help/bases/functions),
[Cards](https://obsidian.md/help/bases/views/cards).

Copy all bundled `assets/card-wall/placeholders/*.svg` into
`图片资源/literature_card_placeholders/`. No-cover triage installation prepares
these shared files transactionally and skips identical existing copies. Conflicting
files require explicit update and backup. The Base maps the eight paper-type
filenames, falling back to other. These images say 类型占位 and contain no paper
findings; never write a placeholder into card_cover or mark it as generated GA.
Verify real covers take priority and missing/unknown legacy types still display.
