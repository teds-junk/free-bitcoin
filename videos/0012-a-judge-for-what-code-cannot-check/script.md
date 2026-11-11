# A judge for what code cannot check — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0012-a-judge-for-what-code-cannot-check.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** How do I grade a quality that no pattern can decide?  
**The viewer starts:** A professional programmer who knows the shell and has measured the changelog-entry skill with Vally on two models, claude-haiku-4.5 and gpt-5.6-terra. Works in the course's practice folder. Knows skill, agent, model, eval file (its defaults block, and that a stimulus's request sits in a field named prompt), stimulus, grader, trial, run, the results folder with results.jsonl and one folder per trial holding workspace.patch, and how to read a patch. Knows vally eval with -e, --model, --runs, --workers and --output-dir, and vally lint, including its usual warning that with several graders and no scoring block every grader must pass. Knows that runs are charged to a GitHub Copilot plan. Has written graders that are code: patterns over the diff (diff-contains and its relatives), an empty-diff check, a hidden grading script, and a check of which skills loaded; knows a stimulus passes only when every grader on it passes, and that a grader records evidence. Has tested graders with vally oracle, whose --verbose flag prints each grader's evidence, and has re-graded a saved run from inside its folder with vally grade, which starts no agent. Knows the skill's rules, including 'one line per change, written for people who use the tool', and has seen a model write an entry about the code instead. Has never used a model as a grader, and does not know the words LLM judge, rubric, label, judge_model, or the prompt grader.

1. **when-a-judge**: after this, the viewer can say when an LLM judge is the right grader, and name the three habits that make its verdicts usable
2. **how-it-decides**: after this, the viewer can point to the three additions that put a judge in an eval file, and predict what a judged trial prints
3. **write-and-regrade**: after this, the viewer can label saved entries yes or no, add a yes-or-no judge, and run it over saved trials without starting an agent
4. **what-it-found**: after this, the viewer can read the judge's verdicts and reasons, and say why a well-written reason is not yet evidence

## s01 — When a judge fits

**Role:** hook · **Mode:** think · **Stage:** when-a-judge  
**On screen:** Headline 'What code cannot check' in the display serif. Two cards, one above the other: 'the skill' with its line 'One line per change, written for people who use the tool.' in a dark box, and 'one entry a model wrote' with a real entry from our run. 'written for people who use the tool' lights, then the words 'streaming … parser' in the entry.  
**Renderer:** html (scenes/s01.html)

> Our skill says each entry should be written for people who use the tool.
> Yet when the fix was a switch to a streaming parser, one model's entry told users about the streaming parser.  _(depends on what the demo produced)_
> None of our graders checks for that, because no pattern can.
> Here, you'll write a grader that asks another model one yes-or-no question, run it over saved trials, and read its reasons.

## s02

**Role:** body · **Mode:** think · **Stage:** when-a-judge  
**On screen:** Headline 'Not a pattern'. Two blocks side by side, no arrow: 'Code can see · a pattern in the diff · an empty diff · a script's check · which skills loaded' and 'Code can't decide · does this entry say how the fix was coded?'. Under them the same entry in a dark box. The first block fills as the graders are listed, then the second.  
**Renderer:** html (scenes/s02.html)

> Let's start with why code can't check this.
> Every grader so far is code: a pattern, an empty-diff check, a script, or a check of which skills loaded.
> Each one checks something code can see.
> Whether an entry says how a fix was coded isn't something a pattern can match, because the giveaway words could be anything.
> Here they're streaming parser, when all a user cares about is that big imports no longer crash.
> Checking that takes something that can read, and that something is another model.

## s03

**Role:** body · **Mode:** think · **Stage:** when-a-judge · **Introduces:** LLM judge  
**On screen:** Headline 'A model as the grader'. One wide block: 'LLM judge · a grader that asks a language model to read what the agent did, and decide whether it meets a criterion you wrote'. Under it three smaller blocks in a row: 'slower than code', 'one model call per trial', 'can be wrong in new ways'. The definition fills first, then each cost as it is said.  
**Renderer:** html (scenes/s03.html)

> That kind of grader is called an LLM judge, where LLM stands for large language model.
> It asks a language model to read what the agent did, and decide whether it meets a criterion you wrote.
> Such a judge can decide things code can't, but it has costs.
> It's slower than code, and every trial it judges costs a call to a model.
> It can also be wrong in ways a pattern can't: swayed by confident wording, or reading your criterion differently from you.
> So we use a judge only for what code can't decide, and everything graded so far stays with code.

