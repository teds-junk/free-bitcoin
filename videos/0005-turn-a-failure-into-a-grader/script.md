# Turn a failure into a grader — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0005-turn-a-failure-into-a-grader.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (lesson 5), 2026-11-10. Not narrated.

- Authored without a storyboard checkpoint (waived for storyboards that follow the lesson page).
- Not recorded yet. src/run/ holds a STAND-IN (the course's verified run); see src/run/PROVISIONAL.
  Every "outcome" sentence (s14, s15, s17, s18, s19, s20) is worded to that stand-in and must be
  checked against this video's own two runs; build-src/make-scenes.py asserts each stated count.
- Where the video differs from the page:
  - The page's piece-by-piece table of the regular expression is cut to one scene (s09) and the
    backslash explanation is dropped: the audience is programmers.
  - The page's step 1 (typing the graders into the eval file) and step 5 (adding the rules to the
    skill) are not typed on screen. The files are shown in panels (s08, s10, s16) and installed by
    the tapes' hidden setup from src/state/; the narration says so ("The graders are now in the eval
    file", "With the rules in the skill").
  - The page's shortened output block (the first FAIL block) is not shown: the run's output is longer
    than a screen, so the recording comes back on its end (last failures, model summary, last line).
  - s04's "10 of 10 passed, 5 with a made-up number" is the lesson 3 video's run, not a page claim.
  - Lesson 12 is not named ("Those wait until later"); lesson 7 is "Later, we'll run that test on
    purpose": lesson talk stays out of body scenes.
- The hook's three failure modes are the three stimuli the shipped eval file fixes. Check them
  against the failure list the lesson 4 video actually ends with.
- Cold read: done by the author, not an independent reader (a fork may not launch subagents).
<!-- /notes -->

## The story

**The question this video answers:** How do I make code decide whether a trial has one of these failures?  
**The viewer starts:** A professional programmer who knows the shell and regular expressions, and has watched the changelog-entry skill measured so far: one request on two models (claude-haiku-4.5 and gpt-5.6-terra), then five trials each, then six ordinary requests run without grading and read patch by patch. Knows skill, agent, model, eval, eval file, workspace, patch, stimulus, grader, trial and run; the vally eval command with -e, --model, --runs, --workers and --output-dir; vally lint; the results folder with a workspace.patch per trial; the words PASS, FLAKY, FAIL and ERROR; and that the eval file's one grader so far only looks for the words 'notes add', so it passed trials that made up a pull request number. Has a short written list of the skill's failure modes, each a named way its output goes wrong, among them: a made-up pull request number, an entry for a change users cannot see, and a security fix filed under Fixed. Has never written a grader, and does not know the diff graders.

1. **worth-having**: after this, the viewer can name the three habits that make a grader worth having
2. **diff-graders**: after this, the viewer can read a diff grader and predict which patches it passes
3. **measure-edit-measure**: after this, the viewer can count how often each failure happens before and after an edit to the skill, with one command each time
4. **what-the-counts-show**: after this, the viewer can show, with three graders and a count before and after, what one edit to the skill changed on each model

## s01 — Hand the reading to code

**Role:** hook · **Mode:** think · **Stage:** worth-having  
**On screen:** Headline 'Turn a failure into a grader' in the display serif. Three blocks in a row, no arrows, one per failure mode: 'A made-up pull request number', 'An entry for a change users can't see', 'A security fix filed under Fixed', each with the stimulus that showed it. Each fills in turn during the first sentence, then all rest.  
**Renderer:** html (scenes/s01.html)

> By now, we have a list of ways this skill goes wrong, and we found every one by going through patches.
> We could fix the skill now: add a rule, try it, and look at the result.
> But looking at the result means going through patches again, on both models, several times each, after every edit.
> Hardly anybody keeps that up.
> Here, you'll hand that work to code: one small grader for each failure, so that one command counts how often it happens, before an edit and after it.

## s02 — Three habits for graders

**Role:** body · **Mode:** think · **Stage:** worth-having  
**On screen:** Headline 'Grade the result, not the route'. Two blocks side by side, no arrow: 'The route · look in the file or search it, one edit or two' and 'The result · what the agent left behind: the patch'. The first fills as routes are named, the second on 'left behind'.  
**Renderer:** html (scenes/s02.html)

> Let's start with what makes a grader worth having: three habits.
> First, we grade the result, not the route.
> An agent can reach a correct changelog by many routes: opening the file or searching it, one edit or two.
> Any grader that insists on one route fails every good route we didn't think of.
> So we look at what the agent left behind.

## s03

