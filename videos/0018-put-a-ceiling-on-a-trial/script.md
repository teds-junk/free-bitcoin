# Put a ceiling on a trial — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0018-put-a-ceiling-on-a-trial.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** How do I fail, or stop, a trial that costs or takes too much?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through seventeen lessons. Knows skill, eval file, stimulus, grader, trial, run, patch, results.jsonl and the trial record with its metrics and token usage. Has written diff graders and a script grader, and knows the every-grader-must-pass rule and lint's scoring-defaults-applied warning. Knows vally lint, vally eval with --model, --workers and --output-dir, and vally grade with -e and --run-dir, including that script graders fail every trial in a re-grade because the workspace is gone. Knows the two ways a grader can be wrong, and the habit of testing a grader on saved trials before paying for agent runs. Knows turns as the requests of a conversation. Has run the cost experiment: four variants (haiku-low, haiku-high, terra-low, terra-high), its report.md with median tokens, turns and duration per stimulus, and cost per passing trial. Knows the timeout in the eval file's defaults. Has never limited what a trial may use, and does not know the budget graders or the constraints block.

1. **a-budget-is-a-grader**: after this, the viewer can say what a budget catches, why it is set from measured trials, and why it stays beside a check that the work was done
2. **budget-graders**: after this, the viewer can read a budget grader in an eval file and predict which trials it fails
3. **limits-that-stop**: after this, the viewer can choose between a budget grader, max_agent_duration and max_duration for a trial that runs too long
4. **set-budgets-from-runs**: after this, the viewer can set budgets from measured trials, test them on saved trials in a free re-grade, widen them, add a time limit and run
5. **what-the-limits-caught**: after this, the viewer can say why a budget needs room above the typical trial, and what a token budget does not tell you

## s01 — A budget is a grader

**Role:** hook · **Mode:** think · **Stage:** a-budget-is-a-grader  
**On screen:** Headline 'Put a ceiling on a trial' in the display serif. Two blocks side by side: 'Is the work right?' with the names of the graders written so far beneath it, and 'What did it take?' with 'tokens · time · turns · no grader asks'. The first lights, then the second.  
**Renderer:** html (scenes/s01.html)

> Every grader we've written so far asks whether the work is right.
> None of them asks what it took.
> If a trial writes the right entry after reading the same file forty times, it passes them all, and we pay for every call.
> One trial that loops can cost ten times the usual, and a run every night multiplies whatever slips through.
> Here, you'll put limits on what a trial may use, and test each limit on trials you've already saved.

## s02

**Role:** body · **Mode:** think · **Stage:** a-budget-is-a-grader  
**On screen:** Headline 'A budget is a grader'. One definition block, 'budget · a limit on what one trial may use', above four small blocks: tokens, time, turns, tool calls. Each lights as it is named.  
**Renderer:** html (scenes/s02.html)

> Let's start with what a budget is.
> When we say budget, we mean a limit on what one trial may use: tokens, time, turns, or tool calls.
> Written as a grader, it fails any trial that goes over.

## s03

**Role:** body · **Mode:** think · **Stage:** a-budget-is-a-grader  
**On screen:** Headline 'Two kinds of trouble'. Two blocks side by side: 'a loop · one trial gone wrong' and 'a cost regression · an edit makes every trial read more, or take longer'. Each lights as it is named.  
**Renderer:** html (scenes/s03.html)

> It catches two kinds of trouble.
> One is a trial that loops: a single run gone wrong.
> The second is a cost regression: an edit to the skill after which every trial takes more tokens, or more time.
> No grader of the result would notice that.

## s04

**Role:** body · **Mode:** think · **Stage:** a-budget-is-a-grader  
**On screen:** Headline 'Measure first, then set it'. Three blocks: 'too low · fails good work', 'too high · can never fail', 'measured · set from real trials, tested on a saved run'. Each lights as it is named.  
**Renderer:** html (scenes/s04.html)

> Guessed budgets tend to be wrong in one of the two ways a grader can be wrong.
> Too low, and it fails good work.
> Too high, and it can never fail.
> So we set it from trials we've measured, and a saved run is a free test of whatever we choose.

## s05

**Role:** body · **Mode:** think · **Stage:** a-budget-is-a-grader  
**On screen:** Headline 'Not too much, and right'. Two blocks side by side: 'a budget says · not too much' and 'the other graders say · and it was right'. A note under them: 'a trial that gives up after one turn is inside every budget'.  
**Renderer:** html (scenes/s05.html)

