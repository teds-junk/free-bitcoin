#!/bin/bash
# Regenerate the file panels (make-scenes.py clears them). Run from the video directory.
# Every file is one the tapes install into the practice folder, or the file it replaces:
#   src/state/vally-executor.stub.mjs   the plugin as the starter ships it (verified/lesson-25)
#   src/state/vally-executor.mjs        the plugin with execute written (verified/lesson-26)
#   src/state/vally.yaml                .vally.yaml with the three plugins lines (verified/lesson-26)
#   src/state/release-assistant.mjs     the app's own function (unchanged since lesson 25)
#   src/state/release-app.experiment.yaml   the new experiment file (verified/lesson-26)
set -e
fp(){ node "$HOME/src/me/skills/skills/video-lesson/scripts/file-panel.js" "$@" >/dev/null; }
# s05: the end of the shipped file. Lines 67-68 are the starter's comment telling the reader what to do.
fp --file src/state/vally-executor.stub.mjs --label 'app/vally-executor.mjs · as shipped' --id stub \
   --width 46 --rows 9 --show 65-66,69-77 \
   --expect '66=name: "release-app"' --expect '70=execute is not written yet' --expect '75=registerExecutors' \
   --mark '66=name:"release-app"' --mark '69=exec:execute(stimulus, options)' --mark '72=shut:shutdown()' \
   --mark 75-76=reg --into scenes/s05.html
# s06 and s07: one panel on the written execute function; s07 opens where s06 ends.
EXEC=(--file src/state/vally-executor.mjs --label 'app/vally-executor.mjs' --width 46 --rows 9 --show 67-101
      --expect '69=writeEntries' --expect '88=computeMetrics' --expect '98=executor: "release-app"')
fp "${EXEC[@]}" --id exec \
   --mark '67=sig:execute(stimulus, options)' --mark '69=we:writeEntries' --mark '70=wd:options.workDir' \
   --mark '71=model:options.model' --mark 72-73=sk --mark '74=req:stimulus.prompt' \
   --mark '75=to:options.timeout' --mark '76=tel:telemetryFor(options)' \
   --mark '77=tc:options.traceContext' --into scenes/s06.html
fp "${EXEC[@]}" --id exec2 \
   --mark '80=tte:toTrajectoryEvents(events)' --mark 84-86=ret --mark '88=cm:computeMetrics(trajectoryEvents)' \
   --mark '89=wall:wallTimeMs' --mark 92=meta --mark 93-95=meta --mark 98=meta --into scenes/s07.html
# s08: three branches of the renaming helper.
fp --file src/state/vally-executor.mjs --label 'app/vally-executor.mjs' --id events --width 62 --rows 9 \
   --show 23-28,37-50 --expect '23=tool.execution_start' --expect '37=skill.invoked' --expect '40=assistant.usage' \
   --mark '25=tool:"tool_call"' --mark '38=skill:"skill_activation"' --mark '42=usage:"token_usage"' \
   --mark 48-50=cost --into scenes/s08.html
# s09: the three new lines at the top of .vally.yaml.
fp --file src/state/vally.yaml --label '.vally.yaml' --id vy --width 46 --rows 7 --show 1-5 \
   --expect '1=plugins:' --expect '3=./app/vally-executor.mjs' --expect '4=suites:' \
   --mark 1-3=plug --mark '4=suites:suites:' --into scenes/s09.html
# s14: where the app creates its client.
fp --file src/state/release-assistant.mjs --label 'app/release-assistant.mjs' --id ra --width 62 --rows 9 \
   --show 13-19 --expect '13=writeEntries' --expect '18=onGetTraceContext' \
   --mark '18=fn:onGetTraceContext' --mark 17=tc --mark '18=tc:() => options.traceContext ?? {},' \
   --into scenes/s14.html
# s19: the experiment file, whole.
fp --file src/state/release-app.experiment.yaml --label 'evals/release-app.experiment.yaml' --id exp \
   --width 44 --rows 9 --expect '6=vary:' --expect '11=executor: release-app' --expect '12=runs: 3' \
   --mark '4=ev:release.eval.yaml' --mark '6=vary:[/defaults/model]' --mark '11=exec:executor: release-app' \
   --mark '12=runs:runs: 3' --into scenes/s19.html
echo panels-ok