**Role:** body · **Mode:** think · **Stage:** worth-having  
**On screen:** Headline 'One grader per failure mode'. A three-row table: 'Failure mode' and 'A grader named after it': a made-up pull request number → no-made-up-number; an entry for a change users can't see → adds-nothing; a security fix filed under Fixed → under-security. 'no-made-up-number' lights when it is said.  
**Renderer:** html (scenes/s03.html)

> Second, we write one grader for each failure mode, and name it after the failure.
> If a grader called no made-up number fails, you know what went wrong without opening a file.
> One grader that checks five things at once only tells you that something went wrong.

## s04

**Role:** body · **Mode:** think · **Stage:** worth-having  
**On screen:** Headline 'Can this grader fail?'. Left: a card 'The only grader so far' with its six lines from the eval file in a dark box. Right: one block with a large count from the five-trial run, '10 of 10 trials passed', and under it '5 of them with a made-up number'. The count fills on 'passed every trial'.  
**Renderer:** html (scenes/s04.html)

> Third, a grader has to be able to fail.
> So far we've had one grader, and it passed every trial, including the trials that made up a number.
> A grader that has never failed might be checking nothing.
> So the first time we run a new grader, we run it where we already know the failure happens.
> If it passes there, the grader is wrong.

## s05

**Role:** body · **Mode:** think · **Stage:** worth-having  
**On screen:** Headline 'Code first, where code decides'. Two blocks side by side: 'A pattern can decide · is there a made-up number? is there a Security heading?' and 'Beyond a pattern · is the entry written for the people who use the tool?'. Each fills as it is spoken.  
**Renderer:** html (scenes/s05.html)

> One more habit goes with those three: code does everything that code can decide.
> A pattern costs nothing to run, and it gives the same answer every time.
> Some qualities are beyond a pattern, such as whether an entry is written for the people who use the tool.
> Those wait until later.

## s06 — Graders that read the diff

**Role:** body · **Mode:** works · **Stage:** diff-graders · **Introduces:** diff-contains, diff-not-contains, diff-empty  
**On screen:** Headline 'Three graders read the patch'. Dark code box, left, three lines: diff-contains, diff-not-contains, diff-empty. Right, level with each: 'the patch contains it', 'the patch doesn't contain it', 'the agent changed nothing'. Each line lights as it is named.  
**Renderer:** html (scenes/s06.html)

> Those are the habits; here's what Vally gives us to follow them.
> Three of the failure modes on our list are about what the agent added to the changelog, or whether adding anything was right.
> The patch already holds exactly that, and Vally has three graders that look at it.
> Vally calls the patch the diff, which is another word for the same thing.
> Diff contains passes when the patch contains the text or pattern we give it.
> Diff not contains passes when the patch doesn't contain it.
> Finally, diff empty passes when the agent changed nothing at all.

## s07

**Role:** body · **Mode:** works · **Stage:** diff-graders · **Introduces:** workspace.patch, workspace.patch · gpt-5.6-terra  
**On screen:** Headline 'They see unchanged lines too'. File panel labelled 'workspace.patch · gpt-5.6-terra': the patch from a trial of the five-trial run, with a 'lines hidden' row above. '(#41)' on an unchanged line lights, with the note 'unchanged, still in the patch'; then the added entry line ending '(#42)', with the note 'added by the agent'.  
**Renderer:** html (scenes/s07.html)

> One thing to know before using them: these graders see the whole patch, including the unchanged lines around the change.
> Here's the patch from a trial that made up a number.
> This unchanged line happens to hold a pull request number, forty-one.
> It's in the patch, so a grader that looked for any number in brackets would find one in every trial.
> What matters is this line, the one the agent added.
> So a grader for made-up numbers has to look only at lines that begin with a plus.

## s08

**Role:** body · **Mode:** works · **Stage:** diff-graders · **Introduces:** changelog.eval.yaml, evals/changelog.eval.yaml  
**On screen:** Headline 'A value, or a pattern'. File panel labelled 'evals/changelog.eval.yaml', with a minimap, opening on the first stimulus, typo-fix. It scrolls to that stimulus's graders block. The name 'adds-an-entry' lights, then its value '"notes add"' with the note 'exact text'; then 'no-made-up-number', then its pattern with the note 'a regular expression'.  
**Renderer:** html (scenes/s08.html)

> Each of these graders takes a value, which is exact text, or a pattern, which is a regular expression.
> Here's the eval file we're going to run: three of the six stimuli we went through earlier, with graders at the end of each.
> Its first stimulus is the typo fix, and it gets two graders.
> The first asks whether the agent added an entry at all.
> Nothing in the starting changelog mentions notes add, so that text can only be in the patch if the agent wrote it.
> The second is the grader for made-up numbers, and it passes only if its pattern is found nowhere in the patch.

## s09

