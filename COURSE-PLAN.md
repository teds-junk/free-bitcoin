# Course plan: Vally & Agent Evals

Status: verified
<!-- draft → agreed → authored → built → verified -->
<!-- Revision 2 (2026-11-10): adds cost, partial credit, budgets, your own provider, vally compare,
     debugging, and a second part on evaluating the skill inside an AI app. Lessons 1-13 keep their
     files; old 14 becomes 15 and old 15 becomes 21. Changes to existing lessons are marked "Rev 2". -->

## Story
Starting problem: You wrote a skill and it works when you try it, but you cannot tell whether it works on another model, on the fifth run, or after your next edit, or what each run costs.
Destination: You can edit the skill, or change the model under it, and say with evidence whether it got better and what it costs, using checks a teammate can run too; and you can evaluate the same behaviour when an application, not a person, asks the agent for it.
Running example: `changelog-entry`, a short skill that tells an agent how to record a change in the `CHANGELOG.md` of a made-up tool, `notes-cli`. The course ships it as a deliberately plain first draft in `./practice-starter/`. Lesson 1 copies that folder to `./practice/`, and every later lesson measures the skill, finds a problem and improves it there. Part 2 (lessons 22 to 26) keeps the same skill and imagines that the `notes-cli` team has built it into their release tooling: on each merge, a small app asks an agent to write the Unreleased entry from the git history. No new example: the app is a short script shipped in `./practice-starter/app/`.

Evidence for the example (pilot, 2026-11-09, 42 trials, saved in `research/pilot-2026-11-09/`): with the first-draft skill, every model passed a loose check on every request, while the saved patches showed one model inventing a pull request number, all three recording a change users cannot see, all three filing a security fix under Fixed, and two describing a fix in implementation words.

## Practice
- `./practice-starter/` (shipped): the first-draft skill, two neighbouring skills used in lesson 9, two changelog fixtures, the lesson 1 eval file and the six-request eval file used from lesson 4. Rev 2 adds: the broken eval files for lesson 20 (`evals/broken/`), the release app and its run script for lessons 22 to 26 (`app/`), and a trace converter for lesson 25.
- `./practice/` (created by the reader in lesson 1): all hands-on work. Every path in a lesson is relative to it.
- `./verified/lesson-NN/` (shipped): the state of the practice folder at the end of each lesson and the console output from our run, for a reader who wants to compare. Rev 2 renames `lesson-14` to `lesson-15` and `lesson-15` to `lesson-21`.
- Models: the reader lists their own account's models in lesson 1 and picks two. The course home names the two the course used and the date they were checked. Commands print the course's pair as a marked stand-in.
- Vocabulary rule: lesson 1 uses plain words (request, check, run). Lesson 2 introduces Vally's words for them (stimulus, grader, trial). From lesson 2 on the course uses Vally's words and no synonyms.

## Lessons

## Part: Measure the skill

### 1. It works for me
File: 0001-it-works-for-me.html
Question: My skill works when I try it. Does it do the same thing on another model?
Win: Run one changelog request on two models and find, in the files Vally saved, that the two models changed the file differently.
Hand-off: Both models got a green tick, yet they did different things. So what did the tick check?
Time: 15 minutes, about 2 agent runs
Sections:
1. A skill is advice, and each model reads it its own way | think | "It worked when I tried it" is one model, one run: the skill is instructions that a model interprets.
2. What one Vally run does | works | An eval gives a request to an agent in a scratch folder with the skill installed, saves what the agent changed, then checks it.
3. Reading a patch | works | A patch is a file listing the lines added and removed; Vally saves one per run.
4. Run it on two models | use | Check the prerequisites, copy the starter, read the skill, list your account's models, run with two of them, open each saved patch.
5. What the two patches show | think | Both models passed and did different things; one invented a pull request number.
Recalls: none
Primary source: Vally docs, Run Your First Eval

### 2. What the tick checked
File: 0002-what-the-tick-checked.html
Question: What exactly did Vally run and check when it gave both models a tick?
Win: Explain every line of the eval file, and find any run's request, changes, verdict and token count in the results folder.
Hand-off: You can read everything about a run. But each model ran once. Would it do the same thing next time?
Time: 17 minutes, no agent runs
Sections:
1. The eval file, line by line | works | An eval file holds stimuli (a request plus its graders) and the agent environment (what the agent starts with).
2. What a run leaves behind | works | The results folder holds a report, `results.jsonl`, and one folder per trial; a trial's verdict comes from its graders.
3. What a trial used | works | Rev 2. Each trial records its token usage (input, output, and the share read from cache) and, on Copilot, a cost in `nano-aiu`; the report's Tokens column is the median. In real money: a billion nano-AIU is one AIU, one AIU is one GitHub AI Credit, and an AI Credit is $0.01 (GitHub billing docs, checked 2026-11-10), so our typical trial cost about 2 AIU, about 2 cents; usage counts first against the plan's monthly allowance. Shown, not yet used: lesson 16 builds on it.
4. Why both models passed | think | A grader only objects to what you told it to look for; a pass means "no objection", not "correct".
5. Find it in the files | use | Lint the eval file, open the report and each trial folder, and answer four questions from what is there (Rev 2: the fourth is "which model used more tokens?").
Recalls: what the `+` lines in a patch mean; what the workspace is
Primary source: Vally docs, Eval Spec reference; Trajectory Format

### 3. The same request, five times
File: 0003-the-same-request-five-times.html
Question: If the same model gets the same request again, does it do the same thing?
Win: Run five trials on each model and state, as counts, how often each one invents a pull request number.
Hand-off: You counted one problem on one request by reading ten patches. What else goes wrong when the requests get messier?
Time: 12 minutes, about 10 agent runs
Sections:
1. One run is one sample | think | Agents vary from run to run, so the useful question is "how often", and that needs several trials.
2. Trials and their four outcomes | works | `runs` repeats each stimulus; a stimulus ends as PASS, FLAKY, FAIL or ERROR, and ERROR is not a verdict.
3. Why the course limits workers | works | Trials run in parallel sessions; too many at once drop sessions and produce ERROR, so the course uses two.
4. Count it | use | Run five trials per model with two workers, open the ten patches, fill in a tally.
5. What the tally says | think | A count per model replaces an impression; the grader failed the one trial that asked.
Recalls: what a stimulus is; where a trial's patch is saved
Primary source: Anthropic, Demystifying evals for AI agents (2026-01-09)

