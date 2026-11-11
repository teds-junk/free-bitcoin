# s16: check the plugin file, then run the release eval through the app on both models.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Hidden setup, from this video's src/state/ (verified/lesson-26 files), each step safe to repeat:
#   app/vally-executor.mjs   the plugin with execute written (the page's step 1)
#   .vally.yaml              the three plugins lines are put at its top unless a plugins section is there
#                            already (the page's step 3); the rest of the file is left as the series has it
#   results/lesson-26        an existing one is moved to /Users/Shared/.demo-old.lesson-26.<time>; nothing is deleted
# Needs app/node_modules (npm install --prefix app, done for lesson 25): Vally imports the plugin, and the
# plugin imports @microsoft/vally and the app, which imports @github/copilot-sdk.
# Vally prints its Saved line as an absolute path; the wrapper shows /Users/Shared/demo as ~/src/demo (nothing
# else changes) and keeps a copy of what Vally printed in /tmp/vl-l26/s16.log for src/run/.
# EXPECTED in this take: tracker-down ends in ERROR on both models, with the "does not support tool-call
# simulation" message, at no cost. That is the lesson's point; do NOT rerun the take for it. Rerun only if
# since-last-release ends in ERROR on either model.
# The run takes under a minute and is cut.
# Spend: 2 agent runs
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 34
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l26 && cp src/state/vally-executor.mjs /Users/Shared/demo/practice/app/vally-executor.mjs && { grep -q '^plugins:' /Users/Shared/demo/practice/.vally.yaml || { cat src/state/plugins.yaml /Users/Shared/demo/practice/.vally.yaml > /tmp/vl-l26/vally.yaml && cp /tmp/vl-l26/vally.yaml /Users/Shared/demo/practice/.vally.yaml; }; } && cd /Users/Shared/demo/practice && { [ -e results/lesson-26 ] && mv results/lesson-26 "/Users/Shared/.demo-old.lesson-26.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l26/s16.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "node --check app/vally-executor.mjs"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 2s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/release.eval.yaml \`
Sleep 400ms
Enter
Type `  --executor release-app \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-26"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