## s04

**Role:** body · **Mode:** think · **Stage:** when-a-judge  
**On screen:** Headline 'Three habits for a judge'. Three numbered blocks in a row: '1 · One question per judge', '2 · Yes or no', '3 · Our own answers first'. Block 1 fills, then block 2.  
**Renderer:** html (scenes/s04.html)

> When a judge is needed, three habits make its verdicts usable.
> First, one question per judge.
> Asked whether an entry is good, a judge weighs several things at once, and you can't tell which one tipped it.
> Second, the answer is yes or no.
> With a score from one to five, it's hard for anyone, the judge included, to say what separates a three from a four.
> Yes or no forces the criterion to be clear.

## s04b

**Role:** body · **Mode:** think · **Stage:** when-a-judge · **Introduces:** label  
**On screen:** The same three numbered blocks. Block 3, 'Our own answers first', fills; its text adds 'each answer is a label'.  
**Renderer:** html (scenes/s04b.html)

> Third, we decide our own answers first.
> Before writing the criterion, we go through real examples, and say yes or no to each.
> If we hesitate over one, the criterion isn't clear yet, and the judge would inherit the muddle.
> Each answer we write down is called a label, and our labels are what the judge gets checked against.

## s05 — How the judge decides

**Role:** body · **Mode:** works · **Stage:** how-it-decides · **Introduces:** wording.eval.yaml, wording.eval.yaml · with a judge added, judge_model  
**On screen:** File panel 'wording.eval.yaml · with a judge added', with a minimap, open at the top of the file. Line 5, 'judge_model: claude-sonnet-5.5', lights, with the note on the right 'the model that judges'.  
**Renderer:** html (scenes/s05.html)

> That's when to use one; here's how Vally's judge is written.
> This eval file ships in the practice folder, and we're looking at it with a judge already added.
> It takes three additions, in three places.
> First, under defaults, judge model names the model that does the judging.
> Without that line Vally picks one, and its choice can change from one version of Vally to the next.
> We name a model that isn't one of the two being tested, so that no model marks its own work.

## s06

**Role:** body · **Mode:** works · **Stage:** how-it-decides · **Introduces:** rubric  
**On screen:** The same panel, scrolled to the first stimulus, 'parser'. Its request lights (lines 17 to 20), with the note 'a request in coding terms'; then the three rubric lines (21 to 23), with the note 'the rubric: one criterion'.  
**Renderer:** html (scenes/s06.html)

> Each stimulus in this file is a request worded in coding terms, like this one about a streaming parser.
> The second addition is the rubric: a list of criteria for this stimulus, in plain words.
> Ours has a single criterion.
> It asks that the new entry says what changes for people who use the tool, and doesn't say how it was coded.

## s07

**Role:** body · **Mode:** works · **Stage:** how-it-decides · **Introduces:** prompt grader, scoring: binary  
**On screen:** The same panel, scrolled on to the stimulus's graders. 'type: prompt' lights with the note 'the judge'; then 'scoring: binary' with 'yes or no'; then the 'prompt:' line under it with 'an extra instruction'; then the diff-contains grader below with 'was there already'.  
**Renderer:** html (scenes/s07.html)

> The third addition is the judge itself: a grader of type prompt.
> Its name is unlucky, because it's unrelated to the prompt field that holds each request.
> This grader reads the rubric of the stimulus it sits in.
> Scoring binary makes its answer yes or no.
> On the next line is an extra instruction, telling the judge to start each reason by quoting the entry.
> That way, each reason shows what the judge was looking at.
> Below it is the grader that was there already, a pattern that checks the entry cites its pull request.

## s08

**Role:** body · **Mode:** works · **Stage:** how-it-decides  
**On screen:** Headline 'A verdict and a reason'. Three numbered blocks in a row: '1 · The judge model is given · the request · the rubric · files holding what the agent said and did'; '2 · It returns · a verdict and a reason'; '3 · Vally records · the verdict as the grader's pass or fail · the reason as its evidence'. Each fills as it is said.  
**Renderer:** html (scenes/s08.html)

