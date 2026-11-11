"""Generate lesson 4's scene pages. File panels are inserted afterwards by panels.sh.

Same parts as lessons 1 to 3: the theme's one frame (eyebrow, short display-serif headline, .stage),
code and files in a dark box on the left with notes on the right (.annotated + .callout). Nothing
here sets a colour or a font outside the theme's variables; a scene's own CSS is sizes and spacing.

Everything quoted on screen is read from src/:
  src/six-requests.eval.yaml, SKILL.md   the practice folder's files (identical to verified/lesson-04)
  src/earlier-terra.patch                the gpt-5.6-terra patch from the lesson 1 video's run
  src/state/notes/failures.md            the notes file the lesson writes; s13.tape copies it into
                                         practice/notes/ out of sight
  src/run/<stimulus>-<model>.patch       the twelve patches of the run this video's s12 records
                                         (name in src/run/RUN). While src/run/PROVISIONAL exists they
                                         are stand-ins copied from verified/lesson-04.

The asserts below are what the narration says about the run. If the video's own run differs, an assert
fails: reword the outcome sentences, the NOTES here and src/state/notes/failures.md, then change the assert.

Run from anywhere:  python3 build-src/make-scenes.py && bash build-src/panels.sh
"""
import json, pathlib, re, subprocess, textwrap

D = pathlib.Path(__file__).resolve().parent.parent
SKILL = pathlib.Path.home() / 'src/me/skills/skills/video-lesson'
MODELS = ('claude-haiku-4.5', 'gpt-5.6-terra')
H, T = MODELS


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


# ---- The real things, read from src/ -----------------------------------------------------------
STIMULI = ('typo-fix', 'refactor', 'two-changes', 'security', 'parser', 'after-release')


def prompts():
    """Each stimulus's request, word for word: the lines of its `prompt: |` block joined by spaces."""
    out, name, grab = {}, None, False
    for line in (D / 'src/six-requests.eval.yaml').read_text().splitlines():
        m = re.match(r'  - name: (\S+)', line)
        if m:
            name, grab = m.group(1), False
        elif line.strip() == 'prompt: |':
            grab, out[name] = True, []
        elif grab and line.startswith('      '):
            out[name].append(line.strip())
        else:
            grab = False
    return {k: ' '.join(v) for k, v in out.items()}


PROMPT = prompts()
assert tuple(PROMPT) == STIMULI, list(PROMPT)
assert 'graders' not in (D / 'src/six-requests.eval.yaml').read_text()

RUN = (D / 'src/run/RUN').read_text().strip()
PROVISIONAL = (D / 'src/run/PROVISIONAL').exists()


