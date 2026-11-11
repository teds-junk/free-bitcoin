# Is the agent better with the skill — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: /Users/ted/src/learn/vally/lessons/0010-is-the-agent-better-with-the-skill.html  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** Are the results better with the skill than without it?  
**The viewer starts:** A professional programmer who knows the shell and has followed the changelog-entry skill through nine lessons. Knows skill, agent, model, eval, eval file, workspace, patch, stimulus, grader, trial, the agent environment and its skills list, the eval file's defaults, the results folder (the report eval-results.md, results.jsonl, a folder per trial holding workspace.patch), the practice folder where all the course's files live, the vally eval command with --model, --workers and --output-dir, vally lint, token usage, and that a baseline is what a result is compared against. Knows the changelog eval: five stimuli (typo-fix, refactor, security, two-changes, after-release) with their graders, which the edited skill now mostly passes on both models, claude-haiku-4.5 and gpt-5.6-terra. Remembers that with the first-draft skill gpt-5.6-terra ended its typo-fix entry with a made-up pull request number, and that a rule added to the skill stopped it. Has always run with the skill installed, and has never seen an experiment file, a variant, vally experiment run, --dry-run or report.md.

1. **beat-no-skill**: after this, the viewer can name the three answers a with-and-without comparison can give for a stimulus, and say what the baseline is
2. **experiment-file**: after this, the viewer can read an experiment file and predict which variants run, what they may differ in, and what the run prints and saves
3. **run-it**: after this, the viewer can run four variants and read, from the table and the failures above it, which stimuli the skill made the difference on
4. **what-it-showed**: after this, the viewer can say in one sentence where the skill helps, where it makes no difference, and what it changes in tokens

## s01 — Does the skill beat no skill?

**Role:** hook · **Mode:** think · **Stage:** beat-no-skill  
**On screen:** Headline 'Better with the skill?' in the display serif. Two blocks side by side, no arrow: 'With the skill · measured in every run so far' and 'With no skill · never run'. The first fills when the earlier versions are mentioned, the second on 'nothing'.  
**Renderer:** html (scenes/s01.html)

> Models already know what a changelog is.
> So perhaps they'd pass our graders with no skill at all, and the skill is decoration.
> Or perhaps the skill matters a great deal.
> So far, we've measured the skill against earlier versions of itself, but not against no skill.
> Here, you'll run the same stimuli with the skill and without it, and say where the skill earns its place.

## s02

**Role:** body · **Mode:** think · **Stage:** beat-no-skill  
**On screen:** Headline 'A skill costs something'. Three blocks in a row, each filled as it is named: 'More text to read · on every request', 'Upkeep · it has to be maintained', 'Mistakes · a skill can be wrong'.  
**Renderer:** html (scenes/s02.html)

> Let's start with what a skill costs.
> It adds to the text the model reads on every request.
> It has to be maintained, and it can be wrong.
> So it earns its place only on requests where the agent does better with it than without.

## s03

**Role:** body · **Mode:** think · **Stage:** beat-no-skill  
**On screen:** Headline 'Skills don't always help'. Three blocks: 'About +17 points · share of tasks completed, on average, with skills written with care', '13 of 87 tasks · made worse by those same skills', 'Lower · with skills the models wrote for themselves'. A note: 'Source: SkillsBench, version 4, 2026 · a preprint · one benchmark of 87 tasks'. Each block fills as its figure is said.  
**Renderer:** html (scenes/s03.html)

> We can't assume that it does.
> One study from twenty twenty-six ran the same eighty-seven tasks with skills and without.
> Skills written with care raised the share of tasks completed by about seventeen percentage points, on average.
> Yet they made thirteen of the eighty-seven tasks worse.
> And skills that the models wrote for themselves completed fewer tasks than no skills at all.

## s04

