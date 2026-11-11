# Lesson 21's runs, for lessons 22 to 26

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Spend: 70 agent runs and 12 judge calls (`claude-sonnet-5.5`): the quick suite once
(10 runs), the full suite twice (30 runs and 6 judge calls each; the first take had two ERROR trials).

## The recordings

| Scene | Command | Run folder | Result | Exit |
|---|---|---|---|---|
| s13 | `vally lint -e evals/changelog.eval.yaml` | none | one warning, `scoring-defaults-applied`, no errors | 0 |
| s13 | `vally eval --suite quick --model claude-haiku-4.5,gpt-5.6-terra --workers 2 --require-pass --output-dir results/lesson-21-quick` | `results/lesson-21-quick/2026-11-11T16-13-09-826Z` | changelog 5/5 on both models; 10 trials, 24.42 AIU, 1.63 to 3.49 AIU a trial; largest trial 90,935 tokens (haiku, typo-fix), most turns 6, slowest 13.3 s | 0 |
| s14 | `vally grade -e ../../../evals/changelog.eval.yaml --run-dir . --require-pass < results.jsonl` in `results/lesson-5-before/2026-11-11T05-21-37-779Z` | none written | 18 blocks; the three haiku typo-fix trials pass 5/5, the other fifteen fail a result grader; no budget grader failed | **1** |
| s16 | the same command with typo-fix's `token-budget` `max` lowered to 70000 for that one command | none written | haiku's three typo-fix trials now fail on the budget alone (74,099 / 74,239 / 74,122 tokens, `Score: 98.8% | FAILED`); two terra typo-fix trials fail the budget as well as a result grader (73,517 and 85,855) | **1** |
| s18, kept (take 2) | `vally eval --suite full …same options… --output-dir results/lesson-21-full` | `results/lesson-21-full/2026-11-11T16-22-42-652Z` | changelog 5/5, conversation 1/1, loading 6/6, wording 3/3 on **both** models; 30 of 30 trials finished and passed; 66.57 AIU (haiku 27.19, terra 39.38; 2.22 a trial); 6 judge calls | 0 |
| s18, first take | the same | moved aside: `/Users/Shared/.demo-old.lesson-21-full.1794414136` (was `…/2026-11-11T16-18-12-120Z`) | two ERROR trials on claude-haiku-4.5 (`Session disconnected while waiting for a response`: conversation · three-requests, wording · cache) and one real FAIL: loading · skip-question on gpt-5.6-terra (`The following disallowed skills were called: changelog-entry`); 28 trials finished, 62.03 AIU | **1** |

- The first take was re-recorded because of its ERROR trials (the retake rule), not for its outcome. The video
  shows it in s19 and s24 as "our first run", from `src/earlier/` (log, exit code, records, README).
- `--require-pass` behaved as the page says: exit 0 when every stimulus passed, 1 for a failing verdict, 1 for an
  over-budget trial, 1 for a run with ERROR trials.
- `loading · skip-question` on gpt-5.6-terra failed in one run and passed minutes later: the skill is sometimes
  loaded for "What changed in version 1.2.0?". Later lessons that run `loading.eval.yaml` once may see it fail.
- Earlier videos' figures this one quotes: lesson 5 (1 pair of 6 passed), lesson 16 (haiku-low 15 of 15 at 0.21 AIU),
  lesson 19 (swapped compare: ours -0.33 [-0.75, +0.08], exit 0; the course's earlier run -0.49 [-0.90, -0.07],
  exit 1, shown as "an earlier run"). `standing.json` → `conversation_after_fix` is no longer used by a scene.

## Demo folder end state

- **`.vally.yaml`** now exists in `practice/` (lesson 26 needs it), byte-identical to
  `verified/lesson-21/practice/.vally.yaml` and to `src/state/.vally.yaml`: suite `quick`
  (`evals/changelog.eval.yaml`, `filter: { tier: quick }`) and suite `full` (changelog, conversation, loading,
  wording; no filter). Run from `practice/` with `vally eval --suite quick|full`.
- `evals/changelog.eval.yaml` has `tags: { tier: quick }` under each of its five stimulus names and is
  byte-identical to `verified/lesson-21`. Budgets are back at 215000 / 10 / 30s (the lowering in s16 lasted one
  command and was restored by the tape's wrapper; checked afterwards).
- `CONVENTIONS.md` now exists in `practice/`, byte-identical to `verified/lesson-21`. Its last line says
  "checked on 2026-11-10", the page's date; our runs are dated 2026-11-11. The video shows the file as it is and
  does not read the date aloud.
- New results folders: `results/lesson-21-quick/` (one run) and `results/lesson-21-full/` (one run, the kept
  take). A tape that lists `results/` will see both.
- Moved aside, not deleted: `/Users/Shared/.demo-old.lesson-21-full.1794414136` (the first take).
- Nothing under `skills/` was touched; `evals/` is otherwise as lesson 20 left it (`evals/wording-scaled.eval.yaml`
  was already there and is not in either suite).
- Tape logs and exit codes are in `/tmp/vl-l21/` (`s18.1.*` is the kept take) and copied to `src/run/`.

## Recording state of this video

- s13, s14, s16 are recorded once each; s18 twice (second kept). None must be re-recorded; the tapes must not be
  edited. Credential scans: all four were partly scanned (output scrolled); all 12 stills of each were looked at
  and each is marked reviewed (commands, grader blocks, summary tables, `~/src/demo` paths, run IDs, exit codes;
  nothing sensitive). No hits.
- `src/run/PROVISIONAL` is gone; generator asserts pass on the real run; narration is current; strict lint exits 0.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
