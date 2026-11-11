#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/list-merged.mjs is the release tool as the practice folder has it; release.eval.yaml and
# check-release.mjs are the two files the tapes install (from verified/lesson-22/practice), so the
# panels show what the run used.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/state/list-merged.mjs --label 'tools/list-merged.mjs' --id tool --width 52 --rows 9 \
   --show 5-11 --expect '6=#74 feat' --expect '8=#76 refactor' \
   --mark 6-7=ff --mark 8=rf --into scenes/s05.html
fp --file src/state/release.eval.yaml --label 'evals/release.eval.yaml' --id spec --width 62 --rows 9 \
   --show 6-23 --expect '12=../tools/list-merged.mjs' --expect '17=prompt: >-' --expect '23=node tools/list-merged.mjs' \
   --mark 12-13=tool --mark 17-19=prompt --mark 21=cmds \
   --mark '22=q:"mkdir -p release"' --mark '23=q:"node tools/list-merged.mjs > release/merged.txt"' --into scenes/s07.html
fp --file src/state/release.eval.yaml --label 'evals/release.eval.yaml' --id spec2 --width 62 --rows 9 \
   --show 24-32 --expect '24=grading_environment' --expect '29=run-command' \
   --mark 24-27=genv --mark '30=gname:every-change-handled' \
   --mark '32=cmd:node .vally-grading/check-release.mjs' --into scenes/s11.html
fp --file src/state/check-release.mjs --label 'evals/grading/check-release.mjs' --id test --width 62 --rows 9 \
   --expect '6=release/merged.txt' --expect '13=item.match' --expect '28=process.exit(1)' \
   --mark 6=list --mark 7=log --mark 8-10=unrel --mark '13=parts:number, type' --mark 15=found \
   --mark 16-17=ref --mark 18-19=one --mark 20-21=share --mark 28=exit --into scenes/s12.html
echo panels-ok
