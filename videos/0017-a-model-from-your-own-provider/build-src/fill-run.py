"""Fill src/run/ from this video's own run of the qwen-local variant. Reads the run; writes only src/run/.

  python3 build-src/fill-run.py /Users/Shared/demo/practice/results/lesson-17/<run>

Writes RUN, trials.json (one row per trial), record.json (the typo-fix record's token usage, laid out the
way the panel shows it), results.jsonl (a copy, with /Users/Shared/demo shown as ~/src/demo) and s17.log
(what the tape's wrapper saved in /tmp/vl-l17/s17.log, with colour codes and the live progress redraws
removed: the text from the run's last "Comparison unavailable" line on, plus the FAIL blocks before it).
"""
import json, pathlib, re, sys

D = pathlib.Path(__file__).resolve().parent.parent
run = pathlib.Path(sys.argv[1])
src = run / 'qwen-local' / 'results.jsonl'
recs = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
order = ['after-release', 'refactor', 'security', 'two-changes', 'typo-fix']
recs.sort(key=lambda r: order.index(r['stimulus']))
rows = []
for r in recs:
    tu = (r.get('trajectory') or {}).get('metrics', {}).get('tokenUsage') or {}
    by = tu.get('byModel') or {}
    assert len(by) <= 1, by
    model, counts = next(iter(by.items())) if by else (r.get('model'), {})
    g = r.get('gradeResult') or {}
    failed = [d for d in g.get('details', []) if not d.get('passed')]
    rows.append(dict(
        stimulus=r['stimulus'], status=r.get('status'), error=r.get('status') != 'success',
        passed=bool(g.get('passed')) and r.get('status') == 'success',
        grader=failed[0]['name'] if failed else None, evidence=failed[0].get('evidence') if failed else None,
        inputTokens=counts.get('inputTokens', 0), outputTokens=counts.get('outputTokens', 0),
        cacheReadTokens=tu.get('cacheReadTokens', 0), callCount=tu.get('callCount'),
        durationMs=r.get('durationMs'), skillActivations=(r.get('trajectory') or {}).get('metrics', {}).get('skillActivationCount', 0),
        cost=tu.get('cost'), model=model, endReason=(r.get('trajectory') or {}).get('endReason')))
out = D / 'src/run'
(out / 'trials.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
(out / 'RUN').write_text(run.name + '\n')
(out / 'results.jsonl').write_text(src.read_text().replace('/Users/Shared/demo', '~/src/demo'))

typo = next(r for r in recs if r['stimulus'] == 'typo-fix')
tu = typo['trajectory']['metrics']['tokenUsage']
body = json.dumps(tu, indent=2).splitlines()
lines = ['    "metrics": {', '      "tokenUsage": ' + body[0]] + ['      ' + l for l in body[1:-1]] + ['      },']
(out / 'record.json').write_text('\n'.join(lines) + '\n')

ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b[()][A-Z0-9]|\r|\x04|\x08')
raw = ANSI.sub('', pathlib.Path('/tmp/vl-l17/s17.log').read_text(errors='replace')).splitlines()
last = max(n for n, l in enumerate(raw) if 'Comparison unavailable' in l)
end = next(n for n in range(last, len(raw)) if raw[n].strip().startswith('stimuli'))
fails, n = [], 0
while n < last:
    if re.match(r'\s*(FAIL|ERROR)\s+\S+', raw[n]) and raw[n].strip() not in [f.strip() for f in fails]:
        fails += [raw[n].rstrip(), raw[n + 1].rstrip(), '']
    n += 1
tail_end = min(len(raw), end + 4)
(out / 's17.log').write_text('\n'.join(fails + [l.rstrip() for l in raw[last:tail_end]]).replace('/Users/Shared/demo', '~/src/demo') + '\n')
for r in rows:
    print(r['stimulus'], r['status'], 'passed' if r['passed'] else 'failed', r['grader'], r['inputTokens'], r['outputTokens'],
          r['cacheReadTokens'], f"{r['durationMs'] / 1000:.0f}s", 'skill', r['skillActivations'], 'cost', r['cost'])
