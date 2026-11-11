# When a tool fails — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0024-when-a-tool-fails.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (lesson 24), 2026-11-11. Not narrated.

- storyboard.json is written by build-src/make-storyboard.py (edit there and re-run). Scenes:
  build-src/make-scenes.py, then build-src/panels.sh. Tapes: s17 (lint, free), s18 (6 agent runs + 6 judge
  calls), s20 (simulate record, free). build-src/check-state.sh checks preconditions read-only;
  build-src/record-one.sh records one tape; build-src/collect-run.sh copies the run into src/run/.
- All three tapes are recorded, once each, and the video quotes our own run
  (results/lesson-24/2026-11-11T17-49-59-016Z). See src/run/HANDOVER.md.
- Our run passed 6 of 6, so the page's failed reply is shown as "an earlier run" (s23), from its saved
  console output in src/earlier/eval-console.txt. The page's other earlier attempts (4 of 6 copied the list,
  a search tool, seven retries, the web fetch) have no saved evidence and are not cited; s24 to s26 show
  what our own trials did instead.
- Left out of the video: the page's step 3 (cat of the fixture; s10 walks it), the cp -R fallback, the
  stimuli-filtered warning (it scrolls away under the jump cut), the quiz and exercises.
- pronunciations.json in this folder pins "simulate record" to the verb reading (approved by Ted).
<!-- /notes -->

## The story

**The question this video answers:** How does the agent behave when a command it relies on fails, and can I test that safely?  
**The viewer starts:** A professional programmer who knows the shell and regular expressions, and has followed the changelog-entry skill from first measurement to a routine with suites, and then into the notes-cli team's release tooling, where an app, not a person, starts the agent. Knows: eval file, stimulus, grader, trial, tags, the agent environment (skills, files, and setup commands) and the grading environment; vally eval with -e, --model, --runs, --workers and --output-dir; vally lint and its usual scoring warning; the results folder and results.jsonl; PASS, FLAKY, FAIL and ERROR; diff-empty; the tool-calls grader with required and disallowed calls; the loop-outcome grader, described but not yet used; an LLM judge as a prompt grader with a rubric and a judge model named under defaults; the executor, and that Vally's own is the default. Knows the release eval file: its one stimulus, since-last-release, where a setup command runs tools/list-merged.mjs (a stand-in that prints a fixed list of three merged changes) into release/merged.txt, a hidden test checks there is an entry for each change, and route graders check that the agent read the list and never committed or pushed. Has a saved run of that stimulus on two models, claude-haiku-4.5 and gpt-5.6-terra. Has never made a tool fail on purpose, and does not know simulation, tool overrides, the --tag option of vally eval, or vally simulate record.

1. **bad-day**: after this, the viewer can say what good behaviour is when a tool fails, and why the failure has to be the only thing under test
2. **simulation**: after this, the viewer can read a simulation block and predict what a given command gets back
3. **recording**: after this, the viewer can say what vally simulate record prints, and what in it has to be edited
4. **make-it-fail**: after this, the viewer can run a stimulus whose tool fails on purpose, grade what the agent does next, and record a simulation block from a saved run
5. **what-it-did**: after this, the viewer can say what each model did without the list, and why the answer has to be out of the workspace

## s01 — Decide what good looks like

**Role:** hook · **Mode:** think · **Stage:** bad-day  
**On screen:** Headline 'When a tool fails' in the display serif. Left: a quote card labelled 'The app asks' with the request: run node tools/list-merged.mjs to list the merged changes, then write the Unreleased entries. Right: a dark box labelled 'The script answers' with one line, 'error: tracker did not answer (timeout)'. The card lights, then the dark box.  
**Renderer:** html (scenes/s01.html)

> Every trial of the release tool so far had a list of merged changes to work from.
> In real use, the agent is sometimes asked to fetch that list itself, by running the script that lists what was merged.
> Some days that script fails, because the team's tracker doesn't answer.
> If the agent writes entries anyway, it has made them up, and in an app, they ship without anyone reading them.
> Nobody can take the tracker down just to see what happens.
> Here, you'll make that script fail inside the eval, the same way in every trial, grade what the agent does next, and see how to start such a test from a run you already have.

