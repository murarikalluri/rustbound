# Rustbound: learn one topic at a time

92 individual topic modules, 40 production scenarios, 40 MCQs, and a separate 100-question coding course.

Every learning page follows five sections: what it is and how it works; real-life use; syntax; an example; one simple lab. Open A closer look for technical detail. Syntax sketches may contain placeholders; example labels distinguish runnable code from commands and design sketches.

The official Rust Book guides the learning areas, but each topic is its own module. Existing lesson IDs and reading completions are preserved. Advanced topics require earlier knowledge; younger learners can work with a helper.

This is an original teaching curriculum, not an exhaustive list of every crate or unstable Rust feature. Reading and lab completion are self-assessed.

## Choose your path

First steps: six guided activities covering a greeting, variables, integer addition, if/else, loops, and a function. Predict the output, edit a value in a fixed template, compare the preview, then try a transfer task in real Rust. Activities support a helper, optional read-aloud, and account-saved completion. They are not compiler-graded challenges.

Developer path: use the topic library and independent project briefs. Build a packing-list CLI, receipt calculator, text-search tool, bounded worker queue, async client, and a service with stored data. Each brief includes acceptance criteria, edge cases, a failure investigation, and a deliverable. Project work is self-reviewed.

## Installing Rust

Before cooking, you need a kitchen. Before running Rust, you need its tools. rustup installs the compiler; the compiler checks your instructions and builds a program your computer can run.

Project: Create a rust-study folder and write down the full path.

- Day 1: Installing Rust

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch01-00-getting-started.html)

## Hello, world!

A program is a list of instructions. This first program asks the computer to say hello. It starts at main, follows the instruction inside the braces, then finishes.

Project: Type the example yourself and run it once.

- Day 2: Hello, world!

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch01-00-getting-started.html)

## Cargo

Cargo is your project helper. It keeps the project settings together and asks Rust to check, build, or run your code. You run its commands in a terminal from your project folder.

Project: Create a package named study_cli and find its manifest and entry point.

- Day 3: Cargo

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch01-00-getting-started.html)

## Compiler messages

The compiler checks your code before it runs. If something does not fit Rust's rules, it shows you where to look. Read the first message carefully, make one change, and check again.

Project: Create a deliberate type mismatch by assigning text to an explicitly typed integer.

- Day 4: Compiler messages

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch01-00-getting-started.html)

## Printing and formatting

Printing shows a message. Formatting puts values into that message, like filling a name into a greeting card. format! creates text you can keep; println! writes text to the screen.

Project: Print a user-facing message to stdout and a diagnostic to stderr.

- Day 5: Printing and formatting

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch01-00-getting-started.html)

## Project: a guessing game

The player guesses a number and the program says whether it is too high, too low, or correct. Build one small step at a time. Keep the comparison easy to test even when the final game chooses a random secret.

Project: Read the official chapter, then run the deterministic core above.

- Day 6: Project: a guessing game

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html)

## Variables

A variable is a name you give a value so you can use it later. Imagine putting a name label on a score. In Rust, a value cannot be reassigned through that name unless you allow changes with mut.

Project: Create a variable named apples with value three. Print it and check that it is three.

- Day 7: Variables

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Changing a variable

Some values need to change, like a score after winning a point. mut tells Rust that you intend to change a binding. Without it, accidental reassignment is rejected before the program runs.

Project: Start with two points, add three, and check that the final score is five.

- Day 8: Changing a variable

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Constants

A constant gives a name to a value known at compile time. Think of the number of minutes in an hour: the name explains the number and the value is not reassigned.

Project: Define SECONDS_PER_MINUTE and calculate the number of seconds in three minutes.

- Day 9: Constants

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Shadowing

Shadowing gives a new value an existing name with another let. It is useful when the same idea changes form, such as text becoming a number. The new binding hides the old one in that scope.

Project: Change the input to "8" and check that adding one produces nine.

- Day 10: Shadowing

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Integers