def added(stim, model):
    """The lines a trial's patch added to CHANGELOG.md, verbatim, blank lines dropped."""
    lines = (D / f'src/run/{stim}-{model}.patch').read_text().splitlines()
    assert any(l.startswith('+++ b/CHANGELOG.md') for l in lines), (stim, model)
    return [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++') and l[1:].strip()]


ADDED = {(s, m): added(s, m) for s in STIMULI for m in MODELS}
PR = re.compile(r'\(#(\d+)\)\s*$')
entries = lambda s, m: [l for l in ADDED[s, m] if l.startswith('- ')]
heads = lambda s, m: [l for l in ADDED[s, m] if l.startswith('#')]

# ---- What the narration says about this run ------------------------------------------------------
# s13, s14: both models recorded the refactor, under Changed.
for m in MODELS:
    assert heads('refactor', m) == ['### Changed'] and len(entries('refactor', m)) == 1, ADDED['refactor', m]
# s15: haiku gave no pull request number on the typo fix; terra made one up.
assert not PR.search(entries('typo-fix', H)[0]) and PR.search(entries('typo-fix', T)[0])
TYPO_PR = PR.search(entries('typo-fix', T)[0]).group(0).strip()
# s16: both split the two changes into two entries, Added and Fixed, both citing #60.
for m in MODELS:
    e = entries('two-changes', m)
    assert len(e) == 2 and all(PR.search(x).group(1) == '60' for x in e), e
    assert heads('two-changes', m) == ['### Fixed'], heads('two-changes', m)   # the Added section existed
# s17: both filed the security fix under Fixed.
for m in MODELS:
    assert heads('security', m) == ['### Fixed'], heads('security', m)
# s18: haiku's entry names the streaming parser; terra's does not.
HOW = 'by using streaming JSON parser'
assert HOW in entries('parser', H)[0] and 'pars' not in entries('parser', T)[0].lower()
# s19: both added an Unreleased heading; haiku with brackets, terra without.
assert heads('after-release', H)[0] == '## [Unreleased]' and heads('after-release', T)[0] == '## Unreleased'

# The note we wrote for each trial, shown beside it (s14 to s19). Ours; reworded if the run differs.
NOTES = {
    'refactor': ('users cannot see this', 'same problem'),
    'typo-fix': ('no number: fine', 'a number nobody gave it'),
    'two-changes': ('two entries, both #60: fine', 'same split: fine'),
    'security': ('under Fixed', 'under Fixed'),
    'parser': ('how it was coded', 'what users notice: fine'),
    'after-release': ('matches the file: fine', 'no brackets'),
}

# The notes file: its first lines are the failure modes, each with the trial that shows it.
notes_lines = (D / 'src/state/notes/failures.md').read_text().splitlines()
assert notes_lines[0] == '# Failure modes' and notes_lines[8] == '# Notes, one per trial'
MODES = [re.match(r'^(\d)\. (.*)\. ([a-z-]+, \w+)\.$', l).groups() for l in notes_lines[2:7]]
assert [n for n, _, _ in MODES] == list('12345')
assert sum(l.startswith('- ') for l in notes_lines[9:]) == 12

skill_lines = (D / 'src/SKILL.md').read_text().splitlines()
RULES = skill_lines[9:13]
assert RULES[0] == '- Add the entry under Unreleased, in the right category.' and RULES[2] == '- Reference the pull request.'

earlier = [l[1:] for l in (D / 'src/earlier-terra.patch').read_text().splitlines() if l.startswith('+- ')]
assert len(earlier) == 1 and PR.search(earlier[0])
mark_pr = lambda e, cid='pr': PR.sub(lambda m: f'⟦{cid}:{m.group(0).strip()}⟧', e)

# ---- Hook ----------------------------------------------------------------------------------------
FRAGS = [('refactor', 'Nothing changes for users, it\'s purely a cleanup.'),
         ('two-changes', 'while I was in there I fixed the bug'),
         ('parser', 'I swapped JSON.parse for a streaming parser')]
for s, f in FRAGS:
    assert f in PROMPT[s], (s, f)
framed('s01', 'Vally &amp; Agent Evals', 'Read the runs first', f'''<div class="cols pair">
    {quote('tidy', 'The request so far', '“' + esc(PROMPT['typo-fix']) + '”')}
    <div class="messy">
      {quote('m1', 'Messier', '“… ' + esc(FRAGS[0][1]) + '”')}
      {quote('m2', 'Messier', '“… ' + esc(FRAGS[1][1]) + ' …”')}
      {quote('m3', 'Messier', '“… ' + esc(FRAGS[2][1]) + ' …”')}
    </div>
  </div>''', [
    {"type": "focus", "target": "tidy", "at": "1~tidier", "color": "blue"},
    {"type": "focus", "target": "m1", "at": "2~can't see", "color": "yellow"},
    {"type": "focus", "target": "m2", "at": "2~bundle", "color": "yellow"},
    {"type": "focus", "target": "m3", "at": "2~coded", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "3"}],
    h='h1', title_class='scene-title chapter',
    css='.scene-title.chapter{font-size:116px}.pair{align-items:center}'
        '.messy{display:flex;flex-direction:column;gap:18px}.messy .quote{padding-top:14px;padding-bottom:14px}'
        '.messy .quote p{font-size:32px}')

# ---- Chapter: Why reading comes first ------------------------------------------------------------
EB1 = 'Why reading comes first'
framed('s02', EB1, 'Failures come from the models', f'''<div class="cols wide terms">
    {block("imagined", "structure", "A list written beforehand", "comes from your imagination", words=True)}
    {block("found", "attention", "What a model did", "found by reading a run", words=True)}
  </div>
  {card('seen', f'{mono(T)} · the entry it wrote in the first run we saw', code(mark_pr(earlier[0]), 'markdown'))}''', [
    {"type": "focus", "target": "imagined", "at": "2~imagination", "color": "blue"},
    {"type": "focus", "target": "found", "at": "2~models", "color": "yellow"},
    {"type": "focus", "target": "pr", "at": "3~made-up", "color": "yellow"}],
    css='.terms .semantic-block{min-height:200px}.terms .label{font-size:34px}.stage{gap:36px}'
        '.card{width:100%}.card > .code.dark{font-size:36px;padding:24px 32px}.card .who{font-size:30px}')

steps = [('s1', 'structure', 'Run', 'realistic requests'), ('s2', 'transform', 'Read', 'what came back'),
         ('s3', 'attention', 'Note', 'what is off'), ('s4', 'change', 'Group', 'the notes')]
framed('s03', EB1, 'Discover errors, don’t imagine them', f'''{quote('rule', 'A rule from practitioners', '“Write evaluators for errors you discover, not errors you imagine.”')}
  <div class="cols">
    {''.join(block(c, r, t, l, step=i) for i, (c, r, t, l) in enumerate(steps, 1))}
  </div>
  <p class="note">Source: Husain and Shankar, AI Evals FAQ (2026) · “evaluators” is their word for graders</p>''', [
    {"type": "focus", "target": "rule", "at": "0~write evaluators", "color": "blue"},
    {"type": "focus", "target": "s1", "at": "3~run", "color": "blue"},
    {"type": "focus", "target": "s2", "at": "3~go through", "color": "cyan"},
    {"type": "focus", "target": "s3", "at": "3~note", "color": "yellow"},
    {"type": "focus", "target": "s4", "at": "3~group", "color": "orange"},
    {"type": "focus", "target": "none", "at": "4"}],
    css='.cols .semantic-block{min-height:210px}.stage{gap:30px}.quote{width:100%}')

framed('s04', EB1, 'A failure mode has a name', f'''{block("def", "structure", "failure mode", "A named way the skill’s output goes wrong, seen in at least one real trial.")}
  <div class="cols wide terms">
    {block("ex1", "attention", "“Records a change users cannot see”", "a failure mode", words=True)}
    {block("ex2", "structure", "“Trial 3 looked odd”", "not one yet", words=True)}
  </div>''', [
    {"type": "focus", "target": "def", "at": "1", "color": "blue"},
    {"type": "focus", "target": "ex1", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "ex2", "at": "3", "color": "blue"}],
    css='.stage{gap:30px}.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:38px}'
        '.terms .semantic-block{min-height:190px}.terms .title{font-size:38px}.terms .label{font-size:34px}')

framed('s05', EB1, 'Reading changes what you want', f'''<p class="lead"><span data-concept="q" data-rep="note">Is a security fix filed under “Fixed” wrong?</span></p>
  <div class="cols wide terms">
    {block("before", "structure", "Criteria written beforehand", "incomplete", words=True)}
    {block("after", "attention", "Criteria after reading", "include what you saw", words=True)}
  </div>
  <p class="note">Source: Shankar et al., “Who Validates the Validators?” (2024)</p>''', [
    {"type": "focus", "target": "q", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "after", "at": "2~once you do", "color": "yellow"},
    {"type": "focus", "target": "before", "at": "3~beforehand", "color": "blue"}],
    css='.terms .semantic-block{min-height:240px}.terms .label{font-size:34px}.lead{font-size:44px;margin:0}.stage{gap:36px}')

framed('s06', EB1, 'How many runs are enough?', f'''<div class="cols wide terms">
    {block("hundred", "structure", "100 or more", "suggested for a real product")}
    {block("twelve", "attention", "12", "what we read here")}
  </div>
  <p class="lead"><span data-concept="stop" data-rep="note">Stop when new runs stop showing anything new.</span></p>
  <p class="note">Source: Husain and Shankar, AI Evals FAQ (2026)</p>''', [
    {"type": "focus", "target": "hundred", "at": "1~hundred", "color": "blue"},
    {"type": "focus", "target": "stop", "at": "1~stopping", "color": "blue"},
    {"type": "focus", "target": "twelve", "at": "2", "color": "yellow"}],
    css='.terms .semantic-block{min-height:280px;justify-content:center}.terms .title{font-size:104px;line-height:1.1}'
        '.terms .label{font-size:36px}.lead{font-size:40px;margin:0}.stage{gap:30px}')

# ---- Chapter: Six ordinary requests --------------------------------------------------------------
EB2 = 'Six ordinary requests'
framed('s07', EB2, 'Six stimuli, no graders', f'''<div class="annotated">
    {panel('evalfile')}
    {callouts(('typo', 'the request we know'), ('env', 'its starting changelog'),
              ('skill', 'listed once, for all six'), ('released', '1.3.0 is out: no Unreleased'))}
  </div>''', [
    {"type": "scroll", "target": "#evalfile", "to": "10-16", "at": "3"},
    {"type": "focus", "target": "typo", "at": "3~request", "color": "blue"},
    {"type": "scroll", "target": "#evalfile", "to": "15-18", "at": "4"},
    {"type": "focus", "target": "env", "at": "4~agent environment", "color": "yellow"},
    {"type": "scroll", "target": "#evalfile", "to": "top", "at": "5"},
    {"type": "focus", "target": "skill", "at": "5~once", "color": "blue"},
    {"type": "scroll", "target": "#evalfile", "to": "end", "at": "6"},
    {"type": "focus", "target": "released", "at": "6~different changelog", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "7"}], layout='layout-file')

framed('s08', EB2, 'Four more, each with a gap', f'''<div class="grid">
    {quote('refactor', 'refactor', '“' + esc(PROMPT['refactor']) + '”')}
    {quote('two', 'two-changes', '“' + esc(PROMPT['two-changes']) + '”')}
    {quote('security', 'security', '“' + esc(PROMPT['security']) + '”')}
    {quote('parser', 'parser', '“' + esc(PROMPT['parser']) + '”')}
  </div>''', [
    {"type": "focus", "target": "refactor", "at": "1", "color": "yellow"},
    {"type": "focus", "target": "two", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "security", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "parser", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px 28px;width:100%}'
        '.grid .quote{padding-top:16px;padding-bottom:18px}.grid .quote p{font-size:30px;line-height:1.36}'
        '.grid .quote .who{font-family:var(--font-code)}')

CATS = ['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security']
fmt = '⟦unrel:## [Unreleased]⟧\n' + '\n'.join(f'⟦cat{i}:### {c}⟧' for i, c in enumerate(CATS))
framed('s09', EB2, 'The changelog follows a format', f'''<div class="annotated">
    {code(fmt, 'markdown', 'fmt')}
    {callouts(('unrel', 'unshipped changes, in square brackets'), ('cat0', 'six categories, in this order'))}
  </div>
  {quote('says', 'All the skill says about it', '“' + esc(RULES[0][2:]) + '”')}
  <p class="note">Source: Keep a Changelog 1.1.0</p>''', [
    {"type": "focus", "target": "cat0", "at": "2~six categories", "color": "blue"},
    {"type": "focus", "target": "cat1", "at": "2~changed", "color": "blue"},
    {"type": "focus", "target": "cat2", "at": "2~deprecated", "color": "blue"},
    {"type": "focus", "target": "cat3", "at": "2~removed", "color": "blue"},
    {"type": "focus", "target": "cat4", "at": "2~fixed", "color": "blue"},
    {"type": "focus", "target": "cat5", "at": "2~security", "color": "blue"},
    {"type": "focus", "target": "unrel", "at": "3~unreleased", "color": "yellow"},
    {"type": "focus", "target": "says", "at": "4", "color": "blue"}],
    css='.code.dark.fmt{min-width:640px;font-size:34px;line-height:1.42;padding:20px 32px}.callout{font-size:32px}'
        '.stage{gap:22px;justify-content:flex-start}.quote{width:100%;padding-top:12px;padding-bottom:14px}.quote p{font-size:34px}')

cmd = ('vally eval -e ⟦file:evals/six-requests.eval.yaml⟧ \\\n'
       '  --model claude-haiku-4.5,gpt-5.6-terra \\\n'
       '  ⟦skip:--skip-grade⟧ --workers 2 \\\n'
       '  --output-dir results/lesson-4')
framed('s10', EB2, 'Run now, grade later', f'''<div class="annotated">
    {code(cmd, 'bash', 'cmd')}
    {callouts(('file', 'six stimuli'), ('skip', 'run and save, grade nothing'))}
  </div>
  {block("tick", "attention", "✓ with " + mono("--skip-grade"), "the trial finished · nothing was graded", words=True)}''', [
    {"type": "focus", "target": "skip", "at": "0~skip grade", "color": "blue"},
    {"type": "focus", "target": "file", "at": "2~this file", "color": "blue"},
    {"type": "focus", "target": "skip", "at": "2~states", "color": "blue"},
    {"type": "focus", "target": "tick", "at": "3", "color": "yellow"}],
    css='.code.dark.cmd{font-size:36px;line-height:1.6}.callout{font-size:32px}.stage{gap:34px}'
        '.stage > .semantic-block{width:100%}.stage > .semantic-block .label{font-size:36px}')

# ---- Chapter: Read and name ----------------------------------------------------------------------
EB3 = 'Read and name'
CASES = [('c1', 'a refactor users cannot see'), ('c2', 'two changes in one pull request'), ('c3', 'a security fix'),
         ('c4', 'a fix described in code terms'), ('c5', 'no Unreleased section')]
framed('s11', EB3, 'Which will it handle badly?', f'''<div class="cols pair">
    {card('rules', 'The skill’s four rules', code(chr(10).join(textwrap.fill(r, 40, subsequent_indent='  ') for r in RULES), 'markdown'))}
    <div class="cases">
      {''.join(block(c, 'structure', t, '', words=True) for c, t in CASES)}
    </div>
  </div>''', [
    {"type": "focus", "target": "rules", "at": "3", "color": "blue"},
    {"type": "focus", "target": "c1", "at": "4~refactor", "color": "yellow"},
    {"type": "focus", "target": "c2", "at": "4~two changes", "color": "yellow"},
    {"type": "focus", "target": "c3", "at": "4~security fix", "color": "yellow"},
    {"type": "focus", "target": "c4", "at": "4~code terms", "color": "yellow"},
    {"type": "focus", "target": "c5", "at": "4~no unreleased", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}],
    css='.pair{align-items:center}.cases{display:flex;flex-direction:column;gap:14px}'
        '.cases .semantic-block{padding:16px 26px;min-height:0}.cases .title{font-size:34px}.cases .label{display:none}'
        '.card > .code.dark{font-size:32px;line-height:1.5}')


def wrap(line, width=64):
    """A changelog line as the patch has it, wrapped for the box; continuation lines are indented."""
    return textwrap.wrap(line, width, subsequent_indent='    ', break_long_words=False, break_on_hyphens=False)


def trial_scene(sid, stim, headline, marks, cues):
    """One stimulus: the request, what each model's patch added, and our note for each trial.

    marks = (phrase in haiku's lines, phrase in terra's lines): each becomes the highlight target
    'h' or 't', and that trial's note is the callout level with it."""
    body = []
    for key, m, phrase in zip('ht', MODELS, marks):
        out = [m]
        hit = 0
        for line in ADDED[stim, m]:
            # Keep the marked phrase on one row: its spaces are held together while the line is wrapped.
            for w in (x.replace('\x00', ' ') for x in wrap(line.replace(phrase, phrase.replace(' ', '\x00')))):
                if phrase in w and not hit:
                    w, hit = w.replace(phrase, f'⟦{key}:{phrase}⟧', 1), 1
                out.append('  ' + w)
        assert hit, (stim, m, phrase, ADDED[stim, m])
        body.append('\n'.join(out))
    n = NOTES[stim]
    src = 'stand-in: the course’s verified run' if PROVISIONAL else f'our run · {RUN}'
    framed(sid, EB3, headline, f'''{quote('req', f'{mono(stim)} · the request', '“' + esc(PROMPT[stim]) + '”')}
  <div class="annotated">
    {code((chr(10) * 2).join(body), 'markdown', 'added')}
    {callouts(('h', n[0]), ('t', n[1]))}
  </div>
  <p class="note">what each model’s patch added · {src}</p>''', cues,
           css='.stage{gap:18px;justify-content:safe center}.quote{width:100%;padding-top:10px;padding-bottom:12px}'
               '.quote p{font-size:30px;line-height:1.34}.quote .who .mono{font-family:var(--font-code)}'
               '.code.dark.added{font-size:28px;line-height:1.36;padding:16px 28px;min-width:1150px}.callout{font-size:32px}'
               '.note{margin:0}')


trial_scene('s14', 'refactor', 'A change users can’t see', ('### Changed', '### Changed'), [
    {"type": "focus", "target": "t", "at": "0", "color": "yellow"},
    {"type": "focus", "target": "h", "at": "1~each model", "color": "yellow"},
    {"type": "focus", "target": "t", "at": "1~records", "color": "yellow"}])
trial_scene('s15', 'typo-fix', 'A number nobody gave', (entries('typo-fix', H)[0][2:], TYPO_PR), [
    {"type": "focus", "target": "h", "at": "1~haiku", "color": "green"},
    {"type": "focus", "target": "t", "at": "2", "color": "yellow"}])
trial_scene('s16', 'two-changes', 'Two changes, handled well', ('### Fixed', '### Fixed'), [
    {"type": "focus", "target": "req", "at": "0~two changes", "color": "blue"},
    {"type": "focus", "target": "h", "at": "1~both models", "color": "green"},
    {"type": "focus", "target": "t", "at": "1~both cite", "color": "green"},
    {"type": "focus", "target": "none", "at": "2"}])
trial_scene('s17', 'security', 'A security fix, under Fixed', ('### Fixed', '### Fixed'), [
    {"type": "focus", "target": "h", "at": "0~both", "color": "yellow"},
    {"type": "focus", "target": "t", "at": "0~security fix", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "1"}])
trial_scene('s18', 'parser', 'How it was coded', (HOW, entries('parser', T)[0][2:30]), [
    {"type": "focus", "target": "h", "at": "0~streaming", "color": "yellow"},
    {"type": "focus", "target": "t", "at": "1", "color": "green"}])
trial_scene('s19', 'after-release', 'A heading without brackets', ('## [Unreleased]', '## Unreleased'), [
    {"type": "focus", "target": "req", "at": "0", "color": "blue"},
    {"type": "focus", "target": "h", "at": "2", "color": "green"},
    {"type": "focus", "target": "t", "at": "3", "color": "yellow"}])

framed('s20', EB3, 'Twelve notes, five failure modes', f'''{panel('notes')}''', [
    {"type": "focus", "target": "m1", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "m2", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "m3", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "m4", "at": "5", "color": "yellow"},
    {"type": "focus", "target": "m5", "at": "6", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "7"}], layout='layout-file')

# ---- Chapter: Where the failures come from -------------------------------------------------------
EB4 = 'Where the failures come from'
framed('s21', EB4, 'Every failure is a gap', f'''<div class="annotated">
    {panel('skill')}
    {callouts(('place', 'Which categories? What heading?'),
              ('users', 'Which changes? Ruling out what?'),
              ('reference', 'And with no number?'))}
  </div>''', [
    {"type": "scroll", "target": "#skill", "to": "10-13", "at": "1"},
    {"type": "focus", "target": "reference", "at": "2", "color": "yellow"},
    {"type": "focus", "target": "users", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "place", "at": "4", "color": "yellow"},
    {"type": "focus", "target": "none", "at": "5"}], layout='layout-file')

SETTLED = {'3': 'the format: a Security category', '5': 'the format: ## [Unreleased]'}
rows = ''.join(f'''<tr><td class="num">{n}</td><td><span data-concept="mode{n}" data-rep="cell">{esc(mode)}</span></td>
        <td class="mono">{trial}</td><td>{SETTLED.get(n, '')}</td></tr>\n''' for n, mode, trial in MODES)
framed('s22', EB4, 'Some of it is taste', f'''<table class="data-table full modes">
    <thead><tr><th></th><th>Failure mode</th><th>Seen in</th><th>Settled by</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>
  <p class="note">from the top of {mono('notes/failures.md')}</p>''', [
    {"type": "focus", "target": "mode3", "at": "2~security", "color": "blue"},
    {"type": "focus", "target": "mode5", "at": "2~heading", "color": "blue"}],
    css='.modes{font-size:32px;margin-top:30px}.modes th{font-size:28px}.modes td{padding-top:20px;padding-bottom:20px}'
        '.modes td.mono{font-family:var(--font-code);font-size:28px;white-space:nowrap}')

parts = ''.join(f'''<div class="part" data-concept="p{i}" data-rep="part">
      <div class="step">{i}</div><div class="title">{t}</div><div class="label">{l}</div></div>''' for i, (t, l) in enumerate([
    ('Run', 'realistic requests'),
    ('Read', 'what came back'),
    ('Note', 'what is wrong with each'),
    ('Group', 'the notes into failure modes')], 1))
framed('s23', 'Recap', 'What are the four steps?', f'''<div class="semantic-block" id="steps" data-role="structure">
    <div class="title words">error analysis</div>
    <div class="parts">{parts}</div>
  </div>''', [
    {"type": "expand", "target": "#steps", "at": "1"},
    {"type": "focus", "target": "p1", "at": "1", "color": "blue"},
    {"type": "focus", "target": "p2", "at": "2", "color": "cyan"},
    {"type": "focus", "target": "p3", "at": "3", "color": "yellow"},
    {"type": "focus", "target": "p4", "at": "4", "color": "orange"}], layout='layout-expand',
    css='#steps{width:100%;padding:36px 40px 44px;gap:24px}'
        '#steps .parts{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;width:100%}'
        '#steps .part{min-height:280px}#steps .part .title{font-size:52px;line-height:1.2}'
        '#steps .part .label{font-size:30px}')

scene('s24', 'Next', '''<main class="scene title-card">
  <div class="eyebrow">Next</div>
  <h1 class="scene-title chapter">Turn a failure into a grader</h1>
  <p class="lead">Can code do the reading?</p>
  <p class="note">Exercises are on the lesson page · Source: Husain and Shankar, AI Evals FAQ (2026)</p>
</main>''', [], css='.scene-title.chapter{font-size:104px}')
print('ok', 'PROVISIONAL run' if PROVISIONAL else RUN)
