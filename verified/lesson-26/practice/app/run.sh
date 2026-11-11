#!/bin/sh
# Run the release app once, outside Vally, as the release
# tooling does after a merge. From the practice folder:
#   sh app/run.sh <model>
# Everything it makes goes in app-run/ (replaced each time):
#   repo/          the checkout the agent works in
#   before/        a copy of repo/ before the agent started
#   traces.jsonl   the app's OpenTelemetry traces
#   change.diff    what the agent changed, as a diff
set -e
rm -rf app-run
mkdir -p app-run/repo/release app-run/repo/tools
mkdir -p app-run/skills

# The checkout: the same files the eval file stages.
cp evals/fixtures/notes-cli/CHANGELOG.md app-run/repo/
cp tools/list-merged.mjs app-run/repo/tools/
cp -R skills/changelog-entry app-run/skills/

# The release tooling's own setup step.
cd app-run/repo
node tools/list-merged.mjs > release/merged.txt
cd ../..
cp -R app-run/repo app-run/before

# The app itself: one agent session, traced to a file.
node app/run.mjs app-run/repo app-run/skills "$1" \
  app-run/traces.jsonl

# What changed. diff exits 1 when it finds a difference.
cd app-run
diff -ruN before repo > change.diff || true
echo "Wrote app-run/traces.jsonl and app-run/change.diff"
