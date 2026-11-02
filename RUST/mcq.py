"""Original single-answer Rust questions. Keys stay on the server until submission."""
QUESTIONS=[]
def q(topic,prompt,correct,wrong1,wrong2,wrong3,explanation,code=''):
    # Rotate authored options so correct answers are not always in the first slot.
    entries=[correct,wrong1,wrong2,wrong3];rotation=len(QUESTIONS)%4
    options=entries[rotation:]+entries[:rotation]
    QUESTIONS.append(dict(id=f'mcq-{len(QUESTIONS)+1:03d}',topic=topic,prompt=prompt,code=code,
                          options=[x[0] for x in options],answer=(-rotation)%4,
                          rationales=[x[1] for x in options],explanation=explanation))

q('Foundations','Which command checks a Cargo project without producing its final executable?',
 ('cargo check','It performs compilation checks without the final executable build.'),('cargo run','This builds and runs an executable.'),('cargo fmt','This formats source; it does not type-check the program.'),('cargo clean','This removes generated build artifacts.'),
 'Use check for fast compiler feedback, test for behavioral checks, and run when you want to execute the program.')
q('Foundations','Why does this function fail to satisfy its declared return type?',
 ('The final semicolon discards the integer value.','The body then produces unit, not i32.'),('The literal 7 must have a suffix.','The return type provides enough inference for this literal.'),('Functions cannot return literals.','A literal is a valid return expression.'),('Every function requires return.','Rust permits a trailing expression without return.'),
 'Remove the semicolon or use an explicit return. Statements and value-producing expressions have different roles.', 'fn number() -> i32 { 7; }')
q('Foundations','What does the second let do?',
 ('Creates a new binding that shadows the earlier one.','The new binding may have a different type.'),('Mutates the original String in place.','The original value here is a string slice, and parsing creates a number.'),('Changes the type of an existing mutable variable.','No mutable variable is being reassigned.'),('Causes a duplicate-name error.','Shadowing is legal in this scope.'),
 'Shadowing introduces a new binding; mut permits reassignment to one existing binding with its established type.', 'let count = "12";\nlet count: u32 = count.parse().unwrap();')
q('Foundations','Which operation reports failure rather than truncating when converting 300u16 to u8?',
 ('u8::try_from(300u16)','TryFrom returns an error because the value does not fit.'),('300u16 as u8','This narrowing cast discards high bits.'),('u8::from(300u16)','This infallible conversion is not implemented for arbitrary u16 values.'),('300u16.to_string()','This produces text, not a checked byte conversion.'),
 'Choose a fallible conversion when the range is not guaranteed by the source type.')
q('Ownership','Why is the last line rejected?',
 ('The String moved into second.','first no longer owns the value.'),('println! always consumes every argument.','Formatting is not the source of this move.'),('String cannot be printed.','String supports the formatting used here.'),('Both variables require mut.','Mutability does not restore moved ownership.'),
 'Assignment moves non-Copy owned values. Borrow or explicitly clone if both paths must access the text.', 'let first = String::from("notes");\nlet second = first;\nprintln!("{first}");')
q('Ownership','A function only reads UTF-8 text and does not retain it. Which parameter is generally most flexible?',
 ('&str','It accepts borrowed views from String and string literals.'),('&String','It unnecessarily requires a String container.'),('String','This transfers ownership when only reading is required.'),('&mut String','This requests exclusive mutation access unnecessarily.'),
 'Ask for the capability the function needs. A borrowed string slice avoids unnecessary ownership and container constraints.')
q('Ownership','Why can push conflict with the later println! here?',
 ('Growth may invalidate the borrowed element.','The immutable element borrow is used after a potentially reallocating mutation.'),('Vec never allows push after creation.','Growing a mutable vector is legal when borrow rules permit it.'),('println! needs an exclusive borrow.','It can format through shared access.'),('Integers cannot be stored by reference.','References to integers are valid while their owners and access rules remain valid.'),
 'End the element borrow before mutating, or copy the small Copy element if an independent value is intended.', 'let mut values = vec![1, 2];\nlet first = &values[0];\nvalues.push(3);\nprintln!("{first}");')
