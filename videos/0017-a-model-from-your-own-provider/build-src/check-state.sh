#!/bin/bash
# Read-only. Run before recording s14, s16 and s17: says whether Ollama and /Users/Shared/demo/practice
# are in the state the tapes assume. It changes nothing and starts no model.
P=/Users/Shared/demo/practice; V="$(cd "$(dirname "$0")/.." && pwd)"; S="$V/src/state"
echo "== Ollama (s14, s17)"
command -v ollama >/dev/null && ollama --version 2>&1 | head -1 || echo "MISSING: ollama is not installed"
if ollama list >/dev/null 2>&1; then
  ollama list | grep -q '^qwen3.5:9b' && echo "ok: Ollama is serving and qwen3.5:9b is pulled" || echo "MISSING: qwen3.5:9b is not pulled"
else
  echo "MISSING: Ollama is not serving (start its app)"
fi
echo "== evals/cost.experiment.yaml (s16 and s17 copy src/state/cost.experiment.yaml over it)"
if [ ! -e "$P/evals/cost.experiment.yaml" ]; then
  echo "MISSING: no cost.experiment.yaml in the demo folder yet (the lesson 16 video creates it)"
elif diff -q "$P/evals/cost.experiment.yaml" "$S/cost.experiment.before.yaml" >/dev/null; then
  echo "ok: as verified/lesson-16 has it"
elif diff -q "$P/evals/cost.experiment.yaml" "$S/cost.experiment.yaml" >/dev/null; then
  echo "ok: already has the qwen-local variant (s16 or s17 has run)"
else
  echo "DIFFERS from both src/state versions: update src/state/cost.experiment.yaml from the demo's file before recording, or the hidden copy will overwrite it"
fi
echo "== evals/changelog.eval.yaml (the eval the experiment runs; this lesson does not change it)"
diff -q "$P/evals/changelog.eval.yaml" "$S/changelog.eval.before.yaml" >/dev/null \
  && echo "ok: as verified/lesson-16 has it" \
  || echo "DIFFERS from verified/lesson-16: check it has five stimuli and no judge grader, or the run's shape and its zero Copilot spend change"
echo "== results/lesson-17 (s17 moves an existing one aside)"
n=$(/bin/ls -d "$P"/results/lesson-17/2026* 2>/dev/null | wc -l | tr -d ' '); echo "run folders: $n (s17 leaves 1)"
echo "== this video"
[ -e "$V/src/run/PROVISIONAL" ] && echo "src/run is still provisional" || echo "src/run holds our own run"
true
