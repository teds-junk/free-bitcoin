"""Generate lesson 8's scene pages, then insert their file panels.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/changelog.eval.yaml          the eval file as the practice folder has it (correct pattern)
  src/state/changelog.flawed.eval.yaml   the same file with (?m) deleted from no-made-up-number
  src/run/                               what this video's own commands printed, in the series' own
                                         demo folder (filled by build-src/capture-run.sh; see
                                         src/run/PROVISIONAL while it still holds stand-ins)

Every count the narration states is asserted below. If a real run differs, this script fails and the
`outcome` sentences in storyboard.json are reworded to what happened.

Run from anywhere:  python3 build-src/make-scenes.py
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


def fp(*args):
    """Insert a file panel into a scene (scripts/file-panel.js), run from the video directory."""
    subprocess.run(['node', str(SKILL / 'scripts/file-panel.js'), *args], cwd=D, check=True,
                   capture_output=True, text=True)


# ---- The real things, read from src/ -----------------------------------------------------------
read = lambda p: (D / 'src' / p).read_text()
RUN = read('run/RUN').strip()

# The grader, as the eval file has it and as we first wrote it: one line differs, by four characters.
right, flawed = read('state/changelog.eval.yaml').splitlines(), read('state/changelog.flawed.eval.yaml').splitlines()
differ = [i for i, (a, b) in enumerate(zip(right, flawed)) if a != b]
assert len(right) == len(flawed) and differ == [28], differ
P_RIGHT, P_FLAWED = right[28].strip(), flawed[28].strip()
assert P_RIGHT == r"pattern: '(?m)^\+.*\(#\d+\)'" and P_FLAWED == r"pattern: '^\+.*\(#\d+\)'"
assert right[25].strip() == '- type: diff-not-contains' and right[26].strip() == 'name: no-made-up-number'

# A saved trial we know is bad: its patch adds one entry, ending with a number nobody gave it.
PR = re.compile(r'\(#\d+\)\s*$')
patch = read('run/bad-trial.patch').splitlines()
assert patch[0].startswith('diff --git') and not patch[0].startswith('+')
added = [i for i, l in enumerate(patch, 1) if l.startswith('+- ')]
assert len(added) == 1, added
ENTRY_LINE = added[0]
ENTRY = patch[ENTRY_LINE - 1][1:]
assert PR.search(ENTRY), ENTRY
assert re.search(r'(?m)^\+.*\(#\d+\)', '\n'.join(patch)) and not re.search(r'^\+.*\(#\d+\)', '\n'.join(patch))
mark_pr = lambda e, cid='pr': PR.sub(lambda m: f'⟦{cid}:{m.group(0).strip()}⟧', e)


def blocks(path):
    """The blocks a re-grade printed: [(stimulus, passed, [(grader, evidence line)], lines)]."""
    out, cur = [], None
    for l in read(path).splitlines():
        m = re.match(r'━━━ (\S+) ━━━', l)
        if m:
            cur = [m.group(1), None, [], [l]]
            out.append(cur)
        elif cur and l.strip():
            cur[3].append(l)
            if l.startswith('✅') or l.startswith('❌'):
                cur[1] = l.startswith('✅')
            g = re.match(r'\s+✗ \[([^\]]+)\]', l)
            if g:
                cur[2].append((g.group(1), l))
    assert all(b[1] is not None for b in out), path
    return out


def typo_counts(bs):
    t = [b for b in bs if b[0] == 'typo-fix']
    named = lambda g: sum(any(n == g for n, _ in b[2]) for b in t)
    return {'trials': len(t), 'passed': sum(b[1] for b in t),
            'nmn': named('no-made-up-number'), 'aae': named('adds-an-entry')}


BEFORE, FLAWED, RESTORED = blocks('run/grade-before.txt'), blocks('run/grade-flawed.txt'), blocks('run/grade-restored.txt')
CB, CF = typo_counts(BEFORE), typo_counts(FLAWED)
# What the narration says about these re-grades. If the real run differs, the sentences change too.
assert len(BEFORE) == len(FLAWED) == 18, (len(BEFORE), len(FLAWED))                # s10, s14: "eighteen blocks"
assert CB == {'trials': 6, 'passed': 3, 'nmn': 2, 'aae': 1}, CB                      # s11
assert CF == {'trials': 6, 'passed': 5, 'nmn': 0, 'aae': 1}, CF                      # s15
assert [(b[0], b[1], [g for g, _ in b[2]]) for b in RESTORED] == \
       [(b[0], b[1], [g for g, _ in b[2]]) for b in BEFORE]                          # s16: "matches the first"
REFACTOR = [b for b in BEFORE if b[0] == 'refactor']
assert len(REFACTOR) == 6 and all([g for g, _ in b[2]] == ['adds-nothing'] for b in REFACTOR)   # s18
# The oracle, asked about the flawed grader (s13).
o1, o2 = read('run/oracle-flawed.txt'), read('run/oracle-flawed-baseline.txt')
assert 'PASSED' in o1 and r'/^\+.*\(#\d+\)/ not found' in o1
assert re.search(r'\[adds-an-entry\] failed as expected', o2) and re.search(r'\[no-made-up-number\] N/A', o2)
assert 'baseline OK' in o2.strip().splitlines()[-1]
# The oracle's line about the grader with the right pattern, from the earlier oracle run (s01).
NA = next(l for l in read('run/oracle-baseline.txt').splitlines() if '[no-made-up-number]' in l)
assert ' N/A — ' in NA and '(?m)' in NA
na_parts = NA.strip().split(' — ')
NA_SHOWN = na_parts[0].replace('N/A', '⟦na:N/A⟧') + ' — ' + na_parts[1] + '\n    — ' + ' — '.join(na_parts[2:])

TERMS_CSS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Check graders against saved trials', f'''<div class="results">
      {card('card-a', 'the oracle, on an untouched file', code(NA_SHOWN, 'text'))}
      {card('card-b', 'a saved trial · the entry it added', code(mark_pr(ENTRY), 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "na", "at": "0~vouch", "color": "yellow"},
    {"type": "focus", "target": "pr", "at": "2~make up", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:100px}'
        '.results{display:flex;flex-direction:column;gap:36px;width:100%}'
        '.results .card > .code.dark{font-size:34px;padding:26px 34px}.results .card .who{font-size:32px}')

# ---- Chapter: Saved trials are tests -------------------------------------------------------------
framed('s02', 'Saved trials are tests', 'Every saved trial has an answer', f'''<div class="cols wide terms">
    {block("bad", "attention", "A trial you know is bad", "tests a grader that checks for absence: the grader must fail it", words=True)}
    {block("good", "structure", "A trial you know is good, worded differently", "tests whether a grader is too strict", words=True)}
  </div>''', [
    {"type": "focus", "target": "bad", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "good", "at": "4", "color": "blue"},
    {"type": "focus", "target": "none", "at": "6~wording"}],
    css=TERMS_CSS)

framed('s03', 'Saved trials are tests', 'A must-not grader needs a failure', f'''<div class="annotated">
    {panel('grader')}
    {callouts(('type', 'passes when the pattern is absent'))}
  </div>
  {card('known-bad', 'a saved trial we know is bad · the entry it added', code(mark_pr(ENTRY), 'markdown'))}''', [
    {"type": "focus", "target": "type", "at": "0~absent", "color": "blue"},
    {"type": "focus", "target": "pr", "at": "1~number nobody", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    layout='layout-file',
    css='.card > .code.dark{font-size:32px;padding:18px 28px}.card .who{font-size:30px}.stage{gap:26px}.callout{font-size:32px}')

# ---- Chapter: Re-grade a saved run ---------------------------------------------------------------
GRADE = ('⟦cmd:vally grade⟧ ⟦e:-e ../../../evals/changelog.eval.yaml⟧ \\\n'
         '  ⟦rundir:--run-dir .⟧ ⟦input:< results.jsonl⟧')
framed('s04', 'Re-grade a saved run', 'Grade again, with no agent', f'''<div class="annotated">
    {code(GRADE, 'bash')}
    {callouts(('e', 'the graders, as they are now'), ('input', 'the saved trials, as input'))}
  </div>
  <p class="note">no agent starts · nothing is spent</p>''', [
    {"type": "focus", "target": "cmd", "at": "1~grade", "color": "blue"},
    {"type": "focus", "target": "e", "at": "3~Dash e", "color": "blue"},
    {"type": "focus", "target": "input", "at": "6~results", "color": "yellow"},
    {"type": "focus", "target": "rundir", "at": "7~run dir", "color": "orange"}],
    css='.annotated .code.dark{font-size:36px;line-height:1.9;padding:34px 40px}.callout{font-size:32px}')

TREE = (f'⟦run:{RUN}/⟧\n'
        '  ⟦rec:results.jsonl⟧\n'
        '  ⟦diffs:diffs/⟧\n'
        '  changelog/typo-fix/gpt-5.6-terra/0/\n'
        '    ⟦patch:workspace.patch⟧')
framed('s05', 'Re-grade a saved run', 'A run keeps its diffs', f'''<div class="annotated">
    {code(TREE, 'text', 'tree')}
    {callouts(('run', 'one saved run'), ('rec', 'one record per trial'), ('diffs', 'a copy of every trial’s diff'),
              ('patch', 'the same diff, for us to read'))}
  </div>
  <p class="note"><span class="mono">diffs/</span> is kept only when the eval file has a diff grader</p>''', [
    {"type": "focus", "target": "patch", "at": "0~workspace patch", "color": "blue"},
    {"type": "focus", "target": "diffs", "at": "1~diffs", "color": "yellow"},
    {"type": "focus", "target": "run", "at": "2~which run", "color": "orange"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "diffs", "at": "4~no copies", "color": "yellow"}],
    css='.code.dark.tree{min-width:860px;font-size:36px;line-height:1.7}.callout{font-size:32px}')

framed('s06', 'Re-grade a saved run', 'Script graders can’t be re-graded', f'''<div class="cols wide terms">
    {block("diffg", "success", "diff grader", "works from the saved diff · its result holds", words=True)}
    {block("scriptg", "failure", "script grader", "needs the workspace, which is gone · fails every trial", words=True)}
  </div>
  <div class="annotated">
    {code('⟦msg:no CHANGELOG.md to check⟧', 'text')}
    {callouts(('msg', 'what our script says in a re-grade'))}
  </div>''', [
    {"type": "focus", "target": "diffg", "at": "1", "color": "green"},
    {"type": "focus", "target": "scriptg", "at": "2", "color": "red"},
    {"type": "focus", "target": "msg", "at": "4~no changelog", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.terms .semantic-block{min-height:210px}.terms .label{font-size:32px}'
        '.annotated .code.dark{font-size:38px;padding:24px 36px}.callout{font-size:32px}.stage{gap:34px}')

quoted = lambda p: p.split(': ', 1)[1]
PATTERNS = (f'pattern: ⟦first:{quoted(P_FLAWED)}⟧\n'
            f"pattern: '⟦sw:(?m)⟧" + quoted(P_RIGHT)[len("'(?m)"):])
framed('s07', 'Re-grade a saved run', 'A pattern that looks right', f'''<div class="annotated">
    {code(PATTERNS, 'yaml')}
    {callouts(('first', 'as we first wrote it'), ('sw', 'as the eval file has it'))}
  </div>
  <p class="note">the pattern of <span class="mono">no-made-up-number</span>, a <span class="mono">diff-not-contains</span> grader</p>''', [
    {"type": "focus", "target": "first", "at": "1~pattern", "color": "yellow"},
    {"type": "focus", "target": "sw", "at": "2~four characters", "color": "blue"},
    {"type": "focus", "target": "first", "at": "3~plus sign", "color": "yellow"},
    {"type": "focus", "target": "first", "at": "4", "color": "red"}],
    css='.annotated .code.dark{font-size:44px;line-height:2;padding:34px 44px}.callout{font-size:34px}')

framed('s08', 'Re-grade a saved run', 'No patch starts with a plus', f'''<div class="annotated">
    {panel('patch')}
    {callouts(('start', 'without (?m), ^ means only here'), ('entry', 'the line the grader has to find'))}
  </div>''', [
    {"type": "focus", "target": "entry", "at": "1~every line", "color": "blue"},
    {"type": "focus", "target": "start", "at": "2~very start", "color": "yellow"},
    {"type": "focus", "target": "entry", "at": "4~made-up numbers", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file', css='.callout{font-size:32px}')

# ---- Chapter: Catch a grader that cannot fail ----------------------------------------------------
STEP_CSS = '.steps .semantic-block{min-height:330px}.steps .label{font-size:32px}'
framed('s09', 'Catch a grader that cannot fail', 'Four steps, no agent runs', f'''<div class="cols steps">
    {block("st1", "structure", "re-grade", "the saved run, with the graders as they are", step=1, words=True)}
    {block("st2", "change", "swap", "the flawed pattern goes in", step=2, words=True)}
    {block("st3", "attention", "ask twice", "the oracle, then the saved trials", step=3, words=True)}
    {block("st4", "success", "restore", "the right pattern goes back", step=4, words=True)}
  </div>''', [
    {"type": "focus", "target": "st1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "st2", "at": "2", "color": "orange"},
    {"type": "focus", "target": "st3", "at": "2~ask the oracle", "color": "yellow"},
    {"type": "focus", "target": "st4", "at": "3", "color": "green"},
    {"type": "focus", "target": "none", "at": "4"}], css=STEP_CSS)


def typo_lines(bs):
    out = []
    for b in [b for b in bs if b[0] == 'typo-fix']:
        verdict = next(l for l in b[3] if l.startswith('✅') or l.startswith('❌'))
        out.append(f'⟦ok:{verdict}⟧' if b[1] else verdict)
        for g, line in b[2]:
            cid = {'no-made-up-number': 'nmn', 'adds-an-entry': 'aae'}[g]
            out.append(line.replace(f'[{g}]', f'[⟦{cid}:{g}⟧]', 1))
    return '\n'.join(out)


framed('s11', 'Catch a grader that cannot fail', 'Six trials of one stimulus', f'''<div class="lists">
    {card('six', f'the re-grade · the six {mono("typo-fix")} blocks, each one’s verdict and the grader it names',
          code(typo_lines(BEFORE), 'text'))}
  </div>
  <p class="note">from our run · {RUN} · the blocks do not name the model</p>''', [
    {"type": "focus", "target": "ok", "at": "1~Three passed", "color": "green"},
    {"type": "focus", "target": "nmn", "at": "2~no made-up number", "color": "yellow"},
    {"type": "focus", "target": "aae", "at": "3~adds an entry", "color": "blue"}],
    css='.lists{display:flex;flex-direction:column;width:100%}'
        '.lists .card > .code.dark{font-size:31px;line-height:1.5;padding:20px 28px}.lists .card .who{font-size:30px}'
        '.stage{gap:22px}')

framed('s12', 'Catch a grader that cannot fail', 'Four characters come out', f'''<div class="annotated">
    {panel('flawed')}
    {callouts(('pattern', '(?m) deleted from the front'))}
  </div>''', [
    {"type": "focus", "target": "name", "at": "1~no made-up number", "color": "blue"},
    {"type": "focus", "target": "pattern", "at": "1~four characters", "color": "orange"},
    {"type": "focus", "target": "none", "at": "2"}], layout='layout-file', css='.callout{font-size:32px}')

cell = lambda cid, n: f'<td class="num"><span data-concept="{cid}" data-rep="cell">{n}</span></td>'
framed('s15', 'Catch a grader that cannot fail', 'The grader cannot fail', f'''<table class="data-table full cmp">
    <thead><tr><th>the six {mono("typo-fix")} trials, re-graded</th><th class="num">passed</th>
      <th class="num">failed {mono("no-made-up-number")}</th><th class="num">failed {mono("adds-an-entry")}</th></tr></thead>
    <tbody>
      <tr><td>with the right pattern</td>{cell('b-pass', CB['passed'])}{cell('b-nmn', CB['nmn'])}{cell('b-aae', CB['aae'])}</tr>
      <tr><td>with the flawed pattern</td>{cell('f-pass', CF['passed'])}{cell('f-nmn', CF['nmn'])}{cell('f-aae', CF['aae'])}</tr>
    </tbody>
  </table>
  {card('still', 'still in a saved patch, in both re-grades', code(mark_pr(ENTRY), 'markdown'))}''', [
    {"type": "focus", "target": "b-nmn", "at": "0~two failed", "color": "yellow"},
    {"type": "focus", "target": "f-nmn", "at": "1~none", "color": "red"},
    {"type": "focus", "target": "pr", "at": "1~made up", "color": "yellow"},
    {"type": "focus", "target": "f-pass", "at": "2~Five", "color": "red"},
    {"type": "focus", "target": "f-aae", "at": "2~sixth", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.cmp{font-size:52px}.cmp th{font-size:28px}.cmp td{padding-top:26px;padding-bottom:26px}'
        '.cmp td:first-child{font-size:36px}.cmp th:last-child,.cmp td:last-child{padding-right:16px}'
        '.card > .code.dark{font-size:32px;padding:18px 28px}.card .who{font-size:30px}.stage{gap:30px}')

# ---- Chapter: A habit for every grader -----------------------------------------------------------
framed('s17', 'A habit for every grader', 'The oracle couldn’t tell', f'''<div class="cols wide terms">
    {block("orc", "structure", "the oracle", "accepted the flawed grader", words=True)}
    {block("saved", "attention", "the saved trials", "showed that it cannot fail", words=True)}
  </div>''', [
    {"type": "focus", "target": "orc", "at": "2", "color": "blue"},
    {"type": "focus", "target": "saved", "at": "3", "color": "yellow"}], css=TERMS_CSS)

rb = REFACTOR[0]
RB = '\n'.join(l.replace('[adds-nothing]', '[⟦an:adds-nothing⟧]', 1) for l in rb[3] if not l.startswith('Score'))
framed('s18', 'A habit for every grader', 'The same run settled another', f'''<div class="lists">
    {card('rblock', f'the first re-grade · one of the six {mono("refactor")} blocks', code(RB, 'text'))}
  </div>
  <div class="cols wide terms">
    {block("six", "attention", f"{len(REFACTOR)} of {len(REFACTOR)}", f'{mono("refactor")} trials that {mono("adds-nothing")} failed')}
  </div>''', [
    {"type": "focus", "target": "an", "at": "1~Adds nothing", "color": "blue"},
    {"type": "focus", "target": "six", "at": "1~all six", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.lists{display:flex;flex-direction:column;width:100%}'
        '.lists .card > .code.dark{font-size:30px;line-height:1.5;padding:18px 28px}.lists .card .who{font-size:30px}'
        '.terms .semantic-block{min-height:190px;justify-content:center}.terms .title{font-size:84px;line-height:1.1}'
        '.terms .label{font-size:34px}.stage{gap:28px}')

framed('s19', 'A habit for every grader', 'Oracle, saved run, then agents', f'''<div class="cols steps">
    {block("h1", "structure", "oracle", "a correct answer, and an untouched file · free", step=1, words=True)}
    {block("h2", "attention", "re-grade", "a saved run where the failure is known to occur · free", step=2, words=True)}
    {block("h3", "change", "agent runs", "only then · paid", step=3, words=True)}
  </div>''', [
    {"type": "focus", "target": "h1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "h2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "h3", "at": "3", "color": "orange"}], css=STEP_CSS)

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('the oracle', 'an untouched file passes it honestly, so it is marked N/A'),
    ('a saved bad trial', 'in a re-grade, the grader must fail it')], 1))
framed('s20', 'Recap', 'What tests a must-not grader?', f'''<div class="semantic-block" id="kind" data-role="structure">
    <div class="title words">a grader that checks for absence</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#kind", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"}], layout='layout-expand',
    css='#kind{width:100%;padding:36px 40px 44px;gap:24px}'
        '#kind .parts{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;width:100%}'
        '#kind .part{min-height:280px}#kind .part .title{font-size:52px;line-height:1.2}'
        '#kind .part .label{font-size:32px}')

scene('s21', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Does the skill load?</h1>
  <p class="lead">Will it load for other wordings, and stay out of requests that are not its job?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “CLI: grade”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')

# ---- File panels (the generator above cleared them) ----------------------------------------------
fp('--file', 'src/state/changelog.eval.yaml', '--label', 'evals/changelog.eval.yaml', '--id', 'grader',
   '--width', '46', '--rows', '6', '--show', '26-29', '--expect', '29=(?m)',
   '--mark', '26=type:diff-not-contains', '--mark', '29=pat', '--into', 'scenes/s03.html')
fp('--file', 'src/run/bad-trial.patch', '--label', 'workspace.patch · a saved trial', '--id', 'patch',
   '--width', '46', '--rows', '8', '--show', f'1-4,{ENTRY_LINE - 1}-{ENTRY_LINE}', '--expect', '1=diff --git',
   '--mark', '1=start', '--mark', f'{ENTRY_LINE}=entry', '--into', 'scenes/s08.html')
fp('--file', 'src/state/changelog.flawed.eval.yaml', '--label', 'evals/changelog.eval.yaml', '--id', 'flawed',
   '--width', '46', '--rows', '6', '--show', '26-29', '--expect', "29=pattern: '^",
   '--mark', '27=name:no-made-up-number', '--mark', '29=pattern', '--into', 'scenes/s12.html')
print('ok')
