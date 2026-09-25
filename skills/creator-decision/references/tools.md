# Local tools

Python 3.10+; standard library only. No network, model API, telemetry, or account required. Paths below assume the repository root. These commands work with authored examples; do not mistake their contents for real audience evidence.

```sh
python skills/creator-decision/scripts/decision.py validate examples/game/prototype.json
python skills/creator-decision/scripts/decision.py render examples/game/prototype.json --output card.md
python skills/creator-decision/scripts/decision.py save examples/game/prototype.json --root private-work
```

`render` refuses an existing output. `save` preserves the original JSON bytes and refuses overwriting an existing report, including an identical report. Keep `private-work` outside any public repository, or ensure it stays ignored. Sources can contain confidential material even when a report seems harmless.

Use the project, report and recommendation IDs in your report to inspect decisions:

```sh
python skills/creator-decision/scripts/decision.py status --root private-work --project PROJECT --report REPORT
```

Only after the user actually decides, record their statement:

```sh
python skills/creator-decision/scripts/decision.py decide --root private-work --project PROJECT --report REPORT --recommendation RECOMMENDATION --decision defer --statement "I want to review the prototype first." --confirmed-human
```

Replace placeholders with real IDs. Never use this example statement as a user's decision. Choices: `accept`, `modify`, `reject`, `defer`. `modify` also needs `--replacement`. The flag records the caller's assertion of confirmation; it does not authenticate a human. This is a local journal, not an approval security system.

For a reassessment, assign a new report ID, increase its revision, and set `parent_report_id`. Save the parent before the child. Run `diff OLD.json NEW.json` to inspect structural changes and explain separately which new evidence or changed goal justifies the update. Human decisions bind to exact report bytes; they do not transfer to a revised report.

If a process stops while writing, existing committed files remain. A `.write.lock` may remain after a crash. Check that no writer is active and back up the directory before manually removing only that lock. Do not automatically discard it. File hashes detect ordinary changes; someone able to rewrite all files can also rewrite the hash chain. Do not use this as tamper-proof storage.

Validation checks object relationships, types, source hashes and literal quote presence. It cannot establish that a source is truthful, that a quote supports an interpretation, or that an experiment will predict demand. An error is not permission to invent missing information. If Python is unavailable, use the Markdown card and explicitly leave machine validation and persistence unchecked.
