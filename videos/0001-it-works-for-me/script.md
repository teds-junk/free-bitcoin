# It works for me — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0001-it-works-for-me.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** My skill works when I try it. Does it do the same thing on another model?  
**The viewer starts:** A professional programmer who has written a skill for an AI agent, or is about to, and has tried it by hand; knows the shell. Has the course folder, a GitHub Copilot sign-in, and Node and Vally installed from the course home's Before you start. Has never run Vally, written an eval, or read a patch.

1. **skill-is-advice**: after this, the viewer can point to the gaps in a skill that each model must fill with its own guess
2. **one-run**: after this, the viewer can name, in order, the four things Vally does in one run, and the three parts of a vally eval command
3. **read-a-patch**: after this, the viewer can read a patch and say which lines the agent added
4. **run-two-models**: after this, the viewer can run one request on two models and open each saved patch
5. **what-it-shows**: after this, the viewer can find, in the files Vally saved, that two models changed the file differently

## s01 — Will it work on another model?

**Role:** hook · **Mode:** think · **Stage:** skill-is-advice  
**On screen:** Headline 'It works for me.' in the display serif, with 'me' in blue italic. Left: the request in a quote box. Right: two cards, 'Your run, on claude-haiku-4.5' and 'A teammate's run, on gpt-5.6-terra', each showing the changelog entry that model really wrote. The request lights, then each card as it is mentioned, then '(#42)' at the end of the second entry.  
**Renderer:** html (scenes/s01.html)

> Imagine you wrote a skill, tried it once, and the agent did what you wanted.
> Then a teammate runs it on another model and gets something different, and neither of you can say which result is normal.
> Here, you'll run an experiment on two models, and find the differences in their behavior.

## s03 — A skill is advice

**Role:** body · **Mode:** think · **Stage:** skill-is-advice · **Introduces:** skill, agent, model, claude-haiku-4.5, gpt-5.6-terra  
**On screen:** Three blocks in a row, no arrows: skill, agent, model (with the two model names). Each block fills with colour as it is defined; at the end skill, then model.  
**Renderer:** html (scenes/s03.html)

> Let's start with what a skill is.
> It's a folder with a file called SKILL dot M D in it: a name, a one-line description, and instructions.
> An agent is a program that uses a language model to do a task with tools: it reads files, edits them, and runs commands.
> The model is the part that decides what to do, and the same agent can run on different models.
> So a skill isn't code that runs the same way every time.
> It's advice, and each model reads it its own way.

## s04

**Role:** body · **Mode:** think · **Stage:** skill-is-advice · **Introduces:** changelog, CHANGELOG.md, notes-cli/CHANGELOG.md, pull request  
**On screen:** File panel on the real changelog, labelled notes-cli/CHANGELOG.md, lines 1-16, with a minimap that is a miniature of the file. Highlights in turn: '## [Unreleased]' (line 5), '### Added' (line 7), the entry on line 8, then '(#41)'.  
**Renderer:** html (scenes/s04.html)

> The skill this course improves is about one small chore: keeping a changelog.
> A changelog lists what changed in each version of a tool, for the people who use it.
> Changes that haven't shipped yet go under a heading called Unreleased.
> They're grouped into categories such as Added and Fixed, one line per entry.
> And an entry often ends with a reference like this one: the number of the pull request that made the change.
> A pull request is a numbered proposal to change a project's code.

## s05

**Role:** body · **Mode:** think · **Stage:** skill-is-advice · **Introduces:** SKILL.md, changelog-entry/SKILL.md  
**On screen:** File panel on the real skill, labelled changelog-entry/SKILL.md, all 13 lines; it scrolls to lines 10-13. 'in the right category' (line 10) lights and the note level with it, 'Which categories exist?', lights with it; then 'Reference the pull request.' (line 12) and its note, 'In what form? What if there isn't one?'. Only one is lit at a time.  
**Renderer:** html (scenes/s05.html)

> Here's the skill.
> It tells an agent how to add an entry to a changelog, and it's a plain first draft, the kind you write in five minutes.
> Let's read it the way a model has to.
> Add the entry in the right category.
> Which categories exist?
> Reference the pull request.
> In what form, and what if there isn't one?
> The skill doesn't say, so each model fills the gap with its own guess.

## s06

**Role:** body · **Mode:** think · **Stage:** skill-is-advice  
**On screen:** A grid: rows 'your model', 'another model', 'a third model'; columns run 1-5. Only the first cell has a tick; the rest are '?'. The tick lights, then the other models' cells, then the other runs of your model.  
**Renderer:** html (scenes/s06.html)

> When you try the skill by hand, you see one model's guess, once.
> That's one observation, and it tells you little about the next model, or the next request.
> To see more than that, you need a tool that runs the agent for you and keeps a record.

## s07 — What one Vally run does

**Role:** body · **Mode:** works · **Stage:** one-run · **Introduces:** Vally, eval  
**On screen:** Two definition blocks side by side: Vally (a command-line tool that runs the GitHub Copilot agent for you and keeps a record) and eval (a repeatable test: same request, same starting folder, checked the same way). Each fills with colour as it is defined.  
**Renderer:** html (scenes/s07.html)

> That's the problem.
> Now here's how Vally works.
> Vally is a command-line tool that runs an agent in a controlled way and keeps a record of what it did.
> The agent it runs is the one that comes with GitHub Copilot, which is why this course needs a Copilot account.
> What it runs is an eval: a repeatable test of an agent, with the same request, in the same starting folder, checked the same way every time.

## s07b

**Role:** body · **Mode:** works · **Stage:** one-run · **Introduces:** workspace  
**On screen:** Four numbered blocks in a row, no arrows: 1 workspace, 2 agent + model, 3 patch, 4 check, each with what Vally does in that step. A highlight moves to each as it is named; then the line under them, 'Once for each model you name, in a new workspace every time.'  
**Renderer:** html (scenes/s07b.html)

> First, Vally makes a fresh scratch folder, called the workspace, and copies in the starting files and the skill.
> Second, it starts an agent on the model you named, and gives it the request.
> Third, when the agent stops, it saves a record of what the agent changed.
> And fourth, it runs the check, and prints a tick or a cross.
> Every run gets a new workspace, so no run can see what another one did.
> What's inside the check, we'll explain later.

## s08

**Role:** body · **Mode:** works · **Stage:** one-run · **Introduces:** vally eval, -e, --model, --output-dir, evals/one-request.eval.yaml, one-request.eval.yaml  
**On screen:** Dark code box, left: the command from the page over three lines. Right, level with each flag: 'which eval file to run', 'which models to run it on', 'where to save the results'. Each flag and its note light in turn. Under them, the request from the eval file in a quote box.  
**Renderer:** html (scenes/s08.html)

> The command that does all this is vally eval, and we're going to start by giving it three things.
> Dash e, followed by the eval file to run.
> The course comes with one, holding a single request.
> It says: I fixed the typo in the help text for notes add.
> Put that in the changelog.
> Dash dash model, followed by one model name, or several separated by commas.
> With several, Vally does the whole run once for each.
> And dash dash output dir, followed by the folder to save the results in.

## s08b

**Role:** body · **Mode:** works · **Stage:** one-run · **Introduces:** ERROR, session  
**On screen:** Three rows: Writes: only inside results/lesson-1. Spends: one short agent session for each model, from your Copilot plan. ERROR: the run didn't finish, usually a dropped connection, so run it again.  
**Renderer:** html (scenes/s08b.html)

> It writes only inside that results folder, but each run is one short session with the agent, and that spends requests from your Copilot plan.
> If the connection drops, Vally prints ERROR for that model.
> That says nothing about the skill, so you'd just run the command again.

## s09

**Role:** body · **Mode:** works · **Stage:** one-run · **Introduces:** list-my-models, models  
**On screen:** Dark code box, left: the command with --model list-my-models, then the first lines of the real error. Right, level with them: 'a name no account has' beside list-my-models, and 'the names your account does have' beside 'Available models: …'.  
**Renderer:** html (scenes/s09.html)

> One more thing we'll use in a moment: model names differ from account to account.
> If you name a model your account doesn't have, Vally stops before starting any agent, and prints the names you do have.
> So a made-up name is a free way to see your list.

## s10 — Reading a patch

**Role:** body · **Mode:** works · **Stage:** read-a-patch · **Introduces:** patch, workspace.patch, lesson-1, 2026, typo-fix  
**On screen:** Dark code box, left: the saved path as a tree, one folder per line (results/lesson-1, the timestamp, one-request, typo-fix, claude-haiku-4.5, 0, workspace.patch). Right, level with each line: what it is. A highlight moves down the lines as each is named.  
**Renderer:** html (scenes/s10.html)

> Step three, the record of what the agent changed, is a patch: a text file that records a change to other files as lines added and lines removed.
> Vally writes one for every run, and names it workspace dot patch.
> It saves each command's results in a folder named with the time the command started.
> Inside that, the patch sits under the eval's name, then the request's name, then the model, then a run number that starts at zero.

## s11

**Role:** body · **Mode:** works · **Stage:** read-a-patch  
**On screen:** File panel on a real workspace.patch from claude-haiku-4.5 (14 lines), added lines in green. Highlights in turn: line 1 'CHANGELOG.md'; the '@@ -7,6 +7,9 @@' header; the context lines starting with a space; the '+' lines.  
**Renderer:** html (scenes/s11.html)

> Here's a real one, from the run you're about to see.
> The first line names the file that changed.
> The next three repeat it in other forms, and you can skip them.
> This line says where the change is: starting at line seven.
> The rest of that line you can skip.
> A line that begins with a space was already there, and hasn't changed.
> It's context, so you can see where the change sits.
> A line that begins with a plus was added by the agent.
> A minus would mean one it removed, and this patch has none.
> So this model added a Fixed heading and one entry under Unreleased, and touched nothing else.
> You can read exactly what an agent did to a file without opening the file.

## s12 — Run it on two models

**Role:** practice · **Mode:** use · **Stage:** run-two-models  
**On screen:** Two quote boxes: the request, and 'The skill says: Reference the pull request.' Under them: 'Neither names a pull request number. What will each model write?' A two-second beat after the question.  
**Renderer:** html (scenes/s12.html)

> That's everything you need.
> If you tried it yourself, here's what you'd see.
> Both models get the same skill, the same changelog, and the same request, and the request doesn't mention a pull request.
> So what would you expect each model to do about reference the pull request?  _(2s to read after)_

## s13

**Role:** practice · **Mode:** use · **Stage:** run-two-models · **Introduces:** node, vally --version, practice-starter, --version, -R  
**On screen:** Terminal; the prompt shows only the current folder name: node --version, vally --version, cp -R practice-starter practice, cd practice.  
**Renderer:** terminal (tapes/s13.tape)

> First, we check the tools: node twenty-two point fifteen or later, and Vally zero point twenty-one.  _(finishes before typed:1)_
> Then we copy the starter that ships with the course into a new practice folder, and change into it.  _(waits for done:2; finishes before typed:3)_
> Every checkpoint in the course starts there.  _(waits for done:4)_

## s14

**Role:** practice · **Mode:** use · **Stage:** run-two-models  
**On screen:** Terminal: the list-my-models command over three lines, then its error with the list of available models. The Saved line reads ~/src/demo/practice/results/models/…  
**Renderer:** terminal (tapes/s14.tape)

> Next, we list the models, using the made-up name.  _(finishes before typed:1)_
> It starts no agent and spends nothing.  _(finishes before enter:1)_
> There's the list, inside the error.  _(waits for output:1+1)_
> Yours will differ.
> We'll use claude haiku four point five and G P T five point six terra.  _(1s to read after)_

## s15

**Role:** practice · **Mode:** use · **Stage:** run-two-models  
**On screen:** Terminal: the vally eval command over three lines with both models; jump cut; the model summary with a tick for each, held until it has been read. Then ls results/lesson-1 showing one timestamped folder; cd into it; cd one-request/typo-fix; ls showing the two model folders.  
**Renderer:** terminal (tapes/s15.tape)

> Now the real run, on both models.
> You'd put your own two model names in place of these.  _(finishes before typed:1)_
> This one spends two short agent runs from your plan.
> We're watching for a tick or a cross next to each model.  _(finishes before enter:1)_
> About twenty seconds later, there's a tick for each model.  _(waits for output:1; depends on what the demo produced)_
> The Saved line at the bottom says where the results went.  _(3s to read after)_
> So let's look in that results folder.  _(finishes before typed:2)_
> There's one folder in it, named with the time of the run.  _(waits for output:2)_
> We change into it, then into the folders for the eval and the request, and list what's there.  _(finishes before typed:3)_
> One folder for each model.  _(waits for output:5)_

## s16

**Role:** practice · **Mode:** use · **Stage:** run-two-models  
**On screen:** Terminal: cat claude-haiku-4.5/0/workspace.patch, held to be read; the screen is cleared out of sight; cat gpt-5.6-terra/0/workspace.patch, held to be read; then cd ../../../../..  
**Renderer:** terminal (tapes/s16.tape)

> Here's the patch from the first model.  _(finishes before typed:1)_
> The zero in the path is its first run.  _(waits for typed:1; finishes before enter:1)_
> The lines that begin with a plus are what it added.  _(3s to read after; waits for output:1)_
> And here's the patch from the second model.  _(finishes before typed:2)_
> Its entry ends differently from the first model's.  _(4s to read after; waits for output:2; depends on what the demo produced)_
> Then we change back up to the practice folder.  _(finishes before typed:3)_

## s17 — What the two patches show

**Role:** body · **Mode:** think · **Stage:** what-it-shows  
**On screen:** The two entries from the opening come back as the real patches, side by side, labelled by model, added lines in green. The end of each entry lights: nothing after `notes add` on the left, '(#42)' on the right. Then '(#41)' in the line above, in both.  
**Renderer:** html (scenes/s17.html)

> So what did that show?
> Both models got a tick.  _(depends on what the demo produced)_
> One wrote an entry with no pull request number.  _(depends on what the demo produced)_
> The other ended its entry with pull request forty-two.  _(depends on what the demo produced)_
> Nobody mentioned a pull request forty-two.
> The entry above it is forty-one, and the model made up the next number.
> In our runs, terra usually made up a number, and haiku usually didn't.
> Your two models may differ in another way, or agree.
> Either way, it's evidence about your skill that would be difficult to discover for every model if you were trying by hand.

## s18

**Role:** recap · **Stage:** what-it-shows  
**On screen:** A block labelled 'one run'; after the question and a pause it opens to show four numbered parts, each a verb: 1 Makes a workspace, 2 Runs an agent, 3 Saves a patch, 4 Runs the check. Each lights as it is said.  
**Renderer:** html (scenes/s18.html)

> Before you go on: what are the four things Vally does in one run, in order?
> It makes a fresh workspace, with the starting files and the skill.  _(pause 2.5s first)_
> It runs an agent on the model you named, and gives it the request.
> It saves a patch of what the agent changed.
> Then it runs the check.

## s19

**Role:** next · **Stage:** what-it-shows  
**On screen:** 'Next: What the tick checked' in the display serif. Below, the hand-off question. A note: 'Exercises are on the lesson page · Source: Vally docs, Run Your First Eval'.  
**Renderer:** slide (scenes/s19.html)

> In this rudimentary eval, both models got a green tick, yet they did different things.
> So what did the tick check?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
