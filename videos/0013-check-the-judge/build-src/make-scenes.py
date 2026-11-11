"""Generate lesson 13's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
real text in a dark box, numbers in a .data-table, terms in .semantic-block. Nothing here sets a
colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

This lesson records nothing: its checkpoint is counting. Everything it counts is read from src/run/:
  src/run/trials.tsv          one row per trial of the series' own lesson 12 run, tab-separated, with a
                              header: stimulus, model, trial, entry (pull request number left off),
                              ours (yes|no, written before the judge ran), judge (yes|no),
                              our_reason, judge_reason (the judge's reason, verbatim)
  src/run/wording-labels.md   notes/wording-labels.md as the lesson 12 video left it (no decision yet)
  src/run/decision.txt        the decision we wrote from this run's two rates and its one disagreement
  src/wording.eval.yaml       the eval file from the demo folder, for the criterion's exact words

The four boxes, TPR, TNR and every figure on screen are computed here from trials.tsv. Each number
the narration states is asserted below; if the run changes, the assert names the sentences to reword.

It writes src/state/wording-labels.md: the notes file as this lesson leaves it (the run's file plus
the decision as its last line). s16 shows it, and it is what belongs in practice/notes afterwards.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import csv, html, json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
SHORT = {'claude-haiku-4.5': 'haiku', 'gpt-5.6-terra': 'terra'}   # as the notes file names them


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


def card(cid, who, body):
    return f'''<div class="card" data-concept="{cid}" data-rep="card">
        <div class="who">{who}</div>
        {body}
      </div>'''


def mono(t):
    return f'<span class="mono">{t}</span>'


def note_span(cid, text):
    return f'<span data-concept="{cid}" data-rep="note">{text}</span>'


def pct(a, b):
    return int(100 * a / b + 0.5)    # halves round up, as the lesson page does (5 of 8 is 63%)


# ---- The run, read from src/run/ -----------------------------------------------------------------
with open(D / 'src/run/trials.tsv', newline='') as f:
    T = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
assert T and set(T[0]) == {'stimulus', 'model', 'trial', 'entry', 'ours', 'judge', 'our_reason', 'judge_reason'}, T[0].keys()
assert all(t['ours'] in ('yes', 'no') and t['judge'] in ('yes', 'no') and t['model'] in SHORT for t in T)
name = lambda t: f"{t['stimulus']}, {SHORT[t['model']]}, {t['trial']}"          # as in the notes file
BOX = {(j, o): [t for t in T if t['judge'] == j and t['ours'] == o] for j in ('yes', 'no') for o in ('yes', 'no')}
YY, YN, NY, NN = (len(BOX[k]) for k in (('yes', 'yes'), ('yes', 'no'), ('no', 'yes'), ('no', 'no')))
N, N_YES, N_NO = len(T), YY + NY, YN + NN
assert N_YES and N_NO, 'a rate needs at least one label of each kind'
TPR, TNR = pct(YY, N_YES), pct(NN, N_NO)
DISAGREE = BOX[('yes', 'no')] + BOX[('no', 'yes')]

# The notes file must be the same twelve rows: entry, ours, judge.
notes = (D / 'src/run/wording-labels.md').read_text()
rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in notes.splitlines() if l.startswith('|')][2:]
assert [(r[0], r[2], r[3]) for r in rows] == [(name(t), t['ours'], t['judge']) for t in T], 'wording-labels.md and trials.tsv differ'
assert all(r[1] == t['entry'] for r, t in zip(rows, T)), 'an entry differs between wording-labels.md and trials.tsv'

# ---- What the narration says about this run. If the run changes, these sentences change too. -----
clean = lambda r: r.replace('\\"', '"')       # the tool prints some quotes escaped; shown as plain quotes
AGREE = pct(YY + NN, N)
assert N == 12, 'hook, s10, s12, s13, s16, s17, s20 and the chapter title say twelve'
assert (YY, YN, NY, NN) == (7, 1, 0, 4), f's12 sentences 1-2, s13 sentences 1-3, s16 sentence 1: boxes are {(YY, YN, NY, NN)}'
assert (N_YES, N_NO) == (7, 5), 's13 sentences 1-2, s16 sentence 1, s17 sentence 3'
assert (TPR, TNR, AGREE) == (100, 80, 92), 's13 sentences 1-3, s17 sentence 2'
# s10, s15, s15b: one disagreement, judge yes and ours no, and its near twin where both said no.
assert len(DISAGREE) == 1, 's10 sentence 2, s15 sentence 0'
DIS = DISAGREE[0]
assert (DIS['judge'], DIS['ours']) == ('yes', 'no'), 's10 sentence 4, s12 sentence 2'
TWIN = next(t for t in T if (t['stimulus'], t['model']) == (DIS['stimulus'], DIS['model']) and t is not DIS)
assert (TWIN['judge'], TWIN['ours']) == ('no', 'no'), 's15 sentences 3-4'
HOW = 'by caching the tag index'
assert HOW in DIS['entry'] and HOW in TWIN['entry'], 's15 sentence 2'
assert set(DIS['entry'].split()) ^ set(TWIN['entry'].split()) == {'note'}, 's15 sentence 1: the two entries differ by one word'
assert DIS['our_reason'] == TWIN['our_reason'] and DIS['our_reason'].startswith('hesitated'), 's15 sentence 3'
assert 'states the implementation' in TWIN['judge_reason'], 's15 sentence 4, s15b sentence 2'
assert 'minor blemish' in DIS['judge_reason'], 's15 sentence 5'
assert int(TWIN['trial']) < int(DIS['trial']), 's15 says "the first" and "the second"'
ONE = 100 // N_NO
assert (NN, N_NO, ONE) == (4, 5, 20), 's17 sentence 3 and headline: one no label is worth 20 points'
ALL_YES = (N_YES, N_NO, 0, 0)       # s18: the same labels, under a judge that passes everything
lines = (D / 'src/wording.eval.yaml').read_text().splitlines()
i = next(k for k, l in enumerate(lines) if l.strip() == 'rubric:')
RUBRIC = ' '.join(l.strip().lstrip('- ') for l in lines[i + 1:i + 3])
assert RUBRIC.endswith('does not say how it was coded.'), RUBRIC

# ---- The notes file as this lesson leaves it ------------------------------------------------------
DECISION = (D / 'src/run/decision.txt').read_text().strip()
assert '\n' not in DECISION
assert f'On {N} labels ({N_YES} yes, {N_NO} no) the judge matched {YY + NN}: TPR {TPR}%, TNR {TNR}%.' in DECISION, 'decision.txt and the counts differ (s16)'
(D / 'src/state').mkdir(exist_ok=True)
(D / 'src/state/wording-labels.md').write_text(notes.rstrip('\n') + '\n\n' + DECISION + '\n')

# ---- The four boxes ------------------------------------------------------------------------------
GRID_CSS = ('.four{font-size:56px}.four th{font-size:32px;padding-bottom:16px}'
            '.four td{padding-top:22px;padding-bottom:22px}.four td:first-child{font-size:38px;padding-right:90px}'
            '.four td:first-child{white-space:nowrap;width:300px}.four td.num,.four th.num{width:40%}'
            '.four tr.total td{font-size:34px;color:var(--ink-soft)}.four tr.total td.num{font-size:38px}'
            '.four tr.rate td{font-size:34px}.four tr.rate td.num{font-size:40px}'
            '.four .means{font:400 34px/1.3 var(--font-body);color:var(--ink)}'
            '.stage{justify-content:flex-start;gap:30px}')


def cell(cid, text, p=''):
    return f'<td class="num"><span data-concept="{p}{cid}" data-rep="cell">{text}</span></td>'


def grid(counts, p='', totals=False, rates=False, cells=None, extra='', short=False):
    """The two-by-two table. counts = (yy, yn, ny, nn); cells overrides what each box holds."""
    yy, yn, ny, nn = counts
    c = cells or {k: str(v) for k, v in zip(('yy', 'yn', 'ny', 'nn'), counts)}
    out = f'''<table class="data-table full four {extra}">
    <thead><tr><th></th><th class="num">Ours: yes</th><th class="num">Ours: no</th></tr></thead>
    <tbody>
      <tr><td>Judge: yes</td>{cell('yy', c['yy'], p)}{cell('yn', c['yn'], p)}</tr>
      <tr><td>Judge: no</td>{cell('ny', c['ny'], p)}{cell('nn', c['nn'], p)}</tr>
'''
    if totals:
        out += f'''      <tr class="total"><td>labels</td>{cell('tot-yes', yy + ny, p)}{cell('tot-no', yn + nn, p)}</tr>\n'''
    if rates:
        tpr = f'TPR · {pct(yy, yy + ny)}%' if short else f'TPR · {yy} of {yy + ny} · {pct(yy, yy + ny)}%'
        tnr = f'TNR · {pct(nn, yn + nn)}%' if short else f'TNR · {nn} of {yn + nn} · {pct(nn, yn + nn)}%'
        out += f'''      <tr class="rate"><td>rate</td>{cell('tpr', tpr, p)}{cell('tnr', tnr, p)}</tr>\n'''
    return out + '    </tbody>\n  </table>'


# ---- Hook ----------------------------------------------------------------------------------------
H = next(t for t in T if t['ours'] == 'no' and t['judge'] == 'no')      # one entry, its verdict and ours
framed('s01', 'Vally &amp; Agent Evals', 'Check the judge', f'''<div class="hook">
    {card('entry', f'one of the twelve entries · {mono(name(H))}', code(H['entry'], 'markdown'))}
    <div class="cols">
      {block('judge-b', 'attention', f"Judge: {H['judge']}", html.escape(clean(H['judge_reason'])), words=True)}
      {block('ours-b', 'structure', f"Ours: {H['ours']}", 'written down before the judge ran', words=True)}
    </div>
  </div>''', [
    {"type": "focus", "target": "judge-b", "at": "0~reason", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "ours-b", "at": "3~our own", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.hook{display:flex;flex-direction:column;gap:30px;width:100%}'
        '.hook .card > .code.dark{font-size:29px;padding:24px 28px;flex:none}.hook .card .who{font-size:30px}'
        '.hook .semantic-block .label{font-size:30px;line-height:1.35}.hook .cols{grid-auto-columns:auto;grid-template-columns:3fr 2fr}')

# ---- Chapter: A judge is measured ----------------------------------------------------------------
TERMS = '.terms .semantic-block{min-height:260px}.terms .label{font-size:34px}'
framed('s02', 'A judge is measured', 'Wrong in two directions', f'''<div class="cols wide terms">
    {block("slip", "failure", "Judge says yes · we’d say no", "a failure slips through: the skill looks better than it is", words=True)}
    {block("alarm", "attention", "Judge says no · we’d say yes", "a false alarm: we hunt for a problem that isn’t there", words=True)}
  </div>''', [
    {"type": "focus", "target": "slip", "at": "2", "color": "red"},
    {"type": "focus", "target": "alarm", "at": "3", "color": "yellow"}], css=TERMS)

MARK = {'y': ('tick', '✔'), 'n': ('cross', '✘')}
row20 = lambda cid, label, marks: (
    f'<div class="trow" data-concept="{cid}" data-rep="row"><span class="who">{label}</span><span class="boxes">'
    + ''.join(f'<span class="box {MARK[m][0]}">{MARK[m][1]}</span>' for m in marks) + '</span></div>')
framed('s03', 'A judge is measured', 'Agreement hides the direction', f'''<div class="rows">
    {row20('labels-row', 'our labels', 'y' * 18 + 'n' * 2)}
    {row20('judge-row', 'a judge that always says yes', 'y' * 20)}
  </div>
  <div class="cols wide figs">
    {block("agree", "structure", "18 of 20", "agree · 90%")}
    {block("caught", "failure", "0 of 2", "bad entries caught")}
  </div>
  <p class="note">An invented example · ✔ is a yes, ✘ is a no</p>''', [
    {"type": "focus", "target": "labels-row", "at": "2", "color": "blue"},
    {"type": "focus", "target": "judge-row", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "agree", "at": "3~eighteen times", "color": "blue"},
    {"type": "focus", "target": "caught", "at": "4", "color": "red"},
    {"type": "focus", "target": "agree", "at": "5~agreement", "color": "blue"}],
    css='.rows{display:flex;flex-direction:column;gap:10px;width:100%}'
        '.trow{display:flex;align-items:center;gap:30px;padding:10px 18px;border-radius:10px;width:fit-content}'
        '.boxes{display:flex;gap:8px}'
        '.box{display:flex;align-items:center;justify-content:center;width:54px;height:54px;border-radius:7px;'
        'border:3px solid var(--ink-muted);font:700 32px/1 var(--font-body);color:var(--ink)}'
        '.box.tick{color:var(--green-ink)}.box.cross{color:var(--red-ink)}'
        '.trow .who{font:500 32px/1.2 var(--font-body);color:var(--ink);width:330px}'
        '.figs .semantic-block{min-height:150px;justify-content:center}.figs .title{font-size:64px}.figs .label{font-size:34px}'
        '.stage{gap:26px}')

framed('s04', 'A judge is measured', 'Two counts, not one', f'''<div class="cols wide terms">
    {block("q-yes", "structure", "Of our yes labels", "how many did the judge pass?", words=True)}
    {block("q-no", "structure", "Of our no labels", "how many did the judge fail?", words=True)}
  </div>
  <p class="lead">{note_span('aim', 'Aim above 90% on each, from 100 or more labels, for a judge to depend on.')}</p>
  <p class="note">Sources: Husain and Shankar, validate-evaluator skill · AI Evals FAQ (2026)</p>''', [
    {"type": "focus", "target": "q-yes", "at": "1", "color": "blue"},
    {"type": "focus", "target": "q-no", "at": "2", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "aim", "at": "5~ninety", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "6"}],
    css='.terms .semantic-block{min-height:220px}.terms .label{font-size:38px}.lead{font-size:40px;margin:0}.stage{gap:34px}')

framed('s05', 'A judge is measured', 'Three changes undo it', f'''<div class="cols terms">
    {block("c1", "change", "the rubric’s wording", "change it, and we label again", words=True)}
    {block("c2", "change", "the judge model", "change it, and we label again", words=True)}
    {block("c3", "change", "the kind of request", "change it, and we label again", words=True)}
  </div>
  <p class="lead">{note_span('aside', 'While a rubric is reworded, some labelled entries stay aside, unread.')}</p>''', [
    {"type": "focus", "target": "c1", "at": "1~rubric's wording", "color": "orange"},
    {"type": "focus", "target": "c2", "at": "1~judge model", "color": "orange"},
    {"type": "focus", "target": "c3", "at": "1~different kind", "color": "orange"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "aside", "at": "3~aside", "color": "blue"}],
    css='.terms .semantic-block{min-height:240px}.terms .label{font-size:32px}.lead{font-size:40px;margin:0}.stage{gap:40px}')

# ---- Chapter: TPR and TNR ------------------------------------------------------------------------
framed('s06', 'TPR and TNR', 'Two rates, two names', f'''<div class="cols wide rates">
    <div class="semantic-block" data-concept="tpr" data-rep="block" data-role="structure">
      <div class="title">TPR</div><div class="label full">true positive rate</div>
      <div class="label">of the trials we labelled yes, the share the judge also passed</div>
    </div>
    <div class="semantic-block" data-concept="tnr" data-rep="block" data-role="structure">
      <div class="title">TNR</div><div class="label full">true negative rate</div>
      <div class="label">of the trials we labelled no, the share the judge also failed</div>
    </div>
  </div>
  <p class="lead">{note_span('pos', 'positive is a yes')} · {note_span('neg', 'negative is a no')}</p>''', [
    {"type": "focus", "target": "tpr", "at": "1", "color": "blue"},
    {"type": "focus", "target": "pos", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "tnr", "at": "3", "color": "blue"},
    {"type": "focus", "target": "neg", "at": "4", "color": "yellow"}],
    css='.rates .semantic-block{min-height:300px}.rates .title{font-size:72px}'
        '.rates .label.full{font-size:40px;color:var(--ink);font-weight:600}.rates .label{font-size:34px}'
        '.lead{font-size:38px;margin:0}.stage{gap:36px}')

INVENTED = (11, 3, 1, 5)
INV_NOTE = '<p class="note">An invented judge, to show the arithmetic · 20 labelled entries</p>'
framed('s07', 'TPR and TNR', 'Every trial, one box', grid(INVENTED, totals=True) + '\n  ' + INV_NOTE, [
    {"type": "focus", "target": "tot-yes", "at": "2~twelve yes", "color": "blue"},
    {"type": "focus", "target": "tot-no", "at": "2~eight no", "color": "blue"},
    {"type": "focus", "target": "yy", "at": "3~eleven", "color": "green"},
    {"type": "focus", "target": "yn", "at": "3~three", "color": "red"},
    {"type": "focus", "target": "ny", "at": "4~one of", "color": "yellow"},
    {"type": "focus", "target": "nn", "at": "4~five", "color": "green"}], css=GRID_CSS)

framed('s08', 'TPR and TNR', 'Each rate reads one column', grid(INVENTED, totals=True, rates=True) + f'''
  <p class="lead">{note_span('agree', 'agreement · 16 of 20 · 80%')}</p>''', [
    {"type": "focus", "target": "tpr", "at": "1", "color": "blue"},
    {"type": "focus", "target": "tnr", "at": "2", "color": "blue"},
    {"type": "focus", "target": "agree", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "tnr", "at": "4", "color": "red"}],
    css=GRID_CSS + '.lead{font-size:40px;margin:0;font-family:var(--font-code);color:var(--ink)}.stage{gap:22px}')

framed('s09', 'TPR and TNR', 'What a low rate means', f'''<div class="cols wide rates">
    <div class="semantic-block" data-concept="low-tpr" data-rep="block" data-role="attention">
      <div class="title">low TPR</div><div class="label full">false alarms</div>
      <div class="label">the judge is stricter than we are</div>
    </div>
    <div class="semantic-block" data-concept="low-tnr" data-rep="block" data-role="failure">
      <div class="title">low TNR</div><div class="label full">missed failures</div>
      <div class="label">the judge is more lenient than we are</div>
    </div>
  </div>''', [
    {"type": "focus", "target": "low-tpr", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "low-tnr", "at": "2", "color": "red"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.rates .semantic-block{min-height:300px}.rates .title{font-size:64px}'
        '.rates .label.full{font-size:44px;color:var(--ink);font-weight:600}.rates .label{font-size:36px}')

# ---- Chapter: Count, compare, decide -------------------------------------------------------------
means = lambda t: f'<span class="means">{t}</span>'
framed('s10', 'Count, compare, decide', 'Twelve trials, four boxes', grid((0, 0, 0, 0), cells={
    'yy': means('both say yes'), 'yn': means('a failure slips through'),
    'ny': means('a false alarm'), 'nn': means('both say no')}, extra='empty') + f'''
  <p class="note">our {N} trials · no agent runs, no judge calls</p>''', [
    {"type": "focus", "target": "yy", "at": "1~four boxes", "color": "blue"},
    {"type": "focus", "target": "nn", "at": "1~both rates", "color": "blue"},
    {"type": "focus", "target": "yn", "at": "2~differ", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "yn", "at": "4~judge said yes", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css=GRID_CSS + '.four.empty td{padding-top:44px;padding-bottom:44px}')

framed('s11', 'Count, compare, decide', 'Both lists, side by side', panel('labels'), [
    {"type": "focus", "target": "ours", "at": "1~our yes", "color": "blue"},
    {"type": "focus", "target": "judge", "at": "1~judge's", "color": "yellow"},
    {"type": "focus", "target": "ours", "at": "2", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2~haven't"},
    {"type": "scroll", "target": "#labels", "to": "end", "at": "2~changed"}], layout='layout-file')


def chips(k):
    ts = BOX[k]
    return (f'<span class="count">{len(ts)}</span>'
            + ('<span class="chips">' + ''.join(f'<span class="chip">{name(t)}</span>' for t in ts) + '</span>' if ts else ''))


framed('s12', 'Count, compare, decide', 'Twelve trials, sorted', grid((YY, YN, NY, NN), cells={
    'yy': chips(('yes', 'yes')), 'yn': chips(('yes', 'no')), 'ny': chips(('no', 'yes')), 'nn': chips(('no', 'no'))},
    extra='sorted') + '''
  <p class="note">each trial is named as in the notes file: stimulus, model, trial</p>''', [
    {"type": "focus", "target": "yy", "at": "1~yes from both", "color": "green"},
    {"type": "focus", "target": "nn", "at": "1~no from both", "color": "green"},
    {"type": "focus", "target": "yn", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "ny", "at": "2~last box", "color": "blue"}],
    css=GRID_CSS + '.sorted td{vertical-align:top;padding-top:12px;padding-bottom:12px}'
        '.sorted td.num > span{display:inline-flex;flex-direction:column;align-items:flex-end;gap:6px;padding:6px 14px}'
        '.sorted .count{font-size:52px;line-height:1}'
        '.sorted .chips{display:grid;grid-template-columns:auto auto;gap:2px 34px}'
        '.sorted .chip{font:400 28px/1.22 var(--font-code);color:var(--ink-soft);white-space:nowrap}'
        '.sorted td:first-child{vertical-align:top;padding-top:24px}.stage{gap:12px}')

framed('s13', 'Count, compare, decide', 'Both rates, from our counts', grid((YY, YN, NY, NN), totals=True, rates=True) + f'''
  <p class="lead">{note_span('agree', f'agreement · {YY + NN} of {N} · {AGREE}%')}</p>
  <p class="note">{note_span('rough', f'from {N} labels · both rates are rough')}</p>''', [
    {"type": "focus", "target": "tpr", "at": "1", "color": "blue"},
    {"type": "focus", "target": "tnr", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "agree", "at": "3", "color": "blue"},
    {"type": "focus", "target": "rough", "at": "4", "color": "yellow"}],
    css=GRID_CSS + '.lead{font-size:40px;margin:0;font-family:var(--font-code);color:var(--ink)}.note{font-size:34px}.stage{gap:20px}')

framed('s14', 'Count, compare, decide', 'A disagreement gets examined', f'''<div class="cols pair">
    {block("again", "structure", "For each disagreement", "read the entry and the judge’s reason again, and decide who is right", words=True)}
    <div class="cases">
      {block("still", "failure", "We still disagree", "one error of the judge’s", words=True)}
      {block("persuaded", "attention", "The judge persuaded us", "our criterion wasn’t what we thought", words=True)}
    </div>
  </div>
  <p class="lead">{note_span('stays', 'Either way, the label stays as first written, and the entry counts as a disagreement.')}</p>''', [
    {"type": "focus", "target": "again", "at": "1", "color": "blue"},
    {"type": "focus", "target": "still", "at": "2", "color": "red"},
    {"type": "focus", "target": "persuaded", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "stays", "at": "4", "color": "blue"},
    {"type": "focus", "target": "none", "at": "6"}],
    css='.pair{align-items:stretch}.cases{display:flex;flex-direction:column;gap:22px;justify-content:center}'
        '.cases .semantic-block{min-height:150px;justify-content:center}.pair .label{font-size:34px}'
        '.pair > .semantic-block{justify-content:center}.lead{font-size:38px;margin:0}.stage{gap:34px}')

# s15 and s15b: the one disagreement and its near twin, from the run.
pair_code = code('\n'.join(
    f"{t['trial']}  " + t['entry'].replace(HOW, f'⟦how:{HOW}⟧').replace('large note folders', 'large ⟦word:note⟧ folders')
    for t in (TWIN, DIS)), 'text')
pair_who = f"{mono(DIS['stimulus'])} · {mono(DIS['model'])} · the entry from each of its two trials"
ours_both = note_span('ours', f"ours, for both: no · {html.escape(DIS['our_reason'])}")
HES_CSS = ('.hes{display:flex;flex-direction:column;gap:24px;width:100%}'
           '.hes .card > .code.dark{font-size:32px;line-height:1.6;padding:20px 30px;flex:none}.hes .card .who{font-size:30px}'
           '.hes .ours{font:400 32px/1.3 var(--font-body);color:var(--ink);margin:0}'
           '.hes .semantic-block .title{font-size:34px}.hes .semantic-block .label{font-size:28px;line-height:1.35}'
           '.stage{justify-content:flex-start}')
verdict = lambda cid, t, role: block(cid, role, f"The judge, trial {t['trial']} · {t['judge']}",
                                     html.escape(clean(t['judge_reason'])), words=True)
framed('s15', 'Count, compare, decide', 'One word apart, two verdicts', f'''<div class="hes">
    {card('pair', pair_who, pair_code)}
    <p class="ours">{ours_both}</p>
    <div class="cols">
      {verdict('j0', TWIN, 'structure')}
      {verdict('j1', DIS, 'attention')}
    </div>
  </div>''', [
    {"type": "focus", "target": "word", "at": "1~single word", "color": "yellow"},
    {"type": "focus", "target": "how", "at": "2~caching", "color": "yellow"},
    {"type": "focus", "target": "ours", "at": "3", "color": "blue"},
    {"type": "focus", "target": "j0", "at": "4", "color": "blue"},
    {"type": "focus", "target": "j1", "at": "5", "color": "yellow"}], css=HES_CSS)

framed('s15b', 'Count, compare, decide', 'One error of the judge’s', f'''<div class="hes">
    {card('pair', pair_who, pair_code)}
    <div class="cols">
      {block('crit', 'structure', 'The criterion', html.escape(RUBRIC), words=True)}
      {block('still', 'failure', 'We still disagree', 'the judge said no to one entry, and yes to its near twin', words=True)}
      {block('stays', 'structure', 'Our label stays', 'no, as first written, with our hesitation on record', words=True)}
    </div>
  </div>''', [
    {"type": "focus", "target": "crit", "at": "1", "color": "blue"},
    {"type": "focus", "target": "how", "at": "1~caching", "color": "yellow"},
    {"type": "focus", "target": "still", "at": "3", "color": "red"},
    {"type": "focus", "target": "none", "at": "4"},
    {"type": "focus", "target": "stays", "at": "5", "color": "blue"}],
    css=HES_CSS + '.hes .semantic-block{min-height:230px}.hes .semantic-block .label{font-size:30px}')

framed('s16', 'Count, compare, decide', 'The decision, written down', panel('decided'), [
    {"type": "scroll", "target": "#decided", "to": "end", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "decision", "at": "1", "color": "blue"}], layout='layout-file')

# ---- Chapter: What twelve labels show ------------------------------------------------------------
framed('s17', 'What twelve labels show', f'One entry is {ONE} points', f'''<div class="cols wide figs">
    {block("now", "attention", f"{NN} of {N_NO} · {TNR}%", "TNR in our run, with its one miss")}
    {block("other", "success", f"{N_NO} of {N_NO} · 100%", "TNR had that one entry gone the other way")}
  </div>
  <p class="lead">{note_span('cant', f'{N} labels can’t tell a judge that’s right 99% of the time from one that’s right 85% of the time.')}</p>''', [
    {"type": "focus", "target": "now", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "other", "at": "3~hundred", "color": "green"},
    {"type": "focus", "target": "cant", "at": "4", "color": "blue"}],
    css='.figs .semantic-block{min-height:260px;justify-content:center}.figs .title{font-size:76px;line-height:1.1}'
        '.figs .label{font-size:36px}.lead{font-size:38px;margin:0}.stage{gap:40px}')

SMALL = ('.two{display:grid;grid-template-columns:1fr 1fr;gap:70px;width:100%}'
         '.two .card .who{font-size:32px}'
         '.two .four{font-size:48px;width:100%}.two .four th{font-size:28px}.two .four td{padding:14px 20px 14px 0}'
         '.two .four td:first-child{font-size:32px;padding-right:20px;width:190px}'
         '.two .four tr.rate td{font-size:30px}.two .four tr.rate td.num{font-size:38px}.stage{justify-content:center}')
framed('s18', 'What twelve labels show', 'Still a real result', f'''<div class="two">
    {card('ours-t', 'our judge', grid((YY, YN, NY, NN), p='a-', rates=True, short=True))}
    {card('all-t', 'a judge that passes everything, on the same labels', grid(ALL_YES, p='b-', rates=True, short=True))}
  </div>''', [
    {"type": "focus", "target": "b-tnr", "at": "1~zero", "color": "red"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "a-tnr", "at": "4", "color": "yellow"}], css=GRID_CSS + SMALL)

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('TPR · 100%', 'it passed all 9 entries we labelled yes'),
    ('TNR · 0%', 'it passed the 1 entry we labelled no'),
    ('agreement · 90%', '9 of 10, which hides both')], 1))
framed('s19', 'Recap', 'A judge that always says yes', f'''<div class="semantic-block" id="always" data-role="structure">
    <div class="title words">yes to every trial · we labelled nine yes, and one no</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#always", "at": "2"},
    {"type": "focus", "target": "p1", "at": "2", "color": "green"},
    {"type": "focus", "target": "p2", "at": "3", "color": "red"},
    {"type": "focus", "target": "p3", "at": "4", "color": "yellow"}], layout='layout-expand',
    css='#always{width:100%;padding:36px 40px 44px;gap:24px}'
        '#always .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#always .part{min-height:260px}#always .part .title{font-size:50px;line-height:1.2}'
        '#always .part .label{font-size:32px}')

scene('s20', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Partial credit</h1>
  <p class="lead">Can a grader give partial credit without hiding a failure?</p>
  <p class="note">Exercises are on the lesson page · Source: Husain and Shankar, validate-evaluator skill</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', dict(boxes=(YY, YN, NY, NN), TPR=TPR, TNR=TNR))
