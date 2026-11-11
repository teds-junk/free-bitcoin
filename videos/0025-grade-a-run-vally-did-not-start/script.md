# Grade a run Vally did not start — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0025-grade-a-run-vally-did-not-start.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (not for the viewer).

- Sources: the lesson page; verified/lesson-25 (console output only); NOTES.md lines 53, 137, 165, 166, 169.
- Every figure quoted is from our own recordings on 2026-11-11 (src/run/HANDOVER.md). src/run/ holds the
  cleaned copies written by build-src/extract-run.py; make-scenes.py asserts what the narration states and
  refuses a src/run file holding a /Users/ or /var/folders path, an email address or the account attribute.
- Our run matched the page's verdict (3 of 5; the hidden test and the skill check failed), so no "earlier
  run" is cited. It differs in size: 143 trace lines, five tool calls, five steps. The comparison uses the
  lesson 23 video's own run (haiku: hidden test 1 of 3, skill 1 of 3), not the page's 0 of 3.
- Left to the page: the token and cost comparison in step 7, the terra exercise, the quiz, cached_tokens.
- An independent cold read was run by the coordinator; its eight findings are applied.
- Not done: the full render, timing fit (sync-report.js), assembly, verify, transcript.
<!-- /notes -->

## The story

**The question this video answers:** The app ran the agent itself, from a few shell commands, and recorded what it did as traces. Can Vally grade that run?  
**The viewer starts:** Has built an eval file for the release tool's request: the since-last-release stimulus, whose setup commands write release/merged.txt in the workspace, graded by a hidden test (a run-command grader staged by the grading environment), two tool-calls graders, a max-repeat loop check and a skill-invocation grader; and a tracker-down stimulus where a simulation makes the tool fail. Has run that since-last-release stimulus inside Vally, three trials on each model, and kept the run. Knows trajectories, tool calls, budget graders such as wall-time, cost in AIU, the executor, and that vally grade re-grades a saved run from its results file without starting an agent. Knows the practice folder, the changelog-entry skill and its rule to leave out changes users can't see. A professional programmer: JSON, shell, diff and Node need no explanation. Has never seen a trace, a span, or a trajectory that Vally did not write.

1. **after-or-inside**: after this, the viewer can say what grading an app's real run afterwards shows, and what only trials inside Vally can
2. **trajectory-from-outside**: after this, the viewer can name the three inputs vally grade needs for a run it did not start, and which graders read each
3. **traces-to-steps**: after this, the viewer can follow a model call and a tool call from a trace's spans into a step of an ATIF file
4. **run-convert-grade**: after this, the viewer can run the release app's script, convert its trace file to a trajectory, and grade the result with the eval file they already have
5. **what-carried-over**: after this, the viewer can grade a real run of the app with the eval file they already have, and say which graders carried over, which fields did not, and why one run cannot be compared with trials

## s01 — A run nobody started in Vally

**Role:** hook · **Mode:** think · **Stage:** after-or-inside  
**On screen:** Headline 'A run Vally didn't start' in the display serif. Two cards side by side, no arrow. Left, 'Inside Vally': four short lines, 'prepares the workspace', 'starts the agent', 'records the trajectory', 'grades it'. Right, 'The release tool': 'a script prepares a checkout', 'the release app starts the agent', and under a rule 'what's left: the changed checkout · the app's own record'. The left card lights during the first sentence, the right card from the third, its last line on 'what's left'.  
**Renderer:** html (scenes/s01.html)

> So far, Vally has done everything itself, from preparing the workspace to grading the result.
> The team's release tool doesn't work that way.
> After a merge, a script prepares a checkout, and a small program, the release app, starts an agent session itself.
> Nobody runs Vally, so what's left afterwards is the changed checkout, and the app's own record of the session.
> Here, you'll run that app, turn its record into a file Vally can read, and grade the run with the eval file we already have.

## s02

**Role:** body · **Mode:** think · **Stage:** after-or-inside  
**On screen:** Eyebrow 'Inside Vally or after the fact'. Headline 'Two ways to grade an app'. Two blocks side by side, no arrow: 'After the fact · the real app, its real inputs and model · each run happens once' and 'Inside Vally · repeat a stimulus, change the model · a reproduction of the app'. The first fills from the second sentence.  
**Renderer:** html (scenes/s02.html)

