# s17: lint the release eval file once the failing stimulus is in it. Free: no agent runs.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The hidden setup is run from
# the video folder (the tape's working directory), so the copy below uses a relative src/state/ path.
# Hidden setup WRITES one file: evals/release.eval.yaml becomes src/state/release.eval.yaml, which is
# verified/lesson-24's (the page's steps 1 and 2: the stand-in tool moved into since-last-release,
# judge_model under defaults, and the tracker-down stimulus added). Run build-src/check-state.sh s17
# first: it fails if the demo's file is neither the lesson 23 file nor this one, so a series file that
# differs is not overwritten unseen.
# Vally's output is also saved to /tmp/vl-l24/s17.log (the scenes do not quote it; kept for checking).
# The page's step 3, cat of the fixture tool, is left out: a panel has walked that file.
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
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l24 && cp src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g; s|/private/var/folders/[^ \"]*/T/vally-eval-trial-[A-Za-z0-9]*|/tmp/trial|g; s|/var/folders/[^ \"]*/T/vally-eval-trial-[A-Za-z0-9]*|/tmp/trial|g' | tee /tmp/vl-l24/s17.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/release.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
