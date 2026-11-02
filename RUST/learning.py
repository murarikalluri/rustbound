"""Independent reading curriculum. Examples are not coding-challenge answers."""
LESSONS = []
MODULES = ['First steps', 'Values and decisions', 'Ownership and borrowing', 'Model your domain', 'Collections and text', 'Errors and boundaries', 'Reusable abstractions', 'Memory and lifetimes', 'Testing and tooling', 'Concurrency', 'Async services', 'Advanced Rust', 'Shipping software', 'Specialist paths']
BOOK = 'https://doc.rust-lang.org/book/'
def lesson(module, slug, title, explain, code, walkthrough, use, pitfall, question, source, language='rust'):
    LESSONS.append(dict(id=slug, module=MODULES[module], stage='Beginner' if module<4 else 'Intermediate' if module<9 else 'Advanced', title=title, explain=explain, code=code, walkthrough=walkthrough, use=use, pitfall=pitfall, question=question, source=source if source.startswith('https:') else BOOK+source, language=language))

lesson(0,'setup','Install Rust and meet the tools',
'A program is a set of instructions stored in a text file. Rust compiles that source into a native executable before it runs. rustup manages toolchains, rustc compiles Rust, and Cargo builds projects and manages dependencies. Install through the official instructions for your operating system; Windows also needs a supported native linker.',
'rustup --version\nrustc --version\ncargo --version\nrustup doc --book',
'Run these in a terminal after installing Rust and reopening the terminal. The first three commands confirm that tools are on PATH. The last opens locally installed documentation. Version numbers depend on your toolchain.',
'A new teammate uses the same toolchain as CI so compiler behavior is reproducible.',
'Installing an editor extension alone does not install a compiler or linker.',
'What does the compiler do, and what does Cargo add?', 'ch01-01-installation.html','shell')
lesson(0,'hello','Hello, world! — your first program',
'Execution starts at main. Braces group its instructions. println! writes text followed by a newline; the exclamation mark marks a macro invocation. A string literal is text between double quotes. A semicolon ends this statement. Start by observing one predictable action before adding input or branching.',
'fn main() {\n    println!("Hello, world!");\n}',
'Save this as main.rs, run rustc main.rs, then run the produced executable (./main on Unix or .\\main.exe in PowerShell). It prints Hello, world! exactly once.',
'A small startup message proves a command-line tool is installed and launching correctly.',
'Single quotes represent characters, not strings. Rust distinguishes uppercase and lowercase names.',
'What changes if you use print! instead of println!?', 'ch01-02-hello-world.html')
lesson(0,'cargo','Create, build, and run a Cargo project',
'A Cargo package contains a manifest and source files. Cargo.toml describes package metadata and dependencies. src/main.rs is the conventional entry point for a binary. cargo check catches many compiler errors without producing the final executable; cargo run builds and executes it.',
'cargo new weather_cli\ncd weather_cli\ncargo check\ncargo run\ncargo build --release',
'The first command creates a project containing a greeting. Debug builds favor development speed. The release profile enables optimizations and writes artifacts under target/release; measure performance there.',
'A team uses cargo check during editing and tests a release build before shipping a CLI.',
'Do not compare debug-build timings with optimized production binaries.',
'Which files belong in source control, and which are generated?', 'ch01-03-hello-cargo.html','shell')
lesson(0,'diagnostics','Read compiler errors and format code',
'Compiler diagnostics identify a location, explain a mismatch, and often suggest a repair. Fix the first meaningful error before chasing cascades. rustfmt standardizes layout; Clippy finds suspicious or unnecessarily complex patterns. These tools support review but cannot decide whether your business rules are correct.',
'cargo fmt --check\ncargo clippy --all-targets\ncargo test\nrustc --explain E0308',
'Formatting checks report style differences. Clippy analyzes targets. Tests execute checks you wrote. E0308 explains a type mismatch; use the error code from your own diagnostic.',
'A pull request pipeline catches accidental mistakes before reviewers focus on design.',
'Suppressing warnings globally hides new defects. Explain narrow exceptions near the affected code.',
'Why can a program pass Clippy and still charge a customer incorrectly?', 'https://doc.rust-lang.org/clippy/','shell')

lesson(1,'bindings','Variables, mutability, constants, and shadowing',
'let gives a value a name. Bindings are immutable unless marked mut, so accidental reassignment is rejected. Shadowing creates a new binding and can change its type. const declares a compile-time value with an explicit type; it is not a mutable global variable.',
'fn main() {\n    const PACK_SIZE: u32 = 6;\n    let boxes = "3";\n    let boxes: u32 = boxes.parse().expect("known number");\n    let mut bottles = boxes * PACK_SIZE;\n    bottles -= 1;\n    assert_eq!(bottles, 17);\n}',
'boxes first holds text, then a parsed integer under a new binding. bottles changes after one item is used. The assertion checks the resulting inventory.',
'Inventory code distinguishes configuration that never changes from stock that changes per transaction.',
'Use expect here only because the literal is controlled; external input needs a Result branch.',
'When would you choose shadowing over mut?', 'ch03-01-variables-and-mutability.html')
lesson(1,'types','Numbers, booleans, characters, tuples, and arrays',
'Types constrain which operations are meaningful. Integer widths determine range; signed types allow negative values. Floats approximate real numbers and are unsuitable for exact money accounting without a deliberate rounding policy. char is a Unicode scalar, not a byte. Tuples combine different types; arrays hold a fixed number of one type.',
'fn main() {\n    let reading: (i16, bool) = (-7, true);\n    let samples: [i16; 3] = [-7, -6, -5];\n    let (temperature, valid) = reading;\n    assert!(valid && samples[0] == temperature);\n    assert_eq!(250u8.checked_add(10), None);\n}',
'Destructuring names both tuple fields. The array has exactly three elements. checked_add makes overflow explicit instead of depending on build settings.',
'A sensor protocol needs precise numeric bounds and a separate validity flag.',
'as casts can truncate or reinterpret numeric values; use try_from for fallible conversions.',
'Why can a byte count differ from a character count?', 'ch03-02-data-types.html')
lesson(1,'functions','Functions, expressions, and control flow',
'Functions name reusable behavior and declare parameter types. An expression produces a value; a trailing expression without a semicolon becomes the return value. if can itself be an expression, but its branches must agree on a type. match makes multiple alternatives explicit and checks coverage.',
'fn shipping(weight: u32) -> u32 {\n    if weight == 0 { 0 } else if weight <= 5 { 40 } else { 75 }\n}\nfn main() {\n    assert_eq!(shipping(4), 40);\n    let label = match shipping(0) { 0 => "free", _ => "paid" };\n    assert_eq!(label, "free");\n}',
'The if expression determines the function result. match maps the numeric fee to a label, including a fallback arm.',
'A checkout service separates price rules into small testable functions.',
'A semicolon after the final if expression discards its value and changes the body result to ().',
'How would you test the boundaries at weights 0, 5, and 6?', 'ch03-03-how-functions-work.html')
lesson(1,'loops','Loops, ranges, and early exits',
'for consumes an iterator, while repeats while a condition holds, and loop repeats until a break. Exclusive ranges a..b omit b; inclusive ranges a..=b include it. Use continue to skip one iteration and break to leave the loop. Choose an iteration form that makes termination obvious.',
'fn main() {\n    let mut accepted = 0;\n    for value in [2, -1, 4, 9] {\n        if value < 0 { continue; }\n        if value > 5 { break; }\n        accepted += value;\n    }\n    assert_eq!(accepted, 6);\n}',
'The negative entry is ignored. Reaching 9 stops processing, so only 2 and 4 contribute.',
'A batch importer stops at a sentinel and skips records classified as irrelevant.',
'An unbounded loop without a blocking operation can consume an entire CPU core.',
'What changes if break is replaced with continue?', 'ch03-05-control-flow.html')

