"""Replace the stand-ins in src/ with the series' own runs. Reads the demo folder; writes only inside
this video's folder. Starts no agent and runs no vally command.

  python3 build-src/capture-run.py --budgets
      BEFORE recording, once the series' own lesson 16 run exists. Reads its four variants'
      results.jsonl, finds the largest median tokens, turns and duration per stimulus, and writes
      src/state/budgets.json (first budgets: typical rounded up a little; wider: about twice) and the
      'typical' facts. Then run build-src/make-state.py, and record s16, s18, s21, then s23.

  python3 build-src/capture-run.py
      AFTER all four tapes are recorded. Copies /tmp/vl-l18/<scene>.log into src/run/ (control
      characters removed, the demo path shown as ~/src/demo), rewrites src/run/facts.json from the
      lesson 16 and lesson 18 runs, and deletes src/run/PROVISIONAL. Then run build-src/make-scenes.py:
      its asserts say which `outcome` sentences in build-src/make-storyboard.py need rewording.
"""
import glob, json, math, pathlib, re, statistics, sys

D = pathlib.Path(__file__).resolve().parent.parent
P = pathlib.Path('/Users/Shared/demo/practice')
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f]')


def one(pattern, what):
    hits = sorted(glob.glob(str(P / pattern)))
    assert len(hits) == 1, f'expected exactly one {what}, found {len(hits)}: {pattern}'
    return pathlib.Path(hits[0])


def trials(path):
    out = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get('type') != 'trial-result':     # a run also writes summary lines
            continue
        m = (r.get('trajectory') or {}).get('metrics') or {}
        tu = m.get('tokenUsage') or {}
        out.append({'stimulus': r.get('stimulus'), 'model': r.get('model'), 'status': r.get('status'),
                    'passed': bool((r.get('gradeResult') or {}).get('passed')),
                    'tokens': tu.get('totalTokens'), 'turns': m.get('turnCount'), 'ms': m.get('wallTimeMs'),
                    'cost': (tu.get('cost') or {}).get('amount')})
    return out


def lesson16():
    run = one('results/lesson-16/2026*', 'run under results/lesson-16')
    v = {d.name: trials(d / 'results.jsonl') for d in sorted(run.iterdir()) if (d / 'results.jsonl').exists()}
    assert {'haiku-high', 'terra-high'} <= set(v), sorted(v)
    return run.name, v


def typical(variants):
    """The largest per-stimulus median, across variants, for tokens, turns and seconds (as report.md prints them)."""
    best = {}
    for name, ts in variants.items():
        for stim in sorted({t['stimulus'] for t in ts}):
            done = [t for t in ts if t['stimulus'] == stim and t['tokens'] is not None]
            if not done:
                continue
            for key, field, f in (('tokens', 'tokens', round), ('turns', 'turns', lambda x: x), ('seconds', 'ms', lambda x: round(x / 1000, 1))):
                val = f(statistics.median(t[field] for t in done))
                if key not in best or val > best[key]['value']:
                    best[key] = {'value': val, 'variant': name, 'stimulus': stim}
    best['turns']['value'] = int(best['turns']['value']) if float(best['turns']['value']).is_integer() else best['turns']['value']
    return best


up = lambda x, step: int(math.ceil(x / step) * step)
facts_path = D / 'src/run/facts.json'
facts = json.loads(facts_path.read_text())
run16, variants = lesson16()
typ = typical(variants)
facts.update({'l16_run': run16, 'typical': typ})

if '--budgets' in sys.argv:
    tight = {'tokens': up(typ['tokens']['value'] + 1, 1000), 'turns': math.ceil(typ['turns']['value']),
             'wall': f"{math.ceil(typ['seconds']['value'] + 0.01)}s"}
    wide = {'tokens': up(2 * typ['tokens']['value'], 5000), 'turns': 2 * math.ceil(typ['turns']['value']),
            'wall': f"{up(2 * typ['seconds']['value'], 5)}s"}
    bp = D / 'src/state/budgets.json'
    b = json.loads(bp.read_text())
    b.update({'tight': tight, 'wide': wide,
              '_about': b['_about'].split(' STAND-IN')[0] + f' Set from the series\' own lesson 16 run {run16} by capture-run.py --budgets.'})
    bp.write_text(json.dumps(b, indent=2) + '\n')
    facts_path.write_text(json.dumps(facts, indent=1) + '\n')
    print(json.dumps({'typical': typ, 'tight': tight, 'wide': wide}, indent=1))
    print('budgets written. Next: python3 build-src/make-state.py, then record. src/run/ logs are still stand-ins.')
    sys.exit(0)

