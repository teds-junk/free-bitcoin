"""Generate lesson 6's scene pages, file panels included.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/            the practice files as lesson 6 leaves them (verified/lesson-06/practice)
  src/*.yaml, *.mjs, *.CHANGELOG.md   files the lesson does not change
  src/run/              this video's own runs (s14, s16, s19) and the lesson 5 video's after run; see its README
  src/earlier-run/      evidence from an earlier run of the same stimuli, shown and narrated as "an earlier
                        run", never as ours; see its README

The asserts state what the narration says about the runs. If a recording changes a result, an assert
fails here: reword the outcome sentences in storyboard.json, then change the assert.

Run from anywhere:  python3 build-src/make-scenes.py
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
HAIKU, TERRA = MODELS


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


PANELS = []


def file_panel(sid, pid, file, label, show, marks, expect, width=None, rows=9):
    """Queued; run after the scene pages are written."""
    cmd = ['node', str(SKILL / 'scripts/file-panel.js'), '--file', f'src/{file}', '--label', label, '--id', pid,
           '--rows', str(rows), '--show', show, '--into', f'scenes/{sid}.html']
    if width:
        cmd += ['--width', str(width)]
    for m in marks:
        cmd += ['--mark', m]
    for e in expect:
        cmd += ['--expect', e]
    PANELS.append(cmd)


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


def src(path):
    return (D / 'src' / path).read_text()


def line_no(path, text):
    """1-based number of the one line of src/<path> that equals text."""
    hits = [i for i, l in enumerate(src(path).splitlines(), 1) if l == text]
    assert len(hits) == 1, f'{path}: {text!r} found {len(hits)} times'
    return hits[0]


# ---- The real things, read from src/ -----------------------------------------------------------
EVAL = 'state/changelog.eval.yaml'
ev = src(EVAL).splitlines()
L_TWO, L_AFTER = line_no(EVAL, '  - name: two-changes'), line_no(EVAL, '  - name: after-release')
assert (L_TWO, L_AFTER) == (57, 81)
assert ev[66] == '    grading_environment:' and ev[71] == '      - type: program' and ev[77:79] == [
    '            - Added=60', '            - Fixed=60'] and ev[100] == '            - Added=58'


def prompt_of(start):
    """The prompt of the stimulus whose name line is `start` (1-based), as one paragraph."""
    assert ev[start] == '    prompt: |'
    out, i = [], start + 1
    while ev[i].startswith('      '):
        out.append(ev[i].strip())
        i += 1
    return ' '.join(out)


PROMPT_TWO, PROMPT_AFTER = prompt_of(L_TWO), prompt_of(L_AFTER)
assert 'PR 60' in PROMPT_TWO and 'PR 58' in PROMPT_AFTER
assert '## [Unreleased]' not in src('just-released.CHANGELOG.md') and '## [Unreleased]' in src('notes-cli.CHANGELOG.md')

script_lines = src('check-entry.mjs').splitlines()
assert len(script_lines) == 45 and script_lines[35] == 'function report(passed, evidence) {'
assert script_lines[14] == 'const end = rest.search(/^## /m);'

skill = src('state/SKILL.md').splitlines()
assert len(skill) == 23 and skill[20].startswith('- If the changelog has no Unreleased section')
assert src('state/SKILL.before.md').splitlines() == skill[:20]
assert src('state/changelog.eval.before.yaml').splitlines() == ev[:55]

RUN = {r: src(f'run/{r}/RUN').strip() for r in ('first', 'after')}
STIMULI = ('typo-fix', 'refactor', 'security', 'two-changes', 'after-release')


def trials(path):
    out = [json.loads(l) for l in src(path).splitlines() if l.strip()]
    out = [t for t in out if t.get('type') == 'trial-result']
    assert all(t['status'] == 'success' for t in out), f'{path}: a trial did not finish'
    return out


def grades(path):
    """{(model, stimulus): [passed, ...]}, one entry per trial."""
    g = {}
    for t in trials(path):
        g.setdefault((t['model'], t['gradeResult']['stimulusName']), []).append(t['gradeResult']['passed'])
    return g


def evidence(path, model, stimulus):
    return [d['evidence'] for t in trials(path) if (t['model'], t['gradeResult']['stimulusName']) == (model, stimulus)
            for d in t['gradeResult']['details']]


def added(path):
    """The lines a patch added, verbatim, without blank ones."""
    return [l[1:] for l in src(path).splitlines() if l.startswith('+') and not l.startswith('+++') and l[1:].strip()]


def removed(path):
    return [l[1:] for l in src(path).splitlines() if l.startswith('-') and not l.startswith('---')]


# What the narration says about OUR runs. If a re-recording changes these, the sentences change too.
G1, G2 = grades('run/first/results.jsonl'), grades('run/after/results.jsonl')
assert all(len(v) == 1 for v in list(G1.values()) + list(G2.values())) and len(G1) == len(G2) == 10
passed_n = lambda g, m: sum(g[(m, s)][0] for s in STIMULI)
assert (passed_n(G1, HAIKU), passed_n(G1, TERRA)) == (5, 4)                                # s16
assert G1[(TERRA, 'after-release')] == [False]                                             # s16
assert evidence('run/first/results.jsonl', TERRA, 'after-release') == ["no '## [Unreleased]' heading"]
assert (passed_n(G2, HAIKU), passed_n(G2, TERRA)) == (5, 5)                                # s19
assert src('run/kept-files.txt').split() == ['kept/main/typo-fix/CHANGELOG.md',
                                             'kept/main/typo-fix/changelog-entry/SKILL.md']  # s14
FIRST_AR = {m: added(f'run/first/after-release.{m}.patch') for m in MODELS}                # s17, s20
assert '## Unreleased' in FIRST_AR[TERRA] and '## [Unreleased]' not in FIRST_AR[TERRA]
assert '## [Unreleased]' in FIRST_AR[HAIKU] and '## Unreleased' not in FIRST_AR[HAIKU]
assert all('## [Unreleased]' in added(f'run/after/after-release.{m}.patch') for m in MODELS)   # s20
for r, g in (('first', G1), ('after', G2)):                                                # s21: all four right
    for m in MODELS:
        tc = f'run/{r}/two-changes.{m}.patch'
        assert g[(m, 'two-changes')] == [True] and not removed(tc), tc
        assert sum('(#60)' in l for l in added(tc)) == 2 and '### Fixed' in added(tc), tc
# s23: with the security rule in the skill, haiku and the security stimulus, in our runs
L5 = grades('run/lesson5-after.results.jsonl')[(HAIKU, 'security')]
OURS = L5 + G1[(HAIKU, 'security')] + G2[(HAIKU, 'security')]
assert len(L5) == 3 and len(OURS) == 5 and all(OURS)
assert all('### Security' in added(f'run/{r}/security.{HAIKU}.patch') for r in ('first', 'after'))
UNDER_FIXED_OURS = sum(not ok for ok in OURS)

# What the narration says about the EARLIER run (src/earlier-run): reported as such, never as ours.
EXCERPT = src('earlier-run/two-changes.excerpt.patch').rstrip('\n').splitlines()
assert EXCERPT[4] == '-## [1.2.0] - 2026-09-14' and EXCERPT[5] == '+### Fixed' and '…' in EXCERPT[6] and len(EXCERPT) == 10
earlier_console = src('earlier-run/lesson5-after-console.txt')
assert re.search(r'claude-haiku-4\.5\n\s+FLAKY\s+security\s+2 passed · 1 failed', earlier_console)
assert 'Running with 3 trial(s)' in earlier_console and 'under-security  2 passed · 1 failed' in earlier_console
EARLIER_UNDER_FIXED, EARLIER_TRIALS = 1, 3

# ---- Hook ----------------------------------------------------------------------------------------
golden_fixed = '- Fix `notes list` repeating the final note from the prior page (#60)'
hook = '\n'.join(['⟦unrel:## [Unreleased]⟧', '', '### Added', '- Add `notes list --tag` to filter by tag (#41)', '',
                  '⟦fixed:### Fixed⟧', golden_fixed.replace('(#60)', '⟦pr:(#60)⟧'), '',
                  '⟦rel:## [1.2.0] - 2026-09-14⟧'])
framed('s01', 'Vally &amp; Agent Evals', 'Keep graders out of reach', f'''<div class="results">
      {card('answer', f'{mono("CHANGELOG.md")} · a correct answer to one of our requests', code(hook, 'text'))}
  </div>''', [
    {"type": "focus", "target": "pr", "at": "0~citing", "color": "yellow"},
    {"type": "focus", "target": "fixed", "at": "1~under Fixed", "color": "blue"},
    {"type": "focus", "target": "unrel", "at": "1~inside Unreleased", "color": "blue"},
    {"type": "focus", "target": "rel", "at": "1~version", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.results{width:100%}'
        '.results .card > .code.dark{font-size:36px;line-height:1.4;padding:26px 36px}.results .card .who{font-size:32px}')

# ---- Chapter: Why hide the grader ----------------------------------------------------------------
TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'
framed('s02', 'Why hide the grader', 'A grader in plain sight', f'''<div class="cols terms">
    {block("read", "structure", "Read it", "and learn exactly what is being looked for", words=True)}
    {block("edit", "failure", "Edit it", "so that it always passes", words=True)}
    {block("fix", "attention", "“Fix” it", "distracted by a file it did not expect", words=True)}
  </div>
  <p class="note">what an agent could do with a grading script left in its workspace</p>''', [
    {"type": "focus", "target": "read", "at": "2~read it", "color": "blue"},
    {"type": "focus", "target": "edit", "at": "3", "color": "red"},
    {"type": "focus", "target": "fix", "at": "4~distracted", "color": "yellow"}], css=TERMS)

framed('s03', 'Why hide the grader', 'Agents do find the answers', f'''<div class="cols wide terms">
    {block("berkeley", "attention", "73% to 100%", "scored on eight benchmarks by agents that solved none of the tasks", words=True)}
    {block("cursor", "attention", "63%", "of one model’s passing runs copied the published fix", words=True)}
  </div>
  <p class="note">Sources: Berkeley RDI, April 2026 · Cursor, June 2026 (the vendor’s own report, one model, one benchmark)</p>''', [
    {"type": "focus", "target": "berkeley", "at": "2~seventy-three", "color": "yellow"},
    {"type": "focus", "target": "cursor", "at": "5~sixty-three", "color": "yellow"}],
    css=TERMS + '.terms .title{font-size:84px;line-height:1.15}')

framed('s04', 'Why hide the grader', 'Two plain rules', f'''<div class="cols wide terms">
    {block("sight", "structure", "Out of sight", "grading scripts and expected answers stay where the agent cannot see them", words=True, step=1)}
    {block("reach", "structure", "Out of reach", "no grader depends on a file the agent could have altered", words=True, step=2)}
  </div>''', [
    {"type": "focus", "target": "sight", "at": "2", "color": "blue"},
    {"type": "focus", "target": "reach", "at": "3", "color": "blue"}], css=TERMS)

# ---- Chapter: What the agent is given ------------------------------------------------------------
framed('s05', 'What the agent is given', 'Copied before the agent starts', f'''<div class="annotated">
    {panel('env')}
    {callouts(('skill', 'copied as a whole folder'), ('dest', 'arrives under this name'))}
  </div>''', [
    {"type": "focus", "target": "env", "at": "1~agent environment", "color": "blue"},
    {"type": "focus", "target": "skill", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "dest", "at": "4", "color": "yellow"}], layout='layout-file')
file_panel('s05', 'env', 'one-request.eval.yaml', 'one-request.eval.yaml', '6-11',
           ['6=env', '8=skill', '11=dest'], ['8=changelog-entry', '11=dest: CHANGELOG.md'], width=44)

kept = '\n'.join(['vally eval … ⟦flag:--workspace kept⟧', '', '⟦kept:kept/⟧', '  ⟦main:main/⟧', '    ⟦stim:typo-fix/⟧'])
framed('s06', 'What the agent is given', 'A workspace we can keep', f'''<div class="annotated">
    {code(kept, 'text', 'tree')}
    {callouts(('flag', 'keep each trial’s workspace'), ('kept', 'the folder we named'), ('main', 'a folder Vally adds'),
              ('stim', 'one per stimulus: no model name'))}
  </div>
  <p class="note">with several models, Vally stops first: <span class="mono" data-concept="collide" data-rep="note">workspace-collision</span></p>''', [
    {"type": "focus", "target": "flag", "at": "1~workspace", "color": "blue"},
    {"type": "focus", "target": "kept", "at": "2~folder we name", "color": "blue"},
    {"type": "focus", "target": "main", "at": "2~main", "color": "blue"},
    {"type": "focus", "target": "stim", "at": "2~each stimulus", "color": "blue"},
    {"type": "focus", "target": "flag", "at": "3", "color": "blue"},
    {"type": "focus", "target": "stim", "at": "4~no model name", "color": "yellow"},
    {"type": "focus", "target": "collide", "at": "4~collision", "color": "red"}],
    css='.code.dark.tree{min-width:900px;font-size:40px;line-height:1.6}.callout{font-size:34px}.stage{gap:34px}')

tree = '\n'.join(['skills/', '  ⟦skill:changelog-entry/⟧', '    SKILL.md', '⟦evals:evals/⟧', '  changelog.eval.yaml', '  fixtures/'])
framed('s07', 'What the agent is given', 'Evals live beside the skill', f'''<div class="annotated">
    {code(tree, 'text', 'tree')}
    {callouts(('skill', 'copied whole into the workspace'), ('evals', 'never copied whole'))}
  </div>''', [
    {"type": "focus", "target": "skill", "at": "0~inside", "color": "yellow"},
    {"type": "focus", "target": "evals", "at": "1", "color": "blue"}],
    css='.code.dark.tree{min-width:900px;font-size:40px;line-height:1.6}.callout{font-size:34px}')

# ---- Chapter: Files only graders get -------------------------------------------------------------
WS = 'CHANGELOG.md\nchangelog-entry/\n  SKILL.md'
GC = WS + '\n⟦added:.vally-grading/⟧\n  ⟦added:check-entry.mjs⟧'
TWO_CSS = ('.two .card > .code.dark{font-size:38px;line-height:1.6;padding:30px 36px;min-height:330px}'
           '.two .card .who{font-size:32px}')


def two_boxes():
    return f'''<div class="cols wide two">
    {card('ws', 'Workspace · the agent works here', code(WS, 'text'))}
    {card('gc', 'Grading copy · only graders run here', code(GC, 'text'))}
  </div>'''


framed('s08', 'Files only graders get', 'Added after the agent stops', two_boxes() + '''
  <p class="note">the grading copy is made when the agent stops, and thrown away when grading ends</p>''', [
    {"type": "focus", "target": "gc", "at": "2~copy", "color": "blue"},
    {"type": "focus", "target": "added", "at": "4~script", "color": "yellow"}], css=TWO_CSS)

framed('s09', 'Files only graders get', 'A grader that runs a script', f'''<div class="annotated">
    {panel('stim')}
    {callouts(('genv', 'files for graders only'), ('src', 'where we keep the script'), ('dest', 'where it goes in the grading copy'),
              ('ptype', 'run a program, take its verdict'), ('args', 'the script, then what to look for'))}
  </div>''', [
    {"type": "focus", "target": "genv", "at": "1", "color": "blue"},
    {"type": "focus", "target": "src", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "dest", "at": "3", "color": "yellow"},
    {"type": "scroll", "target": "#stim", "to": "71-79", "at": "4"},
    {"type": "focus", "target": "ptype", "at": "4~program", "color": "blue"},
    {"type": "focus", "target": "node", "at": "6~node", "color": "blue"},
    {"type": "focus", "target": "args", "at": "6~arguments", "color": "yellow"}], layout='layout-file')
file_panel('s09', 'stim', EVAL, 'changelog.eval.yaml', '57,67-79',
           ['67=genv', '69=src', '70=dest', '72=ptype', '75=node', '76=args', '77-79=args2'],
           ['57=two-changes', '72=type: program'], width=46)

framed('s10', 'Files only graders get', 'One line of JSON', panel('script'), [
    {"type": "focus", "target": "comment", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#script", "to": "36-44", "at": "3"},
    {"type": "focus", "target": "print", "at": "4", "color": "blue"},
    {"type": "focus", "target": "namekind", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "verdict", "at": "6", "color": "yellow"},
    {"type": "focus", "target": "evidence", "at": "7", "color": "yellow"},
    {"type": "focus", "target": "exit", "at": "8", "color": "blue"}], layout='layout-file')
file_panel('s10', 'script', 'check-entry.mjs', 'check-entry.mjs', '1-4,36-45',
           ['1-4=comment', '37=print', '38-39=namekind', '40-41=verdict', '42=evidence', '44=exit'],
           ['37=console.log(JSON.stringify', '44=process.exit(0)'])


def stim_card(cid, who, prompt, args, argid):
    a = '\n'.join(f'⟦{argid}:{x}⟧' for x in args)
    return f'''<div class="card" data-concept="{cid}" data-rep="card">
        <div class="who">{who}</div>
        <div class="quote"><span class="who">The request</span><p>“{re.sub(r'(--[a-z-]+)', lambda m: '<span class="nb">' + m.group(1) + '</span>', prompt.replace('`', ''))}”</p></div>
        {code(a, 'text')}
      </div>'''


framed('s11', 'Files only graders get', 'Two stimuli for the script', f'''<div class="cols two">
    {stim_card('c-two', mono('two-changes'), PROMPT_TWO, ['Added=60', 'Fixed=60'], 'a60')}
    {stim_card('c-after', f'{mono("after-release")} · starts with no Unreleased section', PROMPT_AFTER, ['Added=58'], 'a58')}
  </div>''', [
    {"type": "focus", "target": "c-two", "at": "1", "color": "blue"},
    {"type": "focus", "target": "a60", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "c-after", "at": "4", "color": "blue"},
    {"type": "focus", "target": "a58", "at": "5", "color": "yellow"}],
    css='.two .quote{font-size:30px;padding:20px 28px 24px;flex:1}.two .quote p{margin:0}.nb{white-space:nowrap}.two .card .who{font-size:30px}'
        '.two .card > .code.dark{flex:none;font-size:36px;padding:20px 32px}')

errs = '⟦vis:grading-file-src-agent-visible⟧\n\n⟦schema:Grader output did not match schema⟧'
framed('s12', 'Files only graders get', 'Two mistakes Vally catches', f'''<div class="annotated">
    {code(errs, 'text', 'tree')}
    {callouts(('vis', 'lint: the agent could see the script'), ('schema', 'the script’s result lacks a field'))}
  </div>''', [
    {"type": "focus", "target": "vis", "at": "1", "color": "red"},
    {"type": "focus", "target": "schema", "at": "2", "color": "red"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.code.dark.tree{min-width:900px;font-size:38px;line-height:1.6}.callout{font-size:34px}')

framed('s12b', 'Files only graders get', 'Evidence that says why', f'''<div class="cols wide two">
    {card('rc', f'{mono("run-command")} · passes when the script exits with 0', code('Expected exit code 0, got 1', 'text'))}
    {card('pg', f'{mono("program")} · the script prints its verdict', code('no entry citing #60 under Fixed', 'text'))}
  </div>
  <p class="note">the evidence each grader leaves when a trial fails</p>''', [
    {"type": "focus", "target": "rc", "at": "0~run command", "color": "blue"},
    {"type": "focus", "target": "pg", "at": "2", "color": "green"}],
    css='.two .card > .code.dark{font-size:36px;padding:44px 36px}.two .card .who{font-size:30px}')

# ---- Chapter: A script the agent never sees ------------------------------------------------------
framed('s13', 'A script the agent never sees', 'Look inside, then hide a script', f'''<div class="cols terms">
    {block("p1", "structure", "Keep one workspace", "and list its files", words=True, step=1)}
    {block("p2", "transform", "Add the two stimuli", "and run all five on both models", words=True, step=2)}
    {block("p3", "change", "Add a rule to the skill", "and run again", words=True, step=3)}
  </div>''', [
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "p3", "at": "3", "color": "orange"},
    {"type": "focus", "target": "p1", "at": "4", "color": "blue"}],
    css=TERMS + '.terms .title{font-size:40px}')

framed('s15', 'A script the agent never sees', 'Five stimuli now', panel('five'), [
    {"type": "focus", "target": "old", "at": "1~three", "color": "blue"},
    {"type": "scroll", "target": "#five", "to": "57-81", "at": "1~two graded"},
    {"type": "focus", "target": "new", "at": "1~script", "color": "yellow"}], layout='layout-file')
file_panel('s15', 'five', EVAL, 'changelog.eval.yaml', '11,29,42,57,81',
           ['11=old', '29=old', '42=old', '57=new', '81=new'], ['81=after-release'])

framed('s18', 'A script the agent never sees', 'One more rule', panel('skill'), [
    {"type": "focus", "target": "rule", "at": "1", "color": "yellow"}], layout='layout-file')
file_panel('s18', 'skill', 'state/SKILL.md', 'changelog-entry/SKILL.md', '16-23', ['21-23=rule'],
           ['21=no Unreleased section', '23=## [Unreleased]'])

# ---- Chapter: What the script caught -------------------------------------------------------------
def added_box(lines, cid, target):
    return code('\n'.join(f'⟦{cid}:{l}⟧' if l == target else l for l in lines), 'text')


framed('s20', 'What the script caught', 'Terra dropped the brackets', f"""<div class="results">
      {card('ar-h', f'{mono(HAIKU)} · the lines its {mono("after-release")} trial added', added_box(FIRST_AR[HAIKU], 'good', '## [Unreleased]'))}
      {card('ar-t', f'{mono(TERRA)} · the lines its {mono("after-release")} trial added', added_box(FIRST_AR[TERRA], 'head', '## Unreleased'))}
  </div>
  <p class="note">first run · one trial for each model · {RUN['first']}</p>""", [
    {"type": "focus", "target": "head", "at": "1~without brackets", "color": "red"},
    {"type": "focus", "target": "good", "at": "1~with them", "color": "green"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.results{display:flex;flex-direction:column;gap:20px;width:100%}'
        '.results .card{gap:10px}.results .card > .code.dark{font-size:30px;line-height:1.4;padding:16px 28px}'
        '.results .card .who{font-size:30px}.stage{justify-content:flex-start;gap:18px}')

ex = list(EXCERPT)
ex[4] = f'⟦del:{ex[4]}⟧'
ex[5], ex[6] = f'⟦fixed:{ex[5]}⟧', f'⟦fixed:{ex[6]}⟧'
ex[8], ex[9] = f'⟦below:{ex[8]}⟧', f'⟦below:{ex[9]}⟧'
framed('s21', 'What the script caught', 'A wrong answer, passed', f"""<div class="annotated">
    {card('earlier', f'an earlier run · {mono("two-changes")} · part of the patch the script passed', code(chr(10).join(ex), 'diff'))}
    {callouts(('del', 'a released version’s heading, deleted'), ('fixed', 'the Fixed entry, in its place'))}
  </div>
  <p class="note">an excerpt: the patch’s first five lines are left out, and … marks words left out of one line</p>""", [
    {"type": "focus", "target": "fixed", "at": "3~Fixed entry", "color": "yellow"},
    {"type": "focus", "target": "del", "at": "3~deleted", "color": "red"},
    {"type": "focus", "target": "below", "at": "4~entries", "color": "yellow"}],
    css='.card > .code.dark{font-size:32px;line-height:1.45;padding:22px 30px}.card .who{font-size:30px}'
        '.callout{font-size:32px}.stage{gap:22px}')

framed('s22', 'What the script caught', 'The tick says stop looking', f"""<div class="annotated">
    {panel('script2')}
    {callouts(('findhead', 'find the Unreleased heading'), ('nexthead', 'take everything down to the next one'))}
  </div>""", [
    {"type": "scroll", "target": "#script2", "to": "10-16", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "findhead", "at": "1~Unreleased heading", "color": "blue"},
    {"type": "focus", "target": "nexthead", "at": "1~next version", "color": "yellow"},
    {"type": "focus", "target": "nexthead", "at": "2", "color": "red"},
    {"type": "focus", "target": "none", "at": "3"}], layout='layout-file')
file_panel('s22', 'script2', 'check-entry.mjs', 'check-entry.mjs', '10-16', ['10-11=findhead', '14-16=nexthead'],
           ['10=## [Unreleased]', '15=rest.search(/^## /m)'], width=48)

framed('s23', 'What the script caught', 'A glimpse, not a measurement', f"""<div class="cols wide terms">
    {block("before", "attention", f"{EARLIER_UNDER_FIXED} of {EARLIER_TRIALS}", "filed under Fixed · an earlier run")}
    {block("now", "success", f"{UNDER_FIXED_OURS} of {len(OURS)}", "filed under Fixed · our runs")}
  </div>
  <p class="note">{mono(HAIKU)} · the security stimulus · the security rule already in the skill</p>""", [
    {"type": "focus", "target": "before", "at": "1~one of three", "color": "yellow"},
    {"type": "focus", "target": "now", "at": "2~five trials", "color": "green"},
    {"type": "focus", "target": "none", "at": "3"}],
    css=TERMS + '.terms .title{font-size:110px;line-height:1.1}.terms .semantic-block{justify-content:center}')

framed('s24', 'Recap', 'What does each one add?', two_boxes(), [
    {"type": "focus", "target": "ws", "at": "1", "color": "blue"},
    {"type": "focus", "target": "gc", "at": "2", "color": "yellow"}], css=TWO_CSS)

scene('s25', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Test a grader</h1>
  <p class="lead">without running an agent</p>
  <p class="lead">How do you test a grader?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Writing Eval Specs”, Grader-only files</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')

for cmd in PANELS:
    r = subprocess.run(cmd, cwd=D, capture_output=True, text=True)
    assert r.returncode == 0, ' '.join(cmd) + '\n' + r.stderr + r.stdout
    info = json.loads(r.stdout)
    print(cmd[cmd.index('--into') + 1], 'rows', len(info.get('rows', [])) if isinstance(info.get('rows'), list) else info.get('rows'),
          'position', info.get('position'), 'wrapped', info.get('wrapped'))
print('ok')
