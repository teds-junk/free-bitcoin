"""Generate lesson 14's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 4: the theme's one frame (eyebrow, short display-serif headline, .stage),
code, files and console output in a dark box on the left with notes on the right (.annotated +
.callout), numbers in a .data-table, terms in .semantic-block. Nothing here sets a colour or a font
outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/wording.eval.yaml                       the judge's eval file as lesson 13 leaves it
  src/state/wording-scaled.eval.yaml          the copy with the judge on a scale (verified/lesson-14);
                                              s15.tape and s16.tape install it out of sight
  src/state/wording-scaled.scoring.eval.yaml  the same with the scoring block at its end; s19.tape
                                              installs it out of sight, then puts the first one back
  src/run/trials.tsv                 one row per trial of the series' own lesson 12 run, tab-separated,
                                     with a header: stimulus, model, trial, entry (pull request number
                                     left off), ours (yes|no), judge (yes|no), ... (the lesson 13
                                     video's file, as it is)
  src/run/wording-labels.before.md   notes/wording-labels.md as the lesson 13 video leaves it
  src/run/s15-lint.log               what s15.tape's vally lint printed   (/tmp/vl-l14/s15-lint.log)
  src/run/s16-grade.log              the first re-grade, no scoring block (/tmp/vl-l14/s16-grade.log)
  src/run/s19-lint.log               lint with the scoring block          (/tmp/vl-l14/s19-lint.log)
  src/run/s19-grade.log              the second re-grade, with it         (/tmp/vl-l14/s19-grade.log)
  src/run/sentence.txt               the one sentence we add to the notes file (ours to write)
  src/run/PROVISIONAL                present while the above are stand-ins from verified/lesson-12..14

Written here: src/state/notes/wording-labels.md, the notes file as the lesson leaves it (the labels
file plus a "1 to 5" column from the first re-grade, plus the sentence). s19.tape copies it into
practice/notes/ out of sight, so run this again after s16 is recorded and before s19 is.

The logs may be raw `script` typescripts: colour codes and carriage returns are stripped here.
The asserts below are what the narration says about the run. If the video's own run differs, an
assert fails and names the scenes to reword; change the sentences, then the assert.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess, textwrap

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
SHORT = {'claude-haiku-4.5': 'haiku', 'gpt-5.6-terra': 'terra'}
STIMS = ('parser', 'cache', 'dates')
JUDGE_THRESHOLD, TRIAL_THRESHOLD = 0.75, 0.6


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
    (D / 'scenes').mkdir(exist_ok=True)
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


def quote(cid, who, text):
    return f'''<div class="quote" data-concept="{cid}" data-rep="quote"><span class="who">{who}</span><p>{text}</p></div>'''


def mono(t):
    return f'<span class="mono">{t}</span>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>'


def wrap_marked(line, width, marks=(), indent='    '):
    """A real line, wrapped for a dark box; continuation rows are indented. Each (id, phrase) in
    marks becomes a highlight target; the phrase is kept on one row."""
    for _, phrase in marks:
        assert line.count(phrase) == 1, (phrase, line)
        line = line.replace(phrase, phrase.replace(' ', '\x00'))
    lead = len(line) - len(line.lstrip(' '))
    rows = textwrap.wrap(line.strip(), width - lead, subsequent_indent=indent,
                         break_long_words=False, break_on_hyphens=False)
    out = []
    for r in rows:
        r = ' ' * lead + r.replace('\x00', ' ')
        for cid, phrase in marks:
            r = r.replace(phrase, f'⟦{cid}:{phrase}⟧')
        out.append(r)
    return out


def tail(entry, n=50):
    """An entry shortened for a table: its last words, with an ellipsis where the start is cut."""
    if len(entry) <= n:
        return entry
    out = []
    for w in reversed(entry.split(' ')):
        if len(' '.join([w] + out)) + 1 > n:
            break
        out.insert(0, w)
    return '…' + ' '.join(out)


# ---- The real things, read from src/ -----------------------------------------------------------
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
WORDS = {3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven'}
SRC_NOTE = 'stand-in: the course’s verified run' if PROVISIONAL else 'from our run'
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x04\x08\r]')


def clean(name):
    return ANSI.sub('', (D / 'src/run' / name).read_text(errors='replace'))


def trials():
    lines = (D / 'src/run/trials.tsv').read_text().splitlines()
    head = lines[0].split('\t')
    assert head[:6] == ['stimulus', 'model', 'trial', 'entry', 'ours', 'judge'], head
    rows = [dict(zip(head, l.split('\t'))) for l in lines[1:] if l.strip()]
    assert len(rows) == 12 and all(r['ours'] in ('yes', 'no') and r['judge'] in ('yes', 'no') for r in rows)
    assert all(r['model'] in SHORT and r['stimulus'] in STIMS for r in rows)
    return rows


def parse_grade(name):
    """The blocks vally grade --verbose printed: one per trial, in the order printed."""
    blocks, cur = [], None
    for line in clean(name).splitlines():
        s = line.strip()
        m = re.match(r'^━+ (\S+) ━+$', s)
        if m:
            cur = {'stim': m.group(1), 'title': s, 'graders': []}
            blocks.append(cur)
            continue
        if cur is None or not s:
            continue
        h = re.match(r'^([✅❌]) (\S+) \((.*)\)$', s)
        g = re.match(r'^([✓✗]) \[(.+?)\] (.*)$', s)
        sc = re.match(r'^Score: ([\d.]+)% \| (PASSED|FAILED)(.*)$', s)
        if h:
            cur['ok'], cur['head'] = h.group(1) == '✅', s
        elif g:
            cur['graders'].append({'ok': g.group(1) == '✓', 'label': g.group(2), 'text': g.group(3), 'line': '  ' + s})
        elif sc:
            cur['score'], cur['scoreline'] = float(sc.group(1)), s
            assert (sc.group(2) == 'PASSED') == cur['ok'], s
    for b in blocks:
        judge = [g for g in b['graders'] if g['label'].startswith('prompt')]
        check = [g for g in b['graders'] if g['label'].startswith('cites-')]
        assert len(judge) == 1 and len(check) == 1 and 'score' in b and 'ok' in b, b
        b['judge'], b['check'] = judge[0], check[0]
    return blocks


def match(blocks, rows):
    """Which row each block belongs to. The blocks name neither model nor trial, so match by the
    entry the judge's reason quotes; a block that quotes none takes the row left over."""
    out = {}
    for stim in STIMS:
        bi = [i for i, b in enumerate(blocks) if b['stim'] == stim]
        free = [j for j, r in enumerate(rows) if r['stimulus'] == stim]
        assert len(bi) == len(free), (stim, len(bi), len(free))
        pending = []
        for i in bi:
            reason = blocks[i]['judge']['text'].replace('\\"', '"')
            hit = [j for j in free if rows[j]['entry'] + ' (#' in reason] or \
                  sorted((j for j in free if rows[j]['entry'] in reason), key=lambda j: -len(rows[j]['entry']))
            if hit:
                out[i] = hit[0]
                free.remove(hit[0])
            else:
                pending.append(i)
        for i, j in zip(pending, free):
            out[i] = j
    assert sorted(out.values()) == list(range(len(rows)))
    return out