lesson(2,'ownership','Ownership, moves, Copy, and Clone',
'An owned value has an owner responsible for cleanup. Assigning a String usually moves ownership instead of copying its allocation. Copy types such as small integers can be duplicated implicitly. Clone explicitly requests duplication and may allocate or perform other work. Ownership prevents two owners from independently freeing the same allocation.',
'fn main() {\n    let draft = String::from("shipment");\n    let queued = draft;\n    let archive = queued.clone();\n    assert_eq!(queued, archive);\n}',
'draft becomes unusable after the move. queued owns the original allocation; archive owns a separate cloned string. Both are cleaned up when they leave scope.',
'Moving a request into a worker makes responsibility for that request clear.',
'Adding clone everywhere may hide a poor API design and add substantial memory traffic.',
'Why does assigning a u32 behave differently from assigning a String?', 'ch04-01-what-is-ownership.html')
lesson(2,'borrowing','Shared and mutable references',
'Borrowing lets a function access a value without owning it. Shared references allow reading; a mutable reference allows exclusive access for mutation. For the same data, overlapping active borrows cannot combine a mutable reference with other references. The compiler often ends a borrow after its last use, before the surrounding scope ends.',
'fn add_tax(cents: &mut u32) { *cents += 20; }\nfn main() {\n    let mut bill = 100;\n    add_tax(&mut bill);\n    let receipt = &bill;\n    assert_eq!(*receipt, 120);\n}',
'The function receives temporary exclusive access, updates through the reference, then returns. The caller remains the owner.',
'A parser can borrow an input buffer while an accounting function can mutate a caller-owned total.',
'A mutable binding is not permission to bypass aliasing rules.',
'When should an API take T, &T, or &mut T?', 'ch04-02-references-and-borrowing.html')
lesson(2,'slices','Slices and borrowed views',
'A slice views contiguous elements without owning them. &[T] borrows an array or vector range, and &str borrows UTF-8 text. Slices carry a length, so APIs can accept different underlying containers. Their validity is tied to the owner; resizing a vector while a slice is still used would risk invalidating its storage.',
'fn total(values: &[i32]) -> i32 { values.iter().sum() }\nfn main() {\n    let daily = vec![3, 5, 8, 13];\n    assert_eq!(total(&daily[1..3]), 13);\n    assert_eq!(total(&[]), 0);\n}',
'Indices 1 and 2 form a borrowed window. No elements are copied and the original vector stays owned by main.',
'An analytics function summarizes a window of measurements without allocating a new vector.',
'Indexing outside a slice panics. Use get when an index is untrusted.',
'Why is accepting &[i32] more flexible than &Vec<i32>?', 'ch04-03-slices.html')
lesson(2,'io','Read input and write files safely',
'I/O can fail for environmental reasons even when the program is correct. std::io returns Results so callers must handle permissions, missing files, and broken pipes. Buffering reduces small system calls. Keep data parsing separate from reading so it can be tested without a real terminal or filesystem.',
'use std::io::{self, BufRead};\nfn count_lines(reader: impl BufRead) -> io::Result<usize> {\n    let mut count = 0;\n    for line in reader.lines() { line?; count += 1; }\n    Ok(count)\n}\nfn main() -> io::Result<()> {\n    assert_eq!(count_lines(io::Cursor::new(b"red\\nblue\\n"))?, 2);\n    Ok(())\n}',
'Cursor supplies in-memory input. Each line may fail independently, so ? propagates its error. The function works with other buffered readers too.',
'A log ingestion utility can use the same parser for files, stdin, and test fixtures.',
'Reading a whole untrusted file into memory requires an explicit size limit.',
'How would you report both a filename and the underlying I/O error?', 'ch12-02-reading-a-file.html')

lesson(3,'structs','Structs, methods, and constructors',
'A struct groups named fields into a domain value. impl attaches associated functions and methods. &self reads an instance, &mut self updates it, and self consumes it. Rust has no special constructor syntax: a function named new is a convention. Keep fields private when every mutation must preserve an invariant.',
'struct Parcel { grams: u32 }\nimpl Parcel {\n    fn new(grams: u32) -> Option<Self> {\n        if grams == 0 { None } else { Some(Self { grams }) }\n    }\n    fn kilograms(&self) -> f64 { self.grams as f64 / 1000.0 }\n}\nfn main() { assert_eq!(Parcel::new(1500).unwrap().kilograms(), 1.5); }',
'The constructor rejects zero weight. kilograms borrows the parcel so it can be queried repeatedly.',
'Domain types prevent invalid inventory records from circulating through a service.',
'Public fields let callers bypass your constructor; visibility belongs in the invariant design.',
'When should a method consume self?', 'ch05-03-method-syntax.html')
lesson(3,'enums','Enums and state machines',
'An enum represents one of several named alternatives, each optionally containing different data. Unlike a string status plus unrelated optional fields, an enum can make contradictory states impossible. match handles each variant and the compiler helps find affected code when you add a new one.',
'enum Delivery { Queued, Sent { tracking: String }, Failed(String) }\nfn label(state: &Delivery) -> &str {\n    match state { Delivery::Queued => "waiting", Delivery::Sent { tracking } => tracking, Delivery::Failed(reason) => reason }\n}\nfn main() {\n    assert_eq!(label(&Delivery::Queued), "waiting");\n    assert_eq!(label(&Delivery::Sent { tracking: "ZX9".into() }), "ZX9");\n    assert_eq!(label(&Delivery::Failed("address".into())), "address");\n}',
'A sent delivery always contains tracking data. The match borrows that data instead of cloning it.',
'Payment and deployment workflows benefit from explicitly modeled states.',
'Enums model data states; legal transitions still need methods or a typestate design.',
'How would you prevent sending an already delivered parcel?', 'ch06-01-defining-an-enum.html')
lesson(3,'option','Option, match, if let, and let else',
'Option<T> represents presence or absence without a null pointer convention. Some carries a value and None carries none. match handles both cases, if let focuses on one case, and let else provides an early-exit path when a pattern fails. Absence is often ordinary business behavior rather than an exceptional failure.',
'fn initial(name: Option<&str>) -> char {\n    let Some(name) = name else { return \'?\'; };\n    name.chars().next().unwrap_or(\'?\')\n}\nfn main() {\n    assert_eq!(initial(Some("Maya")), \'M\');\n    assert_eq!(initial(None), \'?\');\n}',
'Missing names return immediately. An empty supplied string also uses the fallback because next returns None.',
'A profile avatar can display a placeholder when no display name is available.',
'unwrap turns expected absence into a panic.',
'When does Option lose information that a Result should retain?', 'ch06-03-if-let.html')
lesson(3,'modules','Modules, visibility, packages, and crates',
'A package is managed by a Cargo manifest and can contain library and binary crates. Modules organize names inside a crate. Items are private by default; pub exposes an API, while pub(crate) limits access to the current crate. use imports a path into scope without copying or loading a runtime module.',
'mod pricing {\n    pub struct Quote { cents: u32 }\n    impl Quote {\n        pub fn standard() -> Self { Self { cents: 500 } }\n        pub fn cents(&self) -> u32 { self.cents }\n    }\n}\nuse pricing::Quote;\nfn main() { assert_eq!(Quote::standard().cents(), 500); }',
'Callers can obtain and inspect a quote but cannot write its private field directly outside pricing.',
'A library can expose a stable public interface while reorganizing internal modules.',
'Making everything pub couples consumers to implementation details.',
'How does a library crate differ from a binary crate?', 'ch07-02-defining-modules-to-control-scope-and-privacy.html')

