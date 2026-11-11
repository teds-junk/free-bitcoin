# s16: lint the changelog eval file (free), then run its five stimuli once on each model.
# Runs in /Users/Shared/demo/practice in place. Needs: evals/grading/check-entry.mjs (in the starter).
# The hidden setup makes the lesson's first file edit, which the video shows in a panel (s15) and not
# in the terminal: evals/changelog.eval.yaml becomes src/state/changelog.eval.yaml (lesson 5's file
# plus the two stimuli from evals/snippets/lesson-6-stimuli.yaml; identical to verified/lesson-06).
# It also puts skills/changelog-entry/SKILL.md back to src/state/SKILL.before.md (verified/lesson-05),
# so a re-recording after s19 still runs without the fourth rule.
# Leaves: results/lesson-6/<time> (exactly one run folder; s17 completes its name with Tab).
# Re-recording: an existing results/lesson-6 is moved aside, to /Users/Shared/.demo-old.lesson-6.<name>.<time>.
# Any absolute path Vally prints is shown as ~/src/demo (rewritten, nothing else).
# The lint output is cleared out of sight before the run; the run takes about a minute and is cut.
# Spend: 10 agent runs
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-6 ] && mv results/lesson-6 "/Users/Shared/.demo-old.lesson-6.results-lesson-6.$(date +%s)"; true; } && cp /Users/ted/src/learn/vally/videos/0006-keep-graders-out-of-reach/src/state/changelog.eval.yaml evals/changelog.eval.yaml && cp /Users/ted/src/learn/vally/videos/0006-keep-graders-out-of-reach/src/state/SKILL.before.md skills/changelog-entry/SKILL.md && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/changelog.eval.yaml"
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

Type `vally eval -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-6"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
