"""One-topic modules with a simple opening and optional deeper reading."""
# Stable IDs keep previously earned reading progress intact.
ROWS = r'''
setup|Installing Rust|Before cooking, you need a kitchen. Before running Rust, you need its tools. rustup installs the compiler; the compiler checks your instructions and builds a program your computer can run.|rustup --version\nrustc --version\ncargo --version
hello|Hello, world!|A program is a list of instructions. This first program asks the computer to say hello. It starts at main, follows the instruction inside the braces, then finishes.|fn main() { println!("Hello, world!"); }
cargo|Cargo|Cargo is your project helper. It keeps the project settings together and asks Rust to check, build, or run your code. You run its commands in a terminal from your project folder.|cargo new my_project\ncargo check\ncargo run
diagnostics|Compiler messages|The compiler checks your code before it runs. If something does not fit Rust's rules, it shows you where to look. Read the first message carefully, make one change, and check again.|cargo check\nrustc --explain E0308
formatting|Printing and formatting|Printing shows a message. Formatting puts values into that message, like filling a name into a greeting card. format! creates text you can keep; println! writes text to the screen.|println!("Hello, {}!", "Maya");\nlet message = format!("Count: {}", 3);
bindings|Variables|A variable is a name you give a value so you can use it later. Imagine putting a name label on a score. In Rust, a value cannot be reassigned through that name unless you allow changes with mut.|let score = 10;
types|Integers|An integer is a whole number, such as three apples or minus two degrees. Rust's integer types have different ranges. Choosing a type tells the computer which whole numbers you need to represent.|let temperature: i32 = -2;\nlet count: u32 = 3;
functions|Functions|A function is a named set of instructions you can use again. Think of a recipe that accepts ingredients and gives a result. Parameters are the inputs; the return value is the result.|fn double(number: i32) -> i32 { number * 2 }
loops|for loops|A for loop repeats an action for each item. Imagine checking every pencil in a pencil case. Rust gives the loop one item at a time and stops when the items run out.|for number in 1..4 { println!("{number}"); }
conversions|Type conversions|Sometimes a value must move into a different number type. A big number may not fit in a smaller type, just as a big parcel may not fit in a small box. TryFrom lets you handle that failure.|let small = u8::try_from(300u16);
ownership|Ownership|Rust keeps track of who is responsible for a value. Moving a String hands that responsibility to a new owner. The old name cannot keep using the moved value. This helps Rust release memory safely when it is no longer needed.|let owner = String::from("book");\nlet new_owner = owner;
borrowing|Borrowing|Borrowing lets code use a value without taking ownership. A shared borrow can read it. A mutable borrow can change it, but needs exclusive access while it is used. The original owner stays responsible for the value.|let view = &value;\nlet editable = &mut value;
slices|Slices|A slice is a view of part of a list or text. Like looking at three pages of a book without making a copy, it borrows existing data. The original data must stay available while you use the view.|let middle = &numbers[1..3];
structs|Structs|A struct keeps related information together under one name. A parcel might have a weight and an address. Named fields help readers know what each value means instead of guessing from a list of numbers.|struct Parcel { weight: u32 }
enums|Enums|An enum describes a choice between named possibilities. A traffic light can be red, yellow, or green. One enum value is one choice at a time; choices can also carry their own information.|enum Light { Red, Yellow, Green }
option|Option|Sometimes a value is available and sometimes it is missing. Option makes that difference clear. Some holds a value; None means there is no value. You decide what missing means instead of using a secret special number.|let nickname: Option<&str> = Some("Sam");
modules|Modules|A module groups related code, like folders group related papers. Names inside a module do not all need to be available outside it. You choose which parts other code may use with visibility rules.|mod greetings { pub fn hello() {} }
vectors|Vectors|A vector is a list that can grow or shrink. You can add a new item at the end, remove one, or look up an item. Rust tracks the number of items separately from the room reserved for more.|let mut numbers = vec![1, 2];\nnumbers.push(3);
strings|Strings|A String owns text that can grow. Text is stored as UTF-8 bytes, so one visible symbol can need several bytes. Treating every letter as one byte can break names containing accents or emoji.|let mut name = String::from("Maya");\nname.push('!');
maps|HashMap|A HashMap connects a key to a value, like a name connected to a phone number. You ask for a key instead of remembering a list position. It is useful for lookup, but its displayed order is not guaranteed.|use std::collections::HashMap;\nlet mut counts = HashMap::new();\ncounts.insert("blue", 2);
collection-design|VecDeque|A VecDeque is a queue you can add to or remove from at either end. Think of people waiting in a line: take the first person and add a new arrival at the back. It avoids repeatedly shifting every remaining item.|use std::collections::VecDeque;\nlet mut queue = VecDeque::from([1, 2]);\nqueue.pop_front();
result|Result|An operation can succeed or fail. Result carries either Ok with the successful value or Err with information about the failure. It is like receiving either your order or a clear reason it could not be supplied.|let answer: Result<u32, &str> = Ok(5);
error-types|Custom errors|A clear error says what happened in a form the caller can use. Different failures can be named choices, such as empty input or not enough stock. Your program can then choose a suitable next step for each one.|enum ReserveError { Empty, NotEnough }
panic|panic!|A panic stops the current normal path because an assumption failed. It is like sounding an alarm for an unexpected internal problem. Ordinary mistakes in user input should usually get a Result error so the user can try again.|panic!("unexpected internal state");
validation|Newtypes|A newtype gives an existing kind of value a new meaning. UserId and OrderId can both contain numbers but remain different types. This helps stop code from accidentally using an order number where a user number belongs.|struct UserId(u64);
generics|Generics|A generic function can work with different types while using the same idea. It is like a recipe that works with several suitable ingredients. Trait bounds tell Rust which abilities those ingredients must have.|fn pair<T: Clone>(value: T) -> (T, T) { (value.clone(), value) }
traits|Traits|A trait describes something a type can do. Different types can promise the same ability, just as different instruments can all play a sound. Code can ask for the ability without requiring one particular instrument.|trait Describe { fn description(&self) -> &str; }
lifetimes|Lifetimes|A borrowed view must not last longer than the data it views. Lifetimes describe that relationship. They do not keep a value alive by magic; they help the compiler check that a reference will still be valid when used.|fn first(text: &str) -> &str { text }
unit-tests|Unit tests|A unit test checks a small piece of behavior automatically. You supply an input and the result you expect, then let Rust compare them. A useful test includes the edge of a rule, not only an easy middle case.|#[test]\nfn adds_numbers() { assert_eq!(2 + 3, 5); }
property-tests|Property tests|A property is a rule that should hold for many inputs. For example, sorting should keep all the original items. Checking many different inputs can find mistakes that one hand-picked example misses.|assert!(sorted.windows(2).all(|pair| pair[0] <= pair[1]));
io|Reading input|Input is information coming into a program from a person, file, or another source. Reading can fail, so Rust reports a result. Keeping the reading step separate from the calculation makes both easier to understand and test.|std::io::stdin().read_line(&mut input)?;
closures|Closures|A closure is a small function you can write where you need it. It can use nearby values. Think of giving a helper a short instruction plus the information needed to carry it out.|let add_one = |number: i32| number + 1;
iterators|Iterators|An iterator offers items one at a time. You can choose which items to keep or how to change them before collecting a result. Many iterator steps wait until something asks for the next item; they are not eager loops.|let total: i32 = [1, 2, 3].iter().sum();
custom-iterator|Writing an iterator|You can teach your own type to produce a sequence. Each call to next either supplies one item or reports that none is available. The type remembers enough state to know what comes next.|impl Iterator for Countdown { type Item = u8; /* implement next */ }
cargo-deps|Dependencies|A dependency is code your project uses from another package. Cargo finds compatible versions and records the chosen versions in Cargo.lock. Your project can also depend indirectly on packages used by its dependencies.|[dependencies]\n# Add the package and supported version in Cargo.toml.
build-config|Conditional compilation|Some code belongs only on certain computers or with certain features. cfg chooses which pieces are included when building. This is different from an ordinary if that makes a choice while the program runs.|#[cfg(target_os = "windows")]\nfn platform_task() { }
box-drop|Box|Box owns a value stored in a heap allocation. It is useful when one value needs to point to another owned value, including recursive structures. The owner still controls cleanup; using Box does not remove ownership rules.|let value = Box::new(5);
rc-refcell|Rc|Rc lets several owners share the same value on one thread. Cloning the Rc adds another owner rather than copying the whole value. When no strong owners remain, the value can be cleaned up.|let shared = std::rc::Rc::new(String::from("notes"));\nlet other = std::rc::Rc::clone(&shared);
cow|Cow|Cow can hold either borrowed data or owned data. If text already looks right, a function can return a borrowed view. If the text needs changing, it can return a new owned String. This can avoid unnecessary copying.|use std::borrow::Cow;\nlet text: Cow<'_, str> = Cow::Borrowed("hello");
threads|Threads|A thread is another path of work that can run alongside yours. Different threads may run at the same time on different cores. You still need to decide who owns their data and how you wait for their results.|let worker = std::thread::spawn(|| 2 + 3);\nlet result = worker.join();
arc-mutex|Mutex|A mutex is a lock around shared data. A worker gets the lock before using the protected value and releases it when the guard goes away. Keep that time short so other workers do not wait unnecessarily.|let count = std::sync::Mutex::new(0);\n*count.lock().unwrap() += 1;
channels|Channels|A channel sends messages from one part of a program to another. Imagine passing completed forms to a worker. Decide how many forms may wait and what happens when the worker can no longer keep up.|let (sender, receiver) = std::sync::mpsc::channel();
atomics|Atomic operations|An atomic operation makes one update indivisible to other threads. That helps with simple shared counters. It does not automatically keep several different values consistent or publish unrelated data safely.|counter.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
futures|Futures|A future describes work that may finish later. Creating it does not finish the work; something must poll it to make progress. A runtime helps drive many waiting operations so one slow connection need not stop all the others.|async fn answer() -> u32 { 42 }
tokio|Tokio tasks|Tokio runs asynchronous Rust tasks. Tasks can wait for network or timer events while other tasks make progress. They are not one operating-system thread each. Slow blocking work needs a separate plan.|let handle = tokio::spawn(async { 42 });
async-locks|Cancellation|Cancellation means stopping work that is no longer needed. Dropping a future stops its local continuation, but cannot undo a request already committed by another service. Plan what remains unfinished and what can safely be retried.|tokio::select! { result = work() => { /* use result */ }, _ = stop() => {} }
shutdown|Graceful shutdown|A program should stop carefully, like a shop that closes its doors and finishes serving the people already inside. Stop new work, tell workers to finish, and wait within a clear time limit.|stop_accepting();\nnotify_workers();\nwait_for_workers();
network-framing|Message framing|A network connection delivers bytes, not neatly separated messages. Framing tells the receiver where one message ends. Keep incomplete bytes until enough arrive, and reject lengths that are too large.|let length = u16::from_be_bytes([header[0], header[1]]);
dispatch|Trait objects|A trait object lets code use different kinds of values through one shared ability. The concrete choice can be made while the program runs. It is useful for interchangeable backends, but the trait must support this kind of use.|fn send(alert: &dyn Alert) { /* call trait methods */ }
typestate|Typestate|Sometimes an action is allowed only after another action. Separate types can represent those stages. A Draft can become Published, so a method can consume the draft and return a different type with different available actions.|fn publish(self) -> Published { /* complete the transition */ }
patterns|Pattern matching|A pattern looks at the shape of a value and names the pieces you need. It can recognize one enum choice, pull apart a pair, or ignore an unused field. A match chooses one branch that fits.|match light { Light::Red => stop(), _ => continue_trip() }
unsafe|Unsafe Rust|Some low-level operations need checks Rust cannot prove for you. unsafe means you must establish those safety conditions yourself. It is not permission to use invalid memory, and it does not turn off every compiler rule.|let value = unsafe { *pointer };
ffi|Calling other languages|An FFI is a boundary between Rust and another language. Both sides must agree how data is arranged, who owns it, and when it can be released. Rust cannot automatically check all promises made by foreign code.|extern "C" fn add(a: i32, b: i32) -> i32 { a + b }
macros|Macros|A macro creates Rust code from a pattern of input before the program runs. It can remove repeated syntax, but its expansion still needs to be correct. A normal function is usually simpler when you only need to calculate a value.|macro_rules! hello { () => { println!("Hello!") }; }
pin|Pin|Some values rely on staying at one memory address after a certain point. Pin helps APIs keep that promise. It does not make the value live forever, and ordinary movable types often do not need the restriction.|let pinned = Box::pin(value);
const-generics|Const generics|A const generic puts a fixed value, such as an array length, into a type or function parameter. It lets one definition work with several known sizes while keeping the size checked at compile time.|fn width<const N: usize>(_: &[u8; N]) -> usize { N }
advanced-lifetimes|Advanced borrowing|Some APIs must work with borrowed data that changes on every call. Advanced lifetime rules describe those relationships precisely. Learn ordinary borrowing first, then use these rules when a simple reference signature cannot describe the needed contract.|fn inspect<F: for<'a> Fn(&'a str)>(callback: F) { callback("text"); }
http|HTTP requests|HTTP is a set of rules browsers and services use to exchange requests and responses. A Rust service must read the request, check the data and permissions, perform the action, and send a suitable response.|GET /health HTTP/1.1
database|Database transactions|A transaction groups database changes so they can succeed together or be rolled back together under the database's rules. It helps prevent half-finished local updates. It does not automatically include changes made by a remote service.|BEGIN;\n-- related database updates\nCOMMIT;
observability|Logs and measurements|When a service behaves badly, you need clues. Logs describe events, measurements summarize behavior, and traces connect the steps of a request. Record useful timings without copying private information into the logs.|eprintln!("request finished");
release|Releasing a program|A release is the tested version you give to users. Keep a record of its source, compiler, dependencies, and settings so you can reproduce it. Check the actual running version after deployment, not only the code on your laptop.|cargo test --locked\ncargo build --release --locked
profiling|Measuring performance|Measuring tells you where time or memory goes. Start with a question, such as whether parsing or waiting is slow. A tiny one-off timing is only a clue; use repeated realistic measurements before deciding a change helped.|let start = std::time::Instant::now();\nprintln!("{:?}", start.elapsed());
no-std|Rust without an operating system|Small devices may not have files, sockets, or normal threads. no_std lets a library use Rust's core features without assuming those services. Device startup and memory management still need a platform-specific design.|#![no_std]
wasm|WebAssembly|WebAssembly is a format browsers and other hosts can run. Rust can compile suitable code into it. Browser buttons and pages still need bindings; a native file or process API does not simply become a browser API.|rustup target add wasm32-unknown-unknown
book-guess|Project: a guessing game|The player guesses a number and the program says whether it is too high, too low, or correct. Build one small step at a time. Keep the comparison easy to test even when the final game chooses a random secret.|match guess.cmp(&secret) { /* handle the three comparisons */ }
book-search|Project: search a file|This tool looks through text and keeps lines containing a chosen word. Separate the searching from opening a file so you can test the idea with a short string first.|text.lines().filter(|line| line.contains(query))
book-server|Project: a small server|A server receives requests and sends responses. Start with one request, then add a small group of workers. This is a learning project; real public servers need more complete protocol and security handling.|let (sender, receiver) = std::sync::mpsc::sync_channel::<u32>(2);
'''

