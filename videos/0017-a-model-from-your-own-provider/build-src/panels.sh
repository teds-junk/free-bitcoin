#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/run/record.json is part of one record of <run>/qwen-local/results.jsonl, laid out (a stand-in while
# src/run/PROVISIONAL exists). src/state/cost.experiment.yaml is the experiment file after this lesson.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/run/record.json --label qwen-local/results.jsonl --id rec --width 44 --rows 9 \
   --expect '2="tokenUsage"' --expect '6="cacheReadTokens": 0' --expect '9="byModel"' \
   --mark 2=tu --mark 6=cache --mark 9=bym --mark 16=end --into scenes/s08.html
for s in s09 s10; do
  fp --file src/state/cost.experiment.yaml --label evals/cost.experiment.yaml --id exp --width 44 --rows 9 \
     --show 5-13,33-44 --expect '9=/defaults/executor' --expect '35=qwen-local' \
     --mark 6=vary --mark 9=pexec --mark 10=ptime --mark 11=pruns --mark 35=qname --mark 38=timeout --mark 39=runs \
     --mark '44=url:baseUrl: http://localhost:11434/v1' --into scenes/$s.html
done
echo panels-ok
