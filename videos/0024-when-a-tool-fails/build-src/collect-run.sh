#!/bin/bash
# Copy this video's own run and recordings into src/run/, with /Users/Shared/demo shown as ~/src/demo.
# Reads the demo folder and /tmp/vl-l24; writes only inside this video's src/run/.
# Run after recording s17, s18 and s20:   bash build-src/collect-run.sh
set -e
P=${DEMO_PRACTICE:-/Users/Shared/demo/practice}
V="$(cd "$(dirname "$0")/.." && pwd)"
R=$P/results/lesson-24
n=$(find "$R" -maxdepth 1 -type d -name '2026*' | wc -l | tr -d ' ')
[ "$n" = 1 ] || { echo "$R holds $n runs; expected exactly 1"; exit 1; }
RUN=$(find "$R" -maxdepth 1 -type d -name '2026*')
O=$V/src/run
sed 's|/Users/Shared/demo|~/src/demo|g' "$RUN/results.jsonl" > "$O/results.jsonl"
[ -f "$RUN/eval-results.md" ] && sed 's|/Users/Shared/demo|~/src/demo|g' "$RUN/eval-results.md" > "$O/eval-results.md"
basename "$RUN" > "$O/RUN"
# vally's output as the tapes saved it: colour codes and carriage returns removed
for s in s17 s18 s20; do
  sed $'s/\x1b\\[[0-9;?]*[A-Za-z]//g' "/tmp/vl-l24/$s.log" | tr -d '\r' > "$O/$s.log"
done
# which trials left a patch (writes-nothing passes only when there is none, or it is empty)
for m in claude-haiku-4.5 gpt-5.6-terra; do
  for d in "$RUN"/release/tracker-down/$m/*/; do
    [ -d "$d" ] || continue
    f="$d/workspace.patch"
    if [ -s "$f" ]; then echo "PATCH $m $(basename "$d"): $(wc -l < "$f") lines"; else echo "no patch $m $(basename "$d")"; fi
  done
done
python3 - "$O" <<'PY'
import json, sys, pathlib
O = pathlib.Path(sys.argv[1])
ts = [json.loads(l) for l in (O / 'results.jsonl').read_text().splitlines() if l.strip()]
ts = [t for t in ts if t.get('type') == 'trial-result']
print(f'{len(ts)} trials;', 'ERROR:', [(t["model"], t["trialIndex"]) for t in ts if t['status'] != 'success'] or 'none')
for t in sorted(ts, key=lambda t: (t['model'], t['trialIndex'])):
    mt = t['trajectory']['metrics']
    wd = t['trajectory'].get('workDir') or '\0'
    g = {(d.get('configuredName') or d['name']): d['passed'] for d in t['gradeResult']['details']}
    print(f"\n=== {t['model']} trial {t['trialIndex'] + 1} (folder {t['trialIndex']})  status={t['status']}  passed={t['gradeResult']['passed']}  "
          f"simulated={mt.get('simulatedToolCallCount')}  tools={mt.get('toolCallBreakdown')}\n    graders={g}")
    for d in t['gradeResult']['details']:
        if not d['passed']:
            print('    FAILED', d.get('configuredName') or d['name'], '::', d.get('evidence'))
    for e in t['trajectory']['events']:
        if e['type'] == 'tool_call':
            print('    call', e['data']['toolName'], json.dumps(e['data'].get('arguments'))[:260].replace(wd, '<workspace>'))
        if e['type'] == 'tool_result':
            print('      ->', json.dumps(e['data'])[:300].replace(wd, '<workspace>'))
    print('    REPLY:', (t['trajectory'].get('output') or '').strip().replace(wd, '<workspace>'))
PY
