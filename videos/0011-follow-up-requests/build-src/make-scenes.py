"""Generate lesson 11's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout), terms in
soft blocks. Nothing here sets a colour or a font outside the theme's variables; a scene's own CSS is
sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/conversation.start.eval.yaml   the conversation as the practice folder has it before this lesson
  src/state/conversation.eval.yaml         the same file with the five graders (what s14's tape installs)
  src/state/SKILL.md                       the skill with the new rule (what s17's tape installs)
  src/run/                                 what the recordings printed: lint.log, before.log (s14),
                                           failing-turn.diff (s15), after.log (s17), RUN (the run folder).
                                           This video's own runs (src/run/README).
  src/earlier/                             the first take of s14, quoted in s18 as "an earlier run".

The asserts below are what the narration states about the run. If a recording disagrees, this fails:
reword the "outcome" sentences in storyboard.json, then change the asserts to match.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')


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


def card(cid, who, body):
    return f'''<div class="card" data-concept="{cid}" data-rep="card">
        <div class="who">{who}</div>
        {body}
      </div>'''


def mono(t):
    return f'<span class="mono">{t}</span>'


def quote(cid, who, html):
    return f'''<div class="quote" data-concept="{cid}" data-rep="quote"><span class="who">{who}</span><p>{html}</p></div>'''


# ---- Rows of boxes: one box per conversation, one mark per box (as in lesson 3) -------------------
MARK = {'p': ('tick', '✔'), 'f': ('cross', '✘')}


def boxes(marks):
    return '<span class="boxes">' + ''.join(
        f'<span class="box {MARK[m][0]}">{MARK[m][1]}</span>' for m in marks) + '</span>'


BOX_CSS = ('.boxes{display:flex;gap:14px}'
           '.box{display:flex;align-items:center;justify-content:center;width:76px;height:76px;border-radius:8px;'
           'border:3px solid var(--ink-muted);font:700 44px/1 var(--font-body);color:var(--ink)}'
           '.box.tick{color:var(--green-ink)}.box.cross{color:var(--red-ink)}')

# ---- The real things, read from src/ ---------------------------------------------------------------
# The three requests, from the eval file as the practice folder has it.
start = (D / 'src/state/conversation.start.eval.yaml').read_text().splitlines()
assert start[14].strip() == 'turns:' and len(start) == 25, 'conversation.start.eval.yaml changed'
REQ, cur = [], None
for line in start[15:]:
    if line.strip() == '- |':
        cur = []
        REQ.append(cur)
    else:
        cur.append(line.strip())
REQ = [' '.join(r) for r in REQ]
assert len(REQ) == 3 and REQ[0].startswith('PR 64 is merged') and 'PR 65' in REQ[1] and 'PR' not in REQ[2], REQ
req_html = lambda t: re.sub(r'`([^`]+)`', lambda m: mono(m.group(1)), t)

final = (D / 'src/state/conversation.eval.yaml').read_text().splitlines()
assert final[:25] == start and final[25].strip() == 'graders:' and len(final) == 48
assert sum(l.strip().startswith('- type:') for l in final[25:]) == 5          # "the five graders"
assert final[43].strip() == r"pattern: '(?m)^\+.*\(#\d+\)'"

skill = (D / 'src/state/SKILL.md').read_text().splitlines()
before_skill = (D / 'src/state/SKILL.before.md').read_text().splitlines()
assert skill[:28] == before_skill and len(skill) == 31 and skill[28].startswith('- Treat every request on its own.')

ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\r')
log = lambda name: ANSI.sub('', (D / 'src/run' / name).read_text())
RUN = (D / 'src/run/RUN').read_text().strip()
assert not (D / 'src/run/PROVISIONAL').exists(), 'src/run must hold this video\'s own runs'

# s14, lint: "One warning … and no errors."
lint = log('lint.log')
assert '1 warning(s)' in lint and 'scoring-defaults-applied' in lint and 'error' not in lint.lower(), lint


def summary(text):
    """The summary row: {model: passed?} from '  conversation  ✘ 0/1   ✓ 1/1'."""
    m = re.search(r'^\s*conversation\s+([✓✘]) \d/1\s+([✓✘]) \d/1\s*$', text, re.M)
    assert m, 'no summary row'
    return {MODELS[0]: m.group(1) == '✓', MODELS[1]: m.group(2) == '✓'}


def trials(name):
    """{model: [trial, …] by trialIndex} from the reduced results; every trial finished."""
    rows = json.loads((D / 'src/run' / name).read_text())
    assert len(rows) == 6 and all(r['status'] == 'success' and len(r['graders']) == 5 for r in rows), rows
    return {m: sorted((r for r in rows if r['model'] == m), key=lambda r: r['trialIndex']) for m in MODELS}


marks = lambda ts: ''.join('p' if t['passed'] else 'f' for t in ts)

# s14, the first run. What the narration states:
#   - a block above the summary for haiku only: one of its three conversations failed;
#   - the failing grader is third-no-made-up-number, and the terminal points at "trial 2";
#   - every other grader passed on both models, so terra passed all three.
# The terminal counts trials from 1 and file names from 0: its "trial 2" is trialIndex 1 (s15, s20).
before = log('before.log')
assert summary(before) == {MODELS[0]: False, MODELS[1]: True}, summary(before)
fails = re.findall(r'✘ conversation · three-requests \[([^\]]+)\]\n\s+✘ (\S+)\s.*· trials? ([\d, ]+)', before)
assert fails == [('claude-haiku-4.5', 'third-no-made-up-number', '2')], fails
assert 'ERROR' not in before and before.count('three-requests [') == 1
T_BEFORE = trials('before.trials.json')
BEFORE = {m: marks(T_BEFORE[m]) for m in MODELS}
assert BEFORE == {MODELS[0]: 'pfp', MODELS[1]: 'ppp'}, BEFORE
bad = [g['name'] for m in MODELS for t in T_BEFORE[m] for g in t['graders'] if not g['passed']]
assert bad == ['third-no-made-up-number'], bad

# s17, the second run: a tick for each model, no block above the summary, all six passed.
after = log('after.log')
assert summary(after) == {MODELS[0]: True, MODELS[1]: True}, summary(after)
assert not re.search(r'FLAKY|FAIL|ERROR|Failures', after)
AFTER = {m: marks(ts) for m, ts in trials('after.trials.json').items()}
assert AFTER == {m: 'ppp' for m in MODELS}, AFTER


def third_turn(path):
    """The one entry a third turn's diff added, and the lines it added."""
    lines = (D / path).read_text().splitlines()
    hunk = lines[next(i for i, l in enumerate(lines) if l.startswith('@@')) + 1:]
    added = [l[1:] for l in hunk if l.startswith('+')]
    entries = [l for l in added if l.startswith('- ')]
    assert len(entries) == 1 and '### Fixed' in added, added
    return entries[0], hunk