q('Ownership','What does cloning an Rc<String> with Rc::clone do?',
 ('Creates another shared owner of the same allocation.','It increments the strong reference count.'),('Copies the full String into an independent allocation.','That describes cloning the String itself, not the Rc handle.'),('Creates a weak observer.','Rc::downgrade creates a Weak reference.'),('Makes the value thread-safe.','Rc does not provide cross-thread ownership.'),
 'Identify which layer is cloned. Smart-pointer handle cloning and pointee cloning have different semantics and costs.')
q('Collections & text','What does String::len report?',
 ('The number of UTF-8 bytes.','It measures the encoded storage length.'),('The number of visible characters.','Grapheme clusters can contain several Unicode scalars.'),('Always the same value as chars().count().','Multibyte scalars make these counts differ.'),('The allocation capacity.','Capacity is a separate property.'),
 'Byte length, Unicode scalar count, and grapheme count are distinct units.')
q('Collections & text','What can text.get(1..2) return when the range splits a multibyte character?',
 ('None','get rejects invalid UTF-8 boundaries without panicking.'),('An invalid UTF-8 &str','Safe string slicing does not create invalid str values.'),('A replacement character automatically','get does not rewrite the encoding.'),('A guaranteed panic','Direct indexing can panic; get uses Option.'),
 'Use get for a fallible byte range, and define whether your application needs byte, scalar, or grapheme boundaries.')
q('Collections & text','A report must have keys in sorted order. Which collection supplies ordered key iteration?',
 ('BTreeMap','It maintains keys in sorted order.'),('HashMap','Its iteration order is not a sorted-output contract.'),('HashSet','It is a set and does not provide sorted key/value iteration.'),('VecDeque','It preserves queue order, not automatic key order.'),
 'Alternatively sort at the presentation boundary. Choose based on update and query needs, not only average lookup cost.')
q('Collections & text','What is guaranteed after Vec::<u8>::with_capacity(10)?',
 ('Length is zero and capacity is at least ten.','Reservation allocates room without initializing ten elements.'),('There are ten zero-valued elements.','Use an initialized vector such as vec![0; 10] for that.'),('The vector cannot grow beyond ten.','Capacity is not a maximum size limit.'),('Index zero is valid.','The vector still contains no elements.'),
 'Length counts initialized elements; capacity measures available storage.')
q('Errors & patterns','What does ? do when applied to an Err inside a compatible Result-returning function?',
 ('Returns early, converting the error where supported.','It propagates the failure to the caller.'),('Logs the error and continues.','Logging is not part of the operator.'),('Panics automatically.','Propagation is different from unwrap.'),('Retries the operation.','Retry policy must be implemented separately.'),
 'Propagation preserves the distinction between detecting an error and deciding recovery or presentation policy.')
q('Errors & patterns','Which type best represents an optional profile nickname when absence is normal?',
 ('Option<String>','It explicitly models presence or absence.'),('String with a magic value "NONE"','A sentinel can collide with legitimate text and hides the contract.'),('A raw null pointer','This adds unsafe concerns without expressing the domain as clearly.'),('Result<String, panic>','panic is not an error type, and ordinary absence is not a panic.'),
 'Use Result when failure reasons matter; use Option when presence versus absence is the required information.')
q('Errors & patterns','Which match arm returns the result for (0, 0)?',
 ('The first arm.','Arms are evaluated in order; the origin matches immediately.'),('The diagonal arm.','Its condition is true, but an earlier matching arm already wins.'),('Both arms run.','A match selects one arm.'),('The wildcard arm.','The earlier specific arm matches first.'),
 'Ordering matters when patterns or guards overlap.', 'match (0, 0) {\n    (0, 0) => "origin",\n    (x, y) if x == y => "diagonal",\n    _ => "other",\n}')
q('Errors & patterns','What does catch_unwind guarantee about external side effects before a caught panic?',
 ('It does not roll them back.','Catching an unwind is not a transaction.'),('All file writes are reverted.','Filesystem writes are not automatically undone.'),('Remote requests are cancelled.','Remote effects can already have occurred.'),('It catches panic=abort too.','Aborting does not unwind into this handler.'),
 'Recovery requires understanding which invariants and side effects remain after failure.')