> When the judge runs, Vally gives the judge model three things: the request, the rubric, and files holding what the agent said and did in that trial.
> The judge reads them, and returns a verdict and a reason.
> Its verdict becomes the grader's pass or fail, and its reason becomes the grader's evidence.
> Each trial gets one overall verdict, however many criteria the rubric lists.
> With one criterion, that verdict answers our one question.
> With several, it would be a blend, which is another reason to ask about one thing.

## s09

**Role:** body · **Mode:** works · **Stage:** how-it-decides  
**On screen:** Headline 'What a judged trial prints'. Dark box, left: one block of vally grade's output from our run, for a cache trial the judge failed: the '━━━ cache ━━━' heading, the summary line, the '[prompt …]' line with its reason, the '[cites-66]' line, and the score line. Notes on the right, level with each: 'the stimulus', 'the judge: a cross, then its reason', 'the pattern grader', 'every grader must pass'. Each lights in turn.  
**Renderer:** html (scenes/s09.html)

> Here's what one judged trial prints, taken from our run.
> Each trial gets a block, headed by the name of its stimulus.
> Inside, the line that begins with prompt in square brackets is the judge: a tick or a cross, then its reason.
> This reason starts by quoting the entry, and then objects that it leaks implementation detail.  _(3s to read after; depends on what the demo produced)_
> Under it is the pattern grader, which passed.  _(depends on what the demo produced)_
> Since every grader has to pass, this trial fails.  _(depends on what the demo produced)_

## s10

**Role:** body · **Mode:** works · **Stage:** how-it-decides · **Introduces:** vally grade, -e, --run-dir, --verbose, results.jsonl  
**On screen:** Headline 'Judge the trials you saved'. Dark box, left: the vally grade command with one option per line: '-e ../../../evals/wording.eval.yaml', '--run-dir .', '--verbose', '< results.jsonl'. Notes on the right, level with each: 'the eval file's current graders', 'the run folder we're in', 'print each grader's evidence', 'the saved trials'. Each line lights as it is named.  
**Renderer:** html (scenes/s10.html)

> Because a judge is a grader, vally grade can run it over saved trials, without starting an agent.
> We run it from inside the run's folder, so run dir is a dot, and the saved trials come in from results dot jsonl.
> As with the oracle, dash dash verbose prints every grader's evidence, which for a judge is its reason.
> So we can reword the rubric and judge the same trials again, without paying for the agents twice.
> Each judged trial is one call to the judge model, charged to the Copilot plan the way an agent run is.

## s11 — Our answers first

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** File panel 'wording.eval.yaml', as it ships, with a minimap. It scrolls through the three requests: parser (lines 14 to 19), cache (26 to 31), dates (38 to 43). In each, the coding words light: 'streaming parser', 'LRU cache', 'small tokenizer'. Notes on the right give what users notice.  
**Renderer:** html (scenes/s11.html)

> That's how it works; now let's use it.
> As it ships, the eval file has three stimuli, each describing a merged change the way a programmer would.
> One swapped in a streaming parser, so that big imports stop running out of memory.
> Another put a cache in front of the tag index, which makes one command much faster.
> The last rewrote the date parser as a small tokenizer, so single-digit months and days work.
> Each request runs twice on both models, which gives us twelve entries to judge.
> Which model would you expect to name the code more often?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s12

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade · **Introduces:** vally eval, ls, --model, --runs, --workers, --output-dir, lesson-12, 2026  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. The vally eval command over four lines, with --runs 2 --workers 2 and --output-dir results/lesson-12; a jump cut; then the model summary, held until it has been read. The screen is cleared out of sight; ls results/lesson-12 shows one folder named with a time.  
**Renderer:** terminal (tapes/s12.tape)

> Here's the run: vally eval on the wording file, with two trials of each stimulus on both models.  _(finishes before typed:1)_
> It spends twelve short agent runs.  _(finishes before enter:1)_
> So far, the file's only graders check that each entry cites its pull request.  _(finishes before enter:1)_
> About a minute later, there's a tick for each model.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> Let's look in the results folder.  _(finishes before typed:2)_
> It holds one folder, named with the time of the run.  _(1s to read after; waits for output:2)_

## s13

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade · **Introduces:** cd, cat, workspace.patch, wording  
**On screen:** Terminal, continuing in the practice folder. cd into the run's folder; cd wording; ls shows cache, dates and parser; the screen is cleared out of sight; cat parser/claude-haiku-4.5/0/workspace.patch shows the patch, held until it has been read.  
**Renderer:** terminal (tapes/s13.tape)

