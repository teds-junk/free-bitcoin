# s16: the same re-grade with typo-fix's token budget lowered for a moment; print the exit code.
# Runs in the lesson 5 "before" run's folder under /Users/Shared/demo/practice. No agent starts: no spend.
# Hidden setup WRITES one file: it copies src/state/changelog.lowered.eval.yaml (typo-fix's token-budget max
# lowered, see src/run/budget.json) over evals/changelog.eval.yaml, the edit the page makes in an editor (step 7),
# then changes into the one run folder under results/lesson-5-before.
# The wrapper copies src/state/changelog.eval.yaml back (step 8) as soon as the re-grade has finished, before it
# returns vally's exit code, so the budget is lowered only while that one command runs and `echo $?` still prints
# what vally exited with. If a recording is interrupted mid-command, the lowered budget is still in the practice
# folder: build-src/check-state.sh s18 reports it, and recording s14 or s18 puts the normal file back.
# Output and exit code are saved to /tmp/vl-l21/s16.1.log and s16.1.exit. About 110 lines: stills review needed.
# EXPECTED: exit code 1, and the typo-fix trials that passed in s14 now failing on token-budget alone.
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
Type `export PS1='\W $ ' PS2='' V=$PWD && cp src/state/changelog.lowered.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && cd /Users/Shared/demo/practice/results/lesson-5-before/2026* && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l21; mkdir -p $L; N=0; vally(){ N=$((N+1)); if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@"; fi | tee $L/s16.$N.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local e=${PIPESTATUS[0]}; echo $e > $L/s16.$N.exit; cp "$V/src/state/changelog.eval.yaml" /Users/Shared/demo/practice/evals/changelog.eval.yaml; return $e; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

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
