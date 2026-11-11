# Check the judge against your own labels — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0013-check-the-judge.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** Can I trust the judge's verdicts?  
**The viewer starts:** A professional programmer who knows the shell and has followed the course's running example: the changelog-entry skill, measured on claude-haiku-4.5 and gpt-5.6-terra. Knows stimulus (a request plus its graders), grader and trial; that a judge's yes or no becomes its grader's pass or fail; that a grader can be wrong in two ways (it can fail correct work, or pass work that was not done); and has tested code graders against a golden patch and against saved trials. Knows what an LLM judge is, and a rubric with one criterion: the new changelog entry says what changes for people who use the tool, and does not say how it was coded. Has a yes-or-no judge that was run over twelve saved trials and gave a verdict and a reason for each. Has a notes file, wording-labels.md, listing the twelve entries with our own yes or no for each (a label), written before the judge ran, and the judge's yes or no beside it. Knows that eleven of the judge's verdicts match ours and one doesn't, and that the judge gave different verdicts to two nearly identical entries. Has never counted the two lists against each other, and does not know the terms TPR and TNR.

1. **measured-not-trusted**: after this, the viewer can name the two directions a judge can be wrong in, and say why one agreement figure hides them
2. **tpr-and-tnr**: after this, the viewer can work out TPR and TNR from four counts, and say what a low value of each means
3. **count-compare-decide**: after this, the viewer can sort labelled trials into four boxes, work out both rates, examine each disagreement, and write down a decision
4. **what-twelve-labels-show**: after this, the viewer can say what two rates from twelve labels can and can't show, and so how far to rely on the judge

## s01 — A judge is measured

**Role:** hook · **Mode:** think · **Stage:** measured-not-trusted  
**On screen:** Headline 'Check the judge' in the display serif. One of the twelve entries from our run in a dark box, labelled with its stimulus, model and trial. Under it, two blocks side by side: 'Judge: no' with the judge's reason for that entry, verbatim, and 'Ours: no' with 'written before the judge ran'. The judge's block fills when its reason is mentioned, then ours.  
**Renderer:** html (scenes/s01.html)

> Our judge gave a yes or a no to twelve changelog entries, with a well-written reason for each.
> But the judge is a model, and a well-written reason isn't evidence of a correct verdict.
> Code graders could be tested against a golden patch, and there's no golden patch for whether an entry reads well to a user.
> What we do have is our own yes or no for the same twelve entries, written down before the judge ran.
> Here, you'll measure the judge against those labels as two numbers, and decide whether to rely on it.

## s02

**Role:** body · **Mode:** think · **Stage:** measured-not-trusted  
**On screen:** Headline 'Wrong in two directions'. Two blocks side by side, no arrow. Left: 'Judge says yes · we'd say no', with 'a failure slips through'. Right: 'Judge says no · we'd say yes', with 'a false alarm'. Each fills as it is described.  
**Renderer:** html (scenes/s02.html)

> Let's start with how a judge can be wrong.
> Like any grader, it can be wrong in two directions.
> It can say yes to an entry we'd reject: a failure slips through, and we believe the skill is better than it is.
> Or it can say no to an entry we'd accept: a false alarm, and we go hunting for a problem that isn't there.

## s03

**Role:** body · **Mode:** think · **Stage:** measured-not-trusted  
**On screen:** Headline 'Agreement hides the direction'. Two rows of twenty boxes, labelled 'an invented example'. Top row, 'our labels': eighteen hold a tick (yes) and two a cross (no). Bottom row, 'a judge that always says yes': twenty ticks. Under them two figures side by side: '18 of 20 agree · 90%' and '0 of 2 bad entries caught'. The rows light as they are described, then each figure.  
**Renderer:** html (scenes/s03.html)

> The obvious measure is agreement: on what share of the entries did the judge and we say the same thing?
> That makes it a poor measure, because it hides which direction the errors run in.
> Let's say we label twenty entries, and eighteen are fine.
> Even a judge that says yes to everything agrees with us eighteen times out of twenty, which is ninety percent.
> Yet it has caught neither of the two bad entries.
> It's useless, and its agreement looks excellent.

