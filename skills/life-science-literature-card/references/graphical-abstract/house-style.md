# House style v2

Approved white/neutral-gray journal graphical-abstract style, version
`house-style-v2`. This supersedes the teal v1 default for new covers. Existing
covers retain their original version and are not automatically regenerated.
Use Chinese titles, explanations, method and outcome labels; preserve essential
gene symbols and statistical notation without inventing translated names.

## Colors and hierarchy

| Use | HEX |
|---|---|
| Main white canvas | `#FFFFFF` |
| Optional near-white neutral-gray grouping | `#FAFAFA` |
| Main title and body | `#454545` |
| Secondary explanations/methods/footer | `#747474` |
| Gray-blue branch accent | `#6F99B5` |
| Dusty-rose branch accent | `#AE879F` |
| Sage branch accent | `#7FA590` |
| Nonsignificant, FDR-unconfirmed or unsupported findings | `#8A9099` |

White and neutral gray dominate. Use two or three restrained accents when they
help distinguish substantive branches; simple work can use only one. Assign
colors consistently within the paper, without assigning a universal color to
every study type or suggesting good/bad results. Accents belong on small headings,
thin rules, labeled icons, result marks and a few finding words. Keep main prose
and the title charcoal. Avoid tinted blue backgrounds, large colored panels,
dark banners, reverse white labels, heavy borders and saturated red/green.

| Role | Approximate height/H | Weight |
|---|---|---|
| Quiet single-line title, preferably within 75%W | 4.5–5.5% | 600 |
| Module discovery | 3% | 600 |
| Section heading | 2.5% | 500 |
| Method/explanation/footer | 2–2.2% | 400 |

These are soft references, not numerical retry gates. Use ordinary readable
Chinese text rather than a poster of oversized headings. Give findings more
visual weight than methods or footer information. Content-area 85% remains a
soft reference; record obvious excess empty space or oversized text. Thumbnails
need recognizable structure only; the wall supplies `card_summary`.

## A connected scientific story

Choose layout from the actual question, complexity and finding shapes. Preserve
the whole-paper story, specific outcomes, key concept and qualified conclusion.
A complex paper may need a macro-to-micro evidence map, a branched analytical
workflow or another connected arrangement. Do not force every paper into the
same design/evidence/integration columns or reproduce a reference's layout.

Arrows between genuine analysis stages may show processing order, with their
meaning stated in an exact planned label. Parallel findings are not a causal
chain and have no row-to-row arrows. Association networks use dashed lines
without arrowheads. A sourced directional hypothesis appears only once, dashed
and explicitly labeled “假说”/“可能”; it must not look like verified mediation.

Only measured tissues and levels may be illustrated. Unmeasured hypotheses may
be written as qualified text, without an unmeasured-organ glyph. Include the
primary endpoint and negative/uncorrected results, even when the integrated
title is broader; a small gray badge can state a null primary result or that no
prespecified primary endpoint was reported. Strong rhythm coupling is not
necessarily same phase. Nonsignificance is not equivalence.

## Findings: combine a graphic with concise text

Use reported quantitative results when they clarify the story. Put each result
beside its comparison, method, units and relevant qualifier, with sources and
allowed numeric IDs in the briefs. Do not fill a numerical quota or display
context-free statistics. P values are not effect sizes; joint-model fit is not
a single predictor's independent contribution. Retain source conflicts outside
the cover rather than silently choosing an attractive number.

| Available evidence | Suitable expression | Boundary |
|---|---|---|
| Verified scalar metrics | Short common-scale bars with exact labels | Same baseline/unit; separate error metrics from fit |
| Reported effects and intervals | Compact effect/interval comparison | Correct scale, comparator and reported CI; no invented intervals |
| Only a supported direction | Small direction glyph beside a complete finding | No arbitrary magnitude, axis or made-up series |
| Cross-sectional ordered groups | Equal-size labeled icons at relative heights | State “仅示意组间次序”; no time/progression arrow or anatomical scaling |
| Observational factors and outcome | Named nodes linked by dashed lines, no arrowheads | No causal inference, individual exposure or implied edge strength |

