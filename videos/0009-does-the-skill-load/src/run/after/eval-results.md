## Eval Results

> Timestamp: 2026-11-11T06:16:37.108Z

### loading [claude-haiku-4.5] (~/src/demo/practice/evals/loading.eval.yaml)

> **Environment**: 1 file · 3 skills

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| load-indirect | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 14.8s | 107,672 | 7 | <details><summary>6.5 calls (median)</summary>total across 2 trials: view: 5, bash: 4, skill: 2, edit: 2</details> | ✅ |
| load-no-keyword | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.5s | 75,605.5 | 5 | <details><summary>4 calls (median)</summary>total across 2 trials: view: 4, skill: 2, edit: 2</details> | ✅ |
| load-plain | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.5s | 75,583.5 | 5 | <details><summary>4.5 calls (median)</summary>total across 2 trials: view: 4, skill: 2, edit: 2, bash: 1</details> | ✅ |
| skip-commit | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `commit-message` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 6.6s | 29,437.5 | 2 | <details><summary>1 calls (median)</summary>total across 2 trials: skill: 2</details> | ✅ |
| skip-question | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | — | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 6.4s | 44,091 | 3 | <details><summary>2 calls (median)</summary>total across 2 trials: view: 3, glob: 1</details> | ✅ |
| skip-release-notes | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 8.5s | 59,494.5 | 4 | <details><summary>3 calls (median)</summary>total across 2 trials: view: 3, skill: 2, bash: 1</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### loading [gpt-5.6-terra] (~/src/demo/practice/evals/loading.eval.yaml)

> **Environment**: 1 file · 3 skills

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| skip-question | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry`, `release-notes` | ❌ skill-invocation forbids changelog-ent… 1/2 | 1/2 | 100.0% | 25.0% | 9.5s | 54,379 | 4.5 | <details><summary>3.5 calls (median)</summary>total across 2 trials: skill: 2, glob: 2, view: 2, rg: 1</details> | 🟡 [^s2-1] |
| load-indirect | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.4s | 55,080 | 4.5 | <details><summary>4 calls (median)</summary>total across 2 trials: skill: 2, view: 2, apply_patch: 2, glob: 2</details> | ✅ |
| load-no-keyword | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 8.8s | 61,177.5 | 5 | <details><summary>4.5 calls (median)</summary>total across 2 trials: glob: 3, skill: 2, view: 2, apply_patch: 2</details> | ✅ |
| load-plain | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `changelog-entry` (2×) | ✅ skill-invocation requires changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 9.0s | 54,996 | 4.5 | <details><summary>4 calls (median)</summary>total across 2 trials: skill: 2, view: 2, apply_patch: 2, glob: 1, rg: 1</details> | ✅ |
| skip-commit | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `commit-message` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 5.0s | 23,683 | 2 | <details><summary>1 calls (median)</summary>total across 2 trials: skill: 2</details> | ✅ [^s2-2] |
| skip-release-notes | <details><summary>1 file · 3 skills</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`, `../skills/commit-message`, `../skills/release-notes`</details> | `release-notes` (2×) | ✅ skill-invocation forbids changelog-ent… 2/2 | 2/2 | 100.0% | 100.0% | 8.4s | 42,090 | 3.5 | <details><summary>2.5 calls (median)</summary>total across 2 trials: skill: 2, view: 2, rg: 1</details> | ✅ |

[^s2-1]: ⚠️ Flaky (50% minority outcome). Grader breakdown: `skill-invocation forbids changelog-ent…` passed 1/2 trials
[^s2-2]: Trial durations: 3.9s – 6.2s


> Model: gpt-5.6-terra | Executor: copilot-sdk