> One more thing: a budget stays beside a check that the work was done.
> Giving up after one turn keeps a trial well inside every budget.
> So the budget says not too much, and only the other graders say it was right.

## s06 — Budget graders

**Role:** body · **Mode:** works · **Stage:** budget-graders · **Introduces:** token-budget, turn-count, wall-time, tool-call-count, results.jsonl, results.jsonl · one trial’s metrics  
**On screen:** Headline 'Four graders, one number each'. File panel labelled 'results.jsonl · one trial's metrics' with hidden-row markers: the lines totalTokens, toolCallCount, turnCount and wallTimeMs of a real trial record. Callouts on the right, level with each line: 'token-budget', 'tool-call-count', 'turn-count', 'wall-time'. Each line lights as its grader is named.  
**Renderer:** html (scenes/s06.html)

> That's the idea; here are the graders that express it.
> Every trial record ends with a metrics block, and four built-in graders each compare one of its numbers with a max.
> Token budget counts input and output tokens together.
> Turn count counts the model's replies.
> Wall time is the agent's working time, by the clock.
> Fourth, tool call count counts the tool calls a trial makes.

## s07

**Role:** body · **Mode:** works · **Stage:** budget-graders  
**On screen:** Headline 'A turn is one reply'. Two blocks side by side: 'a turn in a conversation · one request' and 'a turn in a trial · one reply from the model'. Under them a note: 'one request, several replies · turn-count counts the replies'. The second block lights, then the first, then the note.  
**Renderer:** html (scenes/s07.html)

> That word, turn, needs some care, because it has had another meaning.
> In a conversation, a turn was one request; here, it's one reply from the model inside a single trial.
> Even with one request, a trial takes several replies, and turn count counts the replies.

## s08

**Role:** body · **Mode:** works · **Stage:** budget-graders · **Introduces:** changelog.eval.yaml, max  
**On screen:** Headline 'Three budgets, no names'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, on the end of the first stimulus's graders: the three budget graders, each with a max; it scrolls two rows to the last one's time and back. Callouts on the right: 'passes at or under max', 'a time has its unit', 'no name: Vally names it from type and limit'.  
**Renderer:** html (scenes/s08.html)

> Here's how they look in the eval file, at the end of one stimulus's graders.
> Each takes one setting, max, and passes when the trial's number is at or under it.
> Times are written with their unit.
> None of the three has a name, and that's on purpose.
> Grader names must be unique across the whole file, and these three go under all five stimuli.
> Left unnamed, each one gets a name from its type and its limit.

## s09

**Role:** body · **Mode:** works · **Stage:** budget-graders · **Introduces:** vally grade, -e, --run-dir  
**On screen:** Headline 'Free to test'. Two blocks side by side: 'script grader · needs the workspace, which is gone · fails every trial in a re-grade' and 'budget grader · reads the saved trial record · judged exactly as in a real run'. The second lights.  
**Renderer:** html (scenes/s09.html)

> These graders work only from what the trial record keeps.
> So a re-grade with vally grade judges them exactly as a real run would, unlike a script grader, which needs the workspace.
> That makes a budget cheap to test, with no agent run.

## s10

**Role:** body · **Mode:** works · **Stage:** budget-graders  
**On screen:** Headline 'Over is over'. Two blocks side by side: 'the score · falls in proportion to the overrun' and 'the verdict · fails, however small the overrun'. Each lights as it is named.  
**Renderer:** html (scenes/s10.html)

> What happens just over the line?
> Once a trial is over the max, the grader's score drops only as far as the trial went over, so a trial that is barely over still scores almost one.
> Its verdict doesn't soften: the grader fails, and since every grader must pass, the trial fails.

## s11 — Limits that stop the agent

**Role:** body · **Mode:** works · **Stage:** limits-that-stop · **Introduces:** constraints, max_agent_duration  
**On screen:** Headline 'A limit that stops the agent'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, on the start of the first stimulus: name and prompt (its text hidden), then 'constraints:' and 'max_agent_duration: 1m', then agent_environment. Callouts on the right: 'limits for this stimulus's trials', 'stop the agent, then grade what it did'. A note: 'the record's endReason: agent_timeout'.  
**Renderer:** html (scenes/s11.html)

> Budget graders judge a trial after it has finished, when the tokens are already spent.
> To stop an agent while it's working, a stimulus takes a constraints block.
> It sits under one stimulus; there's no version for the whole file, so each stimulus gets its own.
> Max agent duration is how long the agent may work.
> At that limit, Vally stops it, and then grades whatever it had done by then, like any finished trial.
> In the trial record, the end reason then says agent timeout.

