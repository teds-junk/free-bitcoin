"""Generate lesson 23's scene pages, file panels included (file-panel.js is called from here, so
there is nothing to quote in a shell; build-src/panels.sh only says so).

Same parts as lessons 1 to 5: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/state/release.eval.yaml          the eval file with the lesson's four graders (verified/lesson-23);
                                       the tapes install it
  src/state/release.before.eval.yaml   the eval file as the lesson 22 video leaves it (verified/lesson-22)
  src/state/release.swap.eval.yaml     WRITTEN HERE: never-commits forbids src/run/swap-command.txt's word
                                       instead of git (commit|push), for the one re-grade in s19
  src/run/s15.log s16.log s19.log s21.log   what the four tapes printed (/tmp/vl-l23/<scene>.log)
  src/run/tool-call-event.json         one tool_call event of one saved trial, pretty-printed
  src/run/l22/, src/run/l23/           results.jsonl, eval-results.md, RUN and <model>-<trial>.patch of the
                                       saved lesson 22 run and of this video's s21 run (build-src/collect-run.sh)

Run from anywhere:  python3 build-src/make-scenes.py
"""
import json, pathlib, re, subprocess

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
H, T = MODELS
GRADERS = ('every-change-handled', 'reads-the-list', 'never-commits', 'no-loop', 'loads-the-skill')
NEW = GRADERS[1:]
SKILL_NAME = 'changelog-entry'
REFACTOR = '#76'            # tools/list-merged.mjs: "#76 refactor: move config loading out of cli.js"
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
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
PANELS = []     # (scene id, file-panel.js arguments), run after the pages are written


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


def panel(sid, pid, *args):
    PANELS.append((sid, ['--id', pid, *args]))
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


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>' if cid else text


# ---- The eval file, and the copy with one pattern swapped for the s19 re-grade -------------------------
spec = (D / 'src/state/release.eval.yaml').read_text()
lines = spec.splitlines()
before = (D / 'src/state/release.before.eval.yaml').read_text().splitlines()
assert lines[:32] == before and len(lines) == 52, 'the lesson adds twenty lines after every-change-handled'
assert lines[29].strip() == 'name: every-change-handled' and lines[33].strip() == 'name: reads-the-list'
assert lines[36].strip() == '- name: ^(view|bash)$' and lines[37].strip() == r'pattern: release/merged\.txt'
assert lines[39].strip() == 'name: never-commits' and lines[43].strip() == 'command: git (commit|push)'
assert lines[44].strip() == '- type: max-repeat' and lines[47].strip() == 'max: 3'
assert lines[49].strip() == 'name: loads-the-skill' and lines[51].strip() == f'required: [{SKILL_NAME}]'
PROMPT = ' '.join(l.strip() for l in lines[17:19])
assert PROMPT == 'Write the Unreleased changelog entries for every change listed in release/merged.txt.'
SWAP = (D / 'src/run/swap-command.txt').read_text().strip()
assert re.fullmatch(r'[a-z][a-z0-9-]*', SWAP), 'swap-command.txt: one plain command word that a saved trial ran'
assert spec.count('command: git (commit|push)') == 1
(D / 'src/state/release.swap.eval.yaml').write_text(spec.replace('command: git (commit|push)', f'command: {SWAP}'))


# ---- What the tapes printed ---------------------------------------------------------------------------
def log(name):
    t = (D / 'src/run' / name).read_text()
    t = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', t).replace('\r', '')
    return re.sub(r'\^D\x08\x08', '', t)


lint_oracle = log('s15.log')
# s15: "one warning, the usual one about scoring"
assert len(re.findall(r'warning \[scoring-defaults-applied\]', lint_oracle)) == 1 and '1 warning(s)' in lint_oracle
# s15: "Three failed as expected: the hidden test, reads the list, and loads the skill."
#      "The two that only forbid something are marked N/A"
ORACLE = {g: ('failed' if re.search(rf'✓ \[{g}\] failed as expected', lint_oracle) else
              'n/a' if re.search(rf'⊘ \[{g}\] N/A', lint_oracle) else '?') for g in GRADERS}
