#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/release.eval.yaml is the eval file the tapes install into the practice folder
# (verified/lesson-24/practice), so the panels show what the run used. The two copies of the tool are
# the course's stand-in (practice-starter/tools) and the fixture staged for tracker-down.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
E=src/state/release.eval.yaml
fp --file $E --label 'evals/release.eval.yaml' --id stim --width 60 --rows 9 \
   --show 55-71 --expect '55=- name: tracker-down' --expect '56=tool-fails' --expect '58=Run `node tools/list-merged.mjs`' \
   --mark '55=name:tracker-down' --mark 56=tags --mark 58-60=prompt --into scenes/s04.html
fp --file src/tools-list-merged.mjs --label 'tools/list-merged.mjs' --id tool --width 60 --rows 9 \
   --expect '5=const merged = [' --expect '8=#76 refactor' --mark 6-8=list --into scenes/s09.html
fp --file src/fixture-list-merged.mjs --label 'fixtures/release/list-merged.mjs' --id fixture --width 64 --rows 7 \
   --expect '3=tracker.example' --expect '7=}' --mark 3=url --mark 5-7=loop --into scenes/s10.html
fp --file $E --label 'evals/release.eval.yaml' --id envs --width 46 --rows 9 \
   --show 7-25 --expect '7=agent_environment:' --expect '15=since-last-release' --expect '21=../tools/list-merged.mjs' \
   --mark 10-12=shared --mark 20-22=own --into scenes/s11.html
fp --file $E --label 'evals/release.eval.yaml' --id graders --width 46 --rows 9 \
   --show 76-89 --expect '78=tries-the-tool' --expect '84=writes-nothing' --expect '89=max_acceptable_retries: 2' \
   --mark '78=g1:tries-the-tool' --mark '84=g2:writes-nothing' --mark '86=g3:stops-retrying' --into scenes/s12.html
# what vally simulate record printed in s20 (the tape's own log), whole: block, then warnings
fp --file src/run/s20.log --lang yaml --label 'what vally simulate record printed' --id recorded --width 60 --rows 9 \
   --expect '6="command":"find ' --expect '11=cd /tmp/trial' --expect '15=Warning: Ignored successful non-shell tool "view"' \
   --mark 6=pat1 --mark 7-10=out1 --mark 11=pat2 --mark 15-16=warn --into scenes/s21.html
echo panels-ok
