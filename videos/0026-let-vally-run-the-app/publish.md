# Publish kit: Let Vally run the app

## Title options
1. Let Vally run the app: a custom executor for the agent you ship
2. Writing an executor plugin so trials run your app's own code (Vally & Agent Evals, lesson 26)
3. The eval measures what ships: trials, experiments and models, through the app

## Description
Grading an app's run afterwards gives one sample. To get trials, experiments and other models, Vally has to start the app itself. In this lesson we write an executor plugin: a small module whose one function calls the app's own code and hands back a trajectory, and we join the app's traces to Vally's with a trace context. Then the same eval file runs through the app, on two models. In our run one model passed every trial either way; on the other, the counts are still too few to say whether the app makes it worse; and every call through the app carried more tokens, because the app's sessions add five extra tools. Lesson 26 of Vally & Agent Evals.

Source: lessons/0026-let-vally-run-the-app.html (Vally & Agent Evals). Vally docs, "Writing Custom Executors". W3C, "Trace Context".

## Chapters
0:00 Plug the app into Vally
0:30 The executor is the seam
1:48 What an executor returns
5:28 Join the app's traces to Vally's
7:02 Run the app as Vally's executor
10:52 What the counts show

## Captions
Upload `0026-let-vally-run-the-app.srt` in YouTube Studio → Subtitles. YouTube ignores the embedded caption track.
