# s16: read the two saved patches from the s15 recording's run, then climb back to practice.
# Each patch is cleared out of sight before the next; the renderer holds it until it has been read.
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
Type `export PS1='\W $ ' && cd /Users/Shared/demo/practice/results/lesson-1/*/one-request/typo-fix && clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cat claude-haiku-4.5/0/workspace.patch"
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

Type "cat gpt-5.6-terra/0/workspace.patch"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd ../../../../.."
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s