### 4. Read the runs before writing graders
File: 0004-read-the-runs-first.html
Question: What else goes wrong when the requests get messier?
Win: A short written list of the skill's failure modes, each with the trial that shows it.
Hand-off: You found the failures by reading. After every edit to the skill you would have to read them all again. Can code do the reading?
Time: 12 minutes, about 12 agent runs
Sections:
1. Why reading comes first | think | You cannot list what to check before seeing what goes wrong; a failure mode is a named way the skill's output is wrong.
2. Six ordinary requests | works | One eval file can hold many stimuli, and `--skip-grade` runs them without grading.
3. Read and name | use | Run six requests on both models, open each patch, write one note per trial, group the notes into failure modes.
4. Where the failures come from | think | Each failure is a question the skill left open, which each model answered its own way.
Recalls: ERROR versus FAIL; what a grader's pass does not tell you
Primary source: Husain and Shankar, AI Evals FAQ (reissued 2026-09-18)

## Part: Graders you can trust

### 5. Turn a failure into a grader
File: 0005-turn-a-failure-into-a-grader.html
Question: How do I make code decide whether a trial has one of these failures?
Win: Show, with three graders and a count before and after, what one edit to the skill changed on each model.
Hand-off: Patterns caught three failures. "Nothing else in the file changed" is not a pattern: it needs a script. Where can a script live so the agent cannot read or edit it?
Time: 15 minutes, about 36 agent runs
Sections:
1. What makes a grader worth having | think | Grade the result, not the route; one grader per failure mode; a grader that cannot fail tells you nothing.
2. Graders that read the diff | works | Diff graders read the patch of what the agent changed; a trial passes only if every grader on its stimulus passes.
3. Measure, edit the skill, measure again | use | Add three graders, run, add one rule to the skill per failure mode, run again, compare the counts per stimulus.
4. What the counts show | think | The same edit worked fully on one model and partly on the other.
Recalls: failure mode; what `runs` does
Primary source: Vally docs, Choose a Grader

### 6. Keep graders out of the agent's reach
File: 0006-keep-graders-out-of-reach.html
Question: Where can I put a grading script so the agent cannot read or change it?
Win: See exactly what an agent is given to work with, and add a grading script that reaches the graders without ever reaching the agent.
Hand-off: A hidden script now decides pass and fail, and only you can see whether it is right. How do you test a grader?
Time: 12 minutes, about 21 agent runs
Sections:
1. Why the agent must not see the grader | think | An agent can read and edit everything in its workspace, so a grader it can see can be satisfied without doing the work.
2. What goes into the workspace | works | The agent environment copies the whole skill folder and the listed files into the workspace before the agent starts.
3. What is added only for grading | works | The grading environment adds files to a copy of the finished workspace after the agent stops, and a `program` grader runs a script there that prints its verdict and evidence as one line of JSON.
4. Look inside, then add the hidden script | use | Keep one workspace, list its files, add two stimuli graded by the staged script, run, add a rule to the skill for what fails, run again.
5. What the script caught | think | A failure nobody had seen, an entry under a released version, and a reminder that single trials vary.
Recalls: what a diff grader reads; the every-grader-must-pass rule
Primary source: Vally docs, Eval Spec reference, Grading environment

### 7. Test a grader without running an agent
File: 0007-test-a-grader.html
Question: How do I know a grader passes correct work and fails missing work?
Win: Keep a golden patch for a stimulus, and use `vally oracle` to show that its graders pass a correct answer and fail an untouched file.
Hand-off: The oracle could not test the graders that check for absence, and it tried only one correct answer each. But you have dozens of real answers saved, good and bad. Can the graders be run on those?
Time: 15 minutes, no agent runs
Sections:
1. Two ways a grader can be wrong | think | A grader can fail correct work or pass work that was not done, so testing it needs a known-correct answer and an untouched file.
2. A golden patch | works | A golden patch is a patch you keep that records exactly the changes a correct answer would make; a saved trial's patch can be used as it is.
3. What vally oracle does | works | `vally oracle` builds the workspace, applies the golden patch in place of an agent, and grades; with `--no-golden-input` it applies nothing, and that untouched state is the baseline.
4. Prove your graders | use | Save a correct trial's patch as the golden patch, name it in the eval file, run the oracle with it and without it, watch it catch a useless grader, repeat for the other stimuli.
5. What the oracle did not test | think | Graders that check for absence, and correct answers worded differently.
Recalls: what the grading environment adds; how to read a patch
Primary source: Vally docs, CLI: oracle

### 8. Check graders against saved trials
File: 0008-check-graders-against-saved-trials.html
Question: The oracle cannot test a grader that checks for absence, and it tries one correct answer. Can I run my graders on the real trials I have already saved?
Win: Re-grade a saved run without starting an agent, and use it to show that a grader which passed the oracle could never fail.
Hand-off: The graders are now tested against correct answers, empty answers and real bad answers. In every trial so far the skill was loaded. Will it load for other wordings, and stay out of requests that are not its job?
Time: 12 minutes, no agent runs
Sections:
1. Saved trials are tests for graders | think | A trial you have read and know to be bad is the test for a grader that checks for absence; a grader that never fails one is broken.
2. Re-grading a saved run | works | `vally grade` applies the eval file's current graders to the trials saved in a run folder, with no agent; it is reliable for graders that read the diff and not for script graders.
3. Catch a grader that cannot fail | use | Re-grade the lesson 5 run of known-bad trials, swap in a pattern that looks right and is not, see the oracle accept it and the saved trials expose it, restore the pattern.
4. A habit for every grader | think | Oracle first, then a saved run of known failures, then agent runs.
Recalls: golden patch; what N/A means in the oracle's report
Primary source: Vally docs, CLI: grade

## Part: Is the skill earning its place

### 9. Does the skill load when it should
File: 0009-does-the-skill-load.html
Question: Does the agent load the skill for the requests it is meant for, and leave it alone for the others?
Win: Show, with a loading eval that includes near-miss requests, what rewriting the description changed on both models.
Hand-off: It loads at the right times. But in one trial the agent did the job without it. Is the result any better with the skill than with no skill at all?
Time: 15 minutes, about 48 agent runs
Sections:
1. The description decides | think | The agent chooses among installed skills by their descriptions; a near-miss request shares words with the skill's job but is not its job.
2. How a trial records loading | works | A loaded skill appears as a `skill_activation` event in the trial's trajectory and in the report's Skills column, and the `skill-invocation` grader reads it.
3. Test loading, then fix the description | use | Write requests that should and should not load the skill, run with neighbouring skills installed, rewrite the description, run again.
4. What the loading test showed | think | One miss on a request without the obvious word; a test that will catch the next one.
Recalls: failure mode; FLAKY
Primary source: agentskills.io, Optimizing skill descriptions

