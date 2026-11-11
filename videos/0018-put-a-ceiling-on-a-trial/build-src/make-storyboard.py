"""Write storyboard.json for lesson 18. The narration lives here so it can be edited as text; run this,
then lint-storyboard.js (which regenerates script.md). Timing fields added later (before, wait_for,
read, pause) should be added HERE, not only in storyboard.json, or the next run of this file drops them.
"""
import json, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
sb = json.loads((D / 'storyboard.json').read_text())
sb.update({"poster": "s01", "people": []})
sb["narrative"] = {
 "question": "How do I fail, or stop, a trial that costs or takes too much?",
 "viewer_starts": "A professional programmer who knows the shell and has followed the changelog-entry skill through seventeen lessons. Knows skill, eval file, stimulus, grader, trial, run, patch, results.jsonl and the trial record with its metrics and token usage. Has written diff graders and a script grader, and knows the every-grader-must-pass rule and lint's scoring-defaults-applied warning. Knows vally lint, vally eval with --model, --workers and --output-dir, and vally grade with -e and --run-dir, including that script graders fail every trial in a re-grade because the workspace is gone. Knows the two ways a grader can be wrong, and the habit of testing a grader on saved trials before paying for agent runs. Knows turns as the requests of a conversation. Has run the cost experiment: four variants (haiku-low, haiku-high, terra-low, terra-high), its report.md with median tokens, turns and duration per stimulus, and cost per passing trial. Knows the timeout in the eval file's defaults. Has never limited what a trial may use, and does not know the budget graders or the constraints block.",
 "arc": [
  {"stage": "a-budget-is-a-grader", "viewer_can": "say what a budget catches, why it is set from measured trials, and why it stays beside a check that the work was done"},
  {"stage": "budget-graders", "viewer_can": "read a budget grader in an eval file and predict which trials it fails"},
  {"stage": "limits-that-stop", "viewer_can": "choose between a budget grader, max_agent_duration and max_duration for a trial that runs too long"},
  {"stage": "set-budgets-from-runs", "viewer_can": "set budgets from measured trials, test them on saved trials in a free re-grade, widen them, add a time limit and run"},
  {"stage": "what-the-limits-caught", "viewer_can": "say why a budget needs room above the typical trial, and what a token budget does not tell you"}
 ]}

def S(id, role, stage, renderer, on_screen, narration, mode=None, chapter=None, introduces=(), shows=None, **kw):
    s = {"id": id, "role": role}
    if mode: s["mode"] = mode
    s["stage"] = stage
    if chapter: s["chapter"] = chapter
    s["renderer"] = renderer
    s["visual"] = f"tapes/{id}.tape" if renderer == 'terminal' else f"scenes/{id}.html"
    s["on_screen"] = on_screen
    s["introduces"] = list(introduces)
    if shows is not None: s["shows"] = list(shows)
    s["narration"] = narration
    s.update(kw)
    return s

def o(text, **kw): return {"text": text, "outcome": True, **kw}
def t(text, **kw): return {"text": text, **kw}

