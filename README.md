# Creator Decision

**Decide what to make next, what to improve, and what to test before investing more.**

A reusable AI skill for people making websites, tools, videos, short dramas, and games with AI. Bring an idea, a draft, or feedback. Get a focused recommendation, what is worth preserving, the assumptions that matter, and a practical next experiment.

[中文说明](README.zh-CN.md) · [Start here](docs/quickstart.md) · [Examples](examples/README.md) · [Current evidence](docs/validation.md) · [64-task progress](docs/task-progress.md)

**Status: 0.1.0-alpha.** Instructions and local tooling are implemented. Authored examples illustrate intended behavior; they are not a user study or evidence that this skill improves decisions. Independent model comparisons and creator trials remain outstanding. Licensing is awaiting the repository owner's decision; see [licensing status](docs/licensing.md).

## A useful review changes a decision

Suppose you want to generate hundreds of game characters. The relevant question may be whether three characters create distinct, consequential relationships. This skill should help you preserve that experience, inspect what exists, and decide whether to deepen those relationships, expand the cast, or run a small playtest. It should explain what would change its advice.

Sometimes the right recommendation is **continue or expand**. Sometimes it is change, narrow, test, or pause. Agreement and criticism are both easy; a justified next step is the aim. Creative expression, enjoyment, learning, portfolio value, and commercial goals can each be valid.

## Use it

1. Download or clone this repository.
2. Copy the entire `skills/creator-decision` folder into your project's `.agents/skills/` directory for Codex. Alternatively, run the optional installer below.
3. Open that project in your assistant and explicitly request the skill:

```text
Use $creator-decision to review my idea.
I want to make a quiet AI-assisted short film about leaving home.
I have a script, two weekends, and no audience feedback yet.
I want to keep its restrained style. Help me decide what to test first.
```

Optional installer (Python 3.10+):

```sh
python scripts/install.py --project /absolute/path/to/your/project
```

The installer refuses to replace an existing skill. Host discovery and capabilities vary: [installation and support limits](docs/quickstart.md). For an assistant without skill support, attach or provide the skill and relevant reference files explicitly; that is manual use, not verified native integration. No model API key is needed by these local tools. Your chosen assistant provides the model and may have its own subscription or costs.

## What you receive

- A short decision card: recommendation, investment affected, and what to preserve.
- Reasons linked to observations, sources, or clearly labeled assumptions.
- Concrete alternatives with tradeoffs, rather than a universal score.
- One feasible experiment and conditions for changing the recommendation.
- A reassessment when new information arrives; the creator retains the decision.

| Work | What the review examines |
|---|---|
| Websites / tools | The task, existing workaround, setup effort, correction, recovery, repeat usefulness |
| Video | Viewing promise, comprehension, progression, payoff, audiovisual constraints |
| Short drama | Character intention, causal choices, scene consequences, continuity |
| Games | Core loop, meaningful choices, feedback, challenge, production scope |

AI involvement is assessed through generation, selection, correction, consistency and maintenance costs. The AI label alone is not a quality verdict. The skill cannot predict sales or virality, certify originality or rights, detect AI reliably, or turn simulated people into real audience evidence.

## Optional local tools

The conversation is the main experience. Python tools add report checks and versioned records:

```sh
python skills/creator-decision/scripts/decision.py validate examples/game/prototype.json
python skills/creator-decision/scripts/decision.py render examples/game/prototype.json --output card.md
python -m unittest discover -s tests -v
python scripts/check_release.py
```

These use the Python standard library. They make no network or model requests and collect no telemetry. They validate structure and literal quote presence, not truth or semantic support. The local human-decision journal records explicit statements and binds them to report bytes; it is not identity verification. See [tools](skills/creator-decision/references/tools.md).

## Evaluation and contribution

The repository includes 12 development scenarios, 12 different pilot scenarios, 24 draft test scenarios, and a reproducible evaluation preparation/analysis tool. Scenarios are fictional text materials. No simulated response is counted as an actual experiment. Read the [protocol](evaluations/PROTOCOL.md) before interpreting any numbers.

Useful contributions include a reproducible failure, an example where justified enthusiasm should survive review, or a domain-specific improvement. See [CONTRIBUTING](CONTRIBUTING.md). Do not upload private chats or someone else's full creative work. A star can signal interest, but repeat use and decisions improved are the outcomes this project still needs to measure.