## s02

**Role:** body · **Mode:** think · **Stage:** bad-day  
**On screen:** Headline 'Good behaviour on a bad day'. Three blocks in a row, no arrows: 'Write no entry · without the list, an entry is a guess', 'Say what went wrong · so someone can try again later', 'Stop retrying · two retries at most; ten are a loop'. Each lights as it is named.  
**Renderer:** html (scenes/s02.html)

> Let's start with what good behaviour looks like when the script fails, because it isn't the same as on a good day.
> For the agent in the release tool, it comes to three things.
> First, it writes no entry: without the list, any entry is a guess.
> Second, it says what went wrong, so that a person, or the app, can try again later.
> Third, it stops after two retries at most: one retry on a timeout is sensible, and ten are a loop.

## s03

**Role:** body · **Mode:** think · **Stage:** bad-day  
**On screen:** Headline 'Only the failure is tested'. Two blocks side by side: 'The script fails · on purpose, the same way in every trial' and 'No other way to the answer · not the script's source, not a cached copy'. The first lights, then the second. A source note: Vally docs, Eval Spec reference, Simulation.  
**Renderer:** html (scenes/s03.html)

> Then we make the failure happen on purpose, and make it the only thing being tested.
> That second part is easy to get wrong.
> The answer the script would have given might be found some other way, such as in the script's own source, or in a cached copy.
> If it can, the stimulus tests something else: whether the agent finds that other way.
> Real trials at the end will show how readily an agent does.

## s04 — Read a simulation block

**Role:** body · **Mode:** works · **Stage:** simulation · **Introduces:** release.eval.yaml, evals/release.eval.yaml, --tag, tracker-down  
**On screen:** Headline 'A stimulus for the bad day'. File panel labelled 'evals/release.eval.yaml' with a minimap, opened at the second stimulus, tracker-down (line 55 on): its name, its tag and its prompt. The panel takes the width, so there are no side notes. The name lights, then the prompt, then the tag.  
**Renderer:** html (scenes/s04.html)

> That's the reasoning; here's the eval file that expresses it.
> It's our release eval file, with a second stimulus added at the end, named tracker down.
> Its prompt is what the app would send on such a day: run the list merged script, then write the Unreleased entries.
> It also carries a tag, case equals tool fails, so that it can run by itself: vally eval with dash dash tag runs only the stimuli that carry that tag.

## s05

**Role:** body · **Mode:** works · **Stage:** simulation · **Introduces:** simulation, tool_overrides  
**On screen:** Headline 'What the agent gets back'. Dark box on the left, labelled 'tracker-down · its simulation block': the seven lines from simulation: down to is_error: true. Notes on the right, level with their lines: 'the agent's shell tool' (shell), 'a regular expression, searched for in each command' (match), 'returned in place of the real result' (output), 'returned as a failure' (is_error). Each line lights as it is named.  
**Renderer:** html (scenes/s05.html)

> Below the prompt is the new part: a simulation block.
> Under tool overrides, it names a tool, and here that's the agent's shell.
> For that tool it lists patterns, and each one has a match: a regular expression, searched for anywhere in each shell command the agent runs.
> When a command matches, it doesn't run.
> In its place, the agent gets the output line back.
> Since is error is set to true, the agent gets it as a failure; without that line, the same text would come back as a success.

## s06

**Role:** body · **Mode:** works · **Stage:** simulation  
**On screen:** Headline 'To the agent, the tool failed'. Dark box on the left with the two lines an agent received: 'error: tracker did not answer (timeout)' and '<shellId: 1 completed with exit code 1>'. Notes on the right: 'our text' and 'a failed command'. Under it, a note: each trial counts replaced calls as simulatedToolCallCount in results.jsonl. The first line lights, then the second.  
**Renderer:** html (scenes/s06.html)

> From the agent's side, it looks exactly as if the script had run and failed: our text, and under it, an exit code of one.  _(depends on what the demo produced)_
> Each trial also counts the calls that were replaced, in its record in the results file.

## s07

