# Validation status · 2026-09-25

This alpha distinguishes implemented behavior, deterministic checks, authored demonstrations, model runs and independent human evidence. The [36-run pilot report](pilot-findings.md) links exact inputs and unedited outputs. Two subsequent instruction refinements are disclosed there and have not received a second model comparison. Skill Creator's official format validator also passed; this is a format check only.

Later owner-assisted development review is recorded in [owner review](owner-review.md). One web-case answer generated in the current development conversation received an owner judgment of useful but incomplete on market acceptance. The gap prompted a new instruction revision and an analysis supplement, not an independent trial or a validated fix. The original 36-run pilot remains unchanged.

The owner subsequently accepted the direction of the displayed market-analysis supplement. A video-case review received positive feedback with a request to include concrete platform/discovery planning. These current-conversation development reviews informed further instructions; they do not extend the isolated pilot count or establish market acceptance, campaign performance or independent usefulness.

| Evidence | Current status | What it establishes |
|---|---|---|
| Python unit/integration checks | 70 tests passed locally on Windows, Python 3.12 | Tested report integrity, quote matching, snapshot/journal behavior, installation and evaluation arithmetic |
| Authored JSON/Markdown examples | 12, four domains × three stages | Intended output and schema compatibility; not model effectiveness |
| Installation smoke check | Temporary project copy and installed helper executed | Copy layout and helper operation; not host auto-discovery |
| Pilot comparison | 36 of 36 isolated subagent responses saved | Exploratory outputs; no independently rated quality conclusion |
| Formal study | Not frozen or run; 24 draft cases | Materials for review only |
| Independent reviewers | None confirmed | No independent scores or agreement statistics |
| Creator trials | None completed | No external usability or outcome claim |
| GitHub CI | [Initial matrix passed](https://github.com/rwGaryWei/creator-decision-skill/actions/runs/36076599120) on Windows/Linux, Python 3.10/3.12 | Tool and package checks; later revisions require their own CI result |

Reproduce engineering checks from the repository root:

```sh
python -X utf8 -m unittest discover -s tests -v
python -X utf8 scripts/check_release.py
```

The local suite checks malformed data, duplicate references/keys, invalid timestamps and URLs, source content hashes, exact quotes, fictional-source labeling, non-observation of inaccessible artifacts, project boundaries, parent revisions, pending human decisions, explicit confirmation, modified decisions, report hash changes, journal corruption, locks and interrupted writes. Installation tests execute the copied helper. Evaluation tests use artificial fixture values solely to check run counts, masking and arithmetic.

**A passing suite does not certify the skill's advice.** A test deliberately shows that a quote may exist while failing to support a broad claim; semantic review remains necessary. File hashes do not authenticate the person who made a decision. Instructions about prompt injection have not been proven resistant by adversarial model trials.

Known limits and next checks:

- First-time creator usability and the quality of all four domains remain unmeasured.
- The text-only comparison cannot assess actual video/audio/interactive capability.
- Formal cases are public, authored drafts, not a protected holdout or a sample of real demand.
- No research output should report invented scores, favorable effect sizes, participant counts or significance.
- Public licensing and release status are recorded separately; an alpha upload does not satisfy the validated-v1 gate.

The task ledger keeps partially implemented and externally dependent work open. An implementation file, planned job or drafted report is not itself evidence that an experiment or human review happened.
