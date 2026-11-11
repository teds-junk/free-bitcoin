"""Generate lesson 9's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout), terms in
blocks, numbers in a .data-table. Nothing here sets a colour or a font outside the theme's variables;
a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/SKILL.before.md, SKILL.after.md   the skill before and after this lesson's one edit
  src/state/loading.eval.yaml                 the loading eval file from the starter
  src/record.json                             one trial's record from the lesson 1 video's run
  src/earlier-eval-results.md                 the report of the lesson 3 video's five-trial run
  src/run/                                    the two runs this video's s16 and s19 recorded (the
                                              third take of s16, the second of s19), copied by
                                              build-src/extract-run.py, with /Users/Shared/demo
                                              shown as ~/src/demo
  src/earlier/                                an earlier run of the same test with the one-line
                                              description (verified/lesson-09's report and console
                                              output of 2026-11-10): the only saved evidence of a miss

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
SHORT = {'claude-haiku-4.5': 'haiku', 'gpt-5.6-terra': 'terra'}
KEY = {'claude-haiku-4.5': 'h', 'gpt-5.6-terra': 't'}
OURS = 'changelog-entry'
assert not (D / 'src/run/PROVISIONAL').exists()


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


def block(cid, role, title, label, words=True):
    lab = f'<div class="label">{label}</div>' if label else ''
    return f'''<div class="semantic-block" data-concept="{cid}" data-rep="block" data-role="{role}">
      <div class="title{' words' if words else ''}">{title}</div>{lab}
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


def cell(cid, text, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<td{c}><span data-concept="{cid}" data-rep="cell">{text}</span></td>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---- The real things, read from src/ ---------------------------------------------------------------
before_skill = (D / 'src/state/SKILL.before.md').read_text().splitlines()
after_skill = (D / 'src/state/SKILL.after.md').read_text().splitlines()
OLD_DESC = 'description: Adds an entry to the project changelog.'
assert before_skill[2] == OLD_DESC, before_skill[2]
assert after_skill[2] == 'description: >-' and after_skill[8] == '---'
# The lesson's one edit: the description line becomes six lines, and nothing else changes.
assert before_skill[:2] + before_skill[3:] == after_skill[:2] + after_skill[8:]
RULES = before_skill[9:13]
assert RULES[0].startswith('- Add the entry under Unreleased') and RULES[3] == '- Leave released versions alone.'


def stimuli():
    """name, prompt (one line), list name ('required' | 'disallowed') for each stimulus, in file order."""
    out, lines = [], (D / 'src/state/loading.eval.yaml').read_text().splitlines()
    i = lines.index('stimuli:') + 1
    while i < len(lines):
        m = re.match(r'  - name: (\S+)$', lines[i])
        if m:
            assert lines[i + 1] == '    prompt: |'
            j, prompt = i + 2, []
            while lines[j].startswith('      '):
                prompt.append(lines[j].strip()); j += 1
            assert lines[j] == '    graders:' and lines[j + 1] == '      - type: skill-invocation'
            g = re.match(r'          (required|disallowed): \[changelog-entry\]$', lines[j + 3])
            assert g, lines[j + 3]
            out.append((m.group(1), ' '.join(prompt), g.group(1)))
            i = j + 3
        i += 1
    return out


STIM = stimuli()
NAMES = [n for n, _, _ in STIM]
assert NAMES == ['load-plain', 'load-no-keyword', 'load-indirect', 'skip-commit', 'skip-release-notes', 'skip-question']
assert [g for _, _, g in STIM] == ['required'] * 3 + ['disallowed'] * 3
PROMPT = {n: p for n, p, _ in STIM}
LOAD, SKIP = NAMES[:3], NAMES[3:]
# "Only the first of them says changelog."
assert [('changelog' in PROMPT[n].lower()) for n in LOAD] == [True, False, False]


def report(path):
    """{model: {stimulus: (skills cell, pass-rate cell)}} from a report's tables, backticks removed."""
    out, model = {}, None
    for line in (D / path).read_text().splitlines():
        m = re.match(r'### \S+ \[([^\]]+)\]', line)
        if m:
            model = m.group(1); out[model] = {}
        elif model and line.startswith('| ') and not line.startswith('| Stimulus') and not line.startswith('|---'):
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            assert len(c) == 12, (len(c), line[:80])
            out[model][c[0]] = (c[2].replace('`', ''), c[4])
    return out


