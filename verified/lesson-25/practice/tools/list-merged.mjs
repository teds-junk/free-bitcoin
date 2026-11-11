// Lists the changes merged since the last release, one per
// line, as "#<pull request> <type>: <summary>".
// The real release tool asks the team's tracker. This copy
// prints a fixed list, so every trial starts the same way.
const merged = [
  "#74 feat: add --since <date> to notes list",
  "#75 fix: notes search missed titles with accents",
  "#76 refactor: move config loading out of cli.js",
];

for (const line of merged) console.log(line);
