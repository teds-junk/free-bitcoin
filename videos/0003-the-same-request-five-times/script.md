# The same request, five times — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0003-the-same-request-five-times.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** If the same model gets the same request again, does it do the same thing?  
**The viewer starts:** A professional programmer who knows the shell and has watched one Vally run: one changelog request on two models with the first-draft changelog-entry skill, one trial each, a tick for each, and two saved patches that differ (gpt-5.6-terra's entry ends with a made-up pull request number, claude-haiku-4.5's has none). Knows skill, agent, model, eval, eval file, workspace, patch, and the vally eval command with -e, --model and --output-dir. Knows Vally's words stimulus, grader, trial and run; that the eval file's one grader only looks for the words 'notes add'; the results folder (the report, results.jsonl, and a folder per trial numbered from 0, holding workspace.patch); and that a trial costs about two or three cents. Has never run a stimulus more than once, and does not know --runs, --workers, or the words FLAKY and ERROR.

1. **one-sample**: after this, the viewer can say why one trial shows that something can happen, and not how often it does
2. **trials-and-outcomes**: after this, the viewer can predict which of Vally's four words a stimulus gets from what its trials did
3. **workers**: after this, the viewer can say what --workers sets, and why we run two at a time
4. **count-it**: after this, the viewer can run five trials on each model and tally what each trial did from its patch
5. **what-the-tally-says**: after this, the viewer can state, as counts, how often each model invents a pull request number, and say what the grader made of it

## s01 — Does it happen every time?

**Role:** hook · **Mode:** think · **Stage:** one-sample  
**On screen:** Headline 'The same request, five times' in the display serif. Two cards side by side, labelled claude-haiku-4.5 and gpt-5.6-terra, each showing the changelog entry that model wrote in the one trial we have seen, with a small label 'one trial'. '(#42)' lights at the end of the second entry, then both 'one trial' labels.  
**Renderer:** html (scenes/s01.html)

> One model made up a pull request number, and the other didn't.
> It's tempting to decide which model is the careless one, and move on.
> But we've watched each model once.
> Here, you'll run the same request five times on each model, and count how often each one makes up a number.

## s02

**Role:** body · **Mode:** think · **Stage:** one-sample  
**On screen:** Headline 'One trial is one sample'. Two rows, one per model, each a row of five boxes numbered 0 to 4. Box 0 of each row holds what that trial did ('no number', '(#42)'); boxes 1 to 4 are empty outlines. The two filled boxes light, then the empty boxes of each row in turn.  
**Renderer:** html (scenes/s02.html)

> Let's start with why once isn't enough.
> A language model doesn't compute one fixed answer.
> It produces one of many plausible answers, and which one you get varies from run to run, even when nothing else changes.
> An agent adds to that, because each step it takes depends on the step before.
> So a single trial tells you that something can happen, and nothing more.

## s03

**Role:** body · **Mode:** think · **Stage:** one-sample  
**On screen:** Two blocks side by side, no arrow: 'Can this happen? · one trial answers it' and 'How often? · needs several trials of the same stimulus'. The first fills as the colleague is mentioned, then the second as the counts are.  
**Renderer:** html (scenes/s03.html)

> If a colleague made a slip the one time you watched, you wouldn't know whether they slip every time, or one time in ten.
> Those call for different responses.
> For any skill, the questions that matter are how often it goes wrong, and whether that's the same on each model.
> Those are counts, and a count needs several trials of the same stimulus: the same request, checked by the same graders.

## s03b

**Role:** body · **Mode:** think · **Stage:** one-sample  
**On screen:** Headline 'Identical runs, different scores'. One row of bars: the same agent's score on the same coding tasks across repeated runs, drawn as a band 2 to 6 percentage points wide, labelled 'an illustration of the reported range'. Large figure beside it: '2 to 6 percentage points'. Source in small type: 'a 2026 preprint from KTH · one benchmark · not yet peer reviewed'. The figure lights when it is said.  
**Renderer:** html (scenes/s03b.html)

