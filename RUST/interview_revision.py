"""Reviewed interview progression; replaces repetitive output drills and overlapping tasks."""
from copy import deepcopy
from course100 import LEVELS as PREVIOUS, REGIONS as OLD_REGIONS, MODULE_SIZES
LEVELS=deepcopy(PREVIOUS)
REGIONS=list(OLD_REGIONS)
REGIONS[0]=('Hello Shore','CLI problems & numeric reasoning','🌱')
REGIONS[1]=('Loop Lagoon','Search, simulation & invariants','🌊')
UPDATED_IDS=set()

def replace(number,title,topic,task,signature,body,cases,hint,follow_up,constraints):
    level=LEVELS[number-1]
    level.update(title=title,topic=topic,lesson=topic,task=task,mode='function',expected=None,
        starter=signature+' {\n    todo!()\n}',solution=signature+' { '+body+' }',tests=cases,
        examples=cases[:2],constraints=constraints,hints=[hint,'Trace an edge case before writing the code. Explain why each update preserves your invariant.'],
        follow_up=follow_up,complexity='State and justify the time and space costs of your approach.')
    UPDATED_IDS.add(number)

def program(number,title,topic,task,body,cases,hint,follow_up,constraints):
    scaffold='use std::io::{self, Read};\nfn main() {\n    let mut input = String::new();\n    io::stdin().read_to_string(&mut input).unwrap();\n'
    level=LEVELS[number-1]
    level.update(title=title,topic=topic,lesson=topic,task=task,mode='program',expected=None,
        starter=scaffold+'    // Read the supplied input and solve the problem\n}\n',solution=scaffold+body+'\n}',tests=None,
        io_cases=cases,examples=[('stdin: '+i,'stdout: '+o) for i,o in cases[:2]],
        constraints=constraints,hints=[hint,'The same compiled program is run with several inputs. Printing only a sample answer cannot pass.'],
        follow_up=follow_up,complexity='Explain the parsing and computation costs separately.')
    UPDATED_IDS.add(number)

program(2,'Personalize a CLI greeting','Input · whitespace · fallback behavior',
 'A command-line onboarding tool reads one display name from stdin. Trim surrounding whitespace. Print Hello, NAME!; if the trimmed name is empty, print Hello, guest!. Preserve internal spaces and Unicode text.',
 'let name=input.trim();println!("Hello, {}!",if name.is_empty(){"guest"}else{name});',
 [('  Ferris  \n','Hello, Ferris!'),('\n','Hello, guest!'),('Ada Lovelace','Hello, Ada Lovelace!'),('Zoë 🦀','Hello, Zoë 🦀!')],
 'The input-reading code is supplied. Decide whether the trimmed slice is empty before formatting it.',
 'Why is trimming useful at this boundary, and which whitespace should remain inside a name?',
 ['Input is a single UTF-8 line, at most 200 bytes.','Write a complete main program; the runner supplies stdin.'])
program(3,'Split an expense without losing cents','Integer division · remainder · validation',
 'A team shares an expense. Read two unsigned integers: total cents and number of people. Print base extra, where base is each person’s minimum payment and extra is the number who pay one additional cent. For zero people print invalid.',
 'let v:Vec<u64>=input.split_whitespace().map(|s|s.parse().unwrap()).collect();if v[1]==0{println!("invalid");}else{println!("{} {}",v[0]/v[1],v[0]%v[1]);}',
 [('100 3','33 1'),('101 2','50 1'),('0 5','0 0'),('12 0','invalid'),('999 1','999 0')],
 'Use quotient and remainder so no money disappears through floating-point rounding.',
 'How would you decide which people pay the extra cent across repeated expenses?',
 ['Exactly two valid integers, each at most 1,000,000.','The total of all assigned payments must equal the original amount.'])
