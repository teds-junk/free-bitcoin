# Wording labels

Does the entry say what changes for people who use the tool, without saying how it was coded?

| Stimulus, model, trial | Entry | Ours | Judge | 1 to 5 |
|---|---|---|---|---|
| parser, haiku, 0 | Fix out-of-memory errors on large imports by using streaming parser in importer.js | no | no | 2 |
| parser, haiku, 1 | Fix out-of-memory error when importing large files | yes | yes | 5 |
| parser, terra, 0 | Prevent out-of-memory errors when importing large files | yes | yes | 5 |
| parser, terra, 1 | Prevent out-of-memory errors when importing large JSON files | yes | yes | 5 |
| cache, haiku, 0 | Improve performance of `notes list --tag` with LRU cache on large folders | no | no | 2 |
| cache, haiku, 1 | Improve performance of `notes list --tag` with LRU cache for tag index | no | no | 2 |
| cache, terra, 0 | Speed up `notes list --tag` on large folders by caching the tag index | no | no | 4 |
| cache, terra, 1 | Speed up `notes list --tag` on large note folders by caching the tag index | no | yes | 4 |
| dates, haiku, 0 | Fix date parser to handle single-digit months and days | yes | yes | 4 |
| dates, haiku, 1 | Fix date parser to handle single-digit months and days | yes | yes | 4 |
| dates, terra, 0 | Parse dates with single-digit months and days | yes | yes | 5 |
| dates, terra, 1 | Parse single-digit months and days in dates | yes | yes | 5 |

On 12 labels (7 yes, 5 no) the judge matched 11: TPR 100%, TNR 80%. The one miss is an entry we hesitated over ourselves, which the judge failed in one trial and passed in the other. That is enough to use it to compare versions of the skill, knowing it may pass a borderline entry, and not enough to trust a single verdict without reading its reason; we will label more whenever the rubric or the judge model changes.

One verdict changed: terra's cache entry 'on large folders by caching the tag index' scored 4 and passed, where the yes-or-no judge said no (its twin 'on large note folders' also scored 4 and passed, as it had with the yes-or-no judge); we labelled both no, so against our 12 labels the 1-to-5 judge has TPR 7 of 7 and TNR 3 of 5.