EARLIER = report('src/earlier-eval-results.md')
# s10: "the changelog entry skill loaded five times on each model."
assert EARLIER == {m: {'typo-fix': ('changelog-entry (5×)', '5/5')} for m in MODELS}, EARLIER

BEFORE_REPORT = report('src/run/before/eval-results.md')
assert set(BEFORE_REPORT) == set(MODELS) and all(set(BEFORE_REPORT[m]) == set(NAMES) for m in MODELS)

COUNTS = json.loads((D / 'src/run/counts.json').read_text())
B, A = COUNTS['before']['models'], COUNTS['after']['models']
for run in (B, A):
    assert set(run) == set(MODELS) and all(set(run[m]) == set(NAMES) for m in MODELS)
    assert all(sum(run[m][n][k] for k in ('passed', 'failed', 'errors')) == 2 for m in MODELS for n in NAMES)


def console(path):
    """The end of a run's console output: everything from the last 'Failures' heading, or from the
    last 'Model summary' when nothing failed. Progress redraws before it are dropped."""
    t = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', (D / path).read_text()).replace('\r', '\n')
    k = max(t.rfind('\nFailures'), -1)
    return t[k if k >= 0 else t.rfind('\nModel summary'):]


def summary(con):
    """The 'eval / loading' table's two cells, e.g. ('✓ 6/6', '✘ 5/6'), and the Failures list's lines."""
    m = re.findall(r'^\s*loading\s+([✘✔✓] \d/6)\s+([✘✔✓] \d/6)\s*$', con, re.M)
    assert m, 'no model table in console output'
    return m[-1], re.findall(r'^\s*(✘|ERROR) loading · (\S+) \[([^\]]+)\]', con, re.M)


CON_B, CON_A = console('src/run/before/console.txt'), console('src/run/after/console.txt')
(TB, FB), (TA, FA) = summary(CON_B), summary(CON_A)
H, T = MODELS
cnt = lambda p=2, f=0, e=0: {'passed': p, 'failed': f, 'errors': e}
core = lambda c: {k: c[k] for k in ('passed', 'failed', 'errors')}

# ---- What the narration says about our two runs. If a recording changes these, the sentences change. ----
# s16: the list has a single line, an ERROR on terra (skip-release-notes); no loading failure; 6/6 and 5/6.
assert FB == [('ERROR', 'skip-release-notes', T)], FB
assert 'Session disconnected' in CON_B and 'not called' not in CON_B
assert TB == ('✓ 6/6', '✘ 5/6'), TB
ERR_B = [(m, n) for m in MODELS for n in NAMES if B[m][n]['errors']]
assert ERR_B == [(T, 'skip-release-notes')] and core(B[T]['skip-release-notes']) == cnt(1, 0, 1)
assert all(core(B[m][n]) == cnt() for m in MODELS for n in NAMES if (m, n) not in ERR_B)
# s17: skip stimuli name a neighbour or show a dash; every load stimulus shows our skill in both trials.
for m in MODELS:
    for n in SKIP:
        assert BEFORE_REPORT[m][n][0] in ('—', 'commit-message (2×)', 'release-notes (2×)', 'release-notes'), BEFORE_REPORT[m][n]
        assert B[m][n]['skills'].get(OURS, 0) == 0
    for n in LOAD:
        assert BEFORE_REPORT[m][n] == (f'{OURS} (2×)', '2/2') and B[m][n]['skills'].get(OURS) == 2
