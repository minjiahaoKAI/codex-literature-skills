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

## Complex cover

Quiet integrated title, narrow left design column, central 3–5 parallel modules,
right sourced integration path, small footer. Macro-to-micro order reflects
evidence scale, not causality. Each module has a labeled level/method icon and a
short finding, with arrow only for an actual direction. Negative/FDR-unconfirmed
findings remain in neutral gray. No connector between central rows.

Left column only design, population/n, conditions/data and duration. Right path
comes from `integrated_conclusion`; record `hypothesis_path` nodes, edge states
and sources. Measured tissues only; uncertain mediation is dashed and marked
“假说”/“机制待验证”. Primary endpoint must appear in a small neutral footer badge;
absence of a single primary endpoint is stated rather than invented.

Prefer ≤16 visible text items for simple work, ≤24 for complex. Title preferably
≤25 Chinese characters /14 English words, one complete integrated finding.
Soft typography/area values follow house style. Numeric facts are source-backed;
2–4 are usually enough, but a justified key effect can exceed that budget without
hiding multiple facts inside one label. A derived percentage-point difference
records the formula and verified operands; never label it a relative percentage.
