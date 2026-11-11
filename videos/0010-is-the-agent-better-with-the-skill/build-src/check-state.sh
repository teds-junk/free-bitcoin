#!/bin/bash
# Read-only check of what each tape needs in the demo folder. Changes nothing.
# Usage: bash build-src/check-state.sh [s13|s14|s17]   (no argument: all three)
V="$(cd "$(dirname "$0")/.." && pwd)"; P=/Users/Shared/demo/practice; bad=0
ok(){ echo "  ok    $1"; }; no(){ echo "  FAIL  $1"; bad=1; }
same(){ if diff -rq "$V/src/state/$1" "$P/$1" >/dev/null 2>&1; then ok "$1 is as verified/lesson-10 has it"; else no "$1 differs from src/state/$1 (or is missing)"; fi; }
start(){
  for f in evals/with-and-without.experiment.yaml evals/changelog.eval.yaml evals/grading/check-entry.mjs \
           evals/fixtures evals/golden skills/changelog-entry/SKILL.md; do same "$f"; done
  command -v vally >/dev/null && ok "vally is on PATH ($(vally --version 2>/dev/null | head -1))" || no "vally is not on PATH"
}
want="${1:-all}"
if [ "$want" = all ] || [ "$want" = s13 ]; then echo "s13 (dry run, free):"; start; fi
if [ "$want" = all ] || [ "$want" = s14 ]; then echo "s14 (20 agent runs):"; start
  if [ -e "$P/results/lesson-10" ]; then echo "  note  results/lesson-10 exists; s14's setup will move it to /Users/Shared/.demo-old.lesson-10.<time>"; else ok "no results/lesson-10 yet"; fi; fi
if [ "$want" = all ] || [ "$want" = s17 ]; then echo "s17 (free, after s14):"
  n=$(/bin/ls -d "$P"/results/lesson-10/2026* 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" = 1 ] && ok "exactly one run folder under results/lesson-10" || no "results/lesson-10 holds $n run folders named 2026*; Tab completion needs exactly one"
  f=$(/bin/ls "$P"/results/lesson-10/2026*/terra-no-skill/changelog/typo-fix/gpt-5.6-terra/0/workspace.patch 2>/dev/null | head -1)
  [ -n "$f" ] && ok "terra-no-skill's typo-fix patch exists" || no "terra-no-skill/changelog/typo-fix/gpt-5.6-terra/0/workspace.patch is missing"; fi
exit $bad
