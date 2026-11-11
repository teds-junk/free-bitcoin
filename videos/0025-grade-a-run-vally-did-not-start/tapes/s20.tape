# s20: convert the app's traces to an ATIF file. Free: no agent, no network.
# Runs in /Users/Shared/demo/practice in place; needs app-run/traces.jsonl (s17). Writes
# app-run/trajectory.json. The command prints nothing.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l25`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `node app/traces-to-atif.mjs app-run/traces.jsonl \`
Sleep 400ms
Enter
Type `  > app-run/trajectory.json`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