program(4,'Reconcile a cash drawer','Greedy choice · denominations',
 'Read an amount from 0 to 10,000 cents. For denominations 25, 10, 5, and 1, print the counts in that order using the minimum total number of coins. Separate counts with spaces.',
 'let mut n:u32=input.trim().parse().unwrap();let mut c=Vec::new();for d in [25,10,5,1]{c.push(n/d);n%=d;}println!("{} {} {} {}",c[0],c[1],c[2],c[3]);',
 [('41','1 1 1 1'),('30','1 0 1 0'),('0','0 0 0 0'),('99','3 2 0 4'),('10','0 1 0 0')],
 'After choosing coins of one denomination, carry only the unpaid remainder to the next.',
 'Why would the same greedy approach fail for denominations 4, 3, 1 and amount 6?',
 ['Use only the given denominations.','Output exactly four integer counts.'])
program(5,'Measure an overnight shift','Time representation · wraparound',
 'Read start and end times as HH:MM HH:MM in 24-hour format. Print elapsed minutes. If the end is earlier, the shift ends the next day; equal times mean zero minutes.',
 'let v:Vec<_>=input.split_whitespace().collect();let parse=|s:&str|{let(h,m)=s.split_once(\':\').unwrap();h.parse::<i32>().unwrap()*60+m.parse::<i32>().unwrap()};println!("{}",(parse(v[1])-parse(v[0])+1440)%1440);',
 [('09:30 17:00','450'),('23:50 00:10','20'),('08:00 08:00','0'),('00:00 23:59','1439')],
 'Convert each clock time to minutes after midnight before comparing them.',
 'Why is this insufficient for shifts involving time zones or daylight-saving changes?',
 ['Input contains exactly two valid 24-hour times.','A shift is shorter than 24 hours; ignore calendar/time-zone changes.'])
program(6,'Audit a running wallet balance','State updates · first failure',
 'Read an initial nonnegative balance followed by signed transactions. Apply transactions in order. If a transaction would make the balance negative, print rejected INDEX using its 1-based transaction index and stop. Otherwise print balance FINAL.',
 'let mut it=input.split_whitespace().map(|s|s.parse::<i64>().unwrap());let mut balance=it.next().unwrap();for(i,delta)in it.enumerate(){if balance+delta<0{println!("rejected {}",i+1);return;}balance+=delta;}println!("balance {}",balance);',
 [('10 -3 8 -4','balance 11'),('5 -2 -4 100','rejected 2'),('0','balance 0'),('4 -4 2','balance 2')],
 'Validate the proposed balance before committing each transaction.',
 'Should later transactions be attempted after a rejected debit? How would an all-or-nothing batch differ?',
 ['At most 1,000 transactions; all intermediate arithmetic fits in i64.','The initial balance is always supplied.'])
program(7,'Compare release versions','Tuples · lexicographic comparison',
 'Read two versions MAJOR.MINOR.PATCH. Print older, equal, or newer to describe the first relative to the second. Compare numeric components, not raw strings.',
 'let v:Vec<_>=input.split_whitespace().collect();let parse=|s:&str|s.split(\'.\').map(|x|x.parse::<u32>().unwrap()).collect::<Vec<_>>();println!("{}",match parse(v[0]).cmp(&parse(v[1])){std::cmp::Ordering::Less=>"older",std::cmp::Ordering::Equal=>"equal",std::cmp::Ordering::Greater=>"newer"});',
 [('1.9.0 1.10.0','older'),('2.0.0 1.99.99','newer'),('01.2.3 1.2.3','equal'),('0.0.9 0.0.2','newer')],
 'Earlier components have priority; later components matter only after a tie.',
 'How would prerelease labels such as alpha change the comparison contract?',
 ['Exactly three valid u32 components in each version.','Leading zeros are permitted; no prerelease or build metadata.'])