# s15, the failing turn's diff in our run: one entry, under a Fixed heading, about notes export,
# citing (#66): a number no request gave (the requests gave 64 and 65).
ENTRY, _ = third_turn('src/run/failing-turn.diff')
assert ENTRY.endswith('(#66)') and 'notes export' in ENTRY, ENTRY
assert not any('66' in r for r in REQ) and '64' in REQ[0] and '65' in REQ[1]
# s18, "an earlier run": the same turn in this video's first take (src/earlier/README) cited (#65),
# the second request's number.
EARLIER, _ = third_turn('src/earlier/turn-2.diff')
assert EARLIER.endswith('(#65)') and 'notes export' in EARLIER, EARLIER
# s19: the Unreleased section as the failing conversation left it, from the whole conversation's diff:
# the lines it added. The first entry, citing (#64), is still there.
whole = (D / 'src/run/failing-conversation.diff').read_text().splitlines()
left = [l[1:] for l in whole if l.startswith('+') and not l.startswith('+++')]
while left and not left[-1].strip():
    left.pop()
assert left[0] == '### Changed' and left[1].endswith('(#64)') and left[-1] == ENTRY, left
# s19: "hadn't made up a number in any of our single-request runs".
single = json.loads((D / 'src/run/haiku-single-requests.json').read_text())
assert single['made_up_a_number'] == 0 and single['trials'] == sum(n for n, _ in single['by_run'].values()) == 16

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Follow-up requests', f'''<div class="asks">
    {quote('q0', 'A request', req_html(REQ[0]))}
    {quote('q1', 'Then a second', req_html(REQ[1]))}
    {quote('q2', 'Then a third', req_html(REQ[2]))}
  </div>''', [
    {"type": "focus", "target": "q0", "at": "1~changelog entry", "color": "blue"},
    {"type": "focus", "target": "q1", "at": "1~second", "color": "blue"},
    {"type": "focus", "target": "q2", "at": "1~third", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:112px}'
        '.asks{display:flex;flex-direction:column;gap:18px;width:100%}'
        '.asks .quote{font-size:33px;padding:18px 34px 20px}.asks .quote > .who{margin-bottom:6px}')

# ---- Chapter: What changes in a conversation -----------------------------------------------------
CH1 = 'What changes in a conversation'
TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'
framed('s02', CH1, 'What the agent keeps', f'''<p class="lead"><span data-concept="turn" data-rep="note">A turn is one request in a conversation.</span></p>
  <div class="cols wide terms">
    {block("ws", "structure", "the workspace", "as the last turn left it", words=True)}
    {block("mem", "attention", "its memory", "of what was said in earlier turns", words=True)}
  </div>''', [
    {"type": "focus", "target": "turn", "at": "1~turn", "color": "blue"},
    {"type": "focus", "target": "ws", "at": "3~workspace", "color": "blue"},
    {"type": "focus", "target": "mem", "at": "4", "color": "yellow"}],
    css=TERMS + '.lead{font-size:42px;margin:0}.stage{gap:44px}')

WAYS = [('fades', 'A rule fades', 'later turns follow recent work more than the skill'),
        ('leaks', 'An earlier turn leaks', 'a detail is carried into a change it has nothing to do with'),
        ('disturbs', 'A later turn disturbs earlier work', 'something already done is rewritten or dropped')]
framed('s03', CH1, 'Three new ways to fail', f'''<div class="cols terms">
    {''.join(block(c, 'attention', t, l, words=True) for c, t, l in WAYS)}
  </div>''', [
    {"type": "focus", "target": "fades", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "leaks", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "disturbs", "at": "4", "color": "yellow"}],
    css='.terms .semantic-block{min-height:330px}.terms .title{font-size:42px;line-height:1.2}.terms .label{font-size:32px}')

framed('s04', CH1, 'Graded turn by turn', f'''<div class="cols wide terms">
    {block("final", "structure", "A grader on the final file", "can’t say which turn went wrong, and can miss a leak", words=True)}
    {block("each", "success", "A grader for each turn", "what did this request alone change?", words=True)}
  </div>''', [
    {"type": "focus", "target": "final", "at": "1", "color": "blue"},
    {"type": "focus", "target": "each", "at": "2~turn by turn", "color": "green"}],
    css=TERMS)

framed('s05', CH1, 'A script, not a user', f'''<div class="cols wide terms">
    {block("script", "structure", "A script of requests", "sent in order, whatever the agent replied: this is what Vally sends", words=True)}
    {block("user", "attention", "A user who answers back", "Vally doesn’t play one", words=True)}
  </div>
  <p class="note">Source: Vally docs, Writing Eval Specs, “Multi-turn conversations”</p>''', [
    {"type": "focus", "target": "script", "at": "1", "color": "blue"},
    {"type": "focus", "target": "user", "at": "2~user", "color": "yellow"},
    {"type": "focus", "target": "script", "at": "3~script", "color": "blue"},
    {"type": "focus", "target": "user", "at": "3~user", "color": "yellow"}],
    css=TERMS)

# ---- Chapter: Turns and scoped graders -----------------------------------------------------------
CH2 = 'Turns and scoped graders'
framed('s06', CH2, 'A stimulus with turns', panel('conv'), [
    {"type": "focus", "target": "turns", "at": "1~turns", "color": "blue"},
    {"type": "focus", "target": "r1", "at": "2~first", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}], layout='layout-file')

framed('s07', CH2, 'Three requests, three rules', panel('conv'), [
    {"type": "focus", "target": "r1", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#conv", "to": "20-25", "at": "2"},
    {"type": "focus", "target": "r2", "at": "2~internal", "color": "yellow"},
    {"type": "focus", "target": "r3", "at": "3", "color": "yellow"}], layout='layout-file')

turn_block = lambda i, which: block(f't{i}', 'structure', f'turn: {i}', f'{which} request<br>its own diff')
framed('s08', CH2, 'Each turn, its own diff', f'''<div class="cols scoped">
    {turn_block(0, 'first')}
    {turn_block(1, 'second')}
    {turn_block(2, 'third')}
  </div>
  {block('whole', 'transform', 'no turn:', 'the whole conversation’s diff')}''', [
    {"type": "focus", "target": "t0", "at": "3~zero", "color": "blue"},
    {"type": "focus", "target": "t2", "at": "4~turn two", "color": "blue"},
    {"type": "focus", "target": "whole", "at": "5", "color": "cyan"}],
    css='.semantic-block .title{font-family:var(--font-code);font-size:42px}.scoped .semantic-block{min-height:230px}'
        '.semantic-block .label{font-size:34px}.stage{gap:36px}.stage > .semantic-block{width:100%;min-height:150px}')

SCOPE = [('diffs3', f'{mono("diff-contains")}, {mono("diff-not-contains")}, {mono("diff-empty")}',
          'the patch of what the agent changed', 'yes'),
         ('events', mono('skill-invocation'), 'the agent’s events', 'yes'),
         ('script', 'a script grader', 'the workspace at the very end', 'no')]
rows = ''.join(f'<tr><td>{g}</td><td>{reads}</td>'
               f'<td><span data-concept="{c}" data-rep="cell">{yn}</span></td></tr>\n' for c, g, reads, yn in SCOPE)
framed('s09', CH2, 'Not every grader can be scoped', f'''<table class="data-table full scope">
    <thead><tr><th>grader</th><th>what it reads</th><th>can take {mono("turn:")}</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>''', [
    {"type": "focus", "target": "diffs3", "at": "1", "color": "green"},
    {"type": "focus", "target": "events", "at": "2", "color": "green"},
    {"type": "focus", "target": "script", "at": "3", "color": "yellow"}],
    css='.scope{font-size:36px}.scope td{padding-top:34px;padding-bottom:34px}.scope td .mono{font-size:32px}'
        '.scope th{font-size:30px;white-space:nowrap}.scope th .mono{font-size:28px}.scope td:first-child{white-space:nowrap}.scope td:first-child .mono{font-size:29px}')

NOTES_A = [('turn0', 'beside type and name'), ('pat64', 'turn 0 must add a line citing (#64)'),
           ('turn1', 'turn 1 must change nothing')]
NOTES_B = [('export', 'turn 2 must add this entry'), ('nopr', 'and no line citing a pull request'),
           ('survive', 'no turn: the whole conversation')]
framed('s10', CH2, 'A grader for each turn', f'''<div class="annotated">
    {panel('graders')}
    {callouts(*NOTES_A, *NOTES_B)}
  </div>''', [
    {"type": "scroll", "target": "#graders", "to": "26-34", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "turn0", "at": "1~turn key", "color": "blue"},
    {"type": "focus", "target": "pat64", "at": "2~sixty-four", "color": "blue"},
    {"type": "focus", "target": "turn1", "at": "3~turn one", "color": "blue"}], layout='layout-file')

framed('s11', CH2, 'The third turn, then everything', f'''<div class="annotated">
    {panel('graders')}
    {callouts(*NOTES_A, *NOTES_B)}
  </div>''', [
    {"type": "scroll", "target": "#graders", "to": "26-34", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#graders", "to": "35-43", "at": "0+0.6"},
    {"type": "focus", "target": "export", "at": "1~notes export", "color": "blue"},
    {"type": "scroll", "target": "#graders", "to": "40-48", "at": "2"},
    {"type": "focus", "target": "nopr", "at": "2~no line", "color": "yellow"},
    {"type": "focus", "target": "survive", "at": "3~no turn", "color": "cyan"}], layout='layout-file')

tree = f'''results/lesson-11/
  ⟦run:{RUN}/⟧
    ⟦diffs:diffs/⟧
      …⟦name:__trial-1__turn-2.diff⟧'''
framed('s12', CH2, 'One diff per turn', f'''<div class="annotated">
    {code(tree, 'text', 'tree')}
    {callouts(('run', 'the run folder'), ('diffs', 'one file per turn of every trial'),
              ('name', 'trial and turn, both from 0'))}
  </div>''', [
    {"type": "focus", "target": "diffs", "at": "1~diffs", "color": "blue"},
    {"type": "focus", "target": "name", "at": "2~trial", "color": "yellow"}],
    css='.code.dark.tree{min-width:860px;font-size:38px;line-height:1.7}.callout{font-size:34px}')

# ---- Chapter: Run the conversation ---------------------------------------------------------------
CH3 = 'Run the conversation'
ASK = [('PR 64: a change in behaviour', 'wanted: an entry citing (#64)'),
       ('PR 65: an internal rename', 'wanted: nothing added'),
       ('a fix, with no number given', 'wanted: an entry citing nothing')]
framed('s13', CH3, 'Which turn goes wrong?', f'''<div class="cols asked">
    {''.join(block(f't{i}', 'structure', f'turn {i}', f'{what}<br>{want}') for i, (what, want) in enumerate(ASK))}
  </div>
  <p class="note">three conversations on each model · every turn graded on its own</p>''', [
    {"type": "focus", "target": "t0", "at": "2~three turns", "color": "blue"},
    {"type": "focus", "target": "t1", "at": "2~expect", "color": "blue"},
    {"type": "focus", "target": "t2", "at": "2~wrong", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.asked .semantic-block{min-height:300px}.asked .title{font-family:var(--font-code);font-size:42px}'
        '.asked .label{font-size:32px;line-height:1.5}')

framed('s16', CH3, 'One more rule', panel('skill'), [
    {"type": "focus", "target": "rule", "at": "1~one more rule", "color": "yellow"}], layout='layout-file')

# ---- Chapter: What the conversation showed -------------------------------------------------------
CH4 = 'What the conversation showed'
pr65 = lambda t: t.replace('PR 65', '<span data-concept="q65" data-rep="quote">PR 65</span>', 1)
both = '\n'.join(['+' + ENTRY.replace('(#66)', '⟦n66:(#66)⟧'), '+' + EARLIER.replace('(#65)', '⟦n65:(#65)⟧')])
framed('s18', CH4, 'One invented, one leaked', f'''<div class="cols asks">
    {quote('second', 'Turn 1 · the second request', pr65(req_html(REQ[1])))}
    {quote('third', 'Turn 2 · the third request', req_html(REQ[2]))}
  </div>
  <div class="annotated">
    {card('added', f'What turn 2 added · {mono("claude-haiku-4.5")}', code(both, 'diff'))}
    {callouts(('n66', 'our run: a number nobody gave'), ('n65', 'an earlier run: the second request’s number'))}
  </div>''', [
    {"type": "focus", "target": "n66", "at": "1~line", "color": "yellow"},
    {"type": "focus", "target": "n65", "at": "3~earlier run", "color": "yellow"},
    {"type": "focus", "target": "q65", "channel": "source", "at": "4~belongs", "until": "5", "color": "yellow"}],
    css='.asks .quote{font-size:31px;padding:20px 28px 22px}.stage{gap:34px}'
        '.card > .code.dark{font-size:29px;flex:none;line-height:1.9;padding:22px 28px}.card .who{font-size:30px}'
        '.callout{font-size:30px}.callouts{margin-top:44px}')

left_src = '\n'.join(left[:-1] + [f'⟦last:{left[-1]}⟧'])
framed('s19', CH4, 'The final file looks fine', f'''<div class="annotated">
    {card('file', f'{mono("CHANGELOG.md")} · Unreleased, at the end of that conversation', code(left_src, 'markdown'))}
    {callouts(('last', 'tidy, well-formed, a plausible reference'))}
  </div>''', [
    {"type": "focus", "target": "last", "at": "1~final file", "color": "yellow"}],
    css='.card > .code.dark{font-size:31px;line-height:1.6;padding:26px 30px}.card .who{font-size:32px}'
        '.callout{font-size:32px}.callouts{margin-top:50px}')


def group(cid, who, marks):
    lines = ''.join(f'<div class="trow" data-concept="{cid}-{m.split("-")[1]}" data-rep="row">'
                    f'<span class="who">{m}</span>{boxes(marks[m])}</div>' for m in MODELS)
    return f'''<div class="card grp" data-concept="{cid}" data-rep="card">
      <div class="who">{who}</div>
      {lines}
    </div>'''


framed('s20', CH4, 'Before the rule, and after', f'''<div class="cols wide">
    {group('before', 'before the rule', BEFORE)}
    {group('after', 'after the rule', AFTER)}
  </div>
  <p class="note">one box per conversation · three on each model · our runs</p>''', [
    {"type": "focus", "target": "before", "at": "0~Before", "color": "yellow"},
    {"type": "focus", "target": "after", "at": "0~after it", "color": "green"},
    {"type": "focus", "target": "none", "at": "1"}],
    css=BOX_CSS + '.grp{gap:22px;padding:26px 30px;border-radius:10px}.grp > .who{font-size:36px}'
        '.trow{display:flex;align-items:center;gap:30px}.trow .who{font:500 32px/1 var(--font-code);color:var(--ink);min-width:340px}')

framed('s21', CH4, 'What no pattern can decide', f'''<div class="cols wide terms">
    {block("q1", "attention", "Is this the right category?", "no grader here asks", words=True)}
    {block("q2", "attention", "Is it written for the people who use the tool?", "the question we left open earlier", words=True)}
  </div>
  <p class="lead"><span data-concept="both" data-rep="note">Both are judgements about meaning.</span></p>''', [
    {"type": "focus", "target": "q1", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "q2", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "both", "at": "4", "color": "blue"}],
    css='.terms .semantic-block{min-height:300px}.terms .title{font-size:42px;line-height:1.2}.terms .label{font-size:34px}'
        '.lead{font-size:40px;margin:0}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (_, t, l) in enumerate(WAYS, 1))
framed('s22', 'Recap', 'Three ways a conversation fails?', f'''<div class="semantic-block" id="ways" data-role="structure">
    <div class="title words">a conversation, not a single request</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#ways", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"}], layout='layout-expand',
    css='#ways{width:100%;padding:36px 40px 44px;gap:24px}'
        '#ways .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#ways .part{min-height:300px}#ways .part .title{font-size:42px;line-height:1.2}'
        '#ways .part .label{font-size:30px}')

scene('s23', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">A judge for what code cannot check</h1>
  <p class="lead">“Written for the people who use the tool” is not a pattern. How do you grade that?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, Writing Eval Specs, “Multi-turn conversations”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok')
