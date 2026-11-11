"""Generate lesson 16's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 4: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/cost.experiment.yaml     the experiment file the lesson adds (verified/lesson-16); the
                                     tapes copy it into practice/evals/ out of sight
  src/earlier-haiku45.json           the claude-haiku-4.5 trial of the lesson 1 video's run (real)
  src/run/                           THIS VIDEO'S RUN, recorded by tapes s15 and s18:
    <variant>/results.jsonl            the four variants' results files, copied from
                                       practice/results/lesson-16/<run>/<variant>/results.jsonl
    RUN                                the run folder's name
    s15.log, s18.log                   what vally printed in those two tapes (/tmp/vl-l16/*.log)
    record.json                        written BY THIS SCRIPT from haiku-low/results.jsonl (its first
                                       typo-fix trial, spread out, /Users/Shared/demo shown as ~/src/demo)
  While src/run/PROVISIONAL exists there are no results.jsonl files: the figures come from
  src/run/summary.provisional.json and the logs and record.json are stand-ins (see PROVISIONAL).

The asserts below are what the narration says about the run. If the video's own run differs, an
assert fails: reword the outcome sentences in storyboard.json, then change the assert.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, math, pathlib, re, statistics, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
VARIANTS = ('haiku-low', 'haiku-high', 'terra-low', 'terra-high')
HL, HH, TL, TH = VARIANTS
H45, H55, TERRA = 'claude-haiku-4.5', 'claude-haiku-5.5', 'gpt-5.6-terra'
NANO = 1e9


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


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def clean(text):
    """Terminal output as text: colour codes and carriage returns removed."""
    return re.sub(r'\x1b\[[0-9;?]*[A-Za-z]|\r', '', text)


# The calculator's own formatting (assets/cost-calculator.js).
aiu = lambda x: f'{x:.2f} AIU'
usd = lambda x: '$' + (f'{x:.3f}' if x < 1 else f'{x:.2f}')
ktok = lambda x: f'{x / 1000:.1f}k'


def wilson(k, n, z=1.96):
    """The range the course's range calculator gives for k passes in n trials, in whole percent."""
    p = k / n
    mid, half = (p + z * z / (2 * n)), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return round(100 * (mid - half) / (1 + z * z / n)), round(100 * min(1, (mid + half) / (1 + z * z / n)))


# ---- This video's run, read from src/run/ --------------------------------------------------------
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
have = [(D / f'src/run/{v}/results.jsonl').exists() for v in VARIANTS]
REAL = all(have)
assert REAL or not any(have), 'src/run/ needs all four <variant>/results.jsonl, or none'
assert REAL != PROVISIONAL, ('delete src/run/PROVISIONAL once the four results.jsonl are in place'
                             if REAL else 'no results.jsonl and no PROVISIONAL marker')


