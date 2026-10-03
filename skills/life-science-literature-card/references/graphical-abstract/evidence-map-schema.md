# Evidence map v2

Required only for complex full papers. The simplified story brief is sufficient
for simple papers and abstract-only triage cards.

```json
{
  "schema_version": "2.0",
  "paper_title_claim": "Title/abstract claim in plain language",
  "primary_endpoint": {"name": "", "result": "", "significant": null, "source": ["S1"]},
  "main_figures": ["Fig 1"],
  "modules": [{"id": "M1", "figure": "Fig 1", "level": "whole_body", "method": "CGM", "question": "", "finding": "", "evidence_strength": "exploratory", "source": ["S1"]}],
  "integrated_conclusion": "Sourced integration without invented mediation",
  "tension": "Primary endpoint versus broad title, or empty string",
  "sources": {"S1": {"locator": "Fig 1", "excerpt": "Optional checked source passage"}}
}
```

Every main figure has at least one module. Supplemental modules enter only when
the authors use them for the central claim. Levels: design, whole_body,
circulation, tissue, cellular, molecular, population, imaging, model.
Use primary/secondary only when that outcome role is known, otherwise exploratory.
No single specified endpoint uses name/result explaining that absence and
significant:null. `tension` must identify title wording stronger than primary
evidence; it is not resolved by hiding the primary endpoint. A cover selects 3–5
modules and lists omission/selection reasons in the story; the map stays complete.
