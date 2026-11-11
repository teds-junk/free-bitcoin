# Lesson 15's run, for lesson 19 (which compares these variants)

Run folder: `results/lesson-15/2026-11-11T07-53-29-176Z` in `/Users/Shared/demo/practice`
(shown on screen as `~/src/demo/practice/results/lesson-15/2026-11-11T07-53-29-176Z`). It is the only folder under
`results/lesson-15`. Each variant has its own folder inside it: `haiku-before`, `haiku-after`, `terra-before`, `terra-after`.

Experiment: `evals/before-and-after.experiment.yaml` on `evals/wording.eval.yaml` (stimuli parser, cache, dates;
judge `claude-sonnet-5.5`, yes-or-no), 3 trials of each stimulus, 2 workers.

| Variant | Model | Skill | Stimuli passed | Trials passed, of finished | Unfinished (ERROR) | Tokens |
|---|---|---|---|---|---|---|
| haiku-before (baseline) | claude-haiku-4.5 | skills/changelog-entry-before | 1/3 | 5 of 9 | 0 | 803.3k |
| haiku-after | claude-haiku-4.5 | skills/changelog-entry | 3/3 | 9 of 9 | 0 | 680.2k |
| terra-before | gpt-5.6-terra | skills/changelog-entry-before | 0/3 | 5 of 6 | 3 | 367.4k |
| terra-after | gpt-5.6-terra | skills/changelog-entry | 3/3 | 9 of 9 | 0 | 501.8k |

Per stimulus, where a trial did not pass:
- haiku-before: cache 0/3 (FAIL); parser 2 passed, 1 failed (FLAKY); dates 3/3.
- terra-before: cache 1 passed, 1 failed, 1 error (trial 3); dates 2 passed, 1 error (trial 3); parser 2 passed, 1 error (trial 2).
  Every error is "Session disconnected while waiting for a response". Those three trials have no verdict.
- haiku-after and terra-after: every trial passed.

Ranges (the course's calculator, 95% Wilson, whole percent): haiku 27% to 81% before, 70% to 100% after (overlap by 11 points);
terra 44% to 97% before, 70% to 100% after (overlap).

Things lesson 19 should know:
- **terra-before has only 6 finished trials** (2 per stimulus), so a pairing by stimulus and trial number against terra-after
  will find three pairs with no "before" side. terra-before's token total covers less work for the same reason.
- This was the third take. Takes one and two also lost trials to ERROR and were rerun under the standing rule; their
  results folders were moved aside, not deleted: `/Users/Shared/.demo-old.lesson-15.<time>` (runs
  `2026-11-11T07-36-56-350Z` and `2026-11-11T07-45-16-299Z`). Their output is in `src/earlier/` of this video.
- `src/run/report.md` here is a copy of the run's report with `/Users/Shared/demo` rewritten to `~/src/demo`.
- Trial times printed by the table: 3m40s, 3m36s, 2m43s, 3m26s (summed over a variant's trials).
