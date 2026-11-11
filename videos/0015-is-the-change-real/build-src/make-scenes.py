"""Generate lesson 15's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 4: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing here
sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/before-and-after.experiment.yaml   the experiment file (in the starter; identical in practice)
  src/state/SKILL.md, SKILL.before.md          the skill after and before this lesson's edit
  src/run/s14.log        the experiment's terminal output from this video's own paid run (tapes/s14.tape
                         tees it to /tmp/vl-l15/s14.log)
  src/run/s13.log        the dry run's output
  src/run/report-row.json   one row of the run's report.md
  src/run/earlier.json   counts from earlier videos' runs that s11, s19 and s20 quote
  src/run/RUN            the run's folder name
While src/run/PROVISIONAL exists these are stand-ins from verified/lesson-15 and the lesson pages.

The ranges are worked out here exactly as the course's calculator does (assets/range-calculator.js:
the 95% Wilson interval, rounded to a whole percent).

The asserts are what the narration says. `says(scene, i, phrase)` fails unless sentence i of that scene in
storyboard.json contains the phrase, so the numbers on screen and the numbers spoken cannot disagree. If the
video's own run differs, an assert fails: reword the outcome sentence it names, then run again.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, math, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
H, T = MODELS
SHORT = {H: 'haiku', T: 'terra'}
STIMULI = ('parser', 'cache', 'dates')
K = 3

SB = json.loads((D / 'storyboard.json').read_text())
NARR = {s['id']: [n if isinstance(n, str) else n['text'] for n in s['narration']] for s in SB['scenes']}


def says(sid, i, phrase):
    """The cue time 'i~phrase', after checking that sentence i of the scene really says the phrase."""
    assert phrase.lower() in NARR[sid][i].lower(), f'{sid} sentence {i} does not say "{phrase}": {NARR[sid][i]}'
    return f'{i}~{phrase.lower()}'


ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()


def w(n):
    """A whole number from 0 to 100, in words as the narration writes it."""
    if n < 20:
        return ONES[n]
    if n == 100:
        return 'one hundred'
    t, o = divmod(n, 10)
    return TENS[t - 2] + (f'-{ONES[o]}' if o else '')


def of(c):
    return f'{c[0]} of {c[1]}'


def wof(c):
    return f'{w(c[0])} of {w(c[1])}'


# ---- The calculator's arithmetic ------------------------------------------------------------------
def wilson(x, n):
    z = 1.96
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def pc(x):
    return int(math.floor(x * 100 + 0.5))   # JavaScript's Math.round


class R:
    """A count with its range, as the calculator shows it."""
    def __init__(self, c):
        self.x, self.n = c
        self.lo, self.hi = wilson(self.x, self.n)
        self.rate = self.x / self.n
        self.plo, self.phi, self.prate = pc(self.lo), pc(self.hi), pc(self.rate)
        self.out = f'{self.prate}%, range {self.plo}% to {self.phi}%'
        self.text = f'{self.plo}% to {self.phi}%'
        self.words = f'{w(self.plo)} to {w(self.phi)}'


def apart(b, a):
    return a.lo > b.hi or b.lo > a.hi


VERDICT = {True: 'The ranges do not overlap. This result supports a real change.',
           False: 'The ranges overlap. This result does not show a change.'}

# The lesson page's table, to prove this arithmetic is the calculator's.
for c, lo, hi in [((7, 10), 40, 89), ((9, 10), 60, 98), ((70, 100), 60, 78), ((90, 100), 83, 94),
                  ((3, 9), 12, 65), ((8, 9), 56, 98), ((7, 8), 53, 98), ((9, 9), 70, 100)]:   # the page prints 57 for 8 of 9; the calculator shows 56
    assert (R(c).plo, R(c).phi) == (lo, hi), (c, R(c).text)


# ---- HTML parts -----------------------------------------------------------------------------------
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


def quote(cid, who, text):
    return f'''<div class="quote" data-concept="{cid}" data-rep="quote"><span class="who">{who}</span><p>{text}</p></div>'''


def mono(t):
    return f'<span class="mono">{t}</span>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def lead(cid, text):
    return f'<p class="lead"><span data-concept="{cid}" data-rep="note">{text}</span></p>'


# A range on a 0 to 100% axis. Sizes and theme variables only.
BARS_CSS = ('.ranges{display:grid;grid-template-columns:max-content 1fr max-content;gap:14px 28px;align-items:center;width:100%}'
            '.ranges .rl{font:500 34px/1.2 var(--font-code);color:var(--ink);white-space:nowrap}'
            '.ranges .rt{font:400 32px/1.2 var(--font-body);color:var(--ink-soft);white-space:nowrap}'
            '.ranges .track{position:relative;height:46px;background:var(--paper-muted);border-radius:var(--radius)}'
            '.ranges .fill{position:absolute;top:0;bottom:0;border-radius:var(--radius)}'
            '.ranges .fill.before{background:var(--focus-blue)}.ranges .fill.after{background:var(--focus-yellow)}'
            '.ranges .at{position:absolute;top:7px;bottom:7px;width:6px;margin-left:-3px;border-radius:3px;background:var(--ink)}'
            '.ranges .axis{grid-column:2;display:flex;justify-content:space-between;font:400 26px/1 var(--font-body);color:var(--ink-muted)}'
            '.ranges .group{grid-column:1 / -1;font:600 28px/1.2 var(--font-body);color:var(--ink-soft);margin-top:10px}')


def bars(rows, axis=True):
    """rows: (concept id, label, R, 'before'|'after', text after the bar) or ('group', title)."""
    out = []
    for r in rows:
        if r[0] == 'group':
            out.append(f'<div class="group">{r[1]}</div>')
            continue
        cid, label, rng, tone, text = r
        out.append(f'''<div class="rl"><span data-concept="{cid}" data-rep="cell">{label}</span></div>
      <div class="track"><div class="fill {tone}" style="left:{rng.lo * 100:.1f}%;width:{(rng.hi - rng.lo) * 100:.1f}%"></div><div class="at" style="left:{rng.rate * 100:.1f}%"></div></div>
      <div class="rt">{text}</div>''')
    if axis:
        out.append('<div class="axis"><span>0%</span><span>50%</span><span>100%</span></div>')
    return '<div class="ranges">\n      ' + '\n      '.join(out) + '\n    </div>'


CALC_CSS = ('.calc{background:var(--paper-muted);border-radius:var(--radius);padding:26px 36px 30px;display:flex;flex-direction:column;gap:16px;min-width:0}'
            '.calc .who{font:600 26px/1.2 var(--font-body);letter-spacing:.03em;color:var(--ink-muted)}'
            '.calc .who .mono{font-family:var(--font-code);color:var(--ink)}'
            '.calc .crow{display:grid;grid-template-columns:150px 96px 44px 96px 1fr;gap:16px;align-items:center;font:400 34px/1.2 var(--font-body);color:var(--ink)}'
            '.calc .cl{font:600 26px/1.2 var(--font-body);letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft)}'
            '.calc .cb{font:500 36px/1 var(--font-code);background:var(--paper);border:2px solid var(--rule);border-radius:8px;padding:12px 0;text-align:center}'
            '.calc .co{font:500 34px/1.2 var(--font-code);white-space:nowrap}'
            '.calc .cv{font:400 34px/1.35 var(--font-body);color:var(--ink);margin:6px 0 0}')


def calc(cid, who, before, after, pre=''):
    """The course's range calculator, as its page shows it: two rows and its verdict, in its own words."""
    b, a = R(before), R(after)
    row = lambda label, c, r, key: (f'<div class="crow"><span class="cl">{label}</span><span class="cb">{c[0]}</span>'
                                    f'<span>of</span><span class="cb">{c[1]}</span>'
                                    f'<span class="co"><span data-concept="{pre}{key}" data-rep="cell">{r.out}</span></span></div>')
    return f'''<div class="calc" data-concept="{cid}" data-rep="card">
      <div class="who">{who}</div>
      {row('Before', before, b, 'cb')}
      {row('After', after, a, 'ca')}
      <p class="cv"><span data-concept="{pre}cv" data-rep="cell">{VERDICT[apart(b, a)]}</span></p>
    </div>'''


