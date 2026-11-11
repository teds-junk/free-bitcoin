# What a passing trial costs — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0016-what-a-passing-trial-costs.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** Which model, at which reasoning effort, gives the most passing trials for what it costs?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through fifteen lessons of Vally runs on claude-haiku-4.5 and gpt-5.6-terra. Knows skill, eval file, stimulus, grader, trial and run; vally eval with -e, --model, --runs, --workers and --output-dir; PASS, FAIL, FLAKY and ERROR, and that ERROR is not a verdict; the results folder and results.jsonl, with one record per trial holding status, gradeResult and trajectory; token usage (input, output and cache read tokens), that a trial's cost is recorded in nano-AIU, and that one AIU is one cent; the report's Tokens column, which is a median; code graders, script graders and LLM judges; an experiment file with variants, vary, a baseline and overrides; vally experiment run, --dry-run, and the table it prints with stimuli passed, total tokens and trial time; pass rate, and the range around a count from a few trials. Has not compared what variants cost, and does not know cost per passing trial, reasoning effort, the --reasoning-effort flag, the byModel block, or the course's cost calculator.

1. **cost-per-pass**: after this, the viewer can work out cost per passing trial from a total and a count of passes, and say when one variant is beaten on both counts
2. **where-cost-is**: after this, the viewer can find a trial's variant, verdict and cost in a variant's results file, and say what that cost leaves out
3. **effort-as-variant**: after this, the viewer can read an experiment file that varies the model and the reasoning effort, and say how many trials it runs
4. **price-the-variants**: after this, the viewer can find the efforts each model accepts without spending anything, run four variants, and get each one's cost per passing trial
5. **what-the-table-says**: after this, the viewer can choose a model and a reasoning effort, and state the choice with its evidence: passes, cost per passing trial, and what the ranges allow

## s01 — Cost per passing trial

**Role:** hook · **Mode:** think · **Stage:** cost-per-pass  
**On screen:** Headline 'What a passing trial costs' in the display serif. Two blocks side by side from our run: 'gpt-5.6-terra' with its median tokens per trial in large figures, and 'claude-haiku-5.5' with its median tokens per trial. Under them one line: 'Which one costs more?' The terra block lights, then the haiku block, then the question.  
**Renderer:** html (scenes/s01.html)

> Every comparison table so far has ended with a row of tokens, and it's tempting to read the variant with fewer tokens as the cheaper one.
> When we ran it, a typical trial on terra used far fewer tokens than one on a newer haiku model.  _(depends on what the demo produced)_
> But each model has its own price per token, and a cheap trial that fails has bought you nothing.
> Here, you'll run two models at two settings, work out what each passing trial costs, and pick one.

## s02

**Role:** body · **Mode:** think · **Stage:** cost-per-pass · **Introduces:** cost per passing trial  
**On screen:** Headline 'Divide by the passes'. One wide definition block: 'cost per passing trial'. Under it a line built of three blocks: 'total cost · every trial of the variant', a division sign, 'trials that passed'. The total lights, then the passes, then the whole definition.  
**Renderer:** html (scenes/s02.html)

> Let's start with the figure itself.
> Cost per passing trial is a variant's total cost, over all of its trials, divided by the number of trials that passed.
> It's what one useful result costs you.

## s03

**Role:** body · **Mode:** think · **Stage:** cost-per-pass  
**On screen:** Headline 'The cheaper trial costs more'. A table with two rows, variant A and variant B, and four columns: cost of a trial (2 AIU, 3 AIU), trials passed (5 of 10, 10 of 10), total (20 AIU, 30 AIU), per passing trial (4 AIU, 3 AIU). A note under it: 'a made-up example · 1 AIU = 1 cent'. Each cell lights as it is said; at the end A's 2 AIU and A's 4 AIU.  
**Renderer:** html (scenes/s03.html)

> Here's a made-up pair of variants, priced in AIU, which are cents: variant A costs two AIU a trial, and passes five of ten.
> Variant B costs three AIU a trial, and passes all ten.
> For A, that's twenty AIU for five passes: four AIU each.
> For B, thirty AIU buys ten passes: three AIU each.
> So the variant with the cheaper trial gives the more expensive result.
> Every failure is paid for, and then thrown away.

## s04

**Role:** body · **Mode:** think · **Stage:** cost-per-pass  
**On screen:** Headline 'Beaten on both counts'. Two blocks side by side. Left: 'Beaten on both counts · costs more, passes no more often · drop it'. Right: 'A real choice · costs more, passes more often · depends on what a failure costs you'. The left lights for sentences two and three, the right for the last two.  
**Renderer:** html (scenes/s04.html)

