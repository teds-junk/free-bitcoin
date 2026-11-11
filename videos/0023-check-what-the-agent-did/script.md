# Check what the agent did — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0023-check-what-the-agent-did.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** How do I check the steps the agent took, not just the file it changed?  
**The viewer starts:** A professional programmer who knows the shell, YAML, regular expressions and git, and has watched the changelog-entry skill measured and improved on two models (claude-haiku-4.5 and gpt-5.6-terra) in the practice folder. Knows skill, agent, eval, eval file, stimulus, grader, trial, workspace and patch; that a trial's trajectory, its record of what the agent did, is saved in the run's results.jsonl, one trial per line; that a loaded skill is recorded there and read by the skill-invocation grader, and shown in the report's Skills column; the agent environment and the grading environment; that every grader on a stimulus must pass unless a scoring block says otherwise, and that vally lint prints a scoring warning to say so; vally oracle with --no-golden-input, which grades the untouched workspace (the baseline), where a grader that requires something should fail and a grader that only checks for absence is marked N/A; vally grade, which applies the eval file's current graders to saved trials without starting an agent, with --run-dir and --verbose, and which cannot re-run a grader that needs the finished workspace; that a grader which checks for absence is tested on a saved trial known to be bad; vally eval with -e, --model, --runs, --workers and --output-dir; time limits that stop an agent. Has just seen the release stimulus: the notes-cli team's release tool writes the list of merged changes to release/merged.txt with a setup command, asks the agent for the Unreleased entries, and a hidden test named every-change-handled checks the finished changelog against that list. Ten trials of it are saved, five on each model; the skill says a refactor gets no entry. Has not seen a tool call event, the tool-calls grader, or a loop check.

1. **when-it-matters**: after this, the viewer can say when a step the agent took is worth grading: when the app requires it, forbids it, or the route is too long
2. **tool-calls**: after this, the viewer can read a tool-calls grader and predict which trials it passes
3. **loops**: after this, the viewer can say what the loop check counts, and when it fails
4. **test-then-run**: after this, the viewer can test route graders on the baseline and on saved trials, show that a forbidding grader can fail, and then run them
5. **what-it-showed**: after this, the viewer can add graders that require a step and forbid another, with a loop check, each tested against saved trials, and say what the route showed about each model

## s01 — Check the route

**Role:** hook · **Mode:** think · **Stage:** when-it-matters  
**On screen:** Headline 'Check what the agent did' in the display serif. Three blocks in a row, no arrows: 'CHANGELOG.md · what the hidden test sees', 'Did the entries come from the list?', 'Did the agent commit or push?'. The first fills as the changelog is named, then the second and third as each question is asked; all rest for the promise.  
**Renderer:** html (scenes/s01.html)

> Inside the release tool, nobody watches the agent work.
> The team cares about the changelog, and also about two things the changelog can't show.
> The entries have to come from the list the tool wrote, and not from guesses that happen to be right.
> And the agent must never commit or push: the release tool does that itself, after a person has checked the result.
> Our hidden test only sees the finished file.
> Here, you'll add graders that check the steps the agent took, and test each one before it runs.

## s02 — When a step is worth grading

**Role:** body · **Mode:** think · **Stage:** when-it-matters  
**On screen:** Eyebrow 'When the route matters'. Headline 'Grade the outcome by default'. Two blocks side by side: 'The outcome · what the agent left behind · the default' and 'The route · the steps it took · only where the app depends on one'. The first fills, then the second. A source note: Anthropic, Demystifying evals for AI agents (2026).  
**Renderer:** html (scenes/s02.html)

> Let's start with when a step is worth grading at all.
> The default is to grade the outcome.
> Agents find valid routes nobody planned for, and a grader that insists on one sequence of steps fails good work.
> An agent that opens a file with one tool instead of another has still opened it.
> So we check the route only when the app depends on it, and then only the step it depends on.

## s03

**Role:** body · **Mode:** think · **Stage:** when-it-matters  
**On screen:** Headline 'Required, forbidden, or too long'. Three blocks in a row, no arrows: 'Required · the agent works from the list', 'Forbidden · a commit, a push, a deleted file', 'Too long · the same call, again and again'. Each fills as it is named.  
**Renderer:** html (scenes/s03.html)

> Sometimes a step is required: the app relies on the agent working from the list, because an entry written from the file names would be right only by luck.
> A step can be forbidden: a commit, a push, a deleted file, anything with effects outside the workspace.
> A commit made by the agent can't be undone by throwing the workspace away.
> And a route can be too long: an agent that repeats the same call costs money and time, even when it gets there.

## s04

