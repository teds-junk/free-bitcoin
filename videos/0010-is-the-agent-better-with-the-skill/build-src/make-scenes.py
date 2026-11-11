"""Generate lesson 10's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout), tables for
numbers. Nothing here sets a colour or a font outside the theme's variables; a scene's own CSS is
sizes and spacing.

Everything quoted on screen is read from src/:
  src/with-and-without.experiment.yaml   the experiment file (verified/lesson-10/practice)
  src/first-draft-SKILL.md               practice-starter's skill, for the rule that caused the number
  src/first-draft-terra.patch            gpt-5.6-terra's typo-fix patch from the lesson 1 video's run
  src/first-draft-run/                   gpt-5.6-terra's five patches from the lesson 3 video's run
  src/run/                               the run this video's s14 recorded (name in src/run/RUN):
                                         s13.log, s14.log (Vally's output), and the no-skill patches.
                                         While src/run/PROVISIONAL exists these are stand-ins from
                                         verified/lesson-10 and the patch checks that need files
                                         verified/ does not keep are skipped.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
VARIANTS = ('haiku-no-skill', 'haiku-with-skill', 'terra-no-skill', 'terra-with-skill')
STIMULI = ('typo-fix', 'refactor', 'security', 'two-changes', 'after-release')
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()


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


def cell(cid, text, rep='cell'):
    return f'<span data-concept="{cid}" data-rep="{rep}">{text}</span>'


# ---- The real things, read from src/ -----------------------------------------------------------
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')
log = lambda name: ANSI.sub('', (D / 'src/run' / name).read_text()).replace('\r', '')
RUN = (D / 'src/run/RUN').read_text().strip()
assert re.fullmatch(r'2026-[\dT-]+Z', RUN), RUN

# The dry run: four plans, one block per variant, in the file's order.
dry = log('s13.log')
assert re.search(r'^Plans:\s+4$', dry, re.M) and re.search(r'^Baseline:\s+haiku-no-skill$', dry, re.M)
assert tuple(re.findall(r'^── (\S+)', dry, re.M)) == VARIANTS

# The run: the failure blocks above the table, and the table.
out = log('s14.log').splitlines()
FAILS = []          # (variant, stimulus, [graders that failed]) in the order printed
for i, l in enumerate(out):
    m = re.match(r'^\s+(FAIL|FLAKY|ERROR)\s+(\S+) · ', l)
    if m:
        v = re.match(r'^(\S+) · (\S+)$', out[i - 1])
        assert v and m.group(1) == 'FAIL', (out[i - 1], l)       # an ERROR take is rerun, not shown
        graders = []
        for n in out[i + 1:]:
            g = re.match(r'^\s+✘ (\S+)\s', n)
            if not g:
                break
            graders.append(g.group(1))
        FAILS.append((v.group(1), m.group(2), graders))
hdr = max(i for i, l in enumerate(out) if re.match(r'^\s+eval\s{2,}', l))     # the final summary's table
cols = re.split(r'\s{2,}', out[hdr].strip())[1:]
assert tuple(c.replace(' (baseline)', '') for c in cols) == VARIANTS and cols[0].endswith('(baseline)'), cols
ROW = {}
for l in out[hdr + 1:hdr + 8]:
    parts = re.split(r'\s{2,}', l.strip())
    if parts[0] in ('stimuli', 'tokens', 'trial time'):
        assert len(parts) == 5, l
        ROW[parts[0]] = dict(zip(VARIANTS, parts[1:]))
assert set(ROW) == {'stimuli', 'tokens', 'trial time'}
PASSED = {v: {s: not any(f[0] == v and f[1] == s for f in FAILS) for s in STIMULI} for v in VARIANTS}
for v in VARIANTS:      # the grid of ticks and crosses must add up to the row Vally printed
    assert ROW['stimuli'][v] == f'{sum(PASSED[v].values())}/5', (v, ROW['stimuli'][v])
ktok = lambda v: float(re.fullmatch(r'([\d.]+)k', ROW['tokens'][v]).group(1))

# What the narration says about this run. If a re-recording changes these, the sentences change too.
assert [ROW['stimuli'][v] for v in VARIANTS] == ['2/5', '5/5', '3/5', '5/5'], ROW['stimuli']       # s15, s18
assert [(v, s, g) for v, s, g in FAILS] == [                                                       # s16
    ('haiku-no-skill', 'after-release', ['entry-in-new-unreleased']),
    ('haiku-no-skill', 'refactor', ['adds-nothing']), ('haiku-no-skill', 'security', ['under-security']),
    ('terra-no-skill', 'refactor', ['adds-nothing']), ('terra-no-skill', 'security', ['under-security'])], FAILS
assert [ROW['tokens'][v] for v in VARIANTS] == ['374.6k', '329.7k', '289.6k', '281.6k'], ROW['tokens']  # s21
assert ktok('haiku-with-skill') < ktok('haiku-no-skill') and ktok('terra-with-skill') < ktok('terra-no-skill')

PR = re.compile(r'\(#\d+\)\s*$')


def added(path):
    return [l[1:] for l in (D / 'src' / path).read_text().splitlines() if l.startswith('+') and not l.startswith('+++')]


def added_entry(path):
    """The changelog entry a trial added: the one '+- ' line of its real patch, verbatim."""
    lines = [l for l in added(path) if l.startswith('- ')]
    assert len(lines) == 1, f'{path}: expected one added entry, found {lines}'
    return lines[0]


# s19: with the first draft, terra made up a number in five trials of five; with no skill, nobody did.
first_draft = added_entry('first-draft-terra.patch')
assert PR.search(first_draft)
assert all(PR.search(added_entry(f'first-draft-run/gpt-5.6-terra-{i}.patch')) for i in range(5))
no_skill = added_entry('run/terra-no-skill-typo-fix.patch')
assert not PR.search(no_skill) and '(#' not in no_skill, no_skill
rule = [l for l in (D / 'src/first-draft-SKILL.md').read_text().splitlines() if 'pull request' in l]
assert rule == ['- Reference the pull request.'], rule
if not PROVISIONAL:
    assert '(#' not in added_entry('run/haiku-no-skill-typo-fix.patch')                    # "neither did the other model"
    for v in ('haiku-no-skill', 'terra-no-skill'):
        sec = added(f'run/{v}-security.patch')                                              # "filed under Fixed"
        assert '### Fixed' in sec and '### Security' not in sec, (v, sec)
        assert any(l.startswith('- ') for l in added(f'run/{v}-refactor.patch')), v         # "wrote an entry"

# ---- Rows of two boxes: without the skill, with it ------------------------------------------------
MARK = {'p': ('tick', '✔'), 'f': ('cross', '✘')}
ANSWERS = [('a-helps', 'fp', 'the skill helps', 'fails without it, passes with it'),
           ('a-same', 'pp', 'no difference', 'the model manages either way'),
           ('a-hurts', 'pf', 'the skill hurts', 'passes without it, fails with it')]


def answer_rows():
    head = ('<div class="trow head"><span class="boxes"><span class="num">without</span>'
            '<span class="num">with</span></span></div>')
    rows = ''
    for cid, marks, word, mean in ANSWERS:
        bx = ''.join(f'<span class="box {MARK[m][0]}">{MARK[m][1]}</span>' for m in marks)
        rows += f'''<div class="trow" data-concept="{cid}" data-rep="row">
      <span class="boxes">{bx}</span><span class="word">{word}</span><span class="mean">{mean}</span>
    </div>'''
    return f'<div class="rows">{head}{rows}</div>'


BOX_CSS = ('.rows{display:flex;flex-direction:column;gap:18px;width:100%}'
           '.trow{display:flex;align-items:center;gap:40px;padding:14px 22px;border-radius:10px;width:fit-content}'
           '.trow.head{padding-top:0;padding-bottom:0}'
           '.boxes{display:flex;gap:18px}'
           '.num{width:150px;text-align:center;font:500 30px/1 var(--font-body);color:var(--ink-muted)}'
           '.box{display:flex;align-items:center;justify-content:center;width:150px;height:96px;border-radius:8px;'
           'border:3px solid var(--ink-muted);font:700 52px/1 var(--font-body);color:var(--ink)}'
           '.box.tick{color:var(--green-ink)}.box.cross{color:var(--red-ink)}'
           '.trow .word{font:600 44px/1 var(--font-body);color:var(--ink);min-width:400px}'
           '.trow .mean{font:400 36px/1.3 var(--font-body);color:var(--ink-soft)}')

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Better with the skill?', f'''<div class="cols wide terms">
    {block("with", "structure", "With the skill", "measured in every run so far", words=True)}
    {block("without", "attention", "With no skill", "never run", words=True)}
  </div>''', [
    {"type": "focus", "target": "with", "at": "3~earlier versions", "color": "blue"},
    {"type": "focus", "target": "without", "at": "3~no skill", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.terms .semantic-block{min-height:260px}.terms .label{font-size:34px}')

# ---- Chapter: Does the skill beat no skill? --------------------------------------------------------
CH1 = 'Does the skill beat no skill?'
framed('s02', CH1, 'A skill costs something', f'''<div class="cols wide terms">
    {block("read", "structure", "More text to read", "on every request", words=True)}
    {block("upkeep", "structure", "Upkeep", "it has to be maintained", words=True)}
    {block("wrong", "attention", "Mistakes", "a skill can be wrong", words=True)}
  </div>''', [
    {"type": "focus", "target": "read", "at": "1", "color": "blue"},
    {"type": "focus", "target": "upkeep", "at": "2~maintained", "color": "blue"},
    {"type": "focus", "target": "wrong", "at": "2~wrong", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.terms .semantic-block{min-height:260px}.terms .label{font-size:34px}')

framed('s03', CH1, 'Skills don’t always help', f'''<div class="cols wide terms">
    {block("care", "success", "About +17 points", "more tasks completed, with skills written with care", words=True)}
    {block("worse", "attention", "13 of 87 tasks", "made worse by those same skills", words=True)}
    {block("self", "failure", "Fewer tasks completed", "with skills the models wrote themselves", words=True)}
  </div>
  <p class="note">Source: SkillsBench, version 4, 2026 · a preprint · one benchmark of 87 tasks</p>''', [
    {"type": "focus", "target": "care", "at": "2~seventeen", "color": "green"},
    {"type": "focus", "target": "worse", "at": "3~thirteen", "color": "yellow"},
    {"type": "focus", "target": "self", "at": "4~fewer", "color": "red"}],
    css='.terms .semantic-block{min-height:300px}.terms .label{font-size:32px}.terms .title{font-size:42px}')

framed('s04', CH1, 'Change one thing', f'''<div class="cols wide terms">
    {block("base", "attention", "No skill installed", "the baseline", words=True)}
    {block("inst", "structure", "The skill installed", "compared against it", words=True)}
  </div>
  <div class="cols wide terms one">
    {block("same", "structure", "Same stimuli · same graders · same model", "everything else is produced the same way", words=True)}
  </div>''', [
    {"type": "focus", "target": "same", "at": "1~same stimuli", "color": "blue"},
    {"type": "focus", "target": "inst", "at": "1~whether", "color": "yellow"},
    {"type": "focus", "target": "base", "at": "2~baseline", "color": "yellow"}],
    css='.terms .semantic-block{min-height:200px}.terms .label{font-size:34px}.terms.one .semantic-block{min-height:150px}'
        '.stage{gap:32px}')

framed('s05', CH1, 'Three possible answers', answer_rows() + '''
  <p class="note">An illustration: one stimulus on one model, without the skill and with it</p>''', [
    {"type": "focus", "target": "a-helps", "at": "1", "color": "green"},
    {"type": "focus", "target": "a-same", "at": "2", "color": "blue"},
    {"type": "focus", "target": "a-hurts", "at": "3", "color": "red"},
    {"type": "focus", "target": "none", "at": "4"}], css=BOX_CSS)

# ---- Chapter: An experiment file -------------------------------------------------------------------
CH2 = 'An experiment file'
exp = (D / 'src/with-and-without.experiment.yaml').read_text().splitlines()
assert exp[3].strip() == '- changelog.eval.yaml' and exp[5].startswith('vary:') and exp[7] == 'baseline: haiku-no-skill'
assert exp[10].strip() == 'haiku-no-skill:' and exp[14].strip() == 'skills: []' and len(exp) == 30
TOP = (('evals', 'the eval file to run'), ('vary', 'what variants may differ in'),
       ('baseline', 'the variant the others are compared with'))
framed('s06', CH2, 'Variants of one eval', f'''<div class="annotated">
    {panel('exp')}
    {callouts(*TOP)}
  </div>''', [
    {"type": "focus", "target": "evals", "at": "4~evals line", "color": "blue"}], layout='layout-file', css='.stage{justify-content:flex-start}')

framed('s07', CH2, 'Only these may differ', f'''<div class="annotated">
    {panel('exp')}
    {callouts(*TOP)}
  </div>
  <p class="note">If a variant differs in anything else, Vally stops with: {cell('drift', 'Experiment drift detected', 'note').replace('<span ', '<span class="mono" ')}</p>''', [
    {"type": "focus", "target": "vary", "at": "0~vary line", "color": "blue"},
    {"type": "focus", "target": "drift", "at": "2~experiment drift", "color": "yellow"},
    {"type": "focus", "target": "baseline", "at": "4~baseline line", "color": "blue"}], layout='layout-file', css='.stage{justify-content:flex-start}')

framed('s08', CH2, 'Four variants, two models', f'''<div class="annotated">
    {panel('exp')}
    {callouts(('vname', 'a name we choose'), ('model', 'replaces the eval file’s default'),
              ('noskill', 'an empty list: no skill installed'), ('skill', 'the skill, as in the eval file'),
              ('terra', 'the same pair, for the other model'))}
  </div>''', [
    {"type": "scroll", "target": "#exp", "to": "11-18", "at": "0"},
    {"type": "focus", "target": "vname", "at": "0~name", "color": "blue"},
    {"type": "focus", "target": "model", "at": "1~model", "color": "blue"},
    {"type": "focus", "target": "noskill", "at": "2~empty", "color": "yellow"},
    {"type": "scroll", "target": "#exp", "to": "16-23", "at": "3"},
    {"type": "focus", "target": "skill", "at": "3~installs", "color": "green"},
    {"type": "scroll", "target": "#exp", "to": "21-28", "at": "4"},
    {"type": "focus", "target": "terra", "at": "4~terra", "color": "blue"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file', css='.stage{justify-content:flex-start}')

CMDS = '''⟦cmd:vally experiment run⟧ \\
  evals/with-and-without.experiment.yaml ⟦dry:--dry-run⟧

vally experiment run \\
  evals/with-and-without.experiment.yaml \\
  ⟦flags:--workers 2 --output-dir results/lesson-10⟧'''
framed('s09', CH2, 'One command runs them all', f'''<div class="annotated">
    {code(CMDS, 'bash')}
    {callouts(('cmd', 'runs every variant in the file'), ('dry', 'print the plan, start no agent'),
              ('flags', 'as with vally eval'))}
  </div>''', [
    {"type": "focus", "target": "cmd", "at": "0~experiment run", "color": "blue"},
    {"type": "focus", "target": "dry", "at": "1~dry run", "color": "yellow"},
    {"type": "focus", "target": "flags", "at": "3~workers", "color": "blue"}],
    css='.annotated .code.dark{font-size:34px;line-height:1.6}.callout{font-size:32px}')


def exp_table(filled):
    """The table Vally prints after an experiment: a column per variant, three rows."""
    head = ''.join(f'<th class="num">{cell("vcol", mono(c.replace(" (baseline)", "")))}'
                   + (f'<br>{cell("basecol", "(baseline)")}' if 'baseline' in c else '') + '</th>' for c in cols)
    body = ''
    for key in ('stimuli', 'tokens', 'trial time'):
        cells = ''
        for v in VARIANTS:
            grp = 'no' if v.endswith('no-skill') else 'with'
            val = ROW[key][v] if filled else ''
            cells += f'<td class="num">{cell(f"{key[:3]}-{grp}", val) if filled else ""}</td>'
        body += f'<tr><td>{cell("r-" + key[:3], key, "head")}</td>{cells}</tr>\n'
    return f'''<table class="data-table full exp">
    <thead><tr><th></th>{head}</tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


EXP_CSS = ('.exp{font-size:44px}.exp th{font-size:27px;vertical-align:bottom}.exp th .mono{font-family:var(--font-code);color:var(--ink)}'
           '.exp td{padding-top:30px;padding-bottom:30px;height:60px}.exp td:first-child{font-size:38px}'
           '.exp th:last-child,.exp td:last-child{padding-right:16px}.exp th,.exp td{padding-right:40px}')
framed('s10', CH2, 'One column per variant', exp_table(False) + f'''
  <p class="note">{cell('above', 'above the table: a block for each stimulus that failed', 'note')}</p>''', [
    {"type": "focus", "target": "vcol", "at": "0~one column", "color": "blue"},
    {"type": "focus", "target": "basecol", "at": "0~baseline", "color": "yellow"},
    {"type": "focus", "target": "r-sti", "at": "1", "color": "blue"},
    {"type": "focus", "target": "r-tok", "at": "2~tokens", "color": "blue"},
    {"type": "focus", "target": "r-tri", "at": "2~trial time", "color": "blue"},
    {"type": "focus", "target": "above", "at": "3", "color": "yellow"}], css=EXP_CSS)

TREE = '''⟦run:results/lesson-10/2026-…/⟧
  ⟦v:haiku-no-skill/⟧
    ⟦res:results.jsonl⟧
    ⟦ev:changelog/⟧
  ⟦v2:haiku-with-skill/⟧
  ⟦v2:terra-no-skill/⟧
  ⟦v2:terra-with-skill/⟧
  ⟦report:report.md⟧
  ⟦more:…⟧'''
framed('s11', CH2, 'One folder per variant', f'''<div class="annotated">
    {code(TREE, 'text', 'tree')}
    {callouts(('run', 'the run’s folder, named with its time'), ('v', 'one folder per variant'),
              ('res', 'its own results'), ('ev', 'the eval’s folder, laid out as before'),
              ('report', 'one report for the whole experiment'),
              ('more', 'and a few files of Vally’s own'))}
  </div>''', [
    {"type": "focus", "target": "v", "at": "0~subfolder", "color": "yellow"},
    {"type": "focus", "target": "res", "at": "1~results", "color": "blue"},
    {"type": "focus", "target": "ev", "at": "1~folder for the eval", "color": "blue"},
    {"type": "focus", "target": "report", "at": "2~report", "color": "orange"}],
    css='.code.dark.tree{min-width:820px;font-size:36px;line-height:1.62}.callout{font-size:32px}')

# ---- Chapter: Four variants, one table -------------------------------------------------------------
CH3 = 'Four variants, one table'
ASKS = {'typo-fix': 'a typo fix, with no pull request number', 'refactor': 'a cleanup that users can’t see',
        'security': 'a security fix', 'two-changes': 'two changes in one pull request',
        'after-release': 'a changelog with no Unreleased section'}
stim_rows = ''.join(f'<tr><td class="mono">{s}</td><td>{cell("q-" + s, ASKS[s])}</td></tr>\n' for s in STIMULI)
framed('s12', CH3, 'Which pass with no skill?', f'''<table class="data-table full stim">
    <thead><tr><th>stimulus</th><th>the request</th></tr></thead>
    <tbody>
{stim_rows}    </tbody>
  </table>''', [
    {"type": "focus", "target": "q-typo-fix", "at": "1~typo fix", "color": "blue"},
    {"type": "focus", "target": "q-refactor", "at": "1~refactor", "color": "blue"},
    {"type": "focus", "target": "q-security", "at": "1~security fix", "color": "blue"},
    {"type": "focus", "target": "q-two-changes", "at": "2~two changes", "color": "blue"},
    {"type": "focus", "target": "q-after-release", "at": "2~Unreleased", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.stim{font-size:40px}.stim td{padding-top:20px;padding-bottom:20px}.stim td.mono{font-family:var(--font-code);font-size:36px}')

framed('s15', CH3, 'The table, filled in', exp_table(True) + f'''
  <p class="note">from our run · {RUN} · tokens and trial time are totals over a variant’s five trials</p>''', [
    {"type": "focus", "target": "sti-no", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "sti-with", "at": "2", "color": "green"}], css=EXP_CSS)

fail_rows = ''.join(
    f'<tr><td class="mono">{cell("fv", v)}</td><td class="mono">{cell("f-" + s, s)}</td>'
    f'<td class="mono">{cell("f-" + s, " ".join(g))}</td></tr>\n' for v, s, g in FAILS)
framed('s16', CH3, 'Which stimuli failed', f'''<table class="data-table full fails">
    <thead><tr><th>variant</th><th>stimulus</th><th>the grader that failed</th></tr></thead>
    <tbody>
{fail_rows}    </tbody>
  </table>
  <p class="note">the blocks our run printed above the table · {RUN}</p>''', [
    {"type": "focus", "target": "fv", "at": "1~no-skill", "color": "yellow"},
    {"type": "focus", "target": "f-refactor", "at": "2~refactor", "color": "red"},
    {"type": "focus", "target": "f-security", "at": "3~security fix", "color": "red"},
    {"type": "focus", "target": "f-after-release", "at": "4", "color": "red"}],
    css='.fails{font-size:38px}.fails td{padding-top:18px;padding-bottom:18px}.fails td.mono{font-family:var(--font-code)}')

# ---- Chapter: What the comparison showed -----------------------------------------------------------
CH4 = 'What the comparison showed'
SHORT = {'haiku-no-skill': ('haiku', 'no skill'), 'haiku-with-skill': ('haiku', 'skill'),
         'terra-no-skill': ('terra', 'no skill'), 'terra-with-skill': ('terra', 'skill')}
HELPS = [s for s in STIMULI if all(PASSED[v][s] == v.endswith('with-skill') for v in VARIANTS)]
SAME = [s for s in STIMULI if all(PASSED[v][s] for v in VARIANTS)]
MIXED = [s for s in STIMULI if s not in HELPS and s not in SAME]
assert HELPS == ['refactor', 'security'] and SAME == ['typo-fix', 'two-changes'] and MIXED == ['after-release']   # s18
assert not PASSED['haiku-no-skill']['after-release'] and PASSED['terra-no-skill']['after-release']             # s18, s22


def grid():
    head = ''.join(
        f'<th class="num">{cell("h-" + ("no" if v.endswith("no-skill") else "with"), f"{SHORT[v][0]} · {SHORT[v][1]}", "head")}</th>'
        for v in VARIANTS)
    body = ''
    for s in STIMULI:
        grp = 'r-help' if s in HELPS else 'r-same' if s in SAME else 'r-mixed'
        cells = ''
        for i, v in enumerate(VARIANTS):
            ok = PASSED[v][s]
            g = f'<span class="{"tick" if ok else "cross"}">{"✔" if ok else "✘"}</span>'
            cells += f'<td class="num">{cell("cell0", g) if (s, i) == ('after-release', 0) else g}</td>'
        body += f'<tr><td class="mono">{cell(grp, s, "head")}</td>{cells}</tr>\n'
    return f'''<table class="data-table full grid">
    <thead><tr><th>stimulus</th>{head}</tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


GRID_CSS = ('.grid{font-size:44px}.grid th{font-size:30px}.grid td{padding-top:14px;padding-bottom:14px}'
            '.grid td.mono{font-family:var(--font-code);font-size:36px}'
            '.grid .tick{color:var(--green-ink);font-weight:700}.grid .cross{color:var(--red-ink);font-weight:700}'
            '.grid th:last-child,.grid td:last-child{padding-right:16px}')
framed('s18', CH4, 'Where the skill helps', grid() + f'''
  <p class="note">from our run · one trial per cell</p>''', [
    {"type": "focus", "target": "h-with", "at": "1~five of five", "color": "green"},
    {"type": "focus", "target": "h-no", "at": "1~two of five", "color": "yellow"},
    {"type": "focus", "target": "r-help", "at": "2~refactor", "color": "green"},
    {"type": "focus", "target": "r-same", "at": "3", "color": "blue"},
    {"type": "focus", "target": "r-mixed", "at": "4", "color": "yellow"}], css=GRID_CSS)

mark_pr = lambda e: PR.sub(lambda m: f'⟦pr:{m.group(0).strip()}⟧', e)
framed('s19', CH4, 'The first draft caused it', f'''<div class="results">
      {card('card-a', f'{mono("gpt-5.6-terra")} · with the first-draft skill', code(mark_pr(first_draft), 'markdown'))}
      {card('card-b', f'{mono("gpt-5.6-terra")} · with no skill', code(no_skill, 'markdown'))}
      {card('card-c', 'the first draft’s rule', code('⟦rule:' + rule[0] + '⟧', 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "pr", "at": "1~made-up", "color": "yellow"},
    {"type": "focus", "target": "card-b", "at": "2", "color": "green"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "rule", "at": "4", "color": "orange"}],
    css='.results{display:flex;flex-direction:column;gap:26px;width:100%}'
        '.results .card > .code.dark{font-size:36px;padding:22px 32px}.results .card .who{font-size:32px}'
        '.results .card{gap:10px}')

framed('s20', CH4, 'A skill made it worse', answer_rows() + '''
  <p class="lead"><span data-concept="what" data-rep="note">The typo fix: no number with no skill, a made-up number with the first draft.</span></p>''', [
    {"type": "focus", "target": "a-hurts", "at": "0", "color": "red"}],
    css=BOX_CSS + '.lead{font-size:38px;margin:0}.stage{gap:30px}')

tok_rows = ''
for key, m, a, b in (('h', MODELS[0], 'haiku-no-skill', 'haiku-with-skill'), ('t', MODELS[1], 'terra-no-skill', 'terra-with-skill')):
    tok_rows += (f'<tr><td class="mono">{m}</td><td class="num">{cell(key + "-tok", ROW["tokens"][a])}</td>'
                 f'<td class="num">{cell(key + "-tok", ROW["tokens"][b])}</td></tr>\n')
framed('s21', CH4, 'What it changes in tokens', f'''<table class="data-table full toks">
    <thead><tr><th></th><th class="num">tokens, no skill</th><th class="num">{cell('withcol', 'tokens, with the skill', 'head')}</th></tr></thead>
    <tbody>
{tok_rows}    </tbody>
  </table>
  <p class="note">from our run · each figure is the total over five trials, one per stimulus</p>''', [
    {"type": "focus", "target": "withcol", "at": "2~fewer", "color": "blue"},
    {"type": "focus", "target": "h-tok", "at": "3", "color": "blue"},
    {"type": "focus", "target": "t-tok", "at": "4", "color": "blue"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.toks{font-size:60px}.toks th{font-size:32px}.toks td{padding-top:40px;padding-bottom:40px}'
        '.toks td.mono{font-family:var(--font-code);font-size:38px}.toks th:last-child,.toks td:last-child{padding-right:16px}')

framed('s22', CH4, 'One trial per cell', grid() + f'''
  <p class="note">from our run · each cell is one trial</p>''', [
    {"type": "focus", "target": "r-help", "at": "1", "color": "green"},
    {"type": "focus", "target": "cell0", "at": "2~single cell", "color": "yellow"}], css=GRID_CSS)

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('The skill helps', 'fails without it, passes with it'),
    ('No difference', 'the same result either way'),
    ('The skill hurts', 'passes without it, fails with it')], 1))
framed('s23', 'Recap', 'What are the three answers?', f'''<div class="semantic-block" id="answers" data-role="structure">
    <div class="title words">one stimulus, with and without the skill</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#answers", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "green"},
    {"type": "focus", "target": "p2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p3", "at": "3", "color": "red"}], layout='layout-expand',
    css='#answers{width:100%;padding:36px 40px 44px;gap:24px}'
        '#answers .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#answers .part{min-height:280px}#answers .part .title{font-size:48px;line-height:1.2}'
        '#answers .part .label{font-size:32px}')

scene('s24', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Follow-up requests</h1>
  <p class="lead">Does the skill still hold when the conversation continues?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Run Your First Experiment”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok' + (' (PROVISIONAL run data)' if PROVISIONAL else ''))
