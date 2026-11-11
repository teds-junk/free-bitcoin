# Vally docs delta: 0.16.0 → 0.21.0

Audit date 2026-11-09. A delta against `research/vally-docs-digest.md` (57 pages, crawled 2026-09-10, v0.16.0).

**Method.** Diffed the docs-site sources of the two tagged trees (`src-old` = 0.16.0, `src-021` = 0.21.0; versions confirmed from `packages/cli/package.json`). Fetched all 83 live URLs under `https://microsoft.github.io/vally/` with plain curl. Compared the heading anchors of every live page against the 0.21 source. No git, no other network.

All URLs below share the prefix `https://microsoft.github.io/vally`. Citation style: `[/path/#anchor]` is a live docs URL; `[CHANGELOG x.y.z]` is the repo `CHANGELOG.md` (rendered live at `/release-notes/x.y.z/`).

## Headline findings

1. **No course link to the Vally docs is broken.** 132 link occurrences, 38 distinct URLs, 24 files: all return HTTP 200, none redirect, none carry a `#anchor`. No docs page was moved, renamed or removed between 0.16 and 0.21. The owner's broken links are therefore not Vally docs links (see §3 for what *is* wrong with them: 14 resolve but now point at pages whose cited content changed or moved).
2. **The live site is 0.21.0.** All 62 content pages match the 0.21 source heading-for-heading (0 mismatches), and `/release-notes/0.21.0/` carries the "Latest release" badge. No 0.22 page exists.
3. **Local auth is now documented** on a new page, `/get-started/runtime-setup/`. The quickstart tells you to set `EVALUATE_USE_HOST_COPILOT_HOME=1`, which is the opposite emphasis from the 0.16 hermeticity section (now deleted).
4. **Node floor moved to `>=22.15.0`** (was `>=22.12.0`).
5. **Default LLM judge model is now `gpt-5.6-terra`** (was `claude-sonnet-4.6`), and the `prompt` grader **no longer retries failed judge calls** in ordinary grading.
6. **CI auth guidance reversed.** The recommended path is now the built-in `${{ github.token }}` with `permissions: copilot-requests: write`; the PAT is the fallback, under different env var names.
7. **A changelog now exists**: `/release-notes/<version>/` for every release, 0.1.0 to 0.21.0. No migration guide page.
8. **Five new docs pages**: Runtime Setup, Choose a Grader, Run Your First Experiment, Running Evals in Docker, CLI: simulate.
9. **The docs site has its own broken links**: 32 internal links on 11 live pages omit the `/vally/` base and 404 (§3 Table C). A learner who follows a course link and then clicks onward can hit these.

---

## 1. Current URL map (0.21.0)

**Framework.** Astro 7 + Starlight 0.42 (`docs-site/astro.config.mjs`; live `<meta name="generator">` reports Astro v7.4.2, Starlight v0.42.7). Files under `docs-site/src/content/docs/**.mdx` map to `/<path>/` with a trailing slash; `index.mdx` maps to the directory URL. The site base is `/vally/`.

**Redirects config.** One entry: `/reference/cli/docker` → `/guides/running-evals-in-docker/`. Live, `/reference/cli/docker/` returns 200 with a `<meta http-equiv="refresh">` to the guide. That page did not exist in 0.16, so the course cannot link to it.

**Release notes are generated**, not files: `docs-site/release-notes.mjs` parses the repo `CHANGELOG.md` and `src/content.config.ts` injects one page per `## [x.y.z] - date` heading at `/release-notes/<version>/`. There is no index: `/release-notes/` is **404**.

**Where the version shows.** The sidebar "Release Notes" group lists versions newest first (five visible, the rest under "Older releases"). `/release-notes/0.21.0/` shows "Version 0.21.0 · Released November 3, 2026 · Latest release". No version appears in the header or footer.

**Not present:** `sitemap-index.xml` and `sitemap-0.xml` both 404 (unchanged from the digest).

**Sidebar changes.** Guides is now split into "Build Evals" (Writing Eval Specs, Authoring Eval Suites, Choose a Grader) and "Extend Vally" (the three custom-plugin guides), followed by Running Evals in Docker, Run Your First Experiment, Debugging Evals. The old "Built-in Graders" group is flattened to a single "Grader Catalog" link. The 22 per-grader pages are still reachable only from the catalog.

### Content pages (62), all 200 live

| URL | Title | Status vs 0.16 |
|---|---|---|
| `/` | Vally | unchanged |
| `/get-started/` | Get Started | rewritten |
| `/get-started/install/` | Installation | changed |
| `/get-started/runtime-setup/` | Runtime Setup | **NEW** |
| `/get-started/run-your-first-eval/` | Run Your First Eval | rewritten |
| `/get-started/add-to-ci/` | Add to CI | changed (auth) |
| `/concepts/why-vally/` | Why Vally | unchanged |
| `/concepts/how-it-works/` | How It Works | minor |
| `/concepts/grader-taxonomy/` | Grader Taxonomy | minor (judge model in example) |
| `/concepts/scoring/` | Scoring | changed |
| `/guides/writing-eval-specs/` | Writing Eval Specs | changed |
| `/guides/authoring-eval-suites/` | Authoring Eval Suites | minor |
| `/guides/choosing-graders/` | Choose a Grader | **NEW** |
| `/guides/writing-custom-graders/` | Writing Custom Graders | restructured |
| `/guides/writing-custom-executors/` | Writing Custom Executors | restructured |
| `/guides/writing-custom-reporters/` | Writing Custom Reporters | restructured |
| `/guides/running-evals-in-docker/` | Running Evals in Docker | **NEW** |
| `/guides/run-your-first-experiment/` | Run Your First Experiment | **NEW** |
| `/guides/debugging-evals/` | Debugging Evals | rewritten |
| `/reference/` | Reference | unchanged |
| `/reference/cli/` | CLI Commands | +simulate card |
| `/reference/cli/init/` | CLI: init | trivial |
| `/reference/cli/lint/` | CLI: lint | changed |
| `/reference/cli/eval/` | CLI: eval | changed |
| `/reference/cli/grade/` | CLI: grade | changed |
| `/reference/cli/oracle/` | CLI: oracle | changed |
| `/reference/cli/compare/` | CLI: compare | changed |
| `/reference/cli/experiment/` | CLI: experiment | changed |
| `/reference/cli/simulate/` | CLI: simulate | **NEW** |
| `/reference/cli/export/` | CLI: export | changed |
| `/reference/cli/serve/` | CLI: serve | changed |
| `/reference/cli/ingest/` | CLI: ingest | minor |
| `/reference/eval-spec/` | Eval Spec Reference | changed heavily |
| `/reference/experiment-file/` | Experiment File Schema | changed |
| `/reference/vally-yaml/` | .vally.yaml Configuration | changed |
| `/reference/graders/` | Grader Catalog | trivial |
| `/reference/trajectory-format/` | Trajectory Format | changed |
| `/reference/scoring-functions/` | Scoring Functions | minor |
| `/reference/results-api/` | Results API | unchanged |
| `/reference/telemetry/` | Telemetry | trivial |
| `/reference/graders/assistant-contains-tool-output/` | Grader: assistant-contains-tool-output | unchanged |
| `/reference/graders/completed/` | Grader: completed / exit-success | unchanged |
| `/reference/graders/custom-metrics/` | Graders: custom-metrics | trivial |
| `/reference/graders/diff-contains/` | Grader: diff-contains | minor |
| `/reference/graders/diff-empty/` | Grader: diff-empty | minor |
| `/reference/graders/file-contains/` | Grader: file-contains | unchanged |
| `/reference/graders/file-exists/` | Grader: file-exists | unchanged |
| `/reference/graders/file-matches/` | Grader: file-matches | unchanged |
| `/reference/graders/loop-outcome/` | Grader: loop-outcome | unchanged |
| `/reference/graders/max-repeat/` | Grader: max-repeat | unchanged |
| `/reference/graders/metric-thresholds/` | Graders: metric thresholds | minor |
| `/reference/graders/output-contains/` | Grader: output-contains | unchanged |
| `/reference/graders/output-matches/` | Grader: output-matches | unchanged |
| `/reference/graders/panel/` | Grader: panel (LLM panel of judges) | changed |
| `/reference/graders/program/` | Grader: program | minor |
| `/reference/graders/prompt/` | Grader: prompt (LLM judge) | changed heavily |
| `/reference/graders/run-command/` | Grader: run-command | trivial |
| `/reference/graders/skill-invocation/` | Grader: skill-invocation | unchanged |
| `/reference/graders/system-event/` | Grader: system-event | unchanged |
| `/reference/graders/tool-calls/` | Grader: tool-calls | minor |
| `/reference/graders/transcript-contains/` | Grader: transcript-contains | unchanged |
| `/reference/graders/transcript-matches/` | Grader: transcript-matches | unchanged |

