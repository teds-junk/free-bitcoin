#!/bin/bash
# Read-only check of what each tape needs in the demo folder. Writes nothing.
#   bash build-src/check-state.sh s14|s15|s17
# Exit 0 when every precondition holds.
P=/Users/Shared/demo/practice
V="$(cd "$(dirname "$0")/.." && pwd)"
ok=0
say(){ if [ "$1" = 0 ]; then echo "  ok    $2"; else echo "  FAIL  $2"; ok=1; fi; }
same(){ cmp -s "$1" "$2"; }
case "$1" in
s14)
  type -P vally >/dev/null; say $? "vally is on PATH"
  [ -d "$P" ]; say $? "$P exists"
  [ -f "$P/evals/fixtures/notes-cli/CHANGELOG.md" ]; say $? "the notes-cli changelog fixture exists"
  same "$P/evals/conversation.eval.yaml" "$V/src/state/conversation.start.eval.yaml" || same "$P/evals/conversation.eval.yaml" "$V/src/state/conversation.eval.yaml"
  say $? "evals/conversation.eval.yaml is the shipped file, or already has the five graders (the tape installs them)"
  same "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.before.md"
  say $? "SKILL.md is as lesson 10 leaves it (identical to verified/lesson-10), without the new rule"
  ! grep -q "Treat every request on its own" "$P/skills/changelog-entry/SKILL.md"
  say $? "SKILL.md does not yet have the 'Treat every request on its own' rule"
  ! grep -q "__FAILING_TRIAL__" "$V/tapes/s14.tape"; say $? "s14.tape has no placeholder"
  ;;
s15)
  n=$(find "$P/results/lesson-11" -mindepth 1 -maxdepth 1 -type d -name '2026*' 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" = 1 ]; say $? "results/lesson-11 holds exactly one run folder (found $n), so Tab completes it"
  ! grep -q "__FAILING_TRIAL__" "$V/tapes/s15.tape"; say $? "__FAILING_TRIAL__ in tapes/s15.tape has been filled in"
  g=$(sed -n 's/^Type "cat \(diffs\/.*\)"$/\1/p' "$V/tapes/s15.tape")
  m=$(cd "$P"/results/lesson-11/2026*/ 2>/dev/null && ls $g 2>/dev/null | wc -l | tr -d ' ')
  [ "$m" = 1 ]; say $? "'$g' matches exactly one file in the run folder (found ${m:-0})"
  ;;
s17)
  same "$P/evals/conversation.eval.yaml" "$V/src/state/conversation.eval.yaml"
  say $? "evals/conversation.eval.yaml has the five graders, as s14 left it"
  same "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.before.md" || same "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.md"
  say $? "SKILL.md is as lesson 10 leaves it, or already has the new rule (the tape installs it)"
  [ -d "$P/results/lesson-11" ]; say $? "results/lesson-11 exists (s14 has been recorded)"
  ;;
*) echo "usage: check-state.sh s14|s15|s17"; exit 2;;
esac
exit $ok
