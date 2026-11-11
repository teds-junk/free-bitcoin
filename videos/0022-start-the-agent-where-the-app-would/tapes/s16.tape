# s16: the app's situation on both models, five trials each, into results/lesson-22.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The hidden setup is run from
# the video folder, so the copies use relative src/state/ paths. It installs the same two files as s15 (so
# this tape can be recorded alone) and moves an existing results/lesson-22 aside to
# /Users/Shared/.demo-old.lesson-22.<time>. Nothing is deleted.
# Vally prints its Saved line as a path; the wrapper shows /Users/Shared/demo as ~/src/demo (nothing else),
# and saves the output to /tmp/vl-l22/s16.log for build-src/collect-run.sh.
# The run takes a few minutes and is cut. The output is longer than one screen; the recording comes back
# on its end: the failures, the model summary, the table and the Saved line.
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
Type `export PS1='\W $ ' PS2='' && cp src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cp src/state/check-release.mjs /Users/Shared/demo/practice/evals/grading/check-release.mjs && cd /Users/Shared/demo/practice && { [ -e results/lesson-22 ] && mv results/lesson-22 "/Users/Shared/.demo-old.lesson-22.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l22; VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l22/s16.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/release.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --runs 5 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-22"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@1200s /\$\s*$/
Show
Sleep 5s
