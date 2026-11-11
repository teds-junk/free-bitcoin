# Lesson 16's run, for lessons 17, 18 and 21

Run folder: `results/lesson-16/2026-11-11T08-39-02-179Z` in `/Users/Shared/demo/practice`
(shown on screen as `~/src/demo/practice/results/lesson-16/2026-11-11T08-39-02-179Z`). It is the only folder under
`results/lesson-16`. Each variant has its own folder inside it, holding a `results.jsonl`; copies are in this
folder (`src/run/<variant>/results.jsonl`), with the run's `report.md` (paths rewritten to `~/src/demo`).

Experiment: `evals/cost.experiment.yaml` on `evals/changelog.eval.yaml` (five stimuli, code and script graders,
no judge), 3 trials of each stimulus, 2 workers, baseline `haiku-low`. One take; all 60 trials finished, none
ended in ERROR. Vally's line: "No variant beat baseline. Same pass rate (5/5) for all." The run took 4m22s.

| Variant | Model | Effort | Trials finished | Passed | Stimuli | Cost (AIU) | Per passing trial | Cheapest to dearest trial |
|---|---|---|---|---|---|---|---|---|
| haiku-low (baseline) | claude-haiku-5.5 | low | 15 of 15 | 15 | 5/5 | 3.13 | 0.21 | 0.14 to 0.23 |
| haiku-high | claude-haiku-5.5 | high | 15 of 15 | 15 | 5/5 | 3.55 | 0.24 | 0.15 to 0.39 |
| terra-low | gpt-5.6-terra | low | 15 of 15 | 15 | 5/5 | 41.45 | 2.76 | 1.67 to 4.20 |
| terra-high | gpt-5.6-terra | high | 15 of 15 | 15 | 5/5 | 42.38 | 2.83 | 1.70 to 4.21 |

Whole experiment: 90.51 AIU, $0.905 at $0.01 per AIU. No judge calls.

For lesson 18's budgets (per trial, from `trajectory.metrics`):

| Variant | Total tokens (table) | Median tokens | Largest trial, tokens | Median output tokens | Most turns | Most tool calls | Longest wall time |
|---|---|---|---|---|---|---|---|
| haiku-low | 1,324,453 (1324.5k) | 105,169 | 105,398 | 651 | 5 | 4 | 6.2 s |
| haiku-high | 1,377,997 (1378.0k) | 105,810 | 108,012 | 839 | 5 | 5 | 8.9 s |
| terra-low | 807,936 (807.9k) | 61,032 | 74,665 | 351 | 6 | 7 | 13.6 s |
| terra-high | 809,834 (809.8k) | 61,049 | 74,841 | 358 | 6 | 7 | 12.5 s |

Trial times printed by the table (summed over a variant's trials): 1m33s, 2m04s, 2m25s, 2m30s.

**Cheapest variant that passed everything: `haiku-low`** (claude-haiku-5.5 at low effort): 15 of 15 at 0.21 AIU a
passing trial. It beats the other three on both counts (each costs more and passes no more often). Both terra
variants cost 13 to 14 times as much per passing trial. The pass-rate range is 80% to 100% for every variant.

Things the next lessons should know:
- The demo folder now holds `evals/cost.experiment.yaml` (lesson 17 adds a variant to it; keep the variant names).
- `results/lesson-16-efforts/2026-11-11T08-36-52-323Z` is the free efforts check: three ERROR trials on purpose,
  no usage recorded. Accepted efforts on this account: claude-haiku-4.5 none; claude-haiku-5.5 low, medium, high,
  xhigh, max; gpt-5.6-terra none, low, medium, high, xhigh, max.
- A real record has a `shardKey` line after `stimulus` that is too wide for a panel and wraps over three rows.
- The videos' own earlier average on claude-haiku-4.5 and gpt-5.6-terra is 2.38 AIU a trial (205 trials, lessons
  1 to 15; `src/earlier-average.json`), where the lesson page says 2.2. This video's dollar figures use 2.38.
