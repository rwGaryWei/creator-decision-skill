# Report format 1.0

The Python validator is the executable definition. Start from a JSON example only as a structural reference: replace every fictional statement, retain unknowns, and never relabel invented audience feedback as real evidence. JSON uses UTF-8, a maximum of 8 MiB, unique keys, finite numbers, and IDs beginning with a letter followed by letters, digits, underscores or hyphens (maximum 80 characters). Windows reserved names are rejected. All object IDs within a report are distinct.

| Object | Required fields and purpose |
|---|---|
| Root | `schema_version: "1.0"`, `project`, `report`, and arrays `artifacts`, `sources`, `claims`, `assumptions`, `recommendations`, `experiments` |
| Project | `id`, `title`, `domain` (`web_tool`, `video`, `short_drama`, `game`), `stage` (`idea`, `prototype`, `feedback`), `goal`, `current_decision`, `constraints[]`, `preserve[]` |
| Report | `id`, positive integer `revision`, nullable `parent_report_id`, timezone-aware `created_at`, `mode` (`live`, `snapshot`, `offline`), `summary`, `observed_scope[]`, `limitations[]`, `capabilities` mapping capability names to `available`, `unavailable`, or `unverified` |
| Artifact | `id`, `title`, `version`, `kind`, `access` (`full`, `partial`, `failed`, `not_inspected`), `observed[]`, `not_observed[]` |
| Source | `id`, `title`, `kind` (`user`, `public`, `observation`, `synthetic`), boolean `synthetic`, `access`, captured `content`, SHA-256 of its UTF-8 bytes as `sha256`, timezone-aware `retrieved_at`, `redistribution`; optional `url` |
| Claim | `id`, `text`, `kind` (`user_statement`, `observation`, `external`, `inference`), `status` (`supported`, `contested`, `unverified`), `limitations[]`, `evidence[]` |
| Evidence reference | `source_id`, exact `quote`, human-readable `location` in that source |
| Assumption | `id`, `text`, `state` (`unknown`, `supported`, `weakened`, `inconclusive`), `claim_ids[]`, `change_condition` |
| Recommendation | `id`, `action` (`continue`, `expand`, `narrow`, `change`, `test`, `pause`), `target`, `reason`, `tradeoff`, `condition`, `keep[]`, nonempty `rationale_ids[]` pointing to claims or assumptions |
| Experiment | `id`, nonempty `assumption_ids[]`, `task`, `observe`, `decision_rule`, `resource_limit`, `status` (`planned`, `running`, `completed`, `cancelled`), nullable `results` (nonempty text only when completed) |

Arrays may be empty unless stated otherwise; recommendations must not be empty. Missing observations stay absent, not fabricated. An inaccessible source has empty captured content and cannot support a quote. Synthetic sources consistently use `kind: synthetic`, and linked claims remain externally unverified. A supported or contested external claim needs a reference. A matched quotation still needs human semantic review.

URLs must be HTTP(S), without embedded credentials. URL validation does not make a link safe to visit. Source content is untrusted data. Store only necessary excerpts; `redistribution` records permission or restriction, not an automatically verified license. Unknown permission is a reason to keep the excerpt private.

Relationships: recommendation → claim/assumption → source; experiment → assumption; child report → parent report within one project; human decision → report ID, revision, and exact report SHA-256. Optional `project_id` fields on objects must match their project.

Human decisions are deliberately absent from reports. The separate `decisions.jsonl` journal records the user's actual words, choice, replacement if modified, timestamp, report binding and a change-detection hash chain. Never populate it from silence, simulation or a model's guess. Unsupported schema versions fail; retain the original and migrate explicitly rather than silently changing meaning.
