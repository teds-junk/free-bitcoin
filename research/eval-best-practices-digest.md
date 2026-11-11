# Evals for LLM Applications and AI Agents: A Cited Best-Practice Digest

Compiled 2026-09-10 for course grounding. Every claim below is tied to a source I fetched in this session; `[S#]` tags refer to the source list. Direct quotes are in quotation marks. Where a source fetch was partial or the extraction was inconsistent, that is flagged in **Verification notes** at the end. Derived arithmetic (not quoted from a source) is labelled "(derived)".

---

## 1. Source list

### Tier A: Lab / vendor primary guidance

| ID | Title | Author(s) | URL | Date | Trust note |
|---|---|---|---|---|---|
| S1 | Demystifying evals for AI agents | Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe (Anthropic) | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-01-09 | Anthropic engineering blog; the most complete lab-authored treatment of agent evals (terminology, grader types, pass@k vs pass^k, isolation). |
| S2 | Define success criteria and build evaluations (success-criteria section) | Anthropic docs | https://platform.claude.com/docs/en/test-and-evaluate/define-success | living doc, fetched 2026-09-10 | Official docs; basic but authoritative on criteria properties and multidimensional targets. |
| S3 | Define success criteria and build evaluations (develop-tests section) | Anthropic docs | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | living doc, fetched 2026-09-10 | Official docs; aimed at prompt-level evals, with example code graders. Grading-section extraction was inconsistent (see notes). |
| S4 | Skill authoring best practices | Anthropic docs | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | living doc, fetched 2026-09-10 | Official guidance specifically for Agent Skills, including "Build evaluations first". |
| S5 | skill-creator SKILL.md | Anthropic (anthropics/skills repo) | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | fetched 2026-09-10 | Anthropic's own operational workflow for skill evals: with/without-skill baselines and trigger optimization. Primary source for skills evals. |
| S6 | Writing effective tools for AI agents | Ken Aizawa et al. (Anthropic) | https://www.anthropic.com/engineering/writing-tools-for-agents | 2025-09-11 | Anthropic engineering blog; concrete on realistic tasks, held-out sets, and cost and latency metrics. |
| S22 | Evaluation best practices | OpenAI | https://developers.openai.com/api/docs/guides/evaluation-best-practices | living doc, fetched 2026-09-10 | Official OpenAI docs; lists anti-patterns and gives architecture-specific agent advice. |
| S23 | Evaluate Gen AI agents | Google Cloud | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-agents | living doc, fetched 2026-09-10 | Official Google docs; defines trajectory metrics. Product-oriented, with less methodology. |
| S33 | Inspect AI docs (overview; scorer reference) | UK AI Security Institute & Meridian Labs | https://inspect.aisi.org.uk/ ; https://inspect.aisi.org.uk/reference/inspect_ai.scorer.html | fetched 2026-09-10 | Government safety-institute eval framework; authoritative definitions of epochs, pass_at and pass_k. |
| S29 | The End of SWE-bench Verified (podcast write-up) | Latent Space, with Mia Glaese & Olivia Watkins (OpenAI) | https://www.latent.space/p/swe-bench-dead | 2026-02-23 | OpenAI researchers speaking on the record. The original OpenAI post (https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) returned 403, so I used this instead. |

### Tier B: Practitioner experts

| ID | Title | Author(s) | URL | Date | Trust note |
|---|---|---|---|---|---|
| S8 | AI Evals: Everything You Need to Know (FAQ) | Hamel Husain, Shreya Shankar | https://hamel.dev/blog/posts/evals-faq/ | 2025-05-28, modified 2026-09-01 | The most-cited practitioner reference. Authors teach the top evals course and have consulted for 50+ companies [S13]. Opinionated. |
| S9 | FAQ: How do I evaluate agentic workflows? | Hamel Husain, Shreya Shankar | https://hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-agentic-workflows.html | 2025-06-29, modified 2026-09-01 | Same authors; source for the transition failure matrix. |
| S10 | Using LLM-as-a-Judge for Evaluation: A Complete Guide (formerly "Creating a LLM-as-a-Judge That Drives Business Results") | Hamel Husain | https://hamel.dev/blog/posts/llm-judge/ | 2024-10-29 | Step-by-step "critique shadowing" method; widely referenced. |
| S11 | Your AI Product Needs Evals | Hamel Husain | https://hamel.dev/blog/posts/evals/ | 2024-03-29 | Origin of the three-level (unit, human/model, A/B) eval tiering. |
| S12 | A Field Guide to Rapidly Improving AI Products | Hamel Husain | https://hamel.dev/blog/posts/field-guide/ | 2025-03-24 | Anti-patterns ("tools trap", generic metrics) drawn from consulting. |
| S13 | Evals Skills for Coding Agents | Hamel Husain, Shreya Shankar | https://hamel.dev/blog/posts/evals-skills/ | 2026-03-02, modified 2026-08-31 | Their methodology packaged as agent skills. Now lives at github.com/ai-evals-course/evals-skills. |
| S14 | write-judge-prompt SKILL.md | ai-evals-course (Husain & Shankar) | https://raw.githubusercontent.com/ai-evals-course/evals-skills/main/skills/write-judge-prompt/SKILL.md | fetched 2026-09-10 | Their judge-writing rules in their most prescriptive, operational form. |
| S15 | validate-evaluator SKILL.md | ai-evals-course (Husain & Shankar) | https://raw.githubusercontent.com/ai-evals-course/evals-skills/main/skills/validate-evaluator/SKILL.md | fetched 2026-09-10 | Concrete TPR/TNR thresholds, data splits and bias correction. |
| S16 | judgy (Python package) | ai-evals-course | https://github.com/ai-evals-course/judgy | fetched 2026-09-10 | Reference implementation of judge bias correction with confidence intervals (MIT license). |
| S18 | In Defense of AI Evals, for Everyone | Shreya Shankar (with Hamel Husain, Bryan Bischof) | https://www.sh-reya.com/blog/in-defense-ai-evals/ | 2025-09-05 | Responds to the 2025 "anti-evals" debate; useful for the contested-points section. |
| S19 | Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge) | Eugene Yan | https://eugeneyan.com/writing/llm-evaluators/ | 2024-08 | Literature survey of judge reliability and biases; author is a well-known applied-ML practitioner. |
| S20 | Task-Specific LLM Evals that Do & Don't Work | Eugene Yan | https://eugeneyan.com/writing/evals/ | 2024-03 | Evidence-based on which metrics separate good from bad outputs. |
| S21 | An LLM-as-Judge Won't Save The Product—Fixing Your Process Will | Eugene Yan | https://eugeneyan.com/writing/eval-process/ | 2025-04 | Argues evals are a process (scientific method), not a tool. |
| S34 | Statistics for LLM Evals (statsforevals.com) | Ian Arawjo (Université de Montréal) | https://statsforevals.com/ | updated 2026-08 | Academic HCI researcher (ChainForge, EvalGen co-author). A practical stats library and guide. |
| S35 | LLM Evaluation Guidebook | Clémentine Fourrier & Hugging Face community | https://github.com/huggingface/evaluation-guidebook | 2024; GitHub copy unmaintained since Dec 2025 (maintained version on HF Spaces) | From the former lead of the HF Open LLM Leaderboard. Benchmark-oriented; covers contamination and reproducibility. |

