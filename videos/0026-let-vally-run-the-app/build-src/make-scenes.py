"""Generate lesson 26's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout), terms in
blocks, numbers in a .data-table. Nothing here sets a colour or a font outside the theme's
variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/                     the files the tapes install into the practice folder (verified/lesson-26
                                 and lesson-25), which the panels show
  src/run/trials.tsv             one row per since-last-release trial through the app: the eval of s16
                                 (one per model) and the experiment of s21 (three per variant)
  src/run/s16.log, s20.log, s21.log   what Vally printed in those recordings
  src/run/eval-report.json       from the s16 run's eval-results.md
  src/run/trace-join.json        two span lines from the s16 run, cut to their ids
  src/run/vally-executor.json    the series' own lesson 22 and 23 runs through Vally's executor
  src/run/app-earlier.json       the series' lesson 25 run of the app outside Vally
  src/run/facts.json             the GitHub MCP tools counted in this run's app traces, and an earlier
                                 run's two counts (saved as src/run/earlier-run.txt)
While src/run/PROVISIONAL exists these are stand-ins from the course's verified run.

The assert block states what the narration says. If a recording changes a count, an assert fails:
reword the outcome sentences in storyboard.json, change the assert, and run this again.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, math, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
H, T = MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
SHORT = {H: 'haiku', T: 'terra'}
R = D / 'src/run'
PROVISIONAL = (R / 'PROVISIONAL').exists()
STAND_IN = ' · stand-in: the course’s verified run' if PROVISIONAL else ''


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


def cell(cid, text, cls='num'):
    return f'<td class="{cls}"><span data-concept="{cid}" data-rep="cell">{text}</span></td>'


def th(cid, text, cls='num'):
    return f'<th class="{cls}"><span data-concept="{cid}" data-rep="cell">{text}</span></th>'


def focus(target, at, color=None):
    c = {"type": "focus", "target": target, "at": at}
    if color:
        c["color"] = color
    return c


TABLE_CSS = ('.data-table{font-size:38px}.data-table th{font-size:30px}'
             '.data-table td{padding-top:24px;padding-bottom:24px}'
             '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:34px}'
             '.data-table th:last-child,.data-table td:last-child{padding-right:16px}')
TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'
BIG = ('.terms .semantic-block{min-height:300px;justify-content:center}'
       '.terms .title{font-size:104px;line-height:1.1}.terms .label{font-size:34px}')


# ---- The runs ---------------------------------------------------------------------------------------------
def load_trials():
    rows = [l.split('\t') for l in (R / 'trials.tsv').read_text().splitlines() if l.strip()]
    head, rows = rows[0], rows[1:]
    out = []
    for r in rows:
        t = dict(zip(head, r))
        out.append({'run': t['run'], 'variant': t['variant'], 'model': t['model'], 'passed': t['passed'] == 'true',
                    'loaded': t['skills'] != '-', 'tokens': int(t['tokens']), 'calls': int(t['calls']),
                    'aiu': float(t['aiu']), 'entry76': t['entry76'] == 'true'})
    return out


def wilson(k, n, z=1.96):
    """The 95% range the course's range calculator gives for k of n, as whole percentages."""
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0, centre - half) * 100), round(min(1, centre + half) * 100)


APP = load_trials()
EVAL = [t for t in APP if t['run'] == 'eval']
EXP = [t for t in APP if t['run'] == 'experiment']
VX = json.loads((R / 'vally-executor.json').read_text())
EARLIER = json.loads((R / 'app-earlier.json').read_text())
REPORT = json.loads((R / 'eval-report.json').read_text())
JOIN = json.loads((R / 'trace-join.json').read_text())
FACTS = json.loads((R / 'facts.json').read_text())
LOG16, LOG20, LOG21 = ((R / f'{s}.log').read_text() for s in ('s16', 's20', 's21'))
RUN_EVAL = (R / 'RUN-eval').read_text().strip()
RUN_EXP = (R / 'RUN-experiment').read_text().strip()
OURS = 'our run · ' if not PROVISIONAL else ''

app = lambda m, rows=APP: [t for t in rows if t['model'] == m]
count = lambda rows, key: sum(bool(t[key]) for t in rows)
tpc = lambda t: t['tokens'] / t['calls']                      # tokens a model call, one trial
row_tpc = lambda rows: sum(t['tokens'] for t in rows) / sum(t['calls'] for t in rows)
row_aiu = lambda rows: sum(t['aiu'] for t in rows) / len(rows)
row_calls = lambda rows: sum(t['calls'] for t in rows) / len(rows)
vx = lambda m: VX[m]['trials']

