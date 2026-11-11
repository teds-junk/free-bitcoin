# When a run goes wrong — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0020-when-a-run-goes-wrong.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes for lesson 20 (not narrated).
- Every first run of a broken file fails on purpose: s14 ERROR (command is a mapping), s19 ERROR (timeout),
  s25 FAIL (pattern without (?m)), s31 ERROR (judge call fails). Those takes are the result.
- All eleven tapes are recorded, one take each, on 2026-11-11; everything quoted on screen is our own run
  (src/run/, filled by build-src/collect-run.py; details in src/run/HANDOVER.md).
- Where our run differs from the lesson page: the timed-out trials cost 2.95 AIU (terra) and 0.74 AIU (haiku),
  not 1.26 and 1.02; s34's re-grade passed one trial and failed the other on the judge (the page's passed both);
  s22 quotes this request's two trials in the lesson 18 video's run (9.3 s and 7.7 s), not the page's 11.1 s.
- The demo practice folder already held evals/broken, so s14's hidden setup moved it aside before the visible cp.
- Each checkpoint's earlier runs are moved to results/lesson-20-earlier so the run being read is the only
  folder under results/lesson-20; the page says "use the newest folder".
- s34's tape comment still says "two 2/2 blocks expected"; the tape was not edited after recording.
<!-- /notes -->

## The story

**The question this video answers:** When a run ends in ERROR, FLAKY or a surprising FAIL, how do I find out why without paying for more runs?  
**The viewer starts:** A professional programmer who knows the shell, YAML and regular expressions, and has followed the changelog-entry skill through measuring, grading, judging, pricing, budgets and a regression gate. Knows skill, agent, model, eval file, stimulus, grader, trial, run, workspace, patch (which Vally calls the diff) and the practice folder with its starter; vally eval with -e, --model, --workers and --output-dir; vally lint; the results folder with one folder per trial holding workspace.patch, and results.jsonl with a record per trial; that events.jsonl exists in a trial's folder; the trajectory and its skill_activation event; PASS, FLAKY, FAIL and ERROR, and that ERROR is not a verdict; diff graders such as diff-contains with a pattern, including the (?m) switch that makes a caret match at the start of every line; that every grader must pass and lint's scoring-defaults-applied warning says so; vally grade with --run-dir, which re-grades saved trials for free with diff graders; an LLM judge with a rubric and a judge_model; the timeout under defaults and the max_agent_duration limit; token usage and cost in AIU; --workspace. Has not met the commands field, has not opened events.jsonl, and has no order to look in when a run goes wrong.

1. **four-questions**: after this, the viewer can name the four questions in order and say which fixes need a new run
2. **where-answers-live**: after this, the viewer can say where each question's answer is saved, and tell from a trial's folder how far the trial got
3. **fix-four**: after this, the viewer can diagnose a broken eval from what its failed run left, fix it, and prove the fix with the cheapest check
4. **symptoms**: after this, the viewer can match a symptom to where to look and the cheapest proof, and settle validity and completion before believing a verdict

## s01 — Read before you rerun

**Role:** hook · **Mode:** think · **Stage:** four-questions  
**On screen:** Headline 'When a run goes wrong' in the display serif. Three blocks in a row, no arrows: 'ERROR', 'FLAKY', 'a surprising FAIL', each with a short gloss. They light in turn as the second sentence names them. Under them a lead line: 'Nearly every answer is already on disk'.  
**Renderer:** html (scenes/s01.html)

> Now that our eval files have setup, budgets, judges and several models, more can go wrong that has nothing to do with the skill.
> When a run ends in ERROR, or comes out flaky, or fails when nobody expected it to, running it again is tempting.
> But a run costs agent runs and minutes, and it usually prints the same error again.
> Here, you'll take four broken eval files, find each fault from what the failed run left behind, and prove each fix with the cheapest check.

## s02 — Four questions, cheapest first

