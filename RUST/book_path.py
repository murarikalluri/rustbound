"""Original companion lessons organized in the official Rust Book sequence."""
BASE='https://doc.rust-lang.org/book/'
PATH = [
('Getting started','ch01-00-getting-started.html','setup hello cargo diagnostics formatting'),
('Programming a guessing game','ch02-00-guessing-game-tutorial.html','book-guess'),
('Common programming concepts','ch03-00-common-programming-concepts.html','bindings types functions loops conversions'),
('Understanding ownership','ch04-00-understanding-ownership.html','ownership borrowing slices'),
('Using structs to structure related data','ch05-00-structs.html','structs'),
('Enums and pattern matching','ch06-00-enums.html','enums option'),
('Managing growing projects','ch07-00-managing-growing-projects-with-packages-crates-and-modules.html','modules'),
('Common collections','ch08-00-common-collections.html','vectors strings maps collection-design'),
('Error handling','ch09-00-error-handling.html','result error-types panic validation'),
('Generic types, traits, and lifetimes','ch10-00-generics.html','generics traits lifetimes'),
('Writing automated tests','ch11-00-testing.html','unit-tests property-tests'),
('An I/O project: building a command-line program','ch12-00-an-io-project.html','io book-search'),
('Functional language features','ch13-00-functional-features.html','closures iterators custom-iterator'),
('More about Cargo and crates.io','ch14-00-more-about-cargo.html','cargo-deps build-config'),
('Smart pointers','ch15-00-smart-pointers.html','box-drop rc-refcell cow'),
('Fearless concurrency','ch16-00-concurrency.html','threads arc-mutex channels atomics'),
('Async, futures, and streams','ch17-00-async-await.html','futures tokio async-locks shutdown network-framing'),
('Object-oriented programming features','ch18-00-oop.html','dispatch typestate'),
('Patterns and matching','ch19-00-patterns.html','patterns'),
('Advanced features','ch20-00-advanced-features.html','unsafe ffi macros pin const-generics advanced-lifetimes'),
('Final project: a multithreaded web server','ch21-00-final-project-a-web-server.html','book-server'),
('Beyond the Book: production and specialist paths',None,'http database observability release profiling no-std wasm'),
]

