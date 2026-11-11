# s13: lint the tagged eval file, run the quick suite with --require-pass, print its exit code.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The hidden setup is run from the
# video folder (the tape's working directory), so the copies below use relative src/state/ paths.
# Hidden setup WRITES two files into the practice folder (the lesson's steps 1 and 2, which the page does in an
# editor): evals/changelog.eval.yaml with the five tags lines, and .vally.yaml with the two suites. It moves an
# existing results/lesson-21-quick aside to /Users/Shared/.demo-old.lesson-21-quick.<time>. Nothing is deleted.
# src/state/changelog.eval.yaml must be this series' own eval file plus the tags: run build-src/check-state.sh s13
# first, and build-src/make-state.py --from <the demo's file> if it says the two differ.
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (nothing else), saves each call's output to
# /tmp/vl-l21/s13.<n>.log and its exit code to s13.<n>.exit, and returns vally's own exit code, so that
# `echo $?` prints what vally exited with (1 = lint, 2 = the quick suite).
# The quick suite takes about a minute and is cut. With the four command lines its output is a little longer than
# one screen, so expect the credential scan to ask for a stills review.
# EXPECTED: exit code 0 (every stimulus passed, budgets included). A failing stimulus exits 1: that is a real
# result, not a reason to re-record; reword s13's outcome sentences instead. An ERROR trial also exits 1: re-record.
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
Type `export PS1='\W $ ' PS2='' && cp src/state/changelog.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && cp src/state/.vally.yaml /Users/Shared/demo/practice/.vally.yaml && cd /Users/Shared/demo/practice && { [ -e results/lesson-21-quick ] && mv results/lesson-21-quick "/Users/Shared/.demo-old.lesson-21-quick.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l21; mkdir -p $L; N=0; vally(){ N=$((N+1)); if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@"; fi | tee $L/s13.$N.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local e=${PIPESTATUS[0]}; echo $e > $L/s13.$N.exit; return $e; }`
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

Type `vally eval --suite quick \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --workers 2 --require-pass \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-21-quick"
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