**Role:** body · **Mode:** think · **Stage:** when-it-matters  
**On screen:** Headline 'As loose as the requirement'. Two blocks side by side: 'The requirement · open release/merged.txt' and 'One way to meet it · one particular tool'. The first fills, then the second.  
**Renderer:** html (scenes/s04.html)

> Even a route grader should be as loose as the requirement.
> Opening the merged list is the requirement.
> Using one particular tool on it is one way to meet that requirement, and not the only one.
> That difference shapes the first grader we'll write.

## s05 — Read a tool-calls grader

**Role:** body · **Mode:** works · **Stage:** tool-calls · **Introduces:** results.jsonl, results.jsonl · one event of one trial  
**On screen:** Eyebrow 'The tool-calls grader'. Headline 'Every tool use is recorded'. File panel labelled 'results.jsonl · one event of one trial', with a minimap: one tool_call event, spread over its lines. Notes on the right, level with their lines: 'the tool's name' beside toolName, 'what the tool was given' beside the path. A note under it says the workspace's real location is shown as <workspace>.  
**Renderer:** html (scenes/s05.html)

> That's when to check a step; now for where the steps are recorded.
> Every time the agent uses a tool, the trial's trajectory, its record of what the agent did, gains a tool call event.
> Here's one from the saved run, spread out over several lines: an agent opening the merged list.  _(depends on what the demo produced)_
> Tool name is the tool's name; the agent's runtime decides the names.
> Arguments hold what the tool was given: a file tool gets a path, and bash gets a command.

## s06

**Role:** body · **Mode:** works · **Stage:** tool-calls · **Introduces:** eval-results.md  
**On screen:** Headline 'The report counts them'. Left: a card labelled 'eval-results.md · Tool Calls · claude-haiku-4.5' with a dark box holding that cell of the report. Right: a table, 'Tool' and 'What it does': view, edit, apply_patch, bash, skill. The card lights, then each table row as its tool is named.  
**Renderer:** html (scenes/s06.html)

> You don't need to open that file to learn the names.
> The report has a Tool Calls column, which totals them for each stimulus.
> For haiku's five saved trials, it counted eighteen views, five edits, three skill calls, and two bash calls.  _(depends on what the demo produced)_
> View opens a file, edit and apply patch change one, bash runs a shell command, and skill loads a skill.

## s07

**Role:** body · **Mode:** works · **Stage:** tool-calls · **Introduces:** release.eval.yaml, evals/release.eval.yaml  
**On screen:** Headline 'Required: one call must match'. File panel labelled 'evals/release.eval.yaml' with a minimap, opened on the first new grader (lines 33 to 38). Notes on the right, level with their lines: 'exactly view, or exactly bash' beside the name pattern, 'its arguments mention the list' beside the pattern line. The grader's name lights, then 'required', then each of the two lines.  
**Renderer:** html (scenes/s07.html)

> The tool calls grader works from those events.
> Here are two, added to the release eval file after the hidden test.
> The first is named reads the list.
> Under required, it has one entry, and every entry there must match at least one call.
> This entry has two keys, and each is a regular expression.
> Name is matched against the tool's name.
> The pattern is matched against all of the call's arguments, written out as text.
> Both have to match the same call, so this grader needs a call to view, or to bash, whose arguments mention the merged list.

## s08

**Role:** body · **Mode:** works · **Stage:** tool-calls  
**On screen:** Headline 'Why view or bash?'. The same panel on the same lines. The name pattern stays lit while the reason is given, with its note 'exactly view, or exactly bash'.  
**Renderer:** html (scenes/s08.html)

> Why both tools?
> Either one can open a file: view directly, and bash with a command such as cat.
> If a grader required view alone, it would fail a trial that opened the list with cat.
> That trial would have done exactly what the app needs, so the requirement names both tools.
> We anchor the name at both ends, because an expression otherwise matches anywhere in the text.
> Without the anchors, view would also match preview.

## s09

**Role:** body · **Mode:** works · **Stage:** tool-calls  
**On screen:** Headline 'Disallowed: no call may match'. The same panel, scrolled to the second grader (lines 39 to 44). Notes on the right: 'none of these may happen' beside disallowed, 'git commit, or git push' beside the command pattern. The name lights, then 'disallowed', then the command line.  
**Renderer:** html (scenes/s09.html)

> The second grader is named never commits.
> No call may match an entry under disallowed.
> This entry has a name too, and a second key, command, which is matched against a shell call's command.
> So it matches any bash call that contains git commit or git push.
> When a grader has only a disallowed list, it checks for absence, so a trajectory with no calls at all passes it.
> That decides how we test it: the oracle can't show such a grader failing, and only a saved trial that did the forbidden thing can.

