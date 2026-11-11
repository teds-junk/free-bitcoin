# Partial credit — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0014-partial-credit.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (not narrated).
- Sources: Vally docs, Scoring; Grader: prompt. Husain, Using LLM-as-a-Judge, and Anthropic, Demystifying evals for AI agents (2026-01-09), are shown on screen in s04 and not named in the narration. No person is named in the narration.
- The cold read was done by the authoring agent itself, not by a fresh reader (a fork cannot launch one).
- src/run/ is this video's own run: the lesson 12 video's twelve trials (run 2026-11-11T06-48-30-514Z), our labels and the yes-or-no verdicts from the lesson 13 video, and the logs of s15, s16 and s19 as recorded on 2026-11-10 (one take each, no errors, 12 judge calls in s16 and 12 in s19). build-src/make-scenes.py asserts every outcome sentence against them.
- s24 and s25 rest on this video's own run: one entry got a 4 in s16 and a 3 in s19, and a yes-labelled entry got a 4 with a reason outside the rubric. Nothing is reported from an earlier run. The lesson page's own figures (a 4 eight times and a 3 four times across three runs) are not used.
- In our run the yes-or-no judge and our labels disagree on one entry (terra's second cache entry: we said no, the judge yes), so one verdict changed against the yes-or-no judge while two entries we labelled no pass the 1-to-5 judge. The page's run had 6 no labels and full agreement.
- Left out from the page's checkpoint: the two "cd ../../.." returns. The edits the page makes in a text editor (the scale and threshold lines, adding and removing the scoring block, the notes column and sentence) are applied by the tapes out of sight and shown in panels (s07, s10, s21).
- The page's in-section quiz (a failing judge and two passing checks under a threshold with no weights) is used in s09 as the worked example for that rule.
- Judge calls: 12 in s16 and 12 in s19. No agent runs.
<!-- /notes -->

## The story

**The question this video answers:** How do I grade work that can be partly right, without letting a failure hide in an average?  
**The viewer starts:** A professional programmer who knows the shell and has followed the course's running example: the changelog-entry skill, measured on claude-haiku-4.5 and gpt-5.6-terra. Knows stimulus, grader and trial; diff graders such as diff-contains; that a trial passes only if every grader on its stimulus passes, and that vally lint prints a warning named scoring-defaults-applied to say so; vally lint with -e; vally grade, which applies an eval file's current graders to the trials saved in a run folder without starting an agent, with -e, --run-dir, --verbose and the run's results.jsonl on its input. Knows what an LLM judge is: the prompt grader, which gives a judge model the stimulus's rubric and the trial's evidence and records a verdict with a reason; the judge's config has scoring set to binary, and its prompt asks it to begin its reason by quoting the new entry. Has a yes-or-no judge with a one-criterion rubric (the new changelog entry says what changes for people who use the tool, and does not say how it was coded) in evals/wording.eval.yaml, beside a diff-contains check that the entry cites its pull request. Has twelve saved trials of three requests (parser, cache, dates) in a run folder under results/lesson-12, a notes file notes/wording-labels.md with our own yes or no for each entry (a label) and the judge's verdict beside it, and the judge's TPR and TNR against those labels. Has never seen a scoring block, weights, a threshold, or a judge that answers on a scale.

1. **when-a-score-helps**: after this, the viewer can say which kind of check can be partly right and is worth a scale, and which kind has no nearly and must stay pass or fail
2. **scores-to-a-verdict**: after this, the viewer can predict a trial's verdict from its graders' scores, with no scoring block and with weights and a threshold
3. **judge-on-a-scale**: after this, the viewer can turn a judge's answer from 1 to 5 into its score and its tick or cross, and work the answer out from a trial's score line
4. **score-the-wording**: after this, the viewer can re-grade saved trials with a judge that scores 1 to 5 against a threshold, put each score beside the yes-or-no verdict and the label, and watch an average pass a failure
5. **what-the-scores-showed**: after this, the viewer can say which verdicts changed from the yes-or-no judge, whether our labels agree, and why a pass-or-fail check stays out of an average

## s01 — When a score helps

**Role:** hook · **Mode:** think · **Stage:** when-a-score-helps  
**On screen:** Headline 'Partial credit' in the display serif. Two cards side by side, each labelled with its stimulus and model and 'our label: no · the judge: no', each holding one entry from our run in a dark box: on the left one that says how the change was coded, on the right one that leads with what users notice. The left card lights, then the right; then the highlight clears.  
**Renderer:** html (scenes/s01.html)

> Our judge said no to four of the twelve entries, and we said no to five.  _(depends on what the demo produced)_
> Here are two of them.
> One says outright how the change was coded.  _(depends on what the demo produced)_
> The other starts with what users notice, and only hints at how.  _(depends on what the demo produced)_
> Both got the same no, and a yes or no can't tell them apart.
> Here, you'll give the judge a scale, and see how an average can let a failure pass.

## s02

**Role:** body · **Mode:** think · **Stage:** when-a-score-helps  
**On screen:** Headline 'A scale shows how far off'. Two blocks side by side, no arrow: 'Did it pass? · a yes or no' and 'How far off is a failure? · a scale'. The first fills while the yes-or-no is discussed, the second when the scale is.  
**Renderer:** html (scenes/s02.html)

> Let's start with when a score is worth having.
> We asked the judge for a yes or no on purpose: a yes-or-no criterion has to be clear, and the difference between a three and a four rarely is.
> That still holds for the question, did it pass?
> A scale is worth adding when the work really can be partly right, and you want to know how far off a failure is.
> Wording is like that: an entry can be mostly for users, with one word of implementation in it.

## s03

**Role:** body · **Mode:** think · **Stage:** when-a-score-helps · **Introduces:** threshold  
**On screen:** Headline 'Some checks have no nearly'. A quote card labelled 'Vally docs, Scoring' with the sentence quoted from the docs about thresholds. Under it two blocks side by side: 'Can be partly right · the wording of an entry' and 'No nearly · cites its pull request · filed under Security'. The second block fills first, then the quote, then the highlight clears.  
**Renderer:** html (scenes/s03.html)

> Other checks aren't like that.
> An entry either cites its pull request or it doesn't, and a security fix is either under Security or it isn't.
> For these there's no nearly: a skill that gets one wrong has failed, however good everything else is.
> Vally's docs draw the same line: a threshold, meaning a pass mark on a score, is for work that's genuinely graded, not for pass-or-fail checks.
> So we keep checks that must all hold out of any score that gets averaged.

## s04

**Role:** body · **Mode:** think · **Stage:** when-a-score-helps  
**On screen:** Headline 'Where the sources agree'. Two blocks side by side, each a position with its source under it: 'Yes or no, throughout · Husain, Using LLM-as-a-Judge' and 'Partial success is a range · Anthropic, Demystifying evals for AI agents (2026)'. Under them one line: 'Both: a clear line for pass or fail, checked against your own labels.' Each block fills as its position is said, then the line lights.  
**Renderer:** html (scenes/s04.html)

> The sources we rely on differ about scales.
> One argues for yes-or-no judges throughout, and another treats partial success as a range worth recording.
> They agree on the part that matters here: whatever the scale, you still decide pass or fail with a clear line, and you check that line against your own labels.

## s05 — From scores to a verdict

**Role:** body · **Mode:** works · **Stage:** scores-to-a-verdict · **Introduces:** scoring block  
**On screen:** Headline 'Every grader gives a score'. Three blocks in a row, no arrows: 'a grader · a pass or a fail, and a score from 0 to 1'; 'diff-contains · passes: 1 · fails: 0'; 'a trial · one score, from its graders’ scores'. Each fills as it is named.  
**Renderer:** html (scenes/s05.html)

> That's when a score helps; now, here's how Vally turns grader results into a verdict.
> Every grader gives a score between zero and one, as well as a pass or a fail.
> A pass-or-fail grader, such as diff contains, scores one when it passes and zero when it fails.
> For each trial, Vally combines its graders' scores into one score.
> What decides the trial's verdict depends on one optional part of the eval file, called the scoring block.

## s06

**Role:** body · **Mode:** works · **Stage:** scores-to-a-verdict  
**On screen:** Headline 'No block: every grader must pass'. Dark box, left: the warning vally lint prints for the judge's eval file, as it printed in our run, wrapped. Callouts on the right, level with 'equal weights, no threshold' ('the score is a plain average') and with 'any single failing grader fails the stimulus' ('so the score decides nothing').  
**Renderer:** html (scenes/s06.html)

> With no scoring block, which is what every eval file so far has had, every grader must pass.
> Vally still works out a score, the plain average of the graders' scores, and prints it, but that score decides nothing.
> Lint's familiar warning is saying exactly that.

## s07

**Role:** body · **Mode:** works · **Stage:** scores-to-a-verdict · **Introduces:** wording-scaled.eval.yaml, scoring, weights  
**On screen:** Headline 'Weights and a threshold decide'. File panel labelled 'wording-scaled.eval.yaml' with a minimap, opened at the end of the file: a 'lines hidden' row for the three stimuli above, then the five lines of the scoring block. Callouts on the right: 'by grader type, not by name' (weights), 'the judge' (prompt: 0.5), 'the pull request check' (diff-contains: 0.5), 'the score a trial must reach' (threshold: 0.6). Each line lights as it is said.  
**Renderer:** html (scenes/s07.html)

> Here's the scoring block we'll add later, at the end of a copy of our judge's eval file, where it applies to every stimulus in the file.
> Weights say how much each grader type counts towards the trial's score.
> They're keyed by the grader's type, not its name: prompt is the judge, and diff contains is the check that the entry cites its pull request.
> Here, the two count equally.
> The threshold is the score, from zero to one, that a trial must reach to pass.
> With this block, a trial passes when its weighted score reaches the threshold, whatever any single grader said.
> Sixty percent sounds like a fair bar; we're using it to show what goes wrong, not as advice.

## s08

**Role:** body · **Mode:** works · **Stage:** scores-to-a-verdict  
**On screen:** Headline 'A strong score carries a failure'. Dark box, left: three lines of arithmetic, '0.5 × 0.25', '0.5 × 1', '= 0.625'. Callouts on the right: 'the judge: failed', 'the pull request check: passed', 'reaches 0.6: the trial passes'. Each line lights as it is said.  
**Renderer:** html (scenes/s08.html)

> Two rules follow from the arithmetic, and each lets an average hide a failure.
> First, a strong score on one grader can carry a failure on another.
> In this trial, the judge fails with a score of a quarter, and the pull request check passes with a score of one.
> The trial's score comes to zero point six two five, which reaches the threshold, so the trial passes.
> The judge's failure is still printed with a cross; it just no longer decides the verdict.

## s09

**Role:** body · **Mode:** works · **Stage:** scores-to-a-verdict  
**On screen:** Headline 'A missing type stops counting'. Two cards side by side, each a label over a dark box holding a short scoring block. Left, 'The judge left out of the weights': weights with only 'diff-contains: 1'; under it 'the judge is called, and changes nothing'. Right, 'A threshold with no weights': 'threshold: 0.6'; under it the three graders and their scores, 'a yes-or-no judge fails: 0 · two checks pass: 1 and 1', then '(0 + 1 + 1) ÷ 3 = 0.67 · reaches 0.6'. Under both, a quote card labelled 'Vally docs, Scoring': 'Omitting a type silences it, so list every type you care about.' The left card lights, then the quote, then the right card.  
**Renderer:** html (scenes/s09.html)

> Second, a grader type that's left out of the weights stops counting: its weight is taken as zero.
> With diff contains alone in the weights, the judge would still be called and paid for, and its verdict would change nothing.
> The docs put it plainly: omitting a type silences it.
> A threshold with no weights at all takes the plain average of every grader.
> Here's a stimulus with three graders: a yes-or-no judge, and two checks.
> The judge fails, which for a yes-or-no judge is a score of zero, and both checks pass.
> The average is zero point six seven, which reaches zero point six, so the judge is outvoted.

## s10 — A judge on a scale

**Role:** body · **Mode:** works · **Stage:** judge-on-a-scale · **Introduces:** scale_1_5  
**On screen:** Headline 'The judge answers one to five'. File panel labelled 'wording-scaled.eval.yaml' with a minimap, opened at the first stimulus's graders: the prompt grader and its config, with 'lines hidden' rows above and below. Callouts on the right: 'how the judge answers' (scoring: scale_1_5) and 'the judge’s own threshold' (threshold: 0.75). The scoring line lights, then the threshold line.  
**Renderer:** html (scenes/s10.html)

> That's the scoring block; next, here's a judge that can score between zero and one.
> The judge is the prompt grader, and its config has a scoring setting, which so far we've set to binary: a yes or a no.
> That setting has two other values: scale one to five, which is also what a judge does when the setting is left out, and scale one to ten.
> We'll give ours scale one to five.
> It's a different thing from the scoring block: this setting sits inside the judge's config, and changes only how the judge answers.
> Beside it goes a threshold of the judge's own.

## s11

**Role:** body · **Mode:** works · **Stage:** judge-on-a-scale  
**On screen:** Headline 'Five answers, rescaled'. Five blocks in a row, one per answer: '1 · 0', '2 · 0.25', '3 · 0.5 · the default threshold', '4 · 0.75 · our threshold', '5 · 1'. Under them one line: 'the judge passes when its score reaches its threshold'. Block 1 lights, then 5, then 3 for the default, then 4 for ours.  
**Renderer:** html (scenes/s11.html)

> On this scale, the judge gives each rubric criterion a whole number from one to five.
> Vally rescales that number to the range zero to one, so it can be combined with other graders' scores.
> A one becomes zero, a five becomes one, and each step is a quarter.
> The judge passes when its rescaled score reaches its own threshold.
> Left out, that threshold is a half, which means a three passes.
> Ours is zero point seven five, so the judge has to give at least a four.

## s12

**Role:** body · **Mode:** works · **Stage:** judge-on-a-scale  
**On screen:** Headline 'Two thresholds, two jobs'. Two blocks side by side: 'no scoring block · the judge’s own threshold decides: a cross fails the trial' and 'with a scoring block · only the judge’s score counts; the block’s threshold decides'. Each fills as it is said.  
**Renderer:** html (scenes/s12.html)

> So there are two thresholds, and it matters which one decides.
> With no scoring block, the judge's own threshold decides: it sets the judge's tick or cross, and a cross fails the trial.
> With a scoring block, only the judge's score goes into the trial's score, and the judge's own threshold stops deciding the verdict.

## s13

**Role:** body · **Mode:** works · **Stage:** judge-on-a-scale · **Introduces:** vally grade, --verbose  
**On screen:** Headline 'The score line gives it away'. A table with three columns, 'Score line', 'The judge’s score', 'The judge’s answer', and five rows: 100% · 1 · 5; 87.5% · 0.75 · 4; 75% · 0.5 · 3; 62.5% · 0.25 · 2; 50% · 0 · 1. A note under it: 'when the pull request check passes and scores 1'. The first row lights, then the second, then the last.  
**Renderer:** html (scenes/s13.html)

> There's one thing to know before the output appears.
> Vally grade prints a reason and a tick or cross for the judge, and a score line for the trial, but not the judge's own number.
> In our trials, every pull request check passes and scores one, so the trial's score is the average of one and the judge's score.  _(depends on what the demo produced)_
> That means the judge's answer can be worked out from the score line: a hundred percent is a five, eighty-seven point five is a four, and so on down to fifty percent for a one.
> If a trial's check failed, this table wouldn't apply.

## s14 — Score the wording

**Role:** practice · **Mode:** use · **Stage:** score-the-wording  
**On screen:** Headline 'Which verdicts will change?'. A table of our twelve entries, one row each, the five we labelled no first: stimulus and model, the entry (shortened, with an ellipsis), the yes-or-no judge's verdict, our label, and an empty last column headed '1 to 5'. The two verdict columns light together when the agreement is mentioned; the empty column lights on the question; then the scene holds.  
**Renderer:** html (scenes/s14.html)

> That's how the scale works; now let's score our twelve entries with it.
> We'll copy the judge's eval file, put the judge on the scale, and re-grade the twelve saved trials.
> No agent starts; the cost is twelve judge calls.
> The yes-or-no judge agreed with eleven of our twelve labels.  _(depends on what the demo produced)_
> Which of these verdicts would you expect to change, with a judge that has to give at least a four?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s15

**Role:** practice · **Mode:** use · **Stage:** score-the-wording · **Introduces:** cp, vally lint, -e, wording.eval.yaml  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. cp copies evals/wording.eval.yaml to evals/wording-scaled.eval.yaml, typed over two lines. The screen is cleared out of sight; vally lint on the copy prints the scoring-defaults-applied warning and '1 warning(s)', held until it has been read.  
**Renderer:** terminal (tapes/s15.tape)

> First, we copy the judge's eval file, so that the original stays as it is for later.  _(finishes before typed:1)_
> In the copy, the name becomes wording scaled, and each of the three judges gets the two lines we looked at: the scale, and a threshold of zero point seven five.  _(waits for done:1)_
> Lint checks the copy before anything is spent.  _(finishes before typed:2)_
> It prints the familiar warning, and no errors.  _(3s to read after; waits for output:2; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** score-the-wording · **Introduces:** cd, --run-dir, results.jsonl, lesson-12, 2026  
**On screen:** Terminal, continuing in the practice folder. cd into the run folder under results/lesson-12, its name completed with Tab; the prompt becomes the run folder's name. The vally grade command over three lines, as the lesson prints it; a jump cut; then the end of the output: the last blocks, each with the judge's line, the check's line and a Score line, held until it has been read.  
**Renderer:** terminal (tapes/s16.tape)

> The twelve saved trials are in their run folder, so we change into it.  _(finishes before typed:1)_
> Then we re-grade them with the copy, and the verbose flag asks for each grader's line.  _(waits for output:1; finishes before typed:2)_
> Each block will end in a score line.  _(finishes before enter:2)_
> A little later there are twelve blocks, one for each trial, and these are the last of them.  _(9s to read after; waits for output:2; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** score-the-wording  
**On screen:** Headline 'One block, one score'. Dark box, left: one block of the output from our run, word for word and wrapped: its name, the line saying one of two graders passed, the judge's line with a cross and its reason, the check's line with a tick, and 'Score: 62.5% | FAILED'. Callouts on the right, level with the judge's line ('the judge: a cross, and a reason'), the check's line ('the check: a tick, so 1') and the score line ('62.5% · the judge answered 2'). Under the box, the score-line table from before as one strip: 100% · 5, 87.5% · 4, 75% · 3, 62.5% · 2, 50% · 1; its 62.5% column lights with the score line. Each lights as it is said.  
**Renderer:** html (scenes/s17.html)

> Here's one of those blocks in full.
> The judge's line has a cross, and its reason quotes the entry.  _(depends on what the demo produced)_
> The pull request check has a tick.  _(depends on what the demo produced)_
> And the score line says sixty-two point five percent, which, in the table, is a judge's answer of two.  _(depends on what the demo produced)_
> A two is below the judge's threshold, so the judge fails, and the trial fails with it.  _(2s to read after; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** score-the-wording  
**On screen:** Headline 'The same twelve, scored'. The table from before in the same place, its '1 to 5' column now filled from our run; the one row whose verdict differs from the yes-or-no judge's says 'passes' beside its score. The three twos light together, then the scores of the entries we labelled yes, then the two entries that only hint at how, then the word 'passes'.  
**Renderer:** html (scenes/s18.html)

> The blocks don't name the model or the trial, so we match each one to its row by the entry its reason quotes.
> Then each score goes beside the yes-or-no verdict and our label.
> The three entries that say how the change was coded all got a two.  _(depends on what the demo produced)_
> The entries we labelled yes got fours and fives.  _(depends on what the demo produced)_
> The two entries that only hint at how both got a four.  _(depends on what the demo produced)_
> At our threshold a four passes, so both now pass, and since the yes-or-no judge had failed one of them, one verdict has changed.  _(depends on what the demo produced)_
> We had labelled both no.  _(3s to read after; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** score-the-wording  
**On screen:** Terminal in the practice folder. vally lint on the copy now prints that the file is valid, with no warning. cd into the run folder again; the same vally grade command; a jump cut; then the end of the output: the last blocks, each Score line now ending with '(threshold: 60.0%)', held until it has been read.  
**Renderer:** terminal (tapes/s19.tape)

> Now for the average: we put the scoring block from before at the end of the copy, with half the weight on the judge, half on the check, and a threshold of zero point six.  _(finishes before typed:1)_
> Lint now says the file is valid, and the warning has gone, because the file says how to combine its graders.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Then it's the same re-grade, in the same run folder, for twelve more judge calls.  _(finishes before typed:2)_
> This time, each score line ends with the threshold.  _(waits for output:2; finishes before enter:3)_
> These last blocks have passed, and so has every block above them.  _(9s to read after; waits for output:3; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** score-the-wording  
**On screen:** Headline 'A cross inside a pass'. Dark box, left: one block of the second output from our run, word for word and wrapped: a tick beside the trial's name with '1/2 graders passed, 1 failed', the judge's line with a cross and its reason, the check's line with a tick, and 'Score: 62.5% | PASSED (threshold: 60.0%)'. Callouts on the right: 'the judge still fails it' (the judge's line), 'the trial passes' (the first line) and '0.5 × 0.25 + 0.5 × 1 = 0.625' (the score line). Each lights as it is said.  
**Renderer:** html (scenes/s20.html)

> Here's one of the twelve.
> The judge's line still has a cross, and a reason that faults the entry.  _(depends on what the demo produced)_
> But the trial has a tick.  _(depends on what the demo produced)_
> The judge's two rescales to a quarter, the check adds a full one, and half of each comes to zero point six two five, which reaches the threshold.  _(depends on what the demo produced)_
> Four of the twelve passed this way, with a cross from the judge inside.  _(2s to read after; depends on what the demo produced)_

## s21

**Role:** practice · **Mode:** use · **Stage:** score-the-wording · **Introduces:** notes/wording-labels.md, wording-labels.md  
**On screen:** Headline 'Put back, and written down'. File panel labelled 'notes/wording-labels.md' with a minimap: the table's heading row with its new last column, '1 to 5', lit; then the panel scrolls to the end of the file, where the one sentence we added lights.  
**Renderer:** html (scenes/s21.html)

> Last, we take the scoring block out of the copy again.
> The scores go into our notes file as a new column.
> Under the table goes one sentence.
> One verdict changed between the two judges.  _(depends on what the demo produced)_
> Against our twelve labels, the one-to-five judge has TPR seven of seven.  _(depends on what the demo produced)_
> Its TNR is three of five.  _(2s to read after; depends on what the demo produced)_

## s22 — What the scores showed

**Role:** body · **Mode:** think · **Stage:** what-the-scores-showed  
**On screen:** Headline 'Close, or far off'. Two cards side by side, each a label over a dark box of entries from our run. Left, 'far off · the judge answered 2': the three entries that say how the change was coded. Right, 'close · the judge answered 4': the two entries that start with what users notice. The left card lights, then the right, then the left again.  
**Renderer:** html (scenes/s22.html)

> So what did the scores show?
> For one thing, the scale did show which failures were close, and which were far off.
> These entries say how the change was coded.  _(depends on what the demo produced)_
> These start with what users notice.  _(depends on what the demo produced)_
> If we were choosing what to fix in the skill, the entries that are far off say where to start.

## s23

**Role:** body · **Mode:** think · **Stage:** what-the-scores-showed  
**On screen:** Headline 'A threshold is a decision'. Three blocks in a row, each a judge with its TNR against our five no labels, from our run: 'the yes-or-no judge · TNR 4 of 5'; '1 to 5, threshold 0.75 · TNR 3 of 5'; '1 to 5, default threshold 0.5 · TNR 3 of 5'. Under them one line: 'The same check as before: its verdicts against our labels.' The first two blocks light in turn as TNR falls, then the third, then the line.  
**Renderer:** html (scenes/s23.html)

> The scale also changed a verdict, and not for the better.
> With the judge's threshold at zero point seven five, two entries passed that we had labelled no, so TNR fell from four of five to three of five.  _(depends on what the demo produced)_
> At the default threshold of a half, a three would pass as well; in this grading no entry got one, so the count is the same.  _(depends on what the demo produced)_
> A threshold is a decision about where good enough starts.
> The way to know whether it sits where you'd put it is the same check as before: compare its verdicts with your labels.

## s24

**Role:** body · **Mode:** think · **Stage:** what-the-scores-showed  
**On screen:** Headline 'Near the line, verdicts flip'. A table from our two gradings of the same twelve entries: the entry whose answer changed, with '4 · the judge passes it' under 'First grading' and '3 · the judge fails it' under 'Second grading'; and a row for the three entries that say how the change was coded, '2' both times. The changed row's two cells light in turn, then the row of twos.  
**Renderer:** html (scenes/s24.html)

> We graded the same twelve entries twice: once without the scoring block, and once with it.
> The judge's answer changed for one of them: a four the first time, and a three the second.  _(depends on what the demo produced)_
> At the judge's own threshold, that's a pass and then a fail, for the same entry.  _(depends on what the demo produced)_
> A judge is a model, so its answer can vary from one grading to the next, and near the threshold that variation turns into a different verdict.
> The entries that got a two got a two both times.  _(depends on what the demo produced)_

## s25

**Role:** body · **Mode:** think · **Stage:** what-the-scores-showed  
**On screen:** Headline 'A scale invites extra marks'. A card labelled with the stimulus and model and 'our label: yes · the yes-or-no judge: yes · 1 to 5: 4', holding the entry in a dark box. Under it a quote card labelled 'the 1-to-5 judge’s reason', with the reason from our run word for word. The entry lights, then the reason.  
**Renderer:** html (scenes/s25.html)

> The scale also invited the judge to mark things the rubric didn't ask about.
> This entry got a four, not a five, though we and the yes-or-no judge both said yes.  _(depends on what the demo produced)_
> Its reason says the entry could be more concrete, with an example date, which our one criterion doesn't ask for.  _(3s to read after; depends on what the demo produced)_
> A rubric with one criterion keeps a yes-or-no judge on its question.
> Given a scale, the same judge finds other things to mark.

## s26

**Role:** body · **Mode:** think · **Stage:** what-the-scores-showed  
**On screen:** Headline 'A failure hides in an average'. A table of the trials from our second grading that passed with a cross from the judge: columns 'Judge' (a cross), 'Trial' (a tick and 62.5%) and the entry, shortened. Under it one line of arithmetic: '0.5 × 0.25 + 0.5 × 1 = 0.625 · reaches 0.6'. The Judge column lights, then the Trial column, then the arithmetic, then the highlight clears.  
**Renderer:** html (scenes/s26.html)

> Then there's the scoring block.
> These are the trials that passed with a cross from the judge.  _(depends on what the demo produced)_
> The judge failed each of them, in plain words, and each passed as a trial, because the check scored a full one, and the average carried it.  _(depends on what the demo produced)_
> The check nearly always passes, and it carries half the weight.
> So while the check passes, a trial fails at this threshold only if the judge answers one, the lowest mark.
> All twelve trials passed, so nothing in a summary would say that the judge had failed four of them.  _(depends on what the demo produced)_
> That's how a failure hides in an average.

## s27

**Role:** body · **Mode:** think · **Stage:** what-the-scores-showed  
**On screen:** Headline 'The yes or no still decides'. Two blocks side by side: 'yes-or-no judge · decides the verdict' and '1-to-5 judge · says how far off a failure is'. Under them a note: 'Vally docs, Scoring: thresholds for judged quality; pass-or-fail checks left out of the weights'. Each block fills as it is said.  
**Renderer:** html (scenes/s27.html)

> So we follow Vally's advice: thresholds are for judged quality, and pass-or-fail checks stay out of the weighting.
> From here on, the yes-or-no judge decides the verdict.
> The one-to-five judge is a tool to reach for when you want to know how far off a failure is.

## s28

**Role:** recap · **Stage:** what-the-scores-showed  
**On screen:** Headline 'What decides the verdict?'. One block, 'a trial’s verdict', which opens after the question and a pause into two parts: 'no scoring block · every grader must pass' and 'weights and a threshold · the weighted score must reach the threshold'. Each part lights as it is said.  
**Renderer:** html (scenes/s28.html)

> Before you go on: what decides a trial's verdict with no scoring block, and what decides it with weights and a threshold?
> With no scoring block, every grader must pass, and the printed score decides nothing.  _(pause 2.5s first)_
> With weights and a threshold, each grader type's score counts by its weight, and the trial passes when the total reaches the threshold, even if a grader failed.

## s29

**Role:** next · **Stage:** what-the-scores-showed  
**On screen:** 'Next: Is the change real' in the display serif. Below, the hand-off question: 'After an edit, 7 of 10 becomes 9 of 10. Is that real?' A note: 'Exercises are on the lesson page · Source: Vally docs, Scoring; Grader: prompt'.  
**Renderer:** slide (scenes/s29.html)

> You can now re-grade saved trials with a judge that scores one to five, and say which verdicts changed, and whether your labels agree.
> Scores and counts both move after an edit.
> After an edit, seven of ten becomes nine of ten.
> Is that real?
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
