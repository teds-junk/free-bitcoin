#!/bin/bash
# Read-only. Says whether /Users/Shared/demo/practice is in the state each of lesson 12's tapes assumes.
# Run before recording s12, and again before s13, s18 and s19.
P=/Users/Shared/demo/practice; V="$(cd "$(dirname "$0")/.." && pwd)"; S="$V/src/state"
L11=/Users/ted/src/learn/vally/verified/lesson-11/practice

echo "== before s12 (the paid run)"
if diff -q "$P/evals/wording.eval.yaml" "$S/00-start.wording.eval.yaml" >/dev/null; then echo "eval file: as it ships, no judge (matches src/state/00-start)"
elif diff -q "$P/evals/wording.eval.yaml" "$S/04-judge.wording.eval.yaml" >/dev/null; then echo "eval file: already has the judge; s12's hidden setup will put the shipped file back"
else echo "eval file: DIFFERS from both src/state files; s12 would overwrite it. Look first."; fi
if diff -q "$P/skills/changelog-entry/SKILL.md" "$L11/skills/changelog-entry/SKILL.md" >/dev/null; then echo "skill: as verified/lesson-11 has it"
else echo "skill: DIFFERS from verified/lesson-11 (expected only if an earlier lesson's video has not been recorded yet, or chose different wording)"; fi
diff -q "$P/skills/changelog-entry/SKILL.md" "$V/src/skill.md" >/dev/null && echo "skill: matches src/skill.md (the hook quotes its line)" || echo "skill: differs from src/skill.md; copy the demo's SKILL.md there and run make-scenes.py"
[ -e "$P/results/lesson-12" ] && echo "results/lesson-12 exists: s12 will move it aside to /Users/Shared/.demo-old.lesson-12.<time>" || echo "results/lesson-12 absent: ok"

echo "== before s13, s18, s19"
n=$(/bin/ls -d "$P"/results/lesson-12/2026* 2>/dev/null | wc -l | tr -d ' '); echo "run folders under results/lesson-12 starting 2026: $n (need exactly 1)"
for d in "$P"/results/lesson-12/2026*/wording; do [ -d "$d" ] && echo "patches saved: $(/bin/ls "$d"/*/*/*/workspace.patch 2>/dev/null | wc -l | tr -d ' ') (need 12)"; done
[ -e "$P/results/lesson-12" ] && [ -e "$P"/results/lesson-12/2026*/wording/parser/claude-haiku-4.5/0/workspace.patch ] && echo "s13's patch exists: parser/claude-haiku-4.5/0"

echo "== after s19"
[ -s /tmp/vl-l12/s19.log ] && echo "/tmp/vl-l12/s19.log: $(grep -c '^━━━' /tmp/vl-l12/s19.log) judged blocks (need 12)" || echo "/tmp/vl-l12/s19.log: not there yet"
[ -e "$V/src/run/PROVISIONAL" ] && echo "src/run is still PROVISIONAL (verified/lesson-12 stand-ins)"
[ -e "$P/notes/wording-labels.md" ] && echo "notes/wording-labels.md is in the practice folder" || echo "notes/wording-labels.md not in the practice folder yet: copy src/state/wording-labels.md there after make-scenes.py (lesson 13 reads it)"
true
