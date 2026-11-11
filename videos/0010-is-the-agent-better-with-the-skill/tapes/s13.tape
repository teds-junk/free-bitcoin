# s13: the dry run of the with-and-without experiment. Starts no agent and writes nothing to the
# practice folder. Runs in /Users/Shared/demo/practice in place; needs the practice folder as the
# lesson 9 video left it (build-src/check-state.sh checks). Vally's output is also saved to
# /tmp/vl-l10/s13.log for the scene generator. Any absolute path Vally prints is shown as ~/src/demo
# (rewritten, nothing else). FontSize 28: the experiment's table in s14 is 96 columns wide, and the
# two scenes sit together. The plan is 33 lines, longer than the screen, so its last blocks stay in view.
# Spend: none
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l10; VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l10/s13.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally experiment run \`
Sleep 400ms
Enter
Type "  evals/with-and-without.experiment.yaml --dry-run"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 5s
