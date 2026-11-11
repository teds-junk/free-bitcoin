# s17: run only the qwen-local variant, then the folder the run was saved in.
# Runs in /Users/Shared/demo/practice in place.
# This is a LOCAL run: five trials of qwen3.5:9b through Ollama on this computer, one at a time
# (--workers 1). It uses nothing on the Copilot account (the eval file's graders are patterns and a
# script, no judge), so this tape declares no cost. It is slow: about a quarter of an hour in the
# course's run, and up to 45 minutes if every trial runs to its nine-minute limit; the Wait allows 50.
# Needs before recording: Ollama's app running and qwen3.5:9b pulled (ollama list shows it), and nothing
# else using the model. build-src/check-state.sh checks that and the files.
# Hidden setup WRITES in the practice folder: it copies this video's src/state/cost.experiment.yaml over
# evals/cost.experiment.yaml (the same copy s16 makes, so this tape can be recorded alone), and moves an
# existing results/lesson-17 aside, to /Users/Shared/.demo-old.lesson-17.<time>, so the listing shows
# one run. Nothing is deleted. The run adds results/lesson-17/<time>/qwen-local/.
# Vally prints where it saved the run as an absolute path; it is shown as ~/src/demo (rewritten, nothing
# else). The wrapper also saves vally's output to /tmp/vl-l17/s17.log, for src/run/s17.log.
# The wait is cut. The output is longer than a screen, so the recording comes back on its end: the
# stimuli that failed, the comparison line and the table. It is cleared out of sight before the listing;
# the renderer holds it until it has been talked about and read.
# A trial that ends in ERROR (a timeout) is not what the narration describes: rerun, per the workspace note.
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
Type `export PS1='\W $ ' PS2='' V="$PWD" && cd /Users/Shared/demo/practice && cp "$V/src/state/cost.experiment.yaml" evals/cost.experiment.yaml && { [ -e results/lesson-17 ] && mv results/lesson-17 "/Users/Shared/.demo-old.lesson-17.$(date +%s)"; true; } && clear`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l17 && : > /tmp/vl-l17/s17.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l17/s17.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
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
Type `  evals/cost.experiment.yaml \`
Sleep 400ms
Enter
Type `  --variant qwen-local \`
Sleep 400ms
Enter
Type "  --workers 1 --output-dir results/lesson-17"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@3000s /\$\s*$/
Show
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "ls results/lesson-17"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