A, B, C, U, W = 'a-budget-is-a-grader', 'budget-graders', 'limits-that-stop', 'set-budgets-from-runs', 'what-the-limits-caught'
sb["scenes"] = [
 S('s01', 'hook', A, 'html', "Headline 'Put a ceiling on a trial' in the display serif. Two blocks side by side: 'Is the work right?' with the names of the graders written so far beneath it, and 'What did it take?' with 'tokens · time · turns · no grader asks'. The first lights, then the second.", [
   "Every grader we've written so far asks whether the work is right.",
   "None of them asks what it took.",
   "If a trial writes the right entry after reading the same file forty times, it passes them all, and we pay for every call.",
   "One trial that loops can cost ten times the usual, and a run every night multiplies whatever slips through.",
   "Here, you'll put limits on what a trial may use, and test each limit on trials you've already saved."],
   mode='think', chapter='A budget is a grader'),
 S('s02', 'body', A, 'html', "Headline 'A budget is a grader'. One definition block, 'budget · a limit on what one trial may use', above four small blocks: tokens, time, turns, tool calls. Each lights as it is named.", [
   "Let's start with what a budget is.",
   "By a budget, we mean a limit on what one trial may use: tokens, time, turns, or tool calls.",
   "Written as a grader, it fails any trial that goes over."], mode='think'),
 S('s03', 'body', A, 'html', "Headline 'Two kinds of trouble'. Two blocks side by side: 'a loop · one trial gone wrong' and 'a cost regression · an edit makes every trial read more, or take longer'. Each lights as it is named.", [
   "It catches two kinds of trouble.",
   "One is a trial that loops: a single run gone wrong.",
   "The second is a cost regression: an edit to the skill after which every trial takes more tokens, or more time.",
   "No grader of the result would notice that."], mode='think'),
 S('s04', 'body', A, 'html', "Headline 'Measure first, then set it'. Three blocks: 'too low · fails good work', 'too high · can never fail', 'measured · set from real trials, tested on a saved run'. Each lights as it is named.", [
   "Guessed budgets tend to be wrong in one of the two ways a grader can be wrong.",
   "Too low, and it fails good work.",
   "Too high, and it can never fail.",
   "So we set it from trials we've measured, and a saved run is a free test of whatever we choose."], mode='think'),
 S('s05', 'body', A, 'html', "Headline 'Not too much, and right'. Two blocks side by side: 'a budget says · not too much' and 'the other graders say · and it was right'. A note under them: 'a trial that gives up after one turn is inside every budget'.", [
   "One more thing: a budget stays beside a check that the work was done.",
   "Giving up after one turn keeps a trial well inside every budget.",
   "So the budget says not too much, and only the other graders say it was right."], mode='think'),

 S('s06', 'body', B, 'html', "Headline 'Four graders, one number each'. File panel labelled 'results.jsonl · one trial's metrics' with hidden-row markers: the lines totalTokens, toolCallCount, turnCount and wallTimeMs of a real trial record. Callouts on the right, level with each line: 'token-budget', 'tool-call-count', 'turn-count', 'wall-time'. Each line lights as its grader is named.", [
   "That's the idea; here are the graders that express it.",
   "Every trial record ends with a metrics block, and four built-in graders each compare one of its numbers with a max.",
   "Token budget counts input and output tokens together.",
   "Turn count counts the model's replies.",
   "Wall time is the agent's working time, by the clock.",
   "Fourth, tool call count counts the tool calls a trial makes."],
   mode='works', chapter='Budget graders', introduces=['token-budget', 'turn-count', 'wall-time', 'tool-call-count', 'results.jsonl', 'results.jsonl · one trial’s metrics']),
 S('s07', 'body', B, 'html', "Headline 'A turn is one reply'. Two blocks side by side: 'a turn in a conversation · one request' and 'a turn in a trial · one reply from the model'. Under them a note: 'one request, several replies · turn-count counts the replies'. The second block lights, then the first, then the note.", [
   "That word, turn, needs some care, because it has had another meaning.",
   "In a conversation, a turn was one request; here, it's one reply from the model inside a single trial.",
   "Even with one request, a trial takes several replies, and turn count counts the replies."], mode='works'),
 S('s08', 'body', B, 'html', "Headline 'Three budgets, no names'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, on the end of the first stimulus's graders: the three budget graders, each with a max; it scrolls two rows to the last one's time and back. Callouts on the right: 'passes at or under max', 'a time has its unit', 'no name: Vally names it from type and limit'.", [
   "Here's how they look in the eval file, at the end of one stimulus's graders.",
   "Each takes one setting, max, and passes when the trial's number is at or under it.",
   "Times are written with their unit.",
   "None of the three has a name, and that's on purpose.",
   "Grader names must be unique across the whole file, and these three go under all five stimuli.",
   "Left unnamed, each one gets a name from its type and its limit."],
   mode='works', introduces=['changelog.eval.yaml', 'max']),
 S('s09', 'body', B, 'html', "Headline 'Free to test'. Two blocks side by side: 'script grader · needs the workspace, which is gone · fails every trial in a re-grade' and 'budget grader · reads the saved trial record · judged exactly as in a real run'. The second lights.", [
   "These graders work only from what the trial record keeps.",
   "So a re-grade with vally grade judges them exactly as a real run would, unlike a script grader, which needs the workspace.",
   "That makes a budget cheap to test, with no agent run."], mode='works', introduces=['vally grade', '-e', '--run-dir']),
 S('s10', 'body', B, 'html', "Headline 'Over is over'. Two blocks side by side: 'the score · falls in proportion to the overrun' and 'the verdict · fails, however small the overrun'. Each lights as it is named.", [
   "What happens just over the line?",
   "Once a trial is over the max, the grader's score drops only as far as the trial went over, so a trial that is barely over still scores almost one.",
   "Its verdict doesn't soften: the grader fails, and since every grader must pass, the trial fails."], mode='works'),

 S('s11', 'body', C, 'html', "Headline 'A limit that stops the agent'. File panel labelled 'evals/changelog.eval.yaml' with a minimap, on the start of the first stimulus: name and prompt (its text hidden), then 'constraints:' and 'max_agent_duration: 1m', then agent_environment. Callouts on the right: 'limits for this stimulus's trials', 'stop the agent, then grade what it did'. A note: 'the record's endReason: agent_timeout'.", [
   "Budget graders judge a trial after it has finished, when the tokens are already spent.",
   "To stop an agent while it's working, a stimulus takes a constraints block.",
   "It sits under one stimulus; there's no version for the whole file, so each stimulus gets its own.",
   "Max agent duration is how long the agent may work.",
   "At that limit, Vally stops it, and then grades whatever it had done by then, like any finished trial.",
   "In the trial record, the end reason then says agent timeout."],
   mode='works', chapter='Limits that stop the agent', introduces=['constraints', 'max_agent_duration']),
 S('s12', 'body', C, 'html', "Headline 'Three limits, three behaviours'. Three blocks across the width, titles in mono: 'max_agent_duration · stops the agent, grades its partial work', 'max_duration · a hard limit: the trial is stopped and fails', 'max_turns · the most turns; what happens at the limit is not documented'. Each lights as it is named.", [
   "Three limits can go in that block.",
   "Max agent duration stops the agent and grades its partial work, which suits an unfinished attempt that is still worth grading.",
   "Max duration is a hard limit: a trial that reaches it is stopped, and counted as a failure.",
   "It does for one stimulus what the timeout in the file's defaults does for all of them.",
   "If a stimulus sets both, the agent's limit has to be the shorter one; otherwise the hard limit ends the trial first.",
   "Max turns is documented as the most turns a trial may take.",
   "The docs don't say what happens at that limit, so we count turns with the turn count grader instead."],
   mode='works', introduces=['max_duration', 'max_turns']),

 S('s13', 'practice', U, 'html', "Headline 'Tested before they are trusted'. Four numbered blocks, no arrows: 1 'measure · what a typical trial uses'; 2 'set · budgets just above it'; 3 'test · on saved trials, free'; 4 'adjust · then a time limit, and one run'. Each fills as it is named; then the question stays up for a beat.", [
   "That's how they work; now let's set some.",
   "First, we find out what a typical trial used in the cost experiment we already ran.",
   "Then we set budgets just above that, lint the file, and test them on that experiment's saved trials with vally grade, which starts no agent.",
   "After that we adjust them, add a time limit, and run the five stimuli once, with vally eval.",
   t("With budgets just above the typical trial, how many good trials would you expect them to fail?", read=2),
   "If you tried it yourself, here's what you'd see."],
   mode='use', chapter='Set budgets from your runs', introduces=['vally lint', 'vally eval', '--model', '--workers', '--output-dir']),
 S('s14', 'practice', U, 'html', "Headline 'What a typical trial uses'. Three large numbers side by side, each the largest median in one column of the experiment's report.md across the four variants: tokens, turns, seconds, each with the variant and stimulus it comes from. A note names report.md and the run.", [
   "The experiment's report has a table for each variant, with the median tokens, turns and duration of every stimulus.",
   "Across all four variants, we take the largest value in each of those three columns.",
   o("In our run, that's a little over one hundred six thousand tokens, five turns, and about thirteen seconds.", read=2)],
   mode='use', introduces=['report.md']),
 S('s15', 'practice', U, 'html', "Headline 'Budgets just above typical'. A three-row table: tokens, turns, time; columns 'largest typical' and 'first budget'. The budget column lights.", [
   "We add the three budget graders to the end of every stimulus's graders, with those numbers rounded up a little.",
   o("Ours are one hundred seven thousand tokens, five turns, and thirteen seconds.", read=2)],
   mode='use'),
 S('s16', 'practice', U, 'terminal', "Terminal in the practice folder; the prompt shows only the current folder name. vally lint on the eval file prints one warning. The screen is cleared. cd into the one run folder under results/lesson-16, then into haiku-high; then the vally grade command over three lines, as the lesson prints it. Its blocks scroll past and the last screen is held.", [
   t("First, we lint the file, which costs nothing.", before="typed:1"),
   o("No errors, and one warning we've met: with several graders and no scoring block, every grader must pass, which is what we want here.", wait_for="output:1", read=3),
   t("Now the free test: we change into the cost experiment's run folder, and then into one variant, haiku high.", before="typed:2"),
   t("This is the re-grade we've used before: the eval file is four folders up, the run dir is this folder, and the saved results are the input.", wait_for="done:3", before="typed:4"),
   t("Script graders can't be re-graded, so two of the stimuli will show a failing line whatever happens.", before="typed:4"),
   t("What we're looking for is a failing line that names a budget.", before="enter:4"),
   o("Fifteen blocks come back, more than fits on a screen, and one of them, further up, names the token budget.", wait_for="output:4", read=4)],
   mode='use', introduces=['cd', 'lesson-16', '2026', 'haiku-high'], shows=['vally lint', 'cd', 'vally grade']),
 S('s17', 'practice', U, 'html', "Headline 'Barely over, and failed'. Two dark boxes, one above the other. First, labelled as our haiku-high re-grade: the one block that names a budget, as printed: verdict line, the script grader's line, the token budget's line, Score line. Second, labelled 'an earlier run · a trial 28 tokens over': that run's block, whose Score line reads 100.0% and FAILED. Our budget line lights, then our script grader's line, then the earlier run's Score line.", [
   o("Here's that block, as the re-grade printed it."),
   o("One two changes trial went over the token budget, by about one percent."),
   o("Its other failing line is the script grader, which a re-grade can't run."),
   t("In an earlier run, a trial went twenty-eight tokens over, still printed a score of one hundred percent, and failed all the same.", read=2)],
   mode='use'),
 S('s18', 'practice', U, 'terminal', "Terminal, continuing in the haiku-high folder. cd ../terra-high, then the same vally grade command over three lines. Its blocks scroll past and the last screen is held.", [
   t("Now the same test on the other model's variant, terra high.", before="typed:1"),
   t("It's the same command, on that variant's saved trials.", wait_for="done:1", before="enter:2"),
   o("This time it's the turn count budget: two trials each took one turn more than the max of five.", wait_for="output:2", read=4),
   o("No trial went over the wall time budget.", read=2)],
   mode='use', introduces=['terra-high'], shows=['cd', 'vally grade']),
 S('s19', 'practice', U, 'html', "Headline 'Wrong budgets, or wrong trials?'. A table of every trial a budget failed in the two re-grades: stimulus, variant, the budget, what the trial used, the max. Under it a note: how many saved trials were re-graded. Rows light as their kind is named.", [
   "So which is wrong: the budgets, or the trials?",
   "For each trial a budget failed, we ask whether it did the work, and whether it looped.",
   o("All three of these trials passed when the experiment ran, and none of them looped."),
   o("The token failure was about one percent over, and the two turn failures took one turn more than usual."),
   o("So the budgets were wrong, not the trials: set just above typical, they failed three good trials of the thirty we re-graded.", read=2)],
   mode='use'),
 S('s20', 'practice', U, 'html', "Headline 'Room for normal variation'. The table from before with a third column: 'largest typical', 'first budget', 'wider budget'. The new column lights.", [
   "Good trials vary from one to the next, and a budget has to leave room for that, so we raise each one to about twice the largest typical value.",
   o("Ours become two hundred fifteen thousand tokens, ten turns, and thirty seconds.", read=2)],
   mode='use'),
 S('s21', 'practice', U, 'terminal', "Terminal, continuing in the terra-high folder. The same vally grade command; its blocks scroll past. The screen is cleared. cd ../haiku-high and the same command again. The screen is cleared. cd ../../../.. back to the practice folder.", [
   t("Then the same re-grade again, here in terra high.", before="typed:1"),
   o("Only the script graders fail now, as they did before; no block names a budget.", wait_for="output:1", read=3),
   t("Once more in haiku high.", before="typed:2"),
   o("It's the same there.", wait_for="output:3", read=3),
   t("That's the free testing done, so we go back to the practice folder.", before="typed:4")],
   mode='use', shows=['vally grade', 'cd']),
 S('s22', 'practice', U, 'html', "Headline 'Three trials, then none'. A two-row table: 'first budgets' and 'wider budgets'; columns: trials that failed token-budget, turn-count, wall-time, and any budget. The second row lights.", [
   o("With the first budgets, three trials failed a budget; with the wider ones, every budget passes every trial."),
   "No agent ran to find that out."],
   mode='use'),
 S('s23', 'practice', U, 'terminal', "Terminal in the practice folder. vally lint on the eval file. The screen is cleared. The vally eval command over three lines, as the lesson prints it, with --output-dir results/lesson-18; a jump cut; then the summary with a count for each model.", [
   t("Last, the time limit: the constraints block from earlier is now under each of the five stimuli, with a max agent duration of one minute.", before="typed:1"),
   o("Lint has no errors.", wait_for="output:1", read=2),
   t("Now one run of the five stimuli on both models, with the budgets and the limit in place.", before="typed:2"),
   t("It spends ten short agent runs.", before="enter:2"),
   t("What we're hoping for is five of five under each model.", before="enter:2"),
   o("About a minute later, that's what both models show: every trial passed, budgets included.", wait_for="output:2", read=4)],
   mode='use', introduces=['lesson-18'], shows=['vally lint', 'vally eval'], spend="10 agent runs"),
 S('s24', 'practice', U, 'html', "Headline 'Nothing near a limit'. A three-row table: tokens, turns, time; columns 'largest in this run', 'budget', and for time also the one-minute limit. The first column lights.", [
   o("In that run, the largest trial used about seventy-six thousand tokens and five turns, and the slowest took twelve and a half seconds."),
   o("So every trial stayed well inside the budgets, and the one-minute limit never came into it.", read=2)],
   mode='use'),

 S('s25', 'body', W, 'html', "Headline 'Typical is a middle value'. Two blocks side by side with large figures: the count of good trials the first budgets failed, out of those re-graded; and the turns terra-high took for one request. Each lights as it is said.", [
   "So what did the limits catch?",
   o("Our first budgets, set just above the typical trial, failed three good trials of thirty."),
   "That's a grader failing correct work, and the saved trials caught it before any agent ran.",
   "It happened because a typical trial is a middle value: half of all trials are above it.",
   o("Terra took four, five or six turns for the same request."),
   "So a budget at the median fails normal variation."],
   mode='think', chapter='What the limits caught'),
 S('s26', 'body', W, 'html', "Headline 'Room above normal'. Two blocks side by side under the label 'a budget at about twice the largest typical trial': 'a loop, at ten times the usual · fails' and 'one turn more than usual · passes'. Each lights as it is said.", [
   "Budgets are for the trial that runs away, at several times the usual cost, so they need room above normal.",
   "Twice the largest typical trial still fails a loop that costs ten times as much.",
   "It passes a trial that took one turn more than usual.",
   "Whenever the model, the effort or the skill changes, the budgets get tested again, the same free way."], mode='think'),
 S('s27', 'body', W, 'html', "Headline 'What a token budget doesn't do'. A table: model, tokens in a typical trial; three rows. Beside it one block with the token budget every model shares. Rows light in turn.", [
   "It's worth seeing what a token budget doesn't do.",
   "One budget holds for every model the eval runs on, and the models differ.",
   o("In our runs, a typical trial used about a hundred and five thousand tokens on haiku five point five, seventy-five thousand on haiku four point five, and sixty-one thousand on terra."),
   "So a budget set for the hungriest model is loose for the others.",
   o("Tokens aren't price, either, because a token costs a different amount on each model: in the cost experiment, terra used the fewest tokens and cost the most."),
   "Token budgets catch a trial that loops; choosing a cheaper model is what cost per passing trial is for."], mode='think'),
 S('s28', 'body', W, 'html', "Headline 'A limit for the bad day'. Two blocks side by side with large figures: '1m · max_agent_duration: stop the agent, grade what it wrote' and '3m · the file's timeout'. The first lights.", [
   o("Our time limit did nothing in that run, which is what a limit should do on a good day."),
   "It's there for the day an agent stalls.",
   "Then a nightly run loses one minute on that trial, where the file's timeout would lose three, and it still grades what was written."], mode='think'),

 S('s29', 'recap', W, 'html', "Headline 'Budget, or limit?'. One block, 'a ceiling on a trial', which after the question and a pause opens into two parts: 'a budget grader · judges the finished trial' and 'a limit under constraints · acts while the agent works'. Each part lights as it is said.", [
   "Before you go on: how does a budget grader differ from a limit under constraints?",
   t("Budget graders judge the finished trial, and fail it if a number is over the max; by then, the cost is spent.", pause=2.5),
   "Limits act while the agent is working: max agent duration stops it and grades what it produced, and max duration stops it and fails the trial."]),
 S('s30', 'next', W, 'slide', "'Is it worse than before' in the display serif, under the eyebrow 'Next'. Below, the hand-off question: 'Can a check say no worse than before, in quality and in cost?' A note: 'Exercises are on the lesson page · Source: Vally docs, Graders: metric thresholds'.", [
   "You can now add budget graders and an agent time limit, and test each budget on saved trials in a free re-grade.",
   "Budgets now sit beside the other graders on every trial.",
   "Before relying on an edit, you'd want a check that says no worse than before, in quality and in cost.",
   "Can Vally decide that?",
   "That's the next lesson.",
   "For practice, the exercises on the lesson page are worth doing first."]),
]
(D / 'storyboard.json').write_text(json.dumps(sb, indent=1, ensure_ascii=False) + '\n')
print('storyboard-ok', len(sb['scenes']))