> Let's start with a choice: there are two ways to put an app's agent under our graders, and they answer different questions.
> The first is after the fact: the app runs as it always does, and we grade what it recorded.
> That shows the real thing: the app's own settings, its real inputs, and its real model.
> But each run happens once, so we can't ask for five more trials, or for another model.

## s02b

**Role:** body · **Mode:** think · **Stage:** after-or-inside  
**On screen:** The same headline and the same two blocks. The second, 'Inside Vally', fills; the first fills again on 'grading a real run'.  
**Renderer:** html (scenes/s02b.html)

> The other way is inside Vally, which can repeat a stimulus, change the model, and run experiments.
> What it runs, though, is a reproduction of the app, and a reproduction can differ in ways that matter.
> Most teams want both, and here we take the first: grading a real run.

## s03 — Read a trajectory from outside

**Role:** body · **Mode:** works · **Stage:** trajectory-from-outside · **Introduces:** ATIF  
**On screen:** Eyebrow 'A trajectory from outside'. Headline 'A second format: ATIF'. One block, 'ATIF · Agent Trajectory Interchange Format · a JSON file: one agent session as a list of steps'. Inside it, one step drawn as four parts in a row: 'message · what the model said', 'tool_calls · the calls it made', 'observation · what each returned', 'metrics · tokens'. The block lights on the name; each part as it is said.  
**Renderer:** html (scenes/s03.html)

> That's the choice; now, how can Vally grade a run it never saw?
> Vally grade has always read trajectories, and until now they came from Vally's own results file.
> It also reads a second, public format, which any program can write.
> It's called ATIF, the Agent Trajectory Interchange Format: a JSON file that describes one agent session as a list of steps.
> Each step holds what the model said, the tool calls it made, what each call returned, and metrics such as tokens.
> Vally converts a file like that into its own trajectory before grading.

## s04

**Role:** body · **Mode:** works · **Stage:** trajectory-from-outside · **Introduces:** trajectory.json  
**On screen:** Headline 'One step per model answer'. File panel labelled 'app-run/trajectory.json' with a minimap, long values cut short, notes on the right level with their lines. It opens on the top of the file: 'schema_version' lit ('how Vally recognises the file'). It scrolls to step 1: 'step_id' ('one step per answer'), then the tool call's 'function_name' and 'arguments' ('what a tool-calls grader reads'), then scrolls on to 'observation' ('what the call returned') and 'metrics' ('tokens and cost').  
**Renderer:** html (scenes/s04.html)

> Here's the start of the file from the run we're about to make.
> The first line is how Vally recognises it: a version that doesn't begin with ATIF is rejected.
> Then come the steps, one for each time the model answered.
> Each tool call is listed with its name and its arguments, which is what a tool calls grader reads.
> Under observation is what each call returned, matched to its call by an ID.
> Last come the step's metrics, such as its tokens.

## s05

**Role:** body · **Mode:** works · **Stage:** trajectory-from-outside · **Introduces:** vally grade, --stimulus, --workspace, --diff-file, --verbose, -e, release.eval.yaml, repo, app-run/repo  
**On screen:** Headline 'What each grader needs'. Dark box, left: the vally grade command over five lines as the lesson prints it (-e evals/release.eval.yaml, --stimulus since-last-release, --workspace app-run/repo, --diff-file app-run/change.diff, --verbose < app-run/trajectory.json). Notes on the right, level with their lines: 'whose graders apply' beside --stimulus; 'the changed files: run-command, program, file graders' beside --workspace; 'the change: diff graders' beside --diff-file; 'the trajectory: tool-calls, skill-invocation, budgets' beside the redirect. Nothing is lit while the app-run folder is described.  
**Renderer:** slide (scenes/s05.html)

> For a run Vally didn't start, vally grade needs three things besides the eval file, one for each kind of grader.
> In this command, all three come from one folder, app run, which the app's script will leave behind: the checkout the agent worked in, a diff of what it changed, and its record of the session as a trajectory.

## s05b

**Role:** body · **Mode:** works · **Stage:** trajectory-from-outside  
**On screen:** The same headline, command and notes. Each part lights as it is named: the redirect, --diff-file, --workspace, and last --stimulus.  
**Renderer:** html (scenes/s05b.html)