## s12

**Role:** body · **Mode:** works · **Stage:** limits-that-stop · **Introduces:** max_duration, max_turns  
**On screen:** Headline 'Three limits, three behaviours'. Three blocks across the width, titles in mono: 'max_agent_duration · stops the agent, grades its partial work', 'max_duration · a hard limit: the trial is stopped and fails', 'max_turns · the most turns; what happens at the limit is not documented'. Each lights as it is named.  
**Renderer:** html (scenes/s12.html)

> Three limits can go in that block.
> Max agent duration stops the agent and grades its partial work, which suits an unfinished attempt that is still worth grading.
> Max duration is a hard limit: a trial that reaches it is stopped, and counted as a failure.
> It does for one stimulus what the timeout in the file's defaults does for all of them.
> If a stimulus sets both, the agent's limit has to be the shorter one; otherwise the hard limit ends the trial first.
> Max turns is documented as the most turns a trial may take.
> Vally's docs don't say what happens at that limit, so we count turns with the turn count grader instead.

## s13 — Set budgets from your runs

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs · **Introduces:** vally lint, vally eval, --model, --workers, --output-dir  
**On screen:** Headline 'Tested before they are trusted'. Four numbered blocks, no arrows: 1 'measure · what a typical trial uses'; 2 'set · budgets just above it'; 3 'test · on saved trials, free'; 4 'adjust · then a time limit, and one run'. Each fills as it is named; then the question stays up for a beat.  
**Renderer:** html (scenes/s13.html)

> That's how they work; now let's set some.
> First, we find out what a typical trial used in the cost experiment we already ran.
> Then we set budgets just above that, lint the file, and test them on that experiment's saved trials with vally grade, which starts no agent.
> After that we adjust them, add a time limit, and run the five stimuli once, with vally eval.
> With budgets just above the typical trial, how many good trials would you expect them to fail?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s14

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs · **Introduces:** report.md  
**On screen:** Headline 'What a typical trial uses'. Three large numbers side by side, each the largest median in one column of the experiment's report.md across the four variants: tokens, turns, seconds, each with the variant and stimulus it comes from. A note names report.md and the run.  
**Renderer:** html (scenes/s14.html)

> The experiment's report has a table for each variant, with the median tokens, turns and duration of every stimulus.
> Across all four variants, we take the largest value in each of those three columns.
> In our run, that's a little over one hundred six thousand tokens, five turns, and about thirteen seconds.  _(2s to read after; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Headline 'Budgets just above typical'. A three-row table: tokens, turns, time; columns 'largest typical' and 'first budget'. The budget column lights.  
**Renderer:** html (scenes/s15.html)

