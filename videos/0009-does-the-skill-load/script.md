# Does the skill load when it should — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0009-does-the-skill-load.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** Does the agent load the skill for the requests it is meant for, and leave it alone for the others?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through eight steps: it was run on two models (claude-haiku-4.5 and gpt-5.6-terra), its failure modes were named from saved trials, graders were written and tested for them, and rules were added to the skill twice. Knows skill, agent, model, eval, eval file, workspace, patch, stimulus, grader, trial, trajectory, the practice folder and the starter folder; vally eval with -e, --model, --runs, --workers and --output-dir; vally lint; the results folder with its report and results.jsonl; and the words PASS, FLAKY, FAIL and ERROR, where ERROR is a trial that did not finish, for example because its session dropped; and the agent environment, the part of an eval file that says what the agent starts with. Has read the skill's file, including the one-line description at its top. In every trial so far the skill was the only one installed and every request said 'changelog'. Does not know how an agent chooses among skills, what loading a skill means, the term near-miss request, the skill_activation event, the report's Skills column, or the skill-invocation grader.

1. **description-decides**: after this, the viewer can say how an agent chooses a skill, name the two ways loading can fail, and tell a near-miss request from one that should load the skill
2. **how-loading-is-recorded**: after this, the viewer can find whether a skill loaded in a trial's record and in the report, and predict what a skill-invocation grader passes
3. **test-then-fix**: after this, the viewer can run a loading eval on two models, read which skills loaded, rewrite the description, and run it again
4. **what-the-test-showed**: after this, the viewer can show what rewriting the description changed on both models, and say what a result that small supports

## s01 — The description decides

**Role:** hook · **Mode:** think · **Stage:** description-decides  
**On screen:** Headline 'Does the skill load?' in the display serif. Two cards, one above the other, both from the real skill file: 'What the agent is given' holds the one description line; 'What it reads only if it opens the skill' holds the first rules. The rules card lights, then the description card.  
**Renderer:** html (scenes/s01.html)

> Every rule we've added to the skill does nothing unless the agent reads it.
> Agents don't read every skill they have.
> Instead, an agent reads a one-line description of each, and opens a skill only when that line seems to fit the request.
> Here, you'll test whether an agent opens the skill for the requests it's meant for and leaves it alone for the others, and see what rewriting its description changes.

## s02

**Role:** body · **Mode:** think · **Stage:** description-decides · **Introduces:** SKILL.md, changelog-entry/SKILL.md  
**On screen:** File panel labelled 'changelog-entry/SKILL.md', with a minimap, showing the top of the skill file as it stands. Lines 2 and 3 (name and description) light with the note 'all the agent has at the start'; then the lines under the second '---' light with the note 'read only if the skill loads'; then the description line alone.  
**Renderer:** html (scenes/s02.html)

> Let's start with how an agent chooses a skill.
> When it starts, it's given the name and description of every installed skill, and nothing else about them.
> When a request arrives, the model decides whether any description fits.
> If one does, the agent loads that skill, which means it reads the rest of the file.
> If none does, those instructions are never seen.
> Our skill's description is still the one line from the first draft.

## s03

**Role:** body · **Mode:** think · **Stage:** description-decides  
**On screen:** Headline 'Two new ways to fail'. Two blocks side by side, no arrow: 'It doesn't load when it should · the agent works from habit, without the rules' and 'It loads when it shouldn't · changelog rules on a task that isn't a changelog entry'. Each fills as it is described.  
**Renderer:** html (scenes/s03.html)

> That gives a skill two new ways to fail, and the graders we've written can't see either one.
> First, it doesn't load when it should.
> Then the agent does the task anyway, from its own habits, without our rules, and the result may even look fine.
> Second, it loads when it shouldn't, and the agent applies changelog rules to a task that isn't a changelog entry.

## s04

**Role:** body · **Mode:** think · **Stage:** description-decides  
**On screen:** Headline 'Skills often go unused'. Two blocks: 'A skill, in the cases it was meant for' and a large '56%' with 'went unused'. Source note: 'Vercel, 2026 · the vendor's own figure · run counts not published'. The figure lights when it is said.  
**Renderer:** html (scenes/s04.html)