> First, the trajectory: graders of the path, such as tool calls, skill invocation and the budgets, need it, so the ATIF file arrives on standard input.
> Second, the change: diff graders take it from the file that dash dash diff file names.
> Third, the changed files: a grader that runs a command, or opens a file, works in the folder that dash dash workspace names.
> Then there's one more flag, dash dash stimulus, which says whose graders apply, because an ATIF file doesn't say which stimulus it answers.
> Our hidden test still works, because its files are staged for the graders as usual.

## s06

**Role:** body · **Mode:** works · **Stage:** trajectory-from-outside  
**On screen:** Headline 'Three things the file lacks'. Three blocks in a row, no arrows: 'cost · empty · explained with the converter', 'wall time · 0 · no start or end time in the file', 'skill loaded · only if the agent called its skill tool'. Each fills as it is named.  
**Renderer:** html (scenes/s06.html)

> Graders see only what's in the file, and three gaps matter here.
> Vally's own cost field stays empty for a file like this, for a reason we'll come to with the converter.
> Next, the trial's wall time is recorded as zero, because the file has no start and end time for the session.
> Finally, a skill counts as loaded only if the trajectory shows the agent calling its skill tool.

## s07 — From traces to steps

**Role:** body · **Mode:** works · **Stage:** traces-to-steps · **Introduces:** OpenTelemetry, span  
**On screen:** Eyebrow 'From OpenTelemetry traces'. Headline 'The app writes traces'. One trace drawn as bars on a time line: a full-width bar 'invoke_agent · the root: no parent', and inside it, indented and in time order, shorter bars 'chat', 'execute_tool', 'chat', 'execute_tool', 'chat'. Label above: 'one trace · every span carries its ID'. The whole drawing lights on 'traces', one child bar on 'a span', the root bar on 'the root'.  
**Renderer:** html (scenes/s07.html)

> The release app doesn't write ATIF.
> Like most programs built on an agent library, it writes traces.
> Traces come from OpenTelemetry, an open standard for recording what a program does as it runs, so that any tool can read the record.
> One unit of work in a trace is a span: one call to a model, say, or one tool call, with a start time, an end time, and named values called attributes.
> Every span carries the ID of its trace, and a span started inside another names that one as its parent.
> So a span with no parent is the root of its trace.

## s08

**Role:** body · **Mode:** works · **Stage:** traces-to-steps · **Introduces:** GenAI semantic conventions  
**On screen:** Headline 'Shared names for AI work'. Dark box, left, four names one per line: 'chat', 'execute_tool', 'invoke_agent', 'gen_ai.usage.input_tokens'. Notes on the right, level with each: 'a model call', 'a tool call', 'a whole agent session', 'an attribute: input tokens'. A note below: 'OpenTelemetry, semantic conventions for generative AI · status: Development'. Each name lights as it is said.  
**Renderer:** html (scenes/s08.html)

> What goes into those spans is agreed too, in OpenTelemetry's semantic conventions for generative AI.
> A model call is a span named chat.
> A tool call is a span named execute tool, and a whole agent session is one named invoke agent.
> Attributes have agreed names as well, such as the one for input tokens.
> Because the names are shared, a converter written for one library's traces mostly works for another's.
> These conventions are still marked as in development, so the names can change.

## s09

**Role:** body · **Mode:** works · **Stage:** traces-to-steps · **Introduces:** app/run.mjs, run.mjs  
**On screen:** Headline 'Tracing is one setting'. File panel labelled 'app/run.mjs', the whole file (18 lines), with notes on the right level with their lines: 'the app: one request, the stimulus's own words' beside the import; 'write spans to a file, one line of JSON each' beside the telemetry block; 'include messages, tool arguments and results' beside captureContent. The import lights, then the telemetry block, then captureContent.  
**Renderer:** html (scenes/s09.html)

> The release app is built on the GitHub Copilot SDK, the same library Vally's own executor uses to run an agent.
> Here is the app's entry point, all of it.
> The app itself sends one request, in the same words as the stimulus in our eval file.
> It's called with a telemetry setting, which tells the SDK to write every span to a file, one line of JSON each.
> Inside that setting, the line capture content adds the message text, the tool arguments and the tool results to the spans.
> Without that, the spans would hold names and counts only, and no grader could check what a tool call did.

