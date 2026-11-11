# Lesson 26's run (the course's last lesson)

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Spend: 8 agent runs (2 + 6), one take each. The only ERRORs are the designed
tracker-down refusals; no trial of `since-last-release` ended in ERROR; nothing was re-run for its outcome.

## The recordings

| Scene | Command | Result |
|---|---|---|
| s16 | `node --check app/vally-executor.mjs`; `vally eval -e evals/release.eval.yaml --executor release-app --model claude-haiku-4.5,gpt-5.6-terra --workers 2 --output-dir results/lesson-26` | check prints nothing. Run `results/lesson-26/2026-11-11T18-49-03-135Z`, run ID `98c0a64d-d77f-4f1d-ad62-5797e5250191`. tracker-down ERROR on both models (executor does not support tool-call simulation). haiku FAIL since-last-release (`every-change-handled`, `loads-the-skill`); terra passed. Table `✘ 0/2`, `✘ 1/2` |
| s20 | `vally experiment run evals/release-app.experiment.yaml --dry-run` | `Plans: 2`, baseline haiku |
| s21 | `vally experiment run evals/release-app.experiment.yaml --workers 2 --output-dir results/lesson-26-experiment` | run `results/lesson-26-experiment/2026-11-11T18-52-18-877Z`, run ID `5b740ed5-503a-426a-af72-2df647ff65f4`. tracker-down `0 passed · 3 errors` for both variants. "terra beat baseline — 1/2 vs 0/2 stimuli", terra −24% tokens (279.6k against 211.1k), +25% trial time |

## What the runs showed (src/run/; make-scenes.py asserts each figure)

- **Through the app, four `since-last-release` trials a model** (`trials.tsv`):
  haiku passed 0 of 4, loaded the skill in 1 (an experiment trial, which still wrote the refactor entry),
  wrote a #76 entry in 4. terra passed 4, loaded 4, no #76 entry.
- Experiment only (three a variant): haiku 0 passed, 1 loaded, 3 entries for #76, 6.69 AIU; terra 3, 3, 0, 10.75 AIU.
- Report (`eval-report.json`): `Executor: release-app` under both tables; haiku's table has no Skills column,
  tool calls `view: 4, edit: 1`; terra lists `changelog-entry`, `view: 3, skill: 1, apply_patch: 1`.
- Trace join (`trace-join.json`): haiku's `invoke_agent` span carries the trial's trace ID and has Vally's
  `vally.attempt` span as its parent.
- **Against Vally's own executor** (`vally-executor.json`, built by `build-src/vx-from-series.py` from the
  lesson 23 video's saved `l22` and `l23` results; eight trials a model):
  haiku passed 3 of 8, loaded 4 of 8; terra 8 and 8.
  - Skill loads on haiku: 1 of 5 through the app (its four trials plus lesson 25's one run) against 4 of 8;
    95% ranges 4–62% and 22–78%. The video says "too few trials to tell", and cites "an earlier run"
    (the course's verified run, `earlier-run.txt`: 0 of 5 against 1 of 8).
  - Tokens a model call: every app trial above every Vally-executor trial. haiku lowest 17,363 against highest
    15,262 (+16% on average); terra 13,977 against 12,545 (+13%).
  - Model calls a trial: haiku 5.25 against 5.75; terra 5 against 4.75. AIU a trial: haiku 2.54 against 2.58;
    terra 4.03 against 3.27.
  - Five `github-mcp-server-*` tools are in the tool definitions of both models' `app-traces.jsonl`.
- Differences from the lesson page, all stated as ours: haiku loaded once through the app; the app's trials did
  not cost less on both models; the page's "the fix belongs in the skill or the model choice" and its earlier
  test on another request are left out.

## Personal data

- The app's `app-traces.jsonl` files (in each trial's `executor-artifacts/`) capture content and were never
  printed in a tape or copied here; `trace-join.json` keeps four id fields of two spans only.
- Credential scans: s20 fully scanned, no hits. s16 and s21 partly scanned (output scrolled); all 12 stills of
  each were looked at and each is marked reviewed. On screen: the typed commands, Vally's refusal text, the
  summaries and tables, `~/src/demo` paths, run IDs. No app console output, account id, email or real path.

## Demo folder end state

- `app/vally-executor.mjs`: `execute` written (byte-identical to `src/state/vally-executor.mjs`).
- `.vally.yaml`: the three `plugins` lines at its top, the rest as lesson 21 left it (copy in `src/state/vally.yaml`).
- New: `evals/release-app.experiment.yaml`; `results/lesson-26/` and `results/lesson-26-experiment/`, one run each.
- Nothing was moved aside. `evals/release.eval.yaml`, `app-run/`, `app/node_modules`, skills, tools and the
  earlier results folders are untouched. `app/run.sh` was not run.
- Tape logs: `/tmp/vl-l26/s16.log`, `s20.log`, `s21.log` (cleaned copies in `src/run/`).

## Recording state of this video

- s16, s20, s21 recorded once each; their clips build (55.1s, 19.2s, 31.4s). Tapes need no re-recording.
- `src/run/PROVISIONAL` is gone; generator asserts pass on the real runs; narration is current; strict lint exits 0.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
