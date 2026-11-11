# s17: run the release app once, outside Vally. It starts ONE agent session through the Copilot SDK
# (model claude-haiku-4.5), about 2 to 4 AIU. Recorded alone.
# Runs in /Users/Shared/demo/practice in place and needs app/node_modules (s16). The script itself does
# `rm -rf app-run`; hidden setup first moves an existing app-run aside to
# /Users/Shared/.demo-old.lesson-25.app-run.<time>, so nothing is deleted.
# `sh` is wrapped so the script's output passes through a rewrite that shows /Users/Shared/demo as
# ~/src/demo (nothing else) and is saved to /tmp/vl-l25/s17.log. The script prints the agent's reply
# and one line naming the two files it wrote, as relative paths. The run takes some seconds and is cut.
# An ERROR here (the session fails, or no "Wrote ..." line) is NOT expected: rerun.
# Leaves app-run/ (repo, before, skills, traces.jsonl, change.diff). traces.jsonl holds the whole
# prompt, full paths and an account id: it is never printed here; the scenes show a cleaned copy.
# Spend: 1 agent run
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l25 && { [ -e app-run ] && mv app-run "/Users/Shared/.demo-old.lesson-25.app-run.$(date +%s)"; true; }`
Enter
Wait /\$\s*$/
Type `sh(){ command sh "$@" 2>&1 | sed -l 's|/private/Users/Shared/demo|~/src/demo|g; s|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l25/s17.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `sh app/run.sh claude-haiku-4.5`
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@300s /\$\s*$/
Show
Sleep 5s
