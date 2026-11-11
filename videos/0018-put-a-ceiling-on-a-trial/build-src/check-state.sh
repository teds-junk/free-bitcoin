#!/bin/bash
# Read-only check of what each lesson 18 tape needs in the series' demo folder. Changes nothing.
# Run from anywhere:  bash build-src/check-state.sh [s16|s18|s21|s23]   (no argument: all)
V=$(cd "$(dirname "$0")/.." && pwd)
P=/Users/Shared/demo/practice
ok=1
say(){ printf '%-5s %s\n' "$1" "$2"; [ "$1" = FAIL ] && ok=0; return 0; }
runs(){ [ -d "$1" ] && /bin/ls "$1" | grep -c . || echo 0; }
want=${1:-all}
need(){ [ "$want" = all ] || [ "$want" = "$1" ]; }

[ -d "$P" ] && say ok "practice folder exists" || say FAIL "no $P"
for f in tight wide final; do [ -f "$V/src/state/changelog.$f.eval.yaml" ] || say FAIL "src/state/changelog.$f.eval.yaml missing: run build-src/make-state.py"; done
[ -e "$V/src/run/PROVISIONAL" ] && say note "src/state/budgets.json still holds the lesson page's values: run build-src/capture-run.py --budgets, then make-state.py, before recording"

# The demo's eval file must be the base this video adds to, or one of the three files its tapes install.
E="$P/evals/changelog.eval.yaml"
if cmp -s "$E" "$V/src/state/changelog.base.eval.yaml"; then say ok "evals/changelog.eval.yaml is the base (the state lesson 17 leaves)"
elif cmp -s "$E" "$V/src/state/changelog.tight.eval.yaml" || cmp -s "$E" "$V/src/state/changelog.wide.eval.yaml" || cmp -s "$E" "$V/src/state/changelog.final.eval.yaml"; then say ok "evals/changelog.eval.yaml is one of this video's staged files (a tape has run)"
else say FAIL "evals/changelog.eval.yaml differs from src/state/changelog.base.eval.yaml: copy the demo's file over the base and rerun make-state.py (the tapes overwrite it)"; fi

if need s16 || need s18 || need s21; then
  n=$(runs "$P/results/lesson-16")
  [ "$n" = 1 ] && say ok "one run under results/lesson-16 (Tab completes it)" || say FAIL "results/lesson-16 holds $n runs; the tapes need exactly one"
  for v in haiku-high terra-high; do
    f=$(/bin/ls -d "$P"/results/lesson-16/2026*/"$v"/results.jsonl 2>/dev/null | head -n 1)
    [ -n "$f" ] && say ok "$v/results.jsonl exists" || say FAIL "no $v/results.jsonl in the lesson 16 run"
  done
fi
if need s23; then
  for f in evals/grading/check-entry.mjs evals/golden/typo-fix.patch evals/fixtures/notes-cli/CHANGELOG.md skills/changelog-entry/SKILL.md; do
    [ -e "$P/$f" ] && say ok "$f exists" || say FAIL "$f missing (the eval file names it)"
  done
  [ -e "$P/results/lesson-18" ] && say note "results/lesson-18 exists; s23's hidden setup moves it aside to /Users/Shared/.demo-old.lesson-18.<time>"
fi
[ $ok = 1 ] && echo check-ok || { echo check-FAILED; exit 1; }
