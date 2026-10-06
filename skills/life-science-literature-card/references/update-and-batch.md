# Installation, batch and update

Stage outside Git, run the numeric verifier and hard GA checks, then dry-run the
installer. Full cards need the source directory, AI cover, logic map and any
referenced design/results assets; no-cover triage can omit visual arguments.
`--assets-directory` supplies additional SVGs actually referenced by the note.
`--source-directory` is also valid for abstract-only `sources/literature/<key>`;
`--mineru-directory` remains backward compatible for full sources.

```powershell
python scripts/install_card_to_vault.py --vault $vaultPath --note $stagedNote `
  --graphical-abstract $coverPath --logic-map $logicPath `
  --assets-directory $stagedAssets --source-directory $stagedSource `
  --number-report $numberReport --qc $gaQc --visual-brief $visualBrief --dry-run
```

Repeat without `--dry-run` only within authorized installation scope. v2 numeric
reports bind to the incoming note hash, then the installer reruns verification
against the final merged text, including protected user content, before any write.
This also applies to dry-runs and cover-only updates. New reports record private
`source_file` and optional `ledger_file` paths for that recheck. For older reports
or moved staging files, pass `--number-source <source.md>` and, when using derived
values, `--number-ledger <ledger.json>`. Do not guess which source or ledger to use.
The returned `final_number_verification` includes counts and the exact UTF-8/LF
note hash that will be written. QC binds to the selected image hash.
Hard failures or stale reports prevent installation. A zero-not-found numeric
report still needs scientific semantic review of endpoint/unit/model/direction.

## Identity and update

`--skip-existing` skips by `zotero_key` within the selected notes folder.
Duplicate identities report conflict. Normal installs refuse a different
existing note/resource. `--update` merges generated content only when a baseline
generated-region hash is intact, preserves outside text and protected user
regions, and preserves reading/annotation state, projects, priority, date_added
and unknown metadata. Legacy unmarked or edited generated text reports conflict;
do not silently adopt it. `--update --cover-only` changes only cover links and GA
metadata, without rewriting the science or reading notes.

Use `%% generated:start %%` / `%% generated:end %%` once. Put editable text outside
that region or inside paired `%% user:start %%` / `%% user:end %%`. The installer
stamps `generated_content_sha256`; changes inside the unprotected region trigger
manual merging. Backup note/assets/sources under `<notes>/_backup/<timestamp>/`
before replacement; hash-verified temporary copies and rollback protect failures.
Original source images and `graphical_abstract/` records are included.

## Batch

Before processing a Zotero collection, enumerate unprocessed items, report count,
tier and cover setting, and wait for confirmation. This is a batch scope decision,
not repeated per-item installation approval. Triage never calls MinerU.

`--batch <manifest.json>` accepts a `cards` array, with the same option names using
underscores. Paths are relative to the manifest directory (absolute runtime paths
also work). Each failure is reported while other cards continue. Use `--dry-run`
first and `--skip-existing` when appropriate. Keep this manifest private.

Optional `migrate_cards.py --folder <notes> --dry-run` fills only missing fields;
the real run backs up before changing metadata and leaves body unchanged. Legacy
unknown generation count/time is null; legacy GA QC is unverified, not passed.
The card wall works without migration through fallback formulas.

To repair empty added dates, first run:

```powershell
python scripts/fill_card_dates.py --vault $vaultPath --zotero-db $zoteroDbPath --report $dateReport
```

Review the planned dates and their sources before adding `--apply` within the
authorized Vault. The helper opens Zotero read-only, fills only empty dates and
backs up changed notes. For a copied test Vault, pass `--fallback-file-dates` with
a private JSON map of Vault-relative note paths to original creation dates.

For a v2.1 body-only update, retain the selected cover, logic SVG and GA records.
Use cached full text, preserve the calibrated project judgement and reading notes,
then verify the complete incoming note's numbers before installation. This update
does not start cover generation. Triage bodies retain their short structure.

Default no-cover triage installs the shared type SVG set on first use. Reusing
identical placeholders adds no work to the write plan; they are not embedded in
the body. Upgrading with --update produces the dedicated full PNG and preserves
read_stage, annotations, projects, date_added and protected reading notes.