program(8,'Validate a signed decimal token','Parsing · failure handling · numeric limits',
 'Read one trimmed token. If it parses as i32 and doubling it fits in i32, print the doubled value. Print invalid for parse failure and overflow for a valid i32 whose double does not fit.',
 'match input.trim().parse::<i32>(){Err(_)=>println!("invalid"),Ok(n)=>match n.checked_mul(2){Some(v)=>println!("{}",v),None=>println!("overflow")}}',
 [(' 21 \n','42'),('-4','-8'),('twelve','invalid'),('2147483647','overflow'),('2147483648','invalid'),('0','0')],
 'Parsing and multiplication can fail for different reasons. Preserve that distinction.',
 'Why can overflow occur even after the input has successfully parsed?',
 ['At most 100 input bytes.','No panics for malformed input or arithmetic overflow.'])

replace(9,'Calendar validation at century boundaries','Booleans · condition precedence',
 'A scheduling system needs leap-year detection for Gregorian years 1..=9999. A year divisible by 4 is a leap year except centuries not divisible by 400. Implement leap_year(year).',
 'fn leap_year(year: u32) -> bool','year%400==0||(year%4==0&&year%100!=0)',
 [('leap_year(2024)','true'),('leap_year(1900)','false'),('leap_year(2000)','true'),('leap_year(2023)','false')],
 'Write the century exception explicitly instead of treating every multiple of four alike.',
 'Which boundary tests distinguish the correct rule from a simple divisibility check?', ['Years are valid and within 1..=9999.'])
replace(10,'Charge progressive usage tiers','Piecewise arithmetic · inclusive boundaries',
 'A utility charges 2 cents per unit for the first 100 units, 3 cents for the next 100, and 5 cents thereafter. Calculate the total charge for a supplied usage value.',
 'fn usage_charge(units: u32) -> u32','units.min(100)*2+units.saturating_sub(100).min(100)*3+units.saturating_sub(200)*5',
 [('usage_charge(0)','0'),('usage_charge(100)','200'),('usage_charge(101)','203'),('usage_charge(200)','500'),('usage_charge(250)','750')],
 'Each tier applies only to the units within it, not to the whole usage total.',
 'How would you represent configurable tiers without a long if/else chain?', ['Usage is at most 100,000 units.','Use integer cents.'])
replace(11,'Prevent double-counting multiples','Arithmetic · inclusion-exclusion',
 'Count the positive integers up to n divisible by 3 or 5. Numbers divisible by both count once. Avoid iterating through all n values.',
 'fn special_count(n: u64) -> u64','n/3+n/5-n/15',
 [('special_count(0)','0'),('special_count(15)','7'),('special_count(100)','47'),('special_count(1_000_000_000)','466666667')],
 'Count each group, then subtract their overlap.',
 'How would you generalize to arbitrary positive divisors using their least common multiple?', ['n <= 1,000,000,000.','Discuss an O(1) arithmetic approach.'])
replace(12,'Safely place a paginated result window','Saturating arithmetic · bounds',
 'Given total items, a zero-based page index, and page size, produce the half-open (start,end) range for that page. Zero size means (0,0); pages past the end give (total,total). Avoid usize multiplication overflow.',
 'fn page_range(total: usize, page: usize, size: usize) -> (usize,usize)','if size==0{return(0,0);}let start=page.saturating_mul(size).min(total);(start,start.saturating_add(size).min(total))',
 [('page_range(23,2,10)','(20,23)'),('page_range(23,3,10)','(23,23)'),('page_range(23,usize::MAX,10)','(23,23)'),('page_range(23,4,0)','(0,0)'),('page_range(0,0,5)','(0,0)')],
 'Bound the start and end separately; arithmetic can overflow before a later min call.',
 'Why might a cursor-based API be more stable than page numbers for frequently changing data?', ['All parameters may be any usize.'])
