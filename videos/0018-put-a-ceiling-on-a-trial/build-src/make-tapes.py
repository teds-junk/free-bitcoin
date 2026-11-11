"""Write the four tapes of lesson 18. Tapes are generated so their shared header and hidden setup stay
identical; edit here and re-run, BEFORE anything is recorded (a changed tape records again; s23 costs).
Run from anywhere:  python3 build-src/make-tapes.py
"""
import pathlib
D = pathlib.Path(__file__).resolve().parent.parent
V = str(D)
P = '/Users/Shared/demo/practice'
ref = (D.parent / '0003-the-same-request-five-times/tapes/s10.tape').read_text().splitlines()
SET = '\n'.join(l for l in ref if l.startswith('Set '))
WAIT = 'Wait /\\$\\s*$/'

COMMON = '''# Runs in /Users/Shared/demo/practice in place (the course's one practice folder; nothing is reset).
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (rewritten, nothing else) and appends what
# vally printed to /tmp/vl-l18/{sid}.log, which build-src/capture-run.py copies into src/run/.
# When input is redirected (vally grade < results.jsonl) the wrapper uses tee and not `script`, which
# would echo the input file; vally grade prints no colour and no path, so the screen is unchanged.'''


def hidden(sid, setup):
    wrap = ('VB=$(type -P vally); L=/tmp/vl-l18/%s.log; mkdir -p /tmp/vl-l18; : > $L; '
            'vally(){ if [ -t 0 ]; then script -q -a $L "$VB" "$@" | sed -l \'s|/Users/Shared/demo|~/src/demo|g\'; '
            'else "$VB" "$@" 2>&1 | tee -a $L; fi; }') % sid
    return f'''Hide
Type `export PS1='\\W $ ' PS2='' && {setup} && clear`
Enter
{WAIT}
Type `{wrap}`
Enter
{WAIT}
Type "clear"
Enter
{WAIT}
Show
Sleep 500ms
'''

CLEAR = f'''Hide
Type "clear"
Enter
{WAIT}
Show
Sleep 500ms
'''


def cmd(*lines, wait=WAIT, after='1s'):
    out = []
    for i, l in enumerate(lines):
        q = '`' if ('"' in l or '\\' in l) else '"'
        out += [f'Type {q}{l}{q}', 'Sleep 400ms', 'Enter']
    return '\n'.join(out + [wait, f'Sleep {after}']) + '\n'


GRADE = ('vally grade \\', '  -e ../../../../evals/changelog.eval.yaml \\', '  --run-dir . < results.jsonl')
install = lambda f: f'cp {V}/src/state/changelog.{f}.eval.yaml {P}/evals/changelog.eval.yaml'
L16 = f'{P}/results/lesson-16/2026*'

tapes = {}
tapes['s16'] = f'''# s16: lint the eval file with the first (tight) budgets, then re-grade the haiku-high variant of the
# lesson 16 run with them. No agent starts: this tape declares no cost.
{COMMON.format(sid='s16')}
# Hidden setup WRITES to the demo folder: it copies this video's src/state/changelog.tight.eval.yaml over
# evals/changelog.eval.yaml (the lesson page makes this edit in an editor: three budget graders under
# each of the five stimuli). Needs exactly one run folder under results/lesson-16 (Tab completes it).
# The re-grade prints about 60 lines, so the screen scrolls: the credential scan sees one screenful and
# the recording will need the stills review.
{SET}

{hidden('s16', f"cd {P} && {install('tight')}")}
{cmd('vally lint -e evals/changelog.eval.yaml')}
{CLEAR}
Type "cd results/lesson-16/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
{WAIT}
Sleep 1s

{cmd('cd haiku-high')}
{cmd(*GRADE, wait='Wait@60s /\\$\\s*$/', after='4s')}'''

tapes['s18'] = f'''# s18: the same re-grade, with the first (tight) budgets, on the terra-high variant. No agent starts.
{COMMON.format(sid='s18')}
# Hidden setup installs the tight eval file again (so this tape can be recorded alone) and starts in
# the haiku-high folder, where s16 left the terminal, so the page's `cd ../terra-high` is true.
{SET}

{hidden('s18', f"{install('tight')} && cd {L16}/haiku-high")}
{cmd('cd ../terra-high')}
{cmd(*GRADE, wait='Wait@60s /\\$\\s*$/', after='4s')}'''

tapes['s21'] = f'''# s21: the budgets are widened; re-grade terra-high, then haiku-high, then return to the practice folder.
# No agent starts: this tape declares no cost.
{COMMON.format(sid='s21')}
# Hidden setup WRITES to the demo folder: it copies this video's src/state/changelog.wide.eval.yaml over
# evals/changelog.eval.yaml (the lesson page makes this edit in an editor), and starts in the terra-high
# folder, where s18 left the terminal.
{SET}

{hidden('s21', f"{install('wide')} && cd {L16}/terra-high")}
{cmd(*GRADE, wait='Wait@60s /\\$\\s*$/', after='1s')}
{CLEAR}
{cmd('cd ../haiku-high')}
{cmd(*GRADE, wait='Wait@60s /\\$\\s*$/', after='1s')}
{CLEAR}
{cmd('cd ../../../..', after='4s')}'''

tapes['s23'] = f'''# s23: with the time limit added, lint, then run the five stimuli once on both models.
{COMMON.format(sid='s23')}
# Hidden setup WRITES to the demo folder: it copies this video's src/state/changelog.final.eval.yaml over
# evals/changelog.eval.yaml (wide budgets plus a constraints block under each stimulus; the practice
# folder then matches verified/lesson-18), and moves an existing results/lesson-18 aside to
# /Users/Shared/.demo-old.lesson-18.<time>, so a re-recording leaves one run. Nothing is deleted.
# The run takes about a minute and is cut.
# Spend: 10 agent runs
{SET}

{hidden('s23', f'cd {P} && {install("final")} && {{ [ -e results/lesson-18 ] && mv results/lesson-18 "/Users/Shared/.demo-old.lesson-18.$(date +%s)"; true; }}')}
{cmd('vally lint -e evals/changelog.eval.yaml')}
{CLEAR}
Type `vally eval -e evals/changelog.eval.yaml \\`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \\`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-18"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\\$\\s*$/
Show
Sleep 5s
'''
for k, v in tapes.items():
    (D / 'tapes' / f'{k}.tape').write_text(v)
print('tapes-ok', sorted(tapes))
