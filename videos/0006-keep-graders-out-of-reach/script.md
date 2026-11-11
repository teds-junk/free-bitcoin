# Keep graders out of the agent's reach — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0006-keep-graders-out-of-reach.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** Where can I put a grading script so the agent cannot read or change it?  
**The viewer starts:** A professional programmer who knows the shell, JSON and exit codes, and has followed the changelog-entry skill through five steps: one request on two models, the eval file and the results folder, five trials per model, reading runs to name failure modes, and turning three failure modes into pattern graders. Knows skill, agent, model, eval file, stimulus, grader, trial, workspace, patch, the agent environment (the skills and files copied into the workspace before the agent starts), vally eval with -e, --model, --runs, --workers and --output-dir, vally lint, the words PASS, FLAKY, FAIL and ERROR, failure mode, diff graders (which read the patch), and that a trial passes only if every grader on its stimulus passes. The changelog eval file has three stimuli (typo-fix, refactor, security) and the skill has three added rules. Has never kept a workspace, and does not know --workspace, the grading environment, or a grader that runs a script.

1. **why-hide**: after this, the viewer can say why a grader the agent can read or edit tells you nothing
2. **what-goes-in**: after this, the viewer can predict which files an agent will find in its workspace, and keep a workspace to check
3. **grading-only**: after this, the viewer can read a stimulus that stages a script for graders only, and say how the script reports its verdict
4. **look-then-hide**: after this, the viewer can list what an agent was given, and run stimuli graded by a script the agent never had
5. **what-the-script-caught**: after this, the viewer can say what the hidden script caught in our runs, and how a script like it once passed a wrong answer

## s01 — Why hide the grader

