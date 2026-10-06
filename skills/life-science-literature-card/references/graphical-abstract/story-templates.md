# Story templates v2

Choose the center by complexity and the shape of the finding; paper type controls
the design column and evidence footer. An abstract-only triage story uses only
known facts, no scientific numbers in its cover, and explicit abstract scope.
It can use a compact design/context column plus one finding-centered comparison;
do not revert to an equal-width data→method→result icon strip.

## Complexity and preparation

- **Simple:** 1–2 substantive modules at one level. Only a simplified
  `story_brief.json` is required; no complete main-figure map.
- **Complex:** ≥3 modules or ≥2 evidence levels. Make `evidence_map.json` first;
  cover every main figure, then select 3–5 indispensable modules for the cover.
- A user-requested simple display for a complex article records `display_override`
  and omitted modules. It is not a claim of complete paper coverage.
- A triage abstract cannot establish a full figure map; mark unknown complexity
  or choose a simple abstract-level story without inventing missing results.

Sources identify locator and claim, ideally a local file hash and excerpt.
`evidence_strength` is primary only for a specified primary endpoint, secondary
only if prespecified, otherwise exploratory. Do not upgrade strength based on
figure prominence. Compare the paper title/abstract claim with the primary
endpoint; record any tension, and keep both the overall result and the qualifier.
There is no global three-finding cap for complex work.

## Finding shapes and required structures

| Shape | Structure in story | Center |
|---|---|---|
| contrast | `hero_contrast.side_a/side_b`: label, description, outcome | Paired features with explicitly labeled outcomes |
| gradient | `hero_contrast` plus `gradient_levels`: label, exposure, outcome, source | Ordered low-to-high levels, not fabricated numeric curves |
| trajectory | `trajectories`: group, description, direction, source; time labels | Diverging schematic paths labeled as schematic |
| mechanism_chain | `mechanism_chain`: 3–4 labeled nodes and sourced edges with evidence state | Distinguish tested relations and hypothetical links |
| risk_stratification | `risk_strata`: label, outcome/rate, source; `validation_scope` | Labeled high/middle/low or continuous-risk groups, not invented rates |
| null_result | `null_comparison`: groups, estimate, CI, uncertainty, source | Parallel groups, “未见显著差异”; no equality icon |
| mixed | selected independent modules plus integrated conclusion | Complex evidence map, including null/exploratory modules |
| protocol | planned intervention/comparison/outcome and source | Planned study, no finding or efficacy claim |

Explain the key concept in plain language. For a coupling study name both
variables and distinguish strength from phase. `outcomes_named` lists at most
five specific endpoints ordered by importance/effect; do not replace reported
disease names with “several diseases”. Distinguish device and core temperature.

## Complex cover: choose the arrangement from the story

Select 3–5 substantive modules from the full evidence map. A macro-to-micro
arrangement with design, parallel evidence and integration is useful for work
across biological levels. An analytical story can instead connect real data and
model stages, branch into independent findings and return to common sensitivity
checks. Other arrangements are valid when they explain the whole-paper story.
Do not require equal isolated boxes or the same columns in every paper.
Macro-to-micro order reflects evidence scale, not causality; workflow links
describe actual processing order and need a planned analysis-step legend.
Parallel result modules have no row-to-row arrows. Each module pairs its labeled
method/variable with a finding and an informative graphic where evidence allows.
Negative/FDR-unconfirmed findings remain neutral gray; no unsupported direction.

Design information includes design, population/n, conditions/data and duration.
Any explanatory path comes from `integrated_conclusion`; record `hypothesis_path`
nodes, edge states and sources. Measured tissues only; uncertain mediation is dashed and marked
“假说”/“机制待验证”. Primary endpoint must appear in a small neutral footer badge;
absence of a single primary endpoint is stated rather than invented.

## Information and result graphics

Use complete readable Chinese labels and explanatory context, not a row of large
headings. Earlier 16/24 text-item and 2–4 number targets are optional planning
starting points, not caps that remove useful findings. Set `label_budget` in the
visual brief to the actual justified inventory, count every visible item and keep
all labels available for transcription. Do not hide extra text in tiny legends.
Title length, typography and area follow soft house-style references.

Select verified statistics that help explain the paper: sample/time, effects
with reported uncertainty, model fit or error, and qualified significance where
useful. No compulsory number quota. Keep each number beside its actual comparison,
unit/model and qualifier. A P value cannot replace an effect size; joint-model
fit cannot be assigned to a single predictor. Derivations require sourced
operands and explicit arithmetic; a percentage-point difference is not a relative
percentage. Disputed or unresolvable source numbers stay out of the cover.

Use sourced scalar bars or effect/interval summaries for actual quantities.
Use qualitative direction symbols when only direction is supported. For ordered
cross-sectional groups, use equal-size labeled glyphs at relative heights with
an explicit schematic/order caption; no quantitative axis, time progression,
invented effect or anatomy change. Observational association networks use named
nodes and dashed links without arrowheads. Record each graphic's source, intended
meaning and forbidden inference in the panel description. These are choices,
not required plots or a universal layout. See [house style](house-style.md).
