# Frontmatter v2 contract

Optional profile assessment fields: `project_relevance` (`强相关`, `中相关`,
`弱相关`, `弱相关或无关`, `未评估`), `connection_types` (a list of `主题`, `方法`, `叙事`),
and `verdict_reason` (plain explanation). Missing legacy fields mean unassessed;
no migration is required and no existing view depends on their presence.
They may refresh with an explicitly requested profile assessment. Preserve
`projects` until its links are authorized; no short-name note is inferred.
See [project-relevance.md](project-relevance.md) for profile precedence and matching.

Keep every existing field and unknown user property. `card_tier` and `read_stage` are independent: upgrading a triage card must preserve `reading`, `annotation_integrated` or `final_note`, `zotero_annotations`, `projects`, and protected content. Preserve `date_added` after first creation. Update `last_literature_update` only after a completed change.

Existing required fields remain: title, short_title, authors, year, journal, doi, url, zotero_key, pdf_key, mineru_source, source_status, mineru_mode, read_stage, zotero_annotations, graphical_abstract, image_mode, card_cover, card_logic_map, card_summary, note_type, priority, projects, topics, methods, cssclasses, tags, last_literature_update and created_by.

New fields:

```yaml
study_type: observational-cohort
publication_stage: results
design_summary: ""
verdict: ""
key_result: ""
date_added: YYYY-MM-DD
card_tier: full
ga_prompt_version: house-style-v2
ga_attempts: 1
ga_qc: passed
generation_elapsed_seconds: 0
generation_log: "sources/mineru/<key>/graphical_abstract/generation_log.json"
project_relevance: 未评估
connection_types: []
verdict_reason: ""
```

`study_type` uses the paper-type filenames. Mixed work uses a primary design and optional `study_modifiers`. Protocols set `publication_stage: protocol` and report planned outcomes without fabricated results. A missing project file means “未评估：尚未提供课题档案”; only an inspected file with no substantive match justifies “与当前课题无直接关联”. `projects` contains actual resolvable wikilinks.

Allowed GA states: `passed` (hard checks pass), `passed_with_issues` (hard checks pass; soft/style deviations recorded), `failed` (a hard check fails), `not_generated` (cover disabled). Never install a failed generated cover. Default no-cover triage uses empty `card_cover`/`card_logic_map`, `ga_attempts: 0`, `image_mode: disabled`. Full cards require a checked AI PNG and logic SVG. Triage never claims MinerU extraction.

When Zotero's abstract is incomplete and the allowed initial PDF pages supply the
summary, use `source_status: zotero_metadata_pdf_initial_pages` and record the PDF
key, page scope and hash in private provenance. It remains triage, with no MinerU
call; do not describe it as a full-paper reading.

Scientific numeric verification and source-image availability must be explicit. A body claim ends with a locator, e.g. `〔Fig 2b〕`. GA labels and numbers reference source IDs in the brief. Layout dimensions, figure identifiers, dates, DOI and citation years are not study results.

The stdlib frontmatter helper recognizes top-level fields and preserves raw unknown blocks. Unsupported YAML anchors, aliases, duplicate keys or unsafe structures cause a conflict; they are never silently normalized. Markdown user content is protected by `%% user:start %%` / `%% user:end %%`; legacy notes without generated-region markers cannot be automatically replaced.

The shared study-type SVG is computed by the card wall only. It is not a paper
cover, adds no required metadata, and does not count as image generation.
No-cover generation logs live at `sources/literature/<key>/generation_log.json`.