def organize(lessons):
    plain={}
    for row in ROWS.strip().splitlines():
        key,title,intro,syntax=row.split('|',3)
        plain[key]=(title,intro,syntax.replace('\\n','\n').replace('\\"','"'))
    for item in lessons:
        title,intro,syntax=plain[item['id']]
        item.update(title=title,simple=intro,syntax=syntax,syntax_label='Syntax sketch · names may be placeholders',simple_lab=item['lab'][0],group=item['module'])
    focused={
      'bindings':('fn main() { let score = 10; println!("Score: {score}"); assert_eq!(score, 10); }','let gives the value ten the name score. Printing reads that value without changing it. The assertion checks the named value.','Create a variable named apples with value three. Print it and check that it is three.'),
      'types':('fn main() { let temperature: i32 = -2; let count: u32 = 3; assert_eq!(temperature + 5, 3); assert_eq!(count + 1, 4); }','i32 permits negative whole numbers. u32 represents nonnegative whole numbers. Both additions stay inside their types’ ranges.','Give a signed variable the value minus five, add two, and check that the result is minus three.'),
      'functions':('fn double(number: i32) -> i32 { number * 2 }\nfn main() { assert_eq!(double(4), 8); }','Calling double supplies four as the parameter. The final expression multiplies it by two and returns eight.','Write a function triple that multiplies its input by three. Check it with two inputs.'),
      'loops':('fn main() { let mut total = 0; for number in [1, 2, 3] { total += number; } assert_eq!(total, 6); }','The loop visits one, two, and three in order. Each visit adds one item to the total; afterward the loop ends.','Use a for loop to add the numbers in [2, 4, 6] and check that the total is twelve.'),
      'collection-design':('fn main() { let mut queue = std::collections::VecDeque::from(["first", "second"]); assert_eq!(queue.pop_front(), Some("first")); queue.push_back("third"); assert_eq!(queue.pop_front(), Some("second")); }','pop_front serves the oldest item. push_back adds a new arrival behind the remaining items.','Create a queue of three names and remove them in their arrival order.'),
      'box-drop':('fn main() { let value = Box::new(5); assert_eq!(*value, 5); }','Box::new creates owned heap storage for five. Dereferencing with * reads the stored number. The Box releases its owned value when its scope ends.','Put a number in a Box, read it, and check that the value is unchanged.'),
      'rc-refcell':('fn main() { let first = std::rc::Rc::new(String::from("notes")); let second = std::rc::Rc::clone(&first); assert_eq!(std::rc::Rc::strong_count(&first), 2); assert_eq!(&*second, "notes"); }','Both Rc handles own a share of the same String. The count is two because two strong handles exist; the String was not copied by Rc::clone.','Create a third Rc handle and check the strong count before and after dropping it.'),
      'maps':('fn main() { let mut counts = std::collections::HashMap::new(); counts.insert("blue", 2); assert_eq!(counts.get("blue"), Some(&2)); assert_eq!(counts.get("red"), None); }','The key blue identifies a stored count. Looking up an absent key returns None instead of inventing a value.','Store the number of apples and oranges in a map and look up both keys.'),
    }
    for item in lessons:
        if item['id'] in focused:item['code'],item['walkthrough'],item['simple_lab']=focused[item['id']]
    add_topics(lessons)
    details=[]
    for index,item in enumerate(lessons):
        item['day']=index+1;item['module']=item['title'];item['minutes']=20
        item['prerequisite']=lessons[index-1]['id'] if index else None
        details.append(dict(name=item['module'],number=index+1,goal=item['simple'],project=item['simple_lab'],topics=[item['title']],prerequisite=lessons[index-1]['title'] if index else 'Start here',book_source=item.get('book_source'),group=item['group']))
    return [d['name'] for d in details],details

