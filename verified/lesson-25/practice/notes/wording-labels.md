parser, haiku: Fix out-of-memory errors on large imports by using a streaming JSON parser: no
parser, haiku: Fix out-of-memory errors on large imports by using streaming JSON parser: no
parser, terra: Prevent out-of-memory errors when importing large JSON files: yes
parser, terra: Prevent out-of-memory errors when importing large JSON files: yes
cache, haiku: Improve performance of `notes list --tag` on large folders with LRU cache: no
cache, haiku: Improve performance of `notes list --tag` with LRU cache on tag index: no
cache, terra: Speed up `notes list --tag` for folders with many notes: yes
cache, terra: Speed up `notes list --tag` in large folders by caching the tag index: no
dates, haiku: Fix date parser to support single-digit months and days: yes
dates, haiku: Fix date parser to handle single-digit months and days: yes
dates, terra: Parse dates with single-digit months and days: yes
dates, terra: Parse single-digit months and days in dates: yes
(Start-state build: copied from the page's labels; no run.)

On 12 labels (7 yes, 5 no) the judge matched every one: TPR 100%, TNR 100%. That is enough to use it to compare versions of the skill, and not enough to trust a single verdict without reading its reason; we will label more whenever the rubric or the judge model changes.