An integer is a whole number, such as three apples or minus two degrees. Rust's integer types have different ranges. Choosing a type tells the computer which whole numbers you need to represent.

Project: Give a signed variable the value minus five, add two, and check that the result is minus three.

- Day 11: Integers

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Booleans

A boolean is either true or false. It answers a yes-or-no question, such as whether a door is open. Comparisons produce booleans that can control a decision.

Project: Set count to zero and check that !available is true.

- Day 12: Booleans

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Decimal numbers

Floating-point numbers represent values with fractional parts, such as a measured temperature. Many decimal fractions are only approximations in this representation, so calculations need a suitable accuracy rule.

Project: Calculate half of 7.0 and compare it with 3.5 using a small tolerance.

- Day 13: Decimal numbers

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Characters

A char is one Unicode scalar value, written in single quotes. A string is text written in double quotes. Some visible characters need several scalars, so char is not always one user-visible symbol.

Project: Change A to a lowercase letter and check is_ascii_lowercase().

- Day 14: Characters

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Tuples

A tuple keeps a few values together in a fixed order. The values can have different types. It is useful for returning a small pair, such as a measurement and a flag saying it is valid.

Project: Create a tuple containing a name and an age, then destructure and check both values.

- Day 15: Tuples

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Arrays

An array holds a fixed number of values of one type. Think of a tray with a known number of spaces. Its length is part of its type, so it does not grow when you add more information.

Project: Create an array of four scores and check its length and final element.

- Day 16: Arrays

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Functions

A function is a named set of instructions you can use again. Think of a recipe that accepts ingredients and gives a result. Parameters are the inputs; the return value is the result.

Project: Write a function triple that multiplies its input by three. Check it with two inputs.

- Day 17: Functions

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## if and else

if chooses what to do based on a yes-or-no condition. else gives the other path. It can also choose a value, like selecting a ticket label from a simple age rule.

Project: Set stock to zero and check that the result is "wait".

- Day 18: if and else

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## for loops

A for loop repeats an action for each item. Imagine checking every pencil in a pencil case. Rust gives the loop one item at a time and stops when the items run out.

Project: Use a for loop to add the numbers in [2, 4, 6] and check that the total is twelve.

- Day 19: for loops

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## while loops

A while loop repeats while a condition is true. Make sure something can eventually change that condition, otherwise it may run forever.

Project: Start at five and count how many loop iterations occur.

- Day 20: while loops

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## break and continue

break leaves a loop. continue skips the rest of the current turn and goes to the next turn. Their effect differs when useful items remain later in the sequence.

Project: Replace the break with continue and check that the total becomes six.

- Day 21: break and continue

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Type conversions

Sometimes a value must move into a different number type. A big number may not fit in a smaller type, just as a big parcel may not fit in a small box. TryFrom lets you handle that failure.

Project: Compare a narrowing cast with TryFrom using an out-of-range value.

- Day 22: Type conversions

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)

## Ownership

Rust keeps track of who is responsible for a value. Moving a String hands that responsibility to a new owner. The old name cannot keep using the moved value. This helps Rust release memory safely when it is no longer needed.

Project: Try to print draft after the move and identify the move location in the diagnostic.

- Day 23: Ownership

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

## Borrowing

Borrowing lets code use a value without taking ownership. A shared borrow can read it. A mutable borrow can change it, but needs exclusive access while it is used. The original owner stays responsible for the value.

Project: Call add_tax twice and calculate the final bill.

- Day 24: Borrowing

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

## Slices

A slice is a view of part of a list or text. Like looking at three pages of a book without making a copy, it borrows existing data. The original data must stay available while you use the view.

Project: Calculate totals for the complete array, a middle slice, and an empty slice.

- Day 25: Slices

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

## Structs

A struct keeps related information together under one name. A parcel might have a weight and an address. Named fields help readers know what each value means instead of guessing from a list of numbers.

Project: Add assertions for a zero weight and a valid small weight.

- Day 26: Structs

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch05-00-structs.html)

## Methods

A method is a function attached to a type. It can read, change, or consume an instance depending on its receiver. This keeps behavior close to the data it describes.

