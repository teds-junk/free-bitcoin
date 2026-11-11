#!/bin/bash
# Read-only check of what each lesson 24 tape needs in /Users/Shared/demo/practice. Changes nothing.
# Usage: bash build-src/check-state.sh [s17|s18|s20]   (no argument: all three)
cd "$(dirname "$0")/.." || exit 2
P=/Users/Shared/demo/practice
bad=0
ok(){ echo "  ok    $1"; }
no(){ echo "  FAIL  $1"; bad=1; }
same(){ cmp -s "$1" "$2"; }
eval_file(){
  if same "$P/evals/release.eval.yaml" src/state/release.eval.before.yaml; then ok "evals/release.eval.yaml is the lesson 23 file (verified/lesson-23); the tape installs lesson 24's over it"
  elif same "$P/evals/release.eval.yaml" src/state/release.eval.yaml; then ok "evals/release.eval.yaml is already lesson 24's (a re-recording)"
  else no "evals/release.eval.yaml is neither verified/lesson-23's nor lesson 24's: the tape's hidden copy would overwrite a file that differs. Compare it with src/state/release.eval.before.yaml first"; fi
  same "$P/evals/fixtures/release/list-merged.mjs" src/fixture-list-merged.mjs && ok "evals/fixtures/release/list-merged.mjs is the copy that asks the tracker" || no "evals/fixtures/release/list-merged.mjs is missing or differs from src/fixture-list-merged.mjs"
  same "$P/tools/list-merged.mjs" src/tools-list-merged.mjs && ok "tools/list-merged.mjs is the course's stand-in" || no "tools/list-merged.mjs is missing or differs from src/tools-list-merged.mjs"
  [ -f "$P/evals/grading/check-release.mjs" ] && ok "evals/grading/check-release.mjs exists (lesson 22's hidden test; lint resolves it)" || no "evals/grading/check-release.mjs is missing (lesson 22 creates it)"
  [ -f "$P/skills/changelog-entry/SKILL.md" ] && ok "skills/changelog-entry/SKILL.md exists" || no "skills/changelog-entry/SKILL.md is missing"
  type -P vally >/dev/null && ok "vally is on PATH" || no "vally is not on PATH"
}
s17(){ echo "s17 (lint, free)"; eval_file; }
s18(){ echo "s18 (6 agent runs, 6 judge calls)"; eval_file
  [ -e "$P/results/lesson-24" ] && echo "  note  results/lesson-24 exists; the tape moves it aside to /Users/Shared/.demo-old.lesson-24.<time>" || ok "no results/lesson-24 yet"; }
s20(){ echo "s20 (simulate record, free)"
  n=$(find "$P/results/lesson-22" -maxdepth 1 -type d -name '2026*' 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" = 1 ] && ok "results/lesson-22 holds exactly one run folder (Tab completes it)" || no "results/lesson-22 holds $n run folders; the tape's Tab completion needs exactly one"; }
case "${1:-all}" in s17) s17;; s18) s18;; s20) s20;; all) s17; s18; s20;; *) echo "unknown tape $1"; exit 2;; esac
exit $bad