def read_variant(v):
    """The calculator's sums for one variant's results.jsonl, plus the cheapest and dearest trial."""
    g = dict(trials=0, passed=0, errors=0, with_cost=0, costs=[], tokens=[], outs=[], model=None, first=None)
    for line in (D / f'src/run/{v}/results.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get('type') != 'trial-result':
            continue
        assert r.get('variant') == v, (v, r.get('variant'))
        g['model'] = r['model']
        g['trials'] += 1
        g['errors'] += r['status'] != 'success'
        g['passed'] += (r.get('gradeResult') or {}).get('passed') is True
        u = ((r.get('trajectory') or {}).get('metrics') or {}).get('tokenUsage')
        if u:
            if isinstance(u.get('totalTokens'), (int, float)):
                g['tokens'].append(u['totalTokens'])
                g['outs'].append(u.get('outputTokens', 0))
            c = u.get('cost')
            if c and c.get('unit') == 'nano-aiu':
                g['costs'].append(c['amount'] / NANO)
                g['with_cost'] += 1
        if g['first'] is None and r.get('stimulus') == 'typo-fix' and r.get('trialIndex', 0) == 0:
            g['first'] = r
    return dict(model=g['model'], trials=g['trials'], passed=g['passed'], errors=g['errors'],
                with_cost=g['with_cost'], aiu=sum(g['costs']), min=min(g['costs']), max=max(g['costs']),
                med_out=statistics.median(g['outs']), med_tokens=statistics.median(g['tokens']), first=g['first'])


if REAL:
    V = {v: read_variant(v) for v in VARIANTS}
    RUN = (D / 'src/run/RUN').read_text().strip()
    rec = V[HL]['first']
    assert rec, 'no typo-fix trial 0 in haiku-low/results.jsonl'
    (D / 'src/run/record.json').write_text(
        json.dumps(rec, indent=2).replace('/Users/Shared/demo', '~/src/demo') + '\n')
else:
    prov = json.loads((D / 'src/run/summary.provisional.json').read_text())
    V, RUN = prov['variants'], prov['run']
SRC = 'stand-in: the course’s verified run' if PROVISIONAL else f'our run · {RUN}'
for v in VARIANTS:
    V[v]['per'] = V[v]['aiu'] / V[v]['passed'] if V[v]['passed'] else None
TOTAL = sum(V[v]['aiu'] for v in VARIANTS)
TRIALS = sum(V[v]['trials'] for v in VARIANTS)
assert V[HL]['model'] == V[HH]['model'] == H55 and V[TL]['model'] == V[TH]['model'] == TERRA

# The record shown in s07 and s08, and where its lines are (the panel shows real line numbers).
rec_text = (D / 'src/run/record.json').read_text()
REC = json.loads(rec_text)
rl = rec_text.splitlines()
find = lambda pat, start=0: next(i for i in range(start, len(rl)) if re.match(pat, rl[i])) + 1   # 1-based
L = dict(V=find(r'  "variant":'), ST=find(r'  "status":'), P=find(r'    "passed":'))
m = find(r'    "metrics": \{')
L['B'] = find(r'\s+"byModel": \{', m)
L['C'] = find(r'\s+"cost": \{', L['B'])
L['A'] = find(r'\s+"amount":', L['C'])
L['E'] = L['A'] + 1
assert L['V'] < L['ST'] < L['P'] < L['B'] < L['C'] and L['A'] == L['C'] + 3 and L['P'] - L['V'] <= 14, L
(D / 'build-src/record-lines.env').write_text(''.join(f'{k}={n}\n' for k, n in L.items()))
ru = REC['trajectory']['metrics']['tokenUsage']
REC_AIU, REC_TOK = ru['cost']['amount'] / NANO, ru['totalTokens']
assert REC['variant'] == HL and REC['model'] == H55 and REC['status'] == 'success' and REC['gradeResult']['passed'] is True
assert list(ru['byModel']) == [H55] and ru['cost']['unit'] == 'nano-aiu'

# What vally printed (s15: the efforts check; s18: the experiment).
log15 = re.sub(r'\s+', ' ', clean((D / 'src/run/s15.log').read_text()))
EFFORTS = {}
for mdl in (H45, H55, TERRA):
    got = re.search(r'Model "%s" does not support reasoning_effort "list"\. Supported reasoning efforts: ([a-z, ]+)\.' % re.escape(mdl), log15)
    if got:
        EFFORTS[mdl] = [e.strip() for e in got.group(1).split(',')]
    else:
        assert f'Model "{mdl}" does not support reasoning effort configuration' in log15, mdl
        EFFORTS[mdl] = None
log18 = clean((D / 'src/run/s18.log').read_text())
trow = lambda name: re.search(r'^\s*%s\s+(.*)$' % name, log18, re.M).group(1).split()
T_STIM, T_TOK = trow('stimuli'), trow('tokens')
T_TIME = re.search(r'^\s*trial time\s+(.*)$', log18, re.M).group(1).split()
assert len(T_STIM) == len(T_TOK) == len(T_TIME) == 4, (T_STIM, T_TOK, T_TIME)
ktoval = lambda s: float(s.rstrip('k'))

EARLIER = json.loads((D / 'src/earlier-haiku45.json').read_text())
# The average cost of a trial in the videos' own earlier runs on claude-haiku-4.5 and gpt-5.6-terra (s25).
AVG = json.loads((D / 'src/earlier-average.json').read_text())
AVG_AIU = AVG['aiu'] / AVG['trials']
EDIT_CENTS = round(AVG_AIU * 10)                  # ten trials, 1 AIU = 1 cent
NIGHT_AIU = AVG_AIU * 30                          # thirty trials
NIGHTS_USD = round(NIGHT_AIU * 30 / 100)          # thirty nights
OLD_PER100K = EARLIER['nano'] / NANO / EARLIER['totalTokens'] * 1e5
NEW_PER100K = REC_AIU / REC_TOK * 1e5

# ---- Spoken numbers --------------------------------------------------------------------------------
# A number the voice says is checked against the figure the screen shows, so the two cannot drift:
# spoken(0.2179) is "point two two", spoken(2.437) is "two point four", words(11) is "eleven".
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()
words = lambda n: ONES[n] if n < 20 else TENS[n // 10 - 2] + ('-' + ONES[n % 10] if n % 10 else '')
spoken = lambda x: ('point ' + ' '.join(ONES[int(d)] for d in f'{x:.2f}'[2:]) if x < 1 else
                    words(int(f'{x:.1f}'.split('.')[0])) + ' point ' + ONES[int(f'{x:.1f}'[-1])])
SB = {s['id']: [n if isinstance(n, str) else n['text'] for n in s['narration']]
      for s in json.loads((D / 'storyboard.json').read_text())['scenes']}


def says(sid, i, phrase):
    assert phrase in SB[sid][i], f'{sid} sentence {i} should say "{phrase}": {SB[sid][i]}'


# ---- What the narration says about this run ------------------------------------------------------
# s01, s21: terra's typical trial used far fewer tokens than haiku's, roughly half.
for t in (TL, TH):
    for h in (HL, HH):
        assert 0.4 < V[t]['med_tokens'] / V[h]['med_tokens'] < 0.65, (t, h)
# s08: the record cost about a quarter of a cent, for a hundred and five thousand tokens.
assert REC_AIU < 0.25 and round(REC_TOK / 1000) == 105, (REC_AIU, REC_TOK)
says('s08', 3, spoken(REC_AIU) + ' AIU')
# s16: 4.5 takes no effort; 5.5 takes five values, low to max; terra the same five and none.
FIVE = ['low', 'medium', 'high', 'xhigh', 'max']
assert EFFORTS[H45] is None and EFFORTS[H55] == FIVE and EFFORTS[TERRA] == ['none'] + FIVE, EFFORTS
# s18: every variant passed five of five stimuli; no variant beat the baseline; terra's tokens are lowest.
assert T_STIM == ['5/5'] * 4 and 'No variant beat baseline' in log18, T_STIM
assert max(ktoval(T_TOK[2]), ktoval(T_TOK[3])) < min(ktoval(T_TOK[0]), ktoval(T_TOK[1])), T_TOK
assert 'ERROR' not in log18
# s19, s25: sixty trials in four files came to about 89 AIU, 89 cents.
assert TRIALS == 60, TRIALS
says('s19', 2, words(round(TOTAL)) + ' AIU')
says('s19', 2, words(round(TOTAL)) + ' cents')
says('s25', 1, words(round(TOTAL)) + ' cents')
# s25: the same five stimuli on haiku-low alone would cost about one AIU.
says('s25', 4, 'about ' + words(round(5 * V[HL]['per'])) + ' AIU')
says('s25', 3, spoken(AVG_AIU) + ' AIU')
says('s25', 3, words(EDIT_CENTS) + ' cents')
says('s25', 5, words(NIGHTS_USD) + ' dollars')
assert EDIT_CENTS * 20 == 480   # s25 says four dollars eighty
# s20, s21: all four passed 15 of 15; haiku-low about a fifth of an AIU a pass; haiku-high a little more;
# both terra variants about thirteen times as much; haiku-low beats the other three on both counts.
for v in VARIANTS:
    assert V[v]['passed'] == V[v]['trials'] == V[v]['with_cost'] == 15 and V[v]['errors'] == 0, (v, V[v])
says('s20', 2, spoken(V[HL]['per']) + ' AIU')
assert 1.02 < V[HH]['per'] / V[HL]['per'] < 1.5
for t in (TL, TH):
    says('s20', 4, words(round(V[t]['per'] / V[HL]['per'])))
for v in (HH, TL, TH):
    assert V[v]['per'] > V[HL]['per'] and V[v]['passed'] <= V[HL]['passed']
# s22: the first haiku 4.5 trial cost about two and a half AIU per 100,000 tokens, this record about a fifth;
# about eleven times cheaper per token.
says('s22', 1, spoken(OLD_PER100K) + ' AIU')
says('s22', 2, spoken(NEW_PER100K) + ' AIU')
says('s22', 3, words(round(OLD_PER100K / NEW_PER100K)) + ' times')
# s23: 15 of 15 is a range of 80% to 100%; each model's trials varied about threefold; the bands are apart.
RANGE = wilson(15, 15)
assert RANGE == (80, 100), RANGE
H_MIN, H_MAX = min(V[HL]['min'], V[HH]['min']), max(V[HL]['max'], V[HH]['max'])
T_MIN, T_MAX = min(V[TL]['min'], V[TH]['min']), max(V[TL]['max'], V[TH]['max'])
assert 2 < H_MAX / H_MIN < 3 and 2 < T_MAX / T_MIN < 3 and H_MAX < T_MIN, (H_MIN, H_MAX, T_MIN, T_MAX)

exp = (D / 'src/state/cost.experiment.yaml').read_text().splitlines()
assert exp[3].strip() == '- changelog.eval.yaml' and exp[10].strip() == 'runs: 3' and exp[15].strip() == f'model: {H55}'

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'What a passing trial costs', f'''<div class="cols wide big">
    {block("terra", "structure", ktok(V[TL]['med_tokens']), f"tokens in a typical trial · {mono(TERRA)}")}
    {block("haiku", "structure", ktok(V[HL]['med_tokens']), f"tokens in a typical trial · {mono(H55)}")}
  </div>
  <p class="lead"><span data-concept="q" data-rep="note">Which one costs more?</span></p>
  <p class="note">the median trial at low effort · {SRC}</p>''', [
    {"type": "focus", "target": "terra", "at": "1~terra", "color": "blue"},
    {"type": "focus", "target": "haiku", "at": "1~haiku", "color": "blue"},
    {"type": "focus", "target": "q", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:112px}.big .semantic-block{min-height:250px;justify-content:center}'
        '.big .title{font-size:104px;line-height:1.1}.big .label{font-size:34px}.lead{font-size:44px;margin:0}'
        '.stage{gap:28px}.note{margin:0}')

# ---- Chapter: Cost per passing trial -------------------------------------------------------------
EB1 = 'Cost per passing trial'
framed('s02', EB1, 'Divide by the passes', f'''{block("def", "structure", "cost per passing trial", "What one useful result costs you.")}
  <div class="formula">
    {block("total", "attention", "Total cost", "every trial of the variant", words=True)}
    <div class="op">÷</div>
    {block("passes", "attention", "Trials that passed", "only those", words=True)}
  </div>''', [
    {"type": "focus", "target": "total", "at": "1~total cost", "color": "yellow"},
    {"type": "focus", "target": "passes", "at": "1~divided", "color": "yellow"},
    {"type": "focus", "target": "def", "at": "2", "color": "blue"}],
    css='.stage{gap:34px}.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:38px}'
        '.formula{display:grid;grid-template-columns:1fr auto 1fr;gap:32px;align-items:center;width:100%}'
        '.formula .semantic-block{min-height:210px}.formula .title{font-size:46px}.formula .label{font-size:34px}'
        '.formula .op{font-family:var(--font-code);font-size:96px;color:var(--ink);line-height:1}')

framed('s03', EB1, 'The cheaper trial costs more', f'''<table class="data-table full ab">
    <thead><tr><th>Variant</th><th>A trial costs</th><th>Trials passed</th><th>Total</th><th>Per passing trial</th></tr></thead>
    <tbody>
      <tr><td class="v">A</td><td>{cell('a_cost', '2 AIU')}</td><td>{cell('a_pass', '5 of 10')}</td><td>{cell('a_tot', '20 AIU')}</td><td>{cell('a_per', '4 AIU')}</td></tr>
      <tr><td class="v">B</td><td>{cell('b_cost', '3 AIU')}</td><td>{cell('b_pass', '10 of 10')}</td><td>{cell('b_tot', '30 AIU')}</td><td>{cell('b_per', '3 AIU')}</td></tr>
    </tbody>
  </table>
  <p class="note">a made-up example · 1 AIU = 1 cent</p>''', [
    {"type": "focus", "target": "a_cost", "at": "0~two AIU", "color": "blue"},
    {"type": "focus", "target": "a_pass", "at": "0~passes", "color": "blue"},
    {"type": "focus", "target": "b_cost", "at": "1", "color": "blue"},
    {"type": "focus", "target": "b_pass", "at": "1~passes", "color": "blue"},
    {"type": "focus", "target": "a_tot", "at": "2", "color": "blue"},
    {"type": "focus", "target": "a_per", "at": "2~four", "color": "yellow"},
    {"type": "focus", "target": "b_tot", "at": "3", "color": "blue"},
    {"type": "focus", "target": "b_per", "at": "3~three", "color": "yellow"},
    {"type": "focus", "target": "a_cost", "at": "4~cheaper", "color": "blue"},
    {"type": "focus", "target": "a_per", "at": "4~expensive", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.ab{font-size:44px}.ab th{font-size:30px}.ab td{padding-top:34px;padding-bottom:34px;font-family:var(--font-code)}'
        '.ab td.v{font-family:var(--font-body);font-weight:600}.stage{gap:26px}')

framed('s04', EB1, 'Beaten on both counts', f'''<div class="cols wide terms">
    {block("beaten", "structure", "Beaten on both counts", "costs more, and passes no more often: it can be dropped", words=True)}
    {block("choice", "attention", "A real choice", "costs more, and passes more often: it depends on what a failure costs you", words=True)}
  </div>''', [
    {"type": "focus", "target": "beaten", "at": "1", "color": "blue"},
    {"type": "focus", "target": "choice", "at": "3", "color": "yellow"}],
    css='.terms .semantic-block{min-height:300px}.terms .title{font-size:46px}.terms .label{font-size:36px;line-height:1.35}')

framed('s05', EB1, 'Report cost beside accuracy', f'''<div class="cols wide terms">
    {block("rank", "structure", "Agent rankings", "built on accuracy alone", words=True)}
    {block("retry", "attention", "Simple agents that tried again", "the same accuracy, at a fraction of the cost", words=True)}
  </div>
  {quote('argue', 'The researchers’ argument', 'Every evaluation should report cost beside accuracy.')}
  <p class="note">Source: Kapoor et al., “AI Agents That Matter” (2024), a preprint</p>''', [
    {"type": "focus", "target": "argue", "at": "0~argued", "color": "blue"},
    {"type": "focus", "target": "retry", "at": "1~simple agents", "color": "yellow"},
    {"type": "focus", "target": "rank", "at": "1~rankings", "color": "blue"}],
    css='.terms .semantic-block{min-height:210px}.terms .title{font-size:42px}.terms .label{font-size:34px}'
        '.stage{gap:28px}.quote{width:100%}.quote p{font-size:40px}')

# ---- Chapter: Where cost is recorded -------------------------------------------------------------
EB2 = 'Where cost is recorded'
tree = (f'results/lesson-16/{RUN}/\n'
        '  ⟦var:haiku-low/⟧results.jsonl\n'
        '  haiku-high/⟦rec:results.jsonl⟧\n'
        '  terra-low/results.jsonl\n'
        '  terra-high/results.jsonl')
framed('s06', EB2, 'One results file per variant', f'''<div class="annotated">
    {code(tree, 'text', 'tree')}
    {callouts(('var', 'a folder for each variant'), ('rec', 'one record per trial'))}
  </div>
  <p class="note">what an experiment saves · {SRC}</p>''', [
    {"type": "focus", "target": "var", "at": "1~folder", "color": "blue"},
    {"type": "focus", "target": "rec", "at": "2", "color": "yellow"}],
    css='.code.dark.tree{font-size:38px;line-height:1.6;padding:28px 36px;min-width:900px}.callout{font-size:32px}'
        '.stage{gap:24px}.note{margin:0}')

REC_CALLOUTS_TOP = callouts(('variant', 'the variant’s name'), ('status', 'did the trial finish?'),
                            ('passed', 'the verdict'))
framed('s07', EB2, 'Did the trial pass?', f'''<div class="annotated">
    {panel('record')}
    {REC_CALLOUTS_TOP}
  </div>''', [
    {"type": "scroll", "target": "#record", "to": "top", "at": "0"},
    {"type": "focus", "target": "variant", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#record", "to": f"{L['ST']}-{L['P']}", "at": "2"},
    {"type": "focus", "target": "status", "at": "2~finished", "color": "blue"},
    {"type": "focus", "target": "passed", "at": "3", "color": "yellow"}], layout='layout-file')

cents = REC_AIU   # 1 AIU is 1 cent
framed('s08', EB2, 'What the trial cost', f'''<div class="annotated">
    {panel('record')}
    {callouts(('bymodel', 'tokens, split by model'), ('unit', 'billionths of an AIU'), ('amount', 'this trial'))}
  </div>
  <p class="note sum"><span data-concept="sum" data-rep="note">{ru['cost']['amount']:,} nano-AIU = {REC_AIU:.2f} AIU = {cents:.2f} of a cent · {REC_TOK:,} tokens</span></p>''', [
    {"type": "scroll", "target": "#record", "to": f"{L['B']}-{L['B'] + 6}", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "bymodel", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#record", "to": f"{L['C'] - 2}-{L['E']}", "at": "2"},
    {"type": "focus", "target": "unit", "at": "2~nano", "color": "blue"},
    {"type": "focus", "target": "amount", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "sum", "at": "3~quarter", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], layout='layout-file',
    css='.note.sum{font-family:var(--font-code);font-size:30px;margin:0;color:var(--ink)}')

framed('s09', EB2, 'What the figure leaves out', f'''<div class="cols wide terms">
    {block("judge", "attention", "Judge calls", "not counted: an eval with a judge costs more than this", words=True)}
    {block("error", "structure", "A trial that ended in ERROR", "may have no usage recorded at all", words=True)}
  </div>''', [
    {"type": "focus", "target": "judge", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "error", "at": "2", "color": "blue"}],
    css='.terms .semantic-block{min-height:280px}.terms .title{font-size:46px}.terms .label{font-size:36px;line-height:1.35}')

steps = [('c1', 'structure', 'Add', 'every trial’s cost'), ('c2', 'transform', 'Count', 'the trials that passed'),
         ('c3', 'attention', 'Divide', 'cost per passing trial')]
framed('s10', EB2, 'Vally prints no total cost', f'''<div class="cols wide terms">
    {block("table", "structure", "The experiment’s table", "total tokens", words=True)}
    {block("report", "structure", mono("report.md"), "median tokens", words=True)}
  </div>
  {quote('calc', 'The course’s cost calculator', f'A page that reads the {mono("results.jsonl")} files you pick, in your browser.')}
  <div class="cols">
    {''.join(block(c, r, t, l, step=i) for i, (c, r, t, l) in enumerate(steps, 1))}
  </div>''', [
    {"type": "focus", "target": "table", "at": "1~table", "color": "blue"},
    {"type": "focus", "target": "report", "at": "1~report", "color": "blue"},
    {"type": "focus", "target": "calc", "at": "2", "color": "blue"},
    {"type": "focus", "target": "c1", "at": "3~adds", "color": "blue"},
    {"type": "focus", "target": "c2", "at": "3~counts", "color": "cyan"},
    {"type": "focus", "target": "c3", "at": "3~divides", "color": "yellow"}],
    css='.terms .semantic-block{min-height:130px;padding-top:18px;padding-bottom:18px}.terms .title{font-size:38px}'
        '.terms .label{font-size:32px}.stage{gap:22px}.quote{width:100%;padding-top:12px;padding-bottom:14px}'
        '.quote p{font-size:34px}.quote .mono,.terms .mono{font-family:var(--font-code)}'
        '.cols .semantic-block{min-height:170px}')

# ---- Chapter: Reasoning effort as a variant ------------------------------------------------------
EB3 = 'Reasoning effort as a variant'
framed('s11', EB3, 'Reasoning effort', f'''{block("def", "structure", "reasoning_effort", "How much hidden reasoning the agent’s model does before it replies or calls a tool.")}
  <div class="cols wide terms">
    {block("more", "attention", "More effort usually means", "more tokens, and more time on each call", words=True)}
    {block("better", "structure", "Sometimes", "better results", words=True)}
  </div>''', [
    {"type": "focus", "target": "def", "at": "2", "color": "blue"},
    {"type": "focus", "target": "more", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "better", "at": "3~sometimes", "color": "blue"}],
    css='.stage{gap:30px}.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:38px}'
        '.terms .semantic-block{min-height:200px}.terms .title{font-size:40px}.terms .label{font-size:36px}')

defaults = f'defaults:\n  ⟦model:model: {H55}⟧\n  ⟦effort:reasoning_effort: low⟧'
framed('s12', EB3, 'Set beside the model', f'''<div class="annotated">
    {code(defaults, 'yaml', 'defs')}
    {callouts(('model', 'the model'), ('effort', 'how much it reasons'))}
  </div>
  {block("accepted", "attention", "Accepted values depend on the model", "Vally checks before any session starts", words=True)}
  <p class="note">an eval file’s defaults</p>''', [
    {"type": "focus", "target": "effort", "at": "0~defaults", "color": "blue"},
    {"type": "focus", "target": "model", "at": "0~varies the model", "color": "blue"},
    {"type": "focus", "target": "accepted", "at": "1", "color": "yellow"}],
    css='.code.dark.defs{font-size:40px;line-height:1.6;padding:26px 36px;min-width:820px}.callout{font-size:32px}'
        '.stage{gap:28px}.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:36px}.note{margin:0}')

framed('s13', EB3, 'Four variants, sixty trials', f'''<div class="annotated">
    {panel('experiment')}
    {callouts(('evalf', 'five stimuli, graded by code'), ('vary', 'model and effort, nothing else'),
              ('runs', '15 trials a variant, 60 in all'), ('newer', 'a newer haiku: 4.5 takes no effort'))}
  </div>''', [
    {"type": "scroll", "target": "#experiment", "to": "top", "at": "0"},
    {"type": "focus", "target": "evalf", "at": "1", "color": "blue"},
    {"type": "focus", "target": "vary", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#experiment", "to": "6-12", "at": "2~nothing else"},
    {"type": "focus", "target": "runs", "at": "3", "color": "yellow"},
    {"type": "scroll", "target": "#experiment", "to": "11-19", "at": "3~sixty"},
    {"type": "focus", "target": "vhaiku", "at": "4", "color": "blue"},
    {"type": "scroll", "target": "#experiment", "to": "end", "at": "4~two models"},
    {"type": "focus", "target": "vterra", "at": "4~high effort", "color": "blue"},
    {"type": "scroll", "target": "#experiment", "to": "13-21", "at": "5"},
    {"type": "focus", "target": "newer", "at": "5~five point five", "color": "yellow"}], layout='layout-file')

# ---- Chapter: Price the variants -----------------------------------------------------------------
EB4 = 'Price the variants'
EFFORT = {HL: 'low', HH: 'high', TL: 'low', TH: 'high'}
framed('s14', EB4, 'Which costs least per pass?', f'''<div class="cols four">
    {''.join(block('v' + str(i), 'structure', v, f'{V[v]["model"]}<br>{EFFORT[v]} effort') for i, v in enumerate(VARIANTS))}
  </div>''', [],
    css='.four .semantic-block{min-height:300px;justify-content:center}.four .title{font-size:44px}'
        '.four .label{font-size:30px;line-height:1.45;font-family:var(--font-code)}')

eff = lambda mdl: ('does not support reasoning effort configuration' if EFFORTS[mdl] is None else
                   ', '.join(cell('lowhigh', e) if e in ('low', 'high') else e for e in EFFORTS[mdl]))
framed('s16', EB4, 'Two models take an effort', f'''<table class="data-table full eff">
    <thead><tr><th>Model</th><th>Reasoning efforts it accepts</th></tr></thead>
    <tbody>
      <tr><td class="mono">{cell('m45', H45)}</td><td>{eff(H45)}</td></tr>
      <tr><td class="mono">{cell('m55', H55)}</td><td class="mono">{eff(H55)}</td></tr>
      <tr><td class="mono">{cell('mterra', TERRA)}</td><td class="mono">{eff(TERRA)}</td></tr>
    </tbody>
  </table>
  <p class="note">from our account · {'stand-in: the course’s verified run' if PROVISIONAL else 'the check we just ran'} · yours will differ</p>''', [
    {"type": "focus", "target": "m45", "at": "1", "color": "blue"},
    {"type": "focus", "target": "m55", "at": "2", "color": "blue"},
    {"type": "focus", "target": "mterra", "at": "3", "color": "blue"},
    {"type": "focus", "target": "lowhigh", "at": "4", "color": "yellow"}],
    css='.eff{font-size:36px}.eff th{font-size:30px}.eff td{padding-top:30px;padding-bottom:30px}'
        '.eff td.mono{font-family:var(--font-code);font-size:34px}.stage{gap:26px}')


def calc_card(v):
    g = V[v]
    f = lambda k, label, value: f'<div class="f"><dt>{cell(k, label) if k else label}</dt><dd>{value}</dd></div>'
    return f'''<div class="cc">
      <div class="name">{v} <span>· {g['model']}</span></div>
      <dl>
        {f('', 'Trials', g['trials'])}{f('k_pass', 'Passing', f"{g['passed']} of {g['trials']}")}{f('k_err', 'ERROR', g['errors'])}{f('', 'Median tokens', ktok(g['med_tokens']))}
        {f('k_total', 'Total cost', aiu(g['aiu']))}{f('', 'In dollars', usd(g['aiu'] * 0.01))}{f('k_per', 'Per passing trial', aiu(g['per']))}
      </dl>
    </div>'''


framed('s19', EB4, 'Four files, four cards', f'''<div class="calc">
    {''.join(calc_card(v) for v in VARIANTS)}
  </div>
  <p class="lead total"><span data-concept="total" data-rep="note">Across {TRIALS} trials in 4 files: {aiu(TOTAL)}, or {usd(TOTAL * 0.01)} at $0.01 per AIU. Judge calls are not included.</span></p>
  <p class="note">the cost calculator’s result · {SRC}</p>''', [
    {"type": "focus", "target": "k_pass", "at": "1~how many passed", "color": "blue"},
    {"type": "focus", "target": "k_err", "at": "1~ERROR", "color": "blue"},
    {"type": "focus", "target": "k_total", "at": "1~total cost", "color": "blue"},
    {"type": "focus", "target": "k_per", "at": "1~cost per passing", "color": "yellow"},
    {"type": "focus", "target": "total", "at": "2", "color": "yellow"}],
    css='.stage{gap:14px;justify-content:flex-start}.calc{display:grid;grid-template-columns:1fr 1fr;gap:16px 24px;width:100%}'
        '.cc{background:var(--paper-muted);border-radius:var(--radius);padding:18px 28px 22px}'
        '.cc .name{font-family:var(--font-code);font-size:34px;font-weight:600;color:var(--ink);margin-bottom:12px}'
        '.cc .name span{font-weight:400;color:var(--ink-soft)}'
        '.cc dl{display:grid;grid-template-columns:1fr 1fr 1.1fr 1fr;gap:14px 20px;margin:0}.cc .f:nth-child(7){grid-column:span 2}'
        '.cc dt{font-size:25px;color:var(--ink-soft)}'
        '.cc dd{margin:2px 0 0;font-family:var(--font-code);font-size:31px;color:var(--ink);white-space:nowrap}'
        '.lead.total{font-size:32px;margin:6px 0 0;max-width:none}.note{margin:0}')

VNAME = {HL: 'hl', HH: 'hh', TL: 'terra', TH: 'terra'}
rows = ''.join(f'''<tr><td class="mono">{cell('row_' + VNAME[v], v)}</td><td>{cell('pass', f"{V[v]['passed']} of {V[v]['trials']}")}</td>
        <td>{aiu(V[v]['aiu'])}</td><td>{cell('per_' + VNAME[v], aiu(V[v]['per']))}</td><td>{ktok(V[v]['med_tokens'])}</td></tr>\n''' for v in VARIANTS)
times = V[TL]['per'] / V[HL]['per']
SENTENCE = (f'On these five stimuli, {H55} at low effort passed all {V[HL]["passed"]} trials at {V[HL]["per"]:.2f} AIU each, '
            f'against {V[TL]["per"]:.2f} and {V[TH]["per"]:.2f} AIU on {TERRA}, so we would run them on {HL}.')
framed('s20', EB4, 'One variant beats the rest', f'''<table class="data-table full price">
    <thead><tr><th>Variant</th><th>Passing</th><th>Total</th><th>Per passing trial</th><th>Median tokens</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>
  {quote('ours', 'Our sentence', '“' + SENTENCE + '”')}
  <p class="note">{SRC}</p>''', [
    {"type": "focus", "target": "pass", "at": "1", "color": "blue"},
    {"type": "focus", "target": "per_hl", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "per_hh", "at": "3", "color": "blue"},
    {"type": "focus", "target": "per_terra", "at": "4", "color": "blue"},
    {"type": "focus", "target": "row_hl", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "ours", "at": "6", "color": "yellow"}],
    css='.price{font-size:34px}.price th{font-size:28px}.price td{padding-top:15px;padding-bottom:15px;font-family:var(--font-code)}'
        '.stage{gap:18px;justify-content:flex-start}.quote{width:100%;padding-top:12px;padding-bottom:14px}'
        '.quote p{font-size:31px;line-height:1.36}.note{margin:0}')

# ---- Chapter: What the table says ----------------------------------------------------------------
EB5 = 'What the table says'
band = lambda lo, hi: f'{lo:.2f} to {hi:.2f} AIU a trial'
h_tok = f'{ktok(min(V[HL]["med_tokens"], V[HH]["med_tokens"]))}'
t_lo, t_hi = ktok(min(V[TL]["med_tokens"], V[TH]["med_tokens"])), ktok(max(V[TL]["med_tokens"], V[TH]["med_tokens"]))
t_tok = t_lo if t_lo == t_hi else f'{t_lo}–{t_hi}'
framed('s21', EB5, 'Tokens measure work, not price', f'''<div class="cols wide big">
    <div class="semantic-block" data-role="structure">
      <div class="who">{H55}</div><div class="title">{h_tok}</div><div class="label">median tokens in a trial</div>
      <div class="cost">{band(H_MIN, H_MAX)}</div>
    </div>
    <div class="semantic-block" data-role="structure">
      <div class="who">{TERRA}</div><div class="title"><span data-concept="ttok" data-rep="cell">{t_tok}</span></div><div class="label">median tokens in a trial</div>
      <div class="cost"><span data-concept="tcost" data-rep="cell">{band(T_MIN, T_MAX)}</span></div>
    </div>
  </div>
  <p class="note">{SRC}</p>''', [
    {"type": "focus", "target": "tcost", "at": "2~cost the most", "color": "yellow"},
    {"type": "focus", "target": "ttok", "at": "2~fewest", "color": "blue"}],
    css='.big .semantic-block{min-height:360px;justify-content:center;gap:6px}.big .who{font-family:var(--font-code);font-size:32px;color:var(--ink)}'
        '.big .title{font-size:84px;line-height:1.15}.big .label{font-size:32px}'
        '.big .cost{font-family:var(--font-code);font-size:38px;color:var(--ink);margin-top:18px}.stage{gap:24px}.note{margin:0}')

framed('s22', EB5, 'Each model has its own price', f'''<table class="data-table full ppt">
    <thead><tr><th>Model</th><th>A trial of ours</th><th>Tokens</th><th>Cost</th><th>Per 100,000 tokens</th></tr></thead>
    <tbody>
      <tr><td class="mono">{H45}</td><td class="what">the first one these videos ran</td><td>{EARLIER['totalTokens']:,}</td><td>{aiu(EARLIER['nano'] / NANO)}</td><td>{cell('old', aiu(OLD_PER100K))}</td></tr>
      <tr><td class="mono">{H55}</td><td class="what">the record from this run</td><td>{REC_TOK:,}</td><td>{aiu(REC_AIU)}</td><td>{cell('new', aiu(NEW_PER100K))}</td></tr>
    </tbody>
  </table>
  <p class="lead"><span data-concept="ratio" data-rep="note">On our account, the newer haiku was about {round(OLD_PER100K / NEW_PER100K)} times cheaper per token.</span></p>
  <p class="note">{'the second row is a stand-in: the course’s verified run' if PROVISIONAL else f'runs {EARLIER["run"]} and {RUN}'}</p>''', [
    {"type": "focus", "target": "old", "at": "1", "color": "blue"},
    {"type": "focus", "target": "new", "at": "2", "color": "blue"},
    {"type": "focus", "target": "ratio", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.ppt{font-size:34px}.ppt th{font-size:28px}.ppt td{padding-top:30px;padding-bottom:30px;font-family:var(--font-code)}'
        '.ppt td.what{font-family:var(--font-body);font-size:30px}.lead{font-size:40px;margin:0}.stage{gap:28px}.note{margin:0}')

framed('s23', EB5, 'Same ranges, separate costs', f'''<div class="cols wide terms">
    {block("range", "structure", f"15 of 15 · {RANGE[0]}% to {RANGE[1]}%", "the pass rate’s range, the same for all four variants", words=True)}
    <div class="semantic-block" data-concept="bands" data-rep="block" data-role="attention">
      <div class="title words">What a trial cost</div>
      <div class="bandrow"><span>{H55}</span><span>{H_MIN:.2f} to {H_MAX:.2f} AIU</span></div>
      <div class="bandrow"><span>{TERRA}</span><span>{T_MIN:.2f} to {T_MAX:.2f} AIU</span></div>
    </div>
  </div>
  {quote('fair', 'Our sentence, with the ranges', '“As good, as far as these trials can tell, and far cheaper.”')}
  <p class="note">{SRC}</p>''', [
    {"type": "focus", "target": "range", "at": "1", "color": "blue"},
    {"type": "focus", "target": "bands", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "fair", "at": "4", "color": "blue"}],
    css='.terms .semantic-block{min-height:250px}.terms .title{font-size:42px}.terms .label{font-size:34px;line-height:1.35}'
        '.bandrow{display:flex;justify-content:space-between;gap:24px;font-family:var(--font-code);font-size:32px;color:var(--ink);margin-top:10px}'
        '.stage{gap:24px}.quote{width:100%}.quote p{font-size:40px}.note{margin:0}')

framed('s24', EB5, 'True of these five requests', f'''<div class="cols wide terms">
    {block("five", "structure", "These five stimuli", "the ones the skill now passes easily", words=True)}
    {block("wording", "attention", "The wording requests, graded by a judge", "where the models differed: price them the same way", words=True)}
  </div>
  <p class="lead"><span data-concept="method" data-rep="note">Prices change, and your account’s may differ: a method to repeat, not facts about the models.</span></p>''', [
    {"type": "focus", "target": "five", "at": "0", "color": "blue"},
    {"type": "focus", "target": "wording", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "method", "at": "2", "color": "blue"}],
    css='.terms .semantic-block{min-height:280px}.terms .title{font-size:42px}.terms .label{font-size:36px;line-height:1.35}'
        '.lead{font-size:38px;margin:0}.stage{gap:32px}')

framed('s25', EB5, 'What it comes to in dollars', f'''<table class="data-table full bill">
    <thead><tr><th></th><th>Trials</th><th>AIU</th><th>In dollars</th></tr></thead>
    <tbody>
      <tr><td class="what">{cell('r1', 'This experiment')}</td><td>{TRIALS}</td><td>{TOTAL:.2f}</td><td>{usd(TOTAL * 0.01)}</td></tr>
      <tr><td class="what">{cell('r2', 'A check after every edit')}</td><td>10</td><td>about {EDIT_CENTS}</td><td>${EDIT_CENTS / 100:.2f} an edit · ${EDIT_CENTS * 20 / 100:.2f} for twenty edits</td></tr>
      <tr><td class="what">{cell('r2b', 'The same check on haiku-low')}</td><td>5</td><td>about {round(5 * V[HL]['per'])}</td><td>{usd(round(5 * V[HL]['per']) * 0.01)[:-1]} an edit</td></tr>
      <tr><td class="what">{cell('r3', 'Every stimulus, every night')}</td><td>30</td><td>about {round(NIGHT_AIU)}</td><td>about ${NIGHTS_USD} for thirty nights, plus judge calls</td></tr>
    </tbody>
  </table>
  <p class="note">$0.01 per AIU · rows two and four use our earlier runs’ average of about {AVG_AIU:.1f} AIU a trial on {H45} and {TERRA}</p>''', [
    {"type": "focus", "target": "r1", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "r2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "r2b", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "r3", "at": "5", "color": "blue"}],
    css='.bill{font-size:34px}.bill th{font-size:28px}.bill td{padding-top:30px;padding-bottom:30px;font-family:var(--font-code)}'
        '.bill td.what{font-family:var(--font-body);font-weight:600}.bill td:nth-child(-n+3),.bill th{white-space:nowrap}.bill{font-size:32px}.bill td{padding-top:22px;padding-bottom:22px}.stage{gap:22px}')

grows = [('g1', 'stimuli'), ('g2', 'trials'), ('g3', 'models'), ('g4', 'how often you run')]
framed('s26', EB5, 'Small, and it grows', f'''{block("course", "structure", "About $11 of agent runs, plus judge calls", "what verifying this course took", words=True)}
  <p class="lead with">It grows with</p>
  <div class="cols four">
    {''.join(block(c, 'attention', t, '', words=True) for c, t in grows)}
  </div>
  <p class="lead"><span data-concept="allow" data-rep="note">Your plan’s monthly allowance is spent first.</span></p>''', [
    {"type": "focus", "target": "course", "at": "0", "color": "blue"},
    {"type": "focus", "target": "g1", "at": "1~stimuli", "color": "yellow"},
    {"type": "focus", "target": "g2", "at": "1~trials", "color": "yellow"},
    {"type": "focus", "target": "g3", "at": "1~models", "color": "yellow"},
    {"type": "focus", "target": "g4", "at": "1~how often", "color": "yellow"},
    {"type": "focus", "target": "allow", "at": "2", "color": "blue"}],
    css='.stage{gap:28px}.stage > .semantic-block{width:100%}.stage > .semantic-block .title{font-size:46px}'
        '.stage > .semantic-block .label{font-size:34px}.four .semantic-block{min-height:150px;justify-content:center}.four .label{display:none}.lead.with{font-size:34px;margin:0}'
        '.four .title{font-size:38px}.lead{font-size:38px;margin:0}.stage{gap:22px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Total cost', 'every trial, failures included'),
    ('Trials that passed', 'the useful results'),
    ('For each model', 'measured, not carried over')], 1))
framed('s27', 'Recap', 'Why divide by the passes?', f'''<div class="semantic-block" id="cpp" data-role="structure">
    <div class="title words">cost per passing trial</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#cpp", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "p3", "at": "3~each model", "color": "blue"}], layout='layout-expand',
    css='#cpp{width:100%;padding:36px 40px 44px;gap:24px}'
        '#cpp .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#cpp .part{min-height:260px}#cpp .part .title{font-size:46px;line-height:1.2}'
        '#cpp .part .label{font-size:32px}')

scene('s28', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">A model from your own provider</h1>
  <p class="lead">Can Vally run a model from a service of your own?</p>
  <p class="note">Exercises are on the lesson page · Source: Kapoor et al., “AI Agents That Matter” (2024)</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', 'PROVISIONAL run (stand-in figures)' if PROVISIONAL else RUN)
