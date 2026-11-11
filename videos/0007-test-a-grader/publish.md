# Publish kit: Test a grader without running an agent

## Title options
1. Who grades the grader? Testing agent-eval graders with vally oracle
2. Golden patches and the oracle: prove a grader passes correct work and fails missing work (Vally & Agent Evals, lesson 7)
3. A grader that can't fail: catching it for free

## Description
A grader can be wrong in two ways: it can fail correct work, or pass work that was never done. In this lesson we keep a saved trial's patch as a golden patch and use `vally oracle` to run the graders twice, once on that correct answer and once on an untouched file, with no agent and no cost. We watch it catch a grader that can never fail, extend it to four stimuli, and see which graders it could not test: the ones that check for absence. Lesson 7 of Vally & Agent Evals.

Source: lessons/0007-test-a-grader.html (Vally & Agent Evals). Vally docs: "CLI: oracle".

## Chapters
0:00 Who grades the grader?
1:26 A golden patch
2:36 What the oracle does
4:29 Prove the graders
9:19 What the oracle didn't test

## Captions
Upload `0007-test-a-grader.srt` in YouTube Studio → Subtitles. YouTube ignores the embedded caption track.
