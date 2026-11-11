# s15: the two neighbouring skills, then lint on the loading eval file. Free: no agent runs.
# Runs in /Users/Shared/demo/practice in place and changes nothing there.
# Needs: skills/commit-message, skills/release-notes and evals/loading.eval.yaml as the starter ships
# them (build-src/check-state.sh checks). vally's output is also saved to /tmp/vl-l9/s15.log.
# Each cat fills most of a screen, so the screen is cleared out of sight between commands; the
# renderer holds each screen until it has been talked about and read.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l9 && : > /tmp/vl-l9/s15.log; VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee -a /tmp/vl-l9/s15.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cat skills/commit-message/SKILL.md"
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

Type "cat skills/release-notes/SKILL.md"
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

Type "vally lint -e evals/loading.eval.yaml"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 4s