> With several variants, we put each one's pass rate beside its cost.
> Then we look for a variant that's beaten on both counts: some other variant costs less, and passes at least as often.
> Any variant beaten that way can be dropped.
> Those left are real choices, a trade between paying more and passing more.
> Which to pick depends on what a failure costs you.

## s05

**Role:** body · **Mode:** think · **Stage:** cost-per-pass  
**On screen:** Headline 'Report cost beside accuracy'. Two blocks side by side: 'Agent rankings · built on accuracy alone' and 'Simple agents that tried again · the same accuracy, a fraction of the cost'. Under them a quote card, 'The researchers’ argument': 'Every evaluation should report cost beside accuracy.' A source note: Kapoor et al., AI Agents That Matter (2024), a preprint. Each lights as it is said.  
**Renderer:** html (scenes/s05.html)

> This way of comparing comes from research on agent benchmarks, which argued that every evaluation should report cost beside accuracy.
> Its authors had found simple agents matching the leaders of accuracy-only rankings, at a fraction of the cost.

## s06 — Where cost is recorded

**Role:** body · **Mode:** works · **Stage:** where-cost-is · **Introduces:** results.jsonl, results.jsonl · one record, spread out, haiku-low/results.jsonl · one record, spread out  
**On screen:** Headline 'One results file per variant'. Dark box, left: the folder an experiment saves, as a tree: results/lesson-16/, a folder named with a time, then haiku-low/results.jsonl, haiku-high/results.jsonl, terra-low/results.jsonl, terra-high/results.jsonl. Callouts on the right: 'a folder for each variant' level with haiku-low, 'one record per trial' level with its results.jsonl.  
**Renderer:** html (scenes/s06.html)

> That's the figure; now let's see where its two numbers are recorded.
> Every experiment saves a folder for each variant, and each folder holds its own results dot jsonl.
> Inside is one record per trial: the record we've met before, with the variant's name added.

## s07

**Role:** body · **Mode:** works · **Stage:** where-cost-is · **Introduces:** variant, status, passed  
**On screen:** Headline 'Did the trial pass?'. File panel labelled 'haiku-low/results.jsonl · one record, spread out', with a minimap and 'lines hidden' rows: the record's top, from "variant": "haiku-low" to "passed": true. Callouts on the right, level with their lines: 'the variant, as the experiment file names it', 'did the trial finish?', 'the verdict'. Each line lights as it is named.  
**Renderer:** html (scenes/s07.html)

> Here's one of them, spread over several lines.
> Variant names the variant this trial belongs to.
> Status is success for a trial that finished, as before.
> And passed, under grade result, is the verdict: passing trials say true here.

## s08

**Role:** body · **Mode:** works · **Stage:** where-cost-is · **Introduces:** byModel  
**On screen:** Headline 'What the trial cost'. The same file panel, scrolled far down the record to the end of "tokenUsage": the "byModel" block (claude-haiku-5.5 with its input tokens, output tokens and call count) and the "cost" block (provider github-copilot, unit nano-aiu, amount). Callouts: 'tokens, split by model', 'billionths of an AIU', 'this trial'. Under the panel one line turns the amount into AIU and cents for the trial's total tokens.  
**Renderer:** html (scenes/s08.html)

> Further down, the token usage ends with two blocks.
> Next, by model splits the tokens between models, and an agent that called two models would list both.
> Then the cost, in nano-AIU as before.
> This trial's amount is about point two three AIU, under a quarter of a cent, for a hundred and five thousand tokens.  _(depends on what the demo produced)_
> That cost appears only when every model call in the trial reported Copilot as its provider.

## s09

**Role:** body · **Mode:** works · **Stage:** where-cost-is  
**On screen:** Headline 'What the figure leaves out'. Two blocks side by side: 'Judge calls · not counted: an eval with a judge costs more than this' and 'A trial that ended in ERROR · may have no usage recorded'. Each lights as it is said.  
**Renderer:** html (scenes/s09.html)

> Two things are missing from that figure.
> Calls that an LLM judge makes to grade the trial aren't counted, so for an eval with a judge, the true cost is higher.
> Also, a trial that ended in ERROR before the agent finished may have no usage recorded at all.

## s10

