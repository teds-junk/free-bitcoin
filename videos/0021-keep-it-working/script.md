# Keep it working — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0021-keep-it-working.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** How do I make this a routine that I and a teammate can repeat?  
**The viewer starts:** A professional programmer who knows the shell, exit codes and echo $?, and has watched the changelog-entry skill measured through the course so far on two models (claude-haiku-4.5 and gpt-5.6-terra). Knows skill, eval file, stimulus, grader, trial, PASS, FAIL and ERROR, and the practice folder. Has four eval files: changelog (five single-request stimuli graded by patterns and a hidden script), conversation, loading, and wording (graded by an LLM judge with a rubric). Has used vally lint, vally oracle with a golden patch, vally grade to re-grade a saved run (it cannot re-grade script graders), vally eval with -e, --model, --runs, --workers and --output-dir, experiments (with-and-without, before-and-after), cost per passing trial in AIU (one AIU is about a cent), budget graders set to 215000 tokens, 10 turns and 30 seconds with the agent stopped after a minute, and vally compare with --fail-on-regression, whose pairwise judge exits 1 on a regression. Has four questions for a run that goes wrong, and knows an ERROR trial did not complete. Has never tagged a stimulus, defined a suite, or used --require-pass.

1. **cheapest-first**: after this, the viewer can choose the cheapest check that can answer the question in front of them
2. **suites-and-exit-codes**: after this, the viewer can read a suite in .vally.yaml and predict the exit code of a run, with and without --require-pass
3. **two-suites**: after this, the viewer can run a quick suite and a full suite so that a failing verdict or an over-budget trial is an error, and write the conventions down
4. **where-it-stands**: after this, the viewer can keep the skill working after the next edit: say what the two suites and the page guard, what they cost, and what one trial per stimulus cannot show

## s01 — From checks to a routine

**Role:** hook · **Mode:** think · **Stage:** cheapest-first  
**On screen:** Headline 'Keep it working' in the display serif. Three blocks in a row, no arrows: 'After every edit · one short command', 'Before sharing · a longer one', 'For the team · one page'. Each lights as the promise names it.  
**Renderer:** html (scenes/s01.html)

> Everything we've built works when we remember to run it, in the right order, with the right flags.
> That isn't a routine, and it won't survive a busy week or a new teammate.
> Meanwhile the skill will be edited again, and the models under it will change without telling us.
> Here, you'll make the right check the easy one: one short command after every edit, a longer one before sharing, and one page that says what the team agreed.

## s02 — Cheapest check first

**Role:** body · **Mode:** think · **Stage:** cheapest-first  
**On screen:** Eyebrow 'Cheapest check first'. Headline 'Five checks, cheapest first'. A row of five blocks, no arrows: lint · free, oracle · free, re-grade · free, quick · 10 runs, full · 30 runs. The three free ones light together, then quick, then full. A note: agent runs, for two models.  
**Renderer:** html (scenes/s02.html)

> Let's start with what each check costs.
> We now have five ways to check the skill, and they differ enormously in cost.
> Lint, the oracle and a re-grade start no agent, so for code graders they're free.
> The other two are new here: a quick run of the stimuli that code can check, and a full run of everything.
> On two models, the quick one spends ten agent runs, and the full one spends thirty.

## s03

**Role:** body · **Mode:** think · **Stage:** cheapest-first  
**On screen:** Headline 'Match the check to the question'. A table with three columns, Check, Answers, After: vally lint · is the eval file well formed · editing an eval file; vally oracle · do the graders pass a correct answer and fail an untouched file · changing a grader; vally grade · what do today's graders and budgets say about saved trials · changing a pattern, a budget or a rubric; quick · did the edit break what code can check, or go over budget · every edit to the skill; full · does everything still hold · before sharing, or a model change. Each row lights as it is named.  
**Renderer:** html (scenes/s03.html)

> The rule is to use the cheapest check that can answer the question we actually have.
> After editing an eval file, that's lint.
> After changing a grader, it's the oracle, which tries a correct answer and an untouched file.
> After changing a pattern, a budget or a rubric, a re-grade says what the new version makes of trials already saved.
> A script grader can't be re-graded, because the workspace it reads is gone.
> So a change to a script goes back to the oracle.
> After every edit to the skill, the quick run asks whether anything code can check has broken, or gone over budget.
> Finally, before sharing the skill, or when a model changes, the full run asks whether everything still holds.

