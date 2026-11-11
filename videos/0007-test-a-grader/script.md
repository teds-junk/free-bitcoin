# Test a grader without running an agent — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0007-test-a-grader.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** How do I know a grader passes correct work and fails missing work?  
**The viewer starts:** A professional programmer who knows the shell and has watched the course so far. Knows skill, agent, model, eval, eval file, workspace, patch (an added line begins with a plus), stimulus, grader, trial, run, the results folder with a folder per trial holding workspace.patch, failure mode, and the vally eval command with -e. Knows the diff graders (diff-contains, diff-not-contains, diff-empty), file-contains, that a trial passes only if every grader on its stimulus passes, the agent environment, and the grading environment that adds files only for grading, where a program grader runs a hidden script. Works in the practice folder, where every command is typed. The changelog eval file has five stimuli (typo-fix, refactor, security, two-changes, after-release) with six graders between them (adds-an-entry, no-made-up-number, adds-nothing, under-security, two-entries-in-place, entry-in-new-unreleased), the last two run by the hidden script, and the most recent run of it is saved under results/lesson-6-after. Has read saved patches and judged them right or wrong. Has never tested a grader on purpose, and does not know golden patch, vally oracle, --no-golden-input, --stimulus, --verbose, or the word baseline.

1. **two-ways-wrong**: after this, the viewer can name the two ways a grader can be wrong, and the example that tests for each
2. **golden-patch**: after this, the viewer can say what a golden patch is, and point to where the eval file names it
3. **what-oracle-does**: after this, the viewer can predict what vally oracle reports for a grader, with the golden patch applied and without it
4. **prove-your-graders**: after this, the viewer can keep a saved trial's patch as a golden patch, and run the oracle both ways to show that the graders pass a correct answer and fail an untouched file
5. **what-the-oracle-did-not-test**: after this, the viewer can say which graders the oracle has tested in both directions, and which it could not

## s01 — Who grades the grader?

**Role:** hook · **Mode:** think · **Stage:** two-ways-wrong  
**On screen:** Headline 'Who grades the grader?' in the display serif. One card labelled 'changelog.eval.yaml · the graders on typo-fix' holding the two real graders in a dark box (adds-an-entry, no-made-up-number). Beside it two blocks: 'a correct answer' and 'an untouched file'. The graders light when they are named, then each block as the promise names it.  
**Renderer:** html (scenes/s01.html)

> Five stimuli now have graders, and those graders decide whether the skill is improving.
> But a grader is a small program, and programs have bugs.
> If one is wrong, we might fix things that were fine.
> Or we might believe a failure is gone, when the grader simply can't see it.
> Here, you'll test your graders against a correct answer and against an untouched file, without starting an agent.

## s02

**Role:** body · **Mode:** think · **Stage:** two-ways-wrong  
**On screen:** Headline 'Two ways to be wrong'. Two blocks side by side, no arrow: 'It fails correct work · we chase a problem that isn't there' and 'It passes work that wasn't done · we stop looking at a problem that is'. Each fills as it is described.  
**Renderer:** html (scenes/s02.html)

> Let's start with how a grader can be wrong.
> It gives one of two answers, so there are two ways.
> First, it can fail correct work: the agent did the right thing, and the grader objects anyway, perhaps because it insists on one exact wording.
> Then we chase a problem that isn't there.
> Second, it can pass work that was never done: it's so loose, or so broken, that anything satisfies it, including nothing.
> Then we stop looking at a problem that's still there.

## s03

**Role:** body · **Mode:** think · **Stage:** two-ways-wrong  
**On screen:** Headline 'Each test needs its example'. The same two blocks, now each with the example that tests for it: 'A result known to be correct · if the grader fails it, the grader is wrong' and 'The starting files, untouched · if the grader passes them, it isn't checking the work'. Each fills as it is named.  
**Renderer:** html (scenes/s03.html)