def answer(b):
    """The judge's 1 to 5, worked out from the trial's score: the check scored 1, so the score is
    the average of 1 and the judge's rescaled score."""
    assert b['check']['ok'], 'a pull request check failed: the score-line table (s13) does not apply'
    a = (b['score'] / 100 * 2 - 1) * 4 + 1
    assert abs(a - round(a)) < 1e-6 and 1 <= round(a) <= 5, b['scoreline']
    return round(a)


ROWS = trials()


def attach(grading, key):
    """Give each row its block, and the judge's answer, from one grading."""
    for i, j in match(grading, ROWS).items():
        b = grading[i]
        ROWS[j]['b' + key], ROWS[j]['a' + key] = b, answer(b)                   # s13: every check passed
        assert b['judge']['ok'] == (ROWS[j]['a' + key] >= 4), b['scoreline']    # judge's threshold 0.75


G1 = parse_grade('s16-grade.log')
assert len(G1) == 12, len(G1)                                             # s16/3 twelve blocks
attach(G1, '1')
for r in ROWS:
    r['who'] = f"{r['stimulus']} · {SHORT[r['model']]}"
    r['pass1'] = r['b1']['ok']
    assert r['pass1'] == r['b1']['judge']['ok']                           # no scoring block: every grader

NO = [r for r in ROWS if r['ours'] == 'no']
YES = [r for r in ROWS if r['ours'] == 'yes']
FAR = [r for r in NO if r['a1'] <= 2]
NEAR = [r for r in NO if r['a1'] >= 3]
CHANGED = [r for r in ROWS if r['pass1'] != (r['judge'] == 'yes')]

# ---- What the narration says about this run: the labels and the first grading ---------------------
assert len(NO) == 5 and sum(r['judge'] == 'no' for r in ROWS) == 4        # s01/0 judge no to four, we to five
assert sum(r['judge'] == r['ours'] for r in ROWS) == 11                   # s14/3 agreed with eleven of twelve
assert len(FAR) == 3 and all(r['a1'] == 2 for r in FAR)                   # s18/2, s22 three entries, each a two
assert {r['a1'] for r in YES} == {4, 5}                                   # s18/3 "fours and fives"
assert len(NEAR) == 2 and all(r['a1'] == 4 for r in NEAR)                 # s18/4, s22 both got a four
assert len(CHANGED) == 1 and CHANGED[0] in NEAR                           # s18/5, s21/3, s23 one verdict changed
TP = sum(r['pass1'] for r in YES)
TN = sum(not r['pass1'] for r in NO)
TN_YESNO = sum(r['judge'] == 'no' for r in NO)
TN_DEFAULT = sum(r['a1'] < 3 for r in NO)
assert (TP, len(YES), TN, TN_YESNO) == (7, 7, 3, 4)                       # s21/4-5, s23/1 TPR 7 of 7; TNR 4 of 5 -> 3 of 5
assert TN_DEFAULT == TN and not any(r['a1'] == 3 for r in ROWS)           # s23/2 no entry got a three

