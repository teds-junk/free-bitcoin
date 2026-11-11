## Eval Results

> Timestamp: 2026-11-10T07:42:11.141Z

### changelog-entry-hard [claude-haiku-4.5] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/hard.eval.yaml)

Messier, ordinary changelog requests

> **Environment**: 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| implementation-words | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 9.3s | 74,309 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| internal-refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 9.3s | 74,229 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| no-pr-number | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 7.3s | 74,118 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| no-unreleased-section | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 7.8s | 74,240 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| security-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 8.6s | 74,129 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |
| two-changes-one-pr | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 8.0s | 74,204 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### changelog-entry-hard [mai-code-1.1-flash] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/hard.eval.yaml)

Messier, ordinary changelog requests

> **Environment**: 1 skill

| Stimulus | Environment | Skills | Model | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| no-unreleased-section | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | — | — | — | — | — | — | — | — | ❌ [^s2-1] |
| implementation-words | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | mai-code-1.1-flash | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 14.1s | 56,285 | 5 | <details><summary>5 calls</summary>glob: 2, skill: 1, view: 1, edit: 1</details> | ✅ |
| internal-refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | mai-code-1.1-flash | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 21.6s | 59,568 | 5 | <details><summary>7 calls</summary>view: 3, glob: 1, list_bash: 1, skill: 1, edit: 1</details> | ✅ |
| no-pr-number | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | mai-code-1.1-flash | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 23.4s | 70,342 | 6 | <details><summary>6 calls</summary>grep: 2, skill: 1, glob: 1, view: 1, edit: 1</details> | ✅ |
| security-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | mai-code-1.1-flash | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 15.7s | 79,294 | 7 | <details><summary>7 calls</summary>view: 4, glob: 1, skill: 1, edit: 1</details> | ✅ |
| two-changes-one-pr | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | mai-code-1.1-flash | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 16.8s | 57,352 | 5 | <details><summary>5 calls</summary>skill: 1, glob: 1, grep: 1, view: 1, edit: 1</details> | ✅ |

[^s2-1]: Error: Stimulus 'no-unreleased-section' timed out after 180000 ms during turn 1 of 1


> Model: mai-code-1.1-flash | Executor: copilot-sdk

<hr>

### changelog-entry-hard [gpt-5.6-terra] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/hard.eval.yaml)

Messier, ordinary changelog requests

> **Environment**: 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| implementation-words | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 8.4s | 60,509 | 5 | <details><summary>5 calls</summary>skill: 1, glob: 1, rg: 1, view: 1, apply_patch: 1</details> | ✅ |
| internal-refactor | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 10.8s | 60,202 | 5 | <details><summary>5 calls</summary>glob: 2, skill: 1, view: 1, apply_patch: 1</details> | ✅ |
| no-pr-number | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 10.9s | 60,433 | 5 | <details><summary>5 calls</summary>glob: 2, skill: 1, view: 1, apply_patch: 1</details> | ✅ |
| no-unreleased-section | <details><summary>1 file · 1 skill</summary>Files: `fixtures/just-released/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 6.8s | 48,423 | 4 | <details><summary>4 calls</summary>skill: 1, view: 1, glob: 1, apply_patch: 1</details> | ✅ |
| security-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 6.9s | 48,333 | 4 | <details><summary>4 calls</summary>skill: 1, view: 1, glob: 1, apply_patch: 1</details> | ✅ |
| two-changes-one-pr | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` | ✅ file-exists CHANGELOG.md 1/1 | 1/1 | 8.6s | 48,502 | 4 | <details><summary>4 calls</summary>skill: 1, view: 1, glob: 1, apply_patch: 1</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
