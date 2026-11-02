# Question review

This release replaces 32 questions rather than renaming the old output drills.

| Question | Replacement | Reasoning being tested |
| --- | --- | --- |
| 2 | Personalize a CLI greeting | Input · whitespace · fallback behavior |
| 3 | Split an expense without losing cents | Integer division · remainder · validation |
| 4 | Reconcile a cash drawer | Greedy choice · denominations |
| 5 | Measure an overnight shift | Time representation · wraparound |
| 6 | Audit a running wallet balance | State updates · first failure |
| 7 | Compare release versions | Tuples · lexicographic comparison |
| 8 | Validate a signed decimal token | Parsing · failure handling · numeric limits |
| 9 | Calendar validation at century boundaries | Booleans · condition precedence |
| 10 | Charge progressive usage tiers | Piecewise arithmetic · inclusive boundaries |
| 11 | Prevent double-counting multiples | Arithmetic · inclusion-exclusion |
| 12 | Safely place a paginated result window | Saturating arithmetic · bounds |
| 13 | Find the missing sequence number | Arithmetic invariant · wide sums |
| 14 | Find a second distinct high score | One-pass state · duplicate handling |
| 15 | Compress sorted IDs in place | Two pointers · logical length |
| 16 | Move empty slots to the end | Stable partition · in-place mutation |
| 17 | Best single buy and sell | Running minimum · order constraints |
| 18 | Measure an uninterrupted success streak | Run tracking · reset behavior |
| 19 | Detect a monotonic trend | Adjacent comparisons · direction flags |
| 20 | Cancel adjacent duplicate events | Stack · cascading cancellation |
| 21 | Find a balance point | Prefix sums · excluded current item |
| 22 | Buy the maximum number of items | Sorting · budget allocation |
| 23 | Find the first repeated request | HashSet · online detection |
| 24 | Count overlapping search hits | Byte windows · overlap semantics |
| 25 | Validate and total invoice lines | Checked arithmetic · indexed errors |
| 31 | Validate a triangle classification | Sorting · overflow-safe comparison |
| 39 | Minimize copies when sanitizing text | Cow · borrowed versus owned data |
| 40 | Flush an owned buffer without cloning | mem::take · move semantics |
| 41 | Flatten ownership across batches | Nested ownership · allocation sizing |
| 47 | Index borrowed source lines | Byte offsets · lifetimes |
| 48 | Parse an escaped delimiter format | State machine · escape handling |
| 49 | Normalize a relative route safely | Stack · parent segments · validation |
| 74 | Find a peak without scanning | Binary search on a slope |

## Review criteria

- Exactly one fixed-output question: Hello World.
- Seven CLI problems execute against multiple stdin cases with different expected outcomes.
- Ninety-two function/type questions exercise behavior across supplied parameters and edge cases.
- Basic arithmetic, parsing, iteration, ownership, and API design are taught through stated contracts.
- Patterns can recur when a new Rust ownership or API constraint changes the problem; changing only a printed label is not a new question.
- Worked solutions remain server-only; hints contain guidance.
- Unchanged question progress is preserved; replaced-question history stays archived in the database.