Project: Create a second rectangle and check its area.

- Day 27: Methods

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch05-00-structs.html)

## Enums

An enum describes a choice between named possibilities. A traffic light can be red, yellow, or green. One enum value is one choice at a time; choices can also carry their own information.

Project: List invalid combinations possible in a boolean-based delivery design.

- Day 28: Enums

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch06-00-enums.html)

## Option

Sometimes a value is available and sometimes it is missing. Option makes that difference clear. Some holds a value; None means there is no value. You decide what missing means instead of using a secret special number.

Project: Test a missing name, an empty name, and a name beginning with a non-ASCII character.

- Day 29: Option

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch06-00-enums.html)

## Some

Some means an optional value is present. It carries that value with it. You still need to handle the possibility of None when the overall type is Option.

Project: Put a short name inside Some and use if let to inspect it.

- Day 30: Some

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch06-00-enums.html)

## None

None means an optional value is absent. It is not automatically an error: an empty search result can be perfectly normal. The caller decides what absence means.

Project: Compare the fallback for None with the result for Some("Maya").

- Day 31: None

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch06-00-enums.html)

## Modules

A module groups related code, like folders group related papers. Names inside a module do not all need to be available outside it. You choose which parts other code may use with visibility rules.

Project: Move the pricing module into its own source file in a Cargo project.

- Day 32: Modules

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)

## Vectors

A vector is a list that can grow or shrink. You can add a new item at the end, remove one, or look up an item. Rust tracks the number of items separately from the room reserved for more.

Project: Print or assert vector length before and after reserve and push operations.

- Day 33: Vectors

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch08-00-common-collections.html)

## Strings

A String owns text that can grow. Text is stored as UTF-8 bytes, so one visible symbol can need several bytes. Treating every letter as one byte can break names containing accents or emoji.

Project: Compare byte length and chars().count() for ASCII, an emoji, and a combining accent.

- Day 34: Strings

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch08-00-common-collections.html)

## HashMap

A HashMap connects a key to a value, like a name connected to a phone number. You ask for a key instead of remembering a list position. It is useful for lookup, but its displayed order is not guaranteed.

Project: Store the number of apples and oranges in a map and look up both keys.

- Day 35: HashMap

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch08-00-common-collections.html)

## HashSet

A set remembers which different values are present. Adding the same value again does not create a duplicate. It is useful when the question is whether something has already been seen.

Project: Insert three colors with one repeat and check the unique count.

- Day 36: HashSet

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch08-00-common-collections.html)

## VecDeque

A VecDeque is a queue you can add to or remove from at either end. Think of people waiting in a line: take the first person and add a new arrival at the back. It avoids repeatedly shifting every remaining item.

Project: Create a queue of three names and remove them in their arrival order.

- Day 37: VecDeque

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch08-00-common-collections.html)

## BinaryHeap

A heap helps you repeatedly choose the highest-priority item. Rust’s BinaryHeap returns the greatest item first. It is not a fully sorted list when you simply iterate over its storage.

Project: Add a value larger than five before the first pop and predict the result.

- Day 38: BinaryHeap

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch08-00-common-collections.html)

## Result

An operation can succeed or fail. Result carries either Ok with the successful value or Err with information about the failure. It is like receiving either your order or a clear reason it could not be supplied.

Project: Write a table of accepted and rejected configuration strings.

- Day 39: Result

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## Ok

Ok is the successful case of Result. It carries the value produced by an operation. It is not the word okay printed on the screen; it is a structured value your program can examine.

Project: Return Ok from a tiny function that doubles a fixed valid number, then check its result.

- Day 40: Ok

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## Err

Err is the failed case of Result. It carries a reason or error value. This lets a caller respond deliberately, such as asking for a different input instead of crashing.

Project: Write a function that returns Err for an empty name and Ok for a nonempty name.

- Day 41: Err

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## The ? operator

The question mark passes a failure back to the caller. On success it takes out the successful value so the function can continue. It does not log, retry, or hide the failure.

