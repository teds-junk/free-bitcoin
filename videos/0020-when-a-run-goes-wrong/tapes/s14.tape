# s14: copy the four broken eval files in, lint the first, run it. EXPECTED RESULT: ERROR on both models
# ("The "command" argument must be of type string..."), plus a reporter stack trace. That ERROR is the lesson's
# subject: do NOT rerun this take because it ended in ERROR. Rerun only if the error text is a different one.
# No Spend line: neither trial reaches an agent (each ends in milliseconds), so no agent run is used.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The tape's working directory is
# the video folder, so hidden copies use relative src/state/ paths. Nothing is deleted: anything in the way
# is moved aside. Vally's Saved line is shown as ~/src/demo, and the stack trace's file:// paths as
# file:///.../node_modules/ (paths rewritten, nothing else). Vally's output is also saved to /tmp/vl-l20/.
# Hidden setup moves aside, to /Users/Shared/.demo-old.lesson-20.<what>.<time>: an existing evals/broken (so the
# visible cp creates it, as on the page), results/lesson-20 and results/lesson-20-earlier.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && T=$(date +%s) && for x in evals/broken results/lesson-20 results/lesson-20-earlier; do [ -e $x ] && mv $x /Users/Shared/.demo-old.lesson-20.$(basename $x).$T; done; true`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); mkdir -p /tmp/vl-l20; : > /tmp/vl-l20/s14.log; vally(){ if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@" 2>&1; fi | sed -l -e 's|/Users/Shared/demo|~/src/demo|g' -e 's|file:///[^ ]*/node_modules/|file:///.../node_modules/|g' | tee -a /tmp/vl-l20/s14.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cp -R ../practice-starter/evals/broken evals/broken"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "vally lint -e evals/broken/merged-list.eval.yaml"
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

Type `vally eval -e evals/broken/merged-list.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-20"
Sleep 400ms
Enter
Wait@120s /\$\s*$/
Sleep 5s
