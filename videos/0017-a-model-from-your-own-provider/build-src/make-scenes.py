"""Generate lesson 17's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 4: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and output in a dark box on the left with notes on the right (.annotated + .callout), terms in
blocks, numbers in a .data-table. Nothing here sets a colour or a font outside the theme's variables;
a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/byok.yaml                    the hosted provider block the lesson page prints (linted by us, not run)
  src/byok-lint.txt                our lint and unset-key probes of it (verified/lesson-17/output)
  src/state/cost.experiment.yaml   the experiment file after this lesson (identical to verified/lesson-17);
                                   tapes s16 and s17 copy it into practice/evals out of sight
  src/run/                         this video's own run of the qwen-local variant: s14.log, s16.log, s17.log
                                   (what the tapes' wrappers saved), RUN, trials.json (one row per trial),
                                   record.json (part of one record), l16-facts.json (the lesson 16 video's
                                   numbers). While src/run/PROVISIONAL exists they are stand-ins.

The asserts below are what the narration says about the run. If the video's own run differs, an assert
fails: reword the outcome sentences in storyboard.json, then change the assert.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, math, pathlib, re, statistics, subprocess, textwrap

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'


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
    assert len(headline.split()) <= 6, headline
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


def mono(t):
    return f'<span class="mono">{t}</span>'


def cell(cid, text):
    return f'<span data-concept="{cid}" data-rep="cell">{text}</span>'


def wrap_marked(text, width, phrase, cid, indent='  '):
    """Wrap output for a dark box, keeping `phrase` on one row and marking it as concept `cid`."""
    assert text.count(phrase) == 1, (phrase, text)
    held = text.replace(phrase, phrase.replace(' ', '\x00'))
    rows = textwrap.wrap(held, width, subsequent_indent=indent, break_long_words=False, break_on_hyphens=False)
    return [r.replace('\x00', ' ').replace(phrase, f'⟦{cid}:{phrase}⟧') for r in rows]


# ---- The real things, read from src/ -----------------------------------------------------------
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()
RUN = (D / 'src/run/RUN').read_text().strip()
SRC = 'stand-in: the course’s verified run' if PROVISIONAL else f'our run · {RUN}'
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\r')
log = lambda name: ANSI.sub('', (D / 'src/run' / name).read_text())

# The hosted provider block the page prints.
byok = (D / 'src/byok.yaml').read_text().rstrip('\n')
for cid, line in [('dflt', 'defaults:'), ('cfg', 'config:'), ('model', 'model: my-model-name'), ('name', 'name: copilot-sdk'), ('prov', 'provider:'),
                  ('url', 'baseUrl: https://api.example.com/v1'), ('type', 'type: openai'),
                  ('key', 'apiKeyEnv: MY_PROVIDER_KEY')]:
    assert byok.count(line) == 1, line
    byok = byok.replace(line, f'⟦{cid}:{line}⟧')

# Our two probes of it: lint with a key in the file, and a run with the variable not set.
probe = (D / 'src/byok-lint.txt').read_text().splitlines()
lint_err = next(l for l in probe if l.startswith('✘ error [executor-config-invalid]'))
i = next(n for n, l in enumerate(probe) if l.strip() == 'ERROR  hello')
unset_err = ' '.join(l.strip() for l in probe[i + 1:i + 3])
assert unset_err.endswith('before running.') and 'MY_PROVIDER_KEY' in unset_err, unset_err

# The experiment file after this lesson, and the variant's provider block.
exp = (D / 'src/state/cost.experiment.yaml').read_text().splitlines()
assert exp[8] == '  - /defaults/executor' and exp[34] == '  qwen-local:' and exp[37] == '      timeout: 9m'
assert exp[38] == '      runs: 1' and exp[43] == '            baseUrl: http://localhost:11434/v1' and len(exp) == 44
assert not any('apiKey' in l for l in exp)
local_block = textwrap.dedent('\n'.join(exp[39:44]))

# ---- What the narration says about the run -------------------------------------------------------
TRIALS = json.loads((D / 'src/run/trials.json').read_text())
L16 = json.loads((D / 'src/run/l16-facts.json').read_text())
N, P = len(TRIALS), sum(t['passed'] for t in TRIALS)
TIN, TOUT = sum(t['inputTokens'] for t in TRIALS), sum(t['outputTokens'] for t in TRIALS)
PRICE_IN, PRICE_OUT = 0.10, 0.40          # dollars per million tokens: made up for the arithmetic (the page's)
CIN, COUT = TIN * PRICE_IN / 1e6, TOUT * PRICE_OUT / 1e6
TOTAL = CIN + COUT
PER_PASS = TOTAL / P
HL, TL = L16['haiku-low'], L16['terra-low']
HL_C, TL_C = HL['aiu_per_passing_trial'], TL['aiu_per_passing_trial']   # one AIU is one cent


def wilson(k, n, z=1.96):
    """The 95% range around k passes in n trials, as the course's range calculator gives it."""
    p = k / n
    mid, half = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(100 * max(0, mid - half)), round(100 * min(1, mid + half))


