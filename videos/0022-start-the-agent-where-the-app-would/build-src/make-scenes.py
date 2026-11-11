"""Generate lesson 22's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/release.eval.yaml, check-release.mjs   the two files the tapes install (verified/lesson-22/practice)
  src/state/list-merged.mjs                        the release tool, already in the practice folder
  src/changelog.eval.yaml                          the earlier, person-written requests (typo-fix, refactor)
  src/run/                                         this video's lesson 22 run: trials.json (model, trial,
                                                   passed, loaded, reply), <model>-<trial>.patch, RUN, s16.log.
                                                   Until s16 is recorded it is a stand-in (src/run/PROVISIONAL);
                                                   build-src/collect-run.sh replaces it.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess, textwrap

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
H, T = MODELS
RUNS = 5
SHOWN = {H: 1, T: 0}          # the trial folders tapes s17 and s18 print with cat


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


# ---- The files the lesson works with --------------------------------------------------------------------
spec = (D / 'src/state/release.eval.yaml').read_text().splitlines()
assert spec[16].strip() == 'prompt: >-' and spec[20].strip() == 'commands:', spec[16:21]
APP_PROMPT = [spec[17].strip(), spec[18].strip()]
assert ' '.join(APP_PROMPT) == 'Write the Unreleased changelog entries for every change listed in release/merged.txt.'
SETUP = spec[22].strip().strip('- ').strip('"')
assert SETUP == 'node tools/list-merged.mjs > release/merged.txt', SETUP
MERGED = re.findall(r'^\s*"(#\d+ \w+: [^"]+)",$', (D / 'src/state/list-merged.mjs').read_text(), re.M)
assert [m.split(':')[0] for m in MERGED] == ['#74 feat', '#75 fix', '#76 refactor'], MERGED


def person_prompt(name):
    lines = (D / 'src/changelog.eval.yaml').read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip() == f'- name: {name}')
    j = next(k for k in range(i, len(lines)) if lines[k].strip() == 'prompt: |')
    out = []
    for l in lines[j + 1:]:
        if not l.startswith('      '):
            break
        out.append(l.strip())
    return ' '.join(out)


TYPO_REQ, REFACTOR_REQ = person_prompt('typo-fix'), person_prompt('refactor')
assert 'Nothing changes for users' in REFACTOR_REQ and 'tittle' in TYPO_REQ

# ---- This video's run -----------------------------------------------------------------------------------
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
RUN = (D / 'src/run/RUN').read_text().strip()
RUN_LABEL = 'stand-in: the course’s verified run, not yet ours' if PROVISIONAL else f'our run · {RUN}'
trials = json.loads((D / 'src/run/trials.json').read_text())
assert len(trials) == len(MODELS) * RUNS, len(trials)
bad = [(t['model'], t['trial']) for t in trials if t['status'] != 'success']
assert not bad, f'trials that did not finish (ERROR): {bad}. Re-record tapes/s16.tape.'
TR = {(t['model'], t['trial']): t for t in trials}


def patch(m, i):
    return (D / f'src/run/{m}-{i}.patch').read_text().splitlines()


def added(m, i):
    return [l[1:] for l in patch(m, i) if l.startswith('+') and not l.startswith('+++')]


def cites(m, i, pr):
    return [l for l in added(m, i) if f'(#{pr})' in l]


def heading_of(m, i, line):
    """The ### heading the added line sits under, read from the patch (context lines included)."""
    head = None
    for l in patch(m, i):
        body = l[1:]
        if body.startswith('### '):
            head = body[4:].strip()
        if l.startswith('+') and body == line:
            return head


def count(m, pr):
    return sum(len(cites(m, i, pr)) > 0 for i in range(RUNS))


for m in MODELS:
    for i in range(RUNS):
        files = [l for l in patch(m, i) if l.startswith('diff --git')]
        # s17: "Only the changelog is in the patch: the merged file isn't."
        assert files == ['diff --git a/CHANGELOG.md b/CHANGELOG.md'], (m, i, files)
        merged_two = [l for l in added(m, i) if l.count('(#') > 1]
        handled = (len(cites(m, i, 74)) == 1 and len(cites(m, i, 75)) == 1 and not cites(m, i, 76) and not merged_two)
        # The hidden test's verdict should be what the patch shows.
        assert handled == TR[m, i]['passed'], (m, i, handled, TR[m, i]['passed'])

