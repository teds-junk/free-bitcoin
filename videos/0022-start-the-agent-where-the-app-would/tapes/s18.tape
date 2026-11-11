# s18: one passing trial's patch, for comparison. Free: no agent runs.
# Starts where s17 ended: the hidden setup changes into the one run folder under results/lesson-22 and its
# stimulus folder. Changes nothing. The patch printed is gpt-5.6-terra folder 0, the page's example: it
# must be a PASSING trial (build-src/check-state.sh s18 checks). If folder 0 failed in our run, change the
# 0 below to a passing folder and SHOWN in make-scenes.py.
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 30
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice/results/lesson-22/2026*/release/since-last-release && clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cat gpt-5.6-terra/0/workspace.patch"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 5s