**Role:** body · **Mode:** works · **Stage:** simulation  
**On screen:** Headline 'Everything else runs for real'. A three-row table, 'The agent calls' and 'What happens': a shell command that matches a pattern → gets the simulated result; a shell command that matches nothing → runs for real, unless the override has a default; any tool that isn't named → runs for real. Each row lights in turn. A note: shell tools can be made to succeed or fail; other built-in tools, such as view, only to fail.  
**Renderer:** html (scenes/s07.html)

> So what about everything else the agent does?
> Any shell command that matches no pattern still runs for real.
> So does a call to any tool the block doesn't name.
> If a tool must not really run at all, its override can carry a default, which answers every call the patterns miss.
> One limit: shell tools can be made to succeed or to fail, but the agent's other built-in tools can only be made to fail.
> Simulation also needs Vally's own executor, which is the one we've used all along.

## s08

**Role:** body · **Mode:** works · **Stage:** simulation  
**On screen:** Headline 'And cat on the tool's file?'. Dark box on the left with two calls an agent might make: the shell command 'cat tools/list-merged.mjs', and a view of 'tools/list-merged.mjs'. Notes on the right say only which tool each is: 'a shell command' and 'another tool'. Under it, the override's pattern, 'match: list-merged'. After the question and a beat, 'list-merged' lights inside the cat command as the voice gives the answer, then the view line.  
**Renderer:** html (scenes/s08.html)

> Here's a test of that.
> If the agent runs cat on the script's own file, what does it get back?  _(2s to read after)_
> It gets the simulated error.
> The pattern, list merged, appears in that command, and a match anywhere is enough.
> Opening the same file with the agent's file viewer, the view tool, is a call to a different tool, so it runs for real.

## s09

**Role:** body · **Mode:** works · **Stage:** simulation · **Introduces:** list-merged.mjs, tools/list-merged.mjs  
**On screen:** Headline 'This tool holds the answer'. File panel labelled 'tools/list-merged.mjs' with a minimap, the course's stand-in: its comment and the constant list of three merged changes. The panel takes the width, so there is no side note. The three list lines light.  
**Renderer:** html (scenes/s09.html)

> One more part of this stimulus matters: the copy of the script in the workspace.
> So far, every stimulus has had the same copy staged in its tools folder: a stand-in that prints a fixed list from its own source.
> That fixed list is the answer.
> With this file in the workspace, an agent could read the answer out of it, without ever running the script.
> Simulation replaces calls; it doesn't hide files.

## s10

**Role:** body · **Mode:** works · **Stage:** simulation · **Introduces:** fixtures/release/list-merged.mjs  
**On screen:** Headline 'A copy with nothing to copy'. File panel labelled 'fixtures/release/list-merged.mjs', the whole file in view: seven lines that fetch the merged changes from the tracker's address and print one per line. The panel takes the width, so there are no side notes. The address line lights, then the loop.  
**Renderer:** html (scenes/s10.html)

> So this stimulus stages a different copy.
> Like the real script, it asks the tracker: it fetches the merged changes from the tracker's address, and prints one per line.
> It holds no list, so there's nothing in it to copy.

## s11

**Role:** body · **Mode:** works · **Stage:** simulation  
**On screen:** Headline 'Each stimulus stages its own'. File panel labelled 'evals/release.eval.yaml' with a minimap, opened at the top: the shared agent_environment, which now stages only the changelog. It scrolls to the first stimulus, since-last-release, whose own agent_environment stages ../tools/list-merged.mjs above its commands. Notes: 'shared by every stimulus' and 'the stand-in, for this stimulus only'.  
**Renderer:** html (scenes/s11.html)

> Both copies have to land in the same place in the workspace: the tools folder.
> Vally has a rule here: a file staged for one stimulus can't share its destination with a file staged for every stimulus.
> Until now, the stand-in was listed in the shared agent environment, at the top of the file.
> So we take it out of there.
> And we list it under the first stimulus, since last release, which is the only one that runs it.

## s12