**Role:** body · **Mode:** think · **Stage:** beat-no-skill  
**On screen:** Headline 'Change one thing'. Two blocks side by side: 'No skill installed · the baseline' and 'The skill installed'. Under them one wide block: 'Same stimuli · same graders · same model'. The wide block fills first, then the two skill blocks together as the one difference, then the baseline block alone.  
**Renderer:** html (scenes/s04.html)

> The way to find out is a fair comparison.
> It keeps the same stimuli, the same graders and the same model, and changes one thing: whether the skill is installed.
> Here the baseline, the thing a result is compared against, is the run with no skill.

## s05

**Role:** body · **Mode:** think · **Stage:** beat-no-skill  
**On screen:** Headline 'Three possible answers'. Three rows, labelled 'an illustration: one stimulus on one model'. Each row has two boxes under the column heads 'without' and 'with', then its answer: cross, tick, 'the skill helps'; tick, tick, 'no difference'; tick, cross, 'the skill hurts'. Each row lights as it is said.  
**Renderer:** html (scenes/s05.html)

> For each stimulus, the comparison gives one of three answers.
> The skill helps: the stimulus fails without it, and passes with it.
> The skill makes no difference: the model manages either way, so the skill isn't earning anything there.
> Or the skill hurts: the stimulus passes without it, and fails with it.
> All three are worth knowing.

## s06 — An experiment file

**Role:** body · **Mode:** works · **Stage:** experiment-file · **Introduces:** experiment file, variant, with-and-without.experiment.yaml  
**On screen:** File panel labelled 'with-and-without.experiment.yaml', with a minimap, open at the top of the file: name, evals, vary, baseline and the first variant. Callouts on the right, level with their lines. The 'changelog.eval.yaml' line lights with its note 'the eval file to run'.  
**Renderer:** html (scenes/s06.html)

> That's the idea; here's the file that expresses it.
> An experiment file lists variants of an eval, and one command runs them all.
> Each variant is one version of the set-up being compared: the same eval, run with one setting changed.
> Our practice folder came with one, for comparing with and without the skill.
> Its evals line names the eval file to run: the changelog eval, whose stimuli and graders are used unchanged in every variant.

## s07

**Role:** body · **Mode:** works · **Stage:** experiment-file  
**On screen:** The same panel, in the same place. The vary line lights with its note 'what variants may differ in'; then, under the panel, the message 'Experiment drift detected' in a mono note; then the baseline line with its note 'the one the others are compared with'.  
**Renderer:** html (scenes/s07.html)

> Next, the vary line lists the settings that variants are allowed to differ in.
> Each is written as a path into the eval's settings: one for the list of skills in the agent environment, and one for the model.
> If a variant differed in anything else, Vally would refuse to run, and report experiment drift.
> That's what keeps the comparison fair.
> Then the baseline line names the variant that the others are compared with.

## s08