## s04

**Role:** body · **Mode:** think · **Stage:** measured-not-trusted  
**On screen:** Headline 'Two counts, not one'. Two blocks side by side: 'Of our yes labels · how many did the judge pass?' and 'Of our no labels · how many did the judge fail?'. A note under them: 'Aim above 90% on each · 100 or more labels for a judge you depend on · Husain and Shankar, validate-evaluator skill; AI Evals FAQ (2026)'. Each block fills as its question is asked; the note lights when the aim is given.  
**Renderer:** html (scenes/s04.html)

> So we count the two directions separately.
> Of the entries we said yes to, how many did the judge pass, by saying yes too?
> Of the entries we said no to, how many did it fail?
> That makes two numbers, and a judge has to do well on both.
> How well is well enough?
> Practitioners this course leans on suggest aiming above ninety percent on each number, and labelling a hundred or more examples for a judge we intend to depend on.
> Twelve labels, which is what we have, can show that a judge is badly wrong.
> They can't show that it's reliably right.

## s05

**Role:** body · **Mode:** think · **Stage:** measured-not-trusted  
**On screen:** Headline 'Three changes undo it'. Three blocks in a row: 'the rubric's wording', 'the judge model', 'the kind of request', each labelled 'change it, and we label again'. Under them one line: 'While a rubric is reworded, some labelled entries stay aside, unread.' Each block fills as it is named, then the line lights.  
**Renderer:** html (scenes/s05.html)

> One caution before the arithmetic: a measurement like this holds for one rubric, one judge model, and one kind of request.
> Changing the rubric's wording, changing the judge model, or pointing the judge at a different kind of request undoes it.
> Each of them means labelling again.
> When we reword a rubric to fix a disagreement, we set some labelled entries aside first, and don't look at them while rewording.
> Otherwise, we'd be fitting the rubric to the examples we're testing it on.

## s06 — TPR and TNR

**Role:** body · **Mode:** works · **Stage:** tpr-and-tnr · **Introduces:** TPR, TNR  
**On screen:** Headline 'Two rates, two names'. Two blocks side by side. Left: 'TPR', 'true positive rate', 'of the trials we labelled yes, the share the judge also passed'. Right: 'TNR', 'true negative rate', 'of the trials we labelled no, the share the judge also failed'. A note: 'positive = yes · negative = no'. Each block fills as it is defined.  
**Renderer:** html (scenes/s06.html)

> That's the idea; here's how the two numbers are worked out, starting with their names.
> First, the true positive rate, or TPR: of the trials we labelled yes, the share the judge also passed.
> Positive is the statistician's word for yes.
> Second, the true negative rate, or TNR: of the trials we labelled no, the share the judge also failed.
> Negative is the word for no.

## s07

**Role:** body · **Mode:** works · **Stage:** tpr-and-tnr  
**On screen:** Headline 'Every trial, one box'. A two-by-two table, labelled 'an invented judge, to show the arithmetic': columns 'Ours: yes' and 'Ours: no'; rows 'Judge: yes' and 'Judge: no'; counts 11, 3, 1, 5. Under the columns, their totals: 12 and 8. The column totals light, then the 11, the 3, the 1 and the 5 as each is said.  
**Renderer:** html (scenes/s07.html)

> To work them out, every trial goes into one of four boxes, by what the judge said and what we said.
> Here's an invented judge, to show the arithmetic.
> We labelled twenty entries: twelve yes, and eight no.
> This judge passed eleven of our twelve, and it also passed three of our eight.
> So it failed one of our yes entries, and five of our no entries.

## s08

**Role:** body · **Mode:** works · **Stage:** tpr-and-tnr  
**On screen:** Headline 'Each rate reads one column'. The same table in the same place, now with a last row of rates under the columns: 'TPR · 11 of 12 · 92%' under the left, 'TNR · 5 of 8 · 63%' under the right, and under the table 'agreement · 16 of 20 · 80%'. The left column's rate lights, then the right column's, then the agreement figure, then the right column's rate again.  
**Renderer:** html (scenes/s08.html)