# ---- What the narration says. If a recording changes these, the sentences change too. ----------------------
# s01, s15: the app's one earlier run on haiku failed, no skill loaded, an entry for the refactor; and
#           Vally's own trials on haiku passed three of eight.
assert EARLIER['model'] == H and not EARLIER['passed'] and not EARLIER['skill_loaded'] and EARLIER['entry76'], EARLIER
assert (VX[H]['passed'], len(vx(H))) == (3, 8), VX[H]['passed']
# s11, s16: the refusal message is what Vally printed, for tracker-down, on both models.
MESSAGE = ("Executor 'release-app' does not support tool-call simulation, but stimulus 'tracker-down' "
           "declares a 'simulation' block. Use a simulation-capable executor (e.g. 'copilot-sdk') or "
           "remove the simulation config.")
flat16 = re.sub(r'\s+', ' ', LOG16)
assert flat16.count(MESSAGE) >= 2 and re.search(r'ERROR\s+tracker-down', LOG16), 'refusal message not in s16.log'
# s16: one trial per model; haiku failed since-last-release, terra passed; the table says 0/2 and 1/2.
assert len(EVAL) == 2 and len(app(H, EVAL)) == 1 and not app(H, EVAL)[0]['passed'] and app(T, EVAL)[0]['passed'], EVAL
m = re.search(r'^\s*release\s+\S (\d)/(\d)\s+\S (\d)/(\d)\s*$', LOG16, re.M)
assert m and m.groups() == ('0', '2', '1', '2'), m and m.groups()
# s17: executor release-app for both; haiku no Skills column, tools: four views and one edit;
#      terra lists changelog-entry and a skill call.
assert all(REPORT[mdl]['executor'] == 'release-app' for mdl in MODELS), REPORT
tools = lambda mdl: dict((k.strip(), int(v)) for k, v in (x.split(':') for x in REPORT[mdl]['tool_calls'].split(',')))
assert REPORT[H]['skills'] == [] and not REPORT[H]['has_skills_column'] and tools(H) == {'view': 4, 'edit': 1}, REPORT[H]
assert REPORT[T]['skills'] == ['changelog-entry'] and tools(T).get('skill', 0) >= 1, REPORT[T]
# s18: one trace id on both lines; the session's parent is Vally's attempt span.
A, S = JOIN['attempt'], JOIN['session']
assert A['traceId'] == S['traceId'] and S['parentSpanId'] == A['spanId'] and A['name'] == 'vally.attempt' \
    and S['name'] == 'invoke_agent', JOIN
