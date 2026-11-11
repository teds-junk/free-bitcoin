"""Write storyboard.json for lesson 15. The storyboard is the source of the script; this file only
keeps its long narration readable. Run:  python3 build-src/make-storyboard.py
The production step may add before / wait_for / read / pause to storyboard.json directly; if it has,
do not run this again without carrying those over."""
import json, pathlib

D = pathlib.Path(__file__).resolve().parent.parent
O = lambda text, **kw: {"text": text, "outcome": True, **kw}
S = lambda text, **kw: {"text": text, **kw}

ST1, ST2, ST3, ST4 = 'small-samples', 'experiment-output', 'before-and-after', 'what-it-supports'

scenes = [
 dict(id='s01', role='hook', mode='think', stage=ST1, chapter='What a small sample can show', renderer='html',
      on_screen="Headline 'Is the change real?' in the display serif. Two blocks side by side: '7 of 10 · before the edit' and '9 of 10 · after the edit'. Under them a note: 'the skill so far: four edits, each judged on a count smaller than these'. The left block lights, then the right, then the note.",
      introduces=[],
      narration=[
       "After an edit to the skill, seven of ten trials passing becomes nine of ten.",
       "That looks like an improvement, but the same model with the same request gives different results from run to run.",
       "So some of that gain may be chance, and we've already edited this skill four times on counts smaller than these.",
       "Here, you'll make one more edit, measure the skill before and after it, and say in one sentence what the result supports."]),
 dict(id='s02', role='body', mode='think', stage=ST1, renderer='html',
      on_screen="Headline 'A count is an estimate'. Left: a block '7 of 10 · 70% passed'. Right: one range bar on a 0 to 100% axis, filled from 40% to 89%, labelled '40% to 89%', with a tick at 70%. Under it a note: 'probably = about 95 times in 100'. The block lights, then the bar, then the note.",
      introduces=[],
      narration=[
       "Let's start with what a count from a few trials can tell us.",
       "When seven of ten trials pass, seventy percent is an estimate.",
       "Ten more trials might give five passes, or nine.",
       "The true pass rate is the one we'd see over a very large number of trials.",
       "All we know is a range for it: probably between forty and eighty-nine percent.",
       "Probably means that a range worked out this way holds the true rate about ninety-five times in a hundred."]),
 dict(id='s03', role='body', mode='think', stage=ST1, renderer='html',
      on_screen="Headline 'Do the ranges overlap?'. Two groups of range bars on one 0 to 100% axis. '10 trials each': 7 of 10 (40% to 89%) above 9 of 10 (60% to 98%), overlapping. '100 trials each': 70 of 100 (60% to 78%) above 90 of 100 (83% to 94%), apart. The first pair lights, then the second.",
      introduces=[],
      narration=[
       "Now back to the edit that took seven of ten to nine of ten.",
       "Here are the two ranges, forty to eighty-nine, and sixty to ninety-eight, and they overlap almost completely.",
       "If the skill's true pass rate were eighty percent both before and after, it could easily produce those two counts.",
       "So this result doesn't show a change.",
       "With the same two rates over a hundred trials each, the ranges don't touch, and that would be evidence."]),
 dict(id='s04', role='body', mode='think', stage=ST1, renderer='html',
      on_screen="Headline 'Three habits for small counts'. Three numbered blocks: 1 'Like with like · same stimuli, graders, model, sitting'; 2 'Counts, not percentages · 100% is 3 of 3, or 300 of 300'; 3 'These trials cannot tell · when the ranges overlap'. Each lights as it is said.",
      introduces=[],
      narration=[
       "Three habits follow from that.",
       "First, we compare like with like: the same stimuli, the same graders and the same model, with both versions run in one sitting.",
       "Second, we report counts, and not only percentages, because one hundred percent could be three of three, or three hundred of three hundred.",
       "Third, when the ranges overlap, we say that these trials cannot tell.",
       "That doesn't mean the edit did nothing; it means we don't know yet, and more trials are how to find out."]),
 dict(id='s05', role='body', mode='think', stage=ST1, renderer='html',
      on_screen="Headline 'Certainty costs trials'. Three range bars on one axis, all at a 70% pass rate: 7 of 10, 28 of 40, 112 of 160, each with its range and its width in points; each is about half as wide as the one above. Bars light from top to bottom.",
      introduces=[],
      narration=[
       "More trials narrow a range, but slowly: it takes about four times the trials to halve its width.",
       "That's the real price of certainty, and the reason to spend trials where a decision depends on them."]),
 dict(id='s06', role='body', mode='think', stage=ST1, renderer='html',
      on_screen="Headline 'A calculator for the range'. One card drawn like the course's range calculator: a 'Before' row with boxes '7' of '10' and the result '70%, range 40% to 89%'; an 'After' row with '9' of '10' and '90%, range 60% to 98%'; beneath, its verdict 'The ranges overlap. This result does not show a change.' A note: 'on the course site · 95% Wilson interval · Source: Evan Miller, Adding Error Bars to Evals (2024)'. The rows light, then the verdict.",
      introduces=['range calculator'],
      narration=[
       "The arithmetic is tedious, so the course has a small calculator for it.",
       "It takes a count before and a count after, and shows the range around each.",
       "Then it says whether the two ranges overlap, which here they do."]),

 dict(id='s07', role='body', mode='works', stage=ST2, chapter='What the experiment prints', renderer='html',
      on_screen="Headline 'Two versions, two models'. File panel labelled 'before-and-after.experiment.yaml' with a minimap, callouts on the right. It opens at the top (the eval it names), moves to 'runs: 3' under overrides, then to the two haiku variants: 'haiku-before' with the skill folder changelog-entry-before, and 'haiku-after' with changelog-entry. Callouts: 'the judged eval · 3 requests', '3 trials of each stimulus', 'the skill before our edit', 'the skill we edit'.",
      introduces=['before-and-after.experiment.yaml', 'changelog-entry-before'],
      shows=['before-and-after.experiment.yaml'],
      narration=[
       "That's how to read a count; here's the experiment that will give us some.",
       "It's an experiment file, which names variants of one eval, and this one comes with the starter folder.",
       "The eval is the one graded by our judge: three requests worded in coding terms.",
       "Runs, set to three under overrides, gives every variant three trials of each stimulus.",
       "Both of our models, haiku and terra, get two variants each.",
       "One uses a copy of the skill as it is before our edit, in a folder named changelog entry before.",
       "Its partner uses the skill itself, which we're about to edit."]),
 dict(id='s08', role='body', mode='works', stage=ST2, renderer='html',
      on_screen="Headline 'A block for every miss'. Dark box, left: blocks from our run's output, each cut to its first two lines: the variant and model, then the state, the stimulus and its trial counts (for example 'haiku-before · claude-haiku-4.5' / 'FAIL  parser  0/3'). Callouts on the right: 'variant · model', 'trials passed and failed', and under the box a note 'no block = every trial passed'.",
      introduces=[],
      narration=[
       "When the experiment runs, each stimulus that wasn't a clean pass gets a block, headed by its variant and model.",
       "With a judge, the block lists the judge's verdict for each trial.",
       O("Here are some from a run of this experiment, cut down to their first two lines."),
       "After the stimulus name comes the count of trials that passed and failed.",
       "A stimulus with no block passed all of its trials, so the blocks are enough to count trials for each variant."]),
 dict(id='s09', role='body', mode='works', stage=ST2, renderer='html',
      on_screen="Headline 'Three columns per stimulus'. A one-row table from the saved report, labelled 'report.md': Stimulus 'cache', Pass Rate '2/3', pass@k '100.0%', pass^k '29.6%'. Under it, three small notes level with the columns: 'passed, out of finished', 'did at least one of k pass?', 'would k in a row all pass? (2/3)³'. Each column's cell lights as it is explained.",
      introduces=['pass@k', 'pass^k', 'report.md'],
      narration=[
       "The saved report, in the experiment's run folder, gives the same counts another way.",
       "When a stimulus runs more than once, its row gains three columns, and in their names, k is the number of trials.",
       O("This row is from the same run: one stimulus, three trials, two of which passed."),
       "Pass rate is the count: trials that passed, out of trials that finished.",
       "Pass at k asks whether at least one of the k trials passed, so it answers: can the agent do this at all?",
       O("Here one did, so it shows one hundred percent."),
       "Pass hat k asks a harder question: how likely is it that k trials in a row would all pass?",
       O("Passing two times in three, three times running, comes to just under thirty percent.")]),
 dict(id='s10', role='body', mode='works', stage=ST2, renderer='html',
      on_screen="Headline 'Which column to trust'. Two blocks side by side for a stimulus that passes 2 times in 3: 'pass@k · 100% · can it do this at all?' and 'pass^k · 29.6% · can I count on it every time?'. Under them two short notes: 'a trial that ends in ERROR: dashes in these columns' and 'no column gives a range'. The right block lights as the answer, then the left, then each note.",
      introduces=[],
      narration=[
       "So which column describes a skill that has to work every time?",
       "Pass hat k does, because a single passing trial is enough to make pass at k show one hundred percent.",
       "If any trial ends in error, the stimulus shows dashes in these columns, and its finished trials are counted in the terminal output only.",
       "None of these columns gives a range, which is what the calculator is for."]),

 dict(id='s11', role='practice', mode='use', stage=ST3, chapter='Compare before and after', renderer='html',
      on_screen="Headline 'One rule, sharpened'. File panel labelled 'changelog-entry/SKILL.md' with a minimap, opened at the skill's rules. The second rule is three lines; its first line ('One line per change, written for people who use the tool:') lights, then the two added lines. Callouts: 'the rule until now', 'added: what they will notice', 'added: what to leave out'.",
      introduces=['SKILL.md'],
      shows=['SKILL.md'],
      narration=[
       "That's what the experiment prints; now let's use it on a real edit.",
       O("Our judge found entries that still say how a fix was coded."),
       "Until now, the skill's second rule only said to write for people who use the tool.",
       "Our edit adds two lines to it: say what they'll notice, and don't say how it was coded.",
       "It also names what to leave out: any library, algorithm, data structure or source file.",
       "To compare fairly, we keep a copy of the skill as it was, beside the edited one."]),
 dict(id='s12', role='practice', mode='use', stage=ST3, renderer='html',
      on_screen="Headline 'What will nine trials show?'. A table with a row per model (claude-haiku-4.5, gpt-5.6-terra) and two empty columns, 'before the edit' and 'after the edit', headed 'trials passed, of 9'. A note: '3 stimuli × 3 trials = 9 trials for each variant'. The note lights, then the empty cells; the scene holds on the question.",
      introduces=[],
      narration=[
       "Each variant runs three stimuli three times, so every count will be out of nine trials.",
       S("What would you expect: will the count go up on both models, and will nine trials be enough to show it?", read=2),
       "If you tried it yourself, here's what you'd see."]),
 dict(id='s13', role='practice', mode='use', stage=ST3, renderer='terminal', visual='tapes/s13.tape',
      on_screen="Terminal in the practice folder; the prompt shows only the folder name. cp -R copies skills/changelog-entry to skills/changelog-entry-before. Out of sight the new rule is put into the skill and the screen is cleared. Then vally experiment run with --dry-run: a block for each variant; the list is longer than the screen and ends on the last two.",
      introduces=['cp', '-R', 'changelog-entry', 'vally experiment', '--dry-run'],
      shows=['cp', 'vally experiment'],
      narration=[
       S("First, we copy the skill folder, so the version before the edit is kept.", before='typed:1'),
       S("With the copy made, the new rule goes into the skill itself, which is an edit to one file.", before='typed:2'),
       S("Before spending anything, a dry run checks the plan.", before='typed:2'),
       S("It starts no agent, and it should list four plans, one for each variant.", before='enter:2'),
       O("It does: the list is longer than the screen, and these are the last of the four.", wait_for='output:2', read=4)]),
 dict(id='s14', role='practice', mode='use', stage=ST3, renderer='terminal', visual='tapes/s14.tape',
      on_screen="Terminal in the practice folder. vally experiment run over three lines, with --workers 2 and --output-dir results/lesson-15; a jump cut; then the end of the output: the last lines of a block, the table with a column for each variant (rows wording, stimuli, tokens, trial time), the run id and the output folder. Held until it has been read.",
      introduces=['--workers', '--output-dir', 'lesson-15'],
      shows=['vally experiment'],
      spend='36 agent runs',
      narration=[
       S("Now the experiment itself: both versions of the skill, on both models, two trials at a time, saved in a results folder of its own.", before='typed:1'),
       S("It spends thirty-six agent runs, and thirty-six calls to the judge.", before='enter:1'),
       S("We're after the table at the end: its stimuli row counts, for each variant, the stimuli that passed in all three trials.", before='enter:1'),
       O("Several minutes later, that row reads one of three, then three of three, for haiku, and zero of three, then three of three, for terra.", wait_for='output:1', read=5),
       O("Terra's zero isn't three failures: each of its stimuli lost a trial to an error, and an unfinished trial has no verdict.", wait_for='output:1', read=2),
       S("Those are counts of stimuli, and a range needs trials.", wait_for='output:1', read=2)]),
 dict(id='s15', role='practice', mode='use', stage=ST3, renderer='html',
      on_screen="Headline 'Count trials, not stimuli'. Dark box, left: every block from our run, cut to its first two lines, grouped by variant. Right: a table 'trials passed' with a row per model and columns 'before the edit' and 'after the edit', filled from the blocks (5 of 9 and 9 of 9; 5 of 6 and 9 of 9), and a note 'no block = 3 of 3 · a trial that ended in ERROR is left out'. Haiku's blocks and cells light, then terra's.",
      introduces=[],
      narration=[
       "Above the table, the output has a block for each stimulus that wasn't a clean pass.",
       "For each variant, we add up the trials that passed over its three stimuli, leaving out any trial that ended in error.",
       O("Haiku passed five of nine before the edit, and nine of nine after."),
       O("Terra passed five of six before, with three trials lost to errors, and nine of nine after.")]),
 dict(id='s16', role='practice', mode='use', stage=ST3, renderer='html',
      on_screen="Headline 'The range around each count'. Two calculator cards side by side, one per model, each with Before and After rows (count, 'of', trials, and the result line with its range) and the calculator's verdict under them, in its own words. Haiku's two result lines light, then its verdict; then terra's.",
      introduces=[],
      narration=[
       "Now the range around each count, from the calculator.",
       O("For haiku, it's twenty-seven to eighty-one percent before, and seventy to one hundred after."),
       O("Those two ranges overlap, by eleven points."),
       O("For terra, it's forty-four to ninety-seven, and seventy to one hundred, which overlap too.")]),
 dict(id='s17', role='practice', mode='use', stage=ST3, renderer='html',
      on_screen="Headline 'One sentence per model'. Two quote cards, one per model, each holding the sentence we wrote: the counts before and after, whether the ranges overlap, and what these trials can and cannot tell. The first lights, then the second.",
      introduces=[],
      narration=[
       "The last step is to say what the result supports, and no more, in one sentence per model.",
       O("For haiku, ours says the judge's passes went from five of nine to nine of nine, and that these trials can't yet tell whether the improvement is real."),
       O("For terra, it says they went from five of six to nine of nine, and that these trials can't tell whether the rule made any difference.")]),

 dict(id='s18', role='body', mode='think', stage=ST4, chapter='The earlier fixes, re-examined', renderer='html',
      on_screen="Headline 'What nine trials can show'. Two blocks side by side, one per model: the count before and after in large type ('3 of 9 → 8 of 9' is written as two counts, 'before' and 'after'), and under each the two ranges as bars on one axis, touching. Haiku's block lights, then terra's, then both clear.",
      introduces=[],
      narration=[
       "So what should we make of those two sentences?",
       O("On haiku, four trials failed before the edit, three of them on one request."),
       O("After the edit, none failed."),
       O("Even so, the two ranges still overlap."),
       O("Nine trials a side are too few to pull them apart, and more trials are the way to find out."),
       O("On terra, only one finished trial failed before the edit, so there was almost nothing left to fix, and nothing these trials could show."),
       "Neither result is a failure of the edit: both are honest statements of what a handful of trials can and can't tell us."]),
 dict(id='s19', role='body', mode='think', stage=ST4, renderer='html',
      on_screen="Headline 'Reasonable, but not measured'. A table of two earlier fixes from our own runs: 'a rule for follow-ups · conversation, haiku' 2 of 3, then 3 of 3; 'a rewritten description · loading, terra' 11 of 11, then 11 of 12; a last column 'ranges' reading 'overlap' for both. Under it three small blocks: 'a patch showed the cause', 'the rule addressed that cause', 'the count moved the right way'. Rows light, then the three blocks in turn.",
      introduces=[],
      narration=[
       "Now let's apply the same honesty to the earlier fixes.",
       O("When we added the rule for follow-up requests, haiku's conversation test went from two of three to three of three."),
       O("When we rewrote the skill's description, the loading test had no failure left to fix: terra passed all eleven trials that finished before, and eleven of twelve after."),
       O("In the calculator, the ranges overlap for both fixes."),
       "So those runs didn't prove that the fixes worked.",
       O("What made the follow-up rule reasonable was something else: a patch showed what caused the failure, the rule addressed exactly that cause, and the result moved the right way."),
       "That's a sound reason to keep a rule, but it isn't the same as having measured it, and it's worth knowing which of the two we have."]),
 dict(id='s20', role='body', mode='think', stage=ST4, renderer='html',
      on_screen="Headline 'A result we can defend'. Top: the made-up-number grader on gpt-5.6-terra, '1 of 3' before and '3 of 3' after, with the two ranges as bars, overlapping. Below, three blocks: '5 of 5 · the same failure, before the fix', 'passing in every run since', 'no skill, no made-up number'. The bars light, then each block.",
      introduces=[],
      narration=[
       O("Even our clearest early fix needs this care: on terra, the grader for made-up numbers went from one of three to three of three, and alone, those ranges overlap widely."),
       O("What makes that result strong is everything around it: five of five trials with the same failure before the fix, and the same stimulus passing in every run since."),
       O("The run with no skill at all showed that the first draft caused it."),
       "Several small results that agree, a cause we can see in a patch, and a comparison with no skill: that's what a result we can defend looks like."]),
 dict(id='s21', role='body', mode='think', stage=ST4, renderer='html',
      on_screen="Headline 'First, trust the grader'. Two numbered blocks: 1 'Test the grader · the oracle, then saved trials'; 2 'Work out the range · count trials, then the calculator'. Under them one line: 'A range around a wrong grader's count measures the wrong thing, carefully.' Block 1 lights, then the line, then block 1 and block 2 in order.",
      introduces=[],
      narration=[
       "One more caution: every count here is only as good as the grader that produced it.",
       "If a grader passes work that's wrong, a range around its count is a careful measurement of the wrong thing.",
       "So we test the graders first, with the oracle and with saved trials, and only then work out a range."]),
 dict(id='s22', role='body', mode='think', stage=ST4, renderer='html',
      on_screen="Headline 'Tokens, in the same table'. Dark box: the experiment's table from our run as printed (the variant names, the stimuli row, the tokens row, the trial time row), with the tokens row marked. Callouts: 'the agent's tokens, over all trials', 'the judge's are not included'. The tokens row lights, then the two haiku cells against the two terra cells.",
      introduces=[],
      narration=[
       "One row of the experiment's table hasn't come up yet.",
       "Beneath the counts are each variant's tokens, added up over all of its trials; they're the agent's tokens, and the judge's aren't included.",
       O("In our run, the two models differ from each other by more than the edit changed either of them."),
       "What that difference costs, for each trial that passes, is a question for later."]),

 dict(id='s23', role='recap', stage=ST4, renderer='html',
      on_screen="Headline 'Is a better count real?'. One block, 'before believing a count', which opens after the question and a pause into four parts: 'Like with like · one experiment, before and after'; 'Count trials · not stimuli or percentages'; 'Find each range · the calculator'; 'Say what it supports · overlap: these trials cannot tell'. Each part lights as it is said.",
      introduces=[],
      narration=[
       "Before you go on: a count goes up after an edit.",
       "What do we do before believing it?",
       S("We compare like with like: the same stimuli, graders and model, before and after, in one experiment.", pause=2.5),
       "We count trials, not stimuli or percentages.",
       "We work out the range around each count.",
       "Finally, if the ranges overlap, we say that these trials can't tell."]),
 dict(id='s24', role='next', stage=ST4, renderer='slide',
      on_screen="'Next: What a passing trial costs' in the display serif. Below, the hand-off: 'The same table printed tokens for each variant.' A note: 'Exercises are on the lesson page · Source: Evan Miller, Adding Error Bars to Evals (2024)'.",
      introduces=[],
      narration=[
       "You can now compare a skill before and after an edit, and say in one sentence what the result supports.",
       "The same table also printed tokens for each variant, and they differ by model.",
       "So what does a passing trial cost?",
       "That's the next lesson.",
       "For practice, the exercises on the lesson page are worth doing first."]),
]

