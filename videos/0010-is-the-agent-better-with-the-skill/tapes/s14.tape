# s14: the four variants, for real: 5 stimuli x 4 variants x 1 trial.
# Runs in /Users/Shared/demo/practice in place and adds results/lesson-10. Nothing else changes.
# Re-recording: the hidden setup moves an existing results/lesson-10 aside, to
# /Users/Shared/.demo-old.lesson-10.<time>, so s17's listing shows one run. Nothing is deleted.
# Vally's output is also saved to /tmp/vl-l10/s14.log (build-src/collect-run.sh copies it and the
# patches the video quotes into src/run/). An absolute path, if Vally prints one, shows as ~/src/demo.
# The run takes a couple of minutes and is cut. FontSize 28 because the table is 96 columns wide.
# The output is longer than the screen: the screen keeps its end, the last failure blocks and the table.
# Spend: 20 agent runs
Set Shell "bash"
Set Width 1920
Set Height 1080
Set Framerate 30
Set FontSize 28
Set FontFamily "JetBrains Mono, Menlo, monospace"
Set Padding 120
Set Theme '{"name":"solarized-essay","background":"#073642","foreground":"#b3c0bf","cursor":"#3cc0b3","selection":"#586e75","black":"#073642","red":"#f26d68","green":"#a4ba1e","yellow":"#d3a41c","blue":"#4ea5e6","magenta":"#ea6aa6","cyan":"#3cc0b3","white":"#eee8d5","brightBlack":"#8296a0","brightRed":"#f0733f","brightGreen":"#a4ba1e","brightYellow":"#d3a41c","brightBlue":"#4ea5e6","brightMagenta":"#959ae6","brightCyan":"#3cc0b3","brightWhite":"#fdf6e3"}'
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-10 ] && mv results/lesson-10 "/Users/Shared/.demo-old.lesson-10.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l10; VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l10/s14.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally experiment run \`
Sleep 400ms
Enter
Type `  evals/with-and-without.experiment.yaml \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-10"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@900s /\$\s*$/
Show
Sleep 5s