# s20: two plans, haiku the baseline.
assert re.search(r'Plans:\s+2\b', LOG20) and re.search(r'Baseline:\s+haiku\b', LOG20), 'dry run plan'
# s21: the table gives terra one stimulus of two and haiku none; terra used about a quarter fewer tokens.
m = re.search(r'^\s*stimuli\s+(\d)/(\d)\s+(\d)/(\d)', LOG21, re.M)
assert m and m.groups() == ('0', '2', '1', '2'), m and m.groups()
m = re.search(r'^\s*tokens\s+([\d.]+)k\s+([\d.]+)k', LOG21, re.M)
assert m and -0.30 <= float(m.group(2)) / float(m.group(1)) - 1 <= -0.20, m and m.groups()
assert len(re.findall(r'ERROR\s+tracker-down\s+0 passed · 3 errors', LOG21)) >= 2, 'tracker-down in s21.log'
# s22: per variant, three trials. Haiku: none passed, one loaded, an entry for #76 every time, about 6.7 AIU.
#      Terra: all passed, all loaded, no entry for #76, about 10.7 AIU.
eh, et = app(H, EXP), app(T, EXP)
assert len(eh) == len(et) == 3, (len(eh), len(et))
assert (count(eh, 'passed'), count(eh, 'loaded'), count(eh, 'entry76')) == (0, 1, 3), eh
assert (count(et, 'passed'), count(et, 'loaded'), count(et, 'entry76')) == (3, 3, 0), et
COST_H, COST_T = sum(t['aiu'] for t in eh), sum(t['aiu'] for t in et)
assert (round(COST_H, 1), round(COST_T, 1)) == (6.7, 10.7), (COST_H, COST_T)
# s24: four trials a model through the app, eight through Vally's executor.
assert len(app(H)) == len(app(T)) == 4 and len(vx(H)) == len(vx(T)) == 8
# s25: terra loaded and passed every time either way; haiku loaded 1 of 5 through the app (its four trials and
#      the one earlier run) against 4 of 8; ranges 4-62% against 22-78%; an earlier run: 0 of 5 against 1 of 8.
assert count(app(T), 'passed') == count(app(T), 'loaded') == 4 and VX[T]['passed'] == VX[T]['loaded'] == 8
APP_LOADED, APP_N = count(app(H), 'loaded') + int(EARLIER['skill_loaded']), len(app(H)) + 1
assert (APP_LOADED, APP_N, VX[H]['loaded']) == (1, 5, 4), (APP_LOADED, APP_N, VX[H]['loaded'])
RANGE_APP, RANGE_VX = wilson(APP_LOADED, APP_N), wilson(VX[H]['loaded'], 8)
assert RANGE_APP == (4, 62) and RANGE_VX == (22, 78), (RANGE_APP, RANGE_VX)
ER = FACTS['earlier_run']
assert ER['app'] == [0, 5] and ER['vally'] == [1, 8]
earlier_txt = (R / 'earlier-run.txt').read_text()
assert 'app haiku 0/5' in earlier_txt and 'Vally haiku 1/8' in earlier_txt, 'earlier-run.txt'  # the saved evidence
# s26: every trial of the app used more tokens a model call than every trial through Vally's executor:
#      haiku about 17,400 against 15,300, terra 14,000 against 12,500; about 16% and 13% more on average.
LOW = {mdl: min(tpc(t) for t in app(mdl)) for mdl in MODELS}
HIGH = {mdl: max(tpc(t) for t in vx(mdl)) for mdl in MODELS}
MORE = {mdl: round((row_tpc(app(mdl)) / row_tpc(vx(mdl)) - 1) * 100) for mdl in MODELS}
hundred = lambda v: round(v / 100) * 100
assert all(LOW[mdl] > HIGH[mdl] for mdl in MODELS), (LOW, HIGH)
assert (hundred(LOW[H]), hundred(HIGH[H]), hundred(LOW[T]), hundred(HIGH[T])) == (17400, 15300, 14000, 12500), (LOW, HIGH)
assert (MORE[H], MORE[T]) == (16, 13), MORE
# s27: five GitHub tools.
assert FACTS['mcp_tools'] == 5
# s28: on haiku the app's trials made fewer calls (5.25 against 5.75) and cost about the same (2.54 against 2.58
#      AIU a trial); on terra they made slightly more calls and cost more (about 4 against 3.27).
CALLS = {mdl: (row_calls(app(mdl)), row_calls(vx(mdl))) for mdl in MODELS}
AIU = {mdl: (row_aiu(app(mdl)), row_aiu(vx(mdl))) for mdl in MODELS}
assert CALLS[H] == (5.25, 5.75), CALLS[H]
assert (round(AIU[H][0], 2), round(AIU[H][1], 2)) == (2.54, 2.58), AIU[H]
assert CALLS[T][0] > CALLS[T][1] and CALLS[T][0] - CALLS[T][1] <= 0.5, CALLS[T]
assert (round(AIU[T][0], 1), round(AIU[T][1], 2)) == (4.0, 3.27), AIU[T]

