# Lesson 25's run, for lesson 26

All figures are from our own recordings on 2026-11-11 in `/Users/Shared/demo/practice` (shown on screen as
`~/src/demo/practice`). Spend: 1 agent run, one take. No ERROR; nothing was re-run for its outcome.

## The recordings

| Scene | Command | Result |
|---|---|---|
| s16 | `npm install --prefix app` | `added 142 packages in 2s`; 69 looking for funding. No "audited" or "vulnerabilities" line was printed |
| s17 | `sh app/run.sh claude-haiku-4.5` (1 agent run) | reply "Done! I've added all three changes from `release/merged.txt` …" listing #74 under Added, #75 under Fixed, #76 under Changed; then `Wrote app-run/traces.jsonl and app-run/change.diff` |
| s20 | `node app/traces-to-atif.mjs app-run/traces.jsonl > app-run/trajectory.json` | prints nothing; writes the trajectory |
| s22 | `vally grade -e evals/release.eval.yaml --stimulus since-last-release --workspace app-run/repo --diff-file app-run/change.diff --verbose < app-run/trajectory.json` | `since-last-release (3/5 graders passed, 2 failed)`, `Score: 60.0% | FAILED`. Failed: `every-change-handled` (exit code 1) and `loads-the-skill` (changelog-entry not called). Passed: `reads-the-list`, `never-commits`, `no-loop` (max observed 1) |

## What the run showed (src/run/; make-scenes.py asserts each figure)

- `change.diff` changes only `CHANGELOG.md`: "Add `notes list --since <date>` to filter by date (#74)" under
  Added, a new `### Fixed` with #75, a new `### Changed` with "Move config loading out of cli.js (#76)".
- `traces.jsonl`: 143 lines (125 spans, 18 metrics); 109 lines are session timings. Five `chat` spans and five
  tool calls: view, view (the read of `release/merged.txt`), view, edit, view. No `skill` call. The `chat` and
  `execute_tool` spans' parent is `invoke_agent`, which has no parent. The file also has two other parentless
  spans (`session.provisioning`, `session.mcp_startup_wait`).
- `trajectory.json`: five steps; steps 1 to 4 hold the tool calls (view, view / view / edit / view), step 5 only
  the reply. Prompt plus completion tokens 86,627; `cost_usd` sums to 0.0336 (3.36 AIU). First model call:
  16,620 prompt tokens, 217 completion, 2.19 AIU. The video states none of the totals.
- Same verdict as the lesson page's run (3 of 5, same two failures), so the video cites no earlier run. The
  page's run had 140 lines, four tool calls and four steps; ours is stated.
- Comparison (s23) uses the lesson 23 video's run `results/lesson-23/2026-11-11T17-27-07-928Z`, haiku, three
  trials: `every-change-handled` 1 of 3, `loads-the-skill` 1 of 3, the other three graders 3 of 3. The page's
  0 of 3 is not used.
- **Lesson 26: one app run on haiku, graded afterwards: 3 of 5 graders, no skill load, refactor entry written.**

## Personal data

- The raw `app-run/traces.jsonl` holds an account attribute (`enduser.pseudo.id`, on `invoke_agent`), an
  email-like string and temp paths under `/var/folders` (both inside `gen_ai.system_instructions`), and 23
  `/Users/Shared/demo` paths. It was never printed in a tape and is not copied into this video.
- `src/run/span-chat.json` and `span-tool.json` keep values only for the attributes the panels show; every
  other attribute and field is "…". `trajectory.json` has paths rewritten and long values cut at 72 characters.
- Credential scans: s16, s17, s20 fully scanned, no hits. s22 partly scanned (the screen filled). All 12 stills
  of each of the four recordings were looked at; each is marked reviewed. Nothing personal on screen.

## Demo folder end state

- New: `app/node_modules/` (142 packages; nothing was moved aside, it did not exist before). **Lesson 26 does
  not need `npm install` again.**
- New: `app-run/` with `repo/`, `before/`, `skills/`, `traces.jsonl`, `change.diff`, `trajectory.json`.
  `app/run.sh` deletes and rebuilds `app-run/` on every run; move it aside first if lesson 26 runs the script.
- Unchanged: `evals/release.eval.yaml` (as lesson 24 left it), `evals/grading/`, `skills/`, `tools/`,
  `results/lesson-22`, `-23`, `-24` (one run each), the `app/*.mjs` and `app/run.sh` files.
- Tape logs: `/tmp/vl-l25/s16.log`, `s17.log`, `s22.log` (copied, cleaned, to `src/run/`).

## Recording state of this video

- s16, s17, s20, s22 recorded once each. Tapes need no re-recording.
- `src/run/PROVISIONAL` is gone; generator asserts pass on the real run; narration is current; strict lint
  exits 0; `preview.js --all` reports no problems.
- Not done: the full render, timing fit (`sync-report.js`), assembly, verify, transcript.
