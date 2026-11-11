# s14: Ollama's version, then the models it has installed.
# Runs in /Users/Shared/demo/practice in place; writes nothing there. Both commands only read.
# Needs: Ollama installed and its app running (ollama list asks the local server), with qwen3.5:9b pulled.
# `ollama pull qwen3.5:9b` (the page's step 2, a 6.6 GB download) is not run: the model is already here.
# The listing shows every model installed on this computer, not only qwen3.5:9b.
# The wrapper also saves what ollama printed to /tmp/vl-l17/s14.log, for src/run/s14.log.
# No agent starts, on the Copilot account or locally.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l17 && : > /tmp/vl-l17/s14.log && clear`
Enter
Wait /\$\s*$/
Type `ollama(){ command ollama "$@" 2>&1 | tee -a /tmp/vl-l17/s14.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ollama --version"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "ollama list"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
