# A model from your own provider — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0017-a-model-from-your-own-provider.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** My app calls a model through its own provider, not my Copilot account. Can Vally run that same model?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through sixteen lessons of Vally evals on claude-haiku and gpt-5.6-terra, all through a Copilot account. Knows skill, eval file, stimulus, grader, trial, run, the results folder and results.jsonl; vally lint; ERROR versus FAIL; --workers and why we use two; whether a skill loads, and failure modes; an experiment file with variants, a baseline, overrides and a vary list; vally experiment run with --dry-run, and experiment drift; a range around a count; reasoning effort as a variant; a trial's token usage, the share read from cache, and its cost in AIU, where one AIU is one cent; the course's cost calculator; and cost per passing trial, compared for four variants named haiku-low, haiku-high, terra-low and terra-high in cost.experiment.yaml. Has never run a model outside the Copilot account, and does not know the words executor or provider block, bring your own key, Ollama, or the --variant flag.

1. **ship-what-you-evaluate**: after this, the viewer can say why a result for a model served somewhere else says little about the one your app calls
2. **bring-your-own-key**: after this, the viewer can read a provider block, say where the key is kept, and predict what a trial through it records
3. **local-variant**: after this, the viewer can predict what the qwen-local variant changes in the experiment, and why it runs with one worker
4. **run-it**: after this, the viewer can run one variant through your own provider, read its tokens, and price a passing trial at your own rates
5. **what-changed**: after this, the viewer can say what carried over to the new provider and what did not, with the counts and the cost to show it

## s01 — Evaluate the model you ship

**Role:** hook · **Mode:** think · **Stage:** ship-what-you-evaluate  
**On screen:** Headline 'A model from your own provider' in the display serif. Two blocks side by side, no arrow: 'Your Copilot account · every trial so far' and 'A provider of your own · one you pay directly, or run yourself'. The first lights, then the second.  
**Renderer:** html (scenes/s01.html)

> Every trial so far has gone through our Copilot account: Vally asked for a model by name, and the account served it.
> An app may not work that way.
> Teams often call a model through a provider they pay directly, or one they run themselves, for reasons of price, data rules, or speed.
> Here, you'll point one variant of an experiment at a model running on our own computer, and work out what its trials would cost.

## s02

**Role:** body · **Mode:** think · **Stage:** ship-what-you-evaluate  
**On screen:** Headline 'Same name, different behavior'. Three blocks in a row, each lit as it is named: 'How it is stored · often compressed to fit smaller machines', 'How tool calls become text · what the model actually reads', 'Its default settings · chosen by whoever serves it'. Note: 'the copy we use here is a 4-bit compressed version'.  
**Renderer:** html (scenes/s02.html)

> Let's start with why that matters.
> We've seen two models take the same skill two ways.
> Less obviously, one model served two ways can behave differently too.
> Whoever serves a model decides how it's stored, and that's often compressed to fit smaller machines.
> They decide how the conversation, and the agent's tool calls, are turned into the text the model sees.
> They also choose its default settings.
> Each of those can change what the agent does, so a result for the same model from somewhere else says little about yours, even when the name matches.

## s03

**Role:** body · **Mode:** think · **Stage:** ship-what-you-evaluate  
**On screen:** Headline 'Only the endpoint can tell'. A card labelled 'another local model on our computer · gpt-oss:20b' over a dark box with the server's answer: '400 invalid tool call arguments', and a callout 'every trial, before any file changed'. Below, three blocks: 'the endpoint the app calls', 'the model name the app sends', 'the same stimuli, graders and skill'.  
**Renderer:** html (scenes/s03.html)

> Here's a case from our own computer.
> Another local model failed every trial before it changed a file, because the server refused the agent's tool calls.
> That model may well be able to write a changelog entry.
> Only a run through that endpoint could show the problem.
> So we evaluate through the endpoint the app calls, with the model name the app sends, and we keep the stimuli, the graders and the skill the same.

## s04 — Bring your own key

**Role:** body · **Mode:** works · **Stage:** bring-your-own-key · **Introduces:** executor, copilot-sdk, bring your own key  
**On screen:** Headline 'The executor runs the agent'. A definition block 'executor · the part of Vally that runs the agent for each trial'. Under it three numbered blocks: 'starts a session', 'sends the stimulus', 'records what happened'. Then a block 'copilot-sdk · the built-in executor, through your Copilot account' and a block 'bring your own key · the executor calls a provider you choose, with your credentials'.  
**Renderer:** html (scenes/s04.html)

