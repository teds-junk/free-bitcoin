#!/bin/bash
# After s13 and s14 are recorded: copy what the video quotes from the run into src/run/.
# Reads /tmp/vl-l10 and /Users/Shared/demo/practice/results/lesson-10; writes only src/run/.
# Then delete src/run/PROVISIONAL and run: python3 build-src/make-scenes.py && bash build-src/panels.sh
set -e
V="$(cd "$(dirname "$0")/.." && pwd)"; R=/Users/Shared/demo/practice/results/lesson-10
run=$(/bin/ls -d "$R"/2026* | head -1); [ "$(/bin/ls -d "$R"/2026* | wc -l | tr -d ' ')" = 1 ] || { echo "expected one run folder in $R"; exit 1; }
clean(){ perl -pe 's/\e\[[0-9;?]*[A-Za-z]//g; s/\r//g; s/\x04|\x08//g' "$1"; }
clean /tmp/vl-l10/s13.log > "$V/src/run/s13.log"
# On a terminal Vally redraws a live summary many times (about 1 MB). Keep what the video quotes:
# each failure block once, in the order printed, then the final summary from its rule to the end.
clean /tmp/vl-l10/s14.log | python3 -c '
import re, sys
L = sys.stdin.read().split("\n"); out = []; seen = set()
for i, l in enumerate(L):
    if re.match(r"^\s+(FAIL|FLAKY|ERROR)\s+\S+ · ", l) and (L[i-1], l) not in seen:
        seen.add((L[i-1], l)); out += [L[i-1], l]
        for n in L[i+1:]:
            if not re.match(r"^\s+✘ ", n): break
            out.append(n)
        out.append("")
last = max(i for i, l in enumerate(L) if l.strip() == "Experiment")
print("\n".join(out + L[last-2:]))' > "$V/src/run/s14.log"
basename "$run" > "$V/src/run/RUN"
for pair in haiku-no-skill:claude-haiku-4.5 terra-no-skill:gpt-5.6-terra; do v=${pair%%:*}; m=${pair##*:}
  for s in typo-fix refactor security; do
    sed 's|/Users/Shared/demo|~/src/demo|g' "$run/$v/changelog/$s/$m/0/workspace.patch" > "$V/src/run/$v-$s.patch"
  done
done
/bin/ls -l "$V/src/run"
