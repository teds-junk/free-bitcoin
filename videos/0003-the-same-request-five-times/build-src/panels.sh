#!/bin/bash
# Regenerate the file panel (make-scenes.py clears it). Run from the video directory.
# src/record.json is the gpt-5.6-terra trial's one-line record from the lesson 1 video's run,
# pretty-printed and otherwise untouched: the same copy lesson 2's video shows.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/record.json --label 'results.jsonl · one record, spread out' --id record --width 48 --rows 9 \
   --show 1-2,8-11,517-519 --expect '518="output"' --mark '518=output:"output"' --into scenes/s07.html
echo panels-ok