### 10. Is the agent better with the skill
File: 0010-is-the-agent-better-with-the-skill.html
Question: Are the results better with the skill than without it?
Win: A with-and-without comparison for each model, and one sentence saying where the skill helps, where it does not, and what it changes in tokens.
Hand-off: Every stimulus so far was one request. Real use goes on: someone asks for a follow-up.
Time: 13 minutes, about 20 agent runs
Sections:
1. A skill has to beat no skill | think | The baseline here is the same stimuli and graders with no skill; a skill can help, make no difference, or hurt.
2. An experiment file | works | An experiment file names variants of one eval; `vally experiment run` runs them all and prints one column of pass counts per variant, with total tokens and trial time beneath.
3. Run with and without | use | Put your models into the shipped experiment file, check it with a dry run, run it, read the table and one no-skill patch, write the sentence.
4. What the comparison showed | think | The skill helps on three stimuli, the first draft caused the invented number, and (Rev 2) in our run the skill did not cost tokens: both models used fewer with it (360.0k vs 371.0k; 255.0k vs 280.9k), from one trial each.
Recalls: near-miss request; the every-grader-must-pass rule
Primary source: Vally docs, Run Your First Experiment

### 11. Follow-up requests
File: 0011-follow-up-requests.html
Question: Does the skill still hold when the conversation continues?
Win: Show, with a three-turn stimulus graded turn by turn on both models, whether the skill's rules survive a follow-up, and fix what fades.
Hand-off: Everything graded so far is structure that code can see. "Written for the people who use the tool" is not a pattern.
Time: 12 minutes, about 12 agent runs
Sections:
1. What changes in a conversation | think | A rule can fade, an earlier turn can leak into a later one, and a later turn can disturb earlier work, so each turn's change needs its own grader.
2. Turns, and graders scoped to a turn | works | `turns:` sends a list of requests in order to the same session, and `turn:` limits a grader to what one turn did; Vally saves a diff per turn.
3. Write and run a conversation | use | Add a grader per turn to the shipped three-request conversation, run on both models, read the failing turn's diff, add a rule to the skill, run again.
4. What the conversation showed | think | A number leaked from one turn into the next, on the model that never invented one.
Recalls: what a diff grader reads; baseline
Primary source: Vally docs, Writing Eval Specs, Multi-turn conversations

## Part: Judgement and evidence

### 12. A judge for what code cannot check
File: 0012-a-judge-for-what-code-cannot-check.html
Question: How do I grade a quality that no pattern can decide?
Win: One yes-or-no LLM judge for "describes what users notice, not how it was built", run over saved trials, with its reasons read.
Hand-off: The judge answered yes for some trials and no for others. It is a model. Is it right?
Time: 12 minutes, about 12 agent runs and 12 judge calls
Sections:
1. When a judge is the right tool | think | An LLM judge is for what code cannot decide; ask one yes-or-no question, and decide your own answers first.
2. How Vally's judge decides | works | The `prompt` grader gives a judge model the `rubric` and the trial's evidence, and records a verdict with reasons.
3. Write the judge and re-grade | use | Run three requests worded in coding terms, write your own yes or no for each of the twelve entries, add a rubric and a `prompt` grader with a named judge model, judge the saved trials, record each verdict beside your own.
4. What the judge found | think | One model half-ignores the wording rule; a well-written reason is not yet evidence.
Recalls: `vally grade`; `turn:`
Primary source: Hamel Husain, Using LLM-as-a-Judge

### 13. Check the judge against your own labels
File: 0013-check-the-judge.html
Question: Can I trust the judge's verdicts?
Win: Your own yes-or-no labels for the same trials, the judge's agreement with them as two numbers, and a decision about relying on it.
Hand-off: Rev 2. The judge's yes and no agree with your labels. But some of the "no" entries were nearly right and some were far off, and a yes-or-no cannot tell them apart. Can a grader give partial credit without hiding a failure?
Time: 12 minutes, no agent runs
Sections:
1. A judge is measured, not trusted | think | A judge can be wrong in two directions, and one agreement figure hides which.
2. TPR and TNR | works | TPR is the share of your yes labels the judge also passed; TNR is the share of your no labels it also failed.
3. Count, compare, decide | use | Sort the twelve trials into four boxes using the labels written in lesson 12, work out both numbers, examine each disagreement, decide.
4. What twelve labels can show | think | Enough to catch a judge that is badly wrong, not to prove one right.
Recalls: rubric; the two ways a grader can be wrong
Primary source: Husain and Shankar, validate-evaluator skill

### 14. Partial credit (new)
File: 0014-partial-credit.html
Question: How do I grade work that can be partly right, without letting a failure hide in an average?
Win: The lesson 12 trials re-graded with a judge scoring 1 to 5 against a threshold, and one sentence saying which verdicts changed from the yes-or-no judge and whether your labels agree.
Hand-off: Scores and counts both move after an edit. After an edit, 7 of 10 becomes 9 of 10. Is that real?
Time: 14 minutes, no agent runs, about 12 judge calls
Sections:
1. When a score beats a yes or no | think | Thresholds are for judged quality and partial credit, not for checks that must all hold; Vally's own advice is to leave pass-or-fail graders out of any weighting.
2. How Vally turns grader results into a verdict | works | With no `scoring` block every grader must pass; with `weights` and a `threshold` the stimulus passes when the weighted score reaches the threshold, and a grader type left out of `weights` stops counting.
3. A judge on a scale | works | `scoring: scale_1_5` asks the judge for 1 to 5 per rubric criterion, rescaled to 0 to 1 (a 4 becomes 0.75), and the grader's own `threshold` decides its pass.
4. Score the wording | use | Change the lesson 12 judge to `scale_1_5` with a threshold, re-grade the saved trials, put each score beside the yes-or-no verdict and your label.
5. What the scores showed | think | Where the scale separated "nearly" from "far off", and why a threshold needs the same label check as a yes-or-no.
Recalls: rubric; TNR
Primary source: Vally docs, Scoring; Grader: prompt

### 15. Is the change real (was 14)
File: 0015-is-the-change-real.html
Question: After I edit the skill, is a better count a real improvement or luck?
Win: A before-and-after comparison on the same stimuli with enough trials, and one sentence stating what it supports.
Hand-off: Rev 2. You can tell whether an edit helped. The same table also printed tokens for each variant, and they differ by model. What does a passing trial cost?
Time: 12 minutes, about 36 agent runs and 36 judge calls
Sections:
1. What a small sample can show | think | A count from a few trials has a wide range around it, and a change inside that range is not evidence.
2. What a before-and-after experiment prints and saves | works | The before-and-after experiment file and the blocks it prints; The report gives a pass rate, pass@k (at least one trial passed) and pass^k (the chance that k trials in a row all pass) for each stimulus; a range around a count comes from the calculator.
3. Compare before and after | use | Keep a copy of the skill, sharpen one rule, run both versions on both models with the judge as four variants, count trials, put the counts in the range calculator, write one sentence per model.
4. The earlier fixes, re-examined | think | Which of the course's fixes were measured and which were only reasonable.
Recalls: variant; TPR
Primary source: Evan Miller, Adding Error Bars to Evals (2024)