Project: Try two valid strings and one invalid string, then explain which path each takes.

- Day 42: The ? operator

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## Custom errors

A clear error says what happened in a form the caller can use. Different failures can be named choices, such as empty input or not enough stock. Your program can then choose a suitable next step for each one.

Project: Add a separate unavailable-warehouse outcome to the reservation model.

- Day 43: Custom errors

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## panic!

A panic stops the current normal path because an assumption failed. It is like sounding an alarm for an unexpected internal problem. Ordinary mistakes in user input should usually get a Result error so the user can try again.

Project: Run the demonstration and distinguish its diagnostic output from its process exit status.

- Day 44: panic!

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## Newtypes

A newtype gives an existing kind of value a new meaning. UserId and OrderId can both contain numbers but remain different types. This helps stop code from accidentally using an order number where a user number belongs.

Project: Create separate types for cents and item count and attempt to interchange them.

- Day 45: Newtypes

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

## Generics

A generic function can work with different types while using the same idea. It is like a recipe that works with several suitable ingredients. Trait bounds tell Rust which abilities those ingredients must have.

Project: Call repeated with an integer, String, and a small custom Clone type.

- Day 46: Generics

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch10-00-generics.html)

## Traits

A trait describes something a type can do. Different types can promise the same ability, just as different instruments can all play a sound. Code can ask for the ability without requiring one particular instrument.

Project: Implement Source for a second type that yields two values.

- Day 47: Traits

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch10-00-generics.html)

## Lifetimes

A borrowed view must not last longer than the data it views. Lifetimes describe that relationship. They do not keep a value alive by magic; they help the compiler check that a reference will still be valid when used.

Project: Write a function returning a borrowed substring of its input.

- Day 48: Lifetimes

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch10-00-generics.html)

## Unit tests

A unit test checks a small piece of behavior automatically. You supply an input and the result you expect, then let Rust compare them. A useful test includes the edge of a rule, not only an easy middle case.

Project: Add threshold-minus-one, threshold, and threshold-plus-one assertions.

- Day 49: Unit tests

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch11-00-testing.html)

## Property tests

A property is a rule that should hold for many inputs. For example, sorting should keep all the original items. Checking many different inputs can find mistakes that one hand-picked example misses.

Project: Construct two different vectors with the same sum to disprove the weak property.

- Day 50: Property tests

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch11-00-testing.html)

## Reading input

Input is information coming into a program from a person, file, or another source. Reading can fail, so Rust reports a result. Keeping the reading step separate from the calculation makes both easier to understand and test.

Project: Test zero lines, one line without a final newline, and several lines.

- Day 51: Reading input

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)

## Project: search a file

This tool looks through text and keeps lines containing a chosen word. Separate the searching from opening a file so you can test the idea with a short string first.

Project: Read the official I/O project and write your CLI contract.

- Day 52: Project: search a file

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch12-00-an-io-project.html)

## Closures

A closure is a small function you can write where you need it. It can use nearby values. Think of giving a helper a short instruction plus the information needed to carry it out.

Project: Change the consuming closure to return message.len() and call it twice.

- Day 53: Closures

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch13-00-functional-features.html)

## Iterators

An iterator offers items one at a time. You can choose which items to keep or how to change them before collecting a result. Many iterator steps wait until something asks for the next item; they are not eager loops.

Project: Predict which orders reach map and what each becomes.

- Day 54: Iterators

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch13-00-functional-features.html)

## Writing an iterator

You can teach your own type to produce a sequence. Each call to next either supplies one item or reports that none is available. The type remembers enough state to know what comes next.

Project: Call next manually until exhaustion and several times afterward.

- Day 55: Writing an iterator

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch13-00-functional-features.html)

## Dependencies

A dependency is code your project uses from another package. Cargo finds compatible versions and records the chosen versions in Cargo.lock. Your project can also depend indirectly on packages used by its dependencies.

Project: Inspect direct and reverse dependency trees in a small package.

