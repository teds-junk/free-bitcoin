# s18: the cost experiment: four variants, five stimuli, three trials each, then the folder it saved.
# Runs in /Users/Shared/demo/practice in place and adds results/lesson-16 beside the earlier runs.
# The hidden setup copies src/state/cost.experiment.yaml into practice/evals/ (as s17 does), so the
# tape can be recorded alone, and moves an existing results/lesson-16 aside, to
# /Users/Shared/.demo-old.lesson-16.<time>, so the listing shows one run. Nothing is deleted.
# Vally prints its Output line as an absolute path; it is shown as ~/src/demo (rewritten, nothing else).
# What vally prints is also saved to /tmp/vl-l16/s18.log: copy it over src/run/s18.log afterwards.
# The run takes several minutes and is cut. Its output (four warnings, then the table) is longer than
# one screen; the table is at its end. It is cleared out of sight before the listing; the renderer
# holds it until it has been talked about and read.
# Spend: 60 agent runs
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
Type `export PS1='\W $ ' PS2='' && cp src/state/cost.experiment.yaml /Users/Shared/demo/practice/evals/cost.experiment.yaml && cd /Users/Shared/demo/practice && { [ -e results/lesson-16 ] && mv results/lesson-16 "/Users/Shared/.demo-old.lesson-16.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l16 && : > /tmp/vl-l16/s18.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l16/s18.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
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
Type `  evals/cost.experiment.yaml \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-16"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@2700s /\$\s*$/
Show
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ls results/lesson-16"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
