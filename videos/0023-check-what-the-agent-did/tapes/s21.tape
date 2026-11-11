# s21: one real run with every grader: the release stimulus, three trials on each model.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Hidden setup WRITES there: evals/release.eval.yaml is replaced by src/state/release.eval.yaml (so a
# re-recording after s19 starts right), and an existing results/lesson-23 is moved aside to
# /Users/Shared/.demo-old.lesson-23.<time>, so the run folder holds one run. Nothing is deleted.
# Vally prints its Saved line as an absolute path; it is shown as ~/src/demo (rewritten, nothing else).
# A copy of the output goes to /tmp/vl-l23/s21.log for build-src/collect-run.sh.
# The run takes a minute or two and is cut. FAIL for haiku is an expected verdict, not a reason to
# re-record; an ERROR trial is: rerun the take.
# The output is longer than one screen (about 32 lines), so the recording will need the stills review.
# Spend: 6 agent runs
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
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l23 && : > /tmp/vl-l23/s21.log && cp /Users/ted/src/learn/vally/videos/0023-check-what-the-agent-did/src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cd /Users/Shared/demo/practice && { [ -e results/lesson-23 ] && mv results/lesson-23 "/Users/Shared/.demo-old.lesson-23.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee -a /tmp/vl-l23/s21.log; }`
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
Type `  --runs 3 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-23"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
