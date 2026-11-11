# Lesson 19's runs, for lesson 21 and later

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`), judging lesson 15's saved trials in `results/lesson-15/2026-11-11T07-53-29-176Z`.
No agent runs. Judge: `claude-sonnet-5.5`. One take of each command.

| Scene | Baseline -> treatment | Check | Pairs | Wins / ties / losses | Mean score [95% range] | Grader flips | Tokens per trial [range] | Exit |
|---|---|---|---|---|---|---|---|---|
| s14 | haiku-before -> haiku-after | off | 9 | 4 / 4 / 1 | +0.33 [-0.08, +0.75] | +4/-0, p=0.125 | -13,685 [-17,686, -9,685] | 0 |
| s17 | terra-before -> terra-after | on | 6 | 2 / 3 / 1 | +0.07 [-0.25, +0.38] | +1/-0, p=1.000 | -8,298 [-15,217, -1,378] | 0 |
| s18 | haiku-after -> haiku-before | on | 9 | 1 / 4 / 4 | -0.33 [-0.75, +0.08] | +0/-4, p=0.125 | +13,685 [+9,685, +17,686] | 0 |

- **`--fail-on-regression` did not exit 1 in any of our runs.** The only exit 1 the video shows is the course's
  earlier run of the swapped comparison (-0.49 [-0.90, -0.07]; `src/earlier/swapped.json`), labelled as such.
  Lesson 21 cannot point at "the check we watched fail" from this video.
- s17 judged 6 pairs: three terra-before trials ended in ERROR in lesson 15's run, and compare printed
  "3 treatment trajectory(s) had no baseline match" (cache trial 2, dates trial 2, parser trial 1). Exit code 0.
- Tokens fell after the edit on both models in our run. "Tokens rose and the check still passed" is shown from the
  course's earlier run (`src/earlier/terra.log`: +11,132 [+665, +21,599], exit 0).
- Judge calls: 18 + 12 + 18 = 48. s14 took about two minutes.
- Pass counts in the record: haiku 5 of 9 before, 9 of 9 after (ranges 27% to 81%, 70% to 100%).

## Files
- `src/run/s14.log`, `s17.log`, `s18.log`: what each compare printed, with an `exit=N` line from the tape's wrapper.
- `src/run/haiku-compare.jsonl`, `terra-compare.jsonl`: the records (`/Users/Shared/demo` rewritten to `~/src/demo`).
- `src/run/pair-before.patch`, `pair-after.patch`: the dates trial 0 patches the video quotes.

## Demo folder end state
- Added inside `results/lesson-15/2026-11-11T07-53-29-176Z/`: `haiku-compare.jsonl` and `terra-compare.jsonl`.
  **`results/lesson-15` listings now show these two files**; a later tape that lists that folder should expect them.
- Nothing else changed: `evals/`, `skills/`, and every other results folder are as lesson 18 left them.
- Nothing was moved aside (no `/Users/Shared/.demo-old.l19.*`).
- Tape logs are in `/tmp/vl-l19/`.

## Recording state of this video
- s13, s14, s17, s18 are recorded once each and must not be re-recorded. s13, s14, s18: credential scan full, no
  hits. s17: partly scanned, all 12 stills looked at, marked reviewed.
- Narration is current; strict lint exits 0; generator asserts pass on the real run; `src/run/PROVISIONAL` is gone.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
