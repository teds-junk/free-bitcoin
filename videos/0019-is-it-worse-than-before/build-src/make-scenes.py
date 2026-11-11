"""Generate lesson 19's scene pages, file panel included (panels.sh is kept only so the usual
`python3 build-src/make-scenes.py && bash build-src/panels.sh` still works).

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and output in a dark box on the left with notes on the right (.annotated + .callout), terms in
soft blocks, numbers in a .data-table. Nothing here sets a colour or a font outside the theme's
variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/earlier/haiku.log      what `vally compare` printed in the course's own earlier run (verified/
                             lesson-19). A fixed specimen: scenes s09 to s11 explain the printed block
                             on it, before this video's own comparisons are run.
  src/earlier/swapped.json   the course's two earlier runs of the swapped comparison (s11, s21).
  src/run/s14.log, s17.log, s18.log   what this video's three comparisons printed, each ending with an
                             "exit=N" line the tape's wrapper adds.
  src/run/haiku-compare.jsonl   the record s14 wrote. Spread out as src/run/haiku-compare.pretty.json
                             for the panel in s15 (json.dumps, indent 2: the same text, one key a line).
  src/run/facts.json         which pair s15 shows, which sentence of its reason is quoted, the two
                             entries of that pair (s02, s03), and which pair is the tie.
  src/run/RUN                the experiment folder's name.
While src/run/PROVISIONAL exists these are stand-ins (see that file) and the run-quoting scenes say so.

The asserts under "What the narration says" state each claim an outcome sentence makes. When a
recording changes one, the assert fails and names the sentences to reword in storyboard.json.

Run from anywhere:  python3 build-src/make-scenes.py
"""
import json, math, pathlib, re, subprocess, textwrap

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
H, T = 'claude-haiku-4.5', 'gpt-5.6-terra'
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
STAND_IN = ' · STAND-IN: the course’s verified run, not yet ours' if PROVISIONAL else ''


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


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>'


# ---- Reading what compare printed ------------------------------------------------------------------
NUM = r'([+\-−]?\d[\d.]*)'
num = lambda s: float(s.replace('−', '-'))


def parse(path, need_exit=True):
    """One comparison's printed block -> a dict of its numbers. Tolerates the terminal's own wrapping."""
    raw = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', path.read_text()).replace('\r', '')
    flat = re.sub(r'\s+', ' ', raw)
    r = {'raw': raw}
    m = re.search(r'(\S+) vs (\S+) \(baseline\)', flat)
    assert m, f'{path.name}: no "X vs Y (baseline)" line'
    r['treatment'], r['baseline'] = m.group(1), m.group(2)
    m = re.search(r'Win rate: (\d+)% (\d+) wins? / (\d+) ties? / (\d+) loss(?:es)? over (\d+) trials', flat)
    assert m, f'{path.name}: no win rate line'
    r['rate'], r['wins'], r['ties'], r['losses'], r['pairs'] = map(int, m.groups())
    m = re.search(rf'Mean score: {NUM} \[95% CI {NUM}, {NUM}\]', flat)
    assert m, f'{path.name}: no mean score line'
    r['mean'], r['lo'], r['hi'] = map(num, m.groups())
    m = re.search(r'McNemar\): \+(\d+)/-(\d+) pass-fail flips, p=([\d.]+) \(exact, ((?:not )?significant)\)', flat)
    r['flips'] = (int(m.group(1)), int(m.group(2)), float(m.group(3)), m.group(4)) if m else None
    m = re.search(rf'tokens {NUM} \[{NUM}, {NUM}\]', flat)
    assert m, f'{path.name}: no tokens line'
    r['tok'], r['tok_lo'], r['tok_hi'] = map(num, m.groups())
    r['regression'] = 'Regression' in flat
    r['unmatched'] = 'no baseline match' in flat
    m = re.search(r'^exit=(\d+)\s*$', raw, re.M)
    assert m or not need_exit, f'{path.name}: no exit= line (the tape\'s wrapper writes it)'
    r['exit'] = int(m.group(1)) if m else None
    return r


sgn = lambda x, nd=2: ('+' if x >= 0 else '−') + f'{abs(x):.{nd}f}'
rng = lambda r: f'{sgn(r["mean"])} [{sgn(r["lo"])}, {sgn(r["hi"])}]'
tk = lambda x: ('+' if x >= 0 else '−') + f'{abs(int(round(x))):,}'
tok_rng = lambda r: f'{tk(r["tok"])} [{tk(r["tok_lo"])}, {tk(r["tok_hi"])}]'


def wilson(k, n, z=1.96):
    """The range the course's calculator puts around a count (Wilson score interval), as whole percents."""
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return math.floor(100 * (c - h) + 0.5), math.floor(100 * (c + h) + 0.5)   # Math.round, as the calculator


# What assets/range-calculator.js shows for the page's counts (the page's prose says 57 for the second).
assert wilson(3, 9) == (12, 65) and wilson(8, 9) == (56, 98)