**Role:** hook · **Mode:** think · **Stage:** why-hide  
**On screen:** Headline 'Keep graders out of reach' in the display serif. One dark box labelled 'a correct answer': the top of the changelog with a new entry citing (#60) under '### Fixed', inside '## [Unreleased]', above '## [1.2.0]'. '(#60)' lights, then the Fixed heading, then the Unreleased heading, then the released version's heading.  
**Renderer:** html (scenes/s01.html)

> With a pattern, a grader can say that a patch contains an entry citing a pull request.
> It can't say that the entry sits under Fixed, inside Unreleased, and not inside a version that has already shipped.
> Checking position takes a few lines of code to read the file, and that makes the grader a script.
> But a script is a file, and the agent works in a folder full of files.
> Here, you'll add a grading script that the agent never sees, and find out what it catches.

## s02

**Role:** body · **Mode:** think · **Stage:** why-hide  
**On screen:** Headline 'A grader in plain sight'. Three blocks in a row, no arrows: 'Read it · and learn what is being looked for', 'Edit it · so that it always passes', 'Fix it · distracted by a file it did not expect'. Each fills as it is said.  
**Renderer:** html (scenes/s02.html)

> Let's start with why the agent mustn't see the grader.
> An agent can read and edit everything in its workspace.
> If the grading script were there, the agent could read it, and learn exactly what's being looked for.
> Worse, it could edit the script so that it always passes.
> Or, most likely, it could be distracted by a file it didn't expect, and start fixing it.

## s03

**Role:** body · **Mode:** think · **Stage:** why-hide  
**On screen:** Headline 'Agents do find the answers'. Two blocks side by side: '73% to 100% · scored on eight benchmarks by agents that solved no task' and '63% · of one model's passing runs copied the published fix'. Note: 'Sources: Berkeley RDI, April 2026 · Cursor, June 2026 (the vendor's own report, one model)'. Each block fills as its figure is said.  
**Renderer:** html (scenes/s03.html)

> This has happened in practice.
> Benchmarks are public sets of tasks with graders, made for comparing agents.
> In April twenty twenty-six, researchers at Berkeley took eight well-known benchmarks, and scored between seventy-three and one hundred percent on them, with agents that solved none of the tasks.
> One way was reading answers that the graders had left where an agent could reach them.
> Two months later, the makers of the Cursor editor reported on one model's passing runs on a coding benchmark.
> In sixty-three percent of them, the agent had found the published fix and copied it.

## s04

**Role:** body · **Mode:** think · **Stage:** why-hide  
**On screen:** Headline 'Two plain rules'. Two numbered blocks: '1 · Out of sight · grading scripts and expected answers stay where the agent cannot see them' and '2 · Out of reach · no grader depends on a file the agent could have altered'. Each fills as it is said.  
**Renderer:** html (scenes/s04.html)

> Our changelog skill doesn't need a security review.
> It needs two plain rules.
> First, grading scripts and expected answers stay where the agent can't see them.
> Second, no grader depends on a file the agent could have altered to make it pass.

## s05 — What the agent is given

**Role:** body · **Mode:** works · **Stage:** what-goes-in · **Introduces:** one-request.eval.yaml  
**On screen:** File panel labelled 'one-request.eval.yaml', lines 6 to 11 (the agent_environment block) with 'lines hidden' rows above and below and a minimap. Notes on the right, level with their lines: 'copied as a whole folder' beside the skills entry, 'arrives under this name' beside dest. The block lights, then the skill line, then the dest line.  
**Renderer:** html (scenes/s05.html)

> Those are the rules; here's what an agent is actually given.
> In an eval file, the agent environment lists the skills and files copied into the workspace before the agent starts.
> Two details matter now.
> Each skill is copied as a whole folder: everything inside it goes into the workspace, and not only the SKILL dot M D file.
> Each listed file arrives under the destination name on the line below it.

## s06

**Role:** body · **Mode:** works · **Stage:** what-goes-in · **Introduces:** vally eval, --workspace  
**On screen:** Headline 'A workspace we can keep'. Dark code box, left: 'vally eval … --workspace kept' and under it the kept path one part per line: 'kept/', '  main/', '    typo-fix/'. Notes on the right, level with each line: 'keep each trial's workspace here', 'the folder we named', 'a folder Vally adds', 'one per stimulus'. Under the box, a note in code type: 'several models → workspace-collision'. The flag lights, then each path part, then the note.  
**Renderer:** html (scenes/s06.html)

> We can check this for ourselves.
> Adding dash dash workspace and a folder name to vally eval tells Vally to keep each trial's workspace in that folder, instead of deleting it when the trial ends.
> Inside the folder we name, there's a folder that Vally calls main, and inside that, one folder for each stimulus.
> Dash dash workspace works with one model at a time.
> The kept path has no model name in it, so with several models, Vally stops before running anything, and reports a workspace collision.

## s07

**Role:** body · **Mode:** works · **Stage:** what-goes-in  
**On screen:** Headline 'Evals live beside the skill'. Dark code box, left: our folders as a short tree: 'skills/' with 'changelog-entry/' and 'SKILL.md' under it, and 'evals/' with 'changelog.eval.yaml' and 'fixtures/' under it. Notes on the right: 'copied whole into the workspace' level with changelog-entry/, 'never copied' level with evals/. The skill folder lights, then the evals folder.  
**Renderer:** html (scenes/s07.html)

> So anything stored inside a skill's folder is handed to the agent: eval files, graders, expected answers.
> So the evals folder sits beside the skills folder, and never inside a skill.

## s08 — Files only graders get

**Role:** body · **Mode:** works · **Stage:** grading-only · **Introduces:** grading environment  
**On screen:** Headline 'Added after the agent stops'. Two cards side by side, each a dark box listing files. Left, 'Workspace · the agent works here': CHANGELOG.md, changelog-entry/. Right, 'Grading copy · made when the agent stops · only graders run here': the same two, plus .vally-grading/ and check-entry.mjs inside it. The left card lights, then the right card, then the two added lines.  
**Renderer:** html (scenes/s08.html)

> So where can a grading script go?
> Vally has a second environment for exactly this, named the grading environment.
> It lists files that Vally adds after the agent has stopped, to a copy of the finished workspace.
> Only graders run in that copy, and it's thrown away when grading ends.
> So the script joins the files once the agent has finished, in a folder the agent never works in.

## s09

**Role:** body · **Mode:** works · **Stage:** grading-only · **Introduces:** changelog.eval.yaml, grading_environment, program, check-entry.mjs  
**On screen:** File panel labelled 'changelog.eval.yaml' with a minimap: the line naming the stimulus two-changes, a '9 lines hidden' row, then its grading_environment and graders blocks. Notes on the right, level with their lines: 'files for graders only', 'where we keep the script', 'where it goes in the grading copy', 'run a program, take its verdict', 'the script, then what to look for'. Each line lights as it is described; the panel scrolls down to the grader.  
**Renderer:** html (scenes/s09.html)

> Here's a stimulus that uses one, in our changelog eval file.
> Its grading environment is written like the files part of the agent environment.
> This source line names our script, in a grading folder under evals, which no agent environment copies.
> Its destination is a folder in the grading copy whose name starts with a dot, which keeps it away from the agent's files.
> Then comes the grader, and its type is program.
> It runs one program inside the grading copy, and takes the verdict from what that program prints.
> Here the program is node, and its arguments are the script to run, and then what to look for.

## s10

**Role:** body · **Mode:** works · **Stage:** grading-only · **Introduces:** check-entry.mjs  
**On screen:** File panel labelled 'check-entry.mjs' with a minimap: the four-line opening comment, a '31 lines hidden' row, then the report function at the end of the file. The comment lights; the panel scrolls to the function; then console.log(JSON.stringify, kind, passed and score, evidence, and process.exit(0) light in turn.  
**Renderer:** html (scenes/s10.html)

> From here on, a program grader that runs a script is a script grader, and this is our script.
> It's plain JavaScript, with nothing to install.
> Its opening comment says what it checks: each argument is a category and a pull request number, and the Unreleased section must have an entry under that category, citing that number.
> Its last lines say how it reports.
> It prints the result as one line of JSON with five fields, and Vally needs all of them.
> Its name and kind say which check this is, and that code made it.
> Passed is the verdict, and score is one for a pass, and zero for a fail.
> Evidence is a sentence saying what the script found, and Vally saves it in the results as the grader's evidence.
> Finally, the script exits with code zero whether the entry is there or not, because the verdict is in what it printed.
> Any other exit code would mean that the script itself had broken.

## s11

**Role:** body · **Mode:** works · **Stage:** grading-only · **Introduces:** two-changes, after-release  
**On screen:** Headline 'Two stimuli for the script'. Two cards side by side. Left, 'two-changes': the request as a quote, and under it a dark box with the script's arguments 'Added=60' and 'Fixed=60'. Right, 'after-release · starts with no Unreleased section': its request, and 'Added=58'. The left card lights, then its two arguments, then the right card, then its argument.  
**Renderer:** html (scenes/s11.html)

> Two new stimuli use the script.
> In the first, named two-changes, one pull request adds a flag and fixes a bug.
> Its arguments, Added equals sixty and Fixed equals sixty, mean that Unreleased must have an entry under Added citing pull request sixty, and another under Fixed.
> An entry in a released version doesn't count, and the heading must be written exactly as Unreleased in square brackets.
> Our second stimulus, named after-release, starts from a changelog with no Unreleased section.
> It asks the script for one entry, under Added, citing pull request fifty-eight.

## s12

**Role:** body · **Mode:** works · **Stage:** grading-only · **Introduces:** vally lint  
**On screen:** Headline 'Two mistakes Vally catches'. Dark code box, left, two lines: 'grading-file-src-agent-visible' and 'Grader output did not match schema'. Notes on the right, level with each: 'lint: the agent could see the script's source', 'the script printed a result with a field missing'. Each line lights as it is described.  
**Renderer:** html (scenes/s12.html)

> Two safeguards are worth knowing in advance.
> Vally lint refuses a grading file whose source the agent could see, such as a script stored inside the skill folder.
> If a script prints a result with a field missing, Vally fails the trial, and says that the grader's output did not match the schema.
> That's a mistake in the script, and not in the agent's work.

## s12b

**Role:** body · **Mode:** works · **Stage:** grading-only · **Introduces:** run-command  
**On screen:** Headline 'Evidence that says why'. Two cards side by side, each a grader's type over the evidence a failure leaves, in a dark box. Left, 'run-command · passes when the script exits with 0': 'Expected exit code 0, got 1'. Right, 'program · the script prints its verdict': 'no entry citing #60 under Fixed'. The left card lights, then the right.  
**Renderer:** html (scenes/s12b.html)

> Vally has a second grader that runs a script, named run command, which passes when the script exits with zero.
> That grader is simpler to write, and it tells you less: when it fails, the evidence is only the exit code.
> We use program, so that the results say why.

## s13 — A script the agent never sees

**Role:** practice · **Mode:** use · **Stage:** look-then-hide  
**On screen:** Headline 'Look inside, then hide a script'. Three numbered blocks in a row, no arrows: '1 · Keep one workspace · and list its files', '2 · Add the two stimuli · and run all five on both models', '3 · Add a rule to the skill · and run again'. Each fills as it is said.  
**Renderer:** html (scenes/s13.html)

> That's how it works; now let's use it.
> First, we'll keep one workspace and list it, to see what an agent is given.
> Then we'll add the two stimuli that use the script, and run all five stimuli on both models.
> Whatever the script fails, we'll answer with a rule in the skill, and run again.
> Which files would you expect to find in the kept workspace?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s14

**Role:** practice · **Mode:** use · **Stage:** look-then-hide · **Introduces:** find, find kept, -type, -e, --model, --output-dir, one-request.eval.yaml, kept, lesson-6-look  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. vally eval on the one-request eval file over four lines, with one model, --workspace kept and --output-dir results/lesson-6-look; a jump cut; the one-line summary, held. Below it, find kept -type f lists two files.  
**Renderer:** terminal (tapes/s14.tape)

> Here's the run that keeps a workspace: the one-request eval file, on one model, with dash dash workspace.  _(finishes before typed:1)_
> It spends one agent run.  _(finishes before enter:1)_
> Moments later, the stimulus is a pass, on a single summary line, because there's one model.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Now we list every file under the kept folder.  _(finishes before typed:2)_
> There's the skill folder with its one file, and the changelog, as the agent left it.  _(2s to read after; waits for output:2; depends on what the demo produced)_
> That's everything the agent had, and nothing from the evals folder is in it.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** look-then-hide  
**On screen:** File panel labelled 'changelog.eval.yaml' with a minimap, showing only the five lines that name a stimulus (typo-fix, refactor, security, two-changes, after-release) with a 'lines hidden' row between each. The first three names light together, then the two new ones.  
**Renderer:** html (scenes/s15.html)

> Next, we paste the two stimuli onto the end of the changelog eval file; the starter folder has them ready, in a snippets file.
> That makes five stimuli: three with pattern graders, and two graded by the script.

## s16

**Role:** practice · **Mode:** use · **Stage:** look-then-hide · **Introduces:** --workers, lesson-6  
**On screen:** Terminal, in the practice folder. vally lint -e evals/changelog.eval.yaml prints one warning and no errors, held. The screen is cleared out of sight. vally eval on the changelog eval file over four lines, with both models, --workers 2 and --output-dir results/lesson-6; a jump cut; then the end of the run's output: the failures list, the model summary and the table of stimuli passed, held until it has been read.  
**Renderer:** terminal (tapes/s16.tape)

> Lint comes first, because it's free, and catches mistakes before we spend anything.  _(finishes before typed:1)_
> It gives the one warning this eval file already had, about scoring, and no errors.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Now the run: all five stimuli, once on each model, with two workers.  _(finishes before typed:2)_
> That spends ten agent runs.  _(finishes before enter:2)_
> With one trial per stimulus, each failure is listed with the grader that failed, and a script grader's line carries the script's own sentence.  _(finishes before enter:2)_
> About a minute later, the after-release stimulus has failed on terra, and the evidence is the script's own: no Unreleased heading in square brackets.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> Meanwhile, haiku passed all five, so its new heading had the brackets.  _(2s to read after; waits for output:2; depends on what the demo produced)_
> At the bottom, the table counts the stimuli each model passed, out of five.  _(3s to read after; waits for output:2; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** look-then-hide · **Introduces:** cd, cat, workspace.patch, 2026  
**On screen:** Terminal, continuing in the practice folder. cd into the run's folder under results/lesson-6; cd changelog; the screen is cleared out of sight; cat after-release/gpt-5.6-terra/0/workspace.patch shows the patch, held until it has been read.  
**Renderer:** terminal (tapes/s17.tape)

> That evidence says what the script didn't find; the trial's patch shows what the agent wrote in its place.  _(finishes before typed:1)_
> We change into the run's folder, and then into the eval's.  _(waits for output:1; finishes before typed:2)_
> Here's terra's patch for the after-release stimulus.  _(waits for done:2; finishes before typed:3)_
> Its new heading says Unreleased without the brackets, so the script found no Unreleased section.  _(6s to read after; waits for output:3; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** look-then-hide · **Introduces:** SKILL.md, changelog-entry/SKILL.md  
**On screen:** File panel labelled 'changelog-entry/SKILL.md' with a minimap: a 'lines hidden' row, then the last rules of the skill, ending with the three new lines. The three new lines light together as the rule is said.  
**Renderer:** html (scenes/s18.html)

> That's a question the skill left open, so we answer it in the skill.
> One more rule goes at the end: if the changelog has no Unreleased section, add one above the newest version, with its heading written exactly, square brackets included.

## s19

**Role:** practice · **Mode:** use · **Stage:** look-then-hide · **Introduces:** lesson-6-after  
**On screen:** Terminal, in the practice folder. The same vally eval command with --output-dir results/lesson-6-after; a jump cut; then the end of the run's output: any failures, the model summary and the table of stimuli passed, held until it has been read.  
**Renderer:** terminal (tapes/s19.tape)

> Then the same five stimuli run again, saved to a new folder.  _(finishes before typed:1)_
> That's another ten agent runs.  _(finishes before enter:1)_
> This time, both models passed all five, so terra's new heading has its brackets.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> With nothing failing, there are no failures to list above the summary.  _(3s to read after; depends on what the demo produced)_

## s20 — What the script caught

**Role:** body · **Mode:** think · **Stage:** what-the-script-caught  
**On screen:** Headline 'Terra dropped the brackets'. Two cards, one above the other, labelled claude-haiku-4.5 and gpt-5.6-terra: the lines each model's after-release trial added in the first run, from its patch. '## Unreleased' lights red in terra's, then '## [Unreleased]' green in haiku's. Under them a note: 'first run · one trial for each model' and the run's name.  
**Renderer:** html (scenes/s20.html)

> So what did the script catch?
> In the first run, terra wrote the new heading without brackets, and haiku wrote it with them.  _(depends on what the demo produced)_
> With one trial for each model, that shows the failure can happen, and not which model is prone to it.
> Once the rule was in the skill, both models wrote the heading correctly.  _(depends on what the demo produced)_

## s21

**Role:** body · **Mode:** think · **Stage:** what-the-script-caught  
**On screen:** Headline 'A wrong answer, passed'. Dark code box labelled 'an earlier run · two-changes · part of the patch the script passed', showing the excerpt with its omitted text marked by an ellipsis, and a note that its first five lines are left out. Notes on the right, level with their lines: 'a released version's heading, deleted' beside the removed '## [1.2.0]' line, 'the Fixed entry, in its place' beside the added '### Fixed'. The added lines light, then the removed line, then the released entries below.  
**Renderer:** html (scenes/s21.html)

> In our two runs, the script passed all four two-changes trials, and all four were right.  _(depends on what the demo produced)_
> An earlier run of these same stimuli went differently: the script passed both of its two-changes trials, and haiku's was wrong.
> Here's part of that patch.
> That agent wrote its Fixed entry where the heading of version one point two had been, and deleted that heading.
> That version has been released, and its entries now sit under Unreleased, as if they had never shipped.  _(3s to read after)_

## s22

**Role:** body · **Mode:** think · **Stage:** what-the-script-caught  
**On screen:** File panel labelled 'check-entry.mjs' with a minimap, now on the lines hidden earlier: where the script finds the '## [Unreleased]' heading and searches for the next line starting with '## '. Notes on the right: 'find the Unreleased heading', 'read down to the next version heading'. Each lights as it is said; then nothing is lit.  
**Renderer:** html (scenes/s22.html)

> Why did the script pass it?
> It finds the Unreleased heading, and takes everything down to the next version heading.
> With that heading gone, the next version heading was further down, so the script found every entry it wanted, and passed.
> When a grader passes a wrong answer, it's worse than having none, because its tick tells you to stop looking.
> Our skill already says to leave released versions alone, so the gap is in the grader, and not in the skill.

## s23

**Role:** body · **Mode:** think · **Stage:** what-the-script-caught  
**On screen:** Headline 'A glimpse, not a measurement'. Two blocks side by side, both about claude-haiku-4.5 and the security stimulus with the security rule in the skill: '1 of 3 · filed under Fixed · an earlier run' and '0 of 5 · filed under Fixed · our runs'. Each fills as it is said.  
**Renderer:** html (scenes/s23.html)

> One more thing happened, and it's quieter.
> In an earlier run, with the security rule already in the skill, haiku filed the security fix under Fixed in one of three trials.
> Across our runs with that rule, it has filed it under Security every time: five trials out of five.  _(depends on what the demo produced)_
> Nothing was changed to cause that.
> It's the variation from run to run, and a reminder that a few trials are a glimpse, and not a measurement.

## s24

**Role:** recap · **Stage:** what-the-script-caught  
**On screen:** The two cards from earlier, Workspace and Grading copy, with their file lists. After the question and a pause, the left card lights as the agent environment is described, then the right card.  
**Renderer:** html (scenes/s24.html)

> Before you go on: what do the agent environment and the grading environment each add, and when?
> The agent environment copies skills and files into the workspace before the agent starts, and the agent can read and edit all of it.  _(pause 2.5s first)_
> The grading environment adds files to a copy of the finished workspace, after the agent has stopped, and only graders run there.

## s25

**Role:** next · **Stage:** what-the-script-caught  
**On screen:** 'Test a grader' in the display serif under the eyebrow 'Next', with the rest of the next lesson's title, 'without running an agent', beneath it. Below, the hand-off question: 'How do you test a grader?' A note: 'Exercises are on the lesson page · Source: Vally docs, Writing Eval Specs, Grader-only files'.  
**Renderer:** slide (scenes/s25.html)

> You can now see exactly what an agent is given, and add a grading script that reaches the graders without ever reaching the agent.
> But a hidden script now decides pass and fail, and only you can see whether it's right.
> How do you test a grader?
> That's the next lesson.
> The exercises on the lesson page are worth doing first; the third one closes the gap we just found.
