// Checks the finished CHANGELOG.md.
// Each argument is Category=number. The Unreleased section
// must have an entry under that category that cites that
// pull request. Prints one result: pass or fail, and why.
import { existsSync, readFileSync } from "node:fs";

if (!existsSync("CHANGELOG.md")) fail("no CHANGELOG.md to check");

const text = readFileSync("CHANGELOG.md", "utf8");
const heading = "## [Unreleased]";
const start = text.indexOf(heading);
if (start < 0) fail("no '" + heading + "' heading");

const rest = text.slice(start + heading.length);
const end = rest.search(/^## /m);
const unreleased = end < 0 ? rest : rest.slice(0, end);

for (const want of process.argv.slice(2)) {
  const [category, number] = want.split("=");
  const from = unreleased.indexOf("### " + category + "\n");
  if (from < 0) fail("no '### " + category + "' in Unreleased");

  const after = unreleased.slice(from + 4);
  const stop = after.search(/^### /m);
  const body = stop < 0 ? after : after.slice(0, stop);
  if (!body.includes("(#" + number + ")")) {
    fail("no entry citing #" + number + " under " + category);
  }
}
report(true, "every entry found in Unreleased");

function fail(why) {
  report(false, why);
}

function report(passed, evidence) {
  console.log(JSON.stringify({
    name: "check-entry",
    kind: "code",
    passed,
    score: passed ? 1 : 0,
    evidence,
  }));
  process.exit(0);
}