**Role:** body · **Mode:** think · **Stage:** four-questions  
**On screen:** Headline 'Four questions, in order'. Four numbered blocks in a row, no arrows: 1 'Is the eval valid?', 2 'Did it complete?', 3 'Why was the result unexpected?', 4 'Does the fix work?'. Each lights as it is asked.  
**Renderer:** html (scenes/s02.html)

> Let's start with the order to look in.
> Vally's debugging guide splits the work into four questions, and each has to be answered before the next one means anything.
> First: is the eval file valid, so that Vally accepts it at all?
> Second: did it complete, so that every trial finished and was graded?
> Third: why was the result unexpected, when the trial did finish?
> Fourth: does the fix work?
> Graders can't be wrong about a trial that didn't finish, and a trial can't finish if the eval file is broken.

## s03

**Role:** body · **Mode:** think · **Stage:** four-questions  
**On screen:** Headline 'Cheapest first'. The same four numbered blocks, each now with where its answer comes from and what it costs: 'vally lint, the run's first lines · free', 'ERROR lines, the trial folder · free', 'evidence, --verbose, the patch · free', 'vally grade, else one new run · cheapest'. The first three light together, then the fourth.  
**Renderer:** html (scenes/s03.html)

> That order is also an order of cost: the first three are answered from what the failed run already printed and saved, for nothing.
> Only the fourth may need a new run, and that depends on what the fix changed.

## s04

**Role:** body · **Mode:** think · **Stage:** four-questions  
**On screen:** Headline 'What did the fix change?'. Two blocks side by side: 'A grader' with 'nothing the agent did changes · grade the saved trials again', and 'The setup, a time limit, the skill' with 'the run itself changes · a new run, often on one model'. Each lights as it is described.  
**Renderer:** html (scenes/s04.html)

> Fixing a grader changes nothing the agent did, so the saved trials can be graded again.
> Fixing the setup, or a time limit, changes the run itself, so it needs a new run, and often one model is enough to prove it.

## s05 — Where each answer lives

**Role:** body · **Mode:** works · **Stage:** where-answers-live · **Introduces:** vally lint  
**On screen:** Headline 'Lint checks the shape'. Two blocks side by side: 'Lint can see' with 'unknown field names · files that don't exist · values of the wrong kind', and 'Lint can't see' with 'what a value means to the program that uses it'. Each lights as it is described.  
**Renderer:** html (scenes/s05.html)

> Those are the questions; here's where each answer is kept, starting with the first.
> Vally lint reads an eval file without starting anything, and reports unknown field names, missing files, and values of the wrong kind.
> Vally eval runs the same checks before it starts any agent.
> What neither can see is what a value means to the program that will use it later.

## s06

**Role:** body · **Mode:** works · **Stage:** where-answers-live · **Introduces:** commands:  
**On screen:** Headline 'Commands run before the agent'. Dark code box, left: three lines of YAML, 'agent_environment:', 'commands:', '- echo hello > note.txt'. Callouts on the right: 'after the files are copied, before the agent starts', 'one command per entry, as a string', 'what it creates is starting state: not in the diff'.  
**Renderer:** html (scenes/s06.html)

> One of our four files uses a field we haven't met: commands.
> It's a list, under the agent environment, of shell commands that Vally runs in the workspace, after copying the files and before the agent starts.
> Each entry is one command, written as a string.
> Whatever the commands create is part of the starting state, so it doesn't appear in the trial's diff.

## s07

**Role:** body · **Mode:** works · **Stage:** where-answers-live  
**On screen:** Headline 'A colon makes a mapping'. Dark code box, left: two list entries, '- echo note: hello' and, below it, the same line wrapped in quotes. Callouts on the right: 'a mapping: key "echo note", value "hello"' beside the first, 'a string' beside the second. The colon lights, then the first entry, then the quoted one.  
**Renderer:** html (scenes/s07.html)

