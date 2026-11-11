# s15: lint the release eval file with the four new graders in it, then the oracle on the baseline.
# Free: vally lint and vally oracle start no agent, so this tape declares no cost.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Hidden setup WRITES one file there: evals/release.eval.yaml, replaced by this video's
# src/state/release.eval.yaml (the lesson 22 file plus the page's twenty lines: step 1 of the checkpoint,
# which the page does in an editor and s07 to s11 show in a panel). build-src/check-state.sh checks first
# that the file being replaced is the one the lesson 22 video left.
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (rewritten, nothing else) and keeps a copy of
# the output in /tmp/vl-l23/s15.log for build-src/collect-run.sh.
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 31
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l23 && : > /tmp/vl-l23/s15.log && cp /Users/ted/src/learn/vally/videos/0023-check-what-the-agent-did/src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee -a /tmp/vl-l23/s15.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/release.eval.yaml"
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

Type `vally oracle -e evals/release.eval.yaml \`
Sleep 400ms
Enter
Type "  --no-golden-input"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 4s
