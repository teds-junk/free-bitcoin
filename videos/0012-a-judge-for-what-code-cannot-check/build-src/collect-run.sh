#!/bin/bash
# Copy this video's own run into src/run/, replacing the stand-ins. Reads /Users/Shared/demo/practice and
# /tmp/vl-l12; writes only inside this video's src/run/. Run after s12 has been recorded (patches, records,
# s12.log), and again after s18 and s19 (their logs). Then:
#   1. read the twelve entries (printed below) and write OUR yes/no and a few words why in src/run/labels.tsv
#   2. delete src/run/PROVISIONAL
#   3. python3 build-src/make-scenes.py && bash build-src/panels.sh   (fails where the run disagrees with the narration)
#   4. copy src/state/wording-labels.md to /Users/Shared/demo/practice/notes/wording-labels.md (lesson 13 reads it)
set -e
P=/Users/Shared/demo/practice; V="$(cd "$(dirname "$0")/.." && pwd)"; R="$V/src/run"
RUN=$(cd "$P/results/lesson-12" && /bin/ls -d 2026* | head -1)
[ "$(/bin/ls -d "$P"/results/lesson-12/2026* | wc -l | tr -d ' ')" = 1 ] || { echo "need exactly one run folder under results/lesson-12"; exit 1; }
echo "$RUN" > "$R/RUN"
for s in parser cache dates; do for m in claude-haiku-4.5 gpt-5.6-terra; do for i in 0 1; do
  cp "$P/results/lesson-12/$RUN/wording/$s/$m/$i/workspace.patch" "$R/$s-$m-$i.patch"
done; done; done
sed 's|/Users/Shared/demo|~/src/demo|g' "$P/results/lesson-12/$RUN/results.jsonl" > "$R/results.jsonl"
for id in s12 s18 s19; do
  if [ -s "/tmp/vl-l12/$id.log" ]; then sed 's|/Users/Shared/demo|~/src/demo|g' "/tmp/vl-l12/$id.log" > "$R/$id.log"; echo "copied $id.log"
  else echo "no /tmp/vl-l12/$id.log yet: src/run/$id.log is still the stand-in"; fi
done
echo "run $RUN: the twelve entries (write labels.tsv from these, before looking at the judge's verdicts):"
for s in parser cache dates; do for m in claude-haiku-4.5 gpt-5.6-terra; do for i in 0 1; do
  printf '%s\t%s\t%s\t%s\n' "$s" "$m" "$i" "$(grep '^+- ' "$R/$s-$m-$i.patch" | cut -c4-)"
done; done; done