> We change into it, then into the folder for the eval.  _(waits for output:1; finishes before typed:2)_
> Then we list what's there.  _(waits for done:2; finishes before typed:3)_
> There's one folder per stimulus: cache, dates and parser.  _(1s to read after; waits for output:3)_
> Each one holds a folder per model and trial, with that trial's patch, and here's the first.  _(finishes before typed:4)_
> Haiku's entry fixes the out-of-memory errors, and then says how: by using a streaming parser.  _(6s to read after; waits for output:4; depends on what the demo produced)_

## s14

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** Headline 'Four entries about the parser'. Dark box, left: the entry each of the four parser trials added, from our run, with the model and trial number on the left. Notes on the right, level with each entry: our own answer, yes or no, and a few words why. Haiku's first lights, then its second and terra's two.  
**Renderer:** html (scenes/s14.html)

> Reading all twelve patches that way gives us twelve entries, and we answer one question about each.
> Does it say what changes for people who use the tool, without saying how it was coded?
> We don't need to know what a streaming parser is, only whether the entry mentions one.
> Haiku's first parser entry names the streaming parser, so we say no.  _(depends on what the demo produced)_
> Its second, and both of terra's, only say that large imports no longer run out of memory, so those get a yes.  _(2s to read after; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** Headline 'Four about the cache'. The same layout: the four cache entries from our run in a dark box, our answer beside each. Haiku's two light, then terra's two, where 'by caching the tag index' lights.  
**Renderer:** html (scenes/s15.html)

> On the cache request, haiku's two entries name the kind of cache outright, so again we say no.  _(depends on what the demo produced)_
> Terra's two are harder: they lead with the speed-up, and then add, by caching the tag index.  _(depends on what the demo produced)_
> That's the benefit plus a hint of the method, and we decided that a hint still counts as saying how.  _(depends on what the demo produced)_
> Hesitating like that is worth noticing, because it marks an edge of the criterion that isn't settled.  _(2s to read after)_

## s16

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade · **Introduces:** wording-labels.md  
**On screen:** Headline 'Four about the dates'. The same layout: the four dates entries from our run, our answer beside each; all four light together. A note under the box: 'our twelve answers are saved in notes/wording-labels.md'.  
**Renderer:** html (scenes/s16.html)

> All four date entries say that single-digit months and days now work, and none mentions the tokenizer.  _(depends on what the demo produced)_
> So those four get a yes.  _(depends on what the demo produced)_
> That makes seven yes and five no.  _(depends on what the demo produced)_
> We write the twelve answers in a notes file, and we won't change them once the judge has spoken.  _(2s to read after)_

## s17 — Add the judge and run it

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** File panel 'wording.eval.yaml · with a judge added', showing only the added lines with 'lines hidden' rows between: line 5, then the rubric and prompt grader of each stimulus. Line 5 lights; then the panel scrolls through the three stimuli, the added lines lit in each.  
**Renderer:** html (scenes/s17.html)

> Now the judge goes into the eval file, just as we walked through it.
> That's the judge model line under defaults.
> Then, in each of the three stimuli, the same rubric and the same prompt grader.

## s18

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade · **Introduces:** vally lint, -e  
**On screen:** Terminal, in the wording folder where we left off. cd ../../../.. returns to the practice folder; vally lint -e evals/wording.eval.yaml prints one warning and no errors, held until it has been read.  
**Renderer:** terminal (tapes/s18.tape)

