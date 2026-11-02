# Rustbound: reviewed interview course

Hello World is the only fixed-output warm-up. Every later question checks input-dependent behavior.

## 1. Hello Shore — CLI problems & numeric reasoning

1. **Hello, world!** — Every executable starts in fn main(). println! prints a line; statements end with a semicolon.
2. **Personalize a CLI greeting** — Input · whitespace · fallback behavior
3. **Split an expense without losing cents** — Integer division · remainder · validation
4. **Reconcile a cash drawer** — Greedy choice · denominations
5. **Measure an overnight shift** — Time representation · wraparound
6. **Audit a running wallet balance** — State updates · first failure
7. **Compare release versions** — Tuples · lexicographic comparison
8. **Validate a signed decimal token** — Parsing · failure handling · numeric limits
9. **Calendar validation at century boundaries** — Booleans · condition precedence
10. **Charge progressive usage tiers** — Piecewise arithmetic · inclusive boundaries
11. **Prevent double-counting multiples** — Arithmetic · inclusion-exclusion
12. **Safely place a paginated result window** — Saturating arithmetic · bounds

## 2. Loop Lagoon — Search, simulation & invariants

13. **Find the missing sequence number** — Arithmetic invariant · wide sums
14. **Find a second distinct high score** — One-pass state · duplicate handling
15. **Compress sorted IDs in place** — Two pointers · logical length
16. **Move empty slots to the end** — Stable partition · in-place mutation
17. **Best single buy and sell** — Running minimum · order constraints
18. **Measure an uninterrupted success streak** — Run tracking · reset behavior
19. **Detect a monotonic trend** — Adjacent comparisons · direction flags
20. **Cancel adjacent duplicate events** — Stack · cascading cancellation
21. **Find a balance point** — Prefix sums · excluded current item
22. **Buy the maximum number of items** — Sorting · budget allocation
23. **Find the first repeated request** — HashSet · online detection
24. **Count overlapping search hits** — Byte windows · overlap semantics

## 3. Function Forest — Functions & collections

25. **Validate and total invoice lines** — Checked arithmetic · indexed errors
26. **Find a common divisor** — Loops · Euclidean algorithm
27. **Checked factorial** — Option · overflow
28. **Identify prime numbers** — Conditions · efficient loops
29. **Build the Fibonacci sequence** — Vec · loops
30. **FizzBuzz labels** — Branch ordering · String
31. **Validate a triangle classification** — Sorting · overflow-safe comparison
32. **Find a range of readings** — Slices · Option · tuples
33. **Count successful readings** — Slice iteration · predicates
34. **Average a measurement batch** — Type conversion · empty cases
35. **Running totals** — Accumulator · Vec
36. **Reverse a sentence** — String slices · joining
37. **Count words consistently** — HashMap · sorting
38. **First unique character** — Unicode · frequency maps

## 4. Ownership Grove — Borrowing & mutation

39. **Minimize copies when sanitizing text** — Cow · borrowed versus owned data
40. **Flush an owned buffer without cloning** — mem::take · move semantics
41. **Flatten ownership across batches** — Nested ownership · allocation sizing
42. **Swap without cloning** — Generic mutable references
43. **Borrow the longest label** — Lifetimes · slices
44. **Shared text prefix** — UTF-8 boundaries · borrowing
45. **Clean an inventory in place** — Vec::retain · mutation
46. **Clamp sensor values** — Mutable slices · bounded values
47. **Index borrowed source lines** — Byte offsets · lifetimes
48. **Parse an escaped delimiter format** — State machine · escape handling
49. **Normalize a relative route safely** — Stack · parent segments · validation
50. **Borrow a stored value** — Lifetimes · key lookup

## 5. Builder Bay — Structs, enums & APIs

51. **Model a rectangle** — Structs · impl methods
52. **Manage stock safely** — Struct state · Result
53. **Cycle a traffic light** — Enums · exhaustive match
54. **Dispatch a command** — Enums with data · validation
55. **Build a generic stack** — Generics · LIFO ownership
56. **Queue support tickets** — VecDeque · FIFO ownership
57. **Keep recent events** — Bounded buffer · eviction
58. **Validate a network port** — Typed errors · parsing
59. **Borrow tokens from a request** — Lifetimes · zero-copy string slices
60. **Parse borrowed configuration** — String parsing · Result · lifetimes
61. **Partition without cloning** — Ownership · generics · FnMut
62. **Rotate a reusable buffer** — Mutable slices · in-place algorithms

## 6. Algorithm Canyon — Searching & problem solving

63. **Insertion sort in place** — Sorting · comparisons
64. **Evaluate postfix arithmetic** — Stacks · Result
65. **Two Sum: reconcile a payment** — HashMap · indices · Option
66. **Validate a normalized palindrome** — Strings · two pointers · ASCII
67. **Compress consecutive events** — Iterators · Unicode · run-length encoding
68. **Deduplicate an event stream** — HashSet · stable ordering
69. **Find the first matching record** — Binary search · boundary invariants
70. **Check nested delimiters** — Stacks · matching pairs
71. **Merge reservation windows** — Sorting · interval merging
72. **Rank frequent search terms** — HashMap · deterministic tie-breaking
73. **Peak traffic window** — Sliding window · numeric bounds
74. **Find a peak without scanning** — Binary search on a slope

## 7. Systems Ridge — Traits, errors & design

75. **Truncate UTF-8 safely** — Byte budgets · char boundaries
76. **Make a transfer atomic** — Mutable references · checked arithmetic
77. **Reverse an owned linked list** — Box · Option::take · moves
78. **Validate a binary search tree** — Recursive borrowing · strict bounds
79. **Parse a batch with useful errors** — Custom enums · error propagation
80. **Design an LRU cache** — Struct API · eviction · recency
81. **Build a lazy merge iterator** — Iterator · associated types · laziness
82. **Compose a validation pipeline** — Trait objects · short-circuiting
83. **Evaluate an expression tree** — Enums · recursion · checked math
84. **Retry a fallible operation** — FnMut · generic errors · exact call counts
85. **Write a single-evaluation macro** — macro_rules! · hygiene · side effects
86. **Schedule dependency jobs** — Graphs · topological ordering · cycles
87. **Find the cheapest route** — Dijkstra · priority queues · stale entries

## 8. Concurrency Summit — Threads, futures & safety

88. **Receive a producer stream** — mpsc channels · ownership
89. **Issue unique tickets** — Atomic fetch_add · shared ownership
90. **Recover a poisoned mutex** — Mutex poisoning · explicit policy
91. **Validate a newtype conversion** — TryFrom · type invariants
92. **Parallelize borrowed data** — Scoped threads · chunking · joins
93. **Bounded parallel map** — Worker scheduling · exactly-once calls
94. **Protect shared account transfers** — Arc · Mutex · compound invariants
95. **Memoize an expensive computation** — Generic closures · cache misses
96. **Initialize a service exactly once** — OnceLock · shared initialization
97. **Implement a cooperative future** — Future · Pin · wake protocol
98. **Release a permit with RAII** — Drop · Arc · atomics
99. **Audit a mutable slice split** — Unsafe boundaries · aliasing · lifetimes
100. **Transactional ledger: the final round** — State machines · idempotency · rollback