> To test for each, we need the matching example.
> For the first, that's a result we know is correct: if the grader fails it, the grader is wrong.
> For the second, it's a result where we know no work was done: the starting files, untouched.
> If the grader passes that, it isn't checking the work.
> You've seen a rough form of the second test already, when new graders ran against the skill before it was edited, and each one failed.
> Both tests can be made exact, and repeatable.

## s04 — A golden patch

**Role:** body · **Mode:** works · **Stage:** golden-patch · **Introduces:** golden patch, golden/typo-fix.patch, typo-fix.patch  
**On screen:** Headline 'A correct answer, kept'. File panel labelled 'golden/typo-fix.patch' on the real patch, lines 6 to 12 with 'lines hidden' rows above and below and a minimap. Notes on the right, level with their lines: 'a new Fixed category' and 'names the command, no pull request'. The two added lines light in turn.  
**Renderer:** html (scenes/s04.html)

> That's the idea; here's the first example, the result known to be correct.
> You already own several: every trial whose patch you've read and judged right.
> One of those, copied to a place where you keep it, is called a golden patch.
> That file holds exactly the changes a correct answer would make to the starting files, and golden is the usual word for a reference answer that's known to be good.
> Here's the one we're about to keep, for the typo fix stimulus: the patch from one of our saved trials, unchanged.
> It adds a Fixed category under Unreleased, in the right place.  _(depends on what the demo produced)_
> Its one entry mentions the command and cites no pull request, because the request gave none.  _(2s to read after; depends on what the demo produced)_

## s05

**Role:** body · **Mode:** works · **Stage:** golden-patch · **Introduces:** golden_patch, changelog.eval.yaml  
**On screen:** Headline 'The eval file names it'. File panel labelled 'changelog.eval.yaml' with a minimap: the typo-fix stimulus's name, a 'lines hidden' row, then golden_patch:, its path, and graders:. Notes on the right: 'beside graders, inside the stimulus' and 'relative to the eval file'. The panel then scrolls to the refactor stimulus and its one grader, diff-empty, with the note 'no golden patch'.  
**Renderer:** html (scenes/s05.html)

> The eval file names the golden patch inside the stimulus it belongs to, and here's how that will look.
> Its key is golden underscore patch, and it sits beside graders.
> The path on the next line is relative to the eval file, and must sit in the eval file's folder or below.
> Not every stimulus can have one.
> For the refactor stimulus, the correct answer is to change nothing, and there's no patch for nothing.

## s06 — What the oracle does

**Role:** body · **Mode:** works · **Stage:** what-oracle-does · **Introduces:** vally oracle  
**On screen:** Headline 'The oracle plays the agent'. Two columns of three numbered steps, each under its command in a dark box. Left, under 'vally oracle': 1 Fresh workspace, 2 Apply the golden patch, 3 Run the graders, and beneath 'every grader should pass'. Right, under 'vally oracle --no-golden-input': 1 Fresh workspace, 2 Apply nothing, 3 Run the graders, and beneath 'every grader should fail'. No arrows. The left column's command and steps light in turn.  
**Renderer:** html (scenes/s06.html)

> Now for the tool that uses it.
> Vally oracle runs your graders against a known answer, with no agent involved.
> The word comes from testing, where an oracle is a source of answers known to be right.
> Plain vally oracle builds the workspace exactly as it would for a real trial.
> Where an agent would have worked, it applies the golden patch instead.
> Applying a patch means making the changes it records, so its plus lines are added to the file.
> Then it runs the graders, and a grader that fails here is failing a correct answer.

## s07

**Role:** body · **Mode:** works · **Stage:** what-oracle-does · **Introduces:** --no-golden-input, baseline  
**On screen:** The same two columns, unchanged. Now the right column lights: its command with '--no-golden-input', then 'Apply nothing' as the baseline is named, then each column's bottom line in turn.  
**Renderer:** html (scenes/s07.html)

> Adding dash dash no golden input does the other test: the same workspace, with nothing applied.
> Vally's name for that untouched state is the baseline.
> So on one side the oracle plays an agent that got everything right, and on the other, an agent that did nothing.

## s08

