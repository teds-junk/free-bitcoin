# s18: the failing stimulus, three trials on each model. The tool's failure is simulated on purpose.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Hidden setup WRITES evals/release.eval.yaml (the same copy as s17, so this tape can be recorded alone)
# and moves an existing results/lesson-24 aside to /Users/Shared/.demo-old.lesson-24.<time>. Nothing is
# deleted. Vally prints its Saved line as a path; the wrapper shows /Users/Shared/demo as ~/src/demo and
# a trial's temporary folder as /tmp/trial (nothing else), and saves the output to /tmp/vl-l24/s18.log,
# which the scenes' checks read.
# EXPECTED here: a FLAKY or FAIL verdict is a result, not a fault (the page's own run was FLAKY on one
# model). An ERROR trial is NOT expected: rerun the take if any trial ends in ERROR.
# The run takes a minute or two and is cut. Its output is longer than one screen: the recording comes
# back on the end of it (the failures with the judge's reason, the model summary, the table).
# Spend: 6 agent runs
# Judge calls: 6 (claude-sonnet-5.5, one per trial; not counted in the agent-run budget)
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
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l24 && cp src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cd /Users/Shared/demo/practice && { [ -e results/lesson-24 ] && mv results/lesson-24 "/Users/Shared/.demo-old.lesson-24.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g; s|/private/var/folders/[^ \"]*/T/vally-eval-trial-[A-Za-z0-9]*|/tmp/trial|g; s|/var/folders/[^ \"]*/T/vally-eval-trial-[A-Za-z0-9]*|/tmp/trial|g' | tee /tmp/vl-l24/s18.log; }`
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
Type `  --tag case=tool-fails \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --runs 3 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-24"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