**Role:** body · **Mode:** works · **Stage:** where-cost-is · **Introduces:** cost calculator  
**On screen:** Headline 'Vally prints no total cost'. Top row, two blocks: 'The experiment’s table · total tokens' and 'report.md · median tokens'. Below, one wide block, 'the course’s cost calculator · a page that reads the results.jsonl files you pick, in your browser', holding three numbered parts: 1 Add · every trial’s cost; 2 Count · the trials that passed; 3 Divide. The top blocks light for sentence two, the calculator for sentence three, the parts in turn for the last sentence.  
**Renderer:** html (scenes/s10.html)

> Vally itself prints no total cost for a variant.
> Each experiment's table gives total tokens, its report gives median tokens, and neither turns tokens into cost.
> So the course has a small calculator: a page that reads the results files you pick, in your browser.
> For each variant, it adds up the cost of every trial, counts the trials that passed, and divides.

## s11 — Reasoning effort as a variant

**Role:** body · **Mode:** works · **Stage:** effort-as-variant · **Introduces:** reasoning_effort  
**On screen:** Headline 'Reasoning effort'. One wide definition block: 'reasoning_effort · how much hidden reasoning the agent’s model does before it replies or calls a tool'. Under it two blocks: 'More effort usually means · more tokens, more time on each call' and 'Sometimes · better results'. The definition lights, then each block.  
**Renderer:** html (scenes/s11.html)

> Besides the model, we'll vary one more setting: reasoning effort.
> Some models can work through a problem in hidden reasoning, before they reply or call a tool.
> Reasoning effort sets how much of that the agent's model does.
> More effort usually means more tokens and more time on each call, and sometimes better results.

## s12

**Role:** body · **Mode:** works · **Stage:** effort-as-variant  
**On screen:** Headline 'Set beside the model'. Dark box, left, labelled 'in an eval file': defaults: with model: claude-haiku-5.5 and reasoning_effort: low under it. Callouts on the right: 'the model' and 'how much it reasons', level with their lines. Below, one block: 'Accepted values depend on the model · Vally checks before any session starts'. The reasoning_effort line lights, then the block.  
**Renderer:** html (scenes/s12.html)

> In an eval file, reasoning effort goes under defaults, beside the model, so an experiment can vary it exactly as it varies the model.
> Which values are accepted depends on the model.
> Vally refuses a value the model doesn't accept before any session starts, and its message lists the values that model does accept.
> So asking for a value that no model has is a free way to see each model's list, and that's how we'll begin.

## s13

**Role:** body · **Mode:** works · **Stage:** effort-as-variant · **Introduces:** cost.experiment.yaml, haiku-low, haiku-high, terra-low, terra-high, claude-haiku-5.5  
**On screen:** Headline 'Four variants, sixty trials'. File panel labelled 'evals/cost.experiment.yaml' with a minimap, callouts on the right. It opens at the top: the evals line ('five stimuli, graded by code'), the vary line ('model and effort, nothing else'), runs: 3 ('15 trials a variant, 60 in all'). Then it scrolls to the variants: haiku-low with model claude-haiku-5.5 and reasoning_effort low, and on to terra-high. Lit in turn: the eval file's name, the vary line, runs: 3, the four variant names, then the claude-haiku-5.5 model line ('a newer haiku: 4.5 takes no effort').  
**Renderer:** html (scenes/s13.html)

> Here's the experiment file we'll run.
> It runs the changelog eval file: five stimuli from earlier, each graded by code, with no judge, so the recorded cost is the whole cost.
> Its variants may differ in the model and in reasoning effort, and in nothing else.
> There are three trials of each stimulus, which makes fifteen trials per variant, and sixty in all.
> Then come the four variants: two models, each at low effort and at high effort.
> For haiku, the file names haiku five point five, a newer model in the same family, because the haiku model we've used so far takes no effort setting, as the first step will show.

## s14 — Price the variants

**Role:** practice · **Mode:** use · **Stage:** price-the-variants  
**On screen:** Headline 'Which costs least per pass?'. Four cards in a row, one per variant, each with its name, its model and its effort: haiku-low (claude-haiku-5.5 · low), haiku-high (claude-haiku-5.5 · high), terra-low (gpt-5.6-terra · low), terra-high (gpt-5.6-terra · high). Nothing is lit while the question is asked and during the beat after it.  
**Renderer:** slide (scenes/s14.html)

> That's the file; now let's run it and price each variant.
> We'll end with one sentence that names the variant we'd choose, and the numbers behind it.
> Which of the four would you expect to cost least for each passing trial?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s15

