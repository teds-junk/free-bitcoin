#!/bin/bash
# Read-only check of what each tape needs in the demo folder before it is recorded.
#   bash build-src/check-state.sh s13|s14|s16|s18     (run from the video directory)
# Writes nothing. Exits 1 with a line per unmet precondition.
P=/Users/Shared/demo/practice
bad=0
no(){ echo "NOT READY: $*"; bad=1; }
strip(){ grep -v '^    tags: { tier: quick }$' "$1"; }
one_run(){ n=$(/bin/ls -d "$P/results/$1"/2026* 2>/dev/null | wc -l | tr -d ' '); [ "$n" = 1 ] || no "results/$1 holds $n run folders; the tape needs exactly one"; }
same_eval(){ # the demo's eval file, tags aside, must equal the one the tapes copy in
  [ -f "$P/evals/changelog.eval.yaml" ] || { no "evals/changelog.eval.yaml is missing"; return; }
  diff -q <(strip "$P/evals/changelog.eval.yaml") <(strip src/state/changelog.eval.yaml) >/dev/null \
    || no "evals/changelog.eval.yaml differs from src/state/changelog.eval.yaml beyond the tags lines (a lowered budget left by an interrupted s16, or a series file that differs from verified/lesson-20): run python3 build-src/make-state.py --from <the right file>, then make-scenes.py and panels.sh"
}
type -P vally >/dev/null || no "vally is not on PATH"
[ -d src/state ] || { echo "run from the video directory"; exit 2; }
case "$1" in
  s13) same_eval
       grep -q 'token-budget' "$P/evals/changelog.eval.yaml" 2>/dev/null || no "the eval file has no budgets yet (lesson 18)" ;;
  s14) same_eval; one_run lesson-5-before
       [ -f "$(/bin/ls -d "$P"/results/lesson-5-before/2026* 2>/dev/null | head -1)/results.jsonl" ] || no "the lesson 5 before run has no results.jsonl" ;;
  s16) one_run lesson-5-before
       [ -f /tmp/vl-l21/s14.1.log ] || no "s14 has not been recorded (no /tmp/vl-l21/s14.1.log)"
       diff -q <(strip "$P/evals/changelog.eval.yaml") <(strip src/state/changelog.eval.yaml) >/dev/null || no "the eval file is not at its normal budgets before s16" ;;
  s18) same_eval
       for f in conversation loading wording; do [ -f "$P/evals/$f.eval.yaml" ] || no "evals/$f.eval.yaml is missing"; done
       for f in evals/changelog.eval.yaml evals/conversation.eval.yaml evals/loading.eval.yaml evals/wording.eval.yaml; do
         grep -q "$f" src/state/.vally.yaml || no "src/state/.vally.yaml does not list $f"; done ;;
  *) echo "usage: bash build-src/check-state.sh s13|s14|s16|s18"; exit 2 ;;
esac
[ $bad = 0 ] && echo "ready: $1"
exit $bad