> Each rate uses one column, read downwards.
> On the left is TPR: eleven out of twelve, which is ninety-two percent.
> On the right is TNR: five out of eight, which is sixty-three percent.
> Agreement is sixteen out of twenty, eighty percent, which sounds respectable.
> TNR tells the real story: of the entries we'd reject, this judge lets more than a third through.

## s09

**Role:** body · **Mode:** works · **Stage:** tpr-and-tnr  
**On screen:** Headline 'What a low rate means'. Two blocks side by side: 'Low TPR · false alarms · the judge is stricter than we are' and 'Low TNR · missed failures · the judge is more lenient than we are'. Each fills as it is said; both rest for the last sentence.  
**Renderer:** html (scenes/s09.html)

> Each number, when it's low, says something different.
> Low TPR means false alarms: the judge is stricter than we are.
> Low TNR means missed failures: the judge is more lenient than we are.
> Which matters more depends on what the judge is for, but a judge with either number low isn't measuring our criterion.

## s10 — Count, compare, decide

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** Headline 'Twelve trials, four boxes'. The two-by-two table with no counts yet: columns 'Ours: yes' and 'Ours: no'; rows 'Judge: yes' and 'Judge: no'; each cell says what landing there means ('both say yes', 'a failure slips through', 'a false alarm', 'both say no'). A note: 'our 12 trials · no agent runs, no judge calls'. The agreeing cells light as the sorting is named, then the 'Judge: yes, Ours: no' cell for the one entry where we differ, and again for the question.  
**Renderer:** html (scenes/s10.html)

> That's how the numbers work; now let's count ours.
> First we'll sort our twelve trials into the four boxes, and work out both rates.
> Then we'll look closely at the one entry where the judge and we differ, and write down what we will and won't rely on the judge for.
> None of it runs an agent or a judge.
> On that entry we said no and the judge said yes: which of the two rates will it lower?  _(2s to read after)_
> If you did the same count yourself, here's what you'd see.

## s11

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide · **Introduces:** wording-labels.md, notes/wording-labels.md  
**On screen:** File panel labelled 'notes/wording-labels.md', with a minimap: the criterion on line 3, then a table with a row per trial and the columns Entry, Ours and Judge. 'Ours' lights in the header row, then 'Judge'. The panel then scrolls down through the twelve rows to the end of the file.  
**Renderer:** html (scenes/s11.html)

> Both lists are in the notes file from the judging, named wording labels.
> Each of the twelve entries has our yes or no, with the judge's beside it.
> Our answers haven't been changed since the judge ran.  _(3s to read after)_

## s12

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** Headline 'Twelve trials, sorted'. The two-by-two table, each cell now holding its count and, under it in small type, the trials that fell there, named by stimulus, model and trial number as in the notes file. From our run: 7 in 'Judge: yes, Ours: yes', 1 in 'Judge: yes, Ours: no' (cache, terra, 1), 0 in 'Judge: no, Ours: yes', 4 in 'Judge: no, Ours: no'. The yes-yes cell lights, then the no-no cell, then the cell with the one disagreement, then the empty cell.  
**Renderer:** html (scenes/s12.html)

> Sorting takes one look at each row's two answers.
> Seven entries got a yes from both of us, and four got a no from both.  _(2s to read after; depends on what the demo produced)_
> One entry got a yes from the judge and a no from us, and the last box is empty.  _(2s to read after; depends on what the demo produced)_

## s13

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** Headline 'Both rates, from our counts'. The same table in the same place with the counts alone (7, 1, 0, 4), the labels row (7 and 5), and a last row of rates under the columns: 'TPR · 7 of 7 · 100%' and 'TNR · 4 of 5 · 80%'. Under the table: 'agreement · 11 of 12 · 92%', and a note: 'from 12 labels · both rates are rough'. The left rate lights, then the right, then the agreement figure, then the note.  
**Renderer:** html (scenes/s13.html)

