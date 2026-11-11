# s11: keep one saved trial's patch as the golden patch for typo-fix (lesson page steps 1, 2 without the cat, 3, 4).
# Runs in /Users/Shared/demo/practice in place. Free: no agent run.
# NEEDS: results/lesson-6-after holding exactly ONE run folder whose name starts with 2026 (Tab completes it),
#        and claude-haiku-4.5/0 below replaced by <model>/<trial> of a typo-fix trial in that run whose patch
#        was read and judged correct (the lesson page uses claude-haiku-4.5/0). The same patch must be
#        src/run/typo-fix.patch, which scene s04 shows.
# Hidden setup (so a re-recording starts clean): an existing evals/golden is moved aside to
#        /Users/Shared/.demo-old.golden.<time> (nothing is deleted), and evals/changelog.eval.yaml is put back to
#        src/state/00-start (= verified/lesson-06; run build-src/check-state.sh first to see it is what is there).
# LEAVES: evals/golden/typo-fix.patch; the eval file as lesson 6 left it.
# The cat of the patch (page step 2) is left out: scene s04 has already walked through that file in a panel.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && S=/Users/ted/src/learn/vally/videos/0007-test-a-grader/src/state && { [ -e evals/golden ] && mv evals/golden "/Users/Shared/.demo-old.golden.$(date +%s)"; true; } && cp $S/00-start.changelog.eval.yaml evals/changelog.eval.yaml && clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `ls results/lesson-6-after`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `cd results/lesson-6-after/2026`
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `cd changelog`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `mkdir ../../../../evals/golden`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `cp typo-fix/claude-haiku-4.5/0/workspace.patch \`
Sleep 400ms
Enter
Type `  ../../../../evals/golden/typo-fix.patch`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `cd ../../../..`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
