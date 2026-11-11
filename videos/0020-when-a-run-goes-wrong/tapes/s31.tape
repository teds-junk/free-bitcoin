# s31: run the fourth broken file. EXPECTED RESULT: ERROR on both models ("Grading error; verdict is invalid."
# with "LLM judge failed: Model "claude-sonnet-5-5" is not available in Copilot" and the account's model list).
# The failed judge call is the lesson's subject: do NOT rerun this take because it ended in ERROR. Rerun only
# if the agents themselves did not finish (an ERROR with no "1/2 graders").
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset. The tape's working directory is
# the video folder, so hidden copies use relative src/state/ paths. Nothing is deleted: anything in the way
# is moved aside. Vally's Saved line is shown as ~/src/demo, and the stack trace's file:// paths as
# file:///.../node_modules/ (paths rewritten, nothing else). Vally's output is also saved to /tmp/vl-l20/.
# Hidden setup installs src/state/broken/judged.eval.yaml (judge_model with a hyphen) and moves the earlier
# runs to results/lesson-20-earlier, so this run's folder is the only one under results/lesson-20 for s34.
# FontSize 28: the failure lines are several hundred characters long.
# Judge calls: 2 attempted, both fail by design (no judge model is reached).
# Spend: 2 agent runs
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
Type `export PS1='\W $ ' PS2='' && cp src/state/broken/judged.eval.yaml /Users/Shared/demo/practice/evals/broken/judged.eval.yaml && cd /Users/Shared/demo/practice && mkdir -p results/lesson-20-earlier && for d in results/lesson-20/2026*; do [ -e "$d" ] && mv "$d" results/lesson-20-earlier/; done; true`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); mkdir -p /tmp/vl-l20; : > /tmp/vl-l20/s31.log; vally(){ if [ -t 0 ]; then script -q /dev/null "$VB" "$@"; else "$VB" "$@" 2>&1; fi | sed -l -e 's|/Users/Shared/demo|~/src/demo|g' -e 's|file:///[^ ]*/node_modules/|file:///.../node_modules/|g' | tee -a /tmp/vl-l20/s31.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/broken/judged.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type "  --workers 2 --output-dir results/lesson-20"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 5s
