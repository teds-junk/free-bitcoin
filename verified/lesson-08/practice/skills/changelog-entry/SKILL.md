---
name: changelog-entry
description: Adds an entry to the project changelog.
---

# Changelog entry

Use this when a change needs to be recorded in CHANGELOG.md.

- Add the entry under Unreleased, in the right category.
- One line per change, written for people who use the tool.
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
