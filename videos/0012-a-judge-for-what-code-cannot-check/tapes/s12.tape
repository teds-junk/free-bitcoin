# s12: two trials of each wording stimulus on each model, then the folder the run was saved in
#      (lesson page step 1, and the listing step 2 asks for).
# Runs in /Users/Shared/demo/practice in place. Nothing is deleted.
# NEEDS: the practice folder as lesson 11's video left it (skills/changelog-entry/SKILL.md with lesson 11's rule).
# Hidden setup: an existing results/lesson-12 is moved aside to /Users/Shared/.demo-old.lesson-12.<time>, so the
#      listing shows one run; evals/wording.eval.yaml is set to src/state/00-start (the file as it ships, with
#      no judge; build-src/check-state.sh says beforehand whether that changes anything). vally is wrapped so
#      that the absolute path on its Saved line shows as ~/src/demo (rewritten, nothing else), and its output
#      is also saved to /tmp/vl-l12/s12.log.
# The run takes about a minute and is cut. Its output is cleared out of sight before the listing; the
#      renderer holds it until it has been talked about and read.
# LEAVES: results/lesson-12/<time>/ with twelve trials.
# Spend: 12 agent runs
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && { [ -e results/lesson-12 ] && mv results/lesson-12 "/Users/Shared/.demo-old.lesson-12.$(date +%s)"; true; } && cp /Users/ted/src/learn/vally/videos/0012-a-judge-for-what-code-cannot-check/src/state/00-start.wording.eval.yaml evals/wording.eval.yaml`
Enter
Wait /\$\s*$/
Type `mkdir -p /tmp/vl-l12 && : > /tmp/vl-l12/s12.log; VB=$(type -P vally); vally(){ script -a -q /tmp/vl-l12/s12.log "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g'; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `vally eval -e evals/wording.eval.yaml \`
Sleep 400ms
Enter
Type `  --model claude-haiku-4.5,gpt-5.6-terra \`
Sleep 400ms
Enter
Type `  --runs 2 --workers 2 \`
Sleep 400ms
Enter
Type `  --output-dir results/lesson-12`
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@600s /\$\s*$/
Show
Sleep 1s

Hide
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `ls results/lesson-12`
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 4s