## Part: Worth what it costs

### 16. What a passing trial costs (new)
File: 0016-what-a-passing-trial-costs.html
Question: Which model, at which reasoning effort, gives the most passing trials for what it costs?
Win: A table of cost per passing trial for two models at two reasoning efforts, from one experiment, and a choice stated with its evidence.
Hand-off: You can price the models your Copilot account offers. The release app in part 2 may call a model through a service of its own. Can Vally run that model too, and what does a passing trial cost there?
Time: 15 minutes, about 60 agent runs
Sections:
1. Cost per passing trial | think | A cheap model that fails costs more per useful result; compare cost divided by passing trials, look for variants that are both cheaper and better than another, and remember the judge's cost is extra.
2. Where cost is recorded | works | Each trial's `tokenUsage` (from lesson 2) splits by model, and its `cost` appears only when every call reported Copilot as the provider; judge calls are not included; the experiment saves one record per trial per variant.
3. Reasoning effort as a variant | works | `reasoning_effort` sets how much the agent's model reasons before it acts; an experiment can vary it like a model, and accepted values depend on the model.
4. Price the variants | use | Check which efforts each model accepts (free: Vally rejects an unknown value before any session starts; `claude-haiku-4.5` accepts none, so the haiku variants use `claude-haiku-5.5`), run four variants (two models, two efforts) on the five stimuli with three trials, open each variant's `results.jsonl` in the cost calculator, compute cost per passing trial.
5. What the table says | think | Which variants are beaten on both counts, and how wide the ranges are at three trials. Real-world scale, in dollars at $0.01 per AIU: what this experiment cost, what a quick suite after every edit costs over a month, what a nightly full suite costs, and what the course itself cost us (the pilot, authoring and verification totals from NOTES), with the judge calls Vally does not count noted as extra.
Recalls: pass rate; variant
Primary source: Kapoor et al., AI Agents That Matter (2024-07)

### 17. A model from your own provider (new; was 18)
File: 0017-a-model-from-your-own-provider.html
Question: My app calls a model through its own provider, not my Copilot account. Can Vally run that same model?
Win: One variant running through your own provider beside the account's models, with its cost worked out from your own price per token.
Hand-off: You can price any model, including one you run yourself, and ours took two to five minutes a trial. One trial that loops can cost or take ten times the typical one. How do you fail, or stop, a trial that costs or takes too much?
Time: 12 minutes, plus about 15 for the optional local run; no Copilot runs (5 local trials with `--workers 1`: Ollama serves one request at a time, so two workers made trials wait on each other and time out)
Sections:
1. Evaluate the model you ship | think | Results on one provider's model say little about another's, even with the same name; evaluate through the endpoint the app uses.
2. Bring your own key | works | The executor (the part of Vally that runs the agent; `copilot-sdk` by default) takes a `provider` block with `baseUrl`, `type` and `apiKeyEnv`; the key is read from Vally's environment, never written in the file; no Copilot cost is recorded, so you price tokens yourself.
3. A variant on a local model | works | The experiment excerpt with the `qwen-local` variant: the `vary` paths it needs (`/defaults/executor`, `/defaults/timeout`, `/defaults/runs`), why one worker, the assumed price, and why a lone variant prints "Comparison unavailable — baseline not run" (section added after the cold read, id `local-variant`).
4. Run a variant on your provider | use | Add a provider variant to lesson 16's experiment, run it, read its tokens, multiply by your price.
5. What changed | think | What carried over between providers and what did not.
Recalls: reasoning effort; cost per passing trial
Primary source: Vally docs, Eval Spec reference, Executor configuration
Provider: local Ollama (agreed 2026-11-10), model `qwen3.5:9b` (spike S4: `gpt-oss:20b` fails with `400 invalid tool call arguments`). Free and needs no key; the step is marked optional because readers need Ollama and a model of about 6.6 GB, and a trial takes minutes (`--timeout 9m`). Also teaches that `cost` is absent and the reader prices tokens at their own rate (here zero, so the lesson prices them as if hosted).

### 18. Put a ceiling on a trial (new; was 17, swapped 2026-11-10 so lesson 17's local run is not cut off by these budgets)
File: 0018-put-a-ceiling-on-a-trial.html
Question: How do I fail, or stop, a trial that costs or takes too much?
Win: Budget graders and an agent time limit on the quick stimuli, each shown failing a real over-budget trial in a free re-grade.
Hand-off: Budgets now guard every trial. Before relying on an edit you want a check that says "no worse than before", in quality and in cost. Can Vally decide that?
Time: 12 minutes, about 10 agent runs
Sections:
1. A budget is a grader | think | A budget catches a cost regression or a loop; set it from measured trials rather than a guess, and pair it with a check that the work was done.
2. Budget graders | works | `token-budget`, `wall-time`, `turn-count` and `tool-call-count` read the trajectory's metrics and fail above `max`.
3. Limits that stop the agent | works | `constraints`: `max_turns`; `max_duration` fails the trial; `max_agent_duration` stops the agent and grades what it produced.
4. Set budgets from your runs | use | Read lesson 16's token counts, set budgets just above the typical trial, re-grade the saved trials (in our run 5 of 29 good trials failed), widen to about twice the largest typical value, re-grade again, add a `max_agent_duration`, run once. `max_turns` is explained but not run (its behaviour at the limit is undocumented); the lesson uses `turn-count`.
5. What the limits caught | think | A budget that fails good work is a grader that is wrong, tested the lesson 8 way.
Recalls: `vally grade`; the two ways a grader can be wrong
Primary source: Vally docs, Graders: metric thresholds; Eval Spec reference, Constraints

