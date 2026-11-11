#!/usr/bin/env python3
"""Builds the storyboards and scenes for the combined course video's joins:
videos/bridges (25 bridges), videos/00-intro and videos/99-outro.

The wording follows COURSE-PLAN.md: the Story for the intro and outro, and each
lesson's Hand-off for the bridge after it. Bridges state only what the lesson
videos themselves showed. Run from anywhere: python3 make-all.py
"""
import html, json, os

VIDEOS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = "Vally & Agent Evals"

# (lesson folder the bridge plays after, headline of six words or fewer, the two spoken sentences)
BRIDGES = [
    ("0001-it-works-for-me", "What did the tick check?",
     ["Both models got a green tick, yet they did different things.",
      "So what did that tick actually check?"]),
    ("0002-what-the-tick-checked", "Would it happen again?",
     ["We can now read everything a run left behind.",
      "But each model ran only once: would it do the same thing next time?"]),
    ("0003-the-same-request-five-times", "What else goes wrong?",
     ["So far we've counted one problem, on one tidy request, by reading ten patches.",
      "What else goes wrong when the requests get messier?"]),
    ("0004-read-the-runs-first", "Can code do the reading?",
     ["We found those failures by reading.",
      "After every edit to the skill, we'd have to read them all again, so can code do the reading?"]),
    ("0005-turn-a-failure-into-a-grader", "Where can a script live?",
     ["Patterns now catch the failures we named.",
      "But checking that nothing else in the file changed is not a pattern: it needs a script, kept where the agent can't read or edit it."]),
    ("0006-keep-graders-out-of-reach", "How do we test a grader?",
     ["A hidden script now decides pass and fail, and only we can see whether it's right.",
      "So how do we test a grader?"]),
    ("0007-test-a-grader", "Graders against real answers",
     ["That test tried one correct answer for each grader, and it couldn't test the graders that check for absence.",
      "But we have dozens of real answers saved, good and bad: can the graders run on those?"]),
    ("0008-check-graders-against-saved-trials", "Does the skill load?",
     ["Our graders are now tested against correct answers, untouched files, and real bad answers.",
      "In every trial so far the skill was there to use: will it load for other wordings, and stay out of requests that aren't its job?"]),
    ("0009-does-the-skill-load", "Better with the skill?",
     ["We know when the skill loads.",
      "But is the result any better with the skill than with no skill at all?"]),
    ("0010-is-the-agent-better-with-the-skill", "What about a follow-up?",
     ["Every stimulus so far has been a single request.",
      "Real use goes on: someone asks for a follow-up."]),
    ("0011-follow-up-requests", "What code can't check",
     ["Everything we've graded so far is structure that code can see.",
      "Whether an entry is written for the people who use the tool is not a pattern, so it needs another kind of grader."]),
    ("0012-a-judge-for-what-code-cannot-check", "Is the judge right?",
     ["The judge said yes for some trials and no for others.",
      "It's a model too, so is it right?"]),
    ("0013-check-the-judge", "Can a grader give partial credit?",
     ["We've measured the judge against our own labels.",
      "But some entries it refused were nearly right and some were far off, and a yes or no can't tell them apart: can a grader give partial credit without hiding a failure?"]),
    ("0014-partial-credit", "Is the change real?",
     ["Scores and counts both move after an edit.",
      "If seven of ten becomes nine of ten, is that real?"]),
    ("0015-is-the-change-real", "What does a pass cost?",
     ["We can now say what a before-and-after result supports.",
      "That same table also printed tokens for each variant, and they differ by model: so what does a passing trial cost?"]),
    ("0016-what-a-passing-trial-costs", "A model of your own",
     ["We can price the models a Copilot account offers.",
      "An app may call a model through a service of its own, or one the team runs: can Vally run that model too, and what does a passing trial cost there?"]),
    ("0017-a-model-from-your-own-provider", "A ceiling on a trial",
     ["We can now price any model, including one we run ourselves, where a single trial took minutes.",
      "One trial that loops can cost or take many times the typical one, so how do we fail, or stop, a trial that takes too much?"]),
    ("0018-put-a-ceiling-on-a-trial", "No worse than before?",
     ["Budgets now guard every trial.",
      "Before relying on an edit, we want a check that says no worse than before: can Vally decide that?"]),
    ("0019-is-it-worse-than-before", "Where do we look first?",
     ["There are many moving parts now, and runs sometimes end in error, or fail for reasons that aren't the skill.",
      "When a run goes wrong, where do we look first?"]),
    ("0020-when-a-run-goes-wrong", "Make it a routine",
     ["We can measure, gate and debug.",
      "What's left is to make it a routine that a teammate can repeat."]),
    ("0021-keep-it-working", "The skill inside an app",
     ["That completes the checks on the skill by itself.",
      "Now a team has put the skill inside their release tooling: does it still hold when an app, not a person, starts the agent?"]),
    ("0022-start-the-agent-where-the-app-would", "How did it get there?",
     ["The hidden test sees only the finished changelog.",
      "In an app, how the agent got there matters too: did it read the list, and did it try to commit or push?"]),
    ("0023-check-what-the-agent-did", "When a tool fails",
     ["In real use, the tracker or the network sometimes fails.",
      "Does the agent cope, and can we test that without breaking anything?"]),
    ("0024-when-a-tool-fails", "A run Vally didn't start",
     ["All of this ran inside Vally.",
      "The app also runs by itself, and keeps its own record of what it did: can Vally grade a run it didn't start?"]),
    ("0025-grade-a-run-vally-did-not-start", "Let Vally run the app",
     ["Grading afterwards gives one sample for each run, on whatever model the app used.",
      "To get trials, experiments and other models, Vally has to start the app itself."]),
]