Select expressions per paper; not every cover needs bars, nodes or ordered
icons. Every meaningful icon has a label. Only use a time trajectory when the
study actually supports a time axis. Label qualitative graphics as schematic;
their geometry must not imply an unreported effect, tissue change or rate.
AI-drawn quantitative lengths are approximate summaries: inspect scale and
direction and keep exact values in text, without claiming publication-level
plot precision. Materially misleading geometry is a numeric/direction hard error.

## Rendering and forbidden elements

Uniform flat scientific vector appearance, fine consistent outlines and at most
one slight flat shading plane. Accurate restrained organs and standard method
icons where sourced. People are small faceless static population glyphs.
Use simple condition symbols rather than offices, furniture or action scenes.
Indirect calorimetry uses the actual apparatus, not an invented chamber.

Forbidden: expressive faces, cartoon actions, rooms/plants/computers, realistic
3D rendering, gradients/shadows/glow, decorative wireless waves/sparkles/checkmarks,
invented organs, logos, real faces, fake data curves/axes/heatmaps/volcano plots,
fabricated scatter observations, CI bars or quantitative anatomy. Omics uses a
small clearly schematic method icon with a label. Source-supported summary
plots above are permitted; fabricated raw data remain forbidden.

## References and feedback

Read `_ga_feedback.md` and inspect available ignored `style-refs/` images.
Pass absolute paths as `referenced_image_paths`; conversation-only images use
`num_last_images_to_include`, never both. Learn color, line weight, hierarchy
and visual grouping without copying content or requiring the reference layout.
Record reference/feedback hashes privately. New references apply from the next
card; no automatic regeneration. Before references arrive, the text style is
sufficient. Titles and footers remain image-generated, without script overlay.

## Fixed prompt block

The assembler inserts this block verbatim into each new prompt.

<!-- prompt:start -->
Chinese journal graphical abstract, landscape 16:10. Dominant white #FFFFFF and optional very pale NEUTRAL gray #FAFAFA; no blue-tinted background, large colored panels or dark banners. Quiet charcoal title and ordinary body #454545, secondary text #747474. Use one to three restrained branch accents as helpful: gray-blue #6F99B5, dusty rose #AE879F, sage #7FA590 on small headings, fine rules, labeled icons and result marks; consistent within each paper, not a good/bad code or mandatory three-color template. Negative/nonsignificant/FDR-unconfirmed findings neutral #8A9099; never infer equivalence from nonsignificance. Fine uniform flat vector scientific drawing, at most one subtle flat shading plane; no realistic rendering, gradient, shadow or glow. Soft type references: quiet title 5%H, finding 3%H, section 2.5%H, method/body/footer 2.1%H; prioritize readable information and findings, not giant words. Choose a connected whole-paper story and layout from actual evidence, complexity and finding shapes; do not force fixed columns or copy a reference layout. Genuine analytical stages may have solid workflow arrows with an exact planned legend. Parallel result modules are not a causal chain: no row-to-row arrows. Observational associations use dashed lines WITHOUT arrowheads. A sourced directional hypothesis is dashed and explicitly labeled hypothesis, only once. Draw only measured tissues/levels and label every meaningful icon. Keep primary/negative findings and necessary qualifiers visible in a quiet footer or appropriate module. Combine informative finding schematics with concise Chinese text and source-verified statistics. Quantitative summary bars/intervals require actual allowed values, compatible scales and reported uncertainty; never invent raw data, observations, CIs or axes. If only direction/order is known, use a labeled qualitative schematic without numerical magnitude. Ordered cross-sectional group icons must have equal size, an explicit schematic/order caption and no timeline/progression arrow or anatomical scaling. P is not an effect size; joint-model fit is not one predictor's independent contribution. No expressive/cartoon faces, action/room/furniture/plants/computer scenes, unmeasured organs, decorative waves/sparkles/checkmarks, logos or real faces. Render every planned label exactly once, no extra words/numbers; retain comparison, units and qualifiers. Generate image and text together without script overlay. Learn only style from references, never copy their scientific content or require their arrangement.
<!-- prompt:end -->