# ---- Hook ------------------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Let Vally run the app', f'''<div class="cols wide terms">
    {block("vally", "structure", f"{VX[H]['passed']} of {len(vx(H))} passed",
           f"Vally’s own trials · skill loaded in {VX[H]['loaded']}", words=True)}
    {block("app", "attention", "1 run, failed", "the release app · no skill loaded, an entry for the refactor", words=True)}
  </div>
  <p class="note">{mono("since-last-release")} on {mono(H)}{STAND_IN}</p>''', [
    focus("app", "0", "yellow"),
    focus("vally", "1", "blue"),
    focus("none", "2")],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.terms .semantic-block{min-height:250px}'
        '.terms .title{font-size:60px}.terms .label{font-size:34px}')

# ---- Chapter: The executor is the seam ---------------------------------------------------------------------
EB1 = 'The executor is the seam'
STEPS = [('before', 'structure', 'Prepare the workspace', 'files, setup commands'),
         ('before', 'structure', 'Take the starting state', 'before the agent'),
         ('exec', 'attention', 'Run the executor', 'stimulus in, trajectory out'),
         ('after', 'structure', 'Save the patch', 'what changed'),
         ('after', 'structure', 'Run the graders', 'a verdict'),
         ('after', 'structure', 'Repeat, then report', 'every trial and model')]
framed('s02', EB1, 'One step runs the agent', f'''<div class="grid6">
    {''.join(block(c, r, t, l, words=True, step=i) for i, (c, r, t, l) in enumerate(STEPS, 1))}
  </div>''', [
    focus("before", "1~prepares", "blue"),
    focus("after", "1~afterwards", "blue"),
    focus("exec", "2", "yellow")],
    css='.grid6{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;width:100%}'
        '.grid6 .semantic-block{min-height:232px;padding-top:18px;padding-bottom:20px}'
        '.grid6 .step{font-size:52px}.grid6 .title{font-size:40px}.grid6 .label{font-size:30px}')

framed('s03', EB1, 'Two sessions, two sets of settings', f'''<div class="cols wide terms">
    {block("own", "structure", "copilot-sdk", "Vally’s own executor · a Copilot SDK session, with Vally’s settings")}
    {block("app", "attention", "release-app", "an executor that calls the app · a Copilot SDK session, with the team’s settings")}
  </div>''', [
    focus("own", "0", "blue"),
    focus("app", "1", "yellow"),
    focus("none", "2"),
    focus("app", "4", "yellow")], css=TERMS)

VIEWS = [('r1', 'Vally’s own executor', 'Does the skill do its job, on any model, apart from the app?'),
         ('r2', 'The app, through an executor plugin', 'Does the feature, as shipped, do its job? Repeatable, so we can count.'),
         ('r3', 'The app’s real runs, graded afterwards', 'Is it still doing its job in real use?')]
views_table = f'''<table class="data-table full views">
    <thead><tr><th>Run it through</th><th>What it answers</th></tr></thead>
    <tbody>
{''.join(f'<tr><td><span data-concept="{c}" data-rep="cell">{a}</span></td><td>{b}</td></tr>' + chr(10) for c, a, b in VIEWS)}    </tbody>
  </table>'''
VIEWS_CSS = TABLE_CSS + '.views td{padding-top:30px;padding-bottom:30px}.views td:first-child{width:38%}'
framed('s04', EB1, 'Three views of one feature', views_table, [
    focus("r1", "1", "blue"),
    focus("r2", "2", "yellow"),
    focus("r3", "3", "blue")], css=VIEWS_CSS)

# ---- Chapter: What an executor returns ---------------------------------------------------------------------
EB2 = 'What an executor returns'
framed('s05', EB2, 'A plugin registers an executor', f'''<div class="annotated">
    {panel('stub')}
    {callouts(('name', 'selected by this name'), ('exec', 'runs one trial'),
              ('shut', 'called at the end'), ('reg', 'what Vally looks for'))}
  </div>''', [
    focus("name", "2~name", "blue"),
    focus("exec", "3", "yellow"),
    {"type": "scroll", "target": "#stub", "to": "71-77", "at": "4"},
    focus("shut", "4~Shutdown", "blue"),
    focus("reg", "5~register executors", "blue")], layout='layout-file')

framed('s06', EB2, 'Execute calls the app’s own function', f'''<div class="annotated">
    {panel('exec')}
    {callouts(('we', 'the app’s own function'), ('wd', 'the prepared workspace'), ('sk', 'each skill’s folder'),
              ('req', 'the stimulus’s prompt'), ('tel', 'traces go to the trial’s folder'), ('tc', 'the trial’s trace'))}
  </div>''', [
    focus("sig", "1", "blue"),
    focus("we", "2~write entries", "yellow"),
    focus("wd", "3", "blue"),
    focus("model", "4~model", "blue"),
    {"type": "scroll", "target": "#exec", "to": "70-77", "at": "5"},
    focus("sk", "5~folders", "blue"),
    focus("req", "6~prompt", "blue"),
    focus("to", "6~time limit", "blue"),
    focus("tel", "7", "blue"),
    focus("tc", "8", "yellow")], layout='layout-file')

framed('s07', EB2, 'It hands back a trajectory', f'''<div class="annotated">
    {panel('exec2')}
    {callouts(('tte', 'the SDK’s events, renamed'), ('ret', 'events, reply, workspace'),
              ('cm', 'tokens, cost, tool calls, skills'), ('wall', 'ours to measure'))}
  </div>''', [
    {"type": "scroll", "target": "#exec2", "to": "70-77", "at": "t=0", "duration": 0},
    {"type": "scroll", "target": "#exec2", "to": "79-86", "at": "0+2"},
    focus("tte", "1~renames", "blue"),
    focus("ret", "2~trajectory", "yellow"),
    {"type": "scroll", "target": "#exec2", "to": "84-92", "at": "3"},
    focus("cm", "3~compute metrics", "blue"),
    focus("wall", "5~wall time", "blue"),
    {"type": "scroll", "target": "#exec2", "to": "92-99", "at": "6"},
    focus("meta", "6~metadata", "blue")], layout='layout-file')

framed('s08', EB2, 'SDK events become Vally’s', panel('events'), [
    focus("tool", "1~tool call event", "blue"),
    {"type": "scroll", "target": "#events", "to": "37-45", "at": "2"},
    focus("skill", "2~skill activation", "blue"),
    focus("usage", "4~token usage", "blue"),
    {"type": "scroll", "target": "#events", "to": "42-50", "at": "4~cost"},
    focus("cost", "5", "yellow")], layout='layout-file')

framed('s09', EB2, 'A plugins section loads it', f'''<div class="annotated">
    {panel('vy')}
    {callouts(('plug', 'loads the plugin file'))}
  </div>''', [
    focus("suites", "0~suites", "blue"),
    focus("plug", "1", "yellow")], layout='layout-file')

SELECT = ('vally eval … ⟦run:--executor release-app⟧\n\n'
          'defaults:\n  ⟦def:executor: release-app⟧\n\n'
          'overrides:\n  ⟦over:executor: release-app⟧')
framed('s10', EB2, 'Loading isn’t selecting', f'''<div class="annotated">
    {code(SELECT, 'yaml', 'select')}
    {callouts(('run', 'for one run'), ('def', 'for one eval file'), ('over', 'for one experiment'))}
  </div>''', [
    focus("run", "1~dash dash executor", "yellow"),
    focus("def", "1~defaults", "blue"),
    focus("over", "1~overrides", "blue")],
    css='.code.dark.select{min-width:900px;font-size:40px;line-height:1.5}.callout{font-size:34px}')

REFUSED = ("⟦err:ERROR⟧  ⟦stim:tracker-down⟧\n"
           " Executor 'release-app' ⟦no:does not support tool-call⟧\n"
           " ⟦no:simulation⟧, but stimulus 'tracker-down' declares a\n"
           " 'simulation' block. Use a simulation-capable executor\n"
           " (e.g. 'copilot-sdk') or remove the simulation config.")
assert re.sub(r'[⟦⟧]|\b(err|stim|no):', '', re.sub(r'\s+', ' ', REFUSED)).split('tracker-down ', 1)[1] == MESSAGE
framed('s11', EB2, 'No simulation, no run', f'''<div class="annotated">
    {code(REFUSED, 'text', 'refused')}
    {callouts(('no', 'ours declares nothing'), ('stim', 'the stimulus with a simulation block'))}
  </div>
  <p class="note">what Vally prints for that stimulus, through this executor{STAND_IN}</p>''', [
    focus("no", "1", "yellow"),
    focus("stim", "2~tracker down", "blue"),
    focus("err", "3~ends in error", "red"),
    focus("none", "4")],
    css='.code.dark.refused{font-size:34px;line-height:1.5}.callout{font-size:32px}.stage{gap:24px}')

# ---- Chapter: Join the app's traces to Vally's --------------------------------------------------------------
EB3 = 'Joining the app’s traces to Vally’s'
TREE = ('Vally · otel-spans.jsonl\n  ⟦trial:vally.trial⟧\n    ⟦attempt:vally.attempt⟧\n\n'
        'the app · its own trace file\n  ⟦session:invoke_agent⟧\n    chat\n    execute_tool')
framed('s12', EB3, 'Two programs, two traces', f'''<div class="annotated">
    {code(TREE, 'text', 'tree')}
    {callouts(('trial', 'one for each trial'), ('attempt', 'one for each attempt'),
              ('session', 'no parent: a trace of its own'))}
  </div>''', [
    focus("trial", "1~span for the trial", "blue"),
    focus("attempt", "1~each attempt", "blue"),
    focus("session", "2~invoke agent", "yellow"),
    focus("none", "4")],
    css='.code.dark.tree{min-width:820px;font-size:38px;line-height:1.45}.callout{font-size:34px}')

PARENT = '⟦tp:traceparent⟧\n\n  ⟦ver:version⟧ - ⟦tid:trace ID⟧ - ⟦pid:parent span ID⟧ - ⟦fl:flags⟧'
framed('s13', EB3, 'A trace context joins them', f'''<div class="annotated">
    {code(PARENT, 'text', 'parent')}
    {callouts(('tp', 'one short string'))}
  </div>
  <div class="cols wide terms">
    {block("tid", "structure", "trace ID", "which trace to join")}
    {block("pid", "attention", "parent span ID", "which span to sit under")}
  </div>
  <p class="note">Source: W3C, “Trace Context”</p>''', [
    focus("tid", "1~ID of a trace", "blue"),
    focus("pid", "1~span that's open", "yellow"),
    focus("none", "2"),
    focus("tp", "3~trace parent", "blue"),
    focus("ver", "3~version", "blue"),
    focus("tid", "3~the trace ID", "blue"),
    focus("pid", "3~parent span's ID", "yellow"),
    focus("fl", "3~flags", "blue")],
    css='.code.dark.parent{font-size:38px;line-height:1.5;padding:22px 34px}.callout{font-size:34px}'
        '.stage{gap:26px}.terms .semantic-block{min-height:150px}.terms .title{font-size:40px}.terms .label{font-size:32px}')

framed('s14', EB3, 'The app needed two lines', panel('ra'), [
    focus("fn", "1~function", "blue"),
    focus("tc", "2~two lines", "yellow"),
    focus("none", "3")], layout='layout-file')

# ---- Chapter: Write and run the executor --------------------------------------------------------------------
EB4 = 'Write and run the executor'
empty = ''.join(f'<tr><td class="mono">{mdl}</td><td class="num"></td><td class="num"></td></tr>\n' for mdl in MODELS)
framed('s15', EB4, 'How will the app compare?', f'''<table class="data-table full ask">
    <thead><tr><th>{mono("since-last-release")}, through the app</th>{th("c1", "Trials passed, of 4")}{th("c2", "Trials that loaded the skill, of 4")}</tr></thead>
    <tbody>
{empty}    </tbody>
  </table>
  <p class="note">four trials a model: one from the eval, three more from the experiment</p>''', [
    focus("c2", "3~loading the skill", "blue"),
    focus("c1", "4~pass", "yellow"),
    focus("none", "5")],
    css=TABLE_CSS + '.ask td{padding-top:34px;padding-bottom:34px;height:56px}.ask th .mono{font-family:var(--font-code)}')

rep_rows = ''.join(
    f'<tr><td class="mono"><span data-concept="{SHORT[mdl]}" data-rep="cell">{mdl}</span></td>'
    f'<td class="mono"><span data-concept="ex" data-rep="cell">{REPORT[mdl]["executor"]}</span></td>'
    f'<td class="mono">{", ".join(REPORT[mdl]["skills"]) or "—"}</td>'
    f'<td class="mono">{REPORT[mdl]["tool_calls"]}</td></tr>\n' for mdl in MODELS)
framed('s17', EB4, 'These trials ran the app', f'''<table class="data-table full rep">
    <thead><tr><th>{mono("since-last-release")}</th><th>Executor</th><th>Skills</th><th>Tool calls</th></tr></thead>
    <tbody>
{rep_rows}    </tbody>
  </table>
  <p class="note">from {mono("eval-results.md")} · {OURS}{RUN_EVAL}{STAND_IN}</p>''', [
    focus("ex", "0~executor", "blue"),
    focus("haiku", "1", "yellow"),
    focus("terra", "2", "green")],
    css=TABLE_CSS + '.rep td{padding-top:30px;padding-bottom:30px;white-space:nowrap}.rep th{white-space:nowrap}.rep td.mono{font-size:28px}.rep td,.rep th{padding-right:28px}.rep th .mono{font-family:var(--font-code)}')

span_a = f'"traceId": "⟦tid:{A["traceId"]}⟧"\n"spanId": "⟦aid:{A["spanId"]}⟧"\n"name": "vally.attempt"'
span_s = f'"traceId": "⟦tid:{S["traceId"]}⟧"\n"parentSpanId": "⟦aid:{S["parentSpanId"]}⟧"\n"name": "invoke_agent"'
framed('s18', EB4, 'The app’s span joined Vally’s trace', f'''<div class="stack">
    {card('va', f'{mono("otel-spans.jsonl")} · Vally’s attempt span · one line, cut to three fields', code(span_a, 'text'))}
    {card('ap', f'{mono("app-traces.jsonl")}, in the trial’s folder · the app’s session span · one line, cut', code(span_s, 'text'))}
  </div>
  <p class="note">{mono(H)} · {OURS}{RUN_EVAL}{STAND_IN}</p>''', [
    focus("tid", "2~one trace ID", "blue"),
    focus("aid", "3~parent", "yellow")],
    css='.stack{display:flex;flex-direction:column;gap:22px;width:100%}.stack .card{width:100%}'
        '.stack .card > .code.dark{font-size:32px;line-height:1.45;padding:18px 30px}.stage{gap:20px}')

framed('s19', EB4, 'One executor, two models', f'''<div class="annotated">
    {panel('exp')}
    {callouts(('vary', 'the variants differ only in the model'), ('exec', 'one executor for both'),
              ('runs', 'three trials each'))}
  </div>''', [
    focus("ev", "1~release eval", "blue"),
    focus("vary", "1~differ", "blue"),
    {"type": "scroll", "target": "#exp", "to": "10-18", "at": "2"},
    focus("exec", "2~executor", "yellow"),
    focus("runs", "3", "blue")], layout='layout-file')


def count_row(cid, name, rows, cost):
    n = len(rows)
    return (f'<tr><td class="mono"><span data-concept="{cid}" data-rep="cell">{name}</span></td>'
            f'<td class="num">{count(rows, "passed")} of {n}</td><td class="num">{count(rows, "loaded")} of {n}</td>'
            f'<td class="num">{count(rows, "entry76")} of {n}</td>{cell("cost", f"{cost:.2f}")}</tr>\n')


framed('s22', EB4, 'What the table leaves out', f'''<table class="data-table full counts">
    <thead><tr><th>Variant</th><th class="num">Passed</th><th class="num">Skill loaded</th>
      <th class="num">Entry for #76</th><th class="num">Cost, AIU</th></tr></thead>
    <tbody>
{count_row('haiku', 'haiku', eh, COST_H)}{count_row('terra', 'terra', et, COST_T)}    </tbody>
  </table>
  <p class="note">the three {mono("since-last-release")} trials of each variant · #76 is the refactor users can’t see · {OURS}{RUN_EXP}{STAND_IN}</p>''', [
    focus("haiku", "1", "yellow"),
    focus("terra", "2", "green"),
    focus("cost", "3", "blue")],
    css=TABLE_CSS + '.counts{font-size:44px}.counts td{padding-top:34px;padding-bottom:34px}')

