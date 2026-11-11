"""Write the three eval files the tapes install, from src/state/changelog.base.eval.yaml and budgets.json.

  changelog.tight.eval.yaml   base + three budget graders under each stimulus, at the tight values
  changelog.wide.eval.yaml    the same, at the wide values
  changelog.final.eval.yaml   wide + a constraints block (max_agent_duration) after each prompt

changelog.base.eval.yaml is the eval file as the practice folder has it before this lesson
(verified/lesson-17). If the series' own demo folder differs, copy its file over the base first.
Run from anywhere:  python3 build-src/make-state.py
"""
import json, pathlib, re

S = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'state'
B = json.loads((S / 'budgets.json').read_text())
base = (S / 'changelog.base.eval.yaml').read_text()
assert 'token-budget' not in base and 'constraints' not in base, 'the base file already has budgets or limits'


def budgets(v):
    return ('      - type: token-budget\n        config:\n          max: %d\n'
            '      - type: turn-count\n        config:\n          max: %d\n'
            '      - type: wall-time\n        config:\n          max: %s\n') % (v['tokens'], v['turns'], v['wall'])


def build(values, limit=None):
    head, *stims = re.split(r'(?m)^(?=  - name: )', base)
    assert len(stims) == 5, len(stims)
    out = [head]
    for s in stims:
        body = s.rstrip('\n')
        assert '    graders:\n' in body and body.splitlines()[-1].startswith('      '), body[-80:]
        if limit:
            lines = body.split('\n')
            p = next(i for i, l in enumerate(lines) if l.startswith('    prompt:'))
            e = next(i for i in range(p + 1, len(lines)) if not lines[i].startswith('      '))
            lines[e:e] = ['    constraints:', f'      max_agent_duration: {limit}']
            body = '\n'.join(lines)
        out.append(body + '\n' + budgets(values) + ('\n' if s.endswith('\n\n') else ''))
    return ''.join(out)


(S / 'changelog.tight.eval.yaml').write_text(build(B['tight']))
(S / 'changelog.wide.eval.yaml').write_text(build(B['wide']))
(S / 'changelog.final.eval.yaml').write_text(build(B['wide'], B['agent_limit']))
print('state-ok')
