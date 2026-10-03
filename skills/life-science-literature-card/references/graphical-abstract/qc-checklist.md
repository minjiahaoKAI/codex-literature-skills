# QC v2: hard gates and soft references

Actually view the native-size image. Save `ga_qc.json` and a human-readable
`ga_qc.md`; record reviewer method and limitations. Five story questions are
answered from the image at original size. Thumbnail checks only cover structure.

## Hard gates: failure requires correction

1. `literal_text`: transcribe **every** visible string, including added/duplicate
   text; compare each planned label character by character, check English spelling,
   genes, symbols, units and numbers. Line wraps can be joined. Do not rewrite the
   planned labels to make an erroneous image pass. Independent OCR is optional;
   maker self-review is disclosed and is not a blind test.
2. `numbers`: every visible quantitative fact is allowed, source-verified and in
   the correct group/scale/denominator; no fabricated data chart.
3. `direction`: arrows/text match the actual result. Nonsignificance ≠ equality;
   strength of coupling ≠ same phase.
4. `evidence_type`: distinguish primary/secondary/exploratory, observation,
   randomization, MR assumptions, prediction and hypothetical mediation.
5. `association_as_cause`: no causal claim/connector for an observational
   association; no arrows between parallel evidence rows.
6. `unmeasured_organs`: inventory every organ/tissue/data icon against sources;
   no unmeasured organs, even within a hypothetical illustration.
7. `cartoon_elements`: expressive characters, life/action scenes and semantic-free
   decoration are forbidden. Faceless labeled population glyphs are allowed.

Each gate is `pass/fail/unverified`; unverified is not a pass. After a hard failure,
the next prompt lists the concrete error and preserves other facts. Never publish
or install a cover with unresolved hard errors. A missing primary result or
ambiguous evidence label that changes interpretation fails the relevant hard gate.

## Soft references: record, no numeric-triggered retry

Typography: title 4.5–5.5%H and preferably ≤75%W; finding ~3%; section ~2.5%;
methods/explanations/footer 2–2.2%, usual weights 600/600/500/400. Area ~85% by
semantic-region tight bounds, excluding decorative panel/background. Record
method, coordinates and uncertainty; these values do **not** determine acceptance.
An obvious oversized title or large empty region should be corrected in the brief
before generation; afterwards record it for the next card, not another automatic
generation. Record flat-rendering consistency, palette and discovery focal area.

Original-size story questions: who/data; key concept; specific variables and
directions; specific endpoints; association or causal evidence? An inability to
answer that reveals a scientific/label hard error is treated as that hard error.
Other clarity limitations are recorded. Do not claim independent blind testing
when the reviewer already knows the brief.

## Cost and log

One call normally; at most two per card. A third call is permitted only if the
second image has a recorded hard failure. Soft deviations never justify a third
call (or an automatic second call). Three hard failures leave `ga_qc: failed`;
keep an earlier hard-passing cover if available, otherwise stop cover publication.
No background fourth call. Triage follows the same text/science hard gates.

Log start/end UTC, total wall time, per-call time/count, selected output, prompt
version/hashes, source scope, feedback/references and hard failure reasons.
Cover-only regeneration has its own operation log and attempt budget. Acceptance
reports the mean elapsed time over all cards, distinguishing existing extraction
reuse and waiting from processing time. Do not infer timing from file mtimes.