**Role:** body · **Mode:** works · **Stage:** diff-graders  
**On screen:** Headline 'An added line with a number'. Dark code box, left: the pattern on one line, then its four pieces one per line: (?m), ^\+, .*, \(#\d+\). Right, level with each piece: '^ matches at every line', 'a line that starts with +', 'anything', 'a hash and digits, in brackets'. Each piece lights as it is described; the whole pattern on the last sentence.  
**Renderer:** html (scenes/s09.html)

> Here's that pattern, a piece at a time.
> A caret and an escaped plus mean a line that starts with a plus: a line the agent added.
> The switch at the front makes the caret match at the start of every line, where it would otherwise match only the start of the whole patch.
> Then comes anything at all, and then a hash and digits in brackets.
> In words: an added line that contains a pull request number.

## s10

**Role:** body · **Mode:** works · **Stage:** diff-graders  
**On screen:** Headline 'One grader each for the rest'. The same file panel, 'evals/changelog.eval.yaml', opening on the refactor stimulus and its graders block, with the prompt lines shown as hidden. 'diff-empty' lights with the note 'passes only when nothing changed'. The panel scrolls to the security stimulus; its pattern lights with the note 'an added ### Security line'.  
**Renderer:** html (scenes/s10.html)

> The other two stimuli get one grader each.
> The refactor changes nothing for users, so the right result is no change to the changelog.
> Diff empty checks exactly that, and it takes no settings.
> For the security fix, the grader looks for an added line that starts with a Security heading.
> It passes when the agent has created a Security category.

## s11

**Role:** body · **Mode:** works · **Stage:** diff-graders · **Introduces:** vally lint  
**On screen:** Headline 'Every grader has to pass'. Three illustration rows for one trial of typo-fix, each with two boxes under the grader names adds-an-entry and no-made-up-number: tick tick 'the trial passes'; tick cross 'the trial fails'; cross tick 'the trial fails'. Below, in a dark box, 'scoring-defaults-applied' with the note 'lint's reminder of this rule'. The rows light in turn, then the warning's name.  
**Renderer:** html (scenes/s11.html)

> Once a stimulus has more than one grader, a trial passes only if every one of them passes.
> Vally lint prints a warning, named scoring defaults applied, to say that this rule is in force.
> It's the rule we want, so we expect the warning.

## s12 — Measure, edit, measure again

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure  
**On screen:** Headline 'A count before, a count after'. An empty table: rows typo-fix, refactor, security; under each model, claude-haiku-4.5 and gpt-5.6-terra, a 'before' and an 'after' column. The 'before' columns light, then the 'after' columns. The cells stay empty.  
**Renderer:** html (scenes/s12.html)

> That's how the graders work; now let's count with them.
> First, we run these three stimuli three times on each model, with the skill as it is.
> Then we add three rules to the skill, and run the same command again.
> Each time, we count how many of a stimulus's three trials passed, on each model.
> What would you expect the edit to change, on each model?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s13

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure · **Introduces:** -e  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. vally lint -e evals/changelog.eval.yaml prints one warning, scoring-defaults-applied, and '1 warning(s)'. Held until it has been read.  
**Renderer:** terminal (tapes/s13.tape)

> The graders are now in the eval file, so we lint it first, which costs nothing.  _(finishes before typed:1)_
> One warning, the one we expected, and no errors.  _(3s to read after; waits for output:1)_

## s14

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure · **Introduces:** vally eval, --model, --runs, --workers, --output-dir, lesson-5-before  
**On screen:** Terminal, continuing in the practice folder. The vally eval command over four lines, with --runs 3 --workers 2 and --output-dir results/lesson-5-before; a jump cut; then the end of the output: the last failures listed with their graders and evidence, the model summary, and the last line with a count for each model. Held until it has been read.  
**Renderer:** terminal (tapes/s14.tape)

> Now we measure the skill as it is: the command from before, with three runs of each stimulus, two at a time.  _(finishes before typed:1)_
> It spends eighteen short agent runs.  _(finishes before enter:1)_
> We're after the table at the end, which says, for each model, how many of the three stimuli passed in every trial.  _(finishes before enter:1)_
> About three minutes later, it says one of the three on haiku, and none on terra.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> Above that table, Vally lists each stimulus that didn't pass, with the grader that objected and its evidence.  _(5s to read after; waits for output:1; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure  
**On screen:** Headline 'The count before the edit'. The table from before, its 'before' columns filled from our run as 'n of 3'; the 'after' columns still empty. The typo-fix row lights, then the refactor and security rows.  
**Renderer:** html (scenes/s15.html)

> The same output says how many trials of each stimulus passed, and that fills in the first half of the table.
> On the typo fix, haiku passed three of three, and terra none.  _(depends on what the demo produced)_
> Neither model passed the refactor or the security fix, in any trial.  _(2s to read after; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure · **Introduces:** SKILL.md, changelog-entry/SKILL.md  
**On screen:** Headline 'Three rules, one per failure'. File panel labelled 'changelog-entry/SKILL.md', with a minimap, showing the end of the skill: its four original rules and the seven added lines. Each added rule lights as it is described.  
**Renderer:** html (scenes/s16.html)

> Next comes the edit to the skill.
> Each failure is a case the skill left open, so we add three rules at the end, one for each failure mode.
> The first covers a missing pull request number: the agent leaves the reference off, never makes one up, and doesn't stop to ask.
> In a Vally run nobody is there to answer a question, so we chose to leave it off.
> The second says that a change which makes no difference to users gets no entry.
> The third lists the categories in order, and puts a security fix under Security.

## s17

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure · **Introduces:** lesson-5-after  
**On screen:** Terminal in the practice folder. The same vally eval command, with --output-dir results/lesson-5-after; a jump cut; then the end of the output: the model summary with three of three for both models, nothing listed above it, and the Saved line.  
**Renderer:** terminal (tapes/s17.tape)

> With the rules in the skill, we measure again, the same way, into a second results folder.  _(finishes before typed:1)_
> That's another eighteen agent runs.  _(finishes before enter:1)_
> About three minutes later, the table says three of three, on both models.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> This time, no failures are listed above it: every trial of every stimulus passed.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** measure-edit-measure  
**On screen:** Headline 'Before and after, side by side'. The same table, now with both halves filled from our two runs. The terra typo-fix cells light, then the refactor row, then the security row, ending on haiku's 'after' cell.  
**Renderer:** html (scenes/s18.html)

> Here are both counts, side by side.
> The made-up number is gone on terra, the model that produced it.  _(depends on what the demo produced)_
> Neither model adds an entry for the refactor any more.  _(depends on what the demo produced)_
> The security rule worked every time, on both models.  _(3s to read after; depends on what the demo produced)_

## s19 — What the counts show

**Role:** body · **Mode:** think · **Stage:** what-the-counts-show  
**On screen:** Headline 'Same words, different effect'. Three blocks side by side, each a large count of trials passed after the edit: terra and haiku from our run (with the count before the edit under each), then haiku from an earlier run of the same edit. The two from our run light together, then the earlier one.  
**Renderer:** html (scenes/s19.html)

> So what do the counts show?
> One edit added three rules, and in our run, all three worked on both models.  _(depends on what the demo produced)_
> An earlier run of the same edit came out differently: haiku still filed one security fix under Fixed, and passed eight of nine.  _(depends on what the demo produced)_
> So the same words can have a different effect, on another model or on another run.
> Going through a couple of patches by hand might well have shown us only the trials where it worked.
> A count shows all of them, and one command will count again after the next edit.

## s20

**Role:** body · **Mode:** think · **Stage:** what-the-counts-show  
**On screen:** Headline 'Every grader failed first'. A four-row table from the first run: each grader's name and how many of its six trials it failed before the edit: adds-an-entry, no-made-up-number, adds-nothing, under-security. The count column lights on 'failed somewhere'.  
**Renderer:** html (scenes/s20.html)

> It's also worth a look at what the graders did in the first run.
> Every one of them failed somewhere, on the kinds of trial we already knew to be bad.  _(depends on what the demo produced)_
> That's a first piece of evidence that they check what we meant.
> Later, we'll run that test on purpose.

## s21

**Role:** recap · **Stage:** what-the-counts-show  
**On screen:** Headline 'What are the three habits?'. One block, 'a grader worth having', which opens after the question and a pause into three parts, each lit as it is said: 'Grade the result · not the route', 'One per failure mode · named after it', 'Able to fail · run it first where the failure is known'.  
**Renderer:** html (scenes/s21.html)

> Before you go on: what are the three habits that make a grader worth having?
> We grade the result the agent left, not the route it took.  _(pause 2.5s first)_
> We write one grader per failure mode, and name it after the failure.
> Last, we make sure each grader can fail, by running it first where the failure is known to happen.

## s22

**Role:** next · **Stage:** what-the-counts-show  
**On screen:** 'Next: Keep graders out of the agent's reach' in the display serif. Below, the hand-off question: 'Where can a script live so the agent cannot read or edit it?' A note: 'Exercises are on the lesson page · Source: Vally docs, Choose a Grader'.  
**Renderer:** slide (scenes/s22.html)

> You can now show, with a count before and after, what an edit to the skill changed on each model.
> Patterns caught three failures.
> Checking that nothing else in the file changed is beyond a pattern: it takes a script.
> Where can we keep a script, so that the agent can't open it or edit it?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
