---
name: life-science-literature-card
description: "Create and improve Chinese-first life-science Obsidian literature cards: make a full paper card, triage an abstract, batch-process a Zotero collection, upgrade a triage card, or regenerate only its graphical-abstract cover. Use source-checked evidence summaries, study-specific appraisal and AI scientific covers. Resolve the recipient's local Zotero/PDF/MinerU sources first; active deep-reading Q&A belongs to life-science-reading-session."
---

# Life Science Literature Card v2.1

Help the reader decide in the first screen whether to read closely, then explain
the paper's question, concepts, narrative, methods and evidence. Chinese first; retain English
method/gene names, avoid generic praise, and distinguish facts from interpretation.

## Route the request

- “做卡片 / 完整卡” or one important paper → `full`.
- “快速看看 / 分拣” → `triage`, using metadata/abstract, no MinerU or image-generation call by default.
- Collection/batch → enumerate unresolved and unprocessed items, propose count,
  tier and cover setting, wait for that scope confirmation, then process.
- Upgrade → full preparation and new full cover, preserving user reading state.
- “只重新生成封面” → cover-only route below, without rewriting the card body.
- “只改完整卡正文” → reuse cached full text and existing cover/GA records;
  explain concepts, narrative and methods, preserve project judgement and reading
  notes, and verify the rewritten numbers. Skip the cover workflow entirely.
- “只更新课题连接 / 阅读判断” → read the current profile and update its connection
  section, relevance metadata and verdict display only; preserve science, sources,
  covers, GA logs, reading records and existing project links. Stage for review.

Read [setup.md](references/setup.md) for source resolution, recipient paths,
token handling, upload consent, staging and installation permissions. Never
request/expose a token, upload an unapproved PDF, silently replace local sources
with web content, or overwrite user content. Stage all artifacts outside Git.
An existing complete source extraction can be reused without another upload.

## Read the paper, then write the card

1. Resolve local Zotero metadata, abstract, PDF, extraction provenance and source
   images. Triage facts come only from the abstract/allowed initial PDF pages.
   Full cards need the complete local source; disclose gaps instead of guessing.
   Default triage skips evidence maps, story/visual briefs and cover QC; it keeps
   abstract numeric/semantic checks and records total elapsed time with zero GA calls.
2. Identify the main design and publication stage. Read only its file under
   [paper-types](references/paper-types/); mixed work can add one necessary modifier.
   Image modality does not replace a cohort/RCT/prediction design. A protocol has
   planned endpoints, no observed efficacy results.
3. Trace question → design → actual measurements → results → qualified conclusion.
   Specify analysis population, denominators, time, comparison unit, outcome and
   adjustment. Separate primary, prespecified secondary and exploratory results.
4. For a full card or explicitly requested cover, decide complexity: simple 1–2 modules at one level needs a simplified story;
   ≥3 modules or ≥2 levels needs a complete main-figure evidence map. For a complex
   full article, make [evidence_map](references/graphical-abstract/evidence-map-schema.md)
   before choosing the 3–5 central cover modules. Keep negative primary findings
   and any tension with the paper's broader title claim.
5. Read the user's `_my_projects.md`, including its usage rules and exclusions.
   Its rules take precedence over default relevance/verdict guidance. Assess broad
   interests and current questions separately; theme, method or narrative can
   each justify a concrete connection. Follow [project-relevance.md](references/project-relevance.md).
   Under the calibrated template, no theme match means no strong relevance;
   method/narrative must name a transferable operation and target task. Strong
   relevance alone does not justify 精读: require a direct current question or
   exceptional short-term reuse. Uncertain gates stay unestablished.
   Display connections as one assessment line, one reason sentence and at most
   two rows in three columns; collapse detailed limitations and gate records.
   Use [my-projects-template.md](references/my-projects-template.md) if absent;
   missing profile means “未评估：尚未提供课题档案”, never invented projects.
6. Draft from [initial-card-template.md](references/initial-card-template.md) or
   [triage-card-template.md](references/triage-card-template.md). Full cover first, then
   a short integrated conclusion/assessment, study profile and quick judgment,
   3–5 expanded concepts, an expanded narrative followed by a logic SVG and
   optional collapsed steps, separate explained methods, an evidence table with
   original figure, innovation/limitations, collapsed type-specific credibility,
   compact project connections, 5–7 questions and collapsed sources.
   Write complete, readable sentences; explain each method's definition, purpose
   in this paper and points to check. Keep triage short and unchanged.
7. Put source locators mainly in the evidence table; append locators to key numbers
   outside it. Avoid citation tags after every explanatory sentence.
   Reporting checklists are information prompts, not quality scores. “Not reported”
   does not mean “not done”. Never call association a causal effect or a null
   test equality. Keep strength of rhythm coupling separate from phase.

## AI cover: four explicit steps

Triage defaults to no cover; the wall displays shared study-type placeholders.
An explicit triage-cover request enables this workflow; upgrading to full creates
a checked paper-specific cover while preserving reading and project state.
Always use the built-in image-generation tool for a requested cover. No script
overlay of its title/footer. Approved default: white/neutral-gray `house-style-v2`,
Chinese labels, landscape 16:10. Use restrained accents to distinguish branches
and source-supported result graphics with concise text. Choose layout per paper;
existing covers retain their recorded style and are not automatically regenerated.

1. **Story:** save `story_brief.json`, with key concept, finding shape, specific
   endpoints, sources, allowed numbers and must_not_show. Complex full papers
   additionally save a complete evidence map. See [story templates](references/graphical-abstract/story-templates.md).