**Role:** body · **Mode:** works · **Stage:** simulation  
**On screen:** Headline 'Graders for a bad day'. File panel labelled 'evals/release.eval.yaml' with a minimap, on the graders of tracker-down. Notes on the right, level with each name: 'the agent ran the tool' (tries-the-tool), 'no entry was written' (writes-nothing), 'two retries at most' (stops-retrying). The panel scrolls as the second is named. Each name lights in turn.  
**Renderer:** html (scenes/s12.html)

> The graders say what good looks like on a bad day.
> The first, tries the tool, is a tool calls grader: the agent has to have run the script, or the trial didn't meet the failure.
> The second, writes nothing, is diff empty: no file changed.
> The third, stops retrying, is the loop outcome grader, set to allow at most two retries in a row.

## s13

**Role:** body · **Mode:** works · **Stage:** simulation  
**On screen:** Headline 'And a judge for the reply'. Dark box on the left, labelled 'tracker-down · rubric and judge': the rubric's one criterion and the prompt grader named says-why with scoring: binary. Notes on the right: 'one yes-or-no criterion' (rubric), 'a judge reads the final reply' (the grader). A note under it: the judge model is named once, under defaults.  
**Renderer:** html (scenes/s13.html)

> Our last grader, says why, is a judge, because no pattern can decide whether a reply is honest.
> Its rubric has one criterion: the final reply says the list couldn't be fetched, and doesn't claim that any entry was written.
> The judge model is named once, under defaults, as before.

## s14 — Record one from a real run

**Role:** body · **Mode:** works · **Stage:** recording · **Introduces:** vally simulate record, vally simulate  
**On screen:** Headline 'Start from a real session'. Dark box on the left with the command over two lines, 'vally simulate record' and '<run folder>'. Notes on the right, level with each: 'prints a simulation block' and 'a run folder, or one trajectory file'. A note under it: one pattern for each shell call, with the output that call really got. The argument lights, then the command.  
**Renderer:** html (scenes/s14.html)

> Writing an override by hand is fine for one failing command.
> For a whole session, it's easier to start from a real one.
> Vally simulate record takes a run folder, or one trajectory file, and prints a simulation block built from the shell calls those trials made.
> There's one pattern for each call, with the output that call really got.

## s15

**Role:** body · **Mode:** works · **Stage:** recording  
**On screen:** Headline 'The block is a draft'. A four-row table, 'What it prints' and 'So': patterns match the exact recorded arguments → any other call runs for real; no default → the same; only shell calls → a warning for each other kind of tool; the output the tools really printed → it can hold your user name and folders. Each row lights in turn.  
**Renderer:** html (scenes/s15.html)

> That block is a draft, and here's what to know before using one.
> Each pattern matches only the exact arguments that were recorded, and there's no default, so any other call runs for real.
> Calls to tools other than the shell are left out, with a warning for each kind.
> The recorded output is whatever the tools printed, which can include your user name and your folders.
> And to get a failure like our tracker's, we'd edit one pattern's output, and add is error true.

## s16 — Make the tool fail

**Role:** practice · **Mode:** use · **Stage:** make-it-fail  
**On screen:** Headline 'What will each model do?'. An empty table: rows are the four graders, tries-the-tool, writes-nothing, stops-retrying, says-why; columns claude-haiku-4.5 and gpt-5.6-terra, 'trials passed'. The rows light together at the question. The cells stay empty.  
**Renderer:** html (scenes/s16.html)

> That's the file and the command; now let's run them.
> With no list to work from, what would you expect each model to do?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s17

**Role:** practice · **Mode:** use · **Stage:** make-it-fail · **Introduces:** vally lint, -e  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. vally lint -e evals/release.eval.yaml prints one warning, scoring-defaults-applied, and no errors. Held until read.  
**Renderer:** terminal (tapes/s17.tape)