assert ORACLE == {'every-change-handled': 'failed', 'reads-the-list': 'failed', 'never-commits': 'n/a',
                  'no-loop': 'n/a', 'loads-the-skill': 'failed'}, ORACLE
assert 'baseline OK' in lint_oracle


def blocks(text):
    """vally grade --verbose: one block per trial -> [{grader: passed}], and the raw blocks."""
    raw = [b for b in re.split(r'━━━ \S+ ━━━', text)[1:]]
    out = []
    for b in raw:
        marks = dict((g, m == '✓') for m, g in re.findall(r'^\s*([✓✗]) \[([\w-]+)\]', b, re.M))
        assert set(marks) == set(GRADERS), marks
        out.append(marks)
    return out, raw


regrade, _ = blocks(log('s16.log'))
swapped, swapped_raw = blocks(log('s19.log'))
N_SAVED = len(regrade)
passed = lambda bs, g: sum(b[g] for b in bs)
# s16: "ten blocks, one for each trial"; "The hidden test fails in every block"
assert N_SAVED == 10 and passed(regrade, 'every-change-handled') == 0
# s17: "Reads the list, never commits and no loop passed all ten trials." "Loads the skill failed five"
assert [passed(regrade, g) for g in ('reads-the-list', 'never-commits', 'no-loop')] == [10, 10, 10]
# s19, s20: with the pattern swapped, never-commits "failed in that one trial, and passed in the other nine",
#           and "its evidence names the entry that matched: a bash call whose command contains <SWAP>"
assert len(swapped) == 10 and passed(swapped, 'never-commits') == 9, passed(swapped, 'never-commits')
assert all(passed(swapped, g) == passed(regrade, g) for g in GRADERS if g != 'never-commits')
bad = [r for b, r in zip(swapped, swapped_raw) if not b['never-commits']][0]
bl = [l.rstrip() for l in bad.splitlines() if l.strip()]
i = next(k for k, l in enumerate(bl) if '[never-commits]' in l)
B_HEAD, B_NC, B_EV = bl[0].strip(), bl[i].strip(), bl[i + 1].strip()
assert B_HEAD.startswith('❌ since-last-release') and B_NC.startswith('✗ [never-commits]')
assert B_EV == f'The following disallowed tools were called: /^bash$/ {{command=/{SWAP}/}}', B_EV

run_out = log('s21.log')
# s21: "Terra passed every grader in all three trials." "Haiku's first and third trials each failed two
#      graders: the hidden test, and loads the skill." "Its second trial passed all five."
# The log holds every redraw of the live progress; the final report is what follows the last redraw.
rows = re.findall(r'^\s*release\s+([✘✓]) (\d)/1\s+([✘✓]) (\d)/1', run_out, re.M)
assert rows and rows[-1] == ('✘', '0', '✓', '1'), rows[-1:]
hb = run_out.rsplit('\n' + H + '\n', 1)[1].split('█')[0]
assert re.match(r'\s+FLAKY\s+since-last-release\s+1 passed · 2 failed', hb), hb[:80]
assert not re.search(rf'\n{re.escape(T)}\n\s+(FAIL|FLAKY|ERROR)', run_out), 'terra has a failure block'
FAILED = dict((g, (int(p), int(f))) for g, p, f in re.findall(r'✘ ([\w-]+)\s+(\d+) passed · (\d+) failed', hb))
assert FAILED == {'every-change-handled': (1, 2), 'loads-the-skill': (1, 2)}, FAILED
fb = run_out.rsplit('Failures', 1)[1].split('Model summary')[0]
assert re.findall(r'trials ([\d, –]+)', fb) == ['1, 3', '1, 3'], fb
N_NEW = 6


