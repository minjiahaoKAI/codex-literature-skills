# House style v1

Approved teal journal graphical-abstract style. Version `house-style-v1`.
Chinese labels by default, retaining gene/method names in their original spelling.
The gray-blue test variant is retired; gray-blue remains a subordinate icon color.

## Colors

| Use | HEX |
|---|---|
| Near-white warm-gray background | `#FAFAF7` |
| Very pale sage panels | `#EEF4F1` |
| Primary teal: icons, small headings, fine outlines | `#4F8A7B` |
| Auxiliary gray-blue: subordinate icons/lines | `#7FA3BC` |
| Single apricot discovery accent | `#D9895B` |
| Nonsignificant, FDR-unconfirmed, unsupported findings | `#8A9099` |
| Charcoal title/body | `#2F3437` |
| Secondary explanations/methods/footer | `#6B7280` |

Large areas stay light. No dark solid banner, reverse white labels, heavy borders,
ochre backgrounds or saturated red/green suggesting good/bad. Title entirely
charcoal. Apricot only for actual findings and their directions, never the sun,
title words, hypothesis arrows or backgrounds. A negative finding has gray text
without a direction arrow; statistical nonsignificance is not equality.

## Typography and layout reference values

| Role | Approximate height/H | Weight |
|---|---|---|
| Single-line title, width preferably ≤75% | 4.5–5.5% | 600 |
| Module discovery | 3% | 600 |
| Section heading | 2.5% | 500 |
| Method/explanation/footer | 2–2.2% | 400 |

These are **soft reference values**, not pass/fail thresholds. Record visible
glyph estimates and distinguish them from SVG font-size. Content-area 85% is
also a soft reference. Never retry merely because a ratio misses its target.
Correct an obviously oversized title or large empty scene in the brief before
generation; if noticed afterwards, record it and improve the next card rather
than spending another generation on a soft deviation.

Discoveries are the focal area. The primary endpoint is a readable small gray
footer badge, alongside design/evidence information. Thumbnails only need a
recognizable structure and hierarchy; title readability is not required because
the card wall already displays `card_summary` below the cover.

## Scientific structure

Simple work uses a finding-centered contrast, gradient, trajectory, mechanism,
risk-stratification or null layout. Complex work has a narrow design column,
3–5 independent central evidence modules from whole-body/population to molecular
levels, one integration column and a quiet footer. No arrows between parallel
central rows. Only the integration column contains a proposed explanatory path;
unverified edges are dashed in a dashed box labeled “假说”/“可能”. Never turn
parallel CGM and calorimetry results into a causal sequence.

Only measured tissues/levels may be drawn. Whole-body physiology does not justify
brain/liver/fat tissue icons. A sourced unmeasured hypothesis may be written as
explicit hypothetical text, without an unmeasured-organ illustration. Keep the
primary endpoint and negative/uncorrected results even if the title claim is
broader. Strong rhythm coupling means stable relations, not necessarily same
phase. Do not draw a null result with an equal sign unless actual equivalence or
noninferiority evidence supports it.

## Rendering and forbidden elements

Uniform flat vector scientific illustration, fine consistent outlines, at most
one slight flat shading plane. Accurate restrained organs, blood, skeletal
muscle, cells and method icons only where sourced. People are small faceless
static population glyphs. Use a sun/window-grid condition symbol and a bulb,
not office scenes. Use a ventilated head hood for indirect calorimetry when that
is the actual method, not a whole-body chamber.

Forbidden: expressive faces, cartoon actions, rooms/furniture/plants/computers,
realistic 3D rendering, gradients, shadows/glow, decorative wireless waves,
sparkles/checkmarks, invented structures, logos, actual faces and fake data
curves/axes/heatmaps/volcano plots. Omics is a small clearly schematic method icon
with a method label. Every meaningful icon has an adjacent textual label.

## References and feedback

Read the user's `_ga_feedback.md` before generation. Inspect local images from
`style-refs/` and pass their absolute paths as `referenced_image_paths`; use
`num_last_images_to_include` only for conversation-only images, never both.
Record reference/feedback hashes in the private generation log. New reference
images apply starting with the next card; do not retroactively regenerate cards.
Learn color, line and layout only, without copying scientific content/elements.
`style-refs/` is ignored by Git. Before images arrive, the fixed text style is
sufficient. Titles and footers remain image-generated; no script text overlay.

## Fixed prompt block

The assembler inserts the block below verbatim into every prompt.

<!-- prompt:start -->
Chinese journal graphical abstract, wide landscape 16:10. Flat vector scientific illustration with fine uniform lines, at most one slight flat shading plane, no realistic render, gradient, shadow or glow. Background #FAFAF7, pale panels #EEF4F1, teal icons/section labels #4F8A7B, auxiliary gray-blue #7FA3BC, all title text charcoal #2F3437, secondary text #6B7280. One apricot accent #D9895B only for evidence findings and their direction arrows. Negative/nonsignificant/FDR-unconfirmed findings #8A9099, no direction arrows or equality signs. No dark solid blocks or banners, no saturated red/green, no orange sun/title/hypothesis. Reference type scale: title 5%H, findings 3%H, section 2.5%H, method/body/footer 2.1%H; title medium semibold, one line, preferably within 75%W. Discoveries are the sole focal area; primary endpoint is a small gray footer badge. No expressive/cartoon faces, action/office/room/furniture/plants/computer scenes, invented organs, decorative wireless waves/sparkles/checkmarks, logos or real faces. No fabricated data curves, axes, heatmaps, scatter/volcano plots. All meaningful method/variable icons have labels. Central evidence modules are parallel, no arrows between them. A sourced speculative explanatory path appears only once in the integration column, dashed and labeled hypothesis. Draw only measured tissues. Render every planned label exactly and no extra words or numbers. Generate the image and its text together, without script overlay. Style references teach palette, lines and layout only; never copy their scientific content or elements.
<!-- prompt:end -->
