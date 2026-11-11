# s15: the oracle catches a grader that cannot fail (lesson page step 8).
# Runs in /Users/Shared/demo/practice in place. Free: no agent run.
# NEEDS: evals/golden/typo-fix.patch (left by s11).
# Hidden setup: the eval file becomes src/state/08-useless-grader (05 plus the five mentions-unreleased lines at
#        the top of the typo-fix graders, shown in scene s14). vally is wrapped as in s13; log /tmp/vl-l7/s15.log.
# LEAVES: the eval file WITH the useless grader still in it. Tape s17's hidden setup replaces the eval file
#        (src/state/10-all-golden), which is when the five lines go (page step 8's last sentence); if s17 is not
#        recorded straight after, copy src/state/05-golden-typo-fix over evals/changelog.eval.yaml by hand.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && S=/Users/ted/src/learn/vally/videos/0007-test-a-grader/src/state && cp $S/08-useless-grader.changelog.eval.yaml evals/changelog.eval.yaml && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l7 && : > /tmp/vl-l7/s15.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l7/s15.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
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
Type `  --stimulus typo-fix --no-golden-input --verbose`
Sleep 400ms
Enter
Sleep 1s
Wait@60s /\$\s*$/
Sleep 4s
