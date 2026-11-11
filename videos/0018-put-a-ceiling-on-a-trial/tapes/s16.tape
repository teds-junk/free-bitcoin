# s16: lint the eval file with the first (tight) budgets, then re-grade the haiku-high variant of the
# lesson 16 run with them. No agent starts: this tape declares no cost.
# Runs in /Users/Shared/demo/practice in place (the course's one practice folder; nothing is reset).
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (rewritten, nothing else) and appends what
# vally printed to /tmp/vl-l18/s16.log, which build-src/capture-run.py copies into src/run/.
# When input is redirected (vally grade < results.jsonl) the wrapper uses tee and not `script`, which
# would echo the input file; vally grade prints no colour and no path, so the screen is unchanged.
# Hidden setup WRITES to the demo folder: it copies this video's src/state/changelog.tight.eval.yaml over
# evals/changelog.eval.yaml (the lesson page makes this edit in an editor: three budget graders under
# each of the five stimuli). Needs exactly one run folder under results/lesson-16 (Tab completes it).
# The re-grade prints about 60 lines, so the screen scrolls: the credential scan sees one screenful and
# the recording will need the stills review.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0018-put-a-ceiling-on-a-trial/src/state/changelog.tight.eval.yaml /Users/Shared/demo/practice/evals/changelog.eval.yaml && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l18/s16.log; mkdir -p /tmp/vl-l18; : > $L; vally(){ if [ -t 0 ]; then script -q -a $L "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; else "$VB" "$@" 2>&1 | tee -a $L; fi; }`
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
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd results/lesson-16/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd haiku-high"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally grade \`
Sleep 400ms
Enter
Type `  -e ../../../../evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type "  --run-dir . < results.jsonl"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 4s
