# s18: the full suite, once, with --require-pass; print its exit code.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Hidden setup WRITES three files into the practice folder: evals/changelog.eval.yaml (tags, budgets at their
# normal values) and .vally.yaml, as s13 does, and CONVENTIONS.md (the lesson's last step, which the page writes
# in an editor; s20 shows it in a panel). It moves an existing results/lesson-21-full aside to
# /Users/Shared/.demo-old.lesson-21-full.<time>. Nothing is deleted.
# Needs the practice folder as the lesson 20 video leaves it: conversation, loading and wording eval files, the
# skill with every rule so far, and the judge model the wording eval names.
# The run takes several minutes and is cut. Its output is longer than one screen: the recording comes back on the
# end of it (the failures list, the model summary, the table), then the exit code. Stills review needed.
# Output and exit code are saved to /tmp/vl-l21/s18.1.log and s18.1.exit.
# EXPECTED: unknown until it runs. In the course's verified run it exited 1, with one FAIL (the conversation on
# haiku) and one ERROR (a dropped session on terra). A FAIL is a real result: keep it and reword s18 to s24.
# An ERROR trial is not this lesson's subject, but the page's own run had one and uses it to tell ERROR from
# FAIL: the orchestrator decides whether to keep the take or re-record.
# Spend: 30 agent runs
# Judge calls: 6
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
Type `export PS1='\W $ ' PS2='' && cp src/state/changelog.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && cp src/state/.vally.yaml /Users/Shared/demo/practice/.vally.yaml && cp src/state/CONVENTIONS.md /Users/Shared/demo/practice/CONVENTIONS.md && cd /Users/Shared/demo/practice && { [ -e results/lesson-21-full ] && mv results/lesson-21-full "/Users/Shared/.demo-old.lesson-21-full.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l21; mkdir -p $L; N=0; vally(){ N=$((N+1)); if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@"; fi | tee $L/s18.$N.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; local e=${PIPESTATUS[0]}; echo $e > $L/s18.$N.exit; return $e; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval --suite full \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --workers 2 --require-pass \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-21-full"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@2400s /\$\s*$/
Show
Sleep 1s

Type "echo $?"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
