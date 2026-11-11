# Vally 0.16.0 → 0.21.0: source-verified delta

Read on 2026-11-09 from two local source trees, no network and no git:

- **Old:** 0.16.0 @ `b2b75cd` (the tree `vally-repo-digest.md` was built from).
- **New:** 0.21.0 @ `ca656e4` (`packages/core/package.json` version `0.21.0`).

This is a delta against `research/vally-repo-digest.md`. It covers `packages/`, `plugins/`, `samples/`, `README.md`, `AGENTS.md` and `CHANGELOG.md`. `docs-site/` is covered separately.

**Citation format.** `path:line` is a path in the **new** tree unless prefixed `old:`. Line numbers were read directly; a bare symbol name means I read the symbol but did not record the line.

**Labels.** *Read* = stated by source I read. *Inferred* = my conclusion from source, not stated by it. **UNCONFIRMED** = source could not settle it.

---

## Breaking for a 0.16-era learner (most important first)

1. **Node minimum is now `>=22.15.0`.** `package.json`, `packages/core/package.json`, `packages/cli/package.json` (`engines`), and `README.md` ("Requires **Node.js >=22.15.0**"). The 0.18.0 changelog says 22.14.0 (`CHANGELOG.md:83`), and `samples/README.md` still says `>=22.12.0`; both are stale against `engines`.
2. **Default LLM judge model is `gpt-5.6-terra`**, not `claude-sonnet-4.6` (`packages/core/src/graders/llm/prompt-grader.ts:67`). Any lesson that reasons about judge behaviour without pinning `judge_model` now gets a different judge.
3. **Unknown stimulus fields are a hard load error** (0.17). A typo such as `grader:` or a stray `rubrics:` on a stimulus now fails with `stimuli[i]: unknown field '…' (allowed: …)` (`packages/core/src/eval/loader.ts:148-181`).
4. **LLM judges no longer receive evidence in the prompt.** Evidence is always written to temp files and the judge reads it with `view`/`grep`. `output_delivery: inline` is rejected; `output_delivery: workspace` is deprecated (`packages/core/src/graders/llm/judge-evidence.ts:17-34`). The judge now sees the **complete** timeline, not a 50-head/50-tail truncation. Section 5 of the old digest is largely obsolete.
5. **Grading errors are reported as `ERROR`, not `FAIL`, and always exit 1.** A grader that cannot produce a valid verdict (`status: "error"`) makes the trial invalid, is shown as `ERROR`, and forces exit code 1 even without `--require-pass`. A valid failing verdict is `FAIL` and exits 0 unless `--require-pass` (`packages/cli/src/exit-policy.ts:15-19`, `packages/cli/src/commands/eval.ts:1601-1609`).
6. **`scoring:` and `--threshold` are still present.** The `grading-v2` removal the old digest warned about has **not** landed in 0.21. `scoring` gained a third field, `timeout` (`packages/core/src/eval/types.ts:541-546`).
7. **Custom executors must throw errors with `retryable: true`** to be retried (0.20). Message-based inference is gone (`packages/core/src/utils/error-classifier.ts:63-71`).
8. **Custom plugins: `withRolledUpGraderError()` removed (0.20); `configureTelemetry` → `configureTracing` (0.17); `cleanup({ preserveWorkspace })` (0.18).** An executor/backend still exposing `configureTelemetry()` makes the host **throw** (`packages/core/src/executor/types.ts`, `isTracingConfigurable`).
9. **Experiment files reject `filter`, `grader_plugins`, `executor_plugins`, `eval_plugin`** (0.18/0.19). Plugins move to `.vally.yaml` `plugins:` or CLI flags (`packages/core/src/experiment/loader.ts:28-39`).
10. **`plugins/executors/` and `plugins/providers/` are gone from the repo.** The claude-cli executor, the cca executor and the ger eval provider no longer exist in the 0.21 tree. Only `plugins/exporters/harbor` and `plugins/vally-grader-example` remain.
11. **`vally grade --workspace` now overrides the workspace for every input kind**, not just ATIF/session input (`packages/cli/src/commands/grade.ts:691-692`, `:1009-1016`).
12. **Reasoning effort is a free string validated against the model**, not the fixed enum `low|medium|high|xhigh` (`packages/core/src/graders/llm/types.ts:24-32`). Unavailable models are rejected before a session starts.
13. **`vally init` now scaffolds `agent_environment:`** (was the deprecated `environment:`) and suggests `model: gpt-5.5` (`packages/cli/src/templates/starter-eval.ts`).

---

## 1. eval.yaml schema

### Top level

Unchanged set (`packages/core/src/eval/loader.ts:134-146`, `EVAL_SPEC_TOP_LEVEL_FIELDS`): `name, description, version, type, tags, defaults, stimuli, scoring, agent_environment, environment, grading_environment`. Unknown keys were already rejected in 0.15.

### `defaults`: full current field list

`packages/core/src/eval/types.ts:78-110` (`EvalDefaults`):

| Field | Status | Notes |
|---|---|---|
| `backend` | **new (0.19)** | string or `{ name, args }`; `args` is a `key=value` string list or a JSON-compatible mapping (`packages/core/src/backend/selection.ts`, `validateBackendSelection`) |
| `runs` | unchanged | positive integer |
| `timeout` | unchanged | duration with unit suffix |
| `model` | unchanged | |
| `reasoning_effort` | **changed (0.20)** | any non-empty string (`loader.ts`: "must be a non-empty string") |
| `executor` | unchanged | string or `{ name, config }` |
| `exporter` | **new (0.21)** | array of `{ name, args }`; `args` values must be strings (`loader.ts:86-131`, `validateExporterDefaults`) |
| `judge_model` | unchanged | |
| `judge_timeout` | **new (0.20)** | per judge *turn*; positive duration with unit suffix |
| `judge_reasoning_effort` | **changed (0.20)** | any non-empty string |
| `judge_provider` | unchanged | |

`defaults.executor.config` for `copilot-sdk` now accepts `provider` **and `autoTier`** (`packages/core/src/executor/copilot-sdk-executor.ts:1833-1841`); any other key is rejected.

### `scoring`: full current field list

```ts
// packages/core/src/eval/types.ts:541-546
export interface ScoringConfig {
  weights?: Record<string, number>;
  threshold?: number;
  /** Total wall-clock budget for grading one stimulus (e.g. 5m, 30s, 500ms). Optional; when omitted, grading is unbounded. */
  timeout?: Duration;
}
```

### Stimulus: full current field list

`loader.ts:148-167` (`STIMULUS_FIELDS`): `name, prompt, turns, attachments, tags, environment, agent_environment, grading_environment, artifacts, graders, rubric, constraints, supported_executors, golden_patch, golden_trajectory, golden_custom_metrics, golden_command, simulation`.

