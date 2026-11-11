# s13: with the flawed pattern in the eval file, ask the oracle about the typo-fix stimulus, twice.
# Runs in /Users/Shared/demo/practice in place. No agent starts: vally grade and vally oracle are free,
# so this tape declares no cost. The practice folder must already hold the series' own lesson 5
# "before" run (exactly one folder under results/lesson-5-before) and the lesson 7 golden patches.
# The vally wrapper shows /Users/Shared/demo as ~/src/demo (rewritten, nothing else). It is skipped
# when input is redirected (vally grade < results.jsonl), where `script` would echo the input file;
# the verified run's re-grade output contains no path.
# Hidden setup WRITES to the demo folder: it copies this video's src/state/changelog.flawed.eval.yaml
# over evals/changelog.eval.yaml (the lesson page makes this edit in a text editor: four characters,
# (?m), deleted from the no-made-up-number pattern). s16 puts the correct file back.
# It then changes into the run's folder, where s10 left the terminal, so the page's `cd ../../..` is true.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0008-check-graders-against-saved-trials/src/state/changelog.flawed.eval.yaml evals/changelog.eval.yaml && cd results/lesson-5-before/2026* && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ if [ -t 0 ]; then script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; else "$VB" "$@"; fi; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd ../../.."
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally oracle -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type "  --stimulus typo-fix --verbose"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally oracle -e evals/changelog.eval.yaml \`
Sleep 400ms
Enter
Type "  --stimulus typo-fix --no-golden-input --verbose"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 4s