q('Traits & lifetimes','What do explicit lifetime annotations primarily describe?',
 ('Relationships and validity constraints between references.','They express requirements checked by the compiler.'),('A way to keep local allocations alive longer.','Annotations do not extend storage lifetime.'),('Runtime timers for objects.','They do not create runtime countdowns.'),('Automatic cloning of borrowed values.','Ownership duplication is a separate operation.'),
 'If a result must outlive its input, it may need to own the data rather than borrow it.')
q('Traits & lifetimes','A function returns impl Display. Can its branches return unrelated concrete types just because both implement Display?',
 ('No; the function must select one concrete hidden return type.','Use an enum or suitable trait object for heterogeneous alternatives.'),('Yes, impl Trait is automatic runtime dispatch.','It normally hides one concrete type rather than creating a trait object.'),('Yes, if both values have the same byte size.','Equal size does not make unrelated types identical.'),('No, because Display cannot be a return bound.','Display can be used as an impl Trait bound; the branch types are the issue.'),
 'Distinguish a hidden concrete type from a dynamically dispatched trait object.')
q('Traits & lifetimes','Which is true about a move closure that only reads its captured String?',
 ('It can implement Fn.','Owning a capture does not imply consuming it during a call.'),('It must implement only FnOnce.','Call behavior, not move alone, determines the repeated-call capabilities.'),('It cannot capture a String.','Owned String capture is valid.'),('It must copy the String on every call.','Reading the captured value does not require cloning.'),
 'Capture mode and invocation behavior are different dimensions of a closure contract.')
q('Traits & lifetimes','Why might a public API use a newtype instead of a type alias for UserId?',
 ('A newtype creates a distinct type that can prevent accidental mixing.','A type alias does not create a separate nominal type.'),('Aliases always allocate on the heap.','Aliases do not change storage by themselves.'),('Newtypes automatically validate every external input.','Validation must still be implemented and protected by visibility.'),('Newtypes remove all runtime checks.','Contextual business and authorization checks can remain necessary.'),
 'Use newtypes for meaningful type distinctions and controlled construction, not as a replacement for all domain policy.')
q('Iterators & testing','Why does the mapping closure not run here?',
 ('The lazy iterator is never consumed.','Adapters describe work until a consumer requests items.'),('map only works with Strings.','It is generic over item types.'),('println! is forbidden inside a closure.','It is allowed, though side effects in lazy pipelines require care.'),('iter consumes the vector immediately.','iter borrows; it does not eagerly visit every item.'),
 'A for loop, collect, sum, or another consumer can drive the pipeline.', 'let values = vec![1, 2];\nlet pending = values.iter().map(|n| println!("{n}"));\ndrop(pending);')
q('Iterators & testing','For an owned Vec<String>, what does into_iter yield?',
 ('Owned String values.','Consuming the vector transfers its elements to iteration.'),('Only shared &String references.','That is the usual behavior of iter.'),('Only mutable references.','That is the usual behavior of iter_mut.'),('UTF-8 bytes from every string.','The iterator yields vector elements, not a flattened byte stream.'),
 'Read the Item type and whether the iterator borrows or consumes its source.')
q('Iterators & testing','Which tests best distinguish a free-shipping rule total >= 1000 from total > 1000?',
 ('Include exactly 1000.','The implementations differ at the threshold.'),('Only test 2000.','Both implementations accept 2000.'),('Only test zero.','Both implementations reject zero.'),('Only check that the function compiles.','Compilation cannot infer the business boundary.'),
 'Test the boundary and neighboring values, deriving expected results from the requirement.')
q('Iterators & testing','Which property is insufficient by itself to prove sorting preserved all elements?',
 ('The output sum equals the input sum.','Different multisets can have the same sum.'),('The full frequency map is unchanged.','That checks multiset preservation, though order still needs a separate check.'),('The output is both sorted and a permutation.','These together express the usual sorting contract.'),('Each distinct value has the same multiplicity.','This describes multiset preservation.'),
 'For example, [1,4] and [2,3] have equal sums but different elements.')
