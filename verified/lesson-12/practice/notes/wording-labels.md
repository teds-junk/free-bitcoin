# Wording labels

Does the entry say what changes for people who use the tool, without saying how it was coded?

| Stimulus, model, trial | Entry | Ours | Judge |
|---|---|---|---|
| parser, haiku, 0 | Fix out-of-memory errors during large imports by using a streaming JSON parser | no | no |
| parser, haiku, 1 | Fix out-of-memory errors when importing large files by using a streaming parser in importer.js | no | no |
| parser, terra, 0 | Prevent out-of-memory errors when importing large JSON files | yes | yes |
| parser, terra, 1 | Prevent out-of-memory errors when importing large files | yes | yes |
| cache, haiku, 0 | Improve performance of `notes list --tag` with LRU caching on large folders | no | no |
| cache, haiku, 1 | Improve performance of `notes list --tag` with LRU cache for tag index | no | no |
| cache, terra, 0 | Speed up `notes list --tag` on large folders by caching the tag index | no | no |
| cache, terra, 1 | Speed up `notes list --tag` for large folders by caching the tag index | no | no |
| dates, haiku, 0 | Fix date parser to support single-digit months and days | yes | yes |
| dates, haiku, 1 | Fix date parser to support single-digit months and days | yes | yes |
| dates, terra, 0 | Parse dates with single-digit months and days | yes | yes |
| dates, terra, 1 | Parse dates with single-digit months and days correctly | yes | yes |