## s10

**Role:** body · **Mode:** works · **Stage:** tool-calls  
**On screen:** Headline 'Two more complete the set'. The same panel, scrolled to the last two graders (lines 45 to 52). The skill-invocation grader's name lights, then the loop check's name. Notes on the right: 'the skill must load' beside required, 'a loop check' beside max-repeat.  
**Renderer:** html (scenes/s10.html)

> Two more graders complete the set.
> The last one we already know: skill invocation, here named loads the skill.
> In the saved run's report, haiku loaded the skill in three of its five trials, and this grader gives every trial a verdict on it.  _(depends on what the demo produced)_
> The other, named no loop, checks for loops, and that's the next thing to explain.

## s11 — Catch a loop

**Role:** body · **Mode:** works · **Stage:** loops  
**On screen:** Eyebrow 'Catching loops'. Headline 'Four in a row fail'. The same panel on the loop check (lines 45 to 48). A note on the right, level with 'max: 3': 'a fourth identical result fails'. The grader type lights, then the max line.  
**Renderer:** html (scenes/s11.html)

> An agent loops when it repeats the same action without getting anywhere: reopening a file, or rerunning a command that fails.
> Vally has two graders for that: max repeat, which counts repeats, and loop outcome, which asks whether looping was expected.
> Both work from the trajectory after the trial has ended, so neither stops a running agent; the time limits we set earlier do that.
> Let's take max repeat first: it fails when one action is repeated, back to back, more than max times.
> Ours allows three, so four identical results in a row fail.

## s12

**Role:** body · **Mode:** works · **Stage:** loops  
**On screen:** Headline 'What counts as the same?'. Dark box, left: three lines, 'match: observation', 'match: name', 'match: name-args'. Notes on the right, level with each: 'calls that got the same result · the default', 'calls to the same tool', 'the same tool, the same arguments'. Each line lights as it is named. A note under it: 'also: tools, max_cycle_period'.  
**Renderer:** html (scenes/s12.html)

> For max repeat, what counts as the same action is set by match.
> Observation, the default, means calls that got the same result.
> Name means calls to the same tool, and a third value adds the arguments: the same tool, called with the same arguments.
> Max repeat has two more settings, which narrow it to some tools, or catch an alternating pattern, such as A, B, A, B.

## s13

**Role:** body · **Mode:** works · **Stage:** loops  
**On screen:** Headline 'A second grader, for retries'. Two blocks side by side: 'max-repeat · the same action, back to back, more than max times' and 'loop-outcome · did it loop, and was that expected?'. The second fills as it is named, then the first, then the second again.  
**Renderer:** html (scenes/s13.html)

> Loop outcome is for a stimulus where retrying is the very thing under test, such as a tool that fails.
> There, max repeat can only say that the agent repeated itself; loop outcome says whether that was what we expected.
> This grader counts retries, the repeats after a first call, against a limit we choose, and a setting named should loop says which answer passes.
> None of our stimuli has a failing tool yet, so loop outcome isn't in this eval file.

## s14 — Test graders before they run

**Role:** practice · **Mode:** use · **Stage:** test-then-run · **Introduces:** vally lint, vally oracle, --no-golden-input, vally grade, --run-dir, --verbose, vally eval, -e, --model, --runs, --workers, --output-dir, cd, lesson-22, 2026, lesson-23  
**On screen:** Eyebrow 'Require, forbid, re-grade'. Headline 'Which fail on an untouched workspace?'. A table of the stimulus's five graders, 'Grader', 'It', 'On the baseline', 'On ten saved trials': every-change-handled (requires), reads-the-list (requires), never-commits (forbids), no-loop (forbids), loads-the-skill (requires); the last two columns are empty. The 'On the baseline' column lights, then the 'On ten saved trials' column, then the never-commits row; all rest for the question and a beat.  
**Renderer:** html (scenes/s14.html)

> Those are the graders; now let's test them, before any of them costs a run.
> First on the baseline: the workspace as it starts, with no agent.
> Then on the ten trials of the saved run, again with no agent.
> Then we make sure the forbidding grader can fail, and run once more.
> Which of these five would you expect to fail on a workspace nobody has touched?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s15

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. vally lint -e evals/release.eval.yaml prints one warning, scoring-defaults-applied, held. The screen is cleared out of sight. vally oracle -e evals/release.eval.yaml --no-golden-input, over two lines, prints the baseline report: three graders 'failed as expected', two 'N/A', and a last line beginning 'Score'. Held until it has been read.  
**Renderer:** terminal (tapes/s15.tape)

