# Wording labels

Does the entry say what changes for people who use the tool, without saying how it was coded?

| Stimulus, model, trial | Entry | Ours | Judge | 1 to 5 |
|---|---|---|---|---|
| parser, haiku, 0 | Fix out-of-memory errors during large imports by using a streaming JSON parser | no | no | 2 |
| parser, haiku, 1 | Fix out-of-memory errors when importing large files by using a streaming parser in importer.js | no | no | 2 |
| parser, terra, 0 | Prevent out-of-memory errors when importing large JSON files | yes | yes | 5 |
| parser, terra, 1 | Prevent out-of-memory errors when importing large files | yes | yes | 5 |
| cache, haiku, 0 | Improve performance of `notes list --tag` with LRU caching on large folders | no | no | 2 |
| cache, haiku, 1 | Improve performance of `notes list --tag` with LRU cache for tag index | no | no | 2 |
| cache, terra, 0 | Speed up `notes list --tag` on large folders by caching the tag index | no | no | 4 |
| cache, terra, 1 | Speed up `notes list --tag` for large folders by caching the tag index | no | no | 3 |
| dates, haiku, 0 | Fix date parser to support single-digit months and days | yes | yes | 4 |
| dates, haiku, 1 | Fix date parser to support single-digit months and days | yes | yes | 4 |
| dates, terra, 0 | Parse dates with single-digit months and days | yes | yes | 5 |
| dates, terra, 1 | Parse dates with single-digit months and days correctly | yes | yes | 5 |

On 12 labels (6 yes, 6 no) the judge matched every one: TPR 100%, TNR 100%. That is enough to use it to compare versions of the skill, and not enough to trust a single verdict without reading its reason; we will label more whenever the rubric or the judge model changes.

One verdict changed: terra's cache entry 'on large folders by caching the tag index' scored 4 and passed, where the yes-or-no judge and our label said no (its twin 'for large folders' scored 3 and failed); against our 12 labels the 1-to-5 judge has TPR 6 of 6 and TNR 5 of 6.
