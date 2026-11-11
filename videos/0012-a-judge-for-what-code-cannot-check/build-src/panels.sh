#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/04-judge.wording.eval.yaml is evals/wording.eval.yaml with the judge added (verified/lesson-12);
# src/state/00-start.wording.eval.yaml is the file as the practice folder ships it (verified/lesson-11).
# Width 62 keeps every line of the file on one row; the minimap shows that the view is partial.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
J=src/state/04-judge.wording.eval.yaml
MARKS=(--mark 5=judge --mark 17-20=request --mark 21-23=rubric --mark '25=ptype:type: prompt'
       --mark '27=binary:scoring: binary' --mark 28=instr --mark 29-32=cites)
for s in s05 s06 s07; do
  fp --file $J --label 'wording.eval.yaml · with a judge added' --id spec --width 62 --rows 9 --show 1-32 \
     --expect '5=judge_model' --expect '25=type: prompt' "${MARKS[@]}" --into scenes/$s.html
done
fp --file src/state/00-start.wording.eval.yaml --label 'wording.eval.yaml' --id ship --width 62 --rows 9 \
   --show 14-19,26-31,38-43 --expect '14=name: parser' --expect '42=tokenizer' \
   --mark '16=p1:streaming' --mark '17=p1:parser' --mark '28=p2:LRU cache' --mark '42=p3:small tokenizer' \
   --into scenes/s11.html
fp --file $J --label 'wording.eval.yaml · with a judge added' --id added --width 62 --rows 9 \
   --show 3-5,21-28,40-47,59-66 --expect '40=rubric' --expect '63=type: prompt' \
   --mark 5=judge --mark 21-23=add1 --mark 25-28=add1 --mark 40-42=add2 --mark 44-47=add2 \
   --mark 59-61=add3 --mark 63-66=add3 --into scenes/s17.html
echo panels-ok
