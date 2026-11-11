# Start the agent where the app would — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0022-start-the-agent-where-the-app-would.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (not narrated):
- Recorded 2026-11-11: s15, s16 (10 agent runs, one take, no ERROR trials), s17, s18. Run 2026-11-11T16-51-44-338Z. Details and the demo end state: src/run/HANDOVER.md.
- Our run differs from the lesson page's: haiku passed 2 of 5 (page: 0), loaded the skill in 3 of 5 (page: 0), recorded the refactor in 3 of 5 (page: 5). s16 and s19 to s22 are written to our run; the earlier run is not cited.
- s17 prints haiku folder 1 (failing, trial 2) and s18 terra folder 0 (passing), as the page does.
- The eval file and the hidden test are installed by hidden tape setup (the page creates them in an editor) and shown in panels s07, s11, s12.
- git: and env: are explained from the page and not run, as on the page.
- An independent cold read was applied (eight findings) before recording.
<!-- /notes -->

## The story

**The question this video answers:** Inside the release tool, the agent does not start from a person's request: the tool first lists what was merged since the last release, then asks for the entries. How do I set that up for a stimulus?  
**The viewer starts:** A professional programmer who knows the shell, YAML, Node and git, and has watched the changelog-entry skill measured and improved on two models (claude-haiku-4.5 and gpt-5.6-terra) in the practice folder. Knows skill, agent, eval, eval file, stimulus, grader, trial, workspace and patch; the agent environment (the skill and the files copied into the workspace before the agent starts) and the grading environment (files added to a copy of the finished workspace after the agent stops, so the agent never has them); the program grader, which runs a staged script that prints its verdict as a line of JSON; exit codes; diff graders, which read the patch; vally lint, vally eval with -e, --model, --runs, --workers and --output-dir, and vally grade, which re-grades saved trials but cannot re-run a script grader; the results folder with a workspace.patch per trial and a report whose Skills column shows which skill a trial loaded; the words PASS, FLAKY, FAIL and ERROR. Knows the skill's rules, including that a refactor gets no entry, and has met the commands: key once, briefly, as shell commands an eval file runs before the agent starts. Every stimulus so far was a person's request for one change. Has not seen the release tool, the run-command grader, or the env and git fields.

1. **app-situation**: after this, the viewer can say what the two halves of a stimulus are when an app starts the agent, and where each one comes from
2. **setup-before-start**: after this, the viewer can predict what is in the workspace when the agent starts, and what the patch will hold, from an eval file's commands
3. **hidden-test**: after this, the viewer can read a run-command grader and its staged script, and say what makes it pass
4. **run-and-grade**: after this, the viewer can run the app's situation on two models and read what a failing and a passing trial changed
5. **what-it-showed**: after this, the viewer can set up a stimulus the way the release tool does, with its own setup command, grade it with a hidden test, and say what that test cannot see

## s01 — An app starts the agent

**Role:** hook · **Mode:** think · **Stage:** app-situation  
**On screen:** Headline 'Where the app starts' in the display serif. Two cards side by side, no arrows. Left, 'A person asks': the typo-fix request in the person's own words. Right, 'The release tool asks': its one-sentence prompt, and under it the three-line merged list in a dark box. The left card lights, then the right one.  
**Renderer:** html (scenes/s01.html)

> So far, every request came from a person, describing one change in their own words.
> Now the team that owns this changelog has built our skill into their release tooling.
> Before each release, a small tool lists the pull requests merged since the last one, saves the list as a file, and asks an agent to write the changelog entries for all of them.
> Nobody types a request, and nobody checks the entries before they ship.
> Here, you'll set up a stimulus that starts the agent exactly where that tool does, and grade what it writes with a test the agent never sees.

## s02

**Role:** body · **Mode:** think · **Stage:** app-situation  
**On screen:** Headline 'Two halves, both from the app'. Two blocks side by side: 'The prompt · what the app sends: short, always the same, written by a developer' and 'The workspace · what the app has prepared when it calls the agent'. Each lights as it is named.  
**Renderer:** html (scenes/s02.html)

> Let's start with what a stimulus is, when the thing under test is a feature of an app.
> It has two halves, and both come from the app.
> One half is the prompt: whatever the app sends, which is usually short, always the same, and written by a developer.
> The other is the workspace: whatever the app has prepared by the time it calls the agent.
> If a stimulus rewords the prompt more kindly, or tidies the workspace, it measures a situation the app never creates.

## s03