lesson(4,'vectors','Vectors, capacity, and safe access',
'Vec<T> owns a growable contiguous allocation. Length counts initialized elements; capacity describes allocated room. push may reallocate, so references into the old buffer cannot survive a conflicting mutation. get returns an Option for uncertain indices, while indexing is appropriate when a valid index is already guaranteed.',
'fn main() {\n    let mut temperatures = Vec::with_capacity(4);\n    temperatures.extend([18, 21, 19]);\n    assert_eq!(temperatures.get(8), None);\n    temperatures.retain(|value| *value >= 19);\n    assert_eq!(temperatures, [21, 19]);\n}',
'Capacity reserves space but does not create elements. retain removes values that fail the predicate and preserves the order of remaining values.',
'A telemetry batch buffers measurements before sending them together.',
'with_capacity is an allocation hint, not a maximum size restriction.',
'What is amortized constant-time push, and when can an individual push be expensive?', 'ch08-01-vectors.html')
lesson(4,'strings','UTF-8 strings and Unicode boundaries',
'String owns UTF-8 bytes; &str borrows valid UTF-8. Byte offsets, Unicode scalar values, and displayed grapheme clusters are different units. chars iterates scalar values, while len counts bytes. Human-visible editing usually needs grapheme segmentation beyond the standard library.',
'fn main() {\n    let city = "Lima 🌊";\n    assert_eq!(city.len(), 9);\n    assert_eq!(city.chars().count(), 6);\n    assert_eq!(city.get(0..4), Some("Lima"));\n    assert_eq!(city.get(6..7), None);\n}',
'The wave occupies four bytes. The invalid byte range begins inside that encoding, so get returns None instead of slicing invalid text.',
'Search previews must truncate text at valid boundaries rather than arbitrary byte counts.',
'chars().count() still does not always count user-perceived characters.',
'How would you handle combining accents in a cursor-position API?', 'ch08-02-strings.html')
lesson(4,'maps','HashMap, HashSet, and ordered collections',
'HashMap associates keys with values; HashSet tracks uniqueness. The entry API combines lookup and conditional insertion with one logical operation. Hash iteration order is unspecified. BTreeMap provides sorted traversal when order is part of the contract. Select the data structure according to lookup and ordering needs.',
'use std::collections::{HashMap, BTreeSet};\nfn main() {\n    let mut counts = HashMap::new();\n    for color in ["blue", "red", "blue"] { *counts.entry(color).or_insert(0) += 1; }\n    assert_eq!(counts["blue"], 2);\n    let sorted: BTreeSet<_> = counts.keys().copied().collect();\n    assert_eq!(sorted.into_iter().collect::<Vec<_>>(), ["blue", "red"]);\n}',
'entry provides a mutable count, inserting zero when absent. The set gives deterministic sorted output separately from counting.',
'A metrics report groups events quickly and sorts labels only when displaying them.',
'Persisting raw HashMap iteration order creates flaky snapshots and unstable output.',
'What tradeoff makes a BTreeMap preferable for range queries?', 'ch08-03-hash-maps.html')
lesson(4,'iterators','Iterators, adapters, and closures',
'An iterator yields values through next. map and filter are lazy adapters; consumers such as sum and collect drive execution. iter borrows elements, iter_mut borrows mutably, and into_iter generally consumes the collection. Closures capture surrounding variables, with borrowing or moving chosen from how the body uses them.',
'fn main() {\n    let minimum = 10;\n    let orders = vec![4, 12, 20];\n    let total: i32 = orders.iter().copied().filter(|n| *n >= minimum).map(|n| n + 2).sum();\n    assert_eq!(total, 36);\n    assert_eq!(orders.len(), 3);\n}',
'Only 12 and 20 pass the filter; each gains 2. sum performs the work. The original vector remains available because iter only borrowed it.',
'An invoice pipeline transforms qualifying line items without manual indexing.',
'An unused lazy iterator may perform none of the side effects you expected.',
'How do Fn, FnMut, and FnOnce describe closure calling behavior?', 'ch13-02-iterators.html')