passed = {m: sum(TR[m, i]['passed'] for i in range(RUNS)) for m in MODELS}
loaded = {m: sum(TR[m, i]['loaded'] for i in range(RUNS)) for m in MODELS}

# ---- What the narration says about the run. If a recording changes these, the sentences change too. -------
# s16: "that table shows a cross for haiku, and a tick for terra"; "the command exited with code one, in all
#      five of haiku's trials".
assert passed == {H: 2, T: RUNS}, passed
FAILED = [i + 1 for i in range(RUNS) if not TR[H, i]['passed']]      # as the console numbers them
assert FAILED == [1, 2, 5], FAILED
# s17 (tapes/s17.tape prints haiku's folder 1): "entries for the feature and the fix, and a third, under
#      Changed, for the refactor."
hs = SHOWN[H]
assert len(cites(H, hs, 74)) == 1 and len(cites(H, hs, 75)) == 1 and len(cites(H, hs, 76)) == 1, added(H, hs)
REFACTOR_ENTRY = cites(H, hs, 76)[0]
assert heading_of(H, hs, REFACTOR_ENTRY) == 'Changed', heading_of(H, hs, REFACTOR_ENTRY)
# s18 (tapes/s18.tape prints terra's folder 0): "a trial from terra, which passed"; "two entries, for the
#      feature and the fix, and nothing for the refactor."
ts = SHOWN[T]
assert TR[T, ts]['passed'] and len(cites(T, ts, 74)) == 1 and len(cites(T, ts, 75)) == 1 and not cites(T, ts, 76)
assert len([l for l in added(T, ts) if l.startswith('- ')]) == 2, added(T, ts)
# s19: "neither model skipped a change, and neither merged two into one entry"; "haiku wrote an entry for the
#      refactor in all five of its trials"; "that entry sits under Changed and names a source file";
#      "Terra left the refactor out every time, and said why in its reply."
for m in MODELS:
    assert count(m, 74) == RUNS and count(m, 75) == RUNS, (m, count(m, 74), count(m, 75))
    assert not any(l.count('(#') > 1 for i in range(RUNS) for l in added(m, i)), m
assert count(H, 76) == 3 and count(T, 76) == 0, (count(H, 76), count(T, 76))
assert re.search(r'\b[\w-]+\.(js|mjs|ts)\b', REFACTOR_ENTRY), REFACTOR_ENTRY
if not PROVISIONAL:
    silent = [i for i in range(RUNS) if not re.search(r'#?76|refactor', TR[T, i]['reply'], re.I)]
    assert not silent, f'terra replies that do not mention the refactor: {silent}'
# s22: "Terra's entries for the feature each say what the new flag filters by, and they don't all say the
#      same thing." The counts are on screen (the callouts), not in the voice.
KINDS = [('on or after', 'created on or after a date'), ('created after', 'created after a date')]
T74 = [cites(T, i, 74)[0] for i in range(RUNS)]
by_kind = [[e for e in T74 if k in e] for k, _ in KINDS]
assert all(sum(k in e for k, _ in KINDS) == 1 for e in T74), T74
assert all(by_kind), f"terra's #74 entries all say the same thing: reword s22 sentence 1. {sorted(set(T74))}"
# s20: "Terra loaded it in all five trials, and haiku in three." "Haiku's two trials without the skill both
#      recorded the refactor; of the three with it, two left the refactor out, and one recorded it anyway."
# s21: "haiku skipped the skill in two of its five trials, and recorded the refactor in both"; "one trial
#      loaded the skill and recorded the refactor anyway".
assert loaded == {H: 3, T: RUNS}, loaded
HL = [(TR[H, i]['loaded'], bool(cites(H, i, 76))) for i in range(RUNS)]
assert sorted(HL) == sorted([(False, True)] * 2 + [(True, False)] * 2 + [(True, True)]), HL
assert all(TR[T, i]['loaded'] and not cites(T, i, 76) for i in range(RUNS))

