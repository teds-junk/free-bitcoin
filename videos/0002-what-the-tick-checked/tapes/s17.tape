# s17: lint the eval file, then walk the results folder of the run the lesson 1 video recorded.
# Reads /Users/Shared/demo/practice in place and writes nothing (vally lint starts no agent), so the
# demo folder is not reset. The prompt shows only the current folder's name.
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
Type `export PS1='\W $ ' && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/one-request.eval.yaml"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 1s

Type "ls results/lesson-1"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd results/lesson-1/2026-11-11T00-11-52-424Z"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "ls"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd one-request/typo-fix"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "ls claude-haiku-4.5/0"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
