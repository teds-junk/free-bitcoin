# s13: keep a copy of the skill, put the new rule into the skill (out of sight), then check the plan with a dry run.
# Runs in /Users/Shared/demo/practice in place; the demo folder is NOT reset.
# Needs: the practice folder as lesson 14 leaves it. evals/before-and-after.experiment.yaml (from the starter)
# and evals/wording.eval.yaml (lesson 12) are used as they are; build-src/check-state.sh checks them.
# Hidden setup, so the tape can be recorded again:
#   - an existing skills/changelog-entry-before is moved aside to /Users/Shared/.demo-old.lesson-15.before.<time>
#     (cp -R into an existing folder would nest the copy). Nothing is deleted.
#   - skills/changelog-entry/SKILL.md is set to src/state/SKILL.before.md (the skill as lesson 14 leaves it), so the
#     copy the viewer watches is the skill before the edit even on a re-record.
# Between the two visible commands, out of sight: src/state/SKILL.md (the sharpened second rule) is copied over
# skills/changelog-entry/SKILL.md, and the screen is cleared. The lesson page makes this edit in an editor.
# Vally's output is also saved to /tmp/vl-l15/s13.log. Any absolute path is shown as ~/src/demo (rewritten).
# The dry run starts no agent. No spend.
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
Type `export PS1='\W $ ' PS2='' && cd /Users/Shared/demo/practice && mkdir -p /tmp/vl-l15 && clear`
Enter
Wait /\$\s*$/
Type `{ [ -e skills/changelog-entry-before ] && mv skills/changelog-entry-before "/Users/Shared/.demo-old.lesson-15.before.$(date +%s)"; true; } && cp /Users/ted/src/learn/vally/videos/0015-is-the-change-real/src/state/SKILL.before.md skills/changelog-entry/SKILL.md && clear`
Enter
Wait /\$\s*$/
Type `VB=$(type -P vally); vally(){ script -q /dev/null "$VB" "$@" | sed -l 's|/Users/Shared/demo|~/src/demo|g' | tee /tmp/vl-l15/s13.log; }`
Enter
Wait /\$\s*$/
Type "clear"
Enter
Wait /\$\s*$/
Show
Sleep 500ms

Type `cp -R skills/changelog-entry \`
Sleep 400ms
Enter
Type "  skills/changelog-entry-before"
Sleep 400ms
Enter
Wait /\$\s*$/
Sleep 1s

Hide
Type `cp /Users/ted/src/learn/vally/videos/0015-is-the-change-real/src/state/SKILL.md skills/changelog-entry/SKILL.md && clear`
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
Type "  evals/before-and-after.experiment.yaml --dry-run"
Sleep 400ms
Enter
Wait@60s /\$\s*$/
Sleep 5s
