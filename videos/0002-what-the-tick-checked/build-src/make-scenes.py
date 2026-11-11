"""Generate lesson 2's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lesson 1: the theme's one frame (eyebrow, short display-serif headline, .stage), code
and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing here
sets a colour or a font; a scene's own CSS is sizes and spacing only.

Everything quoted on screen is read from src/, which holds copies of the real files from the run
the lesson 1 video recorded (2026-11-11T00-11-52-424Z), with /Users/Shared/demo shown as ~/src/demo.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
RUN_FOLDER = '2026-11-11T00-11-52-424Z'


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


def card(cid, who, body):
    return f'''<div class="card" data-concept="{cid}" data-rep="card">
        <div class="who">{who}</div>
        {body}
      </div>'''


# ---- The real things, read from src/ -----------------------------------------------------------
def added_entry(patch):
    """The changelog entry a model added: the one '+- ' line of its real patch, verbatim."""
    lines = [l[1:] for l in (D / 'src' / patch).read_text().splitlines() if l.startswith('+- ')]
    assert len(lines) == 1, f'{patch}: expected one added entry, found {lines}'
    return lines[0]


entry_a, entry_b = added_entry('haiku.patch'), added_entry('terra.patch')
ref = re.search(r'\(#\d+\)\s*$', entry_b)
assert ref and not re.search(r'\(#\d+\)', entry_a), 'one entry ends with a made-up PR number, the other has none'
assert '`notes add`' in entry_a and '`notes add`' in entry_b
entry_b_pr = entry_b[:ref.start()] + '⟦pr42:' + ref.group(0).strip() + '⟧'

eval_lines = (D / 'src/one-request.eval.yaml').read_text().splitlines()
assert eval_lines[17].strip() == 'graders:' and eval_lines[22].strip() == 'value: "notes add"'
GRADER = '\n'.join(l[4:] for l in eval_lines[17:23])          # lines 18-23, dedented, otherwise verbatim

record = json.loads((D / 'src/record.json').read_text())
EVIDENCE = record['gradeResult']['details'][0]['evidence']
usage = record['trajectory']['metrics']['tokenUsage']
assert EVIDENCE == "'notes add' found in CHANGELOG.md"
assert usage['totalTokens'] == 73095 and usage['cost']['amount'] == 3361250000 and usage['callCount'] == 6


def report_rows():
    """Each model's row of the real report (src/eval-results.md), as the columns the video shows."""
    md = (D / 'src/eval-results.md').read_text()
    out = []
    for head, row in re.findall(r'^### (one-request \[[^\]]+\]).*?\n(\| typo-fix .*?)$', md, re.S | re.M):
        c = [x.strip() for x in row.strip().strip('|').split('|')]
        assert len(c) == 10, c
        calls = re.search(r'<summary>([^<]+)</summary>', c[8]).group(1)
        out.append(dict(head=head, stimulus=c[0], graders=c[3].replace('✅', '✔'), rate=c[4], duration=c[5],
                        tokens=c[6], calls=calls, verdict=c[9].replace('✅', '✔')))
    assert [r['tokens'] for r in out] == ['74,210', '73,095'], out
    return out


ROWS = report_rows()
assert ROWS[1]['tokens'].replace(',', '') == str(usage['totalTokens'])


def th(cid, text, num=True):
    return f'<th{" class=\"num\"" if num else ""}><span data-concept="{cid}" data-rep="head">{text}</span></th>'


def td(cid, text, num=True, cls=''):
    c = ' '.join(x for x in ('num' if num else '', cls) if x)
    return f'<td{" class=\"" + c + "\"" if c else ""}><span data-concept="{cid}" data-rep="cell">{text}</span></td>'


def report_table():
    body = ''
    for key, r in zip('ab', ROWS):
        body += f'<tr class="grp"><td colspan="7">{r["head"]}</td></tr>\n<tr><td class="mono">{r["stimulus"]}</td>'
        body += td('c-graders', r['graders'], num=False, cls='mono') + td('c-rate', r['rate'])
        body += f'<td class="num">{r["duration"]}</td>' + td(f'tok-{key}', r['tokens'])
        body += td('c-calls', r['calls']) + td('c-verdict', r['verdict'], cls='tick') + '</tr>\n'
    return f'''<table class="data-table full rep">
    <thead><tr><th>Stimulus</th>{th('c-graders', 'Graders', num=False)}{th('c-rate', 'Pass Rate')}<th class="num">Duration</th>{th('c-tokens', 'Tokens')}{th('c-calls', 'Tool Calls')}{th('c-verdict', 'Verdict')}</tr></thead>
    <tbody>
{body}    </tbody>
  </table>
  <p class="note"><span class="mono">eval-results.md</span> · 3 columns hidden: Environment, Skills, Turns</p>'''