**Role:** body · **Mode:** works · **Stage:** experiment-file  
**On screen:** The same panel, scrolled to the variants. 'haiku-no-skill' lights ('a name we choose'), then its model line ('replaces the eval file's default'), then 'skills: []' ('an empty list: no skill installed'), then the skills line of haiku-with-skill ('the skill, as in the eval file'). The panel scrolls on to the two terra variants.  
**Renderer:** html (scenes/s08.html)

> After that come the variants, each under a name we choose.
> The first, haiku no skill, sets its model under overrides, and overrides replace the eval file's defaults.
> Its list of skills is empty, so no skill is installed.
> Haiku with skill keeps the same model, and installs the changelog entry skill, as the eval file does.
> Two more variants do the same for terra.
> So an experiment sets the model in the file, and not with the dash dash model flag.

## s09

**Role:** body · **Mode:** works · **Stage:** experiment-file · **Introduces:** vally experiment run, --dry-run, --workers, --output-dir, vally experiment, lesson-10  
**On screen:** Headline 'One command runs them all'. Dark code box, left: the two commands we are about to run, the dry run over two lines and the real run over three. Right, level with each part: 'runs every variant in the file', 'print the plan, start no agent', 'as with vally eval'. 'vally experiment run' lights, then '--dry-run', then '--workers 2 --output-dir results/lesson-10'.  
**Renderer:** html (scenes/s09.html)

> The command is vally experiment run, followed by the experiment file.
> Adding dash dash dry run makes it print the plan, one block per variant, without starting an agent.
> That's the experiment's version of lint.
> For the real run, it takes dash dash workers and dash dash output dir, as vally eval does.

## s10

**Role:** body · **Mode:** works · **Stage:** experiment-file  
**On screen:** Headline 'One column per variant'. An empty table: a column for each of the four variants, named as Vally prints them; rows 'stimuli', 'tokens', 'trial time'. The column heads light, then each row label as it is named. The cells stay empty. A note under the table: 'above the table: a block for each stimulus that failed'; it lights on the last sentence.  
**Renderer:** html (scenes/s10.html)

> When the run finishes, it prints a table with one column per variant, and the baseline's column is labelled.
> Its first row counts the stimuli that passed.
> Beneath that are each variant's total tokens over all its trials, and its trial time.
> Above the table, it prints a block for each stimulus that failed, naming its variant, the stimulus, and the grader.

## s11

**Role:** body · **Mode:** works · **Stage:** experiment-file · **Introduces:** report.md  
**On screen:** Headline 'One folder per variant'. Dark code box, left: a tree of the run's folder: report.md, then haiku-no-skill/ holding results.jsonl and changelog/, then the other three variant folders. Right, level with each: 'one report for the whole experiment', 'named after the variant', 'its own results', 'the eval's folder, laid out as before'. The four variant folders light, then results.jsonl and changelog/, then report.md. A last line, '…', with the note 'and a few files of Vally's own'.  
**Renderer:** html (scenes/s11.html)

> The run's folder gets one subfolder per variant, named after it.
> Each has its own results dot jsonl, and a folder for the eval, laid out like the ones we already know.
> There's also one report for the whole experiment, report dot md, with a heading and a table for each variant.
> An experiment writes it in place of a single eval's report.

## s12 — Four variants, one table

**Role:** practice · **Mode:** use · **Stage:** run-it · **Introduces:** typo-fix  
**On screen:** Headline 'Which pass with no skill?'. A table of the changelog eval's five stimuli: the name in mono and what the request is: typo-fix · a typo fix, with no pull request number; refactor · a cleanup that users can't see; security · a security fix; two-changes · two changes in one pull request; after-release · a changelog with no Unreleased section. Each row lights as it is named; then nothing is lit during the question.  
**Renderer:** html (scenes/s12.html)

> That's how it works; now let's run it.
> The changelog eval's stimuli are the typo fix with no pull request number, the refactor, and the security fix.
> Then come the two changes in one pull request, and the changelog with no Unreleased section.
> Which of them would you expect a model to get right with no skill at all?  _(2s to read after)_
> If you tried it yourself, here's what you'd see.

## s13

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Terminal in the practice folder; the prompt shows only the folder name. vally experiment run with the experiment file and --dry-run, over two lines. The plan prints: a block for each variant with its eval, file and model. It is longer than the screen, so the last blocks are what stay in view, held until they have been read.  
**Renderer:** terminal (tapes/s13.tape)

> Our experiment file already names the two models we use, so nothing needs editing.  _(finishes before typed:1)_
> First comes the dry run, which checks the plan and starts no agent.  _(finishes before enter:1)_
> It prints a block for each of the four variants, naming its model; the screen holds the last of them.  _(4s to read after; waits for output:1)_

## s14

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Terminal, same folder. vally experiment run over three lines, with --workers 2 and --output-dir results/lesson-10; a jump cut; then the end of the output: the last failure blocks, the line naming the experiment, and the table with a column per variant and its stimuli, tokens and trial time rows, held until it has been read.  
**Renderer:** terminal (tapes/s14.tape)

> Now the real run, with two workers and a folder for the results.  _(finishes before typed:1)_
> It spends twenty short agent runs: each of the four variants runs the five stimuli once.  _(finishes before enter:1)_
> What we're after is the table at the end.  _(finishes before enter:1)_
> About a minute and a half later, the table is there, with the last of the failed stimuli above it.  _(4s to read after; waits for output:1; depends on what the demo produced)_

## s15

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'The table, filled in'. The table from before, in the same place, now filled from our run: stimuli 2/5, 5/5, 3/5, 5/5; tokens and trial time beneath. The two no-skill cells of the stimuli row light, then the two with-skill cells.  
**Renderer:** html (scenes/s15.html)

> Here's that table again, as a slide.  _(2s to read after)_
> With no skill, haiku passes two of the five stimuli, and terra passes three.  _(depends on what the demo produced)_
> With the skill, each passes all five.  _(2s to read after; depends on what the demo produced)_

## s16

**Role:** practice · **Mode:** use · **Stage:** run-it  
**On screen:** Headline 'Which stimuli failed'. A table built from the failure blocks our run printed: variant, stimulus, the grader that failed. Five rows: haiku-no-skill · after-release · entry-in-new-unreleased; haiku-no-skill · refactor · adds-nothing; haiku-no-skill · security · under-security; terra-no-skill · refactor · adds-nothing; terra-no-skill · security · under-security. The variant column lights, then the two refactor rows, then the two security rows, then the after-release row.  
**Renderer:** html (scenes/s16.html)

> Now for the blocks above the table.
> Our run printed five, and every one is in a no-skill variant.  _(3s to read after; depends on what the demo produced)_
> Without the skill, both models wrote an entry for the refactor, where nothing should be added.  _(depends on what the demo produced)_
> Both also filed the security fix under Fixed, when it belongs under Security.  _(depends on what the demo produced)_
> Haiku, with no skill, also failed the changelog with no Unreleased section.  _(2s to read after; depends on what the demo produced)_

## s17

**Role:** practice · **Mode:** use · **Stage:** run-it · **Introduces:** ls, cd, cat, workspace.patch, 2026  
**On screen:** Terminal, same folder. ls results/lesson-10 shows one folder named with a time; cd into it; cd terra-no-skill/changelog/typo-fix; the screen is cleared out of sight; cat gpt-5.6-terra/0/workspace.patch shows the patch, held until it has been read.  
**Renderer:** terminal (tapes/s17.tape)

> The typo fix is where a model once made up a pull request number, so let's read what one wrote for it with no skill.  _(finishes before typed:1)_
> As before, the run's folder is named with its time, and we change into it.  _(waits for output:1; finishes before typed:2)_
> Each variant's folder is named after the variant, so we go into terra no skill, then the eval, then the typo fix stimulus.  _(waits for done:2; finishes before typed:3)_
> Here's the patch from that model's one trial.  _(waits for done:3+1; finishes before typed:4)_
> It adds an entry for the typo, and the entry ends with no pull request number.  _(6s to read after; waits for output:4; depends on what the demo produced)_

## s18 — What the comparison showed

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'Where the skill helps'. A grid from our run: a row for each of the five stimuli, a column for each variant, one tick or cross per cell. The two with-skill columns light, then the no-skill columns, then the refactor and security rows, then typo-fix and two-changes, then after-release.  
**Renderer:** html (scenes/s18.html)

> So, are the results better with the skill?
> In our run, yes: five of five with the skill on both models, against two of five for haiku and three of five for terra without.  _(depends on what the demo produced)_
> The skill earns its place on the refactor and the security fix.  _(depends on what the demo produced)_
> On the typo fix and the two changes, both models managed without it.  _(depends on what the demo produced)_
> The changelog with no Unreleased section split them: terra handled it alone, and haiku didn't.  _(2s to read after; depends on what the demo produced)_

## s19

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'The first draft caused it'. Three cards stacked, each a label over a dark box: 'gpt-5.6-terra · first-draft skill' with the entry it wrote then, ending '(#42)'; 'gpt-5.6-terra · no skill' with the entry from the patch we just read; 'the first draft's rule' with the line '- Reference the pull request.' '(#42)' lights, then the no-skill card, then the rule.  
**Renderer:** html (scenes/s19.html)

> Now, back to that patch of the typo fix.
> With the first-draft skill, this same model ended its entry with a made-up pull request number, in five trials of five.
> With no skill installed, it made nothing up in its one trial, and neither did the other model.  _(depends on what the demo produced)_
> So the made-up number wasn't that model's own weakness.
> Our first draft caused it.
> It said to reference the pull request, with no word on what to do when there is none, and that pushed a model into making one up.

## s20

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'A skill made it worse'. The three rows of answers from earlier, in the same place; the third row, 'the skill hurts', lights and stays lit. Under them a line: 'the typo fix, with the first-draft skill'.  
**Renderer:** html (scenes/s20.html)

> That's the third kind of answer: the first draft made this result worse than no skill at all.
> We fixed it earlier, without knowing its cause.
> It took a comparison with no skill to show that cause.
> That's a good reason to run one before trusting any skill, and again after any large edit.

## s21

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'What it changes in tokens'. A table from our run's tokens row: rows claude-haiku-4.5 and gpt-5.6-terra; columns 'tokens, no skill' and 'tokens, with the skill': 374.6k, 329.7k; 289.6k, 281.6k. A note: 'total over five trials, one per stimulus'. Each row's pair lights as it is read out.  
**Renderer:** html (scenes/s21.html)

> Then there are the tokens.
> A skill adds text for the model to read.
> Yet in our run, both models used fewer tokens with it than without.  _(depends on what the demo produced)_
> On haiku, that's about three hundred thirty thousand with the skill, against about three hundred seventy-five thousand without.  _(depends on what the demo produced)_
> On terra, it's about two hundred eighty-two thousand, against about two hundred ninety thousand.  _(depends on what the demo produced)_
> Each figure covers five trials: too few to say the skill saves tokens, but enough to see that it doesn't cost many.  _(depends on what the demo produced)_

## s22

**Role:** body · **Mode:** think · **Stage:** what-it-showed  
**On screen:** Headline 'One trial per cell'. The grid of stimuli and variants again, in the same place, with the note 'each cell is one trial'. The refactor and security rows light, then the one cell where haiku with no skill failed after-release.  
**Renderer:** html (scenes/s22.html)

> One caution about those ticks and crosses: each is one trial of one stimulus, so small differences deserve care.
> When a stimulus fails without the skill on every model, that's solid evidence.
> When a single cell differs, as haiku's did on the changelog with no Unreleased section, that's a reason to run more trials.

## s23

**Role:** recap · **Stage:** what-it-showed  
**On screen:** Headline 'What are the three answers?'. One block, 'one stimulus, with and without the skill', which opens after the question and a pause into three parts, each lit as it is said: 'helps · fails without, passes with', 'no difference · the same either way', 'hurts · passes without, fails with'.  
**Renderer:** html (scenes/s23.html)

> Before you go on: what three answers can a with-and-without comparison give for a stimulus?
> The skill helps: the stimulus fails without it, and passes with it.  _(pause 2.5s first)_
> The skill makes no difference: the result is the same either way.
> Or the skill hurts: the stimulus passes without it, and fails with it.

## s24

**Role:** next · **Stage:** what-it-showed  
**On screen:** 'Next: Follow-up requests' in the display serif. Below, the hand-off question: 'Does the skill still hold when the conversation continues?' A note: 'Exercises are on the lesson page · Source: Vally docs, Run Your First Experiment'.  
**Renderer:** slide (scenes/s24.html)

> You can now say where a skill helps, where it makes no difference, and what it changes in tokens.
> But every stimulus so far was one request.
> Real use goes on: someone asks for a follow-up, or changes their mind.
> Does the skill still hold?
> That's the next lesson.
> The exercises on the lesson page are worth doing first.
