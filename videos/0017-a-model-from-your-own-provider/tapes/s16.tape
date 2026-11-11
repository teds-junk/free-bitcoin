# s16: the dry run of the experiment, with the fifth variant in the file.
# Runs in /Users/Shared/demo/practice in place.
# Hidden setup WRITES one file there: the lesson has the reader edit evals/cost.experiment.yaml in a text
# editor (the vary list becomes six lines, and the qwen-local variant is added); the tape copies this
# video's src/state/cost.experiment.yaml over it out of sight. That file is verified/lesson-17's.
# Needs: evals/cost.experiment.yaml as the lesson 16 video left it (build-src/check-state.sh compares it
# with src/state/cost.experiment.before.yaml), and evals/changelog.eval.yaml beside it.
# The wrapper shows /Users/Shared/demo as ~/src/demo (nothing else is changed) and saves vally's output
# to /tmp/vl-l17/s16.log, for src/run/s16.log.
# The plan is about 35 lines, so it scrolls: the screen ends on the last blocks, qwen-local among them.
# A dry run starts nothing: no agent run, on the Copilot account or locally.
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
Type `export PS1='\W $ ' PS2='' V="$PWD" && cd /Users/Shared/demo/practice && cp "$V/src/state/cost.experiment.yaml" evals/cost.experiment.yaml && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l17 && : > /tmp/vl-l17/s16.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l17/s16.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
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
Sleep 4s
