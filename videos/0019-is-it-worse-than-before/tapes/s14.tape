# s14: judge the before skill against the after skill on claude-haiku-4.5 (lesson page step 2).
# Runs inside the series' own lesson 15 experiment folder in /Users/Shared/demo/practice, in place.
# No agent run. It calls the judge model twice for each of nine pairs and takes about two minutes;
# the wait is cut. The output is longer than the screen, so the recording comes back on its end:
# the printed block and the "Wrote" line.
# NEEDS: exactly one 2026* folder under results/lesson-15, with haiku-before and haiku-after in it,
#        each holding results.jsonl (build-src/check-state.sh s14).
# Hidden setup: sets the prompt, changes into that folder, moves an existing haiku-compare.jsonl aside to
#        /Users/Shared/.demo-old.l19.haiku-compare.<time>.jsonl (nothing is deleted), and wraps vally so
#        that an absolute path, if it prints one, shows as ~/src/demo (nothing else is changed), its
#        output is also saved to /tmp/vl-l19/s14.log, and its exit code is kept and written to that log.
# LEAVES: haiku-compare.jsonl in the experiment folder. build-src/collect-run.sh copies it and the log.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice/results/lesson-15/2026*/ && { [ -e haiku-compare.jsonl ] && mv haiku-compare.jsonl "/Users/Shared/.demo-old.l19.haiku-compare.$(date +%s).jsonl"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l19 && : > /tmp/vl-l19/s14.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l19/s14.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local rc=${PIPESTATUS[0]}; echo "exit=$rc" >> /tmp/vl-l19/s14.log; return $rc; }`
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
Type `  --baseline haiku-before \`
Sleep 400ms
Enter
Type `  --treatment haiku-after \`
Sleep 400ms
Enter
Type `  --judge-model claude-sonnet-5.5 \`
Sleep 400ms
Enter
Type "  --output haiku-compare.jsonl"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
