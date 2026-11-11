"""Fill src/run/ from this video's own recordings. Reads /tmp/vl-l20/*.log and /Users/Shared/demo/practice
(read-only); writes only inside this video's src/run/. Run after all eleven tapes are recorded.

Not tested against real lesson 20 runs (none existed when it was written); the field names were checked
against the lesson 5 video's saved run. Read what it prints.
"""
import json, pathlib, re, sys

D = pathlib.Path(__file__).resolve().parent.parent
RUN = D / 'src/run'
P = pathlib.Path('/Users/Shared/demo/practice')
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\r')
H, T = 'claude-haiku-4.5', 'gpt-5.6-terra'

for sid in 's14 s18 s19 s24 s25 s30 s31 s34'.split():
    src = pathlib.Path('/tmp/vl-l20') / f'{sid}.log'
    if not src.exists():
        sys.exit(f'{src} is missing: record tapes/{sid}.tape first')
    (RUN / f'{sid}.log').write_text(ANSI.sub('', src.read_text(errors='replace')))
    print('log', sid)

runs = sorted(list((P / 'results/lesson-20-earlier').glob('2026*')) + list((P / 'results/lesson-20').glob('2026*')))


def trials(run):
    f = run / 'results.jsonl'
    return [t for t in map(json.loads, filter(str.strip, f.read_text().splitlines()))
            if t.get('type') == 'trial-result'] if f.exists() else []


def broken(name):
    """The first run of that eval: the one recorded before its fix."""
    hits = [r for r in runs if (r / name).is_dir()]
    if not hits:
        sys.exit(f'no run of {name} under results/lesson-20 or results/lesson-20-earlier')
    return hits[0]


facts = json.loads((RUN / 'facts.json').read_text())
ml, q, e, j = broken('merged-list'), broken('quick'), broken('entry'), broken('judged')
facts['trial_files'] = {
    'merged-list': sorted(p.name for p in (ml / 'merged-list/from-the-list' / H / '0').iterdir()),
    'quick': sorted(p.name for p in (q / 'quick/typo-fix' / H / '0').iterdir())}
facts['duration_ms'] = {'merged-list': sorted(t['durationMs'] for t in trials(ml))}


def events(model):
    f = q / 'quick/typo-fix' / model / '0/events.jsonl'
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()]


def aiu(ev):
    cp = [x for x in ev if x['type'] == 'session.usage_checkpoint']
    return round(cp[-1]['data']['totalNanoAiu'] / 1e9, 2) if cp else None


facts['aiu'] = {m: aiu(events(m)) for m in (H, T)}


def tail(ev):
    """From skill.invoked (when it is within the last 8 events) to the end, shortened as the page shows it."""
    start = max(len(ev) - 6, 0)
    for i in range(len(ev) - 1, max(len(ev) - 9, -1), -1):
        if ev[i]['type'] == 'skill.invoked':
            start = i
            break
    out = []
    for x in ev[start:]:
        t = x['type']
        if t == 'abort':
            out.append('{"type":"abort","data":{"reason":"%s"}, …}' % x.get('data', {}).get('reason'))
        elif t == 'session.usage_checkpoint':
            out.append('{"type":"session.usage_checkpoint",\n "data":{"totalNanoAiu":%d, …}, …}' % x['data']['totalNanoAiu'])
        else:
            out.append('{"type":"%s", …}' % t)
    return out


model = T if any(x['type'] == 'skill.invoked' for x in events(T)[-8:]) else H
facts['events_tail_model'] = model
(RUN / 'events-tail.txt').write_text('\n'.join(tail(events(model))) + '\n')
print('events tail from', model, '| AIU', facts['aiu'])

(RUN / 'entry-haiku.patch').write_text((e / 'entry/typo-fix' / H / '0/workspace.patch').read_text())
rec = next(g for t in trials(j) if t['model'] == H for g in t['gradeResult']['details']
           if (g.get('configuredName') or g['name']) == 'users-words')
(RUN / 'judge-record.json').write_text(json.dumps(
    {k: rec.get(k) for k in ('name', 'status', 'kind', 'passed', 'score', 'evidence')}, indent=1) + '\n')
(RUN / 'facts.json').write_text(json.dumps(facts, indent=2) + '\n')
print('trial folders', facts['trial_files'], '| durations', facts['duration_ms'])
print('Now: set earlier_slowest_s in src/run/facts.json by hand, delete src/run/PROVISIONAL, and run')
print('     python3 build-src/make-scenes.py && bash build-src/panels.sh')
