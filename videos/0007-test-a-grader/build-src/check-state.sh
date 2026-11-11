#!/bin/bash
# Read-only. Run before recording s11: says whether /Users/Shared/demo/practice is in the state the tapes assume.
P=/Users/Shared/demo/practice; S="$(cd "$(dirname "$0")/.." && pwd)/src/state"
diff -q "$P/evals/changelog.eval.yaml" "$S/00-start.changelog.eval.yaml" && echo "eval file: as lesson 6 left it (matches src/state/00-start)"
n=$(/bin/ls -d "$P"/results/lesson-6-after/2026* 2>/dev/null | wc -l | tr -d ' '); echo "run folders under results/lesson-6-after starting 2026: $n (need 1)"
[ -e "$P/evals/golden" ] && echo "evals/golden exists: s11 will move it aside" || echo "evals/golden absent: ok"
grep -l __TYPO_FIX_TRIAL__ "$S/../../tapes/s11.tape" >/dev/null && echo "tapes/s11.tape still has the __TYPO_FIX_TRIAL__ placeholder"
[ -e "$S/../run/PROVISIONAL" ] && echo "src/run is still provisional"
true
