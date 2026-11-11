# s14: list this account's models with a made-up name (starts no agent, spends nothing).
# Vally prints the results folder as an absolute path; the hidden setup shows /Users/Shared/demo
# as ~/src/demo, the made-up folder this course's videos use. Nothing else about the output changes.
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
Type `export PS1='\W $ ' PS2='' && { [ -e /Users/Shared/demo ] && mv /Users/Shared/demo "/Users/Shared/.demo-old.$(date +%s).$$"; true; } && mkdir -p /Users/Shared/demo && cp -R /Users/ted/src/learn/vally/practice-starter /Users/Shared/demo/ && cd /Users/Shared/demo && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "cp -R practice-starter practice && cd practice && clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/one-request.eval.yaml \`
Sleep 400ms
Enter
Type `  --model list-my-models \`
Sleep 400ms
Enter
Type "  --output-dir results/models"
Sleep 400ms
Enter
Wait@90s /\$\s*$/
Sleep 5s
