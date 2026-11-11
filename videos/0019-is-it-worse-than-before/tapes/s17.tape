# s17: the same on gpt-5.6-terra, with the regression check on, then its exit code (page steps 4 and 5).
# Runs inside the series' own lesson 15 experiment folder, in place. No agent run; 16 to 18 judge calls
# (two per pair), about two minutes, cut. `echo $?` is typed straight after, with no hidden command in
# between, because any command would replace the exit code. The vally wrapper returns vally's own code.
# NEEDS: one 2026* folder under results/lesson-15, with terra-before and terra-after in it
#        (build-src/check-state.sh s17).
# Hidden setup: as s14; moves an existing terra-compare.jsonl aside; log to /tmp/vl-l19/s17.log.
# LEAVES: terra-compare.jsonl in the experiment folder.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice/results/lesson-15/2026*/ && { [ -e terra-compare.jsonl ] && mv terra-compare.jsonl "/Users/Shared/.demo-old.l19.terra-compare.$(date +%s).jsonl"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l19 && : > /tmp/vl-l19/s17.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l19/s17.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local rc=${PIPESTATUS[0]}; echo "exit=$rc" >> /tmp/vl-l19/s17.log; return $rc; }`
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
Type `  --baseline terra-before \`
Sleep 400ms
Enter
Type `  --treatment terra-after \`
Sleep 400ms
Enter
Type `  --judge-model claude-sonnet-5.5 \`
Sleep 400ms
Enter
Type `  --fail-on-regression \`
Sleep 400ms
Enter
Type "  --output terra-compare.jsonl"
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