> Back up in the practice folder, lint checks the edited file before anything is spent.  _(waits for output:1; finishes before typed:2)_
> It reports no errors, and the usual one warning.  _(waits for output:2; depends on what the demo produced)_
> That warning says that with several graders and no scoring block, every grader has to pass.  _(3s to read after; waits for output:2; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** Terminal in the practice folder. cd into the run's folder; then vally grade -e ../../../evals/wording.eval.yaml --run-dir . --verbose < results.jsonl over two lines; a jump cut; the last blocks of its output fill the screen, each with a '[prompt …]' line and a reason, held until they have been read.  
**Renderer:** terminal (tapes/s19.tape)

> For the judging, we change back into the run's folder.  _(finishes before typed:1)_
> From here, vally grade runs the judge over the twelve saved trials.  _(waits for output:1; finishes before typed:2)_
> It starts no agent, and spends twelve calls to the judge model.  _(finishes before enter:2)_
> A minute or two later, twelve blocks have scrolled past, one for each trial.  _(waits for output:2; depends on what the demo produced)_
> Still on screen are the last two, each with its prompt line: here a tick, and then the judge's reason.  _(6s to read after; waits for output:2; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** Headline 'Reading the judge's reasons'. Two cards, one above the other, each a dark box holding one '[prompt …]' line from our run in full: a tick for a parser entry from terra, whose quoted entry lights; then a cross for haiku's parser entry, whose reason quotes no entry: its cross lights, and later the words 'streaming parser, importer.js'.  
**Renderer:** html (scenes/s20.html)

> Here are two of the twelve reasons in full.
> To this parser entry the judge said yes: it's user-focused, and doesn't describe the implementation.  _(2s to read after; depends on what the demo produced)_
> To this one it said no: the entry states the benefit, but includes implementation details.  _(2s to read after; depends on what the demo produced)_
> Each reason was asked to start with its entry, so that a verdict can be matched to its trial.
> Eleven of the twelve did; this second one didn't, and only its mention of the streaming parser tells us which entry it means.  _(depends on what the demo produced)_

## s21

**Role:** practice · **Mode:** use · **Stage:** write-and-regrade  
**On screen:** Headline 'The judge's twelve verdicts'. A table: one row per stimulus and model (six rows), a column 'Ours' and a column 'Judge', each cell holding the two trials' answers ('no · no', 'yes · yes'). The Judge column lights; then the one cell where the judge differs from us (cache, gpt-5.6-terra). A note: 'from notes/wording-labels.md · our run'.  
**Renderer:** html (scenes/s21.html)

> We write each verdict beside our own answer, and leave our answers as they were.
> Across the twelve entries, the judge said yes to eight and no to four.  _(depends on what the demo produced)_
> Eleven of its verdicts match ours, and one doesn't.  _(3s to read after; depends on what the demo produced)_

## s22 — What the judge found

**Role:** body · **Mode:** think · **Stage:** what-it-found  
**On screen:** Headline 'One rule, followed unevenly'. Two blocks side by side, one per model, each with a large count of its six entries the judge said no to: 'claude-haiku-4.5 · 3 of 6', 'gpt-5.6-terra · 1 of 6'. Each block fills as its count is said.  
**Renderer:** html (scenes/s22.html)

> So what did the judge find?
> We now have a grader for a line of the skill that nothing checked before, and it has already told us something.
> Haiku got a no for three of its six entries: it named the cache both times, and the streaming parser once.  _(depends on what the demo produced)_
> Terra got a no for one, a cache entry that adds, by caching the tag index.  _(depends on what the demo produced)_
> So the rule about writing for people who use the tool is followed unevenly, and until now nothing could show that.

## s23

**Role:** body · **Mode:** think · **Stage:** what-it-found  
**On screen:** Headline 'A reason isn't evidence'. Two blocks side by side: 'Every grader before · code, tested with the oracle and against saved trials' and 'This judge · a model's opinion, not yet tested'. The first fills, then the second.  
**Renderer:** html (scenes/s23.html)

> It's tempting to act on that straight away.
> But every grader before this one was code, which we tested with the oracle and against saved trials.
> This one is a model's opinion.
> In our run it said no to one cache entry, and yes to another that differs by a single word.  _(depends on what the demo produced)_
> Its reasons are well written, but good writing doesn't show that a verdict is correct.

## s24

**Role:** recap · **Stage:** what-it-found  
**On screen:** Headline 'What are the three habits?'. One block, 'a judge you can use', which opens after the question and a pause to show its three parts: 'One question per judge', 'Yes or no', 'Our own answers first'. Each part lights as it is said.  
**Renderer:** html (scenes/s24.html)

> Before you go on: what are the three habits that make a judge's verdicts usable?
> One question per judge.  _(pause 2.5s first)_
> A yes-or-no answer.
> Lastly, our own answers, decided on real examples before the judge gives its own.

## s25

**Role:** next · **Stage:** what-it-found  
**On screen:** 'Next: Check the judge against your own labels' in the display serif. Below, the hand-off question: 'It is a model. Is it right?' A note: 'Exercises are on the lesson page · Source: Hamel Husain, Using LLM-as-a-Judge'.  
**Renderer:** slide (scenes/s25.html)

> You can now write a yes-or-no judge, run it over saved trials, and read its reasons.
> The judge said yes to some entries, and no to others.
> But the judge is a model.
> Is it right?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
