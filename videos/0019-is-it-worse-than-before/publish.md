# Publish kit: Is it worse than before

## Title options
1. Is it worse than before? A pairwise judge and a regression check for agent evals
2. `vally compare`: judging two saved runs side by side (Vally & Agent Evals, lesson 19)
3. Graders ask "is it right?"; a pairwise judge asks "is it worse?"

## Description
Graders look at one trial at a time, so two answers that both pass look the same to them. In this lesson we give a pairwise judge both versions' answers to the same request, in both orders, with `vally compare`, and read what it reports: a win rate, a mean score with its range, a second test on the graders alone, and the change in tokens. Then we turn on the regression check. In our run the judge leaned towards the edited skill on one model (+0.33, range −0.08 to +0.75) and could not tell on the other, and the check never failed, even with the versions swapped; an earlier run of the same swap did fail it. So we hold the result loosely, and note what the check ignores: cost. Lesson 19 of Vally & Agent Evals.

Source: lessons/0019-is-it-worse-than-before.html (Vally & Agent Evals). Zheng et al., "Judging LLM-as-a-Judge" (2023). Vally docs, "CLI: compare" and "Run Your First Experiment".

## Chapters
0:00 Is it any worse?
1:51 What compare reports
5:19 Compare before and after
9:25 What it supports

## Captions
Upload `0019-is-it-worse-than-before.srt` in YouTube Studio → Subtitles. YouTube ignores the embedded caption track.
