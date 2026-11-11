# s20: turn a saved run into a simulation block. Free: vally simulate record starts no agent.
# Runs in /Users/Shared/demo/practice in place and changes nothing there.
# The run folder's name is completed with Tab, so the tape does not need to know the time it was made:
# results/lesson-22 must hold EXACTLY ONE folder starting with 2026 (build-src/check-state.sh s20).
# It is the series' own lesson 22 run of since-last-release.
# FontSize 28: the block and its warnings are wide. The output is longer than one screen; what stays in
# view is its end (the warnings). The block itself is shown in the next scene from /tmp/vl-l24/s20.log.
# The wrapper shows /Users/Shared/demo as ~/src/demo and a trial's temporary folder as /tmp/trial.
# The recorded output is whatever the trials' shell calls printed: LOOK at the stills and the log for a
# user name or a folder of this machine before using either (the page warns of exactly this).
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 28
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l24 && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g; s|/private/var/folders/[^ \"]*/T/vally-eval-trial-[A-Za-z0-9]*|/tmp/trial|g; s|/var/folders/[^ \"]*/T/vally-eval-trial-[A-Za-z0-9]*|/tmp/trial|g' | tee /tmp/vl-l24/s20.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally simulate record \`
Sleep 400ms
Enter
Type "  results/lesson-22/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 5s
