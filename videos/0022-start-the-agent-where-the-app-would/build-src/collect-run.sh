#!/bin/bash
# Replace the stand-in run in src/run/ with this video's own lesson 22 run. Run from the video folder,
# after tapes/s16.tape has been recorded. Reads /Users/Shared/demo/practice/results/lesson-22 (exactly
# one run folder) and /tmp/vl-l22/s16.log; writes only into src/run/. Nothing in the demo folder changes.
set -euo pipefail
cd "$(dirname "$0")/.."
R=/Users/Shared/demo/practice/results/lesson-22
n=$(find "$R" -mindepth 1 -maxdepth 1 -type d -name '2026*' | wc -l | tr -d ' ')
[ "$n" = 1 ] || { echo "expected exactly one run folder under $R, found $n" >&2; exit 1; }
RUN=$(basename "$(find "$R" -mindepth 1 -maxdepth 1 -type d -name '2026*')")
S="$R/$RUN/release/since-last-release"
for m in claude-haiku-4.5 gpt-5.6-terra; do for i in 0 1 2 3 4; do
  cp "$S/$m/$i/workspace.patch" "src/run/$m-$i.patch"
done; done
python3 - "$R/$RUN/results.jsonl" <<'PY'
import json, sys
out = []
for line in open(sys.argv[1]):
    if not line.strip(): continue
    t = json.loads(line)
    if t.get('type') != 'trial-result': continue
    tr = t['trajectory']
    out.append({"model": t['model'], "trial": t['trialIndex'], "status": t['status'],
                "passed": bool(t['gradeResult']['passed']),
                "loaded": tr['metrics'].get('skillActivationCount', 0) > 0,
                "reply": (tr.get('output') or '').replace('/Users/Shared/demo', '~/src/demo')})
out.sort(key=lambda x: (x['model'], x['trial']))
json.dump(out, open('src/run/trials.json', 'w'), indent=1)
print(len(out), 'trials')
PY
[ -f /tmp/vl-l22/s16.log ] && sed 's|/Users/Shared/demo|~/src/demo|g' /tmp/vl-l22/s16.log | sed $'s/\x1b\\[[0-9;?]*[A-Za-z]//g; s/\r$//' > src/run/s16.log || echo "warning: /tmp/vl-l22/s16.log missing; s16.log left as it was" >&2
printf '%s\n' "$RUN" > src/run/RUN
rm -f src/run/PROVISIONAL
echo "collected $RUN; now: python3 build-src/make-scenes.py && bash build-src/panels.sh"
