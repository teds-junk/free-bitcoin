# s14: keep one workspace (one-request eval file, one model), then list every file in it.
# Runs in /Users/Shared/demo/practice in place. Needs: the practice folder as the lesson 5 video left it
# (skill with three added rules). Leaves: a folder named kept (kept/main/typo-fix/...) and
# results/lesson-6-look/<time>. Changes no eval or skill file.
# Re-recording: the hidden setup moves an existing kept and results/lesson-6-look aside, to
# /Users/Shared/.demo-old.lesson-6.<name>.<time>. Nothing is deleted.
# Any absolute path Vally prints is shown as ~/src/demo (rewritten, nothing else).
# The run is cut. Its summary stays on screen above the listing.
# Spend: 1 agent run
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e kept ] && mv kept "/Users/Shared/.demo-old.lesson-6.kept.$(date +%s)"; true; } && { [ -e results/lesson-6-look ] && mv results/lesson-6-look "/Users/Shared/.demo-old.lesson-6.results-lesson-6-look.$(date +%s)"; true; } && clear`
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

Type `vally eval -e evals/one-request.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5 \`
Sleep 400ms
Enter
Type `  --workspace kept \`
Sleep 400ms
Enter
Type "  --output-dir results/lesson-6-look"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 1s

Type "find kept -type f"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
