# Statistics and Measurement Validity of AI Evaluations (state of knowledge, November 2026)

Compiled 2026-11-09. Scope: what has changed or been added since `/Users/ted/src/learn/vally/research/eval-best-practices-digest.md` (compiled 2026-09-10). That digest is not re-derived here; its statistical claims are checked in the first question.

Conventions used throughout:
- Every cited finding names its source and date. "(derived)" marks arithmetic I computed from a cited formula; it is not a quotation.
- "Snippet only" marks a claim seen in a search-result excerpt that I could not confirm in the primary text. Treat those as leads, not facts.
- URL check (curl, 2026-11-09): every URL below returned HTTP 200 except the two official proceedings pages for Bean et al. (NeurIPS 2025) and HAL (ICLR 2026), which refused the connection from the command line. The arXiv records for both papers resolve and are what I cite.

---

## 1. What is the current recommended statistical toolkit, and what has followed Miller's "Adding Error Bars to Evals" (2024)?

### Takeaway
Miller's five recommendations still stand as the baseline, but two refinements now sit on top of them: at small n (below a few hundred items) replace the CLT/Wald interval with Wilson or Bayesian intervals, and treat the comparison of two variants as a paired problem in which run-to-run "prediction noise" is usually the larger term, so the fix is more trials per item rather than more items. The digest's formulas are correct; its statements that the 1.96 x SE interval is the default and that bootstrapping is merely "unnecessary" are too generous for suites of tens to low hundreds of cases.

### Cited Findings

