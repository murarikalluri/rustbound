# Rustbound — learn, practice, and investigate

Python + SQLite, a browser game interface, and a Tkinter launcher. No pip or npm packages are required to run the app.

## Start

Install Python 3.10+ with Tkinter and a current stable Rust toolchain from https://rustup.rs. Windows may also need the Microsoft C++ Build Tools linker. Double-click **Start Rustbound.cmd**, or run `python launcher.py` and click **Continue expedition**. Keep the launcher open while playing.

For browser-only use, run `python app.py` and open http://127.0.0.1:8765. Use `--port 9000` for another port.

## Features

- **One topic per module:** 92 individual modules, including separate pages for variables, changing a variable, constants, shadowing, Option, Some, None, Result, Ok, Err, and match. Learning-area filters keep the Rust Book sequence available without grouping several lessons into a single module. Existing lesson IDs and completion records are preserved.
- **Five clear sections:** what it is and how it works; where it is used; syntax; an example; one simple lab. The opening uses plain language. “A closer look” retains professional explanations without crowding the main lesson. Code sketches are labeled separately from standalone examples. Young learners can use the introductory material with a helper; advanced content still requires prerequisites and is not claimed to be independently mastered by a five-year-old.
- **Coverage:** setup, syntax, types, operators, control flow, ownership, borrowing, patterns, data modeling, collections, UTF-8, errors, generics, traits, iterators, lifetimes, smart pointers, tests, build tooling, threads, atomics, async, network framing, unsafe, FFI, macros, Pin, typestate, databases, observability, releases, and specialist introductions. See LEARNING.md for the complete syllabus. External crate ecosystems and unstable language features are not exhaustively covered.
- **40 Rust production scenarios:** the same five-part structure introduces the problem, its real-life setting, code or evidence, an example timeline, and one guided lab. Expand the solution to see cause, fix, verification, and prevention. New cases cover futures never polled, ignored task failures, channel shutdown, RefCell conflicts, costly cloning, lock order, malformed input, floating-point money, invalid keys, lazy iterators, indexing, byte order, partial writes, input buffers, connection scope, FFI panics, stale responses, cache growth, clocks, and disconnected receivers. All incidents and metrics are fictional teaching examples. Seven mechanisms are backed by linked advisories; 33 are general practice cases. The advisory snapshot remains dated **30 October 2026**.
- **Separate MCQ practice:** 40 original questions across ten topics. Answer one question at a time, then inspect explanations for every option. Topic, unanswered, and missed-answer filters support review. The server grades answers; answer keys are absent from the initial question payload. SQLite stores per-account submissions, first-attempt scores, latest results, and retry counts. MCQs do not award coding XP.
- **Personal reading progress:** completed lessons and case studies are stored per account in SQLite and shown in My progress, separately from coding XP. Existing lesson IDs and completions are preserved in this expansion. Marking a lesson complete is self-assessment, not an automated pass; module projects and lab work are self-reviewed. Scratch notes are explicitly unsaved.
- **Example formats:** standalone Rust examples target edition 2024. Shell commands, SQL/design sketches, a no_std library, and the Tokio dependency example have distinct labels and setup notes. Learning examples teach concepts; coding hints still contain no worked answers.
- **100 questions in eight modules**, starting with a complete Hello World program. Hello World is the only fixed-output warm-up. Questions 2–8 are CLI interview problems run against multiple stdin inputs. Questions 9–100 use varied-input function/type tests and progress through algorithms, ownership, APIs, concurrency, futures, and safety.
- **Light/dark theme** on login and game pages, saved in the browser. Without a saved choice, the system preference is used.
- **Larger island scene and walking explorer.** Passing code moves the character along the path with a walking cycle. Failed code does not trigger a walk. Previously completed questions show the character at the destination. Reduced-motion preferences skip the animation.
- **No worked coding solutions** in challenge hints or challenge API responses. Learning examples, incident debriefs, and submitted MCQ explanations are separate teaching features. Reference challenge implementations remain in local Python source for developer verification only.
- **My progress → Overview / My journal / Account.** The journal is inside authenticated personal progress, not the main navigation.
- **Signup:** username, email, optional display name, password, confirm password, and a password-hint question. Username satisfies the name-or-username requirement. Never put your password in the hint question; it is a private reminder, not a reset method.
- **Forgot password is available, but email OTP is intentionally on hold.** The panel explains this and disables sending. It sends no email, generates no OTP, and changes no password.

