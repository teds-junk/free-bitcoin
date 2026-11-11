## Eval Results

> Timestamp: 2026-11-11T17:27:49.341Z

### release [claude-haiku-4.5] (~/src/demo/practice/evals/release.eval.yaml)

> **Environment**: 2 files · 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| since-last-release | <details><summary>2 files · 2 commands · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`, `../tools/list-merged.mjs` → `tools/list-merged.mjs`<br/>Commands: `mkdir -p release`, `node tools/list-merged.mjs &gt; release/merged.txt`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ❌ every-change-handled 1/3<br>✅ reads-the-list 3/3<br>✅ never-commits 3/3<br>✅ no-loop 3/3<br>❌ loads-the-skill 1/3 | 1/3 | 100.0% | 3.7% | 13.7s | 90,870 | 6 | <details><summary>6 calls (median)</summary>total across 3 trials: view: 12, edit: 3, skill: 1</details> | 🟡 [^s1-1] |

[^s1-1]: ⚠️ Flaky (33% minority outcome). Grader breakdown: `every-change-handled` passed 1/3 trials, `loads-the-skill` passed 1/3 trials


> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### release [gpt-5.6-terra] (~/src/demo/practice/evals/release.eval.yaml)

> **Environment**: 2 files · 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| since-last-release | <details><summary>2 files · 2 commands · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`, `../tools/list-merged.mjs` → `tools/list-merged.mjs`<br/>Commands: `mkdir -p release`, `node tools/list-merged.mjs &gt; release/merged.txt`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ every-change-handled 3/3<br>✅ reads-the-list 3/3<br>✅ never-commits 3/3<br>✅ no-loop 3/3<br>✅ loads-the-skill 3/3 | 3/3 | 100.0% | 100.0% | 12.7s | 62,488 | 5 | <details><summary>6 calls (median)</summary>total across 3 trials: view: 9, skill: 3, apply_patch: 3, sql: 2, glob: 1</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