# ---- Chapter: What you can now measure ----------------------------------------------------------------------
EB5 = 'What you can now measure'
framed('s23', EB5, 'One eval, another executor', f'''<div class="cols wide terms">
    {block("b1", "structure", "The eval file", "ran unchanged: setup command, hidden test, tool-calls graders", words=True)}
    {block("b2", "success", "Cost", "filled in, from the runtime’s own usage", words=True)}
    {block("b3", "structure", "Budgets, ranges, comparisons", "these are ordinary trials", words=True)}
  </div>''', [
    focus("b1", "1", "blue"),
    focus("b2", "2", "green"),
    focus("b3", "3", "blue")], css=TERMS + '.terms .title{font-size:40px}')


def beside_row(label, cid, passed, loaded, n, tokens, aiu):
    return (f'<tr><td><span data-concept="{cid}" data-rep="cell">{label}</span></td>'
            f'{cell("p", f"{passed} of {n}")}<td class="num">{loaded} of {n}</td>'
            f'{cell("tok", f"{round(tokens):,}")}{cell("aiu", f"{aiu:.2f}")}</tr>\n')


beside = ''.join(
    beside_row(f'{SHORT[mdl]}, the app', 'approw', count(app(mdl), 'passed'), count(app(mdl), 'loaded'), len(app(mdl)),
               row_tpc(app(mdl)), row_aiu(app(mdl)))
    + beside_row(f'{SHORT[mdl]}, Vally’s executor', 'vxrow', VX[mdl]['passed'], VX[mdl]['loaded'], len(vx(mdl)),
                 row_tpc(vx(mdl)), row_aiu(vx(mdl))) for mdl in MODELS)
