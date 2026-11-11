"""Fill src/run/ from this video's own run of the app. Reads only; writes only into src/run/.

  python3 build-src/extract-run.py <practice folder> <the lesson 23 video's run folder> [--logs /tmp/vl-l25]

Run it after s16, s17, s20 and s22 are recorded. It reads <practice>/app-run/ (traces.jsonl,
trajectory.json, change.diff), the tapes' logs, and the lesson 23 run's results.jsonl, and writes the
cleaned files the scenes show. Cleaning: /Users/Shared/demo becomes ~/src/demo, any other /Users/<name>
path becomes ~, the account attribute (enduser.pseudo.id) is removed, and long values are cut short
with "…" (a trace holds the whole prompt and every file the agent opened). Line counts are unchanged.
Then delete src/run/PROVISIONAL and run make-scenes.py and panels.sh; the generator's asserts say
which sentences need rewording.
"""
import json, pathlib, re, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
logs = pathlib.Path(sys.argv[sys.argv.index('--logs') + 1]) if '--logs' in sys.argv else pathlib.Path('/tmp/vl-l25')
practice, l23dir = pathlib.Path(args[0]), pathlib.Path(args[1])
RUN = pathlib.Path(__file__).resolve().parent.parent / 'src/run'
CUT = 72


def scrub(text):
    text = text.replace('/private/Users/Shared/demo', '~/src/demo').replace('/Users/Shared/demo', '~/src/demo')
    text = re.sub(r'(/private)?/var/folders/[^\s"\\\']+', '/tmp/app-work', text)
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+', '(email removed)', text)
    return re.sub(r'/Users/[^/\s"\\]+', '~', text)


def cut(v):
    if isinstance(v, str):
        return v if len(v) <= CUT else v[:CUT - 1] + '…'
    if isinstance(v, list):
        return [cut(x) for x in v]
    if isinstance(v, dict):
        return {k: cut(x) for k, x in v.items()}
    return v


def plain(text):
    return re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', text).replace('\r', '')


raw = [l for l in (practice / 'app-run/traces.jsonl').read_text().splitlines() if l.strip()]
spans = [s for s in map(json.loads, raw) if s.get('type') == 'span']
spans.sort(key=lambda s: (s['startTime'][0], s['startTime'][1]))
op = lambda s: s['attributes'].get('gen_ai.operation.name')
tools = [s for s in spans if op(s) == 'execute_tool']
chats = [s for s in spans if op(s) == 'chat']
roots = [s for s in spans if s['name'].startswith('invoke_agent')]
merged = [i for i, s in enumerate(tools, 1) if 'release/merged.txt' in str(s['attributes'].get('gen_ai.tool.call.arguments'))]
assert chats and tools and len(roots) == 1 and not roots[0].get('parentSpanId') and merged, (len(chats), len(tools), len(roots), merged)

TOP = ['type', 'traceId', 'spanId', 'parentSpanId', 'name', 'attributes']


def laid_out(span, first):
    """One span as JSON, one attribute per line: the ones the scene shows first, the rest after."""
    a = dict(span['attributes'])
    missing = [k for k in first if k not in a]
    assert not missing, f'{span["name"]}: no attribute {missing}'
    # Only the attributes a panel shows keep their values; every other attribute and field is hidden on
    # screen ("N lines hidden"), so its value is dropped here: the prompt, the account id, the tool list.
    attrs = {k: a[k] for k in first} | {k: '…' for k in a if k not in first}
    out = {k: span.get(k) for k in TOP[:5]} | {'attributes': attrs} | {k: '…' for k in span if k not in TOP}
    return scrub(json.dumps(cut(json.loads(scrub(json.dumps(out)))), indent=1, ensure_ascii=False)) + '\n'


(RUN / 'span-chat.json').write_text(laid_out(chats[0], [
    'gen_ai.operation.name', 'gen_ai.request.model', 'gen_ai.conversation.id', 'gen_ai.usage.input_tokens',
    'gen_ai.usage.output_tokens', 'github.copilot.nano_aiu', 'gen_ai.output.messages']))
(RUN / 'span-tool.json').write_text(laid_out(tools[merged[0] - 1], [
    'gen_ai.operation.name', 'gen_ai.tool.name', 'gen_ai.tool.call.id', 'gen_ai.tool.call.arguments',
    'gen_ai.tool.call.result']))
(RUN / 'counts.json').write_text(json.dumps({
    'trace_lines': len(raw), 'tool_spans': [s['name'] for s in tools],
    'timing_lines': sum('session.timing' in l for l in raw),
    'skill_calls': sum(s['attributes'].get('gen_ai.tool.name') == 'skill' for s in tools),
    'merged_list_call': merged[0], 'root_span': roots[0]['name'],
    'chat_parent_is_root': chats[0].get('parentSpanId') == roots[0]['spanId'],
    'model': chats[0]['attributes'].get('gen_ai.request.model')}, indent=2) + '\n')

traj = json.loads(scrub((practice / 'app-run/trajectory.json').read_text()))
(RUN / 'trajectory.json').write_text(json.dumps(cut(traj), indent=2, ensure_ascii=False) + '\n')
(RUN / 'change.diff').write_text(scrub((practice / 'app-run/change.diff').read_text()))
for name in ('s16', 's17', 's22'):
    (RUN / f'{name}.log').write_text(scrub(plain((logs / f'{name}.log').read_text())))

trials = [json.loads(l) for l in (l23dir / 'results.jsonl').read_text().splitlines() if l.strip()]
trials = [t for t in trials if t.get('type') == 'trial-result' and t['stimulus'] == 'since-last-release'
          and t['model'] == 'claude-haiku-4.5']
bad = [t['trialIndex'] for t in trials if t['status'] != 'success']
assert trials and not bad, f'lesson 23 run: {len(trials)} trials, did not finish: {bad}'
graders = {}
for t in trials:
    for g in t['gradeResult']['details']:
        name = g.get('configuredName') or g['name']
        graders[name] = graders.get(name, 0) + bool(g['passed'])
(RUN / 'l23.json').write_text(json.dumps({'run': l23dir.name, 'model': 'claude-haiku-4.5', 'stimulus': 'since-last-release',
                                          'trials': len(trials), 'graders': graders}, indent=2) + '\n')
left = [p.name for p in RUN.iterdir() if p.is_file() and re.search(r'/Users/|/var/folders|@[\w-]+\.\w', p.read_text())]
assert not left, f'a path from this machine is still in: {left}'
print('src/run/ filled from', practice / 'app-run', 'and', l23dir.name, '· now delete src/run/PROVISIONAL and regenerate')
