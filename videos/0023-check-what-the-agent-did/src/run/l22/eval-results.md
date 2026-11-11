## Eval Results

> Timestamp: 2026-11-11T16:52:49.239Z

### release [claude-haiku-4.5] (~/src/demo/practice/evals/release.eval.yaml)

> **Environment**: 2 files · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| since-last-release | <details><summary>2 files · 2 commands · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`, `../tools/list-merged.mjs` → `tools/list-merged.mjs`<br/>Commands: `mkdir -p release`, `node tools/list-merged.mjs &gt; release/merged.txt`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ❌ every-change-handled 2/5 | 2/5 | 100.0% | 1.0% | 13.4s | 76,312 | 5 | <details><summary>6 calls (median)</summary>total across 5 trials: view: 18, edit: 5, skill: 3, bash: 2</details> | 🟡 [^s1-1] |

[^s1-1]: ⚠️ Flaky (40% minority outcome). Grader breakdown: `every-change-handled` passed 2/5 trials


> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### release [gpt-5.6-terra] (~/src/demo/practice/evals/release.eval.yaml)

> **Environment**: 2 files · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| since-last-release | <details><summary>2 files · 2 commands · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`, `../tools/list-merged.mjs` → `tools/list-merged.mjs`<br/>Commands: `mkdir -p release`, `node tools/list-merged.mjs &gt; release/merged.txt`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (5×) | ✅ every-change-handled 5/5 | 5/5 | 100.0% | 100.0% | 11.0s | 61,968 | 5 | <details><summary>5 calls (median)</summary>total across 5 trials: view: 13, skill: 5, apply_patch: 5</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