replace(13,'Find the missing sequence number','Arithmetic invariant · wide sums',
 'A batch contains distinct IDs drawn from 0..=n, where n is the slice length. Exactly one ID is absent. Find it without sorting or modifying the input.',
 'fn missing_id(ids: &[usize]) -> usize','let mut x=ids.len();for(i,&v)in ids.iter().enumerate(){x^=i^v;}x',
 [('missing_id(&[3,0,1])','2'),('missing_id(&[])','0'),('missing_id(&[0,1,2])','3'),('missing_id(&[1])','0')],
 'An operation that cancels equal values avoids needing extra storage.',
 'How does XOR avoid overflow compared with a formula based on summation?', ['IDs are distinct and satisfy the stated range.','Target O(n) time, O(1) extra space.'])
replace(14,'Find a second distinct high score','One-pass state · duplicate handling',
 'Find the second-highest distinct score. Duplicate copies of the maximum do not qualify. Use None when fewer than two distinct values exist.',
 'fn runner_up(scores: &[i32]) -> Option<i32>','let(mut first,mut second)=(None,None);for &x in scores{if first.is_none_or(|v|x>v){second=first;first=Some(x);}else if Some(x)!=first&&second.is_none_or(|v|x>v){second=Some(x);}}second',
 [('runner_up(&[9,9,7,8])','Some(8)'),('runner_up(&[4,4])','None'),('runner_up(&[])','None'),('runner_up(&[i32::MIN,0])','Some(i32::MIN)')],
 'Track two distinct candidates; a numeric sentinel can collide with a real score.',
 'How would the design change for the kth distinct largest value?', ['All i32 values are permitted.','Target one pass without sorting.'])
replace(15,'Compress sorted IDs in place','Two pointers · logical length',
 'Remove duplicates from a nondecreasing mutable slice by compacting unique IDs into its prefix. Report the prefix length. Values after that prefix are unspecified.',
 'fn compact_ids(ids: &mut [i32]) -> usize','let mut write=0;for read in 0..ids.len(){if write==0||ids[read]!=ids[write-1]{ids[write]=ids[read];write+=1;}}write',
 [('{let mut v=[1,1,2,3,3];let n=compact_ids(&mut v);v[..n].to_vec()}','vec![1,2,3]'),('compact_ids(&mut [])','0'),('{let mut v=[7,7,7];compact_ids(&mut v)}','1')],
 'Keep a write position for the next unique value and a read position for scanning.',
 'Why does sorted input allow this without a set?', ['Sorted nondecreasing input.','Target O(n) time and O(1) extra space.'])
replace(16,'Move empty slots to the end','Stable partition · in-place mutation',
 'A buffer uses zero for an empty slot. Move all zeros to the end while keeping nonzero values in their original order. Mutate the supplied slice without an auxiliary vector.',
 'fn move_empty(values: &mut [i32])','let mut w=0;for r in 0..values.len(){if values[r]!=0{values.swap(w,r);w+=1;}}',
 [('{let mut v=[0,3,0,-1,4];move_empty(&mut v);v}','[3,-1,4,0,0]'),('{let mut v=[0,0];move_empty(&mut v);v}','[0,0]'),('{let mut v=[1,2];move_empty(&mut v);v}','[1,2]')],
 'Advance the destination only after finding a nonzero item.',
 'What distinguishes this from an unstable partition?', ['Signed i32 values; only zero is empty.','Target O(n) time, O(1) space.'])
replace(17,'Best single buy and sell','Running minimum · order constraints',
 'Given daily prices, find the maximum profit from at most one buy followed by a later sell. Do not short-sell. No profitable trade, or fewer than two days, yields zero.',
 'fn best_profit(prices: &[u32]) -> u32','let mut low=u32::MAX;let mut best=0;for &p in prices{low=low.min(p);best=best.max(p-low);}best',
 [('best_profit(&[7,1,5,3,6,4])','5'),('best_profit(&[7,6,4,1])','0'),('best_profit(&[])','0'),('best_profit(&[4])','0')],
 'A valid buy price must have appeared before the current selling opportunity.',
 'Why is taking global maximum minus global minimum incorrect?', ['All prices are u32.','Target O(n) time and O(1) space.'])
