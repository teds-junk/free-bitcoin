#!/bin/bash
# After s13, s14, s17 and s18 are recorded: bring this video's own run into src/run/.
# Reads /tmp/vl-l19 (the logs the tapes' vally wrapper saved) and the experiment folder in the demo
# practice folder; writes only inside this video's folder. /Users/Shared/demo is shown as ~/src/demo.
set -e
cd "$(dirname "$0")/.."
runs=( /Users/Shared/demo/practice/results/lesson-15/2026*/ )
[ "${#runs[@]}" -eq 1 ] && [ -d "${runs[0]}" ] || { echo "expected exactly one results/lesson-15/2026* folder"; exit 1; }
X=${runs[0]}
for s in s14 s17 s18; do
  [ -s /tmp/vl-l19/$s.log ] || { echo "missing /tmp/vl-l19/$s.log: record tapes/$s.tape first"; exit 1; }
  grep -q '^exit=' /tmp/vl-l19/$s.log || { echo "/tmp/vl-l19/$s.log has no exit= line: the recording did not finish"; exit 1; }
done
[ -s "$X/haiku-compare.jsonl" ] || { echo "missing $X/haiku-compare.jsonl: record tapes/s14.tape first"; exit 1; }
for s in s14 s17 s18; do sed 's|/Users/Shared/demo|~/src/demo|g' /tmp/vl-l19/$s.log > src/run/$s.log; done
sed 's|/Users/Shared/demo|~/src/demo|g' "$X/haiku-compare.jsonl" > src/run/haiku-compare.jsonl
basename "$X" > src/run/RUN
rm -f src/run/PROVISIONAL
echo "collected: src/run/{s14,s17,s18}.log, haiku-compare.jsonl, RUN ($(cat src/run/RUN)); PROVISIONAL removed"
echo "next: choose the pair and the quoted sentence in src/run/facts.json, then python3 build-src/make-scenes.py"
