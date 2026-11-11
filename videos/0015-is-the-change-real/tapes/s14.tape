# s14: the before-and-after experiment: both versions of the skill on both models, three trials of each stimulus.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Needs s13's end state: skills/changelog-entry-before (the skill before the edit) and the sharpened rule in
# skills/changelog-entry/SKILL.md. The hidden setup copies src/state/SKILL.md over the skill again (the same
# file s13 installs, so this changes nothing after s13) so that the tape can be recorded alone.
# Re-recording: an existing results/lesson-15 is moved aside to /Users/Shared/.demo-old.lesson-15.<time>.
# Nothing is deleted.
# Vally's output is also saved to /tmp/vl-l15/s14.log: copy it to src/run/s14.log (see src/run/PROVISIONAL).
# Any absolute path is shown as ~/src/demo (rewritten, nothing else).
# The run takes fifteen minutes or more and is cut. The screen comes back on the end of the output: the table.
# Spend: 36 agent runs
# Judge calls: 36
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l15 && { [ -e results/lesson-15 ] && mv results/lesson-15 "/Users/Shared/.demo-old.lesson-15.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `cp /Users/ted/src/learn/vally/videos/0015-is-the-change-real/src/state/SKILL.md skills/changelog-entry/SKILL.md && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l15/s14.log; }`
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
Type `  evals/before-and-after.experiment.yaml \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-15"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@2400s /\$\s*$/
Show
Sleep 5s