> Not loading is the common one.
> In one vendor's report from twenty twenty-six, a skill went unused in fifty-six percent of the cases it was meant for.
> That figure is the vendor's own, and the number of runs behind it wasn't published, but the pattern is widely reported.

## s05

**Role:** body · **Mode:** think · **Stage:** description-decides · **Introduces:** near-miss request  
**On screen:** Headline 'Near the edge'. Two quoted requests from the eval file, side by side: 'An obvious request' (PR 70 adds a notes rename command. Update the changelog.) and 'A near-miss request' (We're announcing 1.2.0 today. Draft the release notes from the changelog.). Under them, the definition: 'shares words or a subject with the skill's job, but is not its job'. The first quote lights, then the second.  
**Renderer:** html (scenes/s05.html)

> Obvious requests tell us little about either failure.
> Any request to update the changelog will load a changelog skill with almost any description.
> What tells us something is a request near the edge of the skill's job.
> So here's a term: a near-miss request shares words or a subject with the skill's job, but isn't its job.
> Draft the release notes from the changelog mentions the changelog, and it isn't asking for a changelog entry.

## s06

**Role:** body · **Mode:** think · **Stage:** description-decides  
**On screen:** Headline 'Two groups of requests'. Two blocks: 'Should load the skill · including requests that never use its obvious word' and 'Near-miss requests · should not load it'. Under them: 'observed in real trials, not asked of the model'. Each block fills as it is named, then the line under them.  
**Renderer:** html (scenes/s06.html)

> So a loading test needs two groups of requests.
> Some should load the skill, including ones that never use its obvious word, which for ours is changelog.
> The rest are near-miss requests, which should not load it.
> And the test has to observe what the agent did, because asking a model whether it would use a skill tests what it says, not what it does.

## s07

**Role:** body · **Mode:** think · **Stage:** description-decides  
**On screen:** Headline 'A description says three things'. Three blocks across the width: 'What the skill does', 'When to use it · a situation, not a word to look for', 'What it is not for'. Each fills as it is said.  
**Renderer:** html (scenes/s07.html)

> When a test shows the description is at fault, a better one says three things.
> It says what the skill does.
> It says when to use it, described as a situation, and not as a word to look for.
> And it says what the skill is not for.

## s08

**Role:** body · **Mode:** think · **Stage:** description-decides  
**On screen:** Headline 'How big a test?'. A table with two rows: 'For a skill you depend on · about 20 requests · 3 trials each · some held back' and 'Our test · 6 requests · 2 trials each · none held back'. Source note: 'agentskills.io, Optimizing skill descriptions · conventions, with no published calculation behind them'. The first row lights, then the 'held back' cell, then the second row.  
**Renderer:** html (scenes/s08.html)

> How big should such a test be?
> For a skill you depend on, the usual guidance is about twenty requests, with three trials each.
> Some of those requests are kept aside and never looked at while rewording the description, so it isn't just fitted to the test.
> Those numbers are conventions; nobody has published a calculation behind them.
> Our test has six requests and two trials each, which is enough to show the method.

## s09 — How a trial records loading

**Role:** body · **Mode:** works · **Stage:** how-loading-is-recorded · **Introduces:** skill_activation, results.jsonl, results.jsonl · one record, spread out  
**On screen:** File panel labelled 'results.jsonl · one record, spread out', with a minimap: the record from our first run, scrolled to one event in its trajectory, with a 'lines hidden' row inside it. '"type": "skill_activation"' lights with the note 'one each time a skill loads'; then '"name": "changelog-entry"' with 'which skill'; then '"turn": 0' with 'which turn, counting from 0'.  
**Renderer:** html (scenes/s09.html)

> That's the idea; here's where a trial records it.
> Each trial's record in results dot jsonl holds its trajectory, the full record of what the agent did, as a list of events.
> When the agent loads a skill, Vally adds an event of the type skill activation.
> Its data names the skill that loaded.
> Its turn field says which request of a conversation that was, counting from zero; every trial so far has had just one.
> Vally calls this activation, and it means what we've been calling loading.

## s10

**Role:** body · **Mode:** works · **Stage:** how-loading-is-recorded · **Introduces:** eval-results.md  
**On screen:** Headline 'The report has a Skills column'. A table of three columns from the report of our earlier five-trial run, labelled 'eval-results.md · three of its twelve columns': Stimulus, Skills, Pass Rate, with one row per model: typo-fix · changelog-entry (5×) · 5/5. The Skills header lights, then the two Skills cells.  
**Renderer:** html (scenes/s10.html)

> You rarely need to open a record to find that out.
> Every report has a column named Skills.
> For each stimulus, it lists the skills that loaded in its trials, with a count.
> Here it is in the report from our five-trial run: the changelog entry skill loaded five times on each model.
> When no skill loaded, the column shows a dash.

## s11

**Role:** body · **Mode:** works · **Stage:** how-loading-is-recorded · **Introduces:** skill-invocation, loading.eval.yaml, evals/loading.eval.yaml, commit-message, release-notes  
**On screen:** File panel labelled 'evals/loading.eval.yaml', with a minimap and notes on the right. First the agent environment: the three skills light with the note 'three installed, so the agent has a choice'. The panel scrolls to the stimulus load-no-keyword: its prompt lights with 'should load, and never says changelog'; then 'required: [changelog-entry]' with 'passes only if it loaded'.  
**Renderer:** html (scenes/s11.html)

> Events like that are read by a grader named skill invocation, which is one more word for loading.
> The starter folder has an eval file that uses it, named loading.
> Its agent environment installs three skills, so the agent has a real choice.
> Beside ours, one writes commit messages, and one drafts release notes; we'll call those two the neighbours.
> This stimulus, load no keyword, should load the skill, and its request never says changelog.
> Its grader lists our skill under required, so it passes only if that skill loaded.

## s12

**Role:** body · **Mode:** works · **Stage:** how-loading-is-recorded  
**On screen:** The same panel, opening where the last scene left it, scrolls on to the stimulus skip-release-notes. Its prompt lights with the note 'a near-miss: it belongs to a neighbour'; then 'disallowed: [changelog-entry]' with 'passes only if it did not load'.  
**Renderer:** html (scenes/s12.html)

> Here's the other kind: a near-miss request, which mentions the changelog, and is a job for the release notes skill.
> Its grader lists our skill under disallowed, so it passes only if that skill did not load.
> Which other skill loaded, if any, doesn't matter to this grader.

## s13

**Role:** body · **Mode:** works · **Stage:** how-loading-is-recorded  
**On screen:** Headline 'Six requests, two shapes'. A table of the six stimuli from the eval file: name, the key sentence of its request, and its grader's list (required or disallowed). The three load- rows light together, then load-plain alone, then the three skip- rows.  
**Renderer:** html (scenes/s13.html)

> That file has six stimuli, in those two shapes.
> Three should load the skill, and their names begin with load.
> Only load plain says changelog; the other two ask to note a change down, and to make sure users can see a fix.
> The other three are near-miss requests, named skip: one wants a commit message, one wants release notes, and one asks what changed in a past version.
> These graders have no name of their own, so in its output Vally labels each with its type and what it requires.
> Loading varies from trial to trial like everything else, so we'll run each stimulus twice.

## s14 — Test loading, then fix it

**Role:** practice · **Mode:** use · **Stage:** test-then-fix  
**On screen:** Headline 'Before and after'. The comparison table, empty: one row per stimulus, and four columns: haiku before, haiku after, terra before, terra after. The 'before' headers light, then the 'after' headers. The cells stay empty.  
**Renderer:** html (scenes/s14.html)

> That's how loading is recorded; now let's test it.
> First, we'll read the two neighbouring skills and check the eval file.
> Then we'll run the six requests on both models, with the description as it stands.
> After that, we'll rewrite the description and run them again.
> What would you expect a one-line description to get wrong?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s15

**Role:** practice · **Mode:** use · **Stage:** test-then-fix · **Introduces:** cat, vally lint, -e  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. cat skills/commit-message/SKILL.md prints a nine-line skill; the screen is cleared out of sight; cat skills/release-notes/SKILL.md prints a ten-line skill; cleared again; vally lint -e evals/loading.eval.yaml prints one line: the file is valid.  
**Renderer:** terminal (tapes/s15.tape)

> Here are the two neighbours, starting with the commit message skill.  _(finishes before typed:1)_
> It has a one-line description of its own, and it tells the agent to reply without editing any file.  _(4s to read after; waits for output:1)_
> Then the release notes skill.  _(finishes before typed:2)_
> It drafts an announcement from the changelog, and doesn't edit it either.  _(4s to read after; waits for output:2)_
> Lint checks the eval file for mistakes without starting an agent.  _(finishes before typed:3)_
> It's valid.  _(1s to read after; waits for output:3)_

## s16

**Role:** practice · **Mode:** use · **Stage:** test-then-fix · **Introduces:** vally eval, --model, --runs, --workers, --output-dir, ls, lesson-9-before  
**On screen:** Terminal, continuing. The vally eval command over four lines: the loading eval file, both models, --runs 2 --workers 2, --output-dir results/lesson-9-before. A jump cut; then the end of the output: the list of failures (one line, an ERROR), the model summary and the table, held until read. The screen is cleared out of sight; ls results/lesson-9-before shows one folder named with a time.  
**Renderer:** terminal (tapes/s16.tape)

> Now the first measurement, with the description as it stands.  _(finishes before typed:1)_
> Six stimuli, two models and two trials each: it spends twenty-four short agent runs.  _(finishes before enter:1)_
> We're watching the list of failures at the end, and the summary under it.  _(finishes before enter:1)_
> About two minutes later, that list has a single line: an error on terra, where a session dropped.  _(waits for output:1; depends on what the demo produced)_
> That trial has no verdict, and it says nothing about loading.  _(waits for output:1; depends on what the demo produced)_
> A loading failure would appear here with evidence that a required skill was not called, Vally's third word for loading; this run has none.  _(waits for output:1; depends on what the demo produced)_
> So the table shows six of six stimuli passing on haiku, and five of six on terra.  _(4s to read after; waits for output:1; depends on what the demo produced)_
> Vally saved the run under results.  _(finishes before typed:2)_
> That folder holds the report.  _(1s to read after; waits for output:2)_

## s17

**Role:** practice · **Mode:** use · **Stage:** test-then-fix  
**On screen:** Headline 'Which skills loaded'. Two tables side by side, one per model, with the note 'eval-results.md · three of its twelve columns': Stimulus, Skills, Pass Rate, six rows each, from the report of the run just made. The three skip- rows' Skills cells light in both tables; then the load- rows' cells.  
**Renderer:** html (scenes/s17.html)

> Here's the Skills column from that report, beside the pass rate, for each model.
> For the three skip stimuli, it names a neighbour or shows a dash, on both models.  _(3s to read after; depends on what the demo produced)_
> So our skill stayed out of every near-miss request.  _(depends on what the demo produced)_
> And for the three load stimuli, it shows our skill loading in both trials, on both models.  _(3s to read after; depends on what the demo produced)_

## s17b

**Role:** practice · **Mode:** use · **Stage:** test-then-fix  
**On screen:** Headline 'An earlier run found one'. Above, three rows from an earlier run's report for claude-haiku-4.5 (Stimulus, Skills, Pass Rate): load-no-keyword shows changelog-entry once and 1/2. Below, two lines of that run's console output in a dark box: the failure on load-no-keyword and its evidence, 'The following required skills were not called: changelog-entry · trial 1'. The 1/2 row lights, then 'were not called'.  
**Renderer:** html (scenes/s17b.html)

> An earlier run of this same test, with the same one-line description, did find a miss.
> On haiku, load no keyword loaded the skill in only one of its two trials.
> In the other, the evidence says the required skill was not called.
> So the one-line description can miss a request that never says changelog, even though our run didn't catch it doing so.  _(2s to read after)_

## s18

**Role:** practice · **Mode:** use · **Stage:** test-then-fix  
**On screen:** Headline 'One line becomes five'. A file panel labelled 'changelog-entry/SKILL.md', with a minimap, showing the top of the edited skill: the description now runs over five lines. Under it, three labels: 'what it does · when to use it · what it's not for'. Each part of the description lights together with its label as it is said.  
**Renderer:** html (scenes/s18.html)

> That one line says what the skill does, and nothing about when.
> Here's the rewrite, which replaces that one line.
> Its first sentence still says what the skill does.
> Then comes the situation: a change, fix or merged pull request to note for the next release, even if the request doesn't say changelog.
> And last, what it's not for: commit messages, release notes, or questions about past versions.
> Nothing else in the skill changes.

## s19

**Role:** practice · **Mode:** use · **Stage:** test-then-fix · **Introduces:** lesson-9-after  
**On screen:** Terminal, continuing in the practice folder. The same vally eval command, with --output-dir results/lesson-9-after. A jump cut; then the end of the output: the list of failures (one line: skip-question on gpt-5.6-terra, failing 'skill-invocation forbids changelog-ent…'), the model summary and the table, held until read.  
**Renderer:** terminal (tapes/s19.tape)

> With the new description in place, we run the same command, saving to a second folder.  _(finishes before typed:1)_
> That's another twenty-four agent runs.  _(finishes before enter:1)_
> This time every trial finished, and the list has one line of a different kind.  _(waits for output:1; depends on what the demo produced)_
> On terra, skip question failed the grader that forbids our skill, in one of its two trials.  _(depends on what the demo produced)_
> So the skill loaded for a near-miss request, which is the second way to fail.  _(4s to read after; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** test-then-fix  
**On screen:** The comparison table from before, now filled from the two runs: for each stimulus and model, the trials that passed before and after, with '1 error' beside the one count where a trial did not finish. The terra cells for skip-question light: '2 of 2', then '1 of 2'.  
**Renderer:** html (scenes/s20.html)

> Now the comparison, stimulus by stimulus: the trials that passed before the rewrite, and after it.
> On terra, skip question went from two of two to one of two.  _(depends on what the demo produced)_
> In every other cell, each trial that finished passed, before and after.  _(4s to read after; depends on what the demo produced)_

## s21 — What the loading test showed

**Role:** body · **Mode:** think · **Stage:** what-the-test-showed  
**On screen:** Headline 'One failure, after the rewrite'. The same filled table. The two 'before' headers light; then the three load- names; then the terra 'after' cell of skip-question, '1 of 2'.  
**Renderer:** html (scenes/s21.html)

> So what did the loading test show?
> In our run, the one-line description did its job in every trial that finished: the skill loaded when it should, and stayed out of every near-miss.  _(depends on what the demo produced)_
> An earlier run caught it missing once, on a request that never says changelog.
> After the rewrite, the skill still loaded in every trial that should load it.  _(depends on what the demo produced)_
> But on terra, it also loaded once for a question about a past version, which the new description says it's not for.  _(depends on what the demo produced)_

## s22

**Role:** body · **Mode:** think · **Stage:** what-the-test-showed  
**On screen:** Headline 'The test is what we keep'. Two blocks: '2 of 2, then 1 of 2 · one stimulus on one model: a small sample' and 'The loading test · one command shows whether the boundary moved'. Each fills as it is said.  
**Renderer:** html (scenes/s22.html)

> One failure in two trials is a small sample, too small to blame the rewrite, and we'll get more careful about samples that small later on.  _(depends on what the demo produced)_
> What we have for certain is the test itself.
> Real projects install dozens of skills, descriptions get edited, and neighbours get added.
> Each of those can change which requests load the skill, and now one command shows whether it did.

## s23

**Role:** recap · **Stage:** what-the-test-showed  
**On screen:** Headline 'Why near-miss requests?'. One block, 'A loading test', which opens after the question and a pause to show its two parts: 'Requests that should load it · catch a skill that stays unused' and 'Near-miss requests · catch a skill that loads where it doesn't belong'. Each part lights as it is said.  
**Renderer:** html (scenes/s23.html)

> Before you go on: why does a loading test need near-miss requests, as well as requests that should load the skill?
> Because a skill can fail in two directions.  _(pause 2.5s first)_
> Requests that should load it catch a skill that stays unused.
> Near-miss requests catch one that loads where it doesn't belong, and obvious requests test neither.

## s24

**Role:** next · **Stage:** what-the-test-showed  
**On screen:** 'Next' and 'Better with the skill?' in the display serif. Below, the hand-off question: 'Is the result any better with the skill than with no skill at all?' A note: 'Exercises are on the lesson page · Source: agentskills.io, Optimizing skill descriptions'.  
**Renderer:** slide (scenes/s24.html)

> You can now show, with a loading eval, what rewriting a description changed on both models.
> As far as this test shows, the skill loads when it should.
> But in one trial of an earlier run, the agent handled the request without loading it.
> Is the result any better with the skill than with no skill at all?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