## s10

**Role:** body · **Mode:** works · **Stage:** traces-to-steps · **Introduces:** traces.jsonl, traces.jsonl · one line, laid out, traces.jsonl · another line, laid out  
**On screen:** Headline 'A model call, as a span'. File panel labelled 'traces.jsonl · one line, laid out' with a minimap and 'lines hidden' rows for the attributes and fields not shown. Notes on the right: 'shared by every span of the session' beside traceId; 'the session's invoke_agent span' beside parentSpanId; 'the kind of work' beside gen_ai.operation.name; 'tokens' beside the two usage attributes; 'the price, in nano-AIU' beside github.copilot.nano_aiu. The operation name lights first, then the trace ID and parent, then the tokens, then the price.  
**Renderer:** html (scenes/s10.html)

> Here's one line of the trace file from our run, laid out with one attribute per line.
> It's a model call: its operation name is chat.
> Its trace ID is shared by every span from this session, and the parent is the session's invoke agent span.
> Its tokens are here, under the conventions' names.
> Then comes its price, in nano AIU, under a name of GitHub's own.

## s11

**Role:** body · **Mode:** works · **Stage:** traces-to-steps  
**On screen:** Headline 'A tool call, as a span'. The same kind of panel on another line of the trace file: an execute_tool span. Notes on the right: 'a tool call, and which tool' beside the operation and tool name; 'the ID the model gave the call' beside gen_ai.tool.call.id; 'recorded because of captureContent' beside the arguments (a path ending release/merged.txt, shown under ~/src/demo) and the result.  
**Renderer:** html (scenes/s11.html)

> This one is a tool call: the one that read the merged list.  _(depends on what the demo produced)_
> Its operation name is execute tool, and the tool's name follows.
> The call ID is the one the model gave the call, and the ATIF file uses it to pair a call with its result.
> The arguments and the result are recorded because of capture content.

## s12

**Role:** body · **Mode:** works · **Stage:** traces-to-steps · **Introduces:** app/traces-to-atif.mjs, traces-to-atif.mjs, node  
**On screen:** Headline 'Spans in, steps out'. File panel labelled 'app/traces-to-atif.mjs' with a minimap, opened on its loop (lines 32 to 66), the lines above and below shown as hidden. Notes on the right: 'a model call starts a new step' beside the chat test; 'token attributes, renamed' beside metrics; 'a tool call joins the step before it' beside the execute_tool test. It scrolls from the chat branch to the execute_tool branch as the voice reaches it, then up to the argumentsOf helper (lines 20 to 27) for the last sentence.  
**Renderer:** html (scenes/s12.html)

> Vally can write traces of its own, but it has no way to read one in.
> So to grade the app's run, something has to turn its spans into ATIF steps.
> Our practice folder has a converter for that, about seventy lines of JavaScript.
> It sorts the spans by start time, and walks through them.
> Each model call, a chat span, becomes a new step, with its token attributes renamed to ATIF's names.
> A tool call is added to the step just before it, because that's where the model asked for it.
> Every other span, such as the session's setup and its timings, is skipped.
> One tool records its arguments as plain text, not JSON, and the converter keeps that text unchanged.

## s12b

**Role:** body · **Mode:** works · **Stage:** traces-to-steps  
**On screen:** Headline 'What happens to cost'. Dark box, left, labelled 'app/traces-to-atif.mjs · lines 49 and 50': the converter's comment 'A billion nano-AIU is one AI Credit: $0.01.' and its line 'cost_usd: (a["github.copilot.nano_aiu"] ?? 0) / 1e11,'. One note on the right, level with that line: 'the trace's nano-AIU, kept as dollars'. Below, one block: 'Vally's cost · empty · it only counts AIU its own Copilot runs report'. The attribute lights, then cost_usd, then the block.  
**Renderer:** html (scenes/s12b.html)

> Cost takes one more step, so here is that story from start to finish.
> The trace carries each model call's price in nano AIU, as we saw.
> The converter keeps it, turned into dollars, in each step's metrics.
> Vally's own cost field still comes out empty, because Vally only counts cost reported in AIU by its own Copilot runs.
> So for a run like this, the cost is in the file, and adding it up is left to us.

