# What the tick checked — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0002-what-the-tick-checked.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** What exactly did Vally run and check when it gave both models a tick?  
**The viewer starts:** A professional programmer who knows the shell and has seen one Vally run: one changelog request on two models with the first-draft changelog-entry skill, a tick for each, and two saved patches that differ (one ends with a made-up pull request number). Knows skill, agent, model, eval, eval file, workspace, patch, workspace.patch, and the vally eval command with -e, --model and --output-dir; knows that Vally runs the GitHub Copilot agent and that runs spend from a Copilot plan. Has used the eval file without reading it, and has seen only the patches in the results folder. Does not know Vally's words stimulus, grader or trial, or what a token is.

1. **read-the-eval-file**: after this, the viewer can say what each part of the eval file tells Vally to do, in Vally's words: agent environment, stimulus, grader
2. **read-the-results**: after this, the viewer can find a trial's row in the report, its grader's evidence in results.jsonl, and its three files in the results folder
3. **what-a-trial-used**: after this, the viewer can read a trial's token usage and turn its cost into cents
4. **why-both-passed**: after this, the viewer can say what a tick does and does not tell you, from the grader behind it
5. **find-it**: after this, the viewer can explain every line of the eval file, and find any run's request, changes, verdict and token count in the results folder

## s01 — What did the tick check?

**Role:** hook · **Mode:** think · **Stage:** read-the-eval-file  
**On screen:** Headline 'What the tick checked' in the display serif. Two cards side by side, labelled claude-haiku-4.5 and gpt-5.6-terra, each showing the changelog entry that model really wrote, with one green tick on each card. Each card lights as it is mentioned; then '(#42)' at the end of the second entry; then the two ticks.  
**Renderer:** html (scenes/s01.html)

> Two models got the same request, and wrote two different changelog entries.
> One entry cites a pull request that doesn't exist, and both got a green tick.
> Here, you'll find out what that tick checked, and where Vally wrote down what happened.

## s02 — Read the eval file

**Role:** body · **Mode:** works · **Stage:** read-the-eval-file · **Introduces:** one-request.eval.yaml, agent environment, agent_environment, defaults, timeout  
**On screen:** File panel on the real eval file, labelled one-request.eval.yaml, 23 lines, with a minimap; notes on the right, level with their lines. Highlights in turn: 'name' (line 1) with the note 'the folder name for its results'; 'timeout: 3m' (line 4) with 'how long the agent may take'; 'agent_environment' (line 6) with 'what the agent starts with'; the skill path (line 8); 'src' and 'dest' (lines 10-11) with 'a file to copy in, and its name in the workspace'.  
**Renderer:** html (scenes/s02.html)

> Let's start with the file that told Vally what to do: the eval file we ran on both models.
> It opens with the eval's name, which Vally uses as a folder name when it saves results.
> Under defaults are settings for the whole file, and this one gives the agent three minutes before Vally stops it.
> Next comes the agent environment: what the agent starts with.
> Everything listed here is copied into the workspace, the fresh scratch folder the agent works in, before the agent begins.
> There's one skill folder to install, given as a path relative to this file.
> And there's one file to copy in: the starting changelog, and the name it gets in the workspace.

## s03

**Role:** body · **Mode:** works · **Stage:** read-the-eval-file · **Introduces:** stimulus, stimuli, grader, graders, file-contains, prompt, typo-fix  
**On screen:** The same file panel, scrolled to lines 13-23, starting where the last scene left it. Highlights in turn, each with its note on the right: 'stimuli' (line 13) 'the things to try'; the entry 'typo-fix' (line 14) 'one stimulus: a request and its graders'; the prompt (lines 15-17) 'the request, word for word'; 'graders' (line 18) 'checks run after the agent stops'; 'type: file-contains' (line 19) 'a built-in grader'; 'path' and 'value' (lines 22-23) 'passes if this file contains this text'; 'name' (line 20) 'ours; the results show it'.  
**Renderer:** html (scenes/s03.html)

