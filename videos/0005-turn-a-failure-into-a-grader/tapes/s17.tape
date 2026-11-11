# s17: the count after the edit. The same command, into results/lesson-5-after.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The hidden setup is run from
# the video folder (the tape's working directory), so the copies below use relative src/state/ paths.
# Vally prints its Saved line as a path; the wrapper shows /Users/Shared/demo as ~/src/demo (nothing else).
# Hidden setup installs the edited skill (src/state/SKILL.md: the first draft plus the lesson's seven
# lines, the page's step 5) and the eval file with graders, and moves an existing results/lesson-5-after
# aside to /Users/Shared/.demo-old.lesson-5-after.<time>. Nothing is deleted. It leaves the practice
# folder's eval file and skill as verified/lesson-05 has them.
# Spend: 18 agent runs
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
Type `export PS1='\W $ ' PS2='' && cp src/state/changelog.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && cp src/state/SKILL.md /Users/Shared/demo/practice/skills/changelog-entry/SKILL.md && cd /Users/Shared/demo/practice && { [ -e results/lesson-5-after ] && mv results/lesson-5-after "/Users/Shared/.demo-old.lesson-5-after.$(date +%s)"; true; } && clear`
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
Type `  --runs 3 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-5-after"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
