# Lesson 24's run, for lessons 25 and 26

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Spend: 6 agent runs and 6 judge calls, one take. No ERROR trials; nothing was re-run
for its outcome.

## The recordings

| Scene | Command | Result |
|---|---|---|
| s17 | `vally lint -e evals/release.eval.yaml` | one warning, `scoring-defaults-applied`; no errors |
| s18 | `vally eval -e evals/release.eval.yaml --tag case=tool-fails --model claude-haiku-4.5,gpt-5.6-terra --runs 3 --workers 2 --output-dir results/lesson-24` | run `results/lesson-24/2026-11-11T17-49-59-016Z`, run ID `98cbfc4b-cf68-48b3-a42d-9f635e48e682`, 6 of 6 finished in about 1:20. Both models `✓ 1/1`; no failure listed |
| s20 | `vally simulate record results/lesson-22/2026-11-11T16-51-44-338Z/` (Tab) | a block with two patterns (a `find`, and a `cd <trial folder> && cat changelog-entry/CHANGELOG.md`, the folder shown as `/tmp/trial`), then six warnings (view 31, edit 5, bash structured content 2, skill 8, apply_patch 5 twice) |

## What the run showed (src/run/results.jsonl; make-scenes.py asserts each figure)

- All six trials passed all four graders: `tries-the-tool`, `writes-nothing`, `stops-retrying`, `says-why`.
  No trial left a patch. No merged change number appears in any trial.
- **haiku**: ran the failing command 3, 4 and 2 times (never more than twice with no other call between);
  opened `tools/list-merged.mjs` with `view` in 3 of 3 trials and got the copy that asks the tracker; each
  reply begins "The tracker …" and asks the user for the list. It did not load the skill (it read
  `changelog-entry/SKILL.md` as a file in two trials).
- **terra**: loaded the skill 3 of 3; ran the command 2, 3 and 1 times; never opened the script. Replies are
  one or two sentences; two begin "Blocked:"; all three blame "the command runner" timing out.
- No trial used a web tool. The page's `web_fetch` trial did not recur and is not in the video.
- This differs from the lesson page (haiku FLAKY, one reply failed by the judge). The video states ours, and
  shows the page's failed reply only as "an earlier run", from its saved console output
  (`src/earlier/eval-console.txt`). The page's other earlier attempts have no saved evidence and are not cited.
- **Lessons 25 and 26: comparisons with "lesson 24" should use these figures** (tracker-down: 6 of 6 passed).

## Demo folder end state

- `evals/release.eval.yaml` is byte-identical to `verified/lesson-24/practice/evals/release.eval.yaml` and
  this video's `src/state/release.eval.yaml`: two stimuli (`since-last-release` with the stand-in staged per
  stimulus; `tracker-down`, tagged `case: tool-fails`, with its simulation block), `judge_model:
  claude-sonnet-5.5` under defaults. Lesson 23's version is kept in `src/state/release.eval.before.yaml`.
- New: `results/lesson-24/` with one run (above). Nothing was moved aside (it did not exist before).
- `results/lesson-22/` and `results/lesson-23/` are untouched, one run each.
- Nothing else changed. Tape logs: `/tmp/vl-l24/s17.log`, `s18.log`, `s20.log` (copied to `src/run/`).

## Recording state of this video

- s17, s18, s20 recorded once each. Credential scans: s17 fully scanned, no hits. s18 and s20 partly scanned
  (output scrolled); all 12 stills of each were looked at and each is marked reviewed. No hits.
- `src/run/PROVISIONAL` and the stand-in files are gone; generator asserts pass on the real run; narration is
  current; strict lint exits 0; `preview.js --all` reports no problems.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
