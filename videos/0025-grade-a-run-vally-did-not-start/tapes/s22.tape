# s22: grade the app's run with the eval file. Free: vally grade starts no agent, and this stimulus has
# no judge grader (the hidden test, two tool-calls graders, max-repeat, skill-invocation).
# Runs in /Users/Shared/demo/practice in place; needs app-run/trajectory.json (s20), app-run/repo and
# app-run/change.diff (s17), and evals/release.eval.yaml with the since-last-release stimulus as the
# lesson 23 and 24 videos leave it. Changes nothing in the practice folder.
# The wrapper does NOT use `script`: with standard input redirected, `script` echoes the whole
# trajectory onto the screen. vally grade prints no colour, so a plain pipe loses nothing. It shows
# /Users/Shared/demo as ~/src/demo (nothing else) and saves the output to /tmp/vl-l25/s22.log.
# FontSize 30, so each grader's line and the five-line command fit one screen.
# A failing verdict here is a result, not an error: do not rerun for a different one.
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 30
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l25`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ "$VB" "$@" 2>&1 | sed -l 's|/private/Users/Shared/demo|~/src/demo|g; s|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l25/s22.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally grade -e evals/release.eval.yaml \`
Sleep 400ms
Enter
Type `  --stimulus since-last-release \`
Sleep 400ms
Enter
Type `  --workspace app-run/repo \`
Sleep 400ms
Enter
Type `  --diff-file app-run/change.diff \`
Sleep 400ms
Enter
Type `  --verbose < app-run/trajectory.json`
Sleep 400ms
Enter
Wait@120s /\$\s*$/
Sleep 5s
