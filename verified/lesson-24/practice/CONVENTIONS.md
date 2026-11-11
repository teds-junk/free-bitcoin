# Conventions for the changelog-entry evals

## What earns a grader
A failure we have seen in a real trial. One grader per failure mode, named after it.

## Code first, judge second
A judge only for what code cannot decide, with one yes-or-no criterion.

## Where files live
`evals/` beside `skills/`, never inside a skill. Grading scripts in `evals/grading`, brought in through the grading environment.

## Before trusting a grader
The oracle, with and without the golden patch. A grader that checks for absence must also fail a saved trial known to be bad. A new budget is re-graded against saved trials and must pass all the good ones.

## Before trusting a judge
Our own labels first. TPR and TNR reported with the number of labels. Label again when the rubric or the judge model changes.

## What we run and when
The quick suite with `--require-pass` after every edit to the skill. The full suite before sharing and when a model changes. A before-and-after experiment and `vally compare --fail-on-regression` before relying on an edit. With-and-without after a large rewrite.

## How we report a result
Counts, per model, with cost per passing trial. "These trials cannot tell" when the ranges overlap.

## What a run may cost
Budgets at about twice the largest typical trial: 215000 tokens, 10 turns, 30 seconds, and a 1-minute limit on the agent. Re-tested for free whenever the skill, the model or the effort changes. Cost per passing trial compared before switching models, with the judge's calls counted on top.

## When a run goes wrong
The four questions in order: is the eval valid, did it complete, why was the result unexpected, does the fix work. Read what the run saved before running anything again; an ERROR is re-run or left out and said so, never counted as a failure of the skill.

## Models and dates
claude-haiku-4.5 and gpt-5.6-terra, judged by claude-sonnet-5.5, checked on 2026-11-10, at $0.01 per AIU.