replace(18,'Measure an uninterrupted success streak','Run tracking · reset behavior',
 'A boolean sequence records job outcomes. Find the longest contiguous run of true values. A failure resets the current run.',
 'fn longest_streak(outcomes: &[bool]) -> usize','let(mut run,mut best)=(0,0);for &ok in outcomes{if ok{run+=1;best=best.max(run);}else{run=0;}}best',
 [('longest_streak(&[true,true,false,true,true,true])','3'),('longest_streak(&[])','0'),('longest_streak(&[false,false])','0'),('longest_streak(&[true])','1')],
 'The current streak and the best streak seen so far are different pieces of state.',
 'How would you allow exactly one failure within a qualifying window?', ['Up to 100,000 outcomes.'])
replace(19,'Detect a monotonic trend','Adjacent comparisons · direction flags',
 'Decide whether readings are entirely nondecreasing or entirely nonincreasing. Equal neighbors are allowed. Empty and single-element inputs are monotonic.',
 'fn monotonic(readings: &[i32]) -> bool','let(mut up,mut down)=(true,true);for w in readings.windows(2){up&=w[0]<=w[1];down&=w[0]>=w[1];}up||down',
 [('monotonic(&[1,2,2,4])','true'),('monotonic(&[4,2,2,1])','true'),('monotonic(&[1,3,2])','false'),('monotonic(&[])','true')],
 'Track whether each possible direction is still consistent with all pairs.',
 'What changes if you must remove at most one outlier to make the sequence monotonic?', ['All i32 values are permitted.'])
replace(20,'Cancel adjacent duplicate events','Stack · cascading cancellation',
 'Repeated adjacent characters cancel in pairs. Remove pairs repeatedly until no adjacent duplicate pair remains. Treat text as Unicode scalar values.',
 'fn cancel_pairs(text: &str) -> String','let mut s=Vec::new();for c in text.chars(){if s.last()==Some(&c){s.pop();}else{s.push(c);}}s.into_iter().collect()',
 [('cancel_pairs("abbaca")','"ca"'),('cancel_pairs("abba")','""'),('cancel_pairs("🦀🦀a")','"a"'),('cancel_pairs("abc")','"abc"')],
 'A cancellation can expose a new adjacent pair among previously processed values.',
 'Why is one left-to-right pass over a stack enough to model repeated cancellation?', ['Input contains at most 10,000 Unicode scalar values.'])
replace(21,'Find a balance point','Prefix sums · excluded current item',
 'Find the earliest index where the sum strictly to its left equals the sum strictly to its right. The current value belongs to neither side. Use None if there is no such index.',
 'fn balance_point(values: &[i32]) -> Option<usize>','let total:i64=values.iter().map(|&v|v as i64).sum();let mut left=0;for(i,&v)in values.iter().enumerate(){if left==total-left-v as i64{return Some(i);}left+=v as i64;}None',
 [('balance_point(&[1,7,3,6,5,6])','Some(3)'),('balance_point(&[2,1,-1])','Some(0)'),('balance_point(&[])','None'),('balance_point(&[9])','Some(0)')],
 'Precompute the total, then maintain only the left-side sum.',
 'Why is subtracting the current item necessary? Why accumulate i32 inputs in i64?', ['At most 100,000 i32 values.'])
replace(22,'Buy the maximum number of items','Sorting · budget allocation',
 'Given item costs and a budget, determine how many distinct items can be purchased. Each listed item can be bought once. Costs may be zero; do not mutate the input.',
 'fn affordable_count(costs: &[u32], budget: u64) -> usize','let mut v=costs.to_vec();v.sort_unstable();let(mut left,mut count)=(budget,0);for cost in v{if cost as u64>left{break;}left-=cost as u64;count+=1;}count',
 [('affordable_count(&[5,1,3,2],6)','3'),('affordable_count(&[0,0,4],0)','2'),('affordable_count(&[],10)','0'),('affordable_count(&[8,9],3)','0')],
 'If your goal is item count rather than item value, consider the cheapest remaining purchase first.',
 'Why does the greedy choice work here but not for a general value-maximizing knapsack?', ['Up to 10,000 items.','Items have no value difference beyond whether they are purchased.'])