### Release-notes pages (21), all 200 live

`/release-notes/<v>/`, titled "Release notes <v>", for: 0.21.0 (2026-11-03), 0.20.0 (2026-10-22), 0.19.0 (2026-10-13), 0.18.0 (2026-10-05), 0.17.0 (2026-09-23), 0.16.0 (2026-09-08), 0.15.0, 0.14.0, 0.13.0, 0.12.0, 0.11.0, 0.10.0, 0.9.0, 0.8.0, 0.7.0, 0.6.0, 0.5.0, 0.4.0, 0.3.0, 0.2.0, 0.1.0.

---

## 2. Moved, removed and added pages

**Moved or renamed: none.** Every one of the digest's 57 URLs still exists at the same path with the same title.

**Removed: none.**

**Added (26 URLs):**

| URL | One-line description |
|---|---|
| `/get-started/runtime-setup/` | Step 2 of the quickstart: authenticate the default `copilot-sdk` executor locally, by reusing a Copilot CLI login or with a `COPILOT_GITHUB_TOKEN` PAT. |
| `/guides/choosing-graders/` | Decision guide mapping evidence (responses, files, behaviour, custom logic) to the simplest reliable grader, plus a five-step selection order and `prompt` vs `panel`. |
| `/guides/run-your-first-experiment/` | Walkthrough: two-variant experiment file, `--dry-run`, `--require-pass --compare`, then `vally compare --fail-on-regression`; ends with a matrix example. |
| `/guides/running-evals-in-docker/` | The built-in Docker backend: task/grade container split, image requirements, backend arguments, plugins in containers, cleanup. |
| `/reference/cli/simulate/` | `vally simulate record`: turn a recorded run into a paste-ready `simulation.tool_overrides` block. |
| `/release-notes/0.1.0/` … `/release-notes/0.21.0/` | 21 per-version changelog pages generated from `CHANGELOG.md`. |
| `/reference/cli/docker/` | Redirect stub only → `/guides/running-evals-in-docker/`. |

**Anchors that disappeared** (pages kept their URL, but a deep link to these would now land at the top of the page). None of these is used by the course today; listed so new links avoid them.

| Page | Removed anchor (0.16) | Nearest 0.21 anchor |
|---|---|---|
| `/guides/debugging-evals/` | `#step-0-validate-your-eval-spec` | `#step-1-make-the-eval-valid` |
| | `#step-1-read-the-evidence`, `#step-2-use---verbose`, `#step-3-inspect-trajectories-and-executor-logs` | `#step-3-find-why-the-result-was-unexpected` |
| | `#step-4-re-grade-without-re-running`, `#step-5-preserve-the-workspace` | `#step-4-verify-the-fix` |
| | `#common-failure-patterns` and its four children | `#troubleshoot-by-symptom` |
| | `#debugging-llm-judge-graders`, `#prompt-grader-returns-low-scores`, `#comparison-disagrees-across-position-swap`, `#llm-judge-retries-exhausted` | `#troubleshoot-by-symptom`, `#llm-judge-failures` |
| | `#hermeticity-local-copilot-settings` | **no equivalent section**; nearest is `/get-started/runtime-setup/#sign-in-with-copilot-cli` |
| `/guides/writing-eval-specs/` | `#validate-before-running` | `#run-and-inspect-the-eval` |
| | `#full-structure` | `#expanded-example` |
| | `#environments`, `#root-environment`, `#stimulus-environment`, `#using-named-environments` | `#agent-and-grading-environments`, `#root-agent-environment`, `#stimulus-agent-environment`, `#named-agent-environments` |
| `/guides/writing-custom-graders/` | `#the-grader-interface` | `#interface` |
| | `#reading-files-from-the-run` | `#graderinput-and-run-files` |
| | `#example-a-no-errors-grader` | `#implementation` |
| | `#example-a-tool-count-grader` | removed, no replacement |
| `/guides/writing-custom-executors/` | `#the-executor-interface`, `#implementing-an-executor`, `#executor-config` | `#interface`, `#implementation`, `#configuration` |
| `/guides/writing-custom-reporters/` | `#the-planreporter-interface`, `#implementing-a-reporter` | `#interface`, `#implementation` |
| | `#lifecycle-ordering-and-timing-contract` | `#lifecycle-and-ordering` |
| | `#stable-identifiers-idempotency--at-least-once-delivery` | `#stable-identifiers` |
| `/guides/authoring-eval-suites/` | `#quick-checklist` | removed |
| `/reference/eval-spec/` | `#environment`, `#environment-fields` | `#agent-environment`, `#agent-environment-fields` |
| `/reference/vally-yaml/` | `#environment-fields` | `#agent-environment-fields` |
| `/reference/graders/` | `#at-a-glance` | removed (table is now the page top) |
| `/reference/graders/prompt/` | `#what-workspace-mode-provides` | `#what-the-evidence-files-provide` |
| `/get-started/install/` | `#use-as-a-library`, `#next-steps` | `#optional-use-vally-as-a-library` |
| `/get-started/run-your-first-eval/` | `#what-youll-do`, `#next-steps` | `#what-vally-init-created`, `#what-to-try-next` |

---

## 3. Course link audit (Vally docs links only)

**Scope.** `lessons/*.html`, `reference/*.html`, `index.html`, `RESOURCES.md`. (`GLOSSARY.md`, `MISSION.md`, `NOTES.md`, `index.html` contain no Vally docs links.)

**Result.**

| Check | Count |
|---|---|
| Link occurrences | 132 |
| Distinct URLs | 38 |
| Files containing links | 24 |
| HTTP 200 | 38 of 38 |
| 404 | 0 |
| Redirects | 0 |
| Links with `#anchor` | 0 |
| Anchor missing | 0 |

### Table A: broken links (file → broken URL → fix)

| File | Broken URL | Fix |
|---|---|---|
| (none) | (none) | (none) |

The pattern the owner suspected (moved or renamed docs pages) did not happen. Whatever is broken lies in the non-Vally external links or the internal relative links, which another process is checking.

### Table B: links that resolve but whose cited content changed or moved

These are the ones worth editing. Each "fix" URL and anchor was confirmed present on the live page.

