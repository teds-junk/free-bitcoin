## Eval Results

> Timestamp: 2026-11-11T05:30:01.126Z

### changelog [claude-haiku-4.5] (~/src/demo/practice/evals/changelog.eval.yaml)

> **Environment**: 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| after-release | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ entry-in-new-unreleased 1/1 | 1/1 | 10.1s | 74,611 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ adds-nothing 1/1 | 1/1 | 8.4s | 58,888 | 4 | <details><summary>3 calls</summary>view: 2, skill: 1</details> | ✅ |
| security | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ under-security 1/1 | 1/1 | 8.8s | 74,745 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| two-changes | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ two-entries-in-place 1/1 | 1/1 | 8.4s | 74,862 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ adds-an-entry 1/1<br>✅ no-made-up-number 1/1 | 1/1 | 8.0s | 74,575 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### changelog [gpt-5.6-terra] (~/src/demo/practice/evals/changelog.eval.yaml)

> **Environment**: 1 skill

#### ⚠️ Warnings

- `[scoring-defaults-applied] Multiple graders with no scoring config` at scoring

| Stimulus | Environment | Skills | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| after-release | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ❌ entry-in-new-unreleased 0/1 | 0/1 | 5.9s | 48,320 | 4 | <details><summary>3 calls</summary>skill: 1, view: 1, apply_patch: 1</details> | ❌ [^s2-1] |
| refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ adds-nothing 1/1 | 1/1 | 4.7s | 23,634 | 2 | <details><summary>1 calls</summary>skill: 1</details> | ✅ |
| security | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ under-security 1/1 | 1/1 | 7.6s | 48,468 | 4 | <details><summary>3 calls</summary>skill: 1, view: 1, apply_patch: 1</details> | ✅ |
| two-changes | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ two-entries-in-place 1/1 | 1/1 | 8.2s | 60,435 | 5 | <details><summary>4 calls</summary>skill: 1, glob: 1, view: 1, apply_patch: 1</details> | ✅ |
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ adds-an-entry 1/1<br>✅ no-made-up-number 1/1 | 1/1 | 7.8s | 60,454 | 5 | <details><summary>5 calls</summary>skill: 1, glob: 1, rg: 1, view: 1, apply_patch: 1</details> | ✅ |

[^s2-1]: Failed grader(s): `entry-in-new-unreleased`


> Model: gpt-5.6-terra | Executor: copilot-sdk
