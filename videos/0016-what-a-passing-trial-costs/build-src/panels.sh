#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/state/cost.experiment.yaml is the experiment file the lesson adds (verified/lesson-16), untouched.
# src/run/record.json is one trial's record from haiku-low/results.jsonl, spread over lines; its line
# numbers differ from run to run, so make-scenes.py finds them and writes build-src/record-lines.env:
#   V "variant"   ST "status"   P "passed"   B "byModel"   C "cost"   A "amount"   E the cost block's end
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
. build-src/record-lines.env
REC=(--file src/run/record.json --label 'haiku-low/results.jsonl · one record, spread out' --id record --width 48 --rows 9
     --show "$V-$P,$B-$E" --expect "$V=haiku-low" --expect "$P=true" --expect "$((C+2))=nano-aiu" --expect "$A=amount"
     --mark "$V=variant" --mark "$ST=status" --mark "$P=passed" --mark "$B=bymodel"
     --mark "$((C+2))=unit:\"nano-aiu\"" --mark "$A=amount")
fp "${REC[@]}" --into scenes/s07.html
fp "${REC[@]}" --into scenes/s08.html
fp --file src/state/cost.experiment.yaml --label evals/cost.experiment.yaml --id experiment --width 46 --rows 9 \
   --expect '4=changelog.eval.yaml' --expect '11=runs: 3' --expect '16=claude-haiku-5.5' --expect '26=terra-high' \
   --mark '4=evalf:changelog.eval.yaml' --mark 6=vary --mark '11=runs:runs: 3' \
   --mark '14=vhaiku:haiku-low' --mark '18=vhaiku:haiku-high' --mark '22=vterra:terra-low' --mark '26=vterra:terra-high' \
   --mark '16=newer:claude-haiku-5.5' --into scenes/s13.html
echo panels-ok
