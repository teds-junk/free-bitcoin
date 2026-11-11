"""Fill src/state and a PROVISIONAL src/run from the course's verified lesson 12 run.

src/state/ is real and final: the eval file before and after the judge, copied from verified/.
src/run/ made here is a stand-in so the scenes preview before this video's own run exists.
The verified folder keeps the console output but not the results folder, so the twelve patches
are rebuilt from the one printed patch (output/04-cat.txt) and the entries in
practice/notes/wording-labels.md. After the real run, build-src/collect-run.sh replaces all of it.

Run:  python3 build-src/provisional.py
"""
import pathlib, re, shutil

D = pathlib.Path(__file__).resolve().parent.parent
V = D.parent.parent / 'verified'
state, run = D / 'src/state', D / 'src/run'
state.mkdir(parents=True, exist_ok=True)
run.mkdir(parents=True, exist_ok=True)

shutil.copy(V / 'lesson-11/practice/evals/wording.eval.yaml', state / '00-start.wording.eval.yaml')
shutil.copy(V / 'lesson-12/practice/evals/wording.eval.yaml', state / '04-judge.wording.eval.yaml')

# The skill as the practice folder has it when lesson 12 starts (lesson 12 does not edit it).
shutil.copy(V / 'lesson-11/practice/skills/changelog-entry/SKILL.md', D / 'src/skill.md')

out = V / 'lesson-12/output'
shutil.copy(out / '01-eval.txt', run / 's12.log')
shutil.copy(out / '06-grade.txt', run / 's19.log')
shutil.copy(out / '05-lint.txt', run / 's18.log')
(run / 'RUN').write_text(out.joinpath('02-ls.txt').read_text().strip() + '\n')

template = (out / '04-cat.txt').read_text()
old = next(l for l in template.splitlines() if l.startswith('+- '))
PR = {'parser': 49, 'cache': 66, 'dates': 67}
MODEL = {'haiku': 'claude-haiku-4.5', 'terra': 'gpt-5.6-terra'}
NOTE = {('parser', 'haiku'): 'names the streaming parser',
        ('parser', 'terra'): 'only what users notice',
        ('cache', 'haiku'): 'names the kind of cache',
        ('cache', 'terra'): 'the benefit, then a hint of the method',
        ('dates', 'haiku'): 'only what users notice',
        ('dates', 'terra'): 'only what users notice'}
rows = ['# stimulus\tmodel\ttrial\tours\tnote']
for line in (V / 'lesson-12/practice/notes/wording-labels.md').read_text().splitlines():
    m = re.match(r'\| (\w+), (\w+), (\d) \| (.+?) \| (yes|no) \| (yes|no) \|', line)
    if not m:
        continue
    stim, who, trial, entry, ours, _ = m.groups()
    patch = template.replace(old, f'+- {entry} (#{PR[stim]})')
    if stim == 'cache':
        patch = patch.replace('+### Fixed', '+### Changed')
    (run / f'{stim}-{MODEL[who]}-{trial}.patch').write_text(patch)
    rows.append('\t'.join([stim, MODEL[who], trial, ours, NOTE[stim, who]]))
assert len(rows) == 13, rows
(run / 'labels.tsv').write_text('\n'.join(rows) + '\n')

(run / 'PROVISIONAL').write_text('''Everything in src/run/ is a STAND-IN from verified/lesson-12 (the course's run of 2026-11-10), not this video's run.

  RUN              the verified run's folder name
  s12.log          vally eval's output (verified/lesson-12/output/01-eval.txt)
  s18.log          vally lint's output (output/05-lint.txt)
  s19.log          vally grade --verbose output, the judge's twelve verdicts and reasons (output/06-grade.txt)
  *.patch          REBUILT, not saved files: the verified folder has no results. Each is output/04-cat.txt with the
                   entry line swapped for the entry in practice/notes/wording-labels.md plus its pull request number.
                   The heading line for the cache patches is a guess.
  labels.tsv       our own yes/no for each of the twelve entries (the "Ours" column of the verified labels file),
                   with a few words of why for the on-screen note. The orchestrator writes this for the real run.
  results.jsonl    absent. The generator then assumes vally grade printed its blocks in the order
                   model, stimulus (alphabetical), trial. With the real file it uses the file's own order.

After the real recordings: bash build-src/collect-run.sh, write labels.tsv, delete this file, then
python3 build-src/make-scenes.py && bash build-src/panels.sh. The generator fails where the run disagrees with the narration.
''')
print('provisional ok')
