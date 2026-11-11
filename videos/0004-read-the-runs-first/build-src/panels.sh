#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/six-requests.eval.yaml and src/SKILL.md are the practice folder's files, untouched.
# src/state/notes/failures.md is the notes file the lesson writes (s13.tape copies it into practice/notes/).
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/six-requests.eval.yaml --label six-requests.eval.yaml --id evalfile --width 50 --rows 9 \
   --show 1-18,62-70 --expect '11=typo-fix' --expect '69=just-released' \
   --mark '11=typo:name: typo-fix' --mark 15-18=env --mark '8=skill:- ../skills/changelog-entry' \
   --mark '69=released:fixtures/just-released/CHANGELOG.md' --into scenes/s07.html
fp --file src/state/notes/failures.md --label notes/failures.md --id notes --rows 9 \
   --show 3-7 --expect '3=1. No rule' --expect '7=5. New Unreleased' \
   --mark 3=m1 --mark 4=m2 --mark 5=m3 --mark 6=m4 --mark 7=m5 --into scenes/s20.html
fp --file src/SKILL.md --label changelog-entry/SKILL.md --id skill --width 42 --rows 9 \
   --expect '12=Reference' --mark 10=place --mark 11=users --mark 12=reference --into scenes/s21.html
echo panels-ok
