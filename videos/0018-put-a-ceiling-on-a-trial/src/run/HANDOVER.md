# Lesson 18's runs, for lessons 20 and 21

All figures are from our own runs in `/Users/Shared/demo/practice` (shown on screen as `~/src/demo/practice`).

## The budgets and the limit now in the eval file

`evals/changelog.eval.yaml` is byte-identical to `verified/lesson-18/practice/evals/changelog.eval.yaml`.
Under each of the five stimuli (typo-fix, refactor, security, two-changes, after-release):

| | Value | Where |
|---|---|---|
| `token-budget` `max` | 215000 | end of the stimulus's `graders` |
| `turn-count` `max` | 10 | same |
| `wall-time` `max` | 30s | same |
| `constraints.max_agent_duration` | 1m | just after the `prompt` |

The budget graders have no `name`; Vally names them `token-budget max 215000`, `turn-count max 10`,
`wall-time max 30s`. The file's `defaults.timeout` is still `3m`.

How they were set: the largest median in lesson 16's `report.md` across its four variants was 106,316 tokens
(haiku-high, two-changes), 5 turns, and 12.9 s (terra-low, security). The first budgets were 107000 / 5 / 13s;
the wider ones are about twice the largest typical value.

## The free re-grades (lesson 16's run `results/lesson-16/2026-11-11T08-39-02-179Z`)

| Budgets | haiku-high (15 trials) | terra-high (15 trials) |
|---|---|---|
| first (107000 / 5 / 13s) | 1 trial failed `token-budget`: two-changes, 108,012 tokens (about 1% over) | 2 trials failed `turn-count`: after-release and two-changes, 6 turns each |
| wider (215000 / 10 / 30s) | none | none |

So the first budgets failed 3 good trials of the 30 re-graded; no `wall-time` failure. In every re-grade the
script graders of two-changes and after-release fail with "no CHANGELOG.md to check" (they cannot be re-graded).
The lesson page's run had 5 of 29, including a trial 28 tokens over that printed "Score: 100.0% | FAILED"; the
video shows that block as "an earlier run" (`src/earlier-run-block.txt`).

## The paid run: `results/lesson-18/2026-11-11T14-39-05-705Z`

`vally eval -e evals/changelog.eval.yaml --model claude-haiku-4.5,gpt-5.6-terra --workers 2 --output-dir results/lesson-18`
One take, 10 agent runs, no ERROR, every trial `endReason: completed`. It is the only folder under
`results/lesson-18`.

| Model | Passed | Tokens: least / median / most | Turns | Slowest | Cost (AIU) |
|---|---|---|---|---|---|
| claude-haiku-4.5 | 5 of 5 | 59,705 / 75,379 / 75,717 | 4 to 5 | 12.5 s (after-release) | 11.42 |
| gpt-5.6-terra | 5 of 5 | 23,800 / 48,771 / 62,447 | 2 to 5 | 11.8 s (two-changes) | 14.13 |

Largest trial overall: 75,717 tokens, 5 turns; slowest 12.5 s. Nothing came near a budget (215000 / 10 / 30s) or
the one-minute limit, so `max_agent_duration` has not been seen stopping an agent in our runs.

Typical tokens per model, as the video states them: claude-haiku-5.5 about 105,000 (lesson 16), claude-haiku-4.5
about 75,000 (this run), gpt-5.6-terra about 61,000 (lesson 16).

## For lesson 21 (suites, exit codes)

- The quick suite is meant to carry these budgets. Lowering one budget "for a moment" in a free re-grade to get a
  failing exit code: any `token-budget` `max` below 59,705 fails every claude-haiku-4.5 trial of this run; a `max` of
  107000 on lesson 16's haiku-high fails exactly one trial (above).
- Lesson 5's run has only diff graders, so its re-grade exit code is meaningful; this run and lesson 16's include
  the two script graders, whose re-grades always fail.

## For lesson 20 (debugging)

- No trial of ours ended in ERROR here. The lesson page's own lesson 18 run had one ("Session disconnected while
  waiting for a response", terra, typo-fix); ours did not, and the video does not mention it.
- The `scoring-defaults-applied` warning prints on every lint and at the start of every `vally eval` of this file.

## Demo folder end state

- `evals/changelog.eval.yaml`: as above (equals `verified/lesson-18`). Nothing else under `evals/` or `skills/` was
  changed by this video.
- `results/lesson-18/2026-11-11T14-39-05-705Z` added. `results/lesson-16` untouched (still one run folder).
- Nothing was moved aside (no `/Users/Shared/.demo-old.lesson-18.*`).
- The tapes' logs are in `/tmp/vl-l18/` (copied to `src/run/s16.log`, `s18.log`, `s21.log`, `s23.log`).

## Recording state of this video

- `s16`, `s18`, `s21` (free) and `s23` (10 agent runs, logged) are recorded once each; all four credential scans
  were partly scanned, every still was looked at, and each is marked reviewed. They must not be re-recorded, and
  the tapes must not be edited (regenerating with `build-src/make-tapes.py` is byte-identical unless that file changes).
- Narration is current (`tts.py` run after the last wording change). Strict lint exits 0.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
