"""Copy what this video quotes out of its two recorded runs into src/run/. Reads the run folders, writes
only inside this video's folder. Run after s16 and s19 are recorded:

  python3 build-src/extract-run.py <practice>/results/lesson-9-before/<run> <practice>/results/lesson-9-after/<run>

Writes src/run/counts.json, src/run/before/eval-results.md and src/run/after/eval-results.md (with
/Users/Shared/demo shown as ~/src/demo), and, if a trial that should have loaded the skill did not,
that trial's patch as src/run/before/miss.patch (or after/miss.patch) with miss.json beside it.
Then copy the console logs and delete src/run/PROVISIONAL (see that file).
"""
import json, pathlib, sys

D = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else D / 'src/run'   # a third argument is for testing
OURS, THREE = 'changelog-entry', ('changelog-entry', 'commit-message', 'release-notes')
counts = {'_about': 'Per stimulus and model: trials that passed, failed a grader, or ended in ERROR, and which '
                    'of the three installed skills loaded in how many trials. Written by build-src/extract-run.py '
                    'from each run\'s results.jsonl.'}
for label, arg in (('before', sys.argv[1]), ('after', sys.argv[2])):
    run = pathlib.Path(arg)
    models = {}
    (OUT / label).mkdir(parents=True, exist_ok=True)
    for line in (run / 'results.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        if t.get('type') != 'trial-result':
            continue
        c = models.setdefault(t['model'], {}).setdefault(
            t['stimulus'], {'passed': 0, 'failed': 0, 'errors': 0, 'skills': {}})
        grade = t.get('gradeResult')
        if t.get('status') != 'success' or not grade:
            c['errors'] += 1
            continue
        c['passed' if grade['passed'] else 'failed'] += 1
        loaded = {e['data']['name'] for e in t['trajectory']['events'] if e['type'] == 'skill_activation'}
        for s in THREE:
            if s in loaded:
                c['skills'][s] = c['skills'].get(s, 0) + 1
        if t['stimulus'].startswith('load-') and OURS not in loaded:
            patch = run / t['evalName'] / t['stimulus'] / t['model'] / str(t['trialIndex']) / 'workspace.patch'
            (OUT / label / 'miss.patch').write_text(patch.read_text() if patch.exists() else '')
            (OUT / label / 'miss.json').write_text(json.dumps(
                {'model': t['model'], 'stimulus': t['stimulus'], 'trial': t['trialIndex'],
                 'output': t['trajectory'].get('output')}, indent=1))
    counts[label] = {'run': run.name, 'models': models}
    report = run / 'eval-results.md'
    if report.exists():
        (OUT / label / 'eval-results.md').write_text(
            report.read_text().replace('/private/Users/Shared/demo', '~/src/demo').replace('/Users/Shared/demo', '~/src/demo'))
(OUT / 'counts.json').write_text(json.dumps(counts, indent=1))
print(json.dumps({k: v['run'] for k, v in counts.items() if k != '_about'}), 'written to', OUT)
