# s13: into the run's folder, list the stimulus folders, read the first patch.
# Runs in /Users/Shared/demo/practice in place, after s12 has recorded results/lesson-4 (one run folder there).
# Hidden setup: the lesson has the reader create notes/failures.md in a text editor; the tape copies this
# video's src/state/notes/failures.md to practice/notes/failures.md out of sight (the only file the lesson
# adds to the practice folder). Nothing else is written.
# The run folder's name is completed with Tab, so the tape does not need to know the time it was made.
# The listing is cleared out of sight before the patch; the renderer holds it until it has been read.
# No spend: no agent starts.
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
Type `export PS1='\W $ ' && cd /Users/Shared/demo/practice && mkdir -p notes && cp /Users/ted/src/learn/vally/videos/0004-read-the-runs-first/src/state/notes/failures.md notes/failures.md && clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd results/lesson-4/2026"
Sleep 300ms
Tab
Sleep 400ms
Type "six"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "ls"
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

Type "cat refactor/claude-haiku-4.5/0/workspace.patch"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
