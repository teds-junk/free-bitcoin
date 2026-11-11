# s19: the same re-grade, with never-commits forbidding a command one saved trial did run.
# Free: vally grade starts no agent, so this tape declares no cost.
# Runs in /Users/Shared/demo/practice in place. Hidden setup WRITES evals/release.eval.yaml there: this video's
# src/state/release.swap.eval.yaml, in which never-commits' command pattern is the word in
# src/run/swap-command.txt instead of git (commit|push) (the page's step 5, done there in an editor and
# shown here in s18's panel). The shell then starts inside the one run folder under results/lesson-22.
# LEAVES the swapped pattern in the demo folder's eval file. s21's hidden setup (and s15's and s16's)
# installs src/state/release.eval.yaml again, so record s21 straight after this tape.
# A FAILING never-commits line is EXPECTED here: it is the point of the scene.
# Wrapper as in s16 (plain pipe; copy of the output in /tmp/vl-l23/s19.log). About 130 lines scroll by,
# so the recording will need the stills review.
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
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l23 && : > /tmp/vl-l23/s19.log && cp /Users/ted/src/learn/vally/videos/0023-check-what-the-agent-did/src/state/release.swap.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cd /Users/Shared/demo/practice/results/lesson-22/2026*/ && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ "$VB" "$@" 2>&1 | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee -a /tmp/vl-l23/s19.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally grade -e ../../../evals/release.eval.yaml \`
Sleep 400ms
Enter
Type "  --run-dir . --verbose < results.jsonl"
Sleep 400ms
Enter
Wait@120s /\$\s*$/
Sleep 4s