lesson(5,'result','Result and error propagation',
'Result<T,E> separates success from a recoverable error. The ? operator returns early on an error and can convert it through From. Handle errors where you have enough context to decide a policy; lower layers usually preserve detail rather than printing and continuing with invented defaults.',
'fn parse_port(text: &str) -> Result<u16, std::num::ParseIntError> {\n    let port = text.trim().parse::<u16>()?;\n    Ok(port)\n}\nfn main() {\n    assert_eq!(parse_port(" 8080 "), Ok(8080));\n    assert!(parse_port("70000").is_err());\n}',
'The numeric type enforces an upper bound. Invalid syntax and out-of-range numbers become errors instead of silently wrapping.',
'A service refuses an invalid configuration before opening a listening socket.',
'A syntactically valid port may still be invalid for your policy; parsing is not full domain validation.',
'Where should a command-line application turn a Result into an exit code?', 'ch09-02-recoverable-errors-with-result.html')
lesson(5,'error-types','Design meaningful domain errors',
'An error enum lets callers distinguish failures without parsing human-readable strings. A library should expose enough stable structure for recovery while keeping implementation details private. Display serves people; the Error trait supports diagnostic chains. Decide whether each failure is retryable, permanent, or a caller mistake.',
'#[derive(Debug, PartialEq)]\nenum ReserveError { Empty, NotEnough { available: u32 } }\nfn reserve(stock: u32, wanted: u32) -> Result<u32, ReserveError> {\n    if wanted == 0 { Err(ReserveError::Empty) }\n    else if wanted > stock { Err(ReserveError::NotEnough { available: stock }) }\n    else { Ok(stock - wanted) }\n}\nfn main() { assert_eq!(reserve(3, 4), Err(ReserveError::NotEnough { available: 3 })); }',
'The caller can offer a smaller order for NotEnough and reject an empty request separately.',
'An API translates domain failures into consistent client-facing responses without leaking database internals.',
'Returning one generic string prevents reliable automated recovery.',
'Which error details should be logged internally but omitted from an HTTP response?', 'https://doc.rust-lang.org/std/error/trait.Error.html')
lesson(5,'panic','Panics, unwinding, and recovery limits',
'A panic signals a failed assumption, not an ordinary invalid request. Depending on the panic strategy, Rust may unwind the stack or abort the process. catch_unwind catches unwinding panics only; it is not a general fault isolation boundary and does not undo side effects. Prefer Result for expected operational failures.',
'fn main() {\n    let result = std::panic::catch_unwind(|| {\n        panic!("demonstration of an internal failure");\n    });\n    assert!(result.is_err());\n}',
'With the usual unwinding strategy, the panic hook prints a diagnostic and catch_unwind returns Err. With panic=abort, this example terminates instead.',
'A plugin host may contain some unwinding failures, while a separate process provides a stronger isolation boundary.',
'Catching a panic does not prove shared state is still consistent.',
'Why should malformed user input not normally trigger panic!?', 'ch09-01-unrecoverable-errors-with-panic.html')
lesson(5,'validation','Validation, newtypes, and boundary contracts',
'A newtype wraps an existing type to express a distinct domain concept. Validate untrusted data once when constructing it, then pass the validated value internally. Keep its field private so callers cannot bypass the check. This reduces repeated defensive checks and makes units visible in function signatures.',
'struct Percent(u8);\nimpl Percent {\n    fn new(value: u8) -> Result<Self, &\'static str> {\n        if value <= 100 { Ok(Self(value)) } else { Err("percent exceeds 100") }\n    }\n    fn value(&self) -> u8 { self.0 }\n}\nfn main() { assert_eq!(Percent::new(25).unwrap().value(), 25); assert!(Percent::new(101).is_err()); }',
'Successful construction establishes the range invariant. Internal code works with Percent rather than guessing whether an arbitrary u8 was checked.',
'Separate types for user IDs, tenant IDs, cents, and percentages prevent accidental mixups.',
'Deserialization or public fields can bypass validation unless you deliberately route them through constructors.',
'What additional policy might be needed for a discount percentage?', 'ch20-03-advanced-types.html')

lesson(6,'generics','Generic functions and trait bounds',
'Generics describe behavior over multiple types without copying the implementation. Trait bounds state the operations required from those types. Rust normally monomorphizes generic code into concrete versions, enabling optimization but potentially increasing compile time and binary size. A bound should express the smallest useful contract.',
'fn repeated<T: Clone>(value: T) -> [T; 2] { [value.clone(), value] }\nfn main() {\n    assert_eq!(repeated(7), [7, 7]);\n    assert_eq!(repeated(String::from("ok")), ["ok", "ok"]);\n}',
'The first element needs a duplicate; the second can consume the original. Clone is sufficient, whereas requiring Copy would reject String.',
'A reusable buffering utility can support both small scalars and owned messages.',
'Generic code can still perform expensive clones; zero-cost abstraction is not a promise of zero work.',
'How does a where clause help with several complex bounds?', 'ch10-01-syntax.html')
lesson(6,'traits','Traits, default methods, and associated types',
'A trait defines a behavior contract that types can implement. Default methods can build on required methods. An associated type chooses a related type as part of an implementation, whereas a generic parameter can support multiple trait instantiations. Traits let consumers depend on behavior instead of a concrete storage implementation.',
'trait Source {\n    type Item;\n    fn next_item(&mut self) -> Option<Self::Item>;\n}\nstruct Once(Option<u32>);\nimpl Source for Once {\n    type Item = u32;\n    fn next_item(&mut self) -> Option<u32> { self.0.take() }\n}\nfn main() { let mut s = Once(Some(9)); assert_eq!(s.next_item(), Some(9)); assert_eq!(s.next_item(), None); }',
'The implementation fixes Item to u32. take moves the optional value out and leaves None, so the source yields at most once.',
'A pipeline can accept multiple sources with a common item contract.',
'Rust coherence rules restrict implementing foreign traits for foreign types; a local newtype is often the solution.',
'Why does Iterator use an associated Item type?', 'ch20-02-advanced-traits.html')
lesson(6,'dispatch','Static dispatch, dyn Trait, and impl Trait',
'A generic parameter or argument impl Trait typically uses static dispatch. A dyn Trait reference uses a vtable for runtime dispatch and can hide different concrete types behind one interface. Not every trait is dyn-compatible. Returning impl Trait hides one concrete return type, not an arbitrary mixture of unrelated types.',
'trait Alert { fn text(&self) -> &str; }\nstruct Email;\nimpl Alert for Email { fn text(&self) -> &str { "email" } }\nfn send(alert: &dyn Alert) -> &str { alert.text() }\nfn main() { assert_eq!(send(&Email), "email"); }',
'send works through a borrowed trait object. A vector of Box<dyn Alert> could own different implementations selected at runtime.',
'A service chooses a notification backend from configuration without exposing its concrete type to the caller.',
'Dynamic dispatch may complicate inlining; measure before assuming it is a bottleneck.',
'When would an enum be a better choice than a trait object?', 'ch18-02-trait-objects.html')
lesson(6,'closures','Closure captures and callback APIs',
'A closure can borrow or own its environment. move transfers captured values into the closure, which is useful when it must outlive the current scope. Fn can be called through a shared reference, FnMut may mutate captures, and FnOnce may consume them. Every closure supports FnOnce; some also support the stronger repeated-call traits.',
'fn apply_twice(mut action: impl FnMut()) { action(); action(); }\nfn main() {\n    let mut count = 0;\n    apply_twice(|| count += 1);\n    assert_eq!(count, 2);\n    let message = String::from("owned");\n    let consume = move || message;\n    assert_eq!(consume(), "owned");\n}',
'The counter closure needs mutable access. The second closure returns its captured String, consuming it, so it cannot be called twice.',
'Callback APIs can accept mutation for counters while one-shot tasks transfer ownership safely.',
'move changes capture ownership; it does not automatically mean the closure implements only FnOnce.',
'Why can a move closure still implement Fn?', 'ch13-01-closures.html')

