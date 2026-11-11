# s17: into the run s16 recorded, then read one failing trial's patch.
# Reads /Users/Shared/demo/practice in place and writes nothing. The run's folder is named with a time
# that is not known until s16 has run, so its name is completed with Tab (one run is there).
# WHICH PATCH is shown depends on s16's result: this types the after-release trial of gpt-5.6-terra,
# which failed in the lesson page's run. Change the cat line to a trial that failed in our run.
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

Type "cd results/lesson-6/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd changelog"
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

Type "cat after-release/gpt-5.6-terra/0/workspace.patch"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
