#!/bin/bash
# Read-only check of what each lesson 25 tape needs in the demo folder. Changes nothing.
#   bash build-src/check-state.sh [s16|s17|s20|s22|extract]     (no argument: everything)
P=/Users/Shared/demo/practice
V="$(cd "$(dirname "$0")/.." && pwd)"
want="${1:-all}"; fail=0
ok(){ echo "  ok    $1"; }
no(){ echo "  FAIL  $1"; fail=1; }
note(){ echo "  note  $1"; }
has(){ [ -e "$P/$1" ] && ok "$1 exists" || no "$1 is missing"; }
same(){ cmp -s "$P/$1" "$V/$2" && ok "$1 is the file the panels show" || no "$1 differs from $2"; }
sec(){ [ "$want" = all ] || [ "$want" = "$1" ]; }

if sec s16; then echo "s16  npm install --prefix app"
  has app/package.json; has app/package-lock.json
  [ -e "$P/app/node_modules" ] && note "app/node_modules exists: the tape moves it aside so npm prints 'added N packages'" || ok "app/node_modules is absent (npm will install)"
fi
if sec s17; then echo "s17  sh app/run.sh claude-haiku-4.5   (1 agent run)"
  [ -d "$P/app/node_modules/@github/copilot-sdk" ] && ok "the app's libraries are installed" || no "app/node_modules/@github/copilot-sdk is missing: record s16 first"
  same app/run.sh src/app/run.sh; same app/run.mjs src/app/run.mjs
  has app/release-assistant.mjs; has tools/list-merged.mjs; has evals/fixtures/notes-cli/CHANGELOG.md; has skills/changelog-entry/SKILL.md
  [ -e "$P/app-run" ] && note "app-run exists: the tape moves it aside before the script replaces it" || ok "no app-run yet"
fi
if sec s20; then echo "s20  node app/traces-to-atif.mjs ..."
  same app/traces-to-atif.mjs src/app/traces-to-atif.mjs; has app-run/traces.jsonl
fi
if sec s22; then echo "s22  vally grade ... < app-run/trajectory.json"
  has app-run/trajectory.json; has app-run/change.diff; has app-run/repo/CHANGELOG.md; has evals/grading/check-release.mjs
  if [ -e "$P/evals/release.eval.yaml" ]; then
    for g in every-change-handled reads-the-list never-commits no-loop loads-the-skill; do
      grep -q "name: $g" "$P/evals/release.eval.yaml" && ok "release.eval.yaml has grader $g" || no "release.eval.yaml has no grader $g"
    done
    grep -q "name: since-last-release" "$P/evals/release.eval.yaml" && ok "stimulus since-last-release" || no "no stimulus since-last-release"
    cmp -s "$P/evals/release.eval.yaml" "$V/src/release.eval.yaml" && ok "release.eval.yaml equals the copy the scenes quote" || note "release.eval.yaml differs from src/release.eval.yaml (fine if only the tracker-down stimulus differs; s15 quotes the five graders)"
  else no "evals/release.eval.yaml is missing: the lesson 22 to 24 videos create it"; fi
fi
if sec extract; then echo "extract-run.py  (the comparison with the lesson 23 video's run)"
  n=$(find "$P/results/lesson-23" -mindepth 1 -maxdepth 1 -type d -name '2026*' 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" = 1 ] && ok "results/lesson-23 holds exactly one run" || no "results/lesson-23 holds $n runs (need exactly one; pass the right folder to extract-run.py)"
  for l in s16 s17 s22; do [ -e "/tmp/vl-l25/$l.log" ] && ok "/tmp/vl-l25/$l.log exists" || no "/tmp/vl-l25/$l.log is missing"; done
fi
exit $fail