## s04

**Role:** body · **Mode:** think · **Stage:** cheapest-first  
**On screen:** Headline 'Three checks for one-off questions'. Three blocks, no arrows: 'With and without the skill · after a large rewrite', 'Before and after, then vally compare · did an edit help or hurt', 'Cost per passing trial · before changing model or effort'. Each lights in turn.  
**Renderer:** html (scenes/s04.html)

> Three more checks sit outside that order, because each answers a one-off question.
> After a large rewrite, the with-and-without experiment says whether the skill still beats no skill.
> To learn whether one edit really helped, we run a before-and-after experiment, then vally compare, which spends judge calls and starts no agent.
> Finally, cost per passing trial is what to compare before moving to a different model or reasoning effort.

## s05

**Role:** body · **Mode:** think · **Stage:** cheapest-first  
**On screen:** Headline 'What drifts is agreement'. Four blocks in a two-by-two grid, each a question: 'What deserves a grader?', 'Where do grading files go?', 'How is a result reported?', 'What may a run cost?'. Each lights as it is said. Under them a line: 'One page, written down while it is fresh'.  
**Renderer:** html (scenes/s05.html)

> For a team, though, the commands are the easy part.
> What drifts is agreement: what deserves a grader, where grading files are kept, how a result is reported, and what a run may cost.
> So we'll write those down on one page, while they're fresh.
> People can disagree with something written down, and that's how the agreement gets better.

## s06 — Name a group of stimuli

**Role:** body · **Mode:** works · **Stage:** suites-and-exit-codes · **Introduces:** tags, changelog.eval.yaml  
**On screen:** Eyebrow 'Tags, suites and exit codes'. Headline 'A tag labels a stimulus'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, showing the first three stimuli's name lines and the tags line under each, with a 'lines hidden' row between. One callout on the right: 'a name and a value · the words are ours'. The word tags lights, then 'tier: quick', then the same line under the next two stimuli.  
**Renderer:** html (scenes/s06.html)

> That's the plan; here's what Vally gives us to build it, starting with tags.
> When we say tag, we mean a label on a stimulus: a name and a value, on a line named tags.
> Here the name is tier and the value is quick; both words are ours, and any words will do.
> All five stimuli in this file get the same line, because all five are graded by code.

## s07

**Role:** body · **Mode:** works · **Stage:** suites-and-exit-codes · **Introduces:** suite, .vally.yaml  
**On screen:** Headline 'A suite names a group'. File panel labelled '.vally.yaml', the whole file (13 lines), with callouts on the right: 'the name we type' (quick), 'eval files it draws on', 'only stimuli tagged tier: quick' (filter), 'no filter: every stimulus' (full). Each lights as the voice reaches it.  
**Renderer:** html (scenes/s07.html)

> Next, the suite: a named group of stimuli.
> It's a list of eval files, optionally narrowed to the stimuli with a given tag.
> Suites are defined in a file named dot vally dot yaml, in the folder we run Vally from.
> This one defines two; the first is named quick, which is what we'll type on the command line.
> The quick suite draws on one eval file, and its filter is matched against each stimulus's tags, so it keeps the five we just tagged.
> The second, full, lists four eval files with no filter, so every stimulus in them runs.
> Those four hold the single requests, the conversation, the loading test, and the judged wording.

## s08

**Role:** body · **Mode:** works · **Stage:** suites-and-exit-codes · **Introduces:** vally eval, --suite, --model, --workers  
**On screen:** Headline 'One option runs a suite'. Dark box, left: the vally eval command over three lines, with '--suite quick' where '-e' and a file used to be. Callouts on the right: 'in place of -e and a file' beside --suite quick, 'as before' beside the model and workers lines.  
**Renderer:** html (scenes/s08.html)

> To run a suite, vally eval takes dash dash suite and the suite's name, in place of dash e and a file.
> Everything else about the command works as before.
> One thing to know: a suite only names stimuli, and adds no graders of its own.

## s09

