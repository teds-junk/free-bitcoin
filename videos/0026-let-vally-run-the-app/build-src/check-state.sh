#!/bin/bash
# Read-only check of what lesson 26's tapes need in the demo folder. Changes nothing.
#   bash build-src/check-state.sh          (from the video folder)
# Exit 0 when every "need" holds; "note" lines are for the person recording.
P=/Users/Shared/demo/practice
V="$(cd "$(dirname "$0")/.." && pwd)"
bad=0
need(){ if eval "$2"; then echo "ok    $1"; else echo "NEED  $1"; bad=1; fi; }
note(){ echo "note  $1"; }

need "practice folder exists"                              "[ -d $P ]"
need "app/node_modules has @microsoft/vally (npm install --prefix app, from lesson 25)" \
                                                           "[ -d $P/app/node_modules/@microsoft/vally ]"
need "app/node_modules has @github/copilot-sdk"            "[ -d $P/app/node_modules/@github/copilot-sdk ]"
need "app/release-assistant.mjs is the file the panel shows" \
                                                           "cmp -s $P/app/release-assistant.mjs $V/src/state/release-assistant.mjs"
if cmp -s $P/app/vally-executor.mjs $V/src/state/vally-executor.stub.mjs; then
  echo "ok    app/vally-executor.mjs is the shipped stub (s16 installs the written one)"
elif cmp -s $P/app/vally-executor.mjs $V/src/state/vally-executor.mjs; then
  echo "ok    app/vally-executor.mjs already has execute written"
else
  echo "NEED  app/vally-executor.mjs is neither the shipped stub nor the lesson's file: s16 would overwrite it"; bad=1
fi
need "evals/release.eval.yaml is as lesson 24 leaves it (since-last-release with five graders, tracker-down with its simulation block)" \
                                                           "cmp -s $P/evals/release.eval.yaml $V/src/state/release.eval.yaml"
need ".vally.yaml exists (lesson 21 creates it)"           "[ -f $P/.vally.yaml ]"
if grep -q '^plugins:' $P/.vally.yaml 2>/dev/null; then
  if head -3 $P/.vally.yaml | cmp -s - $V/src/state/plugins.yaml; then
    echo "ok    .vally.yaml already starts with the three plugins lines"
  else
    echo "NEED  .vally.yaml has a plugins section that is not the lesson's three lines"; bad=1
  fi
else
  echo "ok    .vally.yaml has no plugins section yet (s16 puts the three lines at its top)"
  cmp -s $P/.vally.yaml $V/src/state/vally.before.yaml || note ".vally.yaml differs from verified/lesson-25's; the s09 panel shows verified/lesson-26's lines 1-5, so check line 4 is still 'suites:'"
fi
need "vally is on PATH"                                    "type -P vally >/dev/null"
need "node is on PATH"                                     "type -P node >/dev/null"
for d in lesson-26 lesson-26-experiment; do
  [ -e $P/results/$d ] && note "results/$d exists; its tape moves it aside to /Users/Shared/.demo-old.$d.<time>"
done
[ -e $P/evals/release-app.experiment.yaml ] && { cmp -s $P/evals/release-app.experiment.yaml $V/src/state/release-app.experiment.yaml \
  && echo "ok    evals/release-app.experiment.yaml is already the lesson's file" \
  || { echo "NEED  evals/release-app.experiment.yaml exists and differs: s20 would overwrite it"; bad=1; }; }
note "for collect-run.py afterwards: results/lesson-26 and results/lesson-26-experiment must each hold exactly one run folder"
exit $bad
