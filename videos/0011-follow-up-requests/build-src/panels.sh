#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# conv     the conversation as the practice folder has it before this lesson (no graders)
# graders  the same file with the five graders added (what s14's tape installs)
# skill    the skill with the new rule at its end (what s17's tape installs)
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
for s in s06 s07; do
  fp --file src/state/conversation.start.eval.yaml --label conversation.eval.yaml --id conv --lang yaml \
     --width 58 --rows 9 --show 13-25 --expect '15=turns:' --expect '21=PR 65' \
     --mark '15=turns:turns:' --mark 16-19=r1 --mark 20-22=r2 --mark 23-25=r3 --into scenes/$s.html
done
for s in s10 s11; do
  fp --file src/state/conversation.eval.yaml --label conversation.eval.yaml --id graders --lang yaml \
     --width 44 --rows 9 --show 26-48 --expect '26=graders:' --expect '46=first-entry-survives' \
     --mark '29=turn0:turn: 0' --mark 31=pat64 --mark '34=turn1:turn: 1' \
     --mark '39=export:"notes export"' --mark 44=nopr --mark '46=survive:first-entry-survives' \
     --into scenes/$s.html
done
fp --file src/state/SKILL.md --label changelog-entry/SKILL.md --id skill \
   --width 62 --rows 9 --show 26-31 --expect '29=Treat every request' --mark 29-31=rule --into scenes/s16.html
echo panels-ok