q('Concurrency','What does Arc provide by itself?',
 ('Thread-safe reference counting for shared ownership.','Mutation and pointee thread safety remain separate concerns.'),('Exclusive mutable access to all contained data.','Use suitable synchronization for mutation.'),('Automatic deadlock prevention.','Ownership counting does not order locks.'),('Thread safety for any T, including RefCell<T>.','Arc does not make an unsuitable pointee safely shareable across threads.'),
 'Arc and Mutex solve different problems. Sharing ownership is not permission for unsynchronized mutation.')
q('Concurrency','Why does a bounded channel alone not necessarily bound total memory?',
 ('Waiting senders and in-flight work can retain additional payloads.','Capacity only bounds the queued portion.'),('Bounded channels ignore their configured capacity.','The queue bound is meaningful; it is not the entire system.'),('Every message is automatically persisted.','Channel storage is not automatically durable.'),('Consumers cannot remove messages.','Consumers do drain messages; the issue is work outside the queue.'),
 'Bound admission, running work, and payload sizes as well as queue capacity.')
q('Concurrency','What does a poisoned mutex indicate?',
 ('A panic while holding the lock may have left invariants broken.','The protected state needs a deliberate recovery policy.'),('The operating system permanently destroyed the mutex.','Poisoning is not that OS condition.'),('Data has definitely been repaired.','Poisoning warns of possible inconsistency.'),('All later lock attempts are automatically safe to ignore.','Ignoring poison does not validate the data.'),
 'Find the original panic and inspect the invariant; recovering a guard is not the same as repairing state.')
q('Concurrency','When can Relaxed ordering be suitable?',
 ('For an independent atomic metrics counter with no publication invariant.','No separate data visibility is being promised by that counter.'),('Whenever a flag publishes a separate non-atomic buffer.','That requires a synchronization argument beyond atomicity alone.'),('Whenever two values must change atomically together.','Two atomics do not automatically form a transaction.'),('Only on single-threaded programs.','Relaxed atomics can be useful across threads.'),
 'Choose ordering from the invariant and visibility relationship, not from a guess about performance.')
q('Async','What happens when an async function is called but its returned future is never polled?',
 ('Its async body does not progress.','Constructing the future is not executing it to completion.'),('It automatically gets a new OS thread.','Async does not imply thread creation.'),('It runs to the first await immediately.','An async function body is driven by polling.'),('It is automatically queued on Tokio.','A runtime must be explicitly involved in driving or spawning it.'),
 'Identify who owns and polls a future. Unused futures do not perform their promised work.')
q('Async','Does aborting the handle of an already-running spawn_blocking task reliably stop its work?',
 ('No.','Started blocking work generally continues; cancellation needs a separate design.'),('Yes, at the next machine instruction.','Tokio does not provide that preemption guarantee.'),('Yes, if the caller has a timeout.','A timeout can stop waiting without stopping the worker.'),('Yes, because all closures are cooperative futures.','A blocking closure is not an async future that yields on await.'),
 'Bound blocking concurrency and plan shutdown for work that cannot be force-cancelled through its handle.')
q('Async','Why is holding a synchronous mutex guard across await dangerous?',
 ('A waiting task can block a thread needed by the suspended lock owner.','This can prevent progress and can also violate Send requirements.'),('await automatically releases all guards.','Live local resources can survive suspension.'),('Mutex locks become read-only in async code.','The mutation contract does not change that way.'),('Every async function has a dedicated thread.','Tasks may share executor threads.'),
 'Keep synchronous critical sections short and end their scope before asynchronous waiting where possible.')
q('Async','A request times out after sending a remote operation. What can be concluded about the remote side effect?',
 ('Its outcome may be unknown.','The remote system may already have committed.'),('It definitely did not happen.','Local cancellation is not remote rollback.'),('It must happen exactly twice.','A timeout does not dictate the number of effects.'),('Retrying without a key is always safe.','Non-idempotent operations can duplicate effects.'),
 'Use durable idempotency and reconciliation where the logical operation must not be repeated blindly.')