> The four new graders are in the eval file, so we lint it first, which is free.  _(finishes before typed:1)_
> There's one warning, the usual one about scoring: with no scoring block, every grader must pass, which is what we want.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Next, the oracle with no golden input: it builds the workspace, applies nothing, and grades that.  _(finishes before typed:2)_
> A grader that requires something should fail here.  _(finishes before enter:2)_
> Three failed as expected: the hidden test, reads the list, and loads the skill.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> The two that only forbid something are marked N/A, because doing nothing breaks no rule.  _(3s to read after; waits for output:2; depends on what the demo produced)_
> So those two still need testing.  _(waits for output:2)_

## s16

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Terminal, continuing in the practice folder. cd into the saved run's folder under results/lesson-22 (its name completed with Tab). vally grade -e ../../../evals/release.eval.yaml --run-dir . --verbose < results.jsonl, over two lines; ten blocks scroll by, one per trial, and the screen holds on the last one, listing the five graders.  
**Renderer:** terminal (tapes/s16.tape)

> Now the saved trials: we change into the saved run's folder, which holds ten trials, five for each model.  _(finishes before typed:1)_
> Vally grade re-grades them with the eval file as it is now, starting no agent, and dash dash verbose prints every grader's line.  _(waits for output:1; finishes before typed:2)_
> The hidden test needs the finished workspace, which a re-grade doesn't have, so it will fail in every block.  _(finishes before enter:2)_
> The four new graders are what we're checking.  _(finishes before enter:2)_
> The command prints ten blocks, one for each trial; the last of them is on screen.  _(3s to read after; waits for output:2; depends on what the demo produced)_
> In it, the hidden test has failed, as expected, and under it are the four new graders.  _(5s to read after; waits for output:2; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Headline 'Three passed all ten'. The table from before, both columns filled from our output: 'On the baseline' (failed as expected, or N/A) and 'On ten saved trials' (passed n of 10; the hidden test: needs the workspace). The three route graders' cells light together, then the loads-the-skill cell, then the never-commits row.  
**Renderer:** html (scenes/s17.html)

> Here are both tests, side by side.
> Reads the list, never commits and no loop passed all ten trials.  _(depends on what the demo produced)_
> Loads the skill failed two: the two haiku trials that hadn't loaded it.  _(depends on what the demo produced)_
> Never commits hasn't failed anywhere yet, and a grader that has never failed might be checking nothing.

## s18

**Role:** practice · **Mode:** use · **Stage:** test-then-run · **Introduces:** release.eval.yaml · for one re-grade, evals/release.eval.yaml · for one re-grade  
**On screen:** Headline 'Forbid a command one ran'. File panel labelled 'evals/release.eval.yaml · for one re-grade' with a minimap, on the never-commits grader (lines 39 to 44), its command pattern now the one word. A note on the right, level with that line: 'in place of git (commit|push), for a moment'.  
**Renderer:** html (scenes/s18.html)

> No saved trial committed anything, so we'll test the grader on a command that one of them did run.
> In one of its trials, haiku ran find.  _(depends on what the demo produced)_
> So, for one re-grade, the pattern forbids find, in place of git commit or push.  _(depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Terminal in the saved run's folder; the prompt shows its name. The same vally grade command, over two lines; the ten blocks scroll by again and the screen holds on the last ones.  
**Renderer:** terminal (tapes/s19.tape)

> With that one change, we re-grade the same ten trials.  _(finishes before typed:1)_
> Never commits should now fail wherever a trial ran that command.  _(finishes before enter:1)_
> It's the same ten blocks, and the one that changed has scrolled off the top, so we'll bring it back on the next screen.  _(5s to read after; waits for output:1; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Headline 'Now it can fail'. A dark box across the width with lines from that re-grade's output, as printed: the failing trial's header line, its never-commits line with a cross, and the evidence line naming the entry that matched. A note under it: 'from the block of the one trial that ran the command · other lines left out'. The never-commits line lights, then the evidence line.  
**Renderer:** html (scenes/s20.html)

> Here's the block for the trial that ran it.
> Never commits failed, and its evidence names the entry that matched: a bash call whose command contains find.  _(depends on what the demo produced)_
> It failed in that one trial, and passed in the other nine.  _(depends on what the demo produced)_
> So the grader can fail, which gives its passes some meaning.

## s20b

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Headline 'The real pattern goes back'. The eval file's panel again, labelled 'evals/release.eval.yaml' with a minimap, on the never-commits grader (lines 39 to 44); its command pattern, git (commit|push), is lit, with the note 'git commit, or git push'.  
**Renderer:** html (scenes/s20b.html)

> With that shown, the pattern goes back to git commit or push.
> This is the eval file the real run will use.

## s21

**Role:** practice · **Mode:** use · **Stage:** test-then-run  
**On screen:** Terminal, back in the practice folder. vally eval on the release eval file over four lines, with both models, --runs 3 --workers 2 and --output-dir results/lesson-23; a jump cut; then the end of the run's output: the failures, the model summary, the table and the Saved line (shown as ~/src/demo). Held until it has been read.  
**Renderer:** terminal (tapes/s21.tape)

> Last, a real run with every grader: the release stimulus, three trials on each model, two at a time.  _(finishes before typed:1)_
> That's six agent runs.  _(finishes before enter:1)_
> When it finishes, the summary lists each grader that failed any trial.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> Terra passed every grader in all three trials.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Haiku's first and third trials each failed two graders: the hidden test, and loads the skill.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> Its second trial passed all five.  _(2s to read after; waits for output:1; depends on what the demo produced)_

## s22 — What the route showed

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Eyebrow 'What the path showed'. Headline 'Two guards never fired'. Two blocks side by side: 'never-commits · failed 0 of 16 real trials' and 'no-loop · failed 0 of 16 real trials'. A note: 'ten saved trials and six new ones'. Both fill together, then the never-commits block alone.  
**Renderer:** html (scenes/s22.html)

> So what did checking the route show?
> Our two guards, never commits and no loop, didn't fail a single real trial: no agent committed, pushed, or looped.  _(depends on what the demo produced)_
> That's what we'd expect of a guard: it's there for the day a model update changes the agent's habits.
> And we've seen that never commits can fail, which is what makes its passes worth anything.

## s23

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'The route each model took'. A table, one row per model, eight trials each (five saved, three new): 'Loaded the skill', 'Recorded the refactor', 'Passed every grader'. Haiku's row lights, then terra's, then haiku's 'loaded' cell.  
**Renderer:** html (scenes/s23.html)

> The more interesting result is the route each model took.
> Haiku has eight trials in all, five saved and three new.  _(depends on what the demo produced)_
> It loaded the skill in four of them, and five of the eight have an entry for the refactor, which the skill says to leave out.  _(depends on what the demo produced)_
> Terra loaded the skill in all eight, and passed all eight.  _(depends on what the demo produced)_
> That points at loading, but it isn't the whole story: all four haiku trials without the skill wrote that entry, and so did one of the four that loaded it.  _(depends on what the demo produced)_
> Eight trials are too few to say more.

## s24

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'A new question for the team'. Two blocks side by side: 'Does the skill write good entries? · measured earlier' and 'Does the app get the skill used? · new'. Under them, the app's prompt as a quote: 'Write the Unreleased changelog entries for every change listed in release/merged.txt.' The first block fills, then the second, then the quote.  
**Renderer:** html (scenes/s24.html)

> For the team, this changes the question.
> Whether the skill writes good entries is something we measured earlier.
> Whether the app gets the skill used is new, and it depends on the model, and on the app's own prompt, which never mentions the skill.
> Both are things the team controls: the app can name the skill in its prompt, or the skill's description can name this situation.
> Either one is an edit to measure, before and after, the way we've measured edits before.

## s25

**Role:** recap · **Stage:** what-it-showed  
**On screen:** Headline 'When is a step worth grading?'. One block, 'grade a step when the app…', which opens after the question and a pause into three parts, each lit as it is said: 'requires it', 'forbids it', 'pays for a long route'.  
**Renderer:** html (scenes/s25.html)

> Before you go on: when is a step worth grading, and how is a grader that only forbids tested?
> It's worth grading when the app requires it, such as opening the list.  _(pause 2.5s first)_
> Or when the app forbids it, such as a commit or a push.
> Or when a long route costs too much, as a loop does.
> And a grader that only forbids is tested on a saved trial that did the forbidden thing, because an untouched workspace always passes it.

## s26

**Role:** next · **Stage:** what-it-showed  
**On screen:** 'Next: When a tool fails' in the display serif. Below, the hand-off question: 'Does the agent cope, and can you test that without breaking anything?' A note: 'Exercises are on the lesson page · Source: Vally docs, Choose a Grader; Grader: tool-calls'.  
**Renderer:** slide (scenes/s26.html)

> You can now add graders for the steps an agent took: one that requires opening the merged list, one that forbids a commit or a push, and a loop check, each tested against saved trials.
> In practice, the tracker or the network sometimes fails.
> Does the agent cope, and can that be tested without breaking anything?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
