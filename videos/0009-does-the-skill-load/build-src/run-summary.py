"""Read-only: print each trial of a run (model, stimulus, trial, status, passed, skills loaded)."""
import json, sys, pathlib
r = pathlib.Path(sys.argv[1]); err = 0
for l in (r / 'results.jsonl').read_text().splitlines():
    if not l.strip(): continue
    t = json.loads(l)
    if t.get('type') != 'trial-result': continue
    g = t.get('gradeResult') or {}
    sk = sorted({e['data']['name'] for e in (t.get('trajectory') or {}).get('events', []) if e['type'] == 'skill_activation'})
    err += t['status'] != 'success'
    print(f"{t['model']:18} {t['stimulus']:20} {t['trialIndex']} {t['status']:8} passed={g.get('passed')} skills={sk}")
print('ERROR trials:', err)
