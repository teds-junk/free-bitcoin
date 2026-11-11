# s13: into the before-and-after experiment's folder, and what it holds (lesson page step 1).
# Runs in /Users/Shared/demo/practice in place. Free: no agent run, no judge call.
# NEEDS: exactly one folder named 2026* under results/lesson-15 (the series' own lesson 15 experiment),
#        so that Tab completes its name. build-src/check-state.sh s13 checks this.
# Hidden setup: sets the prompt, and moves a haiku-compare.jsonl or terra-compare.jsonl left in that
#        folder by an earlier recording aside, to /Users/Shared/.demo-old.l19.<name>.<time>, so the
#        listing is the one the page prints. Nothing is deleted.
# LEAVES: nothing changed.
# Judge calls: 0
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 30
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && for f in results/lesson-15/2026*/haiku-compare.jsonl results/lesson-15/2026*/terra-compare.jsonl; do if [ -e "$f" ]; then mv "$f" "/Users/Shared/.demo-old.l19.$(basename "$f").$(date +%s)"; fi; done; clear`
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd results/lesson-15/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "ls"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
