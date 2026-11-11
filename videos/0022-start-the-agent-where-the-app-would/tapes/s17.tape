# s17: into the saved run, then one failing trial's patch. Free: no agent runs.
# Runs in /Users/Shared/demo/practice in place and changes nothing. Needs exactly one run folder under
# results/lesson-22 (Tab completes its name). The patch printed is claude-haiku-4.5 folder 1, the page's
# example: it must be a FAILING trial that recorded the refactor (build-src/check-state.sh s17 checks).
# If folder 1 passed in our run, change the 1 below to a failing folder and SHOWN in make-scenes.py.
# FontSize 25 so the whole patch (20 lines in our run) and its command fit on one screen (24 rows).
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 25
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ls results/lesson-22"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd results/lesson-22/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd release/since-last-release"
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

Type "cat claude-haiku-4.5/1/workspace.patch"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 5s
