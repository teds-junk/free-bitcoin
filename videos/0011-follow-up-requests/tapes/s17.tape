# s17: the same conversations again, with the new rule in the skill.
# Runs in /Users/Shared/demo/practice in place. Hidden setup:
#   - moves an existing results/lesson-11-after aside to /Users/Shared/.demo-old.lesson-11-after.<time>,
#   - installs SKILL.md with the rule added at its end from this video's src/state/ (the page's
#     step 6; s16 has shown the rule in a file panel),
#   - starts an empty log at /tmp/vl-l11/s17.log for src/run/after.log.
# Needs: the eval file with its five graders, as s14 left it.
# Leaves: the practice folder's conversation eval file and skill as verified/lesson-11 has them.
# Spend: 6 agent runs
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-11-after ] && mv results/lesson-11-after "/Users/Shared/.demo-old.lesson-11-after.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l11 && : > /tmp/vl-l11/s17.log && cp /Users/ted/src/learn/vally/videos/0011-follow-up-requests/src/state/SKILL.md skills/changelog-entry/SKILL.md && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | tee -a /tmp/vl-l11/s17.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/conversation.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --runs 3 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-11-after"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 5s
