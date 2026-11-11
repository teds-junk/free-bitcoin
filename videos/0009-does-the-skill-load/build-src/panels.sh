#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
#   src/state/SKILL.before.md, SKILL.after.md  the skill before and after this lesson's one edit
#                                              (verified/lesson-08 and verified/lesson-09)
#   src/record.json                            the gpt-5.6-terra trial's record from the lesson 1 video's
#                                              run, pretty-printed: the copy lessons 2 and 3 show
#   src/state/loading.eval.yaml                the loading eval file, as the starter ships it
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }

fp --file src/state/SKILL.before.md --label 'changelog-entry/SKILL.md' --id skill --lang markdown --width 46 --rows 9 \
   --show 1-7 --expect '3=Adds an entry to the project changelog.' \
   --mark 2-3=given --mark 6=rest --mark hidden:8=rest --into scenes/s02.html

fp --file src/record.json --label 'results.jsonl · one record, spread out' --id event --width 46 --rows 9 \
   --show 106-109,115-117 --expect '106="skill_activation"' --expect '109="changelog-entry"' \
   --mark '106=type:"skill_activation"' --mark '109=name:"changelog-entry"' --mark '116=turn:"turn": 0' \
   --into scenes/s09.html

for s in s11 s12; do
  fp --file src/state/loading.eval.yaml --label 'evals/loading.eval.yaml' --id loading --width 46 --rows 9 \
     --show 6-10,25-33,54-61 --expect '25=load-no-keyword' --expect '54=skip-release-notes' \
     --mark 8-10=skills --mark 27-29=p1 --mark '33=req:required: [changelog-entry]' \
     --mark 56-57=p2 --mark '61=dis:disallowed: [changelog-entry]' --into scenes/$s.html
done

fp --file src/state/SKILL.after.md --label 'changelog-entry/SKILL.md' --id newskill --lang markdown --width 62 --rows 9 \
   --show 1-8 --expect '3=description: >-' \
   --mark "4=does:Records a change in the project's CHANGELOG.md." \
   --mark '4=when:Use whenever' --mark 5-6=when --mark 7-8=notfor --into scenes/s18.html
echo panels-ok
