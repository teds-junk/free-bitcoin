#!/bin/bash
# Copy this video series' own runs into src/run/, with /Users/Shared/demo shown as ~/src/demo.
# Reads the demo folder and /tmp/vl-l23; writes only inside this video's src/run/.
#   bash build-src/collect-run.sh l22    before recording: the saved lesson 22 run, a real tool_call event,
#                                         and the bash commands its trials ran (to choose swap-command.txt)
#   bash build-src/collect-run.sh l23    after recording s15, s16, s19, s21: the s21 run and the four logs
set -e
P=${DEMO_PRACTICE:-/Users/Shared/demo/practice}
V="$(cd "$(dirname "$0")/.." && pwd)"
W=${1:?l22 or l23}
case $W in
  l22) R=$P/results/lesson-22 ;;
  l23) R=$P/results/lesson-23 ;;
  *) echo "l22 or l23"; exit 2 ;;
esac
n=$(find "$R" -maxdepth 1 -type d -name '2026*' | wc -l | tr -d ' ')
[ "$n" = 1 ] || { echo "$R holds $n runs; expected exactly 1"; exit 1; }
RUN=$(find "$R" -maxdepth 1 -type d -name '2026*')
O=$V/src/run/$W
mkdir -p "$O"
sed 's|/Users/Shared/demo|~/src/demo|g' "$RUN/results.jsonl" > "$O/results.jsonl"
sed 's|/Users/Shared/demo|~/src/demo|g' "$RUN/eval-results.md" > "$O/eval-results.md"
basename "$RUN" > "$O/RUN"
for m in claude-haiku-4.5 gpt-5.6-terra; do
  for d in "$RUN"/release/since-last-release/$m/*/; do
    [ -d "$d" ] || continue
    t=$(basename "$d")
    # a trial that changed nothing has no patch; an empty file stands for it
    if [ -f "$d/workspace.patch" ]; then cp "$d/workspace.patch" "$O/$m-$t.patch"; else : > "$O/$m-$t.patch"; fi
  done
done
if [ "$W" = l23 ]; then
  for s in s15 s16 s19 s21; do cp "/tmp/vl-l23/$s.log" "$V/src/run/$s.log"; done
fi
python3 - "$O" "$V" "$W" <<'PY'
import json, sys, pathlib
O, V, W = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
ts = [json.loads(l) for l in (O / 'results.jsonl').read_text().splitlines() if l.strip()]
ts = [t for t in ts if t.get('type') == 'trial-result']
print(f'{W}: {len(ts)} trials;', 'ERROR:', [(t["model"], t["trialIndex"]) for t in ts if t['status'] != 'success'] or 'none')
for t in ts:
    mt = t['trajectory']['metrics']
    wd = t['trajectory'].get('workDir') or '\0'
    print(f"  {t['model']:17} trial {t['trialIndex']}  passed={t['gradeResult']['passed']}  "
          f"skills={mt.get('skillActivationBreakdown')}  tools={mt.get('toolCallBreakdown')}")
    for e in t['trajectory']['events']:
        if e['type'] == 'tool_call' and e['data']['toolName'] == 'bash':
            print('      bash:', (e['data'].get('arguments') or {}).get('command', '').replace(wd, '<workspace>'))
if W == 'l22':
    # one real tool_call event in which an agent opened the merged list, for s05's panel: a view call if
    # any trial made one, otherwise whichever call mentions the list
    pick = None
    for want in ('view', None):
        for t in ts:
            for e in t['trajectory']['events']:
                if pick is None and e['type'] == 'tool_call' \
                        and 'release/merged.txt' in json.dumps(e['data'].get('arguments')) \
                        and want in (None, e['data']['toolName']):
                    pick = (e, t['trajectory'].get('workDir') or '', t['model'], t['trialIndex'])
        if pick:
            break
    assert pick, 'no saved trial opened release/merged.txt: s05, s07 and the reads-the-list result need rewriting'
    e, wd, m, i = pick
    text = json.dumps(e, indent=2)
    if wd:
        text = text.replace(wd, '<workspace>')
    (V / 'src/run/tool-call-event.json').write_text(text + '\n')
    print(f'tool-call-event.json: a {e["data"]["toolName"]} call in {m} trial {i}')
    print('Now put one command word that exactly one haiku trial ran, and no terra trial, into src/run/swap-command.txt.')
PY
