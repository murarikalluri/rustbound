"""Interview track v1: behavioral checks plus ungraded design discussion."""
REGIONS = [('First Light','Algorithms & collections','🌱'),('The Borrowed Woods','Ownership & API design','🌲'),('Clockwork Canyon','Data structures & traits','⚙'),('The Summit','Concurrency & systems','🏔')]
LEVELS=[]

def question(title, topic, task, constraints, examples, starter, solution, tests, hints, follow_up, complexity):
    i=len(LEVELS)
    LEVELS.append(dict(id=i+1,region=i//9,title=title,topic=topic,task=task,
        constraints=constraints,examples=examples,starter=starter,solution=solution,
        tests=tests,hints=hints,follow_up=follow_up,complexity=complexity,
        lesson=topic+' — Explain your approach, ownership choices, and edge cases before coding.',
        xp=100+(i//9)*50,difficulty=['Easy / medium','Medium','Medium / hard','Advanced'][i//9]))

question('Two Sum: reconcile a payment','HashMap · indices · Option',
 'A payment processor needs two distinct entries whose amounts add up to a target. Implement two_sum. Scan left to right and choose the pair with the smallest second index; for that index, choose the earliest matching first index. Use None when no pair exists.',
 ['0–10,000 entries; values and target are between -1,000,000 and 1,000,000.','Never reuse an entry. Duplicate values are allowed.'],
 [('two_sum(&[2, 7, 11, 15], 9)','Some((0, 1))'),('two_sum(&[3, 3], 6)','Some((0, 1))'),('two_sum(&[1, 2], 8)','None')],
 'fn two_sum(amounts: &[i32], target: i32) -> Option<(usize, usize)> {\n    todo!("Find two different entries")\n}',
 '''fn two_sum(amounts:&[i32],target:i32)->Option<(usize,usize)> {
    let mut seen=std::collections::HashMap::new();
    for (j,&value) in amounts.iter().enumerate() {
        if let Some(&i)=seen.get(&(target-value)) { return Some((i,j)); }
        seen.entry(value).or_insert(j);
    }
    None
}''',
 [('two_sum(&[2,7,11,15],9)','Some((0,1))'),('two_sum(&[3,3],6)','Some((0,1))'),('two_sum(&[],0)','None'),('two_sum(&[3],6)','None'),('two_sum(&[-4,8,1],4)','Some((0,1))'),('two_sum(&[1,1,4,4],5)','Some((0,2))'),('two_sum(&[1,2,3],9)','None')],
 ['For each amount, what previously seen amount would complete the payment?','Look up the complement before inserting the current index. Keep the first index for duplicates.'],
 'How would sorted input change your approach? Why can inserting before lookup accidentally reuse one entry?', 'Target: expected O(n) time, O(n) extra space.')

question('Validate a normalized palindrome','Strings · two pointers · ASCII',
 'A search system treats punctuation and letter case as irrelevant. Decide whether the ASCII letters and digits in a query form a palindrome. Ignore all other ASCII characters; an empty normalized query is valid.',
 ['ASCII input, at most 10,000 bytes.','Case-insensitive for letters; digits must match exactly.'],
 [('palindrome("A man, a plan, a canal: Panama!")','true'),('palindrome("race a car")','false')],
 'fn palindrome(query: &str) -> bool {\n    todo!()\n}',
 '''fn palindrome(query:&str)->bool { let b=query.as_bytes(); let (mut l,mut r)=(0,b.len()); while l<r { if !b[l].is_ascii_alphanumeric(){l+=1;continue;} if !b[r-1].is_ascii_alphanumeric(){r-=1;continue;} if !b[l].eq_ignore_ascii_case(&b[r-1]){return false;} l+=1;r-=1; } true }''',
 [('palindrome("A man, a plan, a canal: Panama!")','true'),('palindrome("race a car")','false'),('palindrome("")','true'),('palindrome("!!!")','true'),('palindrome("0P")','false'),('palindrome("1aA1")','true')],
 ['Compare meaningful characters from opposite ends.','Use byte-level ASCII checks, and treat the right bound as exclusive.'],
 'What changes if input is Unicode? Distinguish bytes, Unicode scalar values, and grapheme clusters.', 'Target: O(n) time, O(1) extra space.')

question('Compress consecutive events','Iterators · Unicode · run-length encoding',
 'A log compressor groups consecutive identical Unicode scalar values. Produce (character, run length) groups, preserving order. Separate runs of the same character must remain separate.',
 ['At most 10,000 Unicode scalar values.','Do not count UTF-8 bytes as characters. Empty input has no groups.'],
 [('compress("aaabbcaa")',"vec![('a',3),('b',2),('c',1),('a',2)]"),('compress("🦀🦀é")',"vec![('🦀',2),('é',1)]")],
 'fn compress(log: &str) -> Vec<(char, usize)> {\n    todo!()\n}',
 '''fn compress(log:&str)->Vec<(char,usize)> { let mut out:Vec<(char,usize)>=vec![]; for c in log.chars(){if let Some(last)=out.last_mut(){if last.0==c {last.1+=1;continue;}} out.push((c,1));} out }''',
 [('compress("aaabbcaa")',"vec![('a',3),('b',2),('c',1),('a',2)]"),('compress("")','vec![]'),('compress("🦀🦀é")',"vec![('🦀',2),('é',1)]"),('compress("aba")',"vec![('a',1),('b',1),('a',1)]"),('compress(" ")',"vec![(' ',1)]")],
 ['Track only the most recent output group.','Use last_mut() to grow the last run without indexing into a String.'],
 'How would you process input in chunks when a run crosses a chunk boundary?', 'Target: O(n) time; O(r) output space for r runs.')

question('Deduplicate an event stream','HashSet · stable ordering',
 'A service receives event IDs with retries. Keep only the first occurrence of each ID while preserving arrival order. Do not sort the result.',
 ['Up to 10,000 signed integer IDs.','The input must remain unchanged.'],
 [('unique_ids(&[4, 2, 4, 3, 2])','vec![4, 2, 3]')],
 'fn unique_ids(ids: &[i32]) -> Vec<i32> {\n    todo!()\n}',
 '''fn unique_ids(ids:&[i32])->Vec<i32> { let mut seen=std::collections::HashSet::new(); ids.iter().copied().filter(|id|seen.insert(*id)).collect() }''',
 [('unique_ids(&[4,2,4,3,2])','vec![4,2,3]'),('unique_ids(&[])','vec![]'),('unique_ids(&[7,7,7])','vec![7]'),('unique_ids(&[-1,0,-1,2,0])','vec![-1,0,2]')],
 ['Membership and output order are separate concerns.','HashSet::insert tells you whether an ID was new.'],
 'Can exact deduplication run forever with bounded memory? What tradeoffs do time windows or probabilistic filters introduce?', 'Target: expected O(n) time, O(u) extra space.')

question('Find the first matching record','Binary search · boundary invariants',
 'An index contains sorted IDs, including duplicates. Locate the first occurrence of a target, or None if absent. A linear scan is not the intended interview approach.',
 ['Sorted nondecreasing slice, length 0–100,000.','Duplicate values may occupy the entire slice.'],
 [('first_index(&[1, 2, 2, 2, 7], 2)','Some(1)'),('first_index(&[1, 3], 2)','None')],
 'fn first_index(ids: &[i32], target: i32) -> Option<usize> {\n    todo!()\n}',
 '''fn first_index(ids:&[i32],target:i32)->Option<usize> { let(mut l,mut r)=(0,ids.len());while l<r{let m=l+(r-l)/2;if ids[m]<target{l=m+1;}else{r=m;}}if ids.get(l)==Some(&target){Some(l)}else{None} }''',
 [('first_index(&[1,2,2,2,7],2)','Some(1)'),('first_index(&[],0)','None'),('first_index(&[4,4,4],4)','Some(0)'),('first_index(&[1,3],2)','None'),('first_index(&[-2,0,9],9)','Some(2)'),('first_index(&[1],0)','None')],
 ['Search for the first index whose value is not smaller than the target.','Maintain a half-open [left, right) search range, then verify the candidate.'],
 'State the loop invariant. How would you find the number of target occurrences?', 'Target: O(log n) time, O(1) space.')

question('Check nested delimiters','Stacks · matching pairs',
 'Build a lightweight delimiter validator for (), [], and {}. Every closing delimiter must match the latest unmatched opening delimiter. Ignore all other characters; this is not a full Rust parser and has no string-literal rules.',
 ['At most 10,000 characters.','An unmatched opener or closer makes the expression invalid.'],
 [('balanced("a * (b + [c])")','true'),('balanced("([)]")','false')],
 'fn balanced(expression: &str) -> bool {\n    todo!()\n}',
 '''fn balanced(expression:&str)->bool { let mut stack=Vec::new();for c in expression.chars(){match c {'('| '['|'{' =>stack.push(c), ')'|']'|'}'=>{let expected=match c{')'=>'(',']'=>'[',_=>'{'};if stack.pop()!=Some(expected){return false;}},_=>{}}}stack.is_empty() }''',
 [('balanced("a * (b + [c])")','true'),('balanced("([)]")','false'),('balanced("((")','false'),('balanced(")")','false'),('balanced("")','true'),('balanced("{[]()} text")','true')],
 ['The most recently opened delimiter must close first.','A Vec can act as a stack with push and pop.'],
 'What additional state would a real parser need to ignore delimiters inside strings and comments?', 'Target: O(n) time, O(depth) space.')

question('Merge reservation windows','Sorting · interval merging',
 'A room-booking service wants a consolidated list of occupied windows. Merge overlapping or touching closed intervals, sort the result by start time, and preserve isolated intervals.',
 ['0–10,000 intervals; every start <= end.','Inputs may be unsorted, repeated, nested, or zero-length.'],
 [('merge_windows(vec![(5,7),(1,3),(3,4)])','vec![(1,4),(5,7)]')],
 'fn merge_windows(mut windows: Vec<(i32, i32)>) -> Vec<(i32, i32)> {\n    todo!()\n}',
 '''fn merge_windows(mut windows:Vec<(i32,i32)>)->Vec<(i32,i32)>{windows.sort_unstable();let mut out:Vec<(i32,i32)>=vec![];for (s,e) in windows{if let Some(last)=out.last_mut(){if s<=last.1{last.1=last.1.max(e);continue;}}out.push((s,e));}out}''',
 [('merge_windows(vec![(5,7),(1,3),(3,4)])','vec![(1,4),(5,7)]'),('merge_windows(vec![])','vec![]'),('merge_windows(vec![(1,10),(2,3),(1,10)])','vec![(1,10)]'),('merge_windows(vec![(-5,-2),(-2,0),(2,2)])','vec![(-5,0),(2,2)]')],
 ['Sort by start time before maintaining the current merged window.','Nested intervals must not shrink the current end.'],
 'How does the overlap condition change for half-open [start, end) intervals?', 'Target: O(n log n) time, O(n) output space.')

question('Rank frequent search terms','HashMap · deterministic tie-breaking',
 'Given exact, case-sensitive search terms, produce the k most frequent distinct terms. Rank by descending count, then ascending lexicographic order for ties. If k exceeds the number of distinct terms, include them all.',
 ['At most 10,000 terms; k may be zero.','Do not lowercase or otherwise normalize the terms.'],
 [('top_terms(&["rust","go","rust","go","c"], 2)','vec!["go", "rust"]')],
 'fn top_terms(terms: &[&str], k: usize) -> Vec<String> {\n    todo!()\n}',
 '''fn top_terms(terms:&[&str],k:usize)->Vec<String>{let mut counts=std::collections::HashMap::new();for &t in terms{*counts.entry(t).or_insert(0usize)+=1;}let mut v:Vec<_>=counts.into_iter().collect();v.sort_by(|a,b|b.1.cmp(&a.1).then(a.0.cmp(b.0)));v.into_iter().take(k).map(|(t,_)|t.to_owned()).collect()}''',
 [('top_terms(&["rust","go","rust","go","c"],2)','vec!["go","rust"]'),('top_terms(&[],3)','Vec::<String>::new()'),('top_terms(&["x"],0)','Vec::<String>::new()'),('top_terms(&["z","a","z"],9)','vec!["z","a"]'),('top_terms(&["Rust","rust"],2)','vec!["Rust","rust"]')],
 ['Count first, then define a total ordering that includes ties.','HashMap iteration order must not determine the answer.'],
 'How would a heap improve performance when k is much smaller than the number of distinct terms?', 'Target: O(n + u log u) time for the sorting solution.')

question('Peak traffic window','Sliding window · numeric bounds',
 'A monitoring service stores signed traffic deltas. Find the largest sum of exactly k consecutive samples. Invalid window sizes (zero or larger than the input) have no answer.',
 ['0–100,000 i32 samples.','Accumulate in i64 to avoid overflow when adding i32 values.'],
 [('peak_window(&[2,-1,4,3], 2)','Some(7)'),('peak_window(&[-5,-2,-8], 2)','Some(-7)')],
 'fn peak_window(samples: &[i32], k: usize) -> Option<i64> {\n    todo!()\n}',
 '''fn peak_window(samples:&[i32],k:usize)->Option<i64>{if k==0||k>samples.len(){return None;}let mut sum:i64=samples[..k].iter().map(|&x|i64::from(x)).sum();let mut best=sum;for i in k..samples.len(){sum+=i64::from(samples[i])-i64::from(samples[i-k]);best=best.max(sum);}Some(best)}''',
 [('peak_window(&[2,-1,4,3],2)','Some(7)'),('peak_window(&[-5,-2,-8],2)','Some(-7)'),('peak_window(&[],1)','None'),('peak_window(&[1],0)','None'),('peak_window(&[1],2)','None'),('peak_window(&[i32::MAX,i32::MAX],2)','Some(4294967294i64)')],
 ['Adjacent windows share all but two samples.','Initialize the best value from a real window, not from zero.'],
 'How would you handle an unbounded stream while retaining only k samples?', 'Target: O(n) time, O(1) extra space.')

question('Borrow tokens from a request','Lifetimes · zero-copy string slices',
 'A request parser needs comma-separated tokens without copying their text. Split the input, trim surrounding whitespace, and omit empty tokens. Every returned &str must borrow from the original request.',
 ['Valid UTF-8 text; commas are separators with no quoting or escaping.','Use the supplied lifetime relationship. Do not allocate or leak replacement strings.'],
 [('tokens(" rust, , ownership , 🦀 ")','vec!["rust","ownership","🦀"]')],
 "fn tokens<'a>(request: &'a str) -> Vec<&'a str> {\n    todo!()\n}",
 "fn tokens<'a>(request:&'a str)->Vec<&'a str>{request.split(',').map(str::trim).filter(|s|!s.is_empty()).collect()}",
 [('tokens(" rust, , ownership , 🦀 ")','vec!["rust","ownership","🦀"]'),('tokens(",,,")','Vec::<&str>::new()'),('tokens("one")','vec!["one"]'),('{let s=String::from(" aa,bb ");let v=tokens(&s);v[0].as_ptr()==s[1..].as_ptr() && v[1].as_ptr()==s[4..].as_ptr()}','true')],
 ['str::split yields borrowed slices.','Trimming a slice adjusts its boundaries; it does not need a new String.'],
 'Why can the returned tokens not outlive the request? What changes if the parser must own its input?', 'Target: O(n) time; allocation only for the output vector.')

question('Parse borrowed configuration','String parsing · Result · lifetimes',
 'Parse nonempty key=value lines into borrowed pairs. Trim keys and values, skip blank lines and full-line comments starting with # after trimming. Split on the first = only. On a missing = or empty key, report the 1-based original line number. Empty values and repeated keys are allowed.',
 ['Input is valid UTF-8; no escape syntax or inline comments.','Keep original line numbers even when skipping blank/comment lines.'],
 [('config("# settings\\nhost = local\\ntoken=a=b")','Ok(vec![("host","local"),("token","a=b")])'),('config("ok=1\\nbroken")','Err(2)')],
 "fn config<'a>(text: &'a str) -> Result<Vec<(&'a str, &'a str)>, usize> {\n    todo!()\n}",
 "fn config<'a>(text:&'a str)->Result<Vec<(&'a str,&'a str)>,usize>{let mut out=vec![];for(i,line)in text.lines().enumerate(){let line=line.trim();if line.is_empty()||line.starts_with('#'){continue;}let(k,v)=line.split_once('=').ok_or(i+1)?;let k=k.trim();if k.is_empty(){return Err(i+1);}out.push((k,v.trim()));}Ok(out)}",
 [('config("# settings\nhost = local\ntoken=a=b")','Ok(vec![("host","local"),("token","a=b")])'),('config("ok=1\nbroken")','Err(2)'),('config("\n#x\n =value")','Err(3)'),('config("k=\nk=two")','Ok(vec![("k",""),("k","two")])'),('config("")','Ok(vec![])')],
 ['Enumerate lines before skipping them.','split_once preserves additional equals signs in the value.'],
 'Why is a borrowed configuration useful, and when would an owned representation be safer?', 'Target: O(n) parsing time; no copied key/value text.')

question('Partition without cloning','Ownership · generics · FnMut',
 'Split owned jobs into accepted and rejected vectors using a predicate. Evaluate the predicate once per item and preserve input order within each group. The jobs may not implement Clone or Copy.',
 ['The function consumes its input vector.','Predicate receives &T and may hold mutable state.'],
 [('partition_jobs(vec![1,2,3,4], |n| n % 2 == 0)','(vec![2,4], vec![1,3])')],
 'fn partition_jobs<T, F: FnMut(&T) -> bool>(jobs: Vec<T>, mut accept: F) -> (Vec<T>, Vec<T>) {\n    todo!()\n}',
 'fn partition_jobs<T,F:FnMut(&T)->bool>(jobs:Vec<T>,mut accept:F)->(Vec<T>,Vec<T>){let(mut yes,mut no)=(vec![],vec![]);for job in jobs{if accept(&job){yes.push(job);}else{no.push(job);}}(yes,no)}',
 [('partition_jobs(vec![1,2,3,4],|n|n%2==0)','(vec![2,4],vec![1,3])'),('partition_jobs(Vec::<i32>::new(),|_|true)','(vec![],vec![])'),('{struct Job(i32);let mut calls=0;let(a,b)=partition_jobs(vec![Job(3),Job(1),Job(4)],|j|{calls+=1;j.0>2});(a.into_iter().map(|j|j.0).collect::<Vec<_>>(),b.into_iter().map(|j|j.0).collect::<Vec<_>>(),calls)}','(vec![3,4],vec![1],3)')],
 ['Borrow each item for the predicate, then move it into exactly one output.','A consuming for loop avoids cloning the jobs.'],
 'Explain the difference between Fn, FnMut, and FnOnce for this API.', 'Target: O(n) time and O(n) output space.')

question('Rotate a reusable buffer','Mutable slices · in-place algorithms',
 'A circular display needs its buffer rotated right by k positions. Mutate the existing slice without cloning elements or allocating another buffer. Handle rotations larger than the length and an empty buffer.',
 ['Generic element type with no trait bounds.','k is any usize; an empty slice must not panic.'],
 [('rotate_right(&mut [1,2,3,4,5], 2)','buffer becomes [4,5,1,2,3]')],
 'fn rotate_right<T>(buffer: &mut [T], k: usize) {\n    todo!()\n}',
 'fn rotate_right<T>(buffer:&mut[T],k:usize){if buffer.is_empty(){return;}let k=k%buffer.len();buffer.reverse();buffer[..k].reverse();buffer[k..].reverse();}',
 [('{let mut v=vec![1,2,3,4,5];rotate_right(&mut v,2);v}','vec![4,5,1,2,3]'),('{let mut v=vec![1,2,3];rotate_right(&mut v,7);v}','vec![3,1,2]'),('{let mut v:Vec<i32>=vec![];rotate_right(&mut v,usize::MAX);v}','vec![]'),('{struct Item(i32);let mut v=[Item(1),Item(2)];rotate_right(&mut v,0);(v[0].0,v[1].0)}','(1,2)')],
 ['Normalize k only after checking for an empty slice.','Consider what reversing the whole slice and then two subranges does.'],
 'Compare this approach with repeated shifting. Why does a generic non-Clone type matter?', 'Target: O(n) time and O(1) extra space.')

question('Truncate UTF-8 safely','Byte budgets · char boundaries',
 'A telemetry field has a byte limit. Select the longest prefix that fits the byte budget without splitting a UTF-8 character. The output must borrow the input; it may split a grapheme cluster but never a Unicode scalar value.',
 ['Valid UTF-8 input; max_bytes may exceed the input length.','No ellipsis is added.'],
 [('truncate_utf8("a🦀é", 5)','"a🦀"'),('truncate_utf8("éclair", 1)','""')],
 'fn truncate_utf8(text: &str, max_bytes: usize) -> &str {\n    todo!()\n}',
 'fn truncate_utf8(text:&str,max_bytes:usize)->&str{let mut end=max_bytes.min(text.len());while !text.is_char_boundary(end){end-=1;}&text[..end]}',
 [('truncate_utf8("a🦀é",5)','"a🦀"'),('truncate_utf8("a🦀é",4)','"a"'),('truncate_utf8("éclair",1)','""'),('truncate_utf8("rust",99)','"rust"'),('truncate_utf8("",0)','""'),('{let s=String::from("résumé");truncate_utf8(&s,4).as_ptr()==s.as_ptr()}','true')],
 ['String length and character count answer different questions.','Clamp the byte endpoint, then move back to a character boundary.'],
 'Why might valid UTF-8 still be visually awkward when truncated? How would grapheme-aware truncation differ?', 'Target: O(1) boundary adjustment after choosing the byte endpoint.')

question('Make a transfer atomic','Mutable references · checked arithmetic',
 'Transfer an unsigned amount between two borrowed balances. Fail with "insufficient funds" if the source is too small, or "overflow" if the destination would overflow u64. On any error, neither balance may change. Insufficient funds takes precedence.',
 ['Source and destination are distinct mutable references.','All u64 amounts, including zero, are valid inputs.'],
 [('transfer(&mut 10, &mut 2, 4)','Ok(()); balances become 6 and 6')],
 "fn transfer(from: &mut u64, to: &mut u64, amount: u64) -> Result<(), &'static str> {\n    todo!()\n}",
 "fn transfer(from:&mut u64,to:&mut u64,amount:u64)->Result<(),&'static str>{if *from<amount{return Err(\"insufficient funds\");}let new_to=to.checked_add(amount).ok_or(\"overflow\")?;*from-=amount;*to=new_to;Ok(())}",
 [('{let(mut a,mut b)=(10,2);let r=transfer(&mut a,&mut b,4);(r,a,b)}','(Ok(()),6,6)'),('{let(mut a,mut b)=(2,5);let r=transfer(&mut a,&mut b,3);(r,a,b)}','(Err("insufficient funds"),2,5)'),('{let(mut a,mut b)=(4,u64::MAX);let r=transfer(&mut a,&mut b,1);(r,a,b)}','(Err("overflow"),4,u64::MAX)'),('{let(mut a,mut b)=(0,u64::MAX);let r=transfer(&mut a,&mut b,0);(r,a,b)}','(Ok(()),0,u64::MAX)')],
 ['Compute and validate the new state before writing either reference.','checked_add represents overflow as None.'],
 'What guarantees prevent both references from pointing to the same balance? How would thread sharing change the design?', 'Target: O(1) time and space.')

question('Reverse an owned linked list','Box · Option::take · moves',
 'Reverse a singly linked list by relinking its existing nodes. Consume and produce Option<Box<Node>>. Do not clone nodes or allocate replacement nodes.',
 ['Node values are i32; list is acyclic.','Prefer an iterative algorithm so input length does not dictate call-stack usage.'],
 [('reverse_list(1 → 2 → 3)','3 → 2 → 1')],
 '#[derive(Debug, PartialEq)]\nstruct Node { value: i32, next: Option<Box<Node>> }\nfn reverse_list(head: Option<Box<Node>>) -> Option<Box<Node>> {\n    todo!()\n}',
 '#[derive(Debug,PartialEq)] struct Node{value:i32,next:Option<Box<Node>>} fn reverse_list(mut head:Option<Box<Node>>)->Option<Box<Node>>{let mut prev=None;while let Some(mut node)=head{head=node.next.take();node.next=prev;prev=Some(node);}prev}',
 [('reverse_list(None)','None'),('{let h=Some(Box::new(Node{value:1,next:Some(Box::new(Node{value:2,next:None}))}));let r=reverse_list(h).unwrap();(r.value,r.next.unwrap().value)}','(2,1)'),('{let h=Box::new(Node{value:7,next:None});let ptr=(&*h) as *const Node;let r=reverse_list(Some(h)).unwrap();((&*r) as *const Node==ptr,r.value,r.next.is_none())}','(true,7,true)'),('{let mut h=None;for i in 0..100{h=Some(Box::new(Node{value:i,next:h}));}let mut r=reverse_list(h);let mut v=vec![];while let Some(n)=r{v.push(n.value);r=n.next;}v}','(0..100).collect::<Vec<_>>()')],
 ['Detach the next node before repointing the current node.','Option::take moves out an owned value and leaves None behind.'],
 'Why does moving a Box not move its heap allocation? What could recursive destruction mean for extremely long lists?', 'Target: O(n) time and O(1) extra space.')

question('Validate a binary search tree','Recursive borrowing · strict bounds',
 'Determine whether a tree is a strict binary search tree: every left descendant must be smaller than its ancestor, and every right descendant larger. Duplicates are invalid. Checking only parent-child relationships is insufficient.',
 ['At most 1,000 nodes and depth at most 100.','Node values may be i32::MIN or i32::MAX.'],
 [('valid_bst(tree with root 10 and right subtree containing 6)','false')],
 'struct Tree { value: i32, left: Option<Box<Tree>>, right: Option<Box<Tree>> }\nfn valid_bst(root: &Option<Box<Tree>>) -> bool {\n    todo!()\n}',
 '''struct Tree{value:i32,left:Option<Box<Tree>>,right:Option<Box<Tree>>}fn valid_bst(root:&Option<Box<Tree>>)->bool{fn check(n:&Option<Box<Tree>>,lo:Option<i32>,hi:Option<i32>)->bool{match n{None=>true,Some(n)=>{if lo.is_some_and(|v|n.value<=v)||hi.is_some_and(|v|n.value>=v){return false;}check(&n.left,lo,Some(n.value))&&check(&n.right,Some(n.value),hi)}}}check(root,None,None)}''',
 [('valid_bst(&None)','true'),('valid_bst(&Some(Box::new(Tree{value:i32::MIN,left:None,right:Some(Box::new(Tree{value:i32::MAX,left:None,right:None}))})))','true'),('valid_bst(&Some(Box::new(Tree{value:10,left:None,right:Some(Box::new(Tree{value:15,left:Some(Box::new(Tree{value:6,left:None,right:None})),right:None}))})))','false'),('valid_bst(&Some(Box::new(Tree{value:2,left:Some(Box::new(Tree{value:2,left:None,right:None})),right:None})))','false')],
 ['Carry bounds from all ancestors, not just the direct parent.','Optional bounds avoid sentinel collisions at integer extremes.'],
 'How would an inorder traversal solve this? How would you avoid recursion for untrusted tree depth?', 'Target: O(n) time, O(height) stack space.')

question('Parse a batch with useful errors','Custom enums · error propagation',
 'Parse a comma-separated batch of signed i64 quantities and sum them using checked addition. Whitespace-only input is zero. Reject an invalid token with Invalid(index), using a zero-based token index; reject arithmetic overflow with Overflow. Stop at the first error.',
 ['Up to 10,000 tokens.','Empty tokens inside a nonempty batch are invalid.'],
 [('sum_batch("10, -3, 2")','Ok(9)'),('sum_batch("1,,2")','Err(BatchError::Invalid(1))')],
 '#[derive(Debug, PartialEq)]\nenum BatchError { Invalid(usize), Overflow }\nfn sum_batch(input: &str) -> Result<i64, BatchError> {\n    todo!()\n}',
 '#[derive(Debug,PartialEq)]enum BatchError{Invalid(usize),Overflow}fn sum_batch(input:&str)->Result<i64,BatchError>{if input.trim().is_empty(){return Ok(0);}let mut sum=0i64;for(i,s)in input.split(\',\').enumerate(){let n=s.trim().parse::<i64>().map_err(|_|BatchError::Invalid(i))?;sum=sum.checked_add(n).ok_or(BatchError::Overflow)?;}Ok(sum)}',
 [('sum_batch("10, -3, 2")','Ok(9)'),('sum_batch("1,,2")','Err(BatchError::Invalid(1))'),('sum_batch(" ")','Ok(0)'),('sum_batch("9223372036854775807,1")','Err(BatchError::Overflow)'),('sum_batch("no,1")','Err(BatchError::Invalid(0))'),('sum_batch("1,")','Err(BatchError::Invalid(1))')],
 ['Separate token parse errors from accumulation errors.','Use enumerate, map_err, checked_add, and ? to preserve the first failure.'],
 'Would you expose parsing-library errors directly or wrap them? What information should a batch API retain?', 'Target: O(n) time and O(1) extra space.')

question('Generic lower bound','Trait bounds · borrowing non-Copy values',
 'Write a reusable lower_bound for sorted slices. Find the insertion index before all values equal to the target; if all values are smaller, choose len(). Work with any Ord type without cloning or moving values out of the slice.',
 ['0–100,000 sorted values; T need not implement Copy or Clone.'],
 [('lower_bound(&[1,3,3,7], &3)','1'),('lower_bound(&[1,3], &4)','2')],
 'fn lower_bound<T: Ord>(values: &[T], target: &T) -> usize {\n    todo!()\n}',
 'fn lower_bound<T:Ord>(values:&[T],target:&T)->usize{let(mut l,mut r)=(0,values.len());while l<r{let m=l+(r-l)/2;if &values[m]<target{l=m+1;}else{r=m;}}l}',
 [('lower_bound(&[1,3,3,7],&3)','1'),('lower_bound(&[1,3],&4)','2'),('lower_bound(&Vec::<i32>::new(),&0)','0'),('{#[derive(Eq,PartialEq,Ord,PartialOrd)]struct Key(i32);lower_bound(&[Key(2),Key(5),Key(9)],&Key(5))}','1'),('lower_bound(&["a","c"],&"b")','1')],
 ['Compare references rather than taking ownership.','A half-open search range naturally includes the insertion index len().'],
 'Why is Ord a stronger contract than PartialOrd? How would a custom comparator change this API?', 'Target: O(log n) comparisons and O(1) extra space.')

question('Design an LRU cache','Struct API · eviction · recency',
 'Implement Lru with new(capacity), get(key), and put(key,value). A successful get and every put mark the key most recent. When full, a new key evicts the least recently used key. Updating a key must not increase the size; capacity zero stores nothing.',
 ['Keys and values are i32; capacity is 0–128.','A missing get does not change recency. An O(capacity) implementation is acceptable for this exercise.'],
 [('put(1,10); put(2,20); get(1); put(3,30), capacity 2','key 2 is evicted; get(1) is Some(10)')],
 'struct Lru {\n    // Add your fields\n}\nimpl Lru {\n    fn new(capacity: usize) -> Self { todo!() }\n    fn get(&mut self, key: i32) -> Option<i32> { todo!() }\n    fn put(&mut self, key: i32, value: i32) { todo!() }\n}',
 'struct Lru{cap:usize,items:std::collections::VecDeque<(i32,i32)>}impl Lru{fn new(capacity:usize)->Self{Self{cap:capacity,items:Default::default()}}fn get(&mut self,key:i32)->Option<i32>{let i=self.items.iter().position(|x|x.0==key)?;let item=self.items.remove(i)?;self.items.push_back(item);Some(item.1)}fn put(&mut self,key:i32,value:i32){if self.cap==0{return;}if let Some(i)=self.items.iter().position(|x|x.0==key){self.items.remove(i);}else if self.items.len()==self.cap{self.items.pop_front();}self.items.push_back((key,value));}}',
 [('{let mut c=Lru::new(2);c.put(1,10);c.put(2,20);c.get(1);c.put(3,30);(c.get(2),c.get(1),c.get(3))}','(None,Some(10),Some(30))'),('{let mut c=Lru::new(0);c.put(1,1);c.get(1)}','None'),('{let mut c=Lru::new(2);c.put(1,1);c.put(2,2);c.put(1,9);c.put(3,3);(c.get(2),c.get(1))}','(None,Some(9))'),('{let mut c=Lru::new(1);c.put(1,1);c.get(99);c.put(2,2);(c.get(1),c.get(2))}','(None,Some(2))')],
 ['Model most-recent and least-recent ends explicitly.','Remove an existing key before appending its updated entry.'],
 'Sketch an expected O(1) design. What ownership challenges arise with a map plus a doubly linked list?', 'Accepted: O(capacity) per operation; discuss an O(1) design.')

question('Build a lazy merge iterator','Iterator · associated types · laziness',
 'Merge two sorted integer streams into one sorted iterator, preserving duplicates. Provide merge_sorted(a,b) for arbitrary iterators of i32. Do not eagerly collect either stream: an input may be infinite.',
 ['Both streams are nondecreasing.','Consume only enough input to produce requested output, with at most one buffered item per stream.'],
 [('merge_sorted([1,4].into_iter(), [2,3].into_iter()).collect::<Vec<_>>()','vec![1,2,3,4]')],
 'fn merge_sorted<A: Iterator<Item=i32>, B: Iterator<Item=i32>>(a: A, b: B) -> impl Iterator<Item=i32> {\n    std::iter::empty() // Replace with a lazy implementation\n}',
 'fn merge_sorted<A:Iterator<Item=i32>,B:Iterator<Item=i32>>(a:A,b:B)->impl Iterator<Item=i32>{let(mut a,mut b)=(a.peekable(),b.peekable());std::iter::from_fn(move||match(a.peek(),b.peek()){(Some(x),Some(y))=>if x<=y{a.next()}else{b.next()},(Some(_),None)=>a.next(),(None,Some(_))=>b.next(),(None,None)=>None})}',
 [('merge_sorted([1,4].into_iter(),[2,3].into_iter()).collect::<Vec<_>>()','vec![1,2,3,4]'),('merge_sorted([1,1].into_iter(),[1].into_iter()).collect::<Vec<_>>()','vec![1,1,1]'),('merge_sorted(std::iter::empty(),[2,5].into_iter()).collect::<Vec<_>>()','vec![2,5]'),('merge_sorted((0..).step_by(2),(1..).step_by(2)).take(6).collect::<Vec<_>>()','vec![0,1,2,3,4,5]')],
 ['Peek at the next item of each iterator before choosing which to advance.','from_fn can capture mutable iterator state and produce one item per call.'],
 'When can this merged iterator promise ExactSizeIterator or FusedIterator?', 'Target: O(1) buffered space and O(1) work per emitted item.')

question('Compose a validation pipeline','Trait objects · short-circuiting',
 'A service runs heterogeneous validators on a request. Define a Check trait with check(&self, input: &str) -> Result<(), String>. Implement validate to run borrowed trait objects in order and stop immediately at the first error. Preserve that error message.',
 ['The validator list may be empty.','Later validators must not execute after failure; tests use observable call counts.'],
 [('checks: [passes, rejects("too long"), passes]','Err("too long"); third check is never called')],
 'trait Check { fn check(&self, input: &str) -> Result<(), String>; }\nfn validate(input: &str, checks: &[&dyn Check]) -> Result<(), String> {\n    todo!()\n}',
 'trait Check{fn check(&self,input:&str)->Result<(),String>;}fn validate(input:&str,checks:&[&dyn Check])->Result<(),String>{for check in checks{check.check(input)?;}Ok(())}',
 [('validate("x",&[])','Ok(())'),('{struct Required;impl Check for Required{fn check(&self,s:&str)->Result<(),String>{if s.is_empty(){Err("empty".into())}else{Ok(())}}}validate("",&[&Required])}','Err(String::from("empty"))'),('{use std::cell::Cell;struct C<\'a>(&\'a Cell<i32>,bool);impl Check for C<\'_>{fn check(&self,_:&str)->Result<(),String>{self.0.set(self.0.get()+1);if self.1{Err("stop".into())}else{Ok(())}}}let n=Cell::new(0);let a=C(&n,false);let b=C(&n,true);let c=C(&n,false);(validate("x",&[&a,&b,&c]),n.get())}','(Err(String::from("stop")),2)')],
 ['All checks share behavior but may have different concrete types.','The ? operator expresses ordered short-circuiting.'],
 'Compare dynamic dispatch with a generic homogeneous slice. Which trait methods would prevent using dyn Check?', 'Target: O(number of checks actually reached), excluding their internal work.')

question('Evaluate an expression tree','Enums · recursion · checked math',
 'Evaluate an integer expression tree with values, addition, and division. Arithmetic is checked: overflow yields "overflow" and division by zero yields "division by zero". Evaluate the left subtree before the right and propagate its first error.',
 ['At most 1,000 nodes and depth at most 100.','Use i64; MIN / -1 is overflow.'],
 [('Add(Value(2), Div(Value(9), Value(3)))','Ok(5)')],
 "enum Expr { Value(i64), Add(Box<Expr>,Box<Expr>), Div(Box<Expr>,Box<Expr>) }\nfn evaluate_expr(expr: &Expr) -> Result<i64, &'static str> {\n    todo!()\n}",
 'enum Expr{Value(i64),Add(Box<Expr>,Box<Expr>),Div(Box<Expr>,Box<Expr>)}fn evaluate_expr(expr:&Expr)->Result<i64,&\'static str>{match expr{Expr::Value(v)=>Ok(*v),Expr::Add(a,b)=>evaluate_expr(a)?.checked_add(evaluate_expr(b)?).ok_or("overflow"),Expr::Div(a,b)=>{let a=evaluate_expr(a)?;let b=evaluate_expr(b)?;if b==0{Err("division by zero")}else{a.checked_div(b).ok_or("overflow")}}}}',
 [('evaluate_expr(&Expr::Add(Box::new(Expr::Value(2)),Box::new(Expr::Div(Box::new(Expr::Value(9)),Box::new(Expr::Value(3))))))','Ok(5)'),('evaluate_expr(&Expr::Div(Box::new(Expr::Value(1)),Box::new(Expr::Value(0))))','Err("division by zero")'),('evaluate_expr(&Expr::Div(Box::new(Expr::Value(i64::MIN)),Box::new(Expr::Value(-1))))','Err("overflow")'),('evaluate_expr(&Expr::Add(Box::new(Expr::Value(i64::MAX)),Box::new(Expr::Value(1))))','Err("overflow")')],
 ['Match each enum variant and recurse through borrowed child nodes.','Distinguish a zero denominator before checked_div.'],
 'How would you add variables, source locations, or an iterative evaluator?', 'Target: O(nodes) time and O(depth) stack space.')

question('Retry a fallible operation','FnMut · generic errors · exact call counts',
 'Implement retry(attempts, operation). Stop on the first success. If every call fails, preserve the last error as Err(Some(error)). With zero attempts, make no calls and use Err(None). Do not require the success or error types to be Clone.',
 ['At most 100 attempts.','The closure may mutate captured state. No delay or sleeping is required.'],
 [('retry(3, operation that fails twice then succeeds with 42)','Ok(42), exactly 3 calls')],
 'fn retry<T,E,F: FnMut() -> Result<T,E>>(attempts: usize, mut operation: F) -> Result<T,Option<E>> {\n    todo!()\n}',
 'fn retry<T,E,F:FnMut()->Result<T,E>>(attempts:usize,mut operation:F)->Result<T,Option<E>>{let mut last=None;for _ in 0..attempts{match operation(){Ok(v)=>return Ok(v),Err(e)=>last=Some(e)}}Err(last)}',
 [('{let mut n=0;let r=retry(5,||{n+=1;if n==3{Ok(42)}else{Err(n)}});(r,n)}','(Ok(42),3)'),('{let mut n=0;let r=retry::<i32,_,_>(2,||{n+=1;Err(n)});(r,n)}','(Err(Some(2)),2)'),('{let mut n=0;let r=retry::<i32,i32,_>(0,||{n+=1;Ok(1)});(r,n)}','(Err(None),0)'),('retry::<_,i32,_>(3,||Ok(String::from("ok")))','Ok(String::from("ok"))')],
 ['The last error can be owned in an Option<E>.','Successful results should leave the function immediately.'],
 'Which failures should not be retried? Discuss idempotency, backoff, jitter, and cancellation.', 'Target: O(attempts) calls and O(1) bookkeeping space.')

question('Write a single-evaluation macro','macro_rules! · hygiene · side effects',
 'Implement collect_once![expressions...] to build a Vec from zero or more expressions, evaluating each exactly once from left to right. Accept an optional trailing comma, move non-Copy values, and avoid interfering with similarly named variables at the call site.',
 ['All expressions in one invocation have a common element type.','Do not implement a repetition-count syntax.'],
 [('collect_once![1, 2 + 3,]','vec![1,5]')],
 'macro_rules! collect_once {\n    // Match a comma-separated list of expressions\n}',
 'macro_rules! collect_once { ($($item:expr),* $(,)?) => {{ let mut output=Vec::new(); $(output.push($item);)* output }}; }',
 [('collect_once![1,2+3,]','vec![1,5]'),('{let v:Vec<i32>=collect_once![];v}','vec![]'),('{let mut n=0;let v=collect_once![{n+=1;n},{n+=1;n}];(v,n)}','(vec![1,2],2)'),('{let output=String::from("owned");collect_once![output]}','vec![String::from("owned")]')],
 ['A repeated expr matcher handles comma-separated inputs.','Expand into a block with a local vector and one push per expression.'],
 'When would a generic function be preferable? What problems require a procedural macro instead?', 'Target: one evaluation per expression; O(n) output space.')

question('Schedule dependency jobs','Graphs · topological ordering · cycles',
 'Jobs are numbered 0..n. Each edge (a,b) means a must finish before b. Produce a valid execution order, choosing the smallest available job each time. Detect cycles with None. Treat duplicate edges as a single dependency.',
 ['n <= 1,000; all endpoints are valid.','Self-dependencies are cycles. Disconnected jobs still belong in the output.'],
 [('schedule(4, &[(0,2),(1,2),(2,3)])','Some(vec![0,1,2,3])'),('schedule(2, &[(0,1),(1,0)])','None')],
 'fn schedule(n: usize, edges: &[(usize,usize)]) -> Option<Vec<usize>> {\n    todo!()\n}',
 'fn schedule(n:usize,edges:&[(usize,usize)])->Option<Vec<usize>>{use std::collections::{HashSet,BinaryHeap};use std::cmp::Reverse;let mut adj=vec![vec![];n];let mut indeg=vec![0;n];let mut seen=HashSet::new();for &(a,b)in edges{if seen.insert((a,b)){adj[a].push(b);indeg[b]+=1;}}let mut ready=BinaryHeap::new();for i in 0..n{if indeg[i]==0{ready.push(Reverse(i));}}let mut out=vec![];while let Some(Reverse(a))=ready.pop(){out.push(a);for &b in &adj[a]{indeg[b]-=1;if indeg[b]==0{ready.push(Reverse(b));}}}if out.len()==n{Some(out)}else{None}}',
 [('schedule(4,&[(0,2),(1,2),(2,3)])','Some(vec![0,1,2,3])'),('schedule(2,&[(0,1),(1,0)])','None'),('schedule(0,&[])','Some(vec![])'),('schedule(3,&[(0,2),(0,2)])','Some(vec![0,1,2])'),('schedule(2,&[(1,1)])','None'),('schedule(3,&[(2,0)])','Some(vec![1,2,0])')],
 ['Track each job’s number of unfinished prerequisites.','A min-priority queue gives the requested deterministic choice among ready jobs.'],
 'How would you expose a useful cycle diagnostic? How would scheduling change if jobs had durations?', 'Target: O((V+E) log V) time or better.')

question('Find the cheapest route','Dijkstra · priority queues · stale entries',
 'Find the cheapest path from start to goal in a directed, nonnegatively weighted graph represented by adjacency lists. Report None when unreachable. Handle zero-cost edges and repeated edges.',
 ['At most 1,000 nodes; start, goal, and edge endpoints are valid.','Weights <= 1,000,000; costs fit in u64.'],
 [('shortest(&[vec![(1,5),(2,1)], vec![], vec![(1,1)]], 0, 1)','Some(2)')],
 'fn shortest(graph: &[Vec<(usize,u64)>], start: usize, goal: usize) -> Option<u64> {\n    todo!()\n}',
 'fn shortest(graph:&[Vec<(usize,u64)>],start:usize,goal:usize)->Option<u64>{use std::{cmp::Reverse,collections::BinaryHeap};let mut d=vec![u64::MAX;graph.len()];let mut q=BinaryHeap::new();d[start]=0;q.push(Reverse((0,start)));while let Some(Reverse((cost,u)))=q.pop(){if cost!=d[u]{continue;}if u==goal{return Some(cost);}for &(v,w)in &graph[u]{let next=cost+w;if next<d[v]{d[v]=next;q.push(Reverse((next,v)));}}}None}',
 [('shortest(&[vec![(1,5),(2,1)],vec![],vec![(1,1)]],0,1)','Some(2)'),('shortest(&[vec![],vec![]],0,1)','None'),('shortest(&[vec![]],0,0)','Some(0)'),('shortest(&[vec![(1,9),(1,0)],vec![(2,0)],vec![]],0,2)','Some(0)'),('shortest(&[vec![(1,8),(2,1)],vec![(3,1)],vec![(1,1)],vec![]],0,3)','Some(3)')],
 ['Expand the node with the smallest tentative distance.','A priority queue may contain obsolete entries after a better route is found.'],
 'Why does Dijkstra fail with negative edges? When would BFS be enough?', 'Target: O((V+E) log V) time with a heap.')

question('Parallelize borrowed data','Scoped threads · chunking · joins',
 'Compute the sum of a borrowed i64 slice using scoped worker threads, without cloning the input or requiring a static lifetime. Use at most workers threads, never more than the number of items. Treat workers=0 as one worker.',
 ['Up to 10,000 values; all sums fit in i64.','An empty slice has sum zero. Threads must be joined before the function completes.'],
 [('parallel_sum(&[1,2,3,4,5], 3)','15')],
 'fn parallel_sum(values: &[i64], workers: usize) -> i64 {\n    todo!()\n}',
 'fn parallel_sum(values:&[i64],workers:usize)->i64{if values.is_empty(){return 0;}let count=workers.max(1).min(values.len());let size=values.len().div_ceil(count);std::thread::scope(|scope|{let handles:Vec<_>=values.chunks(size).map(|chunk|scope.spawn(move||chunk.iter().sum::<i64>())).collect();handles.into_iter().map(|h|h.join().unwrap()).sum()})}',
 [('parallel_sum(&[1,2,3,4,5],3)','15'),('parallel_sum(&[],4)','0'),('parallel_sum(&[-5,2,1],0)','-2'),('parallel_sum(&[8,9],100)','17'),('parallel_sum(&(0..1000).collect::<Vec<i64>>(),7)','499500')],
 ['Scoped threads can borrow slices because they cannot outlive the scope.','Choose a ceiling-divided chunk size and join every partial sum.'],
 'When does thread overhead outweigh parallelism? Explain scoped threads versus thread::spawn and the static bound.', 'Target: O(n) total work; O(workers) handles. Thread usage is a design-review target.')

question('Bounded parallel map','Worker scheduling · exactly-once calls',
 'Implement parallel_map for a borrowed i32 slice and a shared closure. Run the closure on worker threads, exactly once per input, and preserve input order in the results. Limit spawned workers to min(max(workers,1), input length). The closure may observe thread IDs.',
 ['Closure F: Fn(i32) -> i32 + Sync; it will not panic.','Empty input must not call the closure or spawn useful work.'],
 [('parallel_map(&[3,1,2], 2, |x| x*x)','vec![9,1,4]')],
 'fn parallel_map<F: Fn(i32)->i32 + Sync>(values: &[i32], workers: usize, f: F) -> Vec<i32> {\n    todo!()\n}',
 'fn parallel_map<F:Fn(i32)->i32+Sync>(values:&[i32],workers:usize,f:F)->Vec<i32>{if values.is_empty(){return vec![];}let size=values.len().div_ceil(workers.max(1).min(values.len()));std::thread::scope(|scope|{let f=&f;let hs:Vec<_>=values.chunks(size).map(|c|scope.spawn(move||c.iter().map(|&v|f(v)).collect::<Vec<_>>())).collect();hs.into_iter().flat_map(|h|h.join().unwrap()).collect()})}',
 [('parallel_map(&[3,1,2],2,|x|x*x)','vec![9,1,4]'),('parallel_map(&[],0,|_|panic!("no work"))','vec![]'),('{use std::sync::{Mutex,atomic::{AtomicUsize,Ordering}};let parent=std::thread::current().id();let threads=Mutex::new(std::collections::HashSet::new());let calls=AtomicUsize::new(0);let v=parallel_map(&[1,2,3,4,5],2,|x|{assert_ne!(std::thread::current().id(),parent);threads.lock().unwrap().insert(std::thread::current().id());calls.fetch_add(1,Ordering::SeqCst);x+1});(v,calls.load(Ordering::SeqCst),threads.lock().unwrap().len()<=2)}','(vec![2,3,4,5,6],5,true)'),('parallel_map(&[1,2],0,|x|-x)','vec![-1,-2]')],
 ['Give each worker a disjoint chunk and join chunks in input order.','Borrow the shared closure rather than cloning it or holding a global execution lock.'],
 'Chunking can imbalance workers. How would a shared work queue handle variable-duration tasks?', 'Target: O(n) work, O(n) output, bounded worker count.')

question('Protect shared account transfers','Arc · Mutex · compound invariants',
 'Implement Bank::new(balances), transfer(from,to,amount), and snapshot(). The Bank must be shareable through Arc across threads. Reject invalid indices, insufficient funds, and destination overflow with false and no changes. A same-account transfer succeeds only if the index is valid and funds are sufficient; it changes nothing.',
 ['Use u64 balances. No user callbacks run inside transfer.','Validation and both balance updates must be atomic relative to other operations.'],
 [('Bank::new(vec![10,0]); transfer(0,1,4); snapshot()','true; vec![6,4]')],
 'struct Bank { /* synchronized state */ }\nimpl Bank {\n    fn new(balances: Vec<u64>) -> Self { todo!() }\n    fn transfer(&self, from: usize, to: usize, amount: u64) -> bool { todo!() }\n    fn snapshot(&self) -> Vec<u64> { todo!() }\n}',
 'struct Bank{balances:std::sync::Mutex<Vec<u64>>}impl Bank{fn new(balances:Vec<u64>)->Self{Self{balances:std::sync::Mutex::new(balances)}}fn transfer(&self,from:usize,to:usize,amount:u64)->bool{let mut b=self.balances.lock().unwrap();if from>=b.len()||to>=b.len()||b[from]<amount{return false;}if from==to{return true;}let Some(next)=b[to].checked_add(amount)else{return false;};b[from]-=amount;b[to]=next;true}fn snapshot(&self)->Vec<u64>{self.balances.lock().unwrap().clone()}}',
 [('{let b=Bank::new(vec![10,0]);(b.transfer(0,1,4),b.snapshot())}','(true,vec![6,4])'),('{let b=Bank::new(vec![1,u64::MAX]);(b.transfer(0,1,1),b.transfer(0,3,0),b.transfer(0,0,2),b.snapshot())}','(false,false,false,vec![1,u64::MAX])'),('{let b=Bank::new(vec![u64::MAX]);(b.transfer(0,0,1),b.snapshot())}','(true,vec![u64::MAX])'),('{let b=std::sync::Arc::new(Bank::new(vec![1000,0]));let hs:Vec<_>=(0..8).map(|_|{let b=b.clone();std::thread::spawn(move||{for _ in 0..100{assert!(b.transfer(0,1,1));}})}).collect();for h in hs{h.join().unwrap();}b.snapshot()}','vec![200,800]')],
 ['One lock around the full state makes the transfer invariant straightforward.','Validate everything before modifying either balance.'],
 'What deadlocks can two per-account locks introduce? How would you reduce contention without sacrificing atomicity?', 'Target: O(1) transfer work under a mutex; O(n) snapshot.')

question('Memoize an expensive computation','Generic closures · cache misses',
 'Implement Memo<F> for F: FnMut(u64) -> u64. get(key) computes only on a cache miss and reuses the cached value afterward. clear() removes all cached entries so future gets recompute. The closure may be stateful.',
 ['Single-threaded API using &mut self.','Zero is a valid key and a valid cached result.'],
 [('get(5); get(5); clear(); get(5)','the closure runs twice, not three times')],
 'struct Memo<F: FnMut(u64)->u64> { /* cache and closure */ }\nimpl<F: FnMut(u64)->u64> Memo<F> {\n    fn new(compute: F) -> Self { todo!() }\n    fn get(&mut self, key: u64) -> u64 { todo!() }\n    fn clear(&mut self) { todo!() }\n}',
 'struct Memo<F:FnMut(u64)->u64>{compute:F,cache:std::collections::HashMap<u64,u64>}impl<F:FnMut(u64)->u64>Memo<F>{fn new(compute:F)->Self{Self{compute,cache:Default::default()}}fn get(&mut self,key:u64)->u64{if let Some(&v)=self.cache.get(&key){return v;}let v=(self.compute)(key);self.cache.insert(key,v);v}fn clear(&mut self){self.cache.clear();}}',
 [('{let calls=std::cell::Cell::new(0);let mut m=Memo::new(|x|{calls.set(calls.get()+1);x*x});let v=(m.get(5),m.get(5),m.get(0),m.get(0));m.clear();let after=m.get(5);(v,after,calls.get())}','((25,25,0,0),25,3)'),('{let mut m=Memo::new(|x|x+1);(m.get(1),m.get(2),m.get(1))}','(2,3,2)')],
 ['Cache membership must be separate from the cached numeric value.','End an immutable cache lookup before calling the mutable closure and inserting.'],
 'What invalidation policy would you use for changing data? What extra coordination prevents duplicate concurrent computation?', 'Target: expected O(1) cache lookup, excluding the computation.')

question('Initialize a service exactly once','OnceLock · shared initialization',
 'Implement SharedConfig::new() and get_or_init(initializer) -> &String. Multiple threads may call it concurrently; exactly one successful initializer must run and all callers must observe the same stored String. Each initializer is FnOnce() -> String.',
 ['Use only the standard library. Initializers in this exercise do not panic.','The stored String is borrowed from the SharedConfig, not cloned for each caller.'],
 [('get_or_init(|| "first".into()); get_or_init(|| "second".into())','both observe "first"')],
 'struct SharedConfig { /* one-time state */ }\nimpl SharedConfig {\n    fn new() -> Self { todo!() }\n    fn get_or_init<F: FnOnce()->String>(&self, init: F) -> &String { todo!() }\n}',
 'struct SharedConfig{value:std::sync::OnceLock<String>}impl SharedConfig{fn new()->Self{Self{value:std::sync::OnceLock::new()}}fn get_or_init<F:FnOnce()->String>(&self,init:F)->&String{self.value.get_or_init(init)}}',
 [('{let c=SharedConfig::new();let a=c.get_or_init(||"first".into());let b=c.get_or_init(||panic!("called twice"));(a.clone(),std::ptr::eq(a,b))}','(String::from("first"),true)'),('{use std::sync::{Arc,atomic::{AtomicUsize,Ordering}};let c=Arc::new(SharedConfig::new());let n=Arc::new(AtomicUsize::new(0));let hs:Vec<_>=(0..8).map(|_|{let c=c.clone();let n=n.clone();std::thread::spawn(move||c.get_or_init(||{n.fetch_add(1,Ordering::SeqCst);"ready".into()}).clone())}).collect();let all=hs.into_iter().all(|h|h.join().unwrap()=="ready");(all,n.load(Ordering::SeqCst))}','(true,1)')],
 ['A check-then-set sequence without synchronization can run multiple initializers.','The standard library has a synchronization primitive dedicated to one-time initialization.'],
 'What happens if initialization panics or recursively tries to initialize the same value?', 'Target: one successful initializer and borrowed access afterward.')

question('Implement a cooperative future','Future · Pin · wake protocol',
 'Implement YieldN::new(n) as Future<Output=usize>. Its first n polls must decrement remaining work, call wake_by_ref once, and yield Pending. The next poll completes with the original n. Subsequent polls should also be Ready(n). This is a cooperative-yield exercise, not a timer.',
 ['0 <= n <= 100.','Do not block or sleep inside poll. Store enough state to retain the original n.'],
 [('YieldN::new(2), polled three times','Pending, Pending, Ready(2); two wakes')],
 'use std::{future::Future, pin::Pin, task::{Context, Poll}};\nstruct YieldN { /* state */ }\nimpl YieldN { fn new(n: usize) -> Self { todo!() } }\nimpl Future for YieldN {\n    type Output = usize;\n    fn poll(self: Pin<&mut Self>, cx: &mut Context<\'_>) -> Poll<usize> { todo!() }\n}',
 'use std::{future::Future,pin::Pin,task::{Context,Poll}};struct YieldN{remaining:usize,total:usize}impl YieldN{fn new(n:usize)->Self{Self{remaining:n,total:n}}}impl Future for YieldN{type Output=usize;fn poll(self:Pin<&mut Self>,cx:&mut Context<\'_>)->Poll<usize>{let s=self.get_mut();if s.remaining==0{Poll::Ready(s.total)}else{s.remaining-=1;cx.waker().wake_by_ref();Poll::Pending}}}',
 [('{use std::{sync::{Arc,atomic::{AtomicUsize,Ordering}},task::{Wake,Waker}};struct Count(AtomicUsize);impl Wake for Count{fn wake(self:Arc<Self>){self.0.fetch_add(1,Ordering::SeqCst);}}let c=Arc::new(Count(AtomicUsize::new(0)));let w=Waker::from(c.clone());let mut cx=Context::from_waker(&w);let mut f=Box::pin(YieldN::new(2));let a=f.as_mut().poll(&mut cx);let b=f.as_mut().poll(&mut cx);let d=f.as_mut().poll(&mut cx);let e=f.as_mut().poll(&mut cx);(a,b,d,e,c.0.load(Ordering::SeqCst))}','(Poll::Pending,Poll::Pending,Poll::Ready(2),Poll::Ready(2),2)'),('{let mut cx=Context::from_waker(std::task::Waker::noop());let mut f=Box::pin(YieldN::new(0));f.as_mut().poll(&mut cx)}','Poll::Ready(0)')],
 ['Pending needs a mechanism to arrange another poll; this exercise uses the provided waker.','A struct containing only usize fields is Unpin, so get_mut can safely access its state.'],
 'Why would unconditional self-waking be a bad timer implementation? What does Pin protect for a self-referential future?', 'Target: O(1) nonblocking work per poll.')

question('Release a permit with RAII','Drop · Arc · atomics',
 'Implement Permit::new(counter: Arc<AtomicUsize>) so construction increments the active count and dropping the permit decrements it exactly once. Moving a permit must not change the count. It must work across threads and during panic unwinding.',
 ['Counters start at zero; permits must not implement Clone.','Only the permit implementation changes the supplied active count.'],
 [('create two permits; drop one; drop the other','counter: 0 → 2 → 1 → 0')],
 'use std::sync::{Arc, atomic::{AtomicUsize, Ordering}};\nstruct Permit { /* ownership */ }\nimpl Permit { fn new(counter: Arc<AtomicUsize>) -> Self { todo!() } }\nimpl Drop for Permit { fn drop(&mut self) { todo!() } }',
 'use std::sync::{Arc,atomic::{AtomicUsize,Ordering}};struct Permit{counter:Arc<AtomicUsize>}impl Permit{fn new(counter:Arc<AtomicUsize>)->Self{counter.fetch_add(1,Ordering::SeqCst);Self{counter}}}impl Drop for Permit{fn drop(&mut self){self.counter.fetch_sub(1,Ordering::SeqCst);}}',
 [('{let c=Arc::new(AtomicUsize::new(0));let a=Permit::new(c.clone());let b=Permit::new(c.clone());let x=c.load(Ordering::SeqCst);drop(a);let y=c.load(Ordering::SeqCst);std::thread::spawn(move||drop(b)).join().unwrap();(x,y,c.load(Ordering::SeqCst))}','(2,1,0)'),('{let c=Arc::new(AtomicUsize::new(0));let d=c.clone();let _=std::panic::catch_unwind(move||{let _p=Permit::new(d);panic!("simulated failure");});c.load(Ordering::SeqCst)}','0')],
 ['The guard owns one obligation to decrement, regardless of where it moves.','Drop runs when the guard leaves scope, including normal panic unwinding.'],
 'Does Drop always run? Discuss mem::forget, process abort, and whether Relaxed ordering would be sufficient for this counter.', 'Target: O(1) construction/drop; no manual release required.')

question('Audit a mutable slice split','Unsafe boundaries · aliasing · lifetimes',
 'Implement split_checked(slice, mid), producing disjoint mutable prefix and suffix slices when mid <= len and None otherwise. Keep the API safe. You may use split_at_mut first; for the interview follow-up, implement the boundary with raw pointers and justify every unsafe precondition.',
 ['Generic T; include zero-sized types and empty slices.','Both outputs borrow the original slice; no allocations or leaked memory.'],
 [('split_checked(&mut [1,2,3], 1)','Some(([1], [2,3])); mutations affect the original array')],
 'fn split_checked<T>(slice: &mut [T], mid: usize) -> Option<(&mut [T], &mut [T])> {\n    todo!()\n}',
 '''fn split_checked<T>(slice:&mut[T],mid:usize)->Option<(&mut[T],&mut[T])>{let len=slice.len();if mid>len{return None;}let ptr=slice.as_mut_ptr();
    // SAFETY: mid <= len; both ranges remain in the original allocation,
    // are disjoint, initialized and aligned, and borrow for no longer than slice.
    unsafe{Some((std::slice::from_raw_parts_mut(ptr,mid),std::slice::from_raw_parts_mut(ptr.add(mid),len-mid)))}
}''',
 [('{let mut a=[1,2,3];let(l,r)=split_checked(&mut a,1).unwrap();l[0]=9;r[0]=8;a}','[9,8,3]'),('{let mut a=[1,2];split_checked(&mut a,3).is_none()}','true'),('{let mut a:Vec<i32>=vec![];let(l,r)=split_checked(&mut a,0).unwrap();(l.len(),r.len())}','(0,0)'),('{let mut a=[();4];let(l,r)=split_checked(&mut a,2).unwrap();(l.len(),r.len())}','(2,2)'),('{let mut a=[1,2];let(l,r)=split_checked(&mut a,2).unwrap();(l.len(),r.len())}','(2,0)')],
 ['A checked boundary can turn a potentially panicking operation into Option.','For raw pointers, explain alignment, initialization, allocation bounds, lifetimes, and disjoint access.'],
 'Why can passing tests never prove an unsafe implementation sound? How would Miri help during development?', 'Target: O(1) time and space; unsafe soundness requires review.')

question('Transactional ledger: the final round','State machines · idempotency · rollback',
 'Implement Ledger with new(balance), apply(id, delta), and balance(). Each successful ID is applied once. An already successful ID yields Ok(false), regardless of its new delta. A new successful operation yields Ok(true). Reject i64 overflow with "overflow" or a negative resulting balance with "insufficient funds". Failed IDs must remain retryable and failures must not change the balance.',
 ['Initial balance is a nonnegative i64; deltas are any i64.','IDs are arbitrary nonempty strings. This API is single-threaded.'],
 [('balance=10; apply("a",-4); apply("a",99); balance()','Ok(true), Ok(false), 6'),('apply("b",-100); apply("b",2)','first fails; the same ID can then succeed')],
 "struct Ledger { /* state */ }\nimpl Ledger {\n    fn new(balance: i64) -> Self { todo!() }\n    fn apply(&mut self, id: &str, delta: i64) -> Result<bool, &'static str> { todo!() }\n    fn balance(&self) -> i64 { todo!() }\n}",
 'struct Ledger{balance:i64,seen:std::collections::HashSet<String>}impl Ledger{fn new(balance:i64)->Self{Self{balance,seen:Default::default()}}fn apply(&mut self,id:&str,delta:i64)->Result<bool,&\'static str>{if self.seen.contains(id){return Ok(false);}let next=self.balance.checked_add(delta).ok_or("overflow")?;if next<0{return Err("insufficient funds");}self.balance=next;self.seen.insert(id.to_owned());Ok(true)}fn balance(&self)->i64{self.balance}}',
 [('{let mut l=Ledger::new(10);let a=l.apply("a",-4);let b=l.apply("a",99);(a,b,l.balance())}','(Ok(true),Ok(false),6)'),('{let mut l=Ledger::new(3);let a=l.apply("x",-9);let b=l.apply("x",2);(a,b,l.balance())}','(Err("insufficient funds"),Ok(true),5)'),('{let mut l=Ledger::new(i64::MAX);let a=l.apply("x",1);let b=l.apply("x",-1);(a,b,l.balance())}','(Err("overflow"),Ok(true),i64::MAX-1)'),('{let mut l=Ledger::new(0);let a=l.apply("zero",0);let b=l.apply("zero",i64::MIN);(a,b,l.balance())}','(Ok(true),Ok(false),0)')],
 ['Check successful IDs before validating a repeated delta.','Commit the balance and ID only after every validation succeeds.'],
 'How would you make this durable and concurrent? Explain the database transaction and uniqueness constraint needed for idempotency.', 'Target: expected O(1) per operation; O(successful IDs) memory.')

assert len(LEVELS)==36
