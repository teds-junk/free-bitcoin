#!/bin/bash
# After s13, s14, s16 and s18 are recorded: copy what the tapes saved into src/run/.
# Reads /tmp/vl-l21 and the two results folders in the demo folder; writes only src/run/. Run from the video directory.
set -e
L=/tmp/vl-l21; P=/Users/Shared/demo/practice
cpy(){ sed 's|/Users/Shared/demo|~/src/demo|g' "$L/$1.log" > "src/run/$2.log"; cp "$L/$1.exit" "src/run/$2.exit"; echo "$2: exit $(cat src/run/$2.exit)"; }
cpy s13.1 lint; cpy s13.2 quick; cpy s14.1 regrade; cpy s16.1 lowered; cpy s18.1 full
for s in quick full; do
  r=$(/bin/ls -d "$P/results/lesson-21-$s"/2026* | tail -1)
  mkdir -p "src/run/$s"
  sed 's|/Users/Shared/demo|~/src/demo|g' "$r/results.jsonl" > "src/run/$s/results.jsonl"
  basename "$r" > "src/run/$s/RUN"
  echo "$s: $(basename "$r")"
done
echo "Now edit src/run/l19.json, l16.json and standing.json from the earlier videos' runs, delete src/run/PROVISIONAL,"
echo "and run: python3 build-src/make-scenes.py && bash build-src/panels.sh"
