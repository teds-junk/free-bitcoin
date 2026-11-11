# Follow-up requests — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0011-follow-up-requests.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** Does the skill still hold when the conversation continues?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through ten lessons of evals on two models, claude-haiku-4.5 and gpt-5.6-terra. Knows skill, agent, model, session, eval file, stimulus, grader, trial, run, workspace and patch; vally lint and vally eval with -e, --model, --runs, --workers and --output-dir; the words PASS, FLAKY, FAIL and ERROR; the results folder with one run folder named by its time; the practice folder with evals and skills in it. Knows an eval file line by line: each stimulus has a prompt and graders, and the agent environment says what the agent starts with. Knows the run's summary, with a tick or a cross for each model and a block above it for any stimulus that did not pass; and the changelog's categories, such as Changed and Fixed. Knows the three diff graders (diff-contains, diff-not-contains, diff-empty), which read the patch of what the agent changed, that a stimulus passes only if every grader passes, and that lint prints one warning saying so; the pattern that matches an added line ending in a pull request reference; a script grader that sees the finished workspace; the skill-invocation grader that reads the agent's events. Knows the skill's rules so far (leave the reference off when no number is given, add nothing for an internal change), that it loads when it should and beats no skill on both models, and that an early draft made up pull request numbers. Every stimulus so far was a single request. Does not know turns:, turn:, or the diffs folder.

1. **what-changes**: after this, the viewer can name the three ways a conversation can go wrong that a single request cannot, and say why each turn's change needs its own grader
2. **turns-and-scoped-graders**: after this, the viewer can predict which change a grader reads from its turn number, and where Vally saves each turn's diff
3. **write-and-run**: after this, the viewer can grade a three-turn conversation turn by turn on both models, read the failing turn's diff, add a rule to the skill and run again
4. **what-it-showed**: after this, the viewer can show whether the skill's rules survive a follow-up, say what leaked between turns, and say what three conversations can support

## s01 — What changes in a conversation

**Role:** hook · **Mode:** think · **Stage:** what-changes  
**On screen:** Headline 'Follow-up requests' in the display serif. Three quote blocks stacked, labelled 'A request', 'Then a second', 'Then a third', holding the three real requests of the conversation this video runs. Each fills as the voice reaches it; nothing is lit when the promise is made.  
**Renderer:** html (scenes/s01.html)

> Nobody uses an agent one request at a time.
> You ask for a changelog entry, then remember a second change, then a third.
> Yet every stimulus we've written starts a fresh conversation, with a single request.
> Here, you'll test a conversation of three requests, and find a mistake that comes from the conversation itself.

## s02

**Role:** body · **Mode:** think · **Stage:** what-changes  
**On screen:** Headline 'What the agent keeps'. A lead: 'A turn is one request in a conversation.' Two blocks side by side, no arrow: 'the workspace · as the last turn left it' and 'its memory · of what was said in earlier turns'. The lead lights when turn is defined, then each block as it is named.  
**Renderer:** html (scenes/s02.html)

> Let's start with what's different when a conversation goes on.
> Each request in a conversation is called a turn.
> Between turns, the agent keeps two things.
> One is the workspace, exactly as the last turn left it.
> Its memory of what was said is the other.
> That memory is a new source of mistakes.

## s03

**Role:** body · **Mode:** think · **Stage:** what-changes  
**On screen:** Headline 'Three new ways to fail'. Three blocks in a row, no arrows: 'A rule fades · later turns follow recent work more than the skill', 'An earlier turn leaks · a detail is carried into a change it has nothing to do with', 'A later turn disturbs earlier work · something already done is rewritten or dropped'. Each fills as it is named.  
**Renderer:** html (scenes/s03.html)

> Three things can now go wrong that can't go wrong in a single request.
> First, a rule fades.
> The skill was loaded at the start, and several turns later the model follows the pattern of its own recent work more than the rules.
> Second, an earlier turn leaks into a later one: a detail from the previous request is carried into a change it has nothing to do with.
> Third, a later turn disturbs earlier work: while adding the third entry, the agent alters or drops the first.

## s04

**Role:** body · **Mode:** think · **Stage:** what-changes  
**On screen:** Headline 'Graded turn by turn'. Two blocks side by side: 'A grader on the final file · can’t say which turn went wrong, and can miss a leak' and 'A grader for each turn · what did this request alone change?'. The first fills, then the second.  
**Renderer:** html (scenes/s04.html)

> So where should a grader look?
> One that reads only the final file can't tell you which turn went wrong, and it can miss a leak entirely.
> So we grade a conversation turn by turn.
> For each request, the question is: what did the agent change in response to that request alone?

## s05

