# Failure modes

1. No rule for a missing pull request number: invents one. typo-fix, terra.
2. Records a change users cannot see. refactor, both.
3. Files a security fix under Fixed. security, both.
4. Describes how the fix was coded. parser, haiku.
5. New Unreleased heading does not match the file. after-release, terra.

# Notes, one per trial

- refactor, haiku: "Refactor storage.js into three smaller modules..." under Changed. Users cannot see this.
- refactor, terra: "Refactor internal storage modules with no user-facing behavior changes" under Changed. Same problem.
- typo-fix, haiku: entry under Fixed, no number. Fine.
- typo-fix, terra: entry under Fixed ending (#42). Nobody gave a number.
- two-changes, haiku: --json under Added, page-2 bug under Fixed, both (#60). Fine.
- two-changes, terra: same split, both (#60). Fine.
- security, haiku: under Fixed, calls it a path traversal vulnerability.
- security, terra: under Fixed.
- parser, haiku: "...by using streaming parser". How it was coded.
- parser, terra: "Prevent out-of-memory errors when importing large JSON files". Fine.
- after-release, haiku: new "## [Unreleased]" heading. Fine.
- after-release, terra: new "## Unreleased" heading, no brackets.
