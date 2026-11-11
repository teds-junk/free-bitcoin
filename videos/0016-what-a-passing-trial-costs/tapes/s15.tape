# s15: the free check of which reasoning efforts each model accepts.
# Runs in /Users/Shared/demo/practice in place. It asks three models for an effort named "list", which
# no model has: Vally rejects it before any session starts, so every trial ends in ERROR and nothing
# is spent. That ERROR is the plan, not a failed take: do not rerun because of it.
# Re-recording: the hidden setup moves an existing results/lesson-16-efforts aside, to
# /Users/Shared/.demo-old.lesson-16-efforts.<time>. Nothing is deleted.
# Vally prints its Saved line as an absolute path; it is shown as ~/src/demo (rewritten, nothing else).
# What vally prints is also saved to /tmp/vl-l16/s15.log: copy it over src/run/s15.log afterwards.
# The output is longer than one screen (about 45 rows at this size); the recording ends on its tail,
# and scene s16 shows what it said as a table.
# Spend: none
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-16-efforts ] && mv results/lesson-16-efforts "/Users/Shared/.demo-old.lesson-16-efforts.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l16 && : > /tmp/vl-l16/s15.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l16/s15.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/one-request.eval.yaml \`
Sleep 400ms
Enter
Type `  --model \`
Sleep 400ms
Enter
Type `  claude-haiku-4.5,claude-haiku-5.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --reasoning-effort list \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-16-efforts"
Sleep 400ms
Enter
Wait@120s /\$\s*$/
Sleep 5s