- **New: `golden_command`** (0.17). A non-empty shell command string that `vally oracle` runs in the materialized workspace before grading (`types.ts:211-215`, `loader.ts`, `assertGoldenCommandShape`).

### Grader entry (`graders[]`)

`types.ts:411-438` (`StimulusGraderConfig`): `type, name, oracle_baseline, turn, scope, config`.

- **New: `oracle_baseline: allow-pass`** (0.21). The only accepted value; anything else fails load with `graders[gi].oracle_baseline must be "allow-pass"` (`loader.ts`, oracle-baseline check after the `name` check).
- `turn` is **0-based** (`types.ts:426`). This was also true in 0.16 (`old:packages/core/src/eval/types.ts:395`); `samples/README.md` now says "zero-based turns" explicitly.

### Which levels are strict about unknown keys

| Level | Unknown key behaviour in 0.21 | Source |
|---|---|---|
| Eval top level | **load error** | `loader.ts`, `validateEvalSpecTopLevelFields` |
| Stimulus | **load error (new in 0.17)** | `loader.ts:170-181`, `validateRawStimulusFields` |
| `grading_environment` and its `files[]` entries | load error (`only 'files'`, `only 'src' and 'dest'`) | `loader.ts:269-307` |
| `defaults.executor` object | load error (`allowed: name, config`) | `loader.ts:81` |
| `defaults.exporter[]` entries | load error (`allowed: name, args`) | `loader.ts:105` |
| `defaults.backend` object | load error (`allowed: name, args`) | `backend/selection.ts:95` |
| Built-in grader `config` | lint/validation **error** `invalid-grader-config` ("Unrecognized config field") | `packages/core/src/eval/validator.ts`, `validateObject` |
| `defaults` itself | **not checked** by the eval loader (I found no unknown-key check) | `loader.ts:370-435` |
| `scoring` | **not checked** for unknown keys (only weights/threshold/timeout values are validated) | `validator.ts`, `checkScoring*` |
| `agent_environment` / `constraints` / grader entry | no unknown-key check found in loader or validator | *Inferred from absence*; `constraints` only flags the four removed aliases |

### `simulation`

`types.ts:447-539`. MCP tools can now be simulated (0.17):

- `tool_overrides` keys may be an MCP runtime name such as `server-name-tool-name`.
- `BashPatternOverride`/`BashPattern` are renamed `ToolPatternOverride`/`ToolPattern` (old names kept as deprecated type aliases).
- Pattern entries gain `args` (regex per top-level argument name) and `pattern` (regex over `JSON.stringify(arguments)`), alongside `match` (shell `command`).
- New `structured_output` for MCP tools with an output schema.
- MCP tools may return success or error. Other non-shell first-party tools can still only simulate failures.

### New lint codes

`validator.ts` adds: `backend-selection-invalid`, `defaults-judge-timeout-invalid`, `deprecated-grader-config`, `exporter-defaults-invalid`, `invalid-oracle-baseline`, `scoring-timeout-invalid`. I found none removed. The six scoring rules the old digest expected to disappear (`invalid-scoring-weight-key`, `scoring-weight-sum`, `scoring-weight-coverage`, `scoring-defaults-applied`, `scoring-weights-without-threshold`, `scoring-threshold-range`) are all still present.

---

## 2. Scoring and verdict semantics in 0.21

**`scoring.weights`, `scoring.threshold` and `vally eval --threshold` all still exist** (`types.ts:541`, `packages/cli/src/commands/eval.ts:247-251`).

### Per trial

`packages/core/src/pipeline/grading.ts:349-365` builds the trial's `trajectory-grade`:

- `passed` = every grader's `passed` is true (or no graders).
- `score` = `computeWeightedScore`: unweighted mean of grader scores, or the weight-normalized sum by grader *type* when `scoring.weights` is set (`grading.ts:957-990`).
- top-level `status: "error"` if **any** grader detail has `status: "error"`.

The single pass rule (`packages/core/src/scoring/scorer.ts:54-60`):

```ts
export function resolveGradePass(grade, threshold: number | undefined): boolean {
  if (grade.status === "error") return false;
  return threshold !== undefined ? grade.score >= threshold : grade.passed;
}
```

So: with a threshold (spec or `--threshold`), trial pass = `score >= threshold`. Without one, trial pass = all graders passed. **An errored grade never passes**, including at `threshold: 0` (0.19 fix).

### Per stimulus

`packages/core/src/pipeline/plan.ts:1780-1850`. pass@k / pass^k come from the per-trial verdicts (`scorer.ts`, `computeStimulusScore`). A stimulus gets **no** score if any trial errored, has a missing grade, or has an errored grade (`hasInvalidTrial`).

Reporter state per stimulus (`packages/core/src/reporting/internal/result-card.ts:44-53`): `error` if any trial or grade errored, else `pass` if all executed trials passed, `flaky` if some did, `fail` if none did.

### Per eval

`plan.ts:1863-1895`:

- **Scored path** (threshold configured AND at least one scored stimulus AND no execution errors AND no top-level grading errors): `passed = mean(stimulus aggregateScore) >= threshold` (`scorer.ts:150-187`, `computeSkillScore`). `scoringApplied: true`.
- **Binary path** (everything else): every trial must have `passed === true` or `null` (unscored), with no execution errors. `scoringApplied: false`.
- 0.20: stimuli that run successfully with no graders pass without a score, even with a threshold.

Run `passed` = every eval passed (`plan.ts:1920`).

### `scoring.timeout` (0.19)

One wall-clock budget for **all graders of one stimulus trial** (`grading.ts:312-321`). On expiry the running grader and all remaining graders get a timeout error result; completed results are kept (`fillRemainingTimeouts`). Unset = unbounded. Applies in `eval`, `grade` and `oracle`. Graders receive `input.signal` and `input.timeoutMs` (remaining budget); `run-command` and `program` clamp their own timeout to it and kill the process tree.

### `defaults.judge_timeout` / `--judge-timeout` (0.20)

Per judge **turn**. Default 120 s (`graders/llm/types.ts:26`). Effective value is `min(judge_timeout ?? 120s, remaining scoring.timeout budget)` (`graders/llm/judge-helpers.ts:61-68`).

### ERROR vs FAIL

- A grader result has `status?: "success" | "error"`; absent means success (`packages/core/src/graders/types.ts:37,69-76`).
- If graders were configured and grading was enabled but no grade came back, a synthetic `grader-error` result with `status: "error"` is inserted (`packages/core/src/pipeline/normalize-trial-grade.ts`).
- Nested *advisory* errors (in `details` only, top-level status not error) do not invalidate the verdict but still count for the exit code via `hasGraderError()`.