# ---- Hook ------------------------------------------------------------------------------------------------
MERGED_BOX = code('\n'.join(MERGED), 'text', 'merged')
framed('s01', 'Vally &amp; Agent Evals', 'Where the app starts', f'''<div class="cols pair">
    {quote('person', 'A person asks', '“' + esc(TYPO_REQ) + '”')}
    <div class="tool" data-concept="tool" data-rep="card">
      {quote('toolq', 'The release tool asks', '“' + esc(' '.join(APP_PROMPT)) + '”')}
      {card('listc', mono('release/merged.txt'), MERGED_BOX)}
    </div>
  </div>''', [
    {"type": "focus", "target": "person", "at": "0~person", "color": "blue"},
    {"type": "focus", "target": "tool", "at": "2~small tool", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.pair{align-items:center}'
        '.tool{display:flex;flex-direction:column;gap:16px;border-radius:12px}'
        '.quote p{font-size:34px;line-height:1.34}.card{width:100%}.card .who{font-size:28px}'
        '.card > .code.dark.merged{font-size:28px;line-height:1.45;padding:18px 26px}')

# ---- Chapter: An app starts the agent ----------------------------------------------------------------------
EB1 = 'An app starts the agent'
TERMS = '.terms .semantic-block{min-height:290px}.terms .title{font-size:52px}.terms .label{font-size:34px;line-height:1.35}'
framed('s02', EB1, 'Two halves, both from the app', f'''<div class="cols wide terms">
    {block("prompt", "structure", "The prompt", "what the app sends: short, always the same, written by a developer", words=True)}
    {block("workspace", "attention", "The workspace", "what the app has prepared when it calls the agent", words=True)}
  </div>''', [
    {"type": "focus", "target": "prompt", "at": "2", "color": "blue"},
    {"type": "focus", "target": "workspace", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], css=TERMS)

framed('s03', EB1, 'Run the app’s own setup', f'''<p class="lead">Next month, the team changes the list’s format.</p>
  <div class="cols wide terms">
    {block("runs", "success", "An eval that runs their tool", "sees the new format", words=True)}
    {block("copy", "attention", "A hand-written copy of the list", "keeps passing, and tells you nothing", words=True)}
  </div>''', [
    {"type": "focus", "target": "runs", "at": "3", "color": "green"},
    {"type": "focus", "target": "copy", "at": "4", "color": "yellow"}],
    css=TERMS + '.lead{font-size:42px}.stage{gap:34px}')

ONE = (f'⟦p:{APP_PROMPT[0]}⟧\n{APP_PROMPT[1]}\n\n⟦c:{SETUP}⟧')
framed('s04', EB1, 'One sentence, one command', f'''<div class="annotated">
    {code(ONE, 'text', 'one')}
    {callouts(('p', 'what the app sends'), ('c', 'what the app prepares'))}
  </div>
  <p class="note">Source: Anthropic, “Demystifying evals for AI agents” (2026)</p>''', [
    {"type": "focus", "target": "p", "at": "0~one sentence", "color": "blue"},
    {"type": "focus", "target": "c", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.code.dark.one{font-size:36px;line-height:1.55;padding:30px 36px}.callout{font-size:34px}')

# ---- Chapter: Set up before the agent starts ---------------------------------------------------------------
EB2 = 'Set up before the agent starts'
framed('s05', EB2, 'The tool that writes the list', f'''<div class="annotated">
    {panel('tool')}
    {callouts(('ff', 'users notice: an entry each'), ('rf', 'code only: no entry'))}
  </div>''', [
    {"type": "focus", "target": "ff", "at": "4", "color": "green"},
    {"type": "focus", "target": "rf", "at": "5", "color": "yellow"}], layout='layout-file')


def order(parts, spans):
    """Numbered steps in a row (no arrows: they are steps, not a flow of data), with labelled spans under them."""
    blocks = ''.join(block(c, r, t, l, words=True, step=i) for i, (c, r, t, l) in enumerate(parts, 1))
    sp = ''.join(f'<div class="span" style="grid-column:span {w}"><span data-concept="{c}" data-rep="note">{t}</span></div>'
                 for c, w, t in spans)
    return f'<div class="order" style="grid-template-columns:repeat({len(parts)},1fr)">{blocks}{sp}</div>'


ORDER_CSS = ('.order{display:grid;gap:22px 26px;width:100%}'
             '.order .semantic-block{min-height:250px}.order .title{font-size:46px;line-height:1.15}'
             '.order .label{font-size:32px;line-height:1.3}'
             '.order .span{border-top:4px solid var(--ink-muted);padding-top:16px;text-align:center;'
             'font:500 36px/1.2 var(--font-body);color:var(--ink)}'
             '.order .span span{padding:4px 14px;border-radius:8px}')
STEPS = [('b1', 'structure', 'Stage', 'the files and the skill'),
         ('b2', 'transform', 'Run commands', 'in the workspace, in order'),
         ('b3', 'attention', 'Agent works', 'on the app’s prompt')]
framed('s06', EB2, 'Commands run before the agent',
       order(STEPS, [('start', 2, 'the starting state'), ('inpatch', 1, 'in the patch')]), [
    {"type": "focus", "target": "b2", "at": "2~runs them", "color": "cyan"},
    {"type": "focus", "target": "start", "at": "5~starting state", "color": "yellow"},
    {"type": "focus", "target": "inpatch", "at": "6", "color": "green"}], css=ORDER_CSS)

framed('s07', EB2, 'The app’s situation, as a stimulus', f'''<div class="annotated">
    {panel('spec')}
  </div>''', [
    {"type": "focus", "target": "tool", "at": "1~staged", "color": "blue"},
    {"type": "scroll", "target": "#spec", "to": "15-23", "at": "2"},
    {"type": "focus", "target": "prompt", "at": "2~prompt", "color": "yellow"},
    {"type": "focus", "target": "cmds", "at": "3~two commands", "color": "blue"},
    {"type": "focus", "target": "q", "at": "5~quotes", "color": "yellow"}], layout='layout-file')

GIT = 'agent_environment:\n  git:\n    type: ⟦wt:worktree⟧\n    ref: v2.1.0\n    source: ⟦src:../my-repo⟧'
framed('s08', EB2, 'Two more ways to prepare', f'''<div class="envrow">
    {block("env", "structure", "env:", "environment variables for the agent’s process · values can show up in saved trials")}
  </div>
  <div class="annotated">
    {code(GIT, 'yaml', 'git')}
    {callouts(('wt', 'check out a commit, tag or branch'), ('src', 'from a repository on your machine'))}
  </div>
  <p class="note">The shape is from Vally’s Eval Spec reference · not run here</p>''', [
    {"type": "focus", "target": "env", "at": "1", "color": "blue"},
    {"type": "focus", "target": "wt", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "src", "at": "2~history", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.envrow{width:100%}.envrow .semantic-block{min-height:0;padding:22px 32px}.envrow .title{font-size:44px}'
        '.envrow .label{font-size:32px}.code.dark.git{font-size:36px;line-height:1.45;min-width:760px;padding:24px 34px}'
        '.callout{font-size:32px}.stage{gap:26px}.note{margin:0}')

# ---- Chapter: A hidden test ---------------------------------------------------------------------------------
EB3 = 'A hidden test'
NEEDS = '\n'.join(f'⟦n{i}:{m.split(":")[0]}⟧:{m.split(":", 1)[1]}' for i, m in enumerate(MERGED))
framed('s09', EB3, 'The answer depends on the list', f'''<div class="annotated">
    {card('listc', mono('release/merged.txt'), code(NEEDS, 'text', 'needs'))}
    {callouts(('n0', 'one line, citing #74'), ('n1', 'one line, citing #75'), ('n2', 'no line'))}
  </div>''', [
    {"type": "focus", "target": "n0", "at": "1~feature", "color": "green"},
    {"type": "focus", "target": "n1", "at": "1~fix", "color": "green"},
    {"type": "focus", "target": "n2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.card .who{font-size:30px}.card > .code.dark.needs{font-size:36px;line-height:1.7;padding:26px 34px}'
        '.callout{font-size:34px}')

framed('s10', EB3, 'Exit code zero is a pass', f'''<div class="cols wide terms">
    {block("program", "structure", "program", "the script prints its verdict as a line of JSON")}
    {block("rc", "attention", "run-command", "passes when the command exits with code 0")}
  </div>
  <p class="lead">Any test you already have: a test suite, a linter, a script.</p>''', [
    {"type": "focus", "target": "program", "at": "0~program", "color": "blue"},
    {"type": "focus", "target": "rc", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css=TERMS + '.lead{font-size:40px}.stage{gap:34px}')

framed('s11', EB3, 'Staged for grading only', f'''<div class="annotated">
    {panel('spec2')}
  </div>''', [
    {"type": "scroll", "target": "#spec2", "to": "24-32", "at": "1"},
    {"type": "focus", "target": "genv", "at": "1", "color": "blue"},
    {"type": "focus", "target": "gname", "at": "2~grader", "color": "yellow"},
    {"type": "focus", "target": "cmd", "at": "2~runs", "color": "yellow"}], layout='layout-file')

framed('s12', EB3, 'What the hidden test checks', f'''<div class="annotated">
    {panel('test')}
  </div>''', [
    {"type": "scroll", "target": "#test", "to": "4-10", "at": "1"},
    {"type": "focus", "target": "log", "at": "1~changelog", "color": "blue"},
    {"type": "focus", "target": "list", "at": "1~merged list", "color": "yellow"},
    {"type": "focus", "target": "unrel", "at": "2", "color": "blue"},
    {"type": "scroll", "target": "#test", "to": "12-20", "at": "3"},
    {"type": "focus", "target": "parts", "at": "3~number", "color": "blue"},
    {"type": "focus", "target": "found", "at": "3~finds", "color": "blue"},
    {"type": "focus", "target": "ref", "at": "4", "color": "yellow"},
    {"type": "scroll", "target": "#test", "to": "15-23", "at": "5"},
    {"type": "focus", "target": "one", "at": "5~exactly one", "color": "yellow"},
    {"type": "focus", "target": "share", "at": "5~second", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "6"},
    {"type": "scroll", "target": "#test", "to": "21-29", "at": "7"},
    {"type": "focus", "target": "exit", "at": "7~code one", "color": "yellow"}], layout='layout-file')

framed('s13', EB3, 'This one can’t be re-graded', f'''<div class="cols wide terms">
    {block("patchy", "success", "Reads the patch or the trajectory", "can be re-graded from saved trials", words=True)}
    {block("needs", "attention", "Needs the finished workspace", "cannot: Vally doesn’t keep it", words=True)}
  </div>''', [
    {"type": "focus", "target": "needs", "at": "0~needs", "color": "yellow"},
    {"type": "focus", "target": "patchy", "at": "1~patch", "color": "green"}], css=TERMS)

# ---- Chapter: Run it on two models --------------------------------------------------------------------------
EB4 = 'Run it on two models'
ROWS = [(74, 'feat'), (75, 'fix'), (76, 'refactor')]


def entries_table(filled):
    def cell(m, pr):
        if not filled:
            return '<td class="num"></td>'
        cid = 'ok' if pr != 76 else ('h76' if m == H else 't76')
        return f'<td class="num"><span data-concept="{cid}" data-rep="cell">{count(m, pr)} of {RUNS}</span></td>'
    body = ''.join(
        f'<tr><td class="mono"><span data-concept="r{pr}" data-rep="row">#{pr} {kind}</span></td>'
        + ''.join(cell(m, pr) for m in MODELS) + '</tr>\n' for pr, kind in ROWS)
    return f'''<table class="data-table full counts">
    <thead><tr><th>trials with an entry for it</th><th class="mono num">{H}</th><th class="mono num">{T}</th></tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


COUNTS_CSS = ('.counts{font-size:46px}.counts th{font-size:30px}.counts th.mono{font-family:var(--font-code);font-size:32px}'
              '.counts td{padding-top:32px;padding-bottom:32px;height:60px}'
              '.counts td.mono{font-family:var(--font-code);font-size:38px}'
              '.counts th:last-child,.counts td:last-child{padding-right:16px}')
framed('s14', EB4, 'What will each model write?', entries_table(False) + '''
  <p class="note">five trials on each model · the list has three changes</p>''', [
    {"type": "focus", "target": "r76", "at": "4~refactor", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], css=COUNTS_CSS)

# ---- Chapter: What it showed --------------------------------------------------------------------------------
EB5 = 'What it showed'
framed('s19', EB5, 'One kind of failure', entries_table(True) + f'''
  <p class="note">{RUN_LABEL}</p>''', [
    {"type": "focus", "target": "ok", "at": "1", "color": "green"},
    {"type": "focus", "target": "h76", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "t76", "at": "4", "color": "green"}], css=COUNTS_CSS)


def yn(v, cid):
    return f'<td class="num"><span data-concept="{cid}" data-rep="cell">{"yes" if v else "no"}</span></td>'


KIND = {(False, True): 'skip', (True, False): 'used', (True, True): 'odd'}
load_rows = ''.join(
    f'<tr><td class="mono"><span data-concept="{KIND[hl]}" data-rep="row">{H} · trial {i + 1}</span></td>'
    f'{yn(hl[0], KIND[hl])}{yn(hl[1], KIND[hl])}</tr>\n' for i, hl in enumerate(HL))
load_rows += (f'<tr><td class="mono"><span data-concept="t" data-rep="row">{T} · all five trials</span></td>'
              f'{yn(True, "t")}{yn(False, "t")}</tr>\n')
LOAD_TABLE = f'''<table class="data-table full counts load">
    <thead><tr><th></th><th class="num">loaded the skill</th><th class="num">entry for the refactor</th></tr></thead>
    <tbody>
{load_rows}    </tbody>
  </table>'''

framed('s21', EB5, 'The app’s wording matters', f'''<div class="cols pair">
    {quote('person', 'A person’s request, earlier', '“' + esc(REFACTOR_REQ) + '”')}
    {quote('tool', 'The release tool’s input', '“' + esc(' '.join(APP_PROMPT)) + '”<br>' + mono(esc(MERGED[2])))}
  </div>''', [
    {"type": "focus", "target": "tool", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "person", "at": "1~person had said", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.pair{align-items:stretch}.quote p{font-size:36px;line-height:1.36}.quote .mono{font-family:var(--font-code);font-size:32px}')


def wrap(line, width=56):
    return textwrap.wrap(line, width, subsequent_indent='    ', break_long_words=False, break_on_hyphens=False)


said, notes21, cues21 = ['release/merged.txt', f'  ⟦list:{MERGED[0]}⟧', '', f'{T} · what it wrote for #74'], \
    [('list', 'no word on which date')], []
for k, ((needle, _), lines) in enumerate(zip(KINDS, by_kind)):
    if not lines:
        continue
    held = lines[0].replace(needle, needle.replace(' ', '\x00'))
    rows = [w.replace('\x00', ' ') for w in wrap(held)]
    hit = False
    for w in rows:
        if needle in w and not hit:
            w, hit = w.replace(needle, f'⟦w{k}:{needle}⟧', 1), True
        said.append('  ' + w)
    assert hit, (needle, rows)
    notes21.append((f'w{k}', f'{len(lines)} of {RUNS} trials'))
    cues21.append({"type": "focus", "target": f"w{k}", "at": "1~filters by" if not cues21 else "1~same thing", "color": "yellow"})
framed('s22', EB5, 'A pass isn’t proof', f'''<div class="annotated">
    {code(chr(10).join(said), 'markdown', 'said')}
    {callouts(*notes21)}
  </div>
  <p class="note">{RUN_LABEL}</p>''',
       cues21 + [{"type": "focus", "target": "list", "at": "2", "color": "blue"},
                 {"type": "focus", "target": "none", "at": "3"}],
       css='.code.dark.said{font-size:32px;line-height:1.45;padding:22px 30px;min-width:1150px}.callout{font-size:32px}'
           '.stage{gap:22px}.note{margin:0}')

framed('s20', EB5, 'Did it load the skill?', LOAD_TABLE + f'''
  <p class="note">from the saved records of {RUN_LABEL}</p>''', [
    {"type": "focus", "target": "t", "at": "1", "color": "green"},
    {"type": "focus", "target": "skip", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "used", "at": "2~three with it", "color": "green"},
    {"type": "focus", "target": "odd", "at": "2~anyway", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css=COUNTS_CSS + '.load{font-size:36px}.load td{padding-top:15px;padding-bottom:15px;height:auto}'
        '.load td.mono{font-size:32px}.load th{font-size:28px}.stage{gap:18px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Stage', 'files and skill: the starting state'),
    ('Run commands', 'what they make: the starting state'),
    ('Agent works', 'what it changes: in the patch'),
    ('Graders run', 'the hidden test is added here')], 1))
framed('s23', 'Recap', 'What can a diff grader see?', f'''<div class="semantic-block" id="order" data-role="structure">
    <div class="title words">one trial, in order</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#order", "at": "1"},
    {"type": "focus", "target": "p3", "at": "1", "color": "green"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "p4", "at": "3", "color": "blue"}], layout='layout-expand',
    css='#order{width:100%;padding:36px 40px 44px;gap:24px}'
        '#order .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#order .part{min-height:290px}#order .part .title{font-size:46px;line-height:1.2}'
        '#order .part .label{font-size:30px;line-height:1.3}')

scene('s24', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Check what the agent did</h1>
  <p class="lead">Did it read the list, touch other files, try to commit or push?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, Writing Eval Specs, “Grader-only files”</p>
</main>''', [], css='.scene-title.chapter{font-size:112px}')
print('ok', RUN, '(stand-in)' if PROVISIONAL else '')