## Eight modules

| Module | Questions | Focus |
| --- | --- | --- |
| Hello Shore | 1–12 | Hello World, CLI input, validation, numeric reasoning, boundaries |
| Loop Lagoon | 13–24 | Missing IDs, compaction, trading profit, streaks, cancellation, search |
| Function Forest | 25–38 | Functions, Option, vectors, strings, maps |
| Ownership Grove | 39–50 | Borrowing, mutation, lifetimes, UTF-8 |
| Builder Bay | 51–62 | Structs, enums, generics, stacks, queues, parsers |
| Algorithm Canyon | 63–74 | Sorting, search, Two Sum, intervals, sliding windows |
| Systems Ridge | 75–87 | Traits, data structures, errors, iterators, macros, graphs |
| Concurrency Summit | 88–100 | Channels, atomics, mutexes, threads, futures, RAII, safety |

See COURSE.md for all titles. These are original learning/interview-style problems, not questions attributed to specific companies.

## Play

Read the lesson, task, examples, and constraints. Questions 1–8 require a complete `fn main()` program. For questions 2–8, stdin-reading scaffolding is supplied and the runner executes multiple input cases automatically. Questions 9–100 supply function/type signatures; do not add main unless requested. Click **Run code**, or use Ctrl+Enter / Cmd+Enter. All checks must pass to unlock the next question. Replays do not award duplicate XP.

Follow-up prompts are self-review, not automatically graded. Only question 1 uses a fixed-output greeting. The other CLI problems run the same compiled executable with distinct stdin/expected-output cases; a program printing only the visible sample answer is rejected. Behavioral tests are not an anti-cheating system or a proof of the intended algorithm. Function tests cover representative inputs and edge cases, but do not prove asymptotic complexity or unsafe-code soundness. Review your implementation against the design constraints too.

Drafts save automatically. Reset restores the starter after confirmation; completion is retained.

## Upgrade without losing progress

1. Close the launcher/server.
2. Back up and **keep your existing `progress.sqlite3`**. Replace application files with this release; do not replace your database with a blank one.
3. Restart the launcher and reload old browser tabs.

Existing accounts still work. Add an email and hint question under **My progress → Account**, confirming your current password. New accounts require these fields; older accounts are not locked out.

This revision replaces 32 questions. Unchanged questions retain their drafts, completions, and attempts in the new `reviewed_progress` / `reviewed_attempts` tables. Replaced questions start unsolved because they test different skills. All original records remain in the database. Existing accounts, themes, and profile details are retained. Old tabs must be reloaded because writes from the previous track are rejected.

Sessions expire after seven days. Restarting Tkinter may select a different port and require sign-in again. Theme choice is browser-specific. Accounts are local to this installation; there is no cloud sync.

## Accounts and execution

Passwords use salted PBKDF2-HMAC-SHA256 with 600,000 iterations. Sessions use hashed tokens, HttpOnly/SameSite=Strict cookies, and per-session mutation tokens. Email addresses are unique without case sensitivity. Updating account details requires the current password. Email and hint questions are returned only to the signed-in account.

**Rust submissions execute with your computer user's permissions; this is not a code sandbox.** Use trusted personal code only, and keep the server on loopback. Account separation is not OS-level isolation. Public/untrusted multi-user hosting requires an isolated runner, resource limits, production authentication, and HTTPS. Compilation has a 30-second timeout and execution a five-second timeout, which are not complete resource isolation.

The database is created beside app.py, or at `RUSTBOUND_DB` if configured. No mail credentials are needed while OTP is on hold.

## Verify

Run `python -m unittest -v test_app.CurriculumTests test_app.AnswerVisibilityTests test_release` for compiler, answer-visibility, account, and migration checks without network sockets. `test_app.ServerTests` additionally exercises HTTP over localhost.

Files: app.py (server), curriculum.py (course entry), course100.py (new questions), interview_bank.py (retained problems), interview_revision.py (reviewed active questions), launcher.py (Tkinter), static/ (UI), test_app.py and test_release.py (tests).