# s14: Ollama is newer than 0.17.1 and lists the model.
ollama_log = log('s14.log')
ver = tuple(int(x) for x in re.search(r'ollama version is (\d+)\.(\d+)\.(\d+)', ollama_log).groups())
assert ver > (0, 17, 1), ver
assert re.search(r'^qwen3\.5:9b\s+\S+\s+6\.6 GB', ollama_log, re.M)
# s16: the plan has five blocks and ends with qwen-local and its model.
dry = log('s16.log').rstrip().splitlines()
assert any(re.match(r'Plans:\s+5$', l) for l in dry)
last = max(n for n, l in enumerate(dry) if l.startswith('── '))
assert dry[last] == '── qwen-local ──' and any('Model:' in l and 'qwen3.5:9b' in l for l in dry[last:])
# s17, s18: a one-column table, two of five; no baseline to compare with.
run = log('s17.log').rstrip().splitlines()
tail_from = next(n for n, l in enumerate(run) if 'Comparison unavailable — baseline not run' in l)
tail_to = next(n for n, l in enumerate(run) if l.strip().startswith('stimuli'))
TAIL = [l.rstrip() for l in run[tail_from:tail_to + 1] if l.strip()]
# The comparison line is over 64 characters: wrapped where the lesson page wraps it, nothing else changed.
wrapped = []
for l in TAIL:
    if ' (no observed' in l:
        head, rest = l.split(' (no observed', 1)
        wrapped += [head, '    (no observed' + rest]
    else:
        wrapped.append(l)
TAIL = wrapped
assert any(re.match(r'\s*eval\s+qwen-local\s*$', l) for l in TAIL) and any('✘ 2/5' in l for l in TAIL), TAIL
# Each failed trial's grader and what it found, from the records (the console wraps the long ones).
FAILS = {t['stimulus']: (t['grader'], t['evidence']) for t in TRIALS if not t['passed']}
# s19, s20: five trials, two passing, none in ERROR, no cost, about 365 thousand in and under 4 thousand out.
assert (N, P) == (5, 2) and not any(t['error'] for t in TRIALS) and all(t['cost'] is None for t in TRIALS)
assert set(FAILS) == {t['stimulus'] for t in TRIALS if not t['passed']}, FAILS
assert 360_000 <= TIN <= 370_000 and 3_500 < TOUT < 4_000, (TIN, TOUT)
MEDIAN = statistics.median(t['inputTokens'] + t['outputTokens'] for t in TRIALS)
# s08, s25: nothing came from cache.
assert all(t['cacheReadTokens'] == 0 for t in TRIALS)
assert '"cacheReadTokens": 0,' in (D / 'src/run/record.json').read_text()
# s21: about three and a half cents in, a fraction of a cent out, 3.8 cents in all, 1.9 cents per passing trial;
#      haiku-low about a fifth of a cent, terra-low 2.8 cents.
assert 3.4 <= CIN * 100 <= 3.8 and COUT * 100 < 0.25, (CIN, COUT)
assert round(TOTAL * 100, 1) == 3.8 and round(PER_PASS * 100, 1) == 1.9, (TOTAL, PER_PASS)
assert 0.18 <= HL_C <= 0.22 and round(TL_C, 1) == 2.8, (HL_C, TL_C)
# s13, s23: the account's variants passed every trial that finished.
assert L16['every_finished_trial_passed'] and HL['passed'] == HL['trials'] == 15 and TL['passed'] == TL['trials']
# s23: the three failures, by the grader that failed them; one trial of five loaded the skill, and none of
#      the three that failed did.
assert FAILS['security'][0] == 'under-security' and FAILS['refactor'][0] == 'adds-nothing'
assert FAILS['after-release'][0] == 'entry-in-new-unreleased'
LOADED = [t['stimulus'] for t in TRIALS if t['skillActivations'] > 0]
assert len(LOADED) == 1 and not any(s in FAILS for s in LOADED), LOADED
# s23: the after-release trial wrote its entry under a version heading of its own, not under Unreleased.
assert 'no \'## [Unreleased]\' heading' in FAILS['after-release'][1]
# s24: 12 to 77 percent against 80 to 100: no overlap.
RQ, RH = wilson(P, N), wilson(HL['passed'], HL['trials'])
assert RQ == (12, 77) and RH == (80, 100) and RQ[1] < RH[0], (RQ, RH)
# s25: each trial took minutes; about nine times haiku-low's cost per passing trial, under terra-low's.
assert all(t['durationMs'] >= 60_000 for t in TRIALS)
assert 8.5 < PER_PASS * 100 / HL_C < 9.5 and PER_PASS * 100 < TL_C, PER_PASS * 100 / HL_C