> That's the reasoning; now for how Vally reaches a model at all.
> When Vally says executor, it means the part of it that runs the agent for each trial.
> It starts a session, sends the stimulus, and records what happened.
> Unless a file says otherwise, Vally uses its built-in executor, named copilot SDK, which reaches models through your Copilot account.
> Having that executor call a provider you choose, with your own credentials, is called bring your own key.

## s05

**Role:** body · **Mode:** works · **Stage:** bring-your-own-key · **Introduces:** provider block  
**On screen:** Headline 'Where the executor is set'. Dark box, left: an eval file's defaults for a hosted provider (model, executor name copilot-sdk, config, provider with baseUrl, type, apiKeyEnv). Callouts on the right, each lit with its line: 'the provider's name for the model', 'still the built-in executor'. The defaults line lights first, then the model, the executor's name, and the config and provider lines. Note: 'checked with vally lint · not run'.  
**Renderer:** html (scenes/s05.html)

> The executor is chosen in an eval file, under defaults.
> And in an experiment, a variant can choose it too, under its overrides.
> Providers come in two kinds: hosted, meaning a service you pay, or local, meaning a program on your own computer; this file is set up for a hosted one.
> Here, the model line gives the name the provider knows the model by, and Vally doesn't check it against your account's list.
> The executor is still the built-in one; only where it sends the model's requests changes.
> The executor's settings go in a block named config, and here that's a single provider block.

## s05b

**Role:** body · **Mode:** works · **Stage:** bring-your-own-key · **Introduces:** baseUrl, type, apiKeyEnv  
**On screen:** Headline 'What the provider block holds'. The same dark box as the scene before, in the same place. Callouts on the right, each lit with its line: 'the address: the only required field', 'the kind of interface', 'the name of a variable, not the key'. Note: 'checked with vally lint · not run'.  
**Renderer:** html (scenes/s05b.html)

> The provider block has three fields here.
> Base URL is the provider's address, and it's the only field that's required.
> Type names the kind of interface the provider speaks.
> Its default is the interface that Open AI's own servers use, and many other servers copy that interface.
> The last field is API key env.
> It holds the name of an environment variable, and that variable holds the key.

## s06

**Role:** body · **Mode:** works · **Stage:** bring-your-own-key  
**On screen:** Headline 'No field for a key'. Two cards, each a label over a dark box of real output. Left, 'vally lint, with apiKey: abc123 in the provider block': the executor-config-invalid error, 'unknown field apiKey' lit. Right, 'a run with the variable not set': the ERROR block, 'but it is not set' lit.  
**Renderer:** html (scenes/s06.html)

> The key never goes in the file, because eval files are shared, and kept with results.
> Vally enforces that: the provider block has no field for a key, and lint rejects one.
> Vally takes the key from the environment of the vally command, when each trial starts.
> If that variable isn't set, lint still passes, but every trial stops with ERROR before the agent starts.

## s07

**Role:** body · **Mode:** works · **Stage:** bring-your-own-key · **Introduces:** Ollama  
**On screen:** Headline 'A local model needs no key'. A block 'Ollama · a free program that downloads open models and serves them on your machine'. Under it a dark box with the executor lines of a provider block that holds only 'baseUrl: http://localhost:11434/v1', with callouts 'Ollama's address on this computer' and 'no apiKeyEnv'.  
**Renderer:** html (scenes/s07.html)

> A model on your own computer needs no key.
> Ollama is a free program that downloads open models, and serves them on your machine.
> It answers at a local address, with that same Open AI interface, so a provider block with only the base URL is enough.

## s08

**Role:** body · **Mode:** works · **Stage:** bring-your-own-key · **Introduces:** results.jsonl, qwen-local/results.jsonl  
**On screen:** Headline 'Tokens, but no cost'. File panel labelled 'qwen-local/results.jsonl' showing part of one record from our run, laid out: metrics, tokenUsage with inputTokens, outputTokens, cacheReadTokens 0, byModel with the model's own counts, and the closing brace of tokenUsage. Callouts: 'counted as before', 'the tokens for each model: what we price', 'nothing came from cache', 'no cost block follows'.  
**Renderer:** html (scenes/s08.html)

> One thing changes in what a trial saves.
> Its tokens are counted as before, under token usage.
> Its cost is absent, because a cost is recorded only when every call in the trial went through Copilot.
> So we price the tokens ourselves, at our provider's rates, from the counts for each model.
> In this trial from our run, nothing came from cache.  _(depends on what the demo produced)_
> So on every turn, the whole conversation was counted again as new input.  _(depends on what the demo produced)_
> One more consequence: a judge still goes through your Copilot account, because the provider's credentials are for the agent only.