# ---- The fixed specimen: the course's earlier run --------------------------------------------------
elog = (D / 'src/earlier/haiku.log').read_text()
E = parse(D / 'src/earlier/haiku.log', need_exit=False)
assert (E['wins'], E['ties'], E['losses'], E['pairs']) == (6, 3, 0, 9) and rng(E) == '+0.53 [+0.17, +0.89]'
assert E['flips'] == (5, 0, 0.063, 'not significant')
eline = lambda key: next(l for l in elog.splitlines() if key in l)
SWAPPED = json.loads((D / 'src/earlier/swapped.json').read_text())
assert [s['exit'] for s in SWAPPED] == [1, 0] and SWAPPED[0]['hi'] < 0 < SWAPPED[1]['hi']

# ---- This video's own run --------------------------------------------------------------------------
A14, A17, A18 = (parse(D / f'src/run/{s}.log') for s in ('s14', 's17', 's18'))
RUN = (D / 'src/run/RUN').read_text().strip()
FACTS = json.loads((D / 'src/run/facts.json').read_text())
recs = [json.loads(l) for l in (D / 'src/run/haiku-compare.jsonl').read_text().splitlines() if l.strip()]
recs = [r for r in recs if r.get('type') == 'comparison' and r.get('treatment') == 'haiku-after']
assert len(recs) == 1, f'haiku-compare.jsonl: expected one comparison record for haiku-after, found {len(recs)}'
REC = recs[0]
PRETTY = json.dumps(REC, indent=2, ensure_ascii=False)
(D / 'src/run/haiku-compare.pretty.json').write_text(PRETTY + '\n')
plines = PRETTY.splitlines()
pairs = [(st['stimulusName'], tr) for st in REC['stimuli'] for tr in st['trials']]
REASON_KEY = next((k for k in ('evidence', 'reason', 'reasoning', 'rationale') if k in pairs[0][1]), None)
assert REASON_KEY, f'the record keeps the judge\'s reason under a key this script does not know: {list(pairs[0][1])}'
for k in ('trialIndex', 'winner', 'magnitude', 'score', 'baselinePassed', 'treatmentPassed'):
    assert k in pairs[0][1], f'the record has no "{k}" per pair: {list(pairs[0][1])}'


def pair_lines(stimulus, trial):
    """-> (the pair's dict, {key: 1-based line number in the spread-out record})."""
    want = next(i for i, (s, t) in enumerate(pairs) if s == stimulus and t['trialIndex'] == trial)
    seen = -1
    for i, l in enumerate(plines):
        if not re.fullmatch(r'\s*\{', l):
            continue
        ind = len(l) - len(l.lstrip())
        end = next(j for j in range(i + 1, len(plines)) if plines[j] in (' ' * ind + '}', ' ' * ind + '},'))
        keys = {m.group(1): j + 1 for j in range(i + 1, end)
                if (m := re.match(r' {%d}"(\w+)":' % (ind + 2), plines[j]))}
        if 'trialIndex' in keys and 'winner' in keys:
            seen += 1
            if seen == want:
                return pairs[want][1], keys
    raise AssertionError(f'{stimulus} trial {trial}: not found in the spread-out record')


passed = lambda side: sum(bool(t[side + 'Passed']) for _, t in pairs)
BEFORE, AFTER, N = passed('baseline'), passed('treatment'), len(pairs)
RB, RA = wilson(BEFORE, N), wilson(AFTER, N)
SHOWN, SL = pair_lines(FACTS['shown_pair']['stimulus'], FACTS['shown_pair']['trial'])
SECOND, TL = pair_lines(FACTS['second_pair']['stimulus'], FACTS['second_pair']['trial'])
QUOTE = FACTS['reason_quote']

# ---- What the narration says about the run. If a recording changes these, the sentences change too.
T17 = json.loads((D / 'src/run/terra-compare.jsonl').read_text().splitlines()[0])
ET = parse(D / 'src/earlier/terra.log')      # the course's earlier terra comparison (verified/lesson-19)
# s01 sentence 0: "went from five of nine to nine of nine, and the two ranges still overlapped".
assert (BEFORE, AFTER, N) == (5, 9, 9) and RA[0] <= RB[1], \
    f's01 sentence 0, s20 sentence 1: passes {BEFORE}->{AFTER} of {N}, ranges {RB} {RA}'
# s02 sentence 3, s15 sentences 1 to 4: the shown pair is dates, trial 0; both entries passed their graders;
# the after skill's entry was judged slightly worse (-0.4); the quoted sentence is in the judge's reason.
assert (FACTS['shown_pair']['stimulus'], FACTS['shown_pair']['trial']) == ('dates', 0), 's15 sentence 1 names the pair'
assert SHOWN['winner'] == 'baseline' and SHOWN['magnitude'] == 'slightly-worse' and abs(SHOWN['score'] + 0.4) < 1e-9, \
    f's15 sentence 2: {SHOWN["winner"]}, {SHOWN["magnitude"]}, {SHOWN["score"]}'
assert SHOWN['baselinePassed'] and SHOWN['treatmentPassed'], 's02 sentence 3, s15 sentence 4: both passed'
assert SHOWN[REASON_KEY].count(QUOTE) == 1 and '2026-1-5' in QUOTE, 's15 sentence 3: facts.json reason_quote must occur once in the reason'
for side in ('before', 'after'):
    entry, p = FACTS[side + '_entry'], D / f'src/run/pair-{side}.patch'
    assert '+' + entry in p.read_text().splitlines(), f'facts.json {side}_entry is not a line added by src/run/pair-{side}.patch'
