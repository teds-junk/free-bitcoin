# Mission: Vally & Agent Evals

## Why
Ted builds agent skills and works near teams that are adopting evals. A skill that works when he tries it can behave differently on another model, on the fifth run, or after an edit, and today he cannot tell. He wants evals he can trust: a way to measure a skill, improve it, and show that the improvement is real, using a Vally setup he can hand to a teammate and judgement that outlasts any one tool.

## Success looks like
- Run one skill on two models and across repeated runs, and say from the saved files what each run did.
- Explain every line of an eval file, and find any run's request, changes and verdict in the results folder.
- Read saved runs, name what goes wrong, and turn each failure into a check that code can decide.
- Keep checks where the agent cannot read or edit them, and prove each one passes a correct answer and fails an untouched file.
- Show that a skill loads when it should, stays out of the way on near-miss requests, and gives better results than no skill.
- Evaluate a conversation with follow-up requests, checking each turn.
- Write a yes/no LLM judge, measure its agreement with his own labels (TPR and TNR), and say what that evidence supports.
- Read a result from a small, noisy set of runs and state honestly what it supports; choose `runs` on purpose.
- Grade partly-right work with a scaled judge and a threshold, without hiding a failing check in an average.
- Say what a passing trial costs, in tokens, AIU and dollars, for each model and setting; put budgets and time limits on trials; run a model through his own provider.
- Gate a change on "no worse than before" with a side-by-side judged comparison.
- Diagnose a run that ends in ERROR, FLAKY or a surprising FAIL, cheapest check first.
- Set up a quick suite and a full suite, and write a one-page conventions file a teammate can adopt.
- Evaluate the same skill inside an application: prepare the app's situation with setup commands, check the steps the agent took, make tools fail on purpose, grade a run the app made itself from its OpenTelemetry traces, and let Vally run the app through a small executor.

## Subject map
Targets the latest Vally: **0.21.0**, checked against the npm registry on 2026-11-09.

- **Facts**:
  - Install: `@microsoft/vally-cli`, Node 22.15 or newer, a GitHub Copilot sign-in. Runs spend Copilot requests.
  - The eval file (`eval.yaml`): `defaults`, `agent_environment`, `grading_environment`, `stimuli`, `prompt` or `turns`, `graders`, `rubric`, `golden_patch`.
  - The results folder: the report, `results.jsonl`, and one folder per trial holding `workspace.patch`, `events.jsonl` and `metadata.json`.
  - The built-in graders the course uses (including `run-command`, `tool-calls`, `max-repeat`, `loop-outcome` and the budget graders), and where the rest are listed.
  - Cost: `tokenUsage`, `cost` in nano-AIU, 1 AIU = 1 GitHub AI Credit = $0.01 (checked 2026-11-10); `scoring`, `constraints`, `reasoning_effort`, a `provider` block.
  - Outside Vally: `commands:`, `simulation`, ATIF, OpenTelemetry GenAI spans, the executor interface.
  - CLI: `init`, `lint`, `eval`, `oracle`, `grade`, `experiment run`, `compare`, `simulate record`; `--model`, `--runs`, `--workers`, `--workspace`, `--suite`, `--require-pass`, `--fail-on-regression`.
  - `PASS`, `FLAKY`, `FAIL`, `ERROR`, and exit codes.
- **Concepts**:
  - A skill's behaviour depends on the model and varies between runs; one run is one sample.
  - Read runs before writing checks; failure modes.
  - Check the result with code first; a judge only for what code cannot decide.
  - What the agent can see and edit; checks kept out of its reach.
  - A check can be wrong in two ways, and can be tested without running an agent.
  - Loading the skill and benefiting from it are separate questions; near-miss requests; a no-skill baseline.
  - Conversations: later turns can undo or ignore earlier work.
  - A judge is a model and must be measured against human labels.
  - What a small sample can and cannot show.
- **Procedures**:
  - Running an eval on several models with several trials and reading the saved files.
  - Reading runs and naming failure modes; editing the skill; re-measuring.
  - Writing code checks; hiding a script check; proving checks with `vally oracle`; re-checking saved runs with `vally grade`.
  - Loading evals with near-miss requests; with-and-without-skill experiments.
  - Multi-turn evals with checks scoped to a turn.
  - Writing a judge and measuring it against labels.
  - Tagging requests into quick and full suites; writing team conventions.

## Audience
- **Shareable**: the course should work for anyone given the course folder. It creates its own examples and names nothing private.

## Constraints
- About six hours end to end (the lessons' own times add to 355 minutes), in twenty-six lessons of 10 to 25 minutes (changed 2026-11-10 from three hours in fifteen, when Ted asked for cost, debugging, the high-value gaps against the official docs, and a part on evaluating an AI app; earlier, 2026-11-09, from two hours in eight).
- One running example from the first lesson to the last: a small `changelog-entry` skill the course creates in `./practice/`. Part 2 uses the same skill inside a small release app the course ships; no new example.
- Every feature is taught as a way to improve that skill.
- Only the latest Vally. Nothing about earlier versions.
- Plain commands with literal paths. Files are shown before they are queried.
- Eval-practice claims cite dated sources and say when a finding is recent, contested or thinly evidenced.

## Out of scope
- Model training, fine-tuning and training-time benchmarks.
- Other eval frameworks, except as contrast.
- Writing custom grader or reporter plugins. (A small executor in plain JavaScript is in scope since 2026-11-10, for lesson 26; the `program` grader has been in scope since lesson 6.)
- Continuous integration set-up beyond a snippet on a reference sheet: it cannot be run without a hosted repository.
