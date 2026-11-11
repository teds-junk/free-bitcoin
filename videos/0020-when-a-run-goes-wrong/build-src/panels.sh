#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/broken/ is practice-starter/evals/broken (the four files as the first runs use them);
# src/state/fixed/ is verified/lesson-20/practice/evals/broken (the files the tapes install as fixes).
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/state/broken/merged-list.eval.yaml --label 'broken/merged-list.eval.yaml' --id ml --width 60 --rows 9 \
   --show 7-13 --expect '12=commands:' --expect '13=- echo fix: notes add said tittle > merged.txt' \
   --mark '12=cmds' --mark '13=key:echo fix:' --into scenes/s16.html
fp --file src/state/fixed/merged-list.eval.yaml --label 'broken/merged-list.eval.yaml · fixed' --id mlf --width 60 --rows 9 \
   --show 7-13 --expect "13=- 'echo \"fix: notes add said tittle\" > merged.txt'" \
   --mark "13=q:'echo \"fix: notes add said tittle\" > merged.txt'" --into scenes/s17.html
fp --file src/state/broken/quick.eval.yaml --label 'broken/quick.eval.yaml' --id q --width 46 --rows 9 \
   --show 1-8 --expect '4=timeout: 5s' --mark '4=to:timeout: 5s' --into scenes/s22.html
fp --file src/state/fixed/quick.eval.yaml --label 'broken/quick.eval.yaml · fixed' --id qf --width 46 --rows 9 \
   --show 1-8 --expect '4=timeout: 3m' --mark '4=to:timeout: 3m' --into scenes/s23.html
fp --file src/state/broken/entry.eval.yaml --label 'broken/entry.eval.yaml' --id e --width 46 --rows 9 \
   --show 18-22 --expect "22=pattern: '^\\+.*notes add'" --mark "22=pat:'^\\+.*notes add'" --into scenes/s28.html
fp --file src/state/fixed/entry.eval.yaml --label 'broken/entry.eval.yaml · fixed' --id ef --width 46 --rows 9 \
   --show 18-22 --expect "22=pattern: '(?m)^\\+.*notes add'" --mark '22=m:(?m)' --into scenes/s29.html
fp --file src/state/fixed/judged.eval.yaml --label 'broken/judged.eval.yaml · fixed' --id jf --width 46 --rows 9 \
   --show 3-5,30-33 --expect '5=judge_model: claude-sonnet-5.5' --expect '30=- type: diff-contains' \
   --mark '5=jm:claude-sonnet-5.5' --mark '30=dg:diff-contains' --into scenes/s33.html
echo panels-ok