- Day 56: Dependencies

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch14-00-more-about-cargo.html)

## Conditional compilation

Some code belongs only on certain computers or with certain features. cfg chooses which pieces are included when building. This is different from an ordinary if that makes a choice while the program runs.

Project: Write target-specific functions using cfg attributes.

- Day 57: Conditional compilation

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch14-00-more-about-cargo.html)

## Box

Box owns a value stored in a heap allocation. It is useful when one value needs to point to another owned value, including recursive structures. The owner still controls cleanup; using Box does not remove ownership rules.

Project: Put a number in a Box, read it, and check that the value is unchanged.

- Day 58: Box

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

## Drop

Drop is cleanup that happens when an owned value is released. File handles and locks use this idea so resources are not forgotten on an early return.

Project: Put a String in an inner block and explain when its cleanup happens.

- Day 59: Drop

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

## Rc

Rc lets several owners share the same value on one thread. Cloning the Rc adds another owner rather than copying the whole value. When no strong owners remain, the value can be cleaned up.

Project: Create a third Rc handle and check the strong count before and after dropping it.

- Day 60: Rc

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

## RefCell

RefCell checks borrowing rules while the program runs. It can allow mutation through shared access on one thread, but conflicting borrows can fail or panic. It does not remove the exclusivity rule.

Project: Use try_borrow_mut while a shared guard is still alive and check that it reports failure.

- Day 61: RefCell

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

## Weak references

A Weak reference watches a shared value without keeping it alive. Before using it, you ask whether the value still exists. This is useful for a child pointing back to its parent without owning the parent.

Project: Add a second strong owner and check that the weak observer still upgrades until both are dropped.

- Day 62: Weak references

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

## Cow

Cow can hold either borrowed data or owned data. If text already looks right, a function can return a borrowed view. If the text needs changing, it can return a new owned String. This can avoid unnecessary copying.

Project: Test both borrowed and owned branches with matches!.

- Day 63: Cow

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)

## Threads

A thread is another path of work that can run alongside yours. Different threads may run at the same time on different cores. You still need to decide who owns their data and how you wait for their results.

Project: Split an array into two slices and sum them in scoped workers.

- Day 64: Threads

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

## Mutex

A mutex is a lock around shared data. A worker gets the lock before using the protected value and releases it when the guard goes away. Keep that time short so other workers do not wait unnecessarily.

Project: Protect a pair of related fields and update them under one guard.

- Day 65: Mutex

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

## Arc

Arc lets several threads own the same allocation. Cloning its handle adds another owner. The data inside still needs suitable synchronization if it will be changed.

Project: Share a read-only String with a worker and return its length.

- Day 66: Arc

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

## Channels

A channel sends messages from one part of a program to another. Imagine passing completed forms to a worker. Decide how many forms may wait and what happens when the worker can no longer keep up.

Project: Change channel capacity and observe when a producer can block.

- Day 67: Channels

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

## Atomic operations

An atomic operation makes one update indivisible to other threads. That helps with simple shared counters. It does not automatically keep several different values consistent or publish unrelated data safely.

Project: Explain why an independent metrics counter can use Relaxed.

- Day 68: Atomic operations

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch16-00-concurrency.html)

## Futures

A future describes work that may finish later. Creating it does not finish the work; something must poll it to make progress. A runtime helps drive many waiting operations so one slow connection need not stop all the others.

Project: Explain why the example produces no answer despite constructing request().

- Day 69: Futures

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch17-00-async-await.html)

## await

await waits for a future to finish while allowing the surrounding async task to pause. It does not create a new thread. The task must be driven by a runtime or another executor.

Project: In the Tokio project from the task lesson, await a ready value and check the result.

- Day 70: await

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch17-00-async-await.html)

## Tokio tasks

Tokio runs asynchronous Rust tasks. Tasks can wait for network or timer events while other tasks make progress. They are not one operating-system thread each. Slow blocking work needs a separate plan.

Project: Create a small Cargo project with the listed Tokio features.

