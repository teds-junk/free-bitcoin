# s12: lint the six-stimulus eval file, run it once on each model without grading, then list the run's folder.
# Runs in /Users/Shared/demo/practice in place. The demo folder is NOT reset: the runs the earlier videos quote
# (results/lesson-1, results/lesson-3) stay where they are, and this adds results/lesson-4 beside them.
# Re-recording: the hidden setup moves an existing results/lesson-4 aside, to
# /Users/Shared/.demo-old.lesson-4.<time>, so the listing shows one run. Nothing is deleted.
# Vally prints its Saved line as an absolute path; it is shown as ~/src/demo (rewritten, nothing else).
# The run takes a minute or two and is cut. Its output is cleared out of sight before the listing;
# the renderer holds it until it has been talked about and read.
# Spend: 12 agent runs
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-4 ] && mv results/lesson-4 "/Users/Shared/.demo-old.lesson-4.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/six-requests.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally eval -e evals/six-requests.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --skip-grade --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-4"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ls results/lesson-4"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
