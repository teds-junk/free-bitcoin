# s18: back to the practice folder, then lint on the eval file with the judge added (lesson page steps 4 and 5).
#      Free: lint starts no agent and calls no judge.
# Runs in /Users/Shared/demo/practice in place.
# NEEDS: exactly one results/lesson-12/2026* folder (left by s12).
# Hidden setup: evals/wording.eval.yaml becomes src/state/04-judge (the page's step 4, done in an editor and
#      shown in scene s17: judge_model under defaults, and a rubric and a prompt grader in each stimulus).
#      The shell then starts in the run's wording folder, where s13 left off, so the visible cd is the page's.
#      vally is wrapped as in s12; its output is also saved to /tmp/vl-l12/s18.log.
# LEAVES: evals/wording.eval.yaml with the judge (identical to verified/lesson-12).
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0012-a-judge-for-what-code-cannot-check/src/state/04-judge.wording.eval.yaml evals/wording.eval.yaml && cd results/lesson-12/2026*/wording`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l12 && : > /tmp/vl-l12/s18.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l12/s18.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `cd ../../../..`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally lint -e evals/wording.eval.yaml`
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 4s
