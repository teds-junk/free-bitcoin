# Check graders against saved trials — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0008-check-graders-against-saved-trials.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** The oracle cannot test a grader that checks for absence, and it tries one correct answer. Can I run my graders on the real trials I have already saved?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through seven lessons on two models. Knows skill, eval file, stimulus, grader, trial, run, patch and workspace.patch, results.jsonl and the results folder with one folder per trial. Has read saved trials and named failure modes; has written the three diff graders that read the patch (diff-contains, diff-not-contains, diff-empty), including no-made-up-number with its pattern and the (?m) switch at its front, adds-an-entry, adds-nothing and under-security; knows the every-grader-must-pass rule. Has run those graders before and after editing the skill, and still has both runs saved. Knows the grading environment and a script grader that runs after the agent stops. Knows a golden patch, vally oracle with -e, --stimulus, --verbose and --no-golden-input, the baseline, and that the oracle marked the two graders that check for absence N/A. Has never run graders over a saved run, and does not know vally grade or --run-dir.

1. **saved-trials-are-tests**: after this, the viewer can say which saved trial tests a grader that checks for absence, and what result would show that the grader is broken
2. **re-grading**: after this, the viewer can say what vally grade reads from a saved run, and which graders' results to ignore
3. **catch-it**: after this, the viewer can re-grade a saved run without starting an agent, and use it to show that a grader the oracle accepted could never fail
4. **a-habit**: after this, the viewer can choose the order of checks for any new or changed grader: the oracle, a saved run of known failures, then agent runs

## s01 — Saved trials are tests