### Exit codes

```ts
// packages/cli/src/exit-policy.ts:15-19
if (input.hasErrors) return { code: 1, reason: "error" };
if (input.requirePass && !input.passed) return { code: 1, reason: "verdict-gate" };
return { code: 0, reason: "completed" };
```

For `vally eval`, `hasErrors` = execution errors OR output-file write error OR any eval plan-time error OR any grader error anywhere in a trial's grade (`eval.ts:1601-1609`). `--require-pass` exists on `eval`, `grade`, `experiment run` and `experiment merge`. `vally oracle` exits 1 when any stimulus is not ok, and 130/143 on SIGINT/SIGTERM (`packages/cli/src/commands/oracle.ts:61,635`).

---

## 3. CLI

Commands in 0.21: `init, lint, eval, grade, oracle, compare, experiment run, experiment merge, simulate record, export, serve, ingest`. Flag diffs were produced by extracting every option string from `packages/cli/src/commands/*.ts` in both trees. **No flag was removed from any command.**

| Command | Added since 0.16 | Source |
|---|---|---|
| `eval` | `--in-place`, `--judge-timeout <duration>`, `--run-id <id>`; `--backend` now accepts built-in `docker` | `commands/eval.ts:242-272`, `:334-337` |
| `grade` | `--backend <name-or-package>`, `--backend-args <key=value>`, `--run-id <id>`; `--workspace` semantics widened | `commands/grade.ts:656-693` |
| `oracle` | `--diff-output <path>`, `--run-id <id>` | `commands/oracle.ts:216,245-248` |
| `compare` | `--judge-timeout <duration>` | `commands/compare.ts:91-95` |
| `experiment run` | `--grader-plugin`, `--executor-plugin`, `--eval-plugin`, `--judge-model`, `--judge-reasoning-effort`, `--judge-timeout`, `--otlp-endpoint <url>` | `commands/experiment.ts:161-215` |
| `experiment merge` | `--otlp-endpoint <url>` (and `--require-pass` is present) | `commands/experiment.ts:748-759` |
| `simulate record` | **new command**: `<input>` (trajectory file, results directory, or `-`), `-o, --output <path>`, `--mcp-server <name>` | `commands/simulate.ts:159-168` |
| `serve`, `ingest`, `init`, `lint`, `export` | no flag changes | |

Details worth teaching:

- **`vally eval --workspace <path> --in-place`** (`eval.ts:435-460`, `packages/core/src/pipeline/run.ts:2344-2367`). Runs directly in an existing directory. Requires local backend, `--workers 1`, `--max-retries 0` (both are forced). Rejects stimuli with `agent_environment.git/files/skills/commands`, `grading_environment.files`, or turn-scoped diff graders. Prints: "--in-place provides no isolation or reset… Automatic workspace patch capture is disabled." Help text: "diff graders require clean Git".
- **`--workspace <path>` without `--in-place`** is still "Root for preserved trial workspaces". Layout is `<root>/<variant>/<stimulus>` (`packages/core/src/pipeline/plan.ts:1037-1041`); for plain `vally eval` the variant is `main` (`eval.ts:1337`).
- **`--run-id <id>`**: "Stable identifier for this run (a UUID is recommended)". Defaults to `randomUUID()` (`eval.ts:470`). Required with `experiment run --shard`.
- **`experiment run --judge-*`** flags only affect the post-run `--compare` judge; they "require --compare; does not change trial grading".
- **`experiment run --backend`** "Replaces project backend loading and defaults.backend".
- **`--otlp-endpoint`** on `eval` and `experiment run/merge`: "When omitted, traces are written to the output directory."
- **`vally grade`** description: "Grade trajectories from stdin using graders defined in an eval spec"; `-e, --eval-spec` is required and is the "grader source of truth".
- **`vally oracle --stimulus`** default now includes stimuli with a `golden_command`.
- Current `eval` flag spellings in full: `-e, --eval-spec`, `--skill-dir`, `--work-dir`, `--agent, --executor`, `--model`, `--reasoning-effort`, `--timeout`, `--judge-timeout`, `--threshold`, `--require-pass`, `--output-dir`, `--output <format>` (choices: `jsonl`), `--run-id`, `--junit`, `--workspace`, `--in-place`, `--skip-grade`, `--skip-validate`, `--verbose`, `--workers`, `--runs`, `--max-retries`, `--judge-model`, `--judge-reasoning-effort`, `--suite`, `--tag`, `--grader-plugin`, `--executor-plugin`, `--eval-plugin`, `--param`, `--backend`, `--backend-args`, `--reporter-plugin`, `--otlp-endpoint`, `--shutdown-timeout` (`eval.ts:215-360`).

---

## 4. Built-in graders and LLM judges

### Roster: 36 built-in types, unchanged since 0.16

`createDefaultGraderRegistry` is byte-identical between the two trees (`packages/core/src/pipeline/grading.ts:151-191`). No grader added, removed or renamed.

- File state (6): `file-exists`, `file-not-exists`, `file-contains`, `file-not-contains`, `file-matches`, `file-not-matches`
- Diff (3): `diff-contains`, `diff-not-contains`, `diff-empty`
- Output (4): `output-contains`, `output-not-contains`, `output-matches`, `output-not-matches`
- Transcript (5): `transcript-contains`, `transcript-not-contains`, `transcript-matches`, `transcript-not-matches`, `assistant-contains-tool-output`
- Execution (3): `program`, `run-command`, `custom-metrics`
- Trajectory behaviour (7): `skill-invocation`, `system-event`, `tool-calls`, `max-repeat`, `loop-outcome`, `completed`, `exit-success`
- Metric thresholds (6): `token-budget`, `tool-call-count`, `turn-count`, `step-count`, `error-count`, `wall-time` (`graders/static/metric-threshold-grader.ts:242-277`)
- LLM (2): `prompt`, `panel`

### Config and behaviour changes

- **`oracle_baseline: allow-pass`** on any grader entry (0.21): under `vally oracle --no-golden-input`, a pass is classified `n/a` instead of `unexpected-pass` (`packages/core/src/pipeline/oracle.ts:731`).
- **`assertsAbsence` added to more graders**, so absence-only configs report `n/a` on the empty baseline: `file-not-*` (or `negate: true`), `diff-not-contains`, `diff-empty`, `system-event` with only `disallowed`, metric thresholds with only `max` (`graders/static/*.ts`). `tool-calls` and `skill-invocation` already had it.
- **`output-contains` / `transcript-contains` result metadata** now reports the *effective* `substring`, `case_sensitive` and `negate` (including defaults and name-implied negation) instead of echoing raw config (`graders/static/output-contains-grader.ts`, `transcript-contains-grader.ts`).
- **`run-command` / `program`** kill the whole process tree on timeout or grading-deadline abort (`packages/core/src/utils/exec-tree.ts`), and return `status: "error"` with "Command aborted by the grading deadline" on abort.
- **`prompt` / `panel` `reasoning_effort`**: any non-empty string (`eval/validator-schemas.ts`).

