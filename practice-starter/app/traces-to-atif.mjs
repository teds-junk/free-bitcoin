// Turn the release app's OpenTelemetry traces into an ATIF
// trajectory that `vally grade` can read:
//   node app/traces-to-atif.mjs <traces file> > <atif file>
// Each model call (a "chat" span) becomes one agent step,
// holding the tool calls that ran after it and their results.
import { readFileSync } from "node:fs";

const spans = readFileSync(process.argv[2], "utf8")
  .split("\n").filter(Boolean).map((line) => JSON.parse(line))
  .filter((s) => s.type === "span")
  .sort((a, b) => a.startTime[0] - b.startTime[0]
    || a.startTime[1] - b.startTime[1]);

// The text parts of a span's recorded output messages.
const textOf = (json) => JSON.parse(json ?? "[]")
  .flatMap((m) => m.parts)
  .filter((p) => p.type === "text")
  .map((p) => p.content).join("\n");

// Most tools take JSON arguments; apply_patch takes text.
function argumentsOf(raw) {
  try {
    return JSON.parse(raw ?? "{}");
  } catch {
    return { input: raw };
  }
}

const steps = [];
let model = "unknown";
let session = "unknown";
for (const span of spans) {
  const a = span.attributes;
  session = a["gen_ai.conversation.id"] ?? session;
  if (a["gen_ai.operation.name"] === "chat") {
    model = a["gen_ai.request.model"];
    steps.push({
      step_id: steps.length + 1,
      source: "agent",
      model_name: model,
      message: textOf(a["gen_ai.output.messages"]),
      tool_calls: [],
      observation: { results: [] },
      metrics: {
        prompt_tokens: a["gen_ai.usage.input_tokens"],
        completion_tokens: a["gen_ai.usage.output_tokens"],
        cached_tokens:
          a["gen_ai.usage.cache_read.input_tokens"],
        // A billion nano-AIU is one AI Credit: $0.01.
        cost_usd: (a["github.copilot.nano_aiu"] ?? 0) / 1e11,
      },
    });
  } else if (a["gen_ai.operation.name"] === "execute_tool"
      && steps.length > 0) {
    const step = steps[steps.length - 1];
    const id = a["gen_ai.tool.call.id"];
    step.tool_calls.push({
      tool_call_id: id,
      function_name: a["gen_ai.tool.name"],
      arguments: argumentsOf(a["gen_ai.tool.call.arguments"]),
    });
    step.observation.results.push({
      source_call_id: id,
      content: a["gen_ai.tool.call.result"] ?? "",
    });
  }
}

console.log(JSON.stringify({
  schema_version: "ATIF-v1.4",
  session_id: session,
  agent: { name: "notes-cli-release-app", version: "1.0",
    model_name: model },
  steps,
}, null, 2));
