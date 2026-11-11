"""Generate lesson 5's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/terra.patch, l3-results.jsonl, one-request.eval.yaml   the lesson 3 video's run (src/l3-RUN)
  src/state/changelog.eval.yaml, SKILL.md                    the files the tapes install (from
                                                             verified/lesson-05/practice)
  src/run/before/, src/run/after/                            the two runs this video's s14 and s17
                                                             record. results.jsonl when it is there;
                                                             until then console.txt, a stand-in from
                                                             the course's verified run (src/run/PROVISIONAL)

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
STIMULI = ('typo-fix', 'refactor', 'security')
GRADERS = {'typo-fix': ('adds-an-entry', 'no-made-up-number'), 'refactor': ('adds-nothing',),
           'security': ('under-security',)}
RUNS = 3


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


# ---- Rows of boxes, one mark per box (as in lesson 3) ------------------------------------------------
MARK = {'p': ('tick', '✔'), 'f': ('cross', '✘')}
BOX_CSS = ('.rows{display:flex;flex-direction:column;gap:14px;width:100%}'
           '.trow{display:flex;align-items:center;gap:36px;padding:12px 22px;border-radius:10px;width:fit-content}'
           '.boxes{display:flex;gap:14px}'
           '.box{display:flex;align-items:center;justify-content:center;width:320px;height:70px;border-radius:8px;'
           'border:3px solid var(--ink-muted);font:700 42px/1 var(--font-body);color:var(--ink)}'
           '.box.tick{color:var(--green-ink)}.box.cross{color:var(--red-ink)}'
           '.trow.head{padding-top:0;padding-bottom:0}'
           '.gname{width:326px;text-align:center;font:500 28px/1 var(--font-code);color:var(--ink)}'
           '.trow .mean{font:400 36px/1.3 var(--font-body);color:var(--ink-soft)}')

# ---- The lesson 3 video's run: the grader so far, and what it passed -----------------------------------
eval_lines = (D / 'src/one-request.eval.yaml').read_text().splitlines()
assert eval_lines[17].strip() == 'graders:' and eval_lines[22].strip() == 'value: "notes add"'
OLD_GRADER = '\n'.join(l[4:] for l in eval_lines[17:23])
l3 = [json.loads(l) for l in (D / 'src/l3-results.jsonl').read_text().splitlines() if l.strip()]
l3 = [t for t in l3 if t.get('type') == 'trial-result']
L3_PASSED = sum(t['gradeResult']['passed'] for t in l3)
L3_MADE_UP = sum('#42' in t['trajectory']['output'] for t in l3 if t['model'] == 'gpt-5.6-terra')
L3_RUN = (D / 'src/l3-RUN').read_text().strip()
# s04 says: one grader so far, it passed every trial, including the ones that made up a number.
assert len(l3) == 10 and L3_PASSED == 10 and L3_MADE_UP == 5, (len(l3), L3_PASSED, L3_MADE_UP)
patch = (D / 'src/terra.patch').read_text().splitlines()
assert patch[6].endswith('(#41)') and patch[6].startswith(' ') and patch[9].startswith('+- ') and patch[9].endswith('(#42)')


# ---- This video's two runs ----------------------------------------------------------------------------
def load_run(which):
    """-> (passes {(stimulus, model): trials passed of 3}, fails {grader: trials it failed}, label)"""
    d = D / 'src/run' / which
    passes = {(s, m): 0 for s in STIMULI for m in MODELS}
    fails = {g: 0 for gs in GRADERS.values() for g in gs}
    if (d / 'results.jsonl').exists():
        ts = [json.loads(l) for l in (d / 'results.jsonl').read_text().splitlines() if l.strip()]
        ts = [t for t in ts if t.get('type') == 'trial-result']
        assert len(ts) == len(STIMULI) * len(MODELS) * RUNS, f'{which}: {len(ts)} trials'
        bad = [(t['stimulus'], t['model'], t['trialIndex']) for t in ts if t['status'] != 'success']
        assert not bad, f'{which}: trials that did not finish (ERROR): {bad}. Re-record the tape.'
        for t in ts:
            passes[(t['stimulus'], t['model'])] += bool(t['gradeResult']['passed'])
            for g in t['gradeResult']['details']:
                name = g.get('configuredName') or g['name']
                assert name in fails, name
                fails[name] += not g['passed']
        return passes, fails, 'our run · ' + (d / 'RUN').read_text().strip()
    raise SystemExit(f'{which}: src/run/{which}/results.jsonl is missing')


def load_console(path):
    """The console output of the course's own earlier run (the lesson page's). A stimulus with no block passed 3 of 3."""
    passes = {(s, m): RUNS for s in STIMULI for m in MODELS}
    fails = {g: 0 for gs in GRADERS.values() for g in gs}
    model = None
    for line in path.read_text().split('─' * 10)[0].splitlines():
        s = line.strip()
        if s in MODELS:
            model = s
        elif m := re.match(r'(FAIL|FLAKY)\s+(\S+)\s+(?:(\d+)/3|(\d+) passed · \d+ failed)', s):
            passes[(m.group(2), model)] = int(m.group(3) or m.group(4))
        elif m := re.match(r'✘ (\S+)\s+\d+ passed · (\d+) failed', s):
            fails[m.group(1)] += int(m.group(2))
    return passes, fails


B, B_FAILS, B_LABEL = load_run('before')
A, A_FAILS, A_LABEL = load_run('after')
P, P_FAILS = load_console(D / 'src/page-run/after-console.txt')   # the same edit, measured earlier for the lesson page
H, T = MODELS
row = lambda R, s: (R[(s, H)], R[(s, T)])
total = lambda R, m: sum(R[(s, m)] for s in STIMULI)
whole = lambda R, m: sum(R[(s, m)] == RUNS for s in STIMULI)   # the summary line: stimuli that passed every trial

# ---- What the narration says about the two runs. If a recording changes these, the sentences change too.
# s14: "one of three on haiku, and none of three on terra"; and a list of stimuli that did not pass.
assert (whole(B, H), whole(B, T)) == (1, 0), (whole(B, H), whole(B, T))
# s15: "On the typo fix, haiku passed three of three, and terra none." "Neither model passed the refactor
#       or the security fix, in any trial."
assert row(B, 'typo-fix') == (3, 0) and row(B, 'refactor') == (0, 0) and row(B, 'security') == (0, 0), B
# s17: "two of three on haiku, and three of three on terra"; "one stimulus is listed ... flaky".
# s17 (our run): "three of three on both models"; "nothing is listed above it: every trial passed".
assert (whole(A, H), whole(A, T)) == (3, 3), (whole(A, H), whole(A, T))
assert all(n == RUNS for n in A.values()), A
# s18: made-up number gone on terra; neither model adds an entry for the refactor; security worked every
#      time on terra, haiku failed that grader in one of three.
assert A[('typo-fix', T)] == 3 and A_FAILS['no-made-up-number'] == 0
# s18 (our run): the security rule worked every time, on both models.
assert row(A, 'refactor') == (3, 3) and row(A, 'security') == (3, 3) and A_FAILS['under-security'] == 0, A
# s19: on terra all three rules worked; on haiku one failure fixed, another partly fixed.
# s19: in our run all three rules worked on both models; in the earlier run haiku filed one security fix
#      under Fixed and passed eight of nine.
assert total(A, T) == 9 and total(B, T) == 0 and (total(B, H), total(A, H)) == (3, 9)
assert total(P, H) == 8 and P[('security', H)] == 2 and P_FAILS['under-security'] == 1 and total(P, T) == 9, (P, P_FAILS)
# s20: "Every one of them failed somewhere" in the first run.
assert all(n > 0 for n in B_FAILS.values()), B_FAILS

# ---- Hook ------------------------------------------------------------------------------------------------
FAILURES = [('f1', 'A made-up pull request number', 'typo-fix', 'no-made-up-number'),
            ('f2', 'An entry for a change users can’t see', 'refactor', 'adds-nothing'),
            ('f3', 'A security fix filed under Fixed', 'security', 'under-security')]
framed('s01', 'Vally &amp; Agent Evals', 'Turn a failure into a grader', f'''<div class="cols wide terms">
    {''.join(block(c, 'attention', t, f'seen in {mono(s)}', words=True) for c, t, s, _ in FAILURES)}
  </div>''', [
    {"type": "focus", "target": "f1", "at": "0~list", "color": "yellow"},
    {"type": "focus", "target": "f2", "at": "0~goes wrong", "color": "yellow"},
    {"type": "focus", "target": "f3", "at": "0~every one", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "1"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.terms .semantic-block{min-height:250px}.terms .label{font-size:32px}')

# ---- Chapter: Three habits for graders ---------------------------------------------------------------------
EB1 = 'Three habits for graders'
TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'
framed('s02', EB1, 'Grade the result, not the route', f'''<div class="cols wide terms">
    {block("route", "structure", "The route", "open the file or search it · one edit or two", words=True)}
    {block("result", "attention", "The result", "what the agent left behind: the patch", words=True)}
  </div>''', [
    {"type": "focus", "target": "route", "at": "2~routes", "color": "blue"},
    {"type": "focus", "target": "result", "at": "4~left behind", "color": "yellow"}], css=TERMS)

name_rows = ''.join(f'<tr><td>{t}</td><td class="mono"><span data-concept="n-{c}" data-rep="cell">{g}</span></td></tr>\n'
                    for c, t, _, g in FAILURES)
TABLE_CSS = ('.data-table{font-size:40px}.data-table th{font-size:30px}.data-table td{padding-top:30px;padding-bottom:30px}'
             '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:34px}')
framed('s03', EB1, 'One grader per failure mode', f'''<table class="data-table full names">
    <thead><tr><th>Failure mode</th><th>A grader named after it</th></tr></thead>
    <tbody>
{name_rows}    </tbody>
  </table>''', [
    {"type": "focus", "target": "n-f1", "at": "1~no made-up number", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}], css=TABLE_CSS)

framed('s04', EB1, 'Can this grader fail?', f'''<div class="cols pair">
    {card('g', 'The only grader so far', code(OLD_GRADER.replace('"notes add"', '⟦value:"notes add"⟧'), 'yaml'))}
    <div class="semantic-block big" data-concept="passed" data-rep="block" data-role="attention">
      <div class="title">{L3_PASSED} of {len(l3)}</div>
      <div class="label">trials passed · {L3_MADE_UP} of them with a made-up number</div>
    </div>
  </div>
  <p class="note">from the five-trial run · {L3_RUN}</p>''', [
    {"type": "focus", "target": "passed", "at": "1~passed every trial", "color": "yellow"},
    {"type": "focus", "target": "value", "at": "2~checking", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.pair{align-items:stretch}.card > .code.dark{font-size:34px}'
        '.big{justify-content:center;min-height:300px}.big .title{font-size:110px;line-height:1.1}.big .label{font-size:34px}')

framed('s05', EB1, 'Code first, where code decides', f'''<div class="cols wide terms">
    {block("can", "structure", "A pattern can decide", "Is there a made-up number? Is there a Security heading?", words=True)}
    {block("cannot", "attention", "Beyond a pattern", "Is the entry written for the people who use the tool?", words=True)}
  </div>''', [
    {"type": "focus", "target": "can", "at": "1", "color": "blue"},
    {"type": "focus", "target": "cannot", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3~later"}], css=TERMS)

# ---- Chapter: Graders that read the diff -------------------------------------------------------------------
EB2 = 'Graders that read the diff'
framed('s06', EB2, 'Three graders read the patch', f'''<div class="annotated">
    {code('type: ⟦dc:diff-contains⟧\n\ntype: ⟦dnc:diff-not-contains⟧\n\ntype: ⟦de:diff-empty⟧', 'yaml', 'types')}
    {callouts(('dc', 'passes when the patch contains it'), ('dnc', 'passes when the patch doesn’t'),
              ('de', 'passes when the agent changed nothing'))}
  </div>''', [
    {"type": "focus", "target": "dc", "at": "4", "color": "blue"},
    {"type": "focus", "target": "dnc", "at": "5", "color": "blue"},
    {"type": "focus", "target": "de", "at": "6", "color": "blue"}],
    css='.code.dark.types{min-width:760px;font-size:42px;line-height:1.5}.callout{font-size:34px}')

framed('s07', EB2, 'They see unchanged lines too', f'''<div class="annotated">
    {panel('patch')}
    {callouts(('ctx', 'unchanged, still in the patch'), ('added', 'added by the agent'))}
  </div>''', [
    {"type": "focus", "target": "ctx", "at": "2~unchanged", "color": "yellow"},
    {"type": "focus", "target": "added", "at": "4~this line", "color": "green"}], layout='layout-file')

framed('s08', EB2, 'A value, or a pattern', f'''<div class="annotated">
    {panel('spec')}
    {callouts(('value', 'exact text'), ('pattern', 'a regular expression'))}
  </div>''', [
    {"type": "focus", "target": "stim", "at": "2~typo fix", "color": "blue"},
    {"type": "scroll", "target": "#spec", "to": "19-27", "at": "3"},
    {"type": "focus", "target": "g1", "at": "3~entry", "color": "blue"},
    {"type": "focus", "target": "value", "at": "4~notes add", "color": "yellow"},
    {"type": "focus", "target": "g2", "at": "5~made-up", "color": "blue"},
    {"type": "focus", "target": "pattern", "at": "5~pattern", "color": "yellow"}], layout='layout-file')

PIECES = "pattern: ⟦whole:'(?m)^\\+.*\\(#\\d+\\)'⟧\n\n  ⟦m:(?m)⟧\n  ⟦plus:^\\+⟧\n  ⟦any:.*⟧\n  ⟦num:\\(#\\d+\\)⟧"
framed('s09', EB2, 'An added line with a number', f'''<div class="annotated">
    {code(PIECES, 'text', 'pieces')}
    {callouts(('m', '^ matches at the start of every line'), ('plus', 'a line that starts with +'),
              ('any', 'anything'), ('num', 'a hash and digits, in brackets'))}
  </div>''', [
    {"type": "focus", "target": "plus", "at": "1~caret", "color": "green"},
    {"type": "focus", "target": "m", "at": "2~switch", "color": "blue"},
    {"type": "focus", "target": "any", "at": "3~anything", "color": "blue"},
    {"type": "focus", "target": "num", "at": "3~hash", "color": "yellow"},
    {"type": "focus", "target": "whole", "at": "4", "color": "yellow"}],
    css='.code.dark.pieces{min-width:860px;font-size:42px;line-height:1.55}.callout{font-size:34px}')

framed('s10', EB2, 'One grader each for the rest', f'''<div class="annotated">
    {panel('spec2')}
    {callouts(('de', 'passes only when nothing changed'), ('sec', 'an added “### Security” line'))}
  </div>''', [
    {"type": "focus", "target": "refactor", "at": "1~refactor", "color": "blue"},
    {"type": "focus", "target": "de", "at": "2", "color": "yellow"},
    {"type": "scroll", "target": "#spec2", "to": "42-55", "at": "3"},
    {"type": "focus", "target": "security", "at": "3~security fix", "color": "blue"},
    {"type": "focus", "target": "sec", "at": "3~added line", "color": "yellow"}], layout='layout-file')

g1, g2 = GRADERS['typo-fix']
head = f'<div class="trow head"><span class="boxes"><span class="gname">{g1}</span><span class="gname">{g2}</span></span></div>'


def verdict_row(cid, marks, mean):
    bx = ''.join(f'<span class="box {MARK[m][0]}">{MARK[m][1]}</span>' for m in marks)
    return f'<div class="trow" data-concept="{cid}" data-rep="row"><span class="boxes">{bx}</span><span class="mean">{mean}</span></div>'


framed('s11', EB2, 'Every grader has to pass', f'''<div class="rows">
    {head}
    {verdict_row('both', 'pp', 'the trial passes')}
    {verdict_row('one', 'pf', 'the trial fails')}
    {verdict_row('other', 'fp', 'the trial fails')}
  </div>
  <div class="annotated">
    {code('warning ⟦warn:[scoring-defaults-applied]⟧', 'text')}
    {callouts(('warn', 'lint’s reminder that this rule is in force'))}
  </div>
  <p class="note">An illustration: one trial of {mono('typo-fix')}, which has two graders</p>''', [
    {"type": "focus", "target": "both", "at": "0~passes only", "color": "green"},
    {"type": "focus", "target": "warn", "at": "1~warning", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2~expect"}],
    css=BOX_CSS + '.annotated .code.dark{font-size:38px;padding:22px 34px}.callout{font-size:34px}.stage{gap:26px}')

# ---- Chapter: Measure, edit, measure again -----------------------------------------------------------------
EB3 = 'Measure, edit, measure again'


def counts_table(before, after, concept=lambda s, m, w: None):
    """Rows are stimuli; under each model a before and an after column. A cell is 'n of 3' or empty."""
    def cell(R, s, m, w):
        txt = f'{R[(s, m)]} of {RUNS}' if R else ''
        c = concept(s, m, w)
        inner = f'<span data-concept="{c}" data-rep="cell">{txt}</span>' if c and txt else txt
        return f'<td class="num">{inner}</td>'
    hd = lambda w: f'<th class="num"><span data-concept="col-{w}" data-rep="head">{w}</span></th>'
    body = ''.join(
        f'<tr><td class="mono">{s}</td>' + ''.join(cell(before, s, m, 'before') + cell(after, s, m, 'after') for m in MODELS)
        + '</tr>\n' for s in STIMULI)
    return f'''<table class="data-table full counts">
    <thead>
      <tr><th></th><th class="mono num" colspan="2">{H}</th><th class="mono num" colspan="2">{T}</th></tr>
      <tr><th>trials passed</th>{hd('before')}{hd('after')}{hd('before')}{hd('after')}</tr>
    </thead>
    <tbody>
{body}    </tbody>
  </table>'''


COUNTS_CSS = ('.counts{font-size:46px}.counts th{font-size:30px}.counts th.mono{font-family:var(--font-code);font-size:32px}'
              '.counts td{padding-top:30px;padding-bottom:30px;height:60px}'
              '.counts td.mono{font-family:var(--font-code);font-size:36px}'
              '.counts th:last-child,.counts td:last-child{padding-right:16px}')
framed('s12', EB3, 'A count before, a count after', counts_table(None, None) + '''
  <p class="note">three trials of each stimulus on each model · before the edit to the skill, and after it</p>''', [
    {"type": "focus", "target": "col-before", "at": "1~as it is", "color": "blue"},
    {"type": "focus", "target": "col-after", "at": "2~again", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}], css=COUNTS_CSS)

framed('s15', EB3, 'The count before the edit',
       counts_table(B, None, lambda s, m, w: 'typo' if s == 'typo-fix' else 'rest') + f'''
  <p class="note">{B_LABEL}</p>''', [
    {"type": "focus", "target": "typo", "at": "1", "color": "blue"},
    {"type": "focus", "target": "rest", "at": "2", "color": "red"}], css=COUNTS_CSS)

framed('s16', EB3, 'Three rules, one per failure', f'''<div class="annotated">
    {panel('skill')}
  </div>''', [
    {"type": "focus", "target": "r1", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "r2", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "r3", "at": "5", "color": "yellow"}], layout='layout-file')


def s18_concept(s, m, w):
    if s == 'typo-fix':
        return 'terra-typo' if m == T else None
    if s == 'refactor':
        return 'refactor' if w == 'after' else None
    return 'sec' if w == 'after' else None


framed('s18', EB3, 'Before and after, side by side', counts_table(B, A, s18_concept) + f'''
  <p class="note">before: {B_LABEL} · after: {A_LABEL}</p>''', [
    {"type": "focus", "target": "terra-typo", "at": "1", "color": "green"},
    {"type": "focus", "target": "refactor", "at": "2", "color": "green"},
    {"type": "focus", "target": "sec", "at": "3", "color": "green"}], css=COUNTS_CSS)

# ---- Chapter: What the counts show -------------------------------------------------------------------------
EB4 = 'What the counts show'
n = len(STIMULI) * RUNS
framed('s19', EB4, 'Same words, different effect', f'''<div class="cols wide terms">
    {block("ours", "success", f"{total(A, T)} of {n}", f"{mono(T)} · {total(B, T)} of {n} before the edit")}
    {block("ours", "success", f"{total(A, H)} of {n}", f"{mono(H)} · {total(B, H)} of {n} before the edit")}
    {block("earlier", "attention", f"{total(P, H)} of {n}", f"{mono(H)} · an earlier run")}
  </div>
  <p class="lead"><span data-concept="what" data-rep="note">trials passed after one edit of three rules</span></p>''', [
    {"type": "focus", "target": "ours", "at": "1~our run", "color": "green"},
    {"type": "focus", "target": "earlier", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.terms .semantic-block{min-height:300px;justify-content:center}.terms .title{font-size:110px;line-height:1.1}'
        '.terms .label{font-size:34px}.lead{font-size:40px}')

per_grader = len(MODELS) * RUNS
fail_rows = ''.join(
    f'<tr><td class="mono">{g}</td><td class="num"><span data-concept="failed" data-rep="cell">{B_FAILS[g]} of {per_grader}</span></td></tr>\n'
    for gs in GRADERS.values() for g in gs)
framed('s20', EB4, 'Every grader failed first', f'''<table class="data-table full fails">
    <thead><tr><th>Grader</th><th class="num">trials it failed, before the edit</th></tr></thead>
    <tbody>
{fail_rows}    </tbody>
  </table>
  <p class="note">{B_LABEL}</p>''', [
    {"type": "focus", "target": "failed", "at": "1~failed somewhere", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css=TABLE_CSS + '.fails td{padding-top:22px;padding-bottom:22px}.fails{font-size:44px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Grade the result', 'not the route'),
    ('One per failure mode', 'named after the failure'),
    ('Able to fail', 'run first where the failure is known')], 1))
framed('s21', 'Recap', 'What are the three habits?', f'''<div class="semantic-block" id="habits" data-role="structure">
    <div class="title words">a grader worth having</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#habits", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"}], layout='layout-expand',
    css='#habits{width:100%;padding:36px 40px 44px;gap:24px}'
        '#habits .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#habits .part{min-height:300px}#habits .part .title{font-size:50px;line-height:1.2}'
        '#habits .part .label{font-size:32px}')

scene('s22', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Keep graders out of the agent’s reach</h1>
  <p class="lead">Where can a script live so the agent cannot read or edit it?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Choose a Grader”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok')