### LLM judge: what is the same

- `DEFAULT_SCORING = "scale_1_5"`; scales `binary | scale_1_5 | scale_1_10`; `DEFAULT_THRESHOLDS` all `0.5` (`graders/llm/types.ts:254-264`). This fills the old digest's "source not read" gap: normalization is `(clamped - min) / (max - min)` (`types.ts:267-272`), so on `scale_1_5` a raw 3 → 0.5 → pass.
- `score` = normalized `overall_score`; **`passed = normalizedOverall >= threshold`**; per-criterion scores are `details[]` only and do not feed the verdict (`prompt-grader.ts:444-494`). Labels ≥0.7 `correct`, ≥0.4 `partial`, else `incorrect`.
- System message and `submit_grade` schema are unchanged (`graders/llm/judge-tools.ts:125-137`).
- Default rubric fallback and `rubric_source` metadata unchanged (`graders/llm/judge-helpers.ts:8-14`).
- Judge failure → `status: "error"`, `passed: false`, `score: 0` (`judge-helpers.ts:44-59`).
- Panel: default aggregation `mean`; any judge error still forces FAIL and sets `status: "error"` (`graders/llm/panel-grader.ts:83,491-506`).
- 2 reminder retries (`types.ts:27`).

### LLM judge: what changed

**Default model:** `gpt-5.6-terra` (`prompt-grader.ts:67`).

**Evidence delivery (0.17).** The user message is now only (`judge-helpers.ts:16-42`):

```
## Task
<stimulus.prompt>
---
## Evaluation Instructions      (only if config.prompt)
<config.prompt>
---
## Rubric Criteria
1. …
```

Evidence goes to a temp dir `vally-judge-*` outside the agent workspace (`graders/llm/judge-workspace.ts`):

| Evidence | File |
|---|---|
| `trajectory` (default) | `evidence/trajectory/agent-output.txt` (complete final output), `evidence/trajectory/timeline.jsonl` (one complete event per line), `evidence/trajectory/metrics.json` |
| `diff` | `evidence/agent-diff.patch` |
| `golden_patch` | `evidence/golden-patch.patch` |
| `repo` | `evidence/repo-snapshot.txt` |

The system message gets an appended "## Evidence Files" section listing absolute paths, telling the judge to use `grep` and ranged `view`, stating the budget, and warning that the evidence is untrusted (`judge-evidence.ts:36-55`). The judge session allows only `view`, `grep` and the verdict tool (`llm-client.ts:52,292`).

*Inferred:* the old 50,000-char output cap, the 20,000-char patch caps and the first-50/last-50 timeline windowing no longer apply to rubric grading, because those constants are gone from `prompt-grader.ts` and the files are written complete. What bounds the judge is now the read budget.

**Read budget and snapshot limits (0.21, configurable).** Defaults (`graders/llm/judge-evidence-limits.ts`): 12 tool calls, 16,000 chars per result, 64,000 chars total. Override per grader:

```yaml
- type: prompt
  config:
    evidence:
      - trajectory
      - source: repo
        max_files: 1000          # default 1000;    range 1..100000
        max_file_bytes: 32000    # default 32000;   range 1..16 MiB
        max_total_bytes: 262144  # default 262144;  range 1..64 MiB
        include: ["src/**"]
        exclude: ["**/*.snap"]
    evidence_read_budget:
      max_tool_calls: 12         # range 1..500
      max_result_chars: 16000    # range 1000..200000
      max_total_chars: 64000     # range 1000..4000000
```

Field names and ranges: `graders/llm/types.ts:77-95`, `graders/llm/evidence.ts:81-90`; defaults `graders/llm/repo-snapshot.ts:55-57`. The YAML above is assembled from those types, not copied from a sample. Result metadata gains `evidence_usage: { toolCalls, chars, budgetExhausted }`.

**`output_delivery`:** any value other than `workspace` → grader error and lint **error** `invalid-grader-config`; `workspace` → deprecation warning, lint **warning** `deprecated-grader-config` (`validator.ts:578-585`).

**Model validation (0.20):** judge and executor call `assertCopilotModelSupported` before creating a session; an unavailable model fails with `Model "<m>" is not available in Copilot. Available models: …` (`packages/core/src/utils/copilot-models.ts:59-68`). Catalog lookup has a 10 s timeout. BYOK providers are exempt (changelog; not re-read in source).

### Auth: judge vs agent executor

**Agent executor (unchanged).** `new CopilotClient({ env, telemetry, onGetTraceContext })` with no token (`packages/core/src/executor/copilot-sdk-executor.ts:381-385`). Auth is left to the SDK. Vally now names the SDK's env precedence in code: `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN` "in SDK precedence order" (`packages/core/src/executor/copilot-sdk-auth.ts:6-11`); this list is used by the Docker backend to decide which host variables to forward.

**Judge (token line unchanged, keychain fixed).**

```ts
// packages/core/src/graders/llm/llm-client.ts:72-78
const sharedOptions = {
  env: { ...stripProviderEnv(process.env), NODE_NO_WARNINGS: "1" },
  gitHubToken: process.env.GITHUB_COPILOT_API_TOKEN || process.env.GITHUB_TOKEN,
};
```

So the explicit judge token order is still **`GITHUB_COPILOT_API_TOKEN`, then `GITHUB_TOKEN`**. `COPILOT_GITHUB_TOKEN` and `GH_TOKEN` are not read by Vally for the judge (they remain in the inherited `env`, so the SDK may still use them when `gitHubToken` is undefined; that fallback is SDK behaviour, **UNCONFIRMED** from Vally source).

The 0.19 keychain fix: the client used for file-backed judging changed from `mode: "empty"` (`old:…/llm-client.ts:376`) to `mode: "copilot-cli"` with the comment "Empty mode disables OS-keychain auth; isolate judge capabilities per session instead" (`llm-client.ts:114-120`). Since 0.17 every built-in judge call uses that client, so between 0.17 and 0.18 a keychain-only login could not judge; 0.19+ can. *Inferred from the two code states plus `CHANGELOG.md:75`.*

The old gotcha stands: a `GITHUB_TOKEN` in the shell without Copilot access is passed explicitly and will break judging.