## s09 — A variant on a local model

**Role:** body · **Mode:** works · **Stage:** local-variant · **Introduces:** cost.experiment.yaml, evals/cost.experiment.yaml, qwen-local  
**On screen:** Headline 'Three new paths to vary'. File panel labelled 'evals/cost.experiment.yaml' with a minimap, opened at the vary list (lines 6 to 11); callouts beside the three new paths: 'the executor', 'the time limit', 'the number of trials'.  
**Renderer:** html (scenes/s09.html)

> Here's the experiment file from the cost comparison, as it stands once a fifth variant is added.
> We've named the new variant qwen local, and it runs a small open model, qwen three point five, through Ollama.
> It's one that can call the agent's tools, and the one that worked for us.
> The vary list has to name every setting that differs between variants.
> Three of this variant's settings differ, so the list gains three paths: the executor, the time limit, and the number of trials.
> If one were missing, say the executor path, a dry run would stop and report experiment drift.

## s10

**Role:** body · **Mode:** works · **Stage:** local-variant  
**On screen:** Headline 'The fifth variant'. The same panel, scrolled to the qwen-local variant at the end of the file (lines 35 to 44); callouts: 'slow: nine minutes, not three', 'each stimulus once, not three times', 'Ollama's address · no key'.  
**Renderer:** html (scenes/s10.html)

> Down at the end of the file is the variant itself.
> Because a local model is slow, its time limit is nine minutes, instead of the eval file's three.
> It runs each stimulus once, where the other variants run each one three times, so its pass count rests on fewer trials.
> Its provider block holds only Ollama's address.

## s11

**Role:** body · **Mode:** works · **Stage:** local-variant  
**On screen:** Headline 'One worker at a time'. Two blocks side by side: '--workers 2 · each trial waits on the other, and can run out of its nine minutes' and '--workers 1 · one request at a time, the way this server answers'. The second lights first, then the first as the wait is explained.  
**Renderer:** html (scenes/s11.html)

> We'll run it with one worker, not our usual two.
> This local server answers one request at a time, so with two workers each trial would wait on the other, and could run out of its nine minutes.

## s12

**Role:** body · **Mode:** works · **Stage:** local-variant  
**On screen:** Headline 'A price for the arithmetic'. A small table: 'input tokens · $0.10 per million', 'output tokens · $0.40 per million'. Note: 'made up for the arithmetic · not any provider's price'.  
**Renderer:** html (scenes/s12.html)

> To price the tokens we need a price, and a model on our own computer has none.
> So we've made one up for the arithmetic: ten cents per million input tokens, and forty cents per million output tokens.
> This rate isn't any provider's price; yours are on your provider's pricing page, or in your contract.

## s13 — Run a variant on your provider

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'What would you expect?'. A table with a row per variant: haiku-low and terra-low with their passing trials and cost per passing trial from the cost comparison, and qwen-local with both cells empty. The qwen-local row lights on the question.  
**Renderer:** html (scenes/s13.html)

> That's the file; now let's run it.
> We'll check Ollama, check the plan, run only the new variant, and then price its tokens.
> On these five stimuli, the account's variants passed every trial that finished.  _(depends on what the demo produced)_
> How many would you expect a small local model to pass, and what would each passing trial cost?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s14

**Role:** practice · **Mode:** use · **Stage:** run-it · **Introduces:** ollama --version, --version, ollama list  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. 'ollama --version' prints the version; 'ollama list' prints the installed models, with a line for qwen3.5:9b and its size.  
**Renderer:** terminal (tapes/s14.tape)

> First, Ollama itself: older versions can't run this model, so we check for zero point seventeen point one or later.  _(finishes before typed:1)_
> Ours is newer.  _(waits for output:1; depends on what the demo produced)_
> Our model is a download of about six point six gigabytes, which we already have, so we list what's installed.  _(finishes before typed:2)_
> There's the line for qwen three point five; Ollama serves it while its app is running.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** run-it · **Introduces:** vally experiment, vally experiment run, --dry-run  
**On screen:** Terminal in the practice folder. 'vally experiment run evals/cost.experiment.yaml --dry-run' over two lines; the plan scrolls and ends with the block headed 'qwen-local', Model: qwen3.5:9b.  
**Renderer:** terminal (tapes/s16.tape)

> The variant is now in the experiment file, exactly as we saw it.  _(finishes before typed:1)_
> Next, a dry run, which checks the plan and starts nothing.  _(finishes before typed:1)_
> We're looking for a last block headed qwen local.  _(finishes before enter:1)_
> There it is, the fifth plan, with our model's name.  _(8s to read after; waits for output:1)_

