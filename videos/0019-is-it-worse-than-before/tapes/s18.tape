# s18: haiku again with the two roles swapped and the regression check on, then its exit code
# (page steps 6 and 7). Runs inside the series' own lesson 15 experiment folder, in place.
# No agent run; 18 judge calls, about two minutes, cut. This command writes no file.
# The result varies from run to run: in the course's own two runs it exited 1 once and 0 once.
# Record it once and narrate what it did; do not record again for a different exit code.
# NEEDS: one 2026* folder under results/lesson-15, with haiku-before and haiku-after in it
#        (build-src/check-state.sh s18).
# Hidden setup: as s14, with nothing to move aside; log to /tmp/vl-l19/s18.log.
# LEAVES: nothing changed.
# Judge calls: 18
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 30
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice/results/lesson-15/2026*/ &&  clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l19 && : > /tmp/vl-l19/s18.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l19/s18.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local rc=${PIPESTATUS[0]}; echo "exit=$rc" >> /tmp/vl-l19/s18.log; return $rc; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally compare \`
Sleep 400ms
Enter
Type `  --baseline haiku-after \`
Sleep 400ms
Enter
Type `  --treatment haiku-before \`
Sleep 400ms
Enter
Type `  --judge-model claude-sonnet-5.5 \`
Sleep 400ms
Enter
Type "  --fail-on-regression"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 1s

Type "echo $?"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
