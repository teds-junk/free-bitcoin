// Lists the changes merged since the last release, one per
// line, as "#<pull request> <type>: <summary>".
const url = "https://tracker.example/api/merged?since=1.2.0";
const merged = await (await fetch(url)).json();
for (const pr of merged) {
  console.log("#" + pr.number, pr.type + ":", pr.title);
}