> Now the two rates, one column each.
> On the left, TPR is seven out of seven: a hundred percent.  _(depends on what the demo produced)_
> On the right, TNR is four out of five: eighty percent.  _(depends on what the demo produced)_
> Agreement is eleven out of twelve, ninety-two percent, and it wouldn't say which column the miss is in.  _(depends on what the demo produced)_
> With only twelve labels, both rates are rough.  _(2s to read after)_

## s14

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** Headline 'A disagreement gets examined'. Left, one block: 'For each disagreement · read the entry and the judge's reason again'. Right, two blocks stacked: 'We still disagree · one error of the judge's' and 'The judge persuaded us · our criterion wasn't what we thought'. Under them one line: 'Either way the label stays as first written, and the entry counts as a disagreement.' The left block fills, then each right block in turn, then the line lights.  
**Renderer:** html (scenes/s14.html)

> Next, every disagreement gets a second look.
> For each one, we'd read the entry and the judge's reason again, and decide who is right.
> If we still disagree, that's one error of the judge's.
> If the judge has persuaded us, our criterion wasn't what we thought.
> Even then, the label stays as we first wrote it, and the entry still counts as a disagreement.
> Changing labels to match a judge would make any judge look good.
> For a criterion that turned out unclear, the remedy is to reword it, then measure again on fresh labels.

## s15

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** Headline 'One word apart, two verdicts'. A dark box labelled 'cache · gpt-5.6-terra · the entry from each of its two trials' with both entries, trial number on the left; 'by caching the tag index' is marked in each, and 'note', the one word the second has and the first lacks. Under it one line: 'ours, for both: no · hesitated: the benefit, then a hint of the method'. Under that, two blocks side by side with the judge's reason for each, verbatim: 'The judge, trial 0 · no' and 'The judge, trial 1 · yes'. The word lights, then the phrase in both entries, then our line, then each of the judge's blocks in turn.  
**Renderer:** html (scenes/s15.html)

> In our run, there's one to examine.  _(depends on what the demo produced)_
> It's one of two entries from the same model, which differ by a single word.  _(depends on what the demo produced)_
> Both say a command got faster by caching the tag index: the benefit, with a hint of the method.  _(depends on what the demo produced)_
> We hesitated over both when labelling, and said no to both.  _(depends on what the demo produced)_
> To the first, the judge said no as well, because it states the implementation.  _(depends on what the demo produced)_
> To the second, it said yes, calling the same mention a minor blemish.  _(4s to read after; depends on what the demo produced)_

## s15b

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** Headline 'One error of the judge's'. The same dark box with the two entries, in the same place. Under it three blocks in a row: 'The criterion', with the rubric's one line verbatim; 'We still disagree · the judge said no to one entry, and yes to its near twin'; 'Our label stays · no, as first written, with our hesitation on record'. The criterion block fills, then the phrase 'by caching the tag index' in both entries, then the middle block, then the last.  
**Renderer:** html (scenes/s15b.html)

> So who is right?
> Our criterion says an entry doesn't say how the change was coded, and the phrase by caching the tag index says how.
> In its reason for the first entry, the judge says the same.  _(depends on what the demo produced)_
> So we still disagree, and count it as one error of the judge's: it was inconsistent on two entries a single word apart.  _(depends on what the demo produced)_
> It's also the wording we hesitated over ourselves, which suggests our criterion isn't clear at this edge.  _(depends on what the demo produced)_
> Our label stays as we wrote it.

## s16

**Role:** practice · **Mode:** use · **Stage:** count-compare-decide  
**On screen:** File panel labelled 'notes/wording-labels.md', with a minimap, opened at the end of the file: the decision we added as the file's last line: 'On 12 labels (7 yes, 5 no) the judge matched 11: TPR 100%, TNR 80%. The one miss is an entry we hesitated over ourselves, which the judge failed in one trial and passed in the other. That is enough to use it to compare versions of the skill, knowing it may pass a borderline entry, and not enough to trust a single verdict without reading its reason; we will label more whenever the rubric or the judge model changes.' The last line lights and stays lit.  
**Renderer:** html (scenes/s16.html)

