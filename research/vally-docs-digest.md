# Vally Documentation Digest

Crawled 2026-09-10 from https://microsoft.github.io/vally/ (Astro Starlight site). Every page in the site's Pagefind search index was fetched as raw HTML and read in full: **57 pages** (35 in the sidebar plus 22 per-grader pages linked only from the grader catalog). Package facts marked **[npm]** come from `npm view` against the registry, not from the docs.

Citation format: `[ID]` refers to the sitemap table in section (a). All URLs share the prefix `https://microsoft.github.io/vally`.

---

## Surprises and headline findings (read first)

1. **Packages moved and the version jumped.** Ted's local guide (`~/src/me/skills/Vally.md`) covers **v0.3.0**, installed from **GitHub Packages** with a `read:packages` PAT, on Node >= 20. The live docs say `npm install -g @microsoft/vally-cli` with no registry or auth setup, and require **Node.js >= 22.12.0** [gs][install]. `npm view` shows `@microsoft/vally-cli@0.16.0` (latest), `next` tag `0.15.0-next.2`, `engines.node >=22.12.0`, MIT license, first published 2026-07-09 **[npm]**. Every version from 0.3.0 to 0.16.0 is on the registry. Ted's npm resolves through `packagefeedproxy.microsoft.io` (feed `npm-public`).
2. **Third package.** `@microsoft/vally-server@0.16.0` provides the analytics server, REST API and dashboards [install]. The CLI depends on it, plus OpenTelemetry and the Azure Monitor exporter **[npm]**.
3. **The GitHub repo is not publicly reachable.** The docs link `https://github.com/microsoft/vally/tree/main/samples/multi-turn-memory` [g-spec][spec][compare], but `github.com/microsoft/vally` returns **404** anonymously and to the active gh account. The source and `samples/` can't be checked from outside. (A gh check with the second account was blocked by the permission system and not retried.)
4. **The eval.yaml schema changed a lot since 0.3.** Execution config moved from `config:` to `defaults:`. `environment` became `agent_environment`, with `environment` kept as a deprecated alias. `timeout` is now a duration string with a unit suffix (`2m`). Behavioral constraint aliases were removed (lint code `unsupported-constraint`), and presets are no longer documented. See section (l) for how this affects Ted's 20 existing evals.
5. **Auth is required to run evals, not to install.** The default `copilot-sdk` executor reads `COPILOT_GITHUB_TOKEN`, which must be a **fine-grained PAT with Account > Copilot Requests**. `secrets.GITHUB_TOKEN` will not work [ci]. Alternatives: bring your own key (BYOK) via `defaults.executor.config.provider` [spec], or `claude-cli` with `ANTHROPIC_API_KEY` [ci].
6. **Telemetry is on by default.** Opt out with `VALLY_TELEMETRY_OPTOUT=1` or `DO_NOT_TRACK=1` [telemetry].
7. **The site has no FAQ, changelog or best-practices page.** Guidance is spread across concept and guide pages (section j).

---

## (a) Sitemap: every page

| ID | Title | URL |
|---|---|---|
| home | Vally (landing) | https://microsoft.github.io/vally/ |
| gs | Get Started | https://microsoft.github.io/vally/get-started/ |
| install | Installation | https://microsoft.github.io/vally/get-started/install/ |
| first | Run Your First Eval | https://microsoft.github.io/vally/get-started/run-your-first-eval/ |
| ci | Add to CI | https://microsoft.github.io/vally/get-started/add-to-ci/ |
| why | Why Vally | https://microsoft.github.io/vally/concepts/why-vally/ |
| how | How It Works | https://microsoft.github.io/vally/concepts/how-it-works/ |
| tax | Grader Taxonomy | https://microsoft.github.io/vally/concepts/grader-taxonomy/ |
| scoring | Scoring | https://microsoft.github.io/vally/concepts/scoring/ |
| suites | Authoring Eval Suites | https://microsoft.github.io/vally/guides/authoring-eval-suites/ |
| debug | Debugging Evals | https://microsoft.github.io/vally/guides/debugging-evals/ |
| g-exec | Writing Custom Executors | https://microsoft.github.io/vally/guides/writing-custom-executors/ |
| g-grader | Writing Custom Graders | https://microsoft.github.io/vally/guides/writing-custom-graders/ |
| g-rep | Writing Custom Reporters | https://microsoft.github.io/vally/guides/writing-custom-reporters/ |
| g-spec | Writing Eval Specs | https://microsoft.github.io/vally/guides/writing-eval-specs/ |
| ref | Reference (index) | https://microsoft.github.io/vally/reference/ |
| cli | CLI Commands (index) | https://microsoft.github.io/vally/reference/cli/ |
| compare | CLI: compare | https://microsoft.github.io/vally/reference/cli/compare/ |
| eval | CLI: eval | https://microsoft.github.io/vally/reference/cli/eval/ |
| experiment | CLI: experiment | https://microsoft.github.io/vally/reference/cli/experiment/ |
| export | CLI: export | https://microsoft.github.io/vally/reference/cli/export/ |
| grade | CLI: grade | https://microsoft.github.io/vally/reference/cli/grade/ |
| ingest | CLI: ingest | https://microsoft.github.io/vally/reference/cli/ingest/ |
| init | CLI: init | https://microsoft.github.io/vally/reference/cli/init/ |
| lint | CLI: lint | https://microsoft.github.io/vally/reference/cli/lint/ |
| oracle | CLI: oracle | https://microsoft.github.io/vally/reference/cli/oracle/ |
| serve | CLI: serve | https://microsoft.github.io/vally/reference/cli/serve/ |
| spec | Eval Spec Reference (eval.yaml) | https://microsoft.github.io/vally/reference/eval-spec/ |
| expfile | Experiment File Schema | https://microsoft.github.io/vally/reference/experiment-file/ |
| graders | Grader Catalog | https://microsoft.github.io/vally/reference/graders/ |
| results-api | Results API | https://microsoft.github.io/vally/reference/results-api/ |
| scorefn | Scoring Functions | https://microsoft.github.io/vally/reference/scoring-functions/ |
| telemetry | Telemetry | https://microsoft.github.io/vally/reference/telemetry/ |
| traj | Trajectory Format | https://microsoft.github.io/vally/reference/trajectory-format/ |
| vyaml | .vally.yaml Configuration | https://microsoft.github.io/vally/reference/vally-yaml/ |
| gr:actc | Grader: assistant-contains-tool-output | https://microsoft.github.io/vally/reference/graders/assistant-contains-tool-output/ |
| gr:completed | Grader: completed / exit-success | https://microsoft.github.io/vally/reference/graders/completed/ |
| gr:custom-metrics | Graders: custom-metrics | https://microsoft.github.io/vally/reference/graders/custom-metrics/ |
| gr:diff-contains | Grader: diff-contains (+ diff-not-contains) | https://microsoft.github.io/vally/reference/graders/diff-contains/ |
| gr:diff-empty | Grader: diff-empty | https://microsoft.github.io/vally/reference/graders/diff-empty/ |
| gr:metric | Graders: metric thresholds (token-budget, tool-call-count, turn-count, step-count, error-count, wall-time) | https://microsoft.github.io/vally/reference/graders/metric-thresholds/ |
| gr:file-contains | Grader: file-contains (+ file-not-contains) | https://microsoft.github.io/vally/reference/graders/file-contains/ |
| gr:file-exists | Grader: file-exists (+ file-not-exists) | https://microsoft.github.io/vally/reference/graders/file-exists/ |
| gr:file-matches | Grader: file-matches (+ file-not-matches) | https://microsoft.github.io/vally/reference/graders/file-matches/ |
| gr:loop-outcome | Grader: loop-outcome | https://microsoft.github.io/vally/reference/graders/loop-outcome/ |
| gr:max-repeat | Grader: max-repeat | https://microsoft.github.io/vally/reference/graders/max-repeat/ |
| gr:output-contains | Grader: output-contains (+ output-not-contains) | https://microsoft.github.io/vally/reference/graders/output-contains/ |
| gr:output-matches | Grader: output-matches (+ output-not-matches) | https://microsoft.github.io/vally/reference/graders/output-matches/ |
| gr:panel | Grader: panel (LLM panel of judges) | https://microsoft.github.io/vally/reference/graders/panel/ |
| gr:program | Grader: program | https://microsoft.github.io/vally/reference/graders/program/ |
| gr:prompt | Grader: prompt (LLM judge) | https://microsoft.github.io/vally/reference/graders/prompt/ |
| gr:run-command | Grader: run-command | https://microsoft.github.io/vally/reference/graders/run-command/ |
| gr:skill-invocation | Grader: skill-invocation | https://microsoft.github.io/vally/reference/graders/skill-invocation/ |
| gr:system-event | Grader: system-event | https://microsoft.github.io/vally/reference/graders/system-event/ |
| gr:tool-calls | Grader: tool-calls | https://microsoft.github.io/vally/reference/graders/tool-calls/ |
| gr:transcript-contains | Grader: transcript-contains (+ not) | https://microsoft.github.io/vally/reference/graders/transcript-contains/ |
| gr:transcript-matches | Grader: transcript-matches (+ not) | https://microsoft.github.io/vally/reference/graders/transcript-matches/ |

