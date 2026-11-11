#!/bin/bash
# Fill src/run/ from the series' own demo folder. Starts no agent (vally grade and vally oracle are free).
# WRITES to /Users/Shared/demo/practice/evals/changelog.eval.yaml: swaps the flawed pattern in, then puts
# the correct file back, exactly as tapes s13 and s16 do. Run it once the lesson 5 "before" run and the
# lesson 7 golden patches exist there, before or after recording (the commands are deterministic).
# Run from the video directory:  bash build-src/capture-run.sh && python3 build-src/make-scenes.py
set -euo pipefail
V=$(cd "$(dirname "$0")/.." && pwd)
P=/Users/Shared/demo/practice
OUT="$V/src/run"
show(){ sed 's|/private/Users/Shared/demo|~/src/demo|g; s|/Users/Shared/demo|~/src/demo|g'; }
# The demo's eval file must be the one this video shows and restores.
cmp -s "$P/evals/changelog.eval.yaml" "$V/src/state/changelog.eval.yaml" || {
  echo "evals/changelog.eval.yaml in the demo folder differs from src/state/changelog.eval.yaml: update src/state (both files) first" >&2; exit 1; }
[ "$(/bin/ls "$P/results/lesson-5-before" | wc -l | tr -d ' ')" = 1 ] || { echo "expected one run under results/lesson-5-before" >&2; exit 1; }
RUN=$(/bin/ls "$P/results/lesson-5-before")
R="$P/results/lesson-5-before/$RUN"
grade(){ (cd "$R" && vally grade -e ../../../evals/changelog.eval.yaml --run-dir . < results.jsonl 2>&1 | show) || true; }
oracle(){ (cd "$P" && vally oracle -e evals/changelog.eval.yaml --stimulus typo-fix "$@" --verbose 2>&1 | show) || true; }
restore(){ cp "$V/src/state/changelog.eval.yaml" "$P/evals/changelog.eval.yaml"; }
trap restore EXIT
echo "$RUN" > "$OUT/RUN"
grade > "$OUT/grade-before.txt"
oracle --no-golden-input > "$OUT/oracle-baseline.txt"
cp "$V/src/state/changelog.flawed.eval.yaml" "$P/evals/changelog.eval.yaml"
oracle > "$OUT/oracle-flawed.txt"
oracle --no-golden-input > "$OUT/oracle-flawed-baseline.txt"
grade > "$OUT/grade-flawed.txt"
restore
grade > "$OUT/grade-restored.txt"
# A saved typo-fix trial that made up a number: the first whose patch adds a line ending (#N).
BAD=$(grep -l -E '^\+.*\(#[0-9]+\)' "$R"/changelog/typo-fix/*/*/workspace.patch | head -n 1)
[ -n "$BAD" ] || { echo "no typo-fix trial in this run made up a number: the story needs rethinking" >&2; exit 1; }
show < "$BAD" > "$OUT/bad-trial.patch"
echo "bad trial: ${BAD#$R/}"
rm -f "$OUT/PROVISIONAL"
echo capture-ok
