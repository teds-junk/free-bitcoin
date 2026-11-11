# Publish kit: Grade a run Vally did not start

## Title options
1. Grade a run Vally didn't start: scoring an app's own agent session
2. From OpenTelemetry traces to a graded trajectory (Vally & Agent Evals, lesson 25)
3. The app ran by itself. Can the same eval file grade it?

## Description
Until now Vally has prepared the workspace, started the agent, recorded the trajectory and graded it. A real release tool does its own setup and starts its own agent; what's left is the changed checkout and the app's own record. In this lesson we read a trajectory in the ATIF format, follow a model call and a tool call from the app's OpenTelemetry trace into a step, then run the app, convert its traces, and grade the run with the eval file we already have. Every grader worked: the app's run scored three of five, failing the same two graders most of Vally's own trials failed. Cost, wall time and skill loading did not all come across, and the video shows why. Lesson 25 of Vally & Agent Evals.

Source: lessons/0025-grade-a-run-vally-did-not-start.html (Vally & Agent Evals). Vally docs, "CLI: grade" and "Trajectory Format". OpenTelemetry, semantic conventions for generative AI (status: Development).

## Chapters
0:00 A run nobody started in Vally
1:12 Read a trajectory from outside
3:37 From traces to steps
7:40 The script the release tooling runs
8:19 Run the app, convert, grade
12:08 What carried over

## Captions
Upload `0025-grade-a-run-vally-did-not-start.srt` in YouTube Studio → Subtitles. YouTube ignores the embedded caption track.
