# s19: the loading eval again, with the rewritten description.
# Runs in /Users/Shared/demo/practice in place.
# Hidden setup: applies this lesson's one edit, the new description, by copying src/state/SKILL.after.md
# (verified/lesson-09's) over skills/changelog-entry/SKILL.md; s18 has just shown the edit. It also
# moves an existing results/lesson-9-after aside to /Users/Shared/.demo-old.lesson-9-after.<time>.
# Nothing is deleted. Leaves the practice folder's skill as verified/lesson-09 has it.
# Vally's Saved line is shown as ~/src/demo (rewritten, nothing else); output also goes to
# /tmp/vl-l9/s19.log. The run takes about two minutes and is cut; what shows is the end of the output.
# Spend: 24 agent runs
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0009-does-the-skill-load/src/state/SKILL.after.md skills/changelog-entry/SKILL.md && { [ -e results/lesson-9-after ] && mv results/lesson-9-after "/Users/Shared/.demo-old.lesson-9-after.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l9 && : > /tmp/vl-l9/s19.log; VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee -a /tmp/vl-l9/s19.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/loading.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --runs 2 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-9-after"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 1s
Sleep 3s
