"""Generate lesson 18's scene pages, then insert their file panels.

Same parts as lessons 1 to 8: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout), blocks for
terms, the theme's data table for counts. Nothing here sets a colour or a font outside the theme's
variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/budgets.json                 the tight and wide budgets and the agent limit (one place)
  src/state/changelog.*.eval.yaml        the eval files the tapes install (build-src/make-state.py)
  src/metrics.json                       the metrics block of a real trial record (series' lesson 3 run)
  src/run/s16.log s18.log s21.log s23.log   what vally printed in each terminal scene
  src/run/facts.json                     numbers the logs do not hold (build-src/capture-run.py)
While src/run/PROVISIONAL exists these are stand-ins from the course's verified run.

Every number the narration states is asserted below. If the series' own run differs, this script
fails and the `outcome` sentences (in build-src/make-storyboard.py) are reworded to what happened.

Run from anywhere:  python3 build-src/make-scenes.py
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
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
    r = subprocess.run(['node', str(SKILL / 'scripts/file-panel.js'), *args], cwd=D, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr or r.stdout


def cell(cid, text):
    return f'<td class="num"><span data-concept="{cid}" data-rep="cell">{text}</span></td>'


def table(head, rows, cls='cmp'):
    th = ''.join(f'<th{"" if i == 0 else " class=num"}>{h}</th>' for i, h in enumerate(head))
    tr = ''.join('<tr>' + ''.join(c if c.startswith('<td') else f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data-table full {cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


# ---- The real things, read from src/ -----------------------------------------------------------
read = lambda p: (D / 'src' / p).read_text()
B = json.loads(read('state/budgets.json'))
F = json.loads(read('run/facts.json'))
TIGHT, WIDE, LIMIT = B['tight'], B['wide'], B['agent_limit']
secs = lambda s: float(re.fullmatch(r'([\d.]+)s', s).group(1))
n = lambda v: f'{v:,}'

base, tight, wide, final = (read(f'state/changelog.{k}.eval.yaml') for k in ('base', 'tight', 'wide', 'final'))
GRADERS = re.findall(r'(?m)^        name: (\S+)$', base)
assert len(GRADERS) == 6, GRADERS
SCRIPT_GRADERS = {'two-entries-in-place', 'entry-in-new-unreleased'}
assert SCRIPT_GRADERS <= set(GRADERS)
assert base.count('\n  - name: ') == 5                                              # "all five stimuli"
tl = tight.splitlines()
BUD0 = next(i for i, l in enumerate(tl, 1) if l.strip() == '- type: token-budget')   # first stimulus's budgets
assert [l.strip() for l in tl[BUD0 - 1:BUD0 + 8]] == [
    '- type: token-budget', 'config:', f'max: {TIGHT["tokens"]}', '- type: turn-count', 'config:',
    f'max: {TIGHT["turns"]}', '- type: wall-time', 'config:', f'max: {TIGHT["wall"]}']
GR0 = max(i for i, l in enumerate(tl[:BUD0], 1) if l.strip() == 'graders:')
fl = final.splitlines()
CONS = next(i for i, l in enumerate(fl, 1) if l.strip() == 'constraints:')
assert fl[CONS].strip() == f'max_agent_duration: {LIMIT}' and fl[CONS + 1].strip() == 'agent_environment:'
NAME0 = max(i for i, l in enumerate(fl[:CONS], 1) if l.startswith('  - name: '))
TIMEOUT = re.search(r'(?m)^  timeout: (\S+)$', final).group(1)
assert (LIMIT, TIMEOUT) == ('1m', '3m'), (LIMIT, TIMEOUT)                            # s23, s28: "one minute", "three"

ml = read('metrics.json').splitlines()
ML = {k: next(i for i, l in enumerate(ml, 1) if l.strip().startswith(f'"{k}"')) for k in
      ('metrics', 'totalTokens', 'toolCallCount', 'turnCount', 'wallTimeMs')}

ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|[\x00-\x08\x0b-\x1f]')
log = lambda sid: ANSI.sub('', read(f'run/{sid}.log').replace('\r', ''))
BUDGET = re.compile(r'✗ \[(token-budget|turn-count|wall-time) max (\S+)\] ([\d.]+)(s| tokens| turns) exceeds max of (\S+)')


def regrades(text):
    """The re-grades in a log: each a list of blocks {stim, passed, fails:[(grader, line)], lines, error}."""
    runs, cur = [], None
    for l in text.splitlines():
        if l.startswith('warning: Multiple graders'):
            runs.append([])
            continue
        m = re.match(r'━━━ (\S+) ━━━', l)
        if m:
            if not runs:
                runs.append([])
            cur = {'stim': m.group(1), 'passed': None, 'fails': [], 'lines': [], 'error': False}
            runs[-1].append(cur)
        elif cur is not None and l.strip():
            if 'Stimulus error' in l:      # a trial that ended in ERROR prints this line and no block of its own
                continue
            cur['lines'].append(l)
            if l.startswith('✅') or l.startswith('❌'):
                cur['passed'] = l.startswith('✅')
            g = re.match(r'\s+✗ \[([^\]]+)\]', l)
            if g:
                cur['fails'].append((g.group(1), l))
    assert runs and all(b['passed'] is not None for r in runs for b in r)
    return runs


def over(blocks, variant):
    """Every budget line that failed: (variant, block, grader type, used, unit, max)."""
    out = []
    for b in blocks:
        for g, line in b['fails']:
            m = BUDGET.search(line)
            if m:
                out.append({'variant': variant, 'block': b, 'type': m.group(1), 'used': float(m.group(3)),
                            'unit': m.group(4).strip(), 'max': m.group(2), 'line': line})
            else:
                assert g in SCRIPT_GRADERS, (variant, b['stim'], g)       # nothing else may fail in these runs
    return out


s16 = log('s16')
LINT1, _, GRADE_H = s16.partition('warning: Multiple graders')
(H_T,) = regrades('warning: Multiple graders' + GRADE_H)
(T_T,) = regrades(log('s18'))
T_W, H_W = regrades(log('s21'))
s23 = log('s23')
OV_H, OV_T = over(H_T, 'haiku-high'), over(T_T, 'terra-high')
OV = OV_H + OV_T
failed_trials = lambda ov: len({id(o['block']) for o in ov})
REGRADED = len(H_T) + len(T_T)        # blocks: a trial that ended in ERROR has none

TYP = F['typical']
# ---- What the narration says. If the real run differs, these fail and the sentences change. --------
assert 106000 < TYP['tokens']['value'] < 106700 and TYP['turns']['value'] == 5 and 12.5 <= TYP['seconds']['value'] < 13.5   # s14
assert (TIGHT['tokens'], TIGHT['turns'], TIGHT['wall']) == (107000, 5, '13s')                                # s15
assert TYP['tokens']['value'] <= TIGHT['tokens'] and TYP['turns']['value'] <= TIGHT['turns'] and TYP['seconds']['value'] <= secs(TIGHT['wall'])
assert 'scoring-defaults-applied' in LINT1 and '1 warning(s)' in LINT1 and 'error' not in LINT1.lower()        # s16
assert len(H_T) == 15, len(H_T)                                               # s16: "fifteen blocks"
assert [o['type'] for o in OV_H] == ['token-budget'] and failed_trials(OV_H) == 1                             # s16, s17
H_TWO = OV_H[0]
assert H_TWO['block']['stim'] == 'two-changes' and 0.007 <= (H_TWO['used'] - TIGHT['tokens']) / TIGHT['tokens'] <= 0.013   # s17: "about one percent"
assert [g for g, _ in H_TWO['block']['fails'] if g in SCRIPT_GRADERS] == ['two-entries-in-place']             # s17: "its other failing line"
EARLIER = read('earlier-run-block.txt').rstrip()
assert '107028 tokens exceeds max of 107000' in EARLIER and 'Score: 100.0% | FAILED' in EARLIER               # s17: the page's run
T_TURN = [o for o in OV_T if o['type'] == 'turn-count']
assert len(T_TURN) == 2 and all(o['used'] == 6 for o in T_TURN) and len(OV_T) == 2                            # s18: two turn failures, nothing else
assert failed_trials(OV) == 3 and REGRADED == 30, (failed_trials(OV), REGRADED)                               # s19, s25
assert all(o['used'] - TIGHT['turns'] == 1 for o in T_TURN)                                                   # s19: "one turn more"
assert F['budget_failed_trials_passed_in_the_experiment'] is True                                             # s19: "passed when the experiment ran"
assert (WIDE['tokens'], WIDE['turns'], WIDE['wall']) == (215000, 10, '30s')                                   # s20
assert all(1.8 <= w / t <= 2.4 for w, t in ((WIDE['tokens'], TYP['tokens']['value']), (WIDE['turns'], TYP['turns']['value']),
                                           (secs(WIDE['wall']), TYP['seconds']['value'])))                   # s20: "about twice"
assert not over(T_W, 'terra-high') and not over(H_W, 'haiku-high') and (len(T_W), len(H_W)) == (len(T_T), len(H_T))             # s21, s22
assert any(b['fails'] for b in T_W) and any(b['fails'] for b in H_W)                                          # s21: "only the script graders fail"
LINT2 = s23.split('⚠ No executor')[0]
assert 'error' not in LINT2.lower()                                                                           # s23: "Lint has no errors"
LIVE = F['live']
if PROVISIONAL:
    print('PROVISIONAL: s23 says both models show five of five; the stand-in run has', LIVE['passed'], '- not asserted')
else:
    assert set(LIVE['passed'].values()) == {'5/5'} and LIVE['errors'] == 0, LIVE                               # s23
    assert re.search(r'changelog\s+✓ 5/5\s+✓ 5/5', s23), 'the recorded summary is not five of five twice'
assert 75500 <= LIVE['largest_tokens'] < 76500 and LIVE['largest_turns'] == 5 and LIVE['slowest_seconds'] == 12.5   # s24
assert LIVE['largest_tokens'] < WIDE['tokens'] and LIVE['largest_turns'] <= WIDE['turns'] and LIVE['slowest_seconds'] < secs(WIDE['wall'])
assert F['terra_high_turns_one_stimulus']['turns'] == [4, 5, 6]                                                                      # s25
MT = F['median_tokens_by_model']
assert [round(MT[m] / 1000) for m in ('claude-haiku-5.5', 'claude-haiku-4.5', 'gpt-5.6-terra')] == [105, 75, 61]   # s27
assert F['terra_fewest_tokens_highest_cost'] is True                                                          # s27
assert LIVE['slowest_seconds'] < 30                                                                           # s28: "did nothing"

STAND = ''   # scenes on our lesson 16 run and its re-grades: real since 2026-11-11
STAND_LIVE = ' · stand-in until the paid run is recorded' if PROVISIONAL else ''
TERMS = '.terms .semantic-block{min-height:260px}.terms .label{font-size:34px}'
STATS = ('.stats .semantic-block{min-height:300px;justify-content:center}.stats .title{font-size:96px;line-height:1.1}'
         '.stats .label{font-size:32px}')
CMP = ('.cmp{font-size:50px}.cmp th{font-size:28px}.cmp td{padding-top:24px;padding-bottom:24px}'
       '.cmp td:first-child{font-size:36px}.cmp th:last-child,.cmp td:last-child{padding-right:16px}')

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Put a ceiling on a trial', f'''<div class="cols wide terms">
    {block("right", "structure", "Is the work right?", " · ".join(mono(g) for g in GRADERS), words=True)}
    {block("took", "attention", "What did it take?", "tokens · time · turns · no grader asks", words=True)}
  </div>''', [
    {"type": "focus", "target": "right", "at": "0", "color": "blue"},
    {"type": "focus", "target": "took", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:104px}.terms .semantic-block{min-height:300px}.terms .label{font-size:30px;line-height:1.5}.terms .label .mono{white-space:nowrap}')

# ---- Chapter: A budget is a grader ---------------------------------------------------------------
framed('s02', 'A budget is a grader', 'A budget is a grader', f'''<div class="cols wide terms def">
    {block("def", "structure", "budget", "a limit on what one trial may use", words=True)}
  </div>
  <div class="cols kinds">
    {block("k-tokens", "structure", "tokens", "", words=True)}
    {block("k-time", "structure", "time", "", words=True)}
    {block("k-turns", "structure", "turns", "", words=True)}
    {block("k-tools", "structure", "tool calls", "", words=True)}
  </div>''', [
    {"type": "focus", "target": "def", "at": "1", "color": "blue"},
    {"type": "focus", "target": "k-tokens", "at": "1~tokens", "color": "yellow"},
    {"type": "focus", "target": "k-time", "at": "1~time", "color": "yellow"},
    {"type": "focus", "target": "k-turns", "at": "1~turns", "color": "yellow"},
    {"type": "focus", "target": "k-tools", "at": "1~tool calls", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.def .semantic-block{min-height:190px}.def .label{font-size:36px}'
        '.kinds .semantic-block{min-height:130px;justify-content:center}.kinds .title{font-size:44px}.stage{gap:30px}')

framed('s03', 'A budget is a grader', 'Two kinds of trouble', f'''<div class="cols wide terms">
    {block("loop", "attention", "a loop", "one trial gone wrong", words=True)}
    {block("reg", "change", "a cost regression", "an edit makes every trial read more, or take longer", words=True)}
  </div>''', [
    {"type": "focus", "target": "loop", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "reg", "at": "2", "color": "orange"},
    {"type": "focus", "target": "none", "at": "3"}], css=TERMS)

framed('s04', 'A budget is a grader', 'Measure first, then set it', f'''<div class="cols terms">
    {block("low", "failure", "too low", "fails good work", words=True)}
    {block("high", "failure", "too high", "can never fail", words=True)}
    {block("meas", "success", "measured", "set from real trials · tested on a saved run", words=True)}
  </div>''', [
    {"type": "focus", "target": "low", "at": "1", "color": "red"},
    {"type": "focus", "target": "high", "at": "2", "color": "red"},
    {"type": "focus", "target": "meas", "at": "3", "color": "green"}], css=TERMS)

framed('s05', 'A budget is a grader', 'Not too much, and right', f'''<div class="cols wide terms">
    {block("b-says", "attention", "“not too much”", "a budget says", words=True)}
    {block("g-say", "success", "“and it was right”", "only the other graders say", words=True)}
  </div>
  <p class="note">a trial that gives up after one turn is inside every budget</p>''', [
    {"type": "focus", "target": "b-says", "at": "2~not too much", "color": "yellow"},
    {"type": "focus", "target": "g-say", "at": "2~other graders", "color": "green"}], css=TERMS)

# ---- Chapter: Budget graders ---------------------------------------------------------------------
framed('s06', 'Budget graders', 'Four graders, one number each', f'''<div class="annotated">
    {panel('metrics')}
    {callouts(('tok', mono('token-budget')), ('tools', mono('tool-call-count')), ('turns', mono('turn-count')), ('wall', mono('wall-time')))}
  </div>''', [
    {"type": "focus", "target": "tok", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "turns", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "wall", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "tools", "at": "5", "color": "blue"}],
    layout='layout-file', css='.callout{font-size:32px}')

framed('s07', 'Budget graders', 'A turn is one reply', f'''<div class="cols wide terms">
    {block("conv", "structure", "a turn in a conversation", "one request", words=True)}
    {block("trial", "attention", "a turn in a trial", "one reply from the model", words=True)}
  </div>
  <p class="note">one request, several replies · {mono("turn-count")} counts the replies</p>''', [
    {"type": "focus", "target": "conv", "at": "1", "color": "blue"},
    {"type": "focus", "target": "trial", "at": "1~here", "color": "yellow"}], css=TERMS)

framed('s08', 'Budget graders', 'Three budgets, no names', f'''<div class="annotated">
    {panel('budgets')}
    {callouts(('type', 'no name: named from its type and limit'), ('max', 'passes at or under max'), ('time', 'a time has its unit'))}
  </div>''', [
    {"type": "focus", "target": "max", "at": "1", "color": "blue"},
    {"type": "scroll", "target": "#budgets", "to": "end", "at": "2"},
    {"type": "focus", "target": "time", "at": "2", "color": "yellow"},
    {"type": "scroll", "target": "#budgets", "to": "top", "at": "3"},
    {"type": "focus", "target": "type", "at": "3", "color": "orange"}],
    layout='layout-file', css='.callout{font-size:32px}')

framed('s09', 'Budget graders', 'Free to test', f'''<div class="cols wide terms">
    {block("scriptg", "failure", "script grader", "needs the workspace, which is gone · fails every trial in a re-grade", words=True)}
    {block("budg", "success", "budget grader", "reads the saved trial record · judged exactly as in a real run", words=True)}
  </div>''', [
    {"type": "focus", "target": "budg", "at": "0", "color": "green"},
    {"type": "focus", "target": "scriptg", "at": "1~script grader", "color": "red"},
    {"type": "focus", "target": "budg", "at": "2", "color": "green"}], css=TERMS)

framed('s10', 'Budget graders', 'Over is over', f'''<div class="cols wide terms">
    {block("score", "structure", "the score", "falls in proportion to the overrun", words=True)}
    {block("verdict", "failure", "the verdict", "fails, however small the overrun", words=True)}
  </div>''', [
    {"type": "focus", "target": "score", "at": "1", "color": "blue"},
    {"type": "focus", "target": "verdict", "at": "2", "color": "red"}], css=TERMS)

# ---- Chapter: Limits that stop the agent ---------------------------------------------------------
framed('s11', 'Limits that stop the agent', 'A limit that stops the agent', f'''<div class="annotated">
    {panel('constraints')}
    {callouts(('cons', 'limits for this stimulus'), ('mad', 'stop the agent, then grade'))}
  </div>
  <p class="note">in the trial record: {mono("endReason")} says {mono("agent_timeout")}, not {mono("completed")}</p>''', [
    {"type": "focus", "target": "cons", "at": "1", "color": "blue"},
    {"type": "focus", "target": "mad", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    layout='layout-file', css='.callout{font-size:32px}')

framed('s12', 'Limits that stop the agent', 'Three limits, three behaviours', f'''<div class="cols terms limits">
    {block("mad", "success", "max_agent_duration", "stops the agent · grades its partial work")}
    {block("md", "failure", "max_duration", "a hard limit · the trial is stopped, and fails")}
    {block("mt", "attention", "max_turns", "the most turns · what happens at the limit is not documented")}
  </div>''', [
    {"type": "focus", "target": "mad", "at": "1", "color": "green"},
    {"type": "focus", "target": "md", "at": "2", "color": "red"},
    {"type": "focus", "target": "mt", "at": "5", "color": "yellow"}],
    css='.limits .semantic-block{min-height:300px}.limits .title{font-size:38px}.limits .label{font-size:32px}')

# ---- Chapter: Set budgets from your runs ---------------------------------------------------------
framed('s13', 'Set budgets from your runs', 'Tested before they are trusted', f'''<div class="cols steps">
    {block("st1", "structure", "measure", "what a typical trial used", step=1, words=True)}
    {block("st2", "change", "set", "budgets just above it", step=2, words=True)}
    {block("st3", "attention", "test", "on saved trials · no agent", step=3, words=True)}
    {block("st4", "success", "adjust", "then a time limit, and one run", step=4, words=True)}
  </div>''', [
    {"type": "focus", "target": "st1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "st2", "at": "2", "color": "orange"},
    {"type": "focus", "target": "st3", "at": "2~test", "color": "yellow"},
    {"type": "focus", "target": "st4", "at": "3", "color": "green"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.steps .semantic-block{min-height:330px}.steps .label{font-size:32px}')

where = lambda t, what: what + (' · ' + mono(' · '.join(x for x in (t.get('variant'), t.get('stimulus')) if x)) if t.get('variant') else '')
framed('s14', 'Set budgets from your runs', 'What a typical trial used', f'''<div class="cols terms stats">
    {block("tok", "structure", n(TYP['tokens']['value']), where(TYP['tokens'], 'tokens'))}
    {block("turns", "structure", TYP['turns']['value'], where(TYP['turns'], 'turns'))}
    {block("secs", "structure", f"{TYP['seconds']['value']} s", where(TYP['seconds'], 'duration'))}
  </div>
  <p class="note">the largest median in each column of {mono("report.md")}, across the four variants · our run {F['l16_run']}{STAND}</p>''', [
    {"type": "focus", "target": "tok", "at": "2~tokens", "color": "yellow"},
    {"type": "focus", "target": "turns", "at": "2~turns", "color": "yellow"},
    {"type": "focus", "target": "secs", "at": "2~seconds", "color": "yellow"}],
    css=STATS.replace('96px', '84px') + '.stats .label{line-height:1.5}')

ROWS = [('tokens', n(TYP['tokens']['value']), TIGHT['tokens'], WIDE['tokens']),
        ('turns', TYP['turns']['value'], TIGHT['turns'], WIDE['turns']),
        ('time', f"{TYP['seconds']['value']} s", TIGHT['wall'], WIDE['wall'])]
framed('s15', 'Set budgets from your runs', 'Budgets just above typical', table(
    ['', 'largest typical', 'first budget'],
    [[k, f'<td class="num">{t}</td>', cell(f'b-{k}', mono(b))] for k, t, b, _ in ROWS]) +
    f'\n  <p class="note">{mono("max")} of {mono("token-budget")}, {mono("turn-count")} and {mono("wall-time")}, under each of the five stimuli{STAND}</p>', [
    {"type": "focus", "target": "b-tokens", "at": "1~tokens", "color": "yellow"},
    {"type": "focus", "target": "b-turns", "at": "1~turns", "color": "yellow"},
    {"type": "focus", "target": "b-time", "at": "1~seconds", "color": "yellow"}], css=CMP)


def shown(o_list, ids):
    """The blocks that name a budget, as printed, with the budget and script-grader lines marked."""
    out, seen = [], []
    for o in o_list:
        if any(o['block'] is b for b in seen):
            continue
        seen.append(o['block'])
        stim = o['block']['stim']
        for l in o['block']['lines']:
            g = re.match(r'\s+✗ \[([^\]]+)\]', l)
            key = (stim, 'budget') if BUDGET.search(l) else (stim, 'script') if g and g.group(1) in SCRIPT_GRADERS else None
            if key in ids:
                pad = len(l) - len(l.lstrip())
                out.append(l[:pad] + f'⟦{ids[key]}:{l[pad:]}⟧')
            else:
                out.append(l)
        out.append('')
    return '\n'.join(out).rstrip()


EARLIER_SHOWN = '\n'.join(f'⟦e-score:{l}⟧' if l.startswith('Score') else l for l in EARLIER.splitlines() if l.strip())
framed('s17', 'Set budgets from your runs', 'Barely over, and failed', f'''<div class="lists">
    {card('ours', f'our {mono("haiku-high")} re-grade · the block that names a budget, as printed',
          code(shown(OV_H, {('two-changes', 'budget'): 'tb-two', ('two-changes', 'script'): 'sg'}), 'text'))}
    {card('earlier', 'an earlier run · a trial 28 tokens over', code(EARLIER_SHOWN, 'text'))}
  </div>''', [
    {"type": "focus", "target": "tb-two", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "sg", "at": "2", "color": "blue"},
    {"type": "focus", "target": "e-score", "at": "3", "color": "red"}],
    css='.lists{display:flex;flex-direction:column;gap:26px;width:100%}'
        '.lists .card > .code.dark{font-size:31px;line-height:1.5;padding:20px 30px}.lists .card .who{font-size:30px}')


def fail_rows():
    rows, seen = [], []
    for o in OV:
        if any(o['block'] is b for b in seen):
            continue
        seen.append(o['block'])
        mine = [x for x in OV if x['block'] is o['block']]
        kind = 'tok' if mine[0]['type'] == 'token-budget' else 'turn'
        used = ' · '.join((n(int(x['used'])) if x['unit'] != 's' else f"{x['used']}") + ('s' if x['unit'] == 's' else ' ' + x['unit']) for x in mine)
        rows.append([mono(o['block']['stim']), f'<td>{mono(o["variant"])}</td>', f'<td>{" · ".join(mono(x["type"]) for x in mine)}</td>',
                     cell(kind, used), f'<td class="num">{" · ".join(x["max"] for x in mine)}</td>'])
    return rows


framed('s19', 'Set budgets from your runs', 'Wrong budgets, or wrong trials?', table(
    ['stimulus', 'variant', 'budget', 'used', 'max'], fail_rows(), cls='cmp fails') +
    f'\n  <p class="note">every trial a budget failed, of the {REGRADED} saved trials we re-graded{STAND}</p>', [
    {"type": "focus", "target": "tok", "at": "3~token", "color": "yellow"},
    {"type": "focus", "target": "turn", "at": "3~turn", "color": "blue"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.fails{font-size:34px}.fails th{font-size:26px}.fails td{padding-top:18px;padding-bottom:18px}'
        '.fails th:nth-child(2),.fails th:nth-child(3){text-align:left}.fails th:last-child,.fails td:last-child{padding-right:16px}')

framed('s20', 'Set budgets from your runs', 'Room for normal variation', table(
    ['', 'largest typical', 'first budget', 'wider budget'],
    [[k, f'<td class="num">{t}</td>', f'<td class="num">{mono(b)}</td>', cell(f'w-{k}', mono(w))] for k, t, b, w in ROWS]) +
    f'\n  <p class="note">each budget raised to about twice the largest typical value{STAND}</p>', [
    {"type": "focus", "target": "w-tokens", "at": "1~tokens", "color": "yellow"},
    {"type": "focus", "target": "w-turns", "at": "1~turns", "color": "yellow"},
    {"type": "focus", "target": "w-time", "at": "1~seconds", "color": "yellow"}], css=CMP)

cnt = lambda ov, t: len({id(o['block']) for o in ov if o['type'] == t})
OV_W = over(T_W, 'terra-high') + over(H_W, 'haiku-high')
framed('s22', 'Set budgets from your runs', 'Three trials, then none', table(
    ['trials that failed', mono('token-budget'), mono('turn-count'), mono('wall-time'), 'any budget'],
    [['with the first budgets'] + [f'<td class="num">{cnt(OV, t)}</td>' for t in ('token-budget', 'turn-count', 'wall-time')] + [cell('f-any', failed_trials(OV))],
     ['with the wider budgets'] + [f'<td class="num">{cnt(OV_W, t)}</td>' for t in ('token-budget', 'turn-count', 'wall-time')] + [cell('w-any', failed_trials(OV_W))]]) +
    f'\n  <p class="note">the same {REGRADED} saved trials, re-graded twice · no agent ran{STAND}</p>', [
    {"type": "focus", "target": "f-any", "at": "0~three", "color": "yellow"},
    {"type": "focus", "target": "w-any", "at": "0~every", "color": "green"}], css=CMP)

framed('s24', 'Set budgets from your runs', 'Nothing near a limit', table(
    ['', 'largest in this run', 'budget', 'limit'],
    [['tokens', cell('l-tok', n(LIVE['largest_tokens'])), f'<td class="num">{mono(WIDE["tokens"])}</td>', '<td class="num"></td>'],
     ['turns', cell('l-turn', LIVE['largest_turns']), f'<td class="num">{mono(WIDE["turns"])}</td>', '<td class="num"></td>'],
     ['time', cell('l-time', f"{LIVE['slowest_seconds']} s"), f'<td class="num">{mono(WIDE["wall"])}</td>', cell('lim', mono(LIMIT))]]) +
    f'\n  <p class="note">from our run · {LIVE["run"]}{STAND_LIVE}</p>', [
    {"type": "focus", "target": "l-tok", "at": "0~tokens", "color": "yellow"},
    {"type": "focus", "target": "l-turn", "at": "0~turns", "color": "yellow"},
    {"type": "focus", "target": "l-time", "at": "0~slowest", "color": "yellow"},
    {"type": "focus", "target": "lim", "at": "1~one-minute", "color": "blue"}], css=CMP)

# ---- Chapter: What the limits caught -------------------------------------------------------------
turns = F['terra_high_turns_one_stimulus']['turns']
framed('s25', 'What the limits caught', 'Typical is a middle value', f'''<div class="cols wide terms stats">
    {block("five", "attention", f"{failed_trials(OV)} of {REGRADED}", "good trials the first budgets failed")}
    {block("spread", "structure", ', '.join(map(str, turns[:-1])) + f' or {turns[-1]}', f'turns {mono("terra-high")} took for the same request')}
  </div>
  <p class="note">a typical trial is the median: half of all trials are above it{STAND}</p>''', [
    {"type": "focus", "target": "five", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"},
    {"type": "focus", "target": "spread", "at": "4", "color": "blue"},
    {"type": "focus", "target": "none", "at": "5"}], css=STATS)

framed('s26', 'What the limits caught', 'Room above normal', f'''<p class="lead">a budget at about twice the largest typical trial</p>
  <div class="cols wide terms">
    {block("runaway", "failure", "a loop, at ten times the usual", "fails", words=True)}
    {block("onemore", "success", "one turn more than usual", "passes", words=True)}
  </div>''', [
    {"type": "focus", "target": "runaway", "at": "1", "color": "red"},
    {"type": "focus", "target": "onemore", "at": "2", "color": "green"},
    {"type": "focus", "target": "none", "at": "3"}], css=TERMS + '.terms .label{font-size:44px}.stage{gap:30px}')

MODELS = [('claude-haiku-5.5', 'm55'), ('claude-haiku-4.5', 'm45'), ('gpt-5.6-terra', 'mt')]
framed('s27', 'What the limits caught', 'What a token budget doesn’t do', f'''<div class="cols wide split">
    {table(['model', 'tokens in a typical trial'], [[mono(m), cell(c, 'about ' + n(round(MT[m] / 1000) * 1000))] for m, c in MODELS], cls='cmp models')}
    <div class="terms stats">{block("bud", "attention", n(WIDE['tokens']), 'one token budget, for every model')}</div>
  </div>
  <p class="note">from our runs{STAND_LIVE}</p>''', [
    {"type": "focus", "target": "m55", "at": "2~five point five", "color": "yellow"},
    {"type": "focus", "target": "m45", "at": "2~four point five", "color": "yellow"},
    {"type": "focus", "target": "mt", "at": "2~terra", "color": "yellow"},
    {"type": "focus", "target": "bud", "at": "3", "color": "blue"},
    {"type": "focus", "target": "mt", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.split{align-items:center}.models{font-size:40px}.models th{font-size:28px}.models td{padding-top:22px;padding-bottom:22px}'
        '.models td:first-child{font-size:34px}.models th:last-child,.models td:last-child{padding-right:16px}'
        + STATS.replace('96px', '80px').replace('300px', '260px'))

framed('s28', 'What the limits caught', 'A limit for the bad day', f'''<div class="cols wide terms stats">
    {block("lim", "success", LIMIT, mono("max_agent_duration") + ' · stop the agent, grade what it wrote')}
    {block("to", "structure", TIMEOUT, 'the file’s ' + mono("timeout"))}
  </div>''', [
    {"type": "focus", "target": "lim", "at": "0", "color": "green"},
    {"type": "focus", "target": "to", "at": "2~timeout", "color": "blue"}], css=STATS + '.stats .label{line-height:1.5}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('a budget grader', 'judges the finished trial · by then the cost is spent'),
    ('a limit under constraints', 'acts while the agent works · stops it')], 1))
framed('s29', 'Recap', 'Budget, or limit?', f'''<div class="semantic-block" id="kind" data-role="structure">
    <div class="title words">a ceiling on a trial</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#kind", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "yellow"}], layout='layout-expand',
    css='#kind{width:100%;padding:36px 40px 44px;gap:24px}'
        '#kind .parts{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;width:100%}'
        '#kind .part{min-height:280px}#kind .part .title{font-size:52px;line-height:1.2}'
        '#kind .part .label{font-size:32px}')

scene('s30', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Is it worse than before</h1>
  <p class="lead">Can a check say “no worse than before”, in quality and in cost?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Graders: metric thresholds”</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')

# ---- File panels (the generator above cleared them) ----------------------------------------------
fp('--file', 'src/metrics.json', '--label', 'results.jsonl · one trial’s metrics', '--id', 'metrics',
   '--width', '40', '--rows', '9',
   '--show', f"{ML['metrics']},{ML['totalTokens']},{ML['toolCallCount']},{ML['turnCount']}-{ML['wallTimeMs']}",
   '--expect', f"{ML['totalTokens']}=totalTokens",
   '--mark', f"{ML['totalTokens']}=tok", '--mark', f"{ML['toolCallCount']}=tools",
   '--mark', f"{ML['turnCount']}=turns", '--mark', f"{ML['wallTimeMs']}=wall", '--into', 'scenes/s06.html')
fp('--file', 'src/state/changelog.tight.eval.yaml', '--label', 'evals/changelog.eval.yaml', '--id', 'budgets',
   '--width', '40', '--rows', '9', '--show', f'{BUD0}-{BUD0 + 8}', '--expect', f'{BUD0}=token-budget',
   '--mark', f'{BUD0}=type', '--mark', f'{BUD0 + 2}=max', '--mark', f'{BUD0 + 8}=time', '--into', 'scenes/s08.html')
fp('--file', 'src/state/changelog.final.eval.yaml', '--label', 'evals/changelog.eval.yaml', '--id', 'constraints',
   '--width', '40', '--rows', '8', '--show', f'{NAME0}-{NAME0 + 1},{CONS}-{CONS + 2}', '--expect', f'{CONS}=constraints',
   '--mark', f'{CONS}=cons', '--mark', f'{CONS + 1}=mad', '--into', 'scenes/s11.html')
print('ok' + (' (PROVISIONAL stand-ins)' if PROVISIONAL else ''))