lesson(7,'lifetimes','Lifetime relationships and elision',
'Lifetime annotations describe relationships between references; they do not extend how long data lives. A returned borrowed value must refer to data that remains valid. Elision rules infer many common signatures. Use explicit parameters when multiple inputs make the output relationship ambiguous.',
'fn first_line(text: &str) -> &str { text.lines().next().unwrap_or("") }\nstruct Document<\'a> { body: &\'a str }\nfn main() {\n    let owned = String::from("header\\nbody");\n    let doc = Document { body: &owned };\n    assert_eq!(first_line(doc.body), "header");\n}',
'Document borrows owned rather than storing a new string. It cannot be used after owned is dropped. The function output lifetime is inferred from its single reference input.',
'A parser can return borrowed fields into a request buffer to avoid copying.',
'Adding static cannot make a short-lived local reference valid.',
'When should you return an owned String instead of a borrowed &str?', 'ch10-03-lifetime-syntax.html')
lesson(7,'box-drop','Box, Deref, Drop, and RAII',
'Box<T> owns heap-allocated data and enables recursive types with a fixed-size outer representation. Deref lets smart pointers support reference-like access. Drop runs cleanup when ownership ends, a pattern called RAII. Cleanup should be predictable and generally avoid panicking, especially during an existing unwind.',
'enum Chain { Node(i32, Box<Chain>), End }\nfn main() {\n    let chain = Chain::Node(8, Box::new(Chain::End));\n    if let Chain::Node(value, tail) = chain {\n        assert_eq!(value, 8);\n        assert!(matches!(*tail, Chain::End));\n    }\n}',
'Box breaks the otherwise infinitely sized recursive layout. Moving out of chain transfers its boxed tail, which is then cleaned up normally.',
'File handles, lock guards, and transactions use scope-based cleanup to make resource ownership explicit.',
'A very deep recursively linked structure can overflow the stack during recursive destruction.',
'Why does a recursive enum require indirection?', 'ch15-01-box.html')
lesson(7,'rc-refcell','Rc, RefCell, Weak, and interior mutability',
'Rc provides shared ownership on one thread. RefCell permits mutation through a shared reference by checking borrowing rules at runtime; conflicting borrows panic. Weak observes an Rc allocation without keeping the value alive and helps break ownership cycles. These tools solve different problems: ownership sharing is separate from mutation permission.',
'use std::{rc::Rc, cell::RefCell};\nfn main() {\n    let shared = Rc::new(RefCell::new(2));\n    let other = Rc::clone(&shared);\n    *other.borrow_mut() += 3;\n    let observer = Rc::downgrade(&shared);\n    assert_eq!(*shared.borrow(), 5);\n    drop(other); drop(shared);\n    assert!(observer.upgrade().is_none());\n}',
'Both strong handles see the same cell. After both are dropped, the weak handle cannot recover the value.',
'A single-threaded UI can share model ownership while child-to-parent links remain weak.',
'Rc and RefCell do not become thread-safe merely by wrapping them in Arc.',
'How can a memory-safe Rc cycle still cause a memory leak?', 'ch15-05-interior-mutability.html')
lesson(7,'cow','Cow and allocation-aware API design',
'Cow represents borrowed or owned data and allocates only when ownership is needed. It is useful when many inputs can pass through unchanged but some require transformation. Compare it with always cloning: the caller gains an allocation-free fast path, at the cost of a more complex return type and lifetime relationship.',
'use std::borrow::Cow;\nfn normalize(input: &str) -> Cow<\'_, str> {\n    if input.contains(\'_\') { Cow::Owned(input.replace(\'_\', "-")) } else { Cow::Borrowed(input) }\n}\nfn main() {\n    assert!(matches!(normalize("blue"), Cow::Borrowed(_)));\n    assert_eq!(normalize("blue_sky"), "blue-sky");\n}',
'Unchanged input remains borrowed; replaced text is stored in a new owned allocation.',
'A configuration loader normalizes legacy spellings only when necessary.',
'Do not optimize allocations before measuring them; simpler owned APIs may be better at a boundary.',
'What happens when a caller needs the result to outlive the input?', 'https://doc.rust-lang.org/std/borrow/enum.Cow.html')

lesson(8,'unit-tests','Unit tests, integration tests, and documentation tests',
'Unit tests exercise small implementation units, integration tests use a crate as a consumer, and documentation tests keep examples executable. Test behavior at boundaries and include failure cases. A test that merely repeats the implementation can share its bug; derive expected outcomes independently.',
'fn shipping_free(total: u32) -> bool { total >= 1000 }\nfn main() {}\n#[cfg(test)]\nmod tests {\n    use super::*;\n    #[test]\n    fn threshold() { assert!(!shipping_free(999)); assert!(shipping_free(1000)); }\n}',
'Run with cargo test in a package, or rustc --test for a standalone file. The two assertions distinguish the exact threshold from the value below it.',
'A pricing change should retain tests for empty orders, boundary amounts, and invalid configurations.',
'Successful-path coverage alone misses error contracts and off-by-one failures.',
'What belongs in tests/ instead of a module-local test?', 'ch11-03-test-organization.html')
lesson(8,'property-tests','Properties, fuzzing, and regression inputs',
'Example tests check chosen inputs. Property tests describe relationships over many generated inputs. Fuzzing searches for crashes or invariant violations, often using instrumented builds. Neither technique proves correctness, but both reveal cases developers rarely write by hand. Preserve minimized failing inputs as regression fixtures.',
'fn main() {\n    for seed in 0..100 {\n        let mut values = vec![seed % 7, seed % 3, seed % 5];\n        let before_sum: i32 = values.iter().sum();\n        values.sort();\n        assert!(values.windows(2).all(|w| w[0] <= w[1]));\n        assert_eq!(values.iter().sum::<i32>(), before_sum);\n    }\n}',
'This deterministic illustration checks order and a weak preservation property. A real sorting property should compare full multisets, because equal sums can hide missing or changed elements.',
'Protocol parsers benefit from fuzzed byte streams and retained malformed-message samples.',
'A weak property such as equal sums is not sufficient to prove two collections contain the same elements.',
'What invariant would catch a parser accepting a truncated record?', 'https://rust-fuzz.github.io/book/')
lesson(8,'cargo-deps','Dependencies, lockfiles, features, and workspaces',
'Cargo resolves dependency versions and records a concrete graph in Cargo.lock. Features select optional capabilities and are generally additive across dependency users. A workspace coordinates multiple packages. Review changes to the resolved graph, including transitive dependencies, and test the feature combinations you actually support.',
'cargo tree\ncargo tree -e features\ncargo test --workspace\ncargo build --locked',
'The tree commands show dependency and feature relationships. Workspace tests cover member packages. --locked fails rather than silently updating a lockfile that needs changes.',
'A service release uses a reviewed lockfile so CI and deployment resolve the same package versions.',
'A direct dependency can pull a vulnerable transitive crate even when your manifest does not mention it.',
'Why can disabling default features on one dependency edge be insufficient?', 'https://doc.rust-lang.org/cargo/reference/features.html','shell')
lesson(8,'profiling','Benchmarking, profiling, and complexity',
'An algorithmic complexity estimate predicts how work scales; a benchmark measures one workload on one environment. Profile before changing code to find CPU or allocation hotspots. Use realistic input sizes, warmup where appropriate, release builds, and repeated measurements. Preserve correctness tests while optimizing.',
'fn main() {\n    let values: Vec<_> = (0..10_000).collect();\n    let start = std::time::Instant::now();\n    let found = std::hint::black_box(&values).binary_search(&7777);\n    std::hint::black_box(found).unwrap();\n    println!("illustrative elapsed: {:?}", start.elapsed());\n}',
'This shows timing mechanics, not a reliable benchmark: a single tiny operation is dominated by noise. Use a dedicated benchmark harness and many samples for decisions.',
'A backend team distinguishes expensive parsing from database latency before optimizing a hot path.',
'A faster microbenchmark may worsen end-to-end latency through contention or memory pressure.',
'How would you compare an O(n) scan with O(log n) search when sorting has a cost?', 'https://doc.rust-lang.org/std/hint/fn.black_box.html')