**Role:** body · **Mode:** think · **Stage:** app-situation  
**On screen:** Headline 'Run the app’s own setup'. Two blocks side by side under a lead line 'The team changes the list’s format next month': 'An eval that runs their tool · sees the new format' and 'A hand-written copy of the list · keeps passing, tells you nothing'. The first lights, then the second.  
**Renderer:** html (scenes/s03.html)

> So we copy the prompt from the app's code, word for word.
> For the workspace, we run the app's own setup steps, instead of writing their output by hand.
> Next month, the team might change the format of that list.
> But an eval that runs their tool sees the new format straight away.
> An eval with a hand-written copy of the old list keeps passing, and tells you nothing.

## s04

**Role:** body · **Mode:** think · **Stage:** app-situation  
**On screen:** Headline 'One sentence, one command'. Dark box, left: the release tool's prompt over two lines, then its setup command, 'node tools/list-merged.mjs > release/merged.txt'. Callouts on the right: 'what the app sends', 'what the app prepares'. A note: the source, Anthropic, Demystifying evals for AI agents (2026).  
**Renderer:** html (scenes/s04.html)

> Our release tool's prompt is one sentence: it asks for the Unreleased entries, for every change listed in a file named merged, in the release folder.
> Its setup is one command, which writes that file.
> Those two things are what we're going to reproduce.

## s05 — Set up before the agent starts

**Role:** body · **Mode:** works · **Stage:** setup-before-start · **Introduces:** tools/list-merged.mjs, list-merged.mjs, node  
**On screen:** Headline 'The tool that writes the list'. File panel labelled 'tools/list-merged.mjs' (lines 5 to 11, the four comment lines above shown as a hidden row). Notes on the right: beside the feat and fix lines 'users notice: an entry each'; beside the refactor line 'code only: no entry'. The feat and fix lines light together, then the refactor line.  
**Renderer:** html (scenes/s05.html)

> That's the idea; here's how an eval file reproduces it, starting with the tool.
> First, the release tool's opening job is done by a short Node script named list merged.
> In the real one, the list comes from the team's issue tracker; ours prints a fixed list, so every trial starts the same way.
> Each line holds a pull request number and a type, as in the team's commit messages.
> Feat means a new feature, and fix means a bug fix: users notice both, so both need an entry.
> Refactor means only the code changed, and for that, our skill says to add nothing.
> Earlier, a refactor request said outright that nothing changes for users; this list says only refactor, and the agent has to decide.

## s06

**Role:** body · **Mode:** works · **Stage:** setup-before-start · **Introduces:** commands:  
**On screen:** Headline 'Commands run before the agent'. Three numbered blocks in a row, no arrows: '1 Stage · the files and the skill', '2 Run commands · in the workspace, in order', '3 Agent works · on the app’s prompt'. Under blocks 1 and 2 a ruled span labelled 'the starting state'; under block 3 a span labelled 'in the patch'. Block 2 lights, then the first span's label, then the second.  
**Renderer:** html (scenes/s06.html)

> An eval file can run a command like that one, with a key we've met once before: commands.
> Inside an agent environment, commands is a list of shell commands.
> Vally runs them in the workspace, in order, after it has copied in the files and the skill, and before the agent starts.
> Each command gets sixty seconds, unless the file sets a longer limit.
> That order matters for grading.
> Whatever a command creates is part of the starting state, exactly like a staged file: the agent can open it, and it doesn't appear in the patch.
> Only what the agent changes does.

## s07

**Role:** body · **Mode:** works · **Stage:** setup-before-start · **Introduces:** evals/release.eval.yaml, release.eval.yaml, release/merged.txt  
**On screen:** Headline 'The app’s situation, as a stimulus'. File panel labelled 'evals/release.eval.yaml', the width of the stage, with a minimap, opening at lines 6 to 13 (the skill, the changelog and the staged tool), then scrolling to lines 15 to 23 (the stimulus, its prompt, its two commands). The staged tool lights, then the prompt, then the commands key, then the two quoted commands.  
**Renderer:** html (scenes/s07.html)

> Here's the eval file for the release tool.
> Our skill is installed as before, and the tool is staged into the workspace, like the changelog.
> There's one stimulus, and its prompt is the app's sentence, word for word.
> Under it, the stimulus has an agent environment of its own, with two commands.
> One makes the release folder; the other runs the tool, and saves what it prints as the merged file.
> Each command is in quotes, because an unquoted command with a colon and a space in it would be taken for YAML structure, and lint wouldn't catch it.