> That variation shows up in measurements, too.
> In a paper from twenty twenty-six, not yet reviewed by other researchers, the same agent ran the same set of coding tasks several times.
> From one identical run to the next, its score, the share of tasks it completed, moved by two to six percentage points.

## s04 — Five trials, four outcomes

**Role:** body · **Mode:** works · **Stage:** trials-and-outcomes · **Introduces:** vally eval, --runs, one-request, typo-fix, workspace.patch  
**On screen:** Dark code box, left: 'vally eval … --runs 5' on one line, and under it a short tree: one-request/ → typo-fix/ → gpt-5.6-terra/ → 0/ 1/ 2/ 3/ 4/ (the eval, the stimulus, the model, the trial), with workspace.patch under 0/. Right, level with each: 'every stimulus, five times, on every model', 'one folder per trial', 'each with its own patch'. '--runs 5' lights, then the five folders, then workspace.patch.  
**Renderer:** html (scenes/s04.html)

> That's the reason; here's how Vally does it.
> Adding dash dash runs five to vally eval repeats every stimulus five times, on every model you name.
> Each one is a trial of its own, in a fresh workspace.
> And each trial gets its own numbered folder, zero to four, with its own patch inside.
> With one stimulus and two models, that makes ten trials.

## s05

**Role:** body · **Mode:** works · **Stage:** trials-and-outcomes · **Introduces:** PASS, FLAKY, FAIL, ERROR  
**On screen:** Headline 'Four words for a stimulus'. Four rows of five boxes, labelled 'an illustration', each row ending in its word. PASS: five ticks. FLAKY: one cross, four ticks. FAIL: five crosses. ERROR: three ticks and two boxes holding a dash. Each row appears and lights as its word is said, one at a time.  
**Renderer:** html (scenes/s05.html)

> With several trials, a stimulus no longer just passes or fails.
> For each model, Vally sums up the stimulus's trials with one of four words.
> Pass means every trial passed.
> Flaky means some trials passed and some failed.
> Fail means no trial passed.
> Finally, error means at least one trial didn't finish, so the stimulus has no verdict, whatever the other trials did.

## s06

**Role:** body · **Mode:** works · **Stage:** trials-and-outcomes  
**On screen:** The ERROR row from the last scene, alone and larger. The two boxes holding a dash light, with the note 'no answer to judge'. Then a line under the row: 'Run it again, or leave the trial out and say so.'  
**Renderer:** html (scenes/s06.html)

> Error is not a kind of failure.
> It means the agent gave no answer to judge, for example because its connection dropped.
> When that happens, we run the command again, or leave that trial out of the count and say that we did.

## s07

**Role:** body · **Mode:** works · **Stage:** trials-and-outcomes · **Introduces:** output, results.jsonl, results.jsonl · one record, spread out  
**On screen:** File panel labelled 'results.jsonl · one record, spread out': the gpt-5.6-terra record from the run we have already seen, with a minimap, scrolled to the end of its trajectory, with 'lines hidden' rows around it. '"output": "Added an Unreleased **Fixed** changelog entry …"' lights, with the note on the right 'the agent's final reply'.  
**Renderer:** html (scenes/s07.html)

> One more thing is saved for every trial, and it matters when a patch comes back empty.
> An empty patch means the agent changed no file.
> Each trial's record in results dot jsonl keeps the agent's final reply, in a field named output.
> That reply usually says why.

## s08 — Why two workers

**Role:** body · **Mode:** works · **Stage:** workers · **Introduces:** --workers  
**On screen:** Dark code box, left: '--workers 2'. Right, level with it: 'how many agent sessions run at once · default 5'. Below, two rows of ten boxes side by side with their labels: '5 workers · 3 of 10 ended in ERROR' (three boxes hold a dash) and '2 workers · all 10 finished'. Under the first row, in a code box, the message: 'Session disconnected while waiting for a response'. The flag lights, then the first row and its message, then the second row.  
**Renderer:** html (scenes/s08.html)

