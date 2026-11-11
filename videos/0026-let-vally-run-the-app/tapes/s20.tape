# s20: plan the experiment with a dry run. Free: it starts nothing.
# Runs in /Users/Shared/demo/practice in place. Hidden setup, each step safe to repeat, so this tape can be
# recorded alone: the plugin and the plugins lines as in s16, and evals/release-app.experiment.yaml from
# this video's src/state/ (the page's step 7 creates it in an editor; the video shows it in a panel first).
# FontSize 28 so the plan's 17 lines and the command fit one screen (the credential scan sees one screenful).
# What Vally printed is also kept in /tmp/vl-l26/s20.log.
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 28
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l26 && cp src/state/vally-executor.mjs /Users/Shared/demo/practice/app/vally-executor.mjs && { grep -q '^plugins:' /Users/Shared/demo/practice/.vally.yaml || { cat src/state/plugins.yaml /Users/Shared/demo/practice/.vally.yaml > /tmp/vl-l26/vally.yaml && cp /tmp/vl-l26/vally.yaml /Users/Shared/demo/practice/.vally.yaml; }; } && cp src/state/release-app.experiment.yaml /Users/Shared/demo/practice/evals/release-app.experiment.yaml && cd /Users/Shared/demo/practice && true && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l26/s20.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally experiment run \`
Sleep 400ms
Enter
Type "  evals/release-app.experiment.yaml --dry-run"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 5s