framed('s24', EB5, 'The app beside Vally’s executor', f'''<table class="data-table full beside">
    <thead><tr><th>{mono("since-last-release")}</th><th class="num">Passed</th><th class="num">Skill loaded</th>
      <th class="num">Tokens a model call</th><th class="num">AIU a trial</th></tr></thead>
    <tbody>
{beside}    </tbody>
  </table>
  <p class="note">the app: the eval and the experiment · Vally’s executor: our earlier runs of this stimulus{STAND_IN}</p>''', [
    focus("approw", "1~the app has now", "yellow"),
    focus("p", "2", "blue"),
    focus("tok", "3", "blue"),
    focus("aiu", "4", "blue"),
    focus("none", "5")],
    css=TABLE_CSS + '.beside td{padding-top:20px;padding-bottom:20px}.beside th .mono{font-family:var(--font-code)}')

framed('s25', EB5, 'Too few trials to tell', f'''<div class="cols wide terms">
    {block("app", "attention", f"{APP_LOADED} of {APP_N}", f"through the app · {RANGE_APP[0]}% to {RANGE_APP[1]}%")}
    {block("vx", "structure", f"{VX[H]['loaded']} of {len(vx(H))}", f"through Vally’s executor · {RANGE_VX[0]}% to {RANGE_VX[1]}%")}
  </div>
  <p class="lead">trials of {mono(H)} that loaded the skill</p>
  <p class="note"><span data-concept="earlier" data-rep="note">An earlier run: {ER['app'][0]} of {ER['app'][1]} through the app, {ER['vally'][0]} of {ER['vally'][1]} through Vally’s executor</span> · 95% ranges, from the range calculator · the app’s five count its one earlier run{STAND_IN}</p>''', [
    focus("app", "3", "yellow"),
    focus("vx", "4", "blue"),
    focus("none", "5"),
    focus("earlier", "6", "yellow"),
    focus("none", "7")], css=BIG + '.lead{font-size:40px}.lead .mono{font-family:var(--font-code)}')