**Role:** body · **Mode:** works · **Stage:** what-oracle-does · **Introduces:** failed as expected, N/A, trivially passing  
**On screen:** Headline 'Three reports on the baseline'. Dark box, left, labelled 'what the oracle says about a grader, with nothing applied': three lines in the oracle's own words, 'failed as expected', 'N/A', 'passed without the golden solution (trivially passing)'. Notes on the right, level with each: 'it depends on the work: good', 'an absence check: not tested', 'it depends on nothing: baseline PROBLEM'. Each line lights as it is explained.  
**Renderer:** html (scenes/s08.html)

> On the baseline, a grader ought to fail, and the oracle reports that as good news: failed as expected.
> That grader depends on the work being done.
> There are two other things it can say.
> Next, N/A: that's for a grader that checks something is absent, such as diff not contains, or diff empty.
> With nothing done, nothing unwanted is there, so that grader passes honestly, and the test tells us nothing about it.
> Last, trivially passing: the grader passed the untouched workspace, and it isn't an absence check.
> It doesn't depend on the work at all, so the oracle prints baseline problem, and exits with an error.

## s09

**Role:** body · **Mode:** works · **Stage:** what-oracle-does · **Introduces:** -e, --stimulus, --verbose  
**On screen:** Headline 'One stimulus, with evidence'. Dark box, left: the command with one option per line: 'vally oracle -e evals/changelog.eval.yaml', '--stimulus typo-fix', '--verbose'. Notes on the right, level with each part: 'the eval file, as for vally eval', 'only this stimulus', 'each grader's evidence'. Each part lights as it is named.  
**Renderer:** html (scenes/s09.html)

> The command takes dash e and the eval file, as vally eval does.
> Dash dash stimulus, with a name, limits the oracle to one stimulus.
> Dash dash verbose prints each grader's evidence: what it found, or didn't find.
> Without dash dash stimulus, the oracle covers every stimulus that has a golden patch.

## s10 — Prove the graders

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders  
**On screen:** Headline 'Both tests, every grader'. A table with a row for each of the six graders, by stimulus (typo-fix: adds-an-entry, no-made-up-number; refactor: adds-nothing; security: under-security; two-changes: two-entries-in-place; after-release: entry-in-new-unreleased), and two empty columns: 'With the golden patch' and 'Without it'. Each column header lights as it is named. The cells stay empty.  
**Renderer:** html (scenes/s10.html)

> That's how it works; now let's prove our graders.
> First, we'll keep one correct trial as a golden patch, and run the oracle both ways on its stimulus.
> Then we'll do the same for the other stimuli.
> No step starts an agent, so none of it costs anything.
> Which of these six graders would you expect to fail an untouched file?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s11

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders · **Introduces:** ls, cd, mkdir, cp, lesson-6-after, 2026, changelog, workspace.patch, golden, typo-fix.patch  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. ls results/lesson-6-after shows one folder named with a time; cd into it; cd changelog; mkdir ../../../../evals/golden; cp of the typo-fix trial's workspace.patch, over two lines, to ../../../../evals/golden/typo-fix.patch; cd ../../../.. back to practice.  
**Renderer:** terminal (tapes/s11.tape)

> First, we find our most recent run of the changelog eval, saved after the last edit to the skill.  _(finishes before typed:1)_
> There's one folder, named with the time of the run.  _(1s to read after; waits for output:1)_
> We change into it, and then into the folder for the eval.  _(finishes before typed:2)_
> The typo fix trial whose patch we just read is in here.  _(waits for done:3; finishes before typed:4)_
> So we make a folder named golden beside the eval file, and copy that trial's patch into it.  _(finishes before typed:4)_
> Then we go back up to the practice folder.  _(waits for done:5; finishes before typed:6)_

## s12

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders  
**On screen:** Headline 'Two lines, above graders'. The eval file panel from before, at the typo-fix stimulus: golden_patch: and its path lit together, just above graders:. Note on the right: 'added just above graders'.  
**Renderer:** html (scenes/s12.html)

