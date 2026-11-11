# s19: add the scoring block (out of sight), lint, re-grade the same twelve trials; then put the file back.
# Runs in /Users/Shared/demo/practice in place. No agent starts in this lesson.
# The vally wrapper keeps vally on a terminal, shows /Users/Shared/demo as ~/src/demo (rewritten, nothing
# else) and saves what vally printed to /tmp/vl-l14/<scene>-<subcommand>.log (a raw typescript). When
# input is redirected (vally grade < results.jsonl) the file is handed to vally on its input while
# `script` keeps the terminal, so the input file is not echoed and the colours stay.
# Needs exactly one run folder under results/lesson-12, as s16 does.
# Hidden setup: copies this video's src/state/wording-scaled.scoring.eval.yaml (the scaled copy with the
# scoring block at its end: weights prompt 0.5, diff-contains 0.5, threshold 0.6) over
# evals/wording-scaled.eval.yaml. The lesson has the reader add the block in a text editor.
# Hidden at the end (the lesson's last step, also done in an editor): the scoring block is taken out
# again by copying src/state/wording-scaled.eval.yaml back, and src/state/notes/wording-labels.md
# (the labels file with its "1 to 5" column and one sentence; written by build-src/make-scenes.py from
# the s16 re-grade) is copied to notes/wording-labels.md. That leaves the practice folder as
# verified/lesson-14 has it. Run make-scenes.py after s16 is recorded and before this tape is.
# The output scrolls: expect the stills review, as for s16.
# No agent runs. Judge calls: 12 (the budget counts agent runs; these are extra).
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
Type `export PS1='\W $ ' PS2='' VS=s19 && cd /Users/Shared/demo/practice && cp /Users/ted/src/learn/vally/videos/0014-partial-credit/src/state/wording-scaled.scoring.eval.yaml evals/wording-scaled.eval.yaml && clear`
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

Type "vally lint -e evals/wording-scaled.eval.yaml"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type "cd results/lesson-12/2026"
Sleep 300ms
Tab
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Type `vally grade \`
Sleep 400ms
Enter
Type `  -e ../../../evals/wording-scaled.eval.yaml \`
Sleep 400ms
Enter
Type "  --run-dir . --verbose < results.jsonl"
Sleep 400ms
Enter
Sleep 2s
Hide
Wait@300s /\$\s*$/
Show
Sleep 4s

Hide
Type "cd ../../.. && cp /Users/ted/src/learn/vally/videos/0014-partial-credit/src/state/wording-scaled.eval.yaml evals/wording-scaled.eval.yaml && mkdir -p notes && cp /Users/ted/src/learn/vally/videos/0014-partial-credit/src/state/notes/wording-labels.md notes/wording-labels.md && clear"
Enter
Wait /\$\s*$/
