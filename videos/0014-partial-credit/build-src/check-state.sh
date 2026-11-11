#!/bin/bash
# Read-only check of what each lesson 14 tape needs in the demo folder. Changes nothing.
#   bash build-src/check-state.sh [s15|s16|s19]      (no argument: all three)
V="$(cd "$(dirname "$0")/.." && pwd)"
P=/Users/Shared/demo/practice
bad=0
ok(){ echo "  ok    $1"; }
no(){ echo "  FAIL  $1"; bad=1; }
warn(){ echo "  note  $1"; }
common(){
  [ -d "$P" ] && ok "practice folder exists" || no "$P is missing"
  type -P vally >/dev/null && ok "vally is on PATH" || no "vally is not on PATH"
  n=$(find "$P/results/lesson-12" -maxdepth 1 -type d -name '2026*' 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" = 1 ] && ok "exactly one run folder under results/lesson-12" \
    || no "results/lesson-12 holds $n run folders named 2026*; the tapes complete the name with Tab and need exactly one"
  r=$(find "$P/results/lesson-12" -maxdepth 1 -type d -name '2026*' 2>/dev/null | head -1)
  if [ -n "$r" ] && [ -f "$r/results.jsonl" ]; then
    t=$(grep -c '"trial-result"' "$r/results.jsonl")
    [ "$t" = 12 ] && ok "its results.jsonl has 12 trial records" || no "its results.jsonl has $t trial records, not 12"
  else no "no results.jsonl in the lesson 12 run folder"; fi
  cmp -s "$P/evals/wording.eval.yaml" "$V/src/wording.eval.yaml" \
    && ok "evals/wording.eval.yaml matches src/wording.eval.yaml (the scaled copies are made from it)" \
    || no "evals/wording.eval.yaml differs from src/wording.eval.yaml: remake src/state/*.eval.yaml from the demo's file first (the generator asserts how they must differ)"
}
for id in ${1:-s15 s16 s19}; do
  echo "$id"
  common
  case $id in
    s15) [ -e "$P/evals/wording-scaled.eval.yaml" ] && warn "evals/wording-scaled.eval.yaml exists; the tape moves it to /Users/Shared/.demo-old.wording-scaled.<time>.yaml" ;;
    s16) [ -f "$P/notes/wording-labels.md" ] && ok "notes/wording-labels.md exists (copy it to src/run/wording-labels.before.md before s19 is recorded)" \
           || no "notes/wording-labels.md is missing (the lesson 12 and 13 videos write it)" ;;
    s19) [ -e "$V/src/run/PROVISIONAL" ] && no "src/run/PROVISIONAL still exists: src/state/notes/wording-labels.md, which this tape copies into the practice folder, was built from stand-ins" \
           || ok "src/run/ is the video's own run"
         if [ -f /tmp/vl-l14/s16-grade.log ] && [ /tmp/vl-l14/s16-grade.log -nt "$V/src/run/s16-grade.log" ]; then
           no "/tmp/vl-l14/s16-grade.log is newer than src/run/s16-grade.log: copy it in and run make-scenes.py first"
         else ok "src/run/s16-grade.log is not older than the last s16 recording's log"; fi
         [ -f "$V/src/state/notes/wording-labels.md" ] && ok "src/state/notes/wording-labels.md exists" || no "run build-src/make-scenes.py first" ;;
  esac
done
exit $bad
