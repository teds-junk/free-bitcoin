#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# src/run/typo-fix.patch is the golden patch (the saved trial's patch that tape s11 copies);
# src/state/05 and 08 are the eval file after page step 5 and during page step 8.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/run/typo-fix.patch --label golden/typo-fix.patch --id golden --width 40 --rows 9 \
   --show 6-12 --expect '9=### Fixed' --mark 9=fixed --mark 10=entry --into scenes/s04.html
E5=(--file src/state/05-golden-typo-fix.changelog.eval.yaml --label changelog.eval.yaml --id evalfile --width 44 --rows 9)
fp "${E5[@]}" --show 11,19-21,31,40-42 --expect '19=golden_patch' --expect '31=refactor' \
   --mark '19=key:golden_patch' --mark 20=path --mark 31=refactor --into scenes/s05.html
fp "${E5[@]}" --show 11,19-21 --expect '19=golden_patch' --mark 19-20=lines --into scenes/s12.html
fp --file src/state/08-useless-grader.changelog.eval.yaml --label changelog.eval.yaml --id evalfile --width 44 --rows 9 \
   --show 21-27 --expect '23=mentions-unreleased' --mark '23=name:mentions-unreleased' --mark 26=value --into scenes/s14.html
echo panels-ok
