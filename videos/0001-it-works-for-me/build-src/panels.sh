#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# Labels are the short names a viewer needs, not the course's folder layout: that layout has not
# been introduced yet, and a long path over a panel is a distraction.
# Every panel that shows part of its file says so: a minimap where there is room (s04, s05, s11),
# a scrollbar where two panels share the width (s17, --no-minimap). Never neither.
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
fp --file src/CHANGELOG.md --label notes-cli/CHANGELOG.md --id changelog --show 1-16 --rows 9 --width 62 --mark 5=unreleased --mark 7=added --mark '8=entry:Add `notes list --tag` to filter by tag' --mark '8=pr41:(#41)' --expect '5=Unreleased' --into scenes/s04.html
fp --file src/SKILL.md --label changelog-entry/SKILL.md --id skill --width 42 --rows 9 --mark '10=category:in the right category' --mark '12=reference:Reference the pull request.' --expect '12=Reference' --into scenes/s05.html
fp --file src/haiku.patch --label 'workspace.patch' --id patch --width 62 --rows 9 --mark 1=file-line --mark '5=hunk:@@ -7,6 +7,9 @@' --mark 6-8=context --mark 9-11=added --expect '9=+### Fixed' --into scenes/s11.html
fp --file src/haiku.patch --label 'claude-haiku-4.5' --id pa --show 7-10 --width 29 --rows 9 --no-minimap --mark '7=pr41:(#41)' --mark '10=end-a:("tittle" → "title")' --into scenes/s17.html
fp --file src/terra.patch --label 'gpt-5.6-terra' --id pb --show 7-10 --width 29 --rows 9 --no-minimap --mark '7=pr41:(#41)' --mark '10=pr42:(#42)' --into scenes/s17.html
echo panels-ok
