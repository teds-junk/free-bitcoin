# s34: judge the two saved trials of s31's run again, with the judge model's name corrected. No agent runs.
# Judge calls: 2 (claude-sonnet-5.5). The budget unit is agent runs, so no Spend line.
# EXPECTED RESULT: a scoring warning, then two blocks, each "cache (2/2 graders passed)" with the judge's reason.
# Runs in the run's own folder under /Users/Shared/demo/practice/results/lesson-20 (exactly one must be there).
# Hidden setup installs src/state/fixed/judged.eval.yaml and changes into the run's folder. The wrapper skips
# `script` when input is redirected; output is saved to /tmp/vl-l20/s34.log. FontSize 28: the reasons are long.
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 28
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cp src/state/fixed/judged.eval.yaml /Users/Shared/demo/practice/evals/broken/judged.eval.yaml && cd /Users/Shared/demo/practice/results/lesson-20/2026*/`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); mkdir -p /tmp/vl-l20; : > /tmp/vl-l20/s34.log; vally(){ if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@" 2>&1; fi | sed -l -e 's|/Users/Shared/demo|~/src/demo|g' -e 's|file:///[^ ]*/node_modules/|file:///.../node_modules/|g' | tee -a /tmp/vl-l20/s34.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally grade \`
Sleep 400ms
Enter
Type `  -e ../../../evals/broken/judged.eval.yaml \`
Sleep 400ms
Enter
Type "  --run-dir . --verbose < results.jsonl"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@300s /\$\s*$/
Show
Sleep 5s
