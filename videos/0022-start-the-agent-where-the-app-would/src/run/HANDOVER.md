# Lesson 22's run, for lessons 23 to 26

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Spend: 10 agent runs, one take. No ERROR trials; nothing was re-run for its outcome.

## The recordings

| Scene | Command | Result |
|---|---|---|
| s15 | `node tools/list-merged.mjs`; `vally lint -e evals/release.eval.yaml` | the three changes (#74 feat, #75 fix, #76 refactor); `✔ evals/release.eval.yaml is valid` |
| s16 | `vally eval -e evals/release.eval.yaml --model claude-haiku-4.5,gpt-5.6-terra --runs 5 --workers 2 --output-dir results/lesson-22` | run `results/lesson-22/2026-11-11T16-51-44-338Z`, run ID `e22ed4d8-22ff-49f5-8d1f-7b8887e08ec8`, 10 of 10 trials finished in 1:04. claude-haiku-4.5: FLAKY, 2 passed and 3 failed (`every-change-handled`, exit code 1, trials 1, 2, 5), table `✘ 0/1`. gpt-5.6-terra: 5 of 5, `✓ 1/1` |
| s17 | `ls results/lesson-22`, `cd` into the run and `release/since-last-release`, `cat claude-haiku-4.5/1/workspace.patch` | haiku's trial 2 (folder 1), failing: #74 under Added, `### Fixed` with #75, `### Changed` with "Move config loading out of cli.js (#76)" |
| s18 | `cat gpt-5.6-terra/0/workspace.patch` | passing: #74 and #75 only |

## What the run showed (src/run/trials.json, the ten patches, s16.log)

- Every patch changes only `CHANGELOG.md`; `release/merged.txt` is in none. No model skipped #74 or #75 or
  merged two changes into one line.
- **haiku** (folders 0 to 4 = trials 1 to 5): loaded the skill in 3 of 5 (folders 2, 3, 4); wrote a refactor
  entry in 3 of 5 (folders 0, 1, 4). The two trials without the skill both recorded the refactor; of the three
  with it, two left it out and one (folder 4) recorded it anyway. Folder 3 passed but added empty `### Changed`,
  `### Removed` and `### Refactored` headings; the hidden test does not look at headings, and the video does not
  mention it.
- **terra**: loaded the skill 5 of 5, left the refactor out 5 of 5, and each reply says #76 was omitted as an
  internal refactor. Its #74 entries: four say "created on or after a date", one "created after a date".
- This differs from the lesson page's run (haiku 0 of 5 passed, loaded 0 of 5). The video shows only our run; it
  does not cite the earlier one. Its conclusion (s21) is sized to ours: loading matters, it is not the whole
  story, and the app's wording matters as much as the skill's. **Lesson 23 and 26 comparisons with "lesson 22"
  should use these figures**, not the page's.
- The report's Skills column reads `changelog-entry (3×)` for haiku and `(5×)` for terra.

## Demo folder end state

- New, byte-identical to `verified/lesson-22/practice` and this video's `src/state/`:
  `evals/release.eval.yaml` and `evals/grading/check-release.mjs`.
- New results folder `results/lesson-22/` with one run (above). Nothing was moved aside (it did not exist before).
- Nothing else changed: `tools/list-merged.mjs`, `skills/`, `.vally.yaml`, `CONVENTIONS.md`, the other eval
  files and `app/` are as lesson 21 left them. No `npm install` was run.
- Tape logs: `/tmp/vl-l22/s15.log`, `s16.log` (s16's is copied to `src/run/s16.log`).

## Recording state of this video

- s15, s16, s18 recorded once; s17 twice, the second at FontSize 25 because our patch is 20 lines and the command
  scrolled off at 30 (a layout retake of a free tape; same saved run). Tapes need no re-recording.
- Credential scans: s15, s17, s18 fully scanned, no hits. s16 was partly scanned (output scrolled); all 12 stills
  were looked at (command, progress, failure block, summary table, `~/src/demo` path, run ID) and it is marked
  reviewed. No hits.
- `src/run/PROVISIONAL` is gone; generator asserts pass on the real run; narration is current; strict lint exits 0.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