**Role:** body · **Mode:** works · **Stage:** suites-and-exit-codes  
**On screen:** Headline 'Quick stimuli carry their budgets'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, at the typo-fix stimulus: its constraints (max_agent_duration: 1m) and its three budget graders (token-budget 215000, turn-count 10, wall-time 30s). The panel scrolls to the three budgets as they are named and each lights in turn; then it scrolls back up to the time limit, which lights.  
**Renderer:** html (scenes/s09.html)

> The five quick stimuli are the ones that already have budgets, so the quick suite carries them.
> Every trial is checked against a ceiling on its tokens, on its turns, and on its time.  _(2s to read after)_
> The agent is also stopped after a minute, and whatever it had done by then is graded.
> When a trial goes over a budget, its stimulus fails, exactly as it would for a wrong entry.
> That's what makes the quick suite a cost check as well as a quality check.

## s10 — Make failure an error

**Role:** body · **Mode:** works · **Stage:** suites-and-exit-codes · **Introduces:** exit code, echo $?, --require-pass, vally grade, --run-dir  
**On screen:** Headline 'Exit codes make failure loud'. A table: rows 'every stimulus passed', 'a stimulus failed', 'a trial ended in ERROR'; columns 'vally eval' (0, 0, 1) and 'with --require-pass' (0, 1, 1). The 'failed' row's first cell lights, then its second, then the ERROR row. A note: vally grade takes the same option.  
**Renderer:** html (scenes/s10.html)

> The last piece is the exit code, which is what scripts and automated checks act on.
> Unless told otherwise, vally eval exits with zero even when stimuli fail, because the run itself completed.
> Adding dash dash require pass changes that: any failing stimulus makes the exit code one, whichever grader failed it, budgets included.
> When a trial ends in error, the exit code is one either way.
> Vally grade accepts the same option.

## s11

**Role:** body · **Mode:** works · **Stage:** suites-and-exit-codes  
**On screen:** Headline 'A third gate, for judged quality'. Dark box, left: the vally compare command over four lines (--baseline haiku-after, --treatment haiku-before, --judge-model, --fail-on-regression) and, under it, the mean-score line our run printed, then the mean-score and Regression lines of an earlier run. Callouts on the right: 'the newer skill' (baseline), 'the change under test' (treatment), 'exit 1 when the whole range is below zero', 'our run: exit 0', 'an earlier run: exit 1'.  
**Renderer:** html (scenes/s11.html)

> One kind of failure gets past every grader: an edit that makes the entries a little worse, while every pattern still matches.
> That's what the pairwise judge is for.
> Vally compare gives it two runs of the same stimuli, a baseline and a change, and it scores each pair of answers.
> With dash dash fail on regression, the command exits with one when the change scored clearly worse.
> Clearly worse means that the whole range around its score is below zero.
> Earlier, we tested it by treating the older skill as the change.  _(depends on what the demo produced)_
> When we ran it, the range reached just above zero, so the command exited with zero.  _(depends on what the demo produced)_
> In an earlier run of the same comparison, the whole range was below zero, and it exited with one.  _(depends on what the demo produced)_
> It needs a before-and-after experiment and about eighteen judge calls, so it belongs before we rely on an edit, not after every edit.
> It also gates on the judged score alone; a rise in tokens is the budgets' job.

## s12 — Run the quick suite

**Role:** practice · **Mode:** use · **Stage:** two-suites  
**On screen:** Eyebrow 'Two suites and a conventions page'. Headline 'What would the exit code be?'. One block titled 'the quick suite, without --require-pass · one trial over its token budget, nothing else wrong'. After the question and a beat it opens into two parts: 'Exit code 0 · the run itself completed' and 'With --require-pass: 1 · a failing verdict becomes an error'.  
**Renderer:** html (scenes/s12.html)

> That's how the pieces work; now let's put them to work.
> The tags and the suites file are in place in our practice folder, exactly as we just went through them.
> Here's a question first: suppose we ran the quick suite without require pass, and one trial went over its token budget.
> Nothing else fails, and nothing errors: what would the exit code be?  _(2.5s to read after)_
> It would be zero: the budget fails that stimulus, but without the option, a failing verdict doesn't change the exit code.
> So anything automated has to add the option, and we will too.

## s13