PAGE = """<!doctype html>
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
[]
</script>
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=False).replace("'", "’")


def card(eyebrow, headline, lead):
    return ('<main class="scene title-card">\n'
            + (f'  <div class="eyebrow">{esc(eyebrow)}</div>\n' if eyebrow else '')
            + f'  <h1 class="scene-title chapter">{esc(headline)}</h1>\n'
            + (f'  <p class="lead">{esc(lead)}</p>\n' if lead else '') + '</main>')


def blocks(eyebrow, headline, rows, note=None):
    out = [f'<main class="scene ">', f'  <div class="eyebrow">{esc(eyebrow)}</div>',
           f'  <h2 class="scene-title">{esc(headline)}</h2>', '  <div class="stage">']
    for row in rows:
        out.append('  <div class="cols terms">')
        for title, label in row:
            out.append('    <div class="semantic-block" data-role="structure">'
                       f'<div class="title words">{esc(title)}</div>'
                       + (f'<div class="label">{esc(label)}</div>' if label else '') + '</div>')
        out.append('  </div>')
    if note:
        out.append(f'  <p class="note">{esc(note)}</p>')
    out += ['  </div>', '</main>']
    return '\n'.join(out)


BLOCK_CSS = ('.stage{gap:28px}.terms .semantic-block{min-height:170px}'
             '.terms .title{font-size:36px}.terms .label{font-size:28px}')


def write(folder, name, title, body, css=''):
    path = os.path.join(VIDEOS, folder, 'scenes', name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(PAGE.format(title=esc(title), css=css, body=body))


def storyboard(folder, title, kind, narrative, scenes, poster=None):
    path = os.path.join(VIDEOS, folder, 'storyboard.json')
    sb = json.load(open(path))
    sb.update({'title': title, 'slug': folder, 'kind': kind, 'narrative': narrative, 'scenes': scenes})
    if poster:
        sb['poster'] = poster
    with open(path, 'w') as f:
        json.dump(sb, f, indent=2, ensure_ascii=False)
        f.write('\n')


# ---- bridges --------------------------------------------------------------
scenes = []
for n, (after, headline, say) in enumerate(BRIDGES, 1):
    sid = f's{n:02d}'
    write('bridges', f'{sid}.html', headline, card('', headline, None))
    scenes.append({
        'id': sid, 'role': 'bridge', 'after': after, 'stage': 'skill' if n <= 20 else 'app',
        'renderer': 'slide', 'visual': f'scenes/{sid}.html',
        'on_screen': f"'{headline}' in the display serif, alone on the page.",
        'introduces': [], 'narration': say,
    })
storyboard('bridges', 'Bridges', 'bridges', {
    'question': 'What does the viewer have after each part, and why does the next one follow?',
    'viewer_starts': 'Has just watched one part of the course.',
    'arc': [{'stage': 'skill', 'viewer_can': 'say what they can now do with the skill and what question leads on'},
            {'stage': 'app', 'viewer_can': 'carry the same questions over to the skill inside an app'}],
}, scenes)

# ---- intro ----------------------------------------------------------------
write('00-intro', 's01.html', COURSE,
      card('A course in seven parts', COURSE, 'It works when you try it. Does it work?'))
write('00-intro', 's02.html', 'One skill, measured',
      blocks(COURSE, 'One skill, measured', [
          [('Measure the skill', ''), ('Graders you can trust', ''),
           ('Is it earning its place', ''), ('Judgement and evidence', '')],
          [('Worth what it costs', ''), ('Make it routine', ''), ('The skill inside an app', '')],
      ]), BLOCK_CSS)
write('00-intro', 's03.html', 'Say it with evidence',
      card(COURSE, 'Say it with evidence', 'Did the change make it better, and what does it cost?'))
storyboard('00-intro', COURSE, 'intro', {
    'question': 'You wrote a skill and it works when you try it. Does it work?',
    'viewer_starts': 'Has written or used a skill for a coding agent, and has not evaluated one.',
    'arc': [{'stage': 'promise', 'viewer_can': 'say what problem the course starts from and who it is for'},
            {'stage': 'journey', 'viewer_can': 'name the seven parts and where they lead'}],
}, [
    {'id': 's01', 'role': 'hook', 'mode': 'think', 'stage': 'promise', 'chapter': 'Introduction',
     'renderer': 'slide', 'visual': 'scenes/s01.html',
     'on_screen': "The course name in the display serif, under the eyebrow 'A course in seven parts'. Below: 'It works when you try it. Does it work?'",
     'introduces': [],
     'narration': [
         "You wrote a skill for a coding agent, and it works when you try it.",
         "But you can't tell whether it works on another model, on the fifth run, or after your next edit, or what each run costs.",
         "This course is for anyone who writes skills, or builds an agent into an app, and wants evidence in place of a hunch.",
     ]},
    {'id': 's02', 'role': 'body', 'mode': 'think', 'stage': 'journey',
     'renderer': 'slide', 'visual': 'scenes/s02.html',
     'on_screen': "Headline 'One skill, measured'. Seven blocks in two rows, one named for each part of the course.",
     'introduces': [],
     'narration': [
         "We take one short skill, which writes changelog entries, and measure it with Vally.",
         "First we measure the skill, and read what the agent really did.",
         "Then we build graders we can trust, and ask whether the skill earns its place.",
         "We add a judge for what code can't check, and learn what a result does and doesn't support.",
         "We work out what a passing trial costs, and turn the checks into a routine.",
         "Finally, we evaluate the same skill inside an app.",
     ]},
    {'id': 's03', 'role': 'body', 'mode': 'think', 'stage': 'journey',
     'renderer': 'slide', 'visual': 'scenes/s03.html',
     'on_screen': "'Say it with evidence' in the display serif. Below: 'Did the change make it better, and what does it cost?'",
     'introduces': [],
     'narration': [
         "By the end, you can change the skill, or the model under it, and say with evidence whether it got better, and what it costs.",
         "Let's begin.",
     ]},
], poster='s01')

# ---- outro ----------------------------------------------------------------
write('99-outro', 's01.html', 'What you can now do',
      blocks(COURSE, 'What you can now do', [
          [('Say what changed', 'better or not, and at what cost'),
           ('Trust the checks', 'tested graders, a checked judge, ranges'),
           ('Repeat it', 'a routine a teammate can run')],
          [('Evaluate the app', 'when an app, not a person, starts the agent')],
      ]), BLOCK_CSS)
write('99-outro', 's02.html', 'The workflow guide',
      card('Where to go next', 'The workflow guide',
           'On the course site: the whole procedure, for a skill or for a feature in an app.'))
storyboard('99-outro', 'What you can now do', 'outro', {
    'question': 'What can the viewer do now, and where do they go next?',
    'viewer_starts': 'Has watched the whole course.',
    'arc': [{'stage': 'can-do', 'viewer_can': 'say what they can now do with a skill and with an app'},
            {'stage': 'next', 'viewer_can': 'find the exercises and the workflow guide'}],
}, [
    {'id': 's01', 'role': 'hook', 'mode': 'think', 'stage': 'can-do', 'chapter': 'What you can now do',
     'renderer': 'slide', 'visual': 'scenes/s01.html',
     'on_screen': "Headline 'What you can now do'. Four blocks: say what changed, trust the checks, repeat it, evaluate the app.",
     'introduces': [],
     'narration': [
         "That's the whole course.",
         "You can now edit a skill, or change the model under it, and say with evidence whether it got better, and what it costs.",
         "Your graders are tested, your judge is checked against your own labels, and your results come with ranges.",
         "Those checks run as a routine that a teammate can repeat.",
         "And you can evaluate the same skill when an app, not a person, starts the agent.",
     ]},
    {'id': 's02', 'role': 'body', 'mode': 'think', 'stage': 'next',
     'renderer': 'slide', 'visual': 'scenes/s02.html',
     'on_screen': "'The workflow guide' in the display serif under the eyebrow 'Where to go next'. Below: 'On the course site: the whole procedure, for a skill or for a feature in an app.'",
     'introduces': [],
     'narration': [
         "On the course site, you'll find the exercises for every part.",
         "There's also a workflow guide, which walks the whole procedure, for a skill or for a feature in an app.",
     ]},
], poster='s01')

print(f'bridges: {len(BRIDGES)} scenes; intro: 3; outro: 2')