# s15 sentence 5: a pair where the two orders agreed on the winner, not on how much; the weaker verdict is kept.
DOWN = 'the position-swapped pass judged this "slightly-better", so the more confident "much-better" was downgraded'
assert SECOND['winner'] == 'treatment' and SECOND['magnitude'] == 'slightly-better' and DOWN in json.dumps(SECOND, ensure_ascii=False).replace('\\"', '"'), \
    's15 sentence 5: choose another second_pair, or reword'
# s14: "won four of nine pairs", "plus zero point three three", "from minus zero point zero eight to plus zero
#      point seven five, so it includes zero", "on tokens ... wholly below zero ... about fourteen thousand fewer".
assert (A14['treatment'], A14['baseline']) == ('haiku-after', 'haiku-before')
assert (A14['wins'], A14['pairs']) == (4, 9) and rng(A14) == '+0.33 [−0.08, +0.75]', f's14 sentences 3, 4: {A14["wins"]} of {A14["pairs"]}, {rng(A14)}'
assert A14['tok_hi'] < 0 and 13500 <= -A14['tok'] < 14500, f's14 sentence 5: tokens {tok_rng(A14)}'
# s17: "only six pairs were judged: three of the before trials never finished ... as the warning says";
#      "three of the six are ties, and the range includes zero"; "the tokens fell, by about eight thousand per
#      trial, with a range wholly below zero"; "exit code zero".
assert (A17['treatment'], A17['baseline']) == ('terra-after', 'terra-before')
assert A17['pairs'] == 6 and A17['unmatched'] and len(T17['unmatchedTreatment']) == 3, 's17 sentence 2: pairs and unmatched trials'
assert A17['ties'] == 3 and A17['lo'] < 0 < A17['hi'], f's17 sentence 3: {A17["ties"]} ties, {rng(A17)}'
assert A17['tok_hi'] < 0 and 7500 <= -A17['tok'] < 8500, f's17 sentence 4: tokens {tok_rng(A17)}'
assert A17['exit'] == 0 and not A17['regression'], 's17 sentence 6: the check did not exit 0'
# s22 sentence 1: "tokens fell on both models".  s22 sentence 2 (the earlier run, src/earlier/terra.log): "about
# eleven thousand more tokens per trial on terra, with a range wholly above zero, and the check still exited zero".
assert A14['tok'] < 0 and A17['tok'] < 0, 's22 sentence 1'
assert 10500 <= ET['tok'] < 11500 and ET['tok_lo'] > 0 and ET['exit'] == 0 and ET['treatment'] == 'terra-after', 's22 sentence 2'
# The swapped comparison can land on either side of the line. These sentences state its exit code, and are
# checked against the storyboard so that the words must match the recording:
#   exit 0 (our run):  s18[2] "...its range reaches above zero."   s18[4] "Exit code zero: the check passed, ..."
#            s19[2] "None of them, in our run."   s19[3] "...came closest: ... its range crosses it."
#            s21[6] "Ours passed it too, with a range that reaches above zero."
#   exit 1:  s18[2] "...and its whole range is below zero."   s18[4] "Exit code one: the check failed, because the
#            whole range is below zero."   s19[2] "Only the last one, in our run."   s19[3] "With the roles
#            swapped, the mean and its whole range are below zero."   s21[6] "Ours failed it, ..."
_sb = json.loads((D / 'storyboard.json').read_text())
NARR = {x['id']: [n if isinstance(n, str) else n['text'] for n in x['narration']] for x in _sb['scenes']}
FAILED = A18['exit'] == 1
assert (A18['treatment'], A18['baseline']) == ('haiku-before', 'haiku-after')
assert A18['exit'] in (0, 1) and FAILED == A18['regression'] == (A18['hi'] < 0), \
    f's18: exit {A18["exit"]}, regression line {A18["regression"]}, range {rng(A18)} do not agree'


def says(sid, i, *words):
    assert all(w in NARR[sid][i] for w in words), \
        f'{sid} sentence {i} must say {words} for this recording (swapped run exit {A18["exit"]}): "{NARR[sid][i]}"'


if FAILED:
    says('s18', 2, 'whole range is below zero'); says('s18', 4, 'Exit code one', 'failed')
    says('s19', 2, 'Only the last'); says('s19', 3, 'below zero'); says('s21', 6, 'failed')
else:
    says('s18', 2, 'above zero'); says('s18', 4, 'Exit code zero', 'passed')
    says('s19', 2, 'None'); says('s19', 3, 'crosses'); says('s21', 6, 'passed')
# s18 sentence 1: "the first comparison's mean with its sign flipped: minus zero point three three";
# s18 sentence 2: "this one printed exactly that".
assert sgn(-A14['mean']) == sgn(A18['mean']) == '−0.33', f's18 sentences 1, 2: {sgn(-A14["mean"])}, {sgn(A18["mean"])}'
HEAD19 = 'The check failed once' if FAILED else 'The check never failed'
# s20: "four pairs flipped from fail to pass, none flipped back ... not significant"; "one time in eight";
#      "a mean above zero, but its range includes zero too"; the earlier run's pairwise range was above zero.
assert A14['flips'] and A14['flips'][:2] == (4, 0) and A14['flips'][3] == 'not significant', f's20 sentence 2: {A14["flips"]}'
assert A14['flips'][0] == AFTER - BEFORE + A14['flips'][1], 'the record\'s pass counts and the printed flips disagree'
assert abs(A14['flips'][2] - 1 / 8) < 0.001, f's20 sentence 3: p = {A14["flips"][2]}'
assert A14['mean'] > 0 and A14['lo'] < 0 < A14['hi'], f's20 sentences 4, 5: {rng(A14)}'
assert E['lo'] > 0, 's20 sentence 6: the earlier run'

