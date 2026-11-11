#!/bin/bash
# Read-only check of what each tape needs in the demo folder. Usage, from the video folder:
#   bash build-src/check-state.sh s15|s16|s17|s18      (no argument: s15)
# It changes nothing. Exit 0 = ready; exit 1 = something listed below is not as the tape expects.
cd "$(dirname "$0")/.." || exit 1
P=/Users/Shared/demo/practice
bad=0
say(){ echo "  NOT READY: $*"; bad=1; }
same(){ [ -f "$2" ] && cmp -s "$1" "$2" || say "$2 differs from $1 (or is missing)"; }
absent_or_same(){ [ ! -e "$2" ] || cmp -s "$1" "$2" || say "$2 exists and differs from $1: the tape's hidden copy would overwrite it"; }
case "${1:-s15}" in
  s15|s16)
    command -v vally >/dev/null || say "vally is not on PATH"
    command -v node >/dev/null || say "node is not on PATH"
    same src/state/list-merged.mjs "$P/tools/list-merged.mjs"
    same src/state/CHANGELOG.md "$P/evals/fixtures/notes-cli/CHANGELOG.md"
    same src/state/SKILL.md "$P/skills/changelog-entry/SKILL.md"     # the skill as lesson 21 leaves it
    [ -d "$P/evals/grading" ] || say "$P/evals/grading is missing"
    absent_or_same src/state/release.eval.yaml "$P/evals/release.eval.yaml"
    absent_or_same src/state/check-release.mjs "$P/evals/grading/check-release.mjs"
    [ "$1" = s16 ] && [ -e "$P/results/lesson-22" ] && echo "  note: results/lesson-22 exists; s16 will move it aside, not delete it"
    ;;
  s17|s18)
    n=$(find "$P/results/lesson-22" -mindepth 1 -maxdepth 1 -type d -name '2026*' 2>/dev/null | wc -l | tr -d ' ')
    [ "$n" = 1 ] || say "need exactly one run folder under results/lesson-22, found $n"
    S=$(find "$P/results/lesson-22" -mindepth 1 -maxdepth 1 -type d -name '2026*' 2>/dev/null | head -1)/release/since-last-release
    if [ "$1" = s17 ]; then
      f="$S/claude-haiku-4.5/1/workspace.patch"
      [ -f "$f" ] || say "$f is missing"
      grep -q '(#76)' "$f" 2>/dev/null || say "haiku folder 1 did not record the refactor (#76): point tapes/s17.tape at a failing folder"
    else
      f="$S/gpt-5.6-terra/0/workspace.patch"
      [ -f "$f" ] || say "$f is missing"
      grep -q '(#76)' "$f" 2>/dev/null && say "terra folder 0 recorded the refactor (#76): point tapes/s18.tape at a passing folder"
      grep -q '(#74)' "$f" 2>/dev/null && grep -q '(#75)' "$f" 2>/dev/null || say "terra folder 0 lacks an entry for #74 or #75"
    fi
    ;;
  *) echo "usage: check-state.sh s15|s16|s17|s18"; exit 2;;
esac
[ $bad = 0 ] && echo "ready: ${1:-s15}"
exit $bad
