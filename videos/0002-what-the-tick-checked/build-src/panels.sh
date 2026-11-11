#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# Sources are copies of the real files from the run the lesson 1 video recorded; record.json is the
# gpt-5.6-terra trial's one-line record from results.jsonl, pretty-printed with jq and otherwise
# untouched. /Users/Shared/demo is shown as ~/src/demo, the made-up folder this course's videos use.
# Labels are the shortest name that identifies the file.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }

EVAL=(--file src/one-request.eval.yaml --label one-request.eval.yaml --id eval --width 46 --rows 9 --expect '6=agent_environment')
fp "${EVAL[@]}" --mark 1=name --mark '4=timeout:timeout: 3m' --mark 6=agentenv --mark 8=skill --mark 10-11=file --into scenes/s02.html
fp "${EVAL[@]}" --mark 13=stimuli --mark 14=stim --mark 15-17=prompt --mark 18=graders --mark '19=gtype:file-contains' \
   --mark '20=gname:mentions-the-command' --mark '22=path:CHANGELOG.md' --mark '23=value:"notes add"' --into scenes/s03.html

REC=(--file src/record.json --label 'results.jsonl · one record, spread out' --id record --width 48
     --show 1-2,8-35,559-579,598-600 --expect "24='notes add' found in CHANGELOG.md" --expect '563=73095'
     --mark 2=rtype --mark 10=status --mark 12=grade --mark 15=passed --mark 18=details --mark 24=evidence --mark 34=traj
     --mark 560=usage --mark 561=input --mark 562=output --mark 563=total --mark 564=cacheread --mark 566=calls
     --mark 575=provider --mark 576=unit --mark 577=amount)
fp "${REC[@]}" --rows 9 --into scenes/s08.html
fp "${REC[@]}" --rows 9 --into scenes/s09.html
fp "${REC[@]}" --rows 9 --into scenes/s10.html
fp "${REC[@]}" --rows 6 --into scenes/s11.html

fp --file src/metadata.json --label metadata.json --id meta --width 46 --rows 9 --mark 8=model --mark 11=status \
   --expect '8=claude-haiku-4.5' --into scenes/s18.html
echo panels-ok
