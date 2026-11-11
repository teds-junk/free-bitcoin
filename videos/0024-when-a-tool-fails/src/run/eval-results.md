## Eval Results

> Timestamp: 2026-11-11T17:51:20.120Z

### release [claude-haiku-4.5] (~/src/demo/practice/evals/release.eval.yaml)

> **Environment**: 1 file · 1 skill

#### ⚠️ Warnings

- `[stimuli-filtered] Running 1 of 2 stimuli (1 filtered by tags)` at ~/src/demo/practice/evals/release.eval.yaml
- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| tracker-down | <details><summary>2 files · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`, `fixtures/release/list-merged.mjs` → `tools/list-merged.mjs`<br/>Skills: `../skills/changelog-entry`</details> | ✅ tries-the-tool 3/3<br>✅ writes-nothing 3/3<br>✅ stops-retrying 3/3<br>✅ says-why 3/3 | 3/3 | 100.0% | 100.0% | 30.9s | 154,982 | 10 | <details><summary>10 calls (median)</summary>total across 3 trials: bash: 17, view: 12</details> | ✅ |

> Model: claude-haiku-4.5 | Judge: claude-sonnet-5.5 | Executor: copilot-sdk

<hr>

### release [gpt-5.6-terra] (~/src/demo/practice/evals/release.eval.yaml)

> **Environment**: 1 file · 1 skill

#### ⚠️ Warnings

- `[stimuli-filtered] Running 1 of 2 stimuli (1 filtered by tags)` at ~/src/demo/practice/evals/release.eval.yaml
- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| tracker-down | <details><summary>2 files · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`, `fixtures/release/list-merged.mjs` → `tools/list-merged.mjs`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ tries-the-tool 3/3<br>✅ writes-nothing 3/3<br>✅ stops-retrying 3/3<br>✅ says-why 3/3 | 3/3 | 100.0% | 100.0% | 22.2s | 49,071 | 4 | <details><summary>4 calls (median)</summary>total across 3 trials: bash: 6, skill: 3, view: 2</details> | ✅ |

> Model: gpt-5.6-terra | Judge: claude-sonnet-5.5 | Executor: copilot-sdk
