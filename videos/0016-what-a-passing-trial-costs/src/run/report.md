## Eval Results

> Timestamp: 2026-11-11T08:43:23.513Z

### changelog [variant: haiku-high] [claude-haiku-5.5] (changelog.eval.yaml)

> **Environment**: 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| after-release | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ entry-in-new-unreleased 3/3 | 3/3 | 100.0% | 100.0% | 8.9s | 105,810 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, edit: 3</details> | ✅ |
| refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-nothing 3/3 | 3/3 | 100.0% | 100.0% | 6.4s | 41,623 | 2 | <details><summary>1 calls (median)</summary>total across 3 trials: skill: 3</details> | ✅ |
| security | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ under-security 3/3 | 3/3 | 100.0% | 100.0% | 8.1s | 105,856 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, edit: 3</details> | ✅ |
| two-changes | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ two-entries-in-place 3/3 | 3/3 | 100.0% | 100.0% | 9.4s | 106,316 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, edit: 3, bash: 2, glob: 2, view: 2</details> | ✅ |
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-an-entry 3/3<br>✅ no-made-up-number 3/3 | 3/3 | 100.0% | 100.0% | 7.8s | 105,439 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, edit: 3, glob: 2, view: 2, bash: 1, grep: 1</details> | ✅ |

> Model: claude-haiku-5.5 | Executor: copilot-sdk

<hr>

### changelog [variant: haiku-low] [claude-haiku-5.5] (changelog.eval.yaml)

> **Environment**: 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| after-release | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ entry-in-new-unreleased 3/3 | 3/3 | 100.0% | 100.0% | 6.0s | 84,312 | 4 | <details><summary>3 calls (median)</summary>total across 3 trials: skill: 3, edit: 3, bash: 2, glob: 1, view: 1</details> | ✅ |
| refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-nothing 3/3 | 3/3 | 100.0% | 100.0% | 5.4s | 41,439 | 2 | <details><summary>1 calls (median)</summary>total across 3 trials: skill: 3, bash: 1</details> | ✅ |
| security | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ under-security 3/3 | 3/3 | 100.0% | 100.0% | 6.3s | 105,185 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, edit: 3</details> | ✅ |
| two-changes | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ two-entries-in-place 3/3 | 3/3 | 100.0% | 100.0% | 6.3s | 105,328 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, edit: 3, glob: 2, view: 2, bash: 1</details> | ✅ |
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-an-entry 3/3<br>✅ no-made-up-number 3/3 | 3/3 | 100.0% | 100.0% | 6.9s | 105,201 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, edit: 3</details> | ✅ |

> Model: claude-haiku-5.5 | Executor: copilot-sdk

<hr>

### changelog [variant: terra-high] [gpt-5.6-terra] (changelog.eval.yaml)

> **Environment**: 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| after-release | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ entry-in-new-unreleased 3/3 | 3/3 | 100.0% | 100.0% | 8.1s | 48,847 | 4 | <details><summary>3 calls (median)</summary>total across 3 trials: view: 4, skill: 3, apply_patch: 3, glob: 2</details> | ✅ [^s3-1] |
| refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-nothing 3/3 | 3/3 | 100.0% | 100.0% | 7.2s | 36,245 | 3 | <details><summary>2 calls (median)</summary>total across 3 trials: skill: 3, view: 2</details> | ✅ |
| security | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ under-security 3/3 | 3/3 | 100.0% | 100.0% | 10.9s | 61,277 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: glob: 4, skill: 3, view: 3, apply_patch: 3</details> | ✅ |
| two-changes | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ two-entries-in-place 3/3 | 3/3 | 100.0% | 100.0% | 12.5s | 62,376 | 5 | <details><summary>6 calls (median)</summary>total across 3 trials: view: 5, sql: 4, skill: 3, apply_patch: 3, glob: 1</details> | ✅ |
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-an-entry 3/3<br>✅ no-made-up-number 3/3 | 3/3 | 100.0% | 100.0% | 11.9s | 61,297 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, apply_patch: 3, rg: 2</details> | ✅ [^s3-2] |

[^s3-1]: Trial durations: 7.9s – 12.0s
[^s3-2]: Trial durations: 8.3s – 13.1s


> Model: gpt-5.6-terra | Executor: copilot-sdk

<hr>

### changelog [variant: terra-low] [gpt-5.6-terra] (changelog.eval.yaml)

> **Environment**: 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| after-release | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ entry-in-new-unreleased 3/3 | 3/3 | 100.0% | 100.0% | 8.3s | 48,856 | 4 | <details><summary>3 calls (median)</summary>total across 3 trials: skill: 3, view: 3, apply_patch: 3</details> | ✅ |
| refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-nothing 3/3 | 3/3 | 100.0% | 100.0% | 6.2s | 23,808 | 2 | <details><summary>1 calls (median)</summary>total across 3 trials: skill: 3, glob: 1, view: 1</details> | ✅ |
| security | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ under-security 3/3 | 3/3 | 100.0% | 100.0% | 13.6s | 61,412 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, apply_patch: 3, rg: 2</details> | ✅ |
| two-changes | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ two-entries-in-place 3/3 | 3/3 | 100.0% | 100.0% | 9.9s | 61,322 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: view: 4, skill: 3, apply_patch: 3, glob: 2, sql: 2, bash: 1</details> | ✅ |
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ adds-an-entry 3/3<br>✅ no-made-up-number 3/3 | 3/3 | 100.0% | 100.0% | 9.8s | 61,163 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: view: 4, skill: 3, glob: 3, apply_patch: 3, sql: 2, rg: 2</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
