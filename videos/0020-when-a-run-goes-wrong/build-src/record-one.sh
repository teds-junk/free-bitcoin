#!/bin/bash
# Record one tape of lesson 20, alone. Waits until no other video's render is running: a render during a
# recording made vhs lose its terminal once. Only real `node ... render-scenes.js` processes count (a
# shell whose command text merely mentions the script does not).
# Usage: bash build-src/record-one.sh s14 [--allow-spend]
cd /Users/ted/src/learn/vally/videos || exit 1
n=0
while pgrep -f '^node .*render-scenes\.js' >/dev/null; do
  [ $n -ge 360 ] && { echo "another render still running after 30 min"; exit 2; }
  /bin/sleep 5; n=$((n+1))
done
echo "== $(date +%T) recording $1 (waited $((n*5))s)"
node ~/.claude/skills/video-lesson/scripts/render-scenes.js 0020-when-a-run-goes-wrong --only "$1" $2 2>&1 | tail -12
echo "== $(date +%T) $1 render exit=${PIPESTATUS[0]}"