# ---- The run, read from src/run -------------------------------------------------------------------
RUN = (D / 'src/run/RUN').read_text().strip()
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
SRC = 'stand-in: the course’s verified run' if PROVISIONAL else f'our run · {RUN}'


def clean(text):
    """Terminal output as plain lines: control codes, carriage returns and backspaces removed."""
    text = re.sub(r'\x1b\[[0-9;?]*[ -/]*[@-~]', '', text)
    text = re.sub(r'\x1b[()][A-Z0-9]', '', text).replace('\r', '')
    text = re.sub(r'\^D\x08\x08', '', text).replace('\x08', '').replace('\x04', '')
    return [l.rstrip() for l in text.split('\n')]


LOG = clean((D / 'src/run/s14.log').read_text())
DRY = clean((D / 'src/run/s13.log').read_text())
assert any(re.fullmatch(r'Plans:\s+4', l.strip()) for l in DRY), 's13: the dry run should list four plans'

# Blocks: "<variant> · <model>" then "  FAIL|FLAKY|ERROR  <stimulus>  <counts>".
BLOCKS = []
for i, line in enumerate(LOG[:-1]):
    m = re.fullmatch(r'(\S+) · (\S+)', line.strip())
    n = re.fullmatch(r'\s+(PASS|FAIL|FLAKY|ERROR)\s+(\S+)\s+(.+)', LOG[i + 1])
    if m and n and not line.startswith(' '):
        state, stim, rest = n.groups()
        f = re.fullmatch(r'(\d+)/(\d+)', rest.strip())
        if f:
            passed, failed, errors = int(f.group(1)), int(f.group(2)) - int(f.group(1)), 0
        else:
            g = lambda word: int((re.search(rf'(\d+) {word}', rest) or [0, 0])[1])
            passed, failed, errors = g('passed'), g('failed'), g('error')
        assert passed + failed + errors == K, (line, LOG[i + 1])
        BLOCKS.append(dict(variant=m.group(1), model=m.group(2), state=state, stim=stim, passed=passed,
                           failed=failed, errors=errors, head=line.strip(), status=re.sub(r'\s+$', '', LOG[i + 1])))
assert all(b['stim'] in STIMULI for b in BLOCKS), BLOCKS

# The table of variants at the end.
ti = max(i for i, l in enumerate(LOG) if re.match(r'\s+eval\s{2,}', l))
cells = lambda l: re.split(r'\s{2,}', l.strip())
VARIANTS = [re.sub(r' \(baseline\)$', '', v) for v in cells(LOG[ti])[1:]]
assert VARIANTS == ['haiku-before', 'haiku-after', 'terra-before', 'terra-after'], VARIANTS
TABLE = {}
for l in LOG[ti + 1:ti + 8]:
    c = cells(l)
    if c and c[0] in ('wording', 'stimuli', 'tokens', 'trial time'):
        assert len(c) == 5, l
        TABLE[c[0]] = dict(zip(VARIANTS, c[1:]))
        TABLE[c[0] + ':line'] = l
assert set(('stimuli', 'tokens')) <= set(TABLE), list(TABLE)
STIM = {v: tuple(int(x) for x in re.fullmatch(r'(\d+)/(\d+)', TABLE['stimuli'][v]).groups()) for v in VARIANTS}
TOK = {v: float(re.fullmatch(r'([\d.]+)k', TABLE['tokens'][v]).group(1)) for v in VARIANTS}


