# Setup, sources and private installation

Use the current recipient's Vault, Zotero library, CLI and credentials. Resolve the Vault from `OBSIDIAN_VAULT_PATH` or the user's supplied absolute path; require an existing `.obsidian` directory. Default relative folders are `文献笔记`, `图片资源/literature_cards`, and `sources/mineru`.

Resolve Zotero metadata, abstract, local PDF and existing MinerU output before browsing. Never make a formal web-only card without explicit authorization. Record exact source scope: abstract for triage; full text and original figures for full cards. Existing complete MinerU extraction may be reused with file provenance. Prefer the Zotero local API/integration. If SQLite is locked, use a consistent read-only snapshot including WAL/SHM and `PRAGMA quick_check`; never modify the live database.

## MinerU

Resolve `mineru-open-api` on PATH or `MINERU_CLI`. Configure the recipient's own account with `mineru-open-api auth`. Never ask for a token in chat or put it in a command argument, repository, note or log. Never print environment secrets or use verbose extraction. `auth --verify` checks local token format, not successful online extraction.

Before the first online extraction, explain that the selected PDF is uploaded to the configured MinerU service and obtain the user's approval. Reuse any existing approval that explicitly covers this upload. Skill invocation alone is not upload consent.

```powershell
& $mineruCli extract $pdfPath -o $stagedMineruDirectory --format md --timeout 900
if ($LASTEXITCODE -ne 0) { throw 'MinerU precision extraction failed' }
```

Require readable Markdown and intact relative `images/` files. Record `source_status: local_zotero_pdf_mineru_extract`, `mineru_mode: extract`. Preserve authentication, quota, timeout and size failure categories. Use `flash-extract` only after explicit approval; label the downgrade. Inspect partial output before any repeat upload.

## Staging and writes

Stage notes, PNG, SVG, source images, numeric reports and GA records outside the repository. Do not install a note before its required assets. The full-card GA records live in `sources/mineru/<zotero_key>/graphical_abstract/`; triage records use `sources/literature/<zotero_key>/graphical_abstract/` and `mineru_source: ""`. Neither layout asserts extraction where none happened.

Use the installer dry run before any Vault mutation. Obtain filesystem approval when required by the environment; an authorized installation need not be reconfirmed. Do not overwrite an existing card by default. Explicit update requires a backup and protected user sections. Never copy a whole Vault or someone else's `.obsidian` configuration. Verify installed file hashes and local links, then open the note in Obsidian. Filesystem checks alone are not UI acceptance. Do not restart or close the user's Obsidian session without authorization.

Private papers, original figures, generated cards/covers, annotations, paths, tokens and reference images do not enter Git. Public examples contain only manually curated open-paper facts and prompts. See the repository `.gitignore` before each commit.
