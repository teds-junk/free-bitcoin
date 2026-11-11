# s17: the dry run of the cost experiment. Starts no agent.
# Runs in /Users/Shared/demo/practice in place. The hidden setup copies this video's
# src/state/cost.experiment.yaml to practice/evals/cost.experiment.yaml (the file the lesson has the
# reader create; scene s13 walks it), so the tape can be recorded alone. The tape's working directory
# is the video folder, so the copy uses a relative path and no home folder is typed.
# The plan is about 32 rows, longer than one screen; the last blocks are what stays on screen.
# Spend: none
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
Type `export PS1='\W $ ' PS2='' && cp src/state/cost.experiment.yaml /Users/Shared/demo/practice/evals/cost.experiment.yaml && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l16 && : > /tmp/vl-l16/s17.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l16/s17.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
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
Type "  evals/cost.experiment.yaml --dry-run"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 5s
