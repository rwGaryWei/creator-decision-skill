# Contributing

Start with a small, reproducible problem: the creator's goal, domain/stage, supplied material, host/model, skill version, actual output, expected behavior and why the difference matters. Remove names, private chats, keys and third-party creative material you cannot share. A short original fictional reproduction is welcome when clearly labeled.

Useful work includes preserving a noncommercial creative goal, improving a domain-specific experiment, finding an invented observation, or making a justified positive recommendation clearer. Do not optimize for a fixed number of criticisms or a universal numeric verdict.

Before proposing a change:

1. Explain the decision it improves and the tradeoff.
2. Modify the smallest relevant instruction/reference/tool.
3. Run `python -m unittest discover -s tests -v` and `python scripts/check_release.py` for tool/data changes.
4. For behavioral changes, preserve the before/after prompt, exact host/model and output. Do not call authored examples independent runs.
5. Add or update an appropriate development case. Formal test cases must not become a hidden tuning set.

Keep English and Chinese promises consistent. Actual observation and evidence limits must survive wording improvements. Public material must remain free of participant identifiers and confidential source captures.

Licensing is currently pending owner selection; please discuss proposed contributions before sending work that assumes a particular inbound/outbound license. No contributor agreement or authorship claim is inferred from filing an issue.

Maintenance is best effort. There is no hidden telemetry or automatic outreach. Stars and downloads are signals of interest, not evidence of benefit.
