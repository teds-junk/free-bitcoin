#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# s11: src/run/wording-labels.md   notes/wording-labels.md as the lesson 12 video left it.
# s16: src/state/wording-labels.md the same file with the decision as its last line (written by
#      make-scenes.py from the run's counts, or from src/run/decision.txt).
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
LAST=$(wc -l < src/state/wording-labels.md | tr -d ' ')
fp --file src/run/wording-labels.md --label notes/wording-labels.md --id labels --lang text --width 62 --rows 9 \
   --expect '5=| Ours | Judge |' --mark '5=ours:Ours' --mark '5=judge:Judge' --into scenes/s11.html
fp --file src/state/wording-labels.md --label notes/wording-labels.md --id decided --lang text --width 62 --rows 9 \
   --show "1-5,$((LAST-3))-$LAST" --expect "$LAST=the judge" --mark "$LAST=decision" --into scenes/s16.html
echo panels-ok
