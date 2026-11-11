# s10: find the lesson 5 "before" run, change into it, re-grade it with the graders as they are.
# Runs in /Users/Shared/demo/practice in place. No agent starts: vally grade and vally oracle are free,
# so this tape declares no cost. The practice folder must already hold the series' own lesson 5
# "before" run (exactly one folder under results/lesson-5-before) and the lesson 7 golden patches.
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (rewritten, nothing else). It is skipped
# when input is redirected (vally grade < results.jsonl), where `script` would echo the input file;
# the verified run's re-grade output contains no path.
# The re-grade prints about 106 lines, so the screen scrolls: the credential scan sees one screenful
# and the recording will need the stills review (redact.js --stills, secret-scan.js --reviewed).
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ if [ -t 0 ]; then script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; else "$VB" "$@"; fi; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ls results/lesson-5-before"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd results/lesson-5-before/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally grade -e ../../../evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type "  --run-dir . < results.jsonl"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 4s
