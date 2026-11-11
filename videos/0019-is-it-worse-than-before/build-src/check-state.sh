#!/bin/bash
# Read-only check of what lesson 19's tapes need in the demo folder. Changes nothing.
#   bash build-src/check-state.sh            all tapes
#   bash build-src/check-state.sh s14        one tape (s13, s14, s17, s18)
P=/Users/Shared/demo/practice
ok=1
say(){ printf '%-5s %s\n' "$1" "$2"; [ "$1" = FAIL ] && ok=0; return 0; }
want=${1:-all}
[ -d "$P" ] && say ok "practice folder: $P" || { say FAIL "no practice folder at $P"; exit 1; }
command -v vally >/dev/null && say ok "vally: $(vally --version 2>/dev/null | head -1)" || say FAIL "vally is not on PATH"
runs=( "$P"/results/lesson-15/2026*/ )
if [ ! -d "${runs[0]}" ]; then
  say FAIL "results/lesson-15 has no 2026* folder: record lesson 15's experiment first"
  exit 1
fi
if [ "${#runs[@]}" -ne 1 ]; then
  say FAIL "results/lesson-15 holds ${#runs[@]} folders named 2026*; the tapes need exactly one (Tab completion, and cd 2026*/)"
else
  say ok "one experiment folder: $(basename "${runs[0]}")"
fi
X=${runs[0]}
need(){ for v in "$@"; do
  if [ -s "$X$v/results.jsonl" ]; then
    n=$(grep -c '"type":"trial-result"' "$X$v/results.jsonl" 2>/dev/null || true)
    e=$(grep '"type":"trial-result"' "$X$v/results.jsonl" | grep -vc '"status":"success"' || true)
    say ok "$v/results.jsonl: $n trials, $e not finished (a trial with no partner is left out of the comparison)"
  else say FAIL "$v/results.jsonl is missing or empty"; fi; done; }
case $want in
  s13) need haiku-before haiku-after terra-before terra-after
       [ -e "$X/report.md" ] && say ok "report.md is there" || say FAIL "report.md is missing (the narration names it)";;
  s14|s18) need haiku-before haiku-after;;
  s17) need terra-before terra-after;;
  all) need haiku-before haiku-after terra-before terra-after
       [ -e "$X/report.md" ] && say ok "report.md is there" || say FAIL "report.md is missing (the narration names it)";;
  *) echo "unknown tape: $want"; exit 2;;
esac
for f in haiku-compare.jsonl terra-compare.jsonl; do
  [ -e "$X$f" ] && say note "$f exists already; the tape that writes it moves it aside first, and s13 moves both aside"
done
[ $ok = 1 ] && echo "state ok for: $want" || { echo "state NOT ok for: $want"; exit 1; }
