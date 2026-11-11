# s19: the judge over the twelve saved trials (lesson page step 6). Starts no agent.
# Runs in /Users/Shared/demo/practice in place.
# NEEDS: exactly one results/lesson-12/2026* folder (left by s12).
# Hidden setup: evals/wording.eval.yaml is set to src/state/04-judge again (a no-op after s18), so this tape
#      can be recorded alone. vally is wrapped so its output is also saved to /tmp/vl-l12/s19.log: the judge's
#      verdicts and reasons exist nowhere else, and scenes s09, s20, s21 and s22 quote them. The wrapper is a
#      plain pipe through tee, NOT the `script` wrapper of the other tapes: with input redirected from
#      results.jsonl, `script` echoes the whole file to the screen. vally grade prints no colour, so the
#      screen is what it would be unwrapped.
# The judging takes a minute or two and is cut. About 150 rows scroll past; the last screen is what stays up.
#      Because the output scrolls, the credential scan will report this recording as partly scanned:
#      look at the stills (redact.js --stills) and mark it reviewed.
# LEAVES: nothing new on disk. Afterwards: bash build-src/collect-run.sh
# Spend: 12 judge calls
#      (judge calls are charged to the Copilot plan as agent runs are, but the workspace budget counts agent
#      runs; this unit is logged and not counted against it. No agent runs.)
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0012-a-judge-for-what-code-cannot-check/src/state/04-judge.wording.eval.yaml evals/wording.eval.yaml`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l12; VB=$(type -P vally); vally(){ "$VB" "$@" 2>&1 | tee /tmp/vl-l12/s19.log | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type "cd results/lesson-12/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally grade -e ../../../evals/wording.eval.yaml \`
Sleep 400ms
Enter
Type `  --run-dir . --verbose < results.jsonl`
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 5s