lint1 = clean('s15-lint.log')
assert 'scoring-defaults-applied' in lint1 and 'error' not in lint1.lower()   # s15/3

SENTENCE = (D / 'src/run/sentence.txt').read_text().strip()
assert SENTENCE.startswith('One verdict changed') and f'TPR {TP} of {len(YES)}' in SENTENCE \
    and f'TNR {TN} of {len(NO)}' in SENTENCE, SENTENCE                        # s21

scaled = (D / 'src/state/wording-scaled.eval.yaml').read_text()
scored = (D / 'src/state/wording-scaled.scoring.eval.yaml').read_text()
assert scaled.count('scoring: scale_1_5') == 3 and scaled.count('threshold: 0.75') == 3 and 'binary' not in scaled
assert scored.startswith(scaled) and scored[len(scaled):].split() == \
    ['scoring:', 'weights:', 'prompt:', '0.5', 'diff-contains:', '0.5', 'threshold:', '0.6']
original = (D / 'src/wording.eval.yaml').read_text()
assert original.count('scoring: binary') == 3 and \
    scaled == original.replace('name: wording\n', 'name: wording-scaled\n', 1).replace(
        'scoring: binary', 'scoring: scale_1_5\n          threshold: 0.75')

# ---- The notes file as the lesson leaves it ------------------------------------------------------
notes = (D / 'src/run/wording-labels.before.md').read_text().rstrip('\n').splitlines()
hi = next(i for i, l in enumerate(notes) if l.startswith('| Stimulus'))
ri = [i for i, l in enumerate(notes) if l.startswith('| ') and i > hi + 1]
assert notes[hi + 1].startswith('|---') and len(ri) == 12, ri
notes[hi] += ' 1 to 5 |'
notes[hi + 1] += '---|'
for r, i in zip(ROWS, ri):
    assert r['entry'] in notes[i] and r['stimulus'] in notes[i], (r['entry'], notes[i])
    notes[i] += f" {r['a1']} |"
(D / 'src/state/notes').mkdir(parents=True, exist_ok=True)
(D / 'src/state/notes/wording-labels.md').write_text('\n'.join(notes + ['', SENTENCE]) + '\n')

if not (D / 'src/run/s19-grade.log').exists():
    print('notes file written from the first grading; s19 is not recorded yet, so no scenes were made')
    print('answers', ''.join(str(r['a1']) for r in ROWS))
    raise SystemExit(0)

# ---- The second grading, with the scoring block --------------------------------------------------
G2 = parse_grade('s19-grade.log')
assert len(G2) == 12, len(G2)
attach(G2, '2')
for r in ROWS:
    assert r['b2']['ok'] == (0.5 * (r['a2'] - 1) / 4 + 0.5 >= TRIAL_THRESHOLD)  # scoring block: the average
CROSSED = [r for r in ROWS if r['b2']['ok'] and not r['b2']['judge']['ok']]
FLIPPED = [r for r in ROWS if r['a1'] != r['a2']]
MARKED_DOWN = [r for r in YES if r['a1'] == 4]
lint2 = clean('s19-lint.log')
assert 'is valid' in lint2 and 'warning' not in lint2.lower()                 # s19/1
# ---- What the narration says about the second grading -------------------------------------------
assert all(r['b2']['ok'] for r in ROWS)                                # s19/4, s26/5 all twelve pass with the block
assert len(CROSSED) == 4 and all(r in NO for r in CROSSED)             # s20/4, s26/1 four passed with a cross
assert [r for r in CROSSED if r['b2']['score'] == 62.5] == FAR         # s20/3, s26 the three twos: 0.625
assert len(FLIPPED) == 1 and FLIPPED[0] in NEAR and (FLIPPED[0]['a1'], FLIPPED[0]['a2']) == (4, 3)   # s24/1-2
assert all(r['a2'] == 2 for r in FAR)                                  # s24/4 a two both times
DOWN = [r for r in MARKED_DOWN if 'more concrete' in r['b1']['judge']['text'] and 'date' in r['b1']['judge']['text']]
assert DOWN                                                            # s25/1-2 a yes entry, a four, "more concrete ... a date"


def entry_box(rows, width, extra):
    """Entries from our run in a dark box, one per paragraph, wrapped."""
    return code(('\n' if width > 90 else '\n\n').join('\n'.join(textwrap.wrap(r['entry'], width, subsequent_indent='  ',
                                                    break_long_words=False, break_on_hyphens=False)) for r in rows),
                'markdown', extra)


