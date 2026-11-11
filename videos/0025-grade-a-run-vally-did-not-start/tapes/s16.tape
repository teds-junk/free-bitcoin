# s16: install the app's two libraries. Free: it starts no agent, but it downloads about 140 packages
# from npm into /Users/Shared/demo/practice/app/node_modules (a network read; nothing is published).
# Runs in /Users/Shared/demo/practice in place. Hidden setup moves an existing app/node_modules aside to
# /Users/Shared/.demo-old.lesson-25.node_modules.<time>, so npm prints "added N packages" and not
# "up to date". Nothing is deleted.
# npm's output is passed through a rewrite that shows /Users/Shared/demo as ~/src/demo (nothing else),
# and is also saved to /tmp/vl-l25/s16.log. Without a terminal npm prints its plain summary, which is
# what the lesson page shows.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l25 && { [ -e app/node_modules ] && mv app/node_modules "/Users/Shared/.demo-old.lesson-25.node_modules.$(date +%s)"; true; }`
Enter
Wait /\$\s*$/
Type `npm(){ command npm "$@" 2>&1 | sed -l 's|/private/Users/Shared/demo|~/src/demo|g; s|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l25/s16.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `npm install --prefix app`
Sleep 400ms
Enter
Wait@180s /\$\s*$/
Sleep 4s
