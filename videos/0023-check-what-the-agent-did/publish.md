# Publish kit: Check what the agent did

## Title options
1. Check what the agent did: grading the route, not only the result
2. Required, forbidden, or too long: tool-call graders for an agent (Vally & Agent Evals, lesson 23)
3. Did it read the list? Did it commit? Trajectory graders, tested before they run

## Description
A hidden test sees only the finished changelog. It can't say whether the entries came from the app's list, or whether the agent tried to commit or push. In this lesson we grade the route, but only where the app depends on a step: one grader requires a call that opens the list, one forbids a commit or push, one catches a loop, and one requires the skill to load. We test all of them for free on an untouched workspace and on ten saved trials before spending a run. Across sixteen trials the two guards never fired; the route showed something else: one model loaded the skill in four of eight trials, and passed only three. Lesson 23 of Vally & Agent Evals.

Source: lessons/0023-check-what-the-agent-did.html (Vally & Agent Evals). Anthropic, "Demystifying evals for AI agents" (2026). Vally docs, "Choose a Grader" and "Grader: tool-calls".

## Chapters
0:00 Check the route
0:32 When a step is worth grading
1:42 Read a tool-calls grader
4:32 Catch a loop
5:59 Test graders before they run
10:14 What the route showed

## Captions
Upload `0023-check-what-the-agent-did.srt` in YouTube Studio → Subtitles. YouTube ignores the embedded caption track.