> Next, we add those two lines to the typo fix stimulus in the eval file, just above graders.

## s13

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders  
**On screen:** Terminal in the practice folder. vally oracle on the typo-fix stimulus with --verbose, over two lines: a tick for the stimulus marked [oracle], a tick and evidence for each of its two graders, then PASSED. The screen is cleared out of sight. The same command with --no-golden-input: adds-an-entry 'failed as expected', no-made-up-number 'N/A', and a last line beginning 'baseline OK'. Each screen is held until it has been read.  
**Renderer:** terminal (tapes/s13.tape)

> Now the first test: the oracle on that one stimulus, with the golden patch applied.  _(finishes before typed:1)_
> What matters is the mark beside each grader.  _(finishes before enter:1)_
> Both graders pass the correct answer, each with its evidence, and the last line says passed.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> On the stimulus's line, the word oracle in brackets marks a run with the golden patch applied.  _(1s to read after; waits for output:1; depends on what the demo produced)_
> The warning on the first line is about scoring, and only says that every grader must pass.  _(1s to read after; waits for output:1; depends on what the demo produced)_
> Next, the second test: the same command, plus dash dash no golden input.  _(finishes before typed:2)_
> If the graders are sound, its last line begins baseline OK.  _(finishes before enter:2)_
> Adds an entry failed as expected: with nothing done, there's no entry for it to find.  _(3s to read after; waits for output:2; depends on what the demo produced)_
> No made up number is marked N/A, because it checks that something is absent.  _(2s to read after; waits for output:2; depends on what the demo produced)_
> Finally, the last line does begin baseline OK.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s14

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders · **Introduces:** mentions-unreleased  
**On screen:** Headline 'A grader that can't fail'. The eval file panel at the top of the typo-fix graders, now with five new lines: a file-contains grader named mentions-unreleased, with path CHANGELOG.md and value "Unreleased". Notes on the right: 'added on purpose, to be caught' and 'the starting changelog already has this word'. The name lights, then the value.  
**Renderer:** html (scenes/s14.html)

> Here's what a useless grader looks like, added on purpose, so we can watch the oracle catch it.
> This one is a file contains grader named mentions unreleased, and it looks for the word Unreleased in the changelog.
> The starting changelog already contains that word, so this grader can never fail.

## s15

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders  
**On screen:** Terminal in the practice folder. The same vally oracle command with --no-golden-input: a cross for the stimulus; mentions-unreleased marked 'passed without the golden solution (trivially passing)'; the other two graders as before; a last line beginning 'baseline PROBLEM'. Held until it has been read.  
**Renderer:** terminal (tapes/s15.tape)

> With that grader in place, we run the second test again.  _(finishes before typed:1)_
> This time there's a cross: mentions unreleased passed without the golden solution, and the oracle calls it trivially passing.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> The last line now begins baseline problem.  _(2s to read after; depends on what the demo produced)_
> Having seen it caught, we delete those five lines from the eval file.

## s16

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders · **Introduces:** security.patch, two-changes.patch, after-release.patch  
**On screen:** Headline 'Golden patches for the rest'. Dark box, left: the golden folder as a short tree, 'evals/golden/' with typo-fix.patch, security.patch, two-changes.patch, after-release.patch. Notes on the right, level with the three new files: 'a trial we read and judged correct'. Under it a line: 'refactor has none: its correct answer changes nothing'. The three new files light together, then the line about refactor.  
**Renderer:** html (scenes/s16.html)

> The other stimuli get golden patches the same way.
> For security, two changes, and after release, we pick a trial, copy its patch into the golden folder, and add the two lines to its stimulus.
> Each time, it's a trial whose patch we've read and judged correct, not one that merely passed.
> Refactor stays without one.

