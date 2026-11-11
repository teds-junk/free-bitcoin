## Eval Results

> Timestamp: 2026-11-10T14:57:39.753Z

### loading [claude-haiku-4.5] (evals/loading.eval.yaml)

> **Environment**: 1 file · 3 skills

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skip-question | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | — | — | — | — | — | — | — | 1.5 | <details><summary>1 calls (median)</summary>total across 2 trials: bash: 1, view: 1</details> | ❌ [^s1-1] |
| load-no-keyword | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` | ❌ skill-invocation requires changelog-ent… 1/2 | 1/2 | 100.0% | 25.0% | 9.8s | 67,318.5 | 4.5 | <details><summary>3.5 calls (median)</summary>total across 2 trials: view: 3, edit: 2, bash: 1, skill: 1</details> | 🟡 [^s1-2] |
| load-indirect | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 12.5s | 75,789 | 5 | <details><summary>5 calls (median)</summary>total across 2 trials: view: 4, bash: 2, skill: 2, edit: 2</details> | ✅ |
| load-plain | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 11.1s | 83,211 | 5.5 | <details><summary>5 calls (median)</summary>total across 2 trials: view: 5, skill: 2, edit: 2, bash: 1</details> | ✅ |
| skip-commit | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `commit-message` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 6.6s | 29,363 | 2 | <details><summary>1 calls (median)</summary>total across 2 trials: skill: 2</details> | ✅ |
| skip-release-notes | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 11.3s | 74,331 | 5 | <details><summary>4 calls (median)</summary>total across 2 trials: view: 4, bash: 2, skill: 2</details> | ✅ |

[^s1-1]: 1/2 trial(s) errored
[^s1-2]: ⚠️ Flaky (50% minority outcome). Grader breakdown: `skill-invocation requires changelog-ent…` passed 1/2 trials


> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### loading [gpt-5.6-terra] (evals/loading.eval.yaml)

> **Environment**: 1 file · 3 skills

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skip-question | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | — | — | — | — | — | — | — | 1.5 | <details><summary>1 calls (median)</summary>total across 2 trials: glob: 1, view: 1</details> | ❌ [^s2-1] |
| load-indirect | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 10.8s | 60,963 | 5 | <details><summary>4.5 calls (median)</summary>total across 2 trials: glob: 3, skill: 2, view: 2, apply_patch: 2</details> | ✅ |
| load-no-keyword | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 13.1s | 54,868 | 4.5 | <details><summary>3.5 calls (median)</summary>total across 2 trials: view: 3, skill: 2, apply_patch: 2</details> | ✅ [^s2-2] |
| load-plain | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.9s | 48,712.5 | 4 | <details><summary>3.5 calls (median)</summary>total across 2 trials: skill: 2, view: 2, apply_patch: 2, glob: 1</details> | ✅ |
| skip-commit | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `commit-message` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 4.6s | 23,594.5 | 2 | <details><summary>1 calls (median)</summary>total across 2 trials: skill: 2</details> | ✅ |
| skip-release-notes | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.9s | 47,838 | 4 | <details><summary>3.5 calls (median)</summary>total across 2 trials: glob: 3, skill: 2, view: 2</details> | ✅ |

[^s2-1]: 1/2 trial(s) errored
[^s2-2]: Trial durations: 9.6s – 16.6s


> Model: gpt-5.6-terra | Executor: copilot-sdk