## s08

**Role:** body · **Mode:** works · **Stage:** setup-before-start · **Introduces:** env:, git:  
**On screen:** Headline 'Two more ways to prepare'. A block on top: 'env: · environment variables for the agent’s process · values can show up in saved trials'. Below, a dark box with the git shape from the docs (git: type: worktree, ref: v2.1.0, source: ../my-repo) and notes 'check out a commit, tag or branch', 'from a repository on your machine'. A note: 'The shape is from Vally’s Eval Spec reference · not run here'. The env block lights, then the git box.  
**Renderer:** html (scenes/s08.html)

> Two more fields can prepare the start, and this eval needs neither.
> One sets environment variables on the agent's process, for an app that passes its settings that way; their values can show up in saved trials, so it's no place for secrets.
> The other, git, builds the workspace from a repository instead of copied files, which is how a real release tool would get at the history.
> Ours has no repository, so we leave git as the documentation shows it.

## s09 — A hidden test

**Role:** body · **Mode:** works · **Stage:** hidden-test  
**On screen:** Headline 'The answer depends on the list'. Dark box, left: the three lines of release/merged.txt. Callouts on the right, level with each line: 'one line, citing #74', 'one line, citing #75', 'no line'. Each lights in turn.  
**Renderer:** html (scenes/s09.html)

> So the agent starts where the app would; now, what should a grader check?
> For each feature and each fix on the list, the changelog needs exactly one line, citing its pull request.
> For the refactor, it needs none.
> What's correct depends on the list, so the check has to open the merged file as well as the changelog.
> No pattern on the diff can do that; it takes a script.

## s10

**Role:** body · **Mode:** works · **Stage:** hidden-test · **Introduces:** run-command  
**On screen:** Headline 'Exit code zero is a pass'. Two blocks side by side: 'program · the script prints its verdict as a line of JSON' and 'run-command · passes when the command exits with code 0'. Under them a line: 'any test you already have: a test suite, a linter, a script'. The first block lights, then the second.  
**Renderer:** html (scenes/s10.html)

> We've run a grading script before, with the program grader, which expects the script to print a line of JSON.
> The run command grader is simpler; despite its name, it has nothing to do with the setup commands we just saw.
> It runs a shell command in the graded copy of the workspace, and passes when the command's exit code is zero.
> It can also check what the command prints, but the exit code is the heart of it.
> So any test you already have works unchanged: a test suite, a linter, or a script like ours.

## s11

**Role:** body · **Mode:** works · **Stage:** hidden-test · **Introduces:** evals/grading/check-release.mjs, check-release.mjs  
**On screen:** Headline 'Staged for grading only'. File panel labelled 'evals/release.eval.yaml', the width of the stage, with a minimap, scrolled to lines 24 to 32. The grading_environment lines light, then the grader's name, then the command it runs.  
**Renderer:** html (scenes/s11.html)

> Here's the rest of the stimulus.
> Its grading environment stages our script, so the agent never has it: Vally's documentation calls these grader-only files, and a test run this way is a hidden test.
> Then comes the grader, named every change handled, which runs the script with node.

## s12

**Role:** body · **Mode:** works · **Stage:** hidden-test  
**On screen:** Headline 'What the hidden test checks'. File panel labelled 'evals/grading/check-release.mjs', the width of the stage, with a minimap, opening on the top of the file, then scrolling to lines 4 to 10, to the loop (12 to 23), and to the last lines (21 to 29). In turn these light: the two files it opens, the Unreleased lines, the number and type, the lines that cite the pull request, the refactor check, the exactly-one-line check, the second-pull-request check, and the exit with code 1.  
**Renderer:** html (scenes/s12.html)

> Now the script itself, which is short.
> It opens two files: the changelog, and the merged list, which is still there because it was part of the starting state.
> It keeps the lines of the Unreleased section.
> Then, for each change on the list, it takes the number and the type, and finds the lines that cite that pull request.
> For a refactor, there must be none.
> A feature or a fix must be cited on exactly one line, and that line must not cite a second pull request.
> Between them, those checks catch a skipped change, an entry for the refactor, and two changes merged into one entry.
> On any failure, the script exits with code one, and that exit code is the verdict.

## s13

**Role:** body · **Mode:** works · **Stage:** hidden-test  
**On screen:** Headline 'This one can’t be re-graded'. Two blocks side by side: 'Reads the patch or the trajectory · can be re-graded from saved trials' and 'Needs the finished workspace · cannot: Vally doesn’t keep it'. The second lights, then the first.  
**Renderer:** html (scenes/s13.html)