**Role:** practice · **Mode:** use · **Stage:** two-suites · **Introduces:** vally lint, -e, --output-dir, lesson-21-quick  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. vally lint -e evals/changelog.eval.yaml prints its one warning. The screen is cleared out of sight. Then the quick suite over four lines (--suite quick, both models, --workers 2 --require-pass, --output-dir results/lesson-21-quick), a jump cut, the end of its output with the table, and echo $? printing the exit code. Held until read.  
**Renderer:** terminal (tapes/s13.tape)

> First, we lint the eval file, since we've just edited it.  _(finishes before typed:1)_
> There's one warning, the usual one about scoring defaults, and no errors.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Now the quick suite, on both models, two workers at a time, with require pass so that a failure is an error.  _(finishes before typed:2)_
> Its results go to a folder of their own, and it spends ten agent runs.  _(finishes before enter:2)_
> The table at the end counts the stimuli that passed, out of five, for each model.  _(finishes before enter:2)_
> About a minute later, every stimulus has passed on both models, budgets included.  _(3s to read after; waits for output:2; depends on what the demo produced)_
> So what was its exit code?  _(finishes before typed:3)_
> Zero: nothing failed.  _(2s to read after; waits for output:3; depends on what the demo produced)_

## s14 — See a failure exit with one

**Role:** practice · **Mode:** use · **Stage:** two-suites · **Introduces:** results.jsonl, lesson-5-before, 2026  
**On screen:** Terminal in the practice folder. cd into the one run folder under results/lesson-5-before (its name completed with Tab); then vally grade over two lines with --run-dir . --require-pass, reading results.jsonl; its blocks scroll, ending on the last ones; then echo $? prints 1. Held until read.  
**Renderer:** terminal (tapes/s14.tape)

> A passing run can't show the option at work, so let's see a wrong entry fail loudly, without spending anything.  _(finishes before typed:1)_
> The run we'll use is the first one we graded, before the skill had its rules, so it has plenty of failures.  _(finishes before typed:1)_
> None of its graders is a script, and a script grader is the one kind that can't be re-graded.  _(finishes before typed:1)_
> We change into that run's folder.  _(finishes before typed:1)_
> Then we re-grade it with today's eval file, and with require pass.  _(waits for output:1; finishes before typed:2)_
> These are the failing blocks from that run, each now with the budgets among its graders.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> Every budget passed in all eighteen trials, three stimuli three times on two models; only the graders of the result failed.  _(2s to read after; waits for output:2; depends on what the demo produced)_
> So what's the exit code this time?  _(finishes before typed:3)_
> It's one: a failing verdict is now an error.  _(2s to read after; waits for output:3; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** two-suites  
**On screen:** Headline 'One budget lowered, for a moment'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, at the typo-fix stimulus's token-budget grader, whose max now reads 70000. A callout: 'was 215000'. The max line lights.  
**Renderer:** html (scenes/s15.html)