### Tier C: Peer-reviewed / arXiv research

| ID | Title | Author(s) | URL | Date | Trust note |
|---|---|---|---|---|---|
| S7 | Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations | Evan Miller (Anthropic) | https://arxiv.org/abs/2411.00640 | 2024-11-01 (v1) | Canonical eval-statistics paper; read in full (pp. 1-8). |
| S17 | Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences | Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya Parameswaran, Ian Arawjo | https://arxiv.org/abs/2404.12272 | 2024-04-18 | UC Berkeley HCI study; origin of the term "criteria drift". |
| S24 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | Lianmin Zheng et al. | https://arxiv.org/abs/2306.05685 | 2023-06 (NeurIPS 2023 D&B) | Foundational judge-bias paper (position, verbosity, self-enhancement). |
| S25 | How to Correctly Report LLM-as-a-Judge Evaluations | Chungpa Lee, Thomas Zeng, Jongwon Jeong, Jy-yong Sohn, Kangwook Lee | https://arxiv.org/abs/2511.21140 | 2025-11-26, rev. 2026-05-31 (ICML 2026) | Peer-reviewed statistical correction for judge bias. |
| S26 | Evaluating Large Language Models Trained on Code (Codex / HumanEval) | Mark Chen et al. (OpenAI) | https://arxiv.org/abs/2107.03374 | 2021-07 | Origin of the pass@k metric and its unbiased estimator. |
| S27 | τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains | Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan | https://arxiv.org/abs/2406.12045 | 2024-06-17 | Origin of pass^k; grades on final database state. |
| S28 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Carlos E. Jimenez et al. | https://arxiv.org/abs/2310.06770 | 2023-10 (ICLR 2024) | Canonical coding-agent benchmark; grading with fail-to-pass and pass-to-pass tests. |
| S30 | Recent Frontier Models Are Reward Hacking | Sydney Von Arx, Lawrence Chan, Beth Barnes (METR) | https://metr.org/blog/2025-06-05-recent-reward-hacking/ | 2025-06-05 | Independent evaluation org; empirical evidence that agents game graders. |
| S31 | AI Agents That Matter | Sayash Kapoor, Benedikt Stroebl, Zachary Siegel, Nitya Nadgir, Arvind Narayanan (Princeton) | https://arxiv.org/abs/2407.01502 | 2024-07-01 | Makes the case for cost-controlled evals and holdouts against overfitting. |
| S32 | Defeating Nondeterminism in LLM Inference | Horace He et al. (Thinking Machines Lab) | https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ | 2025-09-10 | Explains why temperature 0 is still nondeterministic, with measured results. |

### Community sources

| ID | Title | URL | Trust note |
|---|---|---|---|
| S36 | AI Evals For Engineers & PMs (Maven course page) | https://maven.com/parlance-labs/evals | Vendor page, so its numbers are self-reported. |
| S37 | Latent Space community page | https://www.latent.space/p/community | Self-description. |
| S38 | EleutherAI lm-evaluation-harness README | https://github.com/EleutherAI/lm-evaluation-harness | Project README. |

---

## 2. Error analysis and failure taxonomies

**Core principle: error analysis comes before you write any automated eval.** "Error analysis helps you decide what evals to write in the first place." [S8]

**Process [S8]:**
1. **Open coding.** Read traces and write free-text notes on what went wrong.
2. **Axial coding.** Group the notes into failure categories (a taxonomy).
3. **Iterate** until new traces stop producing new categories. "We recommend reviewing at least 100 traces. Continue past 100 while you are still learning" and "Continue until new traces stop revealing failure modes or changing existing ones. Qualitative researchers call this theoretical saturation." [S8]
4. **Count failures per category** and prioritise. In one engagement, "Three issues accounted for over 60% of all problems." [S12]