lesson(9,'threads','Threads, move closures, and joining',
'Operating-system threads execute concurrently. spawn needs owned or sufficiently long-lived captured data because a thread may outlive its caller. join waits for completion and reports a panic. Scoped threads can borrow local data because the scope waits for them before borrowed values disappear.',
'fn main() {\n    let samples = [3, 4, 5];\n    std::thread::scope(|scope| {\n        let worker = scope.spawn(|| samples.iter().sum::<i32>());\n        assert_eq!(worker.join().unwrap(), 12);\n    });\n}',
'The worker borrows samples safely because the thread scope cannot finish until its threads finish.',
'A CPU-heavy batch can partition independent chunks among workers.',
'Spawning one operating-system thread per small item can cost more than the work itself.',
'What does joining guarantee, and what does it not guarantee about shared data?', 'ch16-01-threads.html')
lesson(9,'arc-mutex','Arc, Mutex, RwLock, and lock scope',
'Arc shares ownership across threads through atomic reference counting. It does not make the contained data mutable or automatically safe. Mutex protects exclusive access; RwLock permits multiple readers or one writer. Keep critical sections short and define a consistent order when acquiring multiple locks.',
'use std::sync::{Arc, Mutex};\nfn main() {\n    let count = Arc::new(Mutex::new(0));\n    let worker_count = Arc::clone(&count);\n    let worker = std::thread::spawn(move || { *worker_count.lock().unwrap() += 1; });\n    worker.join().unwrap();\n    assert_eq!(*count.lock().unwrap(), 1);\n}',
'Both threads own a handle to one mutex. The guard releases the lock when its temporary scope ends.',
'A shared cache uses locks for short metadata updates and performs network work outside the lock.',
'unwrap on a poisoned lock is a policy choice, not universal recovery. Inspect protected invariants before proceeding.',
'Why can an RwLock perform worse than a Mutex under some workloads?', 'ch16-03-shared-state.html')
lesson(9,'channels','Channels and bounded queues',
'Message passing transfers data between workers and can simplify ownership. A bounded channel limits queued messages and applies backpressure when producers outrun consumers. Capacity is part of the resource budget, not just a tuning number. Channel disconnection is a normal shutdown condition that callers should handle.',
'fn main() {\n    let (tx, rx) = std::sync::mpsc::sync_channel(2);\n    let worker = std::thread::spawn(move || { tx.send(String::from("job")).unwrap(); });\n    assert_eq!(rx.recv().unwrap(), "job");\n    worker.join().unwrap();\n    assert!(rx.recv().is_err());\n}',
'The String moves through the channel. After the only sender is dropped and queued messages are drained, recv reports disconnection.',
'A worker pool uses a bounded queue to stop accepted work from exhausting memory.',
'A small queue does not bound the number of tasks waiting to send; admission control may also be needed.',
'When should a full queue block, reject, or drop work?', 'https://doc.rust-lang.org/std/sync/mpsc/fn.sync_channel.html')
lesson(9,'atomics','Send, Sync, atomics, and memory ordering',
'Send permits transferring a value between threads; Sync permits sharing references across threads. They describe safety properties, not scheduling behavior. Atomics support indivisible operations but memory ordering determines what other accesses become visible. Relaxed is appropriate for independent counters, not automatically for publishing related data.',
'use std::sync::atomic::{AtomicUsize, Ordering};\nfn main() {\n    let requests = AtomicUsize::new(0);\n    requests.fetch_add(1, Ordering::Relaxed);\n    assert_eq!(requests.load(Ordering::Relaxed), 1);\n}',
'The counter is updated atomically. No claim is made that observing it publishes some separate request buffer.',
'A metrics counter can often avoid a mutex when it has no cross-variable invariant.',
'Unsafe Send or Sync implementations require a complete safety argument; they are not fixes for inconvenient compiler errors.',
'What extra reasoning is required for release/acquire synchronization?', 'https://doc.rust-lang.org/std/sync/atomic/')

lesson(10,'futures','Async, await, futures, and runtimes',
'An async function returns a future that must be polled to make progress. await suspends the current future when an operation is pending; it does not create an operating-system thread. A runtime schedules tasks and supplies I/O and timer integration. Async is especially useful for many tasks waiting on external work.',
'async fn answer() -> u32 { 42 }\nasync fn request() -> u32 { answer().await + 1 }\nfn main() {\n    let pending = request();\n    drop(pending); // Never polled: request has not executed.\n}',
'This standard-library example compiles but intentionally does not execute the async body. In a service, a runtime drives the returned future.',
'An HTTP server can manage many waiting connections without a dedicated thread for each.',
'Creating a future is not the same as scheduling it, and async does not make CPU-heavy code parallel.',
'Why can a blocking loop inside async starve unrelated tasks?', 'https://tokio.rs/tokio/tutorial/async')
lesson(10,'tokio','Tokio tasks and blocking work',
'Use spawned async tasks for independent asynchronous work. Blocking system calls and long CPU computations can occupy executor threads and delay unrelated requests. spawn_blocking moves blocking work to a separate pool, but concurrency still needs limits. Await handles so errors and panics are observed.',
'// Cargo.toml: tokio = { version = "1", features = ["rt-multi-thread", "macros"] }\n#[tokio::main]\nasync fn main() -> Result<(), Box<dyn std::error::Error>> {\n    let text = tokio::task::spawn_blocking(|| std::fs::read_to_string("config.txt")).await??;\n    println!("{} bytes", text.len());\n    Ok(())\n}',
'Requires Tokio and a config.txt file. The first ? handles the task join error; the second handles the file read error. This is an external-crate example, not standalone rustc code.',
'A service isolates a legacy synchronous library from its async request executor.',
'Started blocking tasks generally cannot be aborted by aborting their handle; shutdown and timeouts need a separate policy.',
'How would you limit concurrent CPU-heavy blocking jobs?', 'https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html','rust-dependency')
lesson(10,'async-locks','Async locks, cancellation, and select',
'Any await can suspend a task, so consider what resources remain held and what happens if the future is dropped there. Prefer extracting owned data under a short synchronous lock, then awaiting after the guard leaves scope. select chooses among futures; losing branches are dropped, which can discard partial progress for operations that are not cancellation-safe.',
'use std::sync::Mutex;\nasync fn store_copy(shared: &Mutex<String>) -> String {\n    let snapshot = { shared.lock().unwrap().clone() };\n    std::future::ready(()).await;\n    snapshot\n}\nfn main() { let state = Mutex::new(String::from("ready")); drop(store_copy(&state)); }',
'The guard is confined to the inner block. The illustrative await happens only after release; a real implementation could send snapshot over the network.',
'A cache endpoint clones a small response before waiting on slow network I/O.',
'An async mutex can be held across await but may still serialize slow requests and create logical deadlocks.',
'What state must survive cancellation during a multi-step write?', 'https://tokio.rs/tokio/tutorial/select')
lesson(10,'shutdown','Timeouts and graceful shutdown',
'A reliable service separates detecting shutdown, notifying workers, and waiting for them. Stop accepting new work before draining existing work. Set a final deadline and define what unfinished work means. A timeout drops a future but does not necessarily undo remote side effects or stop already-running blocking code.',
'// Shutdown protocol sketch; not executable Rust.\nstop_accepting_new_requests()\nbroadcast_cancellation()\nwait_for_in_flight_work_until(deadline)\nflush_durable_state()\nreport_any_unfinished_jobs()',
'The order is the lesson: continued admission prevents draining. Durable jobs need a retry or recovery policy if the process reaches its deadline.',
'A deployment replaces service instances without silently losing accepted background jobs.',
'Killing a process after a grace period is not proof that every accepted operation completed.',
'How would you test shutdown while a worker is waiting on a slow dependency?', 'https://tokio.rs/tokio/topics/shutdown','pseudocode')

