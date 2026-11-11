"""Fill src/run/vally-executor.json from the series' own lesson 22 and 23 runs (saved by the lesson 23 video
in ../0023-check-what-the-agent-did/src/run/l22 and l23). Reads those; writes only src/run/ here.
One object per since-last-release trial through Vally's own executor: tokens, model calls, AIU, the
run's own verdict, whether the skill loaded, whether the patch adds an entry for #76."""
import json, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
SRC = D.parent / '0023-check-what-the-agent-did/src/run'
out = {'_about': "since-last-release through Vally's own executor: the series' own runs, "
                 + ' and '.join((SRC / r / 'RUN').read_text().strip() for r in ('l22', 'l23'))
                 + ' (5 and 3 trials a model). One object per trial. vx-from-series.py.'}
for run in ('l22', 'l23'):
    for line in (SRC / run / 'results.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get('type') != 'trial-result' or r.get('stimulus') != 'since-last-release':
            continue
        assert r['status'] == 'success', r['status']
        u = r['trajectory']['metrics']['tokenUsage']
        assert u['cost']['unit'] == 'nano-aiu'
        loaded = any(e.get('type') == 'skill_activation' for e in r['trajectory']['events'])
        patch = (SRC / run / f"{r['model']}-{r['trialIndex']}.patch").read_text()
        e76 = any('#76' in l for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
        m = out.setdefault(r['model'], {'passed': 0, 'loaded': 0, 'entry76': 0, 'trials': []})
        m['passed'] += bool(r['gradeResult']['passed']); m['loaded'] += loaded; m['entry76'] += e76
        m['trials'].append({'run': run, 'tokens': u['totalTokens'], 'calls': u['callCount'],
                            'aiu': round(u['cost']['amount'] / 1e9, 4), 'passed': bool(r['gradeResult']['passed']),
                            'loaded': loaded, 'entry76': e76})
(D / 'src/run/vally-executor.json').write_text(json.dumps(out, indent=1) + '\n')
for k, v in out.items():
    if k != '_about':
        t = v['trials']
        print(k, 'passed', v['passed'], 'loaded', v['loaded'], 'e76', v['entry76'], 'n', len(t),
              'tok/call', round(sum(x['tokens'] for x in t) / sum(x['calls'] for x in t)),
              'calls/trial', sum(x['calls'] for x in t) / len(t), 'aiu/trial', round(sum(x['aiu'] for x in t) / len(t), 2),
              'per-trial tok/call', [round(x['tokens'] / x['calls']) for x in t])
