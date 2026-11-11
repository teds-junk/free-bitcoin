# Vally & Agent Evals Resources

Checked 2026-11-09 against Vally **0.21.0**. Full, cited research lives in `research/`:

- `research/vally-0.21-repo-delta.md` — source-verified facts for 0.21 (wins conflicts), and `research/vally-0.21-cli-help.txt` — real `--help` output.
- `research/vally-0.21-docs-delta.md` — what the live docs say now, with the full URL map.
- `research/reports/AI evals latest learnings 2026.md` — the November 2026 synthesis of eval practice, with six note files in `research/research_notes/`.
- `research/vally-docs-digest.md`, `research/vally-repo-digest.md`, `research/eval-best-practices-digest.md` — the September 2026 (Vally 0.16) baseline.

Check those before relying on memory.

## Knowledge

### Vally (primary, tool-specific)
- [Get Started](https://microsoft.github.io/vally/get-started/) and [Runtime Setup](https://microsoft.github.io/vally/get-started/runtime-setup/)
  Install (`npm install -g @microsoft/vally-cli`, Node ≥ 22.15), local sign-in or token auth, first run. Use for: setup, onboarding a teammate, any "session was not created with authentication" error.
- [How It Works](https://microsoft.github.io/vally/concepts/how-it-works/) and [Why Vally](https://microsoft.github.io/vally/concepts/why-vally/)
  The Stimulus → Executor → Trajectory → Graders → Score pipeline, plus a mapping from ordinary test vocabulary. Use for: the mental model, explaining Vally to others.
- [Eval Spec Reference (eval.yaml)](https://microsoft.github.io/vally/reference/eval-spec/) and [.vally.yaml](https://microsoft.github.io/vally/reference/vally-yaml/)
  Authoritative schema. Use for: any "is this field valid?" question. Note: several onward links on this page are broken (missing `/vally/`); navigate from the sidebar instead.
- [Choose a Grader](https://microsoft.github.io/vally/guides/choosing-graders/), [Grader Catalog](https://microsoft.github.io/vally/reference/graders/), and [Grader Taxonomy](https://microsoft.github.io/vally/concepts/grader-taxonomy/)
  Evidence-first selection order, the 36 built-in graders, and which loop each belongs in. Use for: choosing graders.
- [Scoring](https://microsoft.github.io/vally/concepts/scoring/) and [Scoring Functions](https://microsoft.github.io/vally/reference/scoring-functions/)
  Weights, thresholds, when not to set them; pass@k, pass^k, flakiness. Use for: verdict semantics, choosing `runs`.
- [Debugging Evals](https://microsoft.github.io/vally/guides/debugging-evals/)
  A four-step workflow (make it valid, get it to complete, find why, verify the fix) and a troubleshoot-by-symptom table. Use for: any red or `ERROR` result.
- [CLI reference](https://microsoft.github.io/vally/reference/cli/) — especially [`grade`](https://microsoft.github.io/vally/reference/cli/grade/), [`oracle`](https://microsoft.github.io/vally/reference/cli/oracle/), [`compare`](https://microsoft.github.io/vally/reference/cli/compare/), [`experiment`](https://microsoft.github.io/vally/reference/cli/experiment/), [`simulate`](https://microsoft.github.io/vally/reference/cli/simulate/)
  Use for: re-grading without re-running agents, proving graders, A/B comparisons, replaying tool calls.
- [Run Your First Experiment](https://microsoft.github.io/vally/guides/run-your-first-experiment/)
  Two-variant walkthrough with `--dry-run` and regression gating. Use for: with/without-skill comparisons. (It says `--compare` uses the default judge; the CLI reference and source say it inherits the evals' judge settings.)
- [Authoring Eval Suites](https://microsoft.github.io/vally/guides/authoring-eval-suites/) and [Add to CI](https://microsoft.github.io/vally/get-started/add-to-ci/)
  Tags, suites, CI tiering, and the Actions-token auth that is now the recommended CI setup. Use for: team rollout.
- [Writing Custom Graders](https://microsoft.github.io/vally/guides/writing-custom-graders/), [Executors](https://microsoft.github.io/vally/guides/writing-custom-executors/), [Reporters](https://microsoft.github.io/vally/guides/writing-custom-reporters/), [`program` grader](https://microsoft.github.io/vally/reference/graders/program/)
  Extension interfaces and plugin packaging. Use for: extending Vally.
- [Release notes for 0.21.0](https://microsoft.github.io/vally/release-notes/0.21.0/) (one page per version; there is no index page)
  The upgrade source of truth, with a Breaking section per release. Use for: reading before every version bump.
- [Writing Eval Specs](https://microsoft.github.io/vally/guides/writing-eval-specs/) and [Trajectory Format](https://microsoft.github.io/vally/reference/trajectory-format/)
  The multi-turn section (`turns`, graders scoped with `turn:`) and how turns, events and per-turn diffs are recorded. Use for: evaluating conversations with follow-up requests.

- [Graders: metric thresholds](https://microsoft.github.io/vally/reference/graders/metric-thresholds/), [Grader: tool-calls](https://microsoft.github.io/vally/reference/graders/tool-calls/), [Grader: max-repeat](https://microsoft.github.io/vally/reference/graders/max-repeat/), [Grader: loop-outcome](https://microsoft.github.io/vally/reference/graders/loop-outcome/), [Grader: run-command](https://microsoft.github.io/vally/reference/graders/run-command/)
  Budgets, the path the agent took, loops, and hidden tests. Use for: lessons 17, 22 and 23.
- [Running Evals in Docker](https://microsoft.github.io/vally/guides/running-evals-in-docker/)
  The built-in isolated backend. Use for: stronger isolation than the course needs; not taught.

### Cost, telemetry and outside data (added 2026-11-10)
- [GitHub Copilot billing — GitHub Docs](https://docs.github.com/en/billing/concepts/product-billing/github-copilot-billing)
  Copilot usage is billed in AI Credits, $0.01 each (checked 2026-11-10; Vally records them as `nano-aiu`, a billion to the credit). Allowances differ by plan. Use for: turning AIU into dollars (lessons 2 and 16).
- [AI Agents That Matter — Kapoor et al., 2024-07](https://arxiv.org/abs/2407.01502)
  Agent evaluations should report cost beside accuracy and compare on the cost–accuracy frontier. Use for: cost per passing trial (lesson 16).
- [OpenTelemetry: Traces](https://opentelemetry.io/docs/concepts/signals/traces/) and [Semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
  Spans, attributes, and the `gen_ai.*` names the Copilot SDK writes. Use for: lesson 25. The GenAI conventions are still marked in development, so attribute names can change.
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
  The `traceparent` header Vally passes to an executor. Use for: lesson 26.
- [Ollama](https://ollama.com/) and its [OpenAI compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)
  A local model server with an OpenAI-style endpoint. Use for: lesson 18 (optional step).
- The Copilot SDK's README (in `node_modules/@github/copilot-sdk/README.md` after `npm install` in `practice/app`)
  Sessions, events, `skillDirectories`, `configDirectory`, and the `telemetry` file exporter. Use for: the release app in lessons 25 and 26.

### Eval practice (general, high-trust)
- [AI Evals FAQ — Hamel Husain & Shreya Shankar (reissued 2026-09-18)](https://hamel.dev/blog/posts/evals-faq/)
  The practitioner method with current numbers: read traces first, binary judges, what goes in CI, how to bring a team along. Use for: process and "what should I build first?".
- [Demystifying evals for AI agents — Anthropic (2026-01-09)](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
  Grader types, outcome vs path, pass@k vs pass^k, capability vs regression, isolation. Use for: the conceptual backbone.
- [Quantifying infrastructure noise in agentic coding evals — Anthropic (2026-02-05)](https://www.anthropic.com/research/infrastructure-noise) and [Eval awareness in BrowseComp — Anthropic (2026-03-06)](https://www.anthropic.com/research/eval-awareness-browsecomp)
  Resource limits alone moved a benchmark by 6 points; a model recognised a benchmark and found its answer key. Use for: why the environment is part of the measurement.
- [Reward hacking on coding benchmarks — Cursor (2026-06-25)](https://cursor.com/blog/reward-hacking-coding-benchmarks), [Trustworthy benchmarks — Berkeley RDI (2026-04)](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/), and [Many SWE-bench-passing PRs would not be merged — METR (2026-03-10)](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/)
  How agents and graders fail each other, and a short checklist for grader design. Use for: isolation, hidden answer keys, validating graders in both directions.
- [Using LLM-as-a-Judge — Hamel Husain](https://hamel.dev/blog/posts/llm-judge/) and the [validate-evaluator skill](https://raw.githubusercontent.com/ai-evals-course/evals-skills/main/skills/validate-evaluator/SKILL.md)
  Critique shadowing, train/dev/test labels, TPR/TNR above 90%, Rogan-Gladen correction. Use for: writing and validating judges. Read with [Fiedler 2026 (preprint)](https://arxiv.org/abs/2605.06939) on when that correction fails.
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena — Zheng et al., 2023](https://arxiv.org/abs/2306.05685)
  Pairwise judges favour one position; swapping the order and counting disagreement as a tie is the standard fix. Use for: lesson 19's side-by-side judging.
- [Adding Error Bars to Evals — Evan Miller, 2024](https://arxiv.org/abs/2411.00640), [Bowyer et al., 2025](https://arxiv.org/abs/2503.01747), and [Measuring all the noises of LLM evals — Sida Wang, 2026](https://arxiv.org/abs/2512.21326)
  Standard errors and paired comparison; why the normal interval fails at small n (use Wilson); why more trials usually beat more items. Use for: deciding whether a change is real.
- [Towards a Science of AI Agent Reliability — Princeton, ICML 2026](https://arxiv.org/abs/2602.16666) and [variance on SWE-bench Verified — KTH, 2026](https://arxiv.org/abs/2602.07150)
  Consistency lags capability; single runs move 2–6 points. Use for: choosing `runs`, reading pass^k.
- [Measuring what Matters — Bean et al., NeurIPS 2025](https://arxiv.org/abs/2511.04703)
  A review of 445 benchmarks' construct validity. Use for: asking what an eval actually measures.
- [Optimizing skill descriptions — agentskills.io](https://agentskills.io/skill-creation/optimizing-descriptions), [`claude plugin eval` docs](https://code.claude.com/docs/en/plugin-evals), and [Improving skill-creator — Anthropic (2026-03-03)](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
  The cross-vendor trigger recipe and the paired with/without-skill design. Use for: everything specific to evaluating skills.
- [SkillsBench (v4)](https://arxiv.org/html/2602.12670v4), [Gloaguen et al. on AGENTS.md files](https://arxiv.org/html/2602.11988v3), and [Vercel's skills vs AGENTS.md evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
  Measured evidence on whether skills and context files help. Use for: why uplift must be measured, not assumed.
- [Benchmarking coding agents — Snowflake](https://www.snowflake.com/en/blog/engineering/Benchmarking-coding-agents/)
  An in-repo suite built from real PRs, with an honest statement of what 65 tasks can detect. Use for: a worked example of small-suite humility.
- [Who Validates the Validators? — Shankar et al., 2024](https://arxiv.org/abs/2404.12272)
  Criteria drift: you cannot fully specify criteria before reading outputs. Use for: why error analysis comes first.

## Wisdom (Communities)

- [AI Evals For Engineers & PMs — Maven course + Discord (Husain & Shankar)](https://maven.com/parlance-labs/evals)
  The most evals-focused practitioner community found. Paid. Use for: critique of judges and error analysis from practitioners.
- [Latent Space Discord + paper club](https://www.latent.space/p/community)
  Free, large AI-engineering community; no dedicated evals channel. Use for: broader agent-engineering discussion.
- [Inspect AI (UK AISI)](https://inspect.aisi.org.uk/) and [Waza (Microsoft, open source)](https://microsoft.github.io/waza/concepts/)
  Two open eval harnesses with public discussion; Waza targets skill evals and defaults to the same Copilot SDK executor. Use for: contrast with Vally's choices.
- "Support - Vally" Teams channel (Microsoft-internal; named in the repo README)
  The maintainers' support channel. Use for: undocumented behaviour, auth problems, whether a custom grader belongs upstream.
- Team practice: the azd team (or whichever team adopts Vally). Use for: testing whether conventions survive contact with other engineers.

## Gaps

- **No public Vally community.** The source repo `microsoft/vally` is private (its URL 404s unless signed in as `tg-msft`); its issues are the closest thing.
- **No simulated user for multi-turn.** Vally 0.21 sends scripted follow-ups only; the docs describe nothing that generates a user's side of a conversation.
- **Two docs pages disagree on auth token order**, and whether the Copilot runtime still installs automatically with the CLI is unconfirmed. Lesson 1 settles both hands-on.
- **Thin evidence in the eval literature**, worth knowing before quoting it to a team: run counts for skill evals (3 runs, about 20 queries) are conventions with no power analysis; judge drift across model versions is unmeasured; the "eval flywheel" is supported by case studies only; CI gating policies for suites under about 50 cases are unvalidated.
- **No OpenTelemetry input.** Vally 0.21 sends its own spans out (`otel-spans.jsonl`, `--otlp-endpoint`) but reads no traces in; checked in source (`otel-endpoint.ts` only normalises URLs). Lesson 25 converts spans to ATIF with a short script of our own.
- **No cost totals.** Vally records cost per trial but totals it nowhere (report, run summary, dashboard); the course ships `assets/cost-calculator.js`.
- **Tooling churn:** OpenAI's hosted Evals platform shuts down on 2026-11-30 and several eval vendors were acquired in 2026. Prefer skills that transfer over features of one product.