lesson(11,'unsafe','Unsafe Rust and safe abstraction boundaries',
'unsafe enables specific operations whose preconditions the compiler cannot fully verify. It does not disable all borrow checking or make undefined behavior acceptable. A safe public abstraction must uphold its promises for every input allowed by the safe API. Keep unsafe blocks small and state allocation, alignment, lifetime, and aliasing assumptions.',
'fn main() {\n    let value = 41u32;\n    let pointer = &value as *const u32;\n    // SAFETY: pointer comes from a live aligned u32; no mutation occurs.\n    let copy = unsafe { *pointer };\n    assert_eq!(copy, 41);\n}',
'The raw pointer remains valid because value is still alive and unmodified. The unsafe read is unnecessary here, but makes the required reasoning visible.',
'A low-level library may wrap a foreign buffer with a checked safe interface.',
'Passing tests does not establish the absence of undefined behavior.',
'Which safety condition fails if the pointer outlives value?', 'ch20-01-unsafe-rust.html')
lesson(11,'ffi','FFI, ABI, layout, and ownership',
'Foreign-function interfaces cross language boundaries where Rust cannot enforce the other side\'s promises. Agree on calling convention, data layout, string encoding, lengths, ownership, and cleanup. repr(C) provides C-compatible struct layout; it does not automatically make every field type suitable for C. Avoid letting unwinding cross an incompatible ABI boundary.',
'#[repr(C)]\nstruct Point { x: f64, y: f64 }\nextern "C" fn distance_squared(point: Point) -> f64 { point.x * point.x + point.y * point.y }\nfn main() { assert_eq!(distance_squared(Point { x: 3.0, y: 4.0 }), 25.0); }',
'This demonstrates a C-layout value and C calling convention inside one executable. Exporting a shared library requires additional build and symbol configuration.',
'A Rust component integrates with an existing C image-processing pipeline.',
'Never assume a foreign pointer is valid or free memory with a different allocator from the one that allocated it.',
'What must a C API document about who frees a returned buffer?', 'https://doc.rust-lang.org/nomicon/ffi.html')
lesson(11,'macros','Declarative and procedural macros',
'Macros generate code before normal type checking. macro_rules! matches token patterns and expands them; procedural macros run Rust code in a separate proc-macro crate and can derive implementations or transform annotated items. Prefer ordinary functions when they express the behavior clearly; generated code can make diagnostics and debugging harder.',
'macro_rules! tagged {\n    ($tag:expr, $value:expr) => { format!("[{}] {}", $tag, $value) };\n}\nfn main() { assert_eq!(tagged!("INFO", "ready"), "[INFO] ready"); }',
'The macro accepts two expressions and expands to a formatting expression. Its syntax is checked during expansion and its resulting types during compilation.',
'Derive macros reduce repetitive serialization or domain boilerplate across many structs.',
'A macro that evaluates an argument multiple times can duplicate side effects; review expansions.',
'When would a function be clearer than a macro?', 'ch20-05-macros.html')
lesson(11,'pin','Pin, Unpin, and self-referential futures',
'Some values rely on remaining at a stable address after being pinned, particularly compiler-generated futures with internal references. Pin restricts moving the pointee through safe APIs when it is not Unpin. Pinning is an API contract, not a general claim that an allocation can never be freed. Most application code should use established safe pinning helpers.',
'fn main() {\n    let mut pinned = Box::pin(12u32);\n    *pinned.as_mut().get_mut() += 1;\n    assert_eq!(*pinned, 13);\n}',
'u32 is Unpin, so get_mut is allowed. A type that is not Unpin intentionally prevents this unrestricted mutable access through Pin.',
'An async runtime polls pinned futures whose internal state may rely on address stability.',
'Pin<Box<T>> does not automatically validate an unsafe self-referential constructor.',
'Why is moving the Box handle different from moving its heap-allocated value?', 'https://doc.rust-lang.org/std/pin/')

