# Verification

## Individual topics and five-part scenarios — 31 October 2026

- 92 modules with exactly one lesson per module. Existing stable IDs remain unchanged; 25 focused topics were added. Variables, match, Ok, and Err have distinct pages. The Rust Book remains linked and supplies learning-area order.
- Learning and production readers use five numbered sections with one lab. Plain-language openings precede optional professional detail; syntax sketches are distinguished from runnable examples. There is no claim of exhaustive ecosystem coverage or independent mastery of advanced Rust by very young children.
- Production lab expanded to 40 explicitly fictional scenarios: seven source-backed advisory mechanisms and 33 general Rust practice cases. The new cases include code/evidence, cause, fix, and verification guidance.
- Backend/compiler checks passed except an obsolete catalog assertion requiring a separate pitfall field for every lesson; that assertion was updated for the requested five-part schema and the catalog test passed on rerun. The remaining 13 checks passed, including examples, account isolation, migrations, MCQ grading, and challenge-answer privacy.
- Existing production and learning completion records remain account-scoped. MCQ behavior and coding questions are unchanged.
- All 82 standalone Rust lesson examples compiled and ran successfully; the library-only example compiled and the unit-test example passed. Dependency-based and illustrative syntax snippets retain their explicit labels.
- JSDOM integration passed for 92 individual topic cards, topic search, five-part learning/scenario pages, separate Variables/Ok/Err/match modules, related RefCell lesson navigation, collapsed/open solutions, note preservation on completion, account progress after reload, and existing MCQ/coding/theme behavior. Rendered visual screenshots remain unverified.

## Book path, incident workshops, and MCQs — 31 October 2026

- Reorganized 67 lessons into the official Rust Book’s 21-chapter sequence plus one extension module. Three original project workshops were added; all existing lesson IDs remain stable. Official chapter links accompany the original local lessons.
- All 20 production cases now contain explicitly fictional incident briefs, timelines, evidence, investigation prompts, and an expandable diagnosis/remediation debrief. Seven retain source-backed advisory mechanisms; advisory review dates remain 30 October 2026.
- Added 40 original MCQs in ten topics. The initial authenticated API omits answer keys and explanations. Submission validates the question/version/choice and grades on the server. Per-account attempts persist in SQLite; first-attempt scores are unchanged by retries.
- Fourteen backend tests passed: all MCQ keys, invalid inputs, stale bank version, CSRF, anonymous access, isolation, retry scoring, persistence, lesson catalog, compiled examples, account migrations, and challenge-answer privacy.
- All 57 standalone lesson examples compiled and ran, the no_std library compiled, and the unit-test example passed. The dependency-based Tokio example remains outside compilation verification.
- JSDOM integration passed for the 21 official chapter links, 67-lesson syllabus, incident evidence and collapsed/open debrief, 40-question navigation, explanations hidden before submission, wrong-answer feedback, correct retry, immutable first score, unanswered/missed filters, and persistence after reload. Existing registration, theme, profile, coding, and walking-state checks also passed.
- Browser rendering still requires visual review; behavioral checks use JSDOM with the real Python request handler. The public deployment remains deferred.

## Daily course expansion

- Expanded all 56 original lessons and added eight dedicated topics, preserving original stable lesson IDs. The course now has 64 ordered sessions, 14 module guides, 256 guided lab steps, and more than 21,000 teaching words (excluding source code).
- Each lesson has three topic-specific teaching paragraphs, an example walkthrough, lab, and review explanation. Catalog checks validate coverage metadata, linked scenario lesson IDs, day ordering, and prerequisite references.
- All 54 standalone Rust examples compiled with edition 2024 and ran successfully; the no_std example compiled as a library. The unit-test example also passed as a test harness. The external-dependency Tokio example was not dependency-built; command and design examples retain their format labels.
- Ten backend tests passed covering the expanded catalog, examples, user isolation, CSRF, persistence, mark-unread, invalid inputs, existing account/course migrations, and coding-answer visibility.
- JSDOM integration against the real Python handler passed for the module overview, 64-session syllabus, global topic search, module progress, daily lesson/lab rendering, module opening, resume, related scenario links, theme controls, existing coding execution, and reading persistence after reload.
- Rendered browser screenshots remain unverified. Session durations are suggested study budgets including hands-on activities, not measured reading times. The curriculum does not claim exhaustive coverage of all Rust ecosystem crates or unstable features.

## Learning library and production lab — 30 October 2026

- 56 lessons across 14 modules; 20 scenarios (seven linked advisories and 13 labeled practice scenarios).
- All 46 standalone Rust examples compiled with edition 2024 and ran successfully. The no_std library compiled as a library; the unit-test example also compiled and passed as a test harness. The Tokio example requires an external dependency and was not dependency-built here; terminal commands and design sketches are labeled rather than represented as executable snippets.
- Ten backend tests passed, including per-account reading isolation, unauthorized access, CSRF rejection, invalid-input rejection, idempotent saves, mark-unread, persistence across database initialization, existing account/course migrations, and absence of coding answers.
- Source review includes primary RustSec advisory pages, Tokio documentation, and SQLite transaction documentation. Version-specific remediation is a dated snapshot and links back to the source.
- DOM integration checks against the real Python handler passed: lesson search/empty results, module filters, examples, case-study remediation, related-lesson navigation, saved completion counts, and persistence on reload. Existing signup, profile, themes, journal, code execution, and walking-success checks also passed. These checks used JSDOM; rendered screenshots remain unverified.
- Publishing remains deferred. Existing local-runner deployment limitations still apply.