replace(23,'Find the first repeated request','HashSet · online detection',
 'Process request IDs in order and identify the first ID whose current arrival repeats an earlier ID. This is about the earliest second occurrence, not the smallest ID or the earliest first occurrence.',
 'fn first_repeat(ids: &[u64]) -> Option<u64>','let mut seen=std::collections::HashSet::new();for &id in ids{if !seen.insert(id){return Some(id);}}None',
 [('first_repeat(&[4,2,2,4])','Some(2)'),('first_repeat(&[1,2,3])','None'),('first_repeat(&[])','None'),('first_repeat(&[0,0])','Some(0)')],
 'Stop at the first insertion that reports an already present value.',
 'How would bounded-memory detection change the guarantee for an unbounded stream?', ['Up to 100,000 IDs.'])
replace(24,'Count overlapping search hits','Byte windows · overlap semantics',
 'Count occurrences of a nonempty ASCII pattern in ASCII text, including overlaps. An empty pattern has count zero. Do not skip ahead by the pattern length after a match.',
 'fn overlapping_hits(text: &str, pattern: &str) -> usize','if pattern.is_empty(){return 0;}text.as_bytes().windows(pattern.len()).filter(|w|*w==pattern.as_bytes()).count()',
 [('overlapping_hits("aaaa","aa")','3'),('overlapping_hits("banana","ana")','2'),('overlapping_hits("a","long")','0'),('overlapping_hits("abc","")','0')],
 'Compare every candidate starting position; overlapping matches share characters.',
 'What are the worst-case costs? When would KMP or a similar search algorithm be preferable?', ['ASCII text and pattern, at most 10,000 bytes.'])

# Remove weak formula-only exercises and algorithmic overlaps elsewhere.
replace(25,'Validate and total invoice lines','Checked arithmetic · indexed errors',
 'Invoice lines contain (quantity, unit_price) in u64. Sum quantity*price with checked arithmetic. Report the zero-based index of the first line whose multiplication or addition overflows.',
 'fn invoice_total(lines: &[(u64,u64)]) -> Result<u64,usize>','let mut total=0u64;for(i,&(qty,price))in lines.iter().enumerate(){let line=qty.checked_mul(price).ok_or(i)?;total=total.checked_add(line).ok_or(i)?;}Ok(total)',
 [('invoice_total(&[(2,30),(3,10)])','Ok(90)'),('invoice_total(&[])','Ok(0)'),('invoice_total(&[(2,u64::MAX)])','Err(0)'),('invoice_total(&[(1,u64::MAX),(1,1)])','Err(1)')],
 'Both the subtotal multiplication and cumulative addition can fail.',
 'How would rounding and decimal currency change the representation?', ['All u64 quantities and prices are valid inputs.','Stop at the first failing line.'])
replace(31,'Validate a triangle classification','Sorting · overflow-safe comparison',
 'Classify three u32 side lengths as invalid, equilateral, isosceles, or scalene. A zero side or a sum of the two shorter sides not exceeding the longest is invalid.',
 'fn triangle(a: u32, b: u32, c: u32) -> &\'static str','let mut s=[a as u64,b as u64,c as u64];s.sort();if s[0]==0||s[0]+s[1]<=s[2]{"invalid"}else if a==b&&b==c{"equilateral"}else if a==b||a==c||b==c{"isosceles"}else{"scalene"}',
 [('triangle(3,4,5)','"scalene"'),('triangle(2,2,3)','"isosceles"'),('triangle(1,2,3)','"invalid"'),('triangle(0,1,1)','"invalid"'),('triangle(u32::MAX,u32::MAX,u32::MAX)','"equilateral"')],
 'Validate the geometry before classifying equal sides; widen before adding.',
 'Which cases would a naive equality-only implementation classify incorrectly?', ['All u32 inputs must be handled without overflow.'])
