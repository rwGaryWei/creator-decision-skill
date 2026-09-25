# Validation status · 2026-09-25

This alpha distinguishes implemented behavior, deterministic checks, authored demonstrations, model runs and independent human evidence.

| Evidence | Current status | What it establishes |
|---|---|---|
| Python unit/integration checks | 69 tests passed locally on Windows, Python 3.12 | Tested report integrity, quote matching, snapshot/journal behavior, installation and evaluation arithmetic |
| Authored JSON/Markdown examples | 12, four domains × three stages | Intended output and schema compatibility; not model effectiveness |
| Installation smoke check | Temporary project copy and installed helper executed | Copy layout and helper operation; not host auto-discovery |
| Pilot comparison | 0 of 36 model jobs executed | No comparative conclusion |
| Formal study | Not frozen or run; 24 draft cases | Materials for review only |
| Independent reviewers | None confirmed | No independent scores or agreement statistics |
| Creator trials | None completed | No external usability or outcome claim |
| GitHub CI | Workflow prepared; remote execution not yet verified | No platform pass claimed until a run completes |

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