for s in scenes:
    s.setdefault('visual', f"scenes/{s['id']}.html")

order = ['id', 'role', 'mode', 'stage', 'chapter', 'renderer', 'visual', 'on_screen', 'introduces', 'shows', 'narration', 'spend']
scenes = [{k: s[k] for k in order if k in s} for s in scenes]

sb = {
 "schema": 2,
 "title": "Is the change real",
 "slug": "0015-is-the-change-real",
 "kind": "lesson",
 "lesson_number": 15,
 "source": "/Users/ted/src/learn/vally/lessons/0015-is-the-change-real.html",
 "created": "2026-11-11",
 "poster": "s01",
 "people": [],
 "pacing": {"lead_in": 0.4, "gap": 0.5, "tail": 0.8},
 "narrative": {
  "question": "After I edit the skill, is a better count a real improvement or luck?",
  "viewer_starts": "A professional programmer who knows the shell and has followed the changelog-entry skill through fourteen lessons on claude-haiku-4.5 and gpt-5.6-terra. Knows skill, eval file, stimulus, grader, trial, runs and workers; PASS, FLAKY, FAIL and ERROR; that the same model gives different results from run to run; failure modes; graders that read the diff and script graders; the oracle and re-grading saved trials with vally grade; the experiment file, variant and baseline, vally experiment run and its dry run, and the table of variants with tokens beneath; the LLM judge with its rubric, the three requests worded in coding terms that it grades, and its TPR and TNR against our own labels; a judge on a 1 to 5 scale with a threshold. Has seen the skill edited four times, each time judged on a count of two or three trials. Has never put a range around a count, and does not know pass@k or pass^k.",
  "arc": [
   {"stage": ST1, "viewer_can": "say why a count from a few trials is a range, and tell whether the ranges around two counts overlap"},
   {"stage": ST2, "viewer_can": "count trials passed for each variant from an experiment's output, and say what pass at k and pass hat k each answer"},
   {"stage": ST3, "viewer_can": "keep a copy of the skill, edit one rule, run both versions on both models, and find the range around each count"},
   {"stage": ST4, "viewer_can": "state in one sentence what a before-and-after result supports, and tell a fix that was measured from one that was only reasonable"}]},
 "scenes": scenes,
}
(D / 'storyboard.json').write_text(json.dumps(sb, indent=1, ensure_ascii=False) + '\n')
print('storyboard:', len(scenes), 'scenes')