# ---- Hook ----------------------------------------------------------------------------------------
far, near = min(NO, key=lambda r: r['a1']), max(NO, key=lambda r: r['a1'])
assert far['a1'] < near['a1'] and far['judge'] == near['judge'] == 'no'       # s01/4 both got the same no
verdicts = 'our label: no · the judge: no'
framed('s01', 'Vally &amp; Agent Evals', 'Partial credit', f'''<div class="cols pair">
    {card('far', f"{mono(far['who'])} · {verdicts}", entry_box([far], 32, 'entry'))}
    {card('near', f"{mono(near['who'])} · {verdicts}", entry_box([near], 32, 'entry'))}
  </div>
  <p class="note">two of our twelve entries · {SRC_NOTE}</p>''', [
    {"type": "focus", "target": "far", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "near", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.pair{align-items:stretch;gap:20px}.stage{gap:20px}.card{padding:14px 18px 18px;border-radius:8px}'
        '.card > .code.dark.entry{font-size:34px;line-height:1.45;padding:26px 30px}.card .who{font-size:28px}'
        '.note{margin:0}')

# ---- Chapter: When a score helps -----------------------------------------------------------------
EB1 = 'When a score helps'
framed('s02', EB1, 'A scale shows how far off', f'''<div class="cols wide terms">
    {block("pass", "structure", "Did it pass?", "a yes or no", words=True)}
    {block("far", "attention", "How far off is a failure?", "a scale", words=True)}
  </div>''', [
    {"type": "focus", "target": "pass", "at": "1", "color": "blue"},
    {"type": "focus", "target": "far", "at": "3", "color": "yellow"}],
    css='.terms .semantic-block{min-height:260px;justify-content:center}.terms .label{font-size:38px}')

DOCS1 = '“Thresholds are for genuinely graded work — judged quality, partial credit — not for pass/fail assertions like file-exists.”'
framed('s03', EB1, 'Some checks have no nearly', f'''{quote('docs', 'Vally docs, Scoring', DOCS1)}
  <div class="cols wide terms">
    {block("partly", "attention", "Can be partly right", "the wording of an entry", words=True)}
    {block("never", "structure", "No nearly", "cites its pull request · filed under Security", words=True)}
  </div>''', [
    {"type": "focus", "target": "never", "at": "1", "color": "blue"},
    {"type": "focus", "target": "docs", "at": "3", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.stage{gap:32px}.quote{width:100%}.quote p{font-size:36px}.terms .semantic-block{min-height:190px}'
        '.terms .label{font-size:34px}')

framed('s04', EB1, 'Where the sources agree', f'''<div class="cols wide terms">
    {block("yesno", "structure", "Yes or no, throughout", "Husain, “Using LLM-as-a-Judge”", words=True)}
    {block("range", "structure", "Partial success is a range", "Anthropic, “Demystifying evals for AI agents” (2026)", words=True)}
  </div>
  <p class="lead"><span data-concept="both" data-rep="note">Both: a clear line for pass or fail, checked against your own labels.</span></p>''', [
    {"type": "focus", "target": "yesno", "at": "1~yes-or-no", "color": "blue"},
    {"type": "focus", "target": "range", "at": "1~another", "color": "blue"},
    {"type": "focus", "target": "both", "at": "2", "color": "yellow"}],
    css='.terms .semantic-block{min-height:220px}.terms .label{font-size:32px}.lead{font-size:42px;margin:0}.stage{gap:40px}')

# ---- Chapter: From scores to a verdict -----------------------------------------------------------
EB2 = 'From scores to a verdict'
framed('s05', EB2, 'Every grader gives a score', f'''<div class="cols terms">
    {block("grader", "structure", "a grader", "a pass or a fail, and a score from 0 to 1", words=True)}
    {block("diff", "transform", "diff-contains", "passes: 1 · fails: 0")}
    {block("trial", "attention", "a trial", "one score, from its graders’ scores", words=True)}
  </div>''', [
    {"type": "focus", "target": "grader", "at": "1", "color": "blue"},
    {"type": "focus", "target": "diff", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "trial", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}')

warn = [l.rstrip() for l in lint1.splitlines() if l.strip()]
wi = next(i for i, l in enumerate(warn) if 'scoring-defaults-applied' in l)
ui = next(i for i, l in enumerate(warn) if l.strip().startswith('Using defaults'))
EQ, ANY = 'equal weights, no threshold', 'any single failing grader fails the stimulus'
box = wrap_marked(warn[wi], 66) + [x for l in warn[wi + 1:ui] for x in wrap_marked(l, 66)] + \
    wrap_marked(warn[ui], 66, [('eq', EQ), ('any', ANY)], indent='  ')
framed('s06', EB2, 'No block: every grader must pass', f'''<div class="annotated">
    {code(chr(10).join(box), 'text', 'out')}
    {callouts(('eq', 'the score is a plain average'), ('any', 'so the score decides nothing'))}
  </div>
  <p class="note">{mono('vally lint')} on the judge’s eval file · {SRC_NOTE}</p>''', [
    {"type": "focus", "target": "eq", "at": "1~plain average", "color": "blue"},
    {"type": "focus", "target": "any", "at": "2", "color": "yellow"}],
    css='.code.dark.out{font-size:30px;line-height:1.5;padding:24px 30px}.callout{font-size:31px}.stage{gap:24px}.note{margin:0}')

framed('s07', EB2, 'Weights and a threshold decide', f'''<div class="annotated">
    {panel('scoring')}
    {callouts(('weights', 'by grader type, not by name'), ('wprompt', 'the judge'),
              ('wdiff', 'the pull request check'), ('thresh', 'the score a trial must reach'))}
  </div>''', [
    {"type": "focus", "target": "weights", "at": "1", "color": "blue"},
    {"type": "focus", "target": "wprompt", "at": "2~prompt", "color": "blue"},
    {"type": "focus", "target": "wdiff", "at": "2~diff contains", "color": "blue"},
    {"type": "focus", "target": "thresh", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "6"}], layout='layout-file')

sums = '0.5 × ⟦j:0.25⟧\n0.5 × ⟦c:1⟧\n⟦sum:= 0.625⟧'
framed('s08', EB2, 'A strong score carries a failure', f'''<div class="annotated">
    {code(sums, 'text', 'sums')}
    {callouts(('j', 'the judge: failed'), ('c', 'the pull request check: passed'), ('sum', 'reaches 0.6: the trial passes'))}
  </div>''', [
    {"type": "focus", "target": "j", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "c", "at": "2~check", "color": "green"},
    {"type": "focus", "target": "sum", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "j", "at": "4", "color": "yellow"}],
    css='.code.dark.sums{font-size:56px;line-height:1.6;padding:36px 48px;min-width:560px}.callout{font-size:34px}')

left_out = 'scoring:\n  weights:\n    ⟦only:diff-contains: 1⟧'
no_weights = 'scoring:\n  ⟦bare:threshold: 0.6⟧'
framed('s09', EB2, 'A missing type stops counting', f'''<div class="cols pair">
    {card('silenced', 'The judge left out of the weights', code(left_out, 'yaml', 'snip') +
          '<div class="who">the judge is called, and changes nothing</div>')}
    {card('outvoted', 'A threshold with no weights', code(no_weights, 'yaml', 'snip') +
          '<div class="who">a yes-or-no judge fails: 0 · two checks pass: 1 and 1</div>'
          '<div class="who">(0 + 1 + 1) ÷ 3 = 0.67 · reaches 0.6</div>')}
  </div>
  {quote('docs', 'Vally docs, Scoring', '“Omitting a type silences it, so list every type you care about.”')}''', [
    {"type": "focus", "target": "silenced", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "docs", "at": "2", "color": "blue"},
    {"type": "focus", "target": "outvoted", "at": "3", "color": "yellow"}],
    css='.stage{gap:18px}.pair{align-items:stretch;gap:20px}.card{padding:14px 18px 18px;border-radius:8px}.card > .code.dark.snip{font-size:34px;line-height:1.5;flex:0 0 auto;min-height:170px}'
        '.card .who{font-size:30px}.quote{width:100%;padding-top:16px;padding-bottom:18px}.quote p{font-size:34px}')

# ---- Chapter: A judge on a scale -----------------------------------------------------------------
EB3 = 'A judge on a scale'
framed('s10', EB3, 'The judge answers one to five', f'''<div class="annotated">
    {panel('judge')}
    {callouts(('scale', 'how the judge answers'), ('jthresh', 'the judge’s own threshold'))}
  </div>''', [
    {"type": "focus", "target": "scale", "at": "1~scoring setting", "color": "blue"},
    {"type": "focus", "target": "jthresh", "at": "5", "color": "yellow"}], layout='layout-file')

SCALE = [('a1', '1', '0', ''), ('a2', '2', '0.25', ''), ('a3', '3', '0.5', 'the default threshold'),
         ('a4', '4', '0.75', 'our threshold'), ('a5', '5', '1', '')]
framed('s11', EB3, 'Five answers, rescaled', f'''<div class="cols five">
    {''.join(block(c, 'structure', t, s + (f'<br>{n}' if n else '')) for c, t, s, n in SCALE)}
  </div>
  <p class="lead">The judge passes when its score reaches its threshold.</p>''', [
    {"type": "focus", "target": "a1", "at": "2~becomes zero", "color": "blue"},
    {"type": "focus", "target": "a5", "at": "2~five", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "a3", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "a4", "at": "5", "color": "green"}],
    css='.five{gap:24px}.five .semantic-block{min-height:290px}.five .title{font-size:96px;line-height:1.1}'
        '.five .label{font-size:34px;line-height:1.3}.lead{font-size:38px;margin:0}.stage{gap:34px}')

framed('s12', EB3, 'Two thresholds, two jobs', f'''<div class="cols wide terms">
    {block("without", "structure", "no scoring block", "the judge’s own threshold decides: a cross fails the trial", words=True)}
    {block("with", "attention", "with a scoring block", "only the judge’s score counts; the block’s threshold decides", words=True)}
  </div>''', [
    {"type": "focus", "target": "without", "at": "1", "color": "blue"},
    {"type": "focus", "target": "with", "at": "2", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px;justify-content:center}.terms .label{font-size:36px}')

MAP = [('100%', '1', '5'), ('87.5%', '0.75', '4'), ('75%', '0.5', '3'), ('62.5%', '0.25', '2'), ('50%', '0', '1')]
rows13 = ''.join(f'''<tr><td class="num">{cell('m' + a, 'Score: ' + s)}</td><td class="num">{j}</td>
        <td class="num">{a}</td></tr>\n''' for s, j, a in MAP)
framed('s13', EB3, 'The score line gives it away', f'''<table class="data-table map">
    <thead><tr><th class="num">Score line</th><th class="num">The judge’s score</th><th class="num">The judge’s answer</th></tr></thead>
    <tbody>
{rows13}    </tbody>
    <caption>when the pull request check passes and scores 1 · half of each</caption>
  </table>''', [
    {"type": "focus", "target": "m5", "at": "3~hundred", "color": "blue"},
    {"type": "focus", "target": "m4", "at": "3~eighty-seven", "color": "blue"},
    {"type": "focus", "target": "m1", "at": "3~fifty", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.map{font-size:40px;align-self:center}.map td{padding-top:14px;padding-bottom:14px}.map th{font-size:30px}'
        '.map th,.map td{padding-right:96px}')

# ---- Chapter: Score the wording ------------------------------------------------------------------
EB4 = 'Score the wording'


def twelve(filled):
    body = ''
    for r in NO + YES:                      # the six we labelled no first, so each group the voice names is together
        if not filled:
            last = ''
        else:
            grp = 'far' if r in FAR else 'near' if r in NEAR else 'yes'
            last = cell(grp, str(r['a1'])) + (' · ' + cell('changed', 'passes') if r in CHANGED else '')
        body += f'''<tr><td class="who">{r['who']}</td><td>{esc(tail(r['entry']))}</td>
        <td>{r['judge']}</td><td>{r['ours']}</td><td class="score">{last}</td></tr>\n'''
    return f'''<table class="data-table full twelve">
    <thead><tr><th>Trial</th><th>Entry, shortened</th><th>{cell('agree', 'Yes-or-no judge')}</th><th>{cell('agree', 'Ours')}</th>
      <th>{cell('col', '1 to 5')}</th></tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


CSS12 = ('.twelve{font-size:28px;line-height:1.3}.twelve th{font-size:28px;padding-bottom:8px;padding-right:36px}'
         '.twelve td{padding:4px 36px 4px 0}.twelve td.who{font-family:var(--font-code);font-size:26px;white-space:nowrap}'
         '.twelve td.score{font-family:var(--font-code);white-space:nowrap;min-width:230px}.stage{justify-content:flex-start}')
framed('s14', EB4, 'Which verdicts will change?', twelve(False), [
    {"type": "focus", "target": "agree", "at": "3", "color": "blue"},
    {"type": "focus", "target": "col", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], css=CSS12)


def block_box(b, width=62):
    """One block of vally grade's output, word for word, wrapped. Targets: head, judge, check, score."""
    j, c = b['judge'], b['check']
    jmark = j['line'].strip().split('] ')[0] + ']'
    cmark = c['line'].strip().split('] ')[0] + ']'
    lines = [b['title'], *wrap_marked(b['head'], width, [('head', b['head'].split(' (')[0])]),
             *wrap_marked(j['line'], width, [('judge', jmark)]),
             *wrap_marked(c['line'], width, [('check', cmark)]), '',
             *wrap_marked(b['scoreline'], width, [('score', b['scoreline'].split(' | ')[0])])]
    return code('\n'.join(lines), 'text', 'out')


CSSB = ('.code.dark.out{font-size:29px;line-height:1.4;padding:20px 28px}.callout{font-size:31px}'
        '.stage{gap:16px;justify-content:safe center}.note{margin:0}')
one = min((r for r in FAR if not r['pass1'] and r['b1']['score'] == 62.5), key=lambda r: len(r['b1']['judge']['text']))['b1']
assert one['judge']['text'].count('"') >= 2                                   # s17/1 the reason quotes the entry
framed('s17', EB4, 'One block, one score', f'''<div class="annotated">
    {block_box(one)}
    {callouts(('judge', 'the judge: a cross, and a reason'), ('check', 'the check: a tick, so 1'),
              ('score', '62.5% · the judge answered 2'))}
  </div>
  <table class="data-table strip">
    <tbody>
      <tr><td>Score line</td>{''.join(f'<td class="num">{cell("score", sc) if a == "2" else sc}</td>' for sc, _, a in MAP)}</tr>
      <tr><td>The judge’s answer</td>{''.join(f'<td class="num">{cell("score", a) if a == "2" else a}</td>' for _, _, a in MAP)}</tr>
    </tbody>
    <caption>one of the twelve blocks, word for word · {SRC_NOTE}</caption>
  </table>''', [
    {"type": "focus", "target": "judge", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "check", "at": "2", "color": "green"},
    {"type": "focus", "target": "score", "at": "3", "color": "yellow"}],
    css=CSSB + '.code.dark.out{font-size:28px;line-height:1.38;padding:16px 26px}'
              '.strip{font-size:30px}.strip td{padding:6px 44px 6px 0}.strip caption{padding-top:8px}')

framed('s18', EB4, 'The same twelve, scored', twelve(True), [
    {"type": "focus", "target": "far", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "yes", "at": "3", "color": "green"},
    {"type": "focus", "target": "near", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "changed", "at": "5~one verdict", "color": "orange"}], css=CSS12)

two = min((r for r in CROSSED if r['b2']['score'] == 62.5), key=lambda r: len(r['b2']['judge']['text']))['b2']
framed('s20', EB4, 'A cross inside a pass', f'''<div class="annotated">
    {block_box(two)}
    {callouts(('head', 'the trial passes'), ('judge', 'the judge still fails it'),
              ('score', '0.5 × 0.25 + 0.5 × 1 = 0.625'))}
  </div>
  <p class="note">one of the twelve blocks, with the scoring block · {SRC_NOTE}</p>''', [
    {"type": "focus", "target": "judge", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "head", "at": "2", "color": "green"},
    {"type": "focus", "target": "score", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], css=CSSB)

framed('s21', EB4, 'Put back, and written down', panel('notes'), [
    {"type": "focus", "target": "col", "at": "1", "color": "yellow"},
    {"type": "scroll", "target": "#notes", "to": "end", "at": "2"},
    {"type": "focus", "target": "sentence", "at": "3", "color": "yellow"}], layout='layout-file')

# ---- Chapter: What the scores showed -------------------------------------------------------------
EB5 = 'What the scores showed'
near_scores = ' and '.join(str(a) for a in sorted({r['a1'] for r in NEAR}, reverse=True))
framed('s22', EB5, 'Close, or far off', f'''{card('far', 'far off · the judge answered 2', entry_box(FAR, 98, 'entries'))}
  {card('near', f'close · the judge answered {near_scores}', entry_box(NEAR, 98, 'entries'))}
  <p class="note">our {WORDS[len(NO)]} “no” entries · {SRC_NOTE}</p>''', [
    {"type": "focus", "target": "far", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "near", "at": "3", "color": "blue"},
    {"type": "focus", "target": "far", "at": "4", "color": "yellow"}],
    css='.stage{gap:10px}.card{width:100%;padding:12px 18px 16px;border-radius:8px}'
        '.card > .code.dark.entries{font-size:28px;line-height:1.3;padding:18px 26px;flex:0 0 auto}'
        '.card .who{font-size:30px}.note{margin:0}')

framed('s23', EB5, 'A threshold is a decision', f'''<div class="cols terms">
    {block("yn", "structure", f"TNR {TN_YESNO} of {len(NO)}", "the yes-or-no judge")}
    {block("ours", "attention", f"TNR {TN} of {len(NO)}", "1 to 5, threshold 0.75")}
    {block("default", "change", f"TNR {TN_DEFAULT} of {len(NO)}", "1 to 5, default threshold 0.5")}
  </div>
  <p class="lead"><span data-concept="check" data-rep="note">The same check as before: its verdicts against our labels.</span></p>''', [
    {"type": "focus", "target": "yn", "at": "1~four of five", "color": "blue"},
    {"type": "focus", "target": "ours", "at": "1~three of five", "color": "yellow"},
    {"type": "focus", "target": "default", "at": "2", "color": "orange"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "check", "at": "4", "color": "blue"}],
    css='.terms .semantic-block{min-height:250px;justify-content:center}.terms .title{font-size:52px}.terms .label{font-size:32px}'
        '.lead{font-size:40px;margin:0}.stage{gap:38px}')

says = lambda a: f"{a} · the judge {'passes' if a >= 4 else 'fails'} it"
rows24 = ''.join(f'''<tr><td>{esc(tail(r['entry'], 54))}</td><td class="num">{cell('g1', says(r['a1']))}</td>
        <td class="num">{cell('g2', says(r['a2']))}</td></tr>\n''' for r in FLIPPED)
rows24 += f'''<tr><td>the {len(FAR)} entries that say how the change was coded</td><td class="num">{cell('same', '2')}</td>
        <td class="num">{cell('same', '2')}</td></tr>\n'''
framed('s24', EB5, 'Near the line, verdicts flip', f'''<table class="data-table full flips">
    <thead><tr><th>Entry</th><th class="num">First grading</th><th class="num">Second grading</th></tr></thead>
    <tbody>
{rows24}    </tbody>
    <caption>the same saved trials, judged twice · judge’s threshold 0.75 · {SRC_NOTE}</caption>
  </table>''', [
    {"type": "focus", "target": "g1", "at": "1~four", "color": "green"},
    {"type": "focus", "target": "g2", "at": "1~three", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "same", "at": "4", "color": "blue"}],
    css='.flips{font-size:34px}.flips th{font-size:28px}.flips td{padding-top:26px;padding-bottom:26px}'
        '.flips td.num{white-space:nowrap}')

down = DOWN[0]
framed('s25', EB5, 'A scale invites extra marks', f'''{card('entry', f"{mono(down['who'])} · our label: yes · the yes-or-no judge: yes · 1 to 5: {down['a1']}",
                                                     entry_box([down], 80, 'entry'))}
  {quote('reason', 'the 1-to-5 judge’s reason', esc(down['b1']['judge']['text'].replace(chr(92) + '"', '"')))}
  <p class="note">{SRC_NOTE}</p>''', [
    {"type": "focus", "target": "entry", "at": "1", "color": "blue"},
    {"type": "focus", "target": "reason", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.stage{gap:14px}.card{width:100%;padding:14px 18px 18px;border-radius:8px}.card > .code.dark.entry{font-size:32px;padding:20px 28px;flex:0 0 auto}'
        '.card .who{font-size:28px}.quote{width:100%;padding-top:18px;padding-bottom:20px}.quote p{font-size:31px;line-height:1.38}.note{margin:0}')

rows26 = ''.join(f'''<tr><td>{cell('jx', '✗ fails')}</td><td>{cell('tk', '✓ passes · ' + ('%g' % r['b2']['score']) + '%')}</td>
        <td>{esc(tail(r['entry'], 58))}</td></tr>\n''' for r in CROSSED)
framed('s26', EB5, 'A failure hides in an average', f'''<table class="data-table full hides">
    <thead><tr><th>Judge</th><th>Trial</th><th>Entry, shortened</th></tr></thead>
    <tbody>
{rows26}    </tbody>
  </table>
  <p class="lead"><span data-concept="sum" data-rep="note">a judge’s 2: 0.5 × 0.25 + 0.5 × 1 = 0.625 · reaches 0.6</span></p>
  <p class="note">the second grading, with the scoring block · {SRC_NOTE}</p>''', [
    {"type": "focus", "target": "jx", "at": "2~failed", "color": "yellow"},
    {"type": "focus", "target": "tk", "at": "2~passed", "color": "green"},
    {"type": "focus", "target": "sum", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.hides{font-size:32px}.hides th{font-size:28px}.hides td{padding-top:14px;padding-bottom:14px}'
        '.hides td:nth-child(-n+2){white-space:nowrap;font-family:var(--font-code);font-size:30px}'
        '.lead{font-size:38px;margin:0}.stage{gap:22px}.note{margin:0}')

framed('s27', EB5, 'The yes or no still decides', f'''<div class="cols wide terms">
    {block("yn", "structure", "yes-or-no judge", "decides the verdict", words=True)}
    {block("scale", "attention", "1-to-5 judge", "says how far off a failure is", words=True)}
  </div>
  <p class="note">Vally docs, Scoring: thresholds for judged quality; pass-or-fail checks left out of the weights</p>''', [
    {"type": "focus", "target": "yn", "at": "1", "color": "blue"},
    {"type": "focus", "target": "scale", "at": "2", "color": "yellow"}],
    css='.terms .semantic-block{min-height:250px;justify-content:center}.terms .label{font-size:38px}.stage{gap:34px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('no scoring block', 'every grader must pass'),
    ('weights and a threshold', 'the weighted score must reach the threshold')], 1))
framed('s28', 'Recap', 'What decides the verdict?', f'''<div class="semantic-block" id="verdict" data-role="structure">
    <div class="title words">a trial’s verdict</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#verdict", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"}], layout='layout-expand',
    css='#verdict{width:100%;padding:36px 40px 44px;gap:24px}'
        '#verdict .parts{display:grid;grid-template-columns:repeat(2,1fr);gap:28px;width:100%}'
        '#verdict .part{min-height:260px}#verdict .part .title{font-size:46px;line-height:1.2}'
        '#verdict .part .label{font-size:34px}')

scene('s29', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Is the change real</h1>
  <p class="lead">After an edit, 7 of 10 becomes 9 of 10. Is that real?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, Scoring; Grader: prompt</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', 'PROVISIONAL run' if PROVISIONAL else 'own run',
      '| answers', ''.join(str(r['a1']) for r in ROWS), '→', ''.join(str(r['a2']) for r in ROWS))
