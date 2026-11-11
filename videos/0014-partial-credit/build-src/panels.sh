#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/wording-scaled.scoring.eval.yaml  the scaled copy with the scoring block at its end (s07)
# src/state/wording-scaled.eval.yaml          the scaled copy as the lesson leaves it (s10)
# src/state/notes/wording-labels.md           the notes file as the lesson leaves it; written by make-scenes.py (s21)
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
S=src/state/wording-scaled.scoring.eval.yaml
L=$(grep -n '^scoring:' $S | cut -d: -f1)
fp --file $S --label wording-scaled.eval.yaml --id scoring --width 44 --rows 9 \
   --show $L-$((L+4)) --expect "$((L+2))=prompt: 0.5" --expect "$((L+4))=threshold: 0.6" \
   --mark $((L+1))=weights --mark "$((L+2))=wprompt:prompt: 0.5" --mark "$((L+3))=wdiff:diff-contains: 0.5" \
   --mark "$((L+4))=thresh:threshold: 0.6" --into scenes/s07.html
fp --file src/state/wording-scaled.eval.yaml --label wording-scaled.eval.yaml --id judge --width 46 --rows 9 \
   --show 24-29 --expect '25=type: prompt' --expect '27=scoring: scale_1_5' --expect '28=threshold: 0.75' \
   --mark '27=scale:scoring: scale_1_5' --mark '28=jthresh:threshold: 0.75' --into scenes/s10.html
N=src/state/notes/wording-labels.md
H=$(grep -n '^| Stimulus' $N | cut -d: -f1)
E=$(wc -l < $N | tr -d ' ')
fp --file $N --label notes/wording-labels.md --id notes --rows 9 \
   --show $H-$((H+2)),$E --expect "$H=1 to 5" --expect "$E=verdict changed" \
   --mark "$H=col:1 to 5" --mark $E=sentence --into scenes/s21.html
echo panels-ok