# ---- The two runs: who loaded the skill, who wrote an entry for the refactor ----------------------------
def load(run):
    """-> per model: trials, loaded, refactor recorded, passed, loaded-and-recorded, tool calls, bash commands"""
    d = D / 'src/run' / run
    ts = [json.loads(l) for l in (d / 'results.jsonl').read_text().splitlines() if l.strip()]
    ts = [t for t in ts if t.get('type') == 'trial-result']
    err = [(t['model'], t['trialIndex']) for t in ts if t['status'] != 'success']
    assert not err, f'{run}: trials that did not finish (ERROR): {err}. Re-record the tape.'
    out = {}
    for m in MODELS:
        mine = [t for t in ts if t['model'] == m]
        r = dict(n=len(mine), loaded=0, refactor=0, passed=0, both=0, without=0, without_rf=0, tools={}, bash=[])
        for t in mine:
            mt = t['trajectory']['metrics']
            ld = SKILL_NAME in (mt.get('skillActivationBreakdown') or {})
            patch = (d / f"{m}-{t['trialIndex']}.patch").read_text()
            rf = any(l.startswith('+') and REFACTOR in l for l in patch.splitlines())
            r['loaded'] += ld; r['refactor'] += rf; r['both'] += ld and rf
            r['without'] += not ld; r['without_rf'] += (not ld) and rf
            r['passed'] += bool(t['gradeResult']['passed'])
            for k, v in (mt.get('toolCallBreakdown') or {}).items():
                r['tools'][k] = r['tools'].get(k, 0) + v
            r['bash'] += [e['data']['arguments'].get('command', '') for e in t['trajectory']['events']
                          if e['type'] == 'tool_call' and e['data']['toolName'] == 'bash']
        out[m] = r
    return out, (d / 'RUN').read_text().strip()


assert not PROVISIONAL, 'the real runs are here: delete src/run/PROVISIONAL'
L22, L22_RUN = load('l22')
L23, L23_RUN = load('l23')
TOOLS = L22[H]['tools']
SWAP_RAN = {m: sum(SWAP in c.split() for c in L22[m]['bash']) for m in MODELS}
FORBIDDEN = 'git (' + 'commit|push)'
assert not any(re.search(FORBIDDEN, c) for m in MODELS for c in L22[m]['bash'] + L23[m]['bash'])
stat = lambda m, k: (L22[m][k], L23[m][k])
BOTH = L22[H]['both'] + L23[H]['both']
tot = lambda m, k: sum(stat(m, k))
N = tot(H, 'n')
# s06: "For haiku's five saved trials, it counted eighteen views, five edits, three skill calls, and two bash calls."
assert stat(H, 'n')[0] == 5 and TOOLS == {'view': 18, 'edit': 5, 'skill': 3, 'bash': 2}, TOOLS
TOOLS_LINE = ', '.join(f'{k}: {v}' for k, v in sorted(TOOLS.items(), key=lambda kv: -kv[1]))
assert f'total across 5 trials: {TOOLS_LINE}' in (D / 'src/run/l22/eval-results.md').read_text()
# s10: "haiku loaded the skill in three of its five trials"; s17: "Loads the skill failed two: the two haiku
#      trials that hadn't loaded it."
assert stat(H, 'loaded')[0] == 3 and stat(T, 'loaded')[0] == 5 and stat(T, 'n')[0] == 5
assert passed(regrade, 'loads-the-skill') == 8
# s18: "In one of its trials, haiku ran <SWAP>."
assert SWAP_RAN[H] == 1 and SWAP_RAN[T] == 0, SWAP_RAN
# s21 agrees with the saved records
assert stat(H, 'n')[1] == 3 and stat(T, 'n')[1] == 3 and stat(H, 'loaded')[1] == FAILED['loads-the-skill'][0] == 1
assert stat(T, 'passed')[1] == 3 and stat(H, 'passed')[1] == 1 and L23[H]['without_rf'] == 2
# s22: "The two guards, never commits and no loop, didn't fail a single real trial" (ten saved and six new)
assert 'never-commits' not in FAILED and 'no-loop' not in FAILED and N_SAVED + N_NEW == 16
# s23: haiku "loaded the skill in four of them, and five of the eight have an entry for the refactor";
#      "Terra loaded the skill in all eight, and passed all eight";
#      "all four haiku trials without the skill wrote that entry, and so did one of the four that loaded it"
assert N == 8 and tot(H, 'loaded') == 4 and tot(H, 'refactor') == 5 and tot(H, 'passed') == 3
assert tot(T, 'loaded') == 8 and tot(T, 'passed') == 8 and tot(T, 'refactor') == 0
assert tot(H, 'without') == 4 and tot(H, 'without_rf') == 4 and BOTH == 1