> Before we run ten trials, one more flag.
> Vally doesn't run trials one after another.
> It runs several agent sessions at once, and dash dash workers sets how many; the default is five.
> More at once is faster, but each session holds an open connection to the model service, and those connections can drop under load.
> When we ran ten trials with five workers, three of them ended in error, with the message session disconnected.
> With two workers, all ten finished.
> So we use two whenever a command starts more than a couple of trials, and accept that it takes longer.
> Even at two, a session drops now and then, so an error is still possible.

## s09 — Count it

**Role:** practice · **Mode:** use · **Stage:** count-it  
**On screen:** Headline 'Ten trials, one tally'. An empty tally table: rows claude-haiku-4.5 and gpt-5.6-terra; columns 'Entry, no number', 'Entry, made-up number', 'No entry'. Each column header lights as it is named. The cells stay empty.  
**Renderer:** html (scenes/s09.html)

> That's how it works; now let's count.
> First, we'll run the same stimulus five times on each model, then open the ten patches.
> Each trial goes in one of three columns: an entry with no number, an entry with a made-up number, or no entry at all.
> What would you expect from each model?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s10

**Role:** practice · **Mode:** use · **Stage:** count-it · **Introduces:** ls, -e, --model, --output-dir, one-request.eval.yaml, lesson-3, 2026  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. The vally eval command over four lines, with --runs 5 --workers 2 and --output-dir results/lesson-3; a jump cut; then the model summary, held until it has been read. The screen is cleared out of sight; ls results/lesson-3 shows one folder named with a time.  
**Renderer:** terminal (tapes/s10.tape)

> Here's the run: the command from before, with the two new flags.  _(finishes before typed:1)_
> It spends ten short agent runs.  _(finishes before enter:1)_
> We're watching the summary at the end, where a model gets a tick only when none of its trials failed.  _(finishes before enter:1)_
> About a minute later, there's a tick for each model: on both, the stimulus is a pass.  _(waits for output:1; depends on what the demo produced)_
> Flaky, fail or error would show up as a line of its own above the summary, and here there's none.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> So let's look in the results folder.  _(finishes before typed:2)_
> There's one folder, named with the time of the run.  _(1s to read after; waits for output:2)_

## s11

**Role:** practice · **Mode:** use · **Stage:** count-it · **Introduces:** cd, cat  
**On screen:** Terminal, continuing in the practice folder. cd into the run's folder; cd one-request/typo-fix; ls gpt-5.6-terra shows 0 1 2 3 4; the screen is cleared out of sight; cat gpt-5.6-terra/0/workspace.patch shows the patch, held until it has been read.  
**Renderer:** terminal (tapes/s11.tape)

> We change into it, then into the folders for the eval and the stimulus.  _(waits for output:1; finishes before typed:2)_
> Then we list one model's trials.  _(waits for done:2; finishes before typed:3)_
> Five folders, numbered from zero.  _(1s to read after; waits for output:3)_
> Here's the patch from that model's trial zero.  _(finishes before typed:4)_
> Its entry ends with a pull request number that nobody gave it.  _(7s to read after; waits for output:4; depends on what the demo produced)_

## s12

**Role:** practice · **Mode:** use · **Stage:** count-it  
**On screen:** Two dark code boxes side by side, labelled claude-haiku-4.5 and gpt-5.6-terra. Each lists the entry line that model added in each of its five trials, taken from the ten saved patches, with the trial number 0 to 4 on the left. '(#42)' lights at the end of all five entries on the right; then the left box, where no entry has a number.  
**Renderer:** html (scenes/s12.html)

> Reading the other nine the same way gives us ten entries, five from each model.
> Here's the line each trial added.  _(3s to read after)_
> Terra ended every one of its five entries with a made-up number.  _(depends on what the demo produced)_
> Haiku didn't add a number in any of its five.  _(2s to read after; depends on what the demo produced)_