---

## 5. `.vally.yaml`

Top-level keys (from `packages/core/src/config/vally-config.schema.json` `properties`, enforced by `config/loader.ts:67-73`): **`metadata, paths, environments, suites, plugins, defaults, params`**. Unknown top-level keys are an error.

```ts
// packages/core/src/config/types.ts
export interface SuiteConfig {
  description?: string;
  filter?: Record<string, string | string[]>;
  evals?: string[];
  metadata?: Record<string, ConfigMetadataValue>;   // new 0.17
}
export interface ProjectDefaultsConfig { backend?: BackendSelectionConfig; evalProvider?: string; }
export interface PluginConfig {
  grader?: string[]; executor?: string[]; reporter?: string[];
  evalProvider?: string[]; backend?: string[];
}
```

In YAML the keys are snake_case: `defaults.eval_provider`, `defaults.backend`, `plugins.grader|executor|reporter|eval_provider|backend` (`config/loader.ts:105-166`). Unknown keys under `defaults` or `plugins` are errors.

```yaml
# Assembled from the loader's accepted keys; not copied from a sample.
metadata: { team: skills }          # passive; exposed to reporters
paths: { skills: skills/, evals: evals/, results: vally-results/ }
plugins:
  grader: [./vally-plugins/my-grader]
  reporter: [./vally-plugins/my-reporter]
defaults:
  backend: docker                    # or { name: docker, args: {...} }
suites:
  ci:
    filter: { cost: [free, low] }
    metadata: { tier: inner-loop }
```

- **Plugin resolution.** Project plugins load first, relative to the project directory; CLI `--*-plugin` flags are additive and resolve from the first `--eval-spec`'s directory (`packages/cli/src/commands/eval.ts:1099-1125`). `plugins.backend` is skipped when `--backend` is given.
- **Backend precedence:** `--backend` > eval `defaults.backend` > `.vally.yaml` `defaults.backend` > `local` (`packages/cli/src/backend-selection.ts:26-33`). Args merge project → eval → CLI for the selected backend name.
- **Eval provider:** `plugins.eval_provider` only loads providers; one is used only if `defaults.eval_provider` names it. Otherwise a warning says they are unused (`eval.ts:1151-1166`). `--eval-plugin` replaces both.
- **`metadata`** (0.17): root-level and per-suite JSON-compatible values. Reporters get `ctx.metadata` (project defaults shallow-overridden by the selected suite) and `ctx.suite` (`packages/core/src/reporting/plan-reporter.ts`).
- **Named environments** (0.21 fix): resolve from each eval's own project config (`CHANGELOG.md:20`). I did not re-trace the code path; treat the mechanism as changelog-sourced.
- **`paths.results`**: parsed and stored (`config/loader.ts:192`) but **not read by any CLI or core code path** (repo-wide search of `packages/*/src`). See section 9.
- Defaults unchanged: `skills/`, `evals/`, `vally-results/`, eval filenames `eval.yaml`/`eval.yml`, walk-up of 10 levels (`config/defaults.ts`).

---

## 6. Results on disk

### Layout for `vally eval`

`<output-dir or ./vally-results>/<ISO timestamp with : and . replaced by ->/` (`eval.ts:473-505`) containing (`packages/cli/src/run-layout.ts:15-22`):

| Name | What |
|---|---|
| `results.jsonl` | data stream (below) |
| `eval-results.md` | markdown report, always written |
| `eval-results.junit.xml` | with `--junit` |
| `otel-spans/`, `otel-spans.jsonl` | local traces when no `--otlp-endpoint` |
| `diffs/` | sidecar workspace diffs referenced by `trajectory.diffPath` |
| `<eval-name>/<stimulus>/<model>/<trial>/` | session logs (layout from 0.8, not re-read) |

Reserved names an eval may not collide with also include `run-summary.jsonl` and `artifacts`.

For `vally experiment run`: `<output-dir>/<timestamp>/<variant>/results.jsonl` plus `<variant>/run-summary.jsonl` (`packages/cli/src/experiment-runner.ts:1022-1024,1513`).

### `results.jsonl` records

Two record types. **Trajectories are inline** in each `trial-result` line (`trajectory` field); there is no separate trajectory file.

```ts
// packages/core/src/reporting/jsonl-record.ts:27-64
export interface TrialResultRecord {
  type: "trial-result";
  runId?: string;                 // new 0.18
  itemId: string;
  evalName: string;
  evalFilePath: string;
  variant: string;                // always present; "main"-style default for plain eval
  stimulus: string;
  shardKey?: string;
  model?: string;                 // omitted for single-model runs
  trialIndex?: number;            // 0-based; omitted for single-run stimuli
  totalTrials?: number;
  status: TrialResult["status"];  // "success" | "error" | "skipped"
  durationMs: number;
  error?: string;
  skipReason?: string;
  workspacePath?: string;
  gradeResult: StimulusGradeResult | null;   // always present
  trajectory: Trajectory | null;             // always present
}
```

```ts
// packages/core/src/reporting/jsonl-record.ts:67-96
export interface RunSummaryRecord {
  type: "run-summary";
  runId: string;                  // new 0.18
  passed: boolean;
  hadExecutionErrors: boolean;
  hadGradingErrors?: boolean;     // new 0.20
  evals: Array<{
    name: string; evalFilePath: string; variant: string; model?: string;
    passed: boolean; hadExecutionErrors?: boolean; hadGradingErrors?: boolean;
    error?: string; overallScore?: number; threshold?: number;
    scoringApplied: boolean; stimuliRun: number; stimuliTotal: number;
    stimuliSkipped?: number; durationMs: number;
  }>;
  jsonlPath?; markdownPath?; junitPath?; sessionLogsDir?; otelTracesFile?;
}
```

`gradeResult` shape (`packages/core/src/pipeline/grading.ts:69-73` + `packages/core/src/graders/types.ts:68-108`): `name` (`"trajectory-grade"`), `status?` (`"success" | "error"`), `kind`, `passed`, `score`, `evidence` (`"N/M graders passed"`), `details[]` (one `GraderResult` per grader, each with `name`, `status?`, `graderType?`, `configuredName?`, `kind`, `passed`, `score`, `label?`, `evidence`, `details?`, `metadata?`), plus `stimulusName`, `trajectoryId`, `timestamp`.

Trajectory events gained `endTimestamp` (0.21) and `tool_result` events may carry `error: { message, code? }` with `result` optional (`packages/core/src/trajectory/types.ts`). `Trajectory` gained `diffError` and metadata `modelDisplayName`.

`vally oracle --no-golden-input` outcomes carry `oracleBaseline: { mode: "baseline", ok }`; consumers must prefer it over score/threshold (`packages/core/src/pipeline/types.ts:29-37`).