cents = lambda c: f'{c:.1f}¢'
usd = lambda d: f'${d:.4f}'
num = lambda n: f'{n:,}'

# ---- Hook ----------------------------------------------------------------------------------------
framed('s01', 'Vally &amp; Agent Evals', 'A model from your own provider', f'''<div class="cols wide terms">
    {block("acct", "structure", "Your Copilot account", "every trial so far", words=True)}
    {block("own", "attention", "A provider of your own", "one you pay directly, or run yourself", words=True)}
  </div>''', [
    {"type": "focus", "target": "acct", "at": "0~copilot account", "color": "blue"},
    {"type": "focus", "target": "own", "at": "2~provider", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:108px}.terms .semantic-block{min-height:230px}.terms .label{font-size:36px}')

# ---- Chapter: Evaluate the model you ship --------------------------------------------------------
EB1 = 'Evaluate the model you ship'
framed('s02', EB1, 'Same name, different behavior', f'''<div class="cols terms">
    {block("stored", "structure", "How it is stored", "often compressed to fit smaller machines", words=True)}
    {block("calls", "transform", "How tool calls become text", "what the model actually sees", words=True)}
    {block("defaults", "attention", "Its default settings", "chosen by whoever serves it", words=True)}
  </div>
  <p class="note">The copy we run here is a 4-bit compressed version.</p>''', [
    {"type": "focus", "target": "stored", "at": "3~stored", "color": "blue"},
    {"type": "focus", "target": "calls", "at": "4~tool calls", "color": "cyan"},
    {"type": "focus", "target": "defaults", "at": "5~default", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "6"}],
    css='.terms .semantic-block{min-height:280px}.terms .title{font-size:40px}.terms .label{font-size:34px}.stage{gap:34px}')

framed('s03', EB1, 'Only the endpoint can tell', f'''{card('seen', f'another local model on our computer, {mono("gpt-oss:20b")} · what its server answered',
        code('⟦err:400 invalid tool call arguments⟧', 'text'))}
  <div class="cols terms">
    {block("ep", "structure", "The endpoint", "the one the app calls", words=True)}
    {block("mname", "structure", "The model name", "the one the app sends", words=True)}
    {block("same", "attention", "Everything else", "the same stimuli, graders and skill", words=True)}
  </div>''', [
    {"type": "focus", "target": "err", "at": "1~refused", "color": "red"},
    {"type": "focus", "target": "ep", "at": "4~endpoint", "color": "blue"},
    {"type": "focus", "target": "mname", "at": "4~model name", "color": "blue"},
    {"type": "focus", "target": "same", "at": "4~keep", "color": "yellow"}],
    css='.stage{gap:36px}.card{width:100%}.card > .code.dark{font-size:38px;padding:24px 32px}.card .who{font-size:30px}'
        '.terms .semantic-block{min-height:200px}.terms .title{font-size:40px}.terms .label{font-size:34px}')

# ---- Chapter: Bring your own key ------------------------------------------------------------------
EB2 = 'Bring your own key'
framed('s04', EB2, 'The executor runs the agent', f'''{block("def", "structure", "executor", "The part of Vally that runs the agent for each trial.")}
  <div class="cols steps">
    {block("st1", "transform", "starts a session", "", words=True, step=1)}
    {block("st2", "transform", "sends the stimulus", "", words=True, step=2)}
    {block("st3", "transform", "records what happened", "", words=True, step=3)}
  </div>
  <div class="cols wide terms">
    {block("sdk", "structure", "copilot-sdk", "the built-in executor: models through your Copilot account")}
    {block("byok", "attention", "bring your own key", "the executor calls a provider you choose, with your credentials", words=True)}
  </div>''', [
    {"type": "focus", "target": "def", "at": "1", "color": "blue"},
    {"type": "focus", "target": "st1", "at": "2~starts", "color": "cyan"},
    {"type": "focus", "target": "st2", "at": "2~sends", "color": "cyan"},
    {"type": "focus", "target": "st3", "at": "2~records", "color": "cyan"},
    {"type": "focus", "target": "sdk", "at": "3~built-in", "color": "blue"},
    {"type": "focus", "target": "byok", "at": "4", "color": "yellow"}],
    css='.stage{gap:22px}.stage > .semantic-block{width:100%;padding-top:18px;padding-bottom:20px}'
        '.stage > .semantic-block .label{font-size:34px}'
        '.steps .semantic-block{min-height:0;padding-top:16px;padding-bottom:18px}.steps .title{font-size:34px}.steps .label{display:none}'
        '.terms .semantic-block{min-height:0;padding-top:18px;padding-bottom:20px}.terms .title{font-size:38px}.terms .label{font-size:30px}')

BYOK_NOTE = f"""<p class="note">An eval file’s defaults, for a hosted provider · checked with {mono('vally lint')}, not run</p>"""
BYOK_CSS = ('.code.dark.byok{font-size:34px;line-height:1.42;padding:20px 32px;min-width:900px}.callout{font-size:32px}'
            '.stage{gap:18px}.note{margin:0}')
# s05 and s05b are one code box in one place: the first walks down to the provider block, the second reads its fields.
framed('s05', EB2, 'Where the executor is set', f'''<div class="annotated">
    {code(byok, 'yaml', 'byok')}
    {callouts(('model', 'the provider’s name for the model'), ('name', 'still the built-in executor'))}
  </div>
  {BYOK_NOTE}''', [
    {"type": "focus", "target": "dflt", "at": "0~defaults", "color": "blue"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "model", "at": "3", "color": "blue"},
    {"type": "focus", "target": "name", "at": "4", "color": "blue"},
    {"type": "focus", "target": "cfg", "at": "5~config", "color": "blue"},
    {"type": "focus", "target": "prov", "at": "5~provider block", "color": "yellow"}], css=BYOK_CSS)

framed('s05b', EB2, 'What the provider block holds', f'''<div class="annotated">
    {code(byok, 'yaml', 'byok')}
    {callouts(('url', 'the address: the only required field'), ('type', 'the kind of interface'),
              ('key', 'the name of a variable, not the key'))}
  </div>
  {BYOK_NOTE}''', [
    {"type": "focus", "target": "prov", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "url", "at": "1", "color": "blue"},
    {"type": "focus", "target": "type", "at": "2", "color": "blue"},
    {"type": "focus", "target": "key", "at": "4", "color": "yellow"}], css=BYOK_CSS)

lint_rows = wrap_marked(lint_err, 62, "unknown field 'apiKey'", 'nokey')
unset_rows = ['ERROR  hello'] + wrap_marked(unset_err, 62, 'but it is not set', 'unset', indent=' ')
unset_rows[1] = ' ' + unset_rows[1]
framed('s06', EB2, 'No field for a key', f'''<div class="annotated">
    {code(chr(10).join(lint_rows), 'text', 'out')}
    {callouts(('nokey', 'lint, with a key in the file'))}
  </div>
  <div class="annotated">
    {code(chr(10).join(unset_rows), 'text', 'out')}
    {callouts(('unset', 'a run, with the variable not set'))}
  </div>
  <p class="note">Our own probes of the block above, with Vally 0.21.0</p>''', [
    {"type": "focus", "target": "nokey", "at": "1~no field", "color": "red"},
    {"type": "focus", "target": "none", "at": "2"},
    {"type": "focus", "target": "unset", "at": "3~isn't set", "color": "red"}],
    css='.code.dark.out{font-size:28px;line-height:1.4;padding:16px 26px;min-width:1160px}.callout{font-size:30px}'
        '.stage{gap:20px}.note{margin:0}')

framed('s07', EB2, 'A local model needs no key', f'''{block("oll", "structure", "Ollama", "A free program that downloads open models and serves them on your machine.")}
  <div class="annotated">
    {code(local_block.replace('baseUrl: http://localhost:11434/v1', '⟦lurl:baseUrl: http://localhost:11434/v1⟧'), 'yaml', 'local')}
    {callouts(('lurl', 'Ollama’s address on this computer · no key'))}
  </div>''', [
    {"type": "focus", "target": "oll", "at": "1", "color": "blue"},
    {"type": "focus", "target": "lurl", "at": "2~local address", "color": "yellow"}],
    css='.stage{gap:30px}.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:36px}'
        '.code.dark.local{font-size:36px;line-height:1.45;min-width:900px}.callout{font-size:32px}')

framed('s08', EB2, 'Tokens, but no cost', f'''<div class="annotated">
    {panel('rec')}
    {callouts(('tu', 'counted as before'), ('cache', 'nothing came from cache'),
              ('bym', 'the tokens for each model: what we price'), ('end', 'no cost block follows'))}
  </div>''', [
    {"type": "focus", "target": "tu", "at": "1~token usage", "color": "blue"},
    {"type": "scroll", "target": "#rec", "to": "end", "at": "2"},
    {"type": "focus", "target": "end", "at": "2~absent", "color": "yellow"},
    {"type": "focus", "target": "bym", "at": "3~each model", "color": "blue"},
    {"type": "scroll", "target": "#rec", "to": "top", "at": "4"},
    {"type": "focus", "target": "cache", "at": "4~cache", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "6"}], layout='layout-file')

# ---- Chapter: A variant on a local model -----------------------------------------------------------
EB3 = 'A variant on a local model'
framed('s09', EB3, 'Three new paths to vary', f'''<div class="annotated">
    {panel('exp')}
    {callouts(('pexec', 'the executor'), ('ptime', 'the time limit'), ('pruns', 'the number of trials'))}
  </div>''', [
    {"type": "focus", "target": "vary", "at": "3~vary list", "color": "blue"},
    {"type": "focus", "target": "pexec", "at": "4~executor", "color": "yellow"},
    {"type": "focus", "target": "ptime", "at": "4~time limit", "color": "yellow"},
    {"type": "focus", "target": "pruns", "at": "4~number of trials", "color": "yellow"},
    {"type": "focus", "target": "pexec", "at": "5~executor path", "color": "blue"}], layout='layout-file')

framed('s10', EB3, 'The fifth variant', f'''<div class="annotated">
    {panel('exp')}
    {callouts(('timeout', 'slow: nine minutes, not three'), ('runs', 'each stimulus once, not three times'),
              ('url', 'Ollama’s address · no key'))}
  </div>''', [
    {"type": "scroll", "target": "#exp", "to": "35-43", "at": "t=0", "duration": 0},
    {"type": "focus", "target": "qname", "at": "0~variant", "color": "blue"},
    {"type": "focus", "target": "timeout", "at": "1~nine minutes", "color": "yellow"},
    {"type": "focus", "target": "runs", "at": "2~once", "color": "yellow"},
    {"type": "scroll", "target": "#exp", "to": "end", "at": "3"},
    {"type": "focus", "target": "url", "at": "3~address", "color": "blue"}], layout='layout-file')

framed('s11', EB3, 'One worker at a time', f'''<div class="cols wide terms">
    {block("w2", "structure", "--workers 2", "each trial waits on the other, and can run out of its nine minutes")}
    {block("w1", "attention", "--workers 1", "one request at a time, the way this server answers")}
  </div>''', [
    {"type": "focus", "target": "w1", "at": "0~one worker", "color": "yellow"},
    {"type": "focus", "target": "w2", "at": "1~two workers", "color": "blue"}],
    css='.terms .semantic-block{min-height:280px}.terms .label{font-size:36px}')

framed('s12', EB3, 'A price for the arithmetic', f'''<table class="data-table price">
    <thead><tr><th></th><th class="num">per million tokens</th></tr></thead>
    <tbody>
      <tr><td>input tokens</td><td class="num">{cell('pin', f'${PRICE_IN:.2f}')}</td></tr>
      <tr><td>output tokens</td><td class="num">{cell('pout', f'${PRICE_OUT:.2f}')}</td></tr>
    </tbody>
  </table>
  <p class="note">Made up for the arithmetic · not any provider’s price</p>''', [
    {"type": "focus", "target": "pin", "at": "1~ten cents", "color": "yellow"},
    {"type": "focus", "target": "pout", "at": "1~forty cents", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "2"}],
    css='.price{font-size:48px}.price th{font-size:30px}.price td{padding-top:26px;padding-bottom:26px}.stage{gap:30px}')

# ---- Chapter: Run a variant on your provider -------------------------------------------------------
EB4 = 'Run a variant on your provider'
VARIANT_HEAD = '<thead><tr><th>Variant</th><th class="num">trials passed</th><th class="num">per passing trial</th></tr></thead>'
framed('s13', EB4, 'What would you expect?', f'''<table class="data-table full variants">
    {VARIANT_HEAD}
    <tbody>
      <tr><td class="mono">haiku-low</td><td class="num">{cell('acct', f"{HL['passed']} of {HL['trials']}")}</td><td class="num">{cents(HL_C)}</td></tr>
      <tr><td class="mono">terra-low</td><td class="num">{cell('acct', f"{TL['passed']} of {TL['trials']}")}</td><td class="num">{cents(TL_C)}</td></tr>
      <tr><td class="mono">{cell('q', 'qwen-local')}</td><td class="num"></td><td class="num"></td></tr>
    </tbody>
  </table>
  <p class="note">The first two rows are from the cost comparison · {SRC if PROVISIONAL else 'our run'}</p>''', [
    {"type": "focus", "target": "acct", "at": "2~every trial", "color": "blue"},
    {"type": "focus", "target": "q", "at": "3", "color": "yellow"}],
    css='.variants{font-size:44px}.variants th{font-size:30px}.variants td{padding-top:26px;padding-bottom:26px}'
        '.variants td.mono{font-family:var(--font-code)}.stage{gap:30px}')

tail = '\n'.join(TAIL).replace('Comparison unavailable — baseline not run', '⟦cmp:Comparison unavailable — baseline not run⟧', 1) \
                      .replace('✘ 2/5', '⟦tab:✘ 2/5⟧', 1)
assert '⟦cmp:' in tail and '⟦tab:' in tail
framed('s18', EB4, 'No baseline in this run', f'''<div class="annotated">
    {code(tail, 'text', 'tail')}
    {callouts(('cmp', 'only qwen-local ran'), ('tab', 'two of five'))}
  </div>
  <p class="note">The end of the run’s output · {SRC}</p>''', [
    {"type": "focus", "target": "cmp", "at": "1~unavailable", "color": "yellow"},
    {"type": "focus", "target": "tab", "at": "2~only", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.code.dark.tail{font-size:34px;line-height:1.42;padding:22px 32px;min-width:1100px}.callout{font-size:32px}'
        '.stage{gap:22px}.note{margin:0}')

calc = [('Trials', str(N), ''), ('Passing', f'{P} of {N}', ''), ('ERROR', str(sum(t['error'] for t in TRIALS)), ''),
        ('Total cost', '—', 'nocost'), ('Per passing trial', '—', 'nocost'), ('Median tokens', f'{MEDIAN / 1000:.1f}k', '')]
framed('s19', EB4, 'No cost was recorded', f'''{card('calc', f'the course’s cost calculator · on {mono("qwen-local/results.jsonl")}',
        '<table class="data-table full calc"><tbody>' + ''.join(
            f'<tr><td>{k}</td><td class="num">{cell(c, v) if c else cell("c" + str(n), v)}</td></tr>'
            for n, (k, v, c) in enumerate(calc)) + '</tbody></table>')}
  <p class="note">{SRC}</p>''', [
    {"type": "focus", "target": "c0", "at": "1~five trials", "color": "blue"},
    {"type": "focus", "target": "c1", "at": "1~two", "color": "blue"},
    {"type": "focus", "target": "c2", "at": "1~none", "color": "blue"},
    {"type": "focus", "target": "nocost", "at": "2~dash", "color": "yellow"}],
    css='.card{width:1100px}.card .who{font-size:30px}.calc{font-size:36px}.calc td{padding-top:13px;padding-bottom:13px}'
        '.stage{gap:18px}.note{margin:0}')

rows = ''.join(f'''<tr><td class="mono">{t['stimulus']}</td><td>{'yes' if t['passed'] else 'no'}</td>
        <td class="num">{num(t['inputTokens'])}</td><td class="num">{num(t['outputTokens'])}</td></tr>\n''' for t in TRIALS)
framed('s20', EB4, 'Tokens, trial by trial', f'''<table class="data-table full toks">
    <thead><tr><th>Stimulus</th><th>Passed</th><th class="num">input tokens</th><th class="num">output tokens</th></tr></thead>
    <tbody>
{rows}      <tr><td>Total</td><td>{P} of {N}</td><td class="num">{cell('tin', num(TIN))}</td><td class="num">{cell('tout', num(TOUT))}</td></tr>
    </tbody>
  </table>
  <p class="note">From each record’s {mono('byModel')} block · {SRC}</p>''', [
    {"type": "focus", "target": "tin", "at": "2~three hundred", "color": "yellow"},
    {"type": "focus", "target": "tout", "at": "2~under four thousand", "color": "yellow"}],
    css='.toks{font-size:34px}.toks th{font-size:28px}.toks td{padding-top:13px;padding-bottom:13px}'
        '.toks td.mono{font-family:var(--font-code)}.stage{gap:18px}.note{margin:0}')

arith = '\n'.join([
    f'⟦ain:{num(TIN):>8} × ${PRICE_IN:.2f} per million = {usd(CIN)}⟧',
    f'⟦aout:{num(TOUT):>8} × ${PRICE_OUT:.2f} per million = {usd(COUT)}⟧',
    f'⟦atot:{"total, " + str(N) + " trials":>29} = {usd(TOTAL)}⟧',
    f'⟦app:{"÷ " + str(P) + " passing trials":>29} = {usd(PER_PASS)}⟧'])
PP_HEAD = f'About {PER_PASS * 100:.1f} cents per pass'
framed('s21', EB4, PP_HEAD, f'''<div class="annotated">
    {code(arith, 'text', 'arith')}
    {callouts(('ain', 'input'), ('aout', 'output'), ('atot', f'about {TOTAL * 100:.1f} cents'), ('app', f'about {PER_PASS * 100:.1f} cents'))}
  </div>
  <table class="data-table full variants">
    <thead><tr><th>Variant</th><th class="num">per passing trial</th></tr></thead>
    <tbody>
      <tr><td class="mono">qwen-local <span class="unit">at the made-up price</span></td><td class="num">{cents(PER_PASS * 100)}</td></tr>
      <tr><td class="mono">haiku-low</td><td class="num">{cell('hl', cents(HL_C))}</td></tr>
      <tr><td class="mono">terra-low</td><td class="num">{cell('tl', cents(TL_C))}</td></tr>
    </tbody>
  </table>''', [
    {"type": "focus", "target": "ain", "at": "1~input", "color": "blue"},
    {"type": "focus", "target": "aout", "at": "1~output", "color": "blue"},
    {"type": "focus", "target": "atot", "at": "2", "color": "blue"},
    {"type": "focus", "target": "app", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "hl", "at": "4~haiku", "color": "blue"},
    {"type": "focus", "target": "tl", "at": "4~terra", "color": "blue"}],
    css='.code.dark.arith{font-size:34px;line-height:1.45;padding:20px 32px;min-width:1000px}.callout{font-size:32px}'
        '.variants{font-size:34px}.variants th{font-size:28px}.variants td{padding-top:12px;padding-bottom:12px}'
        '.variants td.mono{font-family:var(--font-code)}.variants .unit{font-family:var(--font-body)}.stage{gap:24px}')

# ---- Chapter: What changed --------------------------------------------------------------------------
EB5 = 'What changed'
framed('s22', EB5, 'A few lines changed', f'''<div class="cols terms">
    {block("k1", "structure", "the eval file", "", words=True)}
    {block("k2", "structure", "stimuli and graders", "", words=True)}
    {block("k3", "structure", "the skill", "", words=True)}
    {block("k4", "structure", "the results folder", "", words=True)}
  </div>
  {block("chg", "attention", "what changed", "a few lines in one variant", words=True)}''', [
    {"type": "focus", "target": "k1", "at": "2~eval file", "color": "blue"},
    {"type": "focus", "target": "k2", "at": "2~stimuli", "color": "blue"},
    {"type": "focus", "target": "k3", "at": "2~skill", "color": "blue"},
    {"type": "focus", "target": "k4", "at": "2~results", "color": "blue"},
    {"type": "focus", "target": "chg", "at": "3~few lines", "color": "yellow"}],
    css='.terms .semantic-block{min-height:170px;justify-content:center}.terms .title{font-size:36px}.terms .label{display:none}'
        '.stage{gap:32px}.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:38px}')

vrows = ''
for t in TRIALS:
    s = t['stimulus']
    found = f'<span data-concept="f-{s}" data-rep="cell">{FAILS[s][1].replace("&", "&amp;").replace("<", "&lt;")}</span>' if s in FAILS else ''
    loaded = cell('act', 'yes') if t['skillActivations'] else cell('noact', 'no')
    vrows += (f'<tr><td class="mono">{s}</td><td>{"passed" if t["passed"] else "failed"}</td>'
              f'<td>{loaded}</td><td class="mono small">{found}</td></tr>\n')
framed('s23', EB5, 'Four trials skipped the skill', f'''<table class="data-table full verdicts">
    <thead><tr><th>Stimulus</th><th>Verdict</th><th>Skill loaded</th><th>What the grader found</th></tr></thead>
    <tbody>
{vrows}    </tbody>
  </table>
  <p class="note">{mono('skill_activation')} events in each saved trial · {SRC}</p>''', [
    {"type": "focus", "target": "f-security", "at": "2~security fix", "color": "yellow"},
    {"type": "focus", "target": "f-refactor", "at": "2~refactor", "color": "yellow"},
    {"type": "focus", "target": "f-after-release", "at": "2~made up", "color": "yellow"},
    {"type": "focus", "target": "act", "at": "3~only one", "color": "blue"},
    {"type": "focus", "target": "noact", "at": "3~none", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.verdicts{font-size:32px}.verdicts th{font-size:28px}'
        '.verdicts td,.verdicts th{padding-top:11px;padding-bottom:11px;padding-right:36px;white-space:nowrap}'
        '.verdicts td.mono{font-family:var(--font-code)}.verdicts td.small{font-size:28px;white-space:normal}'
        '.stage{gap:18px}.note{margin:0}')

framed('s24', EB5, 'Five trials can settle worse', f'''<table class="data-table full ranges">
    <thead><tr><th>Variant</th><th class="num">trials passed</th><th class="num">95% range</th></tr></thead>
    <tbody>
      <tr><td class="mono">qwen-local</td><td class="num">{P} of {N}</td><td class="num">{cell('rq', f'{RQ[0]}% to {RQ[1]}%')}</td></tr>
      <tr><td class="mono">haiku-low</td><td class="num">{HL['passed']} of {HL['trials']}</td><td class="num">{cell('rh', f'{RH[0]}% to {RH[1]}%')}</td></tr>
    </tbody>
  </table>
  <p class="note">Ranges from the course’s range calculator · {SRC}</p>''', [
    {"type": "focus", "target": "rq", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "rh", "at": "2", "color": "blue"},
    {"type": "focus", "target": "none", "at": "3"}],
    css='.ranges{font-size:46px}.ranges th{font-size:30px}.ranges td{padding-top:30px;padding-bottom:30px}'
        '.ranges td.mono{font-family:var(--font-code)}.stage{gap:30px}')

framed('s25', EB5, 'Cheap tokens, costly passes', f'''<table class="data-table full variants">
    <thead><tr><th>Variant</th><th class="num">per passing trial</th></tr></thead>
    <tbody>
      <tr><td class="mono">qwen-local <span class="unit">at the made-up price</span></td><td class="num">{cell('cq', cents(PER_PASS * 100))}</td></tr>
      <tr><td class="mono">haiku-low</td><td class="num">{cell('ch', cents(HL_C))}</td></tr>
      <tr><td class="mono">terra-low</td><td class="num">{cell('ct', cents(TL_C))}</td></tr>
    </tbody>
  </table>
  <div class="cols wide terms">
    {block("f1", "attention", f"{N - P} of {N} trials failed", "", words=True)}
    {block("f2", "attention", "nothing from cache", "every turn pays for the whole conversation", words=True)}
  </div>''', [
    {"type": "focus", "target": "cq", "at": "2~passing trial", "color": "yellow"},
    {"type": "focus", "target": "ch", "at": "2~haiku", "color": "blue"},
    {"type": "focus", "target": "ct", "at": "3~terra", "color": "blue"},
    {"type": "focus", "target": "f1", "at": "4~three of five", "color": "yellow"},
    {"type": "focus", "target": "f2", "at": "4~nothing from cache", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.variants{font-size:38px}.variants th{font-size:28px}.variants td{padding-top:16px;padding-bottom:16px}'
        '.variants td.mono{font-family:var(--font-code)}.variants .unit{font-family:var(--font-body)}'
        '.terms .semantic-block{min-height:150px;justify-content:center}.terms .title{font-size:38px}.terms .label{font-size:30px}.stage{gap:28px}')

msteps = [('m1', 'structure', 'Run', 'the endpoint your app calls'), ('m2', 'transform', 'Count', 'the tokens'),
          ('m3', 'attention', 'Price', 'at your own rates'), ('m4', 'change', 'Divide', 'by the passing trials')]
framed('s26', EB5, 'One model, served one way', f'''<div class="cols">
    {''.join(block(c, r, t, l, step=i) for i, (c, r, t, l) in enumerate(msteps, 1))}
  </div>''', [
    {"type": "focus", "target": "m1", "at": "2~run", "color": "blue"},
    {"type": "focus", "target": "m2", "at": "2~count", "color": "cyan"},
    {"type": "focus", "target": "m3", "at": "2~price", "color": "yellow"},
    {"type": "focus", "target": "m4", "at": "2~divide", "color": "orange"}],
    css='.cols .semantic-block{min-height:260px}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('The key', 'in the environment of the vally command'),
    ('The tokens', 'counted, for each model'),
    ('The cost', 'absent: we price the tokens')], 1))
framed('s27', 'Recap', 'Where is the key kept?', f'''<div class="semantic-block" id="own" data-role="structure">
    <div class="title words">your own provider</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#own", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"}], layout='layout-expand',
    css='#own{width:100%;padding:36px 40px 44px;gap:24px}'
        '#own .parts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;width:100%}'
        '#own .part{min-height:260px}#own .part .title{font-size:52px;line-height:1.2}'
        '#own .part .label{font-size:32px}')

scene('s28', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Put a ceiling on a trial</h1>
  <p class="lead">How do you fail, or stop, a trial that costs or takes too much?</p>
  <p class="note">Exercises are on the lesson page · Source: Vally docs, Eval Spec reference: Executor config &amp; BYOK</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', 'PROVISIONAL run' if PROVISIONAL else RUN)
