# Bridges — narration script

<!-- Generated from storyboard.json by lint-storyboard.js. Edit storyboard.json, not this file.
     Free-form notes (sources, open questions) go between the notes markers and are kept. -->

Source: —  
Voice: am_echo @ 1.2x

<!-- notes -->

<!-- /notes -->

## The story

**The question this video answers:** What does the viewer have after each part, and why does the next one follow?  
**The viewer starts:** Has just watched one part of the course.

1. **skill**: after this, the viewer can say what they can now do with the skill and what question leads on
2. **app**: after this, the viewer can carry the same questions over to the skill inside an app

## s01

**Role:** bridge · **Stage:** skill  
**On screen:** 'What did the tick check?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s01.html)

> Both models got a green tick, yet they did different things.
> So what did that tick actually check?

## s02

**Role:** bridge · **Stage:** skill  
**On screen:** 'Would it happen again?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s02.html)

> We can now read everything a run left behind.
> But each model ran only once: would it do the same thing next time?

## s03

**Role:** bridge · **Stage:** skill  
**On screen:** 'What else goes wrong?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s03.html)

> So far we've counted one problem, on one tidy request, by reading ten patches.
> What else goes wrong when the requests get messier?

## s04

**Role:** bridge · **Stage:** skill  
**On screen:** 'Can code do the reading?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s04.html)

> We found those failures by reading.
> After every edit to the skill, we'd have to read them all again, so can code do the reading?

## s05

**Role:** bridge · **Stage:** skill  
**On screen:** 'Where can a script live?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s05.html)

> Patterns now catch the failures we named.
> But checking that nothing else in the file changed is not a pattern: it needs a script, kept where the agent can't read or edit it.

## s06

**Role:** bridge · **Stage:** skill  
**On screen:** 'How do we test a grader?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s06.html)

> A hidden script now decides pass and fail, and only we can see whether it's right.
> So how do we test a grader?

## s07

**Role:** bridge · **Stage:** skill  
**On screen:** 'Graders against real answers' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s07.html)

> That test tried one correct answer for each grader, and it couldn't test the graders that check for absence.
> But we have dozens of real answers saved, good and bad: can the graders run on those?

## s08

**Role:** bridge · **Stage:** skill  
**On screen:** 'Does the skill load?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s08.html)

> Our graders are now tested against correct answers, untouched files, and real bad answers.
> In every trial so far the skill was there to use: will it load for other wordings, and stay out of requests that aren't its job?

## s09

**Role:** bridge · **Stage:** skill  
**On screen:** 'Better with the skill?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s09.html)

> We know when the skill loads.
> But is the result any better with the skill than with no skill at all?

## s10

**Role:** bridge · **Stage:** skill  
**On screen:** 'What about a follow-up?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s10.html)

> Every stimulus so far has been a single request.
> Real use goes on: someone asks for a follow-up.

## s11

**Role:** bridge · **Stage:** skill  
**On screen:** 'What code can't check' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s11.html)

> Everything we've graded so far is structure that code can see.
> Whether an entry is written for the people who use the tool is not a pattern, so it needs another kind of grader.

## s12

**Role:** bridge · **Stage:** skill  
**On screen:** 'Is the judge right?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s12.html)

> The judge said yes for some trials and no for others.
> It's a model too, so is it right?

## s13

**Role:** bridge · **Stage:** skill  
**On screen:** 'Can a grader give partial credit?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s13.html)

> We've measured the judge against our own labels.
> But some entries it refused were nearly right and some were far off, and a yes or no can't tell them apart: can a grader give partial credit without hiding a failure?

## s14

**Role:** bridge · **Stage:** skill  
**On screen:** 'Is the change real?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s14.html)

> Scores and counts both move after an edit.
> If seven of ten becomes nine of ten, is that real?

## s15

**Role:** bridge · **Stage:** skill  
**On screen:** 'What does a pass cost?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s15.html)

> We can now say what a before-and-after result supports.
> That same table also printed tokens for each variant, and they differ by model: so what does a passing trial cost?

## s16

**Role:** bridge · **Stage:** skill  
**On screen:** 'A model of your own' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s16.html)

> We can price the models a Copilot account offers.
> An app may call a model through a service of its own, or one the team runs: can Vally run that model too, and what does a passing trial cost there?

## s17

**Role:** bridge · **Stage:** skill  
**On screen:** 'A ceiling on a trial' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s17.html)

> We can now price any model, including one we run ourselves, where a single trial took minutes.
> One trial that loops can cost or take many times the typical one, so how do we fail, or stop, a trial that takes too much?

## s18

**Role:** bridge · **Stage:** skill  
**On screen:** 'No worse than before?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s18.html)

> Budgets now guard every trial.
> Before relying on an edit, we want a check that says no worse than before: can Vally decide that?

## s19

**Role:** bridge · **Stage:** skill  
**On screen:** 'Where do we look first?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s19.html)

> There are many moving parts now, and runs sometimes end in error, or fail for reasons that aren't the skill.
> When a run goes wrong, where do we look first?

## s20

**Role:** bridge · **Stage:** skill  
**On screen:** 'Make it a routine' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s20.html)

> We can measure, gate and debug.
> What's left is to make it a routine that a teammate can repeat.

## s21

**Role:** bridge · **Stage:** app  
**On screen:** 'The skill inside an app' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s21.html)

> That completes the checks on the skill by itself.
> Now a team has put the skill inside their release tooling: does it still hold when an app, not a person, starts the agent?

## s22

**Role:** bridge · **Stage:** app  
**On screen:** 'How did it get there?' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s22.html)

> The hidden test sees only the finished changelog.
> In an app, how the agent got there matters too: did it read the list, and did it try to commit or push?

## s23

**Role:** bridge · **Stage:** app  
**On screen:** 'When a tool fails' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s23.html)

> In real use, the tracker or the network sometimes fails.
> Does the agent cope, and can we test that without breaking anything?

## s24

**Role:** bridge · **Stage:** app  
**On screen:** 'A run Vally didn't start' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s24.html)

> All of this ran inside Vally.
> The app also runs by itself, and keeps its own record of what it did: can Vally grade a run it didn't start?

## s25

**Role:** bridge · **Stage:** app  
**On screen:** 'Let Vally run the app' in the display serif, alone on the page.  
**Renderer:** slide (scenes/s25.html)

> Grading afterwards gives one sample for each run, on whatever model the app used.
> To get trials, experiments and other models, Vally has to start the app itself.
