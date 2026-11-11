# Lesson 23's run, for lessons 24 to 26

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Spend: 6 agent runs, one take. No ERROR trials; nothing was re-run for its outcome.

## The recordings

| Scene | Command | Result |
|---|---|---|
| s15 | `vally lint -e evals/release.eval.yaml`; `vally oracle -e evals/release.eval.yaml --no-golden-input` | one warning, `scoring-defaults-applied`; baseline OK: `every-change-handled`, `reads-the-list`, `loads-the-skill` failed as expected, `never-commits` and `no-loop` N/A |
| s16 | `cd results/lesson-22/2026-11-11T16-51-44-338Z` (Tab), `vally grade -e ../../../evals/release.eval.yaml --run-dir . --verbose < results.jsonl` | ten blocks. `every-change-handled` fails in all ten (a re-grade has no workspace). `reads-the-list`, `never-commits`, `no-loop` pass 10 of 10. `loads-the-skill` passes 8 of 10 (fails the two haiku trials without the skill) |
| s19 | the same command, with `never-commits` forbidding `find` | `never-commits` fails in 1 of 10 (the second block: haiku's folder 0, which ran `find . -name "release" -o -name "merged.txt"`), evidence `/^bash$/ {command=/find/}`; passes the other nine |
| s21 | `vally eval -e evals/release.eval.yaml --model claude-haiku-4.5,gpt-5.6-terra --runs 3 --workers 2 --output-dir results/lesson-23` | run `results/lesson-23/2026-11-11T17-27-07-928Z`, run ID `acc157e1-7613-4734-a0c2-ad541560ca35`, 6 of 6 finished in 0:41. claude-haiku-4.5: FLAKY, 1 passed and 2 failed; trials 1 and 3 failed both `every-change-handled` and `loads-the-skill`; table `✘ 0/1`. gpt-5.6-terra: 3 of 3, `✓ 1/1` |

## What the runs showed (src/run/l22, src/run/l23; make-scenes.py asserts each figure)

- `never-commits` and `no-loop` failed 0 of 16 real trials (ten saved, six new). `reads-the-list` also passed
  all 16. No bash command in either run contains a commit or a push.
- **haiku, eight trials** (five saved, three new): loaded the skill in 4, wrote a refactor (#76) entry in 5,
  passed every grader in 3. The four trials without the skill all wrote the refactor entry; of the four with
  it, three left it out and one (lesson 22's folder 4) wrote it anyway.
- **terra, eight trials**: loaded 8, no refactor entry, passed 8.
- This differs from the lesson page (haiku 0 of 8 passed, loaded 1 of 8). The video states only ours.
  **Lesson 26's eight-trial section should use these figures.**
- Saved report, lesson 22 run, haiku's Tool Calls: `view: 18, edit: 5, skill: 3, bash: 2`.
- New tools seen in the s21 run: terra used `sql` (twice, one trial) and `glob` (once).
- s08 does not cite an earlier run for the view-only grader failing a `cat` trial: no saved trial shows it
  (only a line in NOTES.md), so the video states it as what such a grader would do.

## Demo folder end state

- `evals/release.eval.yaml` is byte-identical to `verified/lesson-23/practice/evals/release.eval.yaml` and this
  video's `src/state/release.eval.yaml`: the lesson 22 file plus the four graders, with the real
  commit-or-push pattern back in `never-commits` (checked with `cmp` after s21).
- New: `results/lesson-23/` with one run (above). Nothing was moved aside (it did not exist before).
- `results/lesson-22/` is untouched and still holds exactly one run.
- Nothing else changed. Tape logs: `/tmp/vl-l23/s15.log`, `s16.log`, `s19.log`, `s21.log` (copied to `src/run/`).

## Recording state of this video

- s16, s19, s21 recorded once. s15 twice: the second at FontSize 31, because at 34 the oracle report pushed the
  command's first line off the screen (a layout retake of a free tape; same output).
- Credential scans: s15 fully scanned, no hits. s16, s19, s21 partly scanned (output scrolled); all 12 stills of
  each were looked at and each is marked reviewed. No hits.
- `src/run/PROVISIONAL` and `facts.json` are gone; generator asserts pass on the real runs; narration is
  current; strict lint exits 0; `preview.js --all` reports no problems.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