Sidebar groups, in order: Get Started (overview, install, run-your-first-eval, add-to-ci). Concepts (why-vally, how-it-works, grader-taxonomy, scoring). Guides (authoring-eval-suites, debugging-evals, writing-custom-executors, writing-custom-graders, writing-custom-reporters, writing-eval-specs). Reference (cli/*, eval-spec, experiment-file, graders, results-api, scoring-functions, telemetry, trajectory-format, vally-yaml).

**Pages that do not exist** (checked: absent from the sitemap-less site's Pagefind index): FAQ, changelog, best practices, presets, environments/isolation concept page, executors reference, reporters reference, dashboard page, `vally new` command, exporter-authoring guide, backend-authoring guide, eval-provider plugin guide. `sitemap.xml` returns 404.

---

## (b) Install and prerequisites

### Commands (verbatim)
```bash
npm install -g @microsoft/vally-cli
vally --version
```
[install]. For library use:
```bash
npm install @microsoft/vally
```
```typescript
import type { Grader, GraderInput, GraderResult } from "@microsoft/vally/graders";
import { createGraderRegistry } from "@microsoft/vally";
```
[install]. "The CLI is a thin wrapper around the core library. Anything the CLI can do, you can do programmatically with more control." [install]

### Packages [install]
| Package | Description (from docs) |
|---|---|
| `@microsoft/vally` | Core library: discovery, parsing, grading, scoring, reporting |
| `@microsoft/vally-cli` | CLI: `lint`, `eval`, `grade`, and more |
| `@microsoft/vally-server` | Analytics server: REST API, dashboards, agent integration |

Other packages referenced:
- `@microsoft/vally-executor-claude-cli`, linked from [ci] (npmjs.com link) and used in an [eval] example as `--executor-plugin @microsoft/vally-executor-claude-cli`. **[npm]** It returned 404 through Ted's Microsoft npm feed proxy, so it may not be mirrored there.

**[npm] details:** `@microsoft/vally-cli` bin is `vally` → `dist/index.js`, latest 0.16.0. Core `@microsoft/vally` subpath exports: `.`, `./backend`, `./config`, `./converters`, `./workspace`, `./executor`, `./executor/mock`, `./otel-endpoint`, `./graders`, `./scoring`, `./params`, `./trajectory`, `./utils`.

### Prerequisites
- **Node.js >= 22.12.0** [gs]. CI examples use `node-version: "22"` [ci].
- **Registry/auth to install:** none mentioned. The public npm registry is implied [install].
- **To run evals:** "This guide requires a working Copilot SDK setup." [first]. Local auth setup is not described anywhere (gap).
- **CI credentials** [ci]:

| Executor | Credential | Env var |
|---|---|---|
| `copilot-sdk` (default) | Fine-grained PAT with **Copilot Requests** | `COPILOT_GITHUB_TOKEN` |
| `claude-cli` | Anthropic API key | `ANTHROPIC_API_KEY` |

  To create the PAT: github.com/settings/tokens → Fine-grained tokens → Generate new token. Under Account permissions, set **Copilot Requests** to **Read and write** [ci].
- **`git` on PATH** is required for diff graders [gr:diff-contains].
- **Telemetry** is on by default. A one-time notice goes to stderr, and a marker file is written at `~/.vally/usage-telemetry-notice` [telemetry].

---

## (c) Core concepts and vocabulary (official terms)

### The pipeline
`Stimulus → Executor → Trajectory → Graders → Score` [how][home]

- **Stimulus**: "a prompt — what you ask the agent to do — plus configuration for how to grade the result." It holds `prompt` (or `turns`), `graders`, optional `constraints`, and an optional environment. "Think of stimuli as your **test cases**." [how]
- **Executor**: "takes a stimulus and runs an agent, producing a trajectory." It sets up the workspace, loads skills, sends the prompt, captures all events, and respects timeouts and constraints. The built-in executor uses the **Copilot SDK** [how]. The built-in names are `copilot-sdk` and `mock` [g-exec]. `claude-cli` and `cca` are named as process-spawning executors [spec].
- **Trajectory**: "the behavioral record of a single run — a flat array of typed events, computed metrics, and the final agent output." [how]
- **Grader**: "evaluates some aspect of an eval and produces a result." It returns `name`, `kind`, `passed`, `score` (0–1), `evidence`, and optional `details` [how].
- **Score**: grader results aggregated using weights and a threshold. With multiple trials Vally also reports pass@k, pass^k and flakiness [how][scoring].
- **Eval spec**: `eval.yaml` / `eval.yml`, which "defines what to test and how to grade it" [g-spec].
- **Eval discovery**: scans `paths.evals` (default `evals/`) for `paths.evalFilenames` (default `eval.yaml`, `eval.yml`) [how][vyaml].
- **Suite**: "a named group of evals defined in `.vally.yaml`", selected by tag `filter` and/or file `evals` globs [suites].
- **Tags**: `Record<string, string | string[]>`. Eval-level tags are inherited; stimulus-level tags override on the same key [spec][suites].
- **Trial**: one run of a stimulus. `runs` = trials per stimulus [scoring].
- **Verdict levels**: Trial, Stimulus, Eval [scoring].
- **GraderResult**: pass/fail + score + evidence ("Test result" in the migration table) [why].
- **Taxonomy metadata**: determinism, cost profile, reference requirement, temporal scope, score kind [tax].
- **Behavior** (`metadata.behavior`): `requiresLlmClient`, `requiresWorkspace` [tax].
- **Rubric**: a stimulus-level list of criteria strings that the LLM judges (`prompt`, `panel`) score [spec][gr:prompt].
- **Judge / judge model**: the LLM used by `prompt`/`panel`. Default `claude-sonnet-4.6` [gr:prompt].
- **Golden patch / golden trajectory / golden custom metrics**: reference solutions used by `vally oracle` [oracle][spec].
- **Negative control / baseline**: `oracle --no-golden-input` [oracle].
- **Absence assertion**: a grader config that correctly passes on empty input (reported N/A in oracle) [g-grader][oracle].
- **Experiment / variant / matrix / vary / baseline**: controlled A/B comparison across variants [expfile][experiment].
- **Baseline vs treatment**: the two sides in `vally compare` [compare].
- **Agent environment vs grading environment**: `agent_environment` is what the agent sees. `grading_environment` holds grader-only files hidden from the agent [spec].
- **Assets directory**: `dest_root: assets`, a per-trial directory outside the graded workspace, exposed as `EVALUATE_ASSETS` [spec].
- **Artifacts**: stimulus `artifacts.include/exclude` copies files out of the workspace into results [spec].
- **Simulation**: canned tool responses (`simulation.tool_overrides`) [spec].
- **Backend**: controls where trials run (`--backend local` or a plugin). Remote workspaces are "a Backend concern, not an executor one" [eval][g-exec].
- **Plugin seams**: "executors, graders, eval providers, and lint reporters", plus reporters, which make five [g-rep]. Exporters are loaded via `vally export --exporter` [export].
- **ATIF**: Agent Trajectory Interchange Format, accepted by `grade` and used for golden trajectories [grade][spec].
- **Hermeticity**: runs use a fresh empty `COPILOT_HOME` [debug].
- **Loops**: inner loop / CI loop / outer loop (nightly) [why][tax].

### Mapping from other eval systems [why]
| Your concept | Vally equivalent |
|---|---|
| Test case / example | **Stimulus** — a prompt + grader config |
| Assertion / check | **Grader** — implements the `Grader` interface |
| Test run / execution | **Trajectory** — captured event log |
| Test result | **GraderResult** — pass/fail + score + evidence |
| Test suite | **eval.yaml** — collection of stimuli |
| CI check | `vally lint` or `eval` command |

### Why Vally [why]
"Everything is a Grader" (one interface). A taxonomy picks the right checks for each loop. The trajectory is first-class data, so graders inspect behavior, not just output. The tool is "Designed for the full development loop": `Write code → Lint locally → Run evals → Gate in CI → Track regressions`. When not to use it: "Running generic LLM benchmarks (MMLU, HumanEval, etc.) — Other frameworks may be simpler."

### Loop guidance [why][tax][scoring]
| Context | What runs | `runs` |
|---|---|---|
| Local development / inner loop | Static graders only; "just run `vally lint`" [tax] | `1` |
| CI / PR gate | Static + complex-static graders | `3` |
| Nightly / outer loop | Everything including LLM judges and A/B | `5–10` |

**Important:** "Taxonomy is descriptive metadata. When you write an `eval.yaml`, you explicitly list the graders you want to run" [tax]. The live docs describe **no automatic grader selection or presets** (see k).

### Trajectory events [how][traj]
`tool_call`, `tool_result`, `token_usage`, `turn_start`/`turn_end`, `assistant_message`, `user_message`, `skill_activation`, `reasoning`, `custom`, `system` (typed, e.g. compaction), `cost_unavailable`, `error`.

### Trajectory metrics [traj]
```typescript
interface TrajectoryMetrics {
  tokenUsage: {
    inputTokens: number;
    outputTokens: number;
    totalTokens: number;
    cacheReadTokens: number;
    cacheWriteTokens: number;
    callCount: number;
    cost?: ProviderCost;
    byModel: Record<
      string,
      {
        inputTokens: number;
        outputTokens: number;
        callCount: number;
      }
    >;
  };
  toolCallCount: number;
  toolCallBreakdown: Record<string, number>; // { "write_file": 3, "read_file": 1 }
  simulatedToolCallCount: number; // tool calls that were simulated, not run for real
  skillActivationCount: number;
  skillActivationBreakdown: Record<string, number>; // { "test-writer": 1 }
  turnCount: number;
  wallTimeMs: number;
  errorCount: number;
}

type ProviderCost = {
  provider: "github-copilot";
  unit: "nano-aiu";
  amount: number;
};
```
`turnCount` = count of `turn_end`. `wallTimeMs` = time from the first to the last event [how].

### Trajectory top level [traj]
```typescript
interface Trajectory {
  id: string; // Unique run identifier
  stimulus: Stimulus; // The prompt + config that produced this
  events: TrajectoryEvent[]; // Flat array of typed events
  metrics: TrajectoryMetrics; // Computed aggregates
  output: string; // Final agent output text
  workDir: string; // Workspace path during run
  artifactDir?: string;
  artifactDirStrict?: boolean;
  assetsDir?: string;
  diff?: string; // Cumulative workspace diff
  diffPath?: string; // Cumulative diff sidecar path
  turnDiffs?: Array<
    { turn: number } & ({ diff: string } | { diffPath: string } | { error: string })
  >;
  workspacePatchSource?: "fast-path" | "snapshot" | "reused-diff";
  workspacePatchCaptureError?: string;
  metadata: TrajectoryMetadata; // Execution context
  raw?: unknown; // In-process only — stripped from JSONL output, never persisted.
}
interface TrajectoryMetadata {
  model: string;
  skillsLoaded: string[];
  startedAt: Date;
  completedAt: Date;
  executor: string;
  sessionID: string;
}
```
- `workspace.patch` is written per trial to `<session-dir>/workspace.patch` (64 MiB cap) [traj].
- `endReason` values mentioned: `"completed"`, `"agent_timeout"` [spec], and `simulation_cap` [spec][gr:loop-outcome].

Sample event JSON [traj]:
```json
{
  "type": "tool_call",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "data": {
    "toolName": "write_file",
    "toolCallId": "call_abc123",
    "turnId": "0",
    "arguments": { "path": "add.test.js", "content": "..." }
  }
}
```

### Skills loading (behavioral change) [eval]
"A run is skill-free by default." Skills load only through `environment.skills` (recommended; paths relative to the eval file) or `--skill-dir <path>`. The two don't stack: `environment.skills` replaces the `--skill-dir` set. "Earlier versions auto-discovered skills from the working directory. They no longer do… pass `--skill-dir .` explicitly." Under `copilot-sdk`, skills already in the workspace also load, so `environment.skills` "is a floor rather than the exact set."

---

## (d) Config file schemas, with YAML copied from the docs

### eval.yaml top-level fields [spec]
| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | Human-readable name |
| `description` | string | No | What this eval tests |
| `version` | string | No | Version for tracking |
| `type` | `"capability"` / `"regression"` | No | Eval intent |
| `agent_environment` | EnvironmentConfig | No | Root agent environment, merged into all stimuli. Deprecated alias: `environment` |
| `grading_environment` | GradingEnvironmentConfig | No | Root grader-only files, hidden from the agent |
| `defaults` | EvalDefaults | No | Execution configuration |
| `stimuli` | Stimulus[] | **Yes** | At least one required |
| `scoring` | ScoringConfig | No | Score aggregation |

Eval-level `tags` are also accepted [spec §Tags][suites].

### defaults [spec]
```yaml
defaults:
  runs: 3 # Trials per stimulus (default: 1)
  timeout: 2m # Per trial (e.g. 5m, 300s, 30000ms); unit suffix required (default: 2m)
  model: gpt-5.5 # Model for agent execution
  reasoning_effort: high # Reasoning effort for the agent under test
  judge_model: gpt-5.5 # Default model for LLM graders
  judge_reasoning_effort: high # Reasoning effort for the judge model
  executor: copilot-sdk # or custom executor via --executor-plugin
```
Also accepted: `judge_provider` (BYOK for judges). `executor` can be a string or `{ name, config }`. `runs` must be a positive integer; `0` is rejected [scoring]. An empty-string executor is rejected [spec].

### Executor BYOK [spec]
```yaml
defaults:
  model: gpt-5.2-codex
  executor:
    name: copilot-sdk
    config:
      provider:
        type: azure # "openai" | "azure" | "anthropic" (default: "openai")
        baseUrl: https://your-resource.openai.azure.com/openai/v1/
        wireApi: responses # "completions" | "responses" (default: "completions")
        apiKeyEnv: FOUNDRY_API_KEY # name of the env var holding the key
        azure:
          apiVersion: "2024-10-21"
```
Provider fields: `baseUrl` (required, absolute http/https), `type`, `wireApi`, `transport` (`http`/`websockets`), `apiKeyEnv`, `bearerTokenEnv` (wins over `apiKeyEnv`), `azure.apiVersion`, `headers`, `maxPromptTokens`, `maxOutputTokens`, `modelId`, `wireModel`. The name sent to the provider resolves as `wireModel → modelId → defaults.model`. Unknown keys are rejected. Literal keys are never accepted. Env vars are read from the **vally process**, not from `environment.env` [spec].

Ollama example [spec]:
```yaml
defaults:
  model: qwen3
  executor:
    name: copilot-sdk
    config:
      provider:
        baseUrl: http://localhost:11434/v1 # e.g. a local Ollama server
        apiKeyEnv: OLLAMA_KEY # omit entirely if the endpoint needs no key
```
Judge BYOK [spec]:
```yaml
defaults:
  judge_model: qwen3
  judge_provider:
    baseUrl: http://localhost:8080/v1 # e.g. a local OpenAI-compatible server
    apiKeyEnv: JUDGE_API_KEY # env-var name; omit if the endpoint needs no key
```
You can also resolve the judge provider from Copilot's env vars: `judge_provider: { source: copilot-env }` or `export VALLY_JUDGE_PROVIDER_SOURCE=copilot-env`. It reads `COPILOT_PROVIDER_BASE_URL` (required) and the other `COPILOT_PROVIDER_*` vars. This path is strictly opt-in, and a conflicting block plus gate is an error [spec].

### Stimulus fields [spec]
```yaml
stimuli:
  - name: my-test-case
    prompt: "Do something"
    agent_environment: { ... }
    artifacts: { ... }
    graders: [...]
    rubric: ["criterion 1", "criterion 2"]
    constraints: { ... }
```
| Field | Required | Notes |
|---|---|---|
| `name` | **Yes** | unique (lint `duplicate-stimulus-name`) |
| `prompt` | one of prompt/turns | ignored when `turns` is set |
| `turns` | one of prompt/turns | multi-turn, same session |
| `attachments` | No | image/document paths; attachment-capable executors only (e.g. `copilot-sdk`) |
| `agent_environment` | No | merged with root; alias `environment` |
| `grading_environment` | No | grader-only files |
| `artifacts` | No | `include` (required, non-empty) / `exclude` globs; `.git` always excluded |
| `graders` | No | GraderConfig[] |
| `rubric` | No | non-empty strings; used by `prompt`/`panel`/`compare` |
| `constraints` | No | resource limits |
| `simulation` | No | tool-call simulation (copilot-sdk only) |
| `supported_executors` | No | allow-list; stimulus is **skipped** under other executors |
| `golden_patch` / `golden_trajectory` / `golden_custom_metrics` | No | for `oracle` |
| `tags` | No | filtering |

Multi-turn [g-spec]:
```yaml
stimuli:
  - name: recall-across-turns
    turns:
      - "Remember this code name for later: ALPHA-7."
      - "Acknowledged? Just say ready."
      - "What was the code name I gave you at the start?"
    graders:
      # Scope a grader to one turn with `turn:` (0-based index into `turns`).
      - type: output-contains
        turn: 1 # the "say ready" acknowledgement
        config:
          substring: "ready"
          case_sensitive: false
      - type: output-contains
        turn: 2 # the recall question
        config:
          substring: "ALPHA-7"
```
A grader without `turn:` sees the whole trajectory. File-based graders can't use `turn:` [g-spec]. The executor must set `supportsMultiTurn` [g-exec].

### Grader config wrapper [spec]
```yaml
graders:
  - type: output-contains
    name: "output includes hello"
    config:
      substring: "hello"
      case_sensitive: false
```
Fields:
- `type` (required).
- `name`: optional display name. The default is derived from config, e.g. `output-matches /Cosmos/`, with a `#1`/`#2` suffix on collision [debug].
- `turn` (0-based).
- `scope`: `parent` | `subagent` | `{ agent: "<id>" }`, non-workspace graders only.
- `config`.

LLM judge evidence selector [spec]:
```yaml
graders:
  - type: prompt
    config:
      evidence: [trajectory, diff, golden_patch, repo]
      output_delivery: workspace
```

Subagent scope [spec]:
```yaml
graders:
  # The parent delegated the edit; assert it did not edit directly.
  - type: tool-calls
    scope: parent
    config:
      disallowed: [edit]
  # Assert the delegated subagent actually performed the edit.
  - type: tool-calls
    scope: subagent
    config:
      required: [edit]
```

### Environment (EnvironmentConfig) [spec][vyaml]
```yaml
environment:
  skills:
    - ./path/to/my-skill # Skill directory (containing SKILL.md)
  files:
    - src: fixtures/input.txt
      dest: input.txt
    - src: fixtures/test-data # directories are copied recursively
      dest: test-data
    - src: fixtures/session-log # staged outside the graded workspace
      dest: session-state/session-1
      dest_root: assets
  commands:
    - npm install
  commandTimeout: 2m
  git:
    type: worktree
    ref: v2.1.0
    source: ../my-repo
  mcpServers:
    db:
      type: stdio
      command: db-serve
      args: ["--port", "5432"]
    api:
      type: http
      url: http://localhost:3000/mcp
  env:
    COPILOT_AGENT_ACTION: review
    LOG_LEVEL: debug
```
- `commands` run **from the workspace directory** in `/bin/sh` or `cmd.exe`. `commandTimeout` defaults to `60s` [spec].
- `files[].dest_root`: `workdir` (default) or `assets`. Files staged into `workdir` are excluded from diffs because the baseline is captured after setup, but file graders still see them [spec].
- `git.type: worktree` needs `ref` and `source`, plus optional `timeout` (default 5m). `git.type: clone` needs `url`, plus optional `ref`, `shallow`, `sparse`, `timeout` [spec].
- `mcpServers` stdio fields: `command`, `args`, `env`, `cwd`, `timeout`. http/sse fields: `url`, `headers`, `timeout` [spec].
- `env` sets vars on the agent process. `${EVALUATE_ASSETS}` is the only token expanded. The `mock` executor ignores `env` and warns [spec].
- Merge rules (root + stimulus): skills are deduplicated with a warning. Duplicate commands **throw**. Same `dest` with a different `src` throws, and identical entries also throw. Arrays concatenate [g-spec][spec].
- Staging agent profiles: Copilot uses `.github/agents/x.agent.md`, Claude Code uses `.claude/agents/x.md`. They load natively and are invoked as model-routed subagents. Gate that with `tool-calls` `required: [{name: "^task$", args: {agent_type: "^Reviewer$"}}]` [spec].
- The hosted `github-mcp-server` is disabled. Workspace `.mcp.json` is not discovered [spec].

### grading_environment [spec]
```yaml
agent_environment: # staged before the run, agent sees it
  files:
    - { src: repo/, dest: . }
grading_environment: # staged only for grading, hidden from the agent
  files:
    - { src: fixtures/answer-key.json, dest: .vally-grading/answer-key.json }
    - { src: fixtures/hidden-tests, dest: tests } # a dir, copied recursively
```
Graders run on a disposable copy. Lint rejects overlap with agent-visible sources (`grading-file-src-agent-visible`) [spec].

### Constraints [spec]
```yaml
constraints:
  max_turns: 10
  max_tokens: 5000
  max_duration: 1m
  max_agent_duration: 45s
```
- `max_duration` is a hard cap: overrunning **fails** the run.
- `max_agent_duration` stops the agent, then grades what it produced as a **success** (`endReason: "agent_timeout"`). Keep it below the hard cap.

The old behavioral aliases were removed; lint reports `unsupported-constraint` and names the equivalent `tool-calls`/`skill-invocation` config [lint].

### Simulation [spec]
```yaml
stimuli:
  - name: npm-registry-down
    prompt: "Install the project dependencies"
    simulation:
      max_iterations: 20
      tool_overrides:
        bash:
          patterns:
            - match: "npm install|npm ci"
              output: |-
                npm error code ETIMEDOUT
                npm error network request to registry.npmjs.org failed
              is_error: true
            - match: "node -v"
              output: "v14.21.3" # successful stdout (is_error defaults to false)
        web_fetch:
          output: "Error: HTTP 403 Forbidden"
          is_error: true
```
- Shell tools (`bash`/`shell`/`powershell`) can simulate success or failure. Non-shell tools can only simulate failures.
- MCP tools are not simulated.
- Simulated calls are flagged `simulated: true` and counted in `simulatedToolCallCount`.

### Golden inputs (oracle) [spec][oracle]
```yaml
stimuli:
  - name: fix-the-bug
    prompt: "Fix the off-by-one error in pagination"
    golden_patch:
      path: solutions/fix-the-bug.patch
  - name: add-readme
    prompt: "Add a README"
    golden_patch:
      inline: |
        --- /dev/null
        +++ b/README.md
        @@ -0,0 +1 @@
        +# My Project
```
`golden_trajectory` (ATIF; `inline` or `path`) and `golden_custom_metrics` (`inline` object or `path`) follow the same pattern. The spec includes a complete inline ATIF example. Rule: keep each `observation` in the same step as its `tool_call` [spec].

### Scoring [spec][scoring]
```yaml
scoring:
  weights:
    file-exists: 0.7
    output-contains: 0.3
  threshold: 0.7
```
See section (e) and the Scoring notes below.

### Complete example [spec]
```yaml
name: test-writer-eval
description: Evaluates the test-writer skill
version: "1.0"
type: capability

agent_environment:
  skills:
    - ./my-skill # Skill directory (containing SKILL.md)

defaults:
  runs: 3
  timeout: 2m
  model: gpt-5.5
  executor: copilot-sdk

stimuli:
  - name: basic-test-generation
    prompt: |
      Write unit tests for this function:
      function add(a, b) { return a + b; }
      Save the tests to add.test.js.
    graders:
      - type: file-exists
        name: "test file was created"
        config:
          path: "add.test.js"
      - type: output-contains
        config:
          substring: "test"
      - type: tool-calls
        config:
          required: ["write_file"]
    constraints:
      max_turns: 10

  - name: edge-case-empty-input
    prompt: "Write tests for a function that takes no arguments."
    graders:
      - type: file-exists
        config:
          path: "*.test.js"

scoring:
  weights:
    file-exists: 0.5
    output-contains: 0.3
    tool-calls: 0.2
  threshold: 0.7
```

### `vally init` starter (evals/hello/eval.yaml) [first]
```yaml
name: hello
description: A minimal example eval — the agent writes a small hello.json and we check it.
type: capability

defaults:
  timeout: 2m

stimuli:
  - name: greeting-json
    prompt: |
      Create a file named hello.json that describes a greeting. It must be
      valid JSON with two fields:

        - "message": a short, friendly greeting
        - "language": the two-letter code "en"
    graders:
      - type: file-exists
        config:
          path: hello.json
      - type: file-matches
        config:
          path: hello.json
          pattern: '"language"\s*:\s*"en"'
      - type: file-matches
        config:
          path: hello.json
          pattern: '"message"\s*:\s*".+"'

scoring:
  weights:
    file-exists: 0.34
    file-matches: 0.66
  threshold: 1.0
```

### Parameters `${KEY}` [eval]
Precedence, highest first:
1. CLI `--param KEY=value`
2. Param file: `eval.params.yaml` (eval-level) or `.vally.yaml` `params:` (suite-level)
3. Inline `${KEY=fallback}`

Escape a literal with `$${HOME}`. `lint --param` suppresses `undefined-param` [lint].

### .vally.yaml [vyaml]
`paths` defaults:

| Field | Default |
|---|---|
| `skills` | `["skills/"]` |
| `evals` | `["evals/"]` |
| `results` | `"vally-results/"` |
| `evalFilenames` | `["eval.yaml","eval.yml"]` (globs allowed; setting it **replaces** the defaults) |

Complete example [vyaml]:
```yaml
paths:
  skills: [skills/]
  evals: [evals/]
  results: vally-results/
  evalFilenames: ["eval.yaml", "eval.yml", "*.eval.yaml"]

environments:
  default-workspace:
    skills: [skills/copilot]
    commands: [npm install]
    mcpServers:
      db:
        type: stdio
        command: db-serve
        args: ["--port", "5432"]

suites:
  ci-gate:
    description: "Fast checks for every PR"
    filter:
      priority: [p0, p1]

  safety:
    description: "All safety evals"
    evals: ["evals/safety/**/*.eval.yaml"]

  safety-p0:
    description: "Critical safety evals only"
    evals: ["evals/safety/**/*.eval.yaml"]
    filter: { priority: p0 }
```
Reference a named environment from an eval [vyaml][g-spec]:
```yaml
agent_environment: auth-workspace
stimuli:
  - name: login-test
    prompt: "Test the login flow"
```
Suite rules [suites][vyaml]:
- Every suite needs at least one of `filter`/`evals`.
- Filters: AND across keys, OR within values, include-only.
- A stimulus missing a filter key does not match.
- `evals` globs resolve relative to the project root, may enter dot-dirs and `..` siblings, do not follow symlinks, and are case-sensitive.
- Negated globs are not supported.
- Both `filter` and `evals` together act as an intersection.
- Tag values must be strings (`"1"`, not `1`).

JSON schema location: `packages/core/src/config/vally-config.schema.json` (VS Code `yaml.schemas`) [vyaml].

### Experiment file [expfile]
```yaml
name: model-comparison
evals:
  - evals/auth/eval.yaml
  - evals/search/eval.yaml

vary: [/defaults/model]

baseline: gpt-5.5
variants:
  gpt-5.5:
    overrides:
      model: gpt-5.5
  claude-sonnet-4.6:
    overrides:
      model: claude-sonnet-4.6
```
Matrix form [expfile]:
```yaml
name: model-x-skills
evals:
  - evals/auth/eval.yaml

matrix:
  model:
    path: /defaults/model
    values: [gpt-5.5, claude-sonnet-4.6]
  skills:
    path: /environment/skills
    values:
      - none: []
      - matched: ["plugins/${eval.parent}/skills/*"]

baseline:
  model: gpt-5.5
  skills: none
```
Key rules:
- Top level: `name`, `evals` (globs), `vary` (JSON Pointers; required with `variants`, forbidden with `matrix`), `baseline`, and exactly one of `variants`/`matrix`. Optional: `overrides` and `execution.workers`.
- `filter`, `grader_plugins`, `executor_plugins`, `eval_plugin` are parsed but **not yet wired**.
- Differences outside `vary` are rejected as drift.
- Overridable fields: `overrides` accepts `runs, timeout, model, executor, judge_model, judge_provider, reasoning_effort, judge_reasoning_effort`. `environment` accepts `skills, git, files, commands, commandTimeout, mcpServers, env`.
- Env merge: arrays **replace**, maps deep-merge, `null` deletes.
- Matrix: 2–256 cells. Names follow `axis=label,…`.
- Interpolation: `${eval.name|path|dir|basename|parent|grandparent}`.
- "`vally experiment` is new in 0.6.0" [experiment].

---

## (e) Every built-in grader

The catalog lists 36 graders [graders]. "All graders are **reference-free** … and **trajectory-level**" [graders]. Regex patterns are JavaScript regex, with inline flags `(?i)`, `(?m)`, `(?s)` [gr:output-matches][gr:file-matches].

### Output graders
| Grader | Determinism/Cost | Config | One-line example |
|---|---|---|---|
| `output-contains` | static/free | `substring` (req), `case_sensitive` (default **false**), `negate` | `{type: output-contains, config: {substring: "hello world"}}` [gr:output-contains] |
| `output-not-contains` | static/free | same; shorthand for `negate: true` | `{type: output-not-contains, config: {substring: "error"}}` |
| `output-matches` | static/free | `pattern` (req, unanchored search), `negate` | `{type: output-matches, config: {pattern: "function\\s+\\w+\\("}}` [gr:output-matches] |
| `output-not-matches` | static/free | same | `{type: output-not-matches, config: {pattern: "(?i)error\|exception"}}` |

These check `trajectory.output`, the final output only. [gr:output-contains] shows the `grade()` source.

### Transcript graders (every assistant message)
| Grader | Config | Example |
|---|---|---|
| `transcript-contains` | `substring` (req), `case_sensitive` (default false), `negate` | `{type: transcript-contains, config: {substring: "could you clarify"}}` [gr:transcript-contains] |
| `transcript-not-contains` | same | `{type: transcript-not-contains, config: {substring: "rm -rf"}}`. **Fails** on zero assistant messages (no vacuous pass). |
| `transcript-matches` | `pattern` (req), `negate` | `{type: transcript-matches, config: {pattern: "(?i)i will not"}}` [gr:transcript-matches] |
| `transcript-not-matches` | same | `{type: transcript-not-matches, config: {pattern: "(?i)error\|exception"}}` |

### assistant-contains-tool-output (static/free) [gr:actc]
- Config: `tools` (string[], req; exact or `name.` prefix) and `pattern` (regex, req; group 1 or the full match is the needle).
- Passes when a **later** assistant message contains the captured value (case-sensitive substring).
- Example: `{type: assistant-contains-tool-output, config: {tools: [tool-catalog-lookup_release_train], pattern: '"release_id":"(rt_[0-9a-f]{16})"'}}`

### Session health [gr:completed]
- `completed` (static/free, no config): output is non-empty, there are no `error` events, and at least one `turn_end` exists. Example: `- type: completed`
- `exit-success` (legacy compat, no config): only checks for non-empty output ("use it when porting evals from skill-validator"). Example: `- type: exit-success`

### File graders (read the workspace)
| Grader | Determinism/Cost | Config | Example |
|---|---|---|---|
| `file-exists` | static/low | `path` (file or glob, req), `negate` | `{type: file-exists, config: {path: "add.test.js"}}` [gr:file-exists] |
| `file-not-exists` | static/low | same | `{type: file-not-exists, config: {path: "*.tmp"}}` |
| `file-contains` | static/low | `path` (req), `value` (req, case-sensitive), `negate` | `{type: file-contains, config: {path: "add.test.js", value: "expect"}}` [gr:file-contains] |
| `file-not-contains` | static/low | same | `{type: file-not-contains, config: {path: "*.csproj", value: "packages.config"}}` |
| `file-matches` | static/low | `path` (glob, req), `pattern` (req), `negate` | `{type: file-matches, config: {path: "**/Program.cs", pattern: "static\\s+\\w+\\s+Add\\("}}` [gr:file-matches] |
| `file-not-matches` | static/low | same | `{type: file-not-matches, config: {path: "**/Program.cs", pattern: "null!"}}` |

Globs match regular files including dotfiles, not directories or symlinks. Unreadable matching files make the result "indeterminate", which fails in both modes [gr:file-contains][gr:file-matches].

### Diff graders (git-based workspace diff)
| Grader | Determinism/Cost | Config | Example |
|---|---|---|---|
| `diff-contains` | complex-static/low | exactly one of `pattern` (regex) / `value` (literal); `negate`; supports `turn` | `{type: diff-contains, config: {pattern: "def divide"}}` [gr:diff-contains] |
| `diff-not-contains` | complex-static/low | same | `{type: diff-not-contains, config: {pattern: "secrets\\."}}` |
| `diff-empty` | complex-static/low | none; supports `turn` | `{type: diff-empty, turn: 0}` [gr:diff-empty] |

Caveats [gr:diff-contains][gr:diff-empty]:
- The diff honors `.gitignore`, so changes to ignored paths are invisible and restraint checks can pass wrongly.
- `git` must be on PATH.
- Re-grading needs the recorded diff (`--run-dir` for sidecars).

### Behavior graders
**`tool-calls`** (static/low) [gr:tool-calls]
- Lists: `required`, `disallowed`, `sequence` (ordered subsequence), `parallel` (same model-response batch). At least one is required.
- Entries are a string (regex on name) or a ToolMatch:
  - `name` (req, unanchored regex)
  - `command`, `path`, `args` (map of regexes)
  - `pattern` (regex on `JSON.stringify(arguments)`)
  - `write_only`/`read_only` (redirect `pattern` to extracted file targets)
  - `result` (regex on output; not allowed on sequence/parallel)
  - `min_count`, `final`, `at_step`, `before_step` (`required` only)
- Example: `{type: tool-calls, config: {required: [{name: bash, command: "npm test"}], disallowed: [{name: view, path: "\\.env$"}]}}`

**`skill-invocation`** (static/free) [gr:skill-invocation]
- Config: `required` / `disallowed` string[] (exact match; at least one required; no overlap).
- Example: `{type: skill-invocation, config: {required: [code-review]}}`

**`system-event`** (static/free) [gr:system-event]
- Config: `required` / `disallowed` lists of `system` event `eventType` values (exact, case-sensitive).
- Example: `{type: system-event, config: {required: [compaction]}}`

**`max-repeat`** (static/free) [gr:max-repeat]
- Config: `max` (req, int >= 1), `max_cycle_period` (1–10, default 1), `match` (`observation` default | `name` | `name-args`), `tools` (regex[]).
- Post-hoc loop detection. Calls within one turn collapse into one step.
- Example: `{type: max-repeat, config: {max: 3}}`

**`loop-outcome`** (static/free) [gr:loop-outcome]
- Config: `should_loop` (default false), `max_acceptable_retries` (req, int >= 0), `max_cycle_period`, `match` (default `name-args`), `tools`.
- A `simulation_cap` ending always counts as a loop.
- Example: `{type: loop-outcome, config: {should_loop: false, max_acceptable_retries: 3}}`

### Metric threshold graders (static/free; `max` required) [gr:metric]
| Grader | `max` type | Example |
|---|---|---|
| `token-budget` | int (input+output tokens) | `{type: token-budget, config: {max: 50000}}` |
| `tool-call-count` | int; optional `tools` regex[] | `{type: tool-call-count, config: {max: 3, tools: ["^web_search$"]}}` |
| `turn-count` | int | `{type: turn-count, config: {max: 10}}` |
| `step-count` | int; optional `tools` (step names: tool name, `response`, or system event type) | `{type: step-count, config: {max: 40}}` |
| `error-count` | int | `{type: error-count, config: {max: 0}}` |
| `wall-time` | duration string | `{type: wall-time, config: {max: "2m"}}` |

Scoring: 1 when within budget. Over budget: `max(0, 1 − (value − max) / max(max, 1))` [gr:metric].

### Command and program graders
**`run-command`** (complex-static/low) [gr:run-command]
- Config: `command` (req; shell string if `args` is omitted, binary if `args` is given), `args`, `expected_exit_code` (default 0), `stdout_contains` / `stderr_contains` / `stdout_matches` / `stdout_not_matches` (string or array; all entries must hold), `sub_path`, `timeout` (default `30s`), `env`.
- Example: `{type: run-command, config: {command: "npm test", expected_exit_code: 0}}`

**`program`** (catalog: static/low) [gr:program]
- Config: `program` (req), `args`, `shell` (default false), `sub_path`, `timeout` (default `60s`), `env` (reserved `EVALUATE_*` names rejected).
- Env passed in: `EVALUATE_WORKSPACE`, `EVALUATE_GRADER_INPUT` (a **path to a temp JSON file** holding the `GraderInput`), `EVALUATE_ASSETS`, `EVALUATE_ARTIFACT_DIR`, `EVALUATE_ARTIFACT_DIR_STRICT`.
- Result modes: **exit-code mode** (print nothing; exit 0 = pass) or **GraderResult JSON on stdout**.
- Cannot re-grade once the workspace is gone.
- Example: `{type: program, config: {program: "python", args: ["graders/validate_schema.py"]}}`

Node example from the docs [gr:program]:
```javascript
import { readFileSync } from "node:fs";

const { trajectory, stimulus } = JSON.parse(
  readFileSync(process.env.EVALUATE_GRADER_INPUT, "utf-8"),
);

const created = trajectory.events.filter(
  (e) => e.type === "tool_call" && e.data.toolName === "create",
);

process.stdout.write(
  JSON.stringify({
    name: "used-create-tool",
    kind: "code",
    passed: created.length > 0,
    score: created.length > 0 ? 1 : 0,
    evidence:
      created.length > 0
        ? `Created ${created.map((e) => e.data.arguments.path).join(", ")} for "${stimulus.name}"`
        : "Agent never called the create tool",
  }),
);
```

**`custom-metrics`** (static/low) [gr:custom-metrics]
- Config: `path` (default `custom_metrics.json`; artifact dir first, then workspace) and `assertions` (req).
- Each assertion takes `metric` plus conditions: `min`, `max`, `gt`, `lt`, `equals` (+ `tolerance`), `matches`, `contains`, `present`, `absent`.
- Score = fraction of assertions passed. Cannot use `turn`.
- Example: `{type: custom-metrics, config: {assertions: [{metric: tests_failed, equals: 0}]}}`

### LLM judges
**`prompt`** (llm/high) [gr:prompt]
- Config:
  - `prompt`: supplemental instructions; does **not** define criteria.
  - `model`: default `claude-sonnet-4.6`.
  - `scoring`: `binary` | `scale_1_5` (default) | `scale_1_10`.
  - `threshold`: default `0.5`, normalized.
  - `evidence`: `trajectory` (default) | `diff` | `golden_patch` | `repo`.
  - `output_delivery`: `inline` (default) | `workspace`.
  - `reasoning_effort`.
- Criteria come from the stimulus `rubric`, one sub-result per criterion. The fallback rubric is "The agent completed the requested task correctly" / "The output is clear and well-structured".
- Normalization is min-max: on scale_1_5, a raw 4 becomes 0.75.
- The judge must call the `submit_grade` tool, and is reminded up to 2 times.
- Retries: 2 (5s → 10s → 20s + jitter, 10-minute budget).
- Judge model resolution: `config.model` → `--judge-model` → `defaults.judge_model` → `EVAL_JUDGE_MODEL` → `claude-sonnet-4.6`.
- Comparison mode uses `submit_comparison_grade` with position-swap debiasing.
- Example: `{type: prompt, config: {scoring: scale_1_5, threshold: 0.75}}` with `rubric: [...]` on the stimulus.

Rubric example [gr:prompt]:
```yaml
stimuli:
  - name: writes-unit-tests
    prompt: Add unit tests for the parser
    rubric:
      - Tests cover edge cases (empty input, nulls, errors)
      - Assertions are specific, not just "toBeTruthy"
      - Tests actually run (valid syntax, proper imports)
    graders:
      - type: prompt
        config:
          prompt: Judge only the tests; ignore unrelated refactoring.
```

**`panel`** (llm/high) [gr:panel]
- Config:
  - `models` (req; strings or `{model, reasoning_effort}`)
  - `aggregation`: `mean` (default) | `median` | `min` | `majority` | `unanimous`
  - `scoring` (default scale_1_5), `threshold` (default 0.5), `prompt`
  - `criteria`: `{name, description, weight, pass_threshold, scoring, required}`. It **replaces** `rubric`.
  - `overall_threshold`, `evidence`
- **Any judge error forces FAIL.** `judge_model` and `--judge-model` are ignored. Only inline delivery is supported.
- Cost ≈ stimuli × runs × judges × per-call cost.
- Example: `{type: panel, config: {models: [claude-sonnet-4.6, gpt-5.5, gpt-5.5-mini]}}`

### Lint-only skill graders [lint]
`vally lint <path>` runs two graders on SKILL.md files:
- **spec-compliance**: kebab-case name <= 64 chars, description <= 1024 chars, valid frontmatter.
- **valid-refs**: every referenced file exists.

---

## (f) CLI commands and key flags

Commands listed at [cli]: `init`, `lint`, `eval`, `grade`, `oracle`, `compare`, `experiment` (`run`, `merge`), `export`, `serve`, `ingest`. (`vally new` from 0.3 is not documented.)

### vally init [dir] [init]
- Default dir `evals/hello`.
- `--force` overwrites.
- Writes a starter eval with commented-out OPTIONAL sections (LLM judge, rubric, constraints, environment, experiment pointer).
- Exit 1 if the file exists and `--force` is not set.

### vally lint [path] [lint]
- Flags: `-e/--eval-spec`, `--known-domains <file>`, `--allowed-external-deps <file>`, `--grader-plugin` (repeatable), `--param`, `--strict` (warnings become errors), `--verbose`.
- Eval-spec **errors**: `unknown-grader-type` (with did-you-mean), `invalid-grader-config`, `invalid-scoring-weight-key`, `scoring-weight-sum`, `invalid-constraint-value`, `unsupported-constraint`, `invalid-rubric`, `environment-file-missing-field`, `environment-file-not-found`, `attachment-file-not-found`, `attachment-not-a-file`, `attachment-not-readable`, `environment-command-timeout-invalid`, `duplicate-stimulus-name`, `executor-config-unsupported`, `executor-config-invalid`, `executor-name-invalid`.
- **Warnings**: `duplicate-grader-type-in-stimulus`, `rubric-without-llm-judge`, `llm-judge-prompt-without-rubric`, `regression-without-baseline`, `ineffective-constraint`, `scoring-defaults-applied`, `scoring-weight-coverage`, `scoring-weights-without-threshold`.
- Also mentioned elsewhere: `environment-file-workdir-escape` (warning), `environment-file-assets-escape` (error), `grading-file-src-agent-visible` [spec], `undefined-param` [lint].
- Reference scan codes: `EXTERNAL-DOMAIN`, `HTTP-NOT-HTTPS`, `PIPE-TO-SHELL`, `SCRIPT-NO-SRI`. Dependency codes: `SCRIPT-FILE`, `INVOKES-SCRIPT`, `NON-BUILTIN-TOOL-REF`.
- Exit 0 = pass; 1 = failure.

### vally eval [eval]
Input:
- `-e/--eval-spec` (repeatable; not with `--suite`)
- `--suite`
- `--tag key=v1,v2` / `key!=v` (not with `--suite`; zero matches exits 1)
- `--param`

Execution:
- `--executor`/`--agent`
- `--model a,b` (multi-model)
- `--reasoning-effort`
- `--timeout <duration>` (default `2m`)
- `--runs n`
- `--workers n` (default **5**)
- `--max-retries n` (default **2**; ignored when runs >= 2)
- `--skill-dir`, `--work-dir`
- `--workspace` (preserve; not with multi-model)
- `--shutdown-timeout` (default 20s)

Grading:
- `--threshold 0..1`
- `--require-pass`
- `--judge-model`, `--judge-reasoning-effort`
- `--skip-grade`, `--skip-validate`

Reporting:
- `--output-dir` (default `./vally-results`, timestamped subdir)
- `--output jsonl` (stdout: `trial-result` records + `run-summary`)
- `--junit` (`eval-results.junit.xml`)
- `--verbose`

Plugins:
- `--grader-plugin`, `--executor-plugin`, `--eval-plugin` (requires `--eval-spec`), `--reporter-plugin` (all repeatable except eval-plugin)
- `--backend` (default `local`), `--backend-args k=v`
- `--otlp-endpoint <url>`

**Exit codes:** 0 = completed without errors, *even if verdicts failed*. 1 = grader/execution/config/tooling error, filter matched nothing, or `--require-pass` with a failing verdict.

Output layout [eval]:
```plaintext
results/
└── <timestamp>/
    ├── results.jsonl
    ├── eval-results.md
    ├── otel-spans.jsonl       (absent when --otlp-endpoint specified)
    └── <eval-name>/<stimulus-name>/<model>/0/
        ├── metadata.json
        ├── events.jsonl   (best-effort, may be absent)
        └── artifacts/     (present only when the stimulus configures `artifacts`)
```

### vally grade [grade]
- Reads stdin.
- Input formats (auto-detected): `trial-result` JSONL, legacy EvalOutcome JSONL, single EvalOutcome JSON, ATIF JSON, Copilot CLI session-run JSON (`{"sessionKind":"copilot-cli","sessionId":"abc123"}` or `sessionPath`). Formats can't be mixed.
- Flags: `-e/--eval-spec` (req), `--stimulus`, `--workspace`, `--run-dir`, `--artifact-dir`, `--assets-dir`, `--diff-file`, `--output jsonl`, `--judge-model`, `--judge-reasoning-effort`, `--grader-plugin`, `--param`, `--verbose`, `--require-pass`.
- Exit 1 on input or grading errors, or `--require-pass` failure.

Examples:
```bash
vally eval --eval-spec eval.yaml --skip-grade --output jsonl \
  | vally grade --eval-spec eval.yaml
vally grade --eval-spec eval.yaml < results/outcomes.jsonl
```

### vally oracle [oracle]
- Flags: `-e/--eval-spec` (req), `--stimulus`, `--no-golden-input` (negative control), `--output jsonl|atif` (atif requires `--skip-grade` + one stimulus), `--skip-grade`, `--judge-model`, `--judge-reasoning-effort`, `--grader-plugin`, `--keep-workspace`, `--workspace` (single stimulus), `--verbose`.
- Exit codes invert in baseline mode.
- Behavior/output graders are rejected without a `golden_trajectory`.

### vally compare [compare]
- Modes: `vally compare <experiment-dir>` or `--baseline <path> --treatment <path>`.
- Flags: `--baseline-variant`, `-e/--eval-spec` (overrides rubric), `--judge-model`, `--judge-reasoning-effort`, `--output <jsonl>`, `--fail-on-regression` (negative mean whose 95% CI is entirely below 0), `--param`, `--verbose`.
- Output: win rate, signed mean score in [-1,1] with a 95% CI, McNemar test, metric deltas with CIs.
- Verdict scale: much better +1.0 / slightly better +0.4 / tie 0 / slightly worse -0.4 / much worse -1.0.
- Judge retries: 2. A partial comparison exits 1.
- Pairing is by stimulus name + trial index. No eval spec is required (the rubric is read from the trajectories).

### vally experiment [experiment]
- `run <file>` flags: `--variant`, `--eval-filter` (repeatable; narrows only), `--output-dir` (default `./vally-experiment-results`), `--workers` (default 5), `--backend`, `--backend-args`, `--shard i/n` + `--run-id`, `--shard-strategy` (`round-robin` | `by-stimulus` | module), `--param`, `--reporter-plugin`, `--workspace`, `--dry-run`, `--require-pass`, `--compare` (default judge; never gates on regression), `--verbose`.
- `merge <shard-dir...> -o <path> [--require-pass]`.
- Output: per-variant `results.jsonl` + `run-summary.jsonl`, and `report.md` (unsharded).

### vally export [export]
- Flags: `--eval-spec` (req, repeatable), `--exporter <specifier>` (req), `--grader-plugin`, `--output-dir` (default `./<exporter-name>/`), `--tag`, `--param`, `--verbose`. `-- key=value` pairs are passed to the exporter.
- Local exporter paths resolve from cwd. Bare package names resolve from the eval's directory.
- Harbor is referenced as an exporter in [spec][grade], but no page documents it.

### vally serve [serve]
- `vally serve [directory]` flags: `--port` (default **3200**), `--host` (default `127.0.0.1`), `--cors`, `--allowed-host` (repeatable), `--store <sqlite>`.
- Host-header validation blocks DNS rebinding. `/api/health` is exempt.

### vally ingest [ingest]
- `vally ingest <directory> [--store eval-history.db]`: imports timestamped runs into SQLite, skipping already-imported runs.

### Results API (served by `vally serve`) [results-api][serve]
Endpoints:
- `GET /api/runs`
- `/api/runs/:id`
- `/api/runs/:id/outcomes`
- `/api/runs/:id/matrix?metric=pass_rate`
- `/api/runs/:id/ranking`
- `/api/runs/:id/graders`
- `/api/runs/:id/compare?modelA=&modelB=`
- `/api/runs/:id/tools`
- `GET /api/outcomes` (filters: `runId, model, stimulus, status, passed, grader, limit<=1000, cursor`)
- `/api/outcomes/:id`
- `/api/outcomes/:id/trajectory`
- `/api/outcomes/:id/tools`
- `GET /api/compare?runs=id1,id2`
- `GET /api/metrics`
- `GET /api/health`

Conventions: errors use `{ error: { code, message } }`. Pagination uses `{ page: { nextCursor, limit, hasMore, total } }`. `graderType` is the stable key; `name` changes with config. The docs suggest an agent "funnel": runs → ranking → failing outcomes → outcome evidence.

### Environment variables mentioned anywhere
| Variable | Purpose |
|---|---|
| `COPILOT_GITHUB_TOKEN` | copilot-sdk auth [ci] |
| `ANTHROPIC_API_KEY` | claude-cli [ci] |
| `EVAL_REASONING_EFFORT` | agent effort fallback [eval] |
| `EVAL_JUDGE_MODEL` | judge fallback [gr:prompt] |
| `VALLY_JUDGE_PROVIDER_SOURCE=copilot-env` | judge provider source [spec] |
| `COPILOT_PROVIDER_*` | judge provider values [spec] |
| `EVALUATE_USE_HOST_COPILOT_HOME=1` | disable hermetic COPILOT_HOME [debug] |
| `EVALUATE_ASSETS` | assets dir [spec] |
| `EVALUATE_*` | program grader inputs [gr:program] |
| `VALLY_TELEMETRY_OPTOUT`, `DO_NOT_TRACK` | telemetry opt-out [telemetry] |
| `OTEL_EXPORTER_OTLP_ENDPOINT`, `VALLY_TELEMETRY_ENDPOINT`, `APPLICATIONINSIGHTS_CONNECTION_STRING` | redirect usage telemetry [telemetry] |

---

## (g) Extension points: exact interfaces

### Grader [g-grader]
```typescript
interface Grader {
  metadata: GraderMetadata;
  grade(input: GraderInput): Promise<GraderResult>;
  // Optional: derive a display name from this instance's config (see below).
  defaultName?(config: Record<string, unknown>): string;
  // Optional: implement to support head-to-head comparison (vally compare).
  compare?(input: GraderComparisonInput): Promise<GraderComparisonResult>;
  // Optional: declare that this instance's config asserts the ABSENCE of something
  // (see the oracle baseline / negative-control note below).
  assertsAbsence?(config: Record<string, unknown>): boolean;
}

interface GraderMetadata {
  name: string;
  description: string;
  behavior: GraderBehavior;
  determinism: "static" | "complex-static" | "slm" | "llm";
  reference: "reference-free" | "reference-based";
  temporalScope: "point-in-time" | "trajectory-level" | "cross-trajectory";
  costProfile: "free" | "low" | "medium" | "high";
}

interface GraderBehavior {
  requiresLlmClient?: boolean;
  requiresWorkspace?: boolean;
}
```
- `GraderInput` holds `trajectory`, `stimulus`, `config` [g-grader]. The program grader payload adds `diffBaseDir`, `goldenPatch` [gr:program].
- Read files with `trajectory.workDir`, `artifactDir` (strict-aware), `assetsDir` (untrusted). Helper: `resolveGraderReadRoot` from `@microsoft/vally/graders`. `describeGraderValue` sanitizes names [g-grader].
- `defaultName` must be a pure function of config, is truncated to 60 graphemes, and must be non-async [g-grader].

Full example [g-grader]:
```typescript
import type { Grader, GraderMetadata, GraderInput, GraderResult } from "@microsoft/vally";

export class NoErrorsGrader implements Grader {
  metadata: GraderMetadata = {
    name: "no-errors",
    description: "Checks that the agent produced no error events",
    behavior: {},
    determinism: "static",
    costProfile: "free",
    reference: "reference-free",
    temporalScope: "trajectory-level",
  };

  async grade(input: GraderInput): Promise<GraderResult> {
    if (!input.trajectory) {
      throw new Error("Missing trajectory");
    }

    const errors = input.trajectory.events.filter((e) => e.type === "error");
    const passed = errors.length === 0;

    return {
      name: this.metadata.name,
      kind: "code",
      passed,
      score: passed ? 1 : 0,
      evidence: passed
        ? "No error events in trajectory"
        : `${errors.length} error(s): ${errors.map((e) => e.data.message).join(", ")}`,
      label: passed ? "correct" : "incorrect",
    };
  }
}
```
In-process registration [g-grader]:
```typescript
import { createGraderRegistry } from "@microsoft/vally";
import { NoErrorsGrader } from "./no-errors-grader.js";

const registry = createGraderRegistry();
registry.register(new NoErrorsGrader());
```
Plugin package [g-grader]:
```typescript
import type { GraderRegistry } from "@microsoft/vally";
import { NoErrorsGrader } from "./no-errors-grader.js";

export function registerGraders(registry: GraderRegistry): void {
  registry.register(new NoErrorsGrader());
}
```
```json
{
  "name": "@myorg/vally-grader-quality",
  "main": "dist/index.js",
  "peerDependencies": {
    "@microsoft/vally": "^0.2.0"
  }
}
```
```bash
vally eval --grader-plugin @myorg/vally-grader-quality --eval-spec eval.yaml
vally eval --grader-plugin ./my-graders --eval-spec eval.yaml
vally lint --eval-spec eval.yaml --grader-plugin ./my-graders
```
- `--grader-plugin` works with lint, grade, oracle, export [g-grader].
- Testing uses Vitest (the example constructs a trajectory directly) [g-grader].
- Taxonomy guideline table [g-grader]: string/file ops → `static`, `free`/`low`. Subprocess/I/O → `complex-static`, `low`. Embedding/small model → `slm`, `medium`. GPT-5.5-class → `llm`, `high`.

### Executor [g-exec]
```typescript
interface Executor {
  name: string;
  supportsPreparedWorkspace?: boolean;
  supportsMultiTurn?: boolean;
  supportsTurnCompletion?: boolean;
  supportsEnvVars?: boolean;
  validateConfig?(config: unknown): void;
  execute(stimulus: Stimulus, options: ExecutorOptions): Promise<Trajectory>;
  shutdown(): Promise<void>;
}

interface ExecutorOptions {
  skills?: Skill[]; // Skills to load for this run
  timeout: number; // Timeout in milliseconds
  workDir: string; // Working directory for the agent
  model?: string; // Model override
  reasoningEffort?: "low" | "medium" | "high" | "xhigh";
  executorConfig?: unknown; // from defaults.executor.config (opaque)
  sessionID?: string; // Resume an existing session
  mcpServers?: Record<string, McpServerConfig>; // MCP servers to attach
  env?: Record<string, string>; // Agent-process env vars
  onRawEvent?: (event: unknown) => void;
  onTurnComplete?: (completion: {
    turn: number;
    status: "completed" | "interrupted" | "unavailable";
    final?: boolean;
  }) => Promise<void>;
  sessionLog?: ExecutorSessionLogOptions;
}

interface ExecutorSessionLogOptions {
  rootDir: string;
  sessionID?: string;
  executorArtifactsDir?: string;
}
```
(Comments abbreviated from the source page.)

Implementation example [g-exec]:
```typescript
import type { Executor, ExecutorOptions, Stimulus, Trajectory } from "@microsoft/vally";
import { computeMetrics } from "@microsoft/vally";

export class MyExecutor implements Executor {
  name = "my-executor";

  async execute(stimulus: Stimulus, options: ExecutorOptions): Promise<Trajectory> {
    const startedAt = new Date();

    // Call your AI backend
    const response = await myAiSdk.complete({
      prompt: stimulus.prompt,
      model: options.model,
      timeout: options.timeout,
    });

    const completedAt = new Date();
    const events = convertToTrajectoryEvents(response);
    const metrics = computeMetrics(events);

    return {
      id: crypto.randomUUID(),
      stimulus,
      events,
      output: response.text,
      workDir: options.workDir,
      metadata: {
        startedAt,
        completedAt,
        model: options.model ?? "unknown",
        executor: this.name,
        skillsLoaded: [],
        sessionID: "",
      },
      metrics: {
        ...metrics,
        wallTimeMs: completedAt.getTime() - startedAt.getTime(),
      },
    };
  }

  async shutdown(): Promise<void> {
    // Clean up connections, pools, etc.
  }
}
```
Plugin [g-exec]:
```typescript
import type { ExecutorRegistry } from "@microsoft/vally";
import { MyExecutor } from "./my-executor.js";

export function registerExecutors(registry: ExecutorRegistry): void {
  registry.register(new MyExecutor());
}
```
```bash
vally eval --executor-plugin @myorg/vally-executor-custom --eval-spec eval.yaml
vally eval --executor-plugin ./my-executor --eval-spec eval.yaml
```
```yaml
defaults:
  executor: my-executor
  model: gpt-5.5
```
Lifecycle [g-exec]:
- `execute()` may run concurrently (`--workers`).
- `shutdown()` is called once, even after errors. Initialize lazily and handle SIGINT/SIGTERM.
- Write the agent's files to `options.workDir`.
- Remote machines are a Backend concern ("Backend egress SPI", not documented).

A config with no `validateConfig` **fails closed**. `lint` validates only built-in executors because it has no `--executor-plugin` flag.

### Reporter (PlanReporter) [g-rep]
```typescript
interface PlanReporter {
  onRunStart?(ctx: PlanRunStartContext): Promise<void>;
  onTrialStart?(item: TrialWorkItem): Promise<void>;
  onTrialResult(event: { item: TrialWorkItem; result: TrialResult }): Promise<void>;
  onTrialPhase?(itemId: string, phase: TrialPhase, detail?: TrialPhaseDetail): Promise<void>;
  onDiagnostics?(diagnostics: ScopedDiagnostic[]): Promise<void>;
  onEvalComplete?(summary: EvalSummary): Promise<void>;
  onRunComplete(
    summary: RunSummary,
    artifacts: RunArtifacts,
    status?: RunCompletionStatus,
  ): Promise<void>;
}

interface PlanRunStartContext {
  evals: EvalPlanMetadata[];
  totalItems: number;
  workers: number;
  source?: { name: string; version: string };
  graderNames?: string[];
  tagFilter?: Record<string, string[]>;
  tagExclude?: Record<string, string[]>;
}

interface TrialResult {
  itemId: string; // matches TrialWorkItem.id
  durationMs: number;
  status: "success" | "error";
  trajectory: Trajectory | null; // null only if the executor errored first
  grade: StimulusGradeResult | null; // null with --skip-grade or no graders
  error?: string;
}
```
- `onTrialResult` and `onRunComplete` are required; a plugin missing them fails at load.
- `RunCompletionStatus` is `"completed" | "failed" | "cancelled"`.
- Ordering: `onRunStart` first. `onTrialResult` at most once per trial, in pool-finish order. `onRunComplete` last.
- Callbacks are serialized per reporter.
- Errors are isolated and never fail the run.
- Copy trajectory data during the callback, because memory is reclaimed afterward.
- Idempotency key: `event.item.id`, or `trajectory.metadata.sessionID`.

Example [g-rep]:
```typescript
import type {
  PlanReporter,
  PlanRunStartContext,
  RunArtifacts,
  RunCompletionStatus,
  RunSummary,
  TrialResult,
  TrialWorkItem,
} from "@microsoft/vally";

export class CollectingReporter implements PlanReporter {
  private readonly trials: Array<{ id: string; passed: boolean }> = [];

  async onRunStart(ctx: PlanRunStartContext): Promise<void> {
    const evalNames = ctx.evals.map((e) => e.evalName).join(", ");
    console.error(`[collecting] run started: ${evalNames} (${ctx.totalItems} trials)`);
  }

  async onTrialResult(event: { item: TrialWorkItem; result: TrialResult }): Promise<void> {
    const id = event.result.trajectory?.metadata.sessionID ?? event.item.id;
    this.trials.push({ id, passed: event.result.grade?.passed ?? false });
  }

  async onRunComplete(
    summary: RunSummary,
    _artifacts: RunArtifacts,
    status: RunCompletionStatus = "completed",
  ): Promise<void> {
    const passed = this.trials.filter((t) => t.passed).length;
    console.error(`[collecting] run ${status}: ${passed}/${this.trials.length} trials passed`);
  }
}
```
```typescript
import type { ReporterRegistry } from "@microsoft/vally";
import { CollectingReporter } from "./collecting-reporter.js";

export function registerReporters(registry: ReporterRegistry): void {
  registry.register(new CollectingReporter());
}
```
```bash
vally eval --reporter-plugin @myorg/vally-reporter-custom --eval-spec eval.yaml
vally experiment run experiment.yaml --reporter-plugin @myorg/vally-reporter-custom
```
Relative plugin paths resolve from the eval-spec directory (or the experiment file's directory), **not cwd**. Prefer absolute paths. A duplicate specifier registers once [g-rep].

Built-in reporters: console, markdown, JUnit XML, JSONL [g-rep].

### Scoring library functions [scorefn]
```typescript
function passAtK(n: number, c: number, k: number): number;          // 1 - C(n-c,k)/C(n,k)
function passAtKNaive(perTrialPassRate: number, k: number): number;  // 1-(1-p)^k, not used
function passToTheK(perTrialPassRate: number, k: number): number;    // p^k
function computeMultiTrialMetrics(trialPassed: boolean[]): MultiTrialMetrics;
function computeStimulusScore(stimulusName: string, trialGrades: Array<{ grade: GraderResult; passed: boolean }>, hasGraders: boolean): StimulusScore;
function computeSkillScore(skillName: string, stimulusScores: StimulusScore[], threshold: number): SkillScore; // eval-level; "Skill" naming historical
```
`computeMultiTrialMetrics([true, true, false, true, true])` → `{ perTrialPassRate: 0.8, passAtK: 1, passToTheK: 0.328, k: 5 }` [scorefn].

### Other seams (named but not documented)
- **Eval providers** (`--eval-plugin`) [eval][g-rep]
- **Lint reporters** [g-rep]
- **Backends** (`--backend`, `--backend-args`; `DisposableTrialResult.supportedExportKinds`) [eval][traj]
- **Exporters** (`--exporter`) [export]
- **Shard strategies** (module specifier) [experiment]

No interface signatures are published for these.

---

## (h) Efficiency features

| Feature | What docs say | Source |
|---|---|---|
| **Re-grading saved trajectories** | `results.jsonl` holds one `trial-result` per trial with the full trajectory inline. Pipe it to `vally grade` to "re-score with different graders without re-running the (expensive) agent execution". The workflow is `--skip-grade --output jsonl > outcomes.jsonl`, then iterate with `grade`. File-based graders need the workspace. Diff graders need `--run-dir`. | [first][grade][debug] |
| **Offline grading of external runs** | ATIF and Copilot CLI session logs, with `--diff-file`, `--artifact-dir`, `--assets-dir` overrides | [grade] |
| **Oracle (no agent)** | Verifies graders against golden inputs. "Re-grading the same inputs is deterministic for static graders, so an oracle run is safe to gate CI on." | [oracle] |
| **Lint first** | "fast, free static check — no agent needed" | [ci][lint] |
| **Workspace caching** | With `runs` >= 2 and setup work, "Vally prepares the workspace **once** and restores it for each trial". Copy-on-write on APFS/btrfs/XFS/ReFS. Skipped for git-backed workspaces and sandbox executors. The executor flag is `supportsPreparedWorkspace`. | [eval][g-exec] |
| **Parallelism** | `--workers` (default 5) sets concurrent stimulus sessions. "Trials within a stimulus run **sequentially**." Experiments share one worker pool across variants. | [eval][experiment] |
| **Sharding** | `experiment run --shard i/n --run-id`, then `experiment merge`. Deterministic, so a lost shard can be re-run. | [experiment] |
| **Retries** | `--max-retries` (default 2, fresh workspace, exponential backoff; ignored when runs >= 2). The prompt judge retries 2x. compare retries 2x. | [eval][gr:prompt][compare] |
| **Rate-limit relief** | Reduce `--workers`, change `--judge-model`, or split `eval --skip-grade` and `grade` | [debug] |
| **Cost/token tracking** | `token_usage` events per call; `metrics.tokenUsage` (input/output/cache/byModel); optional `cost` in `github-copilot` `nano-aiu`, "present only when every `token_usage` event reports the same provider and unit". It "does not include LLM grader or judge usage". `cost_unavailable` event. | [traj][how] |
| **Budget graders** | `token-budget`, `tool-call-count`, `turn-count`, `step-count`, `error-count`, `wall-time`: "most useful for **cost control** … **CI guardrails** … **efficiency tracking**" | [gr:metric] |
| **Loop detection** | `max-repeat`, `loop-outcome`, simulation `max_iterations` | [gr:max-repeat][gr:loop-outcome][spec] |
| **Cost formulas** | prompt: `(num_stimuli × runs × prompt_graders_per_stimulus) × per-call cost`. panel: `stimuli × runs × judges × per-call cost`. Use a smaller `--judge-model` while iterating. | [gr:prompt][gr:panel] |
| **Metric deltas** | compare reports tokens/turns/tool calls/wall time/error deltas with CIs | [compare] |
| **Analytics** | `vally ingest` into SQLite. `vally serve` provides a dashboard plus REST (ranking by pass rate then duration, per-tool stats). | [ingest][serve][results-api] |
| **OTel** | `otel-spans.jsonl` locally, or `--otlp-endpoint`. Spans `vally.trial` → `vally.attempt`. | [eval][telemetry] |
| **Isolation / hermeticity** | Fresh empty `COPILOT_HOME` per run (opt out with `EVALUATE_USE_HOST_COPILOT_HOME=1`) | [debug] |
| | Skill-free by default | [eval] |
| | `grading_environment` hidden from the agent; graders run on a disposable copy | [spec] |
| | `dest_root: assets` outside the graded tree | [spec] |
| | `git` worktree/clone | [spec] |
| | Hosted github-mcp-server disabled | [spec] |
| | `simulation` gives side-effect-free tools | [spec] |
| | `--backend` for remote/Docker | [eval][traj] |
| | Landing page: "Run fast and local while you iterate. Switch to a fully isolated environment when you need a clean, repeatable result" | [home] |
| **Presets** | **Not in the live docs.** The v0.3 local guide described `presets/inner-loop.yaml`, `ci.yaml`, `outer-loop.yaml`. The live site says only to choose graders by taxonomy yourself. | [tax]; local Vally.md |

---

## (i) CI guidance

From [ci]:
1. **Lint on every PR** (`.github/workflows/skill-lint.yml`):
```yaml
name: Skill Lint
on:
  pull_request:
    paths:
      - "**/SKILL.md"
      - "**/*.yaml"

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "22"

      - run: npm install -g @microsoft/vally-cli

      - name: Lint skills
        run: vally lint .

      - name: Validate eval specs
        run: vally lint --eval-spec eval.yaml --strict
```
2. **Eval for behavioral checks** (`.github/workflows/skill-eval.yml`):
```yaml
name: Skill Eval
on:
  pull_request:
    paths:
      - "**/SKILL.md"
      - "**/eval.yaml"

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "22"

      - run: npm install -g @microsoft/vally-cli

      - name: Run evals
        run: |
          vally eval \
            --eval-spec eval.yaml \
            --skill-dir . \
            --require-pass \
            --output-dir ./results
        env:
          COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_CLI_TOKEN }}

      - name: Upload trajectories
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: ./results/
```
   "Always upload trajectory artifacts — they let you re-grade offline with `vally grade` without re-running the agent." [ci]
3. **Exit codes**: `lint` exits 1 if any skill fails. `eval` exits 1 on errors, and on failing verdicts only with `--require-pass` [ci][eval].
4. **Suites per context** [ci]:
```yaml
suites:
  ci-gate:
    filter: { priority: [p0, p1] }
  nightly:
    filter: { priority: [p0, p1, p2] }