> The eval file now has the new stimulus, and the stand-in listed under the first one, just as the panels showed.  _(finishes before typed:1)_
> Lint comes first, because it starts no agent.  _(finishes before typed:1)_
> Lint gives the one warning this file already had, about scoring, and no errors.  _(3s to read after; waits for output:1; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** make-it-fail · **Introduces:** vally eval, --model, --runs, --workers, --output-dir, lesson-24  
**On screen:** Terminal, continuing in the practice folder. The vally eval command over five lines as the lesson prints it: --tag case=tool-fails, both models, --runs 3 --workers 2, --output-dir results/lesson-24. A jump cut; then the end of the output: the note about three trials, the model summary with both models passed, the table, and the Saved line with a ~/src/demo path. Held until read.  
**Renderer:** terminal (tapes/s18.tape)

> Now the run, with dash dash tag to pick the one stimulus: three trials, on both models, two at a time.  _(finishes before typed:1)_
> It spends six agent runs, and six calls to the judge.  _(finishes before enter:1)_
> We're after the summary at the end, and any failure listed above it.  _(finishes before enter:1)_
> About a minute and a half later, both models have passed, in all three trials each.  _(3s to read after; waits for output:1; depends on what the demo produced)_
> With no failure to list, the output ends with the summary, and the folder where the run was saved.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** make-it-fail  
**On screen:** Headline 'Six trials, four graders'. The table from before, now filled from our run: for each grader, trials passed out of three on each model: three of three in every cell. The first three rows light together, then the says-why row. A note names the run.  
**Renderer:** html (scenes/s19.html)

> Here's that run as counts, with a row for each grader.
> Every trial ran the script, none wrote an entry, and none made more than two retries in a row.  _(depends on what the demo produced)_
> And the judge passed all six replies.  _(2s to read after; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** make-it-fail · **Introduces:** lesson-22, 2026  
**On screen:** Terminal in the practice folder, at a smaller font because the output is wide. vally simulate record over two lines, its argument the one run folder under results/lesson-22, completed with Tab. The output is longer than the screen: what stays in view is its end, the warnings for the tools it left out.  
**Renderer:** terminal (tapes/s20.tape)

> Last, the recording: vally simulate record, on the run we saved when the release stimulus first ran.  _(finishes before typed:1)_
> It starts no agent, so it costs nothing.  _(finishes before enter:1)_
> It prints the block first, and after it, a warning for each kind of tool it left out.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s21

**Role:** practice · **Mode:** use · **Stage:** make-it-fail · **Introduces:** what vally simulate record printed  
**On screen:** Headline 'One pattern per shell call'. File panel labelled 'what vally simulate record printed', with a minimap: the simulation block with its two patterns and each call's recorded output, then the warnings. The panel takes the width, so there are no side notes. The first pattern lights; the panel scrolls to its output, then to the second pattern, then to the warnings for view and edit.  
**Renderer:** html (scenes/s21.html)

> Here's what it printed, from the top.
> The trials in that run made two shell calls between them, so the block has two patterns.  _(depends on what the demo produced)_
> Each pattern is a call's exact arguments, written out as text, and under it is what that call printed.
> The second pattern includes the trial's temporary folder, shortened here on screen; that's the kind of detail to look for before sharing a block.  _(depends on what the demo produced)_
> Everything else those trials did, such as view and edit, was left out with a warning.  _(2s to read after; depends on what the demo produced)_

## s22 — What the agents did

**Role:** body · **Mode:** think · **Stage:** what-it-did  
**On screen:** Headline 'Nobody invented a change'. Two cards side by side, one per model, each with the opening of its three final replies from our run, one line per trial. Terra's card lights, then haiku's. A note: six trials, no entry written.  
**Renderer:** html (scenes/s22.html)

> So what did the agents do on a bad day?
> Neither model wrote an entry in any of the six trials, and neither invented a change.  _(depends on what the demo produced)_
> Terra's replies were a sentence or two: each said the command had timed out, and two of the three began with the word Blocked.  _(depends on what the demo produced)_
> Haiku's replies were longer: each said the tracker wasn't answering, and each asked the user for the list of changes.  _(depends on what the demo produced)_
> In an app, there's nobody to answer.

## s23

**Role:** body · **Mode:** think · **Stage:** what-it-did  
**On screen:** Headline 'Already in place'. A quote card labelled 'an earlier run of this stimulus · claude-haiku-4.5 · the judge's reason' with the reason Vally printed for the one reply the judge failed. A note under it: our run, the judge passed 6 of 6; the earlier run, 2 of haiku's 3. The card lights.  
**Renderer:** html (scenes/s23.html)

> The judge passed all six of those replies.  _(depends on what the demo produced)_
> In an earlier run of this same stimulus, it failed one of haiku's three.
> Its reason: the reply mentioned the timeout, but then asserted that the Unreleased entries were already in place.
> An app that reads already in place ships a release with no entries.

## s24

**Role:** body · **Mode:** think · **Stage:** what-it-did  
**On screen:** Headline 'Haiku opened the script'. Dark box on the left with two calls from one of haiku's trials: the shell command that ran list-merged, and a view of tools/list-merged.mjs. Notes on the right: 'simulated: failed as planned' and 'not simulated: ran for real'. A note under it: claude-haiku-4.5 opened the file in 3 of 3 trials, gpt-5.6-terra in 0 of 3. The first lights, then the second.  
**Renderer:** html (scenes/s24.html)

> After the script failed, haiku went looking: in all three of its trials, it opened the script's file with the view tool.  _(depends on what the demo produced)_
> That isn't a shell command, so nothing simulated it, and it ran for real.
> What came back was the copy that asks the tracker: an address, and no list.  _(depends on what the demo produced)_
> Had the stand-in been staged there, that same call would have handed over the answer.

## s25

**Role:** body · **Mode:** think · **Stage:** what-it-did  
**On screen:** Headline 'Calls, not knowledge'. A two-row table, 'The workspace holds' and 'A view of the script returns': the stand-in → the list of merged changes, which is the answer; the copy that asks the tracker → an address and no list, with '0 of 6 trials wrote an entry · our run'. The first row lights, then the second.  
**Renderer:** html (scenes/s25.html)

> Simulation replaces calls, not knowledge.
> We could make the view tool fail for that file too, but an agent has other ways to read a file, such as a search tool.
> What held in our run was taking the answer out of the workspace: with the copy that asks the tracker, no trial wrote an entry.  _(2s to read after; depends on what the demo produced)_

## s26

**Role:** body · **Mode:** think · **Stage:** what-it-did  
**On screen:** Headline 'Retries, counted'. Two blocks side by side, from our run: '4 runs · the most in one trial, claude-haiku-4.5, with other calls in between' and '6 of 6 · trials that stops-retrying passed'. Under them: stops-retrying allows two retries in a row, at most. The first lights, then the second.  
**Renderer:** html (scenes/s26.html)

> Now the retries: one haiku trial ran the failing command four times in all, with other calls in between.  _(depends on what the demo produced)_
> No trial made more than two retries in a row, so stops retrying passed all six.  _(depends on what the demo produced)_

## s27

**Role:** recap · **Stage:** what-it-did  
**On screen:** Headline 'What does a command get back?'. One block, 'under a simulation', which opens after the question and a pause into three parts, each lit as it is said: 'It matches a pattern · it doesn't run; the agent gets our output', 'It matches nothing · it runs for real, unless there's a default', 'A file is not a call · take the answer out of the workspace'.  
**Renderer:** html (scenes/s27.html)

> Before you go on: under a simulation, what does a shell command get back when it matches a pattern, and when it doesn't?
> When it matches, it doesn't run, and the agent gets our output, as a success or as a failure.  _(pause 2.5s first)_
> When it matches nothing, it runs for real, unless the override has a default.
> But none of that hides a file, so the answer itself has to be out of the workspace.

## s28

**Role:** next · **Stage:** what-it-did  
**On screen:** 'Next: Grade a run Vally didn't start' in the display serif. Below, the hand-off question: 'The app also runs by itself. Can Vally grade that run?' A note: 'Exercises are on the lesson page · Source: Vally docs, Eval Spec reference, Simulation'.  
**Renderer:** slide (scenes/s28.html)

> You can now make a tool fail on purpose, grade what the agent does next, and record a simulation block from a saved run.
> All of this ran inside Vally, but the app also runs by itself, and keeps its own record of what it did.
> Can Vally grade a run it didn't start?
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