# s19: every trial finished; one line, terra's skip-question failing the grader that forbids our skill,
# in one of two trials; 6/6 and 5/6.
assert FA == [('✘', 'skip-question', T)], FA
assert 'skill-invocation forbids changelog-ent' in CON_A
assert TA == ('✓ 6/6', '✘ 5/6'), TA
assert not any(A[m][n]['errors'] for m in MODELS for n in NAMES)
assert core(A[T]['skip-question']) == cnt(1, 1, 0) and A[T]['skip-question']['skills'].get(OURS) == 1
# s20, s21: that is the only cell with a failed trial, in either run; it was 2 of 2 before.
FAILED = [(r, m, n) for r, run in (('before', B), ('after', A)) for m in MODELS for n in NAMES if run[m][n]['failed']]
assert FAILED == [('after', T, 'skip-question')], FAILED
assert core(B[T]['skip-question']) == cnt()
# s21: "After the rewrite, the skill still loaded in every trial that should load it."
assert all(A[m][n]['skills'].get(OURS, 0) == 2 and core(A[m][n]) == cnt() for m in MODELS for n in LOAD)
# s21: before, our skill loaded for no near-miss; after, for exactly that one trial.
assert sum(A[m][n]['skills'].get(OURS, 0) for m in MODELS for n in SKIP) == 1

# ---- The earlier run (s17b): saved evidence only ----------------------------------------------------
EARLY = report('src/earlier/eval-results.md')
assert EARLY[H]['load-no-keyword'] == (OURS, '1/2'), EARLY[H]['load-no-keyword']
assert all(EARLY[H][n] == (f'{OURS} (2×)', '2/2') for n in ('load-plain', 'load-indirect'))
EARLY_CON = (D / 'src/earlier/console.txt').read_text()
EARLY_LINES = [l for l in EARLY_CON.splitlines() if l.startswith('  ✘ loading · load-no-keyword [claude-haiku-4.5]')
               or 'The following required skills were not called: changelog-entry · trial 1' in l]
assert len(EARLY_LINES) == 2, EARLY_LINES