## Reviewed interview-question revision

- Replaced 32 questions: 23 repetitive post-Hello-World output drills and nine weak or overlapping later tasks.
- All 100 reference implementations pass; all 100 unfinished starters fail.
- Only Hello World is fixed-output. Seven CLI questions compile once and run against multiple stdin cases. Separate regression checks verify that printing only the first sample answer fails every one of them.
- The remaining 92 questions test functions/types against multiple inputs or scenarios, including boundaries and failure conditions.
- The full compiler/account suite passed (11 tests, including all-question subtests), followed by the sample-only CLI regression test.
- Migration checks preserve unchanged questions and accounts while retaining replaced-question history in the old tables. Old-tab submissions are rejected.

Visual browser screenshots remain unverified. Behavioral tests are not a proof of algorithmic complexity, unsafe-code soundness, or resistance to deliberate test cheating.

## Current 100-question release

- All 100 reference solutions compiled and passed, and all 100 unfinished starters were rejected.
- Compiler failure, incorrect implementations, and runtime-timeout checks passed. A timeout test initially targeted a function challenge with a main program; its target was corrected and the test passed on rerun.
- Account tests passed for required email/hint fields, password confirmation, case-insensitive email uniqueness, current-password confirmation for updates, existing-account upgrades, and separation between users.
- Course migration tests passed for mapping retained interview problems to their new IDs, retaining drafts/attempts, preserving originals, and avoiding duplicate imports.
- DOM integration checks against the real Python request handler passed for signup, the paused Forgot password option, theme persistence, 100 question cards/eight modules, personal journal tabs, profile updates, incorrect/correct Hello World submissions, walking success state, and moving to the next question.
- Worked solutions remain absent from the UI/API. OTP delivery is intentionally not implemented or tested in this release, as requested.

Visual browser rendering and the motion itself were not screenshot-verified; DOM checks validate interaction and animation state rather than rendered appearance. Test databases and accounts are excluded from the package.

## Solution visibility fix

The worked-solution button, answer panel, JavaScript reveal handler, and `/api/hint` answer endpoint have been removed. Hints still provide guidance without exposing the reference implementation. Existing drafts and progress are unchanged.

A regression test verifies that all course payloads omit reference solutions and private tests, starters differ from complete implementations, and the former endpoint returns 404. A DOM check verifies that the course initializes, progressive hints work, the editor retains its starter, and no solution control or answer panel exists. Python compilation and JavaScript syntax checks also pass.

## Current interview track

- All 36 new reference solutions compile and pass their behavioral checks.
- All 36 unfinished starter implementations fail their checks, so a starter cannot complete a question unchanged.
- Incorrect Two Sum implementations, including reusing one entry twice, are rejected. Compiler failures and execution timeouts are covered.
- Six backend integration tests passed: account registration/login/logout/expiry, per-account isolation, sequential unlocks, old-record preservation, one-time legacy import into the archive, stale-track rejection, origin validation, and authentication throttling.
- DOM integration tests against the live Python server passed for interview prompts, examples, constraints, progressive hints, ungraded follow-up labels, incorrect-code rejection, worked-solution reveal, complexity notes, dashboard updates, logout, and progress restoration after login.
- Python compilation and JavaScript syntax checks passed.

New questions use separate progress tables. No existing account records are deleted. Test accounts and databases are excluded from the downloadable package. Visual screenshots remain unverified; DOM tests do not replace browser layout inspection.

## Earlier versions

Verified with Python, Tkinter 8.6, Node 24, and Rust 1.99.1 in the build environment.

- All 36 reference solutions compiled and passed their mission checks.
- Invalid Rust, incorrect output, incorrect function results, and an infinite loop were rejected; the loop reached the runner timeout.
- HTTP integration checks passed for draft saves, SQLite persistence, sequential unlocks, repeat passes, preserving completion after a failed replay, request tokens, and HTML delivery.
- JavaScript syntax and Python compilation checks passed.
- DOM-based integration checks against the live Python server passed for all 36 map entries, the four regions, hint reveal, wrong-code feedback, completion animation state, XP, next mission, rapid-navigation draft saves, journal entries, locked missions, and restored drafts.
- A Tkinter window could be created and closed successfully.

The environment could not launch Chrome or Edge for screenshots. Responsive CSS and SVG artwork are implemented, but visual layout, actual animation rendering, and real-browser accessibility were not visually verified. DOM checks do not replace visual inspection.

Test data was kept outside the delivered project. A new installation starts with no completed missions.

## Account update

Five backend integration tests passed against isolated databases:

- Registration, case-insensitive usernames, duplicate-account handling, salted password storage, HttpOnly/SameSite cookies, logout invalidation, wrong-password rejection, and session expiry.
- Authenticated draft saves, real Rust submissions, replay behavior, and sequential level locks.
- Two independent accounts have separate drafts, completions, activity, and unlocks. Submitted user IDs cannot target another account; stale session request tokens cannot save into a switched account.
- Existing local progress imports into the first account once, while legacy tables remain intact; subsequent accounts start empty.
- Cross-origin writes and excessive authentication attempts are rejected.

DOM integration checks passed for registration, password confirmation, show/hide password, account identity, the personal progress dashboard, completing a real mission, updating XP/activity, logout, wrong-password feedback, and restoring progress after login. This exercised the live Python API with session cookies; visual browser screenshots remain unverified.

No test accounts or test progress are included in the ZIP.
