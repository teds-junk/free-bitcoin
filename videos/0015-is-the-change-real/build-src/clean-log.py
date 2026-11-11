"""Reduce the terminal output that tapes/s14.tape tees to /tmp/vl-l15/s14.log to what Vally printed.

In a terminal `vally experiment run` redraws a live dashboard many times a second, so the raw log is
megabytes of repeats. This keeps, verbatim and in order:
  - the first lines (Running experiment …, Loaded …),
  - every block: a "<variant> · <model>" line and the lines under it up to the next blank line,
  - the final report: from the last line that is exactly "Experiment" (or begins "Experiment  ") to the end.
Terminal control codes and carriage-return redraws are removed; nothing else is changed.

  python3 build-src/clean-log.py /tmp/vl-l15/s14.log src/run/s14.log
"""
import re, sys

raw = open(sys.argv[1], errors='replace').read()
raw = re.sub(r'\x1b\[[0-9;?]*[ -/]*[@-~]', '', raw)
raw = re.sub(r'\x1b[()][A-Z0-9]', '', raw)
raw = re.sub(r'\^D\x08\x08', '', raw).replace('\x08', '').replace('\x04', '')
lines = [l.split('\r')[-1].rstrip() if l.rstrip('\r').split('\r')[-1].strip() else '' for l in raw.split('\n')]
lines = [l.rstrip('\r').split('\r')[-1].rstrip() for l in raw.split('\n')]

head = [l for l in lines[:6] if l.startswith(('Running experiment', 'Loaded '))]
blocks, i = [], 0
while i < len(lines) - 1:
    if re.fullmatch(r'\S+ · \S+', lines[i]) and re.match(r'\s+(PASS|FAIL|FLAKY|ERROR)\s', lines[i + 1]):
        j = i
        while j < len(lines) and lines[j].strip():
            j += 1
        blocks.append(lines[i:j])
        i = j
    else:
        i += 1
starts = [k for k, l in enumerate(lines) if l == 'Experiment' or l.startswith('Experiment  ')]
assert starts, 'no final report in the log'
tail = lines[starts[-1]:]
while tail and not tail[-1].strip():
    tail.pop()
# the dashboard leaves blank lines between rows of the final report: drop runs of blank lines
final = [l for k, l in enumerate(tail) if l.strip() or (k and tail[k - 1].strip())]

seen, uniq = set(), []
for b in blocks:
    key = '\n'.join(b)
    if key not in seen:
        seen.add(key)
        uniq.append(b)
out = head + [''] + [l for b in uniq for l in b + ['']] + ['─' * 56, ''] + final
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
print(f'{len(lines)} raw lines -> {len(out)} lines, {len(uniq)} blocks')
