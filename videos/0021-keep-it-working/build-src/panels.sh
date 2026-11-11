#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/ holds the files the tapes install into the practice folder (build-src/make-state.py),
# so the panels show what the runs used.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
# s06: the tags line under three of the five stimulus names (the minimap shows the file goes on).
fp --file src/state/changelog.eval.yaml --label 'evals/changelog.eval.yaml' --id tags --width 46 --rows 9 \
   --show 11-12,43-44,68-69 --expect '11=typo-fix' --expect '12=tags: { tier: quick }' \
   --expect '44=tags: { tier: quick }' --expect '69=tags: { tier: quick }' \
   --mark '12=tag:tags' --mark '12=tier:tier: quick' --mark 44=all --mark 69=all --into scenes/s06.html
# s09: typo-fix's time limit and its three budget graders.
fp --file src/state/changelog.eval.yaml --label 'evals/changelog.eval.yaml' --id budgets --width 60 --rows 9 \
   --show 11,16-17,33-41 --expect '17=max_agent_duration: 1m' --expect '35=max: 215000' \
   --expect '38=max: 10' --expect '41=max: 30s' \
   --mark '17=stop:max_agent_duration: 1m' --mark 33-35=tok --mark 36-38=turns --mark 39-41=wall --into scenes/s09.html
# s15: the same grader with its max lowered for a moment.
fp --file src/state/changelog.lowered.eval.yaml --label 'evals/changelog.eval.yaml' --id lowered --width 46 --rows 9 \
   --show 11,33-35 --expect '11=typo-fix' --expect '33=token-budget' --expect '35=max: 70000' \
   --mark '35=max:max: 70000' --into scenes/s15.html
# s20: the conventions page, scrolled through.
fp --file src/state/CONVENTIONS.md --label 'CONVENTIONS.md' --id conv --width 63 --rows 9 \
   --expect '3=What earns a grader' --expect '30=Models and dates' \
   --mark 30=models --into scenes/s20.html
echo panels-ok