event = (D / 'src/run/tool-call-event.json').read_text().splitlines()
assert event[1].strip() == '"type": "tool_call",' and event[4].strip().startswith('"toolName": "')
assert event[8].strip() == '"path": "<workspace>/release/merged.txt"', event[8]

# ---- Hook ----------------------------------------------------------------------------------------------
TERMS = '.terms .semantic-block{min-height:280px}.terms .label{font-size:34px}'
framed('s01', 'Vally &amp; Agent Evals', 'Check what the agent did', f'''<div class="cols wide terms">
    {block('file', 'structure', 'The finished changelog', 'all the hidden test sees', words=True)}
    {block('list', 'attention', 'Did the entries come from the list?', mono('release/merged.txt'), words=True)}
    {block('commit', 'failure', 'Did the agent commit or push?', 'the release tool does that itself', words=True)}
  </div>''', [
    {"type": "focus", "target": "file", "at": "1~changelog", "color": "blue"},
    {"type": "focus", "target": "list", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "commit", "at": "3", "color": "red"},
    {"type": "focus", "target": "file", "at": "4", "color": "blue"},
    {"type": "focus", "target": "none", "at": "5"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.terms .semantic-block{min-height:260px}.terms .label{font-size:32px}'
        '.terms .title{font-size:42px;line-height:1.2}')

# ---- Chapter: When the route matters -----------------------------------------------------------------------
EB1 = 'When the route matters'
framed('s02', EB1, 'Grade the outcome by default', f'''<div class="cols wide terms">
    {block('outcome', 'structure', 'The outcome', 'what the agent left behind · the default', words=True)}
    {block('route', 'attention', 'The route', 'the steps it took · only where the app depends on one', words=True)}
  </div>
  <p class="note">Source: Anthropic, “Demystifying evals for AI agents” (2026)</p>''', [
    {"type": "focus", "target": "outcome", "at": "1", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "route", "at": "4", "color": "yellow"}], css=TERMS)

framed('s03', EB1, 'Required, forbidden, or too long', f'''<div class="cols wide terms">
    {block('req', 'structure', 'Required', 'the agent works from the list', words=True)}
    {block('forb', 'failure', 'Forbidden', 'a commit, a push, a deleted file', words=True)}
    {block('long', 'attention', 'Too long', 'the same call, again and again', words=True)}
  </div>''', [
    {"type": "focus", "target": "req", "at": "0", "color": "blue"},
    {"type": "focus", "target": "forb", "at": "1", "color": "red"},
    {"type": "focus", "target": "long", "at": "3", "color": "yellow"}], css=TERMS)

framed('s04', EB1, 'As loose as the requirement', f'''<div class="cols wide terms">
    {block('need', 'structure', 'The requirement', f'open {mono("release/merged.txt")}', words=True)}
    {block('way', 'attention', 'One way to meet it', 'one particular tool', words=True)}
  </div>''', [
    {"type": "focus", "target": "need", "at": "1", "color": "blue"},
    {"type": "focus", "target": "way", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}], css=TERMS)

# ---- Chapter: The tool-calls grader ------------------------------------------------------------------------
EB2 = 'The tool-calls grader'
framed('s05', EB2, 'Every tool use is recorded', f'''<div class="annotated">
    {panel('s05', 'event', '--file', 'src/run/tool-call-event.json', '--label', 'results.jsonl · one event of one trial',
           '--width', '50', '--rows', '9', '--expect', '2="type": "tool_call"', '--expect', '9=release/merged.txt',
           '--mark', '2=kind:"tool_call"', '--mark', '5=tool', '--mark', '9=path')}
    {callouts(('tool', 'the tool’s name'), ('path', 'what the tool was given'))}
  </div>
  <p class="note">the workspace’s real location, a long temporary folder, is shown as &lt;workspace&gt;{STAND_IN}</p>''', [
    {"type": "scroll", "target": "#event", "to": "2-9", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "kind", "at": "1~tool call event", "color": "blue"},
    {"type": "focus", "target": "tool", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "path", "at": "4", "color": "yellow"}], layout='layout-file')

TOOL_ROWS = [('t-view', 'view', 'opens a file'), ('t-edit', 'edit', 'changes a file'),
             ('t-edit', 'apply_patch', 'changes a file'), ('t-bash', 'bash', 'runs a shell command'),
             ('t-skill', 'skill', 'loads a skill')]
tool_rows = ''.join(f'<tr><td class="mono">{cell(c, n)}</td><td>{d}</td></tr>\n' for c, n, d in TOOL_ROWS)
TABLE_CSS = ('.data-table{font-size:40px}.data-table th{font-size:30px}.data-table td{padding-top:22px;padding-bottom:22px}'
             '.data-table td.mono,.data-table th.mono{font-family:var(--font-code);font-size:34px}')
framed('s06', EB2, 'The report counts them', f'''<div class="cols pair">
    {card('cell', f'eval-results.md · Tool Calls · {mono(H)}', code(TOOLS_LINE, 'text'))}
    <table class="data-table tools">
      <thead><tr><th>Tool</th><th>What it does</th></tr></thead>
      <tbody>
{tool_rows}      </tbody>
    </table>
  </div>
  <p class="note">the five saved trials of {mono('since-last-release')} · {L22_RUN}{STAND_IN}</p>''', [
    {"type": "focus", "target": "cell", "at": "1~Tool Calls", "color": "blue"},
    {"type": "focus", "target": "t-view", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "t-edit", "at": "3~edit", "color": "yellow"},
    {"type": "focus", "target": "t-bash", "at": "3~bash", "color": "yellow"},
    {"type": "focus", "target": "t-skill", "at": "3~skill loads", "color": "yellow"}],
    css=TABLE_CSS + '.pair{align-items:center;gap:60px}.card > .code.dark{font-size:31px}.tools{width:100%}')

SPEC = ['--file', 'src/state/release.eval.yaml', '--label', 'evals/release.eval.yaml', '--width', '46', '--rows', '9',
        '--show', '28-52', '--expect', '34=reads-the-list', '--expect', '44=git (commit|push)',
        '--mark', '30=test:every-change-handled', '--mark', '34=g1:reads-the-list', '--mark', '36=req',
        '--mark', '37=nm:^(view|bash)$', '--mark', r'38=pat:release/merged\.txt',
        '--mark', '40=g2:never-commits', '--mark', '42=dis', '--mark', '44=cmd:git (commit|push)',
        '--mark', '45=loop:max-repeat', '--mark', '46=g3:no-loop', '--mark', '48=max',
        '--mark', '50=g4:loads-the-skill', '--mark', f'52=req4:[{SKILL_NAME}]']
at = lambda rng: {"type": "scroll", "target": "#spec", "to": rng, "at": "t=0", "duration": 0}

framed('s07', EB2, 'Required: one call must match', f'''<div class="annotated">
    {panel('s07', 'spec', *SPEC)}
    {callouts(('nm', 'exactly view, or exactly bash'), ('pat', 'its arguments mention the list'))}
  </div>''', [
    at('33-38'),
    {"type": "focus", "target": "g1", "at": "2", "color": "blue"},
    {"type": "focus", "target": "req", "at": "3~required", "color": "yellow"},
    {"type": "focus", "target": "nm", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "pat", "at": "6", "color": "yellow"},
    {"type": "focus", "target": "nm", "at": "7~view", "color": "yellow"},
    {"type": "focus", "target": "pat", "at": "7~mention", "color": "yellow"}], layout='layout-file')

framed('s08', EB2, 'Why view or bash?', f'''<div class="annotated">
    {panel('s08', 'spec', *SPEC)}
    {callouts(('nm', 'exactly view, or exactly bash'), ('pat', 'its arguments mention the list'))}
  </div>''', [
    at('33-38'),
    {"type": "focus", "target": "nm", "at": "0", "color": "yellow"}], layout='layout-file')

framed('s09', EB2, 'Disallowed: no call may match', f'''<div class="annotated">
    {panel('s09', 'spec', *SPEC)}
    {callouts(('dis', 'none of these may happen'), ('cmd', 'git commit, or git push'))}
  </div>''', [
    at('33-38'),
    {"type": "scroll", "target": "#spec", "to": "39-44", "at": "0+0.6"},
    {"type": "focus", "target": "g2", "at": "0~commits", "color": "blue"},
    {"type": "focus", "target": "dis", "at": "1~disallowed", "color": "yellow"},
    {"type": "focus", "target": "cmd", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "dis", "at": "4", "color": "yellow"}], layout='layout-file')

framed('s10', EB2, 'Two more complete the set', f'''<div class="annotated">
    {panel('s10', 'spec', *SPEC)}
    {callouts(('loop', 'a loop check'), ('req4', 'the skill must load'))}
  </div>''', [
    at('39-44'),
    {"type": "scroll", "target": "#spec", "to": "45-52", "at": "0+0.6"},
    {"type": "focus", "target": "g4", "at": "1~loads the skill", "color": "blue"},
    {"type": "focus", "target": "req4", "at": "2~verdict", "color": "yellow"},
    {"type": "focus", "target": "loop", "at": "3", "color": "blue"}], layout='layout-file')

# ---- Chapter: Catching loops -------------------------------------------------------------------------------
EB3 = 'Catching loops'
framed('s11', EB3, 'Four in a row fail', f'''<div class="annotated">
    {panel('s11', 'spec', *SPEC)}
    {callouts(('max', 'a fourth identical result fails'))}
  </div>''', [
    at('45-52'),
    {"type": "focus", "target": "loop", "at": "3", "color": "blue"},
    {"type": "focus", "target": "max", "at": "4", "color": "yellow"}], layout='layout-file')

framed('s12', EB3, 'What counts as the same?', f'''<div class="annotated">
    {code('⟦obs:match: observation⟧\n\n⟦nm:match: name⟧\n\n⟦na:match: name-args⟧', 'yaml', 'types')}
    {callouts(('obs', 'calls that got the same result · the default'), ('nm', 'calls to the same tool'),
              ('na', 'the same tool, the same arguments'))}
  </div>
  <p class="note">also: {mono('tools')}, {mono('max_cycle_period')}</p>''', [
    {"type": "focus", "target": "obs", "at": "1", "color": "blue"},
    {"type": "focus", "target": "nm", "at": "2", "color": "blue"},
    {"type": "focus", "target": "na", "at": "2~third", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.code.dark.types{min-width:760px;font-size:42px;line-height:1.5}.callout{font-size:34px}')

framed('s13', EB3, 'A second grader, for retries', f'''<div class="cols wide terms">
    {block('mr', 'structure', mono('max-repeat'), 'the same action, back to back, more than max times')}
    {block('lo', 'attention', mono('loop-outcome'), 'did it loop, and was that expected?')}
  </div>''', [
    {"type": "focus", "target": "lo", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "mr", "at": "1~max repeat", "color": "blue"},
    {"type": "focus", "target": "lo", "at": "1~loop outcome", "color": "yellow"}], css=TERMS)

# ---- Chapter: Require, forbid, re-grade --------------------------------------------------------------------
EB4 = 'Require, forbid, re-grade'
KIND = {'every-change-handled': 'requires', 'reads-the-list': 'requires', 'never-commits': 'forbids',
        'no-loop': 'forbids', 'loads-the-skill': 'requires'}
BASE = {'failed': 'failed as expected', 'n/a': 'N/A'}


def saved(g):
    if g == 'every-change-handled':
        return 'needs the workspace'
    return f'passed {passed(regrade, g)} of {N_SAVED}'


def tests_table(filled, concept=lambda g, col: None):
    body = ''.join(
        f'<tr><td class="mono">{cell(concept(g, "name"), g)}</td><td>{KIND[g]}</td>'
        f'<td>{cell(concept(g, "base"), BASE[ORACLE[g]]) if filled else ""}</td>'
        f'<td>{cell(concept(g, "saved"), saved(g)) if filled else ""}</td></tr>\n' for g in GRADERS)
    return f'''<table class="data-table full tests">
    <thead><tr><th>Grader</th><th>It</th><th><span data-concept="col-base" data-rep="cell">On the baseline</span></th>
      <th><span data-concept="col-saved" data-rep="cell">On ten saved trials</span></th></tr></thead>
    <tbody>
{body}    </tbody>
  </table>'''


TESTS_CSS = ('.tests{font-size:38px}.tests th{font-size:30px}.tests td{padding-top:20px;padding-bottom:20px;height:52px}'
             '.tests td.mono{font-family:var(--font-code);font-size:34px}')
framed('s14', EB4, 'Which fail on an untouched workspace?',
       tests_table(False, lambda g, col: 'nc' if g == 'never-commits' and col == 'name' else None), [
    {"type": "focus", "target": "col-base", "at": "1", "color": "blue"},
    {"type": "focus", "target": "col-saved", "at": "2", "color": "blue"},
    {"type": "focus", "target": "nc", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}], css=TESTS_CSS)


def s17_concept(g, col):
    if col == 'saved' and g in ('reads-the-list', 'never-commits', 'no-loop'):
        return 'three'
    if col == 'saved' and g == 'loads-the-skill':
        return 'loads'
    return 'nc' if g == 'never-commits' and col == 'name' else None


framed('s17', EB4, 'Three passed all ten', tests_table(True, s17_concept) + f'''
  <p class="note">the saved run · {L22_RUN}{STAND_IN}</p>''', [
    {"type": "focus", "target": "three", "at": "1", "color": "green"},
    {"type": "focus", "target": "loads", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "nc", "at": "3", "color": "yellow"}], css=TESTS_CSS)

framed('s18', EB4, 'Forbid a command one ran', f'''<div class="annotated">
    {panel('s18', 'swap', '--file', 'src/state/release.swap.eval.yaml', '--label', 'evals/release.eval.yaml · for one re-grade',
           '--width', '46', '--rows', '9', '--show', '28-52', '--expect', '40=never-commits', '--expect', f'44=command: {SWAP}',
           '--mark', '40=g2:never-commits', '--mark', f'44=cmd:{SWAP}')}
    {callouts(('cmd', 'in place of git (commit|push), for one re-grade'))}
  </div>''', [
    {"type": "scroll", "target": "#swap", "to": "39-44", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "g2", "at": "0~grader", "color": "blue"},
    {"type": "focus", "target": "cmd", "at": "1", "color": "yellow"}], layout='layout-file')

framed('s20', EB4, 'Now it can fail', f'''{code(f"{B_HEAD}{chr(10)}  ⟦nc:{B_NC}⟧{chr(10)}      ⟦ev:{B_EV}⟧", 'text', 'wide')}
  <p class="note">from the block of the one trial that ran {mono(SWAP)} · that block’s other lines left out{STAND_IN}</p>''', [
    {"type": "focus", "target": "nc", "at": "1", "color": "red"},
    {"type": "focus", "target": "ev", "at": "1~evidence", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.code.dark.wide{font-size:30px;line-height:1.7;width:100%;box-sizing:border-box;padding:34px 40px}')

framed('s20b', EB4, 'The real pattern goes back', f'''<div class="annotated">
    {panel('s20b', 'spec', *SPEC)}
    {callouts(('dis', 'none of these may happen'), ('cmd', 'git commit, or git push'))}
  </div>''', [
    at('39-44'),
    {"type": "focus", "target": "cmd", "at": "0", "color": "yellow"}], layout='layout-file')

# ---- Chapter: What the path showed -------------------------------------------------------------------------
EB5 = 'What the path showed'
framed('s22', EB5, 'Two guards never fired', f'''<div class="cols wide terms">
    {block('nc', 'success', mono('never-commits'), f'failed 0 of {N_SAVED + N_NEW} real trials')}
    {block('nl', 'success', mono('no-loop'), f'failed 0 of {N_SAVED + N_NEW} real trials')}
  </div>
  <p class="note">{N_SAVED} saved trials and {N_NEW} new ones{STAND_IN}</p>''', [
    {"type": "focus", "target": "nc", "at": "1~committed", "color": "green"},
    {"type": "focus", "target": "nl", "at": "1~looped", "color": "green"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "nc", "at": "3", "color": "yellow"}], css=TERMS)

of = lambda m, k: f'{tot(m, k)} of {N}'
framed('s23', EB5, 'The route each model took', f'''<table class="data-table full route">
    <thead><tr><th></th><th class="num">Loaded the skill</th><th class="num">Wrote an entry for the refactor</th>
      <th class="num">Passed every grader</th></tr></thead>
    <tbody>
      <tr><td class="mono">{H}</td><td class="num">{cell('hl', of(H, 'loaded'))}</td>
        <td class="num">{cell('hr', of(H, 'refactor'))}</td><td class="num">{of(H, 'passed')}</td></tr>
      <tr><td class="mono">{T}</td><td class="num">{cell('tl', of(T, 'loaded'))}</td>
        <td class="num">{of(T, 'refactor')}</td><td class="num">{cell('tp', of(T, 'passed'))}</td></tr>
    </tbody>
  </table>
  <p class="note">{N} trials of each model: {stat(H, 'n')[0]} saved, {stat(H, 'n')[1]} new · the refactor should get no entry{STAND_IN}</p>''', [
    {"type": "focus", "target": "hl", "at": "2~loaded", "color": "yellow"},
    {"type": "focus", "target": "hr", "at": "2~entry", "color": "red"},
    {"type": "focus", "target": "tl", "at": "3~loaded", "color": "green"},
    {"type": "focus", "target": "tp", "at": "3~passed", "color": "green"},
    {"type": "focus", "target": "hl", "at": "4~one of the four", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.route{font-size:46px}.route th{font-size:30px}.route td{padding-top:34px;padding-bottom:34px}'
        '.route td.mono{font-family:var(--font-code);font-size:36px}')

framed('s24', EB5, 'A new question for the team', f'''<div class="cols wide terms">
    {block('q1', 'structure', 'Does the skill write good entries?', 'measured earlier', words=True)}
    {block('q2', 'attention', 'Does the app get the skill used?', 'new', words=True)}
  </div>
  <div class="quote" data-concept="prompt" data-rep="quote"><span class="who">The app’s prompt</span><p>“{PROMPT}”</p></div>''', [
    {"type": "focus", "target": "q1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "q2", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "prompt", "at": "2~prompt", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.terms .semantic-block{min-height:200px}.terms .label{font-size:34px}.terms .title{font-size:42px;line-height:1.2}'
        '.stage{gap:30px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title words">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('requires it', 'opening the list'),
    ('forbids it', 'a commit, a push'),
    ('pays for a long route', 'a loop')], 1))
framed('s25', 'Recap', 'When is a step worth grading?', f'''<div class="semantic-block" id="when" data-role="structure">
    <div class="title words">grade a step when the app…</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#when", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "red"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "p2", "at": "4", "color": "red"}], layout='layout-expand',
    css='#when{width:100%;padding:36px 40px 44px;gap:24px}'
        '#when .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#when .part{min-height:260px}#when .part .title{font-size:50px;line-height:1.2}'
        '#when .part .label{font-size:32px}')

scene('s26', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">When a tool fails</h1>
  <p class="lead">Does the agent cope, and can you test that without breaking anything?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, “Choose a Grader”; “Grader: tool-calls”</p>
</main>''', [])

# ---- File panels ---------------------------------------------------------------------------------------
for sid, args in PANELS:
    r = subprocess.run(['node', str(SKILL / 'scripts/file-panel.js'), *args, '--into', f'scenes/{sid}.html'],
                       cwd=D, capture_output=True, text=True)
    assert r.returncode == 0, f'{sid}: {r.stderr or r.stdout}'
print('ok', 'PROVISIONAL (stand-in run)' if PROVISIONAL else f'{L22_RUN} + {L23_RUN}')
