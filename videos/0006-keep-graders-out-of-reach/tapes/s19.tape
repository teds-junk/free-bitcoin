# s19: the same five stimuli again, after the fourth rule is added to the skill.
# Runs in /Users/Shared/demo/practice in place. The hidden setup makes the lesson's second file edit,
# which the video shows in a panel (s18): skills/changelog-entry/SKILL.md becomes src/state/SKILL.md
# (lesson 5's skill plus the three-line Unreleased rule; identical to verified/lesson-06). It also
# makes sure evals/changelog.eval.yaml is src/state/changelog.eval.yaml.
# Leaves: results/lesson-6-after/<time>, and the practice folder equal to verified/lesson-06/practice
# (apart from results, kept and whatever earlier lessons' notes exist).
# Re-recording: an existing results/lesson-6-after is moved aside. Nothing is deleted.
# Any absolute path Vally prints is shown as ~/src/demo (rewritten, nothing else).
# The run takes about a minute and is cut.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-6-after ] && mv results/lesson-6-after "/Users/Shared/.demo-old.lesson-6.results-lesson-6-after.$(date +%s)"; true; } && cp /Users/ted/src/learn/vally/videos/0006-keep-graders-out-of-reach/src/state/changelog.eval.yaml evals/changelog.eval.yaml && cp /Users/ted/src/learn/vally/videos/0006-keep-graders-out-of-reach/src/state/SKILL.md skills/changelog-entry/SKILL.md && clear`
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

Type `vally eval -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-6-after"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
