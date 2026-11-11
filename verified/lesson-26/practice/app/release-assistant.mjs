// The notes-cli release assistant. In a checkout of the
// repository, it asks an agent to write the Unreleased
// changelog entries, using the team's changelog skill.
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { CopilotClient, approveAll }
  from "@github/copilot-sdk";

export const REQUEST = "Write the Unreleased changelog"
  + " entries for every change listed in release/merged.txt.";

export async function writeEntries(options) {
  const client = new CopilotClient({
    // Where to write OpenTelemetry traces, if anywhere.
    telemetry: options.telemetry,
    // A trace to join: the SDK adds the agent's spans to it.
    onGetTraceContext: () => options.traceContext ?? {},
  });
  await client.start();
  const events = [];
  try {
    const session = await client.createSession({
      model: options.model,
      workingDirectory: options.repoDir,
      skillDirectories: options.skillDirs,
      // A fresh settings folder, so nobody's personal
      // Copilot setup changes what the agent does.
      configDirectory: mkdtempSync(
        path.join(tmpdir(), "release-assistant-")),
      onPermissionRequest: approveAll,
    });
    session.on((event) => events.push(event));
    const reply = await session.sendAndWait(
      { prompt: options.request ?? REQUEST },
      options.timeoutMs,
    );
    await session.disconnect();
    return { reply: reply?.data.content ?? "", events };
  } finally {
    await client.stop();
  }
}
