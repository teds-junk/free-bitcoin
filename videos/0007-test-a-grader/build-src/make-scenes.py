"""Generate lesson 7's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/*.changelog.eval.yaml   the eval file at each step of the checkpoint (00 = as lesson 6 left it,
                                    05 = golden_patch on typo-fix, 08 = plus the useless grader, 10 = all four)
  src/run/typo-fix.patch            the golden patch: the saved trial's patch that tape s11 copies
  src/run/s13.log, s15.log, s17.log what vally oracle printed in tapes s13, s15 and s17 (the tapes' wrapper
                                    saves them to /tmp/vl-l7/)
While src/run/PROVISIONAL exists these are stand-ins from verified/lesson-07. The asserts below are what the
narration states; if a recording changes them, this script fails and the sentences change too.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'


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
    st = f'<div class="step">{step}</div>' if step else ''
    return f'''<div class="semantic-block" data-concept="{cid}" data-rep="block" data-role="{role}">
      {st}<div class="title{' words' if words else ''}">{title}</div><div class="label">{label}</div>
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


# ---- The real things, read from src/ -------------------------------------------------------------
state = lambda n: (D / 'src/state' / n).read_text().splitlines()
E05, E08, E10 = (state(f'{n}.changelog.eval.yaml') for n in ('05-golden-typo-fix', '08-useless-grader', '10-all-golden'))
assert E05[18].strip() == 'golden_patch:' and E05[19].strip() == 'path: golden/typo-fix.patch' and E05[20].strip() == 'graders:'
assert E05[30].strip() == '- name: refactor' and E05[40].strip() == '- type: diff-empty'
assert E08[22].strip() == 'name: mentions-unreleased' and E08[25].strip() == 'value: "Unreleased"'
TYPO_GRADERS = '\n'.join(l[4:] for l in E05[20:29])
assert 'adds-an-entry' in TYPO_GRADERS and 'no-made-up-number' in TYPO_GRADERS

# Stimuli and their graders, in the eval file's order.
STIMULI, cur = [], None
for l in E10:
    if m := re.match(r'  - name: (\S+)', l):
        cur = (m.group(1), []); STIMULI.append(cur)
    elif (m := re.match(r'        name: (\S+)', l)) and cur:
        cur[1].append(m.group(1))
GRADERS = [(s, g) for s, gs in STIMULI for g in gs]
assert [s for s, _ in STIMULI] == ['typo-fix', 'refactor', 'security', 'two-changes', 'after-release'] and len(GRADERS) == 6
GOLDEN = {s for s, _ in STIMULI if any(f'golden/{s}.patch' in l for l in E10)}
assert GOLDEN == {'typo-fix', 'security', 'two-changes', 'after-release'}

patch = (D / 'src/run/typo-fix.patch').read_text().splitlines()
added = [l for l in patch if l.startswith('+') and not l.startswith('+++')]
assert len(patch) == 14 and patch[8] == '+### Fixed' and patch[9].startswith('+- '), patch
assert [l for l in added if l.startswith('+- ')] == [patch[9]]            # one entry
assert 'notes add' in patch[9] and not re.search(r'\(#\d+\)', patch[9])   # names the command, cites no PR


def report(name):
    """One oracle log -> {'oracle'|'baseline': {'stimuli': {name: last line}, 'graders': {name: verdict}}}, plus the text."""
    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]|[\x04\x08\r]', '', (D / 'src/run' / name).read_text())
    out, mode, stim = {}, None, None
    for l in text.splitlines():
        if m := re.match(r'\S+ (\S+) \[(oracle|baseline)', l):
            stim, mode = m.group(1), m.group(2)
            out.setdefault(mode, {'stimuli': {}, 'graders': {}})['stimuli'][stim] = None
        elif m := re.match(r'\s+(\S) \[([^\]]+)\] (.*)', l):
            rest = m.group(3)
            v = ('failed as expected' if rest.startswith('failed as expected') else
                 'N/A' if rest.startswith('N/A') else
                 'trivially passing' if 'trivially passing' in rest else
                 'passed' if m.group(1) == '✓' else 'failed')
            out[mode]['graders'][m.group(2)] = v
        elif l.startswith('Score:') and mode:
            out[mode]['stimuli'][stim] = l.split('|', 1)[1].strip()
    return out, text


# What the narration says about each recording.
r13, t13 = report('s13.log')
assert t13.count('warning: Multiple graders with no scoring config') == 2
assert r13['oracle']['graders'] == {'adds-an-entry': 'passed', 'no-made-up-number': 'passed'}
assert r13['oracle']['stimuli'] == {'typo-fix': 'PASSED'} and 'typo-fix [oracle]' in t13
assert r13['baseline']['graders'] == {'adds-an-entry': 'failed as expected', 'no-made-up-number': 'N/A'}
assert r13['baseline']['stimuli']['typo-fix'].startswith('baseline OK')
r15, t15 = report('s15.log')
assert r15['baseline']['graders']['mentions-unreleased'] == 'trivially passing' and '❌ typo-fix' in t15
assert 'passed without the golden solution (trivially passing)' in t15
assert r15['baseline']['stimuli']['typo-fix'].startswith('baseline PROBLEM')
r17, _ = report('s17.log')
WITH, WITHOUT = r17['oracle']['graders'], r17['baseline']['graders']
assert list(r17['oracle']['stimuli']) == ['typo-fix', 'security', 'two-changes', 'after-release']
assert set(r17['oracle']['stimuli'].values()) == {'PASSED'} and set(WITH.values()) == {'passed'} and len(WITH) == 5
assert len(r17['baseline']['stimuli']) == 5 and all(v.startswith('baseline OK') for v in r17['baseline']['stimuli'].values())
BOTH = [g for _, g in GRADERS if WITH.get(g) == 'passed' and WITHOUT[g] == 'failed as expected']
UNTESTED = [g for _, g in GRADERS if WITHOUT[g] == 'N/A']
assert len(BOTH) == 4 and UNTESTED == ['no-made-up-number', 'adds-nothing'], (BOTH, UNTESTED)

TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Who grades the grader?', f'''<div class="cols pair">
    {card('g', f'{mono("changelog.eval.yaml")} · the graders on {mono("typo-fix")}', code(TYPO_GRADERS, 'yaml'))}
    <div class="cases">
      {block("right", "success", "a correct answer", "a healthy grader passes it", words=True)}
      {block("nothing", "attention", "an untouched file", "a healthy grader fails it", words=True)}
    </div>
  </div>''', [
    {"type": "focus", "target": "g", "at": "0~graders", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "right", "at": "4~correct answer", "color": "green"},
    {"type": "focus", "target": "nothing", "at": "4~untouched", "color": "yellow"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.pair{align-items:stretch}'
        '.cases{display:flex;flex-direction:column;gap:22px;justify-content:center}'
        '.cases .semantic-block{min-height:150px;justify-content:center}.cases .title{font-size:40px}.cases .label{font-size:30px}'
        '.card > .code.dark{font-size:30px;line-height:1.45}.card .who{font-size:30px}')

# ---- Two ways a grader can be wrong --------------------------------------------------------------
framed('s02', 'Who grades the grader?', 'Two ways to be wrong', f'''<div class="cols wide terms">
    {block("fails", "failure", "It fails correct work", "we chase a problem that isn’t there", words=True)}
    {block("passes", "attention", "It passes work that wasn’t done", "we stop looking at a problem that is", words=True)}
  </div>''', [
    {"type": "focus", "target": "fails", "at": "2", "color": "red"},
    {"type": "focus", "target": "passes", "at": "4", "color": "yellow"}], css=TERMS)

framed('s03', 'Who grades the grader?', 'Each test needs its example', f'''<div class="cols wide terms">
    {block("right", "success", "A result known to be correct", "if the grader fails it, the grader is wrong", words=True)}
    {block("nothing", "attention", "The starting files, untouched", "if the grader passes them, it isn’t checking the work", words=True)}
  </div>''', [
    {"type": "focus", "target": "right", "at": "1", "color": "green"},
    {"type": "focus", "target": "nothing", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], css=TERMS)

# ---- Chapter: A golden patch ---------------------------------------------------------------------
framed('s04', 'A golden patch', 'A correct answer, kept', f'''<div class="annotated">
    {panel('golden')}
    {callouts(('fixed', 'a new Fixed category'), ('entry', 'names the command, no pull request'))}
  </div>''', [
    {"type": "focus", "target": "fixed", "at": "5", "color": "green"},
    {"type": "focus", "target": "entry", "at": "6", "color": "green"}], layout='layout-file')

framed('s05', 'A golden patch', 'The eval file names it', f'''<div class="annotated">
    {panel('evalfile')}
    {callouts(('key', 'beside graders, inside the stimulus'), ('path', 'relative to the eval file'),
              ('refactor', 'no golden patch: nothing to change'))}
  </div>''', [
    {"type": "focus", "target": "key", "at": "1~golden", "color": "blue"},
    {"type": "focus", "target": "path", "at": "2", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "scroll", "target": "#evalfile", "to": "31-42", "at": "3"},
    {"type": "focus", "target": "refactor", "at": "4", "color": "yellow"}], layout='layout-file')

# ---- Chapter: What the oracle does ---------------------------------------------------------------
def column(k, cmd, steps, outcome):
    return f'''<div class="col">
      {code(f'⟦cmd-{k}:{cmd}⟧', 'bash')}
      {''.join(block(f'{k}{i}', role, t, '', words=True, step=i) for i, (role, t) in enumerate(steps, 1))}
      <p class="lead"><span data-concept="out-{k}" data-rep="note">{outcome}</span></p>
    </div>'''


TWO = f'''<div class="cols two">
    {column('a', 'vally oracle', [('structure', 'Fresh workspace'), ('success', 'Apply the golden patch'), ('transform', 'Run the graders')],
            'every grader should pass')}
    {column('b', 'vally oracle --no-golden-input', [('structure', 'Fresh workspace'), ('attention', 'Apply nothing'), ('transform', 'Run the graders')],
            'every grader should fail')}
  </div>'''
TWO_CSS = ('.two{align-items:start}.col{display:flex;flex-direction:column;gap:14px}'
           '.col .code.dark{font-size:34px;padding:18px 26px}'
           '.col .semantic-block{flex-direction:row;align-items:center;gap:22px;min-height:0;padding:16px 26px}'
           '.col .semantic-block .title{font-size:38px}.col .semantic-block .label{display:none}'
           '.col .lead{font-size:36px;margin:6px 0 0}')
framed('s06', 'What the oracle does', 'The oracle plays the agent', TWO, [
    {"type": "focus", "target": "cmd-a", "at": "1", "color": "blue"},
    {"type": "focus", "target": "a1", "at": "3~workspace", "color": "blue"},
    {"type": "focus", "target": "a2", "at": "4~golden patch", "color": "green"},
    {"type": "focus", "target": "a3", "at": "6", "color": "cyan"},
    {"type": "focus", "target": "out-a", "at": "6~correct answer", "color": "green"}], css=TWO_CSS)

framed('s07', 'What the oracle does', 'The oracle plays the agent', TWO, [
    {"type": "focus", "target": "cmd-b", "at": "0", "color": "blue"},
    {"type": "focus", "target": "b2", "at": "1~baseline", "color": "yellow"},
    {"type": "focus", "target": "out-a", "at": "2~everything right", "color": "green"},
    {"type": "focus", "target": "out-b", "at": "2~did nothing", "color": "yellow"}], css=TWO_CSS)

SAYS = ('⟦fae:✓ failed as expected⟧\n\n⟦na:⊘ N/A⟧\n\n'
        '⟦triv:✗ passed without the golden solution⟧\n⟦triv:  (trivially passing)⟧')
framed('s08', 'What the oracle does', 'Three reports on the baseline', f'''<div class="annotated">
    {card('says', 'what the oracle says about a grader, with nothing applied', code(SAYS, 'text'))}
    {callouts(('fae', 'it depends on the work: good'), ('na', 'an absence check: not tested'),
              ('triv', f'it depends on nothing: {mono("baseline PROBLEM")}'))}
  </div>''', [
    {"type": "focus", "target": "fae", "at": "0~failed as expected", "color": "green"},
    {"type": "focus", "target": "na", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "triv", "at": "5", "color": "red"}],
    css='.card > .code.dark{font-size:36px;line-height:1.5;padding:26px 32px;min-width:900px}.card .who{font-size:30px}'
        '.callout{font-size:32px}.callouts{margin-top:52px}')

CMD = ('vally oracle ⟦e:-e evals/changelog.eval.yaml⟧ \\\n  ⟦stim:--stimulus typo-fix⟧ \\\n  ⟦verbose:--verbose⟧')
framed('s09', 'What the oracle does', 'One stimulus, with evidence', f'''<div class="annotated">
    {code(CMD, 'bash')}
    {callouts(('e', 'the eval file, as for vally eval'), ('stim', 'only this stimulus'), ('verbose', 'each grader’s evidence'))}
  </div>''', [
    {"type": "focus", "target": "e", "at": "0~dash e", "color": "blue"},
    {"type": "focus", "target": "stim", "at": "1", "color": "blue"},
    {"type": "focus", "target": "verbose", "at": "2", "color": "blue"},
    {"type": "focus", "target": "stim", "at": "3~stimulus", "color": "yellow"}],
    css='.annotated .code.dark{font-size:38px;line-height:1.8;padding:30px 36px}.callout{font-size:34px}')

# ---- Chapter: Prove the graders ------------------------------------------------------------------
def table(filled):
    body, last = '', None
    for s, g in GRADERS:
        w = (WITH.get(g) or 'not run: no golden patch') if filled else ''
        wo = WITHOUT[g] if filled else ''
        tag = 'both' if g in BOTH else 'untested'
        wc = {'passed': 'passed'}.get(w, 'notrun')
        woc = {'failed as expected': 'fae', 'N/A': 'na'}.get(wo, 'other')
        body += (f'<tr><td class="mono stim">{s if s != last else ""}</td>'
                 f'<td class="mono"><span data-concept="{tag}" data-rep="cell">{g}</span></td>'
                 f'<td><span data-concept="{wc}" data-rep="cell">{w}</span></td>'
                 f'<td><span data-concept="{woc}" data-rep="cell">{wo}</span></td></tr>\n')
        last = s
    return f'''<table class="data-table full both">
    <thead><tr><th>Stimulus</th><th>Grader</th><th><span data-concept="c-with" data-rep="head">With the golden patch</span></th><th><span data-concept="c-without" data-rep="head">Without it</span></th></tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


TABLE_CSS = ('.both{font-size:32px}.both th{font-size:30px}.both td{padding-top:13px;padding-bottom:13px}'
             '.both td.mono{font-family:var(--font-code);font-size:30px}.stage{justify-content:flex-start}')
framed('s10', 'Prove the graders', 'Both tests, every grader', table(False), [
    {"type": "focus", "target": "c-with", "at": "1~golden patch", "color": "green"},
    {"type": "focus", "target": "c-without", "at": "4~untouched", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], css=TABLE_CSS)

framed('s12', 'Prove the graders', 'Two lines, above graders', f'''<div class="annotated">
    {panel('evalfile')}
    {callouts(('lines', 'added just above graders'))}
  </div>''', [
    {"type": "focus", "target": "lines", "at": "0~two lines", "color": "blue"}], layout='layout-file')

framed('s14', 'Prove the graders', 'A grader that can’t fail', f'''<div class="annotated">
    {panel('evalfile')}
    {callouts(('name', 'added on purpose, to be caught'), ('value', 'the starting changelog already has this word'))}
  </div>''', [
    {"type": "focus", "target": "name", "at": "1~mentions", "color": "yellow"},
    {"type": "focus", "target": "value", "at": "2", "color": "red"}], layout='layout-file')

TREE = ('evals/golden/\n  typo-fix.patch\n  ⟦new:security.patch⟧\n  ⟦new:two-changes.patch⟧\n  ⟦new:after-release.patch⟧')
framed('s16', 'Prove the graders', 'Golden patches for the rest', f'''<div class="annotated">
    {code(TREE, 'text', 'tree')}
    {callouts(('new', 'each from a trial we read and judged correct'))}
  </div>
  <p class="lead"><span data-concept="ref" data-rep="note">{mono("refactor")} has none: its correct answer changes nothing</span></p>''', [
    {"type": "focus", "target": "new", "at": "1", "color": "green"},
    {"type": "focus", "target": "ref", "at": "3", "color": "yellow"}],
    css='.code.dark.tree{min-width:760px;font-size:38px;line-height:1.6}.callout{font-size:34px}.lead{font-size:38px;margin:0}.stage{gap:36px}')

framed('s18', 'Prove the graders', 'Grader by grader', table(True), [
    {"type": "focus", "target": "passed", "at": "1", "color": "green"},
    {"type": "focus", "target": "fae", "at": "2~failed as expected", "color": "green"},
    {"type": "focus", "target": "na", "at": "2~two are", "color": "yellow"}], css=TABLE_CSS)

# ---- Chapter: What the oracle didn't test --------------------------------------------------------
framed('s19', 'What the oracle didn’t test', 'Two graders remain untested', table(True), [
    {"type": "focus", "target": "both", "at": "1", "color": "green"},
    {"type": "focus", "target": "untested", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "na", "at": "3~N/A", "color": "yellow"},
    {"type": "focus", "target": "untested", "at": "4", "color": "yellow"}], css=TABLE_CSS)

framed('s20', 'What the oracle didn’t test', 'One correct answer each', f'''<div class="cols wide terms">
    {block("tried", "success", "Tried", "the one correct answer we chose", words=True)}
    {block("not", "attention", "Not tried", "another correct answer, worded differently", words=True)}
  </div>''', [
    {"type": "focus", "target": "tried", "at": "1", "color": "green"},
    {"type": "focus", "target": "not", "at": "2", "color": "yellow"}], css=TERMS)

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('with the golden patch', 'plays an agent that got everything right · a healthy grader passes'),
    ('--no-golden-input', 'plays an agent that did nothing · a healthy grader fails')], 1))
framed('s21', 'Recap', 'What are the oracle’s two tests?', f'''<div class="semantic-block" id="tests" data-role="structure">
    <div class="title">vally oracle</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#tests", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "green"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"}], layout='layout-expand',
    css='#tests{width:100%;padding:36px 40px 44px;gap:24px}'
        '#tests .parts{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;width:100%}'
        '#tests .part{min-height:280px}#tests .part .title{font-size:46px;line-height:1.2}'
        '#tests .part .label{font-size:32px}')

scene('s22', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Check graders against saved trials</h1>
  <p class="lead">Can the graders be run on the answers you have already saved?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “CLI: oracle”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok')
