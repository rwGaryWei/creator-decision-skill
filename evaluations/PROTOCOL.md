# Evaluation protocol draft · manual-text-v1

**Formal study status: draft, not frozen or executed.** A separate [36-run exploratory pilot](../docs/pilot-findings.md) has been completed with disclosed host-level limitations. No model effect, user benefit or research approval is claimed. All supplied scenarios are fictional text materials; none is a real participant record. Review and timestamp this protocol, exact cases, prompts, skill version, run settings and analysis plan before formal runs.

## Questions and unit of analysis

Primary question: does the skill improve **actionability of the next decision** relative to ordinary assistance and a strong review prompt? Secondary questions: preservation of creative goals, evidence discipline, domain specificity and uncertainty. Exploratory paired questions: does confidence framing distort factual advice, and does decision-relevant new evidence produce an appropriate update?

An independent unit is a **project scenario**, not each response. A 432-response design still has 24 project scenarios. The cases are authored by the implementation process and publicly visible; they are not secret, naturally sampled, or statistically representative. Do not tune the skill against formal test outputs and then report those same outputs as untouched evaluation. If tuning occurs, version the test set and start a new study or label the result exploratory.

## Materials

- Development: 12 projects, four domains × three stages. Available to implementation and calibration.
- Pilot: 12 new projects, same coverage, not renamed development variants. Used to find instruction, runtime and rubric problems.
- Formal candidates: 24 projects, six per domain and two per stage per domain. Text only; all have E0 and a decision-relevant E1 update. Drafts need independent review and a recorded freeze before use.

`review_anchor` fields are reviewer material and must not be sent to model conditions. They describe desirable reasoning, not a single mandatory verdict. A plausible alternative recommendation can score well if evidence, creative intent and tradeoffs justify it.

## Conditions

| Method | Input |
|---|---|
| B0 | Brief ordinary assistance instruction |
| B1 | Strong review prompt with goals, audience, strengths, alternatives, evidence, uncertainty, AI costs and an experiment |
| S | Core skill, all reference files and decision-card template |

`harness.py` contains exact condition prompts. All methods receive identical case material within a condition. Stance wording changes only the creator's confidence (neutral/confident/doubtful), not goal or facts. E1 adds the authored new evidence explicitly. Even after E1, the case remains fictional: conclusions apply within the scenario, not to real demand.

The first protocol is **text-only, no tools or network**. Use the same model version, host, reasoning settings and maximum output budget in fresh isolated conversations. Loading all S references makes the treatment reproducible but differs from native selective-loading skill use. Input length and cost differ; report them. Do not describe this experiment as a test of web research, video viewing, interactive gameplay or host auto-discovery.

## Run counts and selection

Pilot: 12 projects × 3 methods × neutral E0 = **36** planned jobs.

Full: 24 × 3 methods × 3 stances × 2 evidence states = **432** jobs. Attitude comparisons: neutral versus confident and neutral versus doubtful within each evidence state (288 pairs across methods). Evidence comparisons: E0 versus E1 within each stance (216 pairs).

Reduced, selected **before** outcomes: neutral E0 for all 24 projects (72 jobs), confident/doubtful E0 for a balanced 12-project subset (72), and neutral E1 for that subset (36) = **180** jobs. The current deterministic subset is the first three candidate IDs per domain. This balances domain but not every stage; generalization of paired findings is correspondingly limited. Attitude comparisons: 72 pairs; evidence comparisons: 36.

The generator uses seed 1729 and retains the randomized job order. Do not choose the subset after seeing favorable outputs. Fix the design, provider and spending limit before execution. No paid API, automatic runner or model key is configured by this repository.

## Run procedure and failures

1. Review/freeze materials, prompts and skill commit. Save a manifest privately.
2. Run each job in a fresh context with its exact system material and user prompt. Record model ID/version, host/version, settings, start/end timestamps, input hash, full raw output and provenance. If the host does not expose a field, state that explicitly; unknown timestamps stay null with a `timing_note`. Do not infer latency or exact deployment reproducibility from unavailable metadata.
3. Preserve failed attempts with error, elapsed time and any usage/cost returned. One retry is allowed only for transport/availability failures, with a new attempt record linked to the original. A substantive poor response is a result, not a reason to retry.
4. Do not edit or clean responses before scoring. Record truncation and missing outputs. Never fill missing scores with zero.
5. Stop at the predeclared budget; report completed/planned counts and selection order. Do not quietly replace a 432 plan with whichever outputs were cheapest or best.

Example commands (outputs must not already exist):

```sh
python evaluations/harness.py prepare evaluations/cases/pilot.json --design pilot --output private-evaluations/pilot-manifest.json
python evaluations/harness.py prepare evaluations/cases/test-candidates.json --design reduced --output private-evaluations/formal-draft-manifest.json
python evaluations/harness.py ingest private-evaluations/pilot-manifest.json private-evaluations/one-run.json --output private-evaluations/verified-run.json
```

The tool validates a caller-supplied run record; it cannot prove a model executed it. Preserve host exports or provider receipts privately as provenance. Test fixtures in unit tests are not run results. A manifest hash permits later comparison, not proof of preregistration. Do not publish keys, private participant materials or raw exports without permission.

## Scoring

Use [rubric.md](rubric.md). Rate each dimension 0–2 with a quotation/location and explanation. The primary metric is actionability in neutral E0, aggregated within project and method. A severe fabricated observation or invented source is also a critical-error flag, not hidden inside a favorable average.

Calibrate on development material only, including actual attitude/evidence pairs produced from development cases. A neutral-only pilot cannot calibrate paired framing/update judgments. Keep author, model and independent-human ratings in separate analyses. Model scores are not independent human judgments. Record reviewer time for single outputs, stance pairs and evidence pairs separately; the creator's available hours do not include independent reviewer labor.

For independent review, seek at least two people who were not the authoring agent or sole implementation owner. Record expertise, conflicts and consent. Do not recruit or contact them without authorization. Hide method labels using the packet tool and keep the mapping separately. Output style may reveal the method. Do not rewrite outputs to make blinding appear stronger. Prepare stance/evidence pair packets using the private mapping and preserve condition differences needed to judge the update.

Record original independent ratings before any adjudication. Report agreement before consensus, disagreements and the rule used to resolve them. A proposed readiness check is no unresolved rubric-definition disagreement on calibration items; this is a workflow choice, not a statistically validated reliability threshold.

## Analysis and reporting

`analyze` computes descriptive S−B0 and S−B1 actionability differences on complete neutral E0 project triples, averaging reviewer ratings within each project/method. It excludes incomplete triples explicitly and reports counts. It does not calculate significance or prove effectiveness. Use sensitivity analyses for missing cases and rater differences before interpreting a result. With only 24 purposive scenarios, any inferential extension needs a justified analysis plan; do not treat repeated conditions as independent samples.

Report all dimensions, critical errors, paired framing/update judgments, denominators, missing outputs, failures, costs and reviewer time, including unfavorable cases. Distinguish unchanged advice that correctly reflects irrelevant evidence from failure to update; changed advice due to a changed goal is not sycophancy. List authoring bias, text-only scope, shared model, imperfect blinding, public cases, sample size and no market-outcome ground truth.

No final effect conclusion is warranted until actual runs and the appropriate review exist. Academic use additionally requires the applicable institution's research process to be checked before participant recruitment; this document is not ethics approval.
