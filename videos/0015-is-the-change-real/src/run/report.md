## Eval Results

> Timestamp: 2026-11-11T08:00:18.615Z

### wording [variant: haiku-after] [claude-haiku-4.5] (wording.eval.yaml)

> **Environment**: 1 file · 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cache | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-66 3/3 | 3/3 | 100.0% | 100.0% | 27.8s | 75,381 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 6, skill: 3, edit: 3</details> | ✅ |
| dates | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-67 3/3 | 3/3 | 100.0% | 100.0% | 23.3s | 75,696 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 6, skill: 3, edit: 3</details> | ✅ |
| parser | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-49 3/3 | 3/3 | 100.0% | 100.0% | 22.8s | 75,584 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 6, skill: 3, edit: 3</details> | ✅ |

> Model: claude-haiku-4.5 | Judge: claude-sonnet-5.5 | Executor: copilot-sdk

<hr>

### wording [variant: haiku-before] [claude-haiku-4.5] (wording.eval.yaml)

> **Environment**: 1 file · 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cache | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry-before`</details> | `changelog-entry` (3×) | ❌ prompt "Begin your reason b…" 0/3<br>✅ cites-66 3/3 | 0/3 | 0.0% | 0.0% | 24.6s | 91,017 | 6 | <details><summary>5 calls (median)</summary>total across 3 trials: view: 6, skill: 3, bash: 3, edit: 3</details> | ❌ |
| parser | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry-before`</details> | `changelog-entry` (3×) | ❌ prompt "Begin your reason b…" 2/3<br>✅ cites-49 3/3 | 2/3 | 100.0% | 29.6% | 24.4s | 90,930 | 6 | <details><summary>5 calls (median)</summary>total across 3 trials: view: 8, skill: 3, edit: 3, bash: 1</details> | 🟡 [^s2-1] |
| dates | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry-before`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-67 3/3 | 3/3 | 100.0% | 100.0% | 24.4s | 90,714 | 6 | <details><summary>5 calls (median)</summary>total across 3 trials: view: 7, skill: 3, edit: 3, bash: 1</details> | ✅ |

[^s2-1]: ⚠️ Flaky (33% minority outcome). Grader breakdown: `prompt "Begin your reason b…"` passed 2/3 trials


> Model: claude-haiku-4.5 | Judge: claude-sonnet-5.5 | Executor: copilot-sdk

<hr>

### wording [variant: terra-after] [gpt-5.6-terra] (wording.eval.yaml)

> **Environment**: 1 file · 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cache | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-66 3/3 | 3/3 | 100.0% | 100.0% | 25.2s | 61,289 | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, apply_patch: 3, sql: 2</details> | ✅ |
| dates | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-67 3/3 | 3/3 | 100.0% | 100.0% | 20.9s | 48,832 | 4 | <details><summary>3 calls (median)</summary>total across 3 trials: skill: 3, view: 3, apply_patch: 3</details> | ✅ |
| parser | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ prompt "Begin your reason b…" 3/3<br>✅ cites-49 3/3 | 3/3 | 100.0% | 100.0% | 23.7s | 60,971 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: skill: 3, glob: 3, view: 3, apply_patch: 3</details> | ✅ |

> Model: gpt-5.6-terra | Judge: claude-sonnet-5.5 | Executor: copilot-sdk

<hr>

### wording [variant: terra-before] [gpt-5.6-terra] (wording.eval.yaml)

> **Environment**: 1 file · 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cache | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry-before`</details> | `changelog-entry` (2×) | — | — | — | — | — | — | 4 | <details><summary>3 calls (median)</summary>total across 3 trials: skill: 2, glob: 2, view: 2, apply_patch: 2</details> | ❌ [^s4-1] |
| dates | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry-before`</details> | `changelog-entry` (2×) | — | — | — | — | — | — | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: glob: 3, skill: 2, view: 2, apply_patch: 2, rg: 1</details> | ❌ [^s4-2] |
| parser | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `~/src/demo/practice/skills/changelog-entry-before`</details> | `changelog-entry` (2×) | — | — | — | — | — | — | 5 | <details><summary>5 calls (median)</summary>total across 3 trials: glob: 3, view: 3, skill: 2, sql: 2, apply_patch: 2</details> | ❌ [^s4-3] |

[^s4-1]: 1/3 trial(s) errored
[^s4-2]: 1/3 trial(s) errored
[^s4-3]: 1/3 trial(s) errored


> Model: gpt-5.6-terra | Judge: claude-sonnet-5.5 | Executor: copilot-sdk
