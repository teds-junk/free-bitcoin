#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/with-and-without.experiment.yaml is the practice folder's experiment file, untouched
# (verified/lesson-10/practice/evals). The same panel sits in s06, s07 and s08 so the cuts between
# them are invisible; s08 scrolls it to the variants.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
for s in s06 s07 s08; do
  fp --file src/with-and-without.experiment.yaml --label 'with-and-without.experiment.yaml' --id exp \
     --width 46 --rows 8 \
     --expect '6=vary: [/environment/skills, /defaults/model]' --expect '15=skills: []' \
     --mark '4=evals:changelog.eval.yaml' --mark '6=vary' --mark '8=baseline' \
     --mark '11=vname:haiku-no-skill' --mark '13=model' --mark '15=noskill:skills: []' \
     --mark '20=skill:skills: [../skills/changelog-entry]' --mark '21=terra' --mark '26=terra' \
     --into scenes/$s.html
done
echo panels-ok