REP_CSS = ('.rep{font-size:32px}.rep th{font-size:28px}.rep td,.rep th{padding:18px 14px}'
           '.rep .grp td{font:600 30px/1.3 var(--font-code);color:var(--ink);padding-top:34px;border-bottom:0}'
           '.rep td.tick,.s-tick{color:var(--green-ink);font-weight:700}.rep td.mono{font-family:var(--font-code)}')

# ---- Hook ----------------------------------------------------------------------------------------
TICK = '<span class="s-tick" data-concept="tick" data-rep="mark">✔</span>'
framed('s01', 'Vally &amp; Agent Evals', 'What the tick checked', f'''<div class="results">
      {card('card-a', f'{TICK} <span class="mono">claude-haiku-4.5</span>', code(entry_a, 'markdown'))}
      {card('card-b', f'{TICK} <span class="mono">gpt-5.6-terra</span>', code(entry_b_pr, 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "card-a", "at": "0~Two models", "color": "blue"},
    {"type": "focus", "target": "card-b", "at": "0~two different", "color": "blue"},
    {"type": "focus", "target": "pr42", "at": "1~pull request", "color": "yellow"},
    {"type": "focus", "target": "tick", "at": "1~green tick", "color": "green"},
    {"type": "focus", "target": "none", "at": "2"}],
    h='h1', title_class='scene-title chapter',
    css='.results{display:flex;flex-direction:column;gap:36px;width:100%}.results{gap:48px}.results .card > .code.dark{font-size:40px;padding:30px 36px}.results .card .who{font-size:34px}'
        '.s-tick{color:var(--green-ink);font-weight:700}')

# ---- Chapter: Read the eval file -----------------------------------------------------------------
framed('s02', 'Read the eval file', 'What the agent starts with.', f'''<div class="annotated">
    {panel('eval')}
    {callouts(('name', 'the folder name for its results'), ('timeout', 'how long the agent may take'),
              ('agentenv', 'what the agent starts with'), ('skill', 'a skill to install'),
              ('file', 'a file to copy in, and its name in the workspace'))}
  </div>''', [
    {"type": "focus", "target": "name", "at": "1~name", "color": "blue"},
    {"type": "focus", "target": "timeout", "at": "2~three minutes"},
    {"type": "scroll", "target": "#eval", "to": "6-11", "at": "3"},
    {"type": "focus", "target": "agentenv", "at": "3~agent environment", "color": "blue"},
    {"type": "focus", "target": "skill", "at": "5~skill folder"},
    {"type": "focus", "target": "file", "at": "6~file to copy"}], layout='layout-file')

framed('s03', 'Read the eval file', 'One request, one grader.', f'''<div class="annotated">
    {panel('eval')}
    {callouts(('stimuli', 'the things to try'), ('stim', 'one stimulus'), ('prompt', 'the request, word for word'),
              ('graders', 'its checks'), ('gtype', 'a built-in grader'), ('gname', 'our name for it'),
              ('path', 'the file it opens'), ('value', 'the text it looks for'))}
  </div>''', [
    {"type": "scroll", "target": "#eval", "to": "6-11", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#eval", "to": "13-17", "at": "0+0.6"},
    {"type": "focus", "target": "stimuli", "at": "0~stimuli", "color": "blue"},
    {"type": "focus", "target": "stim", "at": "1~stimulus", "color": "blue"},
    {"type": "focus", "target": "prompt", "at": "3", "color": "yellow"},
    {"type": "scroll", "target": "#eval", "to": "18-23", "at": "4"},
    {"type": "focus", "target": "graders", "at": "4~graders", "color": "blue"},
    {"type": "focus", "target": "gtype", "at": "7~type"},
    {"type": "focus", "target": "path", "at": "9~one file"},
    {"type": "focus", "target": "value", "at": "9~text in value", "color": "yellow"},
    {"type": "focus", "target": "gname", "at": "11"}], layout='layout-file')

LINT = '⟦cmd:vally lint⟧ ⟦e:-e evals/one-request.eval.yaml⟧'
framed('s04', 'Read the eval file', 'Lint checks the file for free.', f'''<div class="annotated">
    {code(LINT, 'bash')}
    {callouts(('cmd', 'reports mistakes in an eval file'))}
  </div>
  <p class="lead"><span data-concept="free" data-rep="note">It starts no agent, so it spends nothing.</span></p>''', [
    {"type": "focus", "target": "cmd", "at": "0~vally lint", "color": "blue"},
    {"type": "focus", "target": "e", "at": "2~dash e"},
    {"type": "focus", "target": "free", "at": "2~spends nothing", "color": "green"}],
    css='.annotated .code.dark{font-size:44px;padding:36px 40px}.callout{font-size:36px}.lead{font-size:42px;margin-top:36px}')

# ---- Chapter: What a run leaves behind -----------------------------------------------------------
framed('s05', 'What a run leaves behind', 'One attempt is a trial.', f'''<div class="cols terms">
    {block("stim", "structure", "stimulus", '<span class="names">typo-fix</span>one request and its graders')}
    {block("trial", "transform", "trial", '<span class="names">typo-fix</span>on <span class="mono">claude-haiku-4.5</span>')}
    {block("trial", "transform", "trial", '<span class="names">typo-fix</span>on <span class="mono">gpt-5.6-terra</span>')}
  </div>
  <p class="lead"><span data-concept="run" data-rep="note">One run: one <span class="inline-code">vally eval</span> command, and everything it saves.</span></p>''', [
    {"type": "focus", "target": "trial", "at": "1~a trial", "color": "cyan"},
    {"type": "focus", "target": "stim", "at": "2~one stimulus", "color": "blue"},
    {"type": "focus", "target": "trial", "at": "2~two trials", "color": "cyan"},
    {"type": "focus", "target": "run", "at": "3~a run", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px}'
        '.names{display:block;margin-bottom:10px;font:500 32px/1.4 var(--font-code);color:var(--ink)}')

segs = [('seg-time', f'{RUN_FOLDER}/', 'when the run started'),
        ('seg-report', '  eval-results.md', 'the report, for people'),
        ('seg-results', '  results.jsonl', 'the same, for programs'),
        ('seg-otel', '  otel-spans.jsonl', 'timing data, not used here'),
        ('seg-eval', '  one-request/', 'the eval'),
        ('seg-stim', '    typo-fix/', 'the stimulus'),
        ('seg-model', '      claude-haiku-4.5/', 'the model'),
        ('seg-num', '        0/', 'the trial number, from 0'),
        ('seg-patch', '          workspace.patch', 'what the agent changed'),
        ('seg-events', '          events.jsonl', 'the agent’s own log'),
        ('seg-meta', '          metadata.json', 'facts about the trial'),
        ('seg-other', '      gpt-5.6-terra/0/', 'the same three files')]
tree = '\n'.join(re.sub(r'^(\s*)(\S.*)$', lambda m, c=c: f'{m.group(1)}⟦{c}:{m.group(2)}⟧', p) for c, p, _ in segs)
TREE_CSS = '.code.dark.tree{min-width:820px;font-size:30px;line-height:1.6;padding-top:14px;padding-bottom:14px}.callout{font-size:28px}.stage{justify-content:flex-start}'
framed('s06', 'What a run leaves behind', 'One run, one folder.', f'''<div class="annotated">
    {code(tree, 'text', 'tree')}
    {callouts(*[(c, m) for c, _, m in segs])}
  </div>''', [
    {"type": "focus", "target": "seg-time", "at": "0~named", "color": "blue"},
    {"type": "focus", "target": "seg-report", "at": "1~eval results"},
    {"type": "focus", "target": "seg-results", "at": "2"},
    {"type": "focus", "target": "seg-otel", "at": "3"},
    {"type": "focus", "target": "seg-eval", "at": "4~eval"},
    {"type": "focus", "target": "seg-stim", "at": "4~stimulus"},
    {"type": "focus", "target": "seg-model", "at": "4~model"},
    {"type": "focus", "target": "seg-num", "at": "4~trial number"},
    {"type": "focus", "target": "seg-patch", "at": "6", "color": "orange"},
    {"type": "focus", "target": "seg-events", "at": "7"},
    {"type": "focus", "target": "seg-meta", "at": "8"}], css=TREE_CSS)

framed('s07', 'What a run leaves behind', 'One row for each stimulus.', report_table(), [
    {"type": "focus", "target": "c-graders", "at": "1~graders", "color": "blue"},
    {"type": "focus", "target": "c-rate", "at": "2"},
    {"type": "focus", "target": "c-calls", "at": "3"},
    {"type": "focus", "target": "c-verdict", "at": "4~verdict", "color": "green"},
    {"type": "focus", "target": "c-tokens", "at": "5~tokens", "color": "yellow"}], css=REP_CSS)

framed('s08', 'What a run leaves behind', 'One record for each trial.', f'''<div class="annotated">
    {panel('record')}
    {callouts(('rtype', 'the kind of record'), ('status', 'the agent finished'))}
  </div>''', [
    {"type": "focus", "target": "rtype", "at": "2", "color": "blue"},
    {"type": "focus", "target": "status", "at": "3", "color": "yellow"}], layout='layout-file')

framed('s09', 'What a run leaves behind', 'The evidence behind the tick.', f'''<div class="annotated">
    {panel('record')}
    {callouts(('passed', 'the trial’s verdict'), ('details', 'one per grader'),
              ('evidence', 'what it found'), ('traj', 'all the agent did'))}
  </div>''', [
    {"type": "scroll", "target": "#record", "to": "top", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#record", "to": "12-19", "at": "0+0.6"},
    {"type": "focus", "target": "grade", "at": "0~grade result", "color": "blue"},
    {"type": "focus", "target": "passed", "at": "1", "color": "green"},
    {"type": "focus", "target": "details", "at": "2"},
    {"type": "scroll", "target": "#record", "to": "20-26", "at": "3"},
    {"type": "focus", "target": "evidence", "at": "3~evidence", "color": "green"},
    {"type": "scroll", "target": "#record", "to": "32-35", "at": "4"},
    {"type": "focus", "target": "traj", "at": "4~trajectory", "color": "blue"}], layout='layout-file')

# ---- Chapter: What a trial used ------------------------------------------------------------------
framed('s10', 'What a trial used', 'Each call reads it all again.', f'''<div class="annotated">
    {panel('record')}
    {callouts(('input', 'all it was given'), ('output', 'all it wrote'), ('total', 'input + output'),
              ('cacheread', 'already processed'), ('calls', 'model calls'))}
  </div>''', [
    {"type": "scroll", "target": "#record", "to": "32-35", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#record", "to": "559-566", "at": "0+0.6"},
    {"type": "focus", "target": "usage", "at": "2", "color": "blue"},
    {"type": "focus", "target": "input", "at": "3"},
    {"type": "focus", "target": "output", "at": "4"},
    {"type": "focus", "target": "calls", "at": "5~call count", "color": "yellow"},
    {"type": "focus", "target": "cacheread", "at": "6"},
    {"type": "focus", "target": "total", "at": "7", "color": "green"}], layout='layout-file')

framed('s11', 'What a trial used', 'This trial cost three cents.', f'''<div class="annotated">
    {panel('record')}
    {callouts(('provider', 'from Copilot'), ('unit', 'a billionth of an AIU'), ('amount', 'this trial'))}
  </div>
  <div class="conv"><p><span data-concept="r1" data-rep="note">1 AIU</span> = <span data-concept="r2" data-rep="note">1 AI Credit</span> = <span data-concept="r3" data-rep="note">1 cent</span></p>
    <p><span data-concept="c1" data-rep="note">3,361,250,000 nano-AIU</span> = 3.36 AIU ≈ <span data-concept="c4" data-rep="note">3 cents</span></p></div>''', [
    {"type": "scroll", "target": "#record", "to": "574-578", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "provider", "at": "0~GitHub Copilot", "color": "blue"},
    {"type": "focus", "target": "unit", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "r1", "at": "2"},
    {"type": "focus", "target": "r2", "at": "2~AI Credit"},
    {"type": "focus", "target": "r3", "at": "3~one cent", "color": "green"},
    {"type": "focus", "target": "amount", "at": "4"},
    {"type": "focus", "target": "c1", "at": "4~billion"},
    {"type": "focus", "target": "c4", "at": "4~three cents", "color": "green"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file',
    css='.conv{display:flex;gap:90px;margin-top:24px;width:100%}.conv p{margin:0;font:500 34px/1.4 var(--font-code);color:var(--ink);white-space:nowrap}')

framed('s12', 'What a trial used', 'The same total, in the report.', report_table(), [
    {"type": "focus", "target": "tok-b", "at": "0~total", "color": "yellow"},
    {"type": "focus", "target": "c-tokens", "at": "1~median"},
    {"type": "focus", "target": "none", "at": "2"}], css=REP_CSS)

# ---- Chapter: Why both models passed -------------------------------------------------------------
na = lambda e: e.replace('`notes add`', '⟦na:`notes add`⟧')
framed('s13', 'Why both models passed', 'It looked for two words.', f'''<div class="cols pair">
    {card('g', 'The grader, in the eval file', code(GRADER.replace('"notes add"', '⟦value:"notes add"⟧'), 'yaml'))}
    {card('e', 'Its evidence, in <span class="mono">results.jsonl</span>', code('⟦ev:' + EVIDENCE + '⟧', 'text'))}
  </div>
  <div class="entries">
    {card('ea', '<span class="mono">claude-haiku-4.5</span> wrote', code(na(entry_a), 'markdown'))}
    {card('eb', '<span class="mono">gpt-5.6-terra</span> wrote', code(na(entry_b_pr), 'markdown'))}
  </div>''', [
    {"type": "focus", "target": "value", "at": "2~notes add", "color": "yellow"},
    {"type": "focus", "target": "ev", "at": "3~evidence", "color": "green"},
    {"type": "focus", "target": "na", "at": "4~mentions", "color": "green"},
    {"type": "focus", "target": "pr42", "at": "5~pull request", "color": "yellow"}],
    css='.stage{gap:26px}.pair{align-items:start}.card > .code.dark{font-size:30px;line-height:1.4;padding:16px 22px}'
        '.entries{display:flex;flex-direction:column;gap:18px;width:100%}.card .who{font-size:28px}')

framed('s14', 'Why both models passed', 'A pass means no objection.', f'''<div class="cols wide terms">
    {block("yes", "success", "None of my graders objected.", "what a pass tells you", words=True)}
    {block("no", "failure", "This is correct.", "what it doesn’t tell you", words=True)}
  </div>
  <p class="lead"><span data-concept="one" data-rep="note">So far: one grader, written before anyone had read a run.</span></p>''', [
    {"type": "focus", "target": "yes", "at": "2~none", "color": "green"},
    {"type": "focus", "target": "no", "at": "2~doesn't mean", "color": "red"},
    {"type": "focus", "target": "yes", "at": "3", "color": "green"},
    {"type": "focus", "target": "one", "at": "4~one grader", "color": "yellow"}],
    css='.terms .semantic-block{min-height:260px}.terms .label{font-size:32px}')


def cells(first, rest):
    out = f'<td class="num seen"><span data-concept="seen" data-rep="cell">{first}</span></td>'
    return out + ''.join(f'<td class="num"><span data-concept="{c}" data-rep="cell">?</span></td>' for c in rest)


framed('s15', 'Why both models passed', 'Two trials are not enough.', f'''<table class="data-table full grid">
    <thead><tr><th></th><th class="num">this request, trial 0</th><th class="num">the next trial</th><th class="num">other requests</th></tr></thead>
    <tbody>
      <tr><td class="mono">claude-haiku-4.5</td>{cells('no number', ('again', 'other'))}</tr>
      <tr><td class="mono">gpt-5.6-terra</td>{cells('(#42)', ('again', 'other'))}</tr>
    </tbody>
  </table>''', [
    {"type": "focus", "target": "seen", "at": "1~two trials", "color": "blue"},
    {"type": "focus", "target": "again", "at": "2~always", "color": "yellow"},
    {"type": "focus", "target": "other", "at": "2~other requests", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.grid{font-size:40px}.grid th{font-size:30px}.grid td{padding-top:34px;padding-bottom:34px}'
        '.grid td.mono{font-family:var(--font-code);font-size:34px}.grid td.num{color:var(--ink-muted)}'
        '.grid td.seen{color:var(--ink);font-family:var(--font-code);font-size:34px}')

# ---- Chapter: Find it in the files ---------------------------------------------------------------
framed('s16', 'Find it in the files', 'From the tick to its evidence.', f'''<div class="cols wide terms">
    {block("tickb", "success", "✔ typo-fix", 'a tick for each model')}
    {block("folder", "structure", "results/lesson-1", "the folder our run was saved in")}
  </div>
  <p class="lead"><span data-concept="free" data-rep="note">No agent starts. Nothing is spent.</span></p>''', [
    {"type": "focus", "target": "tickb", "at": "0", "color": "green"},
    {"type": "focus", "target": "folder", "at": "0~results folder", "color": "blue"},
    {"type": "focus", "target": "free", "at": "2", "color": "yellow"}],
    css='.terms .semantic-block{min-height:260px}.terms .title{font-family:var(--font-code);font-size:40px}')

framed('s18', 'Find it in the files', 'A few facts about one trial.', f'''<div class="annotated">
    {panel('meta')}
    {callouts(('model', 'which model'), ('status', 'the agent finished'))}
  </div>''', [
    {"type": "scroll", "target": "#meta", "to": "8-11", "at": "1"},
    {"type": "focus", "target": "model", "at": "1+0.9", "color": "blue"},
    {"type": "focus", "target": "status", "at": "2", "color": "green"},
    {"type": "focus", "target": "none", "at": "3"}], layout='layout-file')

GRADER_Q = GRADER.replace('path: CHANGELOG.md', 'path: ⟦path:CHANGELOG.md⟧').replace('"notes add"', '⟦value:"notes add"⟧')
framed('s19', 'Find it in the files', 'Would this grader pass it?', f'''<div class="cols pair">
    {card('g', 'The only grader', code(GRADER_Q, 'yaml'))}
    <div class="cases">
      {block("case2", "structure", "The entry, under the released 1.2.0 section", "", words=True)}
      {block("case3", "structure", "Nothing changed at all", "", words=True)}
    </div>
  </div>''', [
    {"type": "focus", "target": "path", "at": "2~changelog", "color": "blue"},
    {"type": "focus", "target": "value", "at": "2~notes add", "color": "yellow"},
    {"type": "focus", "target": "case2", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "case2", "at": "4", "color": "green"},
    {"type": "focus", "target": "case3", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "case3", "at": "6", "color": "red"}],
    css='.pair{align-items:stretch}.cases{display:flex;flex-direction:column;gap:28px;justify-content:center}'
        '.cases .semantic-block{min-height:150px;justify-content:center}.cases .label{display:none}'
        '.card > .code.dark{font-size:32px}')

framed('s20', 'Find it in the files', 'Which model used more tokens?', report_table(), [
    {"type": "focus", "target": "c-tokens", "at": "1~tokens column", "color": "blue"},
    {"type": "focus", "target": "tok-a", "at": "1~haiku", "color": "green"},
    {"type": "focus", "target": "none", "at": "2"}], css=REP_CSS)

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part"><div class="step">{i}</div>
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Its request', 'the prompt of a stimulus, in the eval file'),
    ('Its changes', '<span class="mono">workspace.patch</span>'),
    ('Its verdict', 'the report; the evidence is in <span class="mono">results.jsonl</span>'),
    ('Its tokens', 'the report’s Tokens column; detail in <span class="mono">results.jsonl</span>')], 1))
framed('s21', 'Recap', 'Where would you look?', f'''<div class="semantic-block" id="trial" data-role="structure">
    <div class="title">any trial</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#trial", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "orange"},
    {"type": "focus", "target": "p3", "at": "3", "color": "green"},
    {"type": "focus", "target": "p4", "at": "4", "color": "yellow"}], layout='layout-expand',
    css='#trial{width:100%;padding:36px 40px 44px;gap:24px}'
        '#trial .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#trial .part{min-height:330px}#trial .part .title{font-size:32px;line-height:1.2}#trial .part .step{font-size:56px}'
        '#trial .part .label{font-size:28px}')

scene('s22', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">The same request, five times</h1>
  <p class="lead">Each model ran once. Would it do the same thing next time?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Eval Spec reference” and “Trajectory Format”</p>
</main>''', [])
print('ok')
