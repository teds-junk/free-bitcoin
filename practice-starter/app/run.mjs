// Run the release assistant once, with tracing to a file:
//   node app/run.mjs <repo> <skills> <model> <traces file>
import path from "node:path";
import { writeEntries } from "./release-assistant.mjs";

const [repo, skills, model, traces] = process.argv.slice(2);
const { reply } = await writeEntries({
  repoDir: path.resolve(repo),
  skillDirs: [path.resolve(skills)],
  model,
  timeoutMs: 180000,
  telemetry: {
    exporterType: "file",
    filePath: path.resolve(traces),
    captureContent: true,
  },
});
console.log(reply);
