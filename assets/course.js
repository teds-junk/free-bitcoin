/* The one place lesson titles, files and wins are listed. lesson.js renders
   it into every page's course map, so a title is typed once.
   Filled in from COURSE-PLAN.md, one entry per lesson, in teaching order. */
window.COURSE = {
  title: 'Vally & Agent Evals',
  // The whole-course video is too big for the repo, so it lives on a GitHub release.
  video: 'https://github.com/teds-junk/free-bitcoin/releases/download/course-video-v1/vally-agent-evals.mp4',
  videoPoster: 'videos/course/poster.png',
  lessons: [
    { n: 1, file: '0001-it-works-for-me.html', title: 'It works for me', win: 'Run one request on two models and find, in the saved files, that they changed the file differently', part: 'Measure the skill' },
    { n: 2, file: '0002-what-the-tick-checked.html', title: 'What the tick checked', win: 'Explain every line of the eval file and find any run in the results folder', part: 'Measure the skill' },
    { n: 3, file: '0003-the-same-request-five-times.html', title: 'The same request, five times', win: 'State, as counts over five trials, how often each model gets it wrong', part: 'Measure the skill' },
    { n: 4, file: '0004-read-the-runs-first.html', title: 'Read the runs before writing graders', win: 'List the skill\'s failure modes, each with the trial that shows it', part: 'Measure the skill' },
    { n: 5, file: '0005-turn-a-failure-into-a-grader.html', title: 'Turn a failure into a grader', win: 'Show with three graders what one edit to the skill changed on each model', part: 'Graders you can trust' },
    { n: 6, file: '0006-keep-graders-out-of-reach.html', title: 'Keep graders out of the agent\'s reach', win: 'See what an agent is given, and add a grading script it never sees', part: 'Graders you can trust' },
    { n: 7, file: '0007-test-a-grader.html', title: 'Test a grader without running an agent', win: 'Prove with a golden patch that every grader passes correct work and fails missing work', part: 'Graders you can trust' },
    { n: 8, file: '0008-check-graders-against-saved-trials.html', title: 'Check graders against saved trials', win: 'Re-grade a saved run for free and expose a grader that could never fail', part: 'Graders you can trust' },
    { n: 9, file: '0009-does-the-skill-load.html', title: 'Does the skill load when it should', win: 'Show what rewriting the description changed, using near-miss requests', part: 'Is the skill earning its place' },
    { n: 10, file: '0010-is-the-agent-better-with-the-skill.html', title: 'Is the agent better with the skill', win: 'Compare results with and without the skill, for each model', part: 'Is the skill earning its place' },
    { n: 11, file: '0011-follow-up-requests.html', title: 'Follow-up requests', win: 'Grade a three-turn conversation turn by turn and fix what fades', part: 'Is the skill earning its place' },
    { n: 12, file: '0012-a-judge-for-what-code-cannot-check.html', title: 'A judge for what code cannot check', win: 'Write one yes-or-no LLM judge and read its reasons', part: 'Judgement and evidence' },
    { n: 13, file: '0013-check-the-judge.html', title: 'Check the judge against your own labels', win: 'Measure the judge against your labels and decide whether to rely on it', part: 'Judgement and evidence' },
    { n: 14, file: '0014-partial-credit.html', title: 'Partial credit', win: 'Re-grade with a judge scoring 1 to 5 and say which verdicts changed', part: 'Judgement and evidence' },
    { n: 15, file: '0015-is-the-change-real.html', title: 'Is the change real', win: 'Compare before and after an edit and state what the result supports', part: 'Judgement and evidence' },
    { n: 16, file: '0016-what-a-passing-trial-costs.html', title: 'What a passing trial costs', win: 'Work out the cost per passing trial for two models at two reasoning efforts', part: 'Worth what it costs' },
    { n: 17, file: '0017-a-model-from-your-own-provider.html', title: 'A model from your own provider', win: 'Run one variant through your own provider and price its tokens yourself', part: 'Worth what it costs' },
    { n: 18, file: '0018-put-a-ceiling-on-a-trial.html', title: 'Put a ceiling on a trial', win: 'Add budget graders and a time limit, each shown failing a real over-budget trial', part: 'Worth what it costs' },
    { n: 19, file: '0019-is-it-worse-than-before.html', title: 'Is it worse than before', win: 'Judge before against after side by side, with a command that fails on a regression', part: 'Worth what it costs' },
    { n: 20, file: '0020-when-a-run-goes-wrong.html', title: 'When a run goes wrong', win: 'Diagnose and fix four broken eval files with the fewest agent runs', part: 'Make it routine' },
    { n: 21, file: '0021-keep-it-working.html', title: 'Keep it working', win: 'Set up a quick suite, a full suite and a one-page conventions file', part: 'Make it routine' },
    { n: 22, file: '0022-start-the-agent-where-the-app-would.html', title: 'Start the agent where the app would', win: 'Prepare a workspace with the app\'s own setup command and grade it with a hidden test', part: 'The skill inside an app' },
    { n: 23, file: '0023-check-what-the-agent-did.html', title: 'Check what the agent did', win: 'Require and forbid steps with tool-calls graders, and catch loops', part: 'The skill inside an app' },
    { n: 24, file: '0024-when-a-tool-fails.html', title: 'When a tool fails', win: 'Make a tool fail on purpose and grade what the agent does next', part: 'The skill inside an app' },
    { n: 25, file: '0025-grade-a-run-vally-did-not-start.html', title: 'Grade a run Vally did not start', win: 'Convert the app\'s traces to a trajectory and grade it with your eval file', part: 'The skill inside an app' },
    { n: 26, file: '0026-let-vally-run-the-app.html', title: 'Let Vally run the app', win: 'Write a small executor that runs the app for each trial, and compare two models', part: 'The skill inside an app' }
  ],
  references: [
    { file: 'workflow-guide.html', title: 'Workflow guide: improving a skill with evals' },
    { file: 'cli-cheatsheet.html', title: 'Command cheat sheet' },
    { file: 'eval-file-cheatsheet.html', title: 'Eval file cheat sheet' },
    { file: 'results-folder-map.html', title: 'Results folder map' },
    { file: 'grader-catalog.html', title: 'Grader catalog' },
    { file: 'judges-and-statistics.html', title: 'Judges and small counts' },
    { file: 'eval-design-checklist.html', title: 'Eval design checklist' },
    { file: 'troubleshooting.html', title: 'Troubleshooting' },
    { file: 'evaluating-an-app.html', title: 'Evaluating a skill inside an app' }
  ],
  // Zips under downloads/, listed in the reference panel. Paths are from the workspace root.
  downloads: [
    { file: 'downloads/teach-me-skill.zip', title: 'teach-me skill', size: '78 KB', note: 'The agent skill that planned and wrote these lessons.' },
    { file: 'downloads/video-lesson-skill.zip', title: 'video-lesson skill', size: '1.2 MB', note: 'The agent skill that made the videos. Runs on an Apple Silicon Mac.' }
  ]
};