| File:line | Link target | What the course says there | What 0.21 says | Suggested fix |
|---|---|---|---|---|
| `lessons/0010-environments-and-isolation.html:106` | `/guides/debugging-evals/` | Cited for "hermetic `COPILOT_HOME`" | The "Hermeticity: local Copilot settings" section is **deleted**. The page now mentions `EVALUATE_USE_HOST_COPILOT_HOME` only in a "Local and CI results differ" table row. No docs page explains the hermetic default any more. The mechanism still exists in source (`packages/core/src/executor/copilot-home.ts`). | Re-point to `/get-started/runtime-setup/#sign-in-with-copilot-cli` (the caution "Host-home mode exposes persisted Copilot settings to the run") and cite repo source for the default. |
| `reference/cli-cheatsheet.html:221` | `/guides/debugging-evals/` | Source for env vars, including `EVALUATE_USE_HOST_COPILOT_HOME` | Same as above | Add `/get-started/runtime-setup/` as the source for that variable. |
| `lessons/0001-first-run.html:115`, `RESOURCES.md:8` | `/get-started/install/`, `/get-started/` | "Node.js ≥ 22.12" | "Node.js `>=22.15.0`" [/get-started/install/] | Change the number. Link is fine. |
| `lessons/0001-first-run.html:135` | `/get-started/add-to-ci/` | "PAT setup from Add to CI" | Add to CI now leads with the Actions token; the PAT is a "Fallback". Local PAT setup lives on the new page. | Re-point to `/get-started/runtime-setup/#alternative-authenticate-with-a-token`. |
| `lessons/0017-ci-tiers.html:250`, `:316` | `/get-started/add-to-ci/` | "(workflows, PAT permission, …)"; "source for credentials" | Recommended: `permissions: copilot-requests: write` + `GITHUB_TOKEN: ${{ github.token }}`. Fallback PAT is mapped to `GH_TOKEN` **and** `GITHUB_COPILOT_API_TOKEN`. `COPILOT_GITHUB_TOKEN` is gone from this page. | Link is right; rewrite the surrounding workflow and prose. |
| `lessons/0003-reading-trajectories.html:141`, `:222`; `RESOURCES.md:18` | `/guides/debugging-evals/` | "The debug ladder (lint → evidence → verbose → trajectory → re-grade → workspace)"; "common failure signatures, rate-limit relief" | Six steps (0–5) became four: `#step-1-make-the-eval-valid` (run `vally eval`, which validates; lint is no longer step 0), `#step-2-get-the-eval-to-complete` (new: auth and timeout errors), `#step-3-find-why-the-result-was-unexpected` (evidence → `--verbose` → saved records), `#step-4-verify-the-fix` (re-grade, or `--workspace`). Failure signatures are now the `#troubleshoot-by-symptom` table; rate limiting is under `#llm-judge-failures`. | Keep the URL, optionally deep-link `#debugging-workflow`; update the ladder wording. |
| `lessons/0003-reading-trajectories.html:162` | `/reference/cli/grade/` | "`--workspace` only applies to ATIF or Copilot session-log input, not to `results.jsonl`" | Now false. `--workspace` is "Valid for every input format and overrides `trajectory.workDir` on every input record." [/reference/cli/grade/#options] | Rewrite the sentence; optionally deep-link `#offline-re-grading`. |
| `lessons/0002-anatomy-of-eval-yaml.html:243`, `lessons/0010-…:95`, `:303` | `/reference/eval-spec/` | "the Environment … sections" | Section renamed "Agent environment" (`#agent-environment`); `#environment` no longer exists. | Reword; deep-link `#agent-environment` / `#grading-environment` if desired. |
| `lessons/0010-environments-and-isolation.html:249` | `/reference/eval-spec/` | Cited for simulation | Simulation now covers MCP tools, and the "first-party tools only" scope line is gone. See §4. | Link fine (`#simulation` exists); update content. |
| `lessons/0011-llm-judges.html:221`; `lessons/0015-…:61` | `/reference/graders/prompt/` | "(cost formula, judge model resolution)" | Cost formula unchanged (`#cost-considerations`). Resolution chain unchanged but the final default is now `gpt-5.6-terra` (`#judge-model-resolution`). Retry behaviour reversed (`#retry-behavior`). | Link fine; update content. |
| `lessons/0016-comparing-variants.html:84`, `:180` | `/reference/experiment-file/` | Cited for schema | `filter`, `grader_plugins`, `executor_plugins`, `eval_plugin` are **removed** (were "not yet wired"). `baseline` is now wired. | Link fine; update content. |
| `lessons/0018-custom-graders.html:360` | `/guides/writing-custom-graders/` | "(interface, metadata, registration, Vitest)" | The in-process "Register it" step (`createGraderRegistry()` + `registry.register(...)`) is removed from the guide. Plugin registration via `registerGraders` remains under `#shipping-as-a-plugin-package`. | Link fine; drop or re-source the in-process registration claim. |
| `lessons/0019-reporters-and-executors.html:82` | `/guides/writing-custom-reporters/` | "Idempotency key: `event.item.id`, or `trajectory.metadata.sessionID`" | Now contradicted: "Use `event.item.id` as the per-trial idempotency key"; trajectory id and `sessionID` are "executor-owned identifiers for correlation, not trial idempotency. A resumed session may span several trials". [/guides/writing-custom-reporters/#stable-identifiers] | Rewrite; deep-link `#stable-identifiers`. |
| `lessons/0019-reporters-and-executors.html:268`, `:288` | `/guides/writing-custom-executors/` | "handle SIGINT/SIGTERM"; "skim the claude-cli…" | The SIGINT/SIGTERM advice is removed. The docs no longer mention `claude-cli` anywhere, and `plugins/executors/` (claude-cli, cca) is absent from the 0.21 source tree. | Link fine; revise the case study (see §4, Executors). |

Links whose surrounding claims I checked and found still accurate: `/concepts/why-vally/` (MMLU quote), `/reference/graders/prompt/` "reserved for nightly / on-demand" (still in the page's opening aside), `/guides/writing-custom-reporters/` "lists the plugin seams" (still: "the fifth plugin seam, alongside executors, graders, eval providers, and lint reporters"), `/guides/authoring-eval-suites/#suggested-ci-layout` (table intact), `/concepts/scoring/` `runs` guidance 1 / 3 / 5–10 (intact), `RESOURCES.md:14` "36 built-in graders" (still 36).

### Table C: broken links inside the Vally docs site itself (confirmed)

This may be what the owner ran into when clicking through from a course link. The live site ships **32 internal links on 11 pages that omit the `/vally/` base**, e.g. `href="/reference/graders/prompt/#evidence-delivery"`. They resolve to `https://microsoft.github.io/reference/…`, which returns **404** (checked with one request to `https://microsoft.github.io/reference/graders/prompt/`; this is the only fetch made outside the `/vally/` prefix). The source writes them as root-absolute markdown links and Starlight does not rewrite them.

| Live page with broken outbound links | Broken `href` values (as served) | Working equivalent |
|---|---|---|
| `/reference/eval-spec/` | `/reference/graders/prompt/#evidence-options`, `/reference/graders/prompt/#evidence-delivery`, `/reference/trajectory-format/…` | prefix `/vally` |
| `/reference/cli/grade/` | `/reference/graders/prompt/#evidence-delivery` | prefix `/vally` |
| `/reference/cli/compare/` | `/reference/graders/prompt/#evidence-delivery` | prefix `/vally` |
| `/reference/cli/experiment/` | `/reference/cli/eval#parameter-resolution` | `/vally/reference/cli/eval/#parameter-resolution` |
| `/reference/graders/prompt/` | `/get-started/add-to-ci/`, `/reference/cli/compare/#description` | prefix `/vally` |
| `/reference/graders/panel/` | `/reference/graders/prompt/#evidence-options`, `/reference/graders/prompt/#evidence-delivery` | prefix `/vally` |
| `/reference/graders/tool-calls/`, `/reference/graders/system-event/` | `/reference/eval-spec/#subagent-scope`, `/reference/trajectory-format/#system`, `/reference/trajectory-format/#tool_call` | prefix `/vally` |
| `/reference/trajectory-format/` | `/reference/eval-spec/#staging-files`, `/reference/cli/grade/` | prefix `/vally` |
| `/reference/vally-yaml/` | `/reference/eval-spec/#staging-files`, `/reference/experiment-file/#merge-semantics-inside-environment`, others from the shared environment-fields component | prefix `/vally` |
| `/guides/writing-custom-graders/` | `/reference/eval-spec/#staging-files` | prefix `/vally` |

Distinct broken targets seen: `/get-started/add-to-ci/`, `/reference/cli/compare/#description`, `/reference/cli/eval#parameter-resolution`, `/reference/cli/grade/`, `/reference/cli/lint/`, `/reference/eval-spec/#simulation`, `/reference/eval-spec/#staging-files`, `/reference/eval-spec/#subagent-scope`, `/reference/experiment-file/#merge-semantics-inside-environment`, `/reference/graders/custom-metrics/`, `/reference/graders/program/`, `/reference/graders/prompt/` (+ `#evidence-delivery`, `#evidence-options`), `/reference/graders/tool-calls/#parallel-dispatch`, `/reference/trajectory-format/#system`, `/reference/trajectory-format/#tool_call`. The per-page attribution in the table is from the 0.21 source and a grep of the fetched HTML; the exact per-page split of every target was not tabulated.

Consequence for the course: none of its own links are affected, but a learner sent to `/reference/eval-spec/` or `/reference/graders/prompt/` and told to "follow the link to evidence delivery" will hit a 404. Where a lesson depends on such a hop, link the destination directly with the full `https://microsoft.github.io/vally/…` URL. This is an upstream docs bug worth reporting.

One more docs inconsistency to avoid repeating: `/guides/run-your-first-experiment/` says `--compare` "uses the default judge model", while `/reference/cli/experiment/#comparing-variants-after-a-run---compare` says it inherits the evals' judge settings. The reference page matches CHANGELOG 0.19.0.

---

## 4. Content delta by page

Field names, flags and headings are quoted exactly from the 0.21 source.

### Get Started and auth

**`/get-started/` (rewritten).** The card grid is replaced by a three-step `<Steps>` list: Install Vally → Set up the default runtime → Run your first eval. "Add to CI" is no longer one of the three steps. Prerequisites now read: Node.js `>=22.15.0`, and "A GitHub account with an active Copilot subscription for Vally's default runtime."

**`/get-started/install/`.** Node `>=22.15.0` (was `>= 22.12.0`). All three packages declare `engines.node >=22.15.0` at 0.21.0. Note the changelog only records the 0.18.0 bump to 22.14.0 [CHANGELOG 0.18.0]; the further move to 22.15.0 is not called out in any release note. "Use as a library" is retitled "Optional: Use Vally as a library". Package table unchanged.

**`/get-started/runtime-setup/` (NEW). Closes digest gap k#1.**
- "Vally uses the built-in `copilot-sdk` executor by default. The quickest local setup is to reuse a Copilot CLI login."
- `## Sign in with Copilot CLI`: `npm install -g @github/copilot`, run `copilot`, enter `/login`, then `export EVALUATE_USE_HOST_COPILOT_HOME=1` (PowerShell: `$env:EVALUATE_USE_HOST_COPILOT_HOME = "1"`).
- Caution: "Host-home mode exposes persisted Copilot settings to the run. Prefer token authentication when evals need a reproducible runtime configuration."
- `## Alternative: Authenticate with a token`: fine-grained PAT with "**Account permissions > Copilot Requests**", exposed as `COPILOT_GITHUB_TOKEN`. "This token authenticates both the default executor and LLM judge features such as `prompt`, `panel`, `vally compare`, and experiment `--compare`."
- **Inconsistency to flag in the course:** this page says one `COPILOT_GITHUB_TOKEN` covers executor and judges; Add to CI says "the default executor reads `GH_TOKEN`, while LLM judges read `GITHUB_COPILOT_API_TOKEN`" and maps the secret twice. The docs do not reconcile these. UNCONFIRMED which chain is authoritative; verify against `copilot-sdk-executor.ts` and `llm-client.ts` at 0.21.

**`/get-started/run-your-first-eval/` (rewritten).**
- Now "the third and final step". The "requires a working Copilot SDK setup" note is replaced by a link back to Runtime Setup.
- The separate **"Validate it" (`vally lint`) step is removed**: "`vally eval` validates the spec before running the agent."
- Sample console output is the new compact form:
  ```
  Summary
    hello  ✓ 1/1 (score 100% ≥ 100%)

  Saved  ./results/<timestamp>/
  ```
  The old per-stimulus Metrics / Graders / Agent Output blocks are gone from the default output.
- "At completion, unweighted evals show `PASS`, `FAIL`, or `FLAKY`. Weighted evals instead show how many stimuli passed and whether the score met the threshold."
- The starter `eval.yaml` is unchanged (still `file-exists` 0.34 / `file-matches` 0.66, `threshold: 1.0`), now under `## What vally init created`.
- Re-grading moved from step 4 to `## Optional: Re-grade saved trajectories`.
- New `## What to try next` routing table (Choose a grader, multi-turn, experiment, CI, scoring, debugging, dashboard).

**`/get-started/add-to-ci/`.**
- Framing changed from "every PR gets checked" to "linting to every PR and behavioral evaluation to trusted changes".
- Both workflows add `check-latest: true` under `actions/setup-node`, and use `evals/hello/eval.yaml` instead of a root `eval.yaml`.
- **Recommended auth: "GitHub Actions token"**: (1) org owner enables "**Allow use of Copilot CLI billed to the organization**"; (2) `permissions: contents: read` and `copilot-requests: write`; (3) `env: GITHUB_TOKEN: ${{ github.token }}`. "The built-in token is short-lived, authenticates both the default `copilot-sdk` executor and LLM judges, and does not require a repository secret." This reverses the 0.16 statement that `secrets.GITHUB_TOKEN` cannot access Copilot.
- The eval workflow adds `push: branches: [main]` and `workflow_dispatch` triggers, and a job-level `if:` that skips fork PRs. New caution: "Never use `pull_request_target` to execute untrusted fork code with write permissions or secrets."
- **"Fallback: Fine-grained personal access token"**: secret named `COPILOT_CLI_TOKEN`, mapped as `GH_TOKEN` and `GITHUB_COPILOT_API_TOKEN`.
- **Removed:** the executor/credential table, the `claude-cli` row, `ANTHROPIC_API_KEY`, and `COPILOT_GITHUB_TOKEN` in the workflow.
- Exit-code and suite sections unchanged.

### Concepts

**`/concepts/scoring/`. Weights and thresholds are still fully documented** (`#weights`, `#thresholds`, `#what-to-configure`, `#grader-thresholds`); the recommendation not to threshold pass/fail assertions is intact. Changes:
- **No-grader evals now pass.** Old: an all-unscored eval "scores 0% and fails when a threshold is set". New: "An eval whose stimuli run successfully without any graders passes vacuously, even with a threshold configured: threshold scoring is skipped and no overall score is reported. This also satisfies `--require-pass`". [/concepts/scoring/#eval-verdict; CHANGELOG 0.20.0]
- Console no longer prints the per-trial glyph row (`✔ ✘ ✔ ✔`). It prints aggregate counts and a state word, e.g. `FLAKY  my-eval · 4 trials each`. Flakiness is "`FLAKY` in the console, 🟡 in markdown reports".
- "`pass@k` and `pass^k` appear in saved markdown reports rather than the console; they are also available in JUnit output."
- Weighted evals show e.g. `my-eval  ✓ 0/1 (score 87.5% ≥ 80%)`.

**`/concepts/how-it-works/`.** Adds the agent/grading environment split, and one new paragraph: "The executor runs the agent; the backend controls where the trial runs—for example, locally or in Docker." Executor bullet "Setting up the workspace" became "Running the agent in the provided workspace".

**`/concepts/grader-taxonomy/`, `/concepts/why-vally/`.** No substantive change (taxonomy example uses `judge_model: gpt-5.6-terra`).

### Eval spec reference (`/reference/eval-spec/`)

- **Top-level `name` is now Required: "Yes"** (was "No"). The minimal example in the guide gained `name: hello-world`. UNCONFIRMED whether a missing `name` is a hard load error or only a docs correction; test with `vally lint` before telling learners.
- **Unknown stimulus fields are rejected**: "Fields not listed above are rejected when the eval spec is loaded." [CHANGELOG 0.17.0, Breaking]
- **New `defaults` fields:**
  - `judge_timeout` (duration, default `2m`): "Timeout for each `prompt` or `panel` judge turn."
  - `backend`: a name (`local`, `docker`, or a plugin backend) or `{ name, args }`. New section `## Backend selection`: "Selection precedence is CLI arguments, eval spec, then `.vally.yaml`." An explicit `--backend` "discards project backend arguments, but preserves eval arguments when the selected backend matches".
  - `exporter` (object[]): per-exporter default `args`; new section `## Exporter defaults`.
- **Default judge example** is `judge_model: gpt-5.6-terra`.
- **Reasoning effort** (`reasoning_effort`, `judge_reasoning_effort`) is no longer the fixed enum `low|medium|high|xhigh`: "Common values include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`; accepted values depend on the model." Blank values are rejected.
- **New `### Copilot Fusion`**: `model: auto` with `executor.config.autoTier: hydrafusion` (or `hydrafusion-max`).
- **New stimulus field `golden_command`** (non-empty string): a shell command oracle runs in the materialized workspace, after `golden_patch` and before `golden_custom_metrics`. Must exit 0 within five minutes. Output is discarded. `--no-golden-input` withholds it. Section `### Golden command`.
- **New grader-entry field `oracle_baseline: allow-pass`**: "Only applies to `vally oracle --no-golden-input`: allow this grader to pass (reported as N/A)."
- **Environment section renamed `## Agent environment`**; all examples use `agent_environment` (closes digest gap k#2 for this page). `environment` remains a deprecated alias; setting both at one level is an `eval-load-error`.
- **`grading_environment`**: explicitly "has no `skills`, `commands`, `git`, `mcpServers`, or `env` fields"; `dest` must be relative without `..`.
- **LLM judge evidence**: `output_delivery` removed from the example. "Both `prompt` and `panel` automatically copy selected evidence to temporary files outside the agent's working directory." `repo` evidence takes settings on a `source: repo` entry, plus `config.evidence_read_budget`.
- **Empty scope behaviour changed**: old "the grader fails loud"; new "most graders report an error. Absence checks are the exception: `tool-calls` with only `disallowed: [edit]` passes". [CHANGELOG 0.19.0]
- **Simulation**:
  - **MCP tools can be simulated** (old: "MCP server tools are not simulated"). Key is "the exact runtime name: `<server-name>-<tool-name>`".
  - New override field `structured_output` (MCP only; required when the tool declares an `outputSchema`).
  - Pattern rules gain `args` (named-argument regexes) and `pattern` (regex on `JSON.stringify(arguments)`) beside `match`.
  - Clarified: "Calls that do not match an override still run the real tool, so provide a `default` when an overridden tool must never cause real side effects."
- **`scoring.timeout`** (duration): "Shared wall-clock budget for the complete grading phase of one trial." [CHANGELOG 0.19.0]
- Environment fields: `copilot-sdk` "supports MCP sampling … automatically"; the `claude-cli`/`cca` mention in the `env` paragraph is replaced by "custom process-spawning executors"; all Harbor-specific git paragraphs are removed from this component.

### Guide: Writing Eval Specs (`/guides/writing-eval-specs/`)

- "Validate before running" section removed; replaced by `## Run and inspect the eval` (run `vally eval`; it validates).
- `## Full structure` → `## Expanded example`, now explicitly "not an exhaustive schema".
- New `### Grader-only files` section with a `grading_environment` + `run-command` hidden-test example.
- "Named environments apply only to `agent_environment`; `grading_environment` is always declared inline".
- New constraints guidance: "Use `max_duration` when exceeding the limit should fail the trial. Use `max_agent_duration` when Vally should stop the agent cleanly and grade its partial work." Effective hard cap order: "`--timeout` when supplied, otherwise `max_duration`, then `defaults.timeout`."

### Grader catalog and grader pages

**Count and names: unchanged, 36.** `assistant-contains-tool-output`, `completed`, `custom-metrics`, `diff-contains`, `diff-not-contains`, `diff-empty`, `error-count`, `exit-success`, `file-contains`, `file-exists`, `file-matches`, `file-not-contains`, `file-not-exists`, `file-not-matches`, `loop-outcome`, `max-repeat`, `output-contains`, `output-matches`, `output-not-contains`, `output-not-matches`, `panel`, `program`, `prompt`, `run-command`, `skill-invocation`, `system-event`, `step-count`, `token-budget`, `tool-call-count`, `tool-calls`, `transcript-contains`, `transcript-matches`, `transcript-not-contains`, `transcript-not-matches`, `turn-count`, `wall-time`. [/reference/graders/] The "All graders are **reference-free**" line is still there (digest gap k#4 stands).

**`/reference/graders/prompt/` (heavy).**
- Default `model`: `gpt-5.6-terra` (was `claude-sonnet-4.6`). [CHANGELOG 0.17.0, Breaking]
- `output_delivery` field removed from the config table. "`output_delivery: workspace` still works but produces a deprecation warning; `output_delivery: inline` is rejected because inline delivery is no longer supported." Evidence is always delivered as temp files the judge reads with `grep`/`view`. [CHANGELOG 0.17.0, Breaking]
- Old inline caps (50,000-character output, 20,000-character diffs, head/tail timeline windowing) are gone: "Selected captured output, events, metrics, and patches are copied in full".
- New `config.evidence_read_budget`: `max_tool_calls` (default 12, range 1–500), `max_result_chars` (16000), `max_total_chars` (64000). [CHANGELOG 0.21.0]
- New `source: repo` evidence options: `max_files` (1000), `max_file_bytes` (32000), `max_total_bytes` (262144), `include`, `exclude`.
- New `## Authentication`: "LLM judges use a separate Copilot client from the agent being evaluated… Credentials configured only for the evaluated agent or its provider do not automatically configure the judge."
- New `## Timeout`: `defaults.judge_timeout` / `vally eval --judge-timeout`, default `2m`. [CHANGELOG 0.20.0]
- **`## Retry behavior` reversed.** Old: up to 2 retries, 5s → 10s → 20s backoff, 10-minute budget. New: "In ordinary grading, a failed LLM call produces a **failed result** (score 0) with the error in evidence; the prompt grader does not retry the failed call." Retries now exist only in comparison mode, and only for errors explicitly marked retryable. [CHANGELOG 0.20.0]
- Reasoning effort is validated against the Copilot model catalog: unknown model IDs and catalog lookup failures "stop the call before session creation"; BYOK providers are exempt.
- Warning that file-based evidence "may change latency, token usage, and judgments compared with past versions". Relevant to anyone who calibrated a judge on 0.16.
- Comparison mode now also ignores `repo` evidence.
- Unchanged: `scoring` scales, `threshold` default `0.5`, rubric-from-stimulus rule, `submit_grade` tool, cost formula, model resolution order.

**`/reference/graders/panel/`.** Example models now lead with `gpt-5.6-terra`. New `## Timeout` and `## Evidence delivery` sections; each judge gets its own `evidence_read_budget`. "Panel graders support only inline delivery" is gone (panels now use file delivery too). "Any judge failure makes the panel fail" unchanged.

**`/reference/graders/tool-calls/`.** New: with an empty selected scope, a `disallowed`-only grader passes; non-empty `required`/`sequence`/`parallel` errors. ATIF integrations can scope by instance id.

**`/reference/graders/metric-thresholds/`.** Model-routing events (`model_set`, `model_change`, `auto_mode_configured`, `auto_mode_resolved`, `fusion_resolved`) "do not count as steps".

**`/reference/graders/diff-contains/`, `/diff-empty/`.** New paragraph on `--workspace <path> --in-place`: uses the checkout's starting HEAD, requires a clean Git checkout, whole-run diffs only.

**`/reference/graders/program/`, `/run-command/`.** `timeout` must be "no longer than ~24.8 days". `program`: `GraderInput.signal`, `timeoutMs`, `judgeTimeoutMs` are omitted from the JSON payload.

### CLI reference

**New command: `vally simulate record <input> [--output <path>] [--mcp-server <name>]...`** [/reference/cli/simulate/; CHANGELOG 0.18.0]
- `<input>`: a Vally trajectory JSON, ATIF JSON, a `results.jsonl`, a directory containing one, or `-`.
- Flags: `--output, -o <path>`; `--mcp-server <name>` (repeatable).
- Output is a top-level `simulation:` block to paste under a stimulus. Overrides "match on **exact** recorded arguments and have no `default`", so unmatched calls hit the real tool: "a recorded starting point, not a fully offline sandbox".
- Successful non-shell, non-MCP calls are omitted with a warning. Duplicate argument tuples with different results keep the first.

**`vally eval`** [/reference/cli/eval/]
- New flags: `--in-place` (with `--workspace`; section `### Run in an existing directory`), `--judge-timeout <duration>` (default `2m`, "Bounded by the remaining `scoring.timeout`"), `--run-id <id>` (default generated UUID).
- `--backend` default is now "Eval/project backend or `local`"; built-ins are `local` or `docker`.
- `--workspace` redefined: "Root for preserved trial workspaces, or the exact existing directory used for execution with `--in-place`."
- `--in-place`: one worker, no retries, local backend only; forbids `agent_environment.git`/`files`/`skills`/`commands` and `grading_environment.files`. "This is **not a sandbox**."
- Plugin flags are "additive with project `plugins.*`"; `--eval-plugin` *replaces* project eval-provider config.
- Exit codes: "Terminal output labels execution errors and invalid trial grades as `ERROR`, while valid failing verdicts are labeled `FAIL`." "Non-blocking grader errors are reported as warnings: the aggregate verdict remains valid, but the command still exits `1`". [CHANGELOG 0.20.0, 0.21.0]
- `--verbose` on multi-trial runs shows agent output "only for failing trials"; nested evidence is capped at 4,096 characters / 40 lines.
- Workspace caching is additionally skipped for environments that stage any file with `dest_root: assets`.
- The `--executor-plugin @microsoft/vally-executor-claude-cli` OTLP example is removed.
- Skills-loading rules unchanged, reworded to `agent_environment.skills`.

**`vally grade`** [/reference/cli/grade/]
- New flags: `--backend`, `--backend-args`, `--run-id`. [CHANGELOG 0.17.0, 0.18.0]
- `--workspace` now applies to every input format (see §3 Table B).
- New exit codes `130` (SIGINT) and `143` (SIGTERM).
- Judge evidence under re-grade is copied to temp files and deleted; "it does not save them for future re-grading".

**`vally oracle`** [/reference/cli/oracle/]
- New flags: `--run-id`, `--diff-output <path>`.
- New section `## Golden command (running a reference script)`.
- **Metric-threshold graders on the baseline reversed.** Old: a `max:`-only threshold is "**trivially passing**" (exit 1). New: "a max-only threshold is an absence assertion and is reported **N/A**".
- N/A list widened to include `system-event` with only `disallowed:`, "negated output and file graders", `diff-not-contains`, `diff-empty`. So `file-not-exists` moved from "trivially passing" to N/A; the page's trivially-passing example is now `output-matches /^$/`.
- "With `--no-golden-input`, output and trajectory graders—including those with `turn`, `scope`, or both—run against the empty baseline." (0.16 rejected turn- and agent-scoped graders there.)
- Any grader can opt in with `oracle_baseline: allow-pass`. [CHANGELOG 0.21.0]

**`vally compare`** [/reference/cli/compare/]
- New flag `--judge-timeout <duration>` (default `2m`, per judge turn).
- "Standalone `compare` does not inherit judge settings from `--eval-spec` or saved output."
- Retries: only errors whose top-level `retryable` is true are retried; "Unmarked failures from other clients or graders are terminal."
- Evidence is file-based; new warning codes `VALLY_JUDGE_WORKSPACE_CLEANUP_PENDING`, `VALLY_JUDGE_WORKSPACE_CLEANUP_FAILED`.

**`vally experiment`** [/reference/cli/experiment/]
- `run` new flags: `--otlp-endpoint`, `--grader-plugin`, `--executor-plugin`, `--eval-plugin`, and (requiring `--compare`) `--judge-model`, `--judge-timeout`, `--judge-reasoning-effort`.
- `--run-id` is now accepted for unsharded runs (default generated UUID).
- **`--compare` no longer always uses the default judge**: it "inherits `judge_model`, `judge_reasoning_effort`, `judge_provider`, and `judge_timeout` from the selected evals". Conflicting settings across evals make the comparison exit `1`. [CHANGELOG 0.19.0]
- Console comparison is omitted when the baseline was not run or variants saw different stimuli; sharded runs are labelled partial.
- Output adds `otel-spans.jsonl` and `otel-context.json`. `merge` gains `--otlp-endpoint`. [CHANGELOG 0.20.0]
- New caution: "Merge does not compare plugin sources, versions, or configuration across shards."
- The "new in 0.6.0 / not yet wired" note is deleted.

**`vally lint`** [/reference/cli/lint/#eval-spec-checks]
- New error codes: `eval-load-error`, `undefined-param` (now listed in the table), `grading-file-dest-unconfined`, `grading-file-dest-overlap`, `grading-file-src-agent-visible` (now in the table).
- Named `agent_environment` references are not checked for missing files or source overlap.
- Warning codes unchanged. Still no glob/suite option (digest gap k#25 stands).

**`vally export`.** Eval-spec `defaults.exporter` supplies defaults; `--exporter` is still required. Example names `@microsoft/vally-exporter-harbor`.

**`vally serve` / `vally ingest`.** New `## SQLite troubleshooting`: both "use Node's built-in SQLite unless the optional `better-sqlite3` package is installed". Programmatic API: `openDatabase()` from `@microsoft/vally-server`. [CHANGELOG 0.18.0]

**`vally init`.** Starter template comment now says `agent_environment`.

### Backends and Docker (`/guides/running-evals-in-docker/`, NEW)

- `vally eval --backend docker --eval-spec eval.yaml`. Also `vally grade --backend docker` and `vally experiment run … --backend docker`. [CHANGELOG 0.18.0]
- Two container roles: a **task** project runs the agent; a separate **grade** project runs graders. "The agent does not receive hidden grader inputs or judge credentials, and grading cannot change the workspace exported after the trial."
- Default image is built locally and cached as `vally-task:<content-hash>`; "An uncached build needs network access." [CHANGELOG 0.20.0]
- Backend args (`--backend-args key=value` or `defaults.backend.args`): `task-image`, `grade-image`, `task-network`, `grade-network`, `task-env`, `grade-env`, `compose-file`, `resources`. [CHANGELOG 0.21.0 for per-eval images and `resources`]
- "Forward grade credentials with `grade-env`, not `task-env`."
- Image requirements: Linux, non-root `USER`, "the exact host version of `@microsoft/vally`, including `vally-docker-runner`", POSIX `sh`; grade image needs GNU coreutils and Git.
- Plugins must be packages or package directories (no single files); npm install inside the image "does not inherit your host npm configuration, authentication, or proxy variables".
- Cost framing: "Docker adds image and daemon setup overhead; use the default local backend when you don't need container isolation."

### `.vally.yaml` reference (`/reference/vally-yaml/`)

- **New `## plugins`**: keys `grader`, `executor`, `reporter`, `eval_provider`, `backend` (additive lists; local paths relative to `.vally.yaml`). Table of which commands use which: `eval` and `experiment run` use all five; `grade` uses `grader`, `backend`; `oracle`, `lint`, `export` use `grader`. [CHANGELOG 0.19.0]
- **New root `defaults`**: `eval_provider`, and `backend` as `{ name, args }`.
- **New `### Metadata`**: root `metadata` and per-suite `metadata`, "passive, JSON-compatible defaults to integrations such as reporter plugins". Suite metadata is shallow-merged over root. Surfaced as `PlanRunStartContext.metadata` and `.suite`. "Do not store secrets in metadata." [CHANGELOG 0.17.0]
- **New `### Path casing`**: the blanket "matching is case-sensitive on every platform" is replaced by "Paths written in suite or experiment `evals` patterns and `--eval-filter` must match on-disk casing. The project or experiment directory used to resolve relative patterns follows the filesystem's casing rules."
- `environments` are explicitly "Named **agent environments**"; grader-only files "cannot use a named reference".
- Still not documented here: `params:` (digest gap k#14 stands; only mentioned in `/reference/cli/eval/#parameter-resolution`).

### Experiment file (`/reference/experiment-file/`)

- **Removed fields:** `filter` (rejected since 0.18.0), `grader_plugins`, `executor_plugins`, `eval_plugin` (moved to `.vally.yaml` in 0.19.0). Both are listed as Breaking in the changelog.
- `baseline` is now "used as the control by `--compare` and experiment-mode `vally compare`" (closes digest gap k#15).
- Overridable `overrides` fields add `backend` and `judge_timeout`.
- `/environment` in `vary` is explained as "the internal `/environment` path for the resolved **agent environment**"; `grading_environment` is not overridable.
- New `### Variant names and output directories` (sanitized names can collide; prefer lowercase letters, numbers, `.`, `_`, `-`).
- New `### Copilot Fusion` example varying `/defaults/model` and `/defaults/executor`.
- Examples use `gpt-5.6-terra` in place of `claude-sonnet-4.6`.

### Extension guides

**Custom graders (`/guides/writing-custom-graders/`).**
- Reordered: `## Interface` → `## Implementation` → `## GraderInput and run files` → `## Optional capabilities`. `Grader` and `GraderMetadata` signatures unchanged.
- **`GraderInput` is now printed in full**, with new fields: `diffBaseDir`, `goldenPatch`, `signal?: AbortSignal`, `timeoutMs`, `judgeTimeoutMs`. "Every field is optional in the public contract". `signal` "fires when the stimulus's `scoring.timeout` budget expires. Enforcement is cooperative".
- Example grader now validates config (`parseConfig`, `ignoredTypes`) and implements `assertsAbsence()`.
- **In-process "Register it" step removed** (`createGraderRegistry()`); the tool-count example is removed.
- `compare()` clarified: "The current `vally compare` command constructs the built-in `prompt` grader directly. It does not provide a plugin-driven way to select a custom comparison grader."
- `defaultName` example uses `describeGraderList` (was `describeGraderValue`).
- Packaging: the stale `peerDependencies: "^0.2.0"` JSON is replaced by `npm pkg set type=module main=dist/index.js exports=./dist/index.js` and `npm install --save-peer @microsoft/vally` (closes digest gap k#6 for all three guides).
- New "How plugin specifiers resolve" note: for `vally eval`, local paths resolve from the first `--eval-spec` file's directory.
- Breaking for aggregate graders: `withRolledUpGraderError()` removed; use `hasGraderError()`. [CHANGELOG 0.20.0; not in the guide]

**Custom executors (`/guides/writing-custom-executors/`).**
- New capability flags: `supportsSimulation`, `supportsMcpSimulation`, `supportsAttachments`.
- `ExecutorOptions` additions: `maxAgentDurationMs`, `registerCleanup`, `traceContext` (`ExecutorTraceContext { traceparent, tracestate }`). `reasoningEffort` is now `string`.
- New `### Retryable failures`: "Mark retryable failures before throwing… Vally reads only the `retryable` boolean on the error you throw." This is a **Breaking** change in 0.20.0: retries are no longer inferred from messages.
- New `### Per-attempt resources needed by graders` (`options.registerCleanup`; 30-second callback deadline; `executor-cleanup-failed` warnings). [CHANGELOG 0.18.0]
- Backend contract: `cleanup(options?: { preserveWorkspace?: boolean })`; "cleanup is no longer skipped after failed egress". [CHANGELOG 0.18.0, Breaking]
- `metadata.modelDisplayName` is an optional presentation label.
- Lifecycle: `shutdown()` is called for "every executor loaded from a plugin", even if never selected. The SIGINT/SIGTERM handler advice is removed.
- Positioning sharpened: "Use a backend, not an executor, to move execution into containers or remote environments."
- **`claude-cli` and `cca`.** No docs page mentions either any more, and `plugins/executors/` (which held `vally-executor-claude-cli` and `vally-executor-cca` at 0.16) is absent from the 0.21 source tree. The 0.17–0.21 changelog does not announce a removal. UNCONFIRMED whether `@microsoft/vally-executor-claude-cli` is still published or was moved to another repo; check npm before keeping the lesson 19 case study.
- Tracing API rename: `configureTelemetry()` → `configureTracing()`, `ExecutorTelemetryConfig` → `TracingConfig`. [CHANGELOG 0.17.0, Breaking; not in the guide]

**Custom reporters (`/guides/writing-custom-reporters/`).**
- Restructured so a minimal reporter comes first; the contracts moved under `## Production considerations`.
- `PlanRunStartContext` adds `runId?`, `metadata?`, `suite?: { name, metadata? }`.
- `TrialResult.status` adds `"skipped"`; new fields `skipReason?`, `workspacePath?`.
- `summary.hadGradingErrors` documented beside `summary.hadExecutionErrors`.
- Idempotency guidance changed (see §3 Table B). The example now computes `passed` as `status === "success" && (grade?.passed ?? true)`.
- `onRunComplete` now "fires exactly once after the final delivered trial, including failed and cancelled runs" for plugin reporters.

### Debugging guide (`/guides/debugging-evals/`)

Rewritten as a four-step workflow plus a symptom table (structure in §3 Table B). New content:
- Step 2 error table: `Session was not created with authentication…` → Runtime Setup; `Trial execution error: … timed out …` → `--verbose`, then raise the cap.
- `--verbose` on multi-trial runs shows agent output only for failing trials: "inspect `results.jsonl` for passing-trial output".
- Step 4 principle: "Avoid another agent run when the trajectory already contains the evidence your revised graders need."
- `### LLM judge failures`: "Ordinary prompt grading reports a failed LLM call without retrying it." Comparison JSONL records `failure.errorClass`, `failure.retryable`, `failure.attempts`, `failure.message`.
- **Removed:** the hermeticity section; the `logSource` explanation (`"native"` / `"raw-event-fallback"` / `"none"`), which now lives only at `/reference/cli/eval/#trajectory-output`; the `--skip-grade --output jsonl > outcomes.jsonl` tip; the pass@k interpretation bullets.

### Trajectory format (`/reference/trajectory-format/`)

- New `### ATIF tool evidence`: `fromAtif` / `validateAtifTrajectory`, options `toolResultStatus: "require-explicit"` and `subagentIdentity: "instance"`, and the `extra["microsoft.vally"].tool_call_result` convention. [CHANGELOG 0.17.0]
- `Trajectory.diffError?: string`: a failed diff capture is preserved and "a diff grader reports it as an error rather than treating the missing evidence as an empty diff".
- `tool_call` events gain optional `endTimestamp`. [CHANGELOG 0.21.0]
- Failed `tool_result` events "may omit `result` and include an `error` object" (`message` required, `code` optional). [CHANGELOG 0.20.0]
- New `system` event types: `auto_mode_configured`, `auto_mode_resolved`, `fusion_resolved`.
- `TrajectoryMetadata.modelDisplayName?`.
- Machine-readable records carry a top-level `runId` on `trial-result` and `run-summary`. [CHANGELOG 0.18.0]

### Changelog and migration

- **Changelog: yes**, at `/release-notes/<version>/` (closes the first half of digest gap k#12).
- **Migration guide: no page.** The Breaking entries to carry into the course, 0.17 → 0.21:
  - 0.17.0: unknown stimulus fields rejected; `output_delivery: inline` rejected; tracing API rename; default judge → `gpt-5.6-terra`.
  - 0.18.0: experiment `filter` removed; `cleanup({ preserveWorkspace })` contract; Node `>=22.14.0`.
  - 0.19.0: experiment plugin fields removed, move to `.vally.yaml`.
  - 0.20.0: errors must set `retryable: true`; `withRolledUpGraderError()` removed.
  - 0.21.0: no Breaking section.

### New best-practice guidance about eval design

- **Choose a Grader** [/guides/choosing-graders/]: "Start with the evidence that proves the behavior. Prefer a deterministic grader when the requirement can be expressed exactly; use an LLM judge only for qualities that code cannot reliably decide." Selection order: (1) check the final artifact, (2) check the path taken only when it matters, (3) add budgets, (4) use a program for domain logic, (5) use an LLM judge for subjective quality. Tip: "Combine checks that prove different things." `prompt` vs `panel`: "Start with `prompt`. Use `panel` when one judge is too inconsistent and the extra calls justify the cost."
- **Hidden tests** [/guides/writing-eval-specs/#grader-only-files]: stage answer keys via `grading_environment` into `.vally-grading/`, run them with `run-command`.
- **Simulation safety** [/reference/eval-spec/#simulation]: give an overridden tool a `default` if it must never run for real.
- **Fork PRs** [/get-started/add-to-ci/]: skip pre-merge evals on forks, run after merge; never `pull_request_target`.
- **Regression gating** [/guides/run-your-first-experiment/]: `--require-pass` gates each variant's verdict; `--compare` only reports; gate with `vally compare <dir> --fail-on-regression`.
- **Re-grade before re-run** [/guides/debugging-evals/#step-4-verify-the-fix].
- **Reproducibility vs convenience** [/get-started/runtime-setup/]: host-home login is quick; token auth is reproducible.

### Digest gaps (section k) now closed or changed

| Digest gap | Status at 0.21 |
|---|---|
| k#1 local auth undocumented | **Closed** by `/get-started/runtime-setup/` |
| k#2 `environment` vs `agent_environment` inconsistent | **Mostly closed**; experiment files still use `environment` / `/environment`, now explained |
| k#6 stale plugin peerDependency versions | **Closed** (version literals removed) |
| k#8 undocumented seams | Partly: backends now have a user guide and `.vally.yaml` `plugins.backend`, still no interface page; exporters still no interface page |
| k#9 executors `claude-cli`/`cca` | **Changed**: no longer mentioned at all |
| k#12 no changelog | **Closed** (release notes); still no migration guide |
| k#15 experiment `baseline` wiring | **Closed** |
| k#18 `output-contains` default `case_sensitive: false` | Unchanged |
| k#3, k#4, k#5, k#13, k#14, k#25 | Unchanged |

---

## 5. Brand-new docs the course does not cover

| New doc | Why it matters | Course part |
|---|---|---|
| **Runtime Setup** `/get-started/runtime-setup/` | The official local-auth path. Lesson 1 currently derives auth from repo source; it should now teach the two documented options and the `EVALUATE_USE_HOST_COPILOT_HOME=1` trade-off (convenient, not hermetic). | **Foundations** (lesson 1), with a callback in Eval design craft (lesson 10, isolation) |
| **Choose a Grader** `/guides/choosing-graders/` | First official grader-selection guidance: evidence-first, five-step order, `prompt` vs `panel`. Aligns with the course's "deterministic first" stance and gives it an official citation. | **Eval design craft** (lesson 7), and **Judges & statistics** (lesson 11) for `prompt` vs `panel` |
| **`vally simulate record`** `/reference/cli/simulate/` + MCP simulation in `/reference/eval-spec/#simulation` | Record-and-replay for tool responses, and simulating MCP tools with `structured_output`. Changes what is practical for deterministic, side-effect-free stimuli. | **Eval design craft** (lesson 10); mention in **Efficiency & CI** (lesson 15) as a cost lever |
| **Running Evals in Docker** `/guides/running-evals-in-docker/` | A built-in isolated backend with a task/grade credential boundary. The strongest isolation story the docs now offer. | **Eval design craft** (lesson 10, isolation) and **Efficiency & CI** (lesson 17, as an optional CI tier) |
| **Run Your First Experiment** `/guides/run-your-first-experiment/` | Official walkthrough for the lesson 16 workflow, including `--dry-run` and the "`--compare` reports, `compare --fail-on-regression` gates" rule. | **Efficiency & CI** (lesson 16) |
| **Release notes** `/release-notes/<version>/` | The upgrade source of truth; Breaking sections per release. A team needs a habit of reading them before bumping. | **Rollout** (lesson 20); add to `RESOURCES.md` |
| **`.vally.yaml` `plugins`, `defaults`, `metadata`** `/reference/vally-yaml/#plugins`, `#metadata` | Project-wide plugin registration replaces per-command `--*-plugin` flags, and metadata flows to reporters. This is how a team should wire custom graders and reporters. | **Extending Vally** (lessons 18–19) and **Rollout** (lesson 20) |
| **`eval --workspace <path> --in-place`** `/reference/cli/eval/#run-in-an-existing-directory` | Run in an existing checkout for large repos; explicitly "not a sandbox". A sharp trade-off worth one callout. | **Efficiency & CI** (lesson 15) |
| **`golden_command` and `oracle_baseline: allow-pass`** `/reference/eval-spec/#golden-command`, `/reference/cli/oracle/#baseline-negative-control` | Extends oracle to workflows a patch cannot reproduce, and changes how the negative control classifies budget and negated graders. Lesson 15's oracle material is now partly wrong. | **Efficiency & CI** (lesson 15) |
| **Judge evidence model: file delivery, `evidence_read_budget`, `judge_timeout`, no retries** `/reference/graders/prompt/#evidence-delivery`, `#evidence-read-budget`, `#timeout`, `#retry-behavior` | The judge now searches files under a read budget instead of reading a pasted prompt. A judge calibrated on 0.16 should be re-checked; a judge that misses evidence may be budget-limited. | **Judges & statistics** (lessons 11–12) |
| **`scoring.timeout`** `/reference/eval-spec/#scoring` | One wall-clock budget for the whole grading phase; custom graders must honour `GraderInput.signal`. | **Judges & statistics** (lesson 13 or the YAML cheatsheet), **Extending Vally** (lesson 18) |
| **Executor contract additions: `retryable`, `registerCleanup`, capability flags** `/guides/writing-custom-executors/#retryable-failures`, `#per-attempt-resources-needed-by-graders` | A 0.16-era custom executor silently loses retries on 0.20+. | **Extending Vally** (lesson 19) |
| **Actions-token CI auth and fork-PR policy** `/get-started/add-to-ci/` | Replaces the PAT-secret workflow the course teaches. | **Efficiency & CI** (lesson 17), **Rollout** (lesson 20) |
| **Copilot Fusion** `/reference/eval-spec/#copilot-fusion`, `/reference/experiment-file/#copilot-fusion` | `model: auto` with `autoTier`. Niche. | Optional one-line mention in **Efficiency & CI** (lesson 16) |

### Unconfirmed items, collected

- Whether a missing top-level `name` is rejected at load, or the "Required: Yes" cell is only a docs correction.
- Which token chain is authoritative for the executor and for judges (`COPILOT_GITHUB_TOKEN` vs `GH_TOKEN` / `GITHUB_COPILOT_API_TOKEN` / `GITHUB_TOKEN`); the two docs pages disagree.
- Whether `@microsoft/vally-executor-claude-cli` and `-cca` are still published; they are gone from the 0.21 source tree and docs without a changelog entry.
- The exact per-page list of base-less links in §3 Table C (the total of 32 across 11 pages and the 404 are confirmed; the page-by-page split is approximate).
- Which release raised the Node floor from 22.14.0 to 22.15.0 (not in any release note).
