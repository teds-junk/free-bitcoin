#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/before-and-after.experiment.yaml is the starter's experiment file, untouched.
# src/state/SKILL.md is the skill after this lesson's edit (tapes/s13.tape copies it into practice out of sight).
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/state/before-and-after.experiment.yaml --label before-and-after.experiment.yaml --id exp --width 50 --rows 9 \
   --expect '4=wording.eval.yaml' --expect '11=runs: 3' --expect '18=changelog-entry-before' --expect '23=changelog-entry]' \
   --mark '4=eval:wording.eval.yaml' --mark '11=runs:runs: 3' \
   --mark '18=before:../skills/changelog-entry-before' --mark '23=after:../skills/changelog-entry' --into scenes/s07.html
fp --file src/state/SKILL.md --lang markdown --label changelog-entry/SKILL.md --id skill --width 46 --rows 9 --show 15-20 \
   --expect '16=One line per change' --expect '18=Name no library' \
   --mark 16=old --mark 17=new1 --mark 18=new2 --into scenes/s11.html
echo panels-ok
