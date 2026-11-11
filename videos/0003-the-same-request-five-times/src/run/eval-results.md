## Eval Results

> Timestamp: 2026-11-11T04:11:03.606Z

### one-request [claude-haiku-4.5] (~/src/demo/practice/evals/one-request.eval.yaml)

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (5×) | ✅ mentions-the-command 5/5 | 5/5 | 100.0% | 100.0% | 9.5s | 74,343 | 5 | <details><summary>4 calls (median)</summary>total across 5 trials: view: 11, skill: 5, edit: 5</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### one-request [gpt-5.6-terra] (~/src/demo/practice/evals/one-request.eval.yaml)

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (5×) | ✅ mentions-the-command 5/5 | 5/5 | 100.0% | 100.0% | 13.6s | 73,965 | 6 | <details><summary>8 calls (median)</summary>total across 5 trials: glob: 12, view: 9, rg: 7, skill: 5, apply_patch: 5, bash: 2</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
