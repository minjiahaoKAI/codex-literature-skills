---
name: life-science-literature-card
description: Create Chinese-first Obsidian literature cards from a Zotero item, DOI, title, citation, or local PDF, with source-checked graphical abstracts and logic maps. Use for initial screening cards, not for an ongoing deep-reading session.
---

# Life Science Literature Card

Create an `initial_card` that helps the reader decide whether to study the paper closely. Read `references/initial-card-template.md` before drafting. Treat the Zotero library, PDF, Obsidian vault, MinerU CLI, and any token as belonging to the current user; never assume paths or credentials from the skill author's computer.

## Setup and source resolution

1. Resolve the user's Obsidian vault from `OBSIDIAN_VAULT_PATH` or ask for its absolute path. Confirm that the folder exists and contains `.obsidian`. Use `文献笔记`, `图片资源/literature_cards`, and `sources/mineru` inside that vault by default; the user may choose different relative folders.
2. Resolve the paper in the user's Zotero library and locate its local PDF. Prefer an available Zotero integration or local API. If the live SQLite database is locked, use a verified read-only snapshot rather than modifying it. Do not produce a formal card from web content alone without the user's approval.
3. Resolve `mineru-open-api` from the system PATH or `MINERU_CLI` if set. Verify with `mineru-open-api version`. The precision `extract` command needs the current user's token, configured with `mineru-open-api auth` or `MINERU_TOKEN`. Never request that the user paste a token into chat, a repository, a command argument, or a generated note.
4. If a local PDF will be sent to MinerU's online service, explain that upload and obtain approval before the first upload. If writing to the vault needs filesystem approval, request it before the installation step. Stage all files in a writable workspace first.

## Extraction

Use the official MinerU Open API CLI's precision command as the default:

```text
mineru-open-api extract <local-pdf> -o <staged-mineru-directory> --format md --timeout 900
```

Do not use verbose mode, which may expose request details. A successful CLI exit is insufficient: require readable Markdown and preserve its relative `images/` files. Record `source_status: local_zotero_pdf_mineru_extract` and `mineru_mode: extract`. If authentication, quota, limits, timeout, or output validation fails, report the actual reason. Use `flash-extract` only after the user agrees to that fallback, and then record `local_zotero_pdf_mineru_flash` and `mineru_mode: flash-extract`. Before retrying an upload after a timeout, inspect any partial output.

## Card and visuals

Read enough of the extracted paper, captions, methods, and discussion to support each claim. The card must distinguish association from causation and exploratory from confirmatory findings. Use the reference template's frontmatter and core sections, adapting them only for a genuinely different paper type. The `note_type`, `card_cover`, `card_summary`, and `card_logic_map` fields support an optional Obsidian card-wall view; the note itself works without that view. `cssclasses: [literature-note]` is harmless without a matching CSS snippet.

Generate a paper-specific PNG graphical abstract with an available image-generation tool, based only on evidence in the paper. Use `scripts/build_logic_map_svg.py` for a compact 4–6-step SVG logic map and collapsed step notes for detail. Keep both visuals in the staged `图片资源/literature_cards` folder, or the user's chosen asset folder. Update every frontmatter link and body embed to match the chosen folder exactly. Keep the note in the staged note folder and MinerU output in a staged `sources/mineru/<zotero_key>` folder.

When the user asks for a literature card wall, read `references/card-wall-setup.md` and use the bundled `assets/card-wall/` files. Installing cards alone does not create the Obsidian Bases gallery.

## Quality and installation

Before installation, verify UTF-8 text, SVG XML, PNG dimensions and visual preview, exact vault-relative wikilinks, and readable MinerU Markdown with its images. Use the bundled installer; it refuses existing targets and supports a dry run:

```text
python <this-skill>/scripts/install_card_to_vault.py \
  --vault <vault-path> --note <staged-note.md> \
  --graphical-abstract <staged-image.png> --logic-map <staged-map.svg> \
  --mineru-directory <staged-mineru-directory> --dry-run
```

Repeat without `--dry-run` after the dry run passes and any required vault-write approval is granted. Pass `--notes-folder`, `--assets-folder`, and `--sources-folder` when the user chose non-default relative folders. Resolve the script as a real path relative to this `SKILL.md`; the shell snippet is illustrative, not a literal command on Windows.

After installation, check file sizes and links, then open the note in Obsidian and confirm that both PNG and SVG render. If the app view cannot be checked, report `filesystem installed; Obsidian render unverified`. If Obsidian initially misses new files, refresh timestamps once and reopen the note; do not restart the app without the user's approval. Keep a staged backup until the user confirms the result.

The card should answer: what the study measured, in whom, how each key method contributed, what evidence supports the conclusion, what remains uncertain, and which of the user's projects it informs.
