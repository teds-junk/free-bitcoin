# s15: into the run s14 recorded, and read the diff of the turn that failed.
# Reads /Users/Shared/demo/practice in place and writes nothing. The run's folder is named with a
# time that is not known until s14 has run, so its name is completed with Tab (one run is there).
# Filled in after s14 (take 2, run 2026-11-11T06-35-45-792Z): the terminal's "trial 2" is trial-1.
# The placeholder stood for <model>__trial-N__turn-2 of a trial that failed third-no-made-up-number
# in this video's own s14 run; the page's is haiku-4.5__trial-1__turn-2. Fill it in after s14 is
# recorded and before this tape is; the narration of s15 names "trial one, turn two".
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

Type "ls results/lesson-11"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd results/lesson-11/2026"
Sleep 300ms
Tab
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

Type "cat diffs/*haiku-4.5__trial-1__turn-2.diff"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