more_rows = ''.join(
    f'<tr><td class="mono"><span data-concept="{SHORT[mdl]}" data-rep="cell">{mdl}</span></td>'
    f'<td class="num">{round(LOW[mdl]):,}</td><td class="num">{round(HIGH[mdl]):,}</td>{cell("pct", f"+{MORE[mdl]}%")}</tr>\n'
    for mdl in MODELS)
framed('s26', EB5, 'More tokens on every call', f'''<table class="data-table full more">
    <thead><tr><th>Tokens a model call</th><th class="num">The app, lowest trial</th>
      <th class="num">Vally’s executor, highest trial</th><th class="num">The app, on average</th></tr></thead>
    <tbody>
{more_rows}    </tbody>
  </table>
  <p class="note">{mono("since-last-release")} · four trials a model through the app, eight through Vally’s executor{STAND_IN}</p>''', [
    focus("haiku", "2", "yellow"),
    focus("terra", "3", "yellow"),
    focus("pct", "4~sixteen percent", "blue")],
    css=TABLE_CSS + '.more{font-size:44px}.more td{padding-top:34px;padding-bottom:34px}')

framed('s27', EB5, 'Five more tools, every request', f'''<div class="cols wide terms">
    {block("app", "attention", "release-app", f"GitHub’s hosted MCP server is on · {FACTS['mcp_tools']} more tools in every request")}
    {block("own", "structure", "copilot-sdk", "Vally’s own executor · that server is off")}
  </div>
  <div class="quote" data-concept="defn" data-rep="quote"><span class="who">MCP server</span>
    <p>A program that offers an agent extra tools, through a shared protocol: the Model Context Protocol.</p></div>''', [
    focus("defn", "2", "blue"),
    focus("app", "3", "yellow"),
    focus("own", "4", "blue")], css=TERMS + '.terms .semantic-block{min-height:220px}.stage{gap:28px}')