> One limit is worth knowing: a hidden test needs the finished workspace, which Vally doesn't keep.
> So, like a program grader, it can't be re-graded from saved trials; graders that only need the patch or the trajectory can.

## s14 — Run it on two models

**Role:** practice · **Mode:** use · **Stage:** run-and-grade  
**On screen:** Headline 'What will each model write?'. An empty table: rows '#74 feat', '#75 fix', '#76 refactor'; columns claude-haiku-4.5 and gpt-5.6-terra, headed 'trials with an entry'. The rows light as the three kinds are named; the cells stay empty.  
**Renderer:** html (scenes/s14.html)

> That's the setup and the test; now let's run them.
> First, we run the release tool by hand, to see the list.
> Then we lint the eval file, and run it five times on each model.
> After that, we open a patch from each model.
> Three changes are on the list, and one of them is a refactor: what would you expect each model to write?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s15

**Role:** practice · **Mode:** use · **Stage:** run-and-grade · **Introduces:** vally lint, -e  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. node tools/list-merged.mjs prints the three merged changes. Then vally lint -e evals/release.eval.yaml prints that the file is valid. Held until it has been read.  
**Renderer:** terminal (tapes/s15.tape)

> We're in the practice folder, and this is the release tool, run by hand.  _(finishes before typed:1)_
> Three changes come back: a feature, a fix, and a refactor.  _(3s to read after; waits for output:1)_
> Both new files are in place, the hidden test and the eval file, so we lint before spending anything.  _(finishes before typed:2)_
> Lint finds nothing wrong.  _(2s to read after; waits for output:2)_

## s16

**Role:** practice · **Mode:** use · **Stage:** run-and-grade · **Introduces:** vally eval, --model, --runs, --workers, --output-dir, lesson-22  
**On screen:** Terminal, continuing in the practice folder. The vally eval command over four lines, with --runs 5 --workers 2 and --output-dir results/lesson-22; a jump cut; then the end of the output: the grader that failed with its evidence, the model summary, the table with one cell per model, and the Saved line shown as ~/src/demo. Held until it has been read.  
**Renderer:** terminal (tapes/s16.tape)

> Now the app's situation, on both models: five trials each, two at a time.  _(finishes before typed:1)_
> That's ten agent runs.  _(finishes before enter:1)_
> The table at the end counts stimuli, not trials: this file has one stimulus, and it passes only if all five trials do.  _(finishes before enter:1)_
> About a minute later, that table shows a cross for haiku, and a tick for terra.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> Just above it is the grader that failed, every change handled, with its evidence: the command exited with code one in three of haiku's five trials.  _(5s to read after; waits for output:1; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** run-and-grade · **Introduces:** workspace.patch, ls, cd, cat, 2026, since-last-release  
**On screen:** Terminal in the practice folder. ls results/lesson-22 shows one run folder; cd into it (Tab completes its name), then into release/since-last-release. The screen is cleared out of sight. cat claude-haiku-4.5/1/workspace.patch prints a patch that changes only CHANGELOG.md, adding an entry for #74, then '### Fixed' with #75, then '### Changed' with #76. Held until it has been read.  
**Renderer:** terminal (tapes/s17.tape)

