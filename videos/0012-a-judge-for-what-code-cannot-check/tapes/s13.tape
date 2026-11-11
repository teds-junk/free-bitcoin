# s13: into the run's folder and the eval's folder, the three stimulus folders, and the first patch
#      (lesson page steps 2 and 3). Free: no agent run, no judge.
# Runs in /Users/Shared/demo/practice in place and changes nothing.
# NEEDS: exactly one folder under results/lesson-12 whose name starts 2026 (left by s12), so Tab completes it.
# The run folder's name is not known when this tape is written; the page prints it literally, and here
#      it is completed with Tab, as in lesson 3's video.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd results/lesson-12/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `cd wording`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `ls`
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

Type `cat parser/claude-haiku-4.5/0/workspace.patch`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