### 19. Is it worse than before (new)
File: 0019-is-it-worse-than-before.html
Question: Can a check tell me that a change made things worse, in quality or in cost, and fail when it did?
Win: A judged comparison of lesson 15's before and after runs, with its win rate and the change in tokens with a range, and a command that exits 1 on a regression.
Hand-off: You have many moving parts now, and runs sometimes end in ERROR or fail for reasons that are not the skill. When a run goes wrong, where do you look first?
Time: about 22 minutes (7 steps), no agent runs, about 52 judge calls
Sections:
1. Graders and side-by-side judging | think | Graders score each trial against fixed checks; a pairwise judge sees two answers to the same request and says which is better, which notices smaller changes and needs the order swapped to be fair.
2. What vally compare reports | works | Pairs trials by stimulus and trial number, scores each pair from much worse to much better, and prints a win rate, a mean with a 95% range, and the change in tokens, turns and time with ranges; `--fail-on-regression` exits 1 when the whole range is below zero.
3. Compare before and after | use | Run `vally compare` in two-run mode (`--baseline` and `--treatment` on two variant folders inside lesson 15's experiment folder, one model at a time; experiment mode would judge every variant against `haiku-before` and mix a model change in), read the win rate and the token change, then run the haiku pair swapped with `--fail-on-regression` and read its exit code (1). In our run tokens rose for terra with a range wholly above zero and the gate still exited 0: it gates on the judged score only.
4. What it supports | think | How it agrees and disagrees with lesson 15's ranges, and why the experiment's own `--compare` only reports.
Recalls: pass^k; range
Primary source: Vally docs, CLI: compare; Run Your First Experiment

## Part: Make it routine

### 20. When a run goes wrong (new)
File: 0020-when-a-run-goes-wrong.html
Question: When a run ends in ERROR, FLAKY or a surprising FAIL, how do I find out why without paying for more runs?
Win: Four broken eval files from the starter diagnosed and fixed (one that will not load, one that times out, a grader that fails good work, a judge call that fails), with the fewest agent runs.
Hand-off: You can measure, gate and debug. Now make it a routine that you and a teammate repeat.
Time: 20 minutes, 9 agent runs and 2 judge calls (four checkpoints; `commands:` is defined here in a definition box, used fully in L22)
Sections:
1. Four questions, cheapest first | think | Is the eval valid; did it complete; why was the result unexpected; does the fix work. Each answer usually comes from files you already have.
2. Where each answer lives | works | Load errors from lint; ERROR lines and `--verbose`; a trial's evidence, `results.jsonl` and `events.jsonl`; `vally grade` or a kept workspace to check a fix.
3. Fix four broken evals | use | Run each broken file once, follow the four questions, fix it, prove the fix with the cheapest check.
4. A symptom table to keep | think | What each symptom usually means, from our runs and the docs.
Recalls: ERROR versus FAIL; `--workspace`
Primary source: Vally docs, Debugging Evals

### 21. Keep it working (was 15)
File: 0021-keep-it-working.html
Question: How do I make this a routine that I and a teammate can repeat?
Win: Run a quick suite after every edit and a full suite before sharing, with a command that fails loudly on a failing verdict, an over-budget trial or a regression, and hand a teammate a one-page conventions file.
Hand-off: Part 1 is complete. Part 2: the `notes-cli` team has put the skill inside their release tooling. Does it still hold when an app, not a person, starts the agent?
Time: 13 minutes, about 40 agent runs and 6 judge calls
Sections:
1. Cheapest check first | think | Each way of checking costs more than the last, so use the cheapest one that answers the question.
2. Tags, suites and exit codes | works | Tags label stimuli, a suite in `.vally.yaml` names a group of them, and `--require-pass` turns a failing verdict into an error exit.
3. Two suites and a conventions page | use | Tag the stimuli, define both suites (Rev 2: the quick suite carries the lesson 18 budgets), run the quick one with `--require-pass`, read its exit code, see failing exit codes from free re-grades of lesson 5's run (a failing verdict; an over-budget trial, by lowering one budget for a moment; lesson 5's run has only diff graders, so its re-grade exit code is meaningful), point back to lesson 19's `--fail-on-regression` exit code, run the full suite once, write the conventions (Rev 2: ten headings, adding cost and debugging).
4. Where the skill stands | think | From one pair in six passing to the full suite passing, and what each trial costs now.
Recalls: `vally oracle`; `token-budget`
Primary source: Vally docs, Authoring Eval Suites

## Part: The skill inside an app

### 22. Start the agent where the app would (new)
File: 0022-start-the-agent-where-the-app-would.html
Question: Inside the release tool, the agent does not start from a person's request: the tool first lists what was merged since the last release, then asks for the entries. How do I set that up for a stimulus?
Win: A stimulus whose workspace is prepared by the release tool's own setup command (it writes `release/merged.txt`), graded by a hidden test run with `run-command`.
Hand-off: The entries are right. But in the app, how the agent got there matters too: did it read the list, did it touch files it should not, did it try to commit or push?
Time: 14 minutes, about 12 agent runs
Sections:
1. The stimulus is the app's situation | think | The prompt is what the app sends and the workspace is what the app has; an eval of a feature reproduces both, including the app's own setup steps.
2. Setting up before the agent starts | works | `commands:` run shell commands in the workspace after the files are staged and before the agent starts, and what they create is part of the starting state, not the diff (spike S6); `env:` sets variables for the agent; `git:` can clone or check out a real repository (explained, not run: the course ships no repository).
3. A hidden test with run-command | works | `run-command` runs a shell command in the graded copy and checks its exit code and output; with a test staged by the grading environment it becomes a hidden test.
4. Run the setup, then grade | use | Add a `commands:` step that runs the shipped `tools/list-merged.mjs` into `release/merged.txt`, ask for the entries for everything listed, add a hidden test that every listed change has an entry, run on both models.
5. What it showed | think | In our run neither model skipped or merged a change; with the app's terse prompt haiku did not load the skill (0 of 5 in the clean re-run; 1 of 5 while authoring) and recorded the internal refactor in every trial, while terra loaded it every time: the app's wording matters as much as the skill's.
Decided 2026-11-10: no real git history (Claude never runs `git commit`, even in fixtures; Ted chose this over a bundle he would create).
Recalls: grading environment; `program` grader
Primary source: Vally docs, Eval Spec reference, Agent environment; Writing Eval Specs, Grader-only files

### 23. Check what the agent did (new)
File: 0023-check-what-the-agent-did.html
Question: How do I check the steps the agent took, not just the file it changed?
Win: `tool-calls` graders that require reading `release/merged.txt` and forbid `git commit` or `git push`, and a loop check, each tested against saved trials.
Hand-off: In real use, git or the network sometimes fails. Does the agent cope, and can you test that without breaking anything?
Time: 13 minutes, about 12 agent runs
Sections:
1. Grade the path only when it matters | think | Outcome first; check the route when a step is required (read the list) or forbidden (commit, push), because the app relies on it.
2. The tool-calls grader | works | `tool-calls` reads the trajectory's tool calls; `required` and `disallowed` match a tool name and, for shell calls, the command, by regular expression.
3. Catching loops | works | `max-repeat` fails when the same call repeats past a limit; `loop-outcome` decides whether retrying was acceptable.
4. Require, forbid, re-grade | use | Add the graders, test them on the saved lesson 22 trials with `vally grade`, run once more.
5. What the path showed | think | A trial that passed on outcome and took a route the app would not allow, or none, and what that means.
Recalls: trajectory; `skill_activation`; `skill-invocation`
Primary source: Vally docs, Choose a Grader; Grader: tool-calls