trim = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
trial_rows = ''.join(
    f'<tr><td class="mono"><span data-concept="{SHORT[mdl]}" data-rep="cell">{mdl}</span></td>{cell("calls", trim(CALLS[mdl][0]))}'
    f'{cell("calls", trim(CALLS[mdl][1]))}{cell("cost", f"{AIU[mdl][0]:.2f}")}{cell("cost", f"{AIU[mdl][1]:.2f}")}</tr>\n'
    for mdl in MODELS)
framed('s28', EB5, 'Cost depends on the trial', f'''<table class="data-table full trial">
    <thead>
      <tr><th></th><th class="num" colspan="2">Model calls a trial</th><th class="num" colspan="2">AIU a trial</th></tr>
      <tr><th></th><th class="num">the app</th><th class="num">Vally’s executor</th><th class="num">the app</th><th class="num">Vally’s executor</th></tr>
    </thead>
    <tbody>
{trial_rows}    </tbody>
  </table>
  <p class="note">{mono("since-last-release")} · four trials a model through the app, eight through Vally’s executor{STAND_IN}</p>''', [
    focus("calls", "1", "blue"),
    focus("cost", "2", "blue"),
    focus("terra", "3", "yellow"),
    focus("none", "4")],
    css=TABLE_CSS + '.trial{font-size:44px}.trial td{padding-top:30px;padding-bottom:30px}')

framed('s29', EB5, 'The eval measures what ships', views_table, [
    focus("r2", "0", "yellow")], css=VIEWS_CSS)

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title{w}">{t}</div><div class="label">{l}</div></div>''' for i, (t, l, w) in enumerate([
    ('registerExecutors', 'registers an executor by name', ' mono'),
    ('execute', 'gets the stimulus and the trial’s options, and runs the app', ' mono'),
    ('a trajectory', 'the events, the agent’s reply, the metrics', ' words')], 1))
framed('s30', 'Recap', 'What does a plugin provide?', f'''<div class="semantic-block" id="plugin" data-role="structure">
    <div class="title words">an executor plugin</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#plugin", "at": "1"},
    focus("p1", "1", "blue"),
    focus("p2", "2", "blue"),
    focus("p3", "3", "yellow")], layout='layout-expand',
    css='#plugin{width:100%;padding:36px 40px 44px;gap:24px}'
        '#plugin .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#plugin .part{min-height:300px}#plugin .part .title{font-size:46px;line-height:1.2}'
        '#plugin .part .title.mono{font-family:var(--font-code);font-size:40px}#plugin .part .label{font-size:32px}')

scene('s31', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">The workflow guide</h1>
  <p class="lead">The whole procedure, for a skill or for a feature in an app.</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Writing Custom Executors”</p>
</main>''', [])
print('ok', 'PROVISIONAL (stand-in run)' if PROVISIONAL else f'{RUN_EVAL} · {RUN_EXP}')
