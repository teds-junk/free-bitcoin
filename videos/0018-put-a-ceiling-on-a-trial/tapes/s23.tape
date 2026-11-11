# s23: with the time limit added, lint, then run the five stimuli once on both models.
# Runs in /Users/Shared/demo/practice in place (the course's one practice folder; nothing is reset).
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (rewritten, nothing else) and appends what
# vally printed to /tmp/vl-l18/s23.log, which build-src/capture-run.py copies into src/run/.
# When input is redirected (vally grade < results.jsonl) the wrapper uses tee and not `script`, which
# would echo the input file; vally grade prints no colour and no path, so the screen is unchanged.
# Hidden setup WRITES to the demo folder: it copies this video's src/state/changelog.final.eval.yaml over
# evals/changelog.eval.yaml (wide budgets plus a constraints block under each stimulus; the practice
# folder then matches verified/lesson-18), and moves an existing results/lesson-18 aside to
# /Users/Shared/.demo-old.lesson-18.<time>, so a re-recording leaves one run. Nothing is deleted.
# The run takes about a minute and is cut.
# Spend: 10 agent runs
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0018-put-a-ceiling-on-a-trial/src/state/changelog.final.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && { [ -e results/lesson-18 ] && mv results/lesson-18 "/Users/Shared/.demo-old.lesson-18.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l18/s23.log; mkdir -p /tmp/vl-l18; : > $L; vally(){ if [ -t 0 ]; then script -q -a $L "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; else "$VB" "$@" 2>&1 | tee -a $L; fi; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/changelog.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-18"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 5s