## s17

**Role:** practice · **Mode:** use · **Stage:** run-it · **Introduces:** --variant, --workers, --output-dir, ls, lesson-17, results/lesson-17  
**On screen:** Terminal in the practice folder. The run command over four lines: vally experiment run evals/cost.experiment.yaml --variant qwen-local --workers 1 --output-dir results/lesson-17; a jump cut; then the end of the output: the experiment's summary with the paths it varies, the comparison line, the one-column table, and where the run was saved. The screen is cleared out of sight; ls results/lesson-17 shows one folder named with a time.  
**Renderer:** terminal (tapes/s17.tape)

> Now the run: dash dash variant runs one named variant, so the earlier results stay as they were.  _(finishes before typed:1)_
> We give it one worker, and a results folder of its own.  _(finishes before enter:1)_
> That's one trial of each of the five stimuli, all on our computer, so it spends nothing on the Copilot account.  _(finishes before enter:1)_
> About a quarter of an hour later, the table has one column: qwen local passed two of five.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> The stimuli that failed are listed further up, and we'll go through them shortly.  _(2s to read after; waits for output:1)_
> The run is saved in a folder named with the time.  _(finishes before typed:2)_
> There it is.  _(1s to read after; waits for output:2)_

## s18

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'No baseline in this run'. Dark box, left: the end of our run's output, verbatim: the line 'Comparison unavailable — baseline not run (no observed stimuli).' and the one-column table. Callouts: 'only qwen-local ran', 'two of five'.  
**Renderer:** html (scenes/s18.html)

> One line in that output looks like a problem, and isn't.
> It says the comparison is unavailable, because the baseline wasn't run.
> With dash dash variant, only qwen local ran, so this run has nothing from the baseline, haiku low, to compare it with.
> The earlier results sit in a different run folder, so we'll make that comparison by hand.

## s19

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'No cost was recorded'. A card labelled 'the course's cost calculator · on qwen-local/results.jsonl' holding a table of what it reports: Trials, Passing, ERROR, Total cost (a dash), Per passing trial (a dash), Median tokens. The dashes light when cost is mentioned.  
**Renderer:** html (scenes/s19.html)