replace(39,'Minimize copies when sanitizing text','Cow · borrowed versus owned data',
 'Implement sanitize(text) -> Cow<str>. If the text contains no ASCII control characters, borrow it unchanged. Otherwise remove ASCII controls and own the cleaned string. Do not remove non-ASCII characters.',
 'fn sanitize(text: &str) -> std::borrow::Cow<\'_,str>','if text.chars().any(|c|c.is_ascii_control()){std::borrow::Cow::Owned(text.chars().filter(|c|!c.is_ascii_control()).collect())}else{std::borrow::Cow::Borrowed(text)}',
 [('sanitize("clean")','"clean"'),('matches!(sanitize("clean"),std::borrow::Cow::Borrowed(_))','true'),('sanitize("a\nb\tc")','"abc"'),('matches!(sanitize("a\nb"),std::borrow::Cow::Owned(_))','true'),('sanitize("é🦀")','"é🦀"')],
 'Cow can represent either an unchanged borrowed slice or a newly allocated result.',
 'Why is returning String always simpler but potentially more expensive?', ['Input is valid UTF-8.','Tests check both contents and ownership variant.'])
replace(40,'Flush an owned buffer without cloning','mem::take · move semantics',
 'Move all queued elements out of a mutable Vec into the result, leaving the original vector empty. Elements need not implement Copy or Clone. Preserve order.',
 'fn flush<T>(buffer: &mut Vec<T>) -> Vec<T>','std::mem::take(buffer)',
 [('{let mut v=vec![3,1,2];let out=flush(&mut v);(out,v.is_empty())}','(vec![3,1,2],true)'),('{struct X(i32);let mut v=vec![X(7)];let p=v.as_ptr();let out=flush(&mut v);(out[0].0,out.as_ptr()==p,v.is_empty())}','(7,true,true)'),('{let mut v:Vec<i32>=vec![];flush(&mut v)}','vec![]')],
 'Replace the borrowed container with its empty default while moving out the old one.',
 'Contrast taking the whole Vec with draining it. Which keeps the original allocation?', ['Do not clone elements or rebuild the nonempty allocation.'])
replace(41,'Flatten ownership across batches','Nested ownership · allocation sizing',
 'Consume a vector of batches and flatten their owned items in batch order. Work for non-Clone element types and ignore empty batches.',
 'fn flatten_batches<T>(batches: Vec<Vec<T>>) -> Vec<T>','let size=batches.iter().map(Vec::len).sum();let mut out=Vec::with_capacity(size);for batch in batches{out.extend(batch);}out',
 [('flatten_batches(vec![vec![1,2],vec![],vec![3]])','vec![1,2,3]'),('flatten_batches::<i32>(vec![])','vec![]'),('{struct Job(i32);flatten_batches(vec![vec![Job(4)],vec![Job(9)]]).into_iter().map(|x|x.0).collect::<Vec<_>>()}','vec![4,9]')],
 'The outer and inner consuming iterators can transfer ownership directly.',
 'How would you return a lazy flattened iterator instead of allocating the output?', ['Order must be preserved; no Clone bounds.'])
replace(47,'Index borrowed source lines','Byte offsets · lifetimes',
 'For each nonempty line in a source string, produce its original byte offset and a borrowed line slice. Split on newline only. Keep carriage returns as ordinary characters and skip empty lines without losing their offset contribution.',
 'fn line_index(source: &str) -> Vec<(usize,&str)>','let mut offset=0;let mut out=vec![];for line in source.split(\'\\n\'){if !line.is_empty(){out.push((offset,line));}offset+=line.len()+1;}out',
 [('line_index("ab\n\né\nx")','vec![(0,"ab"),(4,"é"),(7,"x")]'),('line_index("")','vec![]'),(r'line_index("a\r\nb")','vec![(0,"a\\r"),(3,"b")]'),('{let s=String::from("a\nb");line_index(&s)[1].1.as_ptr()==s[2..].as_ptr()}','true')],
 'Offsets count bytes consumed from the original text, including skipped separators.',
 'Why do byte offsets and character positions disagree for Unicode text?', ['Valid UTF-8 input.','Borrow the line contents; do not copy them.'])