lesson(12,'http','HTTP boundaries, serialization, and schema changes',
'A web boundary must parse bytes, validate a domain request, authorize it, execute a use case, and serialize a response. Serialization alone proves neither validity nor permission. Bound body sizes before allocating, reject unsupported content types, and plan how older clients behave when fields or enum variants change.',
'// Request-handling design sketch; framework-independent.\nread_body_with_limit(64_KiB)\ndecode_json_into_transport_type()\nauthenticate_and_authorize_resource()\nvalidate_into_domain_type()\nexecute_use_case()\nmap_domain_result_to_http_response()',
'Transport types describe wire representation; domain types establish invariants. Keep the distinction explicit so a deserialized field does not silently become trusted.',
'An order API rejects invalid quantities and cross-tenant access before altering inventory.',
'Returning internal error strings may leak credentials, SQL details, or filesystem paths.',
'Which schema changes preserve compatibility for old clients?', 'https://serde.rs/','pseudocode')
lesson(12,'database','Transactions, idempotency, and connection pools',
'Database transactions group changes under a chosen isolation level. A pool limits and reuses connections, but does not automatically make application operations atomic. Idempotency keys identify retried logical operations; enforce uniqueness in durable storage rather than a process-local map. Keep external network calls outside long-held database transactions where possible.',
'BEGIN;\n-- Require a UNIQUE constraint on request_key.\nINSERT INTO accepted_requests(request_key) VALUES (:key);\nUPDATE inventory SET stock = stock - :qty\nWHERE sku = :sku AND stock >= :qty;\n-- Check exactly one row changed; otherwise ROLLBACK.\nCOMMIT;',
'This SQL sketch needs conflict handling and stored response data for duplicate keys. The conditional update prevents overselling for the targeted row; do not commit when the update affected zero rows.',
'A checkout retry should return the original outcome rather than reserve stock twice.',
'A local transaction cannot atomically commit a remote payment; use a durable workflow or outbox with reconciliation.',
'What happens if the process crashes after commit but before replying?', 'https://www.sqlite.org/lang_transaction.html','sql')
lesson(12,'observability','Tracing, metrics, and useful diagnostics',
'Logs describe individual events, metrics aggregate behavior, and traces connect work across request boundaries. Record latency, queue depth, error classification, and correlation IDs. Instrument boundaries so you can distinguish waiting from computation. Keep sensitive payloads out of logs and control high-cardinality labels.',
'use std::time::Instant;\nfn main() {\n    let start = Instant::now();\n    let request_id = "demo-17";\n    // Structured tracing libraries are preferable in a service.\n    eprintln!("request_id={request_id} operation=health elapsed_us={}", start.elapsed().as_micros());\n}',
'The example establishes correlation and duration without printing request secrets. A tracing subscriber can later collect structured spans across async tasks.',
'On-call engineers can identify whether a latency spike comes from a queue, database, or downstream call.',
'User IDs as metric labels can create unbounded time-series cardinality.',
'Which measurements would distinguish overload from a slow external dependency?', 'https://tokio.rs/tokio/topics/tracing')
lesson(12,'release','Reproducible releases and dependency security',
'A release should identify its source revision, compiler, target, lockfile, and build configuration. Run tests and review dependency advisories before deploying. A clean audit only covers known database entries at scan time, not all possible vulnerabilities. Rollouts need health checks and a rollback plan, including compatibility of stored data.',
'cargo test --locked\ncargo build --release --locked\ncargo tree -d\n# With cargo-audit installed separately:\ncargo audit',
'The build uses the reviewed lockfile. Duplicate versions in the dependency tree deserve inspection, especially if only one copy received a security patch.',
'A release process records evidence needed to reproduce a production binary and investigate regressions.',
'Updating Cargo.toml without rebuilding and redeploying leaves the running vulnerable binary unchanged.',
'How would you verify which dependency version is actually running?', 'https://rustsec.org/','shell')

lesson(13,'const-generics','Const generics and compile-time evaluation',
'Const generics parameterize types or functions by compile-time values such as an array length. const fn allows eligible operations in constant evaluation as well as ordinary calls. Compile-time computation has restrictions, and not every expression involving generic constants is supported in all positions on stable Rust.',
'const fn square(n: usize) -> usize { n * n }\nfn width<const N: usize>(_: &[u8; N]) -> usize { N }\nconst GRID: usize = square(4);\nfn main() { assert_eq!(GRID, 16); assert_eq!(width(&[0; 8]), 8); }',
'GRID is calculated at compile time. width infers N from the array type, which carries its length in the type system.',
'A fixed-size packet or matrix API can enforce dimensions before runtime.',
'Const generics can increase the number of compiled instantiations; they do not replace runtime validation for external data.',
'When should a dimension stay dynamic instead of becoming part of a type?', 'https://doc.rust-lang.org/reference/items/generics.html')
lesson(13,'advanced-lifetimes','Variance, higher-ranked bounds, and GATs',
'Advanced generic APIs sometimes need to work for every borrow lifetime rather than one chosen lifetime. A higher-ranked bound expresses that requirement. Generic associated types let associated types depend on parameters such as the lifetime of a borrow. Variance determines which lifetime substitutions are valid; mutable references are invariant in their pointee type.',
'fn inspect<F>(f: F) -> usize\nwhere F: for<\'a> Fn(&\'a str) -> usize { f("local") }\ntrait Lending {\n    type Item<\'a> where Self: \'a;\n    fn get(&self) -> Self::Item<\'_>;\n}\nimpl Lending for String {\n    type Item<\'a> = &\'a str;\n    fn get(&self) -> &str { self.as_str() }\n}\nfn main() { assert_eq!(inspect(|s| s.len()), 5); assert_eq!(String::from("x").get(), "x"); }',
'inspect accepts a callback valid for any input lifetime. Lending ties its returned associated type to the borrow of self.',
'A streaming parser can lend views into an internal buffer instead of allocating every item.',
'Do not add lifetime parameters until you can explain the relationship each one represents.',
'Why can an iterator lending from its own mutable buffer need a different API from Iterator?', 'https://doc.rust-lang.org/reference/items/associated-items.html')
lesson(13,'no-std','no_std, embedded targets, and allocation budgets',
'no_std removes the automatic standard-library dependency and uses core, which provides fundamental types and traits without operating-system services. alloc can add heap-backed collections when an allocator exists. Embedded programs must supply platform-specific startup, panic handling, and peripheral access. Resource budgets and interrupt behavior become part of API design.',
'#![no_std]\n// Library example: compile with rustc --crate-type lib.\npub fn checksum(bytes: &[u8]) -> u8 {\n    bytes.iter().fold(0, |sum, byte| sum.wrapping_add(*byte))\n}',
'This library performs no allocation and does not need a main function. It can be tested from a separate standard-library test harness.',
'A small sensor node computes packet checksums within a fixed memory budget.',
'A library using no_std is not automatically suitable for every target or interrupt context.',
'Which dependencies would prevent your library from building without an OS?', 'https://docs.rust-embedded.org/book/intro/no-std.html','rust-library')
lesson(13,'wasm','WebAssembly and a practical capstone',
'Rust can target WebAssembly, but browser APIs require bindings and the execution environment differs from a native process. Design a small portable core with explicit inputs and outputs, then add platform adapters. For interview preparation, build one complete application and explain ownership, error handling, concurrency, and deployment decisions together.',
'pub fn estimate_bytes(width: u32, height: u32) -> Option<u32> {\n    width.checked_mul(height)?.checked_mul(4)\n}\nfn main() { assert_eq!(estimate_bytes(640, 480), Some(1_228_800)); }',
'This pure core can be reused in native or WebAssembly code. A real browser export needs a wasm target and bindings; this example deliberately has no browser integration.',
'Capstone: build an image-job service with validated sizes, bounded workers, persistent job status, cancellation, metrics, tests, and a thin browser client.',
'Compilation to WebAssembly does not provide DOM access or make native filesystem APIs available.',
'Explain how you would test the shared core separately from browser and database adapters.', 'https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Rust_to_Wasm')

from course_extension import register
from course_chapters import enrich
register(lesson)
MODULE_DETAILS = enrich(LESSONS, MODULES)
from book_path import arrange
MODULES, MODULE_DETAILS = arrange(LESSONS)
from topic_course import organize
MODULES, MODULE_DETAILS = organize(LESSONS)
