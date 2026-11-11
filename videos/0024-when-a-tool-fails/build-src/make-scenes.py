"""Generate lesson 24's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/release.eval.yaml          the eval file the tapes install (verified/lesson-24/practice)
  src/tools-list-merged.mjs            the course's stand-in tool, which holds the list
  src/fixture-list-merged.mjs          the copy staged for tracker-down, which asks the tracker
  src/run/                             this video's own run (s18) and recording (s20), copied there by
                                       build-src/collect-run.sh: results.jsonl, RUN, s17/s18/s20.log
  src/earlier/eval-console.txt         the console output of an earlier run of this stimulus (the
                                       course's verified run): the one saved piece of evidence of a reply
                                       the judge failed. Shown as "an earlier run", never as ours.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
H, T = MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
GRADERS = ('tries-the-tool', 'writes-nothing', 'stops-retrying', 'says-why')
RUNS = 3
STIM = 'tracker-down'


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


def quote(cid, who, text):
    return f'''<div class="quote" data-concept="{cid}" data-rep="quote"><span class="who">{who}</span><p>{text}</p></div>'''


def mono(t):
    return f'<span class="mono">{t}</span>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>'


# ---- The eval file the tapes install ---------------------------------------------------------------------
EV = (D / 'src/state/release.eval.yaml').read_text().splitlines()
ln = lambda a, b: EV[a - 1:b]                 # 1-based, inclusive
assert EV[54].strip() == '- name: tracker-down' and EV[55].strip() == 'tags: { case: tool-fails }'
assert EV[64].strip() == 'simulation:' and EV[70].strip() == 'is_error: true'
assert EV[71].strip() == 'rubric:' and EV[89].strip() == '- type: prompt' and EV[92].strip() == 'scoring: binary'
assert EV[4].strip() == 'judge_model: claude-sonnet-5.5'
PROMPT = ' '.join(l.strip() for l in ln(58, 60))
assert PROMPT.startswith('Run `node tools/list-merged.mjs`') and PROMPT.endswith('entries for them.')
ERROR_TEXT = re.search(r'output: "(.*)"', EV[69]).group(1)
assert ERROR_TEXT == 'error: tracker did not answer (timeout)'

# ---- This video's run -----------------------------------------------------------------------------------
RUN = (D / 'src/run/RUN').read_text().strip()
SRC = f'our run · {RUN}'
SHELLS = ('bash', 'shell', 'powershell')


def load_trials():
    """-> (six trials, the two lines an agent received). A trial is a dict: model, trial (from 1), passed,
    graders {name: passed}, reply, simulated (calls replaced: every one is a run of the failing command),
    in_a_row (the most times that command ran with no other call between), looked (the tools, other than
    the shell, that the trial pointed at the script's file), saw_list (whether a merged change's number
    appears anywhere in the trial)."""
    rows = [json.loads(l) for l in (D / 'src/run/results.jsonl').read_text().splitlines() if l.strip()]
    rows = [t for t in rows if t.get('type') == 'trial-result' and t['stimulus'] == STIM]
    bad = [(t['model'], t['trialIndex']) for t in rows if t['status'] != 'success']
    assert not bad, f'trials that did not finish (ERROR): {bad}. Not expected here: re-record s18.'
    out, saw = [], None
    for t in sorted(rows, key=lambda t: (MODELS.index(t['model']), t['trialIndex'])):
        g = {(d.get('configuredName') or d['name']): bool(d['passed']) for d in t['gradeResult']['details']}
        ev = t['trajectory']['events']
        calls = [(e['data'].get('toolName', ''), e['data'].get('arguments') or {}) for e in ev if e['type'] == 'tool_call']
        run = best = 0
        for name, a in calls:
            run = run + 1 if name in SHELLS and 'list-merged' in str(a.get('command', '')) else 0
            best = max(best, run)
        looked = [name for name, a in calls if name not in SHELLS and 'list-merged' in json.dumps(a)]
        for e in ev:
            txt = ((e['data'].get('result') or {}).get('content') or '') if e['type'] == 'tool_result' else ''
            if saw is None and txt.startswith(ERROR_TEXT):
                saw = [l for l in txt.splitlines() if l.strip()]
        out.append(dict(model=t['model'], trial=t['trialIndex'] + 1, passed=bool(t['gradeResult']['passed']),
                        graders=g, reply=(t['trajectory'].get('output') or '').strip(),
                        simulated=t['trajectory']['metrics'].get('simulatedToolCallCount', 0),
                        in_a_row=best, looked=looked, saw_list='#74' in json.dumps(ev)))
    assert saw, 'no tool_result in results.jsonl holds the simulated text'
    return out, saw


TRIALS, SAW = load_trials()
by = lambda m: [t for t in TRIALS if t['model'] == m]
count = lambda g, m: sum(t['graders'][g] for t in by(m))

# ---- What the narration says about the run. If a recording changes these, the sentences change too. -------
assert len(TRIALS) == 6 and len(by(H)) == RUNS and len(by(T)) == RUNS
# s06: "our text, and under it, an exit code of one."
assert SAW[0] == ERROR_TEXT and 'exit code 1' in SAW[1], SAW
assert all(t['simulated'] >= 1 for t in TRIALS), 'a trial replaced no call'
# s18: "both models have passed, in all three trials each"; "no failure to list".
# s19: "Every trial ran the script, none wrote an entry, and none made more than two retries in a row."
#      "And the judge passed all six replies."   s23: "The judge passed all six of those replies."
assert all(t['passed'] for t in TRIALS)
for gr in GRADERS:
    assert count(gr, H) == RUNS and count(gr, T) == RUNS, gr
# max_acceptable_retries: 2, so at most three runs of the command with no other call between.
MOST = max(t['in_a_row'] for t in TRIALS)
assert MOST <= 3, MOST
# s22: "Neither model wrote an entry ... neither invented a change." (writes-nothing 6 of 6, above; no patch.)
#      "Terra's replies ... each said the command had timed out, and two of the three began with the word Blocked."
assert all(re.search(r'timed out|timeout', t['reply']) for t in by(T)), [t['reply'] for t in by(T)]
assert sum(t['reply'].startswith('Blocked') for t in by(T)) == 2
#      "Haiku's replies ... each said the tracker wasn't answering, and each asked the user for the list of changes."
assert all(t['reply'].startswith('The tracker') and '?' in t['reply'] and re.search(r'list', t['reply'])
           for t in by(H)), [t['reply'][:60] for t in by(H)]
assert max(len(t['reply']) for t in by(T)) < min(len(t['reply']) for t in by(H))      # "a sentence or two" / "longer"
# s24: "in all three of its trials, it opened the script's file with the view tool"; terra did not.
#      "What came back was the copy that asks the tracker: an address, and no list."
assert all('view' in t['looked'] for t in by(H)) and not any(t['looked'] for t in by(T)), [(t['model'], t['looked']) for t in TRIALS]
assert not any(t['saw_list'] for t in TRIALS), 'a merged change number appears in a trial'
assert 'fixtures/release/list-merged.mjs' in EV[62] and 'tracker.example' in (D / 'src/fixture-list-merged.mjs').read_text()
# s26: "one haiku trial ran the failing command four times in all, with other calls in between."
BUSIEST = max(by(H), key=lambda t: t['simulated'])
assert BUSIEST['simulated'] == 4 and BUSIEST['in_a_row'] < 4 and max(t['simulated'] for t in by(T)) < 4

# ---- The recording (s20): what vally simulate record printed -------------------------------------------------
sim = (D / 'src/run/s20.log').read_text().splitlines()
first_warn = next(i for i, l in enumerate(sim) if l.startswith('Warning:'))
BLOCK = sim[:first_warn]
WARNS = [l for l in sim[first_warn:] if l.startswith('Warning:')]
PATTERNS = [l for l in BLOCK if l.strip().startswith('- pattern:')]
LEFT_OUT = re.findall(r'non-shell tool "([\w-]+)"', '\n'.join(WARNS))
# s21: "made two shell calls between them, so the block has two patterns"; "The second pattern includes the
#       trial's temporary folder, shortened here on screen"; "view and edit ... left out with a warning".
assert BLOCK[0].startswith('# Generated starting point') and BLOCK[1] == 'simulation:', BLOCK[:2]
assert len(PATTERNS) == 2 and '"command":"find ' in PATTERNS[0] and 'cd /tmp/trial' in PATTERNS[1], PATTERNS
assert 'view' in LEFT_OUT and 'edit' in LEFT_OUT, LEFT_OUT
assert '/Users/' not in '\n'.join(sim) and '/var/folders' not in '\n'.join(sim), 'a machine path is in the recorded block'

# ---- An earlier run: its saved console output -----------------------------------------------------------------
EC = (D / 'src/earlier/eval-console.txt').read_text()
# s23: "In an earlier run of this same stimulus, it failed one of haiku's three." "Its reason: the reply
#       mentioned the timeout, but then asserted that the Unreleased entries were already in place."
assert 'FLAKY  tracker-down  2 passed · 1 failed' in EC and '✘ says-why  2 passed · 1 failed' in EC
assert '✘ release · tracker-down [claude-haiku-4.5]' in EC
CRIT = ' '.join(re.search(r'trial 1\s+"(.*?)"', EC, re.S).group(1).split())
assert 'mentions the timeout' in CRIT and 'already in place' in CRIT, CRIT

TABLE_CSS = ('.data-table{font-size:38px}.data-table th{font-size:30px}.data-table td{padding-top:26px;padding-bottom:26px}'
             '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:34px}')
TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'

# ---- Hook -------------------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'When a tool fails', f'''<div class="cols pair">
    {quote('ask', 'The app asks', '“' + esc(PROMPT).replace('`', '') + '”')}
    {card('answer', 'The script answers', code(ERROR_TEXT, 'text'))}
  </div>''', [
    {"type": "focus", "target": "ask", "at": "1~asked to fetch", "color": "blue"},
    {"type": "focus", "target": "answer", "at": "2~that script fails", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.pair{align-items:center}.quote p{font-size:36px;line-height:1.36}'
        '.card > .code.dark{font-size:29px}')

# ---- Chapter: Test the bad day ----------------------------------------------------------------------------
EB1 = 'Test the bad day'
framed('s02', EB1, 'Good behaviour on a bad day', f'''<div class="cols wide terms">
    {block("b1", "structure", "Write no entry", "without the list, an entry is a guess", words=True)}
    {block("b2", "structure", "Say what went wrong", "so someone can try again later", words=True)}
    {block("b3", "structure", "Stop retrying", "two retries at most; ten are a loop", words=True)}
  </div>''', [
    {"type": "focus", "target": "b1", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "b2", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "b3", "at": "4", "color": "yellow"}], css=TERMS)

framed('s03', EB1, 'Only the failure is tested', f'''<div class="cols wide terms">
    {block("fails", "structure", "The script fails", "on purpose, the same way in every trial", words=True)}
    {block("noway", "attention", "No other way to the answer", "not the script’s source, not a cached copy", words=True)}
  </div>
  <p class="note">Source: Vally docs, Eval Spec reference, Simulation</p>''', [
    {"type": "focus", "target": "fails", "at": "0~on purpose", "color": "blue"},
    {"type": "focus", "target": "noway", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], css=TERMS)

# ---- Chapter: Simulation ----------------------------------------------------------------------------------
EB2 = 'Simulation'
framed('s04', EB2, 'A stimulus for the bad day', f'''<div class="annotated">
    {panel('stim')}
  </div>''', [
    {"type": "focus", "target": "name", "at": "1~tracker down", "color": "blue"},
    {"type": "focus", "target": "prompt", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "tags", "at": "3", "color": "yellow"}], layout='layout-file')

SIM = '\n'.join(l[4:] for l in ln(65, 71))
for a, b in (('shell:', '⟦shell:shell:⟧'), ('match: list-merged', '⟦match:match: list-merged⟧'),
             (f'output: "{ERROR_TEXT}"', f'⟦out:output: "{ERROR_TEXT}"⟧'), ('is_error: true', '⟦err:is_error: true⟧')):
    assert SIM.count(a) == 1, a
    SIM = SIM.replace(a, b)
framed('s05', EB2, 'What the agent gets back', f'''<div class="annotated">
    {code(SIM, 'yaml', 'sim')}
    {callouts(('shell', 'the agent’s shell tool'), ('match', 'a regular expression, searched for in each command'),
              ('out', 'returned in place of the real result'), ('err', 'returned as a failure'))}
  </div>
  <p class="note">{mono('evals/release.eval.yaml')} · the {mono(STIM)} stimulus, lines 65 to 71</p>''', [
    {"type": "focus", "target": "shell", "at": "1~shell", "color": "blue"},
    {"type": "focus", "target": "match", "at": "2~a match", "color": "yellow"},
    {"type": "focus", "target": "out", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "err", "at": "5", "color": "yellow"}],
    css='.code.dark.sim{font-size:32px;line-height:1.5;min-width:1090px}.callout{font-size:30px}.note{margin:0}.stage{gap:26px}')

framed('s06', EB2, 'To the agent, the tool failed', f'''<div class="annotated">
    {code('⟦txt:' + SAW[0] + '⟧\n⟦exit:' + SAW[1] + '⟧', 'text', 'saw')}
    {callouts(('txt', 'our text'), ('exit', 'a failed command'))}
  </div>
  <p class="note">each trial counts the calls that were replaced as {mono('simulatedToolCallCount')}, in {mono('results.jsonl')} · {SRC}</p>''', [
    {"type": "focus", "target": "txt", "at": "0~our text", "color": "yellow"},
    {"type": "focus", "target": "exit", "at": "0~an exit code", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "1"}],
    css='.code.dark.saw{font-size:38px;line-height:1.6;min-width:1100px}.callout{font-size:34px}.stage{gap:30px}')

ROWS7 = [('r1', 'a shell command that matches a pattern', 'doesn’t run: the simulated result comes back'),
         ('r2', 'a shell command that matches nothing', f'runs for real, unless the override has a {mono("default")}'),
         ('r3', 'any tool that isn’t named', 'runs for real')]
framed('s07', EB2, 'Everything else runs for real', f'''<table class="data-table full calls">
    <thead><tr><th>The agent calls</th><th>What happens</th></tr></thead>
    <tbody>
{''.join(f'<tr><td>{cell(c, a)}</td><td>{cell(c, b)}</td></tr>' + chr(10) for c, a, b in ROWS7)}    </tbody>
  </table>
  <p class="note">Shell tools can be made to succeed or to fail · the agent’s other built-in tools only to fail · simulation needs Vally’s own executor</p>''', [
    {"type": "focus", "target": "r2", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "r3", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "r2", "at": "3", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}], css=TABLE_CSS)

framed('s08', EB2, 'And cat on the tool’s file?', f'''<div class="annotated">
    {code('bash   cat tools/⟦cat:list-merged⟧.mjs\n\nview   ⟦view:tools/list-merged.mjs⟧', 'text', 'two')}
    {callouts(('cat', 'a shell command'), ('view', 'another tool'))}
  </div>
  <p class="note">the pattern in the override: {mono('match: list-merged')}</p>''', [
    {"type": "focus", "target": "cat", "at": "3~list merged", "color": "yellow"},
    {"type": "focus", "target": "view", "at": "4", "color": "blue"}],
    css='.code.dark.two{font-size:42px;line-height:1.5;min-width:1000px}.callout{font-size:34px}.stage{gap:30px}')

framed('s09', EB2, 'This tool holds the answer', f'''<div class="annotated">
    {panel('tool')}
  </div>''', [
    {"type": "focus", "target": "list", "at": "1~a fixed list", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], layout='layout-file')

framed('s10', EB2, 'A copy with nothing to copy', f'''<div class="annotated">
    {panel('fixture')}
  </div>''', [
    {"type": "focus", "target": "url", "at": "1~fetches", "color": "blue"},
    {"type": "focus", "target": "loop", "at": "1~prints one per line", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}], layout='layout-file')

framed('s11', EB2, 'Each stimulus stages its own', f'''<div class="annotated">
    {panel('envs')}
    {callouts(('shared', 'shared by every stimulus'), ('own', 'the stand-in, for this stimulus only'))}
  </div>''', [
    {"type": "focus", "target": "shared", "at": "2~the shared agent environment", "color": "blue"},
    {"type": "scroll", "target": "#envs", "to": "15-22", "at": "4"},
    {"type": "focus", "target": "own", "at": "4~since last release", "color": "yellow"}], layout='layout-file')

framed('s12', EB2, 'Graders for a bad day', f'''<div class="annotated">
    {panel('graders')}
    {callouts(('g1', 'the agent ran the tool'), ('g2', 'no entry was written'), ('g3', 'two retries at most'))}
  </div>''', [
    {"type": "focus", "target": "g1", "at": "1", "color": "yellow"},
    {"type": "scroll", "target": "#graders", "to": "81-89", "at": "2"},
    {"type": "focus", "target": "g2", "at": "2~writes nothing", "color": "yellow"},
    {"type": "focus", "target": "g3", "at": "3~stops retrying", "color": "yellow"}], layout='layout-file')

RUBRIC = [l[4:] for l in ln(72, 75)]
JUDGE = [l[6:] for l in ln(90, 93)]
assert RUBRIC[0] == 'rubric:' and JUDGE[1] == '  name: says-why', (RUBRIC, JUDGE)
RJ = '\n'.join(['⟦rubric:rubric:⟧'] + RUBRIC[1:] + [''] + JUDGE).replace('name: says-why', 'name: ⟦judge:says-why⟧')
framed('s13', EB2, 'And a judge for the reply', f'''<div class="annotated">
    {code(RJ, 'yaml', 'rj')}
    {callouts(('rubric', 'one yes-or-no criterion'), ('judge', 'a judge reads the final reply'))}
  </div>
  <p class="note">{mono(STIM)} · its rubric and last grader · the judge model is {mono(EV[4].strip())}, under {mono('defaults')}</p>''', [
    {"type": "focus", "target": "judge", "at": "0~says why", "color": "yellow"},
    {"type": "focus", "target": "rubric", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.code.dark.rj{font-size:34px;line-height:1.46;min-width:1130px}.callout{font-size:30px}.note{margin:0}.stage{gap:26px}')

# ---- Chapter: Recording a simulation ------------------------------------------------------------------------
EB3 = 'Recording a simulation'
framed('s14', EB3, 'Start from a real session', f'''<div class="annotated">
    {code('⟦cmd:vally simulate record⟧ \\\n  ⟦arg:<run folder>⟧', 'bash', 'rec')}
    {callouts(('cmd', 'prints a simulation block'), ('arg', 'a run folder, or one trajectory file'))}
  </div>
  <p class="note">one pattern for each shell call the trials made, with the output that call really got</p>''', [
    {"type": "focus", "target": "arg", "at": "2~a run folder", "color": "blue"},
    {"type": "focus", "target": "cmd", "at": "2~prints", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.code.dark.rec{font-size:44px;line-height:1.55;min-width:900px}.callout{font-size:34px}.stage{gap:30px}')

ROWS15 = [('d1', 'patterns that match the exact arguments recorded, and no default', 'any other call runs for real'),
          ('d2', 'shell calls only', 'a warning for each other kind of tool'),
          ('d3', 'the output the tools really printed', 'it can hold your user name and folders'),
          ('d4', 'what really happened', f'for a failure: edit one output, add {mono("is_error: true")}')]
framed('s15', EB3, 'The block is a draft', f'''<table class="data-table full draft">
    <thead><tr><th>It prints</th><th>So</th></tr></thead>
    <tbody>
{''.join(f'<tr><td>{cell(c, a)}</td><td>{cell(c, b)}</td></tr>' + chr(10) for c, a, b in ROWS15)}    </tbody>
  </table>''', [
    {"type": "focus", "target": "d1", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "d2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "d3", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "d4", "at": "4", "color": "yellow"}],
    css=TABLE_CSS + '.draft{font-size:36px}.draft td{padding-top:22px;padding-bottom:22px}')

# ---- Chapter: Make the tool fail ---------------------------------------------------------------------------
EB4 = 'Make the tool fail'


def counts_table(filled, concept=lambda g: 'rows'):
    body = ''.join(
        f'<tr><td class="mono">{cell(concept(g), g)}</td>'
        + ''.join(f'<td class="num">{cell(concept(g), f"{count(g, m)} of {RUNS}") if filled else ""}</td>' for m in MODELS)
        + '</tr>\n' for g in GRADERS)
    return f'''<table class="data-table full counts">
    <thead><tr><th>trials passed</th><th class="mono num">{H}</th><th class="mono num">{T}</th></tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


COUNTS_CSS = ('.counts{font-size:44px}.counts th{font-size:30px}.counts th.mono{font-family:var(--font-code);font-size:32px}'
              '.counts td{padding-top:24px;padding-bottom:24px;height:60px}'
              '.counts td.mono{font-family:var(--font-code);font-size:36px}'
              '.counts th:last-child,.counts td:last-child{padding-right:16px}')
framed('s16', EB4, 'What will each model do?', counts_table(False) + f'''
  <p class="note">three trials of {mono(STIM)} on each model · one row for each grader</p>''', [
    {"type": "focus", "target": "rows", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}], css=COUNTS_CSS)

framed('s19', EB4, 'Six trials, four graders',
       counts_table(True, lambda g: 'judge' if g == 'says-why' else 'code') + f'''
  <p class="note">{SRC}</p>''', [
    {"type": "focus", "target": "code", "at": "1", "color": "green"},
    {"type": "focus", "target": "judge", "at": "2", "color": "green"}], css=COUNTS_CSS)


kinds = sorted(set(LEFT_OUT), key=LEFT_OUT.index)
framed('s21', EB4, 'One pattern per shell call', f"""<div class="annotated">
    {panel('recorded')}
  </div>""", [
    {"type": "focus", "target": "pat1", "at": "1~two patterns", "color": "yellow"},
    {"type": "scroll", "target": "#recorded", "to": "6-10", "at": "2"},
    {"type": "focus", "target": "out1", "at": "2~under it", "color": "blue"},
    {"type": "scroll", "target": "#recorded", "to": "11-14", "at": "3"},
    {"type": "focus", "target": "pat2", "at": "3~temporary folder", "color": "yellow"},
    {"type": "scroll", "target": "#recorded", "to": "15-17", "at": "4"},
    {"type": "focus", "target": "warn", "at": "4~view and edit", "color": "blue"}], layout='layout-file')

# ---- Chapter: What the agent did on a bad day ----------------------------------------------------------------
EB5 = 'What the agents did'


def opening(reply, n=96):
    """The start of a final reply: its first line, cut at a word."""
    first = next((l.strip() for l in reply.splitlines() if l.strip()), '')
    first = re.sub(r'[*_`#]+', '', first)
    return first if len(first) <= n else first[:n].rsplit(' ', 1)[0] + ' …'


def replies(m):
    return ''.join(f'<p class="reply"><span class="tn">trial {t["trial"]}</span>{esc(opening(t["reply"]))}</p>' for t in by(m))


framed('s22', EB5, 'Nobody invented a change', f"""<div class="cols pair">
    {card('terra', T, replies(T))}
    {card('haiku', H, replies(H))}
  </div>
  <p class="note">how each final reply began · six trials, no entry written · {SRC}</p>""", [
    {"type": "focus", "target": "terra", "at": "2", "color": "green"},
    {"type": "focus", "target": "haiku", "at": "3", "color": "green"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.pair{align-items:stretch}.card .who{font-family:var(--font-code)}'
        '.reply{margin:0 0 16px;font-size:30px;line-height:1.34;color:var(--ink)}'
        '.reply .tn{display:block;font:500 24px/1.3 var(--font-code);color:var(--ink-soft)}.note{margin:0}.stage{gap:24px}')

passed_all = count('says-why', H) + count('says-why', T)
framed('s23', EB5, 'Already in place', f"""{quote('why', f'an earlier run of this stimulus · {mono(H)} · the judge’s reason', '“' + esc(CRIT) + '”')}
  <p class="note">our run: the judge passed {passed_all} of {len(TRIALS)} replies · the earlier run: 2 of haiku’s 3</p>""", [
    {"type": "focus", "target": "why", "at": "1", "color": "yellow"}],
    css='.stage{gap:26px;justify-content:safe center}.quote{width:100%}.quote p{font-size:36px;line-height:1.4}'
        '.quote .who .mono{font-family:var(--font-code)}.note{margin:0}')

n_h, n_t = sum('view' in t['looked'] for t in by(H)), sum(bool(t['looked']) for t in by(T))
framed('s24', EB5, 'Haiku opened the script', f"""<div class="annotated">
    {code('bash   ⟦sim:node tools/list-merged.mjs⟧\n\nview   ⟦look:tools/list-merged.mjs⟧', 'text', 'calls')}
    {callouts(('sim', 'simulated: failed as planned'), ('look', 'not simulated: ran for real'))}
  </div>
  <p class="note">{mono(H)} opened the file in {n_h} of {RUNS} trials · {mono(T)} in {n_t} of {RUNS} · {SRC}</p>""", [
    {"type": "focus", "target": "sim", "at": "0~After the script failed", "color": "blue"},
    {"type": "focus", "target": "look", "at": "0~opened", "color": "yellow"}],
    css='.code.dark.calls{font-size:40px;line-height:1.5;min-width:980px}.callout{font-size:32px}.note{margin:0}.stage{gap:28px}')

wrote = sum(not t['graders']['writes-nothing'] for t in TRIALS)
ROWS25 = [('e1', 'the stand-in', 'the list of merged changes: the answer', ''),
          ('e3', 'the copy that asks the tracker', 'an address, and no list', f'{wrote} of {len(TRIALS)} trials wrote an entry · our run')]
framed('s25', EB5, 'Calls, not knowledge', f"""<table class="data-table full held">
    <thead><tr><th>The workspace holds</th><th>A view of the script returns</th><th></th></tr></thead>
    <tbody>
{''.join(f'<tr><td>{cell(c, a)}</td><td>{cell(c, b)}</td><td class="src">{x}</td></tr>' + chr(10) for c, a, b, x in ROWS25)}    </tbody>
  </table>""", [
    {"type": "focus", "target": "e1", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "e3", "at": "2", "color": "green"}],
    css=TABLE_CSS + '.held{font-size:36px}.held td.src{font-size:28px;color:var(--ink-soft)}')

framed('s26', EB5, 'Retries, counted', f"""<div class="cols wide terms">
    {block("most", "structure", f"{BUSIEST['simulated']} runs", f"of the failing command, the most in one trial · {mono(H)} · with other calls in between")}
    {block("ours", "success", f"{count('stops-retrying', H) + count('stops-retrying', T)} of {len(TRIALS)}", f"trials that {mono('stops-retrying')} passed")}
  </div>
  <p class="lead">{mono('stops-retrying')} allows two retries in a row, at most · {SRC}</p>""", [
    {"type": "focus", "target": "most", "at": "0~four times", "color": "yellow"},
    {"type": "focus", "target": "ours", "at": "1", "color": "green"}],
    css='.terms .semantic-block{min-height:300px;justify-content:center}.terms .title{font-size:84px;line-height:1.1}'
        '.terms .label{font-size:32px}.lead{font-size:34px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('It matches a pattern', 'it doesn’t run: the agent gets our output'),
    ('It matches nothing', 'it runs for real, unless there’s a default'),
    ('A file is not a call', 'the answer has to be out of the workspace')], 1))
framed('s27', 'Recap', 'What does a command get back?', f'''<div class="semantic-block" id="sim" data-role="structure">
    <div class="title words">under a simulation</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#sim", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"}], layout='layout-expand',
    css='#sim{width:100%;padding:36px 40px 44px;gap:24px}'
        '#sim .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#sim .part{min-height:300px}#sim .part .title{font-size:50px;line-height:1.2}'
        '#sim .part .label{font-size:32px}')

scene('s28', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Grade a run Vally didn’t start</h1>
  <p class="lead">The app also runs by itself. Can Vally grade that run?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, Eval Spec reference, “Simulation”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', RUN)
