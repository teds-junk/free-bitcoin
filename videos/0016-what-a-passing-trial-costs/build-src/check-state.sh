#!/bin/bash
# Read-only check of what tapes s15, s17 and s18 need in the demo folder. Changes nothing.
# Run from the video directory:  bash build-src/check-state.sh
P=/Users/Shared/demo/practice
ok=1
say(){ printf '%-5s %s\n' "$1" "$2"; [ "$1" = FAIL ] && ok=0; return 0; }
[ -d "$P" ] && say ok "practice folder exists" || say FAIL "no $P"
# s15: the one-request eval file from lesson 1.
[ -f "$P/evals/one-request.eval.yaml" ] && say ok "evals/one-request.eval.yaml exists (s15)" || say FAIL "evals/one-request.eval.yaml missing (s15)"
cmp -s "$P/evals/one-request.eval.yaml" src/state/expect/one-request.eval.yaml \
  && say ok "one-request.eval.yaml matches verified/lesson-15" || say note "one-request.eval.yaml differs from verified/lesson-15 (fine if an earlier video changed it on purpose)"
# s17, s18: the experiment runs changelog.eval.yaml and the skill as lesson 15 leaves them.
for f in evals/changelog.eval.yaml skills/changelog-entry/SKILL.md; do
  ref=src/state/expect/$(basename $f)
  if [ ! -f "$P/$f" ]; then say FAIL "$f missing (s17, s18)"
  elif cmp -s "$P/$f" "$ref"; then say ok "$f matches verified/lesson-15"
  else say note "$f differs from verified/lesson-15: fine if it is what the lesson 15 video left; the narration needs five stimuli graded by code only"; fi
done
n=$(grep -c '^  - name:' "$P/evals/changelog.eval.yaml" 2>/dev/null)
[ "$n" = 5 ] && say ok "changelog.eval.yaml has five stimuli" || say FAIL "changelog.eval.yaml has $n stimuli; s13 says five, and 60 trials"
grep -q 'type: prompt' "$P/evals/changelog.eval.yaml" 2>/dev/null && say FAIL "changelog.eval.yaml has a judge (type: prompt); s13 says no judge" || say ok "changelog.eval.yaml has no judge"
grep -q 'token-budget\|constraints:' "$P/evals/changelog.eval.yaml" 2>/dev/null && say FAIL "changelog.eval.yaml has budgets or constraints (lesson 18 state)" || say ok "no budgets or constraints yet"
cmp -s "$P/evals/cost.experiment.yaml" src/state/cost.experiment.yaml 2>/dev/null \
  && say ok "evals/cost.experiment.yaml already in place (the tapes copy it anyway)" || say note "evals/cost.experiment.yaml not in place yet: s17 and s18 copy it"
for d in results/lesson-16-efforts results/lesson-16; do
  [ -e "$P/$d" ] && say note "$d exists: the tape moves it aside to /Users/Shared/.demo-old.*" || say ok "$d not there yet"
done
command -v vally >/dev/null && say ok "vally on PATH: $(vally --version 2>/dev/null | head -1)" || say FAIL "vally not on PATH"
[ $ok = 1 ] && echo "state ok" || { echo "state NOT ok"; exit 1; }