def trials(variant):
    """(passed, finished, errors) over the variant's three stimuli; a stimulus with no block passed all."""
    mine = {b['stim']: b for b in BLOCKS if b['variant'] == variant}
    passed = sum(mine[s]['passed'] if s in mine else K for s in STIMULI)
    errors = sum(mine[s]['errors'] for s in mine)
    return passed, K * len(STIMULI) - errors, errors


TR = {v: trials(v) for v in VARIANTS}
CNT = {v: TR[v][:2] for v in VARIANTS}
# A stimulus counted as passed in the table passed all its finished trials.
for v in VARIANTS:
    whole = sum(1 for s in STIMULI if not any(b['variant'] == v and b['stim'] == s for b in BLOCKS))
    assert whole == STIM[v][0], (v, whole, STIM[v])
HB, HA, TB, TA = (CNT[v] for v in VARIANTS)
RHB, RHA, RTB, RTA = R(HB), R(HA), R(TB), R(TA)
H_APART, T_APART = apart(RHB, RHA), apart(RTB, RTA)

ROW = json.loads((D / 'src/run/report-row.json').read_text())
EARLIER = json.loads((D / 'src/run/earlier.json').read_text())

# ---- Chapter 1: What a small sample can show ------------------------------------------------------
EB1 = 'What a small sample can show'
framed('s01', 'Vally &amp; Agent Evals', 'Is the change real?', f'''<div class="cols wide terms">
    {block("before", "structure", "7 of 10", "trials passed, before the edit")}
    {block("after", "attention", "9 of 10", "trials passed, after the edit")}
  </div>
  {lead('four', 'The skill so far: four edits, each judged on a smaller count than these.')}''', [
    {"type": "focus", "target": "before", "at": says('s01', 0, 'seven of ten'), "color": "blue"},
    {"type": "focus", "target": "after", "at": says('s01', 0, 'nine of ten'), "color": "yellow"},
    {"type": "focus", "target": "none", "at": "1"},
    {"type": "focus", "target": "four", "at": says('s01', 2, 'four times'), "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.terms .semantic-block{min-height:250px;justify-content:center}'
        '.terms .title{font-size:104px;line-height:1.1}.terms .label{font-size:36px}.lead{font-size:40px;margin:0}.stage{gap:34px}')

r7, r9, r70, r90 = R((7, 10)), R((9, 10)), R((70, 100)), R((90, 100))
assert says('s02', 4, f'{w(r7.plo)} and {w(r7.phi)} percent')
framed('s02', EB1, 'A count is an estimate', f'''<div class="cols wide est">
    {block("count", "structure", "7 of 10", "70% of these trials passed")}
    <div class="right">
      {bars([('rng', 'the true pass rate', r7, 'before', r7.text)])}
      {lead('prob', '“Probably”: ranges worked out this way hold the true rate about 95 times in 100.')}
    </div>
  </div>''', [
    {"type": "focus", "target": "count", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "rng", "at": says('s02', 4, 'a range'), "color": "blue"},
    {"type": "focus", "target": "prob", "at": "5", "color": "yellow"}],
    css=BARS_CSS + '.est{align-items:center;grid-auto-columns:auto;grid-template-columns:520px 1fr}'
        '.est .semantic-block{min-height:300px;justify-content:center}.est .title{font-size:104px;line-height:1.1}'
        '.est .label{font-size:34px}.right{display:flex;flex-direction:column;gap:40px}.lead{font-size:36px;margin:0}'
        '.ranges .rl{font-family:var(--font-body);font-weight:400;font-size:32px}')

assert not apart(r7, r9) and apart(r70, r90)
assert says('s03', 1, f'{w(r7.plo)} to {w(r7.phi)}') and says('s03', 1, f'{w(r9.plo)} to {w(r9.phi)}')
framed('s03', EB1, 'Do the ranges overlap?', bars([
    ('group', '10 trials each'),
    ('a1', '7 of 10', r7, 'before', r7.text), ('a2', '9 of 10', r9, 'after', r9.text),
    ('group', '100 trials each'),
    ('b1', '70 of 100', r70, 'before', r70.text), ('b2', '90 of 100', r90, 'after', r90.text)]), [
    {"type": "focus", "target": "a1", "at": says('s03', 1, 'forty'), "color": "blue"},
    {"type": "focus", "target": "a2", "at": says('s03', 1, 'sixty'), "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "b1", "at": says('s03', 4, 'a hundred trials'), "color": "blue"},
    {"type": "focus", "target": "b2", "at": says('s03', 4, "don't touch"), "color": "yellow"}],
    css=BARS_CSS + '.ranges{gap:16px 32px}.ranges .track{height:54px}.ranges .rl{font-size:38px}.ranges .rt{font-size:36px}'
        '.ranges .group{font-size:30px}')

framed('s04', EB1, 'Three habits for small counts', f'''<div class="cols habits">
    {block("h1", "structure", "Like with like", "same stimuli, graders and model, in one sitting", words=True, step=1)}
    {block("h2", "transform", "Counts, not percentages", "100% is 3 of 3, or 300 of 300", words=True, step=2)}
    {block("h3", "attention", "“These trials cannot tell”", "when the ranges overlap", words=True, step=3)}
  </div>''', [
    {"type": "focus", "target": "h1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "h2", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "h3", "at": "3", "color": "yellow"}],
    css='.habits .semantic-block{min-height:360px}.habits .title{font-size:44px;line-height:1.2}.habits .label{font-size:34px}')

n10, n40, n160 = R((7, 10)), R((28, 40)), R((112, 160))
wd = lambda r: r.phi - r.plo
assert wd(n40) <= wd(n10) * 0.62 and wd(n160) <= wd(n40) * 0.62, (wd(n10), wd(n40), wd(n160))
framed('s05', EB1, 'Certainty costs trials', bars([
    ('group', 'the same 70% pass rate, with four times the trials each time'),
    ('t1', '7 of 10', n10, 'before', f'{n10.text} · {wd(n10)} points wide'),
    ('t2', '28 of 40', n40, 'before', f'{n40.text} · {wd(n40)} points wide'),
    ('t3', '112 of 160', n160, 'before', f'{n160.text} · {wd(n160)} points wide')]), [
    {"type": "focus", "target": "t1", "at": "0", "color": "blue"},
    {"type": "focus", "target": "t2", "at": says('s05', 0, 'four times'), "color": "blue"},
    {"type": "focus", "target": "t3", "at": says('s05', 0, 'halve'), "color": "blue"},
    {"type": "focus", "target": "none", "at": "1"}],
    css=BARS_CSS + '.ranges{gap:18px 32px}.ranges .track{height:54px}.ranges .rl{font-size:38px}.ranges .rt{font-size:34px}'
        '.ranges .group{font-size:30px}')

framed('s06', EB1, 'A calculator for the range', f'''{calc('calc', 'the range around a count', (7, 10), (9, 10))}
  <p class="note">On the course site · 95% Wilson interval · Source: Evan Miller, “Adding Error Bars to Evals” (2024)</p>''', [
    {"type": "focus", "target": "cb", "at": says('s06', 1, 'count before'), "color": "blue"},
    {"type": "focus", "target": "ca", "at": says('s06', 1, 'count after'), "color": "blue"},
    {"type": "focus", "target": "cv", "at": "2", "color": "yellow"}],
    css=CALC_CSS + '.calc{width:100%;padding:36px 48px 40px;gap:22px}.calc .crow{font-size:40px;grid-template-columns:190px 120px 50px 120px 1fr}'
        '.calc .cb{font-size:44px}.calc .co{font-size:40px}.calc .cv{font-size:40px}.calc .cl{font-size:30px}.calc .who{font-size:28px}.stage{gap:30px}')

# ---- Chapter 2: What the experiment prints --------------------------------------------------------
EB2 = 'What the experiment prints'
framed('s07', EB2, 'Two versions, two models', f'''<div class="annotated">
    {panel('exp')}
    {callouts(('eval', 'the judged eval · 3 requests'), ('runs', '3 trials of each stimulus'),
              ('before', 'the skill before our edit'), ('after', 'the skill we edit'))}
  </div>''', [
    {"type": "scroll", "target": "#exp", "to": "top", "at": "1"},
    {"type": "focus", "target": "eval", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#exp", "to": "8-13", "at": "3"},
    {"type": "focus", "target": "runs", "at": "3", "color": "yellow"},
    {"type": "scroll", "target": "#exp", "to": "14-22", "at": "4"},
    {"type": "focus", "target": "none", "at": "4"},
    {"type": "focus", "target": "before", "at": "5", "color": "blue"},
    {"type": "scroll", "target": "#exp", "to": "15-23", "at": "6"},
    {"type": "focus", "target": "after", "at": "6", "color": "yellow"}], layout='layout-file')

# s08: one block of each state our run has, cut to its first two lines.
sample = []
for state in ('FAIL', 'FLAKY', 'ERROR'):
    hit = next((b for b in BLOCKS if b['state'] == state), None)
    if hit:
        sample.append(hit)
assert len(sample) >= 2, 's08 shows blocks of at least two states; this run has ' + str([b['state'] for b in BLOCKS])
shape = []
for i, b in enumerate(sample):
    shape.append((f'⟦hd:{b["head"]}⟧' if i == 0 else b['head']) + '\n' +
                 (re.sub(r'^(\s+)(.*)$', r'\1⟦st:\2⟧', b['status']) if i == 0 else b['status']))
framed('s08', EB2, 'A block for every miss', f'''<div class="annotated">
    {code((chr(10) * 2).join(shape), 'yaml', 'out')}
    {callouts(('hd', 'variant · model'), ('st', 'state · stimulus · trials passed and failed'))}
  </div>
  {lead('noblock', 'A stimulus with no block passed every trial.')}
  <p class="note">the first two lines of each block · {SRC}</p>''', [
    {"type": "focus", "target": "hd", "at": says('s08', 0, 'headed'), "color": "blue"},
    {"type": "focus", "target": "none", "at": "1"},
    {"type": "focus", "target": "st", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "noblock", "at": "4", "color": "blue"}],
    css='.code.dark.out{font-size:34px;line-height:1.45;padding:24px 34px;min-width:1000px}.callout{font-size:32px}'
        '.lead{font-size:38px;margin:0}.stage{gap:26px}.note{margin:0}')

# s09: one row of report.md.
p, n = (int(x) for x in ROW['pass_rate'].split('/'))
assert n == K and 0 < p < n, ROW
assert ROW['pass_at_k'] == '100.0%' and ROW['pass_hat_k'] == f'{(p / n) ** K * 100:.1f}%', ROW
assert (p, n) == (2, 3), 's09 sentences 2, 5 and 7 say two of three passed, 100% and 29.6%: reword them for ' + ROW['pass_rate']
says('s09', 2, 'two of which passed'); says('s09', 7, 'two times in three'); says('s09', 7, 'just under thirty')
assert 29 <= (p / n) ** K * 100 < 30
cell = lambda cid, t: f'<span data-concept="{cid}" data-rep="cell">{t}</span>'
framed('s09', EB2, 'Three columns per stimulus', f'''<table class="data-table full rep">
    <thead><tr><th>Stimulus</th><th class="num">Pass Rate</th><th class="num">pass@k</th><th class="num">pass^k</th></tr></thead>
    <tbody>
      <tr><td class="mono">{ROW['stimulus']}</td><td class="num">{cell('rate', ROW['pass_rate'])}</td><td class="num">{cell('atk', ROW['pass_at_k'])}</td><td class="num">{cell('hatk', ROW['pass_hat_k'])}</td></tr>
      <tr class="what"><td></td><td class="num">passed, out of finished</td><td class="num">did at least one of k pass?</td><td class="num">would k in a row all pass? &nbsp;({p}/{n})³</td></tr>
    </tbody>
  </table>
  <p class="note">one row of {mono('report.md')}, in the experiment’s run folder · k = 3 trials · {SRC}</p>''', [
    {"type": "focus", "target": "rate", "at": "3", "color": "blue"},
    {"type": "focus", "target": "atk", "at": "4", "color": "blue"},
    {"type": "focus", "target": "hatk", "at": "6", "color": "yellow"}],
    css='.rep{font-size:48px}.rep th{font-size:36px;font-family:var(--font-code)}.rep td{padding-top:26px;padding-bottom:26px}'
        '.rep td.mono{font-family:var(--font-code)}.rep tr.what td{font:400 30px/1.3 var(--font-body);color:var(--ink-soft);border-bottom:0}'
        '.note .mono{font-family:var(--font-code)}.stage{gap:34px}')

hat = f'{(2 / 3) ** 3 * 100:.1f}%'
assert hat == '29.6%'
framed('s10', EB2, 'Which column to trust', f'''<div class="cols wide terms">
    {block("atk", "structure", "pass@k · 100%", "can the agent do this at all?")}
    {block("hatk", "attention", "pass^k · " + hat, "can I count on it every time?")}
  </div>
  <p class="note">a stimulus that passes 2 trials in 3</p>
  {lead('err', 'A trial that ends in ERROR: dashes in these columns.')}
  {lead('norange', 'None of the columns gives a range.')}''', [
    {"type": "focus", "target": "hatk", "at": says('s10', 1, 'pass hat k'), "color": "yellow"},
    {"type": "focus", "target": "atk", "at": says('s10', 1, 'pass at k'), "color": "blue"},
    {"type": "focus", "target": "err", "at": "2", "color": "blue"},
    {"type": "focus", "target": "norange", "at": "3", "color": "blue"}],
    css='.terms .semantic-block{min-height:230px;justify-content:center}.terms .title{font-size:64px;line-height:1.15}'
        '.terms .label{font-size:36px}.lead{font-size:38px;margin:0}.note{margin:0}.stage{gap:22px}')

# ---- Chapter 3: Compare before and after ----------------------------------------------------------
EB3 = 'Compare before and after'
assert EARLIER['judge_found_coding_details'], 's11 sentence 1 says the judge found entries that say how a fix was coded'
old = (D / 'src/state/SKILL.before.md').read_text().splitlines()
new = (D / 'src/state/SKILL.md').read_text().splitlines()
assert old[15] == '- One line per change, written for people who use the tool.'
assert new[15:18] == ['- One line per change, written for people who use the tool:',
                      '  say what they will notice. Do not say how it was coded.',
                      '  Name no library, algorithm, data structure or source file.']
assert old[:15] == new[:15] and old[16:] == new[18:], 'the edit is the second rule and nothing else'
framed('s11', EB3, 'One rule, sharpened', f'''<div class="annotated">
    {panel('skill')}
    {callouts(('old', 'the rule until now'), ('new1', 'added: what they will notice'), ('new2', 'added: what to leave out'))}
  </div>''', [
    {"type": "focus", "target": "old", "at": "2", "color": "blue"},
    {"type": "focus", "target": "new1", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "new2", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file')

COUNT_CSS = ('.counts{font-size:44px}.counts th{font-size:32px}.counts td{padding-top:26px;padding-bottom:26px}'
             '.counts td.mono{font-family:var(--font-code);font-size:38px;white-space:nowrap}'
             '.counts td.num{font-family:var(--font-code)}')


def counts_table(filled):
    v = lambda cid, c: cell(cid, of(c)) if filled else ''
    return f'''<table class="data-table full counts">
    <thead><tr><th>trials passed</th><th class="num">before the edit</th><th class="num">after the edit</th></tr></thead>
    <tbody>
      <tr><td class="mono">{H}</td><td class="num">{v('chb', HB)}</td><td class="num">{v('cha', HA)}</td></tr>
      <tr><td class="mono">{T}</td><td class="num">{v('ctb', TB)}</td><td class="num">{v('cta', TA)}</td></tr>
    </tbody>
  </table>'''


framed('s12', EB3, 'What will nine trials show?', f'''{counts_table(False)}
  {lead('nine', '3 stimuli × 3 trials = 9 trials for each variant')}''', [
    {"type": "focus", "target": "nine", "at": "0", "color": "blue"},
    {"type": "focus", "target": "none", "at": "1"}],
    css=COUNT_CSS + '.lead{font-size:40px;margin:0}.stage{gap:36px}.counts td{height:96px}')

# s14: what the table's stimuli row says, in the order the narration reads it.
says('s14', 3, f'{wof(STIM["haiku-before"])}, then {wof(STIM["haiku-after"])}, for haiku')
says('s14', 3, f'{wof(STIM["terra-before"])}, then {wof(STIM["terra-after"])}, for terra')
# s14 sentence 4: terra's zero stimuli before the edit is three stimuli that each lost a trial to ERROR.
tb_blocks = {b['stim']: b for b in BLOCKS if b['variant'] == 'terra-before'}
assert STIM['terra-before'][0] == 0 and set(tb_blocks) == set(STIMULI) and all(b['errors'] == 1 for b in tb_blocks.values()), tb_blocks
says('s14', 4, 'each of its stimuli lost a trial to an error')

# s15: every block, grouped by variant, and the trial counts they add up to.
grouped = []
for v, key in zip(VARIANTS, ('bhb', 'bha', 'btb', 'bta')):
    mine = [b for b in BLOCKS if b['variant'] == v]
    if mine:
        grouped.append(f'⟦{key}:{mine[0]["head"]}⟧\n' + '\n'.join(b['status'] for b in mine))
says('s15', 2, f'{wof(HB)} before'); says('s15', 2, f'{wof(HA)} after')
says('s15', 3, f'{wof(TB)} before'); says('s15', 3, f'{wof(TA)} after')
lost = TR['terra-before'][2]
assert lost == 3 and says('s15', 3, f'{w(lost)} trials lost to errors')
assert all(TR[v][2] == 0 for v in VARIANTS if v != 'terra-before'), 'an ERROR in a variant the narration does not mention: ' + str(TR)
err_note = ' · a trial that ended in ERROR is left out' if any(TR[v][2] for v in VARIANTS) else ''
framed('s15', EB3, 'Count trials, not stimuli', f'''<div class="cols wide tally">
    {code((chr(10) * 2).join(grouped), 'yaml', 'out')}
    <div class="right">
      {counts_table(True)}
      <p class="note">a stimulus with no block passed 3 of 3{err_note}</p>
    </div>
  </div>
  <p class="note">every block of the run, cut to its first lines · {SRC}</p>''', [
    {"type": "focus", "target": "chb", "at": says('s15', 2, wof(HB)), "color": "blue"},
    {"type": "focus", "target": "cha", "at": says('s15', 2, wof(HA) + ' after'), "color": "yellow"},
    {"type": "focus", "target": "ctb", "at": says('s15', 3, wof(TB)), "color": "blue"},
    {"type": "focus", "target": "cta", "at": says('s15', 3, wof(TA) + ' after'), "color": "yellow"}],
    css=COUNT_CSS + '.tally{align-items:start;grid-auto-columns:auto;grid-template-columns:880px minmax(0,1fr);gap:44px}'
        '.code.dark.out{font-size:30px;line-height:1.42;padding:22px 28px}.right{display:flex;flex-direction:column;gap:18px}'
        '.counts{font-size:38px}.counts th{font-size:25px}.counts td.mono{font-size:27px}.counts td{padding-top:20px;padding-bottom:20px}'
        '.note{margin:0}.stage{gap:22px}')

# s16: the calculator, once for each model.
says('s16', 1, RHB.words); says('s16', 1, RHA.words); says('s16', 3, RTB.words); says('s16', 3, RTA.words)
assert not H_APART and not T_APART, 's16 and s17 say both pairs of ranges overlap'
says('s16', 2, f'overlap, by {w(RHB.phi - RHA.plo)} points')
assert 'overlap' in NARR['s16'][3]
framed('s16', EB3, 'The range around each count', f'''<div class="cols twocalc">
    {calc('hc', mono(H), HB, HA, pre='h')}
    {calc('tc', mono(T), TB, TA, pre='t')}
  </div>
  <p class="note">the course’s calculator, with our counts · {SRC}</p>''', [
    {"type": "focus", "target": "hcb", "at": says('s16', 1, RHB.words), "color": "blue"},
    {"type": "focus", "target": "hca", "at": says('s16', 1, RHA.words), "color": "yellow"},
    {"type": "focus", "target": "hcv", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "tcb", "at": says('s16', 3, RTB.words), "color": "blue"},
    {"type": "focus", "target": "tca", "at": says('s16', 3, RTA.words), "color": "yellow"},
    {"type": "focus", "target": "tcv", "at": says('s16', 3, 'overlap too'), "color": "yellow"}],
    css=CALC_CSS + '.twocalc{gap:36px}.calc{padding:28px 30px 30px}.calc .crow{grid-template-columns:118px 66px 30px 66px 1fr;gap:12px;font-size:30px}'
        '.calc .cb{font-size:32px;padding:10px 0}.calc .co{font-size:29px}.calc .cl{font-size:22px}.calc .cv{font-size:30px}.note{margin:0}.stage{gap:26px}')


# s17: the sentence we wrote for each model, built from the counts so it cannot disagree with them.
def sentence(model, b, a, rb, ra):
    start = f'On {model} the new rule took the judge’s passes from {of(b)} to {of(a)}; '
    if apart(rb, ra):
        return start + 'the ranges do not overlap, so these trials support a real improvement.'
    if ra.rate - rb.rate >= 0.3:
        return start + 'the ranges overlap, so these trials cannot yet tell whether it is a real improvement.'
    return start + 'the ranges overlap, so these trials cannot tell whether the rule made any difference there.'


SH, ST_ = sentence(H, HB, HA, RHB, RHA), sentence(T, TB, TA, RTB, RTA)
says('s17', 1, f'from {wof(HB)} to {wof(HA)}'); says('s17', 1, "can't yet tell")
says('s17', 2, f'from {wof(TB)} to {wof(TA)}'); says('s17', 2, 'made any difference')
assert 'cannot yet tell' in SH and 'made any difference' in ST_, (SH, ST_)
framed('s17', EB3, 'One sentence per model', f'''{quote('qh', mono(H), '“' + SH + '”')}
  {quote('qt', mono(T), '“' + ST_ + '”')}''', [
    {"type": "focus", "target": "qh", "at": "1", "color": "blue"},
    {"type": "focus", "target": "qt", "at": "2", "color": "yellow"}],
    css='.quote{width:100%}.quote p{font-size:38px;line-height:1.4}.quote .who .mono{font-family:var(--font-code)}.stage{gap:30px}')

# ---- Chapter 4: The earlier fixes, re-examined ----------------------------------------------------
EB4 = 'The earlier fixes, re-examined'
hb_zero = sum(1 for b in BLOCKS if b['variant'] == 'haiku-before' and b['passed'] == 0)
ha_failed = sum(b['failed'] for b in BLOCKS if b['variant'] == 'haiku-after')
hb_fail = [b['failed'] for b in BLOCKS if b['variant'] == 'haiku-before']
assert sum(hb_fail) == 4 and max(hb_fail) == 3 and ha_failed == 0, f's18 sentences 1 and 2: haiku failed {hb_fail} before and {ha_failed} after'
says('s18', 1, 'four trials failed'); says('s18', 1, 'three of them on one request'); says('s18', 2, 'none failed'); says('s18', 3, 'overlap')
assert TB[1] - TB[0] == 1 and says('s18', 5, 'only one finished trial failed')
assert TB[0] >= TB[1] - 1, 's18 sentence 3 says terra had almost nothing left to fix: ' + of(TB)


def model_block(key, model, b, a, rb, ra):
    return f'''<div class="mb">
      <div class="who">{mono(model)}</div>
      {bars([(key + 'b', of(b), rb, 'before', rb.text), (key + 'a', of(a), ra, 'after', ra.text)])}
    </div>'''


framed('s18', EB4, 'What nine trials can show', f'''<div class="cols wide two">
    {model_block('h', H, HB, HA, RHB, RHA)}
    {model_block('t', T, TB, TA, RTB, RTA)}
  </div>
  <p class="note">trials passed before the edit (blue) and after it (yellow), with the range around each · {SRC}</p>''', [
    {"type": "focus", "target": "hb", "at": says('s18', 1, 'before the edit'), "color": "blue"},
    {"type": "focus", "target": "ha", "at": says('s18', 2, 'after the edit'), "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "tb", "at": "5", "color": "blue"},
    {"type": "focus", "target": "none", "at": "6"}],
    css=BARS_CSS + '.two{gap:56px}.mb{display:flex;flex-direction:column;gap:22px;min-width:0}'
        '.mb .who{font:500 32px/1.2 var(--font-body);color:var(--ink-soft)}.mb .who .mono{font-family:var(--font-code);color:var(--ink)}'
        '.ranges{gap:14px 16px}.ranges .rl{font-size:36px}.ranges .rt{font-size:29px}.ranges .track{height:54px}.ranges .axis{font-size:24px}'
        '.note{margin:0}.stage{gap:34px}')

LO, CO, MU = EARLIER['loading'], EARLIER['conversation'], EARLIER['made_up_number_terra']
pair = lambda e: (tuple(e['before']), tuple(e['after']))
for sid, i, e in (('s19', 1, CO), ('s20', 0, MU)):
    b, a = pair(e)
    says(sid, i, f'from {wof(b)} to {wof(a)}')
    assert not apart(R(b), R(a)), (sid, e)
assert CO['model'] == H and says('s19', 1, "haiku's conversation test")
# s19 sentence 2: before the description rewrite the loading test passed every trial that finished.
lb, la_ = pair(LO)
assert LO['model'] == T and lb[0] == lb[1] and not apart(R(lb), R(la_)), LO
says('s19', 2, f'all {w(lb[0])} trials that finished'); says('s19', 2, f'{wof(la_)} after')
ov = lambda e: 'overlap' if not apart(R(pair(e)[0]), R(pair(e)[1])) else 'apart'
erow = lambda key, fix, what, e: (f'<tr><td>{fix}</td><td class="mono">{what}</td><td class="num">{cell(key + "b", of(pair(e)[0]))}</td>'
                                  f'<td class="num">{cell(key + "a", of(pair(e)[1]))}</td><td>{cell(key + "o", ov(e))}</td></tr>')
framed('s19', EB4, 'Reasonable, but not measured', f'''<table class="data-table full fixes">
    <thead><tr><th>The fix</th><th>What it was for</th><th class="num">before</th><th class="num">after</th><th>ranges</th></tr></thead>
    <tbody>
      {erow('c', 'a rule for follow-ups', 'conversation · haiku', CO)}
      {erow('l', 'a rewritten description', 'loading · terra', LO)}
    </tbody>
  </table>
  <div class="cols why">
    {block("w1", "structure", "A patch showed the cause", "", words=True)}
    {block("w2", "structure", "The rule addressed that cause", "", words=True)}
    {block("w3", "structure", "The count moved the right way", "", words=True)}
  </div>''', [
    {"type": "focus", "target": "ca", "at": "1", "color": "blue"},
    {"type": "focus", "target": "la", "at": "2", "color": "blue"},
    {"type": "focus", "target": "lo", "at": says('s19', 3, 'ranges overlap'), "color": "yellow"},
    {"type": "focus", "target": "co", "at": says('s19', 3, 'both fixes'), "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"},
    {"type": "focus", "target": "w1", "at": says('s19', 5, 'a patch'), "color": "blue"},
    {"type": "focus", "target": "w2", "at": says('s19', 5, 'the rule addressed'), "color": "blue"},
    {"type": "focus", "target": "w3", "at": says('s19', 5, 'moved the right way'), "color": "blue"},
    {"type": "focus", "target": "none", "at": "6"}],
    css='.fixes{font-size:40px}.fixes th{font-size:30px}.fixes td{padding-top:22px;padding-bottom:22px}'
        '.fixes td.mono{font-family:var(--font-code);font-size:30px;white-space:nowrap}.fixes td.num{font-family:var(--font-code)}'
        '.why .semantic-block{min-height:0;padding:22px 28px}.why .title{font-size:34px;line-height:1.25}.why .label{display:none}.stage{gap:36px}')

mb, ma = pair(MU)
assert tuple(EARLIER['lesson3_terra_made_up']) == (5, 5) and says('s20', 1, 'five of five')
assert EARLIER['typo_fix_passed_in_every_later_run'], 's20 sentence 1: the same stimulus passing in every run since'
assert EARLIER['no_skill_run_made_up_a_number'] is False, 's20 sentence 2: the run with no skill showed the first draft caused it'
framed('s20', EB4, 'A result we can defend', f'''<div class="mb">
    <div class="who">{mono('no-made-up-number')} on {mono(T)} · before and after its fix</div>
    {bars([('mub', of(mb), R(mb), 'before', 'before · ' + R(mb).text), ('mua', of(ma), R(ma), 'after', 'after · ' + R(ma).text)])}
  </div>
  <div class="cols why">
    {block("e1", "structure", "5 of 5", "the same failure, before the fix")}
    {block("e2", "structure", "Every run since", "the same stimulus passes")}
    {block("e3", "structure", "No skill", "no made-up number: the first draft caused it", words=False)}
  </div>''', [
    {"type": "focus", "target": "mub", "at": says('s20', 0, wof(mb)), "color": "blue"},
    {"type": "focus", "target": "mua", "at": says('s20', 0, 'to ' + wof(ma)), "color": "yellow"},
    {"type": "focus", "target": "e1", "at": says('s20', 1, 'five of five'), "color": "blue"},
    {"type": "focus", "target": "e2", "at": says('s20', 1, 'the same stimulus'), "color": "blue"},
    {"type": "focus", "target": "e3", "at": "2", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css=BARS_CSS + '.mb{display:flex;flex-direction:column;gap:18px;width:100%}'
        '.mb .who{font:500 32px/1.2 var(--font-body);color:var(--ink-soft)}.mb .who .mono{font-family:var(--font-code);color:var(--ink)}'
        '.ranges .rl{font-size:36px}.ranges .rt{font-size:32px}.ranges .track{height:50px}'
        '.why .semantic-block{min-height:190px}.why .title{font-size:52px;line-height:1.15}.why .label{font-size:30px}.stage{gap:34px}')

framed('s21', EB4, 'First, trust the grader', f'''<div class="cols wide order">
    {block("g1", "attention", "Test the grader", "the oracle, then saved trials", words=True, step=1)}
    {block("g2", "structure", "Work out the range", "count trials, then the calculator", words=True, step=2)}
  </div>
  {lead('wrong', 'A range around a wrong grader’s count measures the wrong thing, carefully.')}''', [
    {"type": "focus", "target": "g1", "at": says('s21', 0, 'the grader'), "color": "yellow"},
    {"type": "focus", "target": "wrong", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "g1", "at": says('s21', 2, 'test the graders'), "color": "yellow"},
    {"type": "focus", "target": "g2", "at": says('s21', 2, 'only then'), "color": "blue"}],
    css='.order .semantic-block{min-height:300px}.order .title{font-size:52px;line-height:1.2}.order .label{font-size:36px}'
        '.lead{font-size:38px;margin:0}.stage{gap:34px}')

# s22: the table as printed, with its tokens row marked. Model gap against what the edit changed.
gap = abs((TOK['haiku-before'] + TOK['haiku-after']) - (TOK['terra-before'] + TOK['terra-after'])) / 2
edit = max(abs(TOK['haiku-after'] - TOK['haiku-before']), abs(TOK['terra-after'] - TOK['terra-before']))
assert gap > edit, f's22 sentence 2: the models differ by {gap:.1f}k on average, the edit changed one by {edit:.1f}k'
tab = [LOG[ti]] + [TABLE[k + ':line'] for k in ('wording', 'stimuli')] + \
      ['⟦tok:' + TABLE['tokens:line'].strip() + '⟧'] + ([TABLE['trial time:line']] if 'trial time:line' in TABLE else [])
tab = [re.sub(r'^  ', '', l) for l in tab]
err_tok = lead('errtok', 'A variant that lost a trial to ERROR did less work, so its total is lower.') if any(TR[v][2] for v in VARIANTS) else ''
framed('s22', EB4, 'Tokens, in the same table', f'''{code(chr(10).join(tab), 'yaml', 'tab')}
  {lead('agent', 'The agent’s tokens, added up over all of a variant’s trials.')}
  {lead('judge', 'The judge’s tokens are not included.')}
  {err_tok}
  <p class="note">the end of the experiment’s output · {SRC}</p>''', [
    {"type": "focus", "target": "tok", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "agent", "at": says('s22', 1, "agent's tokens"), "color": "blue"},
    {"type": "focus", "target": "judge", "at": says('s22', 1, "judge's"), "color": "blue"},
    {"type": "focus", "target": "tok", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.code.dark.tab{font-size:29px;line-height:1.5;padding:22px 30px;width:100%;white-space:pre}.lead{font-size:36px;margin:0}'
        '.note{margin:0}.stage{gap:20px}')

# ---- Recap and next -------------------------------------------------------------------------------
parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="step">{i}</div><div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Like with like', 'one experiment, before and after'),
    ('Count trials', 'not stimuli or percentages'),
    ('Find each range', 'the calculator'),
    ('Say what it supports', 'overlap: these trials cannot tell')], 1))
framed('s23', 'Recap', 'Is a better count real?', f'''<div class="semantic-block" id="steps" data-role="structure">
    <div class="title words">before believing a count</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#steps", "at": "2"},
    {"type": "focus", "target": "p1", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "3", "color": "cyan"},
    {"type": "focus", "target": "p3", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "p4", "at": "5", "color": "orange"}], layout='layout-expand',
    css='#steps{width:100%;padding:36px 40px 44px;gap:24px}'
        '#steps .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#steps .part{min-height:300px}#steps .part .title{font-size:46px;line-height:1.2}'
        '#steps .part .label{font-size:30px}')

scene('s24', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">What a passing trial costs</h1>
  <p class="lead">The same table printed tokens for each variant.</p>
  <p class="note">Exercises are on the lesson page · Source: Evan Miller, “Adding Error Bars to Evals” (2024)</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', 'PROVISIONAL run' if PROVISIONAL else RUN,
      '| trials', {v: of(CNT[v]) for v in VARIANTS}, '| blocks', len(BLOCKS))
