// A Vally executor that runs the release app for each trial
// and turns what the agent did into a Vally trajectory.
// Loaded by the `plugins` list in .vally.yaml.
import { mkdirSync } from "node:fs";
import path from "node:path";
import { randomUUID } from "node:crypto";
import { computeMetrics } from "@microsoft/vally";
import { writeEntries } from "./release-assistant.mjs";

// Copilot SDK session events -> Vally trajectory events.
function toTrajectoryEvents(sdkEvents) {
  const names = new Map();
  const out = [];
  for (const e of sdkEvents) {
    const timestamp = new Date(e.timestamp);
    const d = e.data;
    if (e.type === "assistant.turn_start") {
      out.push({ type: "turn_start", timestamp,
        data: { turnId: String(d.turnId) } });
    } else if (e.type === "assistant.turn_end") {
      out.push({ type: "turn_end", timestamp,
        data: { turnId: String(d.turnId) } });
    } else if (e.type === "tool.execution_start") {
      names.set(d.toolCallId, d.toolName);
      out.push({ type: "tool_call", timestamp,
        data: { toolName: d.toolName,
          toolCallId: d.toolCallId,
          arguments: d.arguments } });
    } else if (e.type === "tool.execution_complete") {
      out.push({ type: "tool_result", timestamp,
        data: { toolName: names.get(d.toolCallId),
          toolCallId: d.toolCallId, success: d.success,
          result: d.result?.content } });
    } else if (e.type === "assistant.message") {
      out.push({ type: "assistant_message", timestamp,
        data: { content: d.content } });
    } else if (e.type === "skill.invoked") {
      out.push({ type: "skill_activation", timestamp,
        data: { name: d.name, path: d.path } });
    } else if (e.type === "assistant.usage") {
      const nanoAiu = d.copilotUsage?.totalNanoAiu;
      out.push({ type: "token_usage", timestamp,
        data: { model: d.model,
          inputTokens: d.inputTokens ?? 0,
          outputTokens: d.outputTokens ?? 0,
          cacheReadTokens: d.cacheReadTokens ?? 0,
          cacheWriteTokens: d.cacheWriteTokens ?? 0,
          ...(nanoAiu === undefined ? {} : { cost: {
            provider: "github-copilot", unit: "nano-aiu",
            amount: nanoAiu } }) } });
    }
  }
  return out;
}

// Where the app writes its own traces: the trial's folder.
function telemetryFor(options) {
  const dir = options.sessionLog?.executorArtifactsDir;
  if (!dir) return undefined;
  mkdirSync(dir, { recursive: true });
  return { exporterType: "file", captureContent: true,
    filePath: path.join(dir, "app-traces.jsonl") };
}

const releaseApp = {
  name: "release-app",
  async execute(stimulus, options) {
    const startedAt = new Date();
    const { reply, events } = await writeEntries({
      repoDir: options.workDir,
      model: options.model,
      skillDirs: (options.skills ?? [])
        .map((skill) => path.dirname(skill.path)),
      request: stimulus.prompt,
      timeoutMs: options.timeout,
      telemetry: telemetryFor(options),
      traceContext: options.traceContext,
    });
    const completedAt = new Date();
    const trajectoryEvents = toTrajectoryEvents(events);
    return {
      id: randomUUID(),
      stimulus,
      events: trajectoryEvents,
      output: reply,
      workDir: options.workDir,
      metrics: {
        ...computeMetrics(trajectoryEvents),
        wallTimeMs: completedAt - startedAt,
      },
      metadata: {
        model: options.model ?? "default",
        skillsLoaded: trajectoryEvents
          .filter((e) => e.type === "skill_activation")
          .map((e) => e.data.name),
        startedAt,
        completedAt,
        executor: "release-app",
        sessionID: "",
      },
    };
  },
  async shutdown() {},
};

export function registerExecutors(registry) {
  registry.register(releaseApp);
}