### 24. When a tool fails (new)
File: 0024-when-a-tool-fails.html
Question: How does the agent behave when a command it relies on fails, and can I test that safely?
Win: A stimulus where the agent is asked to fetch the merged list itself and the command fails on purpose, graded on what the agent does next, and a simulation block recorded from a real run.
Hand-off: All of this ran inside Vally. The app also runs on its own, and keeps its own record of what it did. Can Vally grade a run it did not start?
Time: 13 minutes, about 12 agent runs
Sections:
1. Test the bad day | think | An app meets failing tools; a good agent says so and does not invent, and you test that by making the tool fail on purpose.
2. Simulation | works | `simulation` replaces a tool's result for calls that match a pattern, as success or failure; calls that do not match still run for real.
3. Recording a simulation | works | `vally simulate record` turns a saved trial's real tool calls into a simulation block to edit.
4. Make the tool fail | use | Simulate `node tools/list-merged.mjs` failing (the tracker is unreachable), grade that the agent writes no entry and says why, run on both models; record a block from a lesson 22 trial.
5. What the agent did on a bad day | think | In the final run neither model invented a change; the first attempts showed the answer leaking from the workspace (agents read the list straight out of the staged script, and around a `view` override with `rg`), so simulation intercepts calls, not knowledge: take the answer out of the workspace.
Recalls: `tool-calls`; `diff-empty`
Primary source: Vally docs, Eval Spec reference, Simulation; CLI: simulate