# ---- after recording ----
for sid in ('s16', 's18', 's21', 's23'):
    src = pathlib.Path(f'/tmp/vl-l18/{sid}.log')
    assert src.exists() and src.stat().st_size, f'{src} is missing or empty: record {sid} first'
    text = ANSI.sub('', src.read_text(errors='replace').replace('\r', ''))
    text = text.replace('/private/Users/Shared/demo', '~/src/demo').replace('/Users/Shared/demo', '~/src/demo')
    (D / 'src/run' / f'{sid}.log').write_text(text)

hh, th = variants['haiku-high'], variants['terra-high']
by_model = {}
for ts in variants.values():
    for t in ts:
        if t['tokens'] is not None:
            by_model.setdefault(t['model'], []).append(t)
run18 = one('results/lesson-18/2026*', 'run under results/lesson-18')
live = trials(run18 / 'results.jsonl')
models18 = sorted({t['model'] for t in live})
l16_only = set(by_model)
for t in live:
    if t['tokens'] is not None and t['model'] not in l16_only:
        by_model.setdefault(t['model'], []).append(t)
done = [t for t in live if t['tokens'] is not None]
tot = {m: (sum(t['tokens'] for t in ts), sum(t['cost'] or 0 for t in ts)) for m, ts in by_model.items()}
l16_models = sorted({t['model'] for ts in variants.values() for t in ts})
facts.pop('terra_high_turns', None)
facts.update({
    'l16_failed_or_error_trials': {k: sum(not (t['status'] == 'success' and t['passed']) for t in ts) for k, ts in variants.items()},
    # every trial of the two re-graded variants passed in the experiment itself, so any trial a budget failed had
    'budget_failed_trials_passed_in_the_experiment': all(t['passed'] for t in hh + th if t['status'] == 'success'),
    # the terra-high stimulus whose trials took the widest spread of turns: (stimulus, sorted distinct turn counts)
    'terra_high_turns_one_stimulus': (lambda best: {'stimulus': best[0], 'turns': best[1]})(max(
        ((st, sorted({t['turns'] for t in th if t['stimulus'] == st and t['turns'] is not None})) for st in sorted({t['stimulus'] for t in th})),
        key=lambda x: (x[1][-1] - x[1][0], len(x[1])))),
    # typical tokens per model: lesson 16's trials for its two models, lesson 18's own run for the others
    'median_tokens_by_model': {m: round(statistics.median(t['tokens'] for t in ts)) for m, ts in sorted(by_model.items())},
    'terra_fewest_tokens_highest_cost': (lambda a: min(a, key=lambda m: statistics.median(t['tokens'] for t in by_model[m])) ==
                                         max(a, key=lambda m: statistics.median((t['cost'] or 0) for t in by_model[m])) == 'gpt-5.6-terra')(sorted(l16_only)),
    'live': {'run': run18.name,
             'passed': {m: f"{sum(t['passed'] and t['status'] == 'success' for t in live if t['model'] == m)}/{sum(t['model'] == m for t in live)}" for m in models18},
             'errors': sum(t['status'] != 'success' for t in live),
             'largest_tokens': max(t['tokens'] for t in done), 'largest_turns': max(t['turns'] for t in done),
             'slowest_seconds': round(max(t['ms'] for t in done) / 1000, 1)},
    '_about': f'Facts the scenes quote that the logs do not hold, from the series\' own lesson 16 run {run16} and lesson 18 run {run18.name} (capture-run.py).',
})
facts_path.write_text(json.dumps(facts, indent=1) + '\n')
(D / 'src/run/PROVISIONAL').unlink(missing_ok=True)
print(json.dumps(facts, indent=1))
print('capture-ok. Next: python3 build-src/make-scenes.py (its asserts name what to reword).')