**Role:** practice · **Mode:** use · **Stage:** price-the-variants · **Introduces:** vally eval, --reasoning-effort, -e, --model, --output-dir, one-request.eval.yaml, lesson-16-efforts  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. The vally eval command over five lines: the one-request eval file, three models (claude-haiku-4.5, claude-haiku-5.5, gpt-5.6-terra), --reasoning-effort list, --output-dir results/lesson-16-efforts. It finishes in a few seconds; the output is longer than the screen and ends on the failures list, where each ERROR line names the efforts that model supports, and the model summary.  
**Renderer:** terminal (tapes/s15.tape)

> First, the free check: we run the eval file with the one typo-fix request, from the start of the course, on three models.  _(finishes before typed:1)_
> Dash dash reasoning effort sets the effort for every trial of a run, as dash dash model sets the model.  _(finishes before typed:1)_
> We give it a value that no model accepts: here, the word list.  _(finishes before typed:1)_
> Every trial should be rejected before it starts, so nothing is spent.  _(finishes before enter:1)_
> Each trial ends in ERROR, as planned, and each error names the efforts that its model accepts.  _(8s to read after; waits for output:1; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** price-the-variants  
**On screen:** Headline 'Two models take an effort'. A table read from that output, one row per model: claude-haiku-4.5 · 'does not support reasoning effort configuration'; claude-haiku-5.5 · low, medium, high, xhigh, max; gpt-5.6-terra · none, low, medium, high, xhigh, max. A note: 'from our account; yours will differ'. Each row lights as it is said, then 'low' and 'high' in the two lower rows.  
**Renderer:** html (scenes/s16.html)

> That output runs past one screen, so here's what it said, model by model.
> Haiku four point five, the model we've used so far, doesn't support reasoning effort at all.  _(depends on what the demo produced)_
> Haiku five point five accepts five values, from low to max.  _(depends on what the demo produced)_
> Terra accepts the same five, and also a value named none.  _(depends on what the demo produced)_
> Low and high are accepted by both, so those are our two efforts.  _(depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** price-the-variants · **Introduces:** vally experiment, --dry-run  
**On screen:** Terminal in the practice folder. vally experiment run on evals/cost.experiment.yaml with --dry-run, over two lines. The plan prints at once: a block for each of the four variants naming its eval and its model; the last blocks are on screen.  
**Renderer:** terminal (tapes/s17.tape)

> Our experiment file is now in the evals folder.  _(finishes before typed:1)_
> Before spending anything, we check the plan with a dry run, which starts no agent.  _(finishes before typed:1)_
> It prints a block for each of the four variants, naming its model, and the last of them are on screen.  _(8s to read after; waits for output:1)_

## s18

**Role:** practice · **Mode:** use · **Stage:** price-the-variants · **Introduces:** --workers, ls, lesson-16, 2026  
**On screen:** Terminal in the practice folder. vally experiment run on evals/cost.experiment.yaml with --workers 2 and --output-dir results/lesson-16, over three lines; a jump cut; then the end of the output: the line about the baseline and the table, with rows for stimuli passed, total tokens and trial time under the four variants, held until it has been read. The screen is cleared out of sight; ls results/lesson-16 shows one folder named with a time.  
**Renderer:** terminal (tapes/s18.tape)

> Now the real run: the same command without the dry run, with two workers, saved under results, lesson sixteen.  _(finishes before typed:1)_
> It spends sixty short agent runs.  _(finishes before enter:1)_
> At the end, we're after the table, with its row of stimuli passed and its row of tokens.  _(finishes before enter:1)_
> Several minutes later, every variant shows five of five stimuli passed, so Vally says that no variant beat the baseline.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> Under that is the row of total tokens, where the two terra variants are lowest, and nothing here mentions cost.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> So let's look in the results folder.  _(finishes before typed:2)_
> There's one folder, named with the time of the run, and inside it, as we saw, is a folder for each variant.  _(1s to read after; waits for output:2)_

## s19

**Role:** practice · **Mode:** use · **Stage:** price-the-variants  
**On screen:** Headline 'Four files, four cards'. The cost calculator's result as the lesson page shows it: four cards in a two-by-two grid, one per variant (name and model), each with Trials, Passing, ERROR, Total cost, In dollars, Per passing trial and Median tokens, filled from our run's four results.jsonl files. Under them the calculator's total line: the trials, the files, the AIU and the dollars, and 'Judge calls are not included.' The cards light together, then 'Passing', 'ERROR', 'Total cost' and 'Per passing trial' on the first card as they are named, then the total line.  
**Renderer:** html (scenes/s19.html)

> We give those four results files to the cost calculator, which reads them in the browser and sends nothing anywhere.
> The page shows a card for each variant, with the trials, how many passed, how many ended in ERROR, the total cost, and the cost per passing trial.
> Underneath is the bill for the whole experiment: about ninety-one AIU, which is ninety-one cents.  _(depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** price-the-variants  
**On screen:** Headline 'One variant beats the rest'. A table from our run: Variant, Passing, Total, Per passing trial, Median tokens, one row per variant. The Passing column lights; then haiku-low's cost per passing trial; then haiku-high's; then both terra rows'; then the haiku-low row alone. Under the table, our sentence as a quote card.  
**Renderer:** html (scenes/s20.html)

> Here are the columns we need, side by side.
> All four variants passed fifteen of fifteen trials.  _(depends on what the demo produced)_
> At low effort, haiku cost about point two one AIU for each passing trial.  _(depends on what the demo produced)_
> At high effort, haiku passed no more often, and cost a little more.  _(depends on what the demo produced)_
> Both terra variants passed no more often, and cost thirteen to fourteen times as much.  _(depends on what the demo produced)_
> So haiku low beats the other three on both counts.  _(depends on what the demo produced)_
> That gives us our sentence: on these five stimuli, haiku at low effort passed all fifteen trials at point two one AIU each, against two point seven six and two point eight three on terra, so we'd run them on haiku low.  _(2s to read after; depends on what the demo produced)_

## s21 — What the table says

**Role:** body · **Mode:** think · **Stage:** what-the-table-says  
**On screen:** Headline 'Tokens measure work, not price'. Two blocks side by side, one per model, from our run. Each has the median tokens of a trial in large figures and, under it, what a trial cost, lowest to highest, in AIU: claude-haiku-5.5 with about 105k tokens and a fraction of an AIU; gpt-5.6-terra with about half the tokens and several AIU. The terra block's cost lights, then its tokens.  
**Renderer:** html (scenes/s21.html)

> So what should we make of that table?
> Every trial passed, so here, cost per passing trial is simply cost per trial.  _(depends on what the demo produced)_
> But the variants that cost the most by far are the ones that used the fewest tokens: tokens measure work, not price.  _(depends on what the demo produced)_

## s22

**Role:** body · **Mode:** think · **Stage:** what-the-table-says  
**On screen:** Headline 'Each model has its own price'. A table with two rows: claude-haiku-4.5 (the first trial these videos ran) and claude-haiku-5.5 (the record from this run), with columns Tokens, Cost, and AIU per 100,000 tokens. A note under it gives how many times cheaper per token the newer model was on our account. The first row's price lights, then the second's, then the note.  
**Renderer:** html (scenes/s22.html)

> The cost of a token depends on the model, even between two versions of one family.
> Our very first haiku trial, on version four point five, cost about two point four AIU for every hundred thousand tokens.  _(depends on what the demo produced)_
> This run's haiku five point five record cost about point two two AIU for the same number of tokens.  _(depends on what the demo produced)_
> On our account, that makes the newer model about eleven times cheaper per token.  _(depends on what the demo produced)_
> So the cost we measure on one model can't be carried over to another: change the model, and you measure again.

## s23

**Role:** body · **Mode:** think · **Stage:** what-the-table-says  
**On screen:** Headline 'Same ranges, separate costs'. Left block: 'Pass rate · 15 of 15 · a range of 80% to 100% · the same for all four variants'. Right block: 'Cost of a trial', with two lines from our run: every claude-haiku-5.5 trial, lowest to highest AIU, and every gpt-5.6-terra trial, lowest to highest AIU, and under them 'every haiku trial cost less than the cheapest terra trial'. Below both, a quote card, 'Our sentence, with the ranges': 'As good, as far as these trials can tell, and far cheaper.' The left block lights, then the right, then the quote.  
**Renderer:** html (scenes/s23.html)

> Now the habit from before: how far can these counts be trusted?
> Fifteen passes in fifteen trials gives a range of eighty to a hundred percent, and every variant has that same range.  _(depends on what the demo produced)_
> So these trials can't tell the variants apart on pass rate, and here they don't need to: the case for haiku low rests on cost.  _(depends on what the demo produced)_
> Each model's most expensive trial cost between two and three times its cheapest, but the two bands are well apart: every haiku trial cost less than the cheapest terra trial.  _(depends on what the demo produced)_
> So the ranges make our sentence more careful: haiku low is as good, as far as these trials can tell, and far cheaper.  _(depends on what the demo produced)_

## s24

**Role:** body · **Mode:** think · **Stage:** what-the-table-says  
**On screen:** Headline 'True of these five requests'. Two blocks side by side: 'These five stimuli · the ones the skill now passes easily' and 'The wording requests, graded by a judge · where the models differed: price them the same way'. Under them a line: 'Prices change, and your account’s may differ: a method to repeat, not facts about the models.' The left block lights, then the right, then the line.  
**Renderer:** html (scenes/s24.html)

> That statement is about these five requests only, the ones the skill now passes easily.
> But the wording requests, the ones graded by a judge, are where the models differed, and they'd need pricing the same way before changing the model for everything.  _(depends on what the demo produced)_
> Prices change, too, and your account's may differ from ours, so treat these numbers as a method you can repeat, not as facts about the models.

## s25

**Role:** body · **Mode:** think · **Stage:** what-the-table-says  
**On screen:** Headline 'What it comes to in dollars'. A table with four rows: 'This experiment' (60 trials, its AIU, its dollars); 'A check after every edit' on the two earlier models (10 trials, about 24 AIU, 24 cents an edit, $4.80 for twenty edits); 'The same check on haiku-low' (5 trials, about 1 AIU, a cent an edit); 'Every stimulus, every night' (30 trials, about 71 AIU, about $21 over thirty nights, plus judge calls). A note says which rows use the average of our own earlier runs on those two models, about 2.4 AIU a trial. Each row lights as it is said.  
**Renderer:** html (scenes/s25.html)

> Let's put that in dollars, at one cent per AIU.
> This experiment's sixty trials came to ninety-one cents.  _(depends on what the demo produced)_
> One check after every edit, with these five stimuli on two models, is ten trials.
> On the two models from earlier in the course, where our trials have averaged about two point four AIU, that's twenty-four cents an edit, or four dollars eighty for twenty edits a month.
> On haiku low alone, the same five stimuli would cost about one AIU: a cent an edit.  _(depends on what the demo produced)_
> Running every stimulus in the course each night, about thirty trials, comes to roughly twenty-one dollars over thirty nights at that earlier average, plus the judge calls that Vally doesn't count.

## s26

**Role:** body · **Mode:** think · **Stage:** what-the-table-says  
**On screen:** Headline 'Small, and it grows'. One wide block: 'Verifying this course · about $11 of agent runs, plus judge calls'. Under it the words 'It grows with' and four small blocks in a row: 'stimuli', 'trials', 'models', 'how often you run'. A note: 'your plan’s monthly allowance is spent first'. The wide block lights, then the four in turn, then the note.  
**Renderer:** html (scenes/s26.html)

> For scale, verifying this whole course took about eleven dollars of agent runs, plus judge calls, which isn't large for one person.
> But it grows with the stimuli, the trials, the models, and how often you run, which is why the cheapest check that answers the question comes first.
> Your plan's monthly allowance is spent first, so much of this may cost you nothing extra.

## s27

**Role:** recap · **Stage:** what-the-table-says  
**On screen:** Headline 'Why divide by the passes?'. One block, 'cost per passing trial', which opens after the question and a pause into three parts: 'Total cost · every trial, failures included'; 'Trials that passed · the useful results'; 'Per model · measured, not carried over'. Each part lights as it is said.  
**Renderer:** html (scenes/s27.html)

> Before you go on: what is cost per passing trial, and why does it divide by the passes?
> It's a variant's total cost, divided by the number of its trials that passed.  _(pause 2.5s first)_
> Dividing by the passes charges each useful result with the failures it took to get it.
> So a cheap variant that often fails can be the more expensive one, and each model has to be measured for itself.

## s28

**Role:** next · **Stage:** what-the-table-says  
**On screen:** 'Next: A model from your own provider' in the display serif. Below, the hand-off question: 'Can Vally run a model from a service of your own?' A note: 'Exercises are on the lesson page · Source: Kapoor et al., AI Agents That Matter (2024)'.  
**Renderer:** slide (scenes/s28.html)

> You can now price the models your Copilot account offers, and state a choice with its evidence.
> But an app may call a model through a service of its own.
> Can Vally run that model too, and what does a passing trial cost there?
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