> Then comes a list called stimuli: the things to try.
> One entry in it is a stimulus: a request, together with the graders that check the result.
> This file has a single stimulus, named typo fix.
> Its prompt is the request, word for word as the agent receives it.
> Under the prompt are the graders.
> A grader is what we've been calling the check.
> Vally runs it after the agent has stopped, and it reports pass or fail, with a line of evidence saying what it found.
> The type picks one of Vally's built-in graders.
> This one is called file contains.
> It opens one file in the finished workspace, and passes if that file contains the text in value.
> So the whole check is: does the changelog contain the words notes add?
> The grader's name is ours, and it's what the results show.

## s04

**Role:** body · **Mode:** works · **Stage:** read-the-eval-file · **Introduces:** vally lint, -e  
**On screen:** Dark code box, left: the command 'vally lint -e evals/one-request.eval.yaml'. Right, level with it: 'reports mistakes in an eval file'. Under them: 'It starts no agent, so it spends nothing.' The command lights, then '-e evals/one-request.eval.yaml', then the line under.  
**Renderer:** html (scenes/s04.html)

> One more command belongs with the eval file: vally lint.
> It reports mistakes in an eval file, such as a misspelt key or a missing file, without starting an agent.
> Lint takes dash e and the file's path, the same as vally eval, and it spends nothing.

## s05 — What a run leaves behind

**Role:** body · **Mode:** works · **Stage:** read-the-results · **Introduces:** trial, run  
**On screen:** Three blocks in a row, no arrows: 'stimulus · typo-fix · one request and its graders', 'trial · typo-fix on claude-haiku-4.5', 'trial · typo-fix on gpt-5.6-terra'. The two trials fill together, then the stimulus, then the trials again; then the line under them, 'One run: one vally eval command, and everything it saves.'  
**Renderer:** html (scenes/s05.html)

> That's the file that went in; now let's see what a run leaves behind.
> First, one more of Vally's words: a trial is one attempt at one stimulus by one model.
> Our command had one stimulus and two models, so it made two trials.
> From here on, a run is one vally eval command and everything it saves, and a trial is one attempt inside it.

## s06

**Role:** body · **Mode:** works · **Stage:** read-the-results · **Introduces:** eval-results.md, results.jsonl, otel-spans.jsonl, events.jsonl, metadata.json, report, lesson-1, 2026-11-11T00-11-52-424Z, 0  
**On screen:** Dark code box, left: the run's folder as a tree, headed 2026-11-11T00-11-52-424Z/ (eval-results.md, results.jsonl, otel-spans.jsonl, one-request/typo-fix/claude-haiku-4.5/0/ with workspace.patch, events.jsonl, metadata.json, and the same under gpt-5.6-terra/0/). Right, level with each line: what it is. A highlight moves down the tree as each is named, one at a time.  
**Renderer:** html (scenes/s06.html)

> Each run writes one folder, named with the time it started, and this is everything in ours.
> At the top, eval results dot M D is the report: tables for people to read.
> Results dot jsonl holds the same results for programs, one record on each line.
> The third file is timing data for tracing tools, and this course doesn't use it.
> Below those are nested folders that lead to each trial: the eval's name, then the stimulus, then the model, then a trial number that starts at zero.
> Each trial folder holds three files.
> Workspace dot patch is the one you've seen: the lines the agent added and removed.
> Events dot jsonl is the agent's own log of the session, with every message and every tool it used.
> And metadata dot json holds a few facts about the trial: which model, when it started and ended, and whether it completed.

## s07

**Role:** body · **Mode:** works · **Stage:** read-the-results · **Introduces:** Pass Rate, Verdict, Tool Calls  
**On screen:** The report from our run as a table, labelled eval-results.md, one row under each model's heading: Stimulus, Graders, Pass Rate, Duration, Tokens, Tool Calls, Verdict (typo-fix | ✅ mentions-the-command 1/1 | 1/1 | 9.3s | 74,210 | 4 calls | ✅, and the gpt-5.6-terra row with 16.2s, 73,095, 7 calls). A line under it: '3 columns hidden: Environment, Skills, Turns'. The column headers light in turn: Graders, Pass Rate, Tool Calls, Verdict.  
**Renderer:** html (scenes/s07.html)

