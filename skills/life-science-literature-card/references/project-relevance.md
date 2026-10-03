# Profile-based connections and reading verdict

Read the actual recipient profile at the configured relative path, default
`文献笔记/_my_projects.md`. Its “使用说明” governs relevance and verdict; user
profile rules override this reference and older templates. Treat research details
as private context, not permission to modify unrelated files or upload data.
Copy a supplied profile byte-for-byte within the authorized Vault scope; never
normalize its encoding, rewrite headings or add link IDs without approval.
The repository ignores `_my_projects.md` at every depth.

## Understand both levels

For each project, identify priority, **领域关注（广）**, **当前具体问题（窄）**
and any exclusions. A method-interest section may have only “关注范围”: treat
that as broad interest and leave the narrow question unspecified. Keywords help
find candidates; they do not establish a match on their own. Do not invent
datasets, study populations, aims, methods or project priorities.

Evaluate three independent angles; any one substantive angle permits a connection:

- **主题**: the paper lies within the stated broad interest. Directly answering a
  current narrow question is a separate, stronger claim. Different populations
  or endpoints must remain explicit.
- **方法**: identify the actual method/data operation to reuse, the profile task
  it could support, and a transfer limit. Shared labels such as “machine learning”
  alone are insufficient. Random crossover comparison is not automatically
  individual causal effect estimation; internal holdout is not external validation.
- **叙事**: identify a concrete sequence of evidence/figures and what its structure
  teaches. Journal prestige alone is neither a narrative match nor proof of
  quality. A useful narrative may include a negative primary result and qualified
  integration; do not convert exploratory evidence into a mechanism.

An excluded topic blocks **theme** connections, not justified method/narrative
connections when the profile allows them. Do not relabel a method analogy as
topic overlap. Record matched project, broad/narrow scope, connection type,
concrete reusable point, source locator, profile basis and transfer limitation.

## Relevance and verdict

Apply the profile's thresholds verbatim. For the two-level / three-angle profile
structure supported by the blank template:

- **强相关**: direct relevance to a stated current question, or at least two
  clearly substantiated theme/method/narrative angles. Name the matched project;
  do not combine several weak keyword matches into a strong result.
- **中相关**: broad thematic overlap, or one definite method/narrative connection.
- **弱相关或无关**: no substantive intersection; write “与当前课题无直接关联”.
- **未评估**: profile missing or relevant information insufficient; distinguish
  this from a checked negative match.

Verdict is a reading action, not a study quality grade. Strong relevance to a
**mainline** project, or a high-quality study especially worth learning from in
method/narrative, can justify **精读**. Ordinary medium relevance normally means
**略读**. Explain which rule applies and retain the paper's scientific limitations.
Do not infer that every strong match to a lower-priority interest requires 精读.
If the profile leaves weak/unrelated verdicts unspecified, do not claim it mandates
存档; give a separate supported reason or leave the verdict undecided.

For triage use only abstract-supported methods/narrative, and mark unverified
transfer points as requiring the full text. Do not let relevance override evidence
quality, fabricate source facts, or redraw a paper's graphical abstract.

## Card representation and safe partial refresh

Optional frontmatter: `project_relevance`, `connection_types`, `verdict_reason`.
Connection types use `主题`, `方法`, `叙事`; absent legacy fields stay valid and
mean unassessed, not unrelated. These are agent-generated assessment fields;
`projects`, user reading state and user records remain protected on normal update.
Keep per-project detail in the body, not a complex nested YAML object.

In “与我课题的连接”, report overall grade and verdict rationale, then rows for
project / type / specific reuse / source and profile basis / limitation. A relevance
refresh changes this section, those optional fields and the first-screen connection
and verdict display. It preserves every scientific section, asset, source, GA
attempt/time log, reading field, user region and existing project link. Back up the
old note, check a diff, refresh the generated-region baseline and numeric report
binding after the content changes. Do not use a whole-card regeneration for this.

## Stable project links

Use an existing explicit project link when the profile provides one. Otherwise
propose a short display name and a fixed ASCII block ID in a small standalone
paragraph, for example `课题简称：<简称> ^project-a`. After user confirmation,
`[[文献笔记/_my_projects#^project-a|<简称>]]` remains independent of heading
numbering and title wording. Block IDs permit letters, digits and hyphens.

Before that approval, preserve existing `projects` (or leave it empty for new
cards), name the actual project in prose, and mark links pending. Do not fabricate
unresolvable short-name notes, silently edit the profile, or substitute a file-wide
alias for a project-specific anchor. Block references are Obsidian-specific.

The current card wall groups by the joined raw `projects` values. Block-specific
links remain separate groups, but their group headings can show the full link
rather than only its display alias. If short group headings are required, propose
a display-formula adjustment with the link plan; do not change the target links.

See [Obsidian's block links and display text documentation](https://help.obsidian.md/links).
