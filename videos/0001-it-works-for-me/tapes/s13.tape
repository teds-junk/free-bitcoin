# s13: check the tools and make the practice folder.
# The demo folder is /Users/Shared/demo: a short, generic, real folder (the prompt shows only the
# current folder's name). Each of s13-s15 starts it fresh and moves the old one aside, and s16
# reads the results s15 leaves there, so record them in order: s13, s14, s15, s16.
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
Show
Sleep 500ms

Type "node --version"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "vally --version"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cp -R practice-starter practice"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd practice"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s

