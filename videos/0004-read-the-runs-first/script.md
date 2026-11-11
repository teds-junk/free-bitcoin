# Read the runs before writing graders — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0004-read-the-runs-first.html  
Voice: am_echo @ 1.2x

<!-- notes -->
Production notes (not narrated).
- Sources: Husain and Shankar, AI Evals FAQ (reissued 2026-09-18); Shankar et al., Who Validates the Validators? (2024); Keep a Changelog 1.1.0. No person is named in the narration.
- The cold read was done by the authoring agent itself, not by a fresh reader (the worker could not launch one).
- src/run/ is a stand-in from verified/lesson-04 until s12 is recorded (see src/run/PROVISIONAL). Every outcome sentence in s12 to s22, the notes beside each trial (NOTES in build-src/make-scenes.py) and src/state/notes/failures.md describe that stand-in run and must be checked against the video's own run.
- Left out from the page's checkpoint: step 9 (cd back to the practice folder) and the empty-patch advice in step 7 (no patch was empty). The other ten patches are shown side by side in scenes, not printed one by one.
- The notes file is made in a text editor on the page; s13.tape copies it into practice/notes/ out of sight and s20 shows it in a panel.
<!-- /notes -->

## The story

**The question this video answers:** What else goes wrong when the requests get messier?  
**The viewer starts:** A professional programmer who knows the shell and has watched three Vally runs of one changelog request (a typo fix) with the first-draft changelog-entry skill, on claude-haiku-4.5 and gpt-5.6-terra. Knows skill, agent, model, eval, eval file, workspace, patch and workspace.patch; Vally's words stimulus, grader, trial and run; the agent environment (what the agent starts with); vally lint; vally eval with -e, --model, --runs, --workers and --output-dir, and why we use two workers; the results folder (a folder named with the time, then the eval, the stimulus, the model and the trial number); that a pass means no grader objected; PASS, FLAKY, FAIL and ERROR, and that ERROR is not a verdict. Has counted how often each model makes up a pull request number on that one request. Has never seen an eval file with more than one stimulus, and does not know --skip-grade, the changelog format's categories, or the words failure mode and error analysis.

1. **read-first**: after this, the viewer can say why graders written before reading any runs miss the failures that matter, and what makes something a failure mode
2. **six-requests**: after this, the viewer can predict what the six-stimulus eval file runs, and say what a tick means when grading is skipped
3. **read-and-name**: after this, the viewer can run six stimuli on two models, write a note for each trial from its patch, and group the notes into failure modes
4. **where-failures-come-from**: after this, the viewer can show a short list of the skill's failure modes, each with the trial that shows it, and name the question the skill left open behind each

## s01 — Why reading comes first

