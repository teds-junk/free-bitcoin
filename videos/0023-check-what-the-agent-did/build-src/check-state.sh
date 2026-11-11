#!/bin/bash
# Read-only check of what each tape needs in the demo folder. Writes nothing.
#   bash build-src/check-state.sh [s15|s16|s19|s21]      (no argument: all four)
P=/Users/Shared/demo/practice
V="$(cd "$(dirname "$0")/.." && pwd)"
bad=0
ok(){ echo "  ok    $1"; }
no(){ echo "  FAIL  $1"; bad=1; }
same(){ if cmp -s "$1" "$2"; then ok "$3"; else no "$3"; fi; }
one_run(){
  n=$(find "$P/results/lesson-22" -maxdepth 1 -type d -name '2026*' 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" = 1 ]; then ok "exactly one run under results/lesson-22"
  else no "results/lesson-22 holds $n runs (need exactly 1 for Tab completion)"; fi
}
for s in ${1:-s15 s16 s19 s21}; do
  echo "$s"
  case $s in
  s15)
    if cmp -s "$P/evals/release.eval.yaml" "$V/src/state/release.before.eval.yaml" \
       || cmp -s "$P/evals/release.eval.yaml" "$V/src/state/release.eval.yaml"
    then ok "evals/release.eval.yaml is the lesson 22 file (or already has the four graders)"
    else no "evals/release.eval.yaml differs from src/state/release.before.eval.yaml: s15 would overwrite it"; fi
    if [ -f "$P/evals/grading/check-release.mjs" ]; then ok "evals/grading/check-release.mjs (the hidden test)"
    else no "evals/grading/check-release.mjs is missing"; fi
    if [ -f "$P/tools/list-merged.mjs" ]; then ok "tools/list-merged.mjs"; else no "tools/list-merged.mjs is missing"; fi
    if [ -f "$P/skills/changelog-entry/SKILL.md" ]; then ok "skills/changelog-entry"; else no "skills/changelog-entry is missing"; fi ;;
  s16)
    one_run
    same "$P/evals/release.eval.yaml" "$V/src/state/release.eval.yaml" "evals/release.eval.yaml has the four graders (s15 recorded)"
    f=$(find "$P/results/lesson-22" -maxdepth 2 -name results.jsonl 2>/dev/null | head -1)
    if [ -n "$f" ]; then
      n=$(grep -c '"type":"trial-result"' "$f")
      if [ "$n" = 10 ]; then ok "the saved run has 10 trials"; else no "the saved run has $n trials (the narration says ten)"; fi
    else no "no results.jsonl under results/lesson-22"; fi ;;
  s19)
    one_run
    if [ -f "$V/src/state/release.swap.eval.yaml" ]; then ok "src/state/release.swap.eval.yaml exists (make-scenes.py writes it)"
    else no "run make-scenes.py to write src/state/release.swap.eval.yaml"; fi
    if [ -f "$V/src/run/PROVISIONAL" ] && [ ! -f "$V/src/run/l22/results.jsonl" ]; then
      no "swap-command.txt is still the stand-in: run collect-run.sh l22 and choose a command our trials ran"
    fi ;;
  s21)
    if cmp -s "$P/evals/release.eval.yaml" "$V/src/state/release.eval.yaml" \
       || cmp -s "$P/evals/release.eval.yaml" "$V/src/state/release.swap.eval.yaml"
    then ok "evals/release.eval.yaml is one of this video's two versions (s21 installs the right one)"
    else no "evals/release.eval.yaml is neither of this video's versions: s21 would overwrite it"; fi
    if [ -e "$P/results/lesson-23" ]; then
      echo "  note  results/lesson-23 exists: s21 moves it aside to /Users/Shared/.demo-old.lesson-23.<time>"
    fi ;;
  esac
done
exit $bad
