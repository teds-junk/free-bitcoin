# Lesson 17's run, for later lessons

Run folder: `results/lesson-17/2026-11-11T13-59-30-867Z` in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice/results/lesson-17/2026-11-11T13-59-30-867Z`). It is the only folder under `results/lesson-17`.
It holds one variant folder, `qwen-local`, with `results.jsonl` (copy here, paths rewritten: `src/run/results.jsonl`)
and the trial folders under `qwen-local/changelog/<stimulus>/qwen3.5-9b/0/`.

What ran: `vally experiment run evals/cost.experiment.yaml --variant qwen-local --workers 1 --output-dir results/lesson-17`.
One trial of each of the five stimuli of `evals/changelog.eval.yaml`, on `qwen3.5:9b` through Ollama 0.18.1 on this
computer, time limit 9 minutes. No Copilot usage and no judge calls. The run took 13m23s.

| Stimulus | Status | Passed | Failing grader: what it found | Input tokens | Output tokens | Calls | Time | Loaded the skill |
|---|---|---|---|---|---|---|---|---|
| after-release | success | no | entry-in-new-unreleased: no `## [Unreleased]` heading (it wrote `## [1.3.1] - 2026-11-11`) | 61,757 | 992 | | 165 s | no |
| refactor | success | no | adds-nothing: workspace diff is not empty (an entry under Changed) | 83,243 | 685 | | 147 s | no |
| security | success | no | under-security: no `### Security` line added (filed under Fixed) | 46,640 | 364 | | 100 s | no |
| two-changes | success | yes | | 46,869 | 436 | | 114 s | no |
| typo-fix | success | yes | | 126,278 | 1,380 | 10 | 278 s | yes |
| Total | no ERROR | 2 of 5 | | 364,787 | 3,857 | | | 1 of 5 |

- Every trial finished (`status: success`, `endReason: completed`); none ended in ERROR or timed out.
- No trial has a `cost` in its `tokenUsage`, and `cacheReadTokens` is 0 in all five.
- Median total tokens per trial: 62,749. Largest: 127,658 (typo-fix). Longest trial: 278 s; shortest: 100 s.
- Priced at the lesson's made-up rate ($0.10 per million input tokens, $0.40 per million output): $0.0365 + $0.0015 =
  $0.0380 for five trials (3.8 cents), $0.0190 per passing trial (1.9 cents). Against lesson 16's own run: about nine
  times haiku-low (0.21 cents), under terra-low (2.76 cents).
- 95% range for 2 of 5: 12% to 77%. For 15 of 15: 80% to 100%.

Takes: the first recording of `s17` was lost about ten minutes in, with four of five trials done, when vhs lost its
connection to the terminal (another video was rendering at the time). That killed the run before it wrote a results
file. It was not an ERROR trial and nothing about the outcome was known. The second recording, on a quiet machine,
is the one above. Its partial folder was moved aside by the tape's setup, not deleted:
`/Users/Shared/.demo-old.lesson-17.1794405551`.

## The demo folder after lesson 17

- `evals/cost.experiment.yaml` now has the fifth variant, `qwen-local`, and the six-line `vary` list. It is
  byte-identical to `verified/lesson-17/practice/evals/cost.experiment.yaml`.
- `evals/changelog.eval.yaml` is unchanged by this lesson and byte-identical to `verified/lesson-17` (and to
  `verified/lesson-16`): five stimuli, pattern and script graders, no judge, `timeout: 3m`.
- `results/lesson-16` still has exactly one run folder, `2026-11-11T08-39-02-179Z`.
- `results/lesson-17` has exactly one run folder (above).
- Differences from `verified/lesson-17/practice` that were there before this lesson's turn and are not ours:
  `evals/broken/`, `evals/fixtures/release/`, `evals/wording-scaled.eval.yaml`, and the contents of
  `evals/golden/security.patch` and `evals/golden/two-changes.patch` (the series' own trials).
- Ollama was left serving; nothing was pulled or removed.

Things later lessons should know:
- A long local run inside a recording is fragile: keep the machine otherwise idle while one records.
- With `--variant`, the run's folder holds only that variant; lesson 16's four variants stay in `results/lesson-16`.
- After the jump cut the screen shows the experiment summary, the comparison line, the table, the run id and the
  saved path. The FAIL blocks have scrolled off, so narration must not point at them.