```
```yaml
- name: Run CI gate evals
  run: vally eval --suite ci-gate --require-pass
- name: Run nightly evals
  run: vally eval --suite nightly
```
   "The nightly suite omits it so valid failures are reported without failing the scheduled workflow; operational errors still fail both commands." [ci]

Suggested CI layout [suites]:

| Stage | Suite | What it runs |
|---|---|---|
| PR check | `fast` | `priority: p0` |
| Merge gate | `ci-gate` | `priority: [p0, p1]` |
| Nightly | `full` | all |
| Safety review | `safety` | `evals: ["evals/safety/**"]` |

Other CI-relevant items:
- **JUnit**: `--junit` writes `eval-results.junit.xml`, including scores, multi-trial metrics and flakiness [eval][scoring].
- **Oracle as a CI gate** before publishing a benchmark [oracle].
- **Regression gate**: `vally compare --baseline ./results/main --treatment ./results/pr-branch --fail-on-regression` [compare].
- **CI matrix sharding**: `experiment run --variant` or `--shard` + `merge --require-pass` [experiment].
- **BYOK in CI**: "a long-lived provider key is more durable than a Copilot-seated token" [spec].
- **Hermeticity** addresses "it passes for me but not in CI" [debug].
- **Telemetry in CI**: set the opt-out var in the CI environment [telemetry].

---

## (j) Best-practice guidance the docs give (by topic)

**Authoring stimuli and graders**
- Validate first: `vally lint --eval-spec` before running [debug][g-spec].
- Think of stimuli as test cases and graders as assertions [first].
- Put criteria in `rubric`. Use grader `prompt` only for cross-cutting guidance [gr:prompt].
- Declare taxonomy honestly [tax][g-grader].
- Set an explicit grader `name` so reports stay stable when config changes [debug][spec].
- Give multi-turn stimuli stable names, and write rubrics that describe the whole conversation [compare].
- Gate subagent routing with a grader rather than assuming it happened [spec].

**Scoring**
- "Thresholds are for genuinely graded work — judged quality, partial credit — not for pass/fail assertions like `file-exists`." [scoring]
- What to configure [scoring]: assertions that must all hold → no `scoring` block. Judged quality → `threshold`. Some checks matter more → `weights` **and** `threshold`.
- "Omitting a type silences it, so list every type you care about." [scoring]
- `runs`: 1 inner loop, 3 CI gate, 5–10 nightly [scoring].
- Flakiness "usually means an ambiguous prompt, a tight timeout, or an over-strict grader. Compare a failing trial's trajectory against a passing one." [scoring]
- pass^k is "the gap between 'usually works' and 'safe to gate CI on'." [scoring]
- Use `type: regression` with more trials (`runs: 5`) and a higher threshold (0.9) [g-spec].

**Grader choice**
- Reserve LLM judges for nightly/on-demand runs, not PR gates [gr:prompt][tax].
- Use a panel "only after a single `prompt` grader has proven too noisy". Mix model tiers. Prefer static graders for deterministic checks [gr:panel].
- For judge debugging: use `--verbose`, a more specific prompt, `binary` scoring, or a stronger `--judge-model` [debug].
- Oracle works best with file/static graders [oracle].
- Pair metric-threshold graders with a solution-dependent grader for a meaningful negative control [oracle].
- Don't rely on diff graders to prove ignored paths were untouched [gr:diff-contains].
- Prefer `args` over `pattern` in `tool-calls`. Anchor regexes with `^…$` [gr:tool-calls][gr:metric].
- Use `program` for workspace checks. Use built-in or in-process graders for trajectory checks that must survive re-grading [gr:program].
- Avoid `raw` in custom graders [traj].

**Debugging**
- The docs give a debug ladder: lint → read evidence → `--verbose` → inspect trajectories and logs → re-grade → `--workspace` [debug].

**Environments and security**
- Point `grading_environment` at a dedicated `.vally-grading/` directory. Keep grader sources outside agent-visible trees [spec].
- Don't pass long-lived secrets in `environment.env`. Trajectory files aren't filtered [spec].
- Treat session logs, `workspace.patch` and diffs as sensitive [eval][traj].

**Tags and suites**
- Keep tag keys flat, consistent and lowercase. Common dimensions: `priority`, `area`, `type`, `cost` [suites].

**Experiments**
- `--compare` does not gate. Use `vally compare --fail-on-regression` as a separate step [experiment].

---

## (k) Gaps, ambiguities, contradictions

1. **Local runtime auth is undocumented.** [first] says only "requires a working Copilot SDK setup". [ci] documents `COPILOT_GITHUB_TOKEN` for CI only. There's no default agent model documented either; sample output shows `gpt-5.5` [first].
2. **Deprecated `environment` vs `agent_environment` is used inconsistently.** The eval-spec field tables use `agent_environment`, but its Environment examples use `environment` (the page admits this). The eval CLI page and CI examples say `environment.skills`. Experiment variant overrides and `vary` paths use `environment` (`/environment/skills`) [spec][eval][expfile].
3. **`program` grader determinism conflicts.** The catalog and grader page say `static`/low [graders][gr:program]. The taxonomy guideline says a subprocess should be `complex-static` [g-grader].
4. **"All graders are reference-free"** [graders], yet taxonomy and lint discuss `reference-based` graders [tax][spec], and the `prompt` judge can take a golden patch as reference.
5. **Taxonomy dimension count.** [tax] says "these five properties" but also lists Score kind. `GraderMetadata` has no score-kind or portability field; score kind lives on `GraderResult.kind`. The old `portability` dimension (v0.3 local guide) is gone without mention.
6. **Plugin peerDependency versions are stale and inconsistent**: `^0.2.0` (graders), `^0.3.0` (executors), `^0.6.0` (reporters), against 0.16.0 current [g-grader][g-exec][g-rep][npm].
7. **Registration function names differ from v0.3**: now `registerGraders`, `registerExecutors`, `registerReporters`; v0.3 used `register`. Import paths vary too: types are imported from `@microsoft/vally` in guides but from `@microsoft/vally/graders` on [install].
8. **Undocumented plugin seams**: eval providers, lint reporters, backends ("Backend egress SPI"), exporters (Harbor is referenced repeatedly but has no page; exporter interface not published), shard-strategy modules.
9. **Executors**: only `copilot-sdk` and `mock` are documented built-ins. `claude-cli` is a separate package (link only, no page). `cca` and Codex appear in passing [spec]. There's no reference for executor-specific trajectory shapes or tool names.
10. **Presets and automatic loop selection are gone.** The old guide said "taxonomy determines which ones run in each loop" with `presets/*.yaml`. The live docs say you pick graders explicitly [tax]. No migration note.
11. **Removed constraint aliases aren't named.** [lint] mentions `unsupported-constraint` for "A removed behavioral constraint alias", but no page lists which keys were removed. The v0.3 guide had `reject_tools`, `expect_tools`, `reject_skills`, `expect_skills`, `max_duration_ms`; presumably these are what's removed. That's inference, not stated.
12. **No changelog or migration guide**, despite behavioral-change callouts (skill auto-discovery removed [eval]; "`vally experiment` is new in 0.6.0" [experiment]). `vally new` from v0.3 is absent.
13. **`paths.results` vs `--output-dir`**: `.vally.yaml` default `vally-results/` [vyaml] and `eval --output-dir` default `./vally-results` [eval]. The docs never say whether `paths.results` feeds `--output-dir`. Experiment defaults to `./vally-experiment-results`.
14. **Param files are barely documented**: `eval.params.yaml` and `.vally.yaml params:` appear only in [eval] (not in [vyaml]).
15. **Experiment `baseline` wiring conflicts.** [expfile] says "comparison reporting that consumes this field is not yet wired". [compare] says experiment mode "discovers the baseline variant from the embedded provenance". `filter`/plugins fields are inert [expfile].
16. **Named environments**: [vyaml] says `files` "Paths are relative to the eval file's directory" even for environments defined in `.vally.yaml` (ambiguous). Whether a *stimulus* can reference a named environment by string is not stated in the live docs (v0.3 said yes).
17. **pass@k framing**: [how] calls it "probability of at least 1 success in k trials (unbiased combinatorial estimator)". [scoring][scorefn] clarify that with k = n it is per-stimulus 100%/0% ("did this ever work?").
18. **`output-contains` case default changed**: now `case_sensitive` default **false** [gr:output-contains][debug]. The v0.3 local guide said default true.
19. **Results API vs serve table**: [results-api] lists `/api/runs/:id/compare` and `/api/outcomes/:id/tools`, which the [serve] table omits. There's no dashboard UI documentation at all.
20. **Samples are inaccessible**: `samples/multi-turn-memory` links to a repo that 404s publicly.
21. **`exit-success` references** "vally's `exit_success` assertion type" and "skill-validator" [gr:completed], which are unexplained legacy.
22. **Model names** in examples (`gpt-5.5`, `claude-opus-4.8`, `claude-sonnet-4.6`) come without a list of which models the Copilot SDK exposes. Ted's `.vally.yaml` comments use a `github-copilot/<model>` prefix form that the docs never show.
23. **Tag override vs merge**: stimulus tags "**override** (not merge)" on the same key [suites]. Fine, but the old guide implied merge.
24. **Constraints `max_tokens`/`max_turns` enforcement semantics** (fail vs stop) aren't described; only the duration pair is [spec].
25. **The CI example lints `--eval-spec eval.yaml` at repo root**, which assumes a single root spec. No guidance on linting many specs at once (no glob or suite option on `lint`) [ci][lint].

---

## (l) Local prior art (Ted's ~/src/me/skills, read-only)

Files: `~/src/me/skills/Vally.md` (a 2,159-line "Complete Guide", explicitly "covers vally v0.3.0"), `~/src/me/skills/.vally.yaml`, 20 `skills/*/evals/eval.yaml` files (5,446 lines total), 16 sibling `rubrics.yaml` files, `scripts/eval-skill.js`, `package.json`.

**Patterns Ted uses**
- `.vally.yaml`: `paths: {skills: skills/, evals: skills/, results: results/, evalFilenames: [eval.yaml]}`. Evals live beside skills at `skills/<name>/evals/eval.yaml`. Comments show `--model github-copilot/claude-opus-4.6` and `--judge-model github-copilot/gpt-4.1`.
- `package.json`: `@microsoft/vally` and `@microsoft/vally-cli` `^0.3.0` as devDeps. Scripts: `eval` (`vally eval`), `eval:lint` (`vally lint .`), `eval:skill` (`node scripts/eval-skill.js <skill>` → `npx vally eval --eval-spec skills/<name>/evals/eval.yaml`).
- Eval shape (e.g. coauthor): `type: capability`, `tags: {domain, cost}`, `environment: {skills: [..]}`, `config: {timeout: 120}`. Stimuli are **knowledge probes** ("You have a skill called 'coauthor' loaded in your context. What are the main stages…?") with `constraints: {reject_tools: [bash, edit]}` and `tags: {category, cost}`.
- Grader mix across all evals: `output-matches` 401, `output-contains` 47, `prompt` 14 (fork-prompt, voice-clone), `output-not-matches` 3, `file-exists` 3, `output-not-contains` 2, `file-matches` 2, `file-contains` 1, `tool-calls` 1. This is overwhelmingly regex-on-final-output, typically `(?i)(a|b|c)` alternations.
- `judge_model: claude-sonnet-4.6` appears in fork-prompt and voice-clone. Stimulus `rubric` entries there are multi-line numbered checklists.
- `rubrics.yaml` files are dimension-keyed prose rubrics with 1.0/0.5/0.0 anchors ("Used by LLM judge graders when added to stimuli"). Vally doesn't read these files: it reads stimulus `rubric` [spec]. They're an authoring convention only.

**Things that will likely break or behave differently on 0.16** (compared against the live docs above)
- `config:` block → `defaults:`. `timeout: 120` needs a unit (`120s`) [spec][eval].
- `environment:` → `agent_environment:` (deprecated alias still accepted, with a warning) [spec].
- `constraints.reject_tools` is likely a removed alias (lint `unsupported-constraint`; see k#11). The replacement is a `tool-calls` grader with `disallowed: [bash, edit]` [lint][gr:tool-calls].
- meeting-followup's `tool-calls` grader uses a top-level `config.pattern`. `pattern` is documented only inside ToolMatch entries, so this is likely `invalid-grader-config` [gr:tool-calls][lint].
- Skills are no longer auto-discovered. The evals declare `environment.skills: [..]`, which is still the recommended path [eval].
- Many stimuli have multiple graders and no `scoring` block, which triggers the `scoring-defaults-applied` warning. The verdict is all-or-nothing [scoring][lint].
- `output-contains` is now case-insensitive by default [gr:output-contains].
- Install/auth: the GitHub Packages `.npmrc` + `read:packages` PAT is no longer needed. Node must be >= 22.12.0 [gs][install].