### 25. Grade a run Vally did not start (new)
File: 0025-grade-a-run-vally-did-not-start.html
Question: The app ran the agent itself, from a few shell commands, and recorded what it did as traces. Can Vally grade that run?
Win: Run the release app's script yourself, convert its trace file to a trajectory, and grade the result with the eval file you already have.
Hand-off: Grading afterwards gives one sample per run, on whatever model the app used. To get trials, experiments and models, Vally has to start the app itself.
Time: 15 minutes, 1 app run (the comparison reuses the reader's lesson 23 Vally run)
Sections:
1. Inside Vally or after the fact | think | Grading saved runs works on real traffic but cannot repeat a run; Vally-driven trials can; most teams want both.
2. A trajectory from outside | works | `vally grade` reads an ATIF file (steps holding messages, tool calls and their results) and a workspace folder; graders see only what the file records.
3. From OpenTelemetry traces | works | Vally sends its own traces out but does not read them in; an app's traces carry the model, tokens and tool calls as span attributes, and a short converter turns them into ATIF.
4. The script the release tooling runs | works | `app/run.sh` prepares a work folder the way the eval's setup does, runs the app with file tracing, and writes a plain diff (section added after the cold read, id `run-script`).
5. Run the app, convert, grade | use | Run `app/run.sh`, read its trace file, run the converter, grade with `vally grade --workspace`, compare with a Vally-run trial.
6. What carried over | think | Which graders worked on the converted run and which needed events the traces did not have.
Recalls: `vally grade`; `tool-calls`
Primary source: Vally docs, CLI: grade; Trajectory Format; OpenTelemetry, Semantic conventions for generative AI
Spike S3 passed: the SDK's file exporter, a 60-line converter `app/traces-to-atif.mjs`, `vally grade --workspace … --diff-file …`. Vally's `cost` is empty for ATIF input; the converter keeps `cost_usd` per step.

### 26. Let Vally run the app (new)
File: 0026-let-vally-run-the-app.html
Question: How do I give the app's own agent code Vally's trials, experiments and model comparisons?
Win: A small executor plugin in plain JavaScript that runs the release app for each trial, used in an experiment comparing two models.
Hand-off: The course is complete. The workflow guide walks the whole procedure, for a skill or for a feature in an app.
Time: 15 minutes, about 12 agent runs
Sections:
1. The executor is the seam | think | Vally calls an executor to run each trial; replacing it lets Vally drive any agent code while everything else stays the same.
2. What an executor returns | works | `execute` gets the stimulus and options (model, workspace, time limit) and returns a trajectory of events with metrics; `computeMetrics` adds them up; `.vally.yaml` `plugins` loads the file.
3. Joining the app's traces to Vally's | works | Vally passes a trace context to the executor; handing it to the app puts the app's spans under the trial's span.
4. Write and run the executor | use | Fill in the shipped plugin skeleton, run the lesson 22 eval through it on two models, then the experiment.
5. What you can now measure | think | Inside the app: the same graders, budgets and comparisons as for the skill alone. In our run the app used more tokens per model call in every trial (haiku ~17.4k vs ~15.1k, terra ~14.0k vs ~12.5k) because it keeps the hosted `github-mcp-server` (5 extra tools in every request) that Vally's own executor disables; its trials made fewer calls, so per trial it cost slightly less: overhead per call is steady, cost per trial depends on the trial. Skill loading did not differ beyond chance (haiku 0 of 5 through the app vs 1 of 8 through Vally's executor in lessons 22–23). The experiment includes `tracker-down`, which ends in ERROR in every variant at no cost (the app's executor does not support simulation); the page explains the `0/2` and `1/2` cells.
Recalls: experiment file; ATIF
Primary source: Vally docs, Writing Custom Executors
Spike S2 passed: `app/vally-executor.mjs` maps SDK events by hand; on the same stimulus the app costs more than Vally's own executor (85k vs 74k tokens), which section 5 uses.

## Concept order
| Term, tool or file | Origin | Introduced | First used |
|---|---|---|---|
| skill | agentskills.io | L1 §1 | L1 §4 |
| eval | Vally docs, How It Works | L1 §2 | L1 §4 |
| workspace | Vally docs, How It Works | L1 §2 | L1 §4 |
| patch | Vally results layout (seen in the pilot run) | L1 §3 | L1 §4 |
| `workspace.patch` | Vally results layout | L1 §3 | L1 §4 |
| `vally eval` | Vally CLI reference | L1 §2 | L1 §4 |
| `--model` | Vally CLI reference | L1 §2 | L1 §4 |
| `practice-starter` | course | L1 §4 | L1 §4 |
| `changelog-entry` | course | L1 §4 | L1 §4 |
| eval file | Vally docs, Eval Spec reference (there: eval spec) | L1 §2 | L1 §4 |
| stimulus | Vally docs, How It Works | L2 §1 | L2 §5 |
| grader | Vally docs, How It Works | L2 §1 | L2 §5 |
| agent environment | Vally docs, Eval Spec reference | L2 §1 | L2 §5 |
| `file-contains` | Vally grader catalog | L2 §1 | L2 §5 |
| trial | Vally docs, Scoring | L2 §2 | L2 §5 |
| `results.jsonl` | Vally docs, Trajectory format | L2 §2 | L2 §5 |
| `eval-results.md` | Vally results layout | L2 §2 | L2 §5 |
| `events.jsonl` | Vally results layout | L2 §2 | L2 §5 |
| `vally lint` | Vally CLI reference | L2 §1 | L2 §5 |
| token usage | Vally docs, Trajectory Format | L2 §3 | L2 §5 |
| `tokenUsage` | Vally docs, Trajectory Format | L2 §3 | L16 §2 |
| cache read tokens | Vally docs, Trajectory Format (there: `cacheReadTokens`) | L2 §3 | L16 §2 |
| `nano-aiu` | Vally docs, Trajectory Format | L2 §3 | L16 §4 |
| AI Credit | GitHub Docs, GitHub Copilot billing | L2 §3 | L16 §5 |
| `--runs` | Vally CLI reference | L3 §2 | L3 §4 |
| FLAKY | Vally docs, Scoring | L3 §2 | L3 §4 |
| `--workers` | Vally CLI reference | L3 §3 | L3 §4 |
| failure mode | Husain and Shankar, AI Evals FAQ | L4 §1 | L4 §3 |
| error analysis | Husain and Shankar, AI Evals FAQ | L4 §1 | L4 §3 |
| trajectory | Vally docs, Trajectory Format | L2 §2 | L9 §2 |
| `--skip-grade` | Vally CLI reference | L4 §2 | L4 §3 |
| `diff-contains` | Vally grader catalog | L5 §2 | L5 §3 |
| `diff-not-contains` | Vally grader catalog | L5 §2 | L5 §3 |
| `diff-empty` | Vally grader catalog | L5 §2 | L5 §3 |
| grading environment | Vally docs, Eval Spec reference | L6 §3 | L6 §4 |
| `program` grader | Vally grader catalog | L6 §3 | L6 §4 |
| `run-command` | Vally grader catalog | L6 §3 | L22 §3 |
| line of JSON | Vally grader catalog | L6 §3 | L6 §4 |
| exit code | Vally grader catalog | L6 §3 | L19 §3 |
| `--workspace` | Vally CLI reference | L6 §2 | L6 §4 |
| golden patch | Vally docs, Eval Spec reference | L7 §2 | L7 §4 |
| `vally oracle` | Vally CLI reference, oracle | L7 §3 | L7 §4 |
| `--no-golden-input` | Vally CLI reference, oracle | L7 §3 | L7 §4 |
| `vally grade` | Vally CLI reference, grade | L8 §2 | L8 §3 |
| near-miss request | agentskills.io, Optimizing skill descriptions (there: near-miss) | L9 §1 | L9 §3 |
| `skill_activation` | Vally docs, Trajectory format | L9 §2 | L9 §3 |
| `skill-invocation` | Vally grader catalog | L9 §2 | L9 §3 |
| baseline | Vally docs, CLI: oracle | L7 §3 | L7 §4 |
| experiment file | Vally docs, Run Your First Experiment | L10 §2 | L10 §3 |
| variant | Vally docs, Run Your First Experiment | L10 §2 | L10 §3 |
| `vally experiment run` | Vally CLI reference, experiment | L10 §2 | L10 §3 |
| `--dry-run` | Vally CLI reference, experiment | L10 §2 | L10 §3 |
| `turns:` | Vally docs, Writing Eval Specs | L11 §2 | L11 §3 |
| `turn:` | Vally docs, Eval Spec reference | L11 §2 | L11 §3 |
| LLM judge | Husain, Using LLM-as-a-Judge | L12 §1 | L12 §3 |
| rubric | Vally docs, Eval Spec reference | L12 §2 | L12 §3 |
| `judge_model` | Vally docs, Eval Spec reference | L12 §2 | L12 §3 |
| TPR | Husain and Shankar, validate-evaluator skill | L13 §2 | L13 §3 |
| TNR | Husain and Shankar, validate-evaluator skill | L13 §2 | L13 §3 |
| `scoring` block | Vally docs, Scoring | L14 §2 | L14 §4 |
| `weights` | Vally docs, Scoring | L14 §2 | L14 §4 |
| `threshold` | Vally docs, Scoring | L14 §2 | L14 §4 |
| `scale_1_5` | Vally docs, Grader: prompt | L14 §3 | L14 §4 |
| pass@k | Vally docs, Scoring Functions | L15 §2 | L15 §3 |
| pass^k | Vally docs, Scoring Functions | L15 §2 | L15 §3 |
| cost per passing trial | Kapoor et al., AI Agents That Matter (plain description; there: cost-controlled evaluation) | L16 §1 | L16 §4 |
| `reasoning_effort` | Vally docs, Eval Spec reference | L16 §3 | L16 §4 |
| `token-budget` | Vally docs, Graders: metric thresholds | L18 §2 | L18 §4 |
| `wall-time` | Vally docs, Graders: metric thresholds | L18 §2 | L18 §4 |
| `turn-count` | Vally docs, Graders: metric thresholds | L18 §2 | L18 §4 |
| `constraints` | Vally docs, Eval Spec reference | L18 §3 | L18 §4 |
| `max_duration` | Vally docs, Eval Spec reference | L18 §3 | L18 §4 |
| `max_agent_duration` | Vally docs, Eval Spec reference | L18 §3 | L18 §4 |
| executor | Vally docs, How It Works | L17 §2 | L17 §3 |
| `provider` block | Vally docs, Eval Spec reference (Executor BYOK) | L17 §2 | L17 §3 |
| bring your own key | Vally docs, Eval Spec reference (there: BYOK) | L17 §2 | L17 §3 |
| `apiKeyEnv` | Vally docs, Eval Spec reference | L17 §2 | L17 §3 |
| pairwise judge | Vally docs, CLI: compare (there: comparison mode) | L19 §1 | L19 §3 |
| `vally compare` | Vally CLI reference, compare | L19 §2 | L19 §3 |
| win rate | Vally CLI reference, compare | L19 §2 | L19 §3 |
| `--fail-on-regression` | Vally CLI reference, compare | L19 §2 | L19 §3 |
| treatment | Vally CLI reference, compare | L19 §2 | L19 §3 |
| McNemar's test | Vally CLI reference, compare (printed in its output) | L19 §2 | L19 §3 |
| `echo $?` | POSIX shell | L19 §2 | L19 §3 |
| suite | Vally docs, Authoring Eval Suites | L21 §2 | L21 §3 |
| `.vally.yaml` | Vally docs, .vally.yaml reference | L21 §2 | L21 §3 |
| `--suite` | Vally CLI reference | L21 §2 | L21 §3 |
| `--require-pass` | Vally CLI reference | L21 §2 | L21 §3 |
| `commands:` | Vally docs, Eval Spec reference | L20 §2 | L20 §3 |
| `tool-calls` | Vally docs, Grader: tool-calls | L23 §2 | L23 §4 |
| `max-repeat` | Vally docs, Grader: max-repeat | L23 §3 | L23 §4 |
| `loop-outcome` | Vally docs, Grader: loop-outcome | L23 §3 | L24 §4 |
| `vally eval --tag` | Vally CLI reference, eval | L24 §4 | L24 §4 |
| `simulation` | Vally docs, Eval Spec reference | L24 §2 | L24 §4 |
| `tool_overrides` | Vally docs, Eval Spec reference | L24 §2 | L24 §4 |
| `vally simulate record` | Vally CLI reference, simulate | L24 §3 | L24 §4 |
| ATIF | Vally docs, Trajectory Format (Agent Trajectory Interchange Format) | L25 §2 | L25 §4 |
| OpenTelemetry | opentelemetry.io | L25 §3 | L25 §4 |
| span | OpenTelemetry, Traces | L25 §3 | L25 §4 |
| GenAI semantic conventions | OpenTelemetry, Semantic conventions for generative AI | L25 §3 | L25 §4 |
| `app/run.sh` | course | L25 §4 | L25 §4 |
| `computeMetrics` | Vally docs, Writing Custom Executors | L26 §2 | L26 §4 |
| `plugins` | Vally docs, .vally.yaml reference | L26 §2 | L26 §4 |
| trace context | W3C Trace Context | L26 §3 | L26 §4 |

No coined terms. Rev 2 adds none: "cost per passing trial" and "pairwise judge" are plain descriptions, and their rows name the source's own term.

Where the earlier course used a name of its own, this plan uses a plain description:

| Earlier name | Plain description used instead |
|---|---|
| "the leak" | the eval files are copied into the agent's workspace |
| "golden direction", "prove both ways" | with the golden patch applied; without it |
| "cost ladder", "cheap loop" | cheapest check first |
| "near-miss negative" | near-miss request |
| "fires" | loads |
| "recitation stimulus", "self-report stimulus", "specimen", "second cue" | not needed: they described the terminal-ui example |

"Negative control" is Vally's own heading for the `--no-golden-input` run. Lesson 7 says so once and otherwise writes "without the golden patch".

## Recall and practice across the sequence
- Real practice starts in lesson 1 and every lesson's checkpoint runs or edits the real thing.
- Interleaving: reading a patch (L1) returns in L3, L4, L7 and L11; `vally grade` (L8) returns in L12, L14, L18, L23 and L25; variants (L10) return in L15, L16 and L17; `vally oracle` (L7) returns in L8 and L21; tokens (L2) return in L10, L15, L16, L17 and L19; the grading environment (L6) returns in L22.
- Community: lessons 4, 13, 15 and 16 reach questions of judgement and point to the communities in `RESOURCES.md`.

## What the real runs taught, and where it is taught correctly
- Model names come from the reader's account list: L1 §4, with the course's pair and its checked-on date on the course home.
- Limit parallel workers: L3 §3, taught as the cause of ERROR.
- `--workspace` cannot be combined with several models (the kept folders collide): L6 §2, which keeps a workspace for one model.
- The graded-record field names (`.gradeResult.stimulusName`, `.gradeResult.details[]`): L12 §2 shows an annotated excerpt of a graded record. A one-line query is offered afterwards as an optional aside.
- A grader that is wrong: L7 tests both directions with the oracle, and L8 shows a real case from writing this course, a pattern that passed the oracle and could never fail. In about 150 real trials with the changelog skill no grader failed a correct answer, so the course does not stage one; L7 says what that would look like and how the oracle catches it.
- Rev 2: `cost` is recorded only for Copilot calls and leaves out judge calls: L16 §2. Script graders cannot be re-graded (NOTES), so L18's budgets and L23's `tool-calls` are re-graded, and L22's hidden test is not.

## Spikes before authoring (cheap, mostly free)
- S1. Per-variant total cost: does the experiment's `report.md` give it, or does L16 need a small cost calculator in `assets/` (like the range calculator)? The course rule is "show files, do not query them".
- S2. A plain-JavaScript executor plugin, loaded through `.vally.yaml` `plugins.executor`, that runs a small app built on the Copilot SDK and returns a trajectory that `tool-calls` and `token-budget` can grade.
- S3. The app writes OpenTelemetry spans to a file (the Copilot SDK takes a telemetry setting), a short converter turns them into ATIF, and `vally grade --workspace` accepts the result.
- S4. A provider block that works for L17 (was 18) with tool calls (local Ollama is installed here with `gpt-oss:20b`).
- S5. `vally simulate record` on a saved trial, and `simulation` making `git log` fail under `copilot-sdk`.
- S6. `commands:` ordering: whether files staged by `commands:` count as the starting state for the diff (the docs say the baseline is taken after setup).

## Other work in revision 2
- Syntax highlighting in code blocks: add a language to every `<pre><code>`, load a highlighter pinned from cdnjs, match colours to the existing code card in light and dark, and leave console output plain.
- `MISSION.md`: add the cost and app outcomes to "Success looks like", widen the subject map, move "an executor plugin in plain JavaScript" out of "Out of scope" (custom graders and reporters stay out), and change the time to about five and a half hours in twenty-six lessons.
- MCP servers (`mcpServers`) appear on the eval file cheat sheet only: writing an MCP server is a detour from evaluating one.

## Reference sheets
- eval-file-cheatsheet.html: every eval file field the course used, from lessons 2, 5, 6, 7, 11, 12, 14, 17, 18, 22 and 24, with the experiment file from lessons 10 and 16. Rev 2 adds `scoring`, `constraints`, `provider`, `commands:`, `git:`, `env:`, `mcpServers` (not taught), `simulation`.
- results-folder-map.html: where each fact about a run lives, from lessons 1, 2, 9 and 12. Rev 2 adds `tokenUsage` and `cost`, with the nano-AIU → AIU → dollars conversion and the date the rate was checked.
- grader-catalog.html: the graders the course used and the rest of the built-in list. Rev 2 moves `run-command`, `tool-calls`, `max-repeat`, `loop-outcome` and the budget graders to "used", and adds the 1 to 5 judge.
- cli-cheatsheet.html: every command and flag the course used, in cheapest-first order. Rev 2 adds `vally compare`, `vally simulate record`, `vally grade` with an ATIF file.
- judges-and-statistics.html: writing and measuring a judge, and reading small counts, from lessons 12 to 15. Rev 2 adds scaled scores and pairwise comparison (L19).
- eval-design-checklist.html: the questions to ask of a new eval. Rev 2 adds cost, budgets, the path taken and failing tools.
- troubleshooting.html (new): symptom, where to look, likely cause and fix, from lesson 20 and the Debugging Evals guide.
- evaluating-an-app.html (new): inside Vally or after the fact, the ATIF fields the course used, a span-to-ATIF mapping table, and the executor skeleton, from lessons 22 to 26.
- workflow-guide.html: improving a skill with evals, from a new skill to a quick and a full suite. Rev 2 adds a cost step, budgets, the regression gate and a debugging detour. Includes a continuous integration snippet marked as not run by us.
- Removed: extension-interfaces.html (custom graders and reporters remain out of scope; the executor is covered by evaluating-an-app.html).