**Role:** body · **Mode:** think · **Stage:** what-changes  
**On screen:** Headline 'A script, not a user'. Two blocks side by side: 'A script of requests · sent in order, whatever the agent replied · what Vally sends' and 'A user who answers back · Vally doesn’t play one'. A note: 'Vally docs, Writing Eval Specs, Multi-turn conversations'. The first fills, then the second.  
**Renderer:** html (scenes/s05.html)

> There's one limit to know before designing a conversation.
> Vally sends the follow-up requests you wrote, in order, whatever the agent replied.
> It doesn't play a user who reacts, and its documentation describes no way to make it do so.
> So we can test how the skill copes with a script of requests, but not with a user who answers back.

## s06 — Turns and scoped graders

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders · **Introduces:** conversation.eval.yaml, turns:  
**On screen:** File panel labelled 'conversation.eval.yaml' with a minimap, opened at the stimulus: 'lines hidden' row for 1–12, then '- name: three-requests', 'turns:' and the first requests. 'turns:' lights when it is named, then the three '- |' lines together as a list of requests.  
**Renderer:** html (scenes/s06.html)

> That's the idea; here's how an eval file expresses it.
> A stimulus can have turns in place of prompt, and turns is a list of requests.
> Vally sends the first, waits for the agent to finish, then sends the second to the same session, and so on.
> However many turns it has, one conversation is one trial.

## s07

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders  
**On screen:** The same panel, opening where the last scene left it. The first request lights ('PR 64 is merged…'); the panel scrolls to the second ('One more, PR 65: I renamed some internal helper functions…') and it lights; then the third ('I also fixed the exit code of `notes export`…').  
**Renderer:** html (scenes/s07.html)

> This conversation is already in our practice folder, and each of its three requests leans on a different rule of the skill.
> Its first request names a merged pull request, sixty-four, so the entry should cite it.
> Next comes an internal change, and by the skill's rule the right response is to add nothing.
> Last is a fix with no pull request number, arriving just after two requests that had one.

## s08

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders · **Introduces:** turn:  
**On screen:** Headline 'Each turn, its own diff'. Three blocks in a row, no arrows: 'turn: 0 · first request · its own diff', 'turn: 1 · second request · its own diff', 'turn: 2 · third request · its own diff'. Under them one block across the full width: 'no turn: · the whole conversation’s diff'. The row lights as a grader is scoped, 'turn: 2' when it is named, then the wide block.  
**Renderer:** html (scenes/s08.html)

> Next, the graders.
> You can limit a grader to one turn by adding turn and a number.
> Vally's documentation calls such a grader scoped to a turn.
> Turns are numbered from zero.
> So a diff grader with turn two sees only what the agent changed during the third request.
> With no turn, a grader sees the whole conversation, as before.

## s09

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders  
**On screen:** Headline 'Not every grader can be scoped'. A table of three rows: grader, what it reads, 'turn:'. 'diff-contains, diff-not-contains, diff-empty · the patch of what the agent changed · yes'; 'skill-invocation · the agent’s events · yes'; 'a script grader · the workspace at the very end · no'. Each row's last cell lights as it is named.  
**Renderer:** html (scenes/s09.html)

> Not every grader can be limited this way.
> All three diff graders can.
> So can graders that look at the agent's events, such as skill invocation.
> But a script grader can't, because it sees only the workspace as it is at the very end.