def add_topics(lessons):
    """Small separate lessons, each with its own focused executable example."""
    additions=[]
    def topic(after,slug,title,intro,usage,syntax,code,walk,lab,detail):
        parent=next(x for x in lessons if x['id']==after)
        item=dict(id=slug,title=title,module=title,group=parent['group'],stage=parent['stage'],simple=intro,explain=intro,use=usage,syntax=syntax,syntax_label='Syntax sketch',code=code,language='rust',walkthrough=walk,simple_lab=lab,lab=[lab],paragraphs=[detail],heading='A closer look',review=detail,pitfall='',question='Explain what changes in the example when you change its input.',source=parent['source'],book_source=parent.get('book_source'),book_chapter=parent.get('book_chapter'),minutes=20)
        additions.append((after,item))
    topic('bindings','mutable','Changing a variable',
     'Some values need to change, like a score after winning a point. mut tells Rust that you intend to change a binding. Without it, accidental reassignment is rejected before the program runs.',
     'Use a mutable variable for a running total or a changing counter. Keep it immutable when the value should stay fixed.',
     'let mut score = 0;\nscore += 1;',
     'fn main() { let mut score = 0; score += 1; assert_eq!(score, 1); }',
     'score begins at zero. += adds one and stores the new value. The assertion checks that the stored value is one.',
     'Start with two points, add three, and check that the final score is five.',
     'Mutability is a permission on a binding or access path, not a change to the value type. It does not bypass borrowing rules. Choose a short scope for changing state so later code is easier to reason about.')
    topic('bindings','constants','Constants',
     'A constant gives a name to a value known at compile time. Think of the number of minutes in an hour: the name explains the number and the value is not reassigned.',
     'Use constants for fixed conversion factors or documented limits. Data read from configuration at runtime is not a compile-time constant.',
     'const MINUTES: u32 = 60;',
     'const MINUTES: u32 = 60;\nfn main() { assert_eq!(2 * MINUTES, 120); }',
     'MINUTES has an explicit type and value. Multiplying by two calculates the number of minutes in two hours.',
     'Define SECONDS_PER_MINUTE and calculate the number of seconds in three minutes.',
     'A const declaration needs a type and a value allowed in constant evaluation. It is not the same as a mutable static variable or an immutable value loaded at runtime.')
    topic('bindings','shadowing','Shadowing',
     'Shadowing gives a new value an existing name with another let. It is useful when the same idea changes form, such as text becoming a number. The new binding hides the old one in that scope.',
     'A configuration parser can turn a text setting into a checked numeric value while keeping a clear name.',
     'let count = "3";\nlet count: u32 = count.parse().unwrap();',
     'fn main() { let count = "3"; let count: u32 = count.parse().unwrap(); assert_eq!(count + 1, 4); }',
     'The first count is text. The second count is a new numeric binding. The known literal parses successfully.',
     'Change the input to "8" and check that adding one produces nine.',
     'Shadowing creates a new binding and may change the type. Reassigning a mutable variable keeps its established type. For user input, handle parsing failure instead of assuming unwrap is safe.')
    topic('types','booleans','Booleans',
     'A boolean is either true or false. It answers a yes-or-no question, such as whether a door is open. Comparisons produce booleans that can control a decision.',
     'Use a boolean for a simple condition such as whether an item is available. Use an enum when there are several distinct states.',
     'let available: bool = true;',
     'fn main() { let count = 3; let available = count > 0; assert!(available); }',
     'The comparison count > 0 is true because three is greater than zero. assert! checks that condition.',
     'Set count to zero and check that !available is true.',
     'The ! operator negates a boolean. && and || short-circuit, so the second operand is evaluated only when needed. Avoid several independent booleans when they permit contradictory domain states.')
    topic('types','floats','Decimal numbers',
     'Floating-point numbers represent values with fractional parts, such as a measured temperature. Many decimal fractions are only approximations in this representation, so calculations need a suitable accuracy rule.',
     'Use floats for measurements and geometry. Exact monetary accounting often uses integer minor units or a deliberate decimal representation.',
     'let length: f64 = 2.5;',
     'fn main() { let length: f64 = 2.5; assert!((length * 2.0 - 5.0).abs() < 0.000001); }',
     'The example doubles the length and compares the difference with a small tolerance.',
     'Calculate half of 7.0 and compare it with 3.5 using a small tolerance.',
     'Choose a tolerance from the scale and domain of a calculation, not an arbitrary universal value. Floating-point values also include infinities and NaN, which affect comparisons and validation.')
    topic('types','characters','Characters',
     'A char is one Unicode scalar value, written in single quotes. A string is text written in double quotes. Some visible characters need several scalars, so char is not always one user-visible symbol.',
     'Use char while examining letters or symbols one scalar at a time. A text editor may need a grapheme-aware library for cursor movement.',
     "let letter: char = 'A';",
     "fn main() { let letter = 'A'; assert!(letter.is_ascii_uppercase()); assert_eq!(\"A\".chars().next(), Some(letter)); }",
     'The value is a char. chars().next() reads the first scalar from the string and returns it inside Some.',
     'Change A to a lowercase letter and check is_ascii_lowercase().',
     'char is not a byte. UTF-8 encodes different scalars using different byte lengths. ASCII-only checks intentionally cover a small subset of Unicode and should not be mistaken for general language rules.')
    topic('types','tuples','Tuples',
     'A tuple keeps a few values together in a fixed order. The values can have different types. It is useful for returning a small pair, such as a measurement and a flag saying it is valid.',
     'Use tuples for small temporary groupings. Prefer a struct with named fields when the meaning of positions is difficult to remember.',
     'let reading: (i32, bool) = (21, true);',
     'fn main() { let reading = (21, true); let (temperature, valid) = reading; assert_eq!(temperature, 21); assert!(valid); }',
     'The tuple stores two values. Destructuring gives each position a meaningful local name.',
     'Create a tuple containing a name and an age, then destructure and check both values.',
     'Tuple arity and component types are part of the type. The empty tuple () is the unit type, commonly used when a function has no meaningful result value.')
    topic('types','arrays','Arrays',
     'An array holds a fixed number of values of one type. Think of a tray with a known number of spaces. Its length is part of its type, so it does not grow when you add more information.',
     'Use an array for a fixed-size packet or a known set of measurements. Use Vec when the number of items must grow.',
     'let samples: [i32; 3] = [4, 5, 6];',
     'fn main() { let samples = [4, 5, 6]; assert_eq!(samples.len(), 3); assert_eq!(samples[1], 5); }',
     'Positions start at zero. Position one therefore contains the second value, five.',
     'Create an array of four scores and check its length and final element.',
     'An array owns its elements. A slice borrows a sequence whose length is known at runtime. Indexing outside either sequence panics; get returns an Option for fallible access.')
    topic('functions','if-expression','if and else',
     'if chooses what to do based on a yes-or-no condition. else gives the other path. It can also choose a value, like selecting a ticket label from a simple age rule.',
     'Use it for a small decision with a clear condition, such as whether stock is sufficient.',
     'let label = if available { "ready" } else { "wait" };',
     'fn main() { let stock = 2; let label = if stock > 0 { "ready" } else { "wait" }; assert_eq!(label, "ready"); }',
     'Because stock is positive, the first branch supplies the label. Both branches produce the same type of value.',
     'Set stock to zero and check that the result is "wait".',
     'An if condition must be bool; Rust does not treat arbitrary integers as truthy. Value-producing branches must agree on a compatible type. Boundary tests should include values on both sides of the condition.')
    topic('loops','while-loop','while loops',
     'A while loop repeats while a condition is true. Make sure something can eventually change that condition, otherwise it may run forever.',
     'Use while when the number of steps depends on changing state, such as draining a counter or checking a bounded condition.',
     'while remaining > 0 { remaining -= 1; }',
     'fn main() { let mut remaining = 3; while remaining > 0 { remaining -= 1; } assert_eq!(remaining, 0); }',
     'Each step subtracts one. At zero the condition is false, so the loop stops.',
     'Start at five and count how many loop iterations occur.',
     'Termination is part of the algorithm. A loop waiting for external events also needs a timeout or cancellation policy; changing a counter is not the only way a loop can make progress.')
    topic('loops','break-continue','break and continue',
     'break leaves a loop. continue skips the rest of the current turn and goes to the next turn. Their effect differs when useful items remain later in the sequence.',
     'Skip irrelevant records with continue, and stop at a meaningful ending condition with break.',
     'if value < 0 { continue; }\nif value == 9 { break; }',
     'fn main() { let mut total = 0; for value in [2, -1, 9, 4] { if value < 0 { continue; } if value == 9 { break; } total += value; } assert_eq!(total, 2); }',
     'The negative number is skipped. Nine ends the loop, so the final four is never added.',
     'Replace the break with continue and check that the total becomes six.',
     'Use a test containing items after the stop condition; otherwise different implementations may accidentally produce the same output. Labeled loops can specify which enclosing loop to leave.')
    topic('option','some','Some',
     'Some means an optional value is present. It carries that value with it. You still need to handle the possibility of None when the overall type is Option.',
     'A successful lookup can return Some with the found item instead of inventing a special placeholder.',
     'let found = Some(7);',
     'fn main() { let found = Some(7); if let Some(number) = found { assert_eq!(number, 7); } }',
     'if let opens the present case and gives its inner value a name.',
     'Put a short name inside Some and use if let to inspect it.',
     'Some is a variant of Option, not an independent wrapper type that proves every future operation succeeds. Matching can borrow or move the contained value depending on the expression and pattern.')
    topic('option','none','None',
     'None means an optional value is absent. It is not automatically an error: an empty search result can be perfectly normal. The caller decides what absence means.',
     'Return None when no matching item exists and a detailed failure reason is not required.',
     'let nickname: Option<&str> = None;',
     'fn main() { let nickname: Option<&str> = None; assert_eq!(nickname.unwrap_or("guest"), "guest"); }',
     'Because no nickname is present, unwrap_or supplies the chosen fallback.',
     'Compare the fallback for None with the result for Some("Maya").',
     'A fallback must match the domain. Replacing a missing optional nickname is different from silently replacing a failed bank-balance lookup with zero. Use Result when failure details matter.')
    topic('result','ok','Ok',
     'Ok is the successful case of Result. It carries the value produced by an operation. It is not the word okay printed on the screen; it is a structured value your program can examine.',
     'A parser returns Ok with the parsed value when the input meets its rules.',
     'let result: Result<u32, &str> = Ok(7);',
     'fn main() { let result: Result<u32, &str> = Ok(7); match result { Ok(number) => assert_eq!(number, 7), Err(_) => panic!("known success") } }',
     'match selects the successful branch and names the contained number.',
     'Return Ok from a tiny function that doubles a fixed valid number, then check its result.',
     'Result has separate success and error type parameters. A value inside Ok satisfies the function contract only if the implementation established the required validation; the variant alone does not prove business correctness.')
    topic('result','err','Err',
     'Err is the failed case of Result. It carries a reason or error value. This lets a caller respond deliberately, such as asking for a different input instead of crashing.',
     'Use Err when a requested file cannot be opened, a number cannot be parsed, or a domain rule rejects an operation.',
     'let result: Result<u32, &str> = Err("invalid number");',
     'fn main() { let result: Result<u32, &str> = Err("invalid number"); match result { Ok(_) => panic!("known failure"), Err(reason) => assert_eq!(reason, "invalid number") } }',
     'The error branch receives the reason. No successful number is available on this path.',
     'Write a function that returns Err for an empty name and Ok for a nonempty name.',
     'Returning Err is not the same as panicking. Typed error variants let callers distinguish recovery actions without parsing human-readable strings. Preserve underlying causes when useful.')
    topic('result','question-mark','The ? operator',
     'The question mark passes a failure back to the caller. On success it takes out the successful value so the function can continue. It does not log, retry, or hide the failure.',
     'Use it when a lower-level operation fails and the current function cannot complete without that result.',
     'let value = text.parse::<u32>()?;',
     'fn number(text: &str) -> Result<u32, std::num::ParseIntError> { let value = text.parse::<u32>()?; Ok(value + 1) }\nfn main() { assert_eq!(number("2"), Ok(3)); assert!(number("no").is_err()); }',
     'A valid input reaches the addition. Invalid text returns its parse error before the addition runs.',
     'Try two valid strings and one invalid string, then explain which path each takes.',
     'The enclosing return type must support the propagation. In compatible Result code, error conversion uses From. The caller still owns the recovery policy; ? only makes propagation concise.')
    topic('patterns','match','match',
     'match compares a value with several patterns and selects one branch. Think of a signpost with a route for each kind of arrival. Rust checks that all possible values are handled.',
     'Use match to handle enum choices, success and failure, or several meaningful input cases.',
     'match value { 0 => "zero", _ => "something else" }',
     'fn main() { let value = 2; let word = match value { 0 => "zero", 1 => "one", _ => "many" }; assert_eq!(word, "many"); }',
     'Two does not match zero or one. The wildcard handles the remaining values.',
     'Add a separate branch for two and check that it is chosen.',
     'Arms are considered in order. A wildcard placed too early can hide more specific behavior. Guards add conditions but do not make uncovered alternatives disappear.')
    topic('structs','methods','Methods',
     'A method is a function attached to a type. It can read, change, or consume an instance depending on its receiver. This keeps behavior close to the data it describes.',
     'A rectangle can have an area method so callers do not repeat the calculation everywhere.',
     'impl Rectangle { fn area(&self) -> u32 { self.width * self.height } }',
     'struct Rectangle { width: u32, height: u32 }\nimpl Rectangle { fn area(&self) -> u32 { self.width * self.height } }\nfn main() { let r = Rectangle { width: 3, height: 4 }; assert_eq!(r.area(), 12); }',
     'The method borrows the rectangle and multiplies its dimensions. The rectangle remains available afterward.',
     'Create a second rectangle and check its area.',
     '&self reads through shared access, &mut self permits exclusive mutation, and self consumes ownership. Choose the receiver to express lifecycle needs rather than to work around a compiler error.')
    topic('box-drop','drop','Drop',
     'Drop is cleanup that happens when an owned value is released. File handles and locks use this idea so resources are not forgotten on an early return.',
     'Use scope-based cleanup to release a lock before performing slower work.',
     'drop(value);',
     'fn main() { let data = String::from("temporary"); assert_eq!(data.len(), 9); drop(data); }',
     'drop consumes the String. Trying to use data afterward would be rejected because ownership has ended.',
     'Put a String in an inner block and explain when its cleanup happens.',
     'Drop implementations run synchronously during normal scope exit and unwinding, but process abort is different. Cleanup should not panic during another panic. Explicit drop controls ownership lifetime; it is not a call to a reusable object method.')
    topic('rc-refcell','refcell','RefCell',
     'RefCell checks borrowing rules while the program runs. It can allow mutation through shared access on one thread, but conflicting borrows can fail or panic. It does not remove the exclusivity rule.',
     'A single-threaded UI model may need controlled internal mutation while several parts hold shared references.',
     'let cell = std::cell::RefCell::new(0);\n*cell.borrow_mut() += 1;',
     'fn main() { let cell = std::cell::RefCell::new(0); *cell.borrow_mut() += 1; assert_eq!(*cell.borrow(), 1); }',
     'The temporary mutable guard ends before the shared read begins, so the runtime borrowing rule is satisfied.',
     'Use try_borrow_mut while a shared guard is still alive and check that it reports failure.',
     'borrow_mut panics on a conflict, while try_borrow_mut reports an error. Keep guards short. RefCell is not a replacement for thread-safe synchronization.')
    topic('rc-refcell','weak','Weak references',
     'A Weak reference watches a shared value without keeping it alive. Before using it, you ask whether the value still exists. This is useful for a child pointing back to its parent without owning the parent.',
     'Use weak back-links to avoid reference-counted cycles in trees or UI graphs.',
     'let observer = std::rc::Rc::downgrade(&owner);',
     'fn main() { let owner = std::rc::Rc::new(5); let observer = std::rc::Rc::downgrade(&owner); assert!(observer.upgrade().is_some()); drop(owner); assert!(observer.upgrade().is_none()); }',
     'The observer upgrades while a strong owner exists. After the last strong owner is dropped, upgrade returns None.',
     'Add a second strong owner and check that the weak observer still upgrades until both are dropped.',
     'Weak does not extend the lifetime of the contained value. The control allocation may remain while weak references exist, but that is different from the value being alive.')
    topic('arc-mutex','arc','Arc',
     'Arc lets several threads own the same allocation. Cloning its handle adds another owner. The data inside still needs suitable synchronization if it will be changed.',
     'Use Arc to share immutable configuration or a properly synchronized state object between workers.',
     'let shared = std::sync::Arc::new(5);',
     'fn main() { let shared = std::sync::Arc::new(5); let other = std::sync::Arc::clone(&shared); let handle = std::thread::spawn(move || *other); assert_eq!(handle.join().unwrap(), 5); assert_eq!(*shared, 5); }',
     'The worker owns one handle and main owns another. Both refer to the same immutable number.',
     'Share a read-only String with a worker and return its length.',
     'Arc makes reference counting thread-safe, not arbitrary pointee mutation. The Send and Sync requirements of T still matter. Do not assume Arc<RefCell<T>> is a safe shared mutable structure for multiple threads.')
    topic('maps','hashset','HashSet',
     'A set remembers which different values are present. Adding the same value again does not create a duplicate. It is useful when the question is whether something has already been seen.',
     'Use a HashSet to track unique tags or detect repeated identifiers.',
     'let mut seen = std::collections::HashSet::new();\nseen.insert("blue");',
     'fn main() { let mut seen = std::collections::HashSet::new(); assert!(seen.insert("blue")); assert!(!seen.insert("blue")); assert_eq!(seen.len(), 1); }',
     'The first insertion adds an item. The second reports that the item was already present.',
     'Insert three colors with one repeat and check the unique count.',
     'HashSet does not promise sorted iteration. Equality and hashing must agree, and a stored value must not change in a way that changes its equality or hash behavior.')
    topic('collection-design','binaryheap','BinaryHeap',
     'A heap helps you repeatedly choose the highest-priority item. Rust’s BinaryHeap returns the greatest item first. It is not a fully sorted list when you simply iterate over its storage.',
     'Use a heap for a scheduler that repeatedly picks the next most important job.',
     'let mut heap = std::collections::BinaryHeap::from([2, 5, 1]);\nlet next = heap.pop();',
     'fn main() { let mut heap = std::collections::BinaryHeap::from([2, 5, 1]); assert_eq!(heap.pop(), Some(5)); assert_eq!(heap.pop(), Some(2)); }',
     'pop removes the current greatest value, then maintains the heap so the next selection remains efficient.',
     'Add a value larger than five before the first pop and predict the result.',
     'Reverse can implement minimum-first ordering. Equal-priority FIFO order requires an explicit tie-break key. Choose a different structure when arbitrary ordered traversal or keyed updates dominate.')
    topic('futures','await','await',
     'await waits for a future to finish while allowing the surrounding async task to pause. It does not create a new thread. The task must be driven by a runtime or another executor.',
     'Use await for asynchronous network or timer operations so other tasks can make progress during the wait.',
     'let result = operation().await;',
     'async fn result() -> u32 { std::future::ready(7).await }\nfn main() { drop(result()); }',
     'This example shows valid syntax without running an executor. Dropping the unpolled future means the async body does not execute.',
     'In the Tokio project from the task lesson, await a ready value and check the result.',
     'Awaiting operations one after another is sequential. Concurrency needs both futures to be driven together or separate spawned tasks. Values live across suspension affect task lifetime and Send requirements.')
    # Insert each new topic beside its prerequisite while keeping stable original IDs.
    for after,item in reversed(additions):
        index=next(i for i,x in enumerate(lessons) if x['id']==after)
        lessons.insert(index+1,item)