def arrange(lessons):
    for slug,title,explain,code,walk,paragraphs,lab,review in [
      ('book-guess','Project workshop: build a guessing-game loop',
       'Follow the Book’s first project by building an input–parse–compare loop. Start with a fixed secret so behavior is reproducible, then follow the official chapter to add its random-number dependency. This workshop is original companion material; the linked chapter supplies the complete official progression.',
       'fn feedback(secret: u32, input: &str) -> Result<&\'static str, std::num::ParseIntError> {\n    let guess: u32 = input.trim().parse()?;\n    Ok(match guess.cmp(&secret) {\n        std::cmp::Ordering::Less => "too low",\n        std::cmp::Ordering::Greater => "too high",\n        std::cmp::Ordering::Equal => "correct",\n    })\n}\nfn main() {\n    assert_eq!(feedback(17, "12"), Ok("too low"));\n    assert_eq!(feedback(17, "17"), Ok("correct"));\n    assert!(feedback(17, "nope").is_err());\n}',
       'The testable core trims and parses input before comparing it with a fixed secret. main checks behavior rather than reading a terminal; the lab adds the interactive shell around the same core. Invalid input remains a recoverable error.',
       ['Begin with a written interaction: display a prompt, read one line, parse an integer, compare it with the secret, and repeat until the guess is correct. Separate input errors from a valid but incorrect guess. The user should get another attempt after typing a word, rather than losing the whole session. This project previews concepts that later chapters explain more deeply; you do not need to understand every trait bound on the first pass.',
        'Keep the comparison logic independent of stdin. A small function accepting a secret and a string makes boundary behavior easy to check. When the terminal returns EOF, exit deliberately instead of repeating forever with an empty input buffer. Clear or replace the input buffer on each iteration so a second guess does not accidentally append to the first one. State what numeric range your game accepts.',
        'Add randomness only after the fixed-secret version works. Use the dependency and API described by the linked official chapter rather than guessing a version. Randomness belongs to choosing the secret, not to deciding whether the comparison is correct. Tests can still pass a known secret directly. At the end, explain how the project combines mutability, Result, matching, and loops, and revisit this workshop after studying those topics.'],
       ['Read the official chapter, then run the deterministic core above.', 'Wrap feedback in a terminal loop and handle invalid input and EOF.', 'Add bounded guesses and a winning exit, then test a scripted sequence of guesses.', 'Follow the Book to add random secret selection while keeping core tests deterministic.'],
       'Keep randomness and terminal I/O at the edges. Test comparisons with a fixed secret, and treat an invalid line separately from an incorrect numeric guess. The project becomes a repeatable exercise in handling state and input.'),
      ('book-search','Project workshop: build a file-search CLI',
       'Use the Book’s command-line project to connect arguments, file reading, borrowed text, errors, and tests. Build the search core first, then a binary adapter. The original example below is intentionally small so you can trace where the returned lines are borrowed from.',
       'fn matching_lines<\'a>(query: &str, text: &\'a str) -> Vec<&\'a str> {\n    text.lines().filter(|line| line.contains(query)).collect()\n}\nfn main() {\n    let text = "green tree\\nblue sky\\ngreen hill";\n    assert_eq!(matching_lines("green", text), ["green tree", "green hill"]);\n    assert!(matching_lines("red", text).is_empty());\n}',
       'Each returned slice points into text, not query. The vector owns its list of references but does not copy the matched line contents. The text owner must outlive use of those results.',
       ['Write the CLI contract before reading arguments: which argument is the query, which identifies the file, and what should happen when either is missing? Usage errors should be distinguishable from a file that cannot be opened and a valid search that finds no matches. Keep diagnostic output on stderr so stdout can remain the search-result stream when another program consumes it.',
        'Move the search algorithm into a library function. It can operate on borrowed text without knowing anything about filesystem permissions or process exit codes. Add tests for no matches, several matches, blank lines, and a final line without a newline. Choose and document whether an empty query matches every line. If you add case-insensitive behavior, state whether your implementation handles only ASCII or follows a more general Unicode policy.',
        'Only then connect the binary: parse configuration, read the input, call the core, print results, and translate failures into a useful exit status. Reading the whole file is a reasonable first implementation, but it has a memory cost. Extend the project with buffered line processing and compare the lifetime and allocation design. Use the official chapter as the main project guide and keep your own design decisions in a short README.'],
       ['Read the official I/O project and write your CLI contract.', 'Add core tests for empty input, repeated matches, and an empty query.', 'Connect arguments and filesystem access with explicit error reporting.', 'Implement a buffered variant and compare memory behavior on a large file.'],
       'A returned borrowed line must remain tied to its source text. A streaming implementation cannot keep borrowed views into a buffer that is reused for the next line; it needs immediate processing or owned retained results.'),
      ('book-server','Project workshop: design a bounded web-server worker pool',
       'Follow the Book’s final project in stages: a single connection, a finite worker pool, then orderly shutdown. This workshop supplies a testable scheduling model; the linked chapter supplies the complete TCP and HTTP teaching implementation. A teaching server is not a hardened public HTTP stack.',
       'use std::sync::mpsc;\nfn main() {\n    let (tx, rx) = mpsc::sync_channel::<u32>(2);\n    let worker = std::thread::spawn(move || {\n        let mut total = 0;\n        while let Ok(job) = rx.recv() { total += job; }\n        total\n    });\n    tx.send(3).unwrap();\n    tx.send(7).unwrap();\n    drop(tx);\n    assert_eq!(worker.join().unwrap(), 10);\n}',
       'One worker drains accepted jobs until all senders disappear, then returns its result. Queue capacity limits queued work. The real multiworker design needs deliberate receiver sharing or another queue abstraction; this demonstration does not pretend one receiver can be independently moved to several threads.',
       ['First understand one connection from accept through response. TCP provides bytes, not HTTP messages, so request framing and partial reads matter even in a small server. The official project intentionally simplifies protocol handling to focus on Rust design. Keep those educational assumptions explicit before adding a concurrency layer that would make debugging harder.',
        'A worker pool decouples accepted connections from a fixed number of workers. Decide what happens when workers and queue capacity are exhausted: waiting, rejecting, or allocating unbounded work are different policies. Each accepted job needs an owner, and each worker needs a completion and panic policy. Shared receiver access must be scoped so one worker does not accidentally hold a queue lock while executing an entire slow job.',
        'Shutdown is part of the project rather than an optional last line. Stop accepting work, close producer endpoints, let workers drain or cancel according to the contract, and join them. Test a slow connection while a fast request arrives and while shutdown begins. For real public services, prefer a maintained protocol implementation and an explicit security review. Explain what this project teaches and which production responsibilities remain outside its scope.'],
       ['Work through the official single-threaded server before adding a pool.', 'Trace the bounded-channel model and explain why dropping tx ends the loop.', 'Implement the Book’s pool and test concurrent slow and fast jobs.', 'Add shutdown tests and document queue, request-size, and timeout policies.'],
       'A worker count alone does not bound accepted or queued work. A shutdown that drops handles without joining does not demonstrate completion. Reason about admission, ownership, protocol limits, and draining as separate contracts.'),
    ]:
        lessons.append(dict(id=slug,title=title,explain=explain,code=code,walkthrough=walk,paragraphs=paragraphs,heading='Build the project in deliberate stages',lab=lab,review=review,language='rust',stage='Beginner' if slug=='book-guess' else 'Advanced' if slug=='book-server' else 'Intermediate',minutes=60,use='Keep a working project in your study workspace and use its design decisions in interview practice.',pitfall='Read the linked official chapter for the complete project; this companion example isolates one concept.',question='Explain one ownership decision, one failure path, and one test from your implementation.'))
    by_id={x['id']:x for x in lessons};ordered=[];details=[]
    for index,(title,path,ids) in enumerate(PATH):
        name=f'{index+1:02d} · {title}' if path else title
        entries=[by_id[key] for key in ids.split()]
        for item in entries:
            item['module']=name;item['book_chapter']=index+1 if path else None;item['book_source']=BASE+path if path else None
            item.setdefault('source',BASE+path if path else BASE)
            ordered.append(item)
        details.append(dict(name=name,number=index+1,goal='Read the official chapter, then work through these original explanations and labs.' if path else 'Extend the core language path into practical services and specialist introductions.',project='Complete the project workshop and explain your tests.' if index in (1,11,20) else 'Apply these concepts in your study project; demonstrate a normal case, a boundary, and an error path.',topics=[x['title'] for x in entries],prerequisite=details[-1]['name'] if details else 'No prior Rust experience required',book_source=BASE+path if path else None))
    assert set(by_id)=={x['id'] for x in ordered},'Every lesson must appear in the path exactly once'
    assert len(ordered)==len(by_id)
    for day,item in enumerate(ordered,1):
        item['day']=day;item['prerequisite']=ordered[day-2]['id'] if day>1 else None
    lessons[:]=ordered
    return [x['name'] for x in details],details