---

## 7. Plugin / extension API

### Registration (unchanged names)

`registerGraders`, `registerExecutors`, `registerReporters`, `registerExporters`, `registerBackends`, `registerEvalProviders` (literal `registerFnName` values across `packages/core/src` and `packages/cli/src`). Loading is atomic via a staging registry, with a conflict check against existing names (`packages/core/src/utils/plugin-loader.ts:127-200`).

**How a plugin is selected (new, stricter classification):** `packages/core/src/utils/plugin-selection.ts` header.

| Specifier form | Meaning |
|---|---|
| `./file.mjs`, `../f.cjs`, `/abs/f.js` | that file alone |
| `./dir`, `/abs/dir`, `file:///dir` | that exact directory (its `package.json` entry) |
| `pkg`, `@scope/pkg/subpath` | that npm package |

Classification is lexical, so `foo.js` is an npm package name, not a local file.

**TypeScript plugins.** Entry extensions accepted: `.js, .mjs, .cjs, .ts, .mts, .cts` (`plugin-selection.ts:39`). The loader calls plain `import()` on the resolved target (`plugin-loader.ts:148`) and core has no transpiler dependency. *Inferred:* `.ts` plugins rely on Node's built-in type stripping. **UNCONFIRMED:** which Node versions do this without a flag, and what TS syntax is tolerated.

**Where to register in 0.21:** `.vally.yaml` `plugins:` (project-wide, 0.19) and/or CLI `--grader-plugin`, `--executor-plugin`, `--reporter-plugin`, `--eval-plugin`, `--backend`. Not experiment files.

### Grader

```ts
// packages/core/src/graders/types.ts (GraderInput additions)
signal?: AbortSignal;      // aborted when scoring.timeout expires; graders MUST honor it
timeoutMs?: number;        // remaining total grading budget when this grader starts
judgeTimeoutMs?: number;   // per judge turn
```

What a 0.16 custom grader must change:

- **Nothing is strictly required** to keep loading; `status` is optional and absence means success.
- If it does async work, honor `input.signal`, otherwise it runs past `scoring.timeout`.
- **`withRolledUpGraderError()` is gone** from `@microsoft/vally/graders` (no occurrence in the 0.21 tree; I did not find it in the 0.16 source tree I was given either, so its removal is changelog-sourced, `CHANGELOG.md:30`). An aggregate grader must set its own top-level `status: "error"` for a blocking error. Use `hasGraderError(result)` to detect errors recursively (`graders/types.ts:111-115`).
- A `program` grader's `EVALUATE_GRADER_INPUT` JSON no longer includes `signal`, `timeoutMs` or `judgeTimeoutMs` (`graders/static/program-grader.ts`).
- Optional hooks unchanged: `defaultName(config)`, `assertsAbsence(config)`. The latter now also lets empty agent scopes through to grading.
- Example plugin `peerDependencies`: `"@microsoft/vally": "^0.21.0-0"` (`plugins/vally-grader-example/package.json`).

### Executor

- **`retryable: true`.** `isRetryableError` is now exactly `err.retryable === true` (`utils/error-classifier.ts:69-71`).
- **`ExecutorOptions.registerCleanup(cb)`** (0.18): callbacks run after grading and egress, in reverse order, before workspace disposal; 30 s per callback on the local host (`executor/types.ts`).
- **Tracing rename** (0.17): `ExecutorTelemetryConfig` → `TracingConfig`, `TelemetryConfigurableExecutor` → `TracingConfigurable`, `configureTelemetry()` → `configureTracing()`, `isTelemetryConfigurableExecutor` → `isTracingConfigurable`, `normalizeExecutorTelemetryConfig` → `normalizeTracingConfig`. A component that still has `configureTelemetry` causes: "configureTelemetry() has been replaced by TracingConfigurable.configureTracing()".
- New capability flag `supportsMcpSimulation` beside `supportsSimulation`.
- New export `createDefaultExecutorRegistry` (`packages/core/src/index.ts`).

### Backend

- `cleanup: (options?: { preserveWorkspace?: boolean }) => Promise<void>`; the host **always** calls it, including after failed egress, so a backend must honor `preserveWorkspace` (`packages/core/src/backend/types.ts`).
- `BackendConfig` is now `Record<string, ConfigMetadataValue>` (JSON-compatible), not `Record<string, string | string[]>`.
- `plugins.executor/grader` passed to backends are `{ specifier, cwd }` objects (`BackendPluginSource`), not bare strings with one shared `cwd`.
- Backend instances are per eval (per eval/variant in experiments), not per run.
- Backends may implement `TracingConfigurable`.
- `TrialLogs.supplementary` for extra log files.

### Reporter

`onRunStart` context gains `runId`, `selectedStimuli`, `metadata`, `suite`, `experiment` (`packages/core/src/reporting/plan-reporter.ts`). `RunSummary`/`EvalSummary` gain `hadGradingErrors`. New exports `serializeTrajectoryEvent` and `SerializedTrajectoryEvent` (wire alias `end_timestamp`). A reporter that maps `passed === false` to "fail" should now distinguish `grade.status === "error"` (use `hasGraderError` / `resolveGradePass`).

---

## 8. Install / runtime

