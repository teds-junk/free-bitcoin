# s14: lint the conversation eval file, then run it three times on each model.
# Runs in /Users/Shared/demo/practice in place. Hidden setup:
#   - moves an existing results/lesson-11 aside to /Users/Shared/.demo-old.lesson-11.<time> (nothing is deleted),
#   - installs the eval file with its five graders from this video's src/state/ (the page's step 2;
#     s10 and s11 have shown the graders in a file panel),
#   - starts an empty log at /tmp/vl-l11/s14.log; the vally wrapper copies everything vally prints
#     into it (lint first, then the run), for src/run/lint.log and src/run/before.log.
# Needs: skills/changelog-entry/SKILL.md WITHOUT the "Treat every request on its own" rule
#        (build-src/check-state.sh s14 checks this).
# Vally prints its Saved line as an absolute path; it is shown as ~/src/demo (rewritten, nothing else).
# The run takes about a minute and is cut.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-11 ] && mv results/lesson-11 "/Users/Shared/.demo-old.lesson-11.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l11 && : > /tmp/vl-l11/s14.log && cp /Users/ted/src/learn/vally/videos/0011-follow-up-requests/src/state/conversation.eval.yaml evals/conversation.eval.yaml && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | tee -a /tmp/vl-l11/s14.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/conversation.eval.yaml"
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

Type `vally eval -e evals/conversation.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --runs 3 --workers 2 \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-11"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 5s
