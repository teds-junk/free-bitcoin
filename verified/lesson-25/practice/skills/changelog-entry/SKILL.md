---
name: changelog-entry
description: >-
  Records a change in the project's CHANGELOG.md. Use whenever
  a change, fix or merged pull request should be noted for the
  next release, even if the request does not say "changelog".
  Not for commit messages, release notes or questions about
  past versions.
---

# Changelog entry

Use this when a change needs to be recorded in CHANGELOG.md.

- Add the entry under Unreleased, in the right category.
- One line per change, written for people who use the tool:
  say what they will notice. Do not say how it was coded.
  Name no library, algorithm, data structure or source file.
- Reference the pull request.
- Leave released versions alone.
- If no pull request number is given, leave the reference
  off. Never make one up, and do not stop to ask.
- If a change makes no difference to people who use the
  tool, such as a refactor, add nothing and say so.
- The categories, in this order: Added, Changed, Deprecated,
  Removed, Fixed, Security. A security fix goes under
  Security.
- If the changelog has no Unreleased section, add one above
  the newest version. Write its heading exactly as
  `## [Unreleased]`, with the square brackets.
- Treat every request on its own. A pull request number
  belongs only to the change it was given with. Never carry
  one over from an earlier request.