**Role:** hook · **Mode:** think · **Stage:** saved-trials-are-tests  
**On screen:** Headline 'Check graders against saved trials' in the display serif. Two cards, one above the other. First, labelled 'the oracle, on an untouched file': the oracle's own line for no-made-up-number, 'N/A — pass allowed on the empty baseline'. Second, labelled 'a saved trial': the entry that trial added, ending '(#42)'. 'N/A' lights, then '(#42)'.  
**Renderer:** html (scenes/s01.html)

> Among our graders, no made-up number is the one we've leaned on most, and the oracle couldn't vouch for it.
> An untouched changelog has no made-up number in it, so the grader passes it, and that proves nothing.
> What would prove something is a changelog where a model did make up a number.
> Trials like that are already saved, from a run we paid for earlier.  _(depends on what the demo produced)_
> Here, you'll run your graders over trials you've already saved, and catch a grader that can never fail.

## s02

**Role:** body · **Mode:** think · **Stage:** saved-trials-are-tests  
**On screen:** Headline 'Every saved trial has an answer'. Two blocks side by side, no arrow: 'A trial you know is bad · tests a grader that checks for absence: the grader must fail it' and 'A trial you know is good, in different words · tests whether a grader is too strict'. Each fills as it is named.  
**Renderer:** html (scenes/s02.html)

> Let's start with why saved trials are worth keeping.
> Every trial you've read is an example with a known answer: you know whether it's right or wrong, and why.
> That makes saved trials the best material we have for testing graders, in two ways the oracle can't manage.
> Any trial you know is bad tests a grader that checks for absence, because the grader has to fail it.
> Any trial you know is good, but worded differently from the golden patch, tests whether a grader is too strict.
> The oracle tried one correct answer for each stimulus, while our saved runs hold several, each worded a little differently.
> When a grader fails one of them, it's objecting to wording, not to a fault.

## s03

**Role:** body · **Mode:** think · **Stage:** saved-trials-are-tests · **Introduces:** changelog.eval.yaml, evals/changelog.eval.yaml  
**On screen:** Headline 'A must-not grader needs a failure'. Left: file panel on evals/changelog.eval.yaml at the no-made-up-number grader, with its type, name and pattern. Right, level with the type: 'passes when the pattern is absent'. Below: a card 'a saved trial we know is bad' with the entry ending '(#42)'. The type lights, then '(#42)'.  
**Renderer:** html (scenes/s03.html)

> The example here is no made-up number, which passes when its pattern is absent from the patch: a must-not grader.
> If it doesn't fail a trial where the model wrote a number nobody gave it, the grader is broken, whatever the oracle said.
> That gives us a simple rule: every must-not grader needs at least one saved trial that it fails.
> And when a grader and our own reading disagree, we don't assume either is right: we open the evidence and the patch, and decide.

## s04 — Re-grade a saved run

**Role:** body · **Mode:** works · **Stage:** re-grading · **Introduces:** vally grade, -e, --run-dir, results.jsonl  
**On screen:** Headline 'Grade again, with no agent'. Dark code box, left: the vally grade command on two lines, as the lesson page prints it. Right, level with each part: 'graders over saved trials · no agent', 'the graders as the file has them now', 'the run's folder', 'the saved trials, as input'. Each part lights as it is named.  
**Renderer:** html (scenes/s04.html)

> That's the idea; here's the command that does it.
> Vally grade runs graders over trials that are already saved.
> No agent starts, so it costs nothing.
> Dash e names the eval file.
> Its graders are applied as they are in the file now, matched to each saved trial by stimulus name.
> So when we change a grader, the next re-grade uses the changed one.
> The saved trials are the run's results dot jsonl, given to the command as its input.
> And dash dash run dir names the run's folder, because one more piece is kept there.

## s05

**Role:** body · **Mode:** works · **Stage:** re-grading · **Introduces:** diffs, workspace.patch  
**On screen:** Headline 'A run keeps its diffs'. Dark code box, left: a short tree of one run folder: results.jsonl, diffs/, and a trial folder with workspace.patch. Right, level with each: 'one record per trial', 'a copy of every trial's diff · only when the eval file has a diff grader', 'the same diff, for us to read'. workspace.patch lights, then diffs/.  
**Renderer:** html (scenes/s05.html)

> Each trial's folder has a workspace patch for us to read.
> If the eval file has a diff grader, meaning one of the three graders that work from the patch, the run also keeps a copy of every trial's diff, in a folder named diffs.
> Those copies are what a re-grade reads, and run dir tells it which run to look in.
> There are two limits, and here's the first.
> Runs made before the eval file had a diff grader kept no copies, so they give a diff grader nothing to re-grade.

## s06

**Role:** body · **Mode:** works · **Stage:** re-grading  
**On screen:** Headline 'Script graders can't be re-graded'. Two blocks side by side: 'diff grader · reads the saved diff · its result holds' and 'script grader · needs the workspace, which is gone · fails every trial'. Below, in a dark box with a note on its right, what our script prints in a re-grade: 'no CHANGELOG.md to check'. Each block fills as it is named; then the message lights.  
**Renderer:** html (scenes/s06.html)

> The second limit is about script graders.
> Diff graders work from the saved diff, so their results in a re-grade hold.
> Script graders need the workspace, and a saved run keeps the diff, not the workspace.
> So in a re-grade, a script grader fails on every trial, including trials that really passed.
> Ours even says why: there's no changelog to check.
> In a re-grade we ignore script graders, and test those with the oracle.

## s07

**Role:** body · **Mode:** works · **Stage:** re-grading  
**On screen:** Headline 'A pattern that looks right'. Dark code box, left, two lines: the pattern without (?m), and under it the pattern as the eval file has it. Right, level with each: 'as we first wrote it', 'as the eval file has it'. The first line lights; then '(?m)' in the second; then the first again.  
**Renderer:** html (scenes/s07.html)

> The saved trials are about to catch a real mistake, one we made while writing this course.
> When we first wrote no made-up number, this was its pattern.
> The eval file's pattern is the same, plus four characters at the front.
> And it reads correctly: a line that starts with a plus sign, and contains a number in brackets.
> It's wrong, though.

## s08

**Role:** body · **Mode:** works · **Stage:** re-grading · **Introduces:** workspace.patch · a saved trial  
**On screen:** Headline 'No patch starts with a plus'. File panel labelled 'workspace.patch · a saved trial': the patch's header lines and the added entry ending '(#42)', with 'lines hidden' rows and a minimap. Right, level with line 1: 'without (?m), ^ means only here'. Level with the entry: 'the line the grader has to find'. Line 1 lights, then the entry.  
**Renderer:** html (scenes/s08.html)

> Here's why, on the patch from a saved trial.
> Those four characters are a switch that makes the caret mean the start of every line.
> Without the switch, the caret means only the very start of the whole patch.
> But a patch never starts with a plus sign; it starts with a header line like this one.
> So the pattern can never be found, however many made-up numbers sit further down.
> Any grader that passes when its pattern isn't found will then pass everything.

## s09 — Catch a grader that cannot fail

**Role:** practice · **Mode:** use · **Stage:** catch-it  
**On screen:** Headline 'Four steps, no agent runs'. Four numbered blocks across the width, no arrows: 1 're-grade · the saved run, graders as they are'; 2 'swap · the flawed pattern goes in'; 3 'ask twice · the oracle, then the saved trials'; 4 'restore · the right pattern goes back'. Each fills as it is named.  
**Renderer:** html (scenes/s09.html)

> That's how it works; now let's catch it.
> First, we'll re-grade a saved run where we know failures happened, with the graders as they are.
> Then the flawed pattern goes in, and we ask the oracle and the saved trials about it, one after the other.
> Last, the right pattern goes back.
> What would you expect the oracle to say about a grader that can never fail?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s10

**Role:** practice · **Mode:** use · **Stage:** catch-it · **Introduces:** ls, cd, lesson-5-before, 2026  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. ls results/lesson-5-before shows one folder named with a time; cd into it; then the vally grade command over two lines. Its blocks scroll past and the last screen of them is held until it has been read.  
**Renderer:** terminal (tapes/s10.tape)

> For this, the run we want is the first one we graded with diff graders, made before the skill had any rule about numbers, and before the eval file had a script grader.  _(finishes before typed:1)_
> There's one folder, named with the time of the run.  _(waits for output:1)_
> We change into it, so the paths stay short.  _(finishes before typed:2)_
> Now the re-grade: the eval file is three folders up, the run dir is this folder, and the saved results are the input.  _(waits for done:2; finishes before typed:3)_
> Vally prints one block for each saved trial: the stimulus name, a tick or a cross, and each failing grader with its evidence, but not the model.  _(finishes before enter:3)_
> Eighteen blocks come back, for three stimuli run three times on two models, which is more than fits on a screen.  _(3s to read after; waits for output:3; depends on what the demo produced)_

## s11

**Role:** practice · **Mode:** use · **Stage:** catch-it  
**On screen:** Headline 'Six trials of one stimulus'. One wide dark box labelled 'the re-grade · the six typo-fix blocks': each block's verdict line and, under a failing one, the grader it names with its evidence, as printed. The passing lines light, then the two lines naming no-made-up-number, then the line naming adds-an-entry.  
**Renderer:** html (scenes/s11.html)

> Here are the six blocks for the typo fix stimulus: three trials on each of the two models.
> Three passed and three failed, the same count as when the run was first graded.  _(depends on what the demo produced)_
> Two of the failures name no made-up number: those are the trials where a model invented one.  _(depends on what the demo produced)_
> The third names adds an entry: in that trial the model asked for the number, and wrote nothing.  _(2s to read after; depends on what the demo produced)_

## s12

**Role:** practice · **Mode:** use · **Stage:** catch-it  
**On screen:** Headline 'Four characters come out'. File panel on evals/changelog.eval.yaml at the no-made-up-number grader, as the file is after the edit: the pattern now begins with the caret. Right, level with the pattern: '(?m) deleted from the front'. The grader's name lights, then the pattern.  
**Renderer:** html (scenes/s12.html)

> Next, the flawed pattern goes in.
> In the eval file, under the no made-up number grader, we delete the four characters from the front of the pattern, and save.
> Nothing else in the file changes.

## s13

**Role:** practice · **Mode:** use · **Stage:** catch-it · **Introduces:** vally oracle, --stimulus, --verbose, --no-golden-input  
**On screen:** Terminal, still in the run's folder. cd ../../.. returns to practice. vally oracle on the typo-fix stimulus with --verbose prints PASSED; the screen is cleared out of sight; the same with --no-golden-input prints 'failed as expected', 'N/A' and 'baseline OK'. Each result is held until it has been read.  
**Renderer:** terminal (tapes/s13.tape)

> Back in the practice folder, we ask the oracle about the changed grader.  _(finishes before typed:1)_
> First with the golden patch applied, for the typo fix stimulus alone, printing each grader's evidence.  _(waits for done:1; finishes before typed:2)_
> It passed: with a correct answer in place, the pattern isn't found.  _(3s to read after; waits for output:2; depends on what the demo produced)_
> Then without the golden patch, on the untouched file.  _(finishes before typed:3)_
> Adds an entry failed as expected, no made-up number is marked not applicable, and the last line says baseline OK.  _(4s to read after; waits for output:3; depends on what the demo produced)_
> The oracle has no complaint.  _(waits for done:3; depends on what the demo produced)_

## s14

**Role:** practice · **Mode:** use · **Stage:** catch-it  
**On screen:** Terminal in the practice folder. cd into the run's folder again; the same vally grade command over two lines. The blocks scroll past and the last screen is held.  
**Renderer:** terminal (tapes/s14.tape)

> So let's ask the saved trials: back into the run's folder, and the same re-grade as before.  _(finishes before typed:1)_
> The only thing that has changed is the pattern.  _(waits for done:1; finishes before enter:2)_
> Eighteen blocks again.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** catch-it  
**On screen:** Headline 'The grader cannot fail'. A table of the six typo-fix trials in the two re-grades: rows 'pattern with (?m)' and 'pattern without (?m)'; columns 'passed', 'failed no-made-up-number', 'failed adds-an-entry'. Below it, a card 'still in the saved patch' with the entry ending '(#42)'. The first row's count lights, then the second row's zero and '(#42)', then the second row's passed count.  
**Renderer:** html (scenes/s15.html)

> Side by side, for the six typo fix trials: with the right pattern, two failed no made-up number.  _(depends on what the demo produced)_
> With the flawed pattern, none did, not even the trials where we know a number was made up.  _(depends on what the demo produced)_
> Five of the six now pass, and the sixth still fails adds an entry, because it wrote nothing.  _(depends on what the demo produced)_
> So the oracle accepted this grader, and the saved trials show that it cannot fail.  _(2s to read after)_

## s16

**Role:** practice · **Mode:** use · **Stage:** catch-it  
**On screen:** Terminal in the run's folder, with the correct pattern back in the eval file (restored out of sight). The same vally grade command; the last screen of blocks is held.  
**Renderer:** terminal (tapes/s16.tape)

> Finally, the four characters go back into the eval file, and we run the re-grade once more from the run's folder.  _(finishes before typed:1)_
> These blocks match the first re-grade: no made-up number fails the trials it should.  _(3s to read after; waits for output:1; depends on what the demo produced)_

## s17 — A habit for every grader

**Role:** body · **Mode:** think · **Stage:** a-habit  
**On screen:** Headline 'The oracle couldn't tell'. Two blocks side by side: 'the oracle · accepted the flawed grader' and 'the saved trials · showed that it cannot fail'. Each fills as it is named.  
**Renderer:** html (scenes/s17.html)

> So what should we make of that?
> Four characters were the difference between a grader that works and one that approves everything.
> Our oracle runs couldn't tell the two apart.
> Saved trials could, because some of them were known to be bad.

## s18

**Role:** body · **Mode:** think · **Stage:** a-habit  
**On screen:** Headline 'The same run settled another'. Left: a dark box with one refactor block from the first re-grade, as printed, naming adds-nothing. Right: a block with a large count, '6 of 6', and under it 'refactor trials that adds-nothing failed'. The grader's name lights, then the count.  
**Renderer:** html (scenes/s18.html)

> The same re-grade settled our other must-not grader, with no extra work.
> Adds nothing failed all six refactor trials, as it should, because both models recorded the refactor.  _(depends on what the demo produced)_
> So both must-not graders now have saved trials that they fail.  _(depends on what the demo produced)_

## s19

**Role:** body · **Mode:** think · **Stage:** a-habit  
**On screen:** Headline 'Oracle, saved run, then agents'. Three numbered blocks across the width, no arrows: 1 'oracle · free'; 2 're-grade a saved run where the failure is known · free'; 3 'agent runs · paid'. Each fills as it is named.  
**Renderer:** html (scenes/s19.html)

> This is worth making a habit, whenever we write or change a grader.
> First the oracle, which is free.
> Then a re-grade of a saved run where the failure is known to occur, which is also free.
> Only then do we spend agent runs.

## s20

**Role:** recap · **Stage:** a-habit  
**On screen:** Headline 'What tests a must-not grader?'. One block, 'a grader that checks for absence', which after the question and a pause opens into two parts: 'the oracle · an untouched file passes it honestly: N/A' and 'a saved bad trial · the grader must fail it'. Each part lights as it is said.  
**Renderer:** html (scenes/s20.html)

> Before you go on: which kind of grader can't the oracle test, and what tests it instead?
> Graders that check for absence: an untouched workspace passes them, so the oracle can't test them.  _(pause 2.5s first)_
> What tests it is a re-grade of a saved trial known to contain the fault: the grader must fail that trial.

## s21

**Role:** next · **Stage:** a-habit  
**On screen:** 'Does the skill load?' in the display serif, under the eyebrow 'Next'. Below, the hand-off question: 'Will it load for other wordings, and stay out of requests that are not its job?' A note: 'Exercises are on the lesson page · Source: Vally docs, CLI: grade'.  
**Renderer:** slide (scenes/s21.html)

> You can now re-grade a saved run without starting an agent, and show that a grader the oracle accepted could never fail.
> Our graders have been tested against correct answers, untouched files, and real bad answers.
> But in every trial so far, the skill was loaded.
> But will it load for other wordings, and stay out of requests that aren't its job?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
