# s15: the real run on both models, then into the saved results.
# Spend: 2 agent runs
# The output is cleared out of sight before the next command; the renderer holds it on screen
# until the sentences about it are over and it has been read ("read" in storyboard.json), so the
# Sleep before the clear stays short.
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
Type `export PS1='\W $ ' PS2='' && { [ -e /Users/Shared/demo ] && mv /Users/Shared/demo "/Users/Shared/.demo-old.$(date +%s).$$"; true; } && mkdir -p /Users/Shared/demo && cp -R /Users/ted/src/learn/vally/practice-starter /Users/Shared/demo/ && cd /Users/Shared/demo && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "cp -R practice-starter practice && cd practice && clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/one-request.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-1"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@300s /\$\s*$/
Show
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ls results/lesson-1"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd results/lesson-1/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd one-request/typo-fix"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "ls"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s

