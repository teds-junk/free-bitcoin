# s16: change into the saved lesson 22 run and re-grade its ten trials with the graders as they now are.
# Free: vally grade starts no agent, so this tape declares no cost.
# Hidden setup WRITES evals/release.eval.yaml in the demo folder: src/state/release.eval.yaml again (the
# file s15 installed), so a re-recording after s19 grades with the real pattern.
# Runs in /Users/Shared/demo/practice in place. Needs exactly ONE run folder under results/lesson-22 (the series' own lesson 22
# run): its name is not known until that run exists, so it is completed with Tab, as in lesson 3.
# vally grade reads results.jsonl from redirected input, where `script` would echo the whole file onto
# the screen, so this wrapper is a plain pipe: it shows /Users/Shared/demo as ~/src/demo and keeps a copy
# of the output in /tmp/vl-l23/s16.log. vally grade prints no colour, so nothing is lost.
# The re-grade prints about 130 lines, so the screen scrolls: the credential scan sees one screenful and
# the recording will need the stills review (redact.js --stills, secret-scan.js --reviewed).
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
Type `export PS1='\W $ ' PS2='' && mkdir -p /tmp/vl-l23 && : > /tmp/vl-l23/s16.log && cp /Users/ted/src/learn/vally/videos/0023-check-what-the-agent-did/src/state/release.eval.yaml /Users/Shared/demo/practice/evals/release.eval.yaml && cd /Users/Shared/demo/practice && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ "$VB" "$@" 2>&1 | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee -a /tmp/vl-l23/s16.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd results/lesson-22/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally grade -e ../../../evals/release.eval.yaml \`
Sleep 400ms
Enter
Type "  --run-dir . --verbose < results.jsonl"
Sleep 400ms
Enter
Wait@120s /\$\s*$/
Sleep 4s