q('Advanced Rust','What does unsafe mean at a raw-pointer dereference?',
 ('The programmer must uphold safety preconditions the compiler cannot fully prove.','Validity, alignment, lifetime, initialization, and aliasing still matter.'),('All borrow checking is disabled in the crate.','Unsafe does not disable all language checks.'),('Invalid memory access becomes defined behavior.','Undefined behavior remains invalid.'),('The pointer now owns the allocation.','Dereferencing does not confer ownership.'),
 'A safety comment should explain why the preconditions hold, not merely label the block safe.')
q('Advanced Rust','What does repr(C) on a suitable struct primarily address?',
 ('C-compatible data layout.','It helps specify the layout at the ABI boundary.'),('Automatic ownership transfer to C.','Ownership requires an explicit contract.'),('Automatic null-pointer validation.','Pointer validation remains the API’s responsibility.'),('Making every Rust field type FFI-safe.','Some Rust types still have unsuitable representation or ownership semantics.'),
 'Layout, calling convention, validity, and ownership are separate parts of FFI design.')
q('Advanced Rust','Why can a Pin<Box<T>> handle move while its pointee stays at a stable address?',
 ('Moving the owning pointer is distinct from moving the heap allocation.','The box handle can relocate without relocating T.'),('Pin copies T on each move.','That would defeat address stability.'),('Pin prevents the value from ever being destroyed.','Pinning is not immortality.'),('All T automatically implement Unpin.','Some types intentionally do not.'),
 'Pin constrains operations on an address-sensitive pointee through its contract; it does not freeze every handle’s stack location.')
q('Advanced Rust','What is a possible hazard when a macro expands an argument expression twice?',
 ('The argument’s side effects can occur twice.','Macro expansion generates repeated evaluation sites.'),('Rust always evaluates macro arguments exactly once.','The expansion determines evaluation behavior.'),('Macros run only at runtime.','Expansion occurs before ordinary type checking and execution.'),('The compiler automatically deduplicates side effects.','It cannot silently remove required effects.'),
 'Inspect expansions and prefer a function when ordinary value abstraction is sufficient.')
q('Production','Why can TCP return only part of a message in one read?',
 ('TCP exposes a byte stream, not application message boundaries.','Framing must be implemented by the application protocol.'),('TCP guarantees each write equals one read.','No such correspondence is guaranteed.'),('Partial reads always indicate corrupted data.','They are normal stream behavior.'),('All reads wait for the connection to close.','Reads can return available bytes earlier.'),
 'Retain incomplete input and decode complete frames while preserving any trailing bytes.')
q('Production','Which change addresses two processes overselling inventory from a read-then-write race?',
 ('Use a conditional database update and verify rows affected.','The database enforces the stock condition across processes.'),('Add a mutex only inside one process.','Another process does not share that mutex.'),('Increase the connection pool without changing the query.','More connections do not make the operation atomic.'),('Sleep briefly between read and write.','Timing does not enforce the invariant.'),
 'Group related writes transactionally and handle duplicate logical requests as well as concurrent distinct ones.')
q('Production','An old vulnerable crate remains after updating a direct dependency. What should you inspect?',
 ('All resolved versions and reverse dependency paths.','Another parent may still require an older version.'),('Only the top-level package name.','The vulnerable crate may be transitive.'),('Only source formatting.','Formatting does not affect dependency resolution.'),('Only the latest published version on crates.io.','Availability of a fix does not prove it is resolved or deployed.'),
 'Inspect Cargo.lock and cargo tree, then rebuild and verify the running artifact.')
q('Production','Which metric label is most likely to cause unbounded cardinality?',
 ('A unique request ID on every time series.','Each distinct ID creates another label combination.'),('A small fixed set of HTTP method names.','This is usually bounded.'),('A fixed success/error classification.','This is a small bounded vocabulary.'),('A fixed region list.','A controlled region list is bounded.'),
 'Use traces or logs for high-cardinality correlation IDs; use bounded categories for aggregate metrics.')

def public_questions():
    return [{key:value for key,value in question.items() if key not in ('answer','rationales','explanation')} for question in QUESTIONS]