# ---- Hook ------------------------------------------------------------------------------------------
BIG = ('.terms .semantic-block{min-height:300px;justify-content:center}.terms .title{font-size:104px;line-height:1.1}'
       '.terms .label{font-size:34px}.lead{font-size:38px}')
framed('s01', 'Vally &amp; Agent Evals', 'Is it worse than before', f'''<div class="cols wide terms">
    {block("before", "structure", f"{BEFORE} of {N}", f"before the edit · range {RB[0]}% to {RB[1]}%")}
    {block("after", "attention", f"{AFTER} of {N}", f"after the edit · range {RA[0]}% to {RA[1]}%")}
  </div>
  <p class="lead">{mono(H)} · trials that passed, before and after one edit to the skill</p>
  <p class="note">our run{STAND_IN}</p>''', [
    {"type": "focus", "target": "before", "at": "0~five of nine", "color": "blue"},
    {"type": "focus", "target": "after", "at": "0~nine of nine", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    h='h1', title_class='scene-title chapter', css='.scene-title.chapter{font-size:116px}' + BIG)

# ---- Chapter: Is it any worse? ---------------------------------------------------------------------
EB1 = 'Is it any worse?'
PAIR_ID = f'{FACTS["shown_pair"]["stimulus"]} · trial {FACTS["shown_pair"]["trial"]}'
verdict = lambda c: f'<span class="verdict" data-concept="{c}" data-rep="note">passed its graders</span>'
# A changelog entry wider than the box wraps as the changelog itself would: continuation lines indented.
entry = lambda side: '\n'.join(textwrap.wrap(FACTS[side + '_entry'], 62, subsequent_indent='  ', break_long_words=False))
pair_cards = lambda v: f'''<div class="results">
      {card('c-before', f'before the edit · {mono(PAIR_ID)}{v("v")}', code(entry('before'), 'markdown'))}
      {card('c-after', f'after the edit · {mono(PAIR_ID)}{v("v")}', code(entry('after'), 'markdown'))}
    </div>'''
PAIR_CSS = ('.results{display:flex;flex-direction:column;gap:30px;width:100%}'
            '.results .card > .code.dark{font-size:34px;padding:24px 32px}.results .card .who{font-size:32px}'
            '.verdict{margin-left:28px;font-weight:600}')
framed('s02', EB1, 'Graders see one trial', pair_cards(verdict) + f'''
  <p class="note">the entry each version of the skill wrote for the same request, on {mono(H)}{STAND_IN}</p>''', [
    {"type": "focus", "target": "c-before", "at": "3~two entries", "color": "blue"},
    {"type": "focus", "target": "v", "at": "3~passed both", "color": "green"},
    {"type": "focus", "target": "none", "at": "4"}], css=PAIR_CSS)

framed('s03', EB1, 'Two answers, side by side', pair_cards(lambda c: '') + f'''
  {block("judge", "transform", "pairwise judge", "shown both answers to one request · says which is better, and by how much", words=True)}
  <p class="note">Vally’s docs call this comparison mode</p>''', [
    {"type": "focus", "target": "judge", "at": "1", "color": "cyan"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "judge", "at": "3", "color": "cyan"}],
    css=PAIR_CSS + '.results{gap:18px}.results .card > .code.dark{padding:16px 32px}'
        '.semantic-block{width:100%;min-height:0;padding-top:20px;padding-bottom:20px}.semantic-block .label{font-size:32px}.stage{gap:22px}')

TERMS = '.terms .semantic-block{min-height:190px}.terms .title{font-size:40px}.terms .label{font-size:32px}.stage{gap:26px}'
framed('s04', EB1, 'Each pair is judged twice', f'''<div class="cols wide terms">
    {block("o1", "structure", "First order", "before, then after", words=True)}
    {block("o2", "structure", "Second order", "after, then before", words=True)}
  </div>
  <div class="cols wide terms">
    {block("agree", "success", "Both orders agree", "that verdict stands", words=True)}
    {block("tie", "attention", "The orders disagree", "a tie", words=True)}
  </div>
  <p class="note">Sources: Zheng et al., “Judging LLM-as-a-Judge” (2023) · Vally docs, “CLI: compare”</p>''', [
    {"type": "focus", "target": "o1", "at": "1~one position", "color": "blue"},
    {"type": "focus", "target": "o2", "at": "2~opposite", "color": "blue"},
    {"type": "focus", "target": "agree", "at": "3", "color": "green"},
    {"type": "focus", "target": "tie", "at": "4", "color": "yellow"}], css=TERMS)

framed('s05', EB1, 'Two questions, two tools', f'''<div class="cols wide terms">
    {block("graders", "structure", "Graders", "is it right?", words=True)}
    {block("pairwise", "attention", "Pairwise judge", "is it worse?", words=True)}
  </div>''', [
    {"type": "focus", "target": "pairwise", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "graders", "at": "2", "color": "blue"},
    {"type": "focus", "target": "pairwise", "at": "3", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px;justify-content:center}.terms .title{font-size:56px}.terms .label{font-size:44px}')

# ---- Chapter: What compare reports -----------------------------------------------------------------
EB2 = 'What compare reports'
CMD = ('⟦cmd:vally compare⟧ \\\n  ⟦base:--baseline⟧ haiku-before \\\n  ⟦treat:--treatment⟧ haiku-after \\\n'
       '  ⟦judge:--judge-model⟧ claude-sonnet-5.5 \\\n  ⟦out:--output⟧ haiku-compare.jsonl')
framed('s06', EB2, 'Compare two saved runs', f'''<div class="annotated">
    {code(CMD, 'bash', 'cmd')}
    {callouts(('base', 'the version to compare against'), ('treat', 'the version that changed'),
              ('judge', 'has to be named'), ('out', 'a record of every pair'))}
  </div>''', [
    {"type": "focus", "target": "cmd", "at": "1", "color": "cyan"},
    {"type": "focus", "target": "base", "at": "2~baseline", "color": "blue"},
    {"type": "focus", "target": "treat", "at": "2~treatment", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "judge", "at": "4", "color": "blue"},
    {"type": "focus", "target": "out", "at": "5", "color": "blue"}],
    css='.code.dark.cmd{min-width:840px;font-size:38px;line-height:1.6}.callout{font-size:34px}')

TREE = (f'{RUN}/\n  ⟦hb:haiku-before/⟧   ⟦rj:results.jsonl⟧\n  ⟦ha:haiku-after/⟧    results.jsonl\n'
        '  ⟦tb:terra-before/⟧   results.jsonl\n  ⟦tb:terra-after/⟧    results.jsonl\n  report.md')
framed('s07', EB2, 'Two variants, not the folder', f'''<div class="annotated">
    {code(TREE, 'text', 'tree')}
    {callouts(('hb', 'the experiment’s baseline'), ('ha', 'our treatment'), ('tb', 'another model'))}
  </div>
  <p class="note">the before-and-after experiment’s folder, under {mono("results/lesson-15")}{STAND_IN}</p>''', [
    {"type": "focus", "target": "hb", "at": "1~baseline", "color": "blue"},
    {"type": "focus", "target": "tb", "at": "2~terra", "color": "yellow"},
    {"type": "focus", "target": "ha", "at": "3~two variant", "color": "blue"},
    {"type": "focus", "target": "rj", "at": "4~results", "color": "cyan"}],
    css='.code.dark.tree{min-width:820px;font-size:38px;line-height:1.7}.callout{font-size:34px}')

VERDICTS = [('v1', 'much better', '+1.0'), ('v2', 'slightly better', '+0.4'),
            ('v3', 'equal, or the two orders disagree', '0'), ('v4', 'slightly worse', '−0.4'), ('v5', 'much worse', '−1.0')]
vrows = ''.join(f'<tr><td>{cell(c, v)}</td><td class="num">{cell(c, s)}</td></tr>\n' for c, v, s in VERDICTS)
TABLE = ('.data-table{font-size:40px}.data-table th{font-size:30px}.data-table td{padding-top:20px;padding-bottom:20px}'
         '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:32px}'
         '.data-table th:last-child,.data-table td:last-child{padding-right:16px}')
framed('s08', EB2, 'A verdict becomes a score', f'''<table class="data-table full">
    <thead><tr><th>The judge’s verdict on the treatment</th><th class="num">score</th></tr></thead>
    <tbody>
{vrows}    </tbody>
  </table>
  <p class="note">a pair: the same stimulus and trial number from each version · two judge calls per pair</p>''', [
    {"type": "focus", "target": "v1", "at": "2~much better", "color": "green"},
    {"type": "focus", "target": "v2", "at": "2~slightly better", "color": "green"},
    {"type": "focus", "target": "v3", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "v4", "at": "4~worse", "color": "red"},
    {"type": "focus", "target": "none", "at": "5"}], css=TABLE)

# The specimen block, wrapped where the lesson page wraps it (two lines are wider than a dark box holds).
lw, lm, lg = eline('Win rate'), eline('Mean score'), eline('McNemar')
a, b = lw.split(' over ')
assert a.strip() == 'Win rate: 67%  6 wins / 3 ties / 0 losses'
c, d = lm.split(' (+ = ')
g1, g2 = lg.split('flips, ')
TOP = (f'{eline(" vs ").strip()}\n  ⟦win:Win rate: 67%  6 wins⟧ / ⟦ties:3 ties⟧ / 0 losses\n      over {b.strip()}\n'
       f'  ⟦mean:Mean score: +0.53⟧ ⟦ci:[95% CI +0.17, +0.89]⟧\n      (+ = {d.strip()}')
assert c.strip() == 'Mean score: +0.53 [95% CI +0.17, +0.89]'
SPECIMEN = 'an earlier run of this command, on other saved trials · two long lines wrapped'
framed('s09', EB2, 'Win rate, then mean score', f'''<div class="annotated">
    {code(TOP, 'text', 'out')}
    {callouts(('win', 'pairs the treatment won'), ('ties', 'count against it'), ('mean', 'average of the nine scores'),
              ('ci', 'its range'))}
  </div>
  <p class="note">{SPECIMEN}</p>''', [
    {"type": "focus", "target": "win", "at": "1", "color": "blue"},
    {"type": "focus", "target": "ties", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "mean", "at": "3", "color": "blue"},
    {"type": "focus", "target": "ci", "at": "4", "color": "cyan"}],
    css='.code.dark.out{min-width:900px;font-size:36px;line-height:1.6}.callout{font-size:32px}')

metric = [l for l in elog.splitlines() if re.match(r'\s+(tokens|turns|tool calls|wall time|errors)', l)]
assert len(metric) == 5 and metric[0].split()[0] == 'tokens'
assert g1.strip() == 'Grader pass/fail (McNemar): +5/-0 pass-fail' and g2.strip() == 'p=0.063 (exact, not significant)'
REST = ('  Grader pass/fail ⟦name:(McNemar)⟧: ⟦flips:+5/-0 pass-fail flips⟧,\n      ⟦p:p=0.063⟧ (exact, not significant)\n'
        f'  {eline("Metric deltas").strip()}\n'
        + '\n'.join('    ' + (m.strip().replace('tokens', '⟦tok:tokens⟧', 1).replace('⚠ high variance', '⟦var:⚠ high variance⟧', 1)
                              if i == 0 else m.strip()) for i, m in enumerate(metric)))
framed('s10', EB2, 'A second test, and metrics', f'''<div class="annotated">
    {code(REST, 'text', 'out')}
    {callouts(('name', 'McNemar’s test, on graders only'), ('p', 'could it be chance?'),
              ('tok', 'treatment minus baseline, per trial'))}
  </div>
  <p class="note">{SPECIMEN}</p>''', [
    {"type": "focus", "target": "name", "at": "0", "color": "blue"},
    {"type": "focus", "target": "flips", "at": "1~flipped", "color": "yellow"},
    {"type": "focus", "target": "name", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p", "at": "3", "color": "cyan"},
    {"type": "focus", "target": "tok", "at": "6", "color": "blue"},
    {"type": "focus", "target": "var", "at": "7", "color": "yellow"}],
    css='.code.dark.out{min-width:1060px;font-size:33px;line-height:1.5}.callout{font-size:30px}.stage{justify-content:flex-start}')

S0 = SWAPPED[0]
GATE = [('g-up', rng(E), 'no', '0'),
        ('g-mid', '−0.20 [−0.55, +0.15]', 'the mean is, the range is not', '0'),
        ('g-down', rng(S0), 'the whole range', '1')]
grows = ''.join(f'<tr><td class="num">{cell(c, m)}</td><td>{w}</td><td class="num">{cell(c, x)}</td></tr>\n' for c, m, w, x in GATE)
framed('s11', EB2, 'Exit one on a regression', f'''<div class="annotated">
    {code('vally compare … ⟦flag:--fail-on-regression⟧\n⟦echo:echo $?⟧', 'bash', 'gate')}
    {callouts(('flag', 'fail when the treatment is worse'), ('echo', 'the last command’s exit code'))}
  </div>
  <table class="data-table full gate">
    <thead><tr><th class="num">mean score, with its range</th><th>below zero?</th><th class="num">exit code</th></tr></thead>
    <tbody>
{grows}    </tbody>
  </table>
  <p class="note">rows 1 and 3: earlier runs · row 2: an illustration</p>''', [
    {"type": "focus", "target": "flag", "at": "0~dash dash", "color": "blue"},
    {"type": "focus", "target": "g-down", "at": "1", "color": "red"},
    {"type": "focus", "target": "g-mid", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"},
    {"type": "focus", "target": "echo", "at": "6", "color": "cyan"}],
    css=TABLE + '.annotated .code.dark.gate{min-width:900px;font-size:36px;padding:22px 32px}.callout{font-size:32px}'
        '.gate{font-size:36px}.gate td{padding-top:14px;padding-bottom:14px}.stage{gap:22px}')

# ---- Chapter: Compare before and after -------------------------------------------------------------
EB3 = 'Compare before and after'
RUNS3 = [('r1', 'haiku-before', 'haiku-after', 'off', A14), ('r2', 'terra-before', 'terra-after', 'on', A17),
         ('r3', 'haiku-after', 'haiku-before', 'on', A18)]


def three(filled):
    body = ''
    for c, base, treat, check, r in RUNS3:
        assert (r['baseline'], r['treatment']) == (base, treat)
        exit_ = (str(r['exit']) if check == 'on' else 'check off') if filled else ''
        body += (f'<tr><td class="mono">{cell(c, base)}</td><td class="mono">{cell(c, treat)}</td>'
                 + ('' if filled else f'<td>{check}</td>')
                 + f'<td class="num">{cell(c + "-m", rng(r) if filled else "")}</td>'
                 + (f'<td class="num">{cell(c + "-t", tok_rng(r))}</td>' if filled else '')
                 + f'<td class="num">{cell(c + "-x", exit_)}</td></tr>\n')
    head = ('<th>baseline</th><th>treatment</th>' + ('' if filled else '<th>check</th>')
            + '<th class="num">mean score [range]</th>' + ('<th class="num">tokens per trial [range]</th>' if filled else '')
            + f'<th class="num">{cell("exitcol", "exit code")}</th>')
    return f'''<table class="data-table full three">
    <thead><tr>{head}</tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


THREE = TABLE + '.three td{padding-top:30px;padding-bottom:30px;height:56px}.three{font-size:36px}'
framed('s12', EB3, 'Three comparisons, one check', three(False) + '''
  <p class="note">each one judges saved trials of the before-and-after experiment · no agent runs</p>''', [
    {"type": "focus", "target": "r1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "r2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "r3", "at": "3", "color": "blue"},
    {"type": "focus", "target": "exitcol", "at": "4", "color": "yellow"}], css=THREE)

# s15: the record, spread out. One pair top to bottom, then a second pair's verdict.
ev, ti, wi, ma, sc_, bp, tp = (SL[k] for k in (REASON_KEY, 'trialIndex', 'winner', 'magnitude', 'score', 'baselinePassed', 'treatmentPassed'))
assert max(SL.values()) < TL['trialIndex'], 'the second pair must come after the shown pair in the record'
want = sorted([(1, 4), (ti, sc_), (ev, ev), (bp, tp), (TL['trialIndex'], TL['score'])])
ranges = [list(want[0])]
for a, b in want[1:]:
    if a <= ranges[-1][1] + 2:
        ranges[-1][1] = max(ranges[-1][1], b)
    else:
        ranges.append([a, b])
show = ','.join(f'{a}-{b}' for a, b in ranges)
marks = [f'{ti}=trial', f'{wi}=winner', f'{ma}=mag', f'{sc_}=mag', f'{ev}=reason:{QUOTE}', f'{bp}=passed', f'{tp}=passed',
         f'{TL["magnitude"]}=mag2']
framed('s15', EB3, 'Both passed, one judged better', f'''<div class="annotated">
    {panel('record')}
    {callouts(('trial', PAIR_ID), ('winner', 'the before skill'), ('mag', 'the after skill: slightly worse'),
              ('reason', 'the judge’s reason'), ('passed', 'both passed their graders'), ('mag2', 'the weaker of two verdicts'))}
  </div>
  <p class="note">in a reason, A is the baseline and B the treatment · the second pair’s reason ends: “the position-swapped pass
  judged this ‘slightly-better’, so the more confident ‘much-better’ was downgraded”</p>''', [
    {"type": "scroll", "target": "#record", "to": f"{ti}-{sc_}", "at": "1"},
    {"type": "focus", "target": "trial", "at": "1~dates", "color": "blue"},
    {"type": "focus", "target": "winner", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "mag", "at": "2~score", "color": "yellow"},
    {"type": "scroll", "target": "#record", "to": f"{ev}", "at": "3"},
    {"type": "focus", "target": "reason", "at": "3~example date", "color": "yellow"},
    {"type": "scroll", "target": "#record", "to": f"{bp}-{tp}", "at": "4"},
    {"type": "focus", "target": "passed", "at": "4~passed", "color": "green"},
    {"type": "scroll", "target": "#record", "to": f"{TL['trialIndex']}-{TL['score']}", "at": "5"},
    {"type": "focus", "target": "mag2", "at": "5~weaker", "color": "yellow"}], layout='layout-file',
    css='.scene-title{margin-bottom:16px}')
out = subprocess.run(
    ['node', str(SKILL / 'scripts/file-panel.js'), '--file', 'src/run/haiku-compare.pretty.json', '--lang', 'json',
     '--label', 'haiku-compare.jsonl · one record, spread out', '--id', 'record', '--width', '46', '--rows', '9',
     '--show', show, '--expect', f'{wi}="winner"', '--expect', f'{ev}="{REASON_KEY}"']
    + [x for m in marks for x in ('--mark', m)] + ['--into', 'scenes/s15.html'],
    cwd=D, capture_output=True, text=True)
assert out.returncode == 0, 'file-panel.js: ' + out.stderr + out.stdout

framed('s19', EB3, HEAD19, three(True) + f'''
  <p class="note">our three comparisons · scores from the pairwise judge, tokens from the saved trials · the terra row has {A17['pairs']} pairs: three before trials did not finish</p>''', [
    {"type": "focus", "target": "exitcol", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "r3-x", "at": "2", "color": "red" if FAILED else "green"},
    {"type": "focus", "target": "r3-m", "at": "3", "color": "yellow"}],
    css=TABLE + '.three{font-size:32px}.three th{font-size:26px}.three td{padding-top:26px;padding-bottom:26px}'
        '.three td.mono{font-size:28px}.three td,.three th{white-space:nowrap}')

# ---- Chapter: What it supports ---------------------------------------------------------------------
EB4 = 'What it supports'
fl = A14['flips']
THIRDS = ('.terms .semantic-block{min-height:300px;justify-content:center}.terms .title{font-size:72px;line-height:1.15}'
          '.terms .label{font-size:32px}.lead{font-size:36px}.stage{gap:26px}')
framed('s20', EB4, 'Three views, one answer', f'''<div class="cols wide terms">
    {block("counts", "structure", f"{BEFORE}, then {AFTER}", f"Trials passed, of {N} · the two ranges overlap")}
    {block("flips", "structure", f"+{fl[0]} / −{fl[1]}", f"Grader flips · p = {fl[2]:.3f}, {fl[3]}")}
    {block("pairwise", "structure", sgn(A14['mean']), f"Pairwise judge · range {sgn(A14['lo'])} to {sgn(A14['hi'])}, includes zero")}
  </div>
  <p class="note">{mono(H)}, before the edit against after it, in our run</p>
  <p class="lead"><span data-concept="earlier" data-rep="note">An earlier run, on other saved trials: pairwise {sgn(E['mean'])}, range {sgn(E['lo'])} to {sgn(E['hi'])}, above zero</span></p>''', [
    {"type": "focus", "target": "counts", "at": "1", "color": "blue"},
    {"type": "focus", "target": "flips", "at": "2", "color": "blue"},
    {"type": "focus", "target": "pairwise", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"},
    {"type": "focus", "target": "earlier", "at": "6", "color": "green"},
    {"type": "focus", "target": "none", "at": "7"}], css=THIRDS)

wtl = lambda r: f'{r["wins"]} / {r["ties"]} / {r["losses"]}'
srow = lambda c, who, r: (f'<tr><td>{who}</td><td class="num">{wtl(r)}</td><td class="num">{cell(c, rng(r))}</td>'
                          f'<td class="num">{cell(c, r["exit"])}</td></tr>\n')
framed('s21', EB4, 'Hold that loosely', f'''<table class="data-table full swapped">
    <thead><tr><th>The swapped comparison, with the check on</th><th class="num">wins / ties / losses</th>
      <th class="num">mean score, with its range</th><th class="num">exit code</th></tr></thead>
    <tbody>
{srow('e1', 'an earlier run', SWAPPED[0])}{srow('e2', 'another, on the same saved trials', SWAPPED[1])}{srow('ours', 'ours, on our own saved trials', A18)}    </tbody>
  </table>
  <p class="note">the same command each time{STAND_IN}</p>''', [
    {"type": "focus", "target": "e1", "at": "5~one failed", "color": "red"},
    {"type": "focus", "target": "e2", "at": "5~one passed", "color": "green"},
    {"type": "focus", "target": "ours", "at": "6", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "7"}],
    css=TABLE + '.swapped{font-size:36px}.swapped td{padding-top:30px;padding-bottom:30px}')

framed('s22', EB4, 'The check ignores cost', f'''<div class="cols wide terms">
    {block("ours", "structure", tk(A17['tok']), f"Ours · tokens per trial, range {tk(A17['tok_lo'])} to {tk(A17['tok_hi'])}, below zero")}
    {block("tokens", "attention", tk(ET['tok']), f"An earlier run · tokens per trial, range {tk(ET['tok_lo'])} to {tk(ET['tok_hi'])}, above zero")}
    {block("exit", "success", str(ET['exit']), "That earlier run’s exit code · the check passed")}
  </div>
  <p class="note">{mono(T)}, before the edit against after it · the earlier run judged other saved trials</p>''', [
    {"type": "focus", "target": "ours", "at": "1", "color": "blue"},
    {"type": "focus", "target": "tokens", "at": "2~eleven thousand", "color": "yellow"},
    {"type": "focus", "target": "exit", "at": "2~exited", "color": "green"},
    {"type": "focus", "target": "none", "at": "3"}], css=THIRDS)

framed('s23', EB4, 'One reports, one can fail', f'''<div class="annotated">
    {code('vally experiment run … ⟦rep:--compare⟧\n\nvally compare &lt;folder&gt; ⟦gate:--fail-on-regression⟧'.replace('&lt;', '<').replace('&gt;', '>'), 'bash', 'two')}
    {callouts(('rep', 'judges every variant against the baseline, and reports'), ('gate', 'the step that can fail'))}
  </div>
  <p class="note">Source: Vally docs, “Run Your First Experiment”</p>''', [
    {"type": "focus", "target": "rep", "at": "0~dash dash compare", "color": "blue"},
    {"type": "focus", "target": "gate", "at": "2~fail on regression", "color": "yellow"}],
    css='.code.dark.two{min-width:1000px;font-size:36px;line-height:1.6}.callout{font-size:32px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Mean score below zero', 'the treatment was judged worse'),
    ('Whole range below zero', 'not only the mean'),
    ('Not counted', 'tokens · grader flips')], 1))
framed('s24', 'Recap', 'When does the check fail?', f'''<div class="semantic-block" id="gate" data-role="structure">
    <div class="title words">exit code 1, with {mono("--fail-on-regression")}</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#gate", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "red"},
    {"type": "focus", "target": "p2", "at": "2", "color": "red"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"}], layout='layout-expand',
    css='#gate{width:100%;padding:36px 40px 44px;gap:24px}'
        '#gate .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#gate .part{min-height:280px}#gate .part .title{font-size:44px;line-height:1.2}'
        '#gate .part .label{font-size:32px}')

scene('s25', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">When a run goes wrong</h1>
  <p class="lead">When a run goes wrong, where do you look first?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “CLI: compare”</p>
</main>''', [], css='.scene-title.chapter{font-size:116px}')
print('ok', RUN, '(PROVISIONAL: stand-in run)' if PROVISIONAL else '(our run)')
