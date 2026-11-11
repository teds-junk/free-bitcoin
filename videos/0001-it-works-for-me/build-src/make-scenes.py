"""Generate lesson 1's scene pages. File panels are inserted afterwards by panels.sh.

Every scene is the theme's one frame: an eyebrow naming the chapter, a short display-serif
headline, and a .stage that fills the rest of the safe area. Code, commands and files sit in a
dark box on the left with their notes on the right (.annotated + .callout); the runtime lines
each note up with the line it explains. Nothing here sets a colour or a font: the look lives in
_theme/theme.css (the video-lesson skill's theme).

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
RUN_FOLDER = '2026-11-11T00-11-52-424Z'  # the timestamped folder shown in s10; set to the recorded one


def code(src, lang, extra=''):
    """A dark code box from scripts/code.js. ⟦id:text⟧ marks a concept."""
    out = subprocess.run(['node', str(SKILL / 'scripts/code.js'), '--lang', lang, '--dark'],
                         input=src, capture_output=True, text=True, check=True).stdout.strip()
    return out.replace('class="code dark"', f'class="code dark{" " + extra if extra else ""}"', 1)


def inner(html):
    return re.search(r'<code>([\s\S]*)</code>', html).group(1)


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


def block(cid, role, title, label, step=None, words=False):
    num = f'<div class="step">{step}</div>' if step else ''
    return f'''<div class="semantic-block" data-concept="{cid}" data-rep="block" data-role="{role}">
      {num}<div class="title{' words' if words else ''}">{title}</div><div class="label">{label}</div>
    </div>'''


def panel(pid):
    return f'<!-- file-panel:{pid} -->\n<!-- /file-panel:{pid} -->'


def callouts(*notes):
    return '<aside class="callouts">' + ''.join(
        f'<p class="callout" data-anchor="{anchor}">{text}</p>' for anchor, text in notes) + '</aside>'


REQUEST = 'I fixed the typo in the help text for <span class="inline-code">notes add</span> (it said "tittle"). Put that in the changelog.'


def added_entry(patch):
    """The changelog entry a model added: the one '+- ' line of its real patch, verbatim."""
    lines = [l[1:] for l in (D / 'src' / patch).read_text().splitlines() if l.startswith('+- ')]
    assert len(lines) == 1, f'{patch}: expected one added entry, found {lines}'
    return lines[0]


# ---- Chapter: Will it work on another model? ----------------------------------------------
entry_a, entry_b = added_entry('haiku.patch'), added_entry('terra.patch')
ref = re.search(r'\(#\d+\)\s*$', entry_b)
assert ref and not re.search(r'\(#\d+\)', entry_a), 'the hook shows one entry with a made-up PR number and one without'
entry_b_marked = entry_b[:ref.start()] + '⟦pr42:' + ref.group(0).strip() + '⟧'


def card(cid, who, model, entry):
    return f'''<div class="card" data-concept="{cid}" data-rep="card">
        <div class="who">{who} <span class="mono">{model}</span></div>
        {code(entry, 'markdown')}
      </div>'''


framed('s01', 'Vally &amp; Agent Evals', 'It works for <em>me</em>.', f'''<div class="hook">
    <div class="quote" data-concept="req" data-rep="quote"><span class="who">The request</span><p>“{REQUEST}”</p></div>
    <div class="results">
      {card('card-a', 'Your run, on', 'claude-haiku-4.5', entry_a)}
      {card('card-b', 'A teammate’s run, on', 'gpt-5.6-terra', entry_b_marked)}
    </div>
  </div>''', [
    {"type": "focus", "target": "req", "at": "0~wrote a skill", "color": "blue"},
    {"type": "focus", "target": "card-a", "at": "0~the agent", "color": "green"},
    {"type": "focus", "target": "card-b", "at": "1~another model", "color": "yellow"},
    {"type": "focus", "target": "pr42", "at": "1~something different", "color": "yellow", "channel": "diff", "until": "2"},
    {"type": "focus", "target": "none", "at": "2"}],
    h='h1', title_class='scene-title chapter',
    css='.hook{display:grid;grid-template-columns:560px 1fr;gap:48px;align-items:stretch}'
        '.hook .quote{display:flex;flex-direction:column;justify-content:center}'
        '.results{display:flex;flex-direction:column;gap:36px;justify-content:space-between}'
        '.hook .card > .code.dark{font-size:30px}')

# ---- Chapter: A skill is advice ------------------------------------------------------------
framed('s03', 'A skill is advice', 'A skill is advice.', f'''<div class="cols terms">
    {block("skill", "structure", "skill", "A folder with a SKILL.md file: a name, a description, and instructions.")}
    {block("agent", "transform", "agent", "A program that uses a model and tools to do a task.")}
    {block("model", "attention", "model", 'The part that decides what to do.<span class="names">claude-haiku-4.5<br>gpt-5.6-terra</span>')}
  </div>''', [
    {"type": "focus", "target": "skill", "at": "1", "color": "blue"},
    {"type": "focus", "target": "agent", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "model", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "skill", "at": "4", "color": "blue"},
    {"type": "focus", "target": "model", "at": "5~each model", "color": "yellow"}],
    css='.terms .semantic-block{min-height:330px}'
        '.names{display:block;margin-top:18px;font:500 30px/1.45 var(--font-code);color:var(--ink)}')

framed('s04', 'A skill is advice', 'One line per change.', panel('changelog'), [
    {"type": "focus", "target": "unreleased", "at": "2~Unreleased", "color": "blue"},
    {"type": "focus", "target": "added", "at": "3~Added"},
    {"type": "focus", "target": "entry", "at": "3~one line"},
    {"type": "focus", "target": "pr41", "at": "4~reference", "color": "yellow"}], layout='layout-file')

framed('s05', 'A skill is advice', 'The first draft leaves gaps.', f'''<div class="annotated">
    {panel('skill')}
    {callouts(('category', 'Which categories exist?'), ('reference', 'In what form? What if there isn’t one?'))}
  </div>''', [
    {"type": "scroll", "target": "#skill", "to": "10-13", "at": "2"},
    {"type": "focus", "target": "category", "at": "3~right category", "color": "yellow"},
    {"type": "focus", "target": "reference", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "7"}], layout='layout-file')


def cells(row):
    out = ''
    for i in range(5):
        first = row == 0 and i == 0
        concept = 'first' if first else 'again' if row == 0 else 'others'
        out += f'<td class="num"><span data-concept="{concept}" data-rep="cell">{"✓" if first else "?"}</span></td>'
    return out


framed('s06', 'A skill is advice', 'One try is one observation.', f'''<table class="data-table full grid">
    <thead><tr><th></th>{''.join(f'<th class="num">run {i}</th>' for i in range(1, 6))}</tr></thead>
    <tbody>
      <tr><td>your model</td>{cells(0)}</tr>
      <tr><td>another model</td>{cells(1)}</tr>
      <tr><td>a third model</td>{cells(2)}</tr>
    </tbody>
  </table>''', [
    {"type": "focus", "target": "first", "at": "0~one model", "color": "green"},
    {"type": "focus", "target": "others", "at": "1~next model", "color": "yellow"},
    {"type": "focus", "target": "again", "at": "1~next request", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.grid{font-size:46px}.grid th{font-size:32px}.grid td{padding-top:26px;padding-bottom:26px}'
        '.grid td.num{color:var(--ink-muted)}.grid td.num [data-concept="first"]{color:var(--green-ink);font-weight:700}')

# ---- Chapter: What one Vally run does ---------------------------------------------------------
framed('s07', 'What one Vally run does', 'Vally keeps a record.', f'''<div class="cols wide terms">
    {block("vally", "structure", "Vally", "Runs the GitHub Copilot agent for you, in a controlled way, and keeps a record.")}
    {block("eval", "attention", "eval", "A repeatable test: the same request, the same starting folder, the same check.")}
  </div>''', [
    {"type": "focus", "target": "vally", "at": "2", "color": "blue"},
    {"type": "focus", "target": "eval", "at": "4", "color": "yellow"}],
    css='.terms .semantic-block{min-height:340px}.terms .label{font-size:34px}')

steps = [('ws', 'structure', 'workspace', 'Makes a fresh folder: the starting files and the skill.'),
         ('run', 'transform', 'agent + model', 'Starts an agent and gives it the request.'),
         ('patch', 'change', 'patch', 'Saves what the agent changed.'),
         ('check', 'success', 'check', 'Runs the check and prints ✓ or ✘.')]
STEP_CSS = ('.steps .semantic-block{min-height:380px;padding:30px 32px 36px}.steps .semantic-block .title{font-size:34px}'
            '.steps .semantic-block .label{font-size:30px}')
framed('s07b', 'What one Vally run does', 'One run, four steps.', f'''<div class="cols steps">
    {''.join(block(c, r, t, l, step=i + 1) for i, (c, r, t, l) in enumerate(steps))}
  </div>
  <p class="lead"><span data-concept="repeat" data-rep="note">Once for each model you name, in a new workspace every time.</span></p>''', [
    {"type": "focus", "target": "ws", "at": "0", "color": "blue"},
    {"type": "focus", "target": "run", "at": "1", "color": "cyan"},
    {"type": "focus", "target": "patch", "at": "2", "color": "orange"},
    {"type": "focus", "target": "check", "at": "3", "color": "green"},
    {"type": "focus", "target": "repeat", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "check", "at": "5", "color": "green"}], css=STEP_CSS)

CMD = '''⟦cmd:vally eval⟧ ⟦e:-e evals/one-request.eval.yaml⟧ \\
  ⟦model:--model claude-haiku-4.5,gpt-5.6-terra⟧ \\
  ⟦out:--output-dir results/lesson-1⟧'''
framed('s08', 'What one Vally run does', 'One command, three flags.', f'''<div class="annotated">
    {code(CMD, 'bash')}
    {callouts(('e', 'which eval file to run'), ('model', 'which models to run it on'), ('out', 'where to save the results'))}
  </div>
  <div class="quote" data-concept="request" data-rep="quote"><span class="who">The request in one-request.eval.yaml</span><p>“{REQUEST}”</p></div>''', [
    {"type": "focus", "target": "cmd", "at": "0~vally eval", "color": "blue"},
    {"type": "focus", "target": "e", "at": "1"},
    {"type": "focus", "target": "request", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "model", "at": "5"},
    {"type": "focus", "target": "out", "at": "7"}])

framed('s08b', 'What one Vally run does', 'Safe to run, not free.', '''<table class="data-table full facts">
    <tbody>
      <tr><td><span data-concept="writes" data-rep="row">Writes</span></td><td>only inside <span class="inline-code">results/lesson-1</span></td></tr>
      <tr><td><span data-concept="spends" data-rep="row">Spends</span></td><td>one short agent session for each model, from your Copilot plan</td></tr>
      <tr><td><span class="inline-code" data-concept="error" data-rep="row">ERROR</span></td><td>the run didn’t finish, usually a dropped connection, so run it again</td></tr>
    </tbody>
  </table>''', [
    {"type": "focus", "target": "writes", "at": "0", "color": "blue"},
    {"type": "focus", "target": "spends", "at": "0~session", "color": "yellow"},
    {"type": "focus", "target": "error", "at": "1", "color": "red"}],
    css='.facts{font-size:40px}.facts td{padding-top:30px;padding-bottom:30px}.facts td:first-child{width:300px;font-weight:600}')

LIST_CMD = '''vally eval -e evals/one-request.eval.yaml \\
  --model ⟦fake:list-my-models⟧ \\
  --output-dir results/models'''
LIST_OUT = '''⟦err:ERROR⟧ typo-fix   execution error
Model "list-my-models" is not available in Copilot.
⟦avail:Available models: auto, claude-haiku-4.5,⟧
⟦avail:claude-haiku-5.5, claude-opus-5.5, …⟧'''
framed('s09', 'What one Vally run does', 'A made-up name lists your models.', f'''<div class="annotated">
    <pre class="code dark"><code>{inner(code(LIST_CMD, 'bash'))}

{inner(code(LIST_OUT, 'text'))}</code></pre>
    {callouts(('fake', 'a name no account has'), ('avail', 'the names your account does have'))}
  </div>''', [
    {"type": "focus", "target": "fake", "at": "1~a model", "color": "yellow"},
    {"type": "focus", "target": "avail", "at": "1~prints", "color": "green"},
    {"type": "focus", "target": "fake", "at": "2", "color": "yellow"}],
    css='[data-concept="err"]{color:#f26d68;font-weight:700}')

# ---- Chapter: Reading a patch ------------------------------------------------------------------
segs = [('seg-out', 'results/lesson-1/', 'the folder you named with <span class="mono">--output-dir</span>'),
        ('seg-time', f'  {RUN_FOLDER}/', 'when the command started'),
        ('seg-eval', '    one-request/', 'the eval'),
        ('seg-req', '      typo-fix/', 'the request'),
        ('seg-model', '        claude-haiku-4.5/', 'the model'),
        ('seg-run', '          0/', 'the run number, starting at 0'),
        ('seg-patch', '            workspace.patch', 'the patch: what the agent changed')]
tree = '\n'.join(re.sub(r'^(\s*)(\S.*)$', lambda m, c=c: f'{m.group(1)}⟦{c}:{m.group(2)}⟧', p) for c, p, _ in segs)
framed('s10', 'Reading a patch', 'Every run leaves a patch.', f'''<div class="annotated">
    {code(tree, 'text', 'tree')}
    {callouts(*[(c, m) for c, _, m in segs])}
  </div>''', [
    {"type": "focus", "target": "seg-patch", "at": "0~a patch", "color": "orange"},
    {"type": "focus", "target": "seg-time", "at": "2~time", "color": "blue"},
    {"type": "focus", "target": "seg-eval", "at": "3~eval"},
    {"type": "focus", "target": "seg-req", "at": "3~request"},
    {"type": "focus", "target": "seg-model", "at": "3~model"},
    {"type": "focus", "target": "seg-run", "at": "3~run number"},
    {"type": "focus", "target": "seg-patch", "at": "3~zero", "color": "orange"}],
    css='.tree{min-width:860px}')

framed('s11', 'Reading a patch', 'A patch shows only what changed.', panel('patch'), [
    {"type": "focus", "target": "file-line", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#patch", "to": "5-13", "at": "3"},
    {"type": "focus", "target": "hunk", "at": "3+0.8", "color": "blue"},
    {"type": "focus", "target": "context", "at": "5"},
    {"type": "focus", "target": "added", "at": "7", "color": "green"},
    {"type": "focus", "target": "none", "at": "10"}], layout='layout-file')

# ---- Chapter: Run it on two models ---------------------------------------------------------
framed('s12', 'Run it on two models', 'Same request, two models.', f'''<div class="cols">
    <div class="quote" data-concept="request" data-rep="quote"><span class="who">The request</span><p>“{REQUEST}”</p></div>
    <div class="quote" data-concept="ref" data-rep="quote"><span class="who">The skill says</span><p>“Reference the pull request.”</p></div>
  </div>
  <p class="lead">Neither names a pull request number. What will each model write?</p>''', [
    {"type": "focus", "target": "request", "at": "2~same request", "color": "blue"},
    {"type": "focus", "target": "ref", "at": "3~reference", "color": "yellow"}],
    css='.cols .quote{display:flex;flex-direction:column;justify-content:center;min-height:300px}')

# ---- Chapter: What the two patches show --------------------------------------------------------
framed('s17', 'What the two patches show', 'One model made up a number.',
       f'<div class="cols">{panel("pa")}{panel("pb")}</div>', [
    {"type": "focus", "target": "end-a", "at": "2", "color": "green"},
    {"type": "focus", "target": "pr42", "at": "3", "color": "red"},
    {"type": "focus", "target": "pr41", "at": "5~forty-one", "color": "blue", "channel": "prev", "until": "6"},
    {"type": "focus", "target": "none", "at": "7"}], layout='layout-file')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part"><div class="step">{i}</div>
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Makes a workspace', 'the starting files and the skill'),
    ('Runs an agent', 'on the model you named'),
    ('Saves a patch', 'of what the agent changed'),
    ('Runs the check', '✓ or ✘')], 1))
framed('s18', 'Recap', 'What does one run do?', f'''<div class="semantic-block" id="run" data-role="structure">
    <div class="title">one run</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#run", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "p3", "at": "3", "color": "orange"},
    {"type": "focus", "target": "p4", "at": "4", "color": "green"}], layout='layout-expand',
    css='#run{width:100%;padding:36px 40px 44px;gap:24px}'
        '#run .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#run .part{min-height:330px}#run .part .title{font-size:32px;line-height:1.2}#run .part .step{font-size:56px}')

scene('s19', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">What the tick checked</h1>
  <p class="lead">Both models got a green tick, yet they did different things. So what did the tick check?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Run Your First Eval”</p>
</main>''', [])
print('ok')
