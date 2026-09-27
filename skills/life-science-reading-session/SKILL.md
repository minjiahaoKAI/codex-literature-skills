---
name: life-science-reading-session
description: Answer questions while reading a life-science paper from the user's Zotero PDF and Obsidian card, then integrate durable insights and Zotero annotations into the card when asked. Use for active deep reading rather than a first screening card.
---

# Life Science Reading Session

Use the current user's sources and configuration. A title, DOI, Zotero key, PDF path, or card name is enough to start a session. Resolve the Obsidian vault from `OBSIDIAN_VAULT_PATH` or ask for its absolute path; do not assume the skill author's vault, CLI paths, Zotero library, or token.

## Resolve the paper

1. Find the existing Obsidian card by title, DOI, or Zotero key. Search the user's vault, including their chosen notes folder; `���ױʼ�` is the default used by the companion card skill.
2. Resolve the Zotero item, PDF, and annotations through an available Zotero integration or local API. Read the card and its `mineru_source` link if present. If a source is absent, say which one; do not invent paper details from web summaries. Ask before switching to a web-only discussion.
3. An installed `obsidian-vault-mcp` may help with lookup and annotation retrieval. It is optional. Its own note layout and write tools may differ from this card's schema; do not let it import or rewrite this card automatically. Use its write tools only after checking the exact proposed target and the user's authorization.

If MinerU output is missing or insufficient, inspect the local PDF with an available PDF reader. For a new MinerU online extraction, follow the companion literature-card skill's upload-consent and token rules. Never expose credentials in notes, logs, or chat.

## Reading mode

Answer each question directly in Chinese, citing the relevant paper section, figure, table, or Zotero annotation when available. Separate paper facts, interpretation, and uncertainty. Keep track of useful explanations in the conversation; do not rewrite the main card after every question. If a long session needs a durable record, make a short session note under `<vault>/<notes-folder>/_reading_sessions/`, preserving the user's existing edits.

When editing the card at session start is appropriate, set `read_stage: reading`; otherwise leave it untouched. A local file or vault outside the current writable area may require filesystem approval before writing.

## Integration mode

When the user asks to integrate the session, read the latest card, Zotero annotations, relevant MinerU/PDF passages, and this conversation. Use `references/integration-template.md` as a menu of useful sections, not a transcript to paste. Correct early mistakes, merge repeated points, retain only meaningful highlights and questions, and clearly distinguish the user's interpretations from the paper's claims. Preserve unrelated frontmatter, links, assets, and user edits.

Update `last_literature_update` and the relevant frontmatter state:

- Partial integration: `read_stage: annotation_integrated`, `zotero_annotations: partial`.
- All available annotations integrated: `read_stage: annotation_integrated`, `zotero_annotations: imported`.
- User confirms reading is finished: `read_stage: final_note`; use `zotero_annotations: imported` only if that is true.
- No annotations exist: `zotero_annotations: none`.

An integrated note should say what changed after deep reading, which figures and methods matter, which annotations are useful, what questions were resolved, what remains uncertain, and what can transfer to the user's projects. Verify that Obsidian still opens the edited note and resolves its asset links.
