#!/bin/bash
# Read-only check of what the lesson 15 tapes need in the demo practice folder. Changes nothing.
#   bash build-src/check-state.sh          before recording s13
#   bash build-src/check-state.sh s14      before recording s14 (after s13)
P=/Users/Shared/demo/practice
V="$(cd "$(dirname "$0")/.." && pwd)"
ok=1
say(){ printf '%-4s %s\n' "$1" "$2"; if [ "$1" = FAIL ]; then ok=0; fi; return 0; }
same(){ cmp -s "$1" "$2"; }

[ -d "$P" ] && say ok "practice folder exists" || say FAIL "no $P"
type -P vally >/dev/null && say ok "vally is on PATH" || say FAIL "vally not on PATH"
same "$P/evals/before-and-after.experiment.yaml" "$V/src/state/before-and-after.experiment.yaml" \
  && say ok "evals/before-and-after.experiment.yaml matches src/state (the starter's file)" \
  || say FAIL "evals/before-and-after.experiment.yaml differs from src/state: the s07 panel and the commands assume it"
same "$P/evals/wording.eval.yaml" "$V/src/state/wording.eval.yaml" \
  && say ok "evals/wording.eval.yaml matches src/state (lesson 12's judged eval)" \
  || say WARN "evals/wording.eval.yaml differs from verified/lesson-15: check it still has three stimuli (parser, cache, dates), a prompt grader and a judge_model"
[ -d "$P/skills/commit-message" ] && [ -d "$P/skills/release-notes" ] && say ok "neighbouring skills present" || say WARN "neighbouring skills missing (not used by this experiment)"

if [ "$1" = s14 ]; then
  [ -d "$P/skills/changelog-entry-before" ] && say ok "skills/changelog-entry-before exists" || say FAIL "skills/changelog-entry-before missing: record s13 first"
  same "$P/skills/changelog-entry-before/SKILL.md" "$V/src/state/SKILL.before.md" \
    && say ok "the kept copy is the skill before the edit" || say FAIL "skills/changelog-entry-before/SKILL.md is not src/state/SKILL.before.md"
  if [ -e "$P/skills/changelog-entry-before/changelog-entry" ]; then say FAIL "a nested copy: cp -R ran into an existing folder"; fi
  same "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.md" \
    && say ok "the skill has the sharpened rule" || say WARN "skills/changelog-entry/SKILL.md is not src/state/SKILL.md yet (s14's hidden setup installs it)"
  if [ -e "$P/results/lesson-15" ]; then say WARN "results/lesson-15 exists: s14 will move it aside to /Users/Shared/.demo-old.lesson-15.<time>"; fi
else
  same "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.before.md" \
    && say ok "skills/changelog-entry/SKILL.md is the skill as lesson 14 leaves it (src/state/SKILL.before.md)" \
    || { same "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.md" \
         && say WARN "the skill already has the sharpened rule (s13 was recorded before): s13's hidden setup puts SKILL.before.md back" \
         || say FAIL "skills/changelog-entry/SKILL.md matches neither src/state file: the earlier videos left a different skill. Update src/state/SKILL.before.md and SKILL.md (the edit is the second rule only) before recording, or s13's hidden setup will overwrite it"; }
  if [ -e "$P/skills/changelog-entry-before" ]; then say WARN "skills/changelog-entry-before exists: s13 will move it aside to /Users/Shared/.demo-old.lesson-15.before.<time>"; fi
fi
if [ $ok = 1 ]; then echo "state ok"; else echo "state NOT ok"; exit 1; fi
