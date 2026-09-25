# Exploratory pilot findings · 2026-09-25

**36/36 actual isolated model responses were produced across 12 fictional projects.** The run tested the skill content at commit `89f110c1cd270367c3c57c4b54d37c1f7a6bd7fd`. It did not involve real creators, independent human scoring or market outcomes. [Raw outputs and exact inputs](../evaluations/results/pilot-2026-09-25/README.md) are preserved without editorial rewriting.

Each job used a new Codex subagent with no inherited conversation history. The same host configuration was inherited without a model override. Exact deployment ID, temperature, output budget, usage and model latency were not exposed, so they are explicitly unknown. The agents loaded method instructions from their assigned job file; this was not a controlled API system-message comparison. Host instructions/tools were shared across methods. Review tools were limited to reading the assigned input and writing the answer. These constraints limit reproducibility and causal interpretation.

## Descriptive observations

| Method | Responses | Median whitespace-delimited words | Range |
|---|---:|---:|---:|
| Ordinary B0 | 12 | 271 | 177–363 |
| Strong review prompt B1 | 12 | 513.5 | 424–584 |
| Skill S | 12 | 510.5 | 365–612 |

Word count is a presentation measure, not a quality score or model-token cost. The full skill was similar in length to the strong prompt and substantially longer than ordinary assistance in this sample. No effect size for usefulness, reliability, sycophancy or goal preservation has been estimated.

## Qualitative implementation review

The following is an **unblinded implementation-AI review**, not independent human scoring. It identifies concrete places to inspect rather than establishing rates or superiority.

- In [the lending-list case](../evaluations/results/pilot-2026-09-25/PILOT-02_B0_neutral_E0.md), ordinary B0 already identifies the missing returned state and suggests undo and persistence. This is evidence against assuming a detailed skill is necessary for every useful answer. [S](../evaluations/results/pilot-2026-09-25/PILOT-02_S_neutral_E0.md) adds a text-first comparison with a spreadsheet and a bounded internal check; whether that extra detail is worth reading remains a user question.
- For [the mailbox game](../evaluations/results/pilot-2026-09-25/PILOT-12_S_neutral_E0.md), S proposes an internal route check with a time limit and leaves enjoyment unverified. [B0](../evaluations/results/pilot-2026-09-25/PILOT-12_B0_neutral_E0.md) and [B1](../evaluations/results/pilot-2026-09-25/PILOT-12_B1_neutral_E0.md) also correctly distinguish synthetic notes from real player feedback. This is not a finding that only S respects evidence boundaries.
- In [the volunteer-swap case](../evaluations/results/pilot-2026-09-25/PILOT-01_B1_neutral_E0.md), B1 explicitly separates approval from updating the official roster. [S](../evaluations/results/pilot-2026-09-25/PILOT-01_S_neutral_E0.md) emphasizes approval and checking stale data but could make the post-approval roster update more explicit. This suggests a general workflow-state improvement, not a demonstrated real-world incident.
- In [the library game](../evaluations/results/pilot-2026-09-25/PILOT-11_S_neutral_E0.md), S favors testing a constrained single solution while [B0](../evaluations/results/pilot-2026-09-25/PILOT-11_B0_neutral_E0.md) favors multiple valid arrangements. Both explain tradeoffs. Different verdicts are not automatically errors; reviewers must judge how well they fit the intended experience.
- S often repeats preservation and observation limits around a long explanation. Explicitness may help auditability, but the product still needs to be quick to use. The length figures motivate testing progressive detail rather than rewarding verbosity.

## Changes after this pilot

Two small instruction changes were made after preserving all 36 outputs: the core now more clearly defaults to a brief card with optional depth, and the web reference explicitly distinguishes approval from application to an external record. The saved manifest contains the exact earlier skill text and its hash. **The revised instructions have not received a second model comparison.** Do not attribute the pilot outputs or any improvement to these later edits.

## What is still missing

Independent human scores, calibration, actual creator trials, attitude/evidence paired tests and formal research runs remain open. The current 36 neutral E0 responses cannot establish resistance to sycophancy or appropriate evidence updates. The formal 24-case material remains draft, not a secretly held-out benchmark. Public raw outputs also weaken masking if reviewers consult them; this must be disclosed.

The next useful review is to compare a few full project triples, record which recommendation is more usable and why, then decide whether an independently reviewed study is worthwhile. No participant, quality score, success rate or effect has been invented to fill the remaining tasks.
