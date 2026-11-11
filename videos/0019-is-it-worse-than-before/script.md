# Is it worse than before — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0019-is-it-worse-than-before.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (not narrated).

- Source: lessons/0019-is-it-worse-than-before.html, verified/lesson-19/output, NOTES.md ("From authoring
  lesson 19" and R18). Primary source: Vally docs, CLI: compare.
- Recorded 2026-11-11 on the series' own lesson 15 run (results/lesson-15/2026-11-11T07-53-29-176Z): s13
  (free), s14, s17, s18. One take each. No agent runs; 18 + 12 + 18 = 48 judge calls.
- Our run: haiku +0.33 [-0.08, +0.75] (4/4/1), tokens -13,685; terra 6 pairs (three terra-before trials
  ended in ERROR in lesson 15's third take), +0.07 [-0.25, +0.38], tokens -8,298, exit 0; swapped
  -0.33 [-0.75, +0.08], exit 0. The check did not fail in our run.
- The printed block is explained (s09 to s11) on the course's own earlier output (src/earlier/haiku.log),
  labelled on screen as an earlier run on other saved trials.
- Two of the page's points did not happen in our run and are shown as "an earlier run", from saved output:
  the pairwise range clearing zero (s20; src/earlier/haiku.log) and tokens rising while the check passed
  (s22; src/earlier/terra.log). The check failing once is also an earlier run (s11, s21; src/earlier/swapped.json).
- Our record has no pair that both versions failed, and no tie from the two orders disagreeing in the haiku
  record. s02, s03 and s15 use the dates trial 0 pair instead (both passed; the judge preferred the before
  entry), and s15 ends on parser trial 0 (the orders agreed on the winner, not the strength).
- The test's name, McNemar, is shown on screen (it is in Vally's output) and not spoken.
- Credential scans: s13, s14, s18 scanned in full, no hits. s17 partly scanned (the screen filled); all 12
  stills looked at, marked reviewed.
- The first cold read was the authoring worker's; an independent one followed and its findings are applied.
<!-- /notes -->

## The story

**The question this video answers:** Can a check tell me that a change made things worse, in quality or in cost, and fail when it did?  
**The viewer starts:** A professional programmer who knows the shell (exit codes included) and has followed the changelog-entry skill through eighteen lessons. Knows Vally's words: stimulus, grader, trial, run, eval file, experiment file, variant, baseline, results folder, results.jsonl and report.md. Knows an LLM judge with a rubric and a named judge model, a yes-or-no judge and a judge on a 1-to-5 scale, and that a judge is checked against our own labels. Has run the before-and-after experiment: four variants (haiku-before, haiku-after, terra-before, terra-after), three stimuli worded in coding terms (parser, cache, dates), three trials each, graded by the yes-or-no judge; and has put a range around a count of passing trials and seen that overlapping ranges cannot tell an edit's effect. Knows tokens per trial, cost per passing trial, and the budget graders that fail a trial that costs too much. Has never judged two answers side by side, and does not know vally compare, the words treatment, pairwise judge or win rate, or the --fail-on-regression option.

1. **side-by-side**: after this, the viewer can say what a pairwise judge is shown, why it notices smaller changes than a grader does, and why each pair is judged twice
2. **what-compare-reports**: after this, the viewer can go through the block vally compare prints, and predict its exit code from the mean score's range
3. **compare-before-and-after**: after this, the viewer can judge two saved runs side by side on each model, find one pair in the record, and check the exit code of a regression check
4. **what-it-supports**: after this, the viewer can say what a side-by-side comparison of two saved runs supports, in quality and in cost, and which of the two its exit code answers for

## s01 — Is it any worse?

**Role:** hook · **Mode:** think · **Stage:** side-by-side  
**On screen:** Headline 'Is it worse than before' in the display serif. Two blocks side by side for claude-haiku-4.5: trials that passed before the edit (5 of 9, with its range) and after it (9 of 9, with its range), from the record of our own run. Under them one line: 'trials that passed their graders, before and after one edit to the skill'. The before block lights, then the after block, then both clear.  
**Renderer:** html (scenes/s01.html)

> After one edit to the skill, the passing trials on one model went from five of nine to nine of nine, and the two ranges still overlapped.  _(depends on what the demo produced)_
> So those trials couldn't yet say the edit made things better.
> Before every change we keep, there's a narrower question: is it any worse than before?
> Here, you'll judge two saved runs side by side, and run a check that's built to fail when a change made things worse.

## s02

**Role:** body · **Mode:** think · **Stage:** side-by-side  
**On screen:** Headline 'Graders see one trial'. Two cards, one above the other, 'before the edit' and 'after the edit', each holding the changelog entry that version of the skill wrote for the same request in the same trial (dark box), with 'passed its graders' beside each label. The first card lights, then both 'passed' labels.  
**Renderer:** html (scenes/s02.html)

> Let's start with what our graders can't see.
> Each grader takes one trial at a time, and holds it against a fixed check.
> That can't answer a question like: is the new skill's entry better than the old one's?
> Here are two entries for the same request, and the graders passed both, so the difference between them disappears.  _(depends on what the demo produced)_
> A one-to-five scale has the same limit, since it places each entry by itself.

## s03

**Role:** body · **Mode:** think · **Stage:** side-by-side  
**On screen:** Headline 'Two answers, side by side'. The same two cards, now with one block under them titled 'pairwise judge': 'shown both answers to one request · says which is better, and by how much'. A note: 'Vally's docs call this comparison mode'. The judge block lights as it is defined, and again at the end.  
**Renderer:** html (scenes/s03.html)

> A pairwise judge works differently.
> It's an LLM judge that's shown two answers to the same request, one from each version, and says which is better, and by how much.
> Comparing two answers side by side is easier than scoring either one alone, for people and for models.
> That's why a pairwise judge notices smaller changes.

## s04

**Role:** body · **Mode:** think · **Stage:** side-by-side  
**On screen:** Headline 'Each pair is judged twice'. Four blocks in two rows. Top row: 'First order: before, then after' and 'Second order: after, then before'. Bottom row: 'Both orders agree: a score' and 'The orders disagree: a tie'. A source note: Zheng et al., Judging LLM-as-a-Judge (2023); Vally docs, CLI: compare. Each block lights as it is named.  
**Renderer:** html (scenes/s04.html)

> It has one well-known weakness.
> Shown two answers, a judge tends to prefer one position, often the first, whatever is in it.
> So Vally asks twice, with the two answers in the opposite order.
> When both orders agree, the pair gets that verdict.
> When they disagree, the pair is scored as a tie.

## s05

**Role:** body · **Mode:** think · **Stage:** side-by-side  
**On screen:** Headline 'Two questions, two tools'. Two blocks side by side: 'Graders · is it right?' and 'Pairwise judge · is it worse?'. The first lights, then the second.  
**Renderer:** html (scenes/s05.html)

> A pairwise judge doesn't replace graders.
> It can't say that both versions are wrong, only which one is less wrong.
> So graders stay for the question: is it right?
> The side-by-side judgement is for the other one: is it worse?

## s06 — What compare reports

**Role:** body · **Mode:** works · **Stage:** what-compare-reports · **Introduces:** vally compare, --baseline, --treatment, --judge-model, --output, haiku-compare.jsonl, haiku-before, haiku-after  
**On screen:** Headline 'Compare two saved runs'. Dark box, left: the vally compare command over five lines as the lesson prints it (--baseline haiku-before, --treatment haiku-after, --judge-model claude-sonnet-5.5, --output haiku-compare.jsonl). Callouts on the right, one per flag: 'the version to compare against', 'the version that changed', 'has to be named', 'a record of every pair'. Each flag lights as it is named.  
**Renderer:** html (scenes/s06.html)

> That's the idea; here's the command that does it.
> Vally compare runs a pairwise judge over two sets of saved trials, and adds up the result, without starting an agent.
> Its baseline is the version we compare against, and Vally's word for the version we changed is the treatment.
> Here, both are variants of our before-and-after experiment: one model, with the skill before the edit and after it.
> Next, the judge has to be named with dash dash judge model, because this command doesn't take it from the eval file, and its default may be a model under test.
> Finally, dash dash output names a file for a record of every pair.

## s07

**Role:** body · **Mode:** works · **Stage:** what-compare-reports · **Introduces:** terra-before, terra-after, results.jsonl, report.md  
**On screen:** Headline 'Two variants, not the folder'. Dark box, left: the experiment folder as a tree: the run's folder, then haiku-before, haiku-after, terra-before and terra-after, each holding results.jsonl, then report.md. Callouts: 'the experiment's baseline' beside haiku-before, 'another model' beside the terra folders, 'all compare needs' beside a results.jsonl. haiku-before lights, then the terra folders, then the two haiku folders, then results.jsonl.  
**Renderer:** html (scenes/s07.html)

> Vally compare can also be given a whole experiment folder.
> Then the baseline is the one the experiment file names, here haiku before, and every other variant is judged against it.
> That would set the terra variants against haiku, and mix a change of model into a question about the edit.
> So we'll name two variant folders instead, one model at a time.
> Each holds its own results dot jsonl, which is all compare needs.

## s08

**Role:** body · **Mode:** works · **Stage:** what-compare-reports  
**On screen:** Headline 'A verdict becomes a score'. A table of the five verdicts and their scores: much better +1.0, slightly better +0.4, equal or the two orders disagree 0, slightly worse −0.4, much worse −1.0. A note: 'pairs: the same stimulus and trial number from each version · two judge calls per pair'. The rows light in turn.  
**Renderer:** html (scenes/s08.html)

> Vally pairs the trials by stimulus name and trial number: trial zero with trial zero, and so on.
> For each pair, the judge works from the rubric saved with the trials, and gives a verdict from the treatment's side.
> Much better scores plus one, and slightly better, plus zero point four.
> Ties score zero.
> The worse verdicts mirror those, below zero.
> Each pair costs two judge calls, one for each order.

## s09

**Role:** body · **Mode:** works · **Stage:** what-compare-reports · **Introduces:** win rate  
**On screen:** Headline 'Win rate, then mean score'. Dark box, left: the first lines of the block compare printed in an earlier run of the course (haiku-after vs haiku-before): the win rate line and the mean score line, long lines wrapped. Callouts: 'pairs the treatment won', 'the average of the nine scores', 'its range'. A note: 'an earlier run of this command, on other saved trials · long lines wrapped'. The win rate lights, then the ties, then the mean, then the range.  
**Renderer:** html (scenes/s09.html)

> Here's what compare printed in an earlier run, on other saved trials.
> First, the win rate is the share of pairs that the treatment won: six of nine here.
> Ties count against it, so a win rate isn't the same as not worse.
> Next is the mean of the nine scores, with a range around it.
> That range is a confidence interval: the kind we put around a count, here around a mean, and the true mean is probably inside it.
> This one lies wholly above zero.

## s10

**Role:** body · **Mode:** works · **Stage:** what-compare-reports  
**On screen:** Headline 'A second test, and metrics'. Dark box, left: the rest of the same block: the 'Grader pass/fail (McNemar)' line, wrapped, then 'Metric deltas' with tokens, turns, tool calls, wall time and errors, each with its range. Callouts: 'McNemar’s test: graders only', 'pairs where only one version passed', 'could it be chance?', 'after minus before, per trial', 'the pairs differed a lot'. The same note as before. The flips light, then p, then the tokens line, then 'high variance'.  
**Renderer:** html (scenes/s10.html)

> Below that is a second test, and it ignores the judge.
> This test looks only at the graders' pass or fail, and counts the pairs that flipped: five went from fail to pass, and none the other way.
> You can see the test's name on that line, and it asks whether a split like five to nothing could easily be chance.
> From chance alone, a split that lopsided turns up about six times in a hundred.
> The usual bar for calling a result significant is under five in a hundred.
> So this one is not significant.
> Last come the metric changes: the treatment minus the baseline for each measure, averaged over the pairs, each with a range.
> The words high variance mean the pairs differed a lot from one another.

## s11

**Role:** body · **Mode:** works · **Stage:** what-compare-reports · **Introduces:** --fail-on-regression, echo  
**On screen:** Headline 'Exit one on a regression'. Top: a dark box with two lines, 'vally compare … --fail-on-regression' and 'echo $?', with callouts 'fail when the treatment is worse' and 'the last command's exit code'. Below: a table of three mean scores with their ranges and the exit code each gives with the option on: +0.53 [+0.17, +0.89] → 0; −0.20 [−0.55, +0.15] → 0; −0.49 [−0.90, −0.07] → 1. A note says which rows are earlier runs and which is an illustration. The option lights, then the third row, then the second, then nothing, then echo $?.  
**Renderer:** html (scenes/s11.html)

> One option turns compare into a regression check: dash dash fail on regression.
> With it, the command exits one when the treatment is significantly worse.
> That means its mean score is below zero, and its whole range is below zero too.
> So a negative mean isn't enough if the range reaches above zero.
> Nothing else counts: a rise in tokens doesn't change the exit code, and neither does the second test.
> Apart from that, with or without the option, compare exits one when some pair couldn't be judged, even after retries.
> To print the exit code, there's echo dollar question mark, typed straight after the command.

## s12 — Compare before and after

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after  
**On screen:** Headline 'Three comparisons, one check'. A table with a row for each comparison we are about to run (haiku: before → after; terra: before → after, check on; haiku: after → before, check on) and empty cells for the mean score and the exit code. Each row lights as it is named; then the empty exit-code column lights for the question, and holds.  
**Renderer:** html (scenes/s12.html)

> That's how compare works; now let's run it on the saved trials of our before-and-after experiment.
> First, the before skill against the after skill, on haiku.
> Then the same on terra, with the regression check on.
> Last, haiku again with the two roles swapped, so the before skill becomes the change under test.
> Which of the three would you expect the check to fail?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s13

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after · **Introduces:** cd, ls, lesson-15, 2026  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. cd into the experiment's folder under results/lesson-15 (its name, a time, is completed with Tab); ls shows one folder per variant beside report.md and the experiment's other files.  
**Renderer:** terminal (tapes/s13.tape)

> All three run from inside the experiment's folder, so we change into it.  _(finishes before typed:1)_
> Let's see what it holds.  _(waits for output:1; finishes before typed:2)_
> There's one folder for each variant, beside the experiment's report.  _(3s to read after; waits for output:2)_

## s14

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after  
**On screen:** Terminal, inside the experiment's folder. The vally compare command over five lines, haiku-before as the baseline and haiku-after as the treatment; a jump cut; then the printed block: win rate, mean score with its range, the grader flips, the metric changes, and the line saying the record was written. Held until it has been read.  
**Renderer:** terminal (tapes/s14.tape)

> First, haiku: the before skill as the baseline, and the after skill as the treatment.  _(finishes before typed:1)_
> It spends eighteen judge calls, two for each of nine pairs.  _(finishes before enter:1)_
> We're after the mean score, and whether its range clears zero.  _(finishes before enter:1)_
> About two minutes later, the treatment has won four of nine pairs, and the mean is plus zero point three three.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> Its range runs from minus zero point zero eight to plus zero point seven five, so it includes zero.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> On tokens, the range is wholly below zero: the after skill used about fourteen thousand fewer per trial.  _(3s to read after; waits for output:1; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after · **Introduces:** haiku-compare.jsonl · one record, spread out  
**On screen:** Headline 'Both passed, one judged better'. File panel labelled 'haiku-compare.jsonl · one record, spread out' with a minimap, callouts on the right. It opens on the top of the record (type, baseline, treatment), then scrolls to one pair: trialIndex, winner, magnitude and score light in turn; it scrolls on to the judge's reason, where one sentence lights, then to the two 'Passed' lines. A note says that in the reason A is the baseline and B the treatment, and quotes the second pair's reason. Then the panel scrolls to that second pair, and its magnitude line lights.  
**Renderer:** html (scenes/s15.html)

> The same command also wrote its record: one line of JSON, spread out here so we can go through it.
> This pair is the dates request, trial zero from each version.  _(depends on what the demo produced)_
> The pairwise judge found the after skill's entry slightly worse, for a score of minus zero point four.  _(depends on what the demo produced)_
> Its reason is kept too: the before entry adds an example date, which makes the change more concrete.  _(3s to read after; depends on what the demo produced)_
> On this same pair, both entries had passed their graders.  _(depends on what the demo produced)_
> In another pair, the two orders agreed on the winner but not on how much, so the record keeps the weaker verdict.  _(2s to read after; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after · **Introduces:** terra-compare.jsonl  
**On screen:** Terminal, inside the experiment's folder. The vally compare command over six lines, terra-before as the baseline, terra-after as the treatment, with --fail-on-regression and --output terra-compare.jsonl; a jump cut; then the printed block. Then echo $? prints the exit code under it.  
**Renderer:** terminal (tapes/s17.tape)

> Now the second model, with the regression check on, and a record file of its own.  _(finishes before typed:1)_
> On the result, there are two things to look at: the mean score's range, and the tokens line.  _(finishes before enter:1)_
> This time only six pairs were judged: three of the before trials did not finish, so their partners were left out, as the warning says.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> The judged score barely moved: three of the six are ties, and the range includes zero.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> The tokens fell, by about eight thousand per trial, with a range wholly below zero.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> So did the check fail?  _(finishes before typed:2)_
> Exit code zero: no regression in the judged score.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after  
**On screen:** Terminal, inside the experiment's folder. The vally compare command over five lines with the roles swapped: haiku-after as the baseline, haiku-before as the treatment, with --fail-on-regression; a jump cut; then the printed block. Then echo $? prints the exit code under it.  
**Renderer:** terminal (tapes/s18.tape)

> To see whether the check fails, we swap the two roles: the after skill is the baseline now, and the before skill is the change under test.  _(finishes before typed:1)_
> A consistent judge would print the first comparison's mean with its sign flipped: minus zero point three three.  _(finishes before enter:1; depends on what the demo produced)_
> This one printed exactly that, and its range reaches above zero.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> So what does the check make of that?  _(finishes before typed:2)_
> Exit code zero: the check passed, because the range isn't wholly below zero.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** compare-before-and-after  
**On screen:** Headline stating what the check did across the three runs (from our run: 'The check never failed'). The table from before, now filled from our three comparisons: mean score with its range, tokens per trial with its range, exit code. The exit-code column lights for the question, then the swapped row's mean and its exit code.  
**Renderer:** html (scenes/s19.html)

> Here are all three, side by side.
> So which of the three did the check fail?
> None of them, in our run.  _(depends on what the demo produced)_
> The swapped comparison came closest: its mean is below zero, but its range crosses it.  _(2s to read after; depends on what the demo produced)_

## s20 — What it supports

**Role:** body · **Mode:** think · **Stage:** what-it-supports  
**On screen:** Headline 'Three views, one answer'. Three blocks across, all for claude-haiku-4.5 in our run: trials passed (5, then 9, of 9; the two ranges overlap), grader flips (+4 / −0, p = 0.125, not significant), pairwise judge (+0.33, range −0.08 to +0.75, includes zero). Under them one line for an earlier run on other saved trials: pairwise +0.53, range +0.17 to +0.89, above zero. Each block lights as it is discussed, then the earlier run's line.  
**Renderer:** html (scenes/s20.html)

> So what does this support?
> Counting passes on haiku gave two ranges that overlapped, so the counts couldn't tell.  _(depends on what the demo produced)_
> The second test says the same: four pairs flipped from fail to pass, none flipped back, and it still calls that not significant.  _(depends on what the demo produced)_
> Its number is coin-toss odds: four tosses all landing the same way happen one time in eight.  _(depends on what the demo produced)_
> The pairwise judge leans the same way, with a mean above zero, but its range includes zero too.  _(depends on what the demo produced)_
> So in our run, all three agree: the edit looks better, and these trials can't yet show it.  _(depends on what the demo produced)_
> An earlier run, on other saved trials, went further: there the pairwise range was wholly above zero, while the counts still overlapped.
> A pairwise judge can do that, because it compares the two entries of each pair directly, and sees differences that pass or fail can't.

## s21

**Role:** body · **Mode:** think · **Stage:** what-it-supports  
**On screen:** Headline 'Hold that loosely'. A table of the swapped comparison (haiku-after as the baseline) run three times: two earlier runs of the course on the same saved trials, −0.49 [−0.90, −0.07] with exit code 1 and −0.38 [−0.78, +0.02] with exit code 0, and ours on our own trials. A note: 'the same command each time'. The two earlier rows light together, then our row, then nothing.  
**Renderer:** html (scenes/s21.html)

> Hold that loosely, for three reasons.
> First, the nine pairs aren't nine independent requests: they're three stimuli, tried three times each.
> So the range looks narrower than the evidence really allows.
> Next, the judge is a model, and this pairwise judge hasn't been checked against our own labels, the way the yes-or-no judge was.
> Third, it varies from one run to the next.
> Two earlier runs of the swapped comparison, both on the same saved trials, landed on both sides of the line: one failed the check, and one passed it.
> Our own run passed it too, with a range that reaches above zero.  _(depends on what the demo produced)_
> So trust the sign, and whether the range crosses zero, not the second decimal.

## s22

**Role:** body · **Mode:** think · **Stage:** what-it-supports  
**On screen:** Headline 'The check ignores cost'. Three blocks across for gpt-5.6-terra: 'Ours' (tokens per trial −8,298, range below zero), 'An earlier run' (tokens per trial +11,132, range +665 to +21,599, above zero), and that earlier run's exit code (0). Ours lights, then the earlier run's tokens, then its exit code, then nothing.  
**Renderer:** html (scenes/s22.html)

> Now the other half of the question: worse in cost.
> In our run, the edit made nothing cost more: tokens fell on both models.  _(depends on what the demo produced)_
> In an earlier run, on other saved trials, the after skill took about eleven thousand more tokens per trial on terra, with a range wholly above zero, and the check still exited zero.
> That's by design: the check looks at the judged score alone.
> So cost needs a guard of its own: the budget graders, with their limits set from the before trials.
> Then an edit that costs more fails a trial, like any other grader's failure.

## s23

**Role:** body · **Mode:** works · **Stage:** what-it-supports · **Introduces:** --compare, vally experiment  
**On screen:** Headline 'One reports, one can fail'. Dark box, left, two lines: 'vally experiment run … --compare' and 'vally compare <folder> --fail-on-regression'. Callouts: 'judges every variant against the baseline, and reports' and 'the step that can fail'. A source note: Vally docs, Run Your First Experiment. Each line lights as it is named.  
**Renderer:** html (scenes/s23.html)

> One last piece of how this works: an experiment can run the same judging as soon as it ends, with dash dash compare.
> That option only reports: a regression it finds doesn't fail the command.
> Vally's own guide gives the order: run the experiment, then run compare on its folder with fail on regression, as the step that can fail.

## s24

**Role:** recap · **Stage:** what-it-supports  
**On screen:** Headline 'When does the check fail?'. One block, 'exit code 1, with --fail-on-regression', which opens after the question and a pause into three parts, each lit as it is said: 'Mean score below zero', 'Whole range below zero', 'Not counted: tokens, grader flips'.  
**Renderer:** html (scenes/s24.html)

> Before you go on: what has to be true for the regression check to exit one?
> First, the treatment's mean score is below zero.  _(pause 2.5s first)_
> Second, its whole range is below zero too.
> Nothing else that compare prints counts.

## s25

**Role:** next · **Stage:** what-it-supports  
**On screen:** 'Next: When a run goes wrong' in the display serif. Below, the hand-off question: 'When a run goes wrong, where do you look first?' A note: 'Exercises are on the lesson page · Source: Vally docs, CLI: compare'.  
**Renderer:** slide (scenes/s25.html)

> You can now judge two saved runs side by side, and run a check that fails on a regression.
> At this point there are many moving parts, and runs sometimes end in error, or fail for reasons that aren't the skill.
> When a run goes wrong, where do you look first?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