**Foundational (older, still the reference point)**
- Miller (Anthropic), arXiv v1 dated 2024-11-01, no later revision listed. Formulas: SE_CLT = sqrt( (1/n) * (1/(n-1)) * sum_i (s_i - s_bar)^2 ); for 0/1 scores SE_Bernoulli = sqrt( s_bar (1 - s_bar) / n ); CI_95% = s_bar +/- 1.96 x SE. — [Miller 2024](https://arxiv.org/abs/2411.00640)
- Clustered SE (Miller Eq. 4): SE_clustered = ( SE_CLT^2 + (1/n^2) * sum_c sum_i sum_{j != i} (s_{i,c} - s_bar)(s_{j,c} - s_bar) )^(1/2). On real Anthropic data the clustered/naive ratio was 3.05 on DROP (1.34 vs 0.44), 1.88 on MGSM (1.62% vs 0.86%), 1.10 on RACE-H (0.51% vs 0.46%). — [Miller 2024](https://arxiv.org/abs/2411.00640)
- Variance decomposition: Var(mu_hat) = ( Var(x) + E[sigma_i^2] ) / n, where Var(x) is between-question variance and sigma_i^2 is within-question (resampling) variance; with K resamples per question the second term becomes E[sigma_i^2]/K. In Miller's illustrative uniform-difficulty case (Var(x) = 1/12, E[sigma_i^2] = 1/6), Var(mu_hat | K) = Var(mu_hat | K=1) x (1 + 2/K)/3: K=2 cuts variance by 1/3, K=4 by 1/2, K=6 by 5/9, with a ceiling of 2/3. — [Miller 2024](https://arxiv.org/abs/2411.00640)
- Paired difference: SE_paired = sqrt( Var(s_A - s_B) / n ) = sqrt( SE_A^2 + SE_B^2 - 2 SE_A SE_B Corr(s_A, s_B) ). Miller's (fictional) Table 5 uses correlations of 0.37 to 0.64; e.g. HumanEval difference -3.1% (SE 2.1%), 95% CI (-7.2%, +1.0%), corr 0.64. — [Miller 2024](https://arxiv.org/abs/2411.00640)
- Power (Miller Eq. 9, 10): n = (z_{alpha/2} + z_beta)^2 ( omega^2 + sigma_A^2/K_A + sigma_B^2/K_B ) / delta^2, with omega^2 = Var(x_A) + Var(x_B) - 2 Cov(x_A, x_B); equivalently MDE delta = (z_{alpha/2} + z_beta) sqrt( (omega^2 + sigma_A^2/K_A + sigma_B^2/K_B) / n ). Worked examples: with sigma^2 = 0, omega^2 = 1/9, alpha = 0.05, power 80%, detecting delta = 3 points needs n ≈ 969 questions (hence the advice that new evals have at least 1,000 questions); with sigma_A^2 = sigma_B^2 = 1/6, omega^2 = 1/9, n = 198, raising K from 1 to 10 lowers the MDE from 13.2% to 7.5%. — [Miller 2024](https://arxiv.org/abs/2411.00640)
- Miller's paper has no in-depth treatment of small n; it assumes "a large number of questions" and on that basis calls bootstrapping unnecessary. — [Miller 2024](https://arxiv.org/abs/2411.00640)

**The main critique: CLT intervals fail at small n**
- Bowyer, Aitchison (Bristol) and Ivanova (Oxford), "Position: Don't use the CLT in LLM evals with fewer than a few hundred datapoints", arXiv 2503.01747, v3 dated 2025-05-28, listed under ICML (search results show it in the ICML 2025 position track). Foundational for this question; published before the 12-month window but it is the reference every 2026 source cites. — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- "CLT-based methods perform very poorly, usually dramatically underestimating uncertainty." Simulations used N = 3, 10, 30, 100. Even at N = 100, "95% CLT-based intervals achieve a coverage of only 92.5%." — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Two structural failures of the Wald interval: when the observed rate is 0 or 1 the SE is zero and the interval collapses to a point; and the interval extends outside [0, 1] when theta_hat or 1 - theta_hat is below 1/(1 + N/z^2). — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Recommended single-proportion alternatives: "we recommend using WS [Wilson score] or Bayesian intervals in practice." Wilson: centre (theta_hat + z^2/2N)/(1 + z^2/N), half-width (z/2N)/(1 + z^2/N) x sqrt(4N theta_hat (1 - theta_hat) + z^2). Bayesian: uniform Beta(1,1) prior gives posterior Beta(1 + successes, 1 + failures); report its quantiles. Clopper-Pearson is valid but "overly conservative (too wide) in practice." — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Bootstrap is not a rescue at small n: bootstrap intervals "show poor calibration" on single-model IID data, and for F1 "the bootstrap ones systematically under-cover." — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Comparisons: for independent samples use posterior draws of theta_A - theta_B (or the odds ratio) and take quantiles; for paired data the authors recommend a paired Bayesian model and call unpaired Bayes "a reasonable and easier to implement alternative." — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Clustered data at small n: the Miller-style clustered SE did not achieve nominal coverage; "only the Bayesian method based on a clustered model" did (theta ~ Beta(1,1), d ~ Gamma(1,1), theta_t ~ Beta(d theta, d(1 - theta)), y_{i,t} ~ Bernoulli(theta_t)). — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- The paper deliberately gives no hard cut-off N; "a few hundred" in the title is practical guidance, and adequacy is described as context-dependent. — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Software: `bayes_evals` Python library. — [bayes_evals repo](https://github.com/sambowyer/bayes_evals)

**The main refinement: decompose the noise, pair everything, average predictions**
- Sida I. Wang (FAIR at Meta), "Measuring all the noises of LLM Evals", arXiv 2512.21326, submitted December 2025, v2 dated 2026-03-29. Law of total variance: Var_{x,eps}[A] = Var_x[ E_eps[A] ] (data noise: which questions you sampled) + E_x[ Var_eps[A] ] (prediction noise: the model's sampling on a fixed question). "The total variance is what matters in an experiment." — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- With K predictions averaged per question: Var[A_bar_K] = Var_x[E_eps[A]] + (1/K) E_x[Var_eps[A]]. Averaging shrinks only the prediction term, so it pays off when prediction noise dominates. — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Rule of thumb for correctness (0/1) evals: SE[A - B] ≈ SE[A] ≈ sqrt( p(1 - p) / N ) under paired analysis; the paper recommends this as the simplest heuristic for model developers. Unpaired, SE(A - B) = sqrt( SE(A)^2 + SE(B)^2 ). — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Worked HumanEval example (N = 164, p ≈ 0.5), SE of the difference and the gap needed for p < 0.05: unpaired 6% / 12%; unpaired with averaging 4% / 8%; paired 4% / 8%; paired with averaging 1-2% / 2-4%. — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Under pairing, prediction noise is usually the larger component: about 2x data noise on MATH500; on SWE-bench Verified training curves the data SE is about 1/6 of the prediction SE, so averaging 36 predictions cuts total SE to sqrt(2)/6 ≈ 0.24 of the original. — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Temperature moves noise between the two terms without changing the total much: on CRUXEval prediction noise dominates at T = 0.8 and data noise at T = 0.2, with total noise about the same. This is empirical support for Miller's "don't touch the thermostat". — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Small-K correction for estimating data variance from few repeats: Var_x[E_eps[A]] ≈ Var_hat_x[A_bar_K] - (1/(K-1)) E_hat_x[Var_hat_eps[A]]. — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Relation to other tests: the paper's Appendix E argues the paired bootstrap, the sign test (normal approximation) and its variance method give the same answer. It criticises bootstrap CIs computed against a fixed reference model (as on Chatbot Arena and CRUXEval) as incorrect per-model error bars, and calls the unpaired intervals in the Llama 3 report "much looser than the paired methods." — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Stated limits: all data are correctness evals; the paper itself cites Bowyer et al. that the CLT is unreliable below a few hundred questions and notes agentic evals are often under 1,000 questions (Terminal-Bench under 100). Recommendation to eval builders: release question-level results, ideally with multiple predictions per question. Data and analysis site: — [all-the-noises.github.io](https://all-the-noises.github.io/)

**Bayesian / hierarchical alternatives**
- UK AISI's HiBayES (Luettgau, Coppock, Dubois, Summerfield, Ududec), arXiv 2505.05602, v3 dated 2025-07-13: multilevel Bayesian GLMs with formal model comparison, aimed at nested eval data and "low-data settings" described as "< 20 data points per evaluation"; ships as a beta software package. Older than the window; I found no 2026 revision. — [HiBayES](https://arxiv.org/abs/2505.05602)

**Correcting for an imperfect LLM judge (carried over from the digest, still current)**
- Lee et al., "How to Correctly Report LLM-as-a-Judge Evaluations", arXiv 2511.21140 (2025-11-26, revised 2026-05-31, ICML 2026 per the digest): plug-in bias correction with CIs that include calibration-set uncertainty. URL re-checked 2026-11-09; content not re-read this session. — [Lee et al.](https://arxiv.org/abs/2511.21140)

**Tooling and adoption**
- Inspect (UK AISI): `stderr()` "supports computing clustered standard errors via the `cluster` parameter", e.g. `metrics=[accuracy(), stderr(cluster="category")]`; the `ci()` metric's t-interval uses `clusters - 1` degrees of freedom when clustering; `bootstrap_stderr()` takes 1,000 resamples by default. With epochs, "Metrics normally operate on a reduced score view, where epoch scores for each sample are combined into a single score", and "By default, the reduced view is built with `mean`" — i.e. the default matches Miller's and Wang's advice to average within a question before computing SE across questions. The page does not cite Miller. Fetched 2026-11-09. — [Inspect metrics docs](https://inspect.aisi.org.uk/metrics.html)
- statsforevals.com (Ian Arawjo, Université de Montréal), "last updated August 2026": `pip install evalstats`; `compare_prompts(scores)` applies multiple-comparisons correction; `compare_models(scores)` reports simultaneous confidence intervals over a model x prompt grid; `method="auto"` "picks the most appropriate method based on your data type and sample size"; CLI `evalstats analyze results.csv`. The landing page gives no formulas, sample-size rules or run counts; "Sample Size Planning" and "When Rankings Flip" are listed as planned, unlinked pages. — [statsforevals.com](https://statsforevals.com/)
- Adoption remains low in published benchmarks: "At present, only 16.0% of reviewed benchmarks conducted any statistical testing" (445 benchmarks; category is "uncertainty estimates or statistical tests"). — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Practitioner echo (2026 blog, single author, low authority): for one proportion at small n use Wilson or Clopper-Pearson; Miller is "the canonical treatment". — [Naixin Zhang, "Error Bars, Applied"](https://naixinzhang.com/blog/error-bars-applied)

**Status of the September 2026 digest's statistical claims**
- Still correct as stated: Miller's five recommendations, the Bernoulli SE formula, the clustered-SE ratio of up to 3.05x, the K=2 / K=4 variance reductions (these belong to Miller's illustrative uniform example, as the digest says), the paired-difference advice, and HumanEval's ~3% SE at 164 questions (Miller's table: 83.6% (3.2%)). — [Miller 2024](https://arxiv.org/abs/2411.00640)
- Now traceable: the digest left the "only 16% of 445 benchmarks" figure untraced. The primary source is Bean et al., NeurIPS 2025 Datasets and Benchmarks Track, arXiv 2511.04703. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Needs a caveat: "95% CI = mean ± 1.96 × SE" under-covers at small n and breaks at 0% or 100%; and "bootstrapping is unnecessary" should read "bootstrapping does not help" at small n, since it also under-covers. — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Needs a caveat: "cluster your SEs" is right in direction, but the sandwich-style clustered SE itself under-covers at small n; a hierarchical Bayesian model was the only method with correct coverage in Bowyer et al.'s simulations. — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- The Anthropic agent-evals post (2026-01-09) is still live and unchanged on the points the digest quotes; its pass^k example is "75% per-trial success rate ... 3 trials ... (0.75)³ ≈ 42%". — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Inferences
- Worked interval comparison (derived from the Wald and Wilson formulas above; Clopper-Pearson and Beta(1,1) values for the all-pass rows use the closed forms (alpha/2)^(1/n) and (alpha/2)^(1/(n+1))). 95% intervals:

| Result | Wald (CLT) | Wilson | Note |
|---|---|---|---|
| 3/3 | [1.000, 1.000] | [0.439, 1.000] | Clopper-Pearson lower 0.292; Beta(1,1) lower 0.398 |
| 10/10 | [1.000, 1.000] | [0.722, 1.000] | Clopper-Pearson lower 0.692; Beta(1,1) lower 0.715 |
| 20/20 | [1.000, 1.000] | [0.839, 1.000] | Clopper-Pearson lower 0.832; Beta(1,1) lower 0.839 |
| 50/50 | [1.000, 1.000] | [0.929, 1.000] | Clopper-Pearson lower 0.929; Beta(1,1) lower 0.930 |
| 16/20 (80%) | [0.625, 0.975] | [0.584, 0.919] | |
| 27/30 (90%) | [0.793, 1.007] | [0.744, 0.965] | Wald upper bound exceeds 1 |
| 40/50 (80%) | [0.689, 0.911] | [0.670, 0.888] | |
| 45/50 (90%) | [0.817, 0.983] | [0.786, 0.957] | |
| 80/100 (80%) | [0.722, 0.878] | [0.711, 0.867] | |
| 160/200 (80%) | [0.745, 0.855] | [0.739, 0.850] | |
| 400/500 (80%) | [0.765, 0.835] | [0.763, 0.833] | |
| 800/1000 (80%) | [0.775, 0.825] | [0.774, 0.824] | methods agree |

- Wald 95% half-width as a quick mental table (derived, 1.96 x sqrt(p(1-p)/n)). At p = 0.8: n=20 ±17.5 points; n=30 ±14.3; n=50 ±11.1; n=100 ±7.8; n=200 ±5.5; n=500 ±3.5; n=1000 ±2.5. At p = 0.5: n=20 ±21.9; n=50 ±13.9; n=100 ±9.8; n=200 ±6.9; n=1000 ±3.1.
- "Rule of three" check (derived): zero failures in n trials bounds the true failure rate at roughly 3/n with 95% confidence — 15% at n=20 (exact 13.9%), 6% at n=50, 3% at n=100, 1% at n=300. A clean 20/20 run does not support "failure rate under 5%".
- Minimum detectable effect with one trial per item, alpha = 0.05 two-sided, 80% power (derived: unpaired = 2.80 x sqrt(2p(1-p)/n); paired = 2.80 x sqrt(p(1-p)/n) using Wang's SE[A-B] ≈ SE[A] heuristic):

| n items | Unpaired MDE, p=0.8 | Paired MDE, p=0.8 | Unpaired MDE, p=0.5 | Paired MDE, p=0.5 |
|---|---|---|---|---|
| 20 | 35 pts | 25 pts | 44 pts | 31 pts |
| 50 | 22 pts | 16 pts | 28 pts | 20 pts |
| 100 | 16 pts | 11 pts | 20 pts | 14 pts |
| 200 | 11 pts | 8 pts | 14 pts | 10 pts |
| 500 | 7 pts | 5 pts | 9 pts | 6 pts |
| 1000 | 5 pts | 3.5 pts | 6 pts | 4.4 pts |

- Items needed at p = 0.8 for a given true difference (derived, same assumptions): 2 points needs about 6,280 unpaired or 3,140 paired; 5 points 1,005 / 503; 10 points 252 / 126; 15 points 112 / 56; 20 points 63 / 32. This is why Miller's "at least 1,000 questions" and a product team's 50-case suite are answering different-sized questions.
- Reproduction checks (derived): Miller's 969 = (1.96 + 0.84)^2 x (1/9) / 0.03^2 = 969.0; Miller's MDE 13.2% to 7.5% reproduces as 13.3% and 7.6% from Eq. 10 (rounding of z values).
- The three post-Miller threads do not contradict Miller; they bound where his defaults apply. A workable synthesis for a teaching audience: (a) n in the thousands, one variant: Miller's CLT SE is fine; (b) n below a few hundred, or a rate near 0/1: Wilson or Beta posterior; (c) comparing two variants on the same items: always pair, and if the difference is small, add trials per item before adding items; (d) grouped items at small n: hierarchical Bayes, or at minimum report per-cluster means and treat the cluster count as the effective n.
- The exact sign test (McNemar's exact test) on discordant pairs is the natural small-suite paired test. Derived two-sided p-values: 5 wins vs 0 losses p = 0.0625; 6 vs 0 p = 0.031; 7 vs 1 p = 0.070; 12 vs 4 p = 0.077; 9 vs 3 p = 0.146. So on a small suite, a variant must flip at least six cases in its favour with none against before a conventional 5% test agrees. (Wang's paper supports the sign-test equivalence at large n; the exact small-n p-values are my arithmetic.)

### Gaps
- I found no 2026 paper that critiques Miller directly; the critique literature is Bowyer et al. (2025) plus Wang's refinement. A search specifically for 2026 critiques returned none.
- No peer-reviewed head-to-head of Wilson vs Bayesian vs hierarchical methods on real agentic (multi-trial, clustered, small-n) eval data was found; Bowyer et al. is simulation-led.
- statsforevals.com's "Which Method?" decision page and any simulation evidence behind `method="auto"` were not on the page I fetched, so I cannot state what test evalstats picks at a given n.
- A GitHub repo `vipul21435/evalstats` ("Error bars, paired comparisons, pass@k and sample-size planning ... with clustered standard errors") appeared in search and resolves; it appears to be a different project from Arawjo's `evalstats` package, sharing the name. I did not verify the relationship. — [vipul21435/evalstats](https://github.com/vipul21435/evalstats)
- I could not confirm the ICML 2025 venue of Bowyer et al. from the arXiv page itself (it lists "ICML" as a keyword); a search result listed it under ICML.
- Whether HiBayES has seen adoption outside AISI in 2026 is unknown.

---

## 2. How much run-to-run variance do modern agents show, how many trials are recommended, and what do pass@k, pass^k and the reliability metrics say about consistency versus capability?

### Takeaway
On a 500-task coding benchmark a single run moves by 2 to 6 percentage points from run to run even at temperature 0, and infrastructure settings can add a further 2 to 6 points, so single-run differences of a few points are not evidence. The 2026 reliability literature (Princeton's twelve-metric framework, ICML 2026) finds that consistency has improved much more slowly than accuracy, and recommends reporting it as a separate dimension rather than folding it into a pass rate.

### Cited Findings

**Measured run-to-run variance**
- Bjarnason, Silva, Monperrus (KTH), "On Randomness in Agentic Evals", arXiv 2602.07150, v3 dated 2026-03-25, preprint. Setup: SWE-bench Verified (500 tasks), 10 independent runs each for 3 models x 2 scaffolds at two temperatures; 60,000 trajectories. — [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- Single-run pass@1 ranges span 2.2 to 6.0 percentage points across configurations; run-to-run SDs reach about 1.8 points, and at temperature 0 they are still 1.0 to 1.8 points. Example: one configuration scored 31.4% ± 1.0% with individual runs from 28.8% to 32.4%. — [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- Runs diverge almost immediately: within the first 1% of the trajectory (median first divergence at token 5 at T = 1.0 and token 56 at T = 0 for one configuration). The authors attribute temperature-0 variance to inference-engine and environment non-determinism. — [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- Power analysis for number of full-benchmark runs: n ≥ 2 ( (z_{alpha/2} + z_beta) / (Delta/sigma) )^2 (two-sample, equal n, known equal sigma). At p < 0.05 and 80% power: detecting a 2-point improvement needs 9 runs per agent at sigma = 1.5 points (2 runs at sigma = 0.7); detecting 1 point needs 36 runs at sigma = 1.5 (8 at sigma = 0.7). — [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- pass@k vs pass^k on the same data: one agent has pass@1 34.4%, pass@5 52.9%, pass^5 15.5%; another has pass@1 63.5%, pass@5 76.2%, pass^5 49.1%. Recommendations: "(1) estimate pass@1 from multiple independent runs per task, especially when measuring small improvements", "(2) use statistical power analysis to determine the number of runs needed to detect expected effect sizes", "(3) consider metrics like pass@k (optimistic bound) and pass^k (pessimistic bound) with k>1". — [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- Infrastructure as a separate noise source: Anthropic (Gian Segato), "Quantifying infrastructure noise in agentic coding evals", 2026-02-05. On Terminal-Bench 2.0 the gap between the most- and least-resourced container setups was 6 percentage points (p < 0.01); infra error rates were 5.8% at strict (1x) limits, 2.1% at 3x, 0.5% uncapped. On SWE-bench (227 problems x 10 samples) 5x RAM scored 1.54 points above 1x. — [Anthropic, infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
- "Naive binomial confidence intervals already span 1-2 percentage points", and infrastructure confounders "stack on top of that, not within it." "leaderboard differences below 3 percentage points deserve skepticism" until configuration is documented and matched; "running at multiple times and on multiple days would help average out the noise." — [Anthropic, infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
- Prediction noise exceeds data noise under paired comparison on SWE-bench Verified (data SE about 1/6 of prediction SE). — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- Older foundational result still cited: temperature 0 on a production endpoint produced 80 unique completions in 1,000 requests (2025-09-10). — [Thinking Machines](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)

**Definitions**
- pass@k: probability of at least one success in k attempts; pass^k: probability that all k attempts succeed. "If your agent has a 75% per-trial success rate and you run 3 trials, the probability of passing all three is (0.75)³ ≈ 42%." (2026-01-09.) — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- pass^k originates with τ-bench (2024-06, foundational). — [τ-bench](https://arxiv.org/abs/2406.12045)
- Inspect's `pass_k` reducer uses the draw-without-replacement estimator C(correct, k) / C(total, k) per sample; `pass_at` is the at-least-one counterpart (as recorded in the digest; reference page re-checked as resolving, not re-read). — [Inspect scorer reference](https://inspect.aisi.org.uk/reference/inspect_ai.scorer.html)

**Reliability as its own science (2026)**
- Rabanser, Kapoor, Kirgis, Liu, Utpala, Narayanan (Princeton), "Towards a Science of AI Agent Reliability", arXiv 2602.16666, v1 2026-02-18, v3 2026-06-02, accepted at ICML 2026. Four dimensions (consistency, robustness, predictability, safety) and twelve metrics; 15 models on GAIA (165-task validation split) and a 26-task verified subset of τ-bench airline; K = 5 runs per task. — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Outcome consistency: C_out = (1/T) sum_t (2 p_hat_t - 1)^2, where p_hat_t is task t's success rate over K runs. It is 1 when every task always passes or always fails and 0 when every task is a coin flip — so it is independent of the accuracy level. — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Other consistency metrics: trajectory consistency by action-type distribution (Jensen-Shannon divergence between runs) and by action sequence (normalised Levenshtein distance); resource consistency C_res = exp(-mean coefficient of variation) of cost, time and API calls. — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Headline: "recent capability gains have only yielded small improvements in reliability"; "outcome consistency remains low across all models"; agents show "substantially higher distribution consistency than sequence consistency" (they pick the same kinds of actions but not in the same order); "resource consistency results reveal high variance in token and compute usage across runs." Gains were moderate on τ-bench and barely present on GAIA. — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Framing: "compressing agent behavior into a single success metric obscures critical operational flaws"; the paper ties the capability/reliability gap directly to the divergence between pass@k and pass^k. It suggests organisations set minimum consistency and safety thresholds before moving from pilot to production, and gives "succeeds on at least 95% of runs" as an example pass criterion. Not all consistency is desirable (creative tasks). — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Interactive results: HAL Reliability Dashboard. The HAL site states the team has paused adding new models to the accuracy leaderboard to focus on reliability measurement. — [HAL reliability dashboard](https://hal.cs.princeton.edu/reliability); [HAL](https://hal.cs.princeton.edu/)
- No trial count is prescribed by Anthropic's agent-evals guidance: "Because model outputs vary between runs, we run multiple trials to produce more consistent results", with no number given. — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**Leads seen only in search snippets (not confirmed in primary text)**
- ComponentBench (arXiv 2608.18307, 2026-08-18): a snippet reported aggregate run-to-run deviation of at most 1.4% while 17.3% of tasks flip outcome between runs. The abstract page does not contain these numbers; unverified. — [ComponentBench](https://arxiv.org/abs/2608.18307)
- arXiv 2609.08832 (2026-09): snippet says a GPT-4.1 ReAct agent on AppWorld passes all five runs on only 53% of tasks despite a 77% per-run average. Unverified. — [Closing the Consistency Gap](https://arxiv.org/abs/2609.08832)
- ReliabilityBench (arXiv 2601.06112, 2026-01): snippet notes that under independence pass^k = (pass^1)^k but "stochastic coupling often causes deviations". Unverified beyond the snippet. — [ReliabilityBench](https://arxiv.org/abs/2601.06112)
- "On the Reliability of Computer Use Agents" (arXiv 2604.17849, 2026-04): snippet says pass^k summarises across tasks and misses per-task variation, so the authors add paired tests across repeated runs. Unverified. — [arXiv 2604.17849](https://arxiv.org/abs/2604.17849)
- "Beyond pass@1" (arXiv 2603.29231, 2026-03) and "Identical Runs, Different Results" (arXiv 2609.33812, 2026-09; snippet: 584 runs, a larger model scored higher by less than one run-to-run SD). Unverified. — [arXiv 2603.29231](https://arxiv.org/abs/2603.29231); [arXiv 2609.33812](https://arxiv.org/abs/2609.33812)

### Inferences
- pass^k and pass@k under independence (derived: p^k and 1 - (1-p)^k):

| Per-trial p | pass^3 | pass^5 | pass^8 | pass^10 | pass@3 | pass@5 |
|---|---|---|---|---|---|---|
| 0.75 | 42.2% | 23.7% | 10.0% | 5.6% | 98.4% | 99.9% |
| 0.80 | 51.2% | 32.8% | 16.8% | 10.7% | 99.2% | 99.97% |
| 0.90 | 72.9% | 59.0% | 43.0% | 34.9% | 99.9% | ~100% |
| 0.95 | 85.7% | 77.4% | 66.3% | 59.9% | ~100% | ~100% |
| 0.99 | 97.0% | 95.1% | 92.3% | 90.4% | ~100% | ~100% |

- The independence formula is a floor for pass^k, not a prediction, when tasks differ in difficulty. Check against Bjarnason et al.: pass@1 = 63.5% would give 0.635^5 = 10.3% under a homogeneous-independent model, but the measured pass^5 is 49.1%. The gap exists because most tasks are near-deterministic (always pass or always fail) and only a minority flip. This is exactly what C_out measures, and it is a good exercise: the same average pass rate is compatible with very different pass^k.
- C_out worked values (derived from the formula): a task passing 5/5 or 0/5 contributes 1.0; 4/5 or 1/5 contributes (0.6)^2 = 0.36; 3/5 or 2/5 contributes (0.2)^2 = 0.04. A suite where 80% of tasks are stable and 20% are 3/5 flippers scores 0.8 + 0.2 x 0.04 = 0.808.
- The power-analysis numbers reproduce (derived): 2 x ((1.96 + 0.84)/(2/1.5))^2 = 8.8, rounded up to 9; for 1 point, 35.3, rounded up to 36.
- Run-to-run SD of 1 to 1.8 points on a 500-task benchmark is smaller than the binomial sampling SE of a single run at that size (sqrt(0.3 x 0.7 / 500) ≈ 2.0 points at p = 0.3), consistent with many tasks being deterministic. On a 50-task suite the same per-task flip behaviour gives a run-to-run SD roughly sqrt(10) ≈ 3.2 times larger, i.e. several points per run, before any infrastructure effects. (Scaling argument is mine, not from a source.)
- Trial-count guidance in the 2026 literature is conditional rather than a fixed number: K = 5 (Princeton), 10 runs (KTH, enough for 2-point effects only), K = 3 as a practitioner floor (see question 4). The consistent recommendation is to choose K from a power calculation using your own measured SD.
- Three distinct noise layers should be kept apart when teaching: sampling noise from a finite task set, prediction noise from model stochasticity, and infrastructure noise from the harness. Only the second is reduced by repeated trials; the third needs matched, documented configuration.

### Gaps
- The Princeton paper's per-model consistency values and the accuracy-vs-reliability trend slopes are in figures that my fetch could not read; I can report the direction ("reliability gains lag behind accuracy gains") but not magnitudes.
- I found no primary 2026 source reporting the fraction of tasks that flip across runs with verified numbers; the ComponentBench and AppWorld figures are snippet-only.
- Bjarnason et al. used open-weight models (Qwen3-32B, DeepSWE-preview, Devstral-2); whether frontier closed models show the same 2 to 6 point range on SWE-bench Verified was not established by a source I read.
- No source gives an evidence-based default K for product teams' small suites; guidance is "measure, then power".
- METR-specific 2026 material on variance or time-horizon confidence intervals was not retrieved in this session.

---

## 3. What does the measurement-validity literature now say (construct validity, benchmark-quality reviews, IRT and psychometrics, saturation and contamination), and how does it apply to small in-house suites?

### Takeaway
The 2025-2026 reviews agree that most benchmarks do not show they measure what they claim: only about half present any construct-validity evidence, 16% do any statistical testing, and nearly half of 60 widely reported benchmarks are saturated. The transferable lesson for an in-house suite is a short checklist — define the phenomenon, sample items representatively, keep a held-out set, report uncertainty, and do error analysis — rather than any particular psychometric model.

### Cited Findings

**"Measuring what Matters" (the central review)**
- Bean, Kearns, Romanou, Hafner et al. (42 authors, Oxford Internet Institute-led), "Measuring what Matters: Construct Validity in Large Language Model Benchmarks", arXiv 2511.04703, submitted 2025-11-03, NeurIPS 2025 Datasets and Benchmarks Track. Systematic review of 445 benchmarks by 29 expert reviewers. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Definitions: 78.2% of benchmarks define their phenomenon; of those, 52.2% use a widely agreed definition and 47.8% a contested one; 61.2% treat the phenomenon as composite. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Tasks and data: under 10% use complete real-world tasks; 40.7% use constructed tasks (28.5% exclusively); 42.6% reuse existing data; 38.2% use human exams or other pre-existing sources; 31.2% generate data with LLMs; 47.5% use synthetic examples. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Sampling: 39.3% use convenience sampling at least partly (my sum of the paper's 12.3% exclusively and 27.0% partly); 17.1% use random sampling (7.0% exclusively). — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Scoring: exact match is used by 81.3% (40.7% exclusively); LLM-as-judge by 17.1% (3.1% exclusively); human ratings by 13.0%. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Statistics and validity evidence: 16.0% use uncertainty estimates or statistical tests; 53.4% present evidence for construct validity (35.2% compare to other benchmarks, 32.4% to a human baseline, 31.2% to a more realistic setting). — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- The eight recommendations: (1) define the phenomenon; (2) measure the phenomenon and only the phenomenon; (3) construct a representative dataset for the task; (4) acknowledge limitations of reusing datasets; (5) prepare for contamination; (6) use statistical methods to compare models; (7) conduct an error analysis; (8) justify construct validity. Selected sub-items verbatim: "Report the benchmark's sample size and justify its statistical power"; "Report uncertainty estimates for all primary scores to enable robust model comparisons"; "Maintain a held-out set of task items to facilitate ongoing, uncontaminated evaluation"; "Investigate whether failure modes correlate with non-targeted phenomena (confounders) rather than the intended construct"; "Validate any automated output parsing techniques for accuracy, consistency and bias". — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- On size: "smaller well-designed datasets can provide higher construct validity than larger datasets at less computational cost." A checklist is in the paper's Appendix A; the review codebook is published as a dataset. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703); [codebook dataset](https://huggingface.co/datasets/ambean/construct-validity-review)

**Saturation**
- Akhtar, Reuel et al. (37 authors, including Koyejo, Biderman, Solaiman), "When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation", arXiv 2602.16763, v1 2026-02-18, v4 2026-08-06, ICML 2026 (PMLR 306). 60 LLM benchmarks drawn from major developers' technical reports, characterised on 14 properties. — [Akhtar et al. 2026](https://arxiv.org/abs/2602.16763); [PMLR page](https://proceedings.mlr.press/v306/akhtar26a.html)
- "nearly half of our benchmarks exhibit saturation", with rates rising with benchmark age; resilience "is impacted by expert-curation, not by public test data" — i.e. keeping the test set private showed no protective effect, while expert-curated benchmarks resisted saturation better than crowdsourced ones. — [Akhtar et al. 2026](https://arxiv.org/abs/2602.16763)
- Anthropic's definition for in-house suites: "Eval saturation occurs when an agent passes all of the solvable tasks, leaving no room for improvement." — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- HAL declares CORE-Bench "solved" after a Claude Opus 4.5 + Claude Code scaffold result (95.5% with manual grading fixes) — a concrete 2026 case where grading corrections, not capability alone, moved a benchmark to its ceiling. — [HAL](https://hal.cs.princeton.edu/)

**Validity of agentic benchmarks specifically**
- Zhu et al. (25 authors, including Liang, Kang, Steinhardt, Zaharia, Stoica), "Establishing Best Practices for Building Rigorous Agentic Benchmarks", arXiv 2507.02825, 2025-07-03 (v5 2025-08-07). Introduces the Agentic Benchmark Checklist (ABC). Task-setup and reward-design flaws can under- or over-estimate agent performance "by up to 100% in relative terms"; SWE-bench Verified uses insufficient test cases; τ-bench counts empty responses as successful; applying ABC to CVE-Bench reduced performance overestimation by 33%. Older than the window but the standard reference for grader validity. — [Zhu et al. 2025](https://arxiv.org/abs/2507.02825)
- HAL's log analysis found agents taking shortcuts that invalidate the measurement, e.g. "searching for the benchmark on HuggingFace instead of solving a task" and "misusing credit cards in flight booking tasks". — [HAL paper](https://arxiv.org/abs/2510.11977)
- Princeton's reliability study itself had to drop to a 26-task "verified" subset of τ-bench airline after excluding flawed tasks from the original 50. — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Anthropic: "a 0% pass rate across many trials (i.e. 0% pass@100) is most often a signal of a broken task." — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**Item response theory and psychometric approaches**
- Hofmann et al. (Allen Institute for AI / University of Washington and others), "Fluid Language Model Benchmarking", arXiv 2509.11106, 2025-09-14, COLM 2025. Fits an IRT model to existing results and selects items adaptively per model (computerised adaptive testing). Claims higher validity and lower variance on MMLU with "fifty times fewer items", and better behaviour on saturation; reports "superior performance in all" four dimensions (efficiency, validity, variance, saturation). — [Hofmann et al. 2025](https://arxiv.org/abs/2509.11106)
- Zhou et al., "Lost in Benchmarks? Rethinking Large Language Model Benchmarking with Item Response Theory" (PSN-IRT), arXiv 2505.15055, v3 2026-01-16, AAAI 2026 (Oral). 11 benchmarks, 41,871 items. Finds "significant and varied shortcomings" in benchmark measurement quality; smaller benchmarks built by selecting items with PSN-IRT keep "stronger alignment with human preference." — [Zhou et al. 2025/2026](https://arxiv.org/abs/2505.15055)
- Snippet only: the same paper reportedly finds widespread item saturation and treats outlier-high guessing parameters as a possible contamination signal. Not confirmed in the abstract. — [Zhou et al. 2025/2026](https://arxiv.org/abs/2505.15055)
- Snippet only: ATLAS adaptive testing (arXiv 2511.04689, 2025-11) reports about 90% item reduction; "Auditing LLM Benchmarks with IRT" (arXiv 2605.30504, 2026-05) reports about 95% precision among its top 200 flagged mislabeled items using responses from 114 models. — [ATLAS](https://arxiv.org/abs/2511.04689); [arXiv 2605.30504](https://arxiv.org/abs/2605.30504)

**Contamination**
- Bean et al. recommend contamination tests, a maintained held-out set, and investigating pre-exposure of source materials; 38.2% of benchmarks draw on human exams or other pre-existing sources. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- HAL encrypts published agent traces to prevent benchmark contamination. — [HAL](https://hal.cs.princeton.edu/)

### Inferences
- Mapping the eight recommendations onto a product team's suite of 20 to 200 cases: (1) write one sentence stating what the suite claims to measure and what it excludes; (2) check that failures are caused by the target behaviour and not by output-format parsing or harness limits; (3) sample cases from real traffic strata instead of whatever was convenient — the review shows convenience sampling is the common failure; (4)/(5) keep a held-out slice that is never used for prompt tuning, since tuning against the reported set is the in-house analogue of contamination; (6) report n and an interval; (7) read failures and ask whether they share a confounder; (8) spot-check that suite score tracks a real outcome (production metric, human rating).
- IRT needs many test-takers per item (the cited audits use dozens to 114 models). A product team comparing two or three variants cannot fit item parameters, so IRT is not directly usable in-house. Its cheap proxies are: per-item pass rate across variants and trials (difficulty), and whether an item ever separates a better variant from a worse one (discrimination). Items that always pass or always fail carry no comparison signal and can move to a regression tier. This is my extrapolation; none of the IRT papers address suites this small.
- The saturation result that private test sets did not protect benchmarks suggests saturation is mostly about item difficulty relative to capability, not leakage; for an in-house suite the response is to keep adding hard cases from production failures, which the digest already recommends.
- Grader validity and statistical validity are separate axes. A suite can have tight intervals around a number that reflects a broken grader (CORE-Bench, τ-bench empty responses). Error bars answer "how precisely?", not "of what?".

### Gaps
- The quantitative definition of saturation and the 14 properties in Akhtar et al. were not on the abstract page; a third-party summary said 29 of 60 benchmarks were high or very high saturation, which I did not verify.
- I did not retrieve Stanford HAI / CRFM or AI Index 2026 material on benchmark validity; a secondary article attributing a saturation statistic to the AI Index was unverified and is not used.
- No source directly studies construct validity of small, private, product-team eval suites; the application above is inference from benchmark-scale reviews.
- The official NeurIPS proceedings URL for Bean et al. did not resolve from my link check (connection refused), though it appeared in search results: https://proceedings.neurips.cc/paper_files/paper/2025/hash/1967e0fc3aa6cbbace562f5cb8e3954e-Abstract-Datasets_and_Benchmarks_Track.html
- Fluid Benchmarking's numeric validity and variance gains beyond the "fifty times fewer items" claim were not in the abstract.

---

## 4. What practical guidance exists for small eval suites (tens to low hundreds of cases): what is supportable, how to report honestly, and how to set regression gates without flakiness?

### Takeaway
A small suite can support claims about large effects and about specific failures, and it cannot support claims about differences of a few points; honest reporting means stating n, trials per case, and a Wilson or Bayesian interval, and comparing variants case-by-case on the same items. For gates, the practitioner consensus (vendor-level evidence, not research) is to measure the noise floor on an unchanged build first, gate on a paired delta against a same-job baseline, and repeat cases at least three times.

### Cited Findings
- Small suites are legitimate when effects are large: "20-50 simple tasks drawn from real failures is a great start"; early in development "this large effect size means small sample sizes suffice", while more mature agents may need larger evals to detect smaller effects. (2026-01-09.) — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- At these sizes the CLT interval is the wrong tool: it under-covers, collapses at 0% or 100%, and can leave [0, 1]; use Wilson or a Beta posterior; bootstrap also under-covers. — [Bowyer et al. 2025](https://arxiv.org/abs/2503.01747)
- Very small data (under 20 points per evaluation) with nested structure is the stated target of hierarchical Bayesian GLMs. — [HiBayES](https://arxiv.org/abs/2505.05602)
- For a two-variant comparison, pairing on the same items is what makes small differences detectable, and averaging several predictions per item is the main lever when prediction noise dominates. — [Wang 2025/2026](https://arxiv.org/abs/2512.21326)
- "smaller well-designed datasets can provide higher construct validity than larger datasets at less computational cost." — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Reporting minimums from the validity review: report sample size and justify power; report uncertainty for all primary scores. — [Bean et al. 2025](https://arxiv.org/abs/2511.04703)
- Differences under 3 points on agentic coding evals "deserve skepticism" without matched, documented infrastructure; and a 10-run study can reliably detect 2-point but not smaller improvements. — [Anthropic, infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise); [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- Gate calibration (OpenRouter tutorial, unsigned vendor post, page date shown as "10/1/2026" — ambiguous between 1 October and 10 January 2026): "Measure the threshold from repeated runs against an unchanged branch rather than picking a strict number." Run the suite six times on unchanged `main`; "That lowest pass rate is your floor, and you set your threshold at or below it." Each case is sampled several times (default three) with a majority vote; raise the sample count until the floor stops moving. — [OpenRouter tutorial](https://openrouter.ai/blog/tutorials/how-to-gate-pull-requests-on-llm-evals-in-ci/)
- Granularity problem, same source: with three cases the pass rate can only be 0, 0.33, 0.67 or 1.00, and "With three cases, one case failing on one of those six runs gives a floor of 0.67", which blocks a PR with no regression; the post recommends growing toward 20 or more cases. When a PR fails by one case, rerun against `main`: if `main` fails too it is noise, otherwise treat it as a regression. Triage order for flaky cases: loosen brittle string assertions, then determinism settings (only where the model supports them), then repeated sampling. — [OpenRouter tutorial](https://openrouter.ai/blog/tutorials/how-to-gate-pull-requests-on-llm-evals-in-ci/)
- An illustrative open-source gate (single repo, not a standard) measures a noise floor from K = 3 repeats per case and "refuses a gate inside the judges' own noise floor"; it also reports human agreement, Cohen's kappa and judge self-consistency. — [llm-eval-gate](https://github.com/jkelly-dev1/llm-eval-gate)
- A development-time A/B method for coding agents (single-author preprint, 2026-09-17): only 22 of 113 tasks (19.5%) in one benchmark's published trials tracked full-benchmark performance reliably from a single run; a fixed, budget-capped task subset is proposed for baseline-vs-candidate decisions, explicitly not for rankings. In its case study the cost reduction was significant (USD 1.75 vs 4.18, p = 0.008) while the score change (42.36% vs 36.46%) was not (p = 0.326). — [DeltaSelect](https://arxiv.org/abs/2609.19607)
- Deployment-gating framing from research: require an agent to succeed "on at least 95% of runs" on critical tasks, and set minimum consistency thresholds before production. — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Regression suites "should maintain near 100% pass rates" while capability suites start low (from the digest; page re-verified live). — [Anthropic, Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Inferences
- What a small suite supports and does not (derived from the tables in question 1):
  - Supportable: "variant B fixes these six named cases and breaks none" (exact sign test p = 0.031); "pass rate is somewhere between 67% and 89%" for 40/50; "the failure rate is not above about 6%" after 50/50 clean passes (rule of three); a 20-point or larger improvement on 50 paired cases.
  - Not supportable: "B is 4 points better than A" on 50 cases (paired MDE at p = 0.8 is about 16 points); "we are at 100%" from 20/20 (Wilson lower bound 84%); ranking three or more variants separated by one or two cases; any claim from a single trial per case when cases are known to flip.
- Why absolute-threshold gates flake (derived, binomial): a system with true pass rate 0.90 on a 20-case suite scores 16/20 or worse 13.3% of the time, and 17/20 or worse 32.3% of the time. A gate at "≥ 85%" (needs 17/20) fails about one run in eight with no regression; a gate at "≥ 90%" (needs 18/20) fails about one run in three. On 100 cases, the same system scores 84 or below only 4.0% of the time.
- A gate design consistent with the cited sources: (a) split the suite into a regression tier of deterministic, must-pass cases gated at 100% with a retry-and-majority rule, and a capability tier gated on a paired delta; (b) run baseline and candidate in the same job on the same infrastructure so shared noise cancels; (c) run K ≥ 3 trials per case and analyse per-case means; (d) fail only when the paired interval for the difference excludes zero on the harmful side, or when a named must-pass case fails on a majority of trials; (e) recompute the noise floor whenever the model, harness or suite changes. Steps (a) to (e) are my synthesis; individual elements are sourced above.
- Honest reporting template for a small suite (synthesis): "42/50 cases passed (84%; 95% Wilson interval 71% to 92%), 3 trials per case, per-case majority; versus baseline on the same cases: 5 fixed, 1 broken (exact sign test p = 0.22); model/harness/config versions X." The interval and p-value in this example are derived by me: Wilson for 42/50 is [0.715, 0.917]; two-sided exact sign test for 5 vs 1 is 0.219.
- With clustered cases (several cases from one template or one customer scenario), the effective sample size is closer to the number of clusters; with small n the safer report is per-cluster results rather than a pooled interval, given that the clustered SE under-covers there.

### Gaps
- I found no peer-reviewed or lab-authored 2026 study that validates a noise-floor methodology for CI gates on suites under about 50 cases. The gating guidance is from vendor tutorials and individual repos and should be presented as heuristic.
- Sequential or "always-valid" testing for repeatedly run eval gates (the multiple-looks problem of checking every PR) did not surface in any source I read; it is a known issue in A/B testing generally but I have no eval-specific citation.
- Multiple-comparison handling when a team tracks many metrics per PR is offered by `evalstats` (`compare_prompts`) but I found no documentation of which correction it applies.
- The OpenRouter post's date format is ambiguous and it has no named author.
- Hamel Husain / Shreya Shankar's current position on statistics for small suites was not re-fetched this session; the digest records their ~100-example CI guidance as of September 2026.

---

## 5. How are cost, latency and token usage being treated as first-class metrics?

### Takeaway
Cost-controlled evaluation moved from an argument (AI Agents That Matter, 2024) to infrastructure in 2026: HAL (ICLR 2026) reports accuracy and dollar cost for every agent and plots a cost-accuracy frontier, and Princeton's reliability framework adds run-to-run variance of cost and tokens as a metric in its own right. The evidence that cost and quality need separate significance tests is thin but points one way: cost differences are often easier to establish than score differences.

### Cited Findings
- Foundational (2024-07): Kapoor et al., "AI Agents That Matter", argue accuracy-only benchmarking yields needlessly complex, costly agents and call for joint accuracy-cost optimisation and holdouts. — [Kapoor et al. 2024](https://arxiv.org/abs/2407.01502)
- HAL: Kapoor, Stroebl, Kirgis et al. (31 authors, Narayanan last), "Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation", arXiv 2510.11977, submitted 2025-10-13; the HAL site states it was accepted to ICLR 2026. 21,730 agent rollouts across 9 models and 9 benchmarks (coding, web navigation, science, customer service) at a total cost of about $40,000; the harness cuts evaluation time "from weeks to hours"; 2.5B tokens of agent logs released. — [HAL paper](https://arxiv.org/abs/2510.11977)
- Counter-intuitive finding from the same study: "higher reasoning effort reducing accuracy in the majority of runs." — [HAL paper](https://arxiv.org/abs/2510.11977)
- HAL site (fetched 2026-11-09): each entry reports accuracy (%) and cost ($); a "Cost-Controlled Agent Evaluations" section shows a cost-performance frontier and states "Agents can be 100x more expensive while only being 1% better", which downstream developers "can't tell ... from 1D leaderboards." Benchmarks: AssistantBench, CORE-Bench Hard, GAIA, Online Mind2Web, SciCode, ScienceAgentBench, SWE-bench Verified Mini, TAU-bench Airline, USACO. The site now reports 26,597 rollouts. — [HAL](https://hal.cs.princeton.edu/)
- Search-result summary of the HAL paper (not confirmed in the abstract I fetched): the most expensive models are rarely on the Pareto frontier, and task-specific scaffolds usually score higher than generalist ones at higher cost. — [HAL paper](https://arxiv.org/abs/2510.11977)
- Resource consistency as a reliability metric: C_res = exp(-mean coefficient of variation) over cost, time and API calls; "resource consistency results reveal high variance in token and compute usage across runs." The paper's illustration: "1,000 tokens and 3 tool calls on one run, but 50,000 tokens and 47 tool calls on an identical request", "a 50× cost swing" (an illustrative example, not a measured result). — [Rabanser et al. 2026](https://arxiv.org/abs/2602.16666)
- Resources given to the agent also change the score, so they are part of the cost-accuracy picture: "resource configuration for agentic evals should be treated as a first-class experimental variable"; Anthropic recommends evals "specify both parameters per task" (a guaranteed floor and a hard ceiling) and report the multiplier used. — [Anthropic, infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
- Cost can be the significant result when quality is not: in one 13-evaluation case study, cost fell 58.1% (USD 1.75 vs 4.18, p = 0.008) while the score change was not significant (p = 0.326); total evaluation spend was USD 27.86. Single-author preprint, 2026-09-17. — [DeltaSelect](https://arxiv.org/abs/2609.19607)
- Evaluation's own cost is a design constraint: multi-run studies are expensive (60,000 trajectories and 25.58B tokens for ten runs of six configurations on SWE-bench Verified), which is the practical argument for power analysis before choosing K. — [Bjarnason et al. 2026](https://arxiv.org/abs/2602.07150)
- Adaptive, IRT-based item selection is pitched partly as a cost measure ("fifty times fewer items" on MMLU). — [Hofmann et al. 2025](https://arxiv.org/abs/2509.11106)

### Inferences
- Cost and latency are right-skewed and heavy-tailed, so a mean ± SD summary (as the digest notes skill-creator produces) hides the tail. A coefficient of variation per task across trials (the ingredient of C_res), plus median and a high percentile, is a more faithful small-suite report. The percentile suggestion is mine; C_res is from the Princeton paper.
- Worked C_res values (derived from the formula): mean CV of 0.1 gives exp(-0.1) = 0.905; CV 0.5 gives 0.607; CV 1.0 gives 0.368.
- A Pareto frontier is an exercise-friendly definition: a variant is on the frontier if no other variant is both at least as accurate and at most as costly, with one strict. With intervals on both axes, two variants whose accuracy intervals overlap should be ranked by cost — which is the practical content of "100x more expensive while only being 1% better".
- Because trials multiply eval cost, the three levers trade off explicitly: more items reduce data noise, more trials reduce prediction noise, and both cost money. Wang's result that prediction noise dominates under pairing implies that for a fixed budget on a paired comparison, extra trials on existing items are often the better purchase than new items — until data noise becomes the larger term.
- Paired analysis applies to cost as well as accuracy: per-task cost differences between variants on the same tasks will have much lower variance than the difference of two suite-level means.

### Gaps
- I could not confirm the HAL paper's specific Pareto-frontier findings from primary text; the abstract does not state them and the fuller claims came from search summaries. The official ICLR proceedings URL did not resolve from my link check (connection refused): https://proceedings.iclr.cc/paper_files/paper/2026/hash/a0928f924a344aaebbb7f6cd8d56e34c-Abstract-Conference.html
- HAL's site does not mention confidence intervals or multiple runs on its accuracy-cost leaderboards, and does not show token counts per entry; I found no statement on how uncertainty is displayed on the frontier.
- No source in this session gave statistical guidance specific to cost or latency distributions (e.g. which test or interval to use for skewed cost data, or how to handle prompt-caching in cost accounting; a search summary noted HAL lists incomplete caching cost accounting as a limitation, unverified).
- Latency as a first-class eval metric had almost no 2026 research coverage in what I retrieved; the treatment is in vendor docs already covered by the digest.
- No 2026 measured (as opposed to illustrative) figure for per-task cost variance across identical runs was confirmed from primary text.