- Day 71: Tokio tasks

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch17-00-async-await.html)

## Cancellation

Cancellation means stopping work that is no longer needed. Dropping a future stops its local continuation, but cannot undo a request already committed by another service. Plan what remains unfinished and what can safely be retried.

Project: Mark every resource alive at each await in a small handler.

- Day 72: Cancellation

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch17-00-async-await.html)

## Graceful shutdown

A program should stop carefully, like a shop that closes its doors and finishes serving the people already inside. Stop new work, tell workers to finish, and wait within a clear time limit.

Project: Write the shutdown order for an HTTP server with background jobs.

- Day 73: Graceful shutdown

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch17-00-async-await.html)

## Message framing

A network connection delivers bytes, not neatly separated messages. Framing tells the receiver where one message ends. Keep incomplete bytes until enough arrive, and reject lengths that are too large.

Project: Feed the sample message one byte at a time and track the retained buffer.

- Day 74: Message framing

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch17-00-async-await.html)

## Trait objects

A trait object lets code use different kinds of values through one shared ability. The concrete choice can be made while the program runs. It is useful for interchangeable backends, but the trait must support this kind of use.

Project: Implement a second alert type and call send with both.

- Day 75: Trait objects

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch18-00-oop.html)

## Typestate

Sometimes an action is allowed only after another action. Separate types can represent those stages. A Draft can become Published, so a method can consume the draft and return a different type with different available actions.

Project: Add an editable method only to Draft and a read-only method to Published.

- Day 76: Typestate

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch18-00-oop.html)

## Pattern matching

A pattern looks at the shape of a value and names the pieces you need. It can recognize one enum choice, pull apart a pair, or ignore an unused field. A match chooses one branch that fits.

Project: Add tuple cases and predict the first matching arm.

- Day 77: Pattern matching

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch19-00-patterns.html)

## match

match compares a value with several patterns and selects one branch. Think of a signpost with a route for each kind of arrival. Rust checks that all possible values are handled.

Project: Add a separate branch for two and check that it is chosen.

- Day 78: match

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch19-00-patterns.html)

## Unsafe Rust

Some low-level operations need checks Rust cannot prove for you. unsafe means you must establish those safety conditions yourself. It is not permission to use invalid memory, and it does not turn off every compiler rule.

Project: List each precondition for the raw read in the example.

- Day 79: Unsafe Rust

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)

## Calling other languages

An FFI is a boundary between Rust and another language. Both sides must agree how data is arranged, who owns it, and when it can be released. Rust cannot automatically check all promises made by foreign code.

Project: Write a C-style signature for a byte buffer and its length.

- Day 80: Calling other languages

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)

## Macros

A macro creates Rust code from a pattern of input before the program runs. It can remove repeated syntax, but its expansion still needs to be correct. A normal function is usually simpler when you only need to calculate a value.

Project: Use tagged! with an expression rather than a literal.

- Day 81: Macros

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)

## Pin

Some values rely on staying at one memory address after a certain point. Pin helps APIs keep that promise. It does not make the value live forever, and ordinary movable types often do not need the restriction.

Project: Draw a Box handle separately from its heap allocation.

- Day 82: Pin

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)

## Const generics

A const generic puts a fixed value, such as an array length, into a type or function parameter. It lets one definition work with several known sizes while keeping the size checked at compile time.

Project: Call width with arrays of different lengths and explain inference.

- Day 83: Const generics

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)

## Advanced borrowing

Some APIs must work with borrowed data that changes on every call. Advanced lifetime rules describe those relationships precisely. Learn ordinary borrowing first, then use these rules when a simple reference signature cannot describe the needed contract.

Project: Explain for every input lifetime in your own words.

- Day 84: Advanced borrowing

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch20-00-advanced-features.html)

## Project: a small server

A server receives requests and sends responses. Start with one request, then add a small group of workers. This is a learning project; real public servers need more complete protocol and security handling.

Project: Work through the official single-threaded server before adding a pool.

- Day 85: Project: a small server

