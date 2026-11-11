## Eval Results

> Timestamp: 2026-11-10T07:34:59.293Z

### changelog-entry [claude-haiku-4.5] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml)

Does the agent record a change the way the skill asks?

> **Environment**: 1 file · 1 skill

| Stimulus | Environment | Skills | Graders | Pass Rate | pass@k | pass^k | Duration (median) | Tokens (median) | Turns (median) | Tool Calls (median) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fix-accented-search | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (2×) | — | — | — | — | — | — | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 4, skill: 2, edit: 2</details> | ❌ [^s1-1] |
| change-list-sort | <details><summary>1 file · 1 skill</summary>Files: `fixtures/notes-cli/CHANGELOG.md` → `CHANGELOG.md`<br/>Skills: `../../skills/changelog-entry`</details> | `changelog-entry` (3×) | ✅ mentions-pr-52 3/3 | 3/3 | 100.0% | 100.0% | 12.4s | 74,374 | 5 | <details><summary>4 calls (median)</summary>total across 3 trials: view: 6, skill: 3, edit: 3</details> | ✅ |

[^s1-1]: 1/3 trial(s) errored


> Model: claude-haiku-4.5 | Executor: copilot-sdk

<hr>

### changelog-entry [mai-code-1.1-flash] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml)

#### ❌ Errors

- `[workspace-collision] Workspace path collision at '/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/ws/main/fix-accented-search': claimed by 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × claude-haiku-4.5::fix-accented-search' and 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × mai-code-1.1-flash' (stimulus 'fix-accented-search'). Rename one of the stimuli or use distinct --workspace roots.` at /private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml

#### ❌ Errors

- `Workspace path collision at '/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/ws/main/fix-accented-search': claimed by 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × claude-haiku-4.5::fix-accented-search' and 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × mai-code-1.1-flash' (stimulus 'fix-accented-search'). Rename one of the stimuli or use distinct --workspace roots.`

_No stimuli were executed._


> Model: mai-code-1.1-flash

<hr>

### changelog-entry [gpt-5.6-terra] (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml)

#### ❌ Errors

- `[workspace-collision] Workspace path collision at '/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/ws/main/fix-accented-search': claimed by 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × claude-haiku-4.5::fix-accented-search' and 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × gpt-5.6-terra' (stimulus 'fix-accented-search'). Rename one of the stimuli or use distinct --workspace roots.` at /private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml

#### ❌ Errors

- `Workspace path collision at '/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/ws/main/fix-accented-search': claimed by 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × claude-haiku-4.5::fix-accented-search' and 'variant 'main' / changelog-entry (/private/tmp/claude-501/-Users-ted-src-learn-vally/d8bc06e6-d466-4dfc-9fa5-a53299f0c3f8/scratchpad/pilot/evals/changelog-entry/eval.yaml) × gpt-5.6-terra' (stimulus 'fix-accented-search'). Rename one of the stimuli or use distinct --workspace roots.`

_No stimuli were executed._


> Model: gpt-5.6-terra
