# Lesson 20's runs, for lesson 21 and later

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Eleven tapes, one take each, no retakes. 9 agent runs logged; 2 judge calls
(`claude-sonnet-5.5`) in s34, plus 2 judge calls in s31 that failed by design before reaching a model.

## The six runs

| Scene | Command | Run folder | Result |
|---|---|---|---|
| s14 | `vally eval -e evals/broken/merged-list.eval.yaml`, both models (file broken) | `results/lesson-20-earlier/2026-11-11T15-37-37-941Z` | **ERROR on purpose**, both: `The "command" argument must be of type string. Received an instance of Object`; trials lasted 5 and 8 ms; trial folder holds only `metadata.json`; no `eval-results.md` (the reporter threw); no agent started |
| s18 | same file fixed, `--model claude-haiku-4.5` | `…/2026-11-11T15-40-06-011Z` | PASS, 10.5 s |
| s19 | `evals/broken/quick.eval.yaml` (timeout 5s), both models, `--verbose` | `…/2026-11-11T15-41-20-539Z` | **ERROR on purpose**, both: `Stimulus 'typo-fix' timed out after 5000 ms during turn 1 of 1`; trial folders hold `events.jsonl` and `metadata.json`; `--verbose` printed no reply |
| s24 | same file fixed (timeout 3m), both models | `…/2026-11-11T15-42-47-323Z` | 1/1 on both; 10.2 s (haiku), 9.5 s (terra) |
| s25 | `evals/broken/entry.eval.yaml` (pattern without `(?m)`), both models, `--verbose` | `…/2026-11-11T15-46-46-735Z` | **FAIL on purpose**, both: `adds-an-entry  Pattern /^\+.*notes add/ not found in workspace diff`; both patches add `### Fixed` and an entry with `notes add` |
| s31 | `evals/broken/judged.eval.yaml` (judge model misnamed), both models | `results/lesson-20/2026-11-11T15-49-28-019Z` | **ERROR on purpose**, both: `cache · 1/2 graders`, `Grading error; verdict is invalid.`, `LLM judge failed: Model "claude-sonnet-5-5" is not available in Copilot`; both trial records have status `success` |

Free re-grades (`vally grade … --run-dir . < results.jsonl`, run inside the run's folder):
- s30, entry run, grader fixed: both trials `1/1 graders passed`, `Score: 100.0% | PASSED`.
- s34, judged run, judge model fixed, `--verbose`: **one trial passed 2/2; the other failed the judge**
  (`1/2 graders passed, 1 failed`, `Score: 50.0% | FAILED`). The failing entry is claude-haiku-4.5's,
  "Improve performance of `notes list --tag` with caching (#66)"; the judge's reason says it mentions the
  implementation. The lesson page's run passed both. The video says what ours did: the fix let the judge
  reach a verdict, and one verdict is a real FAIL.

## Figures the video states

- A timed-out trial is not free: the last `session.usage_checkpoint` in each `events.jsonl` of the s19 run
  gives 2,954,400,000 nano-AIU (2.95 AIU) for gpt-5.6-terra and 739,015,000 (0.74 AIU) for claude-haiku-4.5.
  The trial records in `results.jsonl` have no cost. Both logs end `skill.invoked`, `assistant.turn_end`,
  `assistant.turn_start`, `abort` (reason `user_initiated`), `assistant.turn_end`, `session.usage_checkpoint`.
  (The page's figures were 1.26 and 1.02 AIU.)
- "This same request took about eight and nine seconds earlier": the two typo-fix trials of the lesson 18
  video's run, 9,259 ms (haiku) and 7,684 ms (terra), from `results/lesson-18/2026-11-11T14-39-05-705Z/results.jsonl`.
- The account's model list printed in s31 now includes `gemini-4-carbon` (not in the page's list).
- Totals said in s35: nine agent runs and two judge calls.

## For lesson 21 (suites, exit codes, a routine)

- No exit codes were captured in this video's logs.
- A run whose trials all ERROR before an agent starts (s14) saves `results.jsonl` but no `eval-results.md`.
- `--fail-on-regression` and budgets were not used here.

## Demo folder end state

- `evals/broken/` holds the four files **fixed**, byte-identical to `verified/lesson-20/practice/evals/broken`
  (and to this video's `src/state/fixed/`). Nothing else under `evals/` or `skills/` was touched by this video;
  `evals/changelog.eval.yaml` is as lesson 18 left it.
- `results/lesson-20/` holds one run (judged). `results/lesson-20-earlier/` holds the other five. A later tape
  that lists `results/` will see both folders.
- Moved aside, not deleted: `/Users/Shared/.demo-old.lesson-20.broken.1794411420`, the `evals/broken` folder
  the demo had before s14 (identical to the starter's), so the page's `cp` could be shown.
- `vally grade` wrote nothing we rely on; the two re-grades printed to the console only.
- Tape logs are in `/tmp/vl-l20/` (copied to `src/run/s14.log` … `s34.log`).

## Recording state of this video

- s14, s15, s18, s19, s20, s24, s25, s27, s30, s31, s34 are recorded once each and must not be re-recorded;
  the tapes must not be edited. (s34's tape comment still says two 2/2 blocks were expected.)
- Credential scans: s14, s19, s25, s34 were partly scanned; all 12 stills of each were looked at and each is
  marked reviewed (commands, expected errors, summaries, `~/src/demo` paths, run IDs, quoted changelog
  entries; nothing sensitive). s15, s18, s20, s24, s27, s30, s31: full scan, no hits.
- `src/run/PROVISIONAL` is gone; generator asserts pass on the real run; narration is current; strict lint exits 0.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