## s10

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders  
**On screen:** File panel labelled 'conversation.eval.yaml' (the file with its graders added), with a minimap and notes on the right, opened at 'graders:' on line 26. 'turn: 0' lights with the note 'beside type and name'; then the first grader's pattern with 'turn 0 must add a line citing (#64)'; then 'turn: 1' under diff-empty with 'turn 1 must change nothing'.  
**Renderer:** html (scenes/s10.html)

> Here are the graders we'll add under the turns.
> Each turn key sits beside type and name, not nested with the pattern.
> In turn zero, the agent must add a line that cites pull request sixty-four.
> In turn one, it must change nothing, so that grader is diff empty.

## s11

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders  
**On screen:** The same panel, scrolled on to lines 35–48. 'value: "notes export"' lights with the note 'turn 2 must add this entry'; then the diff-not-contains pattern with 'and no line citing a pull request'; the panel scrolls to the end and 'name: first-entry-survives' lights with 'no turn: the whole conversation'.  
**Renderer:** html (scenes/s11.html)

> There are two graders on turn two.
> One says the agent must add an entry that mentions notes export.
> Its partner says the agent must add no line that cites any pull request, with the pattern that caught the made-up number before.
> Our last grader has no turn, so it reads the whole conversation: by the end, the first entry must still be there.

## s12

**Role:** body · **Mode:** works · **Stage:** turns-and-scoped-graders · **Introduces:** diffs  
**On screen:** Headline 'One diff per turn'. Dark code box, left: a short tree, 'results/lesson-11/', the run folder, 'diffs/', and one file name ending '__trial-1__turn-2.diff'. Right, level with each: 'inside the run folder', 'one file per turn of every trial', 'trial and turn, both from 0'. 'diffs/' lights, then the end of the file name.  
**Renderer:** html (scenes/s12.html)

> One more thing before we run it.
> Vally saves a diff for every turn of every trial, in a folder named diffs inside the run folder.
> Each file's name ends with its trial and turn numbers, both counted from zero.

## s13 — Run the conversation

**Role:** practice · **Mode:** use · **Stage:** write-and-run  
**On screen:** Headline 'Which turn goes wrong?'. Three blocks in a row, one per turn, each with what the request is and what its graders want: 'turn 0 · PR 64, a change in behaviour · add an entry citing (#64)', 'turn 1 · PR 65, an internal rename · add nothing', 'turn 2 · a fix, no number given · add an entry, cite nothing'. Nothing is marked; the row lights once at the question and clears.  
**Renderer:** html (scenes/s13.html)

> That's how it works; now let's run it.
> First we add the graders, then run the conversation three times on each model, and then open the diff of any turn that fails.
> Which of the three turns would you expect to go wrong?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s14

**Role:** practice · **Mode:** use · **Stage:** write-and-run · **Introduces:** vally lint, vally eval, -e, --model, --runs, --workers, --output-dir, lesson-11  
**On screen:** Terminal in the practice folder; the prompt shows only the current folder name. vally lint on the conversation eval file prints one warning and no errors. The screen is cleared out of sight; the vally eval command over four lines, with --runs 3 --workers 2 and --output-dir results/lesson-11; a jump cut; then the Failures block for the model that did not pass every conversation, and the model summary, held until read.  
**Renderer:** terminal (tapes/s14.tape)

> With the five graders in the eval file, we lint it first, since that costs nothing.  _(finishes before typed:1)_
> One warning, the reminder that every grader must pass, and no errors.  _(2s to read after; waits for output:1; depends on what the demo produced)_
> Now the run: the conversation, three times on each model, with two workers.  _(finishes before typed:2)_
> This run spends six agent runs of three requests each.  _(finishes before enter:2)_
> We're watching for a block above the summary, which appears for any model that didn't pass all three conversations.  _(finishes before enter:2)_
> About a minute later, there is one, for haiku: one of its three conversations failed.  _(waits for output:2; depends on what the demo produced)_
> Its failing grader, third no made-up number, names the turn and the problem, and points at trial two.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> Every other grader passed on both models, so terra passed all three conversations.  _(2s to read after; waits for output:2; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** write-and-run · **Introduces:** ls, cd, cat, 2026  
**On screen:** Terminal, continuing in the practice folder. ls results/lesson-11 shows one folder named with a time; cd into it; the screen is cleared out of sight; cat of the one diff file whose name ends with the failing trial and turn-2 prints a short patch, held until it has been read.  
**Renderer:** terminal (tapes/s15.tape)

> So let's read what that turn changed, starting in the results folder.  _(finishes before typed:1)_
> There's one run folder, and we change into it.  _(waits for output:1; finishes before typed:2)_
> That summary counted from one and file names count from zero, so its trial two is the file named trial one, turn two.  _(waits for done:2; finishes before typed:3; depends on what the demo produced)_
> That star stands for the start of the file's long name.  _(finishes before enter:3)_
> It's a short patch, holding only what that one turn changed.  _(3s to read after; waits for output:3)_
> It adds one entry under a Fixed heading, and the entry ends with pull request sixty-six.  _(4s to read after; waits for output:3; depends on what the demo produced)_
> But the third request gave no number: the two requests before it gave sixty-four and sixty-five.  _(2s to read after; waits for output:3; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** write-and-run · **Introduces:** SKILL.md, changelog-entry/SKILL.md  
**On screen:** Headline 'One more rule'. File panel labelled 'changelog-entry/SKILL.md' with a minimap, opened at the end of the file: a 'lines hidden' row, then the last two rules. The three lines of the new rule, 29 to 31, light together.  
**Renderer:** html (scenes/s16.html)

> That gap is in the skill, so that's where we fix it.
> We add one more rule at the end: treat every request on its own.
> By this rule, a pull request number belongs only to the change it was given with, and is never carried over from an earlier request.

## s17

**Role:** practice · **Mode:** use · **Stage:** write-and-run · **Introduces:** lesson-11-after  
**On screen:** Terminal in the practice folder. The same vally eval command over four lines, now with --output-dir results/lesson-11-after; a jump cut; then the model summary, held until it has been read.  
**Renderer:** terminal (tapes/s17.tape)

> Then we run the same conversations again, saving to a second folder.  _(finishes before typed:1)_
> That's another six agent runs.  _(finishes before enter:1)_
> This time there's a tick for each model, and no block above the summary: all six conversations passed.  _(3s to read after; waits for output:1; depends on what the demo produced)_

## s18 — What the conversation showed

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'One invented, one leaked'. Top, two quote blocks side by side: 'Turn 1 · the second request' ('One more, PR 65: I renamed some internal helper functions. Add that too.') and 'Turn 2 · the third request' ('I also fixed the exit code of `notes export` when the disk is full. Record that as well.'). Below, a dark box 'What turn 2 added · claude-haiku-4.5' with two real added lines from saved diffs, identical but for the reference: one ending '(#66)', one ending '(#65)'. Notes on the right, level with each: 'our run: a number nobody gave' and 'an earlier run: the second request’s number'. '(#66)' lights; then '(#65)'; then '(#65)' and 'PR 65' in the second request together.  
**Renderer:** html (scenes/s18.html)

> So what did the conversation show?
> Here's the line that the failing turn added, under the two requests before it.
> Sixty-six is a number nobody gave: it simply follows sixty-four and sixty-five.  _(depends on what the demo produced)_
> In an earlier run of this same conversation, that turn cited sixty-five instead.  _(depends on what the demo produced)_
> Sixty-five is a real number: it belongs to the internal rename, which the agent had correctly left out of the changelog a moment before.  _(depends on what the demo produced)_
> So there, the number wasn't invented: it leaked from one turn into the next, and attached itself to a different change.  _(depends on what the demo produced)_

## s19

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'The final file looks fine'. A card 'CHANGELOG.md · Unreleased, at the end of that conversation' with the real lines from the saved diff in a dark box: '### Changed', the notes delete entry citing (#64), '### Fixed', the notes export entry citing (#66). Right, level with the last line: 'tidy, well-formed, a plausible reference'. The last entry lights when the final file is mentioned.  
**Renderer:** html (scenes/s19.html)

> This happened on haiku, which hadn't made up a number in any of our single-request runs; a test of those alone would have called it safe on this point.  _(depends on what the demo produced)_
> Reading only the final file, a grader would have seen this: a tidy, well-formed entry with a plausible reference.  _(2s to read after)_

## s20

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'Before the rule, and after'. Two groups side by side, 'before the rule' and 'after the rule'; each has a row of three boxes per model, one box per conversation, a tick or a cross from our runs. Before: claude-haiku-4.5 has a tick, a cross and a tick, gpt-5.6-terra three ticks. After: three ticks for each. The before group lights, then the after group, then both haiku rows on 'small sample'.  
**Renderer:** html (scenes/s20.html)

> Before the new rule, one of haiku's three conversations failed; after it, all six passed.  _(depends on what the demo produced)_
> One failure in three becoming none in three is, once again, a small sample.

## s21

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'What no pattern can decide'. Two blocks side by side: 'Is this the right category? · no grader here asks' and 'Is it written for the people who use the tool? · the question left open earlier'. A lead under them: 'Both are judgements about meaning.' Each block fills as its question is asked.  
**Renderer:** html (scenes/s21.html)

> There's something these graders didn't check, and we're leaving it alone.
> None of them asks whether an entry is filed under the right category.
> That's a judgement about meaning.
> So is a question we left open earlier: is an entry written for the people who use the tool?
> No pattern can decide either one.

## s22

**Role:** recap · **Stage:** what-it-showed  
**On screen:** Headline 'Three ways a conversation fails?'. One block, 'a conversation, not a single request'. After the question and a pause it opens into three parts, each lit as it is said: 'A rule fades', 'An earlier turn leaks into a later one', 'A later turn disturbs earlier work'.  
**Renderer:** html (scenes/s22.html)

> Before you go on: what are the three ways a conversation can go wrong that a single request can't?
> One: a rule fades.  _(pause 2.5s first)_
> Two: an earlier turn leaks into a later one.
> Three: a later turn disturbs earlier work.

## s23

**Role:** next · **Stage:** what-it-showed  
**On screen:** 'Next' eyebrow and 'A judge for what code cannot check' in the display serif. Below, the hand-off: '“Written for the people who use the tool” is not a pattern. How do you grade that?' A note: 'Exercises are on the lesson page · Source: Vally docs, Writing Eval Specs, Multi-turn conversations'.  
**Renderer:** slide (scenes/s23.html)

> You can now show, turn by turn and on both models, whether the skill's rules survive a follow-up, and fix what doesn't.
> Everything graded so far is structure that code can see.
> Written for the people who use the tool is not a pattern.
> So how do you grade that?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
