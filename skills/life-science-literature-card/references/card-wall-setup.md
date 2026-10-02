# Optional Obsidian literature card wall

Use this when the user asks for a gallery of literature cards. The three files in `../assets/card-wall/` are copied from a working Obsidian vault and contain no vault-specific absolute paths. This is an Obsidian **Bases** Cards view; Notebook Navigator's file cards are a separate sidebar display.

## Install in the current user's vault

1. Resolve the user's vault path and confirm `.obsidian/` exists. Check that the **Bases** core plugin is enabled in Obsidian. Do not copy the source user's vault settings or other plugins.
2. Locate the user's literature notes folder. The companion card skill defaults to `文献笔记`; use the actual folder if they chose another one.
3. Copy `Literature_Card_Wall.base` and `Literature_Card_Wall.md` into that folder, and `literature-card-wall.css` into `<vault>/.obsidian/snippets/`. The `.md` entrypoint embeds `![[Literature_Card_Wall.base#Literature Cards]]`; keep those names and the base view name aligned. The CSS targets a tab named `Literature_Card_Wall`.
4. Before writing, check every destination. If a file already exists, compare contents and preserve the user's version; show the difference or choose new names and update the embed and CSS selectors together. Do not silently overwrite an existing base, note, or snippet. Request any filesystem approval needed for this vault before copying.
5. In Obsidian, open **Settings → Appearance → CSS snippets**, refresh the snippet list if needed, and enable `literature-card-wall`. This CSS only changes spacing and labels; the `.base` view works without it.
6. Open `Literature_Card_Wall.base` or the `Literature_Card_Wall.md` entrypoint. Confirm a known card appears with its cover and summary and opens its full note when clicked. If the wall is empty, check the card frontmatter and source indexing before changing the base.

## Card contract

The base filters notes with `note_type: literature-card`, sorts by `file.mtime` newest first, uses `card_cover` for the image, and displays `card_summary` plus selected metadata. Each card needs a valid local image link, for example:

```yaml
---
note_type: literature-card
card_cover: "[[图片资源/literature_cards/example_graphical_abstract.png]]"
card_summary: "一句简短的中文摘要。"
---
```

The image path must match the actual vault-relative asset path. Cards created by the companion skill already use these fields by default. The base and CSS have no personal data; do not copy the original user's papers, assets, notes, or `.obsidian/appearance.json`.
