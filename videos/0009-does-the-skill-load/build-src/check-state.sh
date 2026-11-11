#!/bin/bash
# Read-only: does /Users/Shared/demo/practice hold what this video's tapes need? Changes nothing.
# Run from anywhere:  bash build-src/check-state.sh
V="$(cd "$(dirname "$0")/.." && pwd)"; P=/Users/Shared/demo/practice; bad=0
ok(){ echo "  ok    $1"; }; no(){ echo "  FAIL  $1"; bad=1; }
same(){ if cmp -s "$1" "$2"; then ok "$3"; else no "$3"; fi; }
echo "s15 (free): the neighbours and the loading eval file, as the starter ships them"
same "$P/skills/commit-message/SKILL.md" "$V/src/state/commit-message.SKILL.md" "skills/commit-message/SKILL.md"
same "$P/skills/release-notes/SKILL.md"  "$V/src/state/release-notes.SKILL.md"  "skills/release-notes/SKILL.md"
same "$P/evals/loading.eval.yaml"        "$V/src/state/loading.eval.yaml"       "evals/loading.eval.yaml"
[ -f "$P/evals/fixtures/notes-cli/CHANGELOG.md" ] && ok "evals/fixtures/notes-cli/CHANGELOG.md exists" || no "evals/fixtures/notes-cli/CHANGELOG.md missing"
echo "s16 (24 runs): the skill before this lesson's edit. s16's hidden setup copies src/state/SKILL.before.md"
echo "    over it, so a difference here means the series' own skill is NOT verified/lesson-08's: look first."
if cmp -s "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.before.md"; then ok "skills/changelog-entry/SKILL.md is the lesson 8 state"
elif cmp -s "$P/skills/changelog-entry/SKILL.md" "$V/src/state/SKILL.after.md"; then ok "skills/changelog-entry/SKILL.md is already the lesson 9 state (s19 has run; s16 will put the old description back)"
else no "skills/changelog-entry/SKILL.md matches neither src/state/SKILL.before.md nor SKILL.after.md"; fi
for r in lesson-9-before lesson-9-after; do
  [ -e "$P/results/$r" ] && echo "  note  results/$r exists; its tape will move it aside to /Users/Shared/.demo-old.$r.<time>" || ok "results/$r not there yet"
done
type -P vally >/dev/null && ok "vally is on PATH" || no "vally is not on PATH"
exit $bad