- **Node:** `>=22.15.0` (all three packages).
- **Packages:** `@microsoft/vally` 0.21.0, `@microsoft/vally-cli` 0.21.0 (bin `vally`), `@microsoft/vally-server` 0.21.0. Core also ships a second bin, `vally-docker-runner`.
- **Copilot runtime dependency changed.** Core no longer pins `@github/copilot` 1.0.82 + `@github/copilot-sdk` 1.0.11. It depends on `@github/copilot-sdk` `^1.0.22` only (`packages/core/package.json`); the lockfile shows the SDK pulling platform packages such as `@github/copilot-sdk-darwin-arm64`. *Inferred:* the runtime is still installed with Vally, now through the SDK's platform packages. **UNCONFIRMED** hands-on.
- **`better-sqlite3`** is an optional peer of `@microsoft/vally-server` (`peerDependenciesMeta.optional: true`); `serve`/`ingest` fall back to `node:sqlite`. Server API: `openDatabase()` returns `{ dataSource, ingestDirectory, close }` (`CHANGELOG.md:83`; not re-read in source).
- **Docker backend** (`--backend docker`, 0.18): uses Docker Compose (`docker compose version` probe at `packages/core/src/backend/docker/docker-cli.ts:294`). Builds and caches a default image `vally-task:<content-hash>` locally from `Dockerfile.task` (Node 24 slim + git + the core package); an uncached build needs network. Args (`backend/docker/config.ts:35-42`): `task-image`, `grade-image` (defaults to `task-image`), `task-network`, `grade-network` (default `default`), `task-env`, `grade-env` (repeatable, env var **names**), `compose-file`, `resources` (object or JSON string, e.g. `resources='{"limits":{"cpus":2}}'`). `--in-place` is incompatible with it.
- **Experiment files.** Allowed top-level keys: `name, evals, overrides, execution, matrix, vary, baseline, variants`. Variant keys: `overrides, environment`. `execution` keys: `workers`. `overrides` keys: `runs, timeout, model, executor, backend, judge_model, judge_timeout, judge_provider, reasoning_effort, judge_reasoning_effort` (`experiment/loader.ts:28-39`, `experiment/constants.ts:12-33`). Sample models changed from `gpt-4o`/`gpt-4o-mini` to `gpt-5.5`/`gpt-5-mini` (`samples/params-with-experiment/upload.experiment.yaml`).
- **Simulation.** `copilot-sdk` sets `supportsSimulation = true` and `supportsMcpSimulation = true` (`copilot-sdk-executor.ts:186-187`). `vally simulate record <input>` emits a `simulation.tool_overrides` YAML block from a recorded run (core export `generateSimulationYaml`).
- **Copilot executor.**
  - **`/skill-name` dispatch** (0.21): a turn matching `^\s*/(\S+)…` is looked up (case-insensitive, name or alias) among runtime commands of `kind: "skill"`; if found, it is invoked natively and the returned agent prompt is sent. If no skill matches, the prompt is sent unchanged (`copilot-sdk-executor.ts:1503-1541`). **UNCONFIRMED:** whether a natively dispatched skill emits a `skill_activation` event.
  - **`model: auto` routing** (0.20): `defaults.executor.config.autoTier` requires `model: auto`; `hydrafusion` / `hydrafusion-max` also set feature flags (`copilot-sdk-executor.ts:521-524,635-644`).
  - **Model and reasoning-effort validation** before session creation (`copilot-sdk-executor.ts:780`); error text lists available models or supported efforts (`utils/copilot-reasoning-effort.ts`).
  - MCP sampling requests are handled through the runtime (`executor/copilot-sampling.ts`).
  - Session options otherwise as before: `approveAll`, isolated `COPILOT_HOME`, `EVALUATE_USE_HOST_COPILOT_HOME` opt-out.
- **Samples:** same five; new `samples/README.md` with a run table.
- **`vally init`:** same flags (`[dir]`, `--force`); template uses `agent_environment:` and `# model: gpt-5.5`.

---

## 9. NOTES.md unverified facts

| Fact | Status | Answer |
|---|---|---|
| Copilot tool names (`create` vs `write_file`) | **PARTLY VERIFIED** | Vally's own list of Copilot built-ins is `read, search, edit, create, task, skill, web_search, web_fetch, ask_user, bash, powershell, grep, glob, view, sql, report_intent, store_memory, fetch_copilot_cli_documentation` (`packages/core/src/skill/external-dep-checker.ts:41-60`); the `tool-calls` grader docs say "tools like 'create'/'edit'/'view'" (`graders/static/tool-call-grader.ts:27`). There is no `write_file`. What a given runtime version actually emits is still runtime behaviour, so keep the "read `toolCallBreakdown`" step. |
| `results.jsonl` record shape | **VERIFIED** | Two record types, `trial-result` and `run-summary`; see section 6 (`packages/core/src/reporting/jsonl-record.ts`). Grader results are at `.gradeResult.details[]`; trajectory is inline at `.trajectory`. |
| Does `vally grade -e <spec>` use that spec's `rubric`? | **VERIFIED: yes** | `grade` looks up the stimulus by `trajectory.stimulus.name` in the spec, and passes that spec stimulus plus its `graders` to grading (`packages/cli/src/commands/grade.ts:1438-1500`); the judge takes the rubric from `input.stimulus.rubric` (`graders/llm/judge-helpers.ts:8-14`). A stimulus name missing from the spec is an error: `No stimulus named "…" found in eval spec`. So a second spec with the same stimulus names and a different rubric/graders works. |
| `vally grade --workspace` only for ATIF/session input | **NOW FALSE** | 0.21 help: "overrides every input trajectory"; code: "Explicit overrides applied to every input kind: --workspace replaces the graded workDir" (`grade.ts:692,1009-1016,1142`). In 0.16 it was "ATIF or session run input only" (`old:…/grade.ts:625`). `vally eval --workspace <dir>` still preserves workspaces under `<dir>/<variant>/<stimulus>`. |
| `paths.results` vs `--output-dir` | **VERIFIED** | `paths.results` is never consulted. Output goes to `--output-dir` if given, else `./vally-results` relative to the **current directory**, then a timestamped subfolder (`eval.ts:473-475,505`; `paths.results` is only assigned in `config/loader.ts:192`). |
| Does `agent_environment.skills` copy the skill's `evals/` dir? | **VERIFIED: yes** | Each skill directory is copied whole with `cp(src, dest, { recursive: true, … })` and no filter, to `<workDir>/<basename>` (`packages/core/src/pipeline/run.ts:1596-1629,2487-2499`). Graders, fixtures and rubrics under `skills/<name>/evals/` are visible to the agent. Keep answer keys in `grading_environment` or outside the skill directory. |
| Experiment `/environment/skills` relative path resolution | **VERIFIED** | Variant `environment.skills` (also `files[].src`, `git.source`, stdio `mcpServers.cwd`, Docker `compose-file`) resolve relative to the **experiment file's directory** (`packages/core/src/experiment/interpolate.ts:67-113`). |
| `GITHUB_COPILOT_API_TOKEN` for judges in CI | **VERIFIED (code path)** | Judge passes `GITHUB_COPILOT_API_TOKEN || GITHUB_TOKEN` (`llm-client.ts:77`). The repo's own workflow sets `GITHUB_TOKEN: ${{ github.token }}` on the eval step (`.github/workflows/evaluate.yml:159`). Whether a particular token has Copilot access is not a source question. |
| `StimulusGradeResult` field names | **VERIFIED** | `GraderResult` fields plus `stimulusName`, `trajectoryId`, `timestamp` (`pipeline/grading.ts:69-73`). Unchanged since 0.16. |
| MockExecutor fixture `assistant_message` `data.content` | **VERIFIED** | Fixture is `{ "output": string, "events"?: TrajectoryEvent[] }` at `<workDir>/.mock-executor/<stimulus.name>.json` (`executor/mock-executor.ts:16-19,200-202`). `assistant_message` is `{ type: "assistant_message", data: { content: string } }` (`trajectory/types.ts:269-274`). An event only needs a string `type` and an object `data` to be kept. Timestamps may be ISO strings (`timestamp`, `endTimestamp`). |
| Oracle rejects output/behaviour graders without `golden_trajectory` | **VERIFIED, with a 0.20 exception** | In golden mode without a `golden_trajectory`, oracle throws for output-scoped types (`output-*`) and trajectory-scoped types (`completed`, `exit-success`, `tool-calls`, `skill-invocation`, `system-event`, `max-repeat`, `loop-outcome`, the six metric graders, `transcript-*`, `assistant-contains-tool-output`), and for any `turn`-scoped grader (`pipeline/oracle.ts:487-700`). **Under `--no-golden-input` they are no longer rejected**: they run against the empty baseline and are classified `expected-fail` / `n/a` / `unexpected-pass` / `error`. |

