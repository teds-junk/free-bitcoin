"""Fill src/run/ from this video's own runs, after s16, s20 and s21 are recorded.

Reads (never writes) /Users/Shared/demo/practice/results/lesson-26/<run>/ and
results/lesson-26-experiment/<run>/, and the logs the tapes kept in /tmp/vl-l26/.
Writes, in src/run/: s16.log, s20.log, s21.log, RUN-eval, RUN-experiment, trials.tsv,
eval-report.json, trace-join.json. It does NOT write vally-executor.json or app-earlier.json:
those come from the lesson 22, 23 and 25 videos' runs.

Run against this video's real results folders on 2026-11-11 and checked by eye against eval-results.md,
the patches and the trace files.

    python3 build-src/collect-run.py
"""
import json, pathlib, re, sys

D = pathlib.Path(__file__).resolve().parent.parent
OUT = D / 'src/run'
P = pathlib.Path('/Users/Shared/demo/practice/results')
TMP = pathlib.Path('/tmp/vl-l26')
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
STIM = 'since-last-release'


def die(msg):
    sys.exit('collect-run: ' + msg)


def one_run(name):
    runs = sorted(p for p in (P / name).glob('2*') if p.is_dir())
    if len(runs) != 1:
        die(f'{P / name} should hold exactly one run folder, found {len(runs)}')
    return runs[0]


def clean(text):
    """What a terminal showed: drop colour codes and carriage returns, and show the demo folder as ~/src/demo."""
    text = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', text).replace('\r', '')
    return text.replace('/Users/Shared/demo', '~/src/demo')


def records(path):
    if not path.exists():
        die(f'no {path}')
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    return [r for r in rows if r.get('type') == 'trial-result' and r.get('stimulus') == STIM]


def trial_row(kind, variant, rec, run_dir):
    m = rec['trajectory']['metrics']
    usage = m.get('tokenUsage') or {}
    cost = usage.get('cost') or {}
    if cost.get('unit') != 'nano-aiu':
        die(f'no nano-aiu cost at trajectory.metrics.tokenUsage.cost in a {rec["model"]} record: {cost}')
    if rec.get('status') != 'success':
        die(f'{kind} {variant} {rec["model"]} trial {rec.get("trialIndex")} did not finish ({rec.get("status")}): re-record')
    skills = [e['data']['name'] for e in rec['trajectory'].get('events', []) if e.get('type') == 'skill_activation']
    patches = list(run_dir.glob(f'**/{STIM}/{rec["model"]}/{rec.get("trialIndex", 0)}/workspace.patch'))
    if len(patches) != 1:
        die(f'expected one workspace.patch for {rec["model"]} trial {rec.get("trialIndex")} under {run_dir}, found {len(patches)}')
    added = [l for l in patches[0].read_text().splitlines() if l.startswith('+') and not l.startswith('+++')]
    return [kind, variant, rec['model'], str(bool(rec['gradeResult']['passed'])).lower(), ','.join(sorted(set(skills))) or '-',
            str(usage['totalTokens']), str(usage['callCount']), f'{cost["amount"] / 1e9:.6g}',
            str(any('#76' in l for l in added)).lower(), str(m.get('wallTimeMs', rec.get('durationMs', 0)))]


ev, ex = one_run('lesson-26'), one_run('lesson-26-experiment')
rows = [trial_row('eval', '-', r, ev) for r in records(ev / 'results.jsonl')]
for variant in ('haiku', 'terra'):
    vdir = ex / variant
    files = list(vdir.glob('**/results.jsonl'))
    if len(files) != 1:
        die(f'expected one results.jsonl under {vdir}, found {len(files)}')
    rows += [trial_row('experiment', variant, r, vdir) for r in records(files[0])]
if len(rows) != 8:
    die(f'expected 8 {STIM} trials (2 from the eval, 6 from the experiment), found {len(rows)}')
head = ['run', 'variant', 'model', 'passed', 'skills', 'tokens', 'calls', 'aiu', 'entry76', 'wall_ms']
(OUT / 'trials.tsv').write_text('\n'.join('\t'.join(r) for r in [head] + rows) + '\n')
(OUT / 'RUN-eval').write_text(ev.name + '\n')
(OUT / 'RUN-experiment').write_text(ex.name + '\n')

# eval-results.md: the "> Model: … | Executor: …" line under each table, and the since-last-release row,
# read by the table's own header (a table with no Skills column means no skill loaded).
report, md = {}, (ev / 'eval-results.md').read_text().splitlines()
for mdl in MODELS:
    line = next((l for l in md if l.startswith('> Model: ' + mdl)), None)
    at = next((i for i, l in enumerate(md) if l.startswith(f'| {STIM} ') and f'| {mdl} |' in l), None)
    if line is None or at is None:
        die(f'eval-results.md has no Model line or {STIM} row for {mdl}')
    head = next(md[i] for i in range(at, -1, -1) if md[i].startswith('| Stimulus '))
    cols = [c.strip() for c in head.strip('|').split('|')]
    cells = [c.strip() for c in md[at].strip().strip('|').split('|')]
    if len(cells) != len(cols):
        die(f'{mdl}: {len(cells)} cells under {len(cols)} headers')
    row = dict(zip(cols, cells))
    calls = re.search(r'</summary>([^<]*)</details>', row['Tool Calls'])
    report[mdl] = {'executor': re.search(r'Executor: (\S+)', line).group(1),
                   'skills': re.findall(r'`([^`]+)`', row.get('Skills', '')),
                   'has_skills_column': 'Skills' in cols,
                   'tool_calls': calls.group(1).strip() if calls else row['Tool Calls']}
report['_about'] = 'From eval-results.md of the s16 run (collect-run.py).'
(OUT / 'eval-report.json').write_text(json.dumps(report, indent=1) + '\n')


def spans(path, name):
    out = []
    for l in path.read_text().splitlines():
        if f'"name":"{name}"' in l.replace('": "', '":"'):
            out.append(json.loads(l))
    return out


traces = list(ev.glob(f'**/{STIM}/{MODELS[0]}/0/executor-artifacts/app-traces.jsonl'))
if len(traces) != 1:
    die(f'expected one app-traces.jsonl for {MODELS[0]} trial 0 under {ev}, found {len(traces)}')
sessions = spans(traces[0], 'invoke_agent')
if len(sessions) != 1:
    die(f'expected one invoke_agent span in {traces[0]}, found {len(sessions)}')
s = sessions[0]
attempts = [a for a in spans(ev / 'otel-spans.jsonl', 'vally.attempt') if a.get('traceId') == s.get('traceId')]
if len(attempts) != 1:
    die(f'expected one vally.attempt span with trace id {s.get("traceId")} in otel-spans.jsonl, found {len(attempts)}')
pick = lambda d: {k: d.get(k) for k in ('traceId', 'spanId', 'parentSpanId', 'name')}
(OUT / 'trace-join.json').write_text(json.dumps({
    '_about': 'Two span lines from the s16 run, cut to their ids (collect-run.py).',
    'attempt': pick(attempts[0]), 'session': pick(s)}, indent=1) + '\n')

for sid in ('s16', 's20', 's21'):
    src = TMP / f'{sid}.log'
    if not src.exists():
        die(f'no {src}: the tape keeps what Vally printed there while it records')
    (OUT / f'{sid}.log').write_text(clean(src.read_text()))
print('collected', ev.name, ex.name)
print('next: fill vally-executor.json and app-earlier.json from the earlier videos, count the GitHub tools in',
      traces[0], 'against facts.json, rm src/run/PROVISIONAL, then make-scenes.py and panels.sh')