2. **Visual:** save `visual_brief.json`: exact label IDs/text/roles, panel positions,
   meaningful labeled icons, named number references and evidence-aware links.
   Center organization follows finding shape and complexity, not paper type alone.
   Parallel result modules have no row-to-row arrows. Genuine analytical stages
   may connect as workflow; association lines are dashed without arrowheads.
   Use at most one sourced explanatory path; hypothetical links dashed and labeled.
   Match quantitative/qualitative graphics to the available evidence; do not
   invent magnitudes, intervals, progression or anatomy. Draw no unmeasured tissue.
3. **Prompt/tool:** read `_ga_feedback.md` and inspect any available ignored
   `references/graphical-abstract/style-refs/` files. Use new references from the
   next card, learning style only. Run `build_ga_prompt.py` to insert the fixed
   [house style](references/graphical-abstract/house-style.md) verbatim and the
   variable panel/label inventory. Save `ga_prompt.md`, tool inputs and original
   PNG; copy the image from the tool's output directory into staging unchanged.
4. **QC:** actually view the original image, transcribe every text item, compare
   with planned labels, check English spelling, numbers, directions, evidence,
   tissues and cartoon elements. Save `ga_qc.json` and `ga_qc.md`; use
   [QC checklist](references/graphical-abstract/qc-checklist.md) and `qc_decision`.
   Answer the five story questions at native size; thumbnails only need structure.

Hard conditions require correction: text mismatch, false number/direction/evidence,
association drawn as cause, unmeasured organs/tissues, cartoon/scene/decoration.
Soft typography and area reference values are recorded, never numeric retry gates.
One call normally, at most two per card; a third only after a documented hard
failure of the second. Never make a fourth call or install a hard-failed image.
`ga_workflow.py` persists attempts and total elapsed UTC wall time. Record soft
issues as `passed_with_issues` only after every hard gate passes.

Full GA records go under `sources/mineru/<key>/graphical_abstract/`; triage records
under `sources/literature/<key>/graphical_abstract/`, with `mineru_mode: not_used`.
Keep briefs, prompt, selected/raw attempts, QC, feedback/reference hashes and
`generation_log.json`. The cover log is private and is not a repository example.

## Exact body visuals and numbers

- `build_design_diagram.py`: sourced cohort, randomized/parallel or crossover RCT,
  and analysis pipeline diagrams. Each numeric fact has a source.
- `build_key_results.py`: 2–8 reported effects with actual CIs on the right scale,
  or task-appropriate metric bars. Skip if no usable numbers; never invent CIs.
- `build_logic_map_svg.py`: short reading-map titles/one-line details, automatic
  wrapping and growing boxes. Step notes add evidence/limitations, not duplication.
- Use one original MinerU image with a concise Chinese explanation in full cards;
  original paper images remain private, outside Git.
- All SVG helpers use `_style.py`, include Microsoft YaHei fallback, and use only
  Python stdlib. Parse XML and view rendered output after the final change.
- Run `verify_card_numbers.py` on body, story, visual and helper JSON. Normalize
  thousands, CI notation and math markup; verified derivations require sourced
  operands and explicit arithmetic. Zero unresolved numbers before installation.
  The installer rechecks the final merged text against the report's local source
  and derivation ledger before writing; see `references/update-and-batch.md` for
  older reports or moved staging paths.
  A numeric text match is a candidate; manually confirm endpoint/unit/model/group.

## Compatibility, batch and updates

Use [frontmatter.md](references/frontmatter.md). Never reset read_stage,
zotero_annotations, projects, date_added or unknown user metadata. Card wall
requires note_type/card_summary and a real card_cover when generated. A no-cover
triage card has empty image links, `image_mode: disabled`, `ga_attempts: 0` and
`ga_qc: not_generated`. Shared placeholders are display-only; never store them
as card_cover or graphical_abstract. The installer copies bundled type SVGs once.
Record triage timing in `sources/literature/<key>/generation_log.json`.
For the card wall, use native Cards `cardSize: 260` as the starting size for
3–4 columns in ordinary windows; verify actual available pane width. Show only
journal, year, verdict and a truncated summary by default; other properties remain
selectable in Obsidian. Fill empty date_added using `fill_card_dates.py` from
read-only Zotero dateAdded, then original file creation date; preserve nonempty dates.

Read [update-and-batch.md](references/update-and-batch.md). Installer supports
dry-run, skip-existing, update, cover-only and batch with per-card failure isolation.
Back up before replacing and preserve protected user regions. Legacy/edited
generated content needs manual conflict review. Batch manifests stay private.
Do not write the note before its assets; verify hashes and exact embedded paths.

Install [literature-note.css](assets/literature-note.css) and the optional
[card wall](references/card-wall-setup.md) within authorized scope. Open actual
Obsidian views to verify; report UI unverified if inaccessible, not “all passed”.
No restart/close of a user's active session without permission.

## Cover-only regeneration

Read saved briefs, current full/abstract scope, feedback and latest house style.
Validate facts/labels without re-reading unrelated papers or rewriting the body.
Create a fresh operation log (`operation: cover_only`), generate/check within the
same attempt budget, stage a versioned PNG and GA records, then dry-run
`--update --cover-only`. Preserve the existing card and cover until the new one
passes hard checks. Backup before final replacement; do not retroactively apply
new style references to other cards.

## Deliver

Return card links, tier, source scope, generation count/time and unresolved issues.
Distinguish artifact, filesystem and actual Obsidian render checks. A batch also
reports skipped/conflict/failed items. See the manually curated public
[cohort card](references/example-card-cohort.md) and
[GA examples](references/graphical-abstract/examples/); private generated cards
and original/AI images never enter repository commits.
