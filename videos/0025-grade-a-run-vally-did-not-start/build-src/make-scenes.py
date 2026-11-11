"""Generate lesson 25's scene pages. File panels are inserted afterwards by panels.sh (panels.py).

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/app/run.sh, run.mjs, traces-to-atif.mjs   the app's real files (identical to the practice folder's)
  src/release.eval.yaml                         the eval file whose graders the lesson reuses
  src/run/                                      this video's own run of the app (s16, s17, s20, s22), written
                                                by build-src/extract-run.py. Until then: stand-ins, listed
                                                in src/run/PROVISIONAL.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
RUN = D / 'src/run'
PROV = (RUN / 'PROVISIONAL').exists()   # absent since the swap to our own run (src/run/HANDOVER.md)
MODEL = 'claude-haiku-4.5'
STIMULUS = 'since-last-release'
WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def code(src, lang, extra=''):
    """A dark code box from scripts/code.js. ⟦id:text⟧ marks a concept."""
    out = subprocess.run(['node', str(SKILL / 'scripts/code.js'), '--lang', lang, '--dark'],
                         input=src, capture_output=True, text=True, check=True).stdout.strip()
    return out.replace('class="code dark"', f'class="code dark{" " + extra if extra else ""}"', 1)


HEAD = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="stylesheet" href="../_theme/theme.css">
  <script src="../_theme/vl-runtime.js" defer></script>
  <style>{css}</style>
</head>
<body>
{body}
<script type="application/json" id="cues">
{cues}
</script>
</body>
</html>
'''


def scene(sid, title, body, cues, css=''):
    (D / 'scenes' / f'{sid}.html').write_text(
        HEAD.format(title=re.sub(r'<[^>]+>', '', title), body=body, css=css, cues=json.dumps(cues, indent=1)))


def framed(sid, eyebrow, headline, stage, cues, layout='', css='', h='h2', title_class='scene-title'):
    scene(sid, headline, f'''<main class="scene {layout}">
  <div class="eyebrow">{eyebrow}</div>
  <{h} class="{title_class}">{headline}</{h}>
  <div class="stage">
{stage}
  </div>
</main>''', cues, css)


def block(cid, role, title, label, words=False):
    return f'''<div class="semantic-block" data-concept="{cid}" data-rep="block" data-role="{role}">
      <div class="title{' words' if words else ''}">{title}</div><div class="label">{label}</div>
    </div>'''


def panel(pid):
    return f'<!-- file-panel:{pid} -->\n<!-- /file-panel:{pid} -->'


def callouts(*notes):
    return '<aside class="callouts">' + ''.join(
        f'<p class="callout" data-anchor="{anchor}">{text}</p>' for anchor, text in notes) + '</aside>'


def mono(t):
    return f'<span class="mono">{t}</span>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


STANDIN = ' · stand-in: the course’s own run' if PROV else ''

# ---- The eval file's five graders ------------------------------------------------------------------------
spec = (D / 'src/release.eval.yaml').read_text()
since = spec.split('  - name: tracker-down')[0].split('  - name: since-last-release')[1]
GRADERS = re.findall(r'- type: (\S+)\n\s+name: (\S+)', since)          # [(type, name)]
assert [n for _, n in GRADERS] == ['every-change-handled', 'reads-the-list', 'never-commits', 'no-loop',
                                   'loads-the-skill'], GRADERS
assert [t for t, _ in GRADERS] == ['run-command', 'tool-calls', 'tool-calls', 'max-repeat', 'skill-invocation']

# ---- This video's own run of the app ---------------------------------------------------------------------
counts = json.loads((RUN / 'counts.json').read_text())
traj = json.loads((RUN / 'trajectory.json').read_text())
l23 = json.loads((RUN / 'l23.json').read_text())
chat = json.loads((RUN / 'span-chat.json').read_text())
tool = json.loads((RUN / 'span-tool.json').read_text())
diff = (RUN / 'change.diff').read_text().splitlines()
app_log = (RUN / 's17.log').read_text().strip().splitlines()
npm_log = (RUN / 's16.log').read_text()
grade_log = (RUN / 's22.log').read_text()
for name in ('counts.json', 'trajectory.json', 'span-chat.json', 'span-tool.json', 'change.diff', 's17.log', 's22.log'):
    assert not re.search(r'/Users/|/var/folders|@[\w-]+\.\w|pseudo', (RUN / name).read_text()), \
        f'{name} still holds a path, an address or the account attribute from this machine'

verdict = dict((n, m == '✓') for m, n in re.findall(r'^\s*([✓✗]) \[([\w-]+)\]', grade_log, re.M))
assert set(verdict) == {n for _, n in GRADERS}, verdict
PASSED = [n for _, n in GRADERS if verdict[n]]
FAILED = [n for _, n in GRADERS if not verdict[n]]
steps = traj['steps']
step_calls = [[c['function_name'] for c in s['tool_calls']] for s in steps]
tool_spans = counts['tool_spans']
entries = [l for l in diff if l.startswith('+- ')]


def heading_of(entry):
    """The '### X' heading an added entry sits under, and whether the diff added that heading."""
    i = diff.index(entry)
    for l in reversed(diff[:i]):
        if l[1:].startswith('### '):
            return l[5:].strip(), l.startswith('+')
    raise AssertionError(entry)


# ---- What the narration says about the run. If a recording changes these, the sentences change too. ----
# s11: "the one that read the merged list" (the tool span shown is that call).
assert tool['attributes']['gen_ai.operation.name'] == 'execute_tool'
assert 'release/merged.txt' in tool['attributes']['gen_ai.tool.call.arguments'], 's11 sentence 0'
# s10: "its operation name is chat"; "the parent is the session's invoke agent span".
assert chat['attributes']['gen_ai.operation.name'] == 'chat' and counts['chat_parent_is_root'], 's10 sentence 2'
assert counts['root_span'].startswith('invoke_agent'), counts['root_span']
# s16: "about a hundred and forty packages".
added = int(re.search(r'added (\d+) packages', npm_log).group(1))
assert 130 <= added <= 150, f's16 sentence 1: npm added {added} packages'
# s17: "the reply says three changes were added, and both files are written".
assert app_log[-1] == 'Wrote app-run/traces.jsonl and app-run/change.diff', app_log[-1]
assert 'three' in ' '.join(app_log[:-1]).lower(), 's17 sentence 3: the reply does not say "three"'
# s18: only the changelog changed; #74 under Added, #75 under Fixed; #76 under a NEW Changed heading.
assert [l for l in diff if l.startswith('diff ')] == ['diff -ruN before/CHANGELOG.md repo/CHANGELOG.md'], 's18 sentence 1'
assert len(entries) == 3, f's18: {len(entries)} entries added'
by_pr = {re.search(r'\(#(\d+)\)', e).group(1): e for e in entries}
assert heading_of(by_pr['74'])[0] == 'Added' and heading_of(by_pr['75'])[0] == 'Fixed', 's18 sentence 2'
assert heading_of(by_pr['76']) == ('Changed', True), 's18 sentence 3: the refactor entry'
# s19: "a hundred and forty-three lines"; "there are five" tool calls; one reads the merged list; no skill call.
assert counts['trace_lines'] == 143, f"s19 sentence 0: {counts['trace_lines']} lines"
assert len(tool_spans) == 5, f's19 sentence 1: {len(tool_spans)} tool calls'
assert counts['timing_lines'] > counts['trace_lines'] / 2, 's19 sentence 1: "most are timing spans"'
assert 1 <= counts['merged_list_call'] <= len(tool_spans), 's19 sentence 2'
assert counts['skill_calls'] == 0 and not any('skill' in t for t in tool_spans), 's19 sentence 3'
# s21: "the five tool calls now sit in four steps ... and a last step holds only the reply".
assert len(steps) == 5 and sum(bool(c) for c in step_calls) == 4 and step_calls[-1] == [], f's21: {step_calls}'
assert [t.split()[-1] for t in tool_spans] == [f for c in step_calls for f in c], 'trace and trajectory disagree'
# s22: three of five passed (list read, nothing committed, nothing looped); hidden test and skill check failed.
assert PASSED == ['reads-the-list', 'never-commits', 'no-loop'], f's22 sentence 3: {PASSED}'
assert FAILED == ['every-change-handled', 'loads-the-skill'], f's22 sentence 4: {FAILED}'
assert '3/5 graders passed' in grade_log
# s23: Vally's own three trials: hidden test never passed, skill loaded once; "the same two graders" failed.
assert l23['model'] == MODEL and l23['stimulus'] == STIMULUS and l23['trials'] == 3, l23
g23 = l23['graders']
assert g23['every-change-handled'] == 1 and g23['loads-the-skill'] == 1, f's23 sentence 2: {g23}'
# s23 sentence 3: "most of Vally's trials failed" those two: each failed in 2 of 3.
assert [n for _, n in GRADERS if g23[n] < l23['trials']] == FAILED, 's23 sentence 3'
assert all(g23[n] == l23['trials'] for n in PASSED), g23
# s24: every grader gave a verdict; the hidden test "caught the refactor's entry" (it failed, and #76 is there).
assert 'Expected exit code 0, got 1' in grade_log and '76' in by_pr, 's24 sentence 2'

# ---- Hook ----------------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'A run Vally didn’t start', f'''<div class="cols wide two">
    <div class="semantic-block" data-concept="inside" data-rep="block" data-role="structure">
      <div class="title words">Inside Vally</div>
      <div class="label">prepares the workspace<br>starts the agent<br>records the trajectory<br>grades it</div>
    </div>
    <div class="semantic-block" data-concept="tool" data-rep="block" data-role="attention">
      <div class="title words">The release tool</div>
      <div class="label">a script prepares a checkout<br>the release app starts the agent</div>
      <div class="label left"><span data-concept="left" data-rep="note">what’s left: the changed checkout · the app’s own record</span></div>
    </div>
  </div>''', [
    {"type": "focus", "target": "inside", "at": "0", "color": "blue"},
    {"type": "focus", "target": "tool", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "left", "at": "3~what's left", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.two .semantic-block{min-height:330px}.two .title{font-size:44px}'
        '.two .label{font-size:34px;line-height:1.5}.two .label.left{margin-top:14px;width:auto}')

# ---- Chapter: Inside Vally or after the fact ---------------------------------------------------------------
EB1 = 'Inside Vally or after the fact'
TERMS = '.terms .semantic-block{min-height:300px}.terms .title{font-size:44px}.terms .label{font-size:34px;line-height:1.45}'
WAYS = f'''<div class="cols wide terms">
    {block("after", "attention", "After the fact", "the real app, its real inputs and model<br>each run happens once", words=True)}
    {block("inside", "structure", "Inside Vally", "repeat a stimulus, change the model<br>a reproduction of the app", words=True)}
  </div>'''
framed('s02', EB1, 'Two ways to grade an app', WAYS, [
    {"type": "focus", "target": "after", "at": "1", "color": "yellow"}], css=TERMS)
framed('s02b', EB1, 'Two ways to grade an app', WAYS, [
    {"type": "focus", "target": "inside", "at": "0", "color": "blue"},
    {"type": "focus", "target": "after", "at": "2~grading", "color": "yellow"}], css=TERMS)

# ---- Chapter: A trajectory from outside ---------------------------------------------------------------------
EB2 = 'A trajectory from outside'
parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('message', 'what the model said'), ('tool_calls', 'the calls it made'),
    ('observation', 'what each returned'), ('metrics', 'tokens')], 1))
framed('s03', EB2, 'A second format: ATIF', f'''<div class="semantic-block" id="atif" data-concept="atif" data-rep="block" data-role="structure">
    <div class="title">ATIF</div>
    <div class="label">Agent Trajectory Interchange Format · a JSON file: one agent session as a list of steps</div>
    <div class="label one">one step</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "focus", "target": "atif", "at": "3", "color": "blue"},
    {"type": "focus", "target": "p1", "at": "4~said", "color": "yellow"},
    {"type": "focus", "target": "p2", "at": "4~tool calls", "color": "yellow"},
    {"type": "focus", "target": "p3", "at": "4~returned", "color": "yellow"},
    {"type": "focus", "target": "p4", "at": "4~metrics", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='#atif{width:100%;padding:36px 40px 44px;gap:18px}#atif>.title{font-size:56px}#atif>.label{font-size:34px}'
        '#atif>.label.one{margin-top:14px;color:var(--ink-soft)}'
        '#atif .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#atif .part{min-height:190px}#atif .part .title{font-size:40px;line-height:1.2}#atif .part .label{font-size:32px}')

framed('s04', EB2, 'One step per model answer', f'''<div class="annotated">
    {panel('traj')}
    {callouts(('ver', 'how Vally recognises the file'), ('step', 'one step per model answer'),
              ('fn', 'what a tool-calls grader reads'), ('obs', 'what the call returned'),
              ('met', 'metrics: tokens and cost'))}
  </div>''', 'CUES:s04', layout='layout-file')

CMD = ('vally grade -e evals/release.eval.yaml \\\n  ⟦stim:--stimulus since-last-release⟧ \\\n'
       '  ⟦ws:--workspace app-run/repo⟧ \\\n  ⟦diff:--diff-file app-run/change.diff⟧ \\\n'
       '  --verbose ⟦in:< app-run/trajectory.json⟧')
NEEDS = f'''<div class="annotated">
    {code(CMD, 'bash', 'cmd')}
    {callouts(('stim', 'whose graders apply'), ('ws', 'the changed files: run-command, program, file graders'),
              ('diff', 'the change: diff graders'), ('in', 'the trajectory: tool-calls, skill-invocation, budgets'))}
  </div>'''
NEEDS_CSS = '.code.dark.cmd{font-size:36px;line-height:1.9;padding:30px 38px}.callout{font-size:32px}'
framed('s05', EB2, 'What each grader needs', NEEDS, [], css=NEEDS_CSS)
framed('s05b', EB2, 'What each grader needs', NEEDS, [
    {"type": "focus", "target": "in", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "diff", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "ws", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "stim", "at": "3", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}], css=NEEDS_CSS)

GAPS = [('cost', 'cost', 'empty', 'explained with the converter', 'add up each step’s dollars'),
        ('wall', 'wall time', '0', 'no start or end time in the file', 'a wall-time grader passes anything'),
        ('skill', 'skill loaded', 'only as a tool call', 'if the agent called its skill tool', 'the agent’s skill call, in the trace')]
GAP_CSS = ('.gaps .semantic-block{min-height:290px}.gaps .title{font-size:40px}.gaps .big{font:500 54px/1.2 var(--font-code);color:var(--ink)}'
           '.gaps .label{font-size:30px;line-height:1.4}')


def gap(cid, name, value, why):
    return f'''<div class="semantic-block" data-concept="{cid}" data-rep="block" data-role="attention">
      <div class="title words">{name}</div><div class="big">{value}</div><div class="label">{why}</div>
    </div>'''


framed('s06', EB2, 'Three things the file lacks', f'''<div class="cols gaps">
    {''.join(gap(c, n, v, why) for c, n, v, why, _ in GAPS)}
  </div>''', [
    {"type": "focus", "target": "cost", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "wall", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "skill", "at": "3", "color": "yellow"}], css=GAP_CSS)

# ---- Chapter: From OpenTelemetry traces ----------------------------------------------------------------------
EB3 = 'From OpenTelemetry traces'
KIDS = [('chat', 3, 17), ('execute_tool', 22, 18), ('chat', 42, 17), ('execute_tool', 61, 18), ('chat', 81, 17)]
kids = ''.join(f'<div class="bar kid" style="margin-left:{left}%;width:{w}%" data-concept="kid{i}" data-rep="block">{n}</div>'
               for i, (n, left, w) in enumerate(KIDS))
framed('s07', EB3, 'The app writes traces', f'''<p class="note top">one trace · every span carries its ID</p>
  <div class="trace">
    <div class="bar root" data-concept="root" data-rep="block">invoke_agent<span class="why">the root: no parent</span></div>
    {kids}
  </div>
  <p class="note">time runs left to right · each bar is one span</p>''', [
    {"type": "focus", "target": "kid0", "at": "3~a span", "color": "yellow"},
    {"type": "focus", "target": "kid1", "at": "3~tool call", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"},
    {"type": "focus", "target": "root", "at": "5", "color": "blue"}],
    css='.trace{display:flex;flex-direction:column;gap:12px;width:100%}'
        '.bar{position:relative;border-radius:10px;padding:14px 22px;font:500 32px/1.2 var(--font-code);color:var(--ink);'
        'white-space:nowrap;box-sizing:border-box}'
        '.bar.root{background:var(--tint-blue);width:100%}.bar.kid{background:var(--tint-cyan)}'
        '.bar .why{font:400 30px/1.2 var(--font-body);color:var(--ink-soft);margin-left:28px}.note.top{margin-bottom:-6px}')

NAMES = '⟦chat:chat⟧\n\n⟦tool:execute_tool⟧\n\n⟦agent:invoke_agent⟧\n\n⟦attr:gen_ai.usage.input_tokens⟧'
framed('s08', EB3, 'Shared names for AI work', f'''<div class="annotated">
    {code(NAMES, 'text', 'names')}
    {callouts(('chat', 'a model call'), ('tool', 'a tool call'), ('agent', 'a whole agent session'),
              ('attr', 'an attribute: input tokens'))}
  </div>
  <p class="note">OpenTelemetry, semantic conventions for generative AI · status: Development</p>''', [
    {"type": "focus", "target": "chat", "at": "1", "color": "blue"},
    {"type": "focus", "target": "tool", "at": "2~execute", "color": "blue"},
    {"type": "focus", "target": "agent", "at": "2~invoke", "color": "blue"},
    {"type": "focus", "target": "attr", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.code.dark.names{min-width:820px;font-size:42px;line-height:1.45}.callout{font-size:34px}.stage{gap:26px}')

framed('s09', EB3, 'Tracing is one setting', f'''<div class="annotated">
    {panel('runmjs')}
    {callouts(('imp', 'the app: one request, in the stimulus’s words'),
              ('tel', 'write spans to a file, one line of JSON each'),
              ('cap', 'include messages, tool arguments and results'))}
  </div>''', [
    {"type": "focus", "target": "imp", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#runmjs", "to": "9-17", "at": "3"},
    {"type": "focus", "target": "tel", "at": "3~telemetry", "color": "yellow"},
    {"type": "focus", "target": "cap", "at": "4", "color": "yellow"}], layout='layout-file')

framed('s10', EB3, 'A model call, as a span', f'''<div class="annotated">
    {panel('chat')}
    {callouts(('trace', 'shared by every span of the session'), ('parent', 'the session’s invoke_agent span'),
              ('op', 'the kind of work'), ('tok', 'tokens'), ('aiu', 'the price, in nano-AIU'))}
  </div>''', [
    {"type": "focus", "target": "op", "at": "1", "color": "blue"},
    {"type": "focus", "target": "trace", "at": "2~trace ID", "color": "yellow"},
    {"type": "focus", "target": "parent", "at": "2~parent", "color": "yellow"},
    {"type": "scroll", "target": "#chat", "to": "8-13", "at": "3"},
    {"type": "focus", "target": "tok", "at": "3~conventions", "color": "yellow"},
    {"type": "focus", "target": "aiu", "at": "4", "color": "yellow"}], layout='layout-file')

framed('s11', EB3, 'A tool call, as a span', f'''<div class="annotated">
    {panel('tool')}
    {callouts(('tool', 'a tool call, and which tool'), ('cid', 'the ID the model gave the call'),
              ('cc', 'recorded because of captureContent'))}
  </div>''', [
    {"type": "focus", "target": "tool", "at": "1", "color": "blue"},
    {"type": "focus", "target": "cid", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "cc", "at": "3", "color": "yellow"}], layout='layout-file')

framed('s12', EB3, 'Spans in, steps out', f'''<div class="annotated">
    {panel('conv')}
    {callouts(('chat', 'a model call: a new step'), ('met', 'tokens, renamed'),
              ('tool', 'a tool call joins the step before it'), ('args', 'plain text stays text'))}
  </div>''', [
    {"type": "focus", "target": "chat", "at": "4", "color": "blue"},
    {"type": "scroll", "target": "#conv", "to": "44-48", "at": "4~becomes"},
    {"type": "focus", "target": "met", "at": "4~renamed", "color": "yellow"},
    {"type": "scroll", "target": "#conv", "to": "53-60", "at": "5"},
    {"type": "focus", "target": "tool", "at": "5~just before", "color": "blue"},
    {"type": "focus", "target": "none", "at": "6"},
    {"type": "scroll", "target": "#conv", "to": "57-61", "at": "6"},
    {"type": "focus", "target": "args", "at": "7", "color": "yellow"}], layout='layout-file')

conv_src = (D / 'src/app/traces-to-atif.mjs').read_text().splitlines()
# s12b quotes lines 49 and 50 of the converter, and says: nano-AIU in the trace, dollars kept in each step.
assert conv_src[48].strip() == '// A billion nano-AIU is one AI Credit: $0.01.', conv_src[48]
assert conv_src[49].strip() == 'cost_usd: (a["github.copilot.nano_aiu"] ?? 0) / 1e11,', conv_src[49]
assert 'github.copilot.nano_aiu' in chat['attributes'] and all('cost_usd' in st['metrics'] for st in steps), 's12b'
COST = conv_src[48].strip() + '\n' + conv_src[49].strip().replace('cost_usd', '⟦usd:cost_usd⟧').replace(
    'a["github.copilot.nano_aiu"]', '⟦aiu:a["github.copilot.nano_aiu"]⟧')
framed('s12b', EB3, 'What happens to cost', f'''<div class="annotated">
    <div class="card"><div class="who">{mono('app/traces-to-atif.mjs')} · lines 49 and 50</div>
    {code(COST, 'javascript', 'cost')}</div>
    {callouts(('usd', 'the trace’s nano-AIU, kept as dollars'))}
  </div>
  <div class="semantic-block wide1" data-concept="empty" data-rep="block" data-role="attention">
    <div class="title words">Vally’s cost</div><div class="big">empty</div>
    <div class="label">it only counts AIU its own Copilot runs report</div>
  </div>''', [
    {"type": "focus", "target": "aiu", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "usd", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "empty", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.card{width:fit-content}.card>.code.dark.cost{font-size:34px;line-height:1.7;padding:26px 34px}.callout{font-size:32px}'
        '.annotated{align-items:end}.stage{gap:34px}.wide1{width:100%;min-height:0;padding:28px 36px}'
        '.wide1 .title{font-size:40px}.wide1 .big{font:500 54px/1.2 var(--font-code);color:var(--ink)}.wide1 .label{font-size:32px}')

PRIVATE = [('pv1', 'the whole prompt'), ('pv2', 'every file the agent opened'), ('pv3', 'full paths on your machine'),
           ('pv4', 'an ID for your account')]
framed('s13', EB3, 'Traces hold private values', f'''<p class="lead">a trace written with content captured holds</p>
  <div class="cols priv">
    {''.join(block(c, 'attention', t, '', words=True) for c, t in PRIVATE)}
  </div>
  <p class="note">the traces in this video were cleaned first</p>''', [
    {"type": "focus", "target": "pv1", "at": "1~whole prompt", "color": "yellow"},
    {"type": "focus", "target": "pv2", "at": "1~every file", "color": "yellow"},
    {"type": "focus", "target": "pv3", "at": "1~full paths", "color": "yellow"},
    {"type": "focus", "target": "pv4", "at": "1~identifies", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.priv .semantic-block{min-height:300px;justify-content:center}.priv .title{font-size:44px;line-height:1.25}'
        '.priv .label{display:none}.lead{font-size:38px}.stage{gap:28px}')

# ---- Chapter: The script the release tooling runs -----------------------------------------------------------
EB4 = 'The script the release tooling runs'
framed('s14', EB4, 'The script does Vally’s setup', f'''<div class="annotated">
    {panel('runsh')}
    {callouts(('co', 'the checkout: the files the eval file stages'), ('setup', 'the same setup command'),
              ('keep', 'the starting state, kept'), ('app', 'the app, on the model we give it'),
              ('diff', 'the change, as a plain diff'))}
  </div>''', [
    {"type": "focus", "target": "co", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#runsh", "to": "20-25", "at": "3"},
    {"type": "focus", "target": "setup", "at": "3~writes", "color": "yellow"},
    {"type": "focus", "target": "keep", "at": "4", "color": "yellow"},
    {"type": "scroll", "target": "#runsh", "to": "26-29", "at": "5"},
    {"type": "focus", "target": "app", "at": "5~on the model", "color": "blue"},
    {"type": "scroll", "target": "#runsh", "to": "30-33", "at": "6"},
    {"type": "focus", "target": "diff", "at": "6~saves", "color": "yellow"}], layout='layout-file')

# ---- Chapter: Run the app, convert, grade ---------------------------------------------------------------------
EB5 = 'Run the app, convert, grade'
TABLE_CSS = ('.data-table{font-size:40px}.data-table th{font-size:30px}.data-table td{padding-top:20px;padding-bottom:20px}'
             '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:34px}')
KIND = {'run-command': 'run-command · the hidden test', 'tool-calls': 'tool-calls', 'max-repeat': 'max-repeat',
        'skill-invocation': 'skill-invocation'}
grader_rows = ''.join(
    f'<tr><td class="mono"><span data-concept="all" data-rep="cell">{n}</span></td><td class="mono">{KIND[t]}</td></tr>\n'
    for t, n in GRADERS)
framed('s15', EB5, 'Which graders will still work?', f'''<table class="data-table full five">
    <thead><tr><th>Grader</th><th>Type</th></tr></thead>
    <tbody>
{grader_rows}    </tbody>
  </table>
  <p class="note">evals/release.eval.yaml · {mono(STIMULUS)}</p>''', [
    {"type": "focus", "target": "all", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}], css=TABLE_CSS)

DIFF_NOTES = [('file', 'only the changelog changed'), ('e74', 'the new option'), ('e75', 'the search fix'), ('e76', 'the refactor: the skill says leave it out')]
framed('s18', EB5, 'What the app changed', f'''<div class="annotated">
    {panel('diff')}
    {callouts(*DIFF_NOTES)}
  </div>''', 'CUES:s18', layout='layout-file')

n_tools = len(tool_spans)
span_lines = '\n'.join(('⟦merged:' if i == counts['merged_list_call'] else f'⟦t{i}:') + f'"name":"{t}"⟧'
                       for i, t in enumerate(tool_spans, 1))
LAST = 'merged' if counts['merged_list_call'] == n_tools else f't{n_tools}'
SPAN_NOTES = ([('merged', 'the read of release/merged.txt'), (LAST, 'no execute_tool skill')] if LAST != 'merged'
              else [('merged', 'the read of release/merged.txt · no execute_tool skill')])
framed('s19', EB5, f'{WORDS[n_tools].capitalize()} tool calls, no skill call', f'''<p class="lead"><span data-concept="count" data-rep="note">{counts['trace_lines']} lines · {counts['timing_lines']} of them session timings</span></p>
  <div class="annotated">
    <div class="card"><div class="who">{mono('app-run/traces.jsonl')} · the lines whose name begins {mono('execute_tool')}</div>
    {code(span_lines, 'text', 'spans')}</div>
    {callouts(*SPAN_NOTES)}
  </div>
  <p class="note">our run{STANDIN}</p>''', [
    {"type": "focus", "target": "count", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "t1" if counts['merged_list_call'] != 1 else "t2", "at": "1~searching", "color": "blue"},
    {"type": "focus", "target": "merged", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.card{width:fit-content}.card>.code.dark.spans{font-size:36px;line-height:1.6;padding:26px 36px;min-width:760px}'
        '.callout{font-size:32px}.lead{font-size:38px}.stage{gap:22px}.annotated{align-items:end}')

step_rows = ''.join(
    f'<tr><td class="num">{s["step_id"]}</td><td class="mono"><span data-concept="{"calls" if c else "reply"}" data-rep="cell">'
    f'{", ".join(c) if c else "none"}</span></td><td>{"" if c else "the reply only"}</td></tr>\n'
    for s, c in zip(steps, step_calls))
n_steps, n_with = len(steps), sum(bool(c) for c in step_calls)
framed('s21', EB5, f'{WORDS[n_steps].capitalize()} steps, {WORDS[n_with]} with tool calls', f'''<table class="data-table steps">
    <thead><tr><th class="num">Step</th><th>Tool calls</th><th></th></tr></thead>
    <tbody>
{step_rows}    </tbody>
  </table>
  <p class="note">{mono('app-run/trajectory.json')} · our run{STANDIN}</p>''', [
    {"type": "focus", "target": "calls", "at": "1~four steps", "color": "blue"},
    {"type": "focus", "target": "reply", "at": "1~last step", "color": "yellow"}],
    css=TABLE_CSS + '.steps{min-width:1100px}.steps td{padding-top:24px;padding-bottom:24px}.steps{font-size:42px}')


def app_cell(n):
    return 'passed' if verdict[n] else 'failed'


cmp_rows = ''.join(
    f'<tr><td class="mono">{n}</td>'
    f'<td class="num"><span data-concept="{"appfail" if n in FAILED else "appok"}" data-rep="cell">{app_cell(n)}</span></td>'
    f'<td class="num"><span data-concept="{"theirs" if n in FAILED else "theirsok"}" data-rep="cell">{g23[n]} of {l23["trials"]}</span></td></tr>\n'
    for n in FAILED + PASSED)
framed('s23', EB5, 'The same two failures', f'''<table class="data-table full cmp">
    <thead><tr><th>{mono(MODEL)} · {mono(STIMULUS)}</th><th class="num">The app’s run · 1</th>
      <th class="num">Vally’s own trials · {l23["trials"]}</th></tr></thead>
    <tbody>
{cmp_rows}    </tbody>
  </table>
  <p class="note">trials that passed each grader{STANDIN}</p>''', [
    {"type": "focus", "target": "theirs", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "appfail", "at": "3", "color": "red"},
    {"type": "focus", "target": "none", "at": "4"}],
    css=TABLE_CSS + '.cmp td{padding-top:18px;padding-bottom:18px}.cmp th.num{max-width:420px}')

# ---- Chapter: What carried over --------------------------------------------------------------------------------
EB6 = 'What carried over'
READS = [('g1', 'every-change-handled', 'a copy of the app’s checkout'),
         ('g2', 'reads-the-list · never-commits', 'the tool calls in the trajectory'),
         ('g3', 'no-loop', 'the same record'),
         ('g4', 'loads-the-skill', 'no skill call in the trajectory')]
read_rows = ''.join(f'<tr><td class="mono"><span data-concept="{c}" data-rep="cell">{n}</span></td><td>{w}</td></tr>\n'
                    for c, n, w in READS)
framed('s24', EB6, 'Every grader worked', f'''<table class="data-table full reads">
    <thead><tr><th>Grader</th><th>What it read, on the app’s run</th></tr></thead>
    <tbody>
{read_rows}    </tbody>
  </table>''', [
    {"type": "focus", "target": "g1", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "g2", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "g3", "at": "4~loop check", "color": "yellow"},
    {"type": "focus", "target": "g4", "at": "4~skill check", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], css=TABLE_CSS + '.reads td{padding-top:26px;padding-bottom:26px}')

framed('s25', EB6, 'What didn’t carry over', f'''<div class="grid4 gaps">
    {''.join(gap(c, n, v, then) for c, n, v, _, then in GAPS)}
    {gap('down', 'tracker-down', 'nothing to grade', 'the tool fails only inside Vally')}
  </div>''', [
    {"type": "focus", "target": "cost", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "wall", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "skill", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"},
    {"type": "focus", "target": "down", "at": "5", "color": "yellow"}],
    css=GAP_CSS + '.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;width:100%}'
                  '.grid4 .semantic-block{min-height:330px}.grid4 .big{font-size:40px}.grid4 .title{font-size:36px}')

framed('s26', EB6, 'One run is one sample', f'''<div class="cols wide terms nums">
    {block("one", "attention", "1 run", "the app, graded afterwards<br>once, on the model the app used")}
    {block("three", "structure", f"{l23['trials']} trials", "Vally’s own<br>repeatable")}
  </div>''', [
    {"type": "focus", "target": "three", "at": "1~trials", "color": "blue"},
    {"type": "focus", "target": "one", "at": "1~happens once", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css=TERMS + '.nums .title{font-size:96px;line-height:1.1}')

rparts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('the trajectory', 'an ATIF file on standard input'),
    ('the change', mono('--diff-file')),
    ('the changed files', mono('--workspace'))], 1))
framed('s27', 'Recap', 'What does vally grade need?', f'''<div class="semantic-block" id="needs" data-role="structure">
    <div class="title words">a run Vally didn’t start</div>
    <div class="parts">{rparts}</div>
  </div>''', [
    {"type": "expand", "target": "#needs", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p3", "at": "3", "color": "blue"}], layout='layout-expand',
    css='#needs{width:100%;padding:36px 40px 44px;gap:24px}'
        '#needs .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#needs .part{min-height:280px}#needs .part .title{font-size:50px;line-height:1.2}'
        '#needs .part .label{font-size:34px}')

scene('s28', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Let Vally run the app</h1>
  <p class="lead">To get trials, experiments and models, Vally has to start the app itself.</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “CLI: grade” and “Trajectory Format”</p>
</main>''', [], css='.scene-title.chapter{font-size:116px}')

# ---- Scenes whose cues depend on line numbers found in the run's files -------------------------------------
tl = (RUN / 'trajectory.json').read_text().splitlines()


def line_of(lines, needle, start=1):
    for i in range(start, len(lines) + 1):
        if needle in lines[i - 1]:
            return i
    raise AssertionError(needle)


T = {'ver': line_of(tl, '"schema_version"'), 'step': line_of(tl, '"step_id": 1')}
T['fn'] = line_of(tl, '"function_name"', T['step'])
T['obs'] = line_of(tl, '"observation"', T['step'])
T['met'] = line_of(tl, '"metrics"', T['step'])
T['end'] = line_of(tl, '"cost_usd"', T['met']) + 1
ARGS_END = next(i for i in range(line_of(tl, '"arguments"', T['fn']) , len(tl) + 1) if tl[i - 1].strip() in ('}', '},') or tl[i - 1].rstrip().endswith(('},', '}')))
T['args_end'] = ARGS_END


def set_cues(sid, cues):
    p = D / 'scenes' / f'{sid}.html'
    p.write_text(p.read_text().replace(json.dumps(f'CUES:{sid}', indent=1), json.dumps(cues, indent=1)))


def window(first, rows=8):
    return f'{first}-{first + rows}'


set_cues('s04', [
    {"type": "focus", "target": "ver", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#traj", "to": f"{T['step'] - 1}-{T['step'] + 3}", "at": "2"},
    {"type": "focus", "target": "step", "at": "2~one for each", "color": "yellow"},
    {"type": "scroll", "target": "#traj", "to": f"{T['fn'] - 1}-{T['args_end']}", "at": "3"},
    {"type": "focus", "target": "fn", "at": "3~name", "color": "yellow"},
    {"type": "scroll", "target": "#traj", "to": f"{T['obs']}-{T['obs'] + 3}", "at": "4"},
    {"type": "focus", "target": "obs", "at": "4~returned", "color": "yellow"},
    {"type": "scroll", "target": "#traj", "to": f"{T['met']}-{T['end']}", "at": "5"},
    {"type": "focus", "target": "met", "at": "5~tokens", "color": "yellow"}])

D74, D75, D76 = (diff.index(by_pr[k]) + 1 for k in ('74', '75', '76'))
set_cues('s18', [
    {"type": "focus", "target": "file", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#diff", "to": f"{max(1, D74 - 2)}-{D75}", "at": "2"},
    {"type": "focus", "target": "e74", "at": "2~new option", "color": "yellow"},
    {"type": "focus", "target": "e75", "at": "2~search fix", "color": "yellow"},
    {"type": "scroll", "target": "#diff", "to": f"{D76 - 3}-{D76}", "at": "3"},
    {"type": "focus", "target": "e76", "at": "3~refactor", "color": "red"}])
(D / 'build-src/lines.json').write_text(json.dumps({'traj': T, 'diff': {'e74': D74, 'e75': D75, 'e76': D76}}, indent=1) + '\n')
print('ok' + (' (stand-in run: src/run/PROVISIONAL)' if PROV else ''))
