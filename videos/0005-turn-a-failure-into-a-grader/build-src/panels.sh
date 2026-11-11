#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/terra.patch is trial 0 of gpt-5.6-terra from the lesson 3 video's run, untouched.
# src/state/changelog.eval.yaml and src/state/SKILL.md are the files the tapes install into the
# practice folder (from verified/lesson-05/practice), so the panels show what the runs used.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/terra.patch --label 'workspace.patch · gpt-5.6-terra' --id patch --width 47 --rows 9 \
   --show 5-12 --expect '7=(#41)' --expect '10=(#42)' \
   --mark '7=ctx:(#41)' --mark 10=added --into scenes/s07.html
fp --file src/state/changelog.eval.yaml --label 'evals/changelog.eval.yaml' --id spec --width 46 --rows 9 \
   --show 10-27 --expect '11=typo-fix' --expect "27=pattern: '(?m)" \
   --mark '11=stim:typo-fix' --mark '21=g1:adds-an-entry' --mark '23=value:"notes add"' \
   --mark '25=g2:no-made-up-number' --mark "27=pattern:'(?m)^\\+.*\\(#\\d+\\)'" --into scenes/s08.html
fp --file src/state/changelog.eval.yaml --label 'evals/changelog.eval.yaml' --id spec2 --width 46 --rows 9 \
   --show 29,36-40,42,49-55 --expect '39=diff-empty' --expect '55=### Security' \
   --mark '29=refactor:refactor' --mark '39=de:diff-empty' --mark '42=security:security' \
   --mark "55=sec:'(?m)^\\+### Security'" --into scenes/s10.html
fp --file src/state/SKILL.md --label 'changelog-entry/SKILL.md' --id skill --width 60 --rows 9 \
   --show 13-20 --expect '14=If no pull request number' --expect '20=Security.' \
   --mark 14-15=r1 --mark 16-17=r2 --mark 18-20=r3 --into scenes/s16.html
echo panels-ok
