# Publish kit: Does the skill load when it should

## Title options
1. Does the skill load? Testing when an agent opens a skill, and when it shouldn't
2. Near-miss requests: a loading test for agent skills with Vally (Vally & Agent Evals, lesson 9)
3. The description decides: skill-invocation graders and what a rewrite changed

## Description
An agent chooses among its installed skills by their descriptions, so a skill can fail in two new ways: it doesn't load when it should, or it loads when it shouldn't. In this lesson we write six requests, three that should load our skill and three near-misses that shouldn't, install two neighbouring skills so the choice is real, and grade loading with `skill-invocation`. Then we rewrite the description and run again. In our run the one-line description loaded correctly in every trial that finished, and after the rewrite the test caught the skill loading once for a near-miss request: a small sample, and exactly what the test is for. Lesson 9 of Vally & Agent Evals.

Source: lessons/0009-does-the-skill-load.html (Vally & Agent Evals). agentskills.io, "Optimizing skill descriptions". Vercel (2026, the vendor's own figure, run counts not published) for skills going unused.

## Chapters
0:00 The description decides
3:08 How a trial records loading
5:31 Test loading, then fix it
9:51 What the loading test showed

## Captions
Upload `0009-does-the-skill-load.srt` in YouTube Studio → Subtitles. YouTube ignores the embedded caption track.
