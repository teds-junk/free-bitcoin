#!/bin/bash
# Read-only: does /Users/Shared/demo/practice meet the preconditions of one of this video's tapes?
#   bash build-src/check-state.sh s14      (or s15 s18 s19 s20 s24 s25 s27 s30 s31 s34)
# Record in that order. Writes nothing. Exit 1 when a precondition fails.
P=/Users/Shared/demo/practice; V=$(cd "$(dirname "$0")/.." && pwd); ok=0
say(){ echo "  $1"; }; bad(){ echo "  FAIL: $1"; ok=1; }
have(){ [ -e "$1" ] && say "found $1" || bad "missing $1"; }
one_run(){ n=$(ls -d $P/results/lesson-20/2026* 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" = 1 ] && say "exactly one run under results/lesson-20" || bad "$n runs under results/lesson-20 (need exactly 1 for Tab or the glob)"; }
run_of(){ [ -d $P/results/lesson-20/2026*/"$1" ] 2>/dev/null && say "that run is of $1" || bad "the run under results/lesson-20 is not of $1"; }
same(){ diff -q "$1" "$2" >/dev/null 2>&1 && say "$(basename $2) is the $3 version" || bad "$2 is not the $3 version"; }
command -v vally >/dev/null && say "vally on PATH" || bad "vally not on PATH"
have $P/skills/changelog-entry/SKILL.md; have $P/evals/fixtures/notes-cli/CHANGELOG.md
case "$1" in
  s14) have /Users/Shared/demo/practice-starter/evals/broken/merged-list.eval.yaml
       diff -rq /Users/Shared/demo/practice-starter/evals/broken $V/src/state/broken >/dev/null && say "starter's broken files match src/state/broken" || bad "starter's evals/broken differs from src/state/broken"
       say "note: an existing evals/broken, results/lesson-20 and results/lesson-20-earlier will be moved aside by the tape" ;;
  s15) one_run; run_of merged-list ;;
  s18) have $P/evals/broken/merged-list.eval.yaml ;;
  s19) have $P/evals/broken/quick.eval.yaml ;;
  s20) one_run; run_of quick ;;
  s24) have $P/evals/broken/quick.eval.yaml ;;
  s25) have $P/evals/broken/entry.eval.yaml ;;
  s27) one_run; run_of entry ;;
  s30) one_run; run_of entry; have $P/results/lesson-20/2026*/results.jsonl; have $P/results/lesson-20/2026*/diffs ;;
  s31) have $P/evals/broken/judged.eval.yaml ;;
  s34) one_run; run_of judged; have $P/results/lesson-20/2026*/results.jsonl; have $P/results/lesson-20/2026*/diffs ;;
  *) echo "usage: check-state.sh s14|s15|s18|s19|s20|s24|s25|s27|s30|s31|s34"; exit 2 ;;
esac
[ $ok = 0 ] && echo "ok: $1" || echo "NOT READY: $1"; exit $ok
