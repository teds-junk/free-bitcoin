## Eval Results

> Timestamp: 2026-11-11T06:10:32.525Z

### loading [claude-haiku-4.5] (~/src/demo/practice/evals/loading.eval.yaml)

> **Environment**: 1 file · 3 skills

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| load-indirect | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 11.8s | 75,817.5 | 5 | <details><summary>4.5 calls (median)</summary>total across 2 trials: view: 4, skill: 2, edit: 2, bash: 1</details> | ✅ |
| load-no-keyword | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 10.8s | 68,038 | 4.5 | <details><summary>4 calls (median)</summary>total across 2 trials: view: 4, skill: 2, edit: 2</details> | ✅ |
| load-plain | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 10.8s | 82,771.5 | 5.5 | <details><summary>5 calls (median)</summary>total across 2 trials: view: 4, bash: 2, skill: 2, edit: 2</details> | ✅ |
| skip-commit | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `commit-message` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 7.9s | 29,512 | 2 | <details><summary>1 calls (median)</summary>total across 2 trials: skill: 2</details> | ✅ |
| skip-question | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | — | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 7.1s | 44,245.5 | 3 | <details><summary>2 calls (median)</summary>total across 2 trials: view: 3, bash: 1</details> | ✅ |
| skip-release-notes | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 8.2s | 59,310.5 | 4 | <details><summary>3 calls (median)</summary>total across 2 trials: view: 4, skill: 2</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### loading [gpt-5.6-terra] (~/src/demo/practice/evals/loading.eval.yaml)

> **Environment**: 1 file · 3 skills

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skip-release-notes | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` | — | — | — | — | — | — | 2 | <details><summary>1.5 calls (median)</summary>total across 2 trials: skill: 1, glob: 1, view: 1</details> | ❌ [^s2-1] |
| load-indirect | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 8.0s | 60,904 | 5 | <details><summary>4.5 calls (median)</summary>total across 2 trials: glob: 3, skill: 2, view: 2, apply_patch: 2</details> | ✅ |
| load-no-keyword | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 10.0s | 67,774.5 | 5.5 | <details><summary>6 calls (median)</summary>total across 2 trials: glob: 3, view: 3, skill: 2, sql: 2, apply_patch: 2</details> | ✅ |
| load-plain | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.5s | 48,596 | 4 | <details><summary>3 calls (median)</summary>total across 2 trials: skill: 2, view: 2, apply_patch: 2</details> | ✅ |
| skip-commit | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `commit-message` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 4.4s | 23,601 | 2 | <details><summary>1 calls (median)</summary>total across 2 trials: skill: 2</details> | ✅ |
| skip-question | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 8.3s | 41,950 | 3.5 | <details><summary>3 calls (median)</summary>total across 2 trials: glob: 3, skill: 1, rg: 1, view: 1</details> | ✅ |

[^s2-1]: 1/2 trial(s) errored


> Model: gpt-5.6-terra | Executor: copilot-sdk
