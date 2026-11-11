# LLM-as-a-Judge Graders: Reliability, Calibration, and Correct Use (state of knowledge, November 2026)

Research date: 2026-11-09. Baseline: `/Users/ted/src/learn/vally/research/eval-best-practices-digest.md` (compiled 2026-09-10), referred to below as "the digest". These notes concentrate on what is new or changed since then.

Reading conventions used in every bullet:

- **Evidence level:** `[peer-reviewed]`, `[workshop]`, `[preprint]`, `[practitioner]`, `[vendor]`.
- **How I read it:** `(abstract)` = I fetched the arXiv/venue page and read the abstract; `(full text)` = I fetched the HTML body; `(snippet)` = seen only in a search-result summary, not opened. Treat `(snippet)` numbers as provisional.
- All URLs returned HTTP 200 on 2026-11-09 unless a bullet says otherwise.
- Most 2026 papers here are arXiv preprints. Only four are confirmed peer-reviewed at a main venue: Lee et al. (ICML 2026), Chae et al. (EMNLP Findings 2026), and, by snippet only, the BT-sigma jury paper (ICML 2026) and the overrating study (SIGIR 2026).

## 1. Judge validity: human agreement, biases, prompt sensitivity, version stability

### Takeaway
The 2026 literature has moved from "judges agree with humans about 80% of the time" to "agreement is the wrong headline number": judges can show high agreement and still miss most real defects, flip under rewording or pushback, and favour their own outputs even on objective binary rubrics. The bias picture has also been reordered: on current frontier judges, position bias is small while formatting/style bias and authorship-label effects are large, and no single mitigation works across judge families.

### Cited Findings

