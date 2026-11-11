"""Generate lesson 3's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 and 2: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/haiku.patch, terra.patch, record.json, one-request.eval.yaml   the lesson 1 video's run
                                                                    (2026-11-11T00-11-52-424Z)
  src/run/                                                          the run this video's s10 recorded
                                                                    (name in src/run/RUN), with
                                                                    /Users/Shared/demo shown as ~/src/demo

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess, textwrap

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


# ---- Rows of trial boxes: one box per trial, one mark per box --------------------------------------
MARK = {'p': ('tick', '✔'), 'f': ('cross', '✘'), 'e': ('dash', '–'), ' ': ('empty', '')}


def boxes(marks, concept=None):
    out = ''
    for i, m in enumerate(marks):
        cls, glyph = MARK[m]
        c = f' data-concept="{concept(i, m)}" data-rep="box"' if concept and concept(i, m) else ''
        out += f'<span class="box {cls}"{c}>{glyph}</span>'
    return f'<span class="boxes">{out}</span>'


def trow(cid, left, marks, right, concept=None):
    return f'''<div class="trow" data-concept="{cid}" data-rep="row">
      {left}{boxes(marks, concept)}{right}
    </div>'''


BOX_CSS = ('.rows{display:flex;flex-direction:column;gap:26px;width:100%}'
           '.trow{display:flex;align-items:center;gap:36px;padding:14px 22px;border-radius:10px;width:fit-content}'
           '.boxes{display:flex;gap:14px}'
           '.box{display:flex;align-items:center;justify-content:center;width:76px;height:76px;border-radius:8px;'
           'border:3px solid var(--ink-muted);font:700 44px/1 var(--font-body);color:var(--ink)}'
           '.box.tick{color:var(--green-ink)}.box.cross{color:var(--red-ink)}.box.dash{color:var(--ink-muted)}'
           '.box.empty{border-color:var(--rule)}'
           '.trow .word{font:600 44px/1 var(--font-code);color:var(--ink);min-width:190px}'
           '.trow .mean{font:400 36px/1.3 var(--font-body);color:var(--ink-soft)}'
           '.trow .who{font:500 34px/1 var(--font-code);color:var(--ink);min-width:400px}')

# ---- The real things, read from src/ -----------------------------------------------------------
def added_entry(path):
    """The changelog entry a trial added: the one '+- ' line of its real patch, verbatim."""
    lines = [l[1:] for l in (D / 'src' / path).read_text().splitlines() if l.startswith('+- ')]
    assert len(lines) == 1, f'{path}: expected one added entry, found {lines}'
    return lines[0]


PR = re.compile(r'\(#\d+\)\s*$')
entry_a, entry_b = added_entry('haiku.patch'), added_entry('terra.patch')
assert PR.search(entry_b) and not PR.search(entry_a)
mark_pr = lambda e, cid='pr': PR.sub(lambda m: f'⟦{cid}:{m.group(0).strip()}⟧', e)

eval_lines = (D / 'src/one-request.eval.yaml').read_text().splitlines()
assert eval_lines[17].strip() == 'graders:' and eval_lines[22].strip() == 'value: "notes add"'
GRADER = '\n'.join(l[4:] for l in eval_lines[17:23])

RUN = (D / 'src/run/RUN').read_text().strip()
ENTRIES = {m: [added_entry(f'run/{m}-{i}.patch') for i in range(5)] for m in MODELS}
MADE_UP = {m: sum(bool(PR.search(e)) for e in ENTRIES[m]) for m in MODELS}
trials = [json.loads(l) for l in (D / 'src/run/results.jsonl').read_text().splitlines() if l.strip()]
trials = [t for t in trials if t.get('type') == 'trial-result']
assert len(trials) == 10 and all(t['status'] == 'success' and t['gradeResult']['passed'] for t in trials)
REPLY = {m: [next(t['trajectory']['output'] for t in trials if t['model'] == m and t['trialIndex'] == i)
             for i in range(5)] for m in MODELS}
# What the narration says about this run. If a re-recording changes these, the sentences change too.
assert MADE_UP == {'claude-haiku-4.5': 0, 'gpt-5.6-terra': 5}, MADE_UP
assert {PR.search(e).group(0).strip() for e in ENTRIES['gpt-5.6-terra']} == {'(#42)'}
assert all('#42' in r for r in REPLY['gpt-5.6-terra'])

# ---- Hook ----------------------------------------------------------------------------------------
once = '<span class="once" data-concept="once" data-rep="note">one trial</span>'
framed('s01', 'Vally &amp; Agent Evals', 'The same request, five times', f'''<div class="results">
      {card('card-a', f'{mono("claude-haiku-4.5")} · {once}', code(entry_a, 'markdown'))}
      {card('card-b', f'{mono("gpt-5.6-terra")} · {once}', code(mark_pr(entry_b), 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "pr", "at": "0~pull request", "color": "yellow"},
    {"type": "focus", "target": "once", "at": "2~once", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}'
        '.results{display:flex;flex-direction:column;gap:44px;width:100%}'
        '.results .card > .code.dark{font-size:40px;padding:30px 36px}.results .card .who{font-size:34px}')

# ---- Chapter: Does it happen every time? ---------------------------------------------------------
nums = '<div class="trow head"><span class="who"></span><span class="boxes">' + ''.join(
    f'<span class="num">{i}</span>' for i in range(5)) + '</span></div>'


def seen_row(model, seen):
    cells = f'<span class="box wide seen" data-concept="seen" data-rep="box">{seen}</span>' + ''.join(
        '<span class="box wide empty" data-concept="rest" data-rep="box"></span>' for _ in range(4))
    return f'<div class="trow"><span class="who">{model}</span><span class="boxes">{cells}</span></div>'


framed('s02', 'Does it happen every time?', 'One trial is one sample', f'''<div class="rows">
    {nums}
    {seen_row('claude-haiku-4.5', 'no number')}
    {seen_row('gpt-5.6-terra', '(#42)')}
  </div>
  <p class="note">trial 0 is the one we have seen · trials 1 to 4 have not been run</p>''', [
    {"type": "focus", "target": "seen", "at": "0~once", "color": "blue"},
    {"type": "focus", "target": "rest", "at": "2~varies", "color": "yellow"},
    {"type": "focus", "target": "seen", "at": "4~single trial", "color": "blue"}],
    css=BOX_CSS + '.box.wide{width:226px;height:110px;font:500 32px/1 var(--font-code)}'
        '.trow.head{padding-top:0;padding-bottom:0}.num{width:226px;text-align:center;font:500 30px/1 var(--font-code);color:var(--ink-muted)}'
        '.trow .who{min-width:380px}.rows{gap:18px}')

framed('s03', 'Does it happen every time?', 'Once can’t say how often', f'''<div class="cols wide terms">
    {block("can", "structure", "Can this happen?", "one trial answers it", words=True)}
    {block("often", "attention", "How often?", "needs several trials of the same stimulus", words=True)}
  </div>''', [
    {"type": "focus", "target": "can", "at": "0~one time", "color": "blue"},
    {"type": "focus", "target": "often", "at": "2~how often", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}')

framed('s03b', 'Does it happen every time?', 'Identical runs, different scores', f'''<div class="cols wide terms">
    {block("same", "structure", "Same agent, same tasks", "run several times", words=True)}
    {block("moved", "attention", "2 to 6 percentage points", "how far its score moved between runs", words=True)}
  </div>
  <p class="note">Source: a 2026 preprint from KTH · one benchmark · not yet peer reviewed</p>''', [
    {"type": "focus", "target": "same", "at": "1~same agent", "color": "blue"},
    {"type": "focus", "target": "moved", "at": "2~two to six", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}')

# ---- Chapter: Five trials, four outcomes ---------------------------------------------------------
segs = [('cmd', 'vally eval … ⟦runs:--runs 5⟧', None),
        ('ev', 'one-request/', 'the eval'),
        ('stim', '  typo-fix/', 'the stimulus'),
        ('model', '    gpt-5.6-terra/', 'one of the models'),
        ('nums', '      0/  1/  2/  3/  4/', 'one folder per trial'),
        ('patch', '        workspace.patch', 'each with its own patch')]
tree = '\n'.join(p if c == 'cmd' else re.sub(r'^(\s*)(\S.*)$', lambda m, c=c: f'{m.group(1)}⟦{c}:{m.group(2)}⟧', p)
                 for c, p, _ in segs)
framed('s04', 'Five trials, four outcomes', 'Five trials, five folders', f'''<div class="annotated">
    {code(tree, 'text', 'tree')}
    {callouts(('runs', 'every stimulus, five times'), *[(c, m) for c, _, m in segs if m])}
  </div>''', [
    {"type": "focus", "target": "runs", "at": "1~runs five", "color": "blue"},
    {"type": "focus", "target": "nums", "at": "3~numbered", "color": "yellow"},
    {"type": "focus", "target": "patch", "at": "3~patch", "color": "orange"},
    {"type": "focus", "target": "stim", "at": "4~one stimulus", "color": "blue"},
    {"type": "focus", "target": "model", "at": "4~two models", "color": "blue"}],
    css='.code.dark.tree{min-width:900px;font-size:38px;line-height:1.7}.callout{font-size:34px}')

WORDS = [('w-pass', 'ppppp', 'PASS', 'every trial passed'),
         ('w-flaky', 'fpppp', 'FLAKY', 'some passed, some failed'),
         ('w-fail', 'fffff', 'FAIL', 'no trial passed'),
         ('w-error', 'pepep', 'ERROR', 'a trial didn’t finish: no verdict')]
word_row = lambda c, m, w, mean: trow(c, '', m, f'<span class="word">{w}</span><span class="mean">{mean}</span>')
framed('s05', 'Five trials, four outcomes', 'Four words for a stimulus', f'''<div class="rows">
    {''.join(word_row(*w) for w in WORDS)}
  </div>
  <p class="note">An illustration: five trials of one stimulus on one model</p>''', [
    {"type": "focus", "target": "w-pass", "at": "2", "color": "green"},
    {"type": "focus", "target": "w-flaky", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "w-fail", "at": "4", "color": "red"},
    {"type": "focus", "target": "w-error", "at": "5", "color": "blue"}], css=BOX_CSS)

framed('s06', 'Five trials, four outcomes', 'Error is not a failure', f'''<div class="rows big">
    {trow('w-error', '', 'pepep', '<span class="word">ERROR</span>',
          concept=lambda i, m: 'gone' if m == 'e' else None)}
  </div>
  <p class="lead"><span data-concept="noanswer" data-rep="note">A trial that didn’t finish gave no answer to judge.</span></p>
  <p class="lead"><span data-concept="again" data-rep="note">We run it again, or leave the trial out and say so.</span></p>''', [
    {"type": "focus", "target": "gone", "at": "1~no answer", "color": "yellow"},
    {"type": "focus", "target": "noanswer", "at": "1~connection", "color": "yellow"},
    {"type": "focus", "target": "again", "at": "2", "color": "blue"}],
    css=BOX_CSS + '.big .box{width:120px;height:120px;font-size:64px}.big .boxes{gap:22px}.big .word{font-size:60px}'
        '.lead{font-size:42px;margin:0}.stage{gap:44px}')

framed('s07', 'Five trials, four outcomes', 'Every trial keeps its reply', f'''<div class="annotated">
    {panel('record')}
    {callouts(('output', 'the agent’s final reply'))}
  </div>''', [
    {"type": "scroll", "target": "#record", "to": "517-519", "at": "2"},
    {"type": "focus", "target": "output", "at": "2~output", "color": "yellow"}], layout='layout-file')

# ---- Chapter: Why two workers --------------------------------------------------------------------
wrow = lambda c, label, marks, right: trow(c, f'<span class="who">{label}</span>', marks, f'<span class="mean">{right}</span>')
framed('s08', 'Why two workers', 'Two at a time', f'''<div class="annotated">
    {code('⟦flag:--workers 2⟧', 'bash')}
    {callouts(('flag', 'agent sessions at once · default 5'))}
  </div>
  <div class="rows">
    {wrow('five', '5 workers', 'ppepppeppe', '3 of 10 ended in ERROR')}
    {wrow('two', '2 workers', 'pppppppppp', 'all 10 finished')}
  </div>
  <p class="note">ERROR · <span class="mono" data-concept="msg" data-rep="note">Session disconnected while waiting for a response</span> · which three trials dropped is illustrative</p>''', [
    {"type": "focus", "target": "flag", "at": "2~workers", "color": "blue"},
    {"type": "focus", "target": "five", "at": "4~five workers", "color": "red"},
    {"type": "focus", "target": "msg", "at": "4~message", "color": "red"},
    {"type": "focus", "target": "two", "at": "5", "color": "green"},
    {"type": "focus", "target": "none", "at": "7"}],
    css=BOX_CSS + '.annotated .code.dark{font-size:44px;padding:30px 40px}.callout{font-size:36px}'
        '.box{width:64px;height:64px;font-size:38px}.boxes{gap:10px}.trow .who{min-width:230px;font-family:var(--font-body);font-size:36px}'
        '.rows{gap:14px}.stage{gap:30px}')

# ---- Chapter: Count it ---------------------------------------------------------------------------
COLS = [('c-none', 'Entry, no number'), ('c-made', 'Entry, made-up number'), ('c-no', 'No entry')]


def tally(filled):
    head = ''.join(f'<th class="num"><span data-concept="{c}" data-rep="head">{t}</span></th>' for c, t in COLS)
    body = ''
    for key, m in zip('ht', MODELS):
        made = MADE_UP[m]
        counts = (5 - made, made, 0) if filled else ('', '', '')
        body += f'<tr><td class="mono">{m}</td>' + ''.join(
            f'<td class="num"><span data-concept="{key}-{c[2:]}" data-rep="cell">{n}</span></td>'
            for (c, _), n in zip(COLS, counts)) + '</tr>\n'
    return f'''<table class="data-table full tally">
    <thead><tr><th></th>{head}</tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


TALLY_CSS = ('.tally{font-size:56px}.tally th{font-size:32px}.tally td{padding-top:40px;padding-bottom:40px;height:70px}'
             '.tally td.mono{font-family:var(--font-code);font-size:36px}'
             '.tally th:last-child,.tally td:last-child{padding-right:16px}')
framed('s09', 'Count it', 'Ten trials, one tally', tally(False) + '''
  <p class="note">one mark per trial · five trials for each model</p>''', [
    {"type": "focus", "target": "c-none", "at": "2~no number", "color": "blue"},
    {"type": "focus", "target": "c-made", "at": "2~made-up", "color": "yellow"},
    {"type": "focus", "target": "c-no", "at": "2~no entry", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}], css=TALLY_CSS)


def entry_list(model, cid=None):
    return '\n'.join(f'{i}  ' + (mark_pr(e, cid) if cid else e) for i, e in enumerate(ENTRIES[model]))


framed('s12', 'Count it', 'One line from each patch', f'''<div class="lists">
    {card('list-a', f'{mono("claude-haiku-4.5")} · the entry each of its five trials added', code(entry_list(MODELS[0]), 'text'))}
    {card('list-b', f'{mono("gpt-5.6-terra")} · the entry each of its five trials added', code(entry_list(MODELS[1], 'pr'), 'text'))}
  </div>''', [
    {"type": "focus", "target": "pr", "at": "2~made-up", "color": "yellow"},
    {"type": "focus", "target": "list-a", "at": "3", "color": "blue"}],
    css='.lists{display:flex;flex-direction:column;gap:30px;width:100%}'
        '.lists .card > .code.dark{font-size:32px;line-height:1.38;padding:14px 28px}.lists .card .who{font-size:30px}'
        '.lists{gap:22px}.lists .card{gap:10px}.stage{justify-content:flex-start}')

framed('s13', 'Count it', 'The tally, filled in', tally(True) + f'''
  <p class="note">from the ten patches of our run · {RUN}</p>''', [
    {"type": "focus", "target": "h-none", "at": "0~five with no number", "color": "blue"},
    {"type": "focus", "target": "t-made", "at": "0~five made up", "color": "yellow"},
    {"type": "focus", "target": "c-no", "at": "0~nothing", "color": "blue"}], css=TALLY_CSS)


def reply_lines():
    out = []
    for i, r in enumerate(REPLY['gpt-5.6-terra']):
        r = r.replace('#42', '⟦pr:#42⟧', 1)
        wrapped = textwrap.wrap(r, 64, break_long_words=False)
        first = f'⟦r0:{i}⟧' if i == 0 else str(i)
        out += [f'{first}  {wrapped[0]}'] + [f'   {w}' for w in wrapped[1:]]
    return '\n'.join(out)


framed('s14', 'Count it', 'The replies say it too', f'''<div class="annotated">
    {card('replies', f'{mono("results.jsonl")} · the {mono("output")} of each {mono("gpt-5.6-terra")} trial', code(reply_lines(), 'text'))}
    {callouts(('r0', 'trial 0’s final reply'))}
  </div>''', [
    {"type": "focus", "target": "r0", "at": "0~final replies", "color": "blue"},
    {"type": "focus", "target": "pr", "at": "2~made-up number", "color": "yellow"}],
    css='.card > .code.dark{font-size:33px;line-height:1.5;padding:22px 30px}.card .who{font-size:32px}.callout{font-size:32px}'
        '.callouts{margin-top:50px}.stage{justify-content:flex-start}')

# ---- Chapter: What the tally says ----------------------------------------------------------------
framed('s15', 'What the tally says', 'Counts replace an impression', f'''<div class="cols wide terms">
    {block("h", "structure", f"{MADE_UP[MODELS[0]]} of 5", mono(MODELS[0]))}
    {block("t", "attention", f"{MADE_UP[MODELS[1]]} of 5", mono(MODELS[1]))}
  </div>
  <p class="lead"><span data-concept="what" data-rep="note">trials that made up a pull request number, with the first-draft skill</span></p>''', [
    {"type": "focus", "target": "h", "at": "2", "color": "blue"},
    {"type": "focus", "target": "t", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "what", "at": "4~skill", "color": "blue"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.terms .semantic-block{min-height:300px;justify-content:center}.terms .title{font-size:110px;line-height:1.1}'
        '.terms .label{font-size:36px}.lead{font-size:40px}')

GRADER_Q = GRADER.replace('"notes add"', '⟦value:"notes add"⟧')
framed('s16', 'What the tally says', 'And every one passed', f'''<div class="cols pair">
    {card('g', 'The only grader', code(GRADER_Q, 'yaml'))}
    <div class="cases">
      {block("case1", "structure", "Entry, no number", "passes", words=True)}
      {block("case2", "structure", "Entry, made-up number", "passes", words=True)}
      {block("case3", "structure", "No entry: the agent asks instead", "fails", words=True)}
    </div>
  </div>''', [
    {"type": "focus", "target": "case2", "at": "0", "color": "green"},
    {"type": "focus", "target": "value", "at": "1~notes add", "color": "yellow"},
    {"type": "focus", "target": "case1", "at": "1~whether", "color": "green"},
    {"type": "focus", "target": "case3", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "case3", "at": "3", "color": "red"}],
    css='.pair{align-items:stretch}.cases{display:flex;flex-direction:column;gap:22px;justify-content:center}'
        '.cases .semantic-block{min-height:130px;justify-content:center}.cases .title{font-size:36px}.cases .label{font-size:30px}'
        '.card > .code.dark{font-size:32px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('PASS', 'every trial passed'),
    ('FLAKY', 'some passed, some failed'),
    ('FAIL', 'none passed'),
    ('ERROR', 'a trial didn’t finish: no verdict')], 1))
framed('s17', 'Recap', 'What are the four words?', f'''<div class="semantic-block" id="words" data-role="structure">
    <div class="title words">one stimulus, five trials</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#words", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "green"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "p3", "at": "3", "color": "red"},
    {"type": "focus", "target": "p4", "at": "4", "color": "blue"}], layout='layout-expand',
    css='#words{width:100%;padding:36px 40px 44px;gap:24px}'
        '#words .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#words .part{min-height:300px}#words .part .title{font-size:52px;line-height:1.2}'
        '#words .part .label{font-size:30px}')

scene('s18', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Read the runs before writing graders</h1>
  <p class="lead">What else goes wrong when the requests get messier?</p>
  <p class="note">Exercises are on the lesson page · Source: Anthropic, “Demystifying evals for AI agents” (2026)</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok')