## s13

**Role:** body · **Mode:** works · **Stage:** traces-to-steps  
**On screen:** Headline 'Traces hold private values'. Four blocks in a row, no arrows, under the label 'a trace written with content captured holds': 'the whole prompt', 'every file the agent read', 'full paths on your machine', 'an ID for your account'. Each fills as it is named. A note below: 'the traces in this video were cleaned first'.  
**Renderer:** html (scenes/s13.html)

> One caution about trace files.
> With content captured, a trace holds the whole prompt, every file the agent opened, full paths on your machine, and an attribute that identifies your account.
> So a raw trace doesn't belong in an issue or in a commit, and the ones shown here were cleaned first.

## s14 — The script the release tooling runs

**Role:** body · **Mode:** works · **Stage:** traces-to-steps · **Introduces:** app/run.sh, run.sh, sh  
**On screen:** Eyebrow 'The script the release tooling runs'. Headline 'The script does Vally's setup'. File panel labelled 'app/run.sh' with a minimap, from the checkout step (line 15) to the end, the lines above shown as hidden. Notes on the right: 'the checkout: the files the eval file stages' beside the cp lines; 'the same setup command' beside the list-merged line; 'the starting state, kept' beside the cp -R to before; 'the app, on the model we give it' beside node app/run.mjs; 'the change, as a plain diff' beside the diff line. It scrolls down once, between the copy of the starting state and the app.  
**Renderer:** html (scenes/s14.html)

> The last piece is the script the release tooling runs.
> This script does by hand what our eval file's agent environment and its setup commands do inside Vally.
> First it builds the checkout: the same changelog, the same tool, and the skill in a folder beside it.
> Then it runs the same setup command, which writes the merged list.
> It keeps a copy of that starting state, so the merged list counts as part of the start, and not as part of the change.
> Next it runs the app, on the model we give it, tracing to a file.
> Finally it compares the two folders, and saves the difference as a plain diff, with no git involved.

## s15 — Run the app, convert, grade

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Eyebrow 'Run the app, convert, grade'. Headline 'Which graders will still work?'. A table of the stimulus's five graders, from the eval file: name and type. every-change-handled · run-command (the hidden test); reads-the-list · tool-calls; never-commits · tool-calls; no-loop · max-repeat; loads-the-skill · skill-invocation. A note: 'evals/release.eval.yaml · since-last-release'. The rows light together when the five are named; nothing is marked pass or fail. The question is held for a beat.  
**Renderer:** html (scenes/s15.html)

> That's every piece; now let's run the app once, convert its traces, and grade the result.
> Our stimulus has five graders: a hidden test, two checks on its tool calls, a loop check, and a check that the skill loaded.
> Which of them would you expect to work on a run that Vally never saw?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s16

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade · **Introduces:** npm install, --prefix  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. npm install --prefix app; npm's summary: packages added, and no vulnerabilities found. Held until it has been read.  
**Renderer:** terminal (tapes/s16.tape)

