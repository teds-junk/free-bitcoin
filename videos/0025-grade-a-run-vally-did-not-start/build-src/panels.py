"""Insert the file panels (make-scenes.py clears them). Run from anywhere, after make-scenes.py.

src/app/* are the app's real files; src/run/* are this video's own run (or the stand-ins listed in
src/run/PROVISIONAL). Line numbers that depend on the run come from build-src/lines.json, which
make-scenes.py writes, so a different run cannot silently shift what a panel shows.
"""
import json, pathlib, subprocess
D = pathlib.Path(__file__).resolve().parent.parent
FP = pathlib.Path.home() / 'src/me/skills/skills/video-lesson/scripts/file-panel.js'
L = json.loads((D / 'build-src/lines.json').read_text())
T, DF = L['traj'], L['diff']


def fp(file, into, pid, label, width, show=None, marks=(), expects=(), rows=9, extra=()):
    cmd = ['node', str(FP), '--file', file, '--label', label, '--id', pid, '--width', str(width), '--rows', str(rows)]
    if show:
        cmd += ['--show', show]
    for m in marks:
        cmd += ['--mark', m]
    for e in expects:
        cmd += ['--expect', e]
    cmd += list(extra) + ['--into', f'scenes/{into}.html']
    r = subprocess.run(cmd, cwd=D, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'{into}: {r.stderr.strip()}')


fp('src/run/trajectory.json', 's04', 'traj', 'app-run/trajectory.json', 46, show=f"1-{T['end']}",
   marks=[f"{T['ver']}=ver", f"{T['step']}=step", f"{T['fn']}-{T['args_end']}=fn", f"{T['obs']}=obs",
          f"{T['met'] + 1}-{T['end'] - 1}=met"],
   expects=[f"{T['ver']}=ATIF-", f"{T['step']}=\"step_id\": 1"])
fp('src/app/run.mjs', 's09', 'runmjs', 'app/run.mjs', 46,
   marks=['4=imp', '12-14=tel', '15=cap'], expects=['4=release-assistant.mjs', '12=telemetry', '15=captureContent'])
fp('src/run/span-chat.json', 's10', 'chat', 'traces.jsonl · one line, laid out', 46, show='1-14',
   marks=['3=trace', '5=parent', '8=op', '11-12=tok', '13=aiu'],
   expects=['3="traceId"', '5="parentSpanId"', '8="gen_ai.operation.name": "chat"', '11=input_tokens',
            '12=output_tokens', '13=nano_aiu'])
fp('src/run/span-tool.json', 's11', 'tool', 'traces.jsonl · another line, laid out', 46, show='6-12',
   marks=['8-9=tool', '10=cid', '11-12=cc'],
   expects=['8="gen_ai.operation.name": "execute_tool"', '9=gen_ai.tool.name', '10=gen_ai.tool.call.id',
            '11=release/merged.txt', '12=gen_ai.tool.call.result'])
fp('src/app/traces-to-atif.mjs', 's12', 'conv', 'app/traces-to-atif.mjs', 48, show='32-66',
   marks=['35=chat', '45-48=met', '53-54=tool', '60=args'],
   expects=['35==== "chat"', '45=prompt_tokens', '53=execute_tool', '60=argumentsOf'])
fp('src/app/run.sh', 's14', 'runsh', 'app/run.sh', 48, show='15-33',
   marks=['16-18=co', '22=setup', '24=keep', '27-28=app', '32=diff'],
   expects=['16=CHANGELOG.md', '22=list-merged.mjs > release/merged.txt', '24=app-run/before', '27=node app/run.mjs',
            '32=diff -ruN before repo'])
fp('src/run/change.diff', 's18', 'diff', 'app-run/change.diff', 48,
   marks=['1=file', f"{DF['e74']}=e74", f"{DF['e75']}=e75", f"{DF['e76']}=e76"],
   expects=['1=CHANGELOG.md', f"{DF['e74']}=(#74)", f"{DF['e75']}=(#75)", f"{DF['e76']}=(#76)"])
print('panels-ok')