**Agreement with human experts**
- Agreement metrics overstate detection. In a deployed multi-turn ordering agent, the built-in LLM judge surfaced "2 of 9 patterns (22%)" of human-confirmed systematic problems in one batch, and its operational gate flagged zero of 100 rounds in a batch where humans confirmed 23 distinct defects. The authors note judge reliability "is almost always reported as agreement with human ratings, not recall of real defects." `[preprint]` (abstract), 2026-06-09 — [Zhang, Wang, Lei, "Catching One in Five"](https://arxiv.org/abs/2606.10315)
- The same paper locates the failure in the rubric, not the model: the judge caught turn-local issues (fabricated statistic, wrong language) but missed cross-turn state issues (confirm-gate lockout, cart hallucination, stale referents), because the rubric had only three coarse axes. 113 of 114 rounds whose raw judge note described a cart/confirm-gate defect were filed under "brand voice". `[preprint]` (abstract) — [Zhang et al. 2026](https://arxiv.org/abs/2606.10315)
- Inter-rater reliability is not a licence to run statistics on judge scores. Arawjo's simulations find false-positive risk is worst at high agreement: for binary labels, Cohen's kappa = 0.81 still produced about a 37% false-positive rate when tests are run on raw judge scores; for Likert data, risk peaks around quadratic-weighted kappa 0.80-0.90 and returns to nominal only above 0.99. The paper says IRR alone "means almost nothing for trusting claims." `[preprint]` (full text, first 100k chars), 2026-09-20 — [Arawjo, "How to Run Statistics over LLM Judges and Trust the Results"](https://arxiv.org/abs/2609.35815)
- A June 2026 critique argues judge benchmarks (MT-Bench, RewardBench, JudgeBench) privilege raw agreement; it reports that judge rankings shift by up to 14 positions across benchmarks and proposes a "Minimum Viable Validation Protocol". `[preprint]` (snippet) — [Norman, Rivera, Hughes, "Reliability without Validity"](https://arxiv.org/abs/2606.19544)
- Expert-expert agreement is often the real ceiling. In the ImpactBench expert audit, the judge matched the majority expert verdict in 83.3% of reviewed cases (Cohen's kappa 0.667, 297 ratings from 19 external experts), but experts agreed with each other only 44.4%-73.3% of the time (Krippendorff's alpha 0.121-0.538) on the subset with multiple raters; 126 audited items had a single reviewer, and the judge was also one of the models being scored. `[vendor]` write-up (full text), 2026-11-04, of a `[preprint]` I did not open — [Kili Technology blog](https://kili-technology.com/blog/data-story-impactbench-llm-judge-expert-audit); primary paper [ImpactBench](https://arxiv.org/abs/2610.20690)
- Two September 2026 application papers report judge-human kappa at or below the human-human level on hard categories: judge-human 0.52 vs human-human 0.54 in one; judge kappa rising from 0.40 to 0.48 after a bias-calibration instruction against a human-human mean of 0.724 in the other. `[preprint]` (snippet) — [arXiv 2609.07662](https://arxiv.org/abs/2609.07662); [arXiv 2609.22971](https://arxiv.org/abs/2609.22971)

**Self-preference / same-family preference**
- Self-preference persists on objective, binary, per-criterion rubrics. On IFEval and LiveCodeBench, "judges can be more than 50% more likely to incorrectly mark [failed rubrics] as satisfied when the output is their own." On HealthBench the bias "skews model scores by up to 10 points." Ensembling judges "helps mitigate SPB, but without fully eliminating it." Negative rubrics and subjective topics are most susceptible. `[preprint]` (abstract), v1 2026-04-08, v3 2026-08-03 — [Pombal, Rei, Martins](https://arxiv.org/abs/2604.06996)
- Counter-evidence on mechanism: when the judged object carries no stylistic fingerprint, "under blind evaluation, self-preference disappears, with a small effect remaining in the opposite direction"; but authorship labels alone ("self" / "other", no model named) shift scores in both directions across ten LLMs. `[peer-reviewed]` EMNLP Findings 2026 (abstract), v1 2026-06-06 — [Chae et al., "Self- and Other-Labels Induce Bidirectional Bias in LLM Judges"](https://arxiv.org/abs/2608.18091)
- A decomposition-based multi-dimensional evaluation strategy is reported to reduce self-preference bias by 31.5% on average. `[preprint]` (snippet), April 2026 — [Yang et al.](https://arxiv.org/abs/2604.22891)
- Foundational (older): self-preference linked to lower perplexity of the judge's own text. `[preprint]` (snippet), October 2024 — [Wataoka et al.](https://arxiv.org/abs/2410.21819)

**Position, verbosity, formatting**
- On five 2025-era judges (Gemini 2.5 Pro, Claude Sonnet 4, GPT-4o, Gemini 2.5 Flash, Llama 3.3-70B), position bias was "≤0.04" for all models. Formatting/style bias was the largest: Pro +0.76, Flash +0.72, Claude +0.68, Llama +0.40, GPT-4o +0.10; humans preferred the markdown version 57% of the time while four judges preferred it 73%-97%. Verbosity bias varied by family (Llama +0.44, Pro +0.40, Flash +0.24, GPT-4o −0.04, Claude −0.12). `[preprint]`, single independent author (full text), v2 2026-06-24; experiments run April-June 2025 — [Soumik, "Judging the Judges"](https://arxiv.org/abs/2604.23178)
- Mitigations are model- and task-specific in that study. Chain-of-thought gave the most consistent style-bias reduction (Claude 0.68 to 0.49, Pro 0.76 to 0.60). Position-swap hurt on LLMBar (Pro −7.5 pp, GPT-4o −11.1 pp, Llama −6.5 pp). No strategy systematically reduced verbosity bias; some increased it. Best combined configuration reached 71.0% human agreement on MT-Bench. `[preprint]` (full text) — [Soumik 2026](https://arxiv.org/abs/2604.23178)
- Pairwise relevance judgments from small open models can flip under position swaps while the model reports high confidence. `[peer-reviewed]` SIGIR 2026 per search result (snippet) — [arXiv 2602.17170](https://arxiv.org/abs/2602.17170)

**Leniency, sycophancy, pressure**
- Judges are persuadable. Across 9 frontier models and 14 judging tasks, every model flipped its verdict 25-71% of the time under static pushback and 62-91% under an adversarial LLM persuader; flips "almost always" reduced accuracy. Baseline jury-majority strength best predicted which items flip. `[preprint]` (abstract), 2026-08-12 — [Zhao et al., "Jagged Judges"](https://arxiv.org/abs/2608.12645)
- Context contaminates the threshold. A completed audit-then-repair episode in the verifier's context lowered false alarms in 15 of 15 model-by-wording combinations (2.8 to 11.5 percentage points, 9-25% relative), and signal-detection analysis attributes it to a criterion shift toward leniency, not a change in discrimination. The effect held with reasoning enabled. `[preprint]` (abstract), 2026-08-17 — [Mazaheri and Mazaheri](https://arxiv.org/abs/2608.16003)
- Overrating is the direction of error documented for small pointwise judges. `[peer-reviewed]` per search result (snippet) — [arXiv 2602.17170](https://arxiv.org/abs/2602.17170)

**Prompt sensitivity and judge-choice variance**
- JudgeSense (25 judges, six providers, four tasks, 880 items issued under two semantically equivalent instructions): rewording reduces agreement on all four tasks, exceeding the authors' practical-significance threshold on two; the ordinal task is least stable; parameter count within a family does not predict stability; sensitivity is measured net of the judge's self-agreement on an identical prompt. `[preprint]` (abstract), v3 2026-09-18 — [Bellibatlu, Raff, Zhang](https://arxiv.org/abs/2604.23478)
- Standard confidence intervals ignore variance from judge model choice, temperature and prompt phrasing: "naive standard errors are 40 - 60% smaller" than the total-evaluation-error-corrected SE, and naive 95% CI coverage falls as n grows. Judge-model choice was the largest variance source under both Likert and pairwise formats (latter clause from snippet). `[preprint]` (abstract), v6 2026-05-13 — [Messing, "Hidden Measurement Error in LLM Pipelines"](https://arxiv.org/abs/2604.11581)
- A method separating prompt-to-prompt variation from repeated-call randomness exists. `[preprint]` (snippet), August 2026 — [arXiv 2608.16253](https://arxiv.org/abs/2608.16253)

**Status of the digest's claims**
- Still stands: judges are noisy classifiers needing task-specific validation (digest §14 item 7). Strengthened by all of the above.
- Needs updating: the digest's bias list (position, verbosity, self-enhancement from Zheng et al. 2023, [arXiv 2306.05685](https://arxiv.org/abs/2306.05685), foundational) should add formatting/style, authorship-label, pushback/persuasion and context-induced leniency, and should note that position bias was near zero on 2025 frontier judges in one study while still present on small models.
- Weakened: Husain and Shankar's "same model is usually fine" position (digest §14 item 3). The FAQ still says this ([hamel.dev FAQ](https://hamel.dev/blog/posts/evals-faq/)), but Pombal et al. now show the bias on exactly the binary per-criterion format they recommend.

### Inferences
- Validation should report detection (recall of known defects, TPR/TNR) rather than only agreement or kappa; three independent 2026 sources (Zhang, Arawjo, Norman) converge on this.
- The Pombal and Chae results are compatible: self-preference on real generated text is probably driven by style/familiarity plus any authorship cue. Practical consequence: strip model identity and authorship framing from judge inputs, and use a different-family judge when comparing models against each other.
- Because formatting bias exceeds position bias on modern judges, normalising output formatting before judging (or testing a markdown/plain pair) is likely a higher-value control than position swapping. This is my inference from one single-author preprint; it is not an established recommendation.
- Never show the judge prior verdicts, repair history or the agent's self-assessment unless that is the thing being graded: both the leniency-shift and persuasion results imply the verdict will move.

### Gaps
- I found no 2026 paper measuring sycophancy toward confident-sounding outputs in judges specifically. "Jagged Judges" measures pushback in a dialogue with the judge, not confidence in the graded output.
- I found no controlled study of verdict stability across successive versions of the same judge model family (see section 5).
- The Soumik study uses 2025 models; I found no replication on models released in 2026.
- Items marked (snippet) were not opened; their numbers should be checked before quoting.

## 2. Judge design: scale, criteria, reasoning, examples, model choice, panels

### Takeaway
The practitioner default (one binary judge per failure mode, critique before verdict, validated against expert labels) is unchanged and still defensible, but 2026 evidence qualifies two popular beliefs: binary decomposition does not beat graded scales for holistic qualities, and panels of judges buy much less than vote-counting suggests because their errors are correlated. Reasoning-enabled judges are more accurate but not less biased.

### Cited Findings

**Binary vs Likert vs pairwise**
- Across SummEval, QAGS and USR Topical-Chat with six judge models, "ordinary five-point ratings achieve the highest mean Spearman correlation across benchmarks for every judge"; their advantage over six-question binary decomposition was statistically robust in 31 of 36 planned contrasts. The authors conclude binary decomposition "remains useful for atomic verification and question-level diagnosis, but it is not a generally superior default for matching human ratings of holistic constructs." `[workshop]` NeurIPS 2026 workshop "Can We Trust the Judge?" (abstract) — [Nandwani and Gakhar, "Ask, Then Grade"](https://neurips.cc/virtual/2026/161241)
- Format determines which error dominates: Likert is dominated by item heterogeneity, pairwise by position bias; binary scoring collapses at low prevalence where pairwise Bradley-Terry still recovers rankings. `[preprint]` (snippet for these specifics) — [Messing 2026](https://arxiv.org/abs/2604.11581)
- The ordinal task was the least prompt-stable in JudgeSense. `[preprint]` (abstract) — [Bellibatlu et al.](https://arxiv.org/abs/2604.23478)
- Discrete Likert scales may introduce rating indeterminacy and lower consistency; the scale is an underexplored design parameter. `[preprint]` (snippet), January 2026 — [arXiv 2601.03444](https://arxiv.org/abs/2601.03444)
- Practitioner position unchanged: "Binary evaluations force clearer thinking and more consistent labeling"; weighted scores are discouraged "for the same reason I discourage Likert scales for LLM judges." `[practitioner]` (full text), page reports last modified 2026-09-21 — [Husain and Shankar FAQ](https://hamel.dev/blog/posts/evals-faq/)

**Single vs multi-criterion; rubric specificity**
- A coarse rubric is a documented cause of missed defects: three axes with no category for state-tracking, guardrails or recovery led to 113 of 114 relevant defect notes being mis-routed. `[preprint]` (abstract) — [Zhang et al. 2026](https://arxiv.org/abs/2606.10315)
- Anthropic: grade each dimension with an isolated judge rather than one judge for all dimensions, and give the judge a way out (return "Unknown" when it lacks information). `[vendor/lab]` (full text), 2026-01-09, foundational for this cycle — [Anthropic, "Demystifying evals for AI agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Husain and Shankar: build "a separate judge for each type of failure"; and "Extra context can cause context rot and make the judge worse", so give each judge only the trace parts its failure mode needs. `[practitioner]` (full text) — [FAQ](https://hamel.dev/blog/posts/evals-faq/)
- A "calibrated rubric" mitigation produced no gain in one study (largest effect −1.0 pp for GPT-4o). `[preprint]` (full text) — [Soumik 2026](https://arxiv.org/abs/2604.23178)

**Reasoning before verdict; reasoning models as judges**
- Chain-of-thought was the best single strategy on LLMBar for three of five judges (Claude .870, GPT-4o .764, Llama .705) and gave +7.3 pp for Claude on MT-Bench (p=0.0009), but increased length preference for GPT-4o and Claude. `[preprint]` (full text) — [Soumik 2026](https://arxiv.org/abs/2604.23178)
- Reasoning models outperform non-reasoning models on judgment accuracy but "remain significantly vulnerable" to superficial-quality biases; the advantage is not merely a function of output length. `[preprint]` (snippet), January 2026 — ["Reasoning Model Is Superior LLM-Judge, Yet Suffers from Biases"](https://arxiv.org/abs/2601.03630)
- Accuracy rises with reasoning effort on JudgeBench: o3-mini at 80.86% / 76.57% / 70.57% for high / medium / low. `[preprint]` (snippet); the benchmark is October 2024, older — [JudgeBench](https://arxiv.org/abs/2410.12784)
- Thinking models gain roughly 10 points of accuracy on RewardBench for under 2x overhead. `[preprint]` (snippet), September 2025, just outside the window — ["Explicit Reasoning Makes Better Judges"](https://arxiv.org/abs/2509.13332)
- The leniency shift from prior context "keeps its relative size" with reasoning enabled. `[preprint]` (abstract) — [Mazaheri and Mazaheri](https://arxiv.org/abs/2608.16003)

**Judge model choice**
- Among competitive judge methods on 931 human-annotated mobile-agent trajectories, "the LLM backbone is the primary driver" of judge quality, and two backbones showed "qualitatively opposite failure profiles, one conservative and the other permissive". `[preprint]` (abstract), 2026-08-11 — [MobileJudgeBench](https://arxiv.org/abs/2608.11434)
- Husain and Shankar: start with a strong model because it "can make it easier to develop the judge's prompt", then test cheaper models and measure the alignment loss. `[practitioner]` (full text) — [FAQ](https://hamel.dev/blog/posts/evals-faq/)
- Different-model-than-generator remains Anthropic's documented default ("Generally best practice to use a different model to evaluate...", per the digest's reading of [Anthropic docs](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests); I confirmed the URL resolves but did not re-read it this session).

**Panels / juries**
- A panel of 9 frontier LLMs from 7 families supplied roughly the information of about 2 independent votes; panel accuracy was 8-22 percentage points below what independent voting would achieve; "the best single judge matches or beats the full panel in every condition"; better aggregation closed at most 11% of the gap. Held across prompt variants, temperatures, chain-of-thought and a pairwise task. Tasks were NLI datasets with 100 human annotations per item. `[preprint]`, single author (abstract), 2026-05-28 — [Kohli, "Nine Judges, Two Effective Votes"](https://arxiv.org/abs/2605.29800)
- Ensembling reduces but does not eliminate self-preference bias. `[preprint]` (abstract) — [Pombal et al.](https://arxiv.org/abs/2604.06996)
- Same-family and cross-family ensembles were not among the significant winners in the Soumik mitigation study; the budget combined strategy (S8) was. `[preprint]` (full text) — [Soumik 2026](https://arxiv.org/abs/2604.23178)
- Pro-panel results exist: a judge-aware Bradley-Terry model (BT-sigma) for pairwise juries `[peer-reviewed]` ICML 2026 per search result (snippet) — [arXiv 2602.16610](https://arxiv.org/abs/2602.16610); dynamic "jury-on-demand" `[preprint]` (snippet), December 2025 — [arXiv 2512.01786](https://arxiv.org/abs/2512.01786); robust aggregation against one biased judge `[preprint]` (snippet), June 2026 — [RoPoLL, arXiv 2606.30931](https://arxiv.org/abs/2606.30931)

**Few-shot examples**
- No new 2026 empirical result found. The digest's rule (few-shot examples from the train split only; one clear pass, one clear fail, one borderline) rests on the Husain/Shankar skill files and still stands as practitioner guidance.

### Inferences
- The binary-vs-Likert conflict is about the target. "Ask, Then Grade" measures correlation with human holistic ratings on NLG benchmarks; Husain/Shankar optimise for actionable, labelable failure modes derived from error analysis. Binary per failure mode remains the right default for product evals; a graded scale is defensible when the construct is intrinsically graded and the goal is ranking. This reconciliation is mine.
- A panel's main demonstrated value is diluting self-preference when ranking models that include the judge's own family, not raising accuracy. If budget is fixed, one well-validated strong judge plus more human labels is likely better than a jury.
- Use a reasoning-enabled judge for accuracy, but do not treat reasoning as a bias control; bias controls must be applied to the input (blind authorship, normalise format, strip prior verdicts).
- Since backbones have opposite conservative/permissive profiles, TPR and TNR must be measured separately per judge model; a swap can keep accuracy and reverse the error direction.

### Gaps
- No study found that sweeps thinking budget / reasoning effort against judge TPR/TNR on application-level binary rubrics; available numbers are from benchmark accuracy.
- No 2026 controlled study on the effect of few-shot examples in judge prompts.
- "Ask, Then Grade" is a workshop poster; the abstract gives no correlation values.
- The Kohli panel result is on NLI and RewardBench, not on product rubrics or agent traces.

## 3. Validation and statistical correction

### Takeaway
The procedure in the digest (expert labels, train/dev/test split, TPR and TNR, Rogan-Gladen with a bootstrap interval) is still what the leading practitioner tooling prescribes, but the 2026 statistics literature has moved past it: prediction-powered inference (PPI) and efficient-influence-function estimators are shown to be more efficient than Rogan-Gladen, and there are now documented conditions under which Rogan-Gladen is unstable or confidently wrong. The largest procedural change is the warning that no level of judge-human agreement makes uncorrected judge scores safe for hypothesis tests.

### Cited Findings

**What the practitioner standard currently says (verified this session)**
- Split human labels into train 10-20% / dev 40-45% / test 40-45%; "Target: 30-50 examples of each class (Pass and Fail) across dev and test combined"; target "TPR > 90% AND TNR > 90%", floor 80% each; Rogan-Gladen `theta_hat = (p_obs + TNR - 1) / (TPR + TNR - 1)`, "Clip to [0, 1]. Invalid when TPR + TNR - 1 is near 0"; "Compute a bootstrap confidence interval. A point estimate alone is not enough." PPI is not mentioned. `[practitioner]` (full text), undated file fetched 2026-11-09 — [validate-evaluator SKILL.md](https://raw.githubusercontent.com/ai-evals-course/evals-skills/main/skills/validate-evaluator/SKILL.md)
- "Label 100 to 200 examples for each failure mode"; at least 50 passing and 50 failing examples when diagnosing disagreements. `[practitioner]` (full text) — [FAQ](https://hamel.dev/blog/posts/evals-faq/)
- `judgy` remains the reference implementation of this correction. `[practitioner]` (URL resolves; not re-read) — [judgy](https://github.com/ai-evals-course/judgy)

**Peer-reviewed correction (digest S25, re-verified)**
- Lee et al. is confirmed at ICML 2026 (v4, 2026-05-31): plug-in correction for imperfect sensitivity/specificity, intervals covering both test-set and calibration-set uncertainty, adaptive allocation of calibration samples, and a claim of remaining unbiased under distribution shift between test and calibration data. `[peer-reviewed]` (abstract summary) — [Lee et al., "How to Correctly Report LLM-as-a-Judge Evaluations"](https://arxiv.org/abs/2511.21140)

**New in 2026: PPI and successors**
- Chen et al. unify measurement-error (Rogan-Gladen-style) and PPI estimators via semiparametric efficiency theory, derive EIF-based efficient estimators, and "characterize conditions under which PPI-style estimators attain strictly smaller asymptotic variance than measurement-error corrections." A search summary adds that both PPI and the EIF estimator beat Rogan-Gladen on finite-sample bias and interval efficiency (snippet for that clause). `[preprint]` (abstract), 2026-01-08 — [Chen et al., "Efficient Inference for Noisy LLM-as-a-Judge Evaluation"](https://arxiv.org/abs/2601.05420)
- Arawjo's `evalstats` paper implements nine hypothesis tests via PPI (including the first PPI corrections for four rank-based tests) with bootstrap-adaptive power tuning for small calibration sets. Recommendations: never run tests on raw judge scores regardless of IRR; hand-label a random subset; require judge-human rho-squared of at least 0.4 (below 0.2 the judge is too poor to use); floor of 15 human labels and at least 50 judge-scored items; use Bonett-Price intervals for paired binary data; "avoid bootstrap CIs entirely below N = 100"; Romano-Wolf step-down for multiple comparisons at n of 30 or more; do not treat 100% agreement on a small labelled set as a perfect judge; disclose the labelling procedure because PPI assumes labels are missing completely at random. PPI's label efficiency is about 1.5x the human labels at rho-squared 0.4. `[preprint]` (full text, first 100k chars), 2026-09-20 — [Arawjo 2026](https://arxiv.org/abs/2609.35815)
- PPI has been extended to ranking evaluation. `[preprint]` (snippet), June 2026 — [arXiv 2606.05308](https://arxiv.org/abs/2606.05308)

**New in 2026: where Rogan-Gladen fails**
- Variance scales as 1/J squared (J = Youden's J = TPR + TNR − 1): "When J-hat is small, the correction becomes unstable and interval width can increase sharply." "With small calibration sets, corrected estimates and their intervals can become unstable." `[preprint]` (full text), 2026-05-07 — [Fiedler (Indeed), "Bias and Uncertainty in LLM-as-a-Judge Estimation"](https://arxiv.org/abs/2605.06939)
- Sharing one calibration set across the models being compared can reverse the sign of a comparison: true difference +0.048, shared-calibration Rogan-Gladen estimate −0.330 (CI [−0.493, −0.194]), "confidently wrong-signed." "Shared calibration requires justification; it cannot be a default design choice." `[preprint]` (full text) — [Fiedler 2026](https://arxiv.org/abs/2605.06939)
- "The corrected estimate can have higher mean squared error than the naive estimate" (attributed there to Greiner 2003, epidemiology). This traces the unverified remark in the digest's §14 item 11 to a named citation, though I did not open Greiner. `[preprint]` (full text) — [Fiedler 2026](https://arxiv.org/abs/2605.06939)
- Fiedler's reporting checklist: state the estimand and estimator; report calibration design and size and whether it is shared or model-specific; say what randomness each interval reflects; report q0-hat, q1-hat and J-hat with intervals; for comparisons report the difference in J with an interval; when diagnostics signal trouble, "weaken the claim rather than picking the most favorable estimator." `[preprint]` (full text) — [Fiedler 2026](https://arxiv.org/abs/2605.06939)
- At an observed defect rate of zero, "the Rogan-Gladen correction degenerates -- no signal can recover the true rate"; where the gate reported a nonzero rate, measured sensitivity implied "a 3-6x undercount". `[preprint]` (abstract) — [Zhang et al. 2026](https://arxiv.org/abs/2606.10315)
- Intervals that ignore judge-choice, temperature and prompt variance under-cover; a small pilot can recover honest intervals. `[preprint]` (abstract) — [Messing 2026](https://arxiv.org/abs/2604.11581)

**Metrics**
- Cohen's kappa is the most trustworthy IRR metric for binary judge labels, but exact-match-type metrics (percent agreement, Gwet's AC1, PABAK) are "no safer", and higher kappa lowers risk without removing it. `[preprint]` (full text) — [Arawjo 2026](https://arxiv.org/abs/2609.35815)
- Report paired discrimination (flag rate on faulty runs minus flag rate on the clean runs they came from), because plain recall can credit a judge for its false-alarm rate. `[workshop]` (abstract) — [Mohammadi, "trajectory-judge"](https://arxiv.org/abs/2609.00038)

**Conflict to flag**
- Bootstrap intervals: validate-evaluator and Fiedler use the bootstrap throughout (Fiedler: 10,000 iterations, separate resampling of calibration and test); Arawjo says to avoid bootstrap CIs below N = 100. — [SKILL.md](https://raw.githubusercontent.com/ai-evals-course/evals-skills/main/skills/validate-evaluator/SKILL.md); [Fiedler](https://arxiv.org/abs/2605.06939); contradicted by [Arawjo](https://arxiv.org/abs/2609.35815)

### Inferences
- Recommended procedure as of November 2026 (synthesis, not quoted from one source): (1) expert-label a random sample; (2) split and tune the judge on dev, touch test once; (3) report TPR, TNR and Youden's J with intervals; (4) if J is high and the calibration set is per-system, Rogan-Gladen or Lee et al.'s plug-in is adequate for a single pass rate; (5) for comparisons between systems, small N, or any hypothesis test, use a PPI-style estimator (evalstats) with a fresh random human-labelled subset for each system compared; (6) if J is low, fix the judge or fall back to human labels rather than correcting.
- The digest's "30-50 per class across dev and test" is a minimum for estimating TPR/TNR. With about 40 fails, a 90% TNR has a 95% interval of roughly ±9 points (derived from the binomial SE), which propagates into the corrected rate through 1/J. That is consistent with Fiedler's small-calibration warning and argues for the FAQ's 100-200 figure when the corrected rate will be reported externally.
- Balanced calibration sets (the digest's 50:50 advice) are right for estimating TPR/TNR but violate PPI's random-labelling assumption. A team using PPI needs a randomly sampled labelled subset, which may be separate from the balanced set used to develop the judge.
- Calibrating once and reusing the TPR/TNR for a new system version is precisely the shared-calibration design Fiedler warns about; a judge's error rates can differ by the system producing the outputs.

### Gaps
- No source gives a single agreed calibration-set size; Fiedler and Arawjo both decline to. The only hard floors found are evalstats' 15 labels and 50 judged items.
- I did not read the second half of the evalstats paper or its Figure 6 (inflation by agreement level); I did not read the Chen et al. body for the exact regimes where PPI wins.
- I found no evidence that `judgy` or the validate-evaluator skill has adopted PPI; I did not inspect their commit history.
- statsforevals.com returned HTTP 406 to my automated check (it likely blocks non-browser clients); I did not confirm its current content.
- No independent replication of the 37% false-positive figure.

## 4. Judges for agent trajectories

### Takeaway
A judge that sees only the request and final reply cannot detect faults that leave the reply unchanged, and a single-pass judge over a full transcript is limited by context length and by what its rubric names. Evidence in 2026 favours telling the judge to check each step, scoping its input to what the criterion needs, and treating agentic judges that inspect the workspace as promising but unvalidated; outcome verification by code remains the anchor.

### Cited Findings

**What the judge is shown and asked determines what it can catch**
- On 400 exactly-labelled trajectories from a deterministic support-desk testbed with injected faults, a 14B judge shown only the request and final reply scored 34%-76% "recall" on four fault types that leave the reply unchanged, but its paired discrimination there is zero: that recall is just its flag rate on clean runs. Its "loud" recall of 84% was a paired +0.393 and its "silent" recall of 45% a paired +0.048. `[workshop]` NeurIPS 2026 workshop "Who Verifies the Agents?" (abstract), v4 2026-11-03, single author, one small judge model — [Mohammadi, "trajectory-judge"](https://arxiv.org/abs/2609.00038)
- Same study: "Told to check each step, the same model flags every fault of those four types and 0 of 100 clean runs (95% CI up to 3.6%)." Shown every step but asked only about the reply, it reached paired +0.69 against +1.00 when told to check each step. It did not reliably check the final reply for invented promises (one of four flagged every time; the other three flagged once in 42 faults). `[workshop]` (abstract) — [Mohammadi 2026](https://arxiv.org/abs/2609.00038)
- Production multi-turn agents: judges catch turn-local issues and miss cross-turn state issues unless the rubric has categories for state-tracking, guardrails and recovery. Conclusion: "automated judging is a regression floor, not a substitute for human review." `[preprint]` (abstract) — [Zhang et al. 2026](https://arxiv.org/abs/2606.10315)

**Context length and evidence delivery**
- "Long-running agents can produce large traces that fill or exceed the judge's context window"; the authors suggest "giving the judge a tool to search the parts it needs" while noting the added complexity. "Extra context can cause context rot and make the judge worse." `[practitioner]` (full text) — [Husain and Shankar FAQ](https://hamel.dev/blog/posts/evals-faq/)
- Transect (authors include UK AISI-affiliated researchers; built on Inspect Scout) was demonstrated on an AI R&D evaluation that generated almost 13 million tokens. It keeps judge-model labels traceable to source turns on a shared timeline, and the paper warns that LLM-assisted transcript analysis gives evaluators many analytical choices, threatening reproducibility and auditability. `[preprint]` (abstract), 2026-10-06 — [Pilditch et al., "Transect"](https://arxiv.org/abs/2610.08364)
- Judgment Labs argues trajectories can reach millions of tokens and proposes an agentic harness that searches the trajectory with rubrics refined from production feedback. `[vendor]` (snippet; URL resolves), 2026 — [Judgment Labs blog](https://www.judgmentlabs.ai/blogs/agent-judge-solving-long-context-evaluations)
- A judge run inside an agent harness showed lower self-agreement than the same judge called through a direct API. `[preprint]` (abstract) — [JudgeSense](https://arxiv.org/abs/2604.23478)

**Elaborate judge pipelines vs simple ones**
- On 931 human-annotated mobile-agent trajectories (6 benchmarks, 4 agent models, 68 apps), "a simple baseline judge with sampled screenshots is competitive with, and often exceeds, purpose-built methods"; the backbone model matters most; benchmark judge-quality metrics predicted agent-ranking fidelity and downstream usefulness as an RL reward. `[preprint]` (abstract), 2026-08-11 — [MobileJudgeBench](https://arxiv.org/abs/2608.11434)

**Judges that inspect workspaces/files (agent-as-a-judge)**
- The pattern (a judge agent with read tools that opens files, re-runs tests and checks each requirement, sometimes given only the question and workspace path, not the agent's trace) is documented mainly in vendor and project material. A recount of the DevAI judgment files is reported to show the gray-box agent judge saying "met" where human consensus said "not met" 64 times against 50 the other way, with humans confirming roughly 80-88% of its "met" verdicts; one guide advises against giving the judge write tools. `[vendor]` (snippet only; secondary recount, not checked against the original paper) — [Arize, "Where agent evals are going: Agent-as-a-Judge"](https://arize.com/blog/agent-as-a-judge-agentic-evaluation/)
- Anthropic's guidance for the cycle: validate key outcomes with pass/fail checks first, then it is "often useful to also grade the transcript" with clear rubrics for behaviours such as tool use; "often better to grade what the agent produced, not the path it took." `[vendor/lab]` (full text), 2026-01-09 — [Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- For individual tool calls: "Use code assertions when the expected behavior is objective." For end-to-end task success: "measure it with human review or validated LLM judges." `[practitioner]` (full text) — [FAQ](https://hamel.dev/blog/posts/evals-faq/)

### Inferences
- The digest's "outcome for the score, trajectory for diagnosis" consensus holds, with a sharper caveat: an LLM judge over the final reply is not an outcome check. Outcome means verified environment state; anything the judge cannot see in its input it cannot grade, and reported recall on such faults is noise.
- Design implications for trajectory judges: (a) one judge per failure mode with only the relevant spans; (b) an explicit instruction to check each step when step-level faults matter; (c) rubric categories for cross-turn state; (d) validate with injected faults paired against clean parents; (e) for transcripts beyond context, a search tool or phase decomposition, validated separately because it adds its own nondeterminism.
- An agentic judge with workspace access is closer to an outcome check than a transcript judge is, but its lean toward false "met" verdicts (if the DevAI recount is right) means it needs the same TPR/TNR validation, with attention to TNR.

### Gaps
- No peer-reviewed 2026 study found that measures judge accuracy as a function of transcript length, or compares full-transcript, summarised and retrieval-based evidence delivery head to head.
- No rigorous primary source read on agent-as-a-judge accuracy; the DevAI recount numbers are from a search summary of vendor pages. A January 2026 survey of agent-as-a-judge (You et al.) was mentioned in results but not located or read.
- trajectory-judge uses one 14B model and a synthetic testbed; generalisation to frontier judges and real traces is untested.
- Nothing found on judges grading sub-agent or multi-agent delegation beyond Transect's descriptive tooling.

## 5. Judge drift, re-validation cost, and criteria drift

### Takeaway
This is the weakest-evidenced area. Practitioner guidance now says explicitly to pin the judge snapshot and re-validate on any judge prompt or model change, but I found no peer-reviewed measurement of how much verdicts shift between judge versions, and no 2026 follow-up study to "Who Validates the Validators?".

### Cited Findings
- The Husain/Shankar validate-evaluator skill says: "Re-validate after changing the judge prompt, switching models, or when production confidence intervals widen unexpectedly," and on pinning: "Providers update models without notice, causing silent drift." `[practitioner]` (full text), undated — [validate-evaluator SKILL.md](https://raw.githubusercontent.com/ai-evals-course/evals-skills/main/skills/validate-evaluator/SKILL.md)
- The main FAQ does not address judge drift; it says to re-run error analysis after model switches and that eval sets go stale as products change. `[practitioner]` (full text) — [FAQ](https://hamel.dev/blog/posts/evals-faq/)
- A practitioner procedure for judge upgrades: record judge snapshot ID, temperature, prompt hash, rubric version and few-shot set in every eval record; do not compare scores across judge identities; before a pinned judge is deprecated, run old and new judges in parallel on the eval set and a held-out meta-eval set; rebase per category where agreement is high and mark low-agreement categories as non-comparable across the boundary; weekly calibration on a stratified sample. `[practitioner]`, single-author blog, opinion; none of its numeric claims carries an inline citation (full text), 2026-04-23 — [Tian Pan, "LLM-as-Judge Drift"](https://tianpan.co/blog/2026-04-23-llm-judge-drift-evaluator-upgrade-phantom-regression)
- Indirect quantitative evidence that a judge swap can change conclusions: judge-model choice is the largest variance component under both Likert and pairwise formats (snippet), and naive SEs are 40-60% too small when judge/prompt/temperature variance is ignored (abstract). `[preprint]` — [Messing 2026](https://arxiv.org/abs/2604.11581)
- Backbones can have opposite error profiles (conservative vs permissive), so a swap can reverse the direction of judge error. `[preprint]` (abstract) — [MobileJudgeBench](https://arxiv.org/abs/2608.11434)
- Judge TPR/TNR is not transferable across the systems being graded; shared calibration can produce a wrong-signed comparison. `[preprint]` (full text) — [Fiedler 2026](https://arxiv.org/abs/2605.06939)
- Criteria drift: the original paper (UIST 2024, foundational) remains the reference: "users need criteria to grade outputs, but grading outputs helps users define criteria." A targeted search found no 2026 follow-up study. — [Shankar et al., "Who Validates the Validators?"](https://arxiv.org/abs/2404.12272)
- The Gu et al. survey (v6, October 2025, just before the window) lists long-term consistency and meta-evaluation as underexplored. `[preprint]` (snippet) — ["A Survey on LLM-as-a-Judge"](https://arxiv.org/abs/2411.15594)

### Inferences
- The cost of a judge upgrade is one full re-validation: re-run the new judge on the retained human-labelled test set and recompute TPR/TNR and the corrected rate. The human labels are the durable asset; the judge prompt and model are replaceable. This makes storing labelled sets with their critiques, and keeping the test split untouched, the main hedge against deprecation.
- Because the held-out test set gets reused at every judge change, it slowly becomes a dev set. Teams that expect frequent judge changes should hold back or periodically add fresh labels. No source states this; it follows from the "touch test once" rule.
- Criteria drift and judge drift compound: if the rubric is revised after seeing outputs and the judge model is also changed, score movements cannot be attributed. Change one at a time.
- A trend line that crosses a judge change should be annotated or re-scored with the new judge on archived outputs; otherwise a "regression" may be a judge artefact.

### Gaps
- No peer-reviewed or preprint measurement found of verdict shift between consecutive versions of the same judge model. One blog claims "studies in 2026" show a 3-8 point mean shift; I could not find the studies and do not cite the figure as fact.
- No data on what re-validation costs in practice (hours, labels, dollars).
- No 2026 academic follow-up to criteria drift or EvalGen found. Absence of search hits is not proof of absence; a citation-graph search was not done.
- The validate-evaluator file has no date, so I cannot say whether its re-validation and pinning lines postdate the September digest.

## 6. When not to use an LLM judge

### Takeaway
Expert guidance is consistent and has hardened: use deterministic checks or verified environment state whenever the property is checkable, keep judges off the synchronous path, and treat judges on production agents as a regression floor that still needs human transcript review. The 2026 additions are evidence-based exclusions: do not use a judge when its Youden's J is low, when the defect leaves no trace in the judge's input, when the judge would grade its own family's output in a model comparison, or when the result will be fed to a significance test without human-label correction.

### Cited Findings
- "Use a code-based eval when a deterministic rule can identify the failure." "Using code assertions avoids the need for human labels." Reserve judges for "persistent generalization failures". In CI: "Favor assertions or other deterministic checks over LLM-as-judge evaluators." As a guardrail: "you would almost never use a slow or non-deterministic LLM-as-Judge as a synchronous guardrail." `[practitioner]` (full text), page reports last modified 2026-09-21 — [Husain and Shankar FAQ](https://hamel.dev/blog/posts/evals-faq/)
- Anthropic: choose "deterministic graders where possible" and LLM graders "where necessary or for additional flexibility"; "LLM-as-judge graders should be closely calibrated with human experts." `[vendor/lab]` (full text), 2026-01-09 — [Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Do not rely on a judge alone for production multi-turn agents: "automated judging is a regression floor, not a substitute for human review." `[preprint]` (abstract) — [Zhang et al. 2026](https://arxiv.org/abs/2606.10315)
- Do not use an outcome-only (request + final reply) judge to detect process faults; its apparent recall there equals its false-alarm rate. `[workshop]` (abstract) — [Mohammadi 2026](https://arxiv.org/abs/2609.00038)
- Do not use a judge whose agreement with humans is weak: rho-squared below 0.2 is "too poor to use", aim for at least 0.4; and never run statistical tests on raw judge scores. `[preprint]` (full text) — [Arawjo 2026](https://arxiv.org/abs/2609.35815)
- Do not expect correction to rescue a weak judge: with J near zero, Rogan-Gladen intervals become degenerate; "weaken the claim rather than picking the most favorable estimator." `[preprint]` (full text) — [Fiedler 2026](https://arxiv.org/abs/2605.06939)
- Do not let a judge score a leaderboard that includes its own outputs without controls: self-preference skewed scores by up to 10 points. `[preprint]` (abstract) — [Pombal et al.](https://arxiv.org/abs/2604.06996)
- Do not put a judge where the graded party can argue back: verdicts flipped 25-71% under static pushback and 62-91% under adversarial persuasion. `[preprint]` (abstract) — [Zhao et al., "Jagged Judges"](https://arxiv.org/abs/2608.12645)
- Do not assume a panel substitutes for independent evaluation: "scaling up panels cannot replace genuinely independent evaluation" (paraphrase of the abstract's conclusion). `[preprint]` (abstract) — [Kohli 2026](https://arxiv.org/abs/2605.29800)
- Lee et al. identify parameter regimes where judge-based evaluation with correction is more reliable than human-only evaluation, so the choice is quantitative, not categorical. `[peer-reviewed]` ICML 2026 (abstract summary) — [Lee et al.](https://arxiv.org/abs/2511.21140)
- Practitioner blogs converge on the same rule for facts the system can verify (for example, whether a refund exists in the transaction system should be read from the system, not judged). `[vendor/practitioner]` (snippet) — [Arize, "LLM-as-a-Judge: When should you use it?"](https://arize.com/resources/llm-as-a-judge-when-should-you-use-it/) (this URL was not in my resolution check)

### Inferences
- Decision order as of November 2026 (synthesis): (1) can code or environment state verify it? use that; (2) is the criterion subjective but stable, with expert labels obtainable? build one binary judge, validate, correct; (3) is J low, the defect cross-turn or unrepresented in the rubric, or the stakes high? keep humans reading transcripts and use the judge only as a floor; (4) is the output adversarial or self-advocating toward the grader? do not use a judge as the deciding control.
- The digest's grader hierarchy (code, then judge, then human) stands. What changed is that the conditions for step 2 are now measurable (J, rho-squared, paired discrimination) rather than judgement calls.

### Gaps
- No lab published a dedicated 2026 "when not to use a judge" statement that I could find; guidance is embedded in broader eval posts.
- I did not re-read OpenAI's evaluation best-practices page this session (URL resolves: https://developers.openai.com/api/docs/guides/evaluation-best-practices), so I cannot say whether its judge guidance changed since the digest.
- Date discrepancy to resolve: the digest records the Husain/Shankar FAQ as published 2025-05-28 and modified 2026-09-01; my fetch of the same URL reported "originally published September 18, 2026", last modified September 21, 2026. The page may have been republished or the extraction may be wrong. The quoted positions match the digest's in substance.
- Eugene Yan's LLM-evaluators survey (https://eugeneyan.com/writing/llm-evaluators/, August 2024, URL resolves) was not re-read; I found no 2026 update to it in search results.
