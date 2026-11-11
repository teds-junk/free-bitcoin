"""Generate lesson 21's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/   the files the tapes install into the practice folder (build-src/make-state.py)
  src/run/     what the recordings printed and what earlier videos' runs found. Until this video's
               tapes are recorded these are stand-ins: see src/run/PROVISIONAL.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
RUN = D / 'src/run'
H, T = MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
SHORT = {H: 'haiku', T: 'terra'}
BUDGET_GRADERS = ('token-budget', 'turn-count', 'wall-time')
PROVISIONAL = (RUN / 'PROVISIONAL').exists()
RUN_NOTE = 'STAND-IN: the course’s verified run, not yet ours' if PROVISIONAL else 'our run'


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


def mono(t):
    return f'<span class="mono">{t}</span>'


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>'


def thousands(n):
    return f'{n:,}'


TABLE_CSS = ('.data-table{font-size:38px}.data-table th{font-size:30px}.data-table td{padding-top:24px;padding-bottom:24px}'
             '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:34px}')
TERMS = '.terms .semantic-block{min-height:260px}.terms .label{font-size:34px}'

# ---- Read what the recordings printed ------------------------------------------------------------------
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\r')


def log(name):
    return ANSI.sub('', (RUN / f'{name}.log').read_text()).splitlines()


def exit_code(name):
    return int((RUN / f'{name}.exit').read_text().strip())


ROW = re.compile(r'^\s+(\w[\w-]*)\s+([✓✘])\s+(\d+)/(\d+)\s+([✓✘])\s+(\d+)/(\d+)\s*$')
FAILED = re.compile(r'^\s+(✘|ERROR)\s+(\w[\w-]*) · (\S+) \[([^\]]+)\]\s+(.*)$')


def summary(lines):
    """-> {eval: {model: (passed, total)}} from the table at the end of a vally eval run."""
    i = [k for k, l in enumerate(lines) if re.match(r'^\s+eval\s+' + re.escape(H) + r'\s+' + re.escape(T), l)][-1]
    out = {}
    for l in lines[i + 1:]:
        m = ROW.match(l)
        if not m:
            break
        out[m.group(1)] = {H: (int(m.group(3)), int(m.group(4))), T: (int(m.group(6)), int(m.group(7)))}
    return out


def failures(lines):
    """-> [(kind, eval, stimulus, model, text)] from the Failures list of a vally eval run."""
    heads = [k for k, l in enumerate(lines) if l.startswith('Failures')]
    return [m.groups() for m in map(FAILED.match, lines[heads[-1]:] if heads else []) if m]


def blocks(lines):
    """-> [(stimulus, passed, [(grader, evidence)], score)] from a vally grade re-grade."""
    out, cur = [], None
    for l in lines:
        if m := re.match(r'^━━━ (\S+) ━━━$', l):
            cur = [m.group(1), None, [], None]
            out.append(cur)
        elif cur is None:
            continue
        elif l.startswith('✅'):
            cur[1] = True
        elif l.startswith('❌'):
            cur[1] = False
            cur.append(l)
        elif m := re.match(r'^\s+✗ \[([^\]]+)\] (.*)$', l):
            cur[2].append((m.group(1), m.group(2)))
        elif m := re.match(r'^Score: ([\d.]+)% \| (PASSED|FAILED)$', l):
            cur[3] = m.group(1)
    assert all(b[1] is not None for b in out), 'a block with no verdict line'
    return out


budget = json.loads((RUN / 'budget.json').read_text())
MAX, LOWERED = budget['max'], budget['lowered']
lint, quick, regrade, lowered, full = (log(n) for n in ('lint', 'quick', 'regrade', 'lowered', 'full'))
Q, F = summary(quick), summary(full)
F_FAILS = failures(full)
# Our FIRST take of the full suite, minutes before the kept one: two sessions dropped (ERROR) and one real FAIL.
# Saved as evidence in src/earlier/ (README there); s19 and s24 show it as our first run.
first = ANSI.sub('', (D / 'src/earlier/full-take1.log').read_text()).splitlines()
F1, F1_FAILS = summary(first), failures(first)
F1_EXIT = int((D / 'src/earlier/full-take1.exit').read_text().strip())
RG, LW = blocks(regrade), blocks(lowered)
budget_only = [b for b in LW if not b[1] and b[2] and all(g.split()[0] == 'token-budget' for g, _ in b[2])]
over_tokens = [int(re.match(r'(\d+) tokens', ev).group(1)) for b in budget_only for _, ev in b[2]]

if (RUN / 'quick/results.jsonl').exists() and (RUN / 'full/results.jsonl').exists():
    def trials(which):
        ts = [json.loads(l) for l in (RUN / which / 'results.jsonl').read_text().splitlines() if l.strip()]
        return [t for t in ts if t.get('type') == 'trial-result']
    aiu = lambda t: t['trajectory']['metrics']['tokenUsage']['cost']['amount'] / 1e9
    qt, ft = trials('quick'), [t for t in trials('full') if t['status'] == 'success']
    COST = {'quick': {'trials': len(qt), 'aiu': sum(map(aiu, qt)),
                      'largest_tokens': max(t['trajectory']['metrics']['tokenUsage']['totalTokens'] for t in qt)},
            'full': {'finished': len(ft), 'aiu': sum(map(aiu, ft)),
                     'judge_calls': sum(t['evalName'] == 'wording' for t in ft)}}
else:
    assert PROVISIONAL, 'src/run/quick/results.jsonl and full/results.jsonl are missing: run build-src/collect-run.sh'
    COST = json.loads((RUN / 'costs.json').read_text())
STANDING = json.loads((RUN / 'standing.json').read_text())
L19 = json.loads((RUN / 'l19.json').read_text())
L16 = json.loads((RUN / 'l16.json').read_text())

state = (D / 'src/state/changelog.eval.yaml').read_text().splitlines()
low = (D / 'src/state/changelog.lowered.eval.yaml').read_text().splitlines()
suites = (D / 'src/state/.vally.yaml').read_text()
conv = (D / 'src/state/CONVENTIONS.md').read_text().splitlines()

# ---- What the narration says. If a recording changes these, the sentences change too. -------------------
# s06: five stimuli carry the tag.
assert sum(l.strip() == 'tags: { tier: quick }' for l in state) == 5
# s07: two suites; quick draws on one eval file with a filter; full lists four with none.
assert suites.count('evals/') == 5 and suites.count('filter:') == 1 and len(suites.splitlines()) == 13
# s09: the screen carries the three budgets (the voice names what each guards); "stopped after a minute".
assert MAX == 215000 and state[16].strip() == 'max_agent_duration: 1m', (MAX, state[16])
assert [state[i].strip() for i in (34, 37, 40)] == [f'max: {MAX}', 'max: 10', 'max: 30s'], state[32:41]
# s11: "In our run, the range reached just above zero, so the command exited with zero. In an earlier run of the
#      same comparison, the whole range was below zero, and it exited with one."
assert L19['ours']['exit'] == 0 and 0 < L19['ours']['hi'] < 0.2 and L19['ours']['lo'] < 0, L19
assert L19['earlier']['exit'] == 1 and L19['earlier']['hi'] < 0, L19
# s13: "one warning, the usual one about scoring defaults, and no errors"; "every stimulus has passed on both
#      models"; "Zero: nothing failed."
assert any('1 warning(s)' in l for l in lint) and any('scoring-defaults-applied' in l for l in lint) \
    and not any('error' in l.lower() for l in lint), lint
assert Q == {'changelog': {H: (5, 5), T: (5, 5)}} and exit_code('quick') == 0, (Q, exit_code('quick'))
# s14: "failing blocks"; "Every budget passed all eighteen trials; only the graders of the result failed";
#      "One: a failing verdict is now an error."
assert len(RG) == 18 and any(not b[1] for b in RG) and exit_code('regrade') == 1, (len(RG), exit_code('regrade'))
assert not [g for b in RG for g, _ in b[2] if g.split()[0] in BUDGET_GRADERS], 'a budget failed in the plain re-grade'
# s15: "seventy thousand, which is below what those trials used".
assert LOWERED == 70000 and low[34].strip() == f'max: {LOWERED}' and over_tokens and min(over_tokens) > LOWERED
# s16: "It's one again."   s17: "These typo fix trials passed every grader a moment ago; now they fail, on the
#      budget alone." "Seventy-four thousand tokens ..." "ninety-eight point eight percent".
assert exit_code('lowered') == 1 and len(LW) == 18
passed_before = sum(b[0] == 'typo-fix' and b[1] for b in RG)
assert budget_only and all(b[0] == 'typo-fix' for b in budget_only) and len(budget_only) == passed_before, \
    (len(budget_only), passed_before)
assert all(round(n / 1000) == 74 for n in over_tokens) and all(b[3] == '98.8' for b in budget_only), (over_tokens, budget_only)
# s18: "every stimulus has passed on both models, in all four files"; "Zero again: nothing failed".
assert list(F) == ['changelog', 'conversation', 'loading', 'wording'] and exit_code('full') == 0, (F, exit_code('full'))
assert all(p == t for e in F.values() for p, t in e.values()) and not F_FAILS, (F, F_FAILS)
FULL_STIMULI = sum(t for e in F.values() for p, t in e.values())
# s19: our first run: "On haiku, two trials ended in error, because their sessions dropped"; "on terra, a question
#      that shouldn't load the skill did load it"; three stimuli listed; "that run did" exit with one.
assert sorted((k, e, s_, m) for k, e, s_, m, _ in F1_FAILS) == [
    ('ERROR', 'conversation', 'three-requests', H), ('ERROR', 'wording', 'cache', H),
    ('✘', 'loading', 'skip-question', T)], F1_FAILS
assert all('disconnected' in t for k, *_, t in F1_FAILS if k == 'ERROR') and F1_EXIT == 1
assert any(k == '✘' and t.startswith('skill-invocation forbids') for k, *_, t in F1_FAILS)
assert sum(t - p for e in F1.values() for p, t in e.values()) == 3, F1
# s21: "one pair of stimulus and model passed, out of six".
assert (STANDING['first_graders']['pairs_passed'], STANDING['first_graders']['pairs']) == (1, 6)
# s22: "ten trials cost about twenty-four AIU"; "thirty trials cost about sixty-seven AIU, with its
#      six judge calls"; "the largest used ninety-one thousand tokens, against two hundred fifteen thousand".
assert COST['quick']['trials'] == 10 and round(COST['quick']['aiu']) == 24, COST
assert COST['full']['finished'] == 30 and round(COST['full']['aiu']) == 67 and COST['full']['judge_calls'] == 6, COST
assert round(COST['quick']['largest_tokens'] / 1000) == 91 and COST['quick']['largest_tokens'] < MAX
# s23: "passed all fifteen of its trials ... at about a fifth of an AIU each"; "about one AIU an edit".
assert L16['passed'] == L16['trials'] == 15 and 0.15 <= L16['aiu_per_passing'] <= 0.25
assert round(L16['aiu_per_passing'] * L16['quick_stimuli']) == 1
# s21: "In our last run, every stimulus in them passed on both models" (asserted for s18 above).
# s24: "the same loading question failed on terra the first time, and passed the second".
assert F1['loading'][T] == (5, 6) and F['loading'][T] == (6, 6)

# ---- Hook ------------------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'Keep it working', f'''<div class="cols wide terms">
    {block('b1', 'structure', 'After every edit', 'one short command', words=True)}
    {block('b2', 'structure', 'Before sharing', 'a longer one', words=True)}
    {block('b3', 'attention', 'For the team', 'one page', words=True)}
  </div>''', [
    {"type": "focus", "target": "b1", "at": "3~one short command", "color": "blue"},
    {"type": "focus", "target": "b2", "at": "3~longer one", "color": "blue"},
    {"type": "focus", "target": "b3", "at": "3~one page", "color": "yellow"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.terms .semantic-block{min-height:250px}.terms .label{font-size:36px}')

# ---- Chapter: Cheapest check first -----------------------------------------------------------------------
EB1 = 'Cheapest check first'
CHECKS = [('free', 'lint', 'free'), ('free', 'oracle', 'free'), ('free', 're-grade', 'free'),
          ('quick', 'quick', '10 agent runs'), ('full', 'full', '30 agent runs')]
framed('s02', EB1, 'Five checks, cheapest first', f'''<div class="cols five">
    {''.join(block(c, 'structure' if c == 'free' else 'attention', mono(t), l) for c, t, l in CHECKS)}
  </div>
  <p class="note">agent runs, on two models · re-grading a judge spends one judge call per trial</p>''', [
    {"type": "focus", "target": "free", "at": "2", "color": "blue"},
    {"type": "focus", "target": "quick", "at": "3~quick run", "color": "yellow"},
    {"type": "focus", "target": "full", "at": "3~full run", "color": "yellow"},
    {"type": "focus", "target": "quick", "at": "4~ten", "color": "yellow"},
    {"type": "focus", "target": "full", "at": "4~thirty", "color": "yellow"}],
    css='.five{gap:24px}.five .semantic-block{min-height:240px;justify-content:center}'
        '.five .title{font-size:44px}.five .label{font-size:32px}')

MATCH = [('r1', 'vally lint', 'Is the eval file well formed?', 'editing an eval file'),
         ('r2', 'vally oracle', 'Do graders pass correct work, and fail an untouched file?', 'changing a grader'),
         ('r3', 'vally grade', 'What do today’s graders say about saved trials?', 'changing a pattern, budget or rubric'),
         ('r4', 'quick', 'Did the edit break a code check, or a budget?', 'every edit to the skill'),
         ('r5', 'full', 'Does everything still hold?', 'sharing · a model change')]
framed('s03', EB1, 'Match the check to the question', f'''<table class="data-table full match">
    <thead><tr><th>Check</th><th>Answers</th><th>After</th></tr></thead>
    <tbody>
{''.join(f'<tr><td class="mono">{cell(c, n)}</td><td>{q}</td><td>{w}</td></tr>' + chr(10) for c, n, q, w in MATCH)}    </tbody>
  </table>''', [
    {"type": "focus", "target": "r1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "r2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "r3", "at": "3", "color": "blue"},
    {"type": "focus", "target": "r4", "at": "6", "color": "yellow"},
    {"type": "focus", "target": "r5", "at": "7", "color": "yellow"}],
    css='.match{font-size:34px}.match th{font-size:28px}.match td{padding-top:16px;padding-bottom:16px}.stage{justify-content:center}'
        '.match td.mono{font-family:var(--font-code);font-size:32px;white-space:nowrap}')

framed('s04', EB1, 'Three checks for one-off questions', f'''<div class="cols wide terms">
    {block('o1', 'structure', 'With and without the skill', 'after a large rewrite', words=True)}
    {block('o2', 'structure', 'Before and after, then ' + mono('vally compare'), 'did an edit help, or hurt?', words=True)}
    {block('o3', 'structure', 'Cost per passing trial', 'before changing model or effort', words=True)}
  </div>''', [
    {"type": "focus", "target": "o1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "o2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "o3", "at": "3", "color": "blue"}],
    css=TERMS + '.terms .title{font-size:40px;line-height:1.25}')

AGREE = [('a1', 'What deserves a grader?'), ('a2', 'Where do grading files go?'),
         ('a3', 'How is a result reported?'), ('a4', 'What may a run cost?')]
framed('s05', EB1, 'What drifts is agreement', f'''<div class="grid2">
    {''.join(f'<div class="semantic-block" data-concept="{c}" data-rep="block" data-role="structure"><div class="title words">{t}</div></div>' for c, t in AGREE)}
  </div>
  <p class="lead"><span data-concept="page" data-rep="note">One page, written down while it is fresh</span></p>''', [
    {"type": "focus", "target": "a1", "at": "1~what deserves", "color": "blue"},
    {"type": "focus", "target": "a2", "at": "1~where grading", "color": "blue"},
    {"type": "focus", "target": "a3", "at": "1~how a result", "color": "blue"},
    {"type": "focus", "target": "a4", "at": "1~what a run", "color": "blue"},
    {"type": "focus", "target": "page", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.grid2{display:grid;grid-template-columns:1fr 1fr;gap:24px;width:100%}'
        '.grid2 .semantic-block{min-height:130px;justify-content:center}.grid2 .title{font-size:42px}.lead{font-size:40px}')

# ---- Chapter: Tags, suites and exit codes ------------------------------------------------------------------
EB2 = 'Tags, suites and exit codes'
framed('s06', EB2, 'A tag labels a stimulus', f'''<div class="annotated">
    {panel('tags')}
    {callouts(('tag', 'a name and a value · the words are ours'))}
  </div>''', [
    {"type": "focus", "target": "tag", "at": "1~label", "color": "yellow"},
    {"type": "focus", "target": "tier", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "all", "at": "3", "color": "blue"}], layout='layout-file')

s = suites.rstrip('\n')
for a, b in [('  quick:', '  ⟦q:quick⟧:'), ('    filter: { tier: quick }', '    ⟦flt:filter: { tier: quick }⟧'), ('  full:', '  ⟦f:full⟧:')]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
i = s.index('    evals:')
j = s.index('    evals:', i + 1)
s = s[:i] + '    ⟦ev:evals⟧:' + s[i + len('    evals:'):j] + '    ⟦ev2:evals⟧:' + s[j + len('    evals:'):]
framed('s07', EB2, 'A suite names a group', f'''<div class="annotated">
    {code(s, 'yaml', 'suites')}
    {callouts(('q', 'the name we type'), ('ev', 'eval files it draws on'), ('flt', 'only stimuli tagged tier: quick'),
              ('ev2', 'no filter: every stimulus in these four'))}
  </div>
  <p class="note">{mono('.vally.yaml')} · the whole file, in the practice folder</p>''', [
    {"type": "focus", "target": "q", "at": "3~quick", "color": "yellow"},
    {"type": "focus", "target": "ev", "at": "4", "color": "blue"},
    {"type": "focus", "target": "flt", "at": "4~filter", "color": "yellow"},
    {"type": "focus", "target": "f", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "ev2", "at": "5~four eval files", "color": "blue"}],
    css='.code.dark.suites{min-width:900px;font-size:30px;line-height:1.36;padding:22px 34px}.callout{font-size:32px}.stage{gap:16px}')

framed('s08', EB2, 'One option runs a suite', f'''<div class="annotated">
    {code('vally eval ⟦suite:--suite quick⟧ \\\n  ⟦rest:--model claude-haiku-4.5,gpt-5.6-terra⟧ \\\n  --workers 2', 'bash', 'cmd')}
    {callouts(('suite', 'in place of -e and a file'), ('rest', 'everything else as before'))}
  </div>''', [
    {"type": "focus", "target": "suite", "at": "0~dash dash suite", "color": "yellow"},
    {"type": "focus", "target": "rest", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.code.dark.cmd{min-width:1000px;font-size:40px;line-height:1.55}.callout{font-size:34px}')

framed('s09', EB2, 'Quick stimuli carry their budgets', f'''{panel('budgets')}''', [
    {"type": "scroll", "target": "#budgets", "to": "33-41", "at": "0~budgets"},
    {"type": "focus", "target": "tok", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "turns", "at": "1~turns", "color": "yellow"},
    {"type": "focus", "target": "wall", "at": "1~time", "color": "yellow"},
    {"type": "scroll", "target": "#budgets", "to": "11-17", "at": "2"},
    {"type": "focus", "target": "stop", "at": "2", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}], layout='layout-file')

framed('s10', EB2, 'Exit codes make failure loud', f'''<table class="data-table full codes">
    <thead><tr><th>The run</th><th class="mono num">vally eval</th><th class="mono num">with --require-pass</th></tr></thead>
    <tbody>
      <tr><td>every stimulus passed</td><td class="num">0</td><td class="num">0</td></tr>
      <tr><td>a stimulus failed, budgets included</td><td class="num">{cell('d2', '0')}</td><td class="num">{cell('r2', '1')}</td></tr>
      <tr><td>a trial ended in ERROR</td><td class="num">{cell('e', '1')}</td><td class="num">{cell('e', '1')}</td></tr>
    </tbody>
  </table>
  <p class="note">the exit code · {mono('vally grade')} takes the same option</p>''', [
    {"type": "focus", "target": "d2", "at": "1", "color": "blue"},
    {"type": "focus", "target": "r2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "e", "at": "3", "color": "red"},
    {"type": "focus", "target": "none", "at": "4"}],
    css=TABLE_CSS + '.codes{font-size:42px}.codes td.num{font-size:46px}.codes td{padding-top:30px;padding-bottom:30px}')

cmp_src = (f"vally compare \\\n  ⟦base:--baseline {L19['baseline']}⟧ \\\n  ⟦treat:--treatment {L19['treatment']}⟧ \\\n"
           f"  --judge-model {L19['judge_model']} \\\n  ⟦gate:--fail-on-regression⟧\n\n"
           f"⟦ours:{L19['ours']['line']}⟧\n\n⟦out:{L19['earlier']['output'][0]}⟧\n" + '\n'.join(L19['earlier']['output'][1:]))
framed('s11', EB2, 'A third gate, for judged quality', f'''<div class="annotated">
    {code(cmp_src, 'text', 'cmp')}
    {callouts(('base', 'the newer skill'), ('treat', 'the change under test'),
              ('gate', 'exit 1 when the whole range is below zero'),
              ('ours', f"our run: exit {L19['ours']['exit']}"), ('out', f"an earlier run: exit {L19['earlier']['exit']}"))}
  </div>''', [
    {"type": "focus", "target": "base", "at": "2", "color": "blue"},
    {"type": "focus", "target": "gate", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "treat", "at": "5", "color": "blue"},
    {"type": "focus", "target": "ours", "at": "6", "color": "blue"},
    {"type": "focus", "target": "out", "at": "7", "color": "red"},
    {"type": "focus", "target": "none", "at": "8"}],
    css='.code.dark.cmp{min-width:920px;font-size:30px;line-height:1.4;padding:22px 34px}.callout{font-size:30px}')

# ---- Chapter: Two suites and a conventions page -----------------------------------------------------------
EB3 = 'Two suites and a conventions page'
framed('s12', EB3, 'What would the exit code be?', f'''<p class="lead">one trial over its token budget · nothing else fails · nothing errors</p>
  <div class="semantic-block" id="q" data-role="structure">
    <div class="title words">the quick suite, without {mono('--require-pass')}</div>
    <div class="parts">
      <div class="part" data-concept="p1" data-rep="part"><div class="title words">Exit code 0</div><div class="label">the run itself completed</div></div>
      <div class="part" data-concept="p2" data-rep="part"><div class="title words">With {mono('--require-pass')}: 1</div><div class="label">a failing verdict becomes an error</div></div>
    </div>
  </div>''', [
    {"type": "expand", "target": "#q", "at": "4"},
    {"type": "focus", "target": "p1", "at": "4", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "5", "color": "yellow"}], layout='layout-expand',
    css='.lead{font-size:46px;align-self:flex-start;color:var(--ink)}#q{width:100%;padding:36px 40px 44px;gap:24px}#q > .title{font-size:44px}'
        '#q .parts{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;width:100%}'
        '#q .part{min-height:220px}#q .part .title{font-size:50px;line-height:1.2}#q .part .label{font-size:34px}'
        '.stage{gap:28px}')

framed('s15', EB3, 'One budget lowered, for a moment', f'''<div class="annotated">
    {panel('lowered')}
    {callouts(('max', f'was {MAX}'))}
  </div>''', [
    {"type": "focus", "target": "max", "at": "1~seventy thousand", "color": "yellow"}], layout='layout-file')

b = budget_only[0]
a_of_b = re.search(r'\((\d+/\d+) graders passed, (\d+) failed\)', b[4])
g, ev = b[2][0]
tok, rest = re.match(r'(\d+ tokens) (.*)', ev).groups()
block_src = (f"❌ typo-fix (⟦did:{a_of_b.group(1)} graders passed⟧, {a_of_b.group(2)} failed)\n"
             f"  ✗ ⟦over:[{g}] {tok}⟧\n    {rest}\n\n⟦score:Score: {b[3]}% | FAILED⟧")
framed('s17', EB3, 'Over budget fails like any other', f'''<div class="annotated">
    {code(block_src, 'text', 'blk')}
    {callouts(('did', 'did the work'), ('over', 'cost too much'), ('score', 'decides nothing without a scoring block'))}
  </div>
  <p class="note">{len(budget_only)} typo-fix trials failed on the budget alone: {' · '.join(thousands(n) for n in over_tokens)} tokens · {RUN_NOTE}</p>''', [
    {"type": "focus", "target": "did", "at": "1", "color": "green"},
    {"type": "focus", "target": "over", "at": "2", "color": "red"},
    {"type": "focus", "target": "score", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "6"}],
    css='.code.dark.blk{min-width:980px;font-size:36px;line-height:1.5;padding:28px 36px}.callout{font-size:34px}')


def full_cell(e, m):
    p, t = F1[e][m]
    return f'<td class="num">{"✓" if p == t else "✘"} {p}/{t}</td>'


def trouble_cards():
    errs = [f for f in F1_FAILS if f[0] == 'ERROR']
    fail = next(f for f in F1_FAILS if f[0] != 'ERROR')
    where = '<br>'.join(f"{mono(e + ' · ' + s_)} on {mono(m)}" for _, e, s_, m, _ in errs)
    return f'''<div class="semantic-block" data-concept="error" data-rep="block" data-role="attention">
      <div class="title">ERROR × {len(errs)}</div><div class="label">{where}<br>{errs[0][4]}</div>
    </div>
    <div class="semantic-block" data-concept="fail" data-rep="block" data-role="failure">
      <div class="title">FAIL</div><div class="label">{mono(fail[1] + ' · ' + fail[2])} on {mono(fail[3])}<br>the skill loaded for a question that should not load it</div>
    </div>'''


framed('s19', EB3, 'Our first run had trouble', f'''<div class="cols pair">
    <table class="data-table fulls">
      <thead><tr><th class="mono">eval</th>{''.join(f'<th class="mono num">{m}</th>' for m in MODELS)}</tr></thead>
      <tbody>
{''.join(f'<tr><td class="mono">{e}</td>{full_cell(e, H)}{full_cell(e, T)}</tr>' + chr(10) for e in F)}      </tbody>
    </table>
    <div class="cards">
      {trouble_cards()}
    </div>
  </div>
  <p class="note">our first run of the full suite, minutes before the one we kept · exit code {F1_EXIT}</p>''', [
    {"type": "focus", "target": "error", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "fail", "at": "6", "color": "red"},
    {"type": "focus", "target": "none", "at": "8"}],
    css='.pair{align-items:start;grid-auto-columns:auto 1fr;gap:64px;margin-top:28px}'
        '.fulls{font-size:36px}.fulls th{font-size:28px}.fulls th.mono,.fulls td.mono{font-family:var(--font-code);font-size:32px}'
        '.fulls td{padding-top:22px;padding-bottom:22px}.fulls td.num{white-space:nowrap}'
        '.cards{display:flex;flex-direction:column;gap:16px}.cards .semantic-block{padding:18px 26px}.cards .title{font-size:36px}.cards .label{font-size:27px;line-height:1.35}'
        '.stage{justify-content:flex-start;gap:18px}')

framed('s20', EB3, 'Ten headings, one page', f'''{panel('conv')}''', [
    {"type": "scroll", "target": "#conv", "to": "3-9", "at": "2"},
    {"type": "scroll", "target": "#conv", "to": "9-12", "at": "2~where files"},
    {"type": "scroll", "target": "#conv", "to": "15-16", "at": "2~judge"},
    {"type": "scroll", "target": "#conv", "to": "18-21", "at": "3"},
    {"type": "scroll", "target": "#conv", "to": "24-25", "at": "3~what a run"},
    {"type": "scroll", "target": "#conv", "to": "27-28", "at": "4"},
    {"type": "scroll", "target": "#conv", "to": "30-31", "at": "4~which models"},
    {"type": "focus", "target": "models", "at": "5", "color": "yellow"}], layout='layout-file')

# ---- Chapter: Where the skill stands -----------------------------------------------------------------------
EB4 = 'Where the skill stands'
fg = STANDING['first_graders']
framed('s21', EB4, 'From one pair to two suites', f'''<div class="cols wide terms">
    {block('w1', 'structure', 'At the start', 'a first draft, and a tick that hid a made-up number', words=True)}
    {block('w2', 'attention', f"{fg['pairs_passed']} of {fg['pairs']}", 'pairs of stimulus and model passed, with our first graders')}
    {block('w3', 'success', f'{FULL_STIMULI // 2} of {FULL_STIMULI // 2}', 'stimuli passed on each model, in the full suite: four eval files, budgets, a judge')}
  </div>''', [
    {"type": "focus", "target": "w1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "w2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "w3", "at": "3", "color": "green"},
    {"type": "focus", "target": "none", "at": "4"}],
    css=TERMS + '.terms .title{font-size:48px}.terms .semantic-block{min-height:300px}')

cq, cf = COST['quick'], COST['full']
framed('s22', EB4, 'What the routine costs', f'''<table class="data-table full costs">
    <thead><tr><th></th><th class="num">trials</th><th class="num">AIU</th><th class="num">about</th></tr></thead>
    <tbody>
      <tr><td>{cell('cq', 'quick suite')}</td><td class="num">{cq['trials']}</td><td class="num">{cq['aiu']:.2f}</td><td class="num">${cq['aiu'] / 100:.2f} an edit</td></tr>
      <tr><td>{cell('cf', 'full suite')}</td><td class="num">{cf['finished']}</td><td class="num">{cf['aiu']:.2f}</td><td class="num">${cf['aiu'] / 100:.2f} · plus {cf['judge_calls']} judge calls</td></tr>
    </tbody>
  </table>
  <p class="lead"><span data-concept="tok" data-rep="note">largest quick trial: {thousands(cq['largest_tokens'])} tokens · budget {thousands(MAX)}</span></p>
  <p class="note">{RUN_NOTE} · $0.01 per AIU</p>''', [
    {"type": "focus", "target": "cq", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "cf", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "tok", "at": "3", "color": "blue"}],
    css=TABLE_CSS + '.costs{font-size:42px}.costs td{padding-top:30px;padding-bottom:30px}.lead{font-size:38px}')

framed('s23', EB4, 'A cheaper model, checked first', f'''<div class="cols wide two">
    {block('ours', 'structure', f"about {round(cq['aiu'])} AIU an edit", 'the quick suite on our two models')}
    {block('cheap', 'success', f"about {round(L16['aiu_per_passing'] * L16['quick_stimuli'])} AIU an edit", f"{mono(L16['model'])}, {L16['effort']} effort · passed {L16['passed']} of {L16['trials']} earlier")}
  </div>
  <div class="cols three">
    {block('m1', 'structure', '1', 'compare cost per passing trial')}
    {block('m2', 'structure', '2', 're-test the budgets on its saved trials')}
    {block('m3', 'structure', '3', 'run the full suite on it first')}
  </div>''', [
    {"type": "focus", "target": "ours", "at": "0", "color": "blue"},
    {"type": "focus", "target": "cheap", "at": "1", "color": "green"},
    {"type": "focus", "target": "m1", "at": "3~compare", "color": "yellow"},
    {"type": "focus", "target": "m2", "at": "3~re-test", "color": "yellow"},
    {"type": "focus", "target": "m3", "at": "3~run the full", "color": "yellow"}],
    css='.two .semantic-block{min-height:210px;justify-content:center}.two .title{font-size:56px}.two .label{font-size:32px}'
        '.three{gap:24px}.three .semantic-block{min-height:150px;flex-direction:row;align-items:center;gap:24px}'
        '.three .title{font-size:52px}.three .label{font-size:32px}.stage{gap:28px}')

framed('s24', EB4, 'One trial per stimulus', f'''<div class="cols wide two">
    {block('then', 'failure', '0 of 1', f'{mono("loading · skip-question")} on {mono(T)}, in our first run')}
    {block('here', 'success', '1 of 1', 'the same question, in the second run, minutes later')}
  </div>
  <p class="lead"><span data-concept="say" data-rep="note">One pass shows it can pass, not that it will every time.</span></p>''', [
    {"type": "focus", "target": "then", "at": "1~failed", "color": "red"},
    {"type": "focus", "target": "here", "at": "1~passed", "color": "green"},
    {"type": "focus", "target": "say", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.two .semantic-block{min-height:280px;justify-content:center}.two .title{font-size:100px;line-height:1.1}'
        '.two .label{font-size:34px}.lead{font-size:42px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Lint', 'after editing an eval file'),
    ('Oracle', 'after changing a grader'),
    ('Re-grade', 'after changing a pattern, a budget or a rubric'),
    ('Quick suite', 'after every edit to the skill'),
    ('Full suite', 'before sharing · when a model changes')], 1))
framed('s25', 'Recap', 'What are the five checks?', f'''<div class="semantic-block" id="checks" data-role="structure">
    <div class="title words">cheapest check first</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#checks", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "blue"},
    {"type": "focus", "target": "p3", "at": "3", "color": "blue"},
    {"type": "focus", "target": "p4", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "p5", "at": "5", "color": "yellow"}], layout='layout-expand',
    css='#checks{width:100%;padding:36px 40px 44px;gap:24px}'
        '#checks .parts{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;width:100%}'
        '#checks .part{min-height:300px}#checks .part .title{font-size:44px;line-height:1.2}'
        '#checks .part .label{font-size:30px}')

scene('s26', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">The skill inside an app</h1>
  <p class="lead">Start the agent where the app would: does the skill hold when an app, not a person, starts the agent?</p>
  <p class="note">Exercises and the workflow guide are on the course site · Source: Vally docs, “Authoring Eval Suites”</p>
</main>''', [], css='.scene-title.chapter{font-size:116px}')
print('ok', 'PROVISIONAL (stand-in run)' if PROVISIONAL else 'own run')