> There's a trap here, and it's in YAML itself.
> Inside a list item, a colon followed by a space turns the line into a key and a value.
> So this entry isn't a string: it's a small mapping, with echo note as its key.
> Lint accepts it, because a list item is allowed to hold a mapping.
> Whatever runs the command then gets a mapping where it expects a string, and says so in its own words.
> Putting the whole line in quotes makes it a string again.

## s08

**Role:** body · **Mode:** works · **Stage:** where-answers-live · **Introduces:** metadata.json, events.jsonl  
**On screen:** Headline 'How far did the trial get?'. A three-row table, 'The trial folder holds' and 'What it means': 'metadata.json only' → 'no agent session started: the failure came during setup'; 'events.jsonl, no workspace.patch' → 'the agent started and was stopped'; 'events.jsonl and workspace.patch' → 'the agent finished: look at the grading or the work'. Each row lights as it is described.  
**Renderer:** html (scenes/s08.html)

> Question two is whether each trial completed.
> Each trial that didn't is reported as ERROR, with one line of explanation, and the same text is saved in the trial's record in results dot jsonl.
> The trial's own folder shows how far it got, by which files exist.
> With only metadata dot json, no agent session started, so the failure came during setup.
> With a session log, events dot jsonl, but no patch, the agent started and was stopped before it finished.
> With both, the agent finished, and anything wrong is in the grading or in the work.

## s09

**Role:** body · **Mode:** works · **Stage:** where-answers-live  
**On screen:** Headline 'The end of a stopped session'. Dark code box, left, labelled 'events.jsonl (end), shortened': six event lines ending 'skill.invoked', turn events, 'abort' with reason 'user_initiated', and 'session.usage_checkpoint' with totalNanoAiu. Callouts on the right: 'the skill had loaded', 'stopped from outside the agent', 'what the session had cost'. Each lights in turn.  
**Renderer:** html (scenes/s09.html)

> That session log, events dot jsonl, is the agent's own raw record, one event per line.
> It matters here because, when a trial is stopped, it's the one place that shows how far the agent got, and what that cost.
> Here's how the log ends when a trial runs out of time.
> This line is the skill loading.
> This one's type is abort, and its reason says the stop came from outside the agent: here, Vally's time limit.
> This last one is a usage checkpoint: what the session had cost so far, about three AIU.  _(depends on what the demo produced)_
> So a trial that ends in ERROR isn't free.

## s10

**Role:** body · **Mode:** works · **Stage:** where-answers-live · **Introduces:** --verbose  
**On screen:** Headline 'Evidence, then the patch'. Dark code box, left: one failing trial's block from a verbose run: the FAIL line, the failing grader with its evidence, the line of turns, tools and tokens, and 'agent output' with the reply. Callouts on the right: 'the grader's evidence', '--verbose adds these', 'the agent's final reply'.  
**Renderer:** html (scenes/s10.html)

> Question three is for a trial that finished with a verdict we didn't expect.
> We start with the grader's evidence, the line Vally prints after each failing grader.
> Then we go through the trial's patch ourselves, and decide who is wrong: the agent or the grader.
> One flag helps here, dash dash verbose: under each failing trial, it adds the number of turns, tool calls and tokens, and the agent's final reply.
> Trials stopped mid-session have no final reply, so verbose adds nothing to a timeout.

## s11

**Role:** body · **Mode:** works · **Stage:** where-answers-live  
**On screen:** Headline 'A judge call can fail'. Dark code box, left, labelled 'results.jsonl · one grader's record': name users-words, status error, kind llm, passed false, score 0, evidence 'LLM judge failed: …'. Callouts on the right: 'no verdict was reached', 'a placeholder, not a judgement', 'the reason, word for word'.  
**Renderer:** html (scenes/s11.html)

> Graders can also fail to reach a verdict at all.
> An LLM judge is a call to another model, and that call can fail; Vally doesn't try it again.
> In the trial's record, the grader then has a status of error, which a grader that simply said no doesn't have.
> Its score is recorded as zero, although nothing was judged.
> The reason is in its evidence, word for word.
> In the run's output, the stimulus is reported as ERROR, with a line saying its verdict isn't valid.

