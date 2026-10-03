# Card wall v2

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

At native size inspect cover labels/science. At 400px thumbnail inspect only
structure. Below image show card_summary, verdict and study_type. CSS is scoped
to literature-note or the Literature_Card_Wall tab and supports light/dark and
responsive grids. Full-card cover height is capped to keep the verdict visible
on the first screen.

If a card is missing, check note_type, card_cover path, indexing and note folder
before changing the Base. Filesystem checks and browser simulations do not prove
Obsidian UI acceptance; record the app render separately.

Official references: [Bases syntax](https://obsidian.md/help/bases/syntax),
[functions](https://obsidian.md/help/bases/functions),
[Cards](https://obsidian.md/help/bases/views/cards).