## s17

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders  
**On screen:** Terminal in the practice folder. vally oracle on the whole eval file with --verbose: four stimuli, each ending PASSED (the report just fills the screen, so the command and the first stimulus's heading scroll off). The screen is cleared out of sight. The same with --no-golden-input, over two lines: a longer report, whose end shows the last stimuli each ending 'baseline OK'. Each screen is held until it has been read.  
**Renderer:** terminal (tapes/s17.tape)

> Now both tests on everything, starting with the golden patches applied.  _(finishes before typed:1)_
> Each of the four stimuli it graded ends in passed.  _(5s to read after; waits for output:1; depends on what the demo produced)_
> Refactor isn't among them, because it has no golden patch to apply.  _(1s to read after; waits for output:1; depends on what the demo produced)_
> Then the same with nothing applied, so refactor takes part too.  _(finishes before typed:2)_
> This report is longer than the screen, so here's its end; all five of its stimuli finish with baseline OK.  _(4s to read after; waits for done:2; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** prove-your-graders  
**On screen:** Headline 'Grader by grader'. The table from before, now filled from the two reports of our run: adds-an-entry passed / failed as expected; no-made-up-number passed / N/A; adds-nothing not run: no golden patch / N/A; under-security, two-entries-in-place and entry-in-new-unreleased passed / failed as expected. The first column lights, then the 'failed as expected' cells, then the two N/A cells.  
**Renderer:** html (scenes/s18.html)

> Here are both reports, grader by grader.  _(3s to read after)_
> With its golden patch applied, every grader that ran has passed.  _(depends on what the demo produced)_
> Without it, four graders failed as expected, and two are marked N/A.  _(2s to read after; depends on what the demo produced)_

## s19 — What the oracle didn't test

**Role:** body · **Mode:** think · **Stage:** what-the-oracle-did-not-test  
**On screen:** Headline 'Two graders remain untested'. The same filled table. The four graders with 'passed' and 'failed as expected' light together; then the rows for no-made-up-number and adds-nothing, whose second column says N/A.  
**Renderer:** html (scenes/s19.html)

> So which graders have now been tested in both directions?
> Four have: they pass a correct answer, and fail an empty one.  _(depends on what the demo produced)_
> Two haven't: no made up number, and adds nothing.  _(depends on what the demo produced)_
> Both check that something is absent, and by marking them N/A, the oracle is saying honestly that an untouched file can't test them.
> Nothing so far has shown that the grader named no made up number would object when a number is invented.

## s20

**Role:** body · **Mode:** think · **Stage:** what-the-oracle-did-not-test  
**On screen:** Headline 'One correct answer each'. Two blocks side by side, no arrow: 'Tried · the one correct answer we chose' and 'Not tried · another correct answer, worded differently'. Each fills as it is named.  
**Renderer:** html (scenes/s20.html)

> There's a second limit.
> The oracle tested each grader against one correct answer, the one we chose.
> Another correct answer, worded differently, hasn't been tried.

## s21

**Role:** recap · **Stage:** what-the-oracle-did-not-test  
**On screen:** Headline 'What are the oracle's two tests?'. One block, 'vally oracle', which opens after the question and a pause into two parts: 'with the golden patch · plays an agent that got everything right · a healthy grader passes' and '--no-golden-input · plays an agent that did nothing · a healthy grader fails'. Each part lights as it is said.  
**Renderer:** html (scenes/s21.html)

> Before you go on: what are the two tests the oracle runs, and what does a healthy grader do in each?
> With the golden patch applied, it plays an agent that got everything right, and a healthy grader passes.  _(pause 2.5s first)_
> With no golden input, it plays an agent that did nothing, and a healthy grader fails.

## s22

**Role:** next · **Stage:** what-the-oracle-did-not-test  
**On screen:** 'Next: Check graders against saved trials' in the display serif. Below, the hand-off question: 'Can the graders be run on the answers you have already saved?' A note: 'Exercises are on the lesson page · Source: Vally docs, CLI: oracle'.  
**Renderer:** slide (scenes/s22.html)

> You can now keep a golden patch, and show that a grader passes a correct answer and fails an untouched file.
> But the oracle couldn't test the graders that check for absence, and it tried only one correct answer each.
> You have dozens of real answers saved, good and bad.
> Can the graders be run on those?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