> Next, a trial that's over budget, which none of ours is, so we make one for a moment.
> In the typo fix stimulus, we lower the token budget from two hundred fifteen thousand to seventy thousand, which is below what those trials used.  _(depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** two-suites  
**On screen:** Terminal in the run's folder. The same vally grade command with --require-pass; its blocks scroll; then echo $? prints 1. Held until read.  
**Renderer:** terminal (tapes/s16.tape)

> We run the same re-grade again, and then print the exit code.  _(finishes before typed:1)_
> It's one again.  _(6s to read after; waits for output:2; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** two-suites  
**On screen:** Headline 'Over budget fails like any other'. Dark box, left: one typo-fix block from that re-grade as printed (4/5 graders passed; token-budget max 70000, the trial's tokens exceed it; Score 98.8% | FAILED). Callouts on the right: 'did the work' (4/5), 'cost too much' (the budget line), 'the score decides nothing here' (the score line). A note gives the other trials' token counts.  
**Renderer:** html (scenes/s17.html)

> That output is longer than one screen, so here's the part that changed.
> These typo fix trials passed every grader a moment ago; now they fail, on the budget alone.  _(depends on what the demo produced)_
> Seventy-four thousand tokens is over a maximum of seventy thousand.  _(depends on what the demo produced)_
> The score still says ninety-eight point eight percent.  _(depends on what the demo produced)_
> That's because going slightly over a budget costs only a little of the score.
> With no scoring block, though, the score decides nothing: every grader has to pass, and one didn't.
> So a trial that did the work and cost too much is a failing verdict like any other.
> With that seen, the budget goes back to two hundred fifteen thousand.

## s18 — Run the full suite

**Role:** practice · **Mode:** use · **Stage:** two-suites · **Introduces:** lesson-21-full  
**On screen:** Terminal in the practice folder. The full suite over four lines (--suite full, both models, --workers 2 --require-pass, --output-dir results/lesson-21-full), a jump cut, then the end of its output: the model summary and the table with a row per eval file, every cell passing; then echo $? prints 0. Held until read.  
**Renderer:** terminal (tapes/s18.tape)

> Now everything, once: the full suite, with the same options, into its own results folder.  _(finishes before typed:1)_
> It spends thirty agent runs and six judge calls.  _(finishes before enter:1)_
> The table at the end has a row for each of the four eval files.  _(finishes before enter:1)_
> Several minutes later, every stimulus has passed on both models, in all four files.  _(5s to read after; waits for output:1; depends on what the demo produced)_
> Let's see what it reported.  _(finishes before typed:2)_
> Zero again: nothing failed, budgets and judge included.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** two-suites  
**On screen:** Headline 'Our first run had trouble'. Left: the table of our FIRST run of the full suite (eval file, one column per model, passed of total). Right: two cards: 'ERROR × 2 · conversation · three-requests and wording · cache on claude-haiku-4.5 · Session disconnected' and 'FAIL · loading · skip-question on gpt-5.6-terra · the skill loaded for a question that should not load it'. A note: our first run, minutes before the one we kept, exit code 1. The ERROR card lights, then the FAIL card.  
**Renderer:** html (scenes/s19.html)

> That was our second run of the full suite; the first, a few minutes before it, ended differently.  _(depends on what the demo produced)_
> Here's the first run's table, with the three stimuli Vally listed above it.  _(depends on what the demo produced)_
> They're two different kinds of trouble.  _(depends on what the demo produced)_
> On haiku, two trials ended in error, because their sessions dropped.  _(depends on what the demo produced)_
> As before, an error isn't a verdict: the trial didn't complete, so it says nothing about the skill.
> So we ran the suite again, and that's the run we kept.  _(depends on what the demo produced)_
> The other is a real fail: on terra, a question that shouldn't load the skill did load it.  _(depends on what the demo produced)_
> The loading grader that forbids that is what caught it.  _(depends on what the demo produced)_
> Either problem alone makes the command exit with one, and that first run did.  _(depends on what the demo produced)_

## s20 — Write down what we agreed

**Role:** practice · **Mode:** use · **Stage:** two-suites · **Introduces:** CONVENTIONS.md  
**On screen:** Headline 'Ten headings, one page'. File panel labelled 'CONVENTIONS.md' with a minimap. It opens at the first headings and scrolls down through the page in steps, as the voice names them; the last heading, 'Models and dates', lights at the end.  
**Renderer:** html (scenes/s20.html)

> One thing is left: the page that says what we've agreed.
> Ours is a file named conventions, with ten headings and a sentence or two under each.
> It opens with what earns a grader, code before judge, where files are kept, and what we check before trusting a grader or a judge.
> Then come what we run and when, how we report a result, and what a run may cost.
> The last two are what to do when a run goes wrong, and which models we used, on which date.
> That last one matters because models and their prices change: a result means little without knowing which model produced it, and when.

## s21 — Where the skill stands

**Role:** body · **Mode:** think · **Stage:** where-it-stands  
**On screen:** Eyebrow 'Where the skill stands'. Headline 'From one pair to two suites'. Three blocks in a row, no arrows: 'At the start · a first draft, and a tick that hid a made-up number', 'First graders · 1 of 6 pairs passed', '30 of 30 · stimuli passed on each model, in the full suite'. Each lights in turn.  
**Renderer:** html (scenes/s21.html)

> So where does the skill stand?
> At the start, it was a first draft that one model answered by making up a pull request number, behind a tick that hid it.
> With our first graders, one pair of stimulus and model passed, out of six.  _(depends on what the demo produced)_
> Now the suites cover a conversation, a loading test with near-miss requests, a judged quality that no pattern can see, and budgets on every quick stimulus.
> In our last run, every stimulus in them passed on both models.  _(depends on what the demo produced)_
> Every rule in the skill is there because a trial showed it was needed, and every grader is there because a failure was seen.

## s22

**Role:** body · **Mode:** think · **Stage:** where-it-stands  
**On screen:** Headline 'What the routine costs'. A table: rows 'quick suite' and 'full suite'; columns trials, AIU, about (dollars). Under it a line with the largest quick trial's tokens beside the budget. The quick row lights, then the full row, then the tokens line. A note names the run.  
**Renderer:** html (scenes/s22.html)

> Now, what does the routine cost?
> In our run, the quick suite's ten trials cost about twenty-four AIU, which is about twenty-four cents an edit.  _(depends on what the demo produced)_
> The full suite's thirty trials cost about sixty-seven AIU, with its six judge calls on top.  _(depends on what the demo produced)_
> None of the quick trials came near the token budget: the largest used ninety-one thousand tokens, against two hundred fifteen thousand.  _(depends on what the demo produced)_

## s23

**Role:** body · **Mode:** think · **Stage:** where-it-stands  
**On screen:** Headline 'A cheaper model, checked first'. Two blocks side by side: 'our two models · about 24 AIU an edit' and 'claude-haiku-5.5, low effort · about 1 AIU an edit · 15 of 15 passed earlier'. Under them, three numbered steps from the conventions: compare cost per passing trial; re-test the budgets on its saved trials; run the full suite on it first. Each lights as it is said.  
**Renderer:** html (scenes/s23.html)

> Those figures are for the two models we've used throughout.
> Earlier, in the cost experiment, the newer haiku model at low effort passed all fifteen of its trials on these same stimuli, at about a fifth of an AIU each.  _(depends on what the demo produced)_
> On that one variant, a quick suite would cost about one AIU an edit: a cent.  _(depends on what the demo produced)_
> Our conventions say how to make that move: compare cost per passing trial, re-test the budgets on its saved trials, and run the full suite on it first.

## s24

**Role:** body · **Mode:** think · **Stage:** where-it-stands  
**On screen:** Headline 'One trial per stimulus'. Two blocks side by side for the loading question skip-question on terra: '0 of 1 · in our first run' and '1 of 1 · in the second run, minutes later'. Under them: 'One pass shows it can pass, not that it will every time.' The first block lights, then the second.  
**Renderer:** html (scenes/s24.html)

> One caution goes with that last table: it's one trial per stimulus.
> In our two runs of the full suite, the same loading question failed on terra the first time, and passed the second.  _(depends on what the demo produced)_
> A single passing trial shows that a stimulus can pass; it doesn't show that it will pass every time.
> The suites are how we find out when that changes.

## s25

**Role:** recap · **Stage:** where-it-stands  
**On screen:** Eyebrow 'Recap'. Headline 'What are the five checks?'. One block, 'cheapest check first', which opens after the question and a pause into five parts, each lit as it is said: lint · after editing an eval file; oracle · after changing a grader; re-grade · after changing a pattern, budget or rubric; quick suite · after every edit; full suite · before sharing, or a model change.  
**Renderer:** html (scenes/s25.html)

> Before you go on: what are the five checks, from cheapest to most expensive?
> Lint, after editing an eval file.  _(pause 2.5s first)_
> The oracle, after changing a grader.
> Re-grading a saved run, after changing a pattern, a budget or a rubric.
> The quick suite, after every edit to the skill.
> Finally, the full suite, before sharing, and whenever a model changes.

## s26

**Role:** next · **Stage:** where-it-stands  
**On screen:** 'Next' card. Headline 'The skill inside an app' in the display serif. Below: 'Start the agent where the app would: does the skill hold when an app, not a person, starts the agent?' A note: 'Exercises and the workflow guide are on the course site · Source: Vally docs, Authoring Eval Suites'.  
**Renderer:** slide (scenes/s26.html)

> That completes the first part of the course.
> You can now run a quick suite after every edit and a full suite before sharing, with commands that fail loudly on a failing verdict, an over-budget trial, or a regression.
> You also have a one-page conventions file to hand to a teammate.
> In the second part, the team behind our made-up tool has put the skill inside its release tooling.
> Does it still hold when an app, not a person, starts the agent?
> That's the next lesson.
> The exercises on the lesson page are worth doing first, and the workflow guide there shows how a service can run the quick suite on every proposed change.
