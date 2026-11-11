// Hidden test for the release stimulus. Each feature and
// fix in release/merged.txt needs a line of its own under
// Unreleased; a refactor needs none. Exit 1 means fail.
import { readFileSync } from "node:fs";

const merged = readFileSync("release/merged.txt", "utf8");
const log = readFileSync("CHANGELOG.md", "utf8");
const start = log.indexOf("## [Unreleased]");
const end = log.indexOf("\n## [", start + 1);
const lines = log.slice(start, end).split("\n");

for (const item of merged.trim().split("\n")) {
  const [, number, type] = item.match(/^#(\d+) (\w+):/);
  const cite = "(#" + number + ")";
  const found = lines.filter((line) => line.includes(cite));
  if (type === "refactor") {
    if (found.length > 0) fail(cite + " is internal");
  } else if (found.length !== 1) {
    fail(cite + " needs one line, found " + found.length);
  } else if (found[0].split("(#").length > 2) {
    fail(cite + " shares a line with another change");
  }
}
console.log("every merged change handled");

function fail(why) {
  console.error(why);
  process.exit(1);
}
