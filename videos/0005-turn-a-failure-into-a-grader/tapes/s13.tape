# s13: lint the eval file once the graders are in it. Free: no agent runs.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The hidden setup is run from
# the video folder (the tape's working directory), so the copies below use relative src/state/ paths.
# Vally prints its Saved line as a path; the wrapper shows /Users/Shared/demo as ~/src/demo (nothing else).
# Hidden setup installs, from this video's src/state/ (verified/lesson-05 and lesson-04 files):
#   evals/changelog.eval.yaml              with the lesson's three graders blocks (the page's step 1)
#   skills/changelog-entry/SKILL.md        the first draft, so a re-recording after s17 starts right
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
Type `export PS1='\W $ ' PS2='' && cp src/state/changelog.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && cp src/state/SKILL.first-draft.md /Users/Shared/demo/practice/skills/changelog-entry/SKILL.md && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/changelog.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
