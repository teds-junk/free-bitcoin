# s15: copy the judge's eval file, put the judge on a scale (out of sight), lint the copy.
# Runs in /Users/Shared/demo/practice in place. No agent starts in this lesson.
# The vally wrapper keeps vally on a terminal, shows /Users/Shared/demo as ~/src/demo (rewritten, nothing
# else) and saves what vally printed to /tmp/vl-l14/<scene>-<subcommand>.log (a raw typescript). When
# input is redirected (vally grade < results.jsonl) the file is handed to vally on its input while
# `script` keeps the terminal, so the input file is not echoed and the colours stay.
# Hidden setup: an existing evals/wording-scaled.eval.yaml is moved aside to
# /Users/Shared/.demo-old.wording-scaled.<time>.yaml, never deleted, so the visible cp creates the file.
# The lesson has the reader edit the copy in a text editor (name: wording-scaled; scale_1_5 and
# threshold 0.75 in each of the three judges); the tape copies this video's
# src/state/wording-scaled.eval.yaml over it out of sight, then clears. The renderer holds the cp on
# screen until the sentence about the edit has ended.
# Free: vally lint starts nothing. No agent runs, no judge calls.
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
Type `export PS1='\W $ ' PS2='' VS=s15 && cd /Users/Shared/demo/practice && { [ -e evals/wording-scaled.eval.yaml ] && mv evals/wording-scaled.eval.yaml "/Users/Shared/.demo-old.wording-scaled.$(date +%s).yaml"; true; } && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); L=/tmp/vl-l14; mkdir -p $L; vally(){ local o=$L/$VS-$1.log; if [ -t 0 ]; then script -q $o "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; else script -q $o bash -c 'exec "$0" "$@" <&3' "$VB" "$@" 3<&0 </dev/tty | sed -l 's|/Users/Shared/demo|~/src/demo|g'; fi; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `cp evals/wording.eval.yaml \`
Sleep 400ms
Enter
Type "  evals/wording-scaled.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Hide
Type "cp /Users/ted/src/learn/vally/videos/0014-partial-credit/src/state/wording-scaled.eval.yaml evals/wording-scaled.eval.yaml && clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "vally lint -e evals/wording-scaled.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