> The course's cost calculator takes this variant's results file, just as it took the earlier ones.
> The calculator counts five trials, two of them passing, and none ending in ERROR.  _(depends on what the demo produced)_
> Every cost is a dash, because no cost was recorded for any trial.  _(2s to read after; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'Tokens, trial by trial'. A table from our run: one row per stimulus with whether it passed, its input tokens and its output tokens, and a total row. The total row lights when the totals are said.  
**Renderer:** html (scenes/s20.html)

> So we add up the tokens ourselves.
> Each record in the results file holds that trial's input and output tokens for each model, as we saw.
> Across the five trials, that's about three hundred and sixty-five thousand input tokens, and under four thousand output tokens.  _(3s to read after; depends on what the demo produced)_

## s21

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'About 1.9 cents per pass'. Dark box, left: the arithmetic, one line each: input tokens times $0.10 per million; output tokens times $0.40 per million; the total for five trials; the total divided by the passing trials. Callouts give each line's meaning. Beside it a small table: cost per passing trial for qwen-local, haiku-low and terra-low.  
**Renderer:** html (scenes/s21.html)

> Each total is priced at its rate per million tokens.
> Nearly all of the cost is input: about three and a half cents, against a fraction of a cent for output.  _(depends on what the demo produced)_
> Together, the five trials would cost about three point eight cents.  _(depends on what the demo produced)_
> Only two of them passed, so each passing trial cost about one point nine cents.  _(depends on what the demo produced)_
> For comparison, haiku low came to about a fifth of a cent per passing trial, and terra low to about two point eight cents.  _(2s to read after; depends on what the demo produced)_

## s22 — What changed

**Role:** body · **Mode:** think · **Stage:** what-changed  
**On screen:** Headline 'A few lines changed'. Four blocks in a row, lit in turn: 'the eval file', 'stimuli and graders', 'the skill', 'the results folder'; under them a block 'what changed · a few lines in one variant'.  
**Renderer:** html (scenes/s22.html)

> So what changed, and what didn't?
> A good deal carried over.
> The same eval file, stimuli, graders and skill ran, and the results had the shape we know.
> Changing the provider was a few lines in one variant, and that's the payoff of evaluating through the endpoint.

## s23

**Role:** body · **Mode:** think · **Stage:** what-changed  
**On screen:** Headline 'Four trials skipped the skill'. A table from our run: a row per stimulus with its verdict, whether the trial loaded the skill (yes or no), and, for each failure, what the grader found. The three failures light in turn, then the one 'yes', then the 'no' cells. Note: 'skill_activation events in each saved trial'.  
**Renderer:** html (scenes/s23.html)

> The results did not carry over.
> This model passed two of five, where the account's variants passed every trial that finished.  _(depends on what the demo produced)_
> Its failures are ones we've met before: the security fix filed under Fixed, an entry for the internal refactor, and, after a release, an entry under a version number it made up, with no Unreleased heading.  _(depends on what the demo produced)_
> The saved trials show why: the skill was in the workspace, but only one of the five trials loaded it, and none of the three that failed did.  _(depends on what the demo produced)_
> So the question of whether the skill loads comes back with each new model.

## s24

**Role:** body · **Mode:** think · **Stage:** what-changed  
**On screen:** Headline 'Five trials can settle worse'. A table with two rows: qwen-local, 2 of 5, range 12% to 77%; haiku-low, 15 of 15, range 80% to 100%. Each range lights as it is said. Note: '95% ranges, from the course's range calculator'.  
**Renderer:** html (scenes/s24.html)

> Is two of five too few trials to say anything?
> Two passes in five gives a range of twelve to seventy-seven percent.  _(depends on what the demo produced)_
> Haiku low's fifteen in fifteen gives eighty to a hundred.  _(depends on what the demo produced)_
> These ranges don't overlap, so even five trials show this model doing worse on these stimuli.  _(depends on what the demo produced)_
> A count that low is enough to say worse; saying by how much would take many more trials.

## s25

**Role:** body · **Mode:** think · **Stage:** what-changed  
**On screen:** Headline 'Cheap tokens, costly passes'. A table of cost per passing trial: qwen-local (at the made-up price), haiku-low, terra-low. Under it two blocks, lit in turn: '3 of 5 trials failed' and 'nothing from cache: every turn pays for the whole conversation'.  
**Renderer:** html (scenes/s25.html)

> Cost didn't carry over either.
> Run locally, the tokens cost nothing, though each trial took minutes, and used the computer's memory the whole time.  _(depends on what the demo produced)_
> Priced at our made-up rate, each passing trial cost about nine times what haiku low's did.  _(depends on what the demo produced)_
> It was still cheaper than terra low's.  _(depends on what the demo produced)_
> Two things drove that, and neither is the price per token: three of five trials failed, and with nothing from cache, every turn paid for the whole conversation again.  _(depends on what the demo produced)_
> So a low price per token is not a low cost per passing trial.

## s26

**Role:** body · **Mode:** think · **Stage:** what-changed  
**On screen:** Headline 'One model, served one way'. Four numbered blocks, no arrows: 1 'Run · the endpoint your app calls', 2 'Count · the tokens', 3 'Price · at your own rates', 4 'Divide · by the passing trials'. Each lights as it is said.  
**Renderer:** html (scenes/s26.html)

> Scope matters here: this is one model, served one way, on one computer, with a price we invented.
> From a hosted provider, the same model might load the skill, cache its input, or be priced differently.
> What carries over is the method: run the endpoint your app calls, count the tokens, price them at your own rates, and divide by the passing trials.

## s27

**Role:** recap · **Stage:** what-changed  
**On screen:** Headline 'Where is the key kept?'. One block, 'your own provider', which opens after the question and a pause into three parts, each lit as it is said: 'The key · in the environment of the vally command', 'The tokens · counted, for each model', 'The cost · absent: we price the tokens'.  
**Renderer:** html (scenes/s27.html)

> Before you go on: with your own provider, where is the key kept, and what does a trial leave out?
> The key is in an environment variable of the vally command, and never in the eval file.  _(pause 2.5s first)_
> The trial still counts its tokens, for each model.
> It leaves out the cost, so we price the tokens ourselves, and divide by the passing trials.

## s28

**Role:** next · **Stage:** what-changed  
**On screen:** 'Next: Put a ceiling on a trial' in the display serif. Below, the hand-off question: 'How do you fail, or stop, a trial that costs or takes too much?' A note: 'Exercises are on the lesson page · Source: Vally docs, Eval Spec reference: Executor config & BYOK'.  
**Renderer:** slide (scenes/s28.html)

> You can now run a variant through your own provider, and work out its cost from your own price per token.
> Our local trials took minutes each, and a trial that gets stuck in a loop can cost ten times as much as a typical one, or take ten times as long.
> How do you fail, or stop, a trial that costs or takes too much?
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
