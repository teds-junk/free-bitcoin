# s13: the oracle on typo-fix, with the golden patch and then without it (lesson page steps 6 and 7).
# Runs in /Users/Shared/demo/practice in place. Free: no agent run.
# NEEDS: evals/golden/typo-fix.patch (left by s11).
# Hidden setup: the eval file becomes src/state/05-golden-typo-fix (lesson 6's file plus the two golden_patch
#        lines in typo-fix: page step 5, shown in scene s12). vally is wrapped so that an absolute path, if it
#        prints one, shows as ~/src/demo (nothing else is changed), and so that its output is also saved to
#        /tmp/vl-l7/s13.log. After recording, copy that log over src/run/s13.log and run make-scenes.py.
# LEAVES: the eval file with the typo-fix golden_patch lines.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && S=/Users/ted/src/learn/vally/videos/0007-test-a-grader/src/state && cp $S/05-golden-typo-fix.changelog.eval.yaml evals/changelog.eval.yaml && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l7 && : > /tmp/vl-l7/s13.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l7/s13.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type `clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally oracle -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type `  --stimulus typo-fix --verbose`
Sleep 400ms
Enter
Sleep 1s
Wait@60s /\$\s*$/
Sleep 1s

Hide
Type `clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally oracle -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type `  --stimulus typo-fix --no-golden-input --verbose`
Sleep 400ms
Enter
Sleep 1s
Wait@60s /\$\s*$/
Sleep 4s