## s13

**Role:** practice · **Mode:** use · **Stage:** count-it  
**On screen:** The tally table from before, now filled from our run: claude-haiku-4.5 → 5, 0, 0; gpt-5.6-terra → 0, 5, 0. Each row's count lights as that model is named; then the 'No entry' column.  
**Renderer:** html (scenes/s13.html)

> That fills in the tally: five with no number for haiku, five made up for terra, and nothing in the last column.  _(3s to read after; depends on what the demo produced)_

## s14

**Role:** practice · **Mode:** use · **Stage:** count-it  
**On screen:** Dark code box labelled 'results.jsonl · the output of each gpt-5.6-terra trial': the five final replies from our run, one per line, trial number on the left. Right, level with the first: 'the agent's final reply'. '#42' lights in each reply.  
**Renderer:** html (scenes/s14.html)

> The final replies in results dot jsonl tell the same story.
> In our run no patch was empty, so every reply reports an edit.  _(depends on what the demo produced)_
> And terra's replies name the made-up number outright.  _(3s to read after; depends on what the demo produced)_

## s15 — What the tally says

**Role:** body · **Mode:** think · **Stage:** what-the-tally-says  
**On screen:** Headline 'Counts replace an impression'. Two blocks side by side, one per model, each with a large count and a row of five boxes showing which trials made up a number: 'claude-haiku-4.5 · 0 of 5', 'gpt-5.6-terra · 5 of 5'. Under them: 'a made-up pull request number, with the first-draft skill'. Each block fills as its count is said.  
**Renderer:** html (scenes/s15.html)

> So what does the tally say?
> We now have counts in place of an impression.
> On haiku, the skill led to a made-up pull request number in none of its five trials.  _(depends on what the demo produced)_
> On terra, it did in five of five.  _(depends on what the demo produced)_
> That's how the skill behaves on each model, as far as five trials can show, and it's worth fixing in the skill.
> Counts like these are also what we'll compare against, once the skill has been edited.

## s16

**Role:** body · **Mode:** think · **Stage:** what-the-tally-says  
**On screen:** Left: the grader from the eval file in a dark box, with '"notes add"' lit. Right: three blocks, one per tally column, each with what this grader says about it: 'Entry, no number · passes', 'Entry, made-up number · passes', 'No entry · fails'. Each fills green or red as it is spoken; nothing is marked before then.  
**Renderer:** html (scenes/s16.html)

> Every trial that made up a number passed.  _(depends on what the demo produced)_
> This grader looks only for the words notes add, so it passes an entry whether or not it has a number.
> The careful answer would be to change nothing, and ask which pull request to cite.
> That's the one kind of answer this grader would mark as a failure.
> Later in the course, one of our trials does exactly that.

## s17

**Role:** recap · **Stage:** what-the-tally-says  
**On screen:** The four rows of five boxes from earlier, with their words hidden. After the question and a pause, each word appears beside its row and the row lights as it is said: PASS, FLAKY, FAIL, ERROR.  
**Renderer:** html (scenes/s17.html)

> Before you go on: what are the four words Vally uses to sum up a stimulus's trials, and what does each one mean?
> Pass: every trial passed.  _(pause 2.5s first)_
> Flaky: some passed, and some failed.
> Fail: none passed.
> Last, error: at least one trial didn't finish, so there's no verdict.

## s18

**Role:** next · **Stage:** what-the-tally-says  
**On screen:** 'Next: Read the runs before writing graders' in the display serif. Below, the hand-off question: 'What else goes wrong when the requests get messier?' A note: 'Exercises are on the lesson page · Source: Anthropic, Demystifying evals for AI agents (2026)'.  
**Renderer:** slide (scenes/s18.html)

> You can now put a count on a problem, for each model.
> But that was one problem, on one request, found by reading ten patches.
> What else goes wrong when the requests get messier?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