**Working rules:**
- **In multi-turn and agent traces, tag the *first* failure.** Upstream errors cascade, so later symptoms mislead root-cause analysis. Tag all independent failures only once patterns stabilise. [S8]
- **Use a transition failure matrix for agents.** Rows are the last successful state and columns are where the first failure occurred. This shows which step transitions concentrate failures (the example shows 12 failures on one transition versus 2 on others). [S9]
- **Start agent analysis black-box.** "Treat the agent as a black box and decide whether it met the user's goal." Drop to step-level diagnostics (tool selection, parameter extraction, error handling, context retention, efficiency) only for workflows that error analysis flags. [S9]
- **Read transcripts to judge the eval as well as the agent.** "When a task fails, the transcript tells you whether the agent made a genuine mistake or whether your graders rejected a valid solution." [S1]
- **Appoint one domain expert (a "benevolent dictator")** as the quality arbiter, instead of labelling by consensus. [S8] Hamel calls this person the "principal domain expert" in [S10].
- **Require written critiques with every pass/fail label,** detailed enough that "a new employee could understand it." [S10]
- **Build a custom annotation or trace viewer.** "This is the single most impactful investment you can make for your AI evaluation workflow." [S8] Custom-viewer teams "iterate 10x faster" per [S12] (a claim from Hamel's consulting experience, not a controlled study).
- **Budget for it.** "we've spent 60-80% of our development time on error analysis and evaluation." [S8]
- **Keep some random sampling of production traces** alongside targeted sampling, so you can find failure modes you don't yet know about. [S8]
- **Agent-assisted discovery:** the `error-discovery` / `error-analysis` skill has a coding agent build a review app, sample traces intelligently, cluster your notes into failure modes, and find similar examples. [S13]

---

## 3. Defining success criteria

**Good criteria have four properties [S2]:**
- **Specific:** "Instead of 'good performance,' specify 'accurate sentiment classification.'"
- **Measurable:** quantitative metrics, or well-defined qualitative scales used consistently.
- **Achievable:** based on benchmarks, prior experiments or expert knowledge.
- **Relevant:** tied to the application's purpose. "Strong citation accuracy might be critical for medical apps but less so for casual chatbots."

**Make criteria multidimensional.** "Most use cases need multidimensional evaluation along several success criteria." [S2] The Anthropic docs example is: F1 ≥ 0.85 on a held-out set of 10,000 posts; 99.5% non-toxic; "90% of errors would cause inconvenience, not egregious error"; "95% response time < 200ms". [S2]

**Standard criteria checklist:** task fidelity (including edge cases), consistency, relevance and coherence, tone and style, privacy preservation, context utilisation, **latency**, **price**. [S2]

**Test your task definitions:**
- **Two-expert test:** "A good task is one where two domain experts would independently reach the same pass/fail verdict." [S1]
- **Reference solution:** write "a known working output that passes all graders". This proves the task is solvable and the graders are wired correctly. [S1]

**Expect criteria to change once you see outputs.** Shankar et al. found "users need criteria to grade outputs, but grading outputs helps users define criteria" (criteria drift) [S17]. Hamel draws the practical conclusion: "It is impossible to completely determine evaluation criteria prior to human judging of LLM outputs" [S12, citing S17]. So write draft criteria, grade real outputs, then revise the criteria.

**Set the bar by risk.** High-risk, external-facing uses (medical, financial) need strict thresholds. Low-risk internal uses can tolerate, for example, "5-10% factual inconsistency." "Don't be paralyzed by the need for perfection." [S20]

**Represent partial success where it matters.** A support agent that verifies the customer but fails to process the refund "is meaningfully better than one that fails immediately. It's important to represent this continuum of success in results." [S1] This conflicts with strict-binary advice; see the contested-points section.

---

## 4. Dataset and stimulus design

**Start small, from real failures:**
- "20-50 simple tasks drawn from real failures is a great start." [S1]
- Source tasks from the manual checks you already do, bug trackers and support queues. [S1]
- "Log everything: Log as you develop so you can mine your logs for good eval cases." [S22]
- Feed production failures back into CI as regression tests. [S8]

**Match real traffic:**
- OpenAI lists "Biased design: Creating eval datasets that don't faithfully reproduce production traffic patterns" as an anti-pattern. [S22]
- "Design evals that mirror your real-world task distribution." [S3]
- Tasks "should be inspired by real-world uses and be based on realistic data sources and services." [S6]

**Use realistic, multi-step tasks for agents [S6]:**
- Strong: "Customer ID 9182 reported three charges for one purchase. Find all relevant log entries and determine if other customers were affected."
- Weak: "Search the payment logs for `purchase_complete`."
- Skill test prompts should be "the kind of thing a real user would actually say", with file paths, personal context and column names. [S5]

**Include edge cases.** The list in [S3]:
- irrelevant or nonexistent input data
- overly long input
- poor, harmful or irrelevant user input (for chat)
- "Ambiguous test cases where even humans would find it hard to reach an assessment consensus"

**Include positive AND negative cases:**
- "Test both the cases where a behavior should occur and where it shouldn't." Class-imbalanced evals create one-sided optimisation pressure. Anthropic's example is web-search evals that include queries that *should* trigger search (weather) and queries that *shouldn't* (answerable from training data). [S1]
- **Skill triggering:** build should-trigger and should-not-trigger query sets. "The most valuable ones are the near-misses — queries that share keywords or concepts with the skill but actually need something different." Should-not-trigger queries that are obviously irrelevant test nothing. [S5]
- For judge calibration data, aim for roughly balanced Pass/Fail examples even if production prevalence differs [S15]. Yan suggests "ideally 50:50 pass/fail splits" when annotating [S21].

**Synthetic data: structure it, and know when to avoid it [S8]:**
- **Define dimensions** first, where each dimension captures one kind of variation. For example, a support bot might have Issue Type × Customer Mood × Prior Context. Generate *tuples* of dimension values, then turn each tuple into a natural-language query in a separate step. [S8]
- An equivalent framing is **features × scenarios × personas.** Keep generating until you stop seeing new failure modes. [S10]
- **Avoid synthetic data** for complex domain documents (legal filings, medical records), low-resource languages, high-stakes applications, or underrepresented user groups, where you can't validate it. [S8]
- OpenAI is more permissive: use a strong model "to generate a diverse set of test data across various scenarios." [S22]

**Size:** "More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals." [S3] For statistical power, see §8.

---

## 5. Grader hierarchy: code first, LLM judge second, human third

**Know the three grader types [S1]:**

| Grader | Methods | Strengths | Weaknesses |
|---|---|---|---|
| Code-based | exact/regex/fuzzy match, unit tests, static analysis, outcome verification, tool-call verification | "Fast, Cheap, Objective, Reproducible, Easy to debug" | Brittle to valid variations, lack nuance |
| Model-based | rubrics, natural-language assertions, pairwise comparison, reference-based, multi-judge consensus | Flexible, captures nuance, handles freeform output | Non-deterministic, costlier, "requires calibration with human graders" |
| Human | SME review, spot checks, A/B tests, inter-annotator agreement | Gold standard; used to calibrate model graders | Expensive, slow, hard to scale |

**Use them in this order:**
1. **Deterministic checks first.** Hamel's Level 1 is scoped assertions that "run fast and cheaply as you develop". He lists skipping Level 1 as a common mistake. [S11] For skills: "For assertions that can be checked programmatically, write and run a script rather than eyeballing it." [S5] Anthropic's docs rank code-based grading as "fastest and most reliable, extremely scalable" but lacking nuance (search-index corroboration only; see notes) [S3].
2. **LLM judges only for failures that persist and that code can't check.** "Focus automated evaluators on failures that persist after fixing your prompts…Only build expensive evaluators for problems you'll iterate on repeatedly." [S8] Some failure modes are "better addressed through code-based assertions rather than additional judges." [S10]
3. **Humans to calibrate judges and keep sampling.** Automated evaluators need periodic human sampling and calibration. [S21] OpenAI's matching anti-pattern is "Ignoring human feedback: Not calibrating your automated metrics against human evals." [S22]

**Guardrails and evaluators are different things [S8]:**
- **Guardrails** are synchronous, inline and cheap (regexes, schema validators, light classifiers). They block high-impact objective failures before users see them.
- **Evaluators** run asynchronously after generation and measure subjective quality.

**For coding agents, stack the graders [S1]:**
- unit tests (correctness)
- static analysis: linters, type checkers, security scanners
- outcome-state checks
- tool-call verification
- an LLM rubric for code quality beyond passing tests

---

## 6. Writing good LLM-judge rubrics and calibrating judges

**Design rules [S14]:**
- **One failure mode per judge.** "Each judge checks exactly one thing." Holistic multi-dimension judges are an anti-pattern.
- **Binary verdicts.** "Outcomes are strictly binary: Pass or Fail. No Likert scales, no letter grades, no partial credit."
- **Critique before verdict.** "Placing the critique first forces the judge to articulate its assessment before committing to a decision." OpenAI agrees: "Add reasoning and chain-of-thought as reasoning before scoring improves eval performance." [S22]
- **Precise Pass and Fail definitions,** taken from your error-analysis taxonomy.
- **Few-shot examples from the *train* split only.** Include at least one clear Pass, one clear Fail and one borderline case. Never reuse dev or test items, because that leaks data.
- **Structured output** (schema-enforced JSON with a critique field and a verdict field).

**Why binary rather than Likert.** "Binary evaluations force clearer thinking and more consistent labeling. Likert scales introduce significant challenges: the difference between adjacent points (like 3 vs 4) is subjective and inconsistent across annotators." [S8] Yan: "Where possible, I have my evaluators return binary outputs." [S19]

**Calibration protocol [S15]:**
1. Get expert (not crowdsourced) labels. Split them into **train 10-20% / dev 40-45% / test 40-45%**, with **30-50 examples of each class** across dev and test.
2. Measure **TPR** = judge-Pass ∧ human-Pass / human-Pass, and **TNR** = judge-Fail ∧ human-Fail / human-Fail.
3. **Target TPR > 90% and TNR > 90%** (floor 80% each). Don't use raw accuracy or percent agreement: "with class imbalance, raw accuracy is misleading."
4. Iterate on dev. Examine false passes and false fails separately. Touch test once, at the end. "Do not tune on test data."
5. Hamel's earlier version of the method: send the expert a spreadsheet of judge verdicts and critiques, refine the prompt on disagreements, and aim for ">90% alignment". [S10] He later sets the ~100-200 labelled examples per failure mode figure in [S8].

**Correct the judge's bias when reporting rates:**
- **Rogan-Gladen correction:** θ̂ = (p_obs + TNR − 1) / (TPR + TNR − 1), reported with a confidence interval. "A point estimate alone is not enough." [S15]
- `judgy` implements this with bootstrap CIs. [S16]
- Lee et al. (ICML 2026) show that "imperfect sensitivity and specificity of the LLM judges induce bias in naive evaluation scores". They give a plug-in correction whose CIs account for uncertainty in both the test set and the calibration set. [S25]

**Choosing a judging format [S19]:**
- **Direct scoring** for objective criteria (factuality, policy violations).
- **Pairwise comparison** for subjective criteria (tone, persuasiveness). It is more stable.
- **Reference-based** when a gold answer exists.
- Evaluate the judge with classification metrics (precision, recall, Cohen's κ) rather than correlation metrics, which "don't account for chance agreement and thus could be overoptimistic."

**Known judge biases [S24]:**
- **Position, verbosity, self-enhancement bias,** and limited reasoning.
- Yan's summary of the literature: claude-v1 and gpt-3.5 "preferred the longer response more than 90% of the time". Self-enhancement gave GPT-4 about a 10% higher win rate and claude-v1 about 25% (older models). [S19]
- On the other hand, strong judges reach ">80% agreement" with human preferences, comparable to human-human agreement. [S24]
- Overall, LLM evaluators are "not reliable enough to systematically replace human judgments" without task-specific validation. [S19]

**Other judge-prompt anti-patterns [S10]:** no critiques in the few-shot examples; terse critiques; missing context the expert relied on (user metadata, system info); low example diversity.

**Don't adopt off-the-shelf judge prompts unvalidated.** Validate against human labels first (said in the RAG context). [S8]

---

## 7. Grading outcomes and environment state vs trajectories

**Default to grading the outcome.** "It's often better to grade what the agent produced, not the path it took." Checking for specific tool-call sequences "can be too rigid" and penalises valid approaches nobody anticipated. [S1]

**Grade end state, not claims:**
- The *outcome* is "Final environmental state at trial end (e.g., whether a reservation exists in a database)." [S1]
- **τ-bench** "compares the database state at the end of a conversation with the annotated goal state." [S27]
- **SWE-bench** applies the patch and runs **fail-to-pass** tests (the fix works) and **pass-to-pass** tests (nothing regressed). [S28]
- **WebArena** checks URL/page state plus backend state. **OSWorld** checks file system, app config, DB contents and UI properties. [S1]

**Beware graders that are too narrow or too wide:**
- In OpenAI's audit of SWE-bench Verified, 49 of 138 problematic tasks had tests "too narrowly defined", rejecting functionally correct solutions. 26 were "too wide", requiring undisclosed features. [S29]
- Anthropic's CORE-Bench example went from 42% to 95% once rigid grading ("96.124991…" vs "96.12") and ambiguous specs were fixed. [S1]

**Use trajectory checks for diagnosis and hard constraints, not as the headline score:**
- Google's trajectory metrics [S23]:
  - **exact match:** identical tool calls, same order
  - **in-order match:** all reference calls in order, extras allowed
  - **any-order match**
  - **precision:** fraction of predicted actions that are relevant
  - **recall:** coverage of required actions
  - **single-tool-use**
- **Tool calls, per Hamel [S9]:** "Test the tool name, arguments, result, and resulting state as separate checks." Also verify authorisation and preconditions, since a technically valid call may still be inappropriate.
- **Tool calls, per OpenAI [S22]:** evaluate tool selection, "Data precision" (correct arguments) and, for multi-agent systems, "Agent handoff accuracy".
- **Efficiency signals:** "lots of redundant tool calls might suggest some rightsizing of pagination." [S6]

**Isolate trials:**
- "Each trial should be 'isolated' by starting from a clean environment." Leftover files, caches or resource exhaustion cause correlated, infrastructure-driven failures. [S1]
- Anthropic saw "Claude gaining an unfair advantage on some tasks by examining the git history from previous trials." [S1]
- Inspect supports sandboxes (Docker, Kubernetes, Modal, etc.) for untrusted agent code. [S33]

---

## 8. Non-determinism, multiple trials, pass@k vs pass^k, and statistics

**Terminology.** A *trial* is one attempt at a task. Multiple trials are needed "since model outputs vary between runs." [S1]

**Temperature 0 is not determinism:**
- One 235B model produced **80 unique completions out of 1,000** temperature-0 requests, diverging at token 103. The main cause is lack of batch invariance as server load changes. [S32]
- Miller: "Don't touch the thermostat!" Lowering temperature to cut variance can shift variance into the conditional means, or bias the estimate. Only change temperature if you mean to study the model at that temperature. [S7]

**pass@k vs pass^k:**
- **pass@k** is the probability of at least one success in k trials. Introduced with HumanEval using an unbiased estimator from n ≥ k samples [S26]. Codex went from 28.8% at 1 sample to 70.2% at 100 samples [S26].
- **pass^k** is the probability that *all* k trials succeed. Introduced by τ-bench to measure reliability. GPT-4o "succeed[s] on <50% of the tasks" and has "pass^8 <25% in retail." [S27]
- "At k=1, they're identical … By k=10, they tell opposite stories: pass@k approaches 100% while pass^k falls to 0%." Use pass@k when one success is enough, such as tools a human retries. Use pass^k for customer-facing agents that need consistency. [S1]
- (derived, assuming independent trials with per-trial success p) pass@k = 1 − (1 − p)^k and pass^k = p^k. At p = 0.8 and k = 5: pass@5 ≈ 99.97%, pass^5 ≈ 32.8%.
- **Tooling:** Inspect's `pass_at` reducer is the "Probability of at least 1 correct sample given `k` epochs". Its `pass_k` reducer is the "Probability that all `k` epoch attempts succeed", computed as "the draw-without-replacement estimator `C(correct, k) / C(total, k)`". Epochs repeat each sample and reducers (mean, median, mode, max, at_least) combine the scores. [S33]

**Miller's five recommendations [S7, p.2]:**
1. "Computing standard errors of the mean using the Central Limit Theorem."
2. "When questions are drawn in related groups, computing clustered standard errors."
3. "Reducing variance by resampling answers and by analyzing next-token probabilities."
4. "When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics."
5. "Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest."

**How to apply them [S7]:**
- **Report the question count and the SE in parentheses** next to every score. 95% CI = mean ± 1.96 × SE. For binary scores, SE = √(p̄(1−p̄)/n). Bootstrapping is "unnecessary unless a complicated sampling scheme or estimator is being used."
- **Cluster your SEs** when tasks share a passage, repo or template. On real Anthropic data, clustered SEs were **up to 3.05× larger** than naive ones.
- **Resample answers K times per question** and compute SE over question-level means. **Don't** pool all K×N answers as if independent. In the worked example, K = 2 cuts variance by 1/3, K = 4 by 1/2, and gains flatten beyond that.
- **Compare models with paired differences** on the same questions. Report the difference, its SE, the CI and the correlation. This is a "free" variance reduction.
- The hypothetical Table 5 shows why: a +2.5% gap on one eval is significant, while −3.1% on HumanEval (164 questions) is not.
- **Small evals need wide error bars.** In Miller's Table 2, HumanEval's 164 questions give SE ≈ 3%.

**Stats in practice:**
- Arawjo's statsforevals.com offers "reasonable statistical defaults for comparing models and prompts." The site claims "only 16% conducted any statistical tests" across 445 benchmarks (the site's figure; I didn't trace its primary source). [S34]
- Skill-creator reports pass rate, time and tokens as **mean ± stddev** with deltas against a baseline. It runs each trigger query **3 times** to get a reliable trigger rate. [S5]

**Tell flakiness apart from capability:**
- "With frontier models, a 0% pass rate across many trials (i.e. 0% pass@100) is most often a signal of a broken task, not an incapable agent." [S1]
- Shared environment state produces correlated infrastructure failures. [S1]
- "Failures should seem fair: it's clear what the agent got wrong and why." [S1]

---

## 9. Capability vs regression evals, and saturation

**Keep two suites [S1]:**
- **Capability evals** ask "What can this agent do well?" They "should start at low pass rates", targeting headroom.
- **Regression evals** ask "Does the agent still handle tasks it used to?" They "should maintain near 100% pass rates."

**Watch for saturation:**
- Saturation means the agent passes every solvable task, so the eval gives no improvement signal. "As evals approach saturation, progress will also slow, as only the most difficult tasks remain." [S1]
- Hamel's version: "If you're passing 100% of your evals, you're likely not challenging your system enough." [S8]
- Public-benchmark case study: OpenAI stopped reporting **SWE-bench Verified** in 2026. Frontier models cluster around 80%, over 60% of the audited remaining problems were unsolvable, and contamination was evident (models reproduced problem statements from task IDs alone). OpenAI recommends SWE-bench Pro instead. [S29]

**Keep the pipeline fresh:** add production failures to CI as regression tests [S8], and "grow the eval set over time" through continuous evaluation [S22].

**Treat the suite as a maintained artifact:**
- "An eval suite is a living artifact that needs ongoing attention and clear ownership." [S1]
- Recommended split: a dedicated evals team owns the infrastructure, while domain experts and product teams contribute most tasks. [S1]

**Evals pay off at model upgrades.** "Teams without evals face weeks of testing while competitors with evals can quickly determine the model's strengths, tune their prompts, and upgrade in days." [S1]

---

## 10. Eval-driven development loops and CI tiers

**Tiering by cost and cadence (Hamel's three levels) [S11]:**
- **Level 1: unit tests and assertions.** Every code change; cheap and fast.
- **Level 2: human and model evals on logged traces.** On a cadence; calibrate model critiques against humans.
- **Level 3: A/B tests.** Post-launch, for mature products with real traffic.

**CI vs production [S8]:**
- CI datasets "are small" (~100 examples). They cover core features and past-bug regressions, and "the cost of each test has to be carefully considered."
- Production: "sample live traces and run evaluators against them asynchronously", using the more expensive reference-free judges.

**A practical inner/outer loop** (synthesised from [S1], [S5], [S8], [S11]):
- **Inner loop, every change (seconds to minutes):** deterministic assertions, schema and format checks, tool-call argument checks, and the regression suite. For skills, add trigger-accuracy checks on should/should-not queries.
- **Outer loop, per PR / nightly / pre-release:** capability suite with multiple trials, calibrated LLM judges, pass^k and paired comparison against the previous version with error bars.
- **Production:** guardrails inline, async judges on sampled traces, periodic human review, A/B tests.
- Anthropic frames the layers with the Swiss Cheese Model: "no single evaluation layer catches every issue." [S1]

**EDD loop for Agent Skills [S4]:**
1. Run Claude on representative tasks *without* the skill and document failures.
2. Build three scenarios testing those gaps.
3. Measure the baseline.
4. Write minimal instructions.
5. Iterate against the baseline.

Supporting practices from the same doc [S4]:
- Checklist: "At least three evaluations created", "Tested with Haiku, Sonnet, and Opus", tested with real usage.
- Use a two-instance loop: "Claude A" refines the skill and "Claude B" uses it on real tasks, while you observe navigation (unexpected exploration paths, missed references, ignored files).

**Skill-creator loop [S5]:**
- For each test case, run with-skill and baseline subagents "in the same turn". The baseline is no skill for a new skill, or the prior snapshot for an update.
- Grade assertions into `grading.json` (`text`, `passed`, `evidence`) and aggregate pass rate, time and tokens.
- Review with a human in the viewer. Optionally run a **blind comparison** ("give two outputs to an independent agent without telling it which is which").
- **Description optimisation:** 60/40 train/test split, 3 runs per query, up to 5 rounds. Pick the best description "by test score rather than train score to avoid overfitting."

**Tool evals [S6]:** run programmatically with simple agent loops, and use held-out test sets "to ensure we did not overfit to our training evaluations."

**Treat evals as a process [S21]:** "evals aren't static artifacts or quick fixes; they're practices". The loop is observe → annotate → hypothesise → experiment → measure.

**Plan roadmaps around experiments [S12]:** "The key metric for AI roadmaps isn't features shipped—it's experiments run."

**Combine eval methods [S1]:** production monitoring, A/B tests, user feedback (sparse and self-selected), manual transcript review and systematic human studies.

---

## 11. Cost and latency as first-class metrics

- **Put cost and latency in the success criteria.** Both **latency** ("acceptable response time") and **price** (budget per call) are standard criteria. The docs' example target is "95% response time < 200ms". [S2]
- **Evaluate agents on accuracy and cost jointly.** Kapoor et al. argue that accuracy-only benchmarking has produced "unnecessarily complex and expensive" agents, and that joint optimisation can "greatly reduce cost while maintaining accuracy." [S31]
- **Collect these per task [S6]:**
  - task accuracy
  - total runtime of tool calls
  - number of tool calls
  - token consumption
  - tool errors
- **Report time and tokens next to pass rate,** as mean ± stddev and as a delta against baseline. Skill-creator does this by default. [S5]
- **Include interaction-cost constraints** such as turn-count limits alongside resolution and tone for conversational agents. [S1]
- **Budget CI cost per test** because CI runs often. [S8] Reserve expensive judges for async production sampling [S8] and problems "you'll iterate on repeatedly." [S8]
- **Mind the eval method's own cost:** DOM-based computer-use interaction is faster but token-heavy, while screenshot-based is slower but token-efficient. [S1]

---

## 12. Anti-patterns

| Anti-pattern | What it looks like | Source |
|---|---|---|
| Generic / vanity metrics | Off-the-shelf "helpfulness", "coherence", BLEU, perplexity used as quality scores. "Generic evaluations waste time and create false confidence" (they can still help find traces). "Generic metrics are worse than useless—they actively impede progress." | [S8], [S12], [S22] |
| Reference-metric overreach | ROUGE, METEOR and BERTScore show poor separation between good and bad outputs. N-gram and embedding-similarity guardrails are "not discriminative enough." | [S20] |
| Vibe-based evals | "Using 'it seems like it's working' as an evaluation strategy, or waiting until you ship before implementing any evals." | [S22] |
| Tools trap | Assuming a framework or dashboard solves quality without looking at failures. Frameworks "are only as good as the eval tasks you run through them." | [S12], [S1] |
| Chasing 100% | Saturated suites give no signal. | [S8], [S1] |
| Overfitting to the eval | Tuning prompts or descriptions against the same set you report. Use held-out test sets and select by test score. Benchmarks without adequate holdouts let agents "overfit to the benchmark in various ways." | [S6], [S5], [S31] |
| Eval leakage (judge) | Few-shot examples drawn from dev or test; tuning the judge on test. | [S14], [S15] |
| Eval leakage (training contamination) | Public benchmark items in training data. Models reproduced SWE-bench Verified problem statements from task IDs. | [S29] |
| Cross-trial leakage | Shared state between trials, such as reading git history from earlier runs. | [S1] |
| Gameable graders / reward hacking | Agents modifying tests, monkey-patching timers or scorers, reading reference answers from the call stack, overriding equality operators. o3 reward-hacked in 30.4% of RE-Bench runs (100% on one task) vs 0.7% on HCAST. Design tasks so "passing genuinely requires solving the problem." METR recommends patching the scoring vulnerabilities rather than only penalising the model. | [S30], [S1] |
| Judge grading its own model unvalidated | Self-enhancement bias. Anthropic's example code: "Generally best practice to use a different model to evaluate than the model used to generate the evaluated output." | [S24], [S19], [S3] |
| Unvalidated judges | Shipping a judge with no TPR/TNR on held-out human labels; reporting raw accuracy on imbalanced data; reporting raw judge pass rates without bias correction. | [S15], [S25] |
| Holistic or Likert judges | One judge scoring many dimensions on 1-5. | [S14], [S10] |
| One-sided datasets | Only should-trigger cases, or trivially irrelevant negatives. | [S1], [S5] |
| Broken or ambiguous tasks | Unspecified file paths, over-precise expected values. Fix the task before blaming the agent. | [S1] |
| Point estimates without error bars | Declaring a winner on a 3-point gap over 164 questions. | [S7] |
| Evals written before looking at data | Writing a big eval suite up front for an unbounded failure surface. The exception is fully specifiable constraints like "never mention competitors". Contested; see §14. | [S8] |
| Premature automation | Removing human review too early; building specialised judges before error analysis. | [S10] |

---

## 13. Communities

| Community | Access | What it offers | Reputation notes |
|---|---|---|---|
| **AI Evals For Engineers & PMs Discord** (Maven course, Husain & Shankar) | Paid: comes with the course ($4,200 for the Oct 10-Nov 21, 2026 cohort) [S36] | Private Discord with lifetime access, office hours, the course reader, and the instructors' evals-skills and `judgy` tooling. | The most evals-specific high-signal community found. The course page claims 4,500+ engineers and PMs trained "from teams like OpenAI, Google, Meta, Amazon, and Microsoft" and a 4.7/5 rating across 901 reviews [S36]. Those are self-reported vendor numbers, and community-size figures vary between sources (1000+ on the course page; a search snippet said 3,000+). Instructors are Hamel Husain (ex-GitHub/Airbnb) and Shreya Shankar (UC Berkeley PhD, joining CMU faculty in 2027), who are co-writing the O'Reilly book "Evals for AI Engineers" [S36]. One trade-off: it teaches a specific, opinionated methodology [S18]. |
| **EleutherAI Discord** (#lm-thunderdome and related channels) | Free | Development and support for `lm-evaluation-harness`, plus benchmark-design discussion. [S38] | Long-standing open-source research community. Oriented to model and benchmark evaluation rather than application or agent evals. |
| **Latent Space Discord + LLM Paper Club** | Free (discord.gg/xJJMRaWCRt; weekly Wednesday paper club) [S37] | AI-engineering discussion, paper club, city meetups; linked to the AI Engineer World's Fair. | Large and influential AI-engineer audience. No dedicated evals channel is advertised [S37], but it hosts eval-relevant content such as the SWE-bench Verified retirement interview [S29]. General AI engineering, not evals-specific. |
| **Inspect AI (UK AISI) ecosystem** | Free / open source | Framework, 200+ pre-built evals, and GitHub issues and discussions (e.g. the inspect_evals repo). [S33] | Government safety-institute backing; strongest for agentic, sandboxed and safety evals. More a project ecosystem than a chat community. |
| **MLOps Community Slack** | Free | Talks and channels on LLM evaluation in production. | Large (a third-party listing cites ~27,900 members). Found via search only; I didn't fetch its own page. Broad MLOps focus, so evals content is mixed in with everything else. |
| **Arawjo's statsforevals.com** | Free | Stats guide and `evalstats` library/CLI. [S34] | Academic; a resource rather than a forum, but worth recommending to learners for the stats gap. |

Following the authors directly is a reasonable supplement to the communities above (Husain and Shankar on hamel.dev and sh-reya.com, Eugene Yan on eugeneyan.com, METR's blog).

---

## 14. Contested and evolving points

1. **Should you write evals before building?**
   - **For:** OpenAI lists "Adopt eval-driven development: Evaluate early and often" [S22]. Anthropic's skills guide says "Create evaluations BEFORE writing extensive documentation" [S4]. Yan frames EDD as TDD-like, with success criteria set up front [S21].
   - **Against:** Husain & Shankar "generally avoid writing evaluators before implementation" because the failure surface is unbounded. They discover failures first, except for fully specifiable constraints [S8].
   - **Reconciliation for teaching:** Anthropic's skills EDD step 1 is "Run Claude on representative tasks without a Skill. Document specific failures" [S4]. That is error analysis on a baseline. Both camps agree that evals should come from observed failures, not imagined ones.

2. **Binary pass/fail vs graded or partial credit.**
   - **Strictly binary:** Husain & Shankar ("No Likert scales, no letter grades, no partial credit") [S14][S8].
   - **Continuum:** Anthropic's agent post says partial success should be represented as a continuum [S1]. Anthropic's docs show Likert and ordinal LLM graders as legitimate examples [S3]. OpenAI suggests numeric scores with a pass/fail threshold for human evals [S22].
   - **One way to reconcile:** keep each judge binary per criterion, and get "partial credit" by counting criteria passed or checkpoints reached.

3. **Can the same model judge its own outputs?**
   - **Use a different model:** Anthropic's example code calls it "Generally best practice" [S3], backed by documented self-enhancement bias [S24][S19].
   - **Same model is fine:** Husain & Shankar say it is "usually fine because the judge is doing a different task…what ultimately matters is how well your judge aligns with human judgments" [S8].
   - **Common ground:** both camps would accept a same-model judge that passes held-out TPR/TNR validation.

4. **Grade outcomes or trajectories?**
   - **Outcome first:** Anthropic says grade the outcome, not the path [S1].
   - **Trajectory metrics:** Google ships exact, in-order and any-order match metrics [S23]. OpenAI recommends tool-selection, argument-precision and handoff evals [S22].
   - **Middle ground:** Husain & Shankar go black-box end-to-end first, then step-level diagnostics [S9].
   - **Emerging consensus:** outcome for the score, trajectory for diagnosis and hard constraints (authorisation, safety, cost).

5. **Volume vs curation.**
   - **More items:** Anthropic docs say "Prioritize volume over quality" [S3].
   - **Fewer, better items:** Anthropic's agent post says start with 20-50 tasks from real failures [S1]. Husain & Shankar keep CI small (~100) and emphasise reading the data [S8].
   - These partly reflect prompt-level classification (S3) versus expensive agent tasks (S1). Statistical power [S7] ultimately decides how many items you need.

6. **Synthetic data.** OpenAI encourages model-generated eval data [S22]. Husain & Shankar require dimension-structured generation and list domains where synthetic data should be avoided [S8]. Anthropic's tools post stresses realistic data sources [S6].

7. **How reliable are LLM judges?** Zheng et al. report ">80% agreement" for strong judges, on par with humans [S24]. Yan's survey concludes they are "not reliable enough to systematically replace human judgments" across tasks [S19]. Newer work treats judges as noisy classifiers needing statistical correction [S25][S16]. **The trend is away from "is the judge good?" towards "measure TPR/TNR and correct for them."**

8. **Pairwise vs direct scoring.** Yan finds pairwise more stable for subjective criteria but inapplicable to right/wrong tasks [S19]. Husain & Shankar centre on binary direct verdicts [S14]. Anthropic lists pairwise comparison as one model-grader method without ranking it [S1].

9. **Temperature and determinism.** A common instinct is to set temperature 0 for reproducible evals. Miller advises against lowering temperature to reduce variance ("Don't touch the thermostat!") [S7]. Thinking Machines shows temperature 0 is not deterministic on production endpoints anyway [S32]. Both point the same way: run multiple trials and report variance.

10. **Do you even need formal evals?**
    - Some teams in 2025 said they relied on vibes and dogfooding. Shankar's position is that "everyone already does evals" in some form (dogfooding and output review count), and that less rigour is acceptable when the task is well covered by post-training or the team has deep domain intuition [S18].
    - She concedes evals "live on a spectrum" and the course shouldn't read as "a rigid, one-size-fits-all prescription" [S18].
    - This is still a live debate, and a good framing question for a course.

11. **Is the bias correction always worth applying?** validate-evaluator says never report raw judge scores without Rogan-Gladen [S15]. Lee et al. add that CIs must include calibration-set uncertainty and give adaptive calibration-sample allocation [S25]. A search result also noted epidemiology literature warning that the estimator can have higher MSE than the naive one. I did not trace that to a primary source, so treat it as unverified.

12. **Public benchmarks as signal.** SWE-bench Verified went from the headline coding benchmark to retired within about two years, because of saturation, contamination and flawed tests [S29][S28]. Treat any public benchmark as having a shelf life, and weight private, task-specific evals more heavily.

---

## Verification notes

- **S3 (Anthropic develop-tests):**
  - Three extractions of this page disagreed. Verified verbatim: the "Prioritize volume over quality" sentence, the edge-case list, the H3 example list (exact match, cosine similarity, ROUGE-L, LLM Likert, LLM binary, LLM ordinal), and the code comment "Generally best practice to use a different model to evaluate than the model used to generate the evaluated output".
  - The grading-method ranking ("fastest and most reliable, extremely scalable") and the LLM-grading tips ("detailed, clear rubrics"; "test to ensure reliability first then scale") came only from a search engine's index of this URL. A verbatim-extraction pass could not locate them, so they may have moved or been removed.
  - I did **not** use an earlier extraction that attributed a "Don't mix multiple concepts in one evaluation" list to this page, because it could not be verified.
- **S29:** The original OpenAI post returned HTTP 403. SWE-bench Verified figures come from the Latent Space interview with OpenAI's Glaese and Watkins, consistent with search-result snippets of the OpenAI post.
- **S22:** The fetched OpenAI page names `gpt-6-astra` as its recommended judge and generator model. I've omitted model names from the guidance since they will date quickly.
- **S8:** The phrase "transition failure matrix" is not on the main FAQ page. It is in the linked agentic-workflows entry [S9]. The "100-200 labelled examples per failure mode" and "train/dev/test" split figures appeared in an extraction of S8 but were verified verbatim only in S15.
- **S34:** The "16% of 445 benchmarks" statistic is the site's claim. I didn't locate its primary citation.
- **S36:** Course numbers (students, reviews, Discord size) are self-reported on a sales page and were inconsistent across sources.
- **MLOps Community:** Membership figure is from a third-party listing found via search, not a fetched primary page.
- **Who Validates the Validators? [S17]:** I verified the arXiv record (April 2024). I did not verify its conference venue, so none is claimed.
