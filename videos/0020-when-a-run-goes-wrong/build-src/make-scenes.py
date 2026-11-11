"""Generate lesson 20's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/broken/*.eval.yaml   the four broken eval files, from practice-starter (what the tapes run first)
  src/state/fixed/*.eval.yaml    the same files fixed, from verified/lesson-20/practice (what the tapes install)
  src/run/                       what this video's own recordings printed and saved. Until they exist it holds
                                 stand-ins (src/run/PROVISIONAL); build-src/collect-run.py replaces them.

The block headed "What the narration says" asserts each statement the outcome sentences make. When a
recording disagrees, the assert names the scene: reword those sentences, then change the assert.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import html, json, pathlib, re, subprocess, textwrap

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
RUN = D / 'src/run'
H, T = MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
PROV = (RUN / 'PROVISIONAL').exists()
FROM = 'stand-in: the course’s verified run, not yet ours' if PROV else 'from our run'
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\r')
esc = html.escape


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


def block(cid, role, title, label, words=False, step=None):
    s = f'<div class="step">{step}</div>' if step else ''
    return f'''<div class="semantic-block" data-concept="{cid}" data-rep="block" data-role="{role}">
      {s}<div class="title{' words' if words else ''}">{title}</div><div class="label">{label}</div>
    </div>'''


def panel(pid):
    return f'<!-- file-panel:{pid} -->\n<!-- /file-panel:{pid} -->'


def callouts(*notes):
    return '<aside class="callouts">' + ''.join(
        f'<p class="callout" data-anchor="{anchor}">{text}</p>' for anchor, text in notes) + '</aside>'


def card(cid, who, body):
    return f'''<div class="card" data-concept="{cid}" data-rep="card">
        <div class="who">{who}</div>
        {body}
      </div>'''


def mono(t):
    return f'<span class="mono">{t}</span>'


def cell(cid, inner):
    return f'<span data-concept="{cid}" data-rep="cell">{inner}</span>'


def focus(target, at, color=None):
    c = {"type": "focus", "target": target, "at": at}
    if color:
        c["color"] = color
    return c


# ---- This video's runs --------------------------------------------------------------------------------
def log(sid):
    return ANSI.sub('', (RUN / f'{sid}.log').read_text())


def blocks(text):
    """-> {model: [lines of that model's block]} from the part of a run's output above the final Failures list.
    A block starts at a line that is exactly a model name and ends at the next one, or where the live
    progress display resumes (a progress bar, a spinner line, a rule or "Live summary")."""
    out, cur = {}, None
    for line in text[:text.rfind('Failures')].splitlines():
        s = line.strip()
        if s in MODELS:
            cur = out.setdefault(s, [])
            cur.clear()
        elif s[:1] in ('█', '░', '─') or s.startswith('Live summary') or ('\u2800' <= s[:1] <= '\u28ff'):
            cur = None
        elif cur is not None:
            cur.append(line.rstrip())
    return out


def paragraphs(lines):
    out, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


facts = json.loads((RUN / 'facts.json').read_text())
AIU = facts['aiu']
EARLIER = facts['earlier_typo_fix_s']      # this request's two trials in the lesson 18 video's run
tail = (RUN / 'events-tail.txt').read_text().rstrip('\n').splitlines()
tail_text = '\n'.join(tail)
record = json.loads((RUN / 'judge-record.json').read_text())
patch = (RUN / 'entry-haiku.patch').read_text().splitlines()
L14, L18, L19, L24, L25, L30, L31, L34 = (log(s) for s in 's14 s18 s19 s24 s25 s30 s31 s34'.split())
entry, judged = blocks(L25), blocks(L31)
spend = [int(m.group(1)) for t in sorted((D / 'tapes').glob('*.tape'))
         for m in re.finditer(r'^# Spend: (\d+) agent runs?', t.read_text(), re.M)]
RUNS_SPENT, JUDGE_CALLS = sum(spend), 2

# ---- What the narration says about the runs. If a recording changes these, the sentences change too. ----
# s14: both trials end in ERROR for the same reason (a command had to be a string), and the last line warns
#      about a reporter error.
CMD_ERR = 'The "command" argument must be of type string. Received an instance of Object'
assert L14.count('ERROR') >= 2 and L14.count(CMD_ERR) >= 2, 's14: the command error is not there twice'
assert 'reporter callback error' in L14, 's16 sentence 2: no reporter warning in the s14 run'
# s15: haiku's trial folder holds metadata.json and nothing else.
assert facts['trial_files']['merged-list'] == ['metadata.json'], f"s15: {facts['trial_files']['merged-list']}"
# s18: the stimulus passes.
assert re.search(r'PASS\s+merged-list', L18), 's18: merged-list did not pass with the fix'
# s19: both trials timed out after 5000 ms; --verbose added no agent reply.
assert L19.count('timed out after 5000 ms') >= 2, 's19 sentence 3: not two timeouts'
assert 'agent output' not in L19, 's19 sentence 4: verbose did print a reply'
# s20: a session log and no patch.
assert facts['trial_files']['quick'] == ['events.jsonl', 'metadata.json'], f"s20: {facts['trial_files']['quick']}"
# s09 and s21: the excerpt shows the skill loading, an abort from outside, and a usage checkpoint;
#      "about one and a quarter AIU" for the model shown, "about one" for the other.
assert 'skill.invoked' in tail_text and '"reason":"user_initiated"' in tail_text and 'totalNanoAiu' in tail_text, \
    's09/s21: the events excerpt lacks skill.invoked, the abort or the usage checkpoint'
SHOWN = facts['events_tail_model']
OTHER = H if SHOWN == T else T
assert SHOWN == T, 's21 sentence 0 says "Terra\'s session log": the excerpt is from the other model'
assert abs(int(re.search(r'"totalNanoAiu":(\d+)', tail_text).group(1)) / 1e9 - AIU[SHOWN]) < 0.006, 'excerpt and facts.json disagree'
assert 2.85 <= AIU[SHOWN] <= 3.15, f's09 sentence 5, s21 sentence 1: "about three AIU" but it is {AIU[SHOWN]}'
assert 0.70 <= AIU[OTHER] <= 0.80, f's21 sentence 1: "about three quarters of one" but the other model\'s is {AIU[OTHER]}'
# s22: "its two trials took about eight and nine seconds"; "five seconds just isn't enough for this request".
assert sorted(round(x) for x in EARLIER.values()) == [8, 9], f's22 sentence 2: {EARLIER}'
assert min(EARLIER.values()) > 5, 's22 sentence 3: a trial finished within five seconds'
# s24: both trials finish and pass.
assert len(re.findall(r'✓ 1/1', L24)) >= 2, 's24: not 1/1 on both models'
# s25: both models failed adds-an-entry, pattern not found in the workspace diff.
EVID = re.search(r'✘ adds-an-entry\s+(Pattern /\^\\\+\.\*notes add/ not found in workspace diff)', L25)
assert EVID and all(any(l.strip().startswith('FAIL') for l in entry[m]) for m in MODELS), 's25: not a FAIL on both'


def verbose(m):
    """-> (stats line, the agent's reply) from what --verbose printed under a failing trial."""
    ps = paragraphs(entry[m])
    stats = next(p for p in ps if 'turns' in p[0] and 'tok' in p[0])
    i = next(i for i, p in enumerate(ps) if p[0] == 'agent output')
    reply = ' '.join(ps[i][1:] if len(ps[i]) > 1 else ps[i + 1])
    return stats[0], reply


STATS, REPLY = zip(*(verbose(m) for m in MODELS))
# s26: haiku says it added the typo fix to the changelog under Fixed; terra says much the same.
assert all('Fixed' in r and 'changelog' in r.lower() for r in REPLY), f's26 sentences 1-2: {REPLY}'
assert 'typo' in REPLY[0].lower(), f's26 sentence 1: {REPLY[0]}'
# s27: an added Fixed heading, and under it an added entry that mentions notes add.
added = [l for l in patch if l.startswith('+') and not l.startswith('+++')]
assert '+### Fixed' in added and any('notes add' in l for l in added if l.startswith('+- ')), f's27: {added}'
# s30: both blocks say 1/1 graders passed.
assert L30.count('(1/1 graders passed)') == 2, 's30: not two passing blocks'
# s31 and s32: both stimuli ERROR with 1/2 graders and an invalid verdict; the judge model's name has a
#      hyphen where the account's list has a dot.
JB = ' '.join(l.strip() for l in judged[H])
assert all(any(re.match(r'\s*ERROR\s+cache · 1/2 graders', l) for l in judged[m]) for m in MODELS), 's31/s32: not ERROR 1/2 on both'
assert 'Grading error; verdict is invalid.' in JB and 'Model "claude-sonnet-5-5" is not available' in JB, 's32'
assert 'claude-sonnet-5.5' in JB, 's32 sentence 3: the dotted name is not on the list printed'
# s11: the record has status error, score 0 and the reason in its evidence.
assert record['status'] == 'error' and record['score'] == 0 and record['evidence'].startswith('LLM judge failed'), 's11'
# s34: the judge reaches a verdict on both trials: one passes 2/2, the other fails on users-words, and its
#      reason names caching. Every reason begins by quoting the entry.
assert L34.count('(2/2 graders passed)') == 1 and L34.count('(1/2 graders passed, 1 failed)') == 1, 's34: not one pass and one fail'
reasons = re.findall(r'\[users-words\] (.*)', L34)
assert len(reasons) == 2 and all('"' in r[:60] for r in reasons), f's34: a reason does not begin by quoting: {reasons}'
assert 'LLM judge failed' not in L34, 's34: the judge call still fails'
failed = next(r for l, r in re.findall(r'(✗|✓) \[users-words\] (.*)', L34) if l == '✗')
assert 'caching' in failed, f's34 sentence 2: the failing reason does not mention caching: {failed}'
# s35: "nine agent runs and two judge calls".
assert RUNS_SPENT == 9, f's35 sentence 3: the tapes declare {RUNS_SPENT} agent runs'

# ---- Hook ------------------------------------------------------------------------------------------------
TERMS = '.terms .semantic-block{min-height:260px}.terms .label{font-size:34px}'
framed('s01', 'Vally &amp; Agent Evals', 'When a run goes wrong', f'''<div class="cols wide terms">
    {block('e', 'attention', 'ERROR', 'no result that could be graded')}
    {block('fl', 'attention', 'FLAKY', 'some trials passed, some failed')}
    {block('fa', 'attention', 'a surprising FAIL', 'a verdict nobody expected')}
  </div>
  <p class="lead">Nearly every answer is already on disk.</p>''', [
    focus('e', '1~ERROR', 'yellow'), focus('fl', '1~flaky', 'yellow'), focus('fa', '1~fails', 'yellow'),
    focus('none', '2')],
    h='h1', title_class='scene-title chapter', css='.scene-title.chapter{font-size:116px}' + TERMS)

# ---- Chapter: Four questions, cheapest first ---------------------------------------------------------------
EB1 = 'Four questions, cheapest first'
QS = [('q1', 'structure', 'Is the eval valid?', 'does Vally accept the file?', 'vally lint, the run’s first lines · free'),
      ('q2', 'transform', 'Did it complete?', 'did every trial finish and get graded?', 'ERROR lines, the trial folder · free'),
      ('q3', 'attention', 'Why was the result unexpected?', 'the agent, or the grader?', 'evidence, --verbose, the patch · free'),
      ('q4', 'change', 'Does the fix work?', 'prove it', 'vally grade, else one new run · cheapest')]
QCSS = ('.qs .semantic-block{min-height:330px}.qs .title{font-size:44px;line-height:1.2}.qs .label{font-size:30px}'
        '.cols.qs{gap:28px}')
framed('s02', EB1, 'Four questions, in order', f'''<div class="cols qs">
    {''.join(block(c, r, t, l, words=True, step=i) for i, (c, r, t, l, _) in enumerate(QS, 1))}
  </div>
  <p class="note">Source: Vally docs, Debugging Evals</p>''', [
    focus('q1', '2', 'blue'), focus('q2', '3', 'cyan'), focus('q3', '4', 'yellow'), focus('q4', '5', 'orange'),
    focus('none', '6')], css=QCSS)

framed('s03', EB1, 'Cheapest first', f'''<div class="cols qs">
    {''.join(block('read' if i < 4 else 'run', r, t, w, words=True, step=i) for i, (c, r, t, _, w) in enumerate(QS, 1))}
  </div>''', [
    focus('read', '0~first three', 'green'), focus('run', '1', 'yellow')], css=QCSS)

framed('s04', EB1, 'What did the fix change?', f'''<div class="cols wide terms">
    {block('g', 'success', 'A grader', 'nothing the agent did changes · grade the saved trials again', words=True)}
    {block('r', 'attention', 'The setup, a time limit, the skill', 'the run itself changes · a new run, often on one model', words=True)}
  </div>''', [
    focus('g', '0', 'green'), focus('r', '1', 'yellow')],
    css='.terms .semantic-block{min-height:300px}.terms .label{font-size:34px}.terms .title{font-size:48px;line-height:1.2}')

# ---- Chapter: Where each answer lives ----------------------------------------------------------------------
EB2 = 'Where each answer lives'
framed('s05', EB2, 'Lint checks the shape', f'''<div class="cols wide terms">
    {block('can', 'structure', 'Lint can see', 'unknown field names · files that don’t exist · values of the wrong kind', words=True)}
    {block('cannot', 'attention', 'Lint can’t see', 'what a value means to the program that uses it', words=True)}
  </div>''', [
    focus('can', '1', 'blue'), focus('cannot', '3', 'yellow')],
    css='.terms .semantic-block{min-height:300px}.terms .label{font-size:34px}.terms .title{font-size:48px}')

CODE_CSS = '.annotated .code.dark{font-size:40px;line-height:1.5;padding:30px 38px}.callout{font-size:34px}'
framed('s06', EB2, 'Commands run before the agent', f'''<div class="annotated">
    {code('agent_environment:\n  ⟦c:commands:⟧\n    - ⟦e:echo hello > note.txt⟧', 'yaml', 'cmds')}
    {callouts(('c', 'after the files are copied, before the agent starts'), ('e', 'one command per entry, as a string'))}
  </div>
  <p class="note">{cell('state', 'what the commands create is starting state: it is not in the trial’s diff')}</p>''', [
    focus('c', '1', 'blue'), focus('e', '2', 'yellow'), focus('state', '3', 'blue')],
    css=CODE_CSS + '.code.dark.cmds{min-width:820px}.stage{gap:30px}')

framed('s07', EB2, 'A colon makes a mapping', f'''<div class="annotated">
    {code("- ⟦k:echo note:⟧ hello\n\n- ⟦s:'echo note: hello'⟧", 'text', 'trap')}
    {callouts(('k', 'a mapping: key “echo note”, value “hello”'), ('s', 'a string'))}
  </div>
  <p class="note">two entries of a {mono('commands:')} list</p>''', [
    focus('k', '1~colon', 'yellow'), focus('s', '5', 'green')],
    css=CODE_CSS + '.code.dark.trap{min-width:820px}.stage{gap:30px}')

TABLE_CSS = ('.data-table{font-size:38px}.data-table th{font-size:30px}.data-table td{padding-top:26px;padding-bottom:26px}'
             '.data-table td.mono{font-family:var(--font-code);font-size:32px;white-space:nowrap}')
folder_rows = [('r1', 'metadata.json only', 'no agent session started: the failure came during setup'),
               ('r2', 'events.jsonl, no workspace.patch', 'the agent started, and was stopped before it finished'),
               ('r3', 'events.jsonl and workspace.patch', 'the agent finished: look at the grading, or the work')]
framed('s08', EB2, 'How far did the trial get?', f'''<table class="data-table full">
    <thead><tr><th>The trial folder holds</th><th>What it means</th></tr></thead>
    <tbody>
{''.join(f'<tr><td class="mono">{cell(c, a)}</td><td>{cell(c, b)}</td></tr>' for c, a, b in folder_rows)}
    </tbody>
  </table>''', [
    focus('r1', '3', 'yellow'), focus('r2', '4', 'yellow'), focus('r3', '5', 'blue')], css=TABLE_CSS)


def events_box(extra):
    src = tail_text.replace('{"type":"skill.invoked"', '{"type":"⟦sk:skill.invoked⟧"', 1)
    src = src.replace('"reason":"user_initiated"', '⟦ab:"reason":"user_initiated"⟧', 1)
    src = re.sub(r'"totalNanoAiu":(\d+)', lambda m: f'⟦cost:"totalNanoAiu":{m.group(1)}⟧', src, count=1)
    return code(src, 'text', extra)


EV_CSS = ('.card{width:100%}.card .who{font-size:30px}.annotated .code.dark{font-size:32px;line-height:1.55;padding:26px 32px}'
          '.callout{font-size:32px}.stage{gap:24px}')
framed('s09', EB2, 'The end of a stopped session', f'''<div class="card">
    <div class="who">{mono('events.jsonl')} · its last lines, shortened to the fields that matter</div>
    <div class="annotated">
      {events_box('ev')}
      {callouts(('sk', 'the skill had loaded'), ('ab', 'stopped from outside the agent'),
                ('cost', f'{AIU[SHOWN]:.2f} AIU before it was stopped'))}
    </div>
  </div>
  <p class="note">a trial that ran out of time · {FROM}</p>''', [
    focus('sk', '3', 'blue'), focus('ab', '4', 'yellow'), focus('cost', '5', 'yellow'), focus('none', '6')],
    css=EV_CSS)


def wrap(text, width, indent):
    return ('\n' + indent).join(textwrap.wrap(text, width))


fail_line = next(l.strip() for l in entry[H] if l.strip().startswith('FAIL'))
vb = (f'{fail_line}\n ⟦ev:✘ adds-an-entry⟧  Pattern /^\\+.*notes add/\n     not found in workspace diff\n\n'
      f' ⟦st:{STATS[0]}⟧\n\n agent output\n ⟦re:{wrap(REPLY[0], 46, " ").splitlines()[0]}⟧'
      + ''.join('\n' + l for l in wrap(REPLY[0], 46, ' ').splitlines()[1:]))
framed('s10', EB2, 'Evidence, then the patch', f'''<div class="annotated">
    {code(vb, 'text', 'vb')}
    {callouts(('ev', 'the grader’s evidence'), ('st', '--verbose adds turns, tools and tokens'),
              ('re', 'and the agent’s final reply'))}
  </div>
  <p class="note">one failing trial, with {mono('--verbose')} · {FROM}</p>''', [
    focus('ev', '1', 'yellow'), focus('st', '3~turns', 'blue'), focus('re', '3~final reply', 'blue'),
    focus('none', '4')],
    css='.annotated .code.dark{font-size:32px;line-height:1.5;padding:26px 32px}.callout{font-size:32px}.stage{gap:24px}')

ev_words = record['evidence'].split(' Available models:')[0]
rec = ('{\n  "name": "' + record['name'] + '",\n  "status": ⟦st:"' + record['status'] + '"⟧,\n  "kind": "' + record['kind']
       + '",\n  "passed": ' + json.dumps(record['passed']) + ',\n  "score": ⟦sc:' + str(record['score']) + '⟧,\n'
       + '  "evidence": ⟦ev:"LLM judge failed:⟧\n    ' + wrap(ev_words.replace('LLM judge failed: ', '').replace('"', '\\"'), 44, '    ')
       + '\n    Available models: auto, …"\n}')
framed('s11', EB2, 'A judge call can fail', f'''<div class="card">
    <div class="who">{mono('results.jsonl')} · one grader’s record, shortened</div>
    <div class="annotated">
      {code(rec, 'text', 'rec')}
      {callouts(('st', 'no verdict was reached'), ('sc', 'a placeholder, not a judgement'), ('ev', 'the reason, word for word'))}
    </div>
  </div>
  <p class="note">{FROM}</p>''', [
    focus('st', '2', 'yellow'), focus('sc', '3', 'yellow'), focus('ev', '4', 'blue'), focus('none', '5')],
    css='.card{width:100%}.card .who{font-size:30px}.annotated .code.dark{font-size:30px;line-height:1.45;padding:24px 32px}'
        '.callout{font-size:32px}.stage{gap:20px}')

regrade = [('g1', 'diff graders', 'the saved diffs', 'nothing'),
           ('g2', 'trajectory graders', 'the saved trajectories', 'nothing'),
           ('g3', 'a judge', 'the saved diffs', 'one judge call per trial'),
           ('g4', 'file and script graders', 'the workspace, which a saved run doesn’t keep', 'ERROR: it needs a new run')]
framed('s12', EB2, 'What a re-grade can read', f'''<table class="data-table full">
    <thead><tr><th>Grader</th><th>Reads</th><th>A re-grade costs</th></tr></thead>
    <tbody>
{''.join(f'<tr><td>{cell(c, a)}</td><td>{cell(c, b)}</td><td>{cell(c, d)}</td></tr>' for c, a, b, d in regrade)}
    </tbody>
  </table>
  <p class="note">{cell('new', 'a change before or during the agent’s session shows only in a new run')}</p>''', [
    focus('g1', '1~Diff', 'green'), focus('g2', '1~trajectory', 'green'), focus('g3', '2', 'blue'),
    focus('g4', '3', 'yellow'), focus('new', '4', 'blue')],
    css='.data-table{font-size:36px}.data-table th{font-size:30px}.data-table td{padding-top:22px;padding-bottom:22px}')

# ---- Chapters: the four broken evals -----------------------------------------------------------------------
FILES = [('merged-list', 'a command read as a mapping', 'one run, on one model', 'run'),
         ('quick', 'a timeout of five seconds', 'a new run', 'run'),
         ('entry', 'a pattern without (?m)', 'vally grade · free', 'grade'),
         ('judged', 'a misnamed judge model', 'vally grade · two judge calls', 'grade')]
FOUR_CSS = ('.data-table{font-size:40px}.data-table th{font-size:30px}.data-table td{padding-top:28px;padding-bottom:28px;height:56px}'
            '.data-table td.mono{font-family:var(--font-code);font-size:34px;white-space:nowrap}')


def four_table(filled):
    rows = ''.join(
        f'<tr><td class="mono">{cell("files", f + ".eval.yaml")}</td>'
        f'<td>{fault if filled else ""}</td><td>{cell(c, proof) if filled else ""}</td></tr>\n'
        for f, fault, proof, c in FILES)
    return f'''<table class="data-table full four">
    <thead><tr><th>{mono('evals/broken/')}</th><th>Fault</th><th>{cell('proof', 'Proof of the fix')}</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>'''


framed('s13', 'An eval that never starts an agent', 'Four files, one fault each', four_table(False), [
    focus('files', '1~four eval files', 'blue'), focus('proof', '4', 'yellow'), focus('none', '5')],
    css=FOUR_CSS + '.four th:nth-child(2){width:44%}.four th:nth-child(3){width:30%}')

EB_A = 'An eval that never starts an agent'
framed('s16', EB_A, 'YAML read a mapping', f'''<div class="annotated">
    {panel('ml')}
  </div>''', [
    focus('cmds', '1~commands entry', 'blue'), focus('key', '2~colon', 'yellow')],
    layout='layout-file')

framed('s17', EB_A, 'Quote the whole command', f'''<div class="annotated">
    {panel('mlf')}
  </div>''', [focus('q', '0~quotes', 'green')], layout='layout-file')

EB_B = 'A trial that runs out of time'
framed('s21', EB_B, 'Stopped, and still paid for', f'''<div class="card">
    <div class="who">{mono(f'quick/typo-fix/{SHOWN}/0/events.jsonl')} · its last lines, shortened</div>
    <div class="annotated">
      {events_box('ev')}
      {callouts(('sk', 'the skill had loaded'), ('ab', 'Vally stopped the session'),
                ('cost', f'{AIU[SHOWN]:.2f} AIU'))}
    </div>
  </div>
  <p class="note">{cell('both', f'{mono(SHOWN)} {AIU[SHOWN]:.2f} AIU · {mono(OTHER)} {AIU[OTHER]:.2f} AIU · for two trials that produced nothing')} · {FROM}</p>''', [
    focus('cost', '1', 'yellow'), focus('both', '2', 'yellow')], css=EV_CSS)

framed('s22', EB_B, 'Five seconds is the limit', f'''<div class="annotated">
    {panel('q')}
    {callouts(('to', 'the hard limit on each trial'))}
  </div>
  <p class="note">{cell('slow', 'this same request, in our run with budgets: ' + ' and '.join(f'{v:.1f} s' for v in EARLIER.values()))}</p>''', [
    focus('to', '1~timeout', 'yellow'), focus('slow', '2', 'blue'), focus('to', '3~five seconds', 'yellow')],
    layout='layout-file')

framed('s23', EB_B, 'Three minutes, like the rest', f'''<div class="annotated">
    {panel('qf')}
    {callouts(('to', 'the value in our other eval files'))}
  </div>''', [focus('to', '0~three minutes', 'green'), focus('none', '1')], layout='layout-file')

EB_C = 'A grader that fails good work'
REPLY_W = 40
framed('s26', EB_C, 'Both agents say they did it', f'''<div class="cols pair">
    {card('h', mono(H), code(STATS[0].split(' · ')[0] + ' · ' + ' · '.join(STATS[0].split(' · ')[1:]) + '\n\nagent output\n' + wrap(REPLY[0], REPLY_W, ''), 'text'))}
    {card('t', mono(T), code(STATS[1] + '\n\nagent output\n' + wrap(REPLY[1], REPLY_W, ''), 'text'))}
  </div>
  <div class="annotated">
    {code('⟦ev:✘ adds-an-entry⟧  ' + EVID.group(1), 'text', 'evid')}
    {callouts(('ev', 'the grader, on both'))}
  </div>
  <p class="note">what {mono('--verbose')} printed under each failing trial · {FROM}</p>''', [
    focus('h', '1', 'blue'), focus('t', '2', 'blue'), focus('ev', '3~grader', 'yellow')],
    css='.pair{align-items:stretch}.card > .code.dark{font-size:28px;line-height:1.45;padding:22px 26px}.card .who{font-size:30px}'
        '.annotated .code.dark.evid{font-size:28px;padding:18px 26px}.callout{font-size:30px}.stage{gap:22px}')

framed('s28', EB_C, 'A pattern that can’t match', f'''<div class="annotated">
    {panel('e')}
    {callouts(('pat', 'no (?m): ^ matches only the start of the patch'))}
  </div>''', [focus('pat', '1~caret', 'yellow')], layout='layout-file')

framed('s29', EB_C, 'Put the switch back', f'''<div class="annotated">
    {panel('ef')}
    {callouts(('m', '^ matches at the start of every line again'))}
  </div>''', [focus('m', '0', 'green')], layout='layout-file')

EB_D = 'A judge call that fails'
err_line = next(l.strip() for l in judged[H] if l.strip().startswith('ERROR'))
models_list = JB.split('Available models:')[1]
before, after = models_list.split('claude-sonnet-5.5', 1)
jb = (err_line.replace('1/2 graders', '⟦g:1/2 graders⟧') + '\n ⟦inv:Grading error; verdict is invalid.⟧\n'
      ' ✘ users-words  LLM judge failed: Model\n   ⟦nm:"claude-sonnet-5-5"⟧ is not available in Copilot.')
assert before.strip().endswith(',') or before.strip() == '', 's32: the dotted name is part of a longer name'
framed('s32', EB_D, 'Only the judge failed', f'''<div class="annotated">
    {code(jb, 'text', 'jb')}
    {callouts(('g', 'the other grader ran, and passed'), ('inv', 'no verdict from the judge'),
              ('nm', 'not on the account’s list'))}
  </div>
  <div class="annotated">
    {code('claude-sonnet-5⟦bad:-⟧5\nclaude-sonnet-5⟦good:.⟧5', 'text', 'spell')}
    {callouts(('bad', 'in the eval file'), ('good', 'on the account’s list'))}
  </div>
  <p class="note">{mono(H)}’s block, without its list of models · {FROM}</p>''', [
    focus('g', '1', 'green'), focus('inv', '2', 'yellow'), focus('nm', '3', 'yellow'),
    focus('bad', '4~hyphen', 'yellow'), focus('good', '4~dot', 'green')],
    css='.annotated .code.dark.jb{font-size:30px;line-height:1.5;padding:22px 30px}.callout{font-size:32px}.stage{gap:22px}'
        '.annotated .code.dark.spell{font-size:64px;line-height:1.35;padding:22px 40px;min-width:860px}')

framed('s33', EB_D, 'One character', f'''<div class="annotated">
    {panel('jf')}
    {callouts(('jm', 'a dot, as the account spells it'), ('dg', 'a diff grader, so the run saved the diffs'))}
  </div>''', [focus('jm', '0~one character', 'green'), focus('dg', '1~diff grader', 'blue')], layout='layout-file')

framed('s35', EB_D, 'Four faults, four proofs', four_table(True) + f'''
  <p class="note">{cell('total', f'{RUNS_SPENT} agent runs and {JUDGE_CALLS} judge calls in all')}</p>''', [
    focus('run', '1', 'yellow'), focus('grade', '2', 'green'), focus('total', '3', 'blue')],
    css=FOUR_CSS.replace('font-size:40px', 'font-size:36px').replace('padding-top:28px;padding-bottom:28px', 'padding-top:20px;padding-bottom:20px'))

# ---- Chapter: A symptom table to keep ----------------------------------------------------------------------
EB4 = 'A symptom table to keep'
framed('s36', EB4, 'Two looked like verdicts', f'''<div class="cols wide terms">
    {block('v1', 'attention', 'FAIL', 'from a grader that could not pass')}
    {block('v2', 'attention', 'score 0', 'from a judge call that failed')}
  </div>
  <p class="lead">{cell('order', 'valid, then complete, then the verdict')}</p>''', [
    focus('v1', '3', 'yellow'), focus('v2', '4', 'yellow'), focus('order', '5', 'blue')],
    css='.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}')

symptoms = [('y1', 'ERROR within milliseconds', 'the trial folder', 'one run, on one model'),
            ('y2', 'ERROR: timed out', 'events.jsonl ends in an abort', 'raise the limit · a new run'),
            ('y3', 'FAIL on a good patch', 'the evidence, then the patch', 'vally grade · free'),
            ('y4', 'ERROR: grading error', 'the grader’s record', 'vally grade · judge calls')]
framed('s37', EB4, 'Symptom, place, proof', f'''<table class="data-table full">
    <thead><tr><th>Symptom</th><th>Where to look</th><th>Cheapest proof of a fix</th></tr></thead>
    <tbody>
{''.join(f'<tr><td>{cell(c, a)}</td><td>{cell(c, b)}</td><td>{cell(c, d)}</td></tr>' for c, a, b, d in symptoms)}
    </tbody>
  </table>
  <p class="note">the four we met · the full table has ten more</p>''', [
    focus('y2', '2', 'yellow'), focus('y4', '3', 'yellow')],
    css='.data-table{font-size:36px}.data-table th{font-size:30px}.data-table td{padding-top:24px;padding-bottom:24px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="step">{i}</div><div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Is it valid?', 'lint, the run’s first lines'),
    ('Did it complete?', 'ERROR lines, the trial folder'),
    ('Why unexpected?', 'evidence, --verbose, the patch'),
    ('Does the fix work?', 'vally grade, or one new run')], 1))
framed('s38', 'Recap', 'What are the four questions?', f'''<div class="semantic-block" id="qs" data-role="structure">
    <div class="title words">when a run goes wrong</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#qs", "at": "1"},
    focus('p1', '1', 'blue'), focus('p2', '2', 'cyan'), focus('p3', '3', 'yellow'), focus('p4', '4', 'orange')],
    layout='layout-expand',
    css='#qs{width:100%;padding:36px 40px 44px;gap:24px}'
        '#qs .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#qs .part{min-height:300px}#qs .part .title{font-size:44px;line-height:1.2}'
        '#qs .part .label{font-size:30px}')

scene('s39', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Keep it working</h1>
  <p class="lead">Make it a routine you and a teammate can repeat.</p>
  <p class="note">Exercises and the full symptom table are on the lesson page · Source: Vally docs, “Debugging Evals”</p>
</main>''', [], css='.scene-title.chapter{font-size:116px}')
print('ok', 'PROVISIONAL (stand-in run data)' if PROV else 'own run')