**Role:** hook · **Mode:** think · **Stage:** read-first  
**On screen:** Headline 'Read the runs first' in the display serif. Left: a quote card labelled 'The request so far' with the typo-fix request. Right: three shorter quote cards labelled 'Messier', each a phrase taken from one of the other requests ('Nothing changes for users, it's purely a cleanup.', 'while I was in there I fixed the bug', 'I swapped JSON.parse for a streaming parser'). The left card lights, then each right card as its kind is named.  
**Renderer:** html (scenes/s01.html)

> So far, we know about one problem with our skill, because we happened to look.
> That was on one request, and it's one of the tidier things a person might ask for.
> Real requests mention changes that users can't see, bundle two changes together, or describe a fix by how it was coded.
> Here, you'll run six ordinary requests on two models, read what each one did, and come away with a short list of what goes wrong.

## s02

**Role:** body · **Mode:** think · **Stage:** read-first  
**On screen:** Headline 'Failures come from the models'. Two blocks side by side, no arrow: 'A list written beforehand · comes from your imagination' and 'What a model did · found by reading a run'. Under them, in a dark box, the entry gpt-5.6-terra wrote in the first run we saw, with '(#42)' lit when the made-up number is mentioned.  
**Renderer:** html (scenes/s02.html)

> Let's start with why reading comes before writing graders.
> It's natural to sit down and list what a good changelog entry looks like, then write a grader for each item.
> But that list comes from your imagination, and the failures come from the models.
> You probably wouldn't have thought to check for a made-up pull request number until a model made one up.

## s03

**Role:** body · **Mode:** think · **Stage:** read-first · **Introduces:** error analysis  
**On screen:** Headline 'Discover errors, don't imagine them'. A quote: 'Write evaluators for errors you discover, not errors you imagine.' Below, four numbered blocks in a row, no arrows: 1 Run · realistic requests; 2 Read · what came back; 3 Note · what is off; 4 Group · the notes. Each block fills as its step is said. Note: 'Source: Husain and Shankar, AI Evals FAQ (2026)'.  
**Renderer:** html (scenes/s03.html)

> People who do this for a living put it as a rule: write evaluators for errors you discover, not errors you imagine.
> Evaluators is their word for graders.
> Their process is plain.
> You run realistic requests, go through what came back, write a short note on each, and group the notes.
> They call it error analysis.
> Graders come after the last step, and only for failures you've seen.

## s04

**Role:** body · **Mode:** think · **Stage:** read-first · **Introduces:** failure mode  
**On screen:** Headline 'A failure mode has a name'. A definition block across the width: 'failure mode · a named way the skill's output goes wrong, seen in at least one real trial'. Under it two blocks side by side: 'Records a change users cannot see · a failure mode' and 'Trial 3 looked odd · not one yet'. The definition fills, then each example as it is said.  
**Renderer:** html (scenes/s04.html)

> Each group of notes gets a name, and that makes it a failure mode.
> By failure mode, we mean a named way in which the skill's output goes wrong, seen in at least one real trial.
> Recording a change that users can't see is a failure mode.
> Saying only that trial three looked odd is not one yet.

## s05

**Role:** body · **Mode:** think · **Stage:** read-first  
**On screen:** Headline 'Reading changes what you want'. Two blocks side by side: 'Criteria written beforehand · incomplete' and 'Criteria after reading · include what you saw'. The first fills at the question, the second at 'once you do'. Note: 'Source: Shankar et al., Who Validates the Validators? (2024)'.  
**Renderer:** html (scenes/s05.html)

> Reading does something else that a list can't: it makes you decide what you want.
> Is a security fix filed under Fixed wrong?
> You may not have an opinion until you see one, and once you do, that opinion is a rule the skill is missing.
> Researchers who studied this found that people's criteria shift while they're reading outputs, so criteria written beforehand are incomplete.

## s06

**Role:** body · **Mode:** think · **Stage:** read-first  
**On screen:** Headline 'How many runs are enough?'. Two blocks with large figures: '100 or more · suggested for a real product' and '12 · what we read here'. Under them a lead: 'Stop when new runs stop showing anything new.' The first block fills, then the lead, then the second block.  
**Renderer:** html (scenes/s06.html)

> How many runs are enough?
> Those same practitioners suggest reading at least a hundred for a real product, and stopping when new ones stop showing you anything new.
> Here, we'll read twelve.
> That's enough to find the main failure modes of a five-line skill, and too few to be sure we've found them all.

## s07 — Six ordinary requests

**Role:** body · **Mode:** works · **Stage:** six-requests · **Introduces:** six-requests.eval.yaml, typo-fix, after-release  
**On screen:** Headline 'Six stimuli, no graders'. File panel labelled 'six-requests.eval.yaml' with a minimap, callouts on the right. It opens at the top (name, defaults, the agent environment with the skill), scrolls to the first stimulus (typo-fix, lines 10 to 18), then to the last (after-release, lines 62 to 70), with a 'lines hidden' row between. Lit in turn: 'name: typo-fix' ('the request we know'), the stimulus's own agent_environment ('its starting changelog'), the skills line at the top ('listed once, for all six'), 'fixtures/just-released' ('1.3.0 is out: no Unreleased'). The last sentence clears the highlight.  
**Renderer:** html (scenes/s07.html)

> That's the reasoning; here's the eval file we'll run.
> It's a second eval file from the starter folder, and it holds six stimuli.
> One eval file can hold as many as you like, and Vally runs each of them on each model.
> Stimulus one is the request we already know, so this run can be compared with the earlier ones.
> Each stimulus can have an agent environment of its own, and here, each one names the changelog it starts from.
> Our skill is listed once, at the top, for all of them.
> Down at the end, the last stimulus starts from a different changelog: one where version one point three has just been released, so there's no Unreleased section yet.
> Nowhere in this file is there a grader, and that's allowed.

## s08

**Role:** body · **Mode:** works · **Stage:** six-requests · **Introduces:** refactor, two-changes, security, parser  
**On screen:** Headline 'Four more, each with a gap'. Four quote cards in a two-by-two grid, each labelled with its stimulus name (refactor, two-changes, security, parser) and holding that stimulus's request, word for word from the eval file. Each card lights as its kind is named; the last sentence clears the highlight.  
**Renderer:** html (scenes/s08.html)

> Between those two sit four more.
> First, a refactor: a tidying of the code that changes nothing for users.
> Next, one pull request that contains two changes.
> Then a security fix.
> Last, a fix described by how it was coded.
> Each one leaves the skill something to decide that it doesn't mention.

## s09

**Role:** body · **Mode:** works · **Stage:** six-requests · **Introduces:** Keep a Changelog  
**On screen:** Headline 'The changelog follows a format'. Dark box, left: '## [Unreleased]' and under it the six category headings in order: ### Added, ### Changed, ### Deprecated, ### Removed, ### Fixed, ### Security. Callouts on the right: 'unshipped changes, in square brackets' level with the Unreleased heading, 'six categories, in this order' level with the first category. Below, a quote labelled 'All the skill says about it': 'Add the entry under Unreleased, in the right category.' Note: 'Source: Keep a Changelog 1.1.0'. Each category lights as it is named, then the heading, then the quote.  
**Renderer:** html (scenes/s09.html)

> To judge the results, we need one fact about this changelog.
> It follows a public format called Keep a Changelog.
> That format has six categories, in this order: Added, Changed, Deprecated, Removed, Fixed and Security.
> It writes the heading for unshipped changes as Unreleased, inside square brackets.
> Our skill mentions none of this.

## s10

**Role:** body · **Mode:** works · **Stage:** six-requests · **Introduces:** vally eval, --skip-grade  
**On screen:** Headline 'Run now, grade later'. Dark box, left: the vally eval command over four lines as the lesson prints it, with '--skip-grade' marked. Callouts on the right, level with their lines: 'six stimuli' (the eval file), 'run and save, grade nothing' (--skip-grade). Below, a block: '✓ with --skip-grade · the trial finished; nothing was graded'. The flag lights, then the block.  
**Renderer:** html (scenes/s10.html)

> Because the purpose of this run is to read, the command adds one flag: dash dash skip grade.
> With it, Vally runs the agents and saves everything as usual, and skips grading.
> This file has no graders, so here the flag changes nothing: it states the purpose, and it's what you'd use on a file that has some.
> Vally's summary still prints ticks.
> With skip grade, a tick means only that the trial finished.

## s11 — Read and name

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'Which will it handle badly?'. Left: a card labelled 'The skill's four rules' with the four rule lines of SKILL.md in a dark box. Right: five small blocks in a column, one per case: 'a refactor users cannot see', 'two changes in one pull request', 'a security fix', 'a fix described in code terms', 'no Unreleased section'. Each block fills as it is named in the question; then the highlight clears and the scene holds.  
**Renderer:** html (scenes/s11.html)

> That's the file and the flag; now let's run it and read.
> Each of the six stimuli runs once on each model, which gives us twelve patches to read.
> For every trial we'll write one note, and then group the notes into failure modes.
> Here are the skill's four rules again.
> Which of these would you expect it to handle badly: the refactor users can't see, the two changes in one pull request, the security fix, the fix described in code terms, or the changelog with no Unreleased section?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s12

**Role:** practice · **Mode:** use · **Stage:** read-and-name · **Introduces:** vally lint, ls, -e, --model, --workers, --output-dir, lesson-4, 2026  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. vally lint on the eval file prints that it is valid. Then the vally eval command over four lines, with --skip-grade --workers 2 and --output-dir results/lesson-4; a jump cut; then the model summary, held until it has been read. The screen is cleared out of sight; ls results/lesson-4 shows one folder named with a time.  
**Renderer:** terminal (tapes/s12.tape)

> First, we check the eval file with vally lint, which starts no agent.  _(finishes before typed:1)_
> Lint says the file is valid.  _(waits for output:1)_
> Here's the run: six stimuli on two models, with no grading, and two workers as before.  _(finishes before typed:2)_
> It spends twelve short agent runs.  _(finishes before enter:2)_
> In the summary, we're looking for six of six under each model.  _(finishes before enter:2)_
> About a minute later, both models show six of six: all twelve trials finished, and nothing was graded.  _(3s to read after; waits for output:2; depends on what the demo produced)_
> So let's look in the results folder.  _(finishes before typed:3)_
> There's one folder, named with the time of the run.  _(1s to read after; waits for output:3)_

## s13

**Role:** practice · **Mode:** use · **Stage:** read-and-name · **Introduces:** cd, cat, six, workspace.patch, notes/failures.md, 2026six, failures.md  
**On screen:** Terminal, continuing in the practice folder. cd into the run's folder and its 'six' folder; ls shows six folders, one per stimulus. The screen is cleared out of sight; cat refactor/claude-haiku-4.5/0/workspace.patch shows the patch, held until it has been read.  
**Renderer:** terminal (tapes/s13.tape)

> We change into that folder, and then into the one for the eval, which is named six.  _(finishes before typed:2)_
> Inside is a folder for each stimulus.  _(2s to read after; waits for output:2)_
> Our notes go in a file of their own, named failures, with one line per trial: the stimulus, the model, what the agent did, and anything we think is wrong.  _(finishes before typed:3)_
> Here's the first patch: the refactor, on the haiku model.  _(finishes before typed:3)_
> One question decides the note: would we be happy to see this in our own changelog?  _(4s to read after; waits for output:3)_
> This trial added an entry under Changed, for a change the request said users can't see.  _(3s to read after; waits for output:3; depends on what the demo produced)_

## s14

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'A change users can't see'. Top: a quote labelled 'refactor · the request' with the request from the eval file. Below, a dark box with what each model's patch added (the model name, then the added lines), and on the right a callout level with each model: our note for that trial ('users cannot see this', 'same problem'). Each model's lines light as it is discussed.  
**Renderer:** html (scenes/s14.html)

> Terra's patch for the refactor does the same thing.  _(depends on what the demo produced)_
> So that's one note for each model: it records a change users can't see.  _(3s to read after; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'A number nobody gave'. Same layout: the typo-fix request as a quote; the dark box with each model's added lines; callouts 'fine' (haiku) and 'a number nobody gave it' (terra). '(#42)' lights at the end of terra's entry.  
**Renderer:** html (scenes/s15.html)

> Let's go through the other ten the same way.
> On the request we already know, haiku's entry has no pull request number, and that's fine.  _(depends on what the demo produced)_
> Terra's ends with a number that nobody gave it.  _(2s to read after; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'Two changes, handled well'. Same layout: the two-changes request; each model's added lines (an entry under Added and a new Fixed section with a second entry, both ending (#60)); callouts 'fine' for both. Each model's lines light in turn.  
**Renderer:** html (scenes/s16.html)

> Now the request that looked hardest: two changes in one pull request.
> Both models split it into two entries, one under Added and one under Fixed, and both cite pull request sixty.  _(depends on what the demo produced)_
> Those are fine.  _(2s to read after; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'A security fix, under Fixed'. Same layout: the security request; each model's added lines with '### Fixed' marked; callouts 'under Fixed' for both. Both headings light together.  
**Renderer:** html (scenes/s17.html)

> Both models filed the security fix under Fixed.  _(depends on what the demo produced)_
> But the format has a Security category of its own, so each of these gets a note.  _(2s to read after; depends on what the demo produced)_

## s18

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'How it was coded'. Same layout: the parser request; each model's added lines; callouts 'how it was coded' (haiku) and 'only what users notice: fine' (terra). 'by using streaming JSON parser' lights at the end of haiku's entry, then terra's entry.  
**Renderer:** html (scenes/s18.html)

> For the out-of-memory fix, haiku's entry ends by naming the streaming parser, which is how the fix was coded.  _(depends on what the demo produced)_
> Terra's entry says only what users notice.  _(2s to read after; depends on what the demo produced)_

## s19

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'A heading without brackets'. Same layout: the after-release request; each model's added lines (a new Unreleased heading, an Added section, one entry); callouts 'matches the file: fine' (haiku) and 'no brackets' (terra). '## [Unreleased]' lights, then '## Unreleased'.  
**Renderer:** html (scenes/s19.html)

> Last, the changelog with no Unreleased section.
> Both models added the heading themselves.  _(depends on what the demo produced)_
> Here, haiku wrote it inside square brackets, like every other heading in that file.  _(depends on what the demo produced)_
> Terra left the brackets off.  _(2s to read after; depends on what the demo produced)_

## s20

**Role:** practice · **Mode:** use · **Stage:** read-and-name  
**On screen:** Headline 'Twelve notes, five failure modes'. File panel labelled 'notes/failures.md' with a minimap: the five numbered failure modes at the top of the file, each ending with the trial that shows it; a 'lines hidden' row for the twelve notes below. Each numbered line lights as it is said.  
**Renderer:** html (scenes/s20.html)

> Grouping the notes that describe the same kind of problem gives us a short list, at the top of the notes file.
> It has five failure modes, each with a trial that shows it.  _(depends on what the demo produced)_
> One: there's no rule for a missing pull request number, so a model invents one.  _(depends on what the demo produced)_
> Two: it records a change users can't see.  _(depends on what the demo produced)_
> Three: it files a security fix under Fixed.  _(depends on what the demo produced)_
> Four: it describes how the fix was coded.  _(depends on what the demo produced)_
> Five: a new Unreleased heading doesn't match the other headings in the file.  _(2s to read after; depends on what the demo produced)_
> Looking back at our run, the request that looked hardest was handled well by both models, and the plain-looking refactor was handled badly by both.  _(depends on what the demo produced)_

## s21 — Where the failures come from

**Role:** body · **Mode:** think · **Stage:** where-failures-come-from · **Introduces:** changelog-entry/SKILL.md, SKILL.md  
**On screen:** Headline 'Every failure is a gap'. File panel labelled 'changelog-entry/SKILL.md', scrolled to its four rules (lines 10 to 13), with a minimap. Callouts on the right, one per rule: 'Which categories? What heading?' beside 'Add the entry under Unreleased, in the right category.'; 'Which changes? Ruling out what?' beside 'One line per change, written for people who use the tool.'; 'And with no number?' beside 'Reference the pull request.'. Each rule lights as its question is asked; the highlight clears when the voice turns to the models.  
**Renderer:** html (scenes/s21.html)

> So where do these five come from?
> In every one, the skill left a question open.
> What to do without a pull request number.
> Which changes count, and what it means to write for the tool's users.
> Which categories exist, and what a new heading looks like.
> Neither model disobeyed the skill.
> Each one filled a gap, and they filled it differently.
> That's good news, because a gap in a skill is something we can fix.

## s22

**Role:** body · **Mode:** think · **Stage:** where-failures-come-from  
**On screen:** Headline 'Some of it is taste'. A table of the five failure modes from the top of the notes file: the failure mode, the trial it was seen in, and a third column 'Settled by' that is filled for two rows only: 'the format: a Security category' beside the security row and 'the format: ## [Unreleased]' beside the heading row. The security row lights, then the heading row.  
**Renderer:** html (scenes/s22.html)

> Your list won't match ours exactly, and some entries on it will be matters of taste.
> Deciding which ones you care about is part of the work.
> For two of ours, the project's format settles it: a security fix has its own category, and the heading has square brackets.  _(2s to read after; depends on what the demo produced)_

## s23

**Role:** recap · **Stage:** where-failures-come-from  
**On screen:** Headline 'What are the four steps?'. One block, 'error analysis', which opens after the question and a pause into four numbered parts: 1 Run · realistic requests; 2 Read · what came back; 3 Note · what is wrong; 4 Group · into failure modes. Each part lights as it is said.  
**Renderer:** html (scenes/s23.html)

> Before you go on: what are the four steps of error analysis?
> First, we run realistic requests.  _(pause 2.5s first)_
> Second, we go through what came back.
> Third, we write a note on what's wrong with each.
> Fourth, we group the notes into failure modes, and only then write graders.

## s24

**Role:** next · **Stage:** where-failures-come-from  
**On screen:** 'Next: Turn a failure into a grader' in the display serif. Below, the hand-off question: 'Can code do the reading?' A note: 'Exercises are on the lesson page · Source: Husain and Shankar, AI Evals FAQ (2026)'.  
**Renderer:** slide (scenes/s24.html)

> You can now name what goes wrong with the skill, and point to a trial for each.
> But you found those failures by reading, and after every edit to the skill, you'd have to read them all again.
> Can code do the reading?
> That's the next lesson.
> For practice, the exercises on the lesson page are worth doing first.
