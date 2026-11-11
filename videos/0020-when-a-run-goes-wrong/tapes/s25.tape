# s25: run the third broken file with --verbose. EXPECTED RESULT: FAIL on both models (adds-an-entry:
# "Pattern /^\+.*notes add/ not found in workspace diff"). The FAIL is the lesson's subject: keep it.
# If a trial ends in ERROR instead, rerun.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The tape's working directory is
# the video folder, so hidden copies use relative src/state/ paths. Nothing is deleted: anything in the way
# is moved aside. Vally's Saved line is shown as ~/src/demo, and the stack trace's file:// paths as
# file:///.../node_modules/ (paths rewritten, nothing else). Vally's output is also saved to /tmp/vl-l20/.
# Hidden setup installs src/state/broken/entry.eval.yaml (the pattern without (?m)) and moves the earlier runs
# to results/lesson-20-earlier, so this run's folder is the only one under results/lesson-20 for s27 and s30.
# Spend: 2 agent runs
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
Type `export PS1='\W $ ' PS2='' && cp src/state/broken/entry.eval.yaml /Users/Shared/demo/practice/evals/broken/entry.eval.yaml && cd /Users/Shared/demo/practice && mkdir -p results/lesson-20-earlier && for d in results/lesson-20/2026*; do [ -e "$d" ] && mv "$d" results/lesson-20-earlier/; done; true`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); mkdir -p /tmp/vl-l20; : > /tmp/vl-l20/s25.log; vally(){ if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@" 2>&1; fi | sed -l -e 's|/Users/Shared/demo|~/src/demo|g' -e 's|file:///[^ ]*/node_modules/|file:///.../node_modules/|g' | tee -a /tmp/vl-l20/s25.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/broken/entry.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --workers 2 --output-dir results/lesson-20 \`
Sleep 400ms
Enter
Type "  --verbose"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 5s