> The run is saved in a folder named for the time it started.  _(finishes before typed:1)_
> We change into it, and then into the folder for our one stimulus.  _(waits for output:1)_
> Let's open one of haiku's failing trials first: trial two, which is folder one, because the folders count from zero.  _(finishes before typed:4; depends on what the demo produced)_
> Only the changelog is in the patch: the merged file isn't, because the setup command made it before the agent started.  _(4s to read after; waits for output:4; depends on what the demo produced)_
> There are entries for the feature and the fix, and a third, under Changed, for the refactor.  _(4s to read after; waits for output:4; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** run-and-grade  
**On screen:** Terminal, in the same stimulus folder. cat gpt-5.6-terra/0/workspace.patch prints a patch with two added entries, for #74 and #75, and nothing for #76. Held until it has been read.  
**Renderer:** terminal (tapes/s18.tape)

> For comparison, here's a trial from terra, which passed.  _(finishes before typed:1; depends on what the demo produced)_
> It has two entries, for the feature and the fix, and nothing for the refactor.  _(8s to read after; waits for output:1; depends on what the demo produced)_

## s19 — What it showed

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'One kind of failure'. The table from before, now filled from our run: for each of '#74 feat', '#75 fix', '#76 refactor', the number of each model's five trials that wrote an entry. The feat and fix rows light, then haiku's refactor cell, then terra's. A note names the run.  
**Renderer:** html (scenes/s19.html)

> So what did the hidden test show?
> When we ran it, neither model skipped a change, and neither merged two into one entry.  _(depends on what the demo produced)_
> Every failure was the same kind: haiku wrote an entry for the refactor in three of its five trials.  _(depends on what the demo produced)_
> In the patch we opened, that entry sits under Changed and names a source file; our skill forbids both.  _(depends on what the demo produced)_
> Terra left the refactor out every time, and said why in its reply.  _(depends on what the demo produced)_

## s20

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'Did it load the skill?'. A table from our run: one row for each of claude-haiku-4.5's five trials and one for gpt-5.6-terra's five together; columns 'loaded the skill' and 'entry for the refactor', each yes or no. Terra's row lights, then haiku's two trials without the skill, then the two that loaded it and left the refactor out, then the one that loaded it and recorded the refactor. A note names the run.  
**Renderer:** html (scenes/s20.html)

> The run's records add one more piece of evidence: which trials loaded our skill.
> Terra loaded it in all five trials, and haiku in three.  _(depends on what the demo produced)_
> Haiku's two trials without the skill both recorded the refactor; of the three with it, two left the refactor out, and one recorded it anyway.  _(depends on what the demo produced)_
> Our hidden test couldn't have told us that: it sees only the finished changelog, not whether the agent opened the list, or used the skill on the way.

## s21

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'The app’s wording matters'. Two quote cards side by side: 'A person’s request, earlier' with the earlier refactor request; and 'The release tool’s input' with its one-sentence prompt and, under it, the list's line '#76 refactor: move config loading out of cli.js'. The tool's card lights, then the person's.  
**Renderer:** html (scenes/s21.html)

> So what does this run support?
> The app's input is shorter than a person's: its prompt is one fixed sentence, and its list says only refactor, where a person had said that nothing changes for users.
> With that input, haiku skipped the skill in two of its five trials, and recorded the refactor in both.  _(depends on what the demo produced)_
> Loading isn't the whole story, since one trial loaded the skill and recorded the refactor anyway.  _(depends on what the demo produced)_
> Five trials on each model, in one run, can't prove a cause, but they suggest that the app's wording matters as much as the skill's.  _(depends on what the demo produced)_
> That's the kind of difference an app brings in without anyone noticing.

## s22

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'A pass isn’t proof'. Dark box, left: the list's line for #74, then terra's entries for it from our run, each distinct wording once. Notes on the right: beside the list line 'no word on which date'; beside each wording, how many of the five trials wrote it.  
**Renderer:** html (scenes/s22.html)

> Passing the test isn't the same as being right, either.
> Terra's entries for the feature each say what the new flag filters by, and they don't all say the same thing.  _(depends on what the demo produced)_
> The list doesn't say; the flag might just as well filter by the date a note was changed.
> None of our graders checks for details the list doesn't support, and in an app, nobody sees the entry before it ships.

## s23

**Role:** recap · **Stage:** what-it-showed  
**On screen:** Headline 'What can a diff grader see?'. One block, 'one trial, in order', which opens after the question and a pause into four parts: 'Stage · files and skill: the starting state', 'Run commands · what they make: the starting state', 'Agent works · what it changes: in the patch', 'Graders run · the hidden test is added here'. The third part lights with the answer, then the second, then the fourth.  
**Renderer:** html (scenes/s23.html)

> Before you go on: if a setup command creates one file, and the agent creates another, which of them can a diff grader see?
> Only the agent's.  _(pause 2.5s first)_
> Commands run before the agent starts, so what they create is part of the starting state, like a staged file.
> And a test that needs both files can still run, hidden, because the grading environment adds it after the agent has stopped.

## s24

**Role:** next · **Stage:** what-it-showed  
**On screen:** 'Next: Check what the agent did' in the display serif. Below, the hand-off question: 'Did it read the list, touch other files, try to commit or push?' A note: 'Exercises are on the lesson page · Source: Vally docs, Writing Eval Specs, “Grader-only files”'.  
**Renderer:** slide (scenes/s24.html)

> You can now set up a stimulus the way an app would, with its own setup command, and grade the result with a hidden test.
> So the entries can be checked.
> But in the app, how the agent got there matters too: did it open the list, did it touch files it shouldn't, did it try to commit or push?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