# ---- Chapter: The description decides ---------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Does the skill load?', f'''<div class="results">
      {card('given', 'What the agent is given', code(OLD_DESC, 'yaml'))}
      {card('rules', 'What it reads only if it opens the skill', code(chr(10).join(RULES), 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "rules", "at": "0~rule", "color": "blue"},
    {"type": "focus", "target": "given", "at": "2~one-line", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}'
        '.results{display:flex;flex-direction:column;gap:34px;width:100%}'
        '.results .card > .code.dark{font-size:36px;padding:26px 36px}.results .card .who{font-size:34px}')

framed('s02', 'The description decides', 'The agent starts with two lines', f'''<div class="annotated">
    {panel('skill')}
    {callouts(('given', 'all the agent has at the start'), ('rest', 'read only if the skill loads'))}
  </div>''', [
    {"type": "focus", "target": "given", "at": "1~name and description", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "rest", "at": "3~rest of the file", "color": "yellow"},
    {"type": "focus", "target": "given", "at": "5", "color": "blue"}], layout='layout-file')

TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'
framed('s03', 'The description decides', 'Two new ways to fail', f'''<div class="cols wide terms">
    {block("noload", "attention", "It doesn’t load when it should", "the agent works from habit, without the rules")}
    {block("overload", "change", "It loads when it shouldn’t", "changelog rules, on a task that isn’t a changelog entry")}
  </div>''', [
    {"type": "focus", "target": "noload", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "overload", "at": "3", "color": "orange"}], css=TERMS)

framed('s04', 'The description decides', 'Skills often go unused', f'''<div class="cols wide terms">
    {block("meant", "structure", "A skill, in the cases it was meant for", "one vendor’s report")}
    {block("unused", "attention", "56%", "of those cases: the skill went unused", words=False)}
  </div>
  <p class="note">Source: Vercel, 2026 · the vendor’s own figure · run counts not published</p>''', [
    {"type": "focus", "target": "meant", "at": "1", "color": "blue"},
    {"type": "focus", "target": "unused", "at": "1~fifty-six", "color": "yellow"}],
    css=TERMS + '.terms [data-concept="unused"] .title{font-size:110px;line-height:1.1}')

OBVIOUS, NEAR = PROMPT['load-plain'], PROMPT['skip-release-notes']
assert OBVIOUS.endswith('Update the changelog.') and NEAR.endswith('Draft the release notes from the changelog.')
quote = lambda cid, who, text: (f'<div class="quote" data-concept="{cid}" data-rep="quote"><span class="who">{who}</span>'
                                f'<p>“{esc(text).replace("`", "")}”</p></div>')
framed('s05', 'The description decides', 'Near the edge', f'''<div class="cols">
    {quote('obvious', 'An obvious request', OBVIOUS)}
    {quote('nearmiss', 'A near-miss request', NEAR)}
  </div>
  <p class="lead"><span data-concept="def" data-rep="note">A near-miss request shares words or a subject with the skill’s job, but is not its job.</span></p>''', [
    {"type": "focus", "target": "obvious", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "def", "at": "3~near-miss", "color": "yellow"},
    {"type": "focus", "target": "nearmiss", "at": "4", "color": "yellow"}],
    css='.quote{min-height:230px}.quote p{margin:0}.lead{font-size:40px}.stage{gap:44px}')

framed('s06', 'The description decides', 'Two groups of requests', f'''<div class="cols wide terms">
    {block("should", "structure", "Requests that should load the skill", "including ones that never use its obvious word")}
    {block("near", "attention", "Near-miss requests", "which should not load it")}
  </div>
  <p class="lead"><span data-concept="observed" data-rep="note">Loading is observed in real trials, not asked of the model.</span></p>''', [
    {"type": "focus", "target": "should", "at": "1", "color": "blue"},
    {"type": "focus", "target": "near", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "observed", "at": "3~observe", "color": "blue"}],
    css=TERMS + '.lead{font-size:40px}')

framed('s07', 'The description decides', 'A description says three things', f'''<div class="cols terms">
    {block("does", "structure", "What the skill does", "")}
    {block("when", "structure", "When to use it", "as a situation, not a word to look for")}
    {block("notfor", "structure", "What it is not for", "")}
  </div>''', [
    {"type": "focus", "target": "does", "at": "1", "color": "blue"},
    {"type": "focus", "target": "when", "at": "2", "color": "blue"},
    {"type": "focus", "target": "notfor", "at": "3", "color": "blue"}],
    css='.terms .semantic-block{min-height:300px;justify-content:center}.terms .label{font-size:34px}')

num = lambda cid, t: cell(cid, t, 'num')
framed('s08', 'The description decides', 'How big a test?', f'''<table class="data-table full size">
    <thead><tr><th></th><th class="num">Requests</th><th class="num">Trials of each</th><th class="num">Requests held back</th></tr></thead>
    <tbody>
      <tr><td>For a skill you depend on</td>{num('g-req', 'about 20')}{num('g-trials', '3')}{num('g-held', 'some')}</tr>
      <tr><td>Our test</td>{num('o-req', '6')}{num('o-trials', '2')}{num('o-held', 'none')}</tr>
    </tbody>
    <caption>Source: agentskills.io, “Optimizing skill descriptions” · conventions, with no published calculation behind them</caption>
  </table>''', [
    {"type": "focus", "target": "g-req", "at": "1~twenty", "color": "blue"},
    {"type": "focus", "target": "g-trials", "at": "1~three", "color": "blue"},
    {"type": "focus", "target": "g-held", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "o-req", "at": "4~six", "color": "blue"},
    {"type": "focus", "target": "o-trials", "at": "4~two trials", "color": "blue"}],
    css='.size{font-size:48px}.size th{font-size:32px}.size td{padding-top:40px;padding-bottom:40px}'
        '.size td:first-child{font-size:40px}')

# ---- Chapter: How a trial records loading ------------------------------------------------------------
framed('s09', 'How a trial records loading', 'Loading leaves an event', f'''<div class="annotated">
    {panel('event')}
    {callouts(('type', 'one each time a skill loads'), ('name', 'which skill'), ('turn', 'which turn, counting from 0'))}
  </div>''', [
    {"type": "scroll", "target": "#event", "to": "106-117", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "type", "at": "2~skill activation", "color": "yellow"},
    {"type": "focus", "target": "name", "at": "3", "color": "blue"},
    {"type": "focus", "target": "turn", "at": "4", "color": "blue"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file')

rows10 = ''.join(
    f'<tr><td class="mono">{m}</td><td class="mono">typo-fix</td>{cell("sk", EARLIER[m]["typo-fix"][0], "mono")}'
    f'<td class="num">{EARLIER[m]["typo-fix"][1]}</td></tr>\n' for m in MODELS)
framed('s10', 'How a trial records loading', 'The report’s Skills column', f'''<table class="data-table full rep">
    <thead><tr><th>Model</th><th>Stimulus</th><th><span data-concept="skills-head" data-rep="head">Skills</span></th><th class="num">Pass Rate</th></tr></thead>
    <tbody>
{rows10}    </tbody>
    <caption>{mono("eval-results.md")} · three of its twelve columns · our five-trial run</caption>
  </table>''', [
    {"type": "focus", "target": "skills-head", "at": "1~Skills", "color": "blue"},
    {"type": "focus", "target": "sk", "at": "3~five times", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.rep{font-size:40px}.rep th{font-size:32px}.rep td{padding-top:36px;padding-bottom:36px}'
        '.rep td.mono{font-family:var(--font-code);font-size:36px}.rep caption{font-size:30px}')

LOADING_NOTES = callouts(('skills', 'three installed: a real choice'),
                         ('p1', 'never says “changelog”'), ('req', 'passes only if it loaded'),
                         ('p2', 'a near-miss request'), ('dis', 'passes only if it did not load'))
framed('s11', 'How a trial records loading', 'A grader for loading', f'''<div class="annotated">
    {panel('loading')}
    {LOADING_NOTES}
  </div>''', [
    {"type": "focus", "target": "skills", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#loading", "to": "25-30", "at": "4"},
    {"type": "focus", "target": "p1", "at": "4~never says", "color": "yellow"},
    {"type": "scroll", "target": "#loading", "to": "30-33", "at": "5"},
    {"type": "focus", "target": "req", "at": "5~required", "color": "green"}], layout='layout-file')

framed('s12', 'How a trial records loading', 'And for staying out', f'''<div class="annotated">
    {panel('loading')}
    {LOADING_NOTES}
  </div>''', [
    {"type": "scroll", "target": "#loading", "to": "30-33", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#loading", "to": "54-61", "at": "0+0.4"},
    {"type": "focus", "target": "p2", "at": "0~mentions", "color": "yellow"},
    {"type": "focus", "target": "dis", "at": "1~disallowed", "color": "red"},
    {"type": "focus", "target": "none", "at": "2"}], layout='layout-file')

PART = {'load-plain': '… Update the changelog.',
        'load-no-keyword': '… note that down where we track what\'s going into the next release?',
        'load-indirect': '… Make sure users will be able to see that it\'s fixed when we ship.',
        'skip-commit': 'Write a commit message for my change. …',
        'skip-release-notes': '… Draft the release notes from the changelog.',
        'skip-question': 'What changed in version 1.2.0? …'}
for n, part in PART.items():
    assert part.strip('… ') in PROMPT[n], (n, part)
rows13 = ''
for n, _, g in STIM:
    grp = 'load' if n in LOAD else 'skip'
    req = esc(PART[n]).replace("'", '’')
    req = f'<span data-concept="plain" data-rep="cell">{req}</span>' if n == 'load-plain' else req
    rows13 += (f'<tr>{cell(grp, n, "mono")}<td>{req}</td><td class="mono">{g}</td></tr>\n')
framed('s13', 'How a trial records loading', 'Six requests, two shapes', f'''<table class="data-table full six">
    <thead><tr><th>Stimulus</th><th>Its request, in part</th><th>Our skill is</th></tr></thead>
    <tbody>
{rows13}    </tbody>
  </table>''', [
    {"type": "focus", "target": "load", "at": "1", "color": "blue"},
    {"type": "focus", "target": "plain", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "skip", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.six{font-size:31px}.six th{font-size:28px}.six td{padding:13px 40px 13px 0}'
        '.six td.mono{font-family:var(--font-code);font-size:29px;white-space:nowrap}')

# ---- Chapter: Test loading, then fix it ---------------------------------------------------------------
def count(c):
    done = c['passed'] + c['failed']
    return f'{c["passed"]} of {done}' + (f' · {c["errors"]} error' if c['errors'] else '')


def compare(filled):
    head = ''.join(f'<th class="num"><span data-concept="{r}" data-rep="head">{SHORT[m]} {r}</span></th>'
                   for m in MODELS for r in ('before', 'after'))
    body = ''
    for n in NAMES:
        grp = 'loadname' if n in LOAD else 'skipname'
        cells = ''.join(num(f'{r[0]}-{KEY[m]}-{n}', count(run[m][n]) if filled else '')
                        for m in MODELS for r, run in (('before', B), ('after', A)))
        body += f'<tr>{cell(grp, n, "mono")}{cells}</tr>\n'
    return f'''<table class="data-table full cmp">
    <thead><tr><th>Stimulus</th>{head}</tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


CMP_CSS = ('.cmp{font-size:32px}.cmp th{font-size:28px}.cmp td{padding:13px 40px 13px 0;height:44px}'
           '.cmp{table-layout:fixed}.cmp th{padding-right:40px}.cmp th:first-child{width:24%}.cmp td.mono{font-family:var(--font-code);font-size:30px}.cmp td.num{font-size:27px;white-space:nowrap}'
           '.cmp th:last-child,.cmp td:last-child{padding-right:12px}')
framed('s14', 'Test loading, then fix it', 'Before and after', compare(False) + '''
  <p class="note">trials that passed, of the two for each stimulus on each model</p>''', [
    {"type": "focus", "target": "before", "at": "2~as it stands", "color": "blue"},
    {"type": "focus", "target": "after", "at": "3~again", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], css=CMP_CSS)


def skills_table(m):
    body = ''
    for n in NAMES:
        sk, rate = BEFORE_REPORT[m][n]
        cid = 'skipsk' if n in SKIP else 'loadsk'
        body += f'<tr><td class="mono">{n}</td>{cell(cid, sk, "mono")}<td class="num">{rate}</td></tr>\n'
    return f'''<div class="card">
      <div class="who">{mono(m)}</div>
      <table class="data-table full skl">
        <thead><tr><th>Stimulus</th><th>Skills</th><th class="num">Pass Rate</th></tr></thead>
        <tbody>
{body}        </tbody>
      </table>
    </div>'''


framed('s17', 'Test loading, then fix it', 'Which skills loaded', f'''<div class="cols wide">
    {skills_table(H)}
    {skills_table(T)}
  </div>
  <p class="note">{mono("eval-results.md")} · three of its twelve columns · the run with the one-line description</p>''', [
    {"type": "focus", "target": "skipsk", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "loadsk", "at": "3", "color": "green"}],
    css='.skl{font-size:28px}.skl th{font-size:28px;white-space:nowrap}.skl td{padding:11px 26px 11px 0}'
        '.skl td.mono{font-family:var(--font-code);font-size:28px;white-space:nowrap}.card .who{font-size:32px}'
        '.stage{gap:26px}.cols.wide{gap:36px}.skl td:last-child,.skl th:last-child{padding-right:0}')

rows17b = ''.join(
    f'<tr><td class="mono">{n}</td>{cell("miss" if n == "load-no-keyword" else "fine", EARLY[H][n][0], "mono")}'
    f'<td class="num">{EARLY[H][n][1]}</td></tr>\n' for n in LOAD)
head, ev = EARLY_LINES[0].strip(), EARLY_LINES[1].strip()
grader, why = ev.split('  ', 1)
why = why.strip().replace('were not called', '⟦called:were not called⟧')
framed('s17b', 'Test loading, then fix it', 'An earlier run found one', f'''<div class="card">
      <div class="who">An earlier run, same one-line description · {mono("eval-results.md")}, {mono(H)}</div>
      <table class="data-table full skl early">
        <thead><tr><th>Stimulus</th><th>Skills</th><th class="num">Pass Rate</th></tr></thead>
        <tbody>
{rows17b}        </tbody>
      </table>
    </div>
    {card('out', 'The same run’s console output', code(head + chr(10) + '    ' + grader + chr(10) + '      ' + why, 'text'))}''', [
    {"type": "focus", "target": "miss", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "called", "at": "2~not called", "color": "red"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.skl{font-size:32px}.skl th{font-size:28px;white-space:nowrap}.skl td{padding:12px 40px 12px 0}'
        '.skl td.mono{font-family:var(--font-code);font-size:30px;white-space:nowrap}.card .who{font-size:30px}'
        '.card > .code.dark{font-size:29px;padding:20px 28px;flex:none}.stage{gap:26px}.card{width:100%}')

framed('s18', 'Test loading, then fix it', 'One line becomes five', f'''{panel('newskill')}
  <p class="lead parts3"><span data-concept="does" data-rep="note">what it does</span> · <span data-concept="when" data-rep="note">when to use it</span> · <span data-concept="notfor" data-rep="note">what it’s not for</span></p>''', [
    {"type": "focus", "target": "does", "at": "2", "color": "blue"},
    {"type": "focus", "target": "when", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "notfor", "at": "4", "color": "orange"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file',
    css='.parts3{font-size:36px;margin:0}.stage{gap:22px}')

framed('s20', 'Test loading, then fix it', 'The two runs, side by side', compare(True) + f'''
  <p class="note">trials that passed, of those that finished · our runs {COUNTS["before"]["run"]} and {COUNTS["after"]["run"]}</p>''', [
    {"type": "focus", "target": "b-t-skip-question", "at": "1~two of two", "color": "green"},
    {"type": "focus", "target": "a-t-skip-question", "at": "1~one of two", "color": "red"},
    {"type": "focus", "target": "none", "at": "2"}], css=CMP_CSS + '.note{font-size:28px}')

# ---- Chapter: What the loading test showed -------------------------------------------------------------
framed('s21', 'What the loading test showed', 'One failure, after the rewrite', compare(True) + '''
  <p class="note">trials that passed, of those that finished</p>''', [
    {"type": "focus", "target": "before", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "loadname", "at": "3", "color": "green"},
    {"type": "focus", "target": "a-t-skip-question", "at": "4", "color": "red"}], css=CMP_CSS + '.note{font-size:28px}')

miss, fixed = B[T]['skip-question'], A[T]['skip-question']
framed('s22', 'What the loading test showed', 'The test is what we keep', f'''<div class="cols wide terms">
    {block("sample", "attention", f"{count(miss)}, then {count(fixed)}", "one stimulus on one model: a small sample")}
    {block("keep", "structure", "The loading test", "one command shows whether the boundary moved")}
  </div>''', [
    {"type": "focus", "target": "sample", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "keep", "at": "1", "color": "blue"}],
    css=TERMS + '.terms .semantic-block{justify-content:center}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Requests that should load it', 'catch a skill that stays unused'),
    ('Near-miss requests', 'catch a skill that loads where it doesn’t belong')], 1))
framed('s23', 'Recap', 'Why near-miss requests?', f'''<div class="semantic-block" id="test" data-role="structure">
    <div class="title words">a loading test</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#test", "at": "1"},
    {"type": "focus", "target": "p1", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "3", "color": "yellow"}], layout='layout-expand',
    css='#test{width:100%;padding:36px 40px 44px;gap:24px}'
        '#test .parts{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;width:100%}'
        '#test .part{min-height:280px}#test .part .title{font-size:46px;line-height:1.2}'
        '#test .part .label{font-size:34px}')

scene('s24', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Better with the skill?</h1>
  <p class="lead">Is the result any better with the skill than with no skill at all?</p>
  <p class="note">Exercises are on the lesson page · Source: agentskills.io, “Optimizing skill descriptions”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok')
