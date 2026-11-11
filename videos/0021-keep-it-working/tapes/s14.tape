# s14: re-grade the series' lesson 5 "before" run with today's eval file and --require-pass; print the exit code.
# Runs in /Users/Shared/demo/practice in place. No agent starts: no spend.
# Hidden setup WRITES one file: it copies src/state/changelog.eval.yaml (tags, budgets at their normal values)
# over evals/changelog.eval.yaml, the same copy s13 makes, so this tape can be recorded alone.
# Needs exactly one run folder under results/lesson-5-before (the lesson 5 video's s14 run): its name is
# completed with Tab, so the tape does not need to know the time it was made.
# vally grade reads results.jsonl on stdin, so the wrapper runs it without `script` (which would echo the file);
# its output and exit code are saved to /tmp/vl-l21/s14.1.log and s14.1.exit.
# The re-grade prints about 106 lines: the recording ends on the last blocks and the exit code, and the credential
# scan will ask for a stills review.
# EXPECTED: exit code 1. That run is full of failing verdicts, and showing one fail loudly is the point.
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
Type `export PS1='\W $ ' PS2='' && cp src/state/changelog.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l21; mkdir -p $L; N=0; vally(){ N=$((N+1)); if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@"; fi | tee $L/s14.$N.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local e=${PIPESTATUS[0]}; echo $e > $L/s14.$N.exit; return $e; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

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
Type "  --run-dir . --require-pass < results.jsonl"
Sleep 400ms
Enter
Wait@180s /\$\s*$/
Sleep 1s

Type "echo $?"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