> Last, we write the decision down, at the end of the same notes file.
> On twelve labels, seven yes and five no, the judge matched eleven.  _(depends on what the demo produced)_
> Its one miss is an entry we hesitated over ourselves, which it failed in one trial and passed in the other.  _(depends on what the demo produced)_
> That's enough to use the judge for comparing versions of the skill, knowing it may pass a borderline entry.  _(depends on what the demo produced)_
> It's not enough to trust a single verdict without reading its reason.  _(depends on what the demo produced)_
> Whenever the rubric or the judge model changes, we'll label more.  _(3s to read after)_

## s17 — What twelve labels show

**Role:** body · **Mode:** think · **Stage:** what-twelve-labels-show  
**On screen:** Headline 'One entry is 20 points'. Two blocks side by side: '4 of 5 · 80% · TNR in our run, with its one miss' and '5 of 5 · 100% · TNR had that one entry gone the other way'. Under them a line: '12 labels can't tell a judge that's right 99% of the time from one that's right 85% of the time.' The first block fills, then the second, then the line lights.  
**Renderer:** html (scenes/s17.html)

> So what does that result show?
> On these twelve entries, this judge model applied this criterion the way we do eleven times.  _(depends on what the demo produced)_
> Its TNR came out at eighty percent, under the ninety we aim for.  _(depends on what the demo produced)_
> But with five no labels, one entry is the whole distance between eighty and a hundred.  _(depends on what the demo produced)_
> Twelve labels are too few to tell a judge that's right ninety-nine percent of the time from one that's right eighty-five percent of the time.

## s18

**Role:** body · **Mode:** think · **Stage:** what-twelve-labels-show  
**On screen:** Headline 'Still a real result'. Two small two-by-two tables side by side, each with its two rates under it. Left, 'our judge': 7, 1, 0, 4, TPR 100%, TNR 80%. Right, 'a judge that passes everything, on the same labels': 7 and 5 in the top row, 0 and 0 in the bottom, TPR 100%, TNR 0%. The right table's TNR lights, then, for the last sentence, the left table's.  
**Renderer:** html (scenes/s18.html)

> It's still a real result.
> Had the judge passed everything, the same twelve labels would have put its TNR at zero.  _(depends on what the demo produced)_
> Likewise, a judge that failed entries for reasons unrelated to the criterion would have shown up at once.
> Those are the most common ways for a judge to go wrong.
> Ours did neither: it caught four of our five no entries, and wavered on one borderline one.  _(depends on what the demo produced)_

## s19

**Role:** recap · **Stage:** what-twelve-labels-show  
**On screen:** Headline 'A judge that always says yes'. One block: 'yes to every trial · we labelled nine yes, and one no'. After the question and a pause it opens into three parts, each lit as it is said: 'TPR · 9 of 9 · 100%', 'TNR · 0 of 1 · 0%', 'agreement · 9 of 10 · 90%'.  
**Renderer:** html (scenes/s19.html)

> Before you go on: a judge says yes to every trial, and we labelled nine trials yes and one no.
> What are its TPR and its TNR?
> TPR is a hundred percent: it passed all nine of the entries we labelled yes.  _(pause 2.5s first)_
> TNR is zero: we labelled one entry no, and the judge passed it.
> Its agreement, ninety percent, hides that completely.

## s20

**Role:** next · **Stage:** what-twelve-labels-show  
**On screen:** 'Next: Partial credit' in the display serif. Below, the hand-off question: 'Can a grader give partial credit without hiding a failure?' A note: 'Exercises are on the lesson page · Source: Husain and Shankar, validate-evaluator skill'.  
**Renderer:** slide (scenes/s20.html)

> You can now measure a judge against your own labels as two numbers, and decide whether to rely on it.
> On these twelve entries, our judge's verdicts match our labels eleven times out of twelve.  _(depends on what the demo produced)_
> But some of the no entries were nearly right and some were far off, and a yes or no can't tell them apart.
> Can a grader give partial credit without hiding a failure?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
