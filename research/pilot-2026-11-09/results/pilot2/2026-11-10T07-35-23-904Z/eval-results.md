## Eval Results

> Timestamp: 2026-11-10T07:36:55.274Z

### changelog-entry [claude-haiku-4.5] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml)

Does the agent record a change the way the skill asks?

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| change-list-sort | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ mentions-pr-52 3/3 | 3/3 | 100.0% | 100.0% | 9.8s | 74,267 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 6, skill: 3, edit: 3</details> | ✅ |
| fix-accented-search | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ mentions-pr-48 3/3 | 3/3 | 100.0% | 100.0% | 9.1s | 74,330 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 6, skill: 3, edit: 3</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### changelog-entry [mai-code-1.1-flash] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml)

Does the agent record a change the way the skill asks?

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| change-list-sort | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (2×) | ✅ mentions-pr-52 3/3 | 3/3 | 100.0% | 100.0% | 12.1s | 56,301 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: glob: 4, view: 4, edit: 3, skill: 2, grep: 1</details> | ✅ |
| fix-accented-search | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ mentions-pr-48 3/3 | 3/3 | 100.0% | 100.0% | 13.5s | 56,057 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: glob: 4, view: 4, skill: 3, edit: 3</details> | ✅ |

> Model: mai-code-1.1-flash | Executor: copilot-sdk

<hr>

### changelog-entry [gpt-5.6-terra] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml)

Does the agent record a change the way the skill asks?

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| change-list-sort | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ mentions-pr-52 3/3 | 3/3 | 100.0% | 100.0% | 8.1s | 60,185 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: glob: 4, skill: 3, view: 3, apply_patch: 3, rg: 1</details> | ✅ |
| fix-accented-search | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ mentions-pr-48 3/3 | 3/3 | 100.0% | 100.0% | 7.7s | 48,488 | 4 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, view: 3, glob: 3, apply_patch: 3, rg: 1</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