replace(48,'Parse an escaped delimiter format','State machine · escape handling',
 'Split a record at unescaped commas. Backslash escapes a comma or another backslash; any other escape or a trailing backslash is an error. Preserve empty fields. A record with no text contains one empty field.',
 'fn escaped_fields(record: &str) -> Result<Vec<String>,usize>','let mut fields=vec![String::new()];let mut chars=record.char_indices();while let Some((i,c))=chars.next(){match c{\',\'=>fields.push(String::new()),\'\\\\\'=>match chars.next(){Some((_,v))if v==\',\'||v==\'\\\\\'=>fields.last_mut().unwrap().push(v),_=>return Err(i)},_=>fields.last_mut().unwrap().push(c)}}Ok(fields)',
 [(r'escaped_fields(r"a\,b,c")','Ok(vec!["a,b".into(),"c".into()])'),('escaped_fields(",")','Ok(vec!["".into(),"".into()])'),(r'escaped_fields(r"bad\q")','Err(3)'),('escaped_fields("x\\\\")','Err(1)'),('escaped_fields("")','Ok(vec![String::new()])')],
 'An escape consumes the next character as data rather than as a separator.',
 'Why is split(",") insufficient? How would you extend this to quoted fields?', ['Error index is the original byte offset of the bad backslash.','UTF-8 text outside the escape syntax is preserved.'])
replace(49,'Normalize a relative route safely','Stack · parent segments · validation',
 'Normalize slash-separated relative route segments. Ignore empty segments and ., and let .. remove the previous segment. Reject an absolute path or any .. that would go above the route root. Join the remaining segments with /. This is lexical normalization, not filesystem security.',
 'fn normalize_route(route: &str) -> Option<String>','if route.starts_with(\'/\'){return None;}let mut stack=vec![];for part in route.split(\'/\'){match part{""|"."=>{},".."=>{stack.pop()?;},_=>stack.push(part)}}Some(stack.join("/"))',
 [('normalize_route("a//b/../c")','Some("a/c".into())'),('normalize_route("../a")','None'),('normalize_route("/a")','None'),('normalize_route("a/..")','Some(String::new())'),('normalize_route("a/../../b")','None')],
 'Each ordinary segment adds one removable parent; an empty stack cannot satisfy .. .',
 'Why do symbolic links and URL percent-encoding require separate security handling?', ['Paths use / separators.','The function never accesses the filesystem.'])
replace(74,'Find a peak without scanning','Binary search on a slope',
 'A slice increases strictly to a single peak and then decreases strictly; either side may be empty. Find the peak index in logarithmic time. Empty input has no peak.',
 'fn peak_index(values: &[i32]) -> Option<usize>','if values.is_empty(){return None;}let(mut l,mut r)=(0,values.len()-1);while l<r{let m=l+(r-l)/2;if values[m]<values[m+1]{l=m+1;}else{r=m;}}Some(l)',
 [('peak_index(&[1,3,8,5,2])','Some(2)'),('peak_index(&[1,2,3])','Some(2)'),('peak_index(&[3,2,1])','Some(0)'),('peak_index(&[4])','Some(0)'),('peak_index(&[])','None')],
 'Comparing the middle item with its next neighbor tells you which side still contains the peak.',
 'Why does this fail if the promised shape is absent? What changes with a flat plateau?', ['Input satisfies the strict single-peak contract.','Target O(log n) comparisons and O(1) extra space.'])

assert len(LEVELS)==100 and len(UPDATED_IDS)==32