## s12

**Role:** body · **Mode:** works · **Stage:** where-answers-live · **Introduces:** vally grade  
**On screen:** Headline 'What a re-grade can read'. A four-row table, 'Grader', 'Reads' and 'A re-grade costs': diff graders → the saved diffs → nothing; trajectory graders → the saved trajectories → nothing; a judge → the saved diffs → one judge call per trial; file and script graders → the workspace, which is not kept → ERROR: needs a new run. Rows light as they are described. A note under it: 'anything before or during the agent's session: only a new run shows it'.  
**Renderer:** html (scenes/s12.html)

> Question four is whether the fix works, and vally grade, which re-grades the trials a run saved, is usually the cheapest proof.
> Diff graders work from the saved diffs, and trajectory graders from the saved trajectories, so re-grading with them costs nothing.
> Re-grading with a judge costs one judge call per trial, and no agent runs.
> File and script graders need the workspace, which a saved run doesn't keep, so with them a re-grade ends in ERROR.
> Changes to anything before or during the agent's session, such as the setup, the time limit or the skill, only show in a new run.

## s13 — An eval that never starts an agent

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'Four files, one fault each'. A four-row table: the file names merged-list, quick, entry and judged in the first column; the columns 'Fault' and 'Proof of the fix' are empty. The file names light in turn, then the empty 'Proof' column on the question.  
**Renderer:** html (scenes/s13.html)

> That's where the answers are kept; now let's put them to work.
> Our starter folder has four eval files, each with one fault.
> For each one, we run it once, answer the four questions from what the run left, fix it, and prove the fix with the cheapest check.
> Each file's first run goes wrong on purpose.
> Which of the four fixes would you expect to need a new run?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s14

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** cp, vally eval, -e, --model, --workers, --output-dir, merged-list.eval.yaml, -R, broken, lesson-20  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. cp -R copies the four broken files in; vally lint on merged-list.eval.yaml prints that the file is valid. The screen is cleared out of sight. Then vally eval on the same file with both models: the end of its output shows two ERROR lines with 'The "command" argument must be of type string. Received an instance of Object', the model summary with 0/1 for each model, the Saved line as ~/src/demo and, last, a warning about a reporter error.  
**Renderer:** terminal (tapes/s14.tape)

