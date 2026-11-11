"""Build the files this video's tapes install into the practice folder, in src/state/.

  python3 build-src/make-state.py [--from <evals/changelog.eval.yaml as the demo folder has it before this lesson>]

Default --from is verified/lesson-20's file. Reads only; writes only src/state/.

  src/state/changelog.eval.yaml          the eval file with `tags: { tier: quick }` under each of the five
                                         stimulus names (the lesson's step 1)
  src/state/changelog.lowered.eval.yaml  the same, with typo-fix's token-budget max lowered for a moment
                                         (step 7). The two numbers come from src/run/budget.json, so a
                                         series whose lesson 18 chose another budget changes one file.
  src/state/.vally.yaml, CONVENTIONS.md  copied from verified/lesson-21/practice (steps 2 and 10)

When --from is the default, the tagged file must equal verified/lesson-21's byte for byte.
"""
import json, pathlib, re, shutil, sys

D = pathlib.Path(__file__).resolve().parent.parent
COURSE = D.parent.parent
V20 = COURSE / 'verified/lesson-20/practice'
V21 = COURSE / 'verified/lesson-21/practice'
STIMULI = ('typo-fix', 'refactor', 'security', 'two-changes', 'after-release')
TAG = '    tags: { tier: quick }'

src = V20 / 'evals/changelog.eval.yaml'
if '--from' in sys.argv:
    src = pathlib.Path(sys.argv[sys.argv.index('--from') + 1])
budget = json.loads((D / 'src/run/budget.json').read_text())
MAX, LOWERED = budget['max'], budget['lowered']

out, seen = [], []
for line in src.read_text().splitlines():
    if line.strip() == TAG.strip():
        continue                                   # already tagged: do not tag twice
    out.append(line)
    m = re.fullmatch(r'  - name: (\S+)', line)
    if m and m.group(1) in STIMULI:
        out.append(TAG)
        seen.append(m.group(1))
assert tuple(seen) == STIMULI, f'expected the five quick stimuli in order, found {seen}'
tagged = '\n'.join(out) + '\n'

state = D / 'src/state'
state.mkdir(parents=True, exist_ok=True)
(state / 'changelog.eval.yaml').write_text(tagged)
if src == V20 / 'evals/changelog.eval.yaml':
    assert tagged == (V21 / 'evals/changelog.eval.yaml').read_text(), 'tagged file differs from verified/lesson-21'

# The lowered variant: the first token-budget max after "- name: typo-fix", and only that one.
lines = tagged.splitlines()
i = lines.index('  - name: typo-fix')
j = next(k for k in range(i, len(lines)) if lines[k].strip() == '- type: token-budget')
k = next(k for k in range(j, j + 4) if lines[k].strip().startswith('max:'))
assert lines[k].strip() == f'max: {MAX}', (lines[k], MAX)
lines[k] = lines[k].replace(str(MAX), str(LOWERED))
(state / 'changelog.lowered.eval.yaml').write_text('\n'.join(lines) + '\n')
assert tagged.count(f'max: {MAX}') == 5, 'expected one token budget per quick stimulus'

for name in ('.vally.yaml', 'CONVENTIONS.md'):
    shutil.copyfile(V21 / name, state / name)
print(f'state ok: tagged from {src}; token budget {MAX}, lowered to {LOWERED} on line {k + 1}')
