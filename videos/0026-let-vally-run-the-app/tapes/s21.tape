# s21: the experiment: three trials a model, through the app.
# Runs in /Users/Shared/demo/practice in place. Hidden setup as in s20, each step safe to repeat; an existing
# results/lesson-26-experiment is moved to /Users/Shared/.demo-old.lesson-26-experiment.<time>, never deleted.
# The wrapper shows /Users/Shared/demo as ~/src/demo and keeps what Vally printed in /tmp/vl-l26/s21.log.
# EXPECTED in this take: tracker-down shows "0 passed · 3 errors" for BOTH variants (the app's executor does
# not support simulation), at no cost, so each variant's count is out of two. Do NOT rerun the take for
# those. Rerun only if a since-last-release trial ends in ERROR.
# The run takes a minute or two and is cut.
# Spend: 6 agent runs
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
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l26 && cp src/state/vally-executor.mjs /Users/Shared/demo/practice/app/vally-executor.mjs && { grep -q '^plugins:' /Users/Shared/demo/practice/.vally.yaml || { cat src/state/plugins.yaml /Users/Shared/demo/practice/.vally.yaml > /tmp/vl-l26/vally.yaml && cp /tmp/vl-l26/vally.yaml /Users/Shared/demo/practice/.vally.yaml; }; } && cp src/state/release-app.experiment.yaml /Users/Shared/demo/practice/evals/release-app.experiment.yaml && cd /Users/Shared/demo/practice && { [ -e results/lesson-26-experiment ] && mv results/lesson-26-experiment "/Users/Shared/.demo-old.lesson-26-experiment.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l26/s21.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally experiment run \`
Sleep 400ms
Enter
Type `  evals/release-app.experiment.yaml \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-26-experiment"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@1500s /\$\s*$/
Show
Sleep 5s