> We add the three budget graders to the end of every stimulus's graders, with those numbers rounded up a little.
> Ours are one hundred seven thousand tokens, five turns, and thirteen seconds.  _(2s to read after; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs · **Introduces:** cd, lesson-16, 2026, haiku-high  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. vally lint on the eval file prints one warning. The screen is cleared. cd into the one run folder under results/lesson-16, then into haiku-high; then the vally grade command over three lines, as the lesson prints it. Its blocks scroll past and the last screen is held.  
**Renderer:** terminal (tapes/s16.tape)

> First, we lint the file, which costs nothing.  _(finishes before typed:1)_
> No errors, and one warning we've met: with several graders and no scoring block, every grader must pass, which is what we want here.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> Now the free test: we change into the cost experiment's run folder, and then into one variant, haiku high.  _(waits for output:2; finishes before typed:3)_
> This is the re-grade we've used before: the eval file is four folders up, the run dir is this folder, and the saved results are the input.  _(waits for done:3; finishes before typed:4)_
> Script graders can't be re-graded, so two of the stimuli will show a failing line whatever happens.  _(finishes before typed:4)_
> What we're looking for is a failing line that names a budget.  _(finishes before enter:4)_
> Fifteen blocks come back, more than fits on a screen, and one of them, further up, names the token budget.  _(4s to read after; waits for output:4; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Headline 'Barely over, and failed'. Two dark boxes, one above the other. First, labelled as our haiku-high re-grade: the one block that names a budget, as printed: verdict line, the script grader's line, the token budget's line, Score line. Second, labelled 'an earlier run · a trial 28 tokens over': that run's block, whose Score line reads 100.0% and FAILED. Our budget line lights, then our script grader's line, then the earlier run's Score line.  
**Renderer:** html (scenes/s17.html)

> Here's that block, as the re-grade printed it.  _(depends on what the demo produced)_
> One two changes trial went over the token budget, by about one percent.  _(depends on what the demo produced)_
> Its other failing line is the script grader, which a re-grade can't run.  _(depends on what the demo produced)_
> In an earlier run, a trial went twenty-eight tokens over, still printed a score of one hundred percent, and failed all the same.  _(2s to read after)_

## s18

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs · **Introduces:** terra-high  
**On screen:** Terminal, continuing in the haiku-high folder. cd ../terra-high, then the same vally grade command over three lines. Its blocks scroll past and the last screen is held.  
**Renderer:** terminal (tapes/s18.tape)

> Now the same test on the other model's variant, terra high.  _(finishes before typed:1)_
> It's the same command, on that variant's saved trials.  _(waits for done:1; finishes before enter:2)_
> This time it's the turn count budget: two trials each took one turn more than the max of five.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> No trial went over the wall time budget.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Headline 'Wrong budgets, or wrong trials?'. A table of every trial a budget failed in the two re-grades: stimulus, variant, the budget, what the trial used, the max. Under it a note: how many saved trials were re-graded. Rows light as their kind is named.  
**Renderer:** html (scenes/s19.html)

> So which is wrong: the budgets, or the trials?
> For each trial a budget failed, we ask whether it did the work, and whether it looped.
> All three of these trials passed when the experiment ran, and none of them looped.  _(depends on what the demo produced)_
> The token failure was about one percent over, and the two turn failures took one turn more than usual.  _(depends on what the demo produced)_
> So the budgets were wrong, not the trials: set just above typical, they failed three good trials of the thirty we re-graded.  _(2s to read after; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Headline 'Room for normal variation'. The table from before with a third column: 'largest typical', 'first budget', 'wider budget'. The new column lights.  
**Renderer:** html (scenes/s20.html)

> Good trials vary from one to the next, and a budget has to leave room for that, so we raise each one to about twice the largest typical value.
> Ours become two hundred fifteen thousand tokens, ten turns, and thirty seconds.  _(2s to read after; depends on what the demo produced)_

## s21

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Terminal, continuing in the terra-high folder. The same vally grade command; its blocks scroll past. The screen is cleared. cd ../haiku-high and the same command again. The screen is cleared. cd ../../../.. back to the practice folder.  
**Renderer:** terminal (tapes/s21.tape)

> Then the same re-grade again, here in terra high.  _(finishes before typed:1)_
> Only the script graders fail now, as they did before; no block names a budget.  _(6s to read after; waits for output:1; depends on what the demo produced)_
> Once more in haiku high.  _(waits for output:2; finishes before typed:3)_
> It's the same there.  _(9s to read after; waits for output:3; depends on what the demo produced)_
> That's the free testing done, so we go back to the practice folder.  _(waits for output:4)_

## s22

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Headline 'Three trials, then none'. A two-row table: 'first budgets' and 'wider budgets'; columns: trials that failed token-budget, turn-count, wall-time, and any budget. The second row lights.  
**Renderer:** html (scenes/s22.html)

> Under the first budgets, three trials failed a budget; under the wider ones, every budget passes every trial.  _(depends on what the demo produced)_
> No agent ran to find that out.

## s23

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs · **Introduces:** lesson-18  
**On screen:** Terminal in the practice folder. vally lint on the eval file. The screen is cleared. The vally eval command over three lines, as the lesson prints it, with --output-dir results/lesson-18; a jump cut; then the summary with a count for each model.  
**Renderer:** terminal (tapes/s23.tape)

> Last, the time limit: the constraints block from earlier is now under each of the five stimuli, with a max agent duration of one minute.  _(finishes before typed:1)_
> Lint has no errors.  _(5s to read after; waits for output:1; depends on what the demo produced)_
> Now one run of the five stimuli on both models, with the budgets and the limit in place.  _(finishes before typed:2)_
> It spends ten short agent runs.  _(finishes before enter:2)_
> What we're hoping for is five of five under each model.  _(finishes before enter:2)_
> About a minute later, that's what both models show: every trial passed, budgets included.  _(8s to read after; waits for output:2; depends on what the demo produced)_

## s24

**Role:** practice · **Mode:** use · **Stage:** set-budgets-from-runs  
**On screen:** Headline 'Nothing near a limit'. A three-row table: tokens, turns, time; columns 'largest in this run', 'budget', and for time also the one-minute limit. The first column lights.  
**Renderer:** html (scenes/s24.html)

> During that run, the largest trial used about seventy-six thousand tokens and five turns, and the slowest took twelve and a half seconds.  _(depends on what the demo produced)_
> So every trial stayed well inside the budgets, and the one-minute limit never came into it.  _(2s to read after; depends on what the demo produced)_

## s25 — What the limits caught

**Role:** body · **Mode:** think · **Stage:** what-the-limits-caught  
**On screen:** Headline 'Typical is a middle value'. Two blocks side by side with large figures: the count of good trials the first budgets failed, out of those re-graded; and the turns terra-high took for one request. Each lights as it is said.  
**Renderer:** html (scenes/s25.html)

> So what did the limits catch?
> Our first budgets, set just above the typical trial, failed three good trials of thirty.  _(depends on what the demo produced)_
> That's a grader failing correct work, and the saved trials caught it before any agent ran.
> It happened because a typical trial is a middle value: half of all trials are above it.
> Terra took four, five or six turns for the same request.  _(depends on what the demo produced)_
> So a budget at the median fails normal variation.

## s26

**Role:** body · **Mode:** think · **Stage:** what-the-limits-caught  
**On screen:** Headline 'Room above normal'. Two blocks side by side under the label 'a budget at about twice the largest typical trial': 'a loop, at ten times the usual · fails' and 'one turn more than usual · passes'. Each lights as it is said.  
**Renderer:** html (scenes/s26.html)

> Budgets are for the trial that runs away, at several times the usual cost, so they need room above normal.
> Twice the largest typical trial still fails a loop that costs ten times as much.
> It passes a trial that took one turn more than usual.
> Whenever the model, the effort or the skill changes, the budgets get tested again, the same free way.

## s27

**Role:** body · **Mode:** think · **Stage:** what-the-limits-caught  
**On screen:** Headline 'What a token budget doesn't do'. A table: model, tokens in a typical trial; three rows. Beside it one block with the token budget every model shares. Rows light in turn.  
**Renderer:** html (scenes/s27.html)

> It's worth seeing what a token budget doesn't do.
> One budget holds for every model the eval runs on, and the models differ.
> Across our runs, a typical trial used about a hundred and five thousand tokens on haiku five point five, seventy-five thousand on haiku four point five, and sixty-one thousand on terra.  _(depends on what the demo produced)_
> So a budget set for the hungriest model is loose for the others.
> Tokens aren't price, either, because a token costs a different amount on each model: in the cost experiment, terra used the fewest tokens and cost the most.  _(depends on what the demo produced)_
> Token budgets catch a trial that loops; choosing a cheaper model is what cost per passing trial is for.

## s28

**Role:** body · **Mode:** think · **Stage:** what-the-limits-caught  
**On screen:** Headline 'A limit for the bad day'. Two blocks side by side with large figures: '1m · max_agent_duration: stop the agent, grade what it wrote' and '3m · the file's timeout'. The first lights.  
**Renderer:** html (scenes/s28.html)

> Our time limit did nothing in that run, which is what a limit should do on a good day.  _(depends on what the demo produced)_
> It's there for the day an agent stalls.
> Then a nightly run loses one minute on that trial, where the file's timeout would lose three, and it still grades what was written.

## s29

**Role:** recap · **Stage:** what-the-limits-caught  
**On screen:** Headline 'Budget, or limit?'. One block, 'a ceiling on a trial', which after the question and a pause opens into two parts: 'a budget grader · judges the finished trial' and 'a limit under constraints · acts while the agent works'. Each part lights as it is said.  
**Renderer:** html (scenes/s29.html)

> Before you go on: how does a budget grader differ from a limit under constraints?
> Budget graders judge the finished trial, and fail it if a number is over the max; by then, the cost is spent.  _(pause 2.5s first)_
> Limits act while the agent is working: max agent duration stops it and grades what it produced, and max duration stops it and fails the trial.

## s30

**Role:** next · **Stage:** what-the-limits-caught  
**On screen:** 'Is it worse than before' in the display serif, under the eyebrow 'Next'. Below, the hand-off question: 'Can a check say no worse than before, in quality and in cost?' A note: 'Exercises are on the lesson page · Source: Vally docs, Graders: metric thresholds'.  
**Renderer:** slide (scenes/s30.html)

> You can now add budget graders and an agent time limit, and test each budget on saved trials in a free re-grade.
> Budgets now sit beside the other graders on every trial.
> Before relying on an edit, you'd want a check that says no worse than before, in quality and in cost.
> Can Vally decide that?
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