> Here's the report, with one table for each model.
> The graders column lists each grader by the name we gave it.
> Pass rate is the trials that passed out of the trials that ran: here, one of one.
> Tool calls is how many times the agent used a tool, such as opening or editing a file.
> And the verdict is the result: a trial passes only if every one of its graders passes.
> The tokens column, we'll come to shortly.

## s08

**Role:** body · **Mode:** works · **Stage:** read-the-results · **Introduces:** status, record, results.jsonl · one record, spread out  
**On screen:** File panel labelled 'results.jsonl · one record, spread out': the gpt-5.6-terra trial's record from our run, pretty-printed, with a minimap. Lines 1-8 in view, with a 'lines hidden' row for the identifiers and paths. Highlights in turn: '"type": "trial-result"' with the note 'the kind of record'; '"status": "success"' with 'the agent finished; not: the answer is right'.  
**Renderer:** html (scenes/s08.html)

> Results dot jsonl holds the detail behind each row of that table.
> Each record is one very long line, so here's one trial's record spread out.
> The type says what kind of record this is: one trial's result.
> Status says whether the agent finished: it's about the trial completing, not about the answer being right.

## s09

**Role:** body · **Mode:** works · **Stage:** read-the-results · **Introduces:** gradeResult, evidence, trajectory  
**On screen:** The same panel scrolls to the gradeResult block. Highlights in turn, with notes level on the right: '"passed": true' 'the trial's verdict'; '"details": [' 'one entry per grader'; '"evidence": "'notes add' found in CHANGELOG.md"' 'what the grader found, in its own words'; then it scrolls to '"trajectory": {' with a 'lines hidden' row for the agent's 40 events, and the note 'the full record of what the agent did'.  
**Renderer:** html (scenes/s09.html)

> Further down is grade result, the part that explains the tick.
> Passed is true: that's the trial's verdict.
> Details has one entry for each grader, and this trial had one.
> Here's that grader's evidence, in its own words: it found the words notes add in the changelog.
> The record ends with the trajectory, which is Vally's name for the full record of what the agent did in a trial.

## s10 — What a trial used

**Role:** body · **Mode:** works · **Stage:** what-a-trial-used · **Introduces:** token, tokens, token usage, tokenUsage, cache read tokens  
**On screen:** The same record, scrolled inside "trajectory" to "metrics" → "tokenUsage", with 'lines hidden' rows around it. Highlights in turn, with notes level on the right: 'inputTokens: 72505' 'everything the model read'; 'outputTokens: 590' 'everything it wrote'; 'callCount: 6' 'each call reads the conversation again'; 'cacheReadTokens: 67270' 'input the service had already processed'; 'totalTokens: 73095' 'input + output'.  
**Renderer:** html (scenes/s10.html)

> Inside the trajectory is a record of what the trial used.
> Models take in and write text in pieces called tokens, each a word or part of a word, and model services charge by the token.
> Every trial saves its token usage.
> Input tokens are everything the model was given: the request, the skill, the files the agent opened, and the conversation so far.
> Output tokens are everything it wrote, and there are far fewer of them.
> The call count explains why input is so much larger: the agent called the model six times, and each call takes in the conversation so far again.
> Cache read tokens are the part of the input the service had already processed earlier in the session, which costs less the second time.
> And total tokens is input plus output.

## s11

**Role:** body · **Mode:** works · **Stage:** what-a-trial-used · **Introduces:** cost, nano-aiu, AIU, AI Credit  
**On screen:** Dark code box, left: the record's "cost" block (provider: github-copilot, unit: nano-aiu, amount: 3361250000). Right, level with each line: 'as GitHub Copilot reported it', 'a billionth of an AIU', 'this trial'. Below, one line that builds left to right with equals signs, each part lighting as it is said: 3,361,250,000 nano-AIU = 3.36 AIU = 3.36 AI Credits ≈ 3 cents.  
**Renderer:** html (scenes/s11.html)

> The token usage ends with what the trial cost, as GitHub Copilot reported it.
> Its unit is the nano-AIU: a billionth of an AIU, which is the unit Copilot reports usage in.
> One AIU is one GitHub AI Credit, the unit Copilot bills in.
> And one AI Credit is one cent.
> So this trial's three point three six billion nano-AIU come to about three cents.
> Copilot counts usage against your plan's monthly allowance first, so a trial may cost you nothing extra until that's used up.

## s12

**Role:** body · **Mode:** works · **Stage:** what-a-trial-used · **Introduces:** Tokens, median  
**On screen:** The report table from before comes back, both models' rows. 73,095 lights in the Tokens column of the gpt-5.6-terra row, the total just seen in its record; then the Tokens header as the median is mentioned.  
**Renderer:** html (scenes/s12.html)

> That total is the number in the report's tokens column, on this trial's row.
> When a stimulus has several trials, the column shows their median, the middle value.
> We'll build on these numbers later, to work out what a passing trial costs.

## s13 — Why both models passed

**Role:** body · **Mode:** think · **Stage:** why-both-passed  
**On screen:** Top row, two cards: 'The grader, in the eval file' (the six grader lines) and 'Its evidence, in results.jsonl' ('notes add' found in CHANGELOG.md). Below, the entry each model wrote, labelled by model. '"notes add"' lights in the grader, then the evidence line, then `notes add` inside both entries, then '(#42)' at the end of the second.  
**Renderer:** html (scenes/s13.html)

> So why did both models pass?
> Let's put the two halves together.
> The eval file's only grader asks one question: does the changelog contain the words notes add?
> And the evidence line says what it found: those words, in the changelog.
> Both models wrote an entry that mentions notes add, so both passed.
> Nothing looked at the made-up pull request forty-two.

## s14

**Role:** body · **Mode:** think · **Stage:** why-both-passed  
**On screen:** Headline 'A pass means no objection.' Two blocks side by side: 'None of my graders objected. · what a pass tells you' fills green; 'This is correct. · what it doesn't tell you' fills red when the voice says what a pass doesn't mean. Under them: 'So far: one grader, written before anyone had read a run.'  
**Renderer:** html (scenes/s14.html)

> Here's the thing to hold on to about any eval result.
> Graders only raise an objection to what you told them to look for.
> A pass means none of your graders objected; it doesn't mean the result is correct.
> So a tick tells you only as much as the graders behind it.
> And so far there's one grader, written before anyone had looked at what the models do.

## s15

**Role:** body · **Mode:** think · **Stage:** why-both-passed  
**On screen:** A grid: rows 'claude-haiku-4.5' and 'gpt-5.6-terra'; columns 'this request, trial 0', 'the next trial', 'other requests'. The first cell of each row holds what that trial did ('no number', '(#42)'); the other cells hold '?'. The two known cells light, then 'the next trial' cells, then 'other requests'.  
**Renderer:** html (scenes/s15.html)

> It's tempting to add a grader for made-up pull request numbers straight away.
> But we've seen two trials.
> We don't yet know whether that model always does this, or what else goes wrong on other requests.
> So the graders can wait until we've looked at more runs.

## s16 — Find it in the files

**Role:** practice · **Mode:** use · **Stage:** find-it  
**On screen:** Headline 'From the tick to its evidence.' Two blocks side by side, no arrow: '✔ typo-fix · a tick for each model' and 'results/lesson-1 · the folder our run was saved in'. Each fills as it is mentioned. Under them: 'No agent starts. Nothing is spent.'  
**Renderer:** html (scenes/s16.html)

> That's the idea; now let's find it in our own results folder.
> If you tried it yourself, here's what you'd see.
> Nothing here starts an agent.

## s17

**Role:** practice · **Mode:** use · **Stage:** find-it · **Introduces:** ls, cd  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. vally lint -e evals/one-request.eval.yaml and its tick; ls results/lesson-1 showing one timestamped folder; cd results/lesson-1/2026-11-11T00-11-52-424Z; ls showing the four entries; cd one-request/typo-fix; ls claude-haiku-4.5/0 showing the three files.  
**Renderer:** terminal (tapes/s17.tape)

> First, we lint the eval file.  _(finishes before typed:1)_
> A tick: the file has no mistakes in it.  _(1s to read after; waits for output:1; depends on what the demo produced)_
> Next, let's find the folder our run was saved in.  _(finishes before typed:2)_
> There's one, named with the time the run started.  _(waits for output:2; finishes before typed:3)_
> We change into it, and list what the run left behind.  _(waits for output:3; finishes before typed:4)_
> The report, results dot jsonl, the timing data, and a folder named after the eval.  _(2s to read after; waits for output:4)_
> Now down to one trial.  _(finishes before typed:5)_
> We change into the eval's folder, then the stimulus, and list the first model's trial zero.  _(waits for output:5; finishes before typed:6)_
> Three files: the agent's events, the metadata, and the patch.  _(2s to read after; waits for output:6)_

## s18

**Role:** practice · **Mode:** use · **Stage:** find-it  
**On screen:** File panel on that trial's real metadata.json, labelled metadata.json, 17 lines, with a minimap; its paths are shown under ~/src/demo. It scrolls to lines 8-11; '"model": "claude-haiku-4.5"' lights with the note 'which model'; then '"status": "success"' with 'the agent finished'.  
**Renderer:** html (scenes/s18.html)

> Here's the metadata file from that folder.
> Model says which model the trial ran on.
> And status says success: the agent finished.
> The rest is identifiers, times, and paths.

## s19

**Role:** practice · **Mode:** use · **Stage:** find-it  
**On screen:** Left: the grader from the eval file in a dark box; 'CHANGELOG.md' then '"notes add"' light for the first answer. Right: two blocks, 'The entry, under the released 1.2.0 section' and 'Nothing changed at all'. Each fills yellow while its question is asked, then green (it passes) or red (it fails) with the answer. No answer is on screen before it is spoken.  
**Renderer:** html (scenes/s19.html)

> Now let's check that we can explain the tick.
> Which file did the grader open, and what did it look for?  _(2s to read after)_
> It opened the changelog in the finished workspace, and looked for the words notes add.
> What if a model had put its entry under the released one point two section instead: would this grader have passed it?  _(2s to read after)_
> Yes: the entry would still contain those words, and the grader looks at nothing else.
> And what if a model had changed nothing at all?  _(2s to read after)_
> Then the trial fails: the starting changelog doesn't contain notes add, so the grader reports that the text wasn't found.

## s20

**Role:** practice · **Mode:** use · **Stage:** find-it  
**On screen:** The report table once more, both models' rows, nothing lit while the question is asked. After the beat the Tokens column lights: 74,210 for claude-haiku-4.5, 73,095 for gpt-5.6-terra.  
**Renderer:** html (scenes/s20.html)

> One last question: which model used more tokens in our run?  _(2s to read after)_
> The report's tokens column has the answer: haiku, by about a thousand tokens.
> Your own run will differ.

## s21

**Role:** recap · **Stage:** find-it  
**On screen:** A block labelled 'any trial'; after the question and a pause it opens to show four parts: 1 Its request (the prompt of a stimulus, in the eval file), 2 Its changes (workspace.patch), 3 Its verdict (the report; evidence in results.jsonl), 4 Its tokens (the report's Tokens column; detail in results.jsonl). Each lights as it is said.  
**Renderer:** html (scenes/s21.html)

> Before you go on: for any trial, where would you find its request, its changes, its verdict, and its token count?
> Its request is the prompt of a stimulus, in the eval file.  _(pause 2.5s first)_
> Its changes are in its workspace dot patch.
> Its verdict is in the report, and the grader's evidence behind it is in results dot jsonl.
> And the token count is in the report's tokens column, with the detail in results dot jsonl.

## s22

**Role:** next · **Stage:** find-it  
**On screen:** 'Next: The same request, five times' in the display serif. Below, the hand-off question: 'Each model ran once. Would it do the same thing next time?' A note: 'Exercises are on the lesson page · Source: Vally docs, Eval Spec reference; Trajectory Format'.  
**Renderer:** slide (scenes/s22.html)

> You can now trace a tick back to its evidence.
> But each model ran once.
> Would it do the same thing next time?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