> First, the app needs two libraries: the Copilot SDK, which runs its agent, and Vally's own package, for a part of the app we haven't used yet.  _(finishes before typed:1)_
> We install them with npm; dash dash prefix names the app's folder, and no agent starts.  _(finishes before typed:1)_
> That adds about a hundred and forty packages, inside the app folder.  _(3s to read after; waits for output:1; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Terminal, continuing in the practice folder. sh app/run.sh claude-haiku-4.5; a jump cut; then the agent's reply, a few lines, and the script's last line: 'Wrote app-run/traces.jsonl and app-run/change.diff'. Held until it has been read.  
**Renderer:** terminal (tapes/s17.tape)

> Now the app itself: the script, followed by the model's name.  _(finishes before typed:1)_
> This spends one agent run.  _(finishes before enter:1)_
> It prints the agent's reply, and then says where it wrote the traces and the diff.  _(finishes before enter:1)_
> Moments later, the reply says three changes were added, and both files are written.  _(5s to read after; waits for output:1; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade · **Introduces:** change.diff  
**On screen:** Headline 'What the app changed'. File panel labelled 'app-run/change.diff', the whole file, with notes on the right level with their lines: 'the new option' beside the Added entry, 'the search fix' beside the Fixed entry, 'the refactor: the skill says leave it out' beside the entry under Changed. The added lines light together, then the first two entries, then the refactor's.  
**Renderer:** html (scenes/s18.html)

> Here's the diff that the script saved.
> Only the changelog changed, with a line for each entry the agent added.  _(depends on what the demo produced)_
> There's an entry for the new option under Added, and one for the search fix under Fixed.  _(depends on what the demo produced)_
> There's also an entry for the refactor, under a new Changed heading, and that's the one our skill says to leave out.  _(2s to read after; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Headline built from the run: 'Five tool calls, no skill call'. Left, a dark box labelled 'app-run/traces.jsonl · the lines whose name begins execute_tool', one line per tool call from our trace (four 'execute_tool view' and one 'execute_tool edit', in the order they ran). Notes on the right: 'the read of release/merged.txt' level with that call; 'no execute_tool skill' below the last. Above the box, a count: '143 lines · 109 of them session timings'. The count lights, then the box, then the merged-list call, then the 'no skill' note.  
**Renderer:** html (scenes/s19.html)

> The trace file is longer: a hundred and forty-three lines, and the ones we care about are the spans for tool calls.  _(depends on what the demo produced)_
> Most lines are timings; searching for execute tool finds the agent's tool calls, and there are five.  _(depends on what the demo produced)_
> One of them is the read of the merged list.  _(depends on what the demo produced)_
> None is a call to the skill tool, so in this run, the agent never loaded the skill.  _(2s to read after; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Terminal in the practice folder. node app/traces-to-atif.mjs app-run/traces.jsonl, with its output sent to app-run/trajectory.json, over two lines as the lesson prints it. The command prints nothing and the prompt returns.  
**Renderer:** terminal (tapes/s20.tape)

> Next, we convert: the converter reads the trace file, and we send what it prints into a new file.  _(finishes before typed:1)_
> Nothing is printed, because the trajectory went into that file.  _(1s to read after; waits for done:1)_

## s21

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Headline built from the run: 'Five steps, four with tool calls'. A table read from app-run/trajectory.json, one row per step: step, the tool calls it made (view, view; view; edit; view; none, 'the reply only'). A note: 'app-run/trajectory.json · our run'. The rows with tool calls light together, then the last row.  
**Renderer:** html (scenes/s21.html)

> Here's the trajectory it wrote, one row per step.
> The five tool calls now sit in four steps, each under the model answer that asked for them, and a last step holds only the reply.  _(2s to read after; depends on what the demo produced)_

## s22

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Terminal in the practice folder, in a slightly smaller type so each grader's line fits. The vally grade command over five lines as the lesson prints it; then one line per grader with a tick or a cross and its evidence, and the last line with the score. Held until it has been read.  
**Renderer:** terminal (tapes/s22.tape)

> Now the grade: our eval file, the stimulus's name, the app's checkout as the workspace, the saved diff, and the trajectory on standard input.  _(finishes before typed:1)_
> Dash dash verbose prints a line for each grader.  _(finishes before enter:1)_
> No agent starts, so this costs nothing.  _(finishes before enter:1)_
> Three of the five graders passed: the list was read, nothing was committed, and nothing looped.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> The hidden test failed, on the refactor's entry, and so did the check that the skill loaded.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s23

**Role:** practice · **Mode:** use · **Stage:** run-convert-grade  
**On screen:** Headline built from the run: 'The same two failures'. A table for claude-haiku-4.5 and the since-last-release stimulus, two columns: 'The app's run · 1' and 'Vally's own trials · 3'. Rows, one per grader: every-change-handled failed / 1 of 3; loads-the-skill failed / 1 of 3; reads-the-list, never-commits, no-loop passed / 3 of 3. The right column lights, then the two failing rows; the question is held for a beat.  
**Renderer:** html (scenes/s23.html)

> Earlier, Vally ran this same stimulus itself: three trials, on the same model.
> The sizes matter here: it's one run of the app, against three trials.
> In those trials, the hidden test passed once, and the skill loaded once.  _(depends on what the demo produced)_
> So the app's run failed the same two graders that most of Vally's trials failed.  _(depends on what the demo produced)_
> Does that show the app is no worse than Vally's own runs?  _(2s to read after)_
> Not yet: it shows that the graders work on the app's run, and give the same kind of verdict.
> With one run, that's as far as the comparison goes.

## s24 — What carried over

**Role:** body · **Mode:** think · **Stage:** what-carried-over  
**On screen:** Eyebrow 'What carried over'. Headline 'Every grader worked'. A table, one row per grader, with what it read on this run: every-change-handled · 'a copy of the app's checkout'; reads-the-list, never-commits · 'the tool calls in the trajectory'; no-loop · 'the same record'; loads-the-skill · 'no skill call in the trajectory'. Each row lights as it is named.  
**Renderer:** html (scenes/s24.html)

> So what carried over to a run that Vally never saw?
> Every grader we wrote inside Vally worked.  _(depends on what the demo produced)_
> The hidden test ran in a copy of the app's checkout, and caught the refactor's entry.  _(depends on what the demo produced)_
> Both tool calls graders found the read of the merged list, and no commit, because the trace recorded every tool call with its arguments.  _(depends on what the demo produced)_
> The loop check counted repeats from the same record, and the skill check saw that no skill call was made.  _(depends on what the demo produced)_
> Those graders ask whether the run did the job the way the app needs, and that has the same answer however the run was started.

## s25

**Role:** body · **Mode:** think · **Stage:** what-carried-over  
**On screen:** Headline 'What didn't carry over'. The three blocks from earlier, with what each means for a grader: 'cost · empty · add up the dollars yourself', 'wall time · 0 · a wall-time grader passes anything', 'skill loaded · only as a tool call'. A fourth block: 'tracker-down · nothing to grade · the tool fails only inside Vally'. Each fills as it is named.  
**Renderer:** html (scenes/s25.html)

> Some things did not carry over, and each one goes back to what the file holds.
> Cost came out empty, as we saw, so comparing cost means adding up each step's dollars ourselves.
> Wall time was zero, so a wall time grader would pass anything.
> And the skill check worked only because loading a skill shows up in the trace as a tool call like any other.
> So before trusting a grader on converted runs, it's worth asking whether the field it reads came across.
> One stimulus has no counterpart here at all: the one where the tracker is down, because that failure exists only when Vally simulates it.

## s26

**Role:** body · **Mode:** think · **Stage:** what-carried-over  
**On screen:** Headline 'One run is one sample'. Two blocks side by side, no arrow: '1 run · the app, graded afterwards · once, on the model the app used' and '3 trials · Vally's own · repeatable'. The second fills on 'takes trials', the first on 'happens once'.  
**Renderer:** html (scenes/s26.html)

> That leaves a question these graders can't answer: is the app as good as Vally's own runs, worse, or better?
> Answering it takes trials, and a real run happens once, on whatever model the app used.
> That's the limit of grading afterwards.

## s27

**Role:** recap · **Stage:** what-carried-over  
**On screen:** Eyebrow 'Recap'. Headline 'What does vally grade need?'. One block, 'a run Vally didn't start', which opens after the question and a pause into three parts, each lit as it is said: 'the trajectory · an ATIF file on standard input', 'the change · --diff-file', 'the changed files · --workspace'.  
**Renderer:** html (scenes/s27.html)

> Before you go on: for a run Vally didn't start, what does vally grade need, besides the eval file?
> It needs the trajectory, as an ATIF file on standard input.  _(pause 2.5s first)_
> It needs the change, as a diff file.
> Last, it needs the changed files, in the workspace folder.

## s28

**Role:** next · **Stage:** what-carried-over  
**On screen:** 'Next: Let Vally run the app' in the display serif. Below, the hand-off: 'To get trials, experiments and models, Vally has to start the app itself.' A note: 'Exercises are on the lesson page · Source: Vally docs, CLI: grade; Trajectory Format'.  
**Renderer:** slide (scenes/s28.html)

> You can now run the release app's script, convert its trace file to a trajectory, and grade the result with the eval file you already have.
> But grading afterwards gives one sample per run, on whatever model the app used.
> To get trials, experiments and other models, Vally has to start the app itself.
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
