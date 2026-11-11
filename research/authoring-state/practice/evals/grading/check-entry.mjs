// Checks the finished CHANGELOG.md.
// Each argument is Category=number. The Unreleased section
// must have an entry under that category that cites that
// pull request. Exits 0 if all are found, 1 if any is not.
import { readFileSync } from "node:fs";

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
console.log("ok");

function fail(why) {
  console.error(why);
  process.exit(1);
}