---

## 10. Old-digest statements now false

| Old claim (digest section) | 0.21 truth | Source |
|---|---|---|
| "Scoring is about to be removed" (headline 1, §1 "Upcoming", §9.6) | `scoring.weights`, `scoring.threshold`, `--threshold` and all six scoring lint rules are still present; `scoring.timeout` was added | `packages/core/src/eval/types.ts:541`; `packages/cli/src/commands/eval.ts:247`; `packages/core/src/eval/validator.ts:757-2160` |
| Default judge model is `claude-sonnet-4.6` (headline 6, §5, §9.10) | `gpt-5.6-terra` | `packages/core/src/graders/llm/prompt-grader.ts:67` |
| `plugins/executors/vally-executor-claude-cli` exists, `private: true`; build from source (headline 2, §2d, §6) | Directory removed from the repo, along with `vally-executor-cca` and `providers/vally-eval-provider-ger`. The only remaining `claude-cli` mentions are in `CHANGELOG.md` and one comment in `run.ts` | `plugins/` listing |
| Core pins `@github/copilot` 1.0.82 and `@github/copilot-sdk` 1.0.11 (§2a) | `@github/copilot-sdk` `^1.0.22`; no direct `@github/copilot` dependency | `packages/core/package.json` |
| Judge user message contains Agent Output / Execution Metrics / Session Timeline, with 50,000-char and first-50/last-50 limits (§5) | User message is Task / Evaluation Instructions / Rubric only; evidence is in files, complete, read under a tool budget | `graders/llm/judge-helpers.ts:16-42`; `graders/llm/judge-workspace.ts` |
| `output_delivery: workspace` is an opt-in mode with fixed 12 / 16,000 / 64,000 limits (§5) | File delivery is the only mode; `inline` rejected; `workspace` deprecated; limits configurable via `evidence_read_budget` | `graders/llm/judge-evidence.ts:17-34`; `graders/llm/evidence.ts:87-90` |
| "source of `DEFAULT_THRESHOLDS` … wasn't read" (§5) | All scales default to 0.5 on the normalized scale; normalization is `(raw-min)/(max-min)` | `graders/llm/types.ts:254-272` |
| Judge workspace client detail: `baseDirectory` host COPILOT_HOME (§2b), implying keychain works | True again from 0.19 (`mode: "copilot-cli"`); it was `mode: "empty"` in 0.16 | `graders/llm/llm-client.ts:114-120` |
| `vally grade --workspace` is for ATIF/session input (NOTES; digest §1 context) | Overrides every input trajectory | `packages/cli/src/commands/grade.ts:692` |
| Node `>=22.12.0` (§1 table, §8) | `>=22.15.0` | `package.json` `engines` |
| CLI commands: init, lint, eval, grade, oracle, compare, experiment, export, serve, ingest (§6) | Adds `simulate` (`simulate record`) | `packages/cli/src/commands/simulate.ts` |
| Plugins declare `peerDependencies` `^0.16.0-0`; harbor `0.1.0-alpha.5` (§6) | `^0.21.0-0`; harbor `0.1.0-alpha.9` | `plugins/*/package.json` |
| `--executor-plugin <path>/plugins/executors/vally-executor-claude-cli` install recipe (§2d) | No such path in 0.21. Whether the package is published elsewhere is **UNCONFIRMED** (no network) | `plugins/` listing |
| "`vally experiment run` never discovers" plugins / experiment `filter`, `grader_plugins` etc. are parsed (implicit in §3 experiment notes) | Those fields are rejected; plugins come from `.vally.yaml` or `experiment run --grader-plugin/--executor-plugin/--reporter-plugin/--eval-plugin` | `packages/core/src/experiment/loader.ts:28-39`; `packages/cli/src/commands/experiment.ts:188-215` |
| Starter template scaffolds a commented `environment:` block (§9.13) | Scaffolds `agent_environment:` | `packages/cli/src/templates/starter-eval.ts` |
| Experiment sample uses `gpt-4o` / `gpt-4o-mini` with `baseline: gpt-4o` (§3) | `gpt-5.5` / `gpt-5-mini`, `baseline: gpt-5.5` | `samples/params-with-experiment/upload.experiment.yaml` |
| Plugin test script `tsc -b tests/tsconfig.json && vitest run --project=<name>` (§8) | `… vitest run --config ../../vitest.config.ts --project=<name>` | `AGENTS.md` |
| "Docs sync rule: changing eval.yaml schema means updating eval-spec.mdx in the same PR" (§8) | Replaced by "A changed source file alone is not a reason to edit documentation" | `AGENTS.md` |
| Reasoning effort enum `low, medium, high, xhigh` (implicit) | Any non-empty string, validated against the model's supported levels | `graders/llm/types.ts:24-32`; `eval/validator-schemas.ts` |
| A failing grader and a broken grader both just show as failed (0.15-era nuance in §1) | Distinct `ERROR` state; grading errors force exit 1 | `reporting/internal/result-card.ts:44-53`; `packages/cli/src/exit-policy.ts` |

### Still true (checked, worth not re-litigating)

- `agent_environment` preferred; `environment` deprecated alias; setting both is an error. The repo's own `tests/evals/eval-authoring/eval.yaml:21` still uses `environment:`.
- Skills are copied to `<workDir>/<basename>/`; `environment.skills` replaces `--skill-dir`.
- The four removed constraint aliases and their `unsupported-constraint` message.
- Program grader env vars `EVALUATE_WORKSPACE`, `EVALUATE_GRADER_INPUT`.
- `skill_activation` comes from the runtime's `skill.invoked` event (`trajectory/copilot-adapter.ts:447-449`).
- pass@k uses the unbiased estimator; pass^k = p^k (`scoring/scorer.ts:70-99`).
- `tests/.vally.yaml` and the `/evaluate` workflow models (`claude-opus-4.6` for agent and judge).
