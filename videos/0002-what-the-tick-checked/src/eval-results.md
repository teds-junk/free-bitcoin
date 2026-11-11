## Eval Results

> Timestamp: 2026-11-11T00:12:10.241Z

### one-request [claude-haiku-4.5] (~/src/demo/practice/evals/one-request.eval.yaml)

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ mentions-the-command 1/1 | 1/1 | 9.3s | 74,210 | 5 | <details><summary>4 calls</summary>view: 2, skill: 1, edit: 1</details> | ✅ |

> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### one-request [gpt-5.6-terra] (~/src/demo/practice/evals/one-request.eval.yaml)

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | Duration | Tokens | Turns | Tool Calls | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| typo-fix | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../skills/changelog-entry`</details> | `changelog-entry` | ✅ mentions-the-command 1/1 | 1/1 | 16.2s | 73,095 | 6 | <details><summary>7 calls</summary>glob: 2, skill: 1, bash: 1, view: 1, rg: 1, apply_patch: 1</details> | ✅ |

> Model: gpt-5.6-terra | Executor: copilot-sdk
