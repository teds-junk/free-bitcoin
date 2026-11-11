# s17: both tests on every stimulus (lesson page step 10).
# Runs in /Users/Shared/demo/practice in place. Free: no agent run.
# NEEDS: evals/golden/typo-fix.patch (left by s11), and src/state/golden/ holding security.patch, two-changes.patch
#        and after-release.patch: each the workspace.patch of a trial from this series' own run that was read and
#        judged correct (page step 9). The three there now are stand-ins from verified/lesson-07.
# Hidden setup: those three patches are copied into evals/golden, and the eval file becomes
#        src/state/10-all-golden (= verified/lesson-07: a golden_patch on four stimuli, none on refactor).
#        vally is wrapped as in s13; log /tmp/vl-l7/s17.log. After recording, copy it over src/run/s17.log.
# The second report is longer than the screen and scrolls: the credential scan will call the recording partly
#        scanned (TERMINAL-DEMOS.md -> Credentials on screen). Scene s18 shows both reports in full as a table.
# LEAVES: the practice folder as verified/lesson-07 has it (golden patches aside).
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && S=/Users/ted/src/learn/vally/videos/0007-test-a-grader/src/state && cp $S/golden/security.patch $S/golden/two-changes.patch $S/golden/after-release.patch evals/golden/ && cp $S/10-all-golden.changelog.eval.yaml evals/changelog.eval.yaml && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l7 && : > /tmp/vl-l7/s17.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l7/s17.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type `clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally oracle -e evals/changelog.eval.yaml --verbose`
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
Type `  --no-golden-input --verbose`
Sleep 400ms
Enter
Sleep 1s
Wait@60s /\$\s*$/
Sleep 4s