[Read the original Rust Book chapter](https://doc.rust-lang.org/book/ch21-00-final-project-a-web-server.html)

## HTTP requests

HTTP is a set of rules browsers and services use to exchange requests and responses. A Rust service must read the request, check the data and permissions, perform the action, and send a suitable response.

Project: Design separate transport and domain types for creating an order.

- Day 86: HTTP requests

## Database transactions

A transaction groups database changes so they can succeed together or be rolled back together under the database's rules. It helps prevent half-finished local updates. It does not automatically include changes made by a remote service.

Project: Mark every crash point between accepting a request, writing state, committing, and replying.

- Day 87: Database transactions

## Logs and measurements

When a service behaves badly, you need clues. Logs describe events, measurements summarize behavior, and traces connect the steps of a request. Record useful timings without copying private information into the logs.

Project: Draw spans for queue, handler, database, and downstream work.

- Day 88: Logs and measurements

## Releasing a program

A release is the tested version you give to users. Keep a record of its source, compiler, dependencies, and settings so you can reproduce it. Check the actual running version after deployment, not only the code on your laptop.

Project: Write a release record listing source, toolchain, target, features, and lockfile.

- Day 89: Releasing a program

## Measuring performance

Measuring tells you where time or memory goes. Start with a question, such as whether parsing or waiting is slow. A tiny one-off timing is only a clue; use repeated realistic measurements before deciding a change helped.

Project: Define the workload and metric for a proposed optimization.

- Day 90: Measuring performance

## Rust without an operating system

Small devices may not have files, sockets, or normal threads. no_std lets a library use Rust's core features without assuming those services. Device startup and memory management still need a platform-specific design.

Project: Compile the checksum as a library and test it from a host harness.

- Day 91: Rust without an operating system

## WebAssembly

WebAssembly is a format browsers and other hosts can run. Rust can compile suitable code into it. Browser buttons and pages still need bindings; a native file or process API does not simply become a browser API.

Project: Test the size calculation with zero, normal, and overflowing dimensions.

- Day 92: WebAssembly

## Reading approach

Individual topics are grouped by learning area in the course filter. Related official Book chapters remain available as source reading. The local lessons are original companion material.

[Official Book appendices](https://doc.rust-lang.org/book/appendix-00.html)

## MCQ practice

40 original questions across ten topics. Answers and per-option explanations are returned after submission. First-attempt scores stay unchanged by retries; latest results and attempt counts are also saved.

## Production lab

Sources reviewed 2026-10-30. This is a curated snapshot, not a live feed or an exhaustive list. Documented advisory remediation is version-specific; follow each source for updates. Practice cases are illustrative rather than reported incidents.

- **Documented advisory**: GraphQL body exhausts server memory — [source](https://rustsec.org/advisories/RUSTSEC-2026-0415.html)
- **Documented advisory**: Build artifacts accidentally contain secrets — [source](https://rustsec.org/advisories/RUSTSEC-2026-0418.html)
- **Documented advisory**: TLS binding keeps a pointer after its owner frees it — [source](https://rustsec.org/advisories/RUSTSEC-2026-0413.html)
- **Documented advisory**: Tiny Markdown causes huge parser output — [source](https://rustsec.org/advisories/RUSTSEC-2026-0414.html)
- **Documented advisory**: TLS handshake enters a nonterminating I/O loop — [source](https://rustsec.org/advisories/RUSTSEC-2024-0336.html)
- **Documented advisory**: HTTP/2 continuation frames drive CPU and latency — [source](https://rustsec.org/advisories/RUSTSEC-2024-0332.html)
- **Documented advisory**: Protocol resets accumulate without a bound — [source](https://rustsec.org/advisories/RUSTSEC-2024-0003.html)
- **Practice scenario**: Requests stall while a task awaits with a lock — [source](https://tokio.rs/tokio/tutorial/shared-state)
- **Practice scenario**: A CPU-heavy request freezes unrelated timers — [source](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)
- **Practice scenario**: An unbounded work queue exhausts memory — [source](https://doc.rust-lang.org/std/sync/mpsc/fn.sync_channel.html)
- **Practice scenario**: A timeout leaves a partially completed operation — [source](https://tokio.rs/tokio/tutorial/select)
- **Practice scenario**: Deployment drops accepted background jobs — [source](https://tokio.rs/tokio/topics/shutdown)
- **Practice scenario**: Truncating a name panics on Unicode — [source](https://doc.rust-lang.org/std/string/struct.String.html)
- **Practice scenario**: A numeric limit behaves differently in release — [source](https://doc.rust-lang.org/std/primitive.u32.html)
- **Practice scenario**: Memory-safe objects never get freed — [source](https://doc.rust-lang.org/book/ch15-06-reference-cycles.html)
- **Practice scenario**: Database writes fail during concurrent requests — [source](https://www.sqlite.org/lang_transaction.html)
- **Practice scenario**: Concurrent inventory updates overwrite each other — [source](https://www.sqlite.org/lang_update.html)
- **Practice scenario**: Snapshot tests pass locally and fail in CI — [source](https://doc.rust-lang.org/std/collections/struct.HashMap.html)
- **Practice scenario**: A worker panic leaves a poisoned mutex — [source](https://doc.rust-lang.org/std/sync/struct.Mutex.html)
- **Practice scenario**: A patched crate is still present alongside an old copy — [source](https://doc.rust-lang.org/cargo/commands/cargo-tree.html)
- **Practice scenario**: A reminder is never sent — [source](https://doc.rust-lang.org/std/future/trait.Future.html)
- **Practice scenario**: A background worker fails silently — [source](https://tokio.rs/tokio/tutorial/spawning)
- **Practice scenario**: A worker never notices shutdown — [source](https://doc.rust-lang.org/std/sync/mpsc/)
- **Practice scenario**: A screen crashes while updating its model — [source](https://doc.rust-lang.org/std/cell/struct.RefCell.html)
- **Practice scenario**: Copying request data makes a service slow — [source](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)
- **Practice scenario**: Two transfers wait forever — [source](https://doc.rust-lang.org/std/sync/struct.Mutex.html)
- **Practice scenario**: One bad form value crashes a request — [source](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html)
- **Practice scenario**: A bill has inconsistent rounding — [source](https://doc.rust-lang.org/std/primitive.f64.html)
- **Practice scenario**: A lookup cannot find an inserted key — [source](https://doc.rust-lang.org/std/collections/struct.HashMap.html)
- **Practice scenario**: A cleanup step does nothing — [source](https://doc.rust-lang.org/std/iter/trait.Iterator.html)
- **Practice scenario**: An empty result crashes the response — [source](https://doc.rust-lang.org/std/vec/struct.Vec.html)
- **Practice scenario**: A device reports impossible packet sizes — [source](https://doc.rust-lang.org/std/primitive.u16.html)
- **Practice scenario**: A saved record is cut short — [source](https://doc.rust-lang.org/std/io/trait.Write.html)
- **Practice scenario**: The second input includes the first — [source](https://doc.rust-lang.org/std/io/trait.BufRead.html)
- **Practice scenario**: The pool runs out of available connections — [source](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)
- **Practice scenario**: A foreign call terminates the process — [source](https://doc.rust-lang.org/nomicon/ffi.html)
- **Practice scenario**: An older search replaces a newer result — [source](https://tokio.rs/tokio/tutorial/select)
- **Practice scenario**: A cache grows until the process runs out of memory — [source](https://doc.rust-lang.org/std/collections/struct.HashMap.html)
- **Practice scenario**: A measured duration suddenly becomes invalid — [source](https://doc.rust-lang.org/std/time/struct.Instant.html)
- **Practice scenario**: A worker panics when the receiver disappears — [source](https://doc.rust-lang.org/std/sync/mpsc/)

All incident narratives, timelines, and metrics are fictional teaching simulations. Read the brief and evidence, propose a diagnosis, then expand the debrief. Advisory-backed mechanisms remain linked to their primary sources.