> First, we copy the four broken files into our practice folder.  _(finishes before typed:1)_
> Question one: is the first file valid?  _(waits for output:1; finishes before typed:2)_
> And lint says it is.  _(2s to read after; waits for output:2; depends on what the demo produced)_
> Question two: does it complete?  _(finishes before typed:3)_
> This starts one trial on each model, and here we expect both to end in ERROR.  _(finishes before enter:3)_
> Both did, for the same reason: a command had to be a string, and Vally was handed a mapping.  _(9s to read after; waits for output:3; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** ls, cd, 2026, 0  
**On screen:** Terminal, continuing in the practice folder. ls results/lesson-20 shows one folder named with the time of the run; cd into it, its name completed with Tab; ls of haiku's trial folder prints metadata.json and nothing else. Held until it has been read.  
**Renderer:** terminal (tapes/s15.tape)

> Let's see how far those trials got, starting with what the run saved.  _(finishes before typed:1)_
> There's one folder, named with the time of the run, and we change into it.  _(waits for output:1; finishes before typed:2)_
> Inside, each trial has a folder of its own; this one is haiku's.  _(waits for output:2; finishes before typed:3)_
> It holds metadata dot json and nothing else, so no agent session ever started.  _(3s to read after; waits for output:3; depends on what the demo produced)_
> So the fault is in the setup, not in the skill.  _(waits for output:3; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'YAML read a mapping'. File panel labelled 'broken/merged-list.eval.yaml' showing the whole short file's agent_environment block, with the commands entry '- echo fix: notes add said tittle > merged.txt' marked. A callout beside it: 'key: echo fix'. The entry lights, then the colon after 'fix'.  
**Renderer:** html (scenes/s16.html)

> That brings us to question three: what did the setup do?
> Here's the file, with its commands entry.
> It's the trap we saw, a colon and a space after the word fix, and the same bad value tripped Vally's report writer too.  _(depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** merged-list.eval.yaml · fixed  
**On screen:** Headline 'Quote the whole command'. File panel on the same file after the fix, the commands entry now one quoted string, marked. A callout: 'one string'.  
**Renderer:** html (scenes/s17.html)

> Our fix is to put the whole command in quotes, so it's one string.
> That changes the setup, which happens before the agent starts, so proving it takes a run.

## s18

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Terminal in the practice folder. The same vally eval command with --model claude-haiku-4.5 only; a jump cut; then 'Summary', 'PASS merged-list' and the Saved line.  
**Renderer:** terminal (tapes/s18.tape)

> One model is enough to show that the setup works, so this spends one agent run.  _(finishes before typed:1)_
> About ten seconds later, the stimulus passes.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s19 — A trial that runs out of time

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** quick.eval.yaml  
**On screen:** Terminal in the practice folder. vally eval on broken/quick.eval.yaml with both models and --verbose, over four lines. The end of its output: two ERROR lines, 'Stimulus 'typo-fix' timed out after 5000 ms during turn 1 of 1', the model summary with 0/1 for each model, and the Saved line.  
**Renderer:** terminal (tapes/s19.tape)

> Our second file is called quick; it passes lint as well, so we go straight to question two: does it complete?  _(finishes before typed:1)_
> With verbose added, we'll see whatever detail there is.  _(finishes before enter:1)_
> This file is set up to run out of time, so we expect ERROR on both models.  _(finishes before enter:1)_
> Both trials were stopped: the stimulus timed out after five thousand milliseconds.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> The verbose flag added nothing, because neither agent had a final reply to show.  _(2s to read after; waits for output:1; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Terminal, continuing. cd into this run's folder under results/lesson-20, its name completed with Tab; ls of haiku's trial folder prints events.jsonl and metadata.json, and no workspace.patch.  
**Renderer:** terminal (tapes/s20.tape)

> Again we go into the folder this run saved, and look at one trial.  _(finishes before typed:2)_
> This time there's a session log, events dot jsonl, and no patch: the agent started, and didn't finish.  _(3s to read after; waits for output:2; depends on what the demo produced)_

## s21

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'Stopped, and still paid for'. Dark code box, left, labelled with the trial's events.jsonl: the end of terra's session log from our run: skill.invoked, abort with reason user_initiated, session.usage_checkpoint. Callouts: 'the skill had loaded', 'Vally stopped it', and the cost. Under it a note with each model's cost in AIU.  
**Renderer:** html (scenes/s21.html)

> Terra's session log ends the same way: the skill loads, then the abort, then the checkpoint.  _(depends on what the demo produced)_
> What's new is the bill: about three AIU for this trial, and about three quarters of one for the other model's.  _(depends on what the demo produced)_
> That was spent on two trials that produced nothing.

## s22

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'Five seconds is the limit'. File panel labelled 'broken/quick.eval.yaml', its defaults block with 'timeout: 5s' marked. Callouts: 'the hard limit on each trial' and, from our earlier run with budgets, how long this request's two trials took.  
**Renderer:** html (scenes/s22.html)

> Question three: why did they run out of time?
> Under defaults, the file sets a timeout of five seconds, and that's the hard limit on each trial.
> When we ran this same request earlier, with budgets, its two trials took about eight and nine seconds.  _(depends on what the demo produced)_
> So nothing is wrong with the skill or the agent: five seconds just isn't enough for this request.  _(depends on what the demo produced)_

## s23

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** quick.eval.yaml · fixed  
**On screen:** Headline 'Three minutes, like the rest'. File panel on the same file after the fix, 'timeout: 3m' marked. A callout: 'the value our other eval files use'.  
**Renderer:** html (scenes/s23.html)

> We change it to three minutes, the value in our other eval files.
> This timeout is different from the max agent duration we used before.
> That one stops only the agent, and still grades what it had done.
> Nothing saved can show a trial finishing, so this fix needs a run too.

## s24

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Terminal in the practice folder. vally eval on broken/quick.eval.yaml with both models; a jump cut; then the model summary with a tick and 1/1 for each model, and the Saved line.  
**Renderer:** terminal (tapes/s24.tape)

> That's two agent runs, one for each model.  _(finishes before typed:1)_
> This time both trials finish, and both pass.  _(7s to read after; waits for output:1; depends on what the demo produced)_

## s25 — A grader that fails good work

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** entry.eval.yaml  
**On screen:** Terminal in the practice folder. vally eval on broken/entry.eval.yaml with both models and --verbose; a jump cut; then the end of the output: under Failures, both models' typo-fix with '✘ adds-an-entry  Pattern /^\+.*notes add/ not found in workspace diff', the model summary with 0/1 for each, and the Saved line.  
**Renderer:** terminal (tapes/s25.tape)

> Our third file is called entry; it passes lint too, and we run it with verbose again.  _(finishes before typed:1)_
> Here we expect both models to fail.  _(finishes before enter:1)_
> Both failed the same grader, adds an entry: its pattern wasn't found in the workspace diff.  _(8s to read after; waits for output:1; depends on what the demo produced)_

## s26

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'Both agents say they did it'. Two cards side by side, one per model, each a dark box with what --verbose printed for that trial: the line of turns, tools and tokens, and the agent's final reply. Under them, the grader's evidence line in a dark box. Each card lights as it is quoted, then the evidence.  
**Renderer:** html (scenes/s26.html)

> Further up, verbose printed each agent's final reply.
> Haiku says it added the typo fix to the changelog, under Fixed.  _(depends on what the demo produced)_
> Terra says much the same.  _(depends on what the demo produced)_
> So either both agents are wrong about their own work, or the grader is.

## s27

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** cat, workspace.patch  
**On screen:** Terminal, continuing. cd into this run's folder, its name completed with Tab; cat of haiku's workspace.patch: an added '### Fixed' heading and an added entry that mentions `notes add`. Held until it has been read.  
**Renderer:** terminal (tapes/s27.tape)

> The patch settles question three, so we go into this run's folder and print haiku's.  _(finishes before typed:2)_
> There's an added Fixed heading, and under it an added entry that mentions notes add.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> That's a correct entry, so the grader is the one that's wrong.  _(waits for output:2; depends on what the demo produced)_

## s28

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'A pattern that can't match'. File panel labelled 'broken/entry.eval.yaml', scrolled to its grader, the pattern '^\+.*notes add' marked. Callouts: 'no (?m) in front' and '^ matches only the start of the patch: diff --git'.  
**Renderer:** html (scenes/s28.html)

> Here's the grader, with its pattern.
> It's missing the switch that makes a caret match at the start of every line, so this caret matches only the very start of the patch.
> For a diff contains grader, that means the pattern can never match, and the grader can never pass.

## s29

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** entry.eval.yaml · fixed  
**On screen:** Headline 'Put the switch back'. File panel on the same file after the fix, the pattern '(?m)^\+.*notes add' marked. A callout: 'a fix to a grader: the saved trials can prove it'.  
**Renderer:** html (scenes/s29.html)

> We put the switch back.
> This time the fix is in a grader, so the saved trials can prove it.

## s30

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** --run-dir, results.jsonl  
**On screen:** Terminal in the run's folder; the prompt shows the run's name. vally grade over three lines, with -e pointing at the corrected eval file, --run-dir . and results.jsonl as input. Two blocks, each '✅ typo-fix (1/1 graders passed)' and 'Score: 100.0% | PASSED'.  
**Renderer:** terminal (tapes/s30.tape)

> From the run's folder, vally grade applies the corrected grader to the two saved trials, with no agent runs.  _(finishes before typed:1)_
> It takes the trials from results dot jsonl, and dash dash run dir points at the folder that holds their diffs.  _(finishes before enter:1)_
> Both blocks now say one of one graders passed.  _(6s to read after; waits for output:1; depends on what the demo produced)_

## s31 — A judge call that fails

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** judged.eval.yaml  
**On screen:** Terminal in the practice folder, in a smaller font because the lines are long. vally eval on broken/judged.eval.yaml with both models; a jump cut; then the end of the output: two ERROR lines under Failures, each 'users-words · LLM judge failed: Model "claude-sonnet-5-5" is not available in Copilot' followed by the account's list of models, the model summary with 0/1 for each, two lines saying a trial grade is invalid, and the Saved line.  
**Renderer:** terminal (tapes/s31.tape)

> Our fourth file passes lint with one warning we know, and it has two graders: a pattern, and a judge.  _(finishes before typed:1)_
> Here the agents are expected to finish, and the judge call to fail.  _(finishes before enter:1)_
> Both stimuli are reported as ERROR, and the reason is the judge: its call failed.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> Much of what's on screen is the list of models our account does have, and under the summary, each trial's grade is marked as not valid.  _(3s to read after; waits for output:1; depends on what the demo produced)_

## s32

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'Only the judge failed'. Dark code box, left: the top of haiku's block from our run: 'ERROR  cache · 1/2 graders', 'Grading error; verdict is invalid.', '✘ users-words  LLM judge failed: Model "claude-sonnet-5-5" is not available in Copilot.' Callouts: 'the other grader ran, and passed', 'no verdict from the judge', 'not on the account's list'. Below it, a second dark box in large type with the two spellings one above the other, claude-sonnet-5-5 and claude-sonnet-5.5, labelled 'in the eval file' and 'on the account's list'; the hyphen lights, then the dot.  
**Renderer:** html (scenes/s32.html)

> Let's go back to one block, for questions two and three.
> It says one of two graders, so the pattern grader ran, and it passed.  _(depends on what the demo produced)_
> That means the agents finished, and only the judge failed.  _(depends on what the demo produced)_
> Its evidence gives the reason: the judge model's name isn't on the account's list.  _(depends on what the demo produced)_
> One character differs, just before the last five: the eval file has a hyphen, and the account has a dot.  _(depends on what the demo produced)_

## s33

**Role:** practice · **Mode:** use · **Stage:** fix-four · **Introduces:** judged.eval.yaml · fixed  
**On screen:** Headline 'One character'. File panel labelled 'broken/judged.eval.yaml' after the fix, the defaults block with 'judge_model: claude-sonnet-5.5' marked, then scrolled to its two graders with the diff-contains grader marked. Callouts: 'a dot, as the account spells it' and 'a diff grader: the run saved the diffs'.  
**Renderer:** html (scenes/s33.html)

> Fixing it takes one character, in the judge model line.
> Because this file also has a diff grader, the run saved the diffs, so both trials can be judged again without running an agent.

## s34

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Terminal in the run's folder, smaller font. vally grade over three lines with --verbose and results.jsonl as input. A warning about scoring, then two blocks for cache, each with the judge's reason, which begins by quoting the new entry, and the pattern grader's evidence: the first '2/2 graders passed' and 'Score: 100.0% | PASSED', the second '1/2 graders passed, 1 failed' and 'Score: 50.0% | FAILED', its reason naming caching.  
**Renderer:** terminal (tapes/s34.tape)

> So we re-grade from the run's folder, with verbose, to see the judge's reasons.  _(finishes before typed:1)_
> That costs two judge calls.  _(finishes before enter:1)_
> This time the judge reaches a verdict on both trials, and each of its reasons begins by quoting the entry.  _(6s to read after; waits for output:1; depends on what the demo produced)_
> The judge passes one, and fails the other, whose entry mentions caching: a real verdict about the work, which is what the fix was for.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s35

**Role:** practice · **Mode:** use · **Stage:** fix-four  
**On screen:** Headline 'Four faults, four proofs'. The table from before, now filled: merged-list · a command read as a mapping · one run, on one model; quick · a five-second timeout · a new run; entry · a pattern without (?m) · vally grade, free; judged · a misnamed judge model · vally grade, two judge calls. The two 'new run' rows light, then the two 'vally grade' rows. A note: the total in agent runs and judge calls.  
**Renderer:** html (scenes/s35.html)

> So here are the four, with what proved each fix.
> For the command taken as a mapping, and for the five-second timeout, the fix changed the run itself, so each needed a new run.
> For the pattern, and for the judge model's name, the fault was in the grading, so re-grading the saved trials was enough.
> All four took nine agent runs and two judge calls.  _(depends on what the demo produced)_

## s36 — A symptom table to keep

**Role:** body · **Mode:** think · **Stage:** symptoms  
**On screen:** Headline 'Two looked like verdicts'. Two blocks side by side: 'FAIL' with 'a grader that could not pass', and 'score 0' with 'a judge call that failed'. Each lights as it is described. Under them a lead line: 'valid, then complete, then the verdict'.  
**Renderer:** html (scenes/s36.html)

> So what did those four have in common?
> None of them was a fault in the skill.
> Two of them looked like results.
> Graders that can't pass report a failure that looks just like a real one.
> Failed judge calls leave a score of zero.
> That's why the order matters: we settle whether the eval is valid, and whether it completed, before believing what any verdict says.

## s37

**Role:** body · **Mode:** think · **Stage:** symptoms  
**On screen:** Headline 'Symptom, place, proof'. A four-row table, 'Symptom', 'Where to look' and 'Cheapest proof of a fix', one row for each fault we met: ERROR in milliseconds; ERROR, timed out; FAIL though the patch looks right; ERROR, grading error. The timeout row lights, then the grading-error row.  
**Renderer:** html (scenes/s37.html)

> It's worth keeping these as a table: the symptom, where to look, and the cheapest proof of a fix.
> Two rows deserve a second look.
> Timed-out trials still cost money, so running a timeout again without raising the limit pays the same again for the same ERROR.
> Judge calls that fail aren't tried again.
> So if a judge fails because its service was down for a moment, the trials are still on disk, and re-grading them is the second try.

## s38

**Role:** recap · **Stage:** symptoms  
**On screen:** Headline 'What are the four questions?'. One block, 'when a run goes wrong', which opens after the question and a pause into four numbered parts, each lit as it is said: 'Is it valid? · lint, the first lines', 'Did it complete? · ERROR lines, the trial folder', 'Why unexpected? · evidence, --verbose, the patch', 'Does the fix work? · vally grade, or one new run'.  
**Renderer:** html (scenes/s38.html)

> Before you go on: what are the four questions, in order?
> Is the eval valid: lint and the run's first lines answer that.  _(pause 2.5s first)_
> Did it complete: the ERROR lines and the trial's folder.
> Why was the result unexpected: the grader's evidence, the verbose output, and the patch.
> Does the fix work: a re-grade of the saved trials, or one new run when the fix changes the run itself.

## s39

**Role:** next · **Stage:** symptoms  
**On screen:** 'Next: Keep it working' in the display serif. Below, the hand-off: 'Make it a routine you and a teammate can repeat.' A note: 'Exercises and the full symptom table are on the lesson page · Source: Vally docs, Debugging Evals'.  
**Renderer:** slide (scenes/s39.html)

> You can now find out why a run went wrong from what it left behind, and prove a fix with the fewest agent runs.
> So we can measure, gate and debug.
> What's left is to make it a routine that you and a teammate can repeat.
> That's the next lesson.
> On the lesson page there are exercises, and a longer table of symptoms to keep.
