# s15: the release tool run by hand, then lint on the new eval file. Free: no agent runs.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The hidden setup is run from
# the video folder (the tape's working directory), so the copies below use relative src/state/ paths.
# Hidden setup installs the lesson's two new files, from this video's src/state/ (verified/lesson-22):
#   evals/release.eval.yaml             the page's steps 3 (the eval file)
#   evals/grading/check-release.mjs     the page's step 2 (the hidden test)
# Both are shown in panels (s07, s11, s12) before this scene. Nothing else in the practice folder changes.
# vally's output is also saved to /tmp/vl-l22/s15.log; /Users/Shared/demo is shown as ~/src/demo.
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
Type `export PS1='\W $ ' PS2='' && cp src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cp src/state/check-release.mjs /Users/Shared/demo/practice/evals/grading/check-release.mjs && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l22; VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l22/s15.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "node tools/list-merged.mjs"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "vally lint -e evals/release.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
