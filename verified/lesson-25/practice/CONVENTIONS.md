# Conventions

## What earns a grader
A failure we have seen in a real trial. One grader per failure mode, named after it.

## Code first, judge second
A judge only for what code cannot decide, with one yes-or-no criterion.

## Where files live
evals/ beside skills/, never inside a skill. Grading scripts in evals/grading, brought in through the grading environment.

## Before trusting a grader
The oracle, with and without the golden patch. A grader that checks for absence must also fail a saved trial known to be bad.

## Before trusting a judge
Our own labels first. TPR and TNR reported with the number of labels. Label again when the rubric or the judge model changes.

## What we run and when
The quick suite after every edit to the skill. The full suite before sharing and when a model changes. With-and-without after a large rewrite.

## How we report a result
Counts, per model. "These trials cannot tell" when the ranges overlap.

## Models and dates
claude-haiku-4.5 and gpt-5.6-terra, judged by claude-sonnet-5.5, checked on 2026-11-10.
