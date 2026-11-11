"""Generate lesson 12's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and output in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/skill.md                       the skill as the practice folder has it when this lesson starts
  src/state/*.wording.eval.yaml      the eval file before and after the judge (file panels)
  src/run/                           the run this video's s12 recorded and s19 judged:
      RUN                            the run folder's name
      <stimulus>-<model>-<n>.patch   the twelve saved patches
      results.jsonl                  the run's records (gives the order vally grade printed its blocks in)
      s12.log, s18.log, s19.log      what vally eval, vally lint and vally grade printed
      labels.tsv                     OUR yes/no for each entry, with a few words why (written by us, after reading)
  While src/run/PROVISIONAL exists these are stand-ins from verified/lesson-12.

It also writes src/state/wording-labels.md: the notes file the lesson has the reader keep (ours and the
judge's answers), for the practice folder; lesson 13 reads it.

Every count the narration states is asserted below. If a recording changes them, this fails, and the
sentence changes before the scene does.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
SHORT = {'claude-haiku-4.5': 'haiku', 'gpt-5.6-terra': 'terra'}
STIMULI = ('parser', 'cache', 'dates')
RUNDIR = D / 'src/run'


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


def wrap(text, width, first='', rest='', spans=()):
    """Wrap text at spaces. spans = [(start, end, id)] character ranges to mark as ⟦id:…⟧, line by line."""
    lines, start = [], 0
    while start < len(text):
        room = width - len(first if not lines else rest)
        end = len(text) if len(text) - start <= room else text.rfind(' ', start, start + room + 1)
        if end <= start:
            end = min(len(text), start + room)
        lines.append((start, end))
        start = end + 1 if end < len(text) and text[end] == ' ' else end
    out = []
    for i, (a, b) in enumerate(lines):
        seg, pos = '', a
        for s, e, cid in sorted(spans):
            s2, e2 = max(s, a), min(e, b)
            if s2 < e2:
                seg += text[pos:s2] + f'⟦{cid}:{text[s2:e2]}⟧'
                pos = e2
        out.append((first if i == 0 else rest) + seg + text[pos:b])
    return '\n'.join(out)


# ---- The real things, read from src/ -------------------------------------------------------------
PROVISIONAL = (RUNDIR / 'PROVISIONAL').exists()
RUN = (RUNDIR / 'RUN').read_text().strip()
PR = re.compile(r'\s*\(#\d+\)\s*$')
TRIALS = [(s, m, i) for s in STIMULI for m in MODELS for i in (0, 1)]


def added_entry(key):
    """The changelog entry a trial added: the one '+- ' line of its saved patch, verbatim."""
    path = RUNDIR / '{}-{}-{}.patch'.format(*key)
    lines = [l[3:] for l in path.read_text().splitlines() if l.startswith('+- ')]
    assert len(lines) == 1, f'{path.name}: expected one added entry, found {lines}'
    return lines[0]


ENTRY = {k: added_entry(k) for k in TRIALS}

OURS, WHY = {}, {}
for line in (RUNDIR / 'labels.tsv').read_text().splitlines():
    if line.strip() and not line.startswith('#'):
        s, m, i, ours, why = line.split('\t')
        assert ours in ('yes', 'no'), line
        OURS[s, m, int(i)], WHY[s, m, int(i)] = ours, why
assert set(OURS) == set(TRIALS), 'labels.tsv must have one row for each of the twelve trials'

# vally grade's blocks, in the order printed. The order of trials is the order of results.jsonl,
# which is what vally grade read; without that file (provisional) it is model, stimulus, trial.
rj = RUNDIR / 'results.jsonl'
if rj.exists():
    recs = [json.loads(l) for l in rj.read_text().splitlines() if l.strip()]
    recs = [r for r in recs if r.get('type') == 'trial-result']
    assert all(r['status'] == 'success' for r in recs), 'a trial ended in ERROR: rerun the take'
    ORDER = [(r['stimulus'], r['model'], r['trialIndex']) for r in recs]
else:
    assert PROVISIONAL, 'src/run/results.jsonl is missing'
    ORDER = [(s, m, i) for m in MODELS for s in sorted(STIMULI) for i in (0, 1)]
assert sorted(ORDER) == sorted(TRIALS), ORDER

log = (RUNDIR / 's19.log').read_text().replace('\r', '')
BLOCKS = []
for chunk in re.split(r'(?m)^━━━ ', log)[1:]:
    lines = chunk.rstrip().split('\n')
    stim = lines[0].replace('━', '').strip()
    j = next(i for i, l in enumerate(lines) if re.match(r'\s+\S+\s+\[prompt', l))
    k = next(i for i in range(j + 1, len(lines)) if re.match(r'\s+[✓✗⚠]\S*\s+\[', lines[i]) or lines[i].startswith('Score:'))
    judge = ' '.join(l.strip() for l in lines[j:k])
    m = re.match(r'(\S+) (\[prompt [^\]]*\]) (.*)$', judge)
    assert m and m.group(1) in '✓✗', f'unexpected judge line: {judge}'
    BLOCKS.append(dict(stim=stim, summary=lines[1], mark=m.group(1), tag=m.group(2), reason=m.group(3),
                       others=[l.strip() for l in lines[k:] if re.match(r'\s+[✓✗⚠]', l)],
                       score=next(l for l in lines if l.startswith('Score:'))))
assert len(BLOCKS) == 12, f'{len(BLOCKS)} judged blocks in s19.log'
norm = lambda t: t.replace('\\', '')
JUDGE, BLOCK_OF = {}, {}
for b, key in zip(BLOCKS, ORDER):
    assert b['stim'] == key[0], (b['stim'], key)
    b['key'], b['quoted'] = key, norm(ENTRY[key]) in norm(b['reason'])
    quoted_other = [k for k in TRIALS if k[0] == key[0] and norm(ENTRY[k]) in norm(b['reason'])]
    assert b['quoted'] or not quoted_other, f'block order does not match the trials: {key} quotes {quoted_other}'
    JUDGE[key], BLOCK_OF[key] = ('yes' if b['mark'] == '✓' else 'no'), b

count = lambda d, v, f=lambda k: True: sum(1 for k in TRIALS if f(k) and d[k] == v)
has = lambda key, *words: all(w.lower() in ENTRY[key].lower() for w in words)
H, T_ = MODELS

# ---- What the narration says about this run. If a recording changes these, the sentences change too.
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')
plain = lambda name: ANSI.sub('', (RUNDIR / name).read_text().replace('\r', ''))
s12log = plain('s12.log')
assert all(re.search(r'✓\s+' + re.escape(m), s12log) for m in MODELS), 's12: a tick for each model'
s18log = plain('s18.log')
assert '1 warning' in s18log and 'scoring' in s18log and 'error' not in s18log.lower(), 's18: one warning, no errors'
# s01, s13: the first patch we open names the streaming parser
assert has(('parser', H, 0), 'out-of-memory', 'by using', 'streaming') and OURS['parser', H, 0] == 'no'
# s14: haiku names the streaming parser in one of its two parser entries; the other three only give the benefit
assert has(('parser', H, 0), 'streaming') and OURS['parser', H, 0] == 'no'
assert all(has(k, 'memory', 'import') and not has(k, 'streaming') and OURS[k] == 'yes'
           for k in [('parser', H, 1), ('parser', T_, 0), ('parser', T_, 1)])
# s15
assert all(has(('cache', H, i), 'LRU') and OURS['cache', H, i] == 'no' for i in (0, 1))
assert all(has(('cache', T_, i), 'Speed up', 'by caching the tag index') and OURS['cache', T_, i] == 'no'
           and WHY['cache', T_, i].startswith('hesitated') for i in (0, 1))
# s16
assert all(has(('dates', m, i), 'single-digit months and days') and not has(('dates', m, i), 'tokenizer')
           and OURS['dates', m, i] == 'yes' for m in MODELS for i in (0, 1))
assert count(OURS, 'yes') == 7 and count(OURS, 'no') == 5
# s20, s21, s22, s23
assert sum(b['quoted'] for b in BLOCKS) == 11, 's20: eleven of the twelve reasons quote their entry'
assert count(JUDGE, 'yes') == 8 and count(JUDGE, 'no') == 4
NO_BY = {m: count(JUDGE, 'no', lambda k, m=m: k[1] == m) for m in MODELS}
assert NO_BY == {H: 3, T_: 1}, NO_BY
assert [k for k in TRIALS if JUDGE[k] == 'no'] == [('parser', H, 0), ('cache', H, 0), ('cache', H, 1), ('cache', T_, 0)]
DISAGREE = [k for k in TRIALS if JUDGE[k] != OURS[k]]
assert DISAGREE == [('cache', T_, 1)] and OURS['cache', T_, 1] == 'no'       # s21: eleven match, one doesn't
# s23: the two terra cache entries differ by one word, and the judge split them
assert ENTRY['cache', T_, 1] == ENTRY['cache', T_, 0].replace('large folders', 'large note folders') != ENTRY['cache', T_, 0]

# Hand-over for lesson 13's video (format given in its src/run/PROVISIONAL): one row per trial.
tsv = ['\t'.join(['stimulus', 'model', 'trial', 'entry', 'ours', 'judge', 'our_reason', 'judge_reason'])]
tsv += ['\t'.join([s, m, str(i), PR.sub('', ENTRY[s, m, i]), OURS[s, m, i], JUDGE[s, m, i], WHY[s, m, i],
                   BLOCK_OF[s, m, i]['reason']]) for s, m, i in TRIALS]
(RUNDIR / 'trials.tsv').write_text('\n'.join(tsv) + '\n')

# The notes file the lesson has us keep: ours and the judge's answers, for the practice folder.
rows = ['# Wording labels', '',
        'Does the entry say what changes for people who use the tool, without saying how it was coded?', '',
        '| Stimulus, model, trial | Entry | Ours | Judge |', '|---|---|---|---|']
rows += [f'| {s}, {SHORT[m]}, {i} | {PR.sub("", ENTRY[s, m, i])} | {OURS[s, m, i]} | {JUDGE[s, m, i]} |' for s, m, i in TRIALS]
(D / 'src/state/wording-labels.md').write_text('\n'.join(rows) + '\n')
(RUNDIR / 'wording-labels.md').write_text('\n'.join(rows) + '\n')

# ---- Hook ----------------------------------------------------------------------------------------
skill = (D / 'src/skill.md').read_text().splitlines()
RULE = next(l for l in skill if 'written for people who use the tool' in l)
assert RULE == '- One line per change, written for people who use the tool.'
rule_marked = RULE.replace('written for people who use the tool', '⟦rule:written for people who use the tool⟧')

HOOK = ENTRY['parser', H, 0]
hm = re.search(r'streaming (\w+ )?parser', HOOK)
assert hm


def entry_box(cid='how'):
    return wrap(HOOK, 62, spans=[(hm.start(), hm.end(), cid)])


framed('s01', 'Vally &amp; Agent Evals', 'What code cannot check', f'''<div class="results">
      {card('card-a', f'the skill · {mono("changelog-entry")}', code(rule_marked, 'markdown'))}
      {card('card-b', f'one entry from our run · {mono(H)}', code(entry_box(), 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "rule", "at": "0~written", "color": "blue"},
    {"type": "focus", "target": "how", "at": "1~entry", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}'
        '.results{display:flex;flex-direction:column;gap:40px;width:100%}'
        '.results .card > .code.dark{font-size:38px;padding:28px 36px}.results .card .who{font-size:34px}')

# ---- Chapter: When a judge fits ------------------------------------------------------------------
CH1 = 'When a judge fits'
framed('s02', CH1, 'Not a pattern', f'''<div class="cols wide terms">
    {block("see", "structure", "Code can see", "a pattern in the diff · an empty diff · a script’s check · which skills loaded", words=True)}
    {block("cant", "attention", "Code can’t decide", "does this entry say how the fix was coded?", words=True)}
  </div>
  {code(entry_box(), 'markdown', 'entry')}''', [
    {"type": "focus", "target": "see", "at": "1", "color": "blue"},
    {"type": "focus", "target": "cant", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "how", "at": "4~streaming", "color": "yellow"},
    {"type": "focus", "target": "cant", "at": "5", "color": "yellow"}],
    css='.terms .semantic-block{min-height:250px}.terms .label{font-size:34px}'
        '.code.dark.entry{font-size:34px;padding:24px 32px;width:100%;box-sizing:border-box}.stage{gap:36px}')

costs = [('slow', 'slower than code', ''),
         ('call', 'a model call per trial', ''),
         ('wrong', 'wrong in new ways', 'swayed by confident wording')]
framed('s03', CH1, 'A model as the grader', f'''<div class="def">
    {block("judge", "structure", "LLM judge", "a grader that asks a language model to read what the agent did, and decide whether it meets a criterion you wrote", words=True)}
  </div>
  <div class="cols wide costs">
    {''.join(block(c, 'attention', t, l, words=True) for c, t, l in costs)}
  </div>''', [
    {"type": "focus", "target": "judge", "at": "0", "color": "blue"},
    {"type": "focus", "target": "slow", "at": "3~slower", "color": "yellow"},
    {"type": "focus", "target": "call", "at": "3~every trial", "color": "yellow"},
    {"type": "focus", "target": "wrong", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "judge", "at": "5", "color": "blue"}],
    css='.def{width:100%}.def .semantic-block{width:100%;box-sizing:border-box}.def .label{font-size:36px}'
        '.costs .semantic-block{min-height:190px}.costs .title{font-size:38px}.costs .label{font-size:30px}.stage{gap:30px}')

HABITS = [('h1', 'One question per judge', 'so a no has one cause'),
          ('h2', 'Yes or no', 'a clear criterion, not a score'),
          ('h3', 'Our own answers first', 'each answer is a label')]
habits = '<div class="cols wide habits">' + ''.join(
    block(c, 'structure', t, l, words=True, step=i) for i, (c, t, l) in enumerate(HABITS, 1)) + '</div>'
HABIT_CSS = '.habits .semantic-block{min-height:340px}.habits .title{font-size:44px}.habits .label{font-size:32px}'
framed('s04', CH1, 'Three habits for a judge', habits, [
    {"type": "focus", "target": "h1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "h2", "at": "3", "color": "blue"}], css=HABIT_CSS)
framed('s04b', CH1, 'Three habits for a judge', habits, [
    {"type": "focus", "target": "h3", "at": "0", "color": "blue"}], css=HABIT_CSS)

# ---- Chapter: How the judge decides --------------------------------------------------------------
CH2 = 'How the judge decides'
framed('s05', CH2, 'Three additions make a judge', panel('spec'), [
    {"type": "focus", "target": "judge", "at": "3~judge model", "color": "blue"}], layout='layout-file')
framed('s06', CH2, 'One criterion, in plain words', panel('spec'), [
    {"type": "scroll", "target": "#spec", "to": "15-23", "at": "0"},
    {"type": "focus", "target": "request", "at": "0~request", "color": "blue"},
    {"type": "focus", "target": "rubric", "at": "1~rubric", "color": "yellow"}], layout='layout-file')
framed('s07', CH2, 'The judge is a grader', panel('spec'), [
    {"type": "scroll", "target": "#spec", "to": "15-23", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#spec", "to": "24-32", "at": "0+0.6"},
    {"type": "focus", "target": "ptype", "at": "0~type prompt", "color": "yellow"},
    {"type": "focus", "target": "binary", "at": "3", "color": "blue"},
    {"type": "focus", "target": "instr", "at": "4", "color": "blue"},
    {"type": "focus", "target": "cites", "at": "6", "color": "blue"}], layout='layout-file')

STEPS = [('g1', 'The judge model is given', 'the request · the rubric · what the agent said and did'),
         ('g2', 'It returns', 'a verdict and a reason'),
         ('g3', 'Vally records', 'the verdict as pass or fail · the reason as evidence')]
framed('s08', CH2, 'A verdict and a reason', '<div class="cols wide habits">' + ''.join(
    block(c, 'structure', t, l, words=True, step=i) for i, (c, t, l) in enumerate(STEPS, 1)) + '</div>', [
    {"type": "focus", "target": "g1", "at": "0", "color": "blue"},
    {"type": "focus", "target": "g2", "at": "1", "color": "blue"},
    {"type": "focus", "target": "g3", "at": "2", "color": "blue"},
    {"type": "focus", "target": "g2", "at": "3", "color": "blue"}], css=HABIT_CSS)

# One judged block as vally grade printed it: a cache trial the judge failed, whose reason quotes the entry.
B9 = next(b for b in BLOCKS if b['key'] == ('cache', H, 1))
assert B9['mark'] == '✗' and B9['quoted'] and 'leaks implementation detail' in B9['reason']
assert B9['others'] and all(o.startswith('✓') for o in B9['others']) and B9['score'].endswith('FAILED')
other = B9['others'][0]
om = re.match(r'(\S+ \[[^\]]+\])( .*)$', other)
block9 = '\n'.join([
    f'⟦hd:━━━ {B9["stim"]} ━━━⟧',
    f'⟦sum:{B9["summary"]}⟧',
    f'  ⟦jl:{B9["mark"]} {B9["tag"]}⟧',
    wrap(B9['reason'], 58, first='    ', rest='    '),
    wrap(om.group(2).strip(), 58, first=f'  ⟦cl:{om.group(1)}⟧ ', rest='    '),
    '',
    f'⟦sc:{B9["score"]}⟧'])
framed('s09', CH2, 'What a judged trial prints', f'''<div class="annotated">
    {code(block9, 'text', 'out')}
    {callouts(('hd', 'the stimulus'), ('jl', 'the judge: a cross, then its reason'),
              ('cl', 'the pattern grader'), ('sc', 'every grader must pass'))}
  </div>''', [
    {"type": "focus", "target": "hd", "at": "1", "color": "blue"},
    {"type": "focus", "target": "jl", "at": "2~prompt", "color": "yellow"},
    {"type": "focus", "target": "cl", "at": "4", "color": "green"},
    {"type": "focus", "target": "sc", "at": "5", "color": "red"}],
    css='.code.dark.out{font-size:32px;line-height:1.45;padding:24px 30px}.callout{font-size:32px}')

cmd = '\n'.join(['⟦grade:vally grade⟧ \\',
                 '  ⟦e:-e ../../../evals/wording.eval.yaml⟧ \\',
                 '  ⟦rd:--run-dir .⟧ \\',
                 '  ⟦vb:--verbose⟧ \\',
                 '  ⟦in:< results.jsonl⟧'])
framed('s10', CH2, 'Judge the trials you saved', f'''<div class="annotated">
    {code(cmd, 'bash', 'cmd')}
    {callouts(('grade', 'grades a saved run · no agent'), ('e', 'the eval file’s current graders'),
              ('rd', 'the run folder we’re in'), ('vb', 'print each grader’s evidence'), ('in', 'the saved trials'))}
  </div>''', [
    {"type": "focus", "target": "grade", "at": "0~vally grade", "color": "blue"},
    {"type": "focus", "target": "rd", "at": "1~run dir", "color": "blue"},
    {"type": "focus", "target": "in", "at": "1~results", "color": "blue"},
    {"type": "focus", "target": "vb", "at": "2~verbose", "color": "yellow"},
    {"type": "focus", "target": "e", "at": "3~rubric", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.code.dark.cmd{font-size:36px;line-height:1.75;padding:30px 36px}.callout{font-size:32px}')

# ---- Chapter: Our answers first ------------------------------------------------------------------
CH3 = 'Our answers first'
framed('s11', CH3, 'Three requests in coding terms', panel('ship'), [
    {"type": "focus", "target": "p1", "at": "2~streaming", "color": "yellow"},
    {"type": "scroll", "target": "#ship", "to": "26-31", "at": "3"},
    {"type": "focus", "target": "p2", "at": "3~tag index", "color": "yellow"},
    {"type": "scroll", "target": "#ship", "to": "38-43", "at": "4"},
    {"type": "focus", "target": "p3", "at": "4~tokenizer", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file')


def entries_scene(sid, stim, headline, cues, note=''):
    text, notes = [], []
    for m in MODELS:
        for i in (0, 1):
            cid = f'{SHORT[m][0]}{i}'
            text.append(wrap(ENTRY[stim, m, i], 59, first=f'⟦{cid}:{SHORT[m]} {i}⟧  ', rest=' ' * 9))
            notes.append((cid, f'<strong>{OURS[stim, m, i]}</strong> · {WHY[stim, m, i]}'))
    framed(sid, CH3, headline, f'''<div class="annotated">
    {card('entries', f'{mono(stim)} · the entry each trial added', code(chr(10).join(text), 'text', 'list'))}
    {callouts(*notes)}
  </div>{note}''', cues,
        css='.card > .code.dark.list{font-size:32px;line-height:1.5;padding:22px 28px}.card .who{font-size:32px}'
            '.callout{font-size:30px}.callouts{margin-top:52px}.stage{justify-content:flex-start;gap:24px}')


entries_scene('s14', 'parser', 'Four entries about the parser', [
    {"type": "focus", "target": "h0", "at": "3", "color": "red"},
    {"type": "focus", "target": "h1", "at": "4", "color": "green"},
    {"type": "focus", "target": "t0", "at": "4~both", "color": "green"},
    {"type": "focus", "target": "t1", "at": "4~large imports", "color": "green"}])
entries_scene('s15', 'cache', 'Four about the cache', [
    {"type": "focus", "target": "h0", "at": "0", "color": "red"},
    {"type": "focus", "target": "h1", "at": "0~outright", "color": "red"},
    {"type": "focus", "target": "t0", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "t1", "at": "1~by caching", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}])
entries_scene('s16', 'dates', 'Four about the dates', [
    {"type": "focus", "target": "h0", "at": "0", "color": "green"},
    {"type": "focus", "target": "h1", "at": "0~single-digit", "color": "green"},
    {"type": "focus", "target": "t0", "at": "0~none", "color": "green"},
    {"type": "focus", "target": "t1", "at": "1", "color": "green"},
    {"type": "focus", "target": "file", "at": "3~notes file", "color": "blue"}],
    note=f'\n  <p class="note"><span data-concept="file" data-rep="note">our twelve answers are saved in {mono("notes/wording-labels.md")}</span></p>')

# ---- Chapter: Add the judge and run it -----------------------------------------------------------
CH4 = 'Add the judge and run it'
framed('s17', CH4, 'The judge goes in', panel('added'), [
    {"type": "focus", "target": "judge", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#added", "to": "21-28", "at": "2"},
    {"type": "focus", "target": "add1", "at": "2+0.3", "color": "yellow"},
    {"type": "scroll", "target": "#added", "to": "40-47", "at": "2+2.6"},
    {"type": "focus", "target": "add2", "at": "2+2.9", "color": "yellow"},
    {"type": "scroll", "target": "#added", "to": "59-66", "at": "2+5.2"},
    {"type": "focus", "target": "add3", "at": "2+5.5", "color": "yellow"}], layout='layout-file')


def reason_card(cid, b, spans):
    s, m, i = b['key']
    line = f'{b["mark"]} {b["tag"]} {b["reason"]}'
    marked = [(line.index(text), line.index(text) + len(text), qid) for qid, text in spans]
    return card(cid, f'{mono(s)} · {mono(m)} · trial {i}', code(wrap(line, 80, rest='  ', spans=marked), 'text', 'why'))


B20_YES = BLOCK_OF['parser', T_, 1]
B20_NO = BLOCK_OF['parser', H, 0]
assert B20_YES['mark'] == '✓' and B20_YES['quoted'] and 'user-focused and does not describe the implementation' in B20_YES['reason']
assert B20_NO['mark'] == '✗' and not B20_NO['quoted'] and 'does state the user benefit' in B20_NO['reason']
framed('s20', CH4, 'Reading the judge’s reasons', f'''<div class="results">
      {reason_card('r-yes', B20_YES, [('q1', norm(ENTRY[B20_YES['key']]))])}
      {reason_card('r-no', B20_NO, [('x2', B20_NO['mark'] + ' ' + B20_NO['tag']), ('q2', 'streaming parser, importer.js')])}
  </div>''', [
    {"type": "focus", "target": "q1", "at": "1", "color": "green"},
    {"type": "focus", "target": "x2", "at": "2", "color": "red"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "q2", "at": "4~streaming", "color": "yellow"}],
    css='.results{display:flex;flex-direction:column;gap:30px;width:100%}'
        '.results .card > .code.dark.why{font-size:32px;line-height:1.5;padding:22px 28px}.results .card .who{font-size:30px}'
        '.stage{justify-content:flex-start}')

pair = lambda d, s, m: f'{d[s, m, 0]} · {d[s, m, 1]}'
trs = ''.join(f'''<tr><td class="mono">{s} · {m}</td>
        <td><span data-concept="o-{s}-{SHORT[m]}" data-rep="cell">{pair(OURS, s, m)}</span></td>
        <td><span data-concept="j-{s}-{SHORT[m]}" data-rep="cell">{pair(JUDGE, s, m)}</span></td></tr>
''' for s in STIMULI for m in MODELS)
framed('s21', CH4, 'The judge’s twelve verdicts', f'''<table class="data-table full verdicts">
    <thead><tr><th>stimulus · model</th><th><span data-concept="ours" data-rep="head">Ours · trials 0, 1</span></th>
      <th><span data-concept="judge" data-rep="head">Judge · trials 0, 1</span></th></tr></thead>
    <tbody>
{trs}    </tbody>
  </table>
  <p class="note">from {mono("notes/wording-labels.md")} · our run · {RUN}</p>''', [
    {"type": "focus", "target": "ours", "at": "0~our own", "color": "blue"},
    {"type": "focus", "target": "judge", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "j-cache-terra", "at": "2~one", "color": "yellow"}],
    css='.verdicts{font-size:36px}.verdicts th{font-size:30px}.verdicts td{padding-top:15px;padding-bottom:15px}'
        '.verdicts td.mono{font-family:var(--font-code);font-size:32px}.stage{gap:20px}')

# ---- Chapter: What the judge found ---------------------------------------------------------------
CH5 = 'What the judge found'
framed('s22', CH5, 'One rule, followed unevenly', f'''<div class="cols wide terms">
    {block("h", "attention", f"{NO_BY[H]} of 6", mono(H))}
    {block("t", "structure", f"{NO_BY[T_]} of 6", mono(T_))}
  </div>
  <p class="lead"><span data-concept="what" data-rep="note">entries the judge said no to: they say how the change was coded</span></p>''', [
    {"type": "focus", "target": "h", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "t", "at": "3", "color": "blue"},
    {"type": "focus", "target": "what", "at": "4~unevenly", "color": "blue"}],
    css='.terms .semantic-block{min-height:300px;justify-content:center}.terms .title{font-size:110px;line-height:1.1}'
        '.terms .label{font-size:36px}.lead{font-size:40px}')

framed('s23', CH5, 'A reason isn’t evidence', f'''<div class="cols wide terms">
    {block("code", "structure", "Every grader before", "code · tested with the oracle and against saved trials", words=True)}
    {block("opinion", "attention", "This judge", "a model’s opinion · not yet tested", words=True)}
  </div>''', [
    {"type": "focus", "target": "code", "at": "1", "color": "blue"},
    {"type": "focus", "target": "opinion", "at": "2", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (_, t, l) in enumerate(HABITS, 1))
framed('s24', 'Recap', 'What are the three habits?', f'''<div class="semantic-block" id="habits" data-role="structure">
    <div class="title words">a judge whose verdicts we can use</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#habits", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p3", "at": "3", "color": "blue"}], layout='layout-expand',
    css='#habits{width:100%;padding:36px 40px 44px;gap:24px}'
        '#habits .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#habits .part{min-height:300px}#habits .part .title{font-size:46px;line-height:1.2}'
        '#habits .part .label{font-size:30px}')

scene('s25', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Check the judge against your labels</h1>
  <p class="lead">The judge is a model. Is it right?</p>
  <p class="note">Exercises are on the lesson page · Source: Hamel Husain, “Using LLM-as-a-Judge”</p>
</main>''', [], css='.scene-title.chapter{font-size:100px}')
print('ok' + (' (src/run is PROVISIONAL)' if PROVISIONAL else ''))
