"""Fictional incident exercises; source-backed mechanisms are identified separately."""
BRIEFS = {
'graphql-body': (
 'You are on call for a GraphQL order gateway. A marketing campaign has started, but several pods restart even when request count is below the usual peak. Customer support reports failed checkouts. The team wants to double memory immediately; you have to determine whether that is a fix or only a temporary mitigation.',
 ['09:10 — memory climbs on two pods while database latency stays normal.', '09:13 — one pod is killed for exceeding its memory limit.', '09:17 — requests with unusually large bodies appear in gateway telemetry.'],
 'Synthetic evidence\nservice: order-gateway\nrequest_count: below normal peak\nlarge POST bodies: present\nresolved dependency: juniper_hyper 0.10.0\napplication body limit: not configured',
 'Choose the first containment step, identify where the body must be bounded, and explain how you will prove the deployed dependency is fixed.',
 ['Could normal traffic volume alone explain the memory curve?', 'Does the proxy enforce its limit for every route and body transfer mode?', 'How will you test concurrency as well as one oversized request?']),
'build-secret': (
 'Your release engineer notices a harmless test credential marker inside a cached build artifact. The application never intentionally logs credentials. The cache was shared with another team, and a new native dependency build ran yesterday. You own the investigation and must separate stopping future exposure from handling already-exposed data.',
 ['14:00 — an artifact scanner finds an environment marker in target/build output.', '14:08 — the cache is quarantined pending review.', '14:20 — the affected Unix build used a newer C compiler helper crate.'],
 'Synthetic build inventory\nhost: Unix\nlibz-sys: 1.1.30\ncc: 1.6.0\nstatic feature: off\nshared target cache: enabled\nNo real secret values are included in this exercise.',
 'Write a containment and recovery sequence covering dependency remediation, artifact access, old caches, and credential exposure.',
 ['Why can an application log scan miss build-time exposure?', 'Which build configurations actually execute the affected probe?', 'Why does a clean rebuild not remove yesterday’s leaked artifact?']),
'ffi-server-name': (
 'A C-facing client library works in unit tests but intermittently fails during TLS handshakes in a Python binding. The binding constructs the client using a temporary hostname buffer. Failures become more frequent when memory is reused aggressively, while keeping the hostname object alive appears to help.',
 ['11:30 — handshake failures appear after a binding refactor.', '11:42 — native Rust integration tests still pass.', '12:05 — a memory-instrumented test reports invalid reads after client construction.'],
 'Synthetic call sequence\nallocate temporary hostname\ncall rustls_client_connection_new\nrelease temporary hostname\ncontinue TLS processing\nrustls-ffi: 0.15.6',
 'State the broken ownership contract and propose both the dependency fix and a regression test that models a foreign caller.',
 ['Who owns the hostname after the constructor returns?', 'Does the native test exercise temporary foreign storage?', 'How will you verify all bindings ship the new native library?']),
'markdown-expansion': (
 'A documentation preview service becomes CPU-bound when rendering a small submitted Markdown page. Upload size limits are working, so the incident initially looks unrelated to input validation. The preview enabled every parser option to support richer internal wiki syntax.',
 ['16:00 — preview latency rises for a small group of documents.', '16:06 — CPU and allocated event count increase together.', '16:15 — ordinary Markdown remains fast; wiki-link syntax correlates with the failures.'],
 'Synthetic configuration\npulldown-cmark: 0.13.4\nparser options: Options::all()\ninput byte limit: enabled\noutput event budget: absent\nDo not replay large hostile documents on shared services.',
 'Explain why the input-size control did not contain the issue and design a bounded regression for the patched parser.',
 ['Which optional feature changes the affected code path?', 'What metric reveals amplification from bytes to events?', 'What is the temporary containment if upgrade cannot happen immediately?']),
'tls-loop': (
 'A native client service stops completing some connections after a remote endpoint closes during TLS setup. One worker remains busy rather than sleeping. Increasing the outer request timeout does not help. You need to identify whether this is an ordinary slow peer, blocked I/O, or a loop inside the TLS integration.',
 ['08:20 — a subset of requests fail to complete.', '08:28 — a sampled worker stack repeatedly includes complete_io.', '08:41 — an isolated peer-close test reproduces nontermination.'],
 'Synthetic inventory\nrustls: 0.23.4\nintegration: StreamOwned\nevent: close notification during handshake\nouter timeout: does not interrupt synchronous worker',
 'Choose an affected-code-path check, a compatible patch, and a verification strategy that cannot hang the entire test suite.',
 ['Which rustls APIs actually use complete_io?', 'Why is a Tokio-only integration not automatically affected by this advisory?', 'What does cancelling the waiter do to the running synchronous code?']),
'http2-flood': (
 'Your API remains online, but p99 latency climbs sharply while a few HTTP/2 connections consume disproportionate CPU. Autoscaling adds capacity without returning latency to normal. You are asked to explain why an availability attack can be serious even when most requests still eventually succeed.',
 ['10:00 — tail latency alert fires.', '10:07 — database and storage timings remain normal.', '10:18 — HTTP/2 frame handling dominates CPU samples.'],
 'Synthetic protocol findings\nh2: 0.4.3\nlong sequences of CONTINUATION frames\nlegitimate requests: still complete\nconnection concentration: high',
 'Propose immediate traffic containment, the actual remediation, and a mixed-traffic test that measures customer impact.',
 ['Why is process uptime an insufficient success metric?', 'How do you inspect multiple resolved copies of h2?', 'Which latency measurement must be compared before and after?']),
'http2-queue': (
 'A gateway loses memory under a small number of persistent HTTP/2 connections. Application queues are empty. Network inspection shows protocol errors generating outbound control work, but the peers are not allowing that work to drain. The team suspects a leak in request handlers.',
 ['19:00 — resident memory grows with a few long-lived connections.', '19:12 — application request queues are ruled out.', '19:25 — protocol reset queues correlate with the growth.'],
 'Synthetic findings\nh2: 0.4.1\ninvalid incoming frames: recurring\noutbound peer receive window: constrained\ninternal resets: accumulating',
 'Distinguish retained protocol work from an ownership leak and describe the boundary that must be enforced.',
 ['Which queue is growing despite normal application metrics?', 'Can a peer prevent generated responses from draining?', 'Why must the patched version also address later advisories?']),
'lock-await': (
 'A profile service stores cached responses behind a mutex. A recent change refreshes missing entries from a remote service while still holding the guard. Under light traffic it looks correct. With overlapping requests, even cached reads become stuck behind one slow refresh.',
 ['09:00 — a cache refresh begins.', '09:01 — a second task attempts the same lock.', '09:02 — requests stop progressing on the test executor.'],
 'Illustrative problematic sketch\nlet mut cache = state.lock().unwrap();\nlet fresh = fetch_remote().await;\ncache.insert(key, fresh);\n\nQuestion: which resource is still held at the await?',
 'Refactor the access sequence and discuss the race between fetching a snapshot and installing it. Explain when an async mutex would still serialize requests.',
 ['What does the waiting task block?', 'Can the remote fetch happen outside the critical section?', 'Does the refactor need a duplicate-refresh or stale-result policy?']),
'executor-starved': (
 'A service adds image compression to an async endpoint. Health checks become slow whenever large images arrive, despite fast database calls and spare memory. The implementation calls a synchronous compression routine inside an async function and assumes the runtime will move it elsewhere.',
 ['13:00 — compression endpoint launches.', '13:08 — health-check latency spikes during image batches.', '13:20 — executor thread samples show compression work rather than waiting.'],
 'Synthetic metrics\ndatabase p95: stable\nexecutor timer lag: rising\nCPU samples: compression loop\njob concurrency limit: none',
 'Design bounded offloading and an overload policy. Account for running jobs, queued jobs, and what a request timeout actually cancels.',
 ['Does async automatically imply parallel CPU work?', 'Why can unlimited spawn_blocking jobs also overload the machine?', 'Which latency metric demonstrates that unrelated tasks recovered?']),
'queue-oom': (
 'A receipt service acknowledges requests immediately and queues PDF jobs in memory. A short burst is followed by steady memory growth and hour-old jobs. The workers are healthy but slower than producers. Increasing worker count hits a downstream rate limit.',
 ['12:00 — a campaign creates a burst of jobs.', '12:15 — queue age continues rising after the burst.', '12:30 — memory pressure threatens the process.'],
 'Synthetic workload\narrival rate: 600 jobs/min\ncompletion rate: 200 jobs/min\nqueue: unbounded\nmean payload: 100 KiB\ndownstream concurrency budget: fixed',
 'Choose an admission policy and durability guarantee. Estimate the growth trend and explain how a bounded queue differs from bounded total work.',
 ['Where are payloads allocated relative to admission?', 'Can blocked senders themselves accumulate?', 'What does an accepted response promise if the process restarts?']),
'cancelled-write': (
 'A customer retries a purchase after a timeout and receives two confirmation records. The first local future was cancelled, so the team believed the first operation could not complete. Remote logs show that its side effect committed just before the response connection disappeared.',
 ['15:00:00 — request reaches the remote service.', '15:00:02 — local deadline expires.', '15:00:03 — client retries without a stable request key.'],
 'Synthetic correlation\nlogical purchase: same\ntransport request IDs: different\nremote commits: two\nlocal first result: timeout\nidempotency record: missing',
 'Design a durable idempotency and reconciliation flow. State what the caller should infer from timeout when the remote outcome is unknown.',
 ['Which effects survive dropping the local future?', 'Where must uniqueness be enforced across service instances?', 'How should the same key with different request content be treated?']),
'shutdown-loss': (
 'A deployment replaces workers while background exports are running. Users already received accepted responses, but a few exports never appear. Jobs were stored only in spawned tasks, and the process exited after the HTTP listener stopped.',
 ['18:00 — deployment begins draining HTTP traffic.', '18:01 — process exits while export tasks remain active.', '18:10 — support reports accepted export IDs with no stored outcome.'],
 'Synthetic lifecycle\njob persistence: none\nspawn handles: discarded\nnew admission: stopped\nworker drain: not awaited\nunfinished-job metric: absent',
 'Define a restart-safe acceptance contract and implement a shutdown order with a finite deadline and observable unfinished work.',
 ['Does stopping the listener also finish background tasks?', 'Which records must exist before replying accepted?', 'How are jobs recovered if the grace deadline is reached?']),
'unicode-panic': (
 'A customer profile preview works for English test names but fails for some emoji and accented names. The formatter truncates the first few bytes to fit a card. A product designer asks for a limit in visible characters, while the backend team proposes simply using chars().take().',
 ['10:00 — a specific profile repeatedly returns an error.', '10:08 — the stack identifies a string slice boundary.', '10:20 — a combining-accent case remains visually incorrect after a scalar-based change.'],
 'Illustrative failing operation\nlet preview = &name[..limit];\n\nInputs to compare: ASCII, emoji, combining accent\nProduct requirement: visible characters\nStorage requirement: valid UTF-8',
 'Separate byte validity from display semantics and design tests for both requirements.',
 ['What units does limit represent?', 'Why can a valid UTF-8 slice still split a displayed grapheme?', 'Which behavior should an empty or shorter name have?']),
'overflow-release': (
 'A batch import passes small tests but reports an implausibly low total for a large order in release mode. The same input panics in a debug build. The arithmetic uses a narrow integer type chosen for a compact record layout.',
 ['11:00 — a large import produces an incorrect total.', '11:15 — debug reproduction panics at addition.', '11:30 — release reproduction completes with a different numeric result.'],
 'Synthetic calculation\nrepresentation: u16\noperation: unchecked running addition\ninput range: not validated\npolicy for overflow: unspecified',
 'Choose an arithmetic policy from the business requirement and prove it behaves consistently across build profiles.',
 ['Should the domain reject, clamp, or wrap?', 'Would switching to a wider integer eliminate every possible overflow?', 'Which boundary values belong in the regression?']),
'rc-leak': (
 'A desktop editor accumulates memory after documents are opened and closed. There is no invalid memory access, and destructors for some document nodes never run. Each parent owns its children, and each child stores a strong parent reference for navigation.',
 ['09:00 — repeated open/close cycles increase retained nodes.', '09:15 — root handles are dropped as expected.', '09:30 — internal strong reference counts remain nonzero.'],
 'Ownership sketch\nParent --Rc--> Child\nChild  --Rc--> Parent\nexternal owners after close: zero\ninternal strong owners: nonzero',
 'Redesign the ownership graph and write a regression that distinguishes a live ownership cycle from allocator caching.',
 ['Which direction actually needs ownership?', 'What happens when a Weak parent link cannot upgrade?', 'Why does memory safety permit this leak?']),
'sqlite-busy': (
 'A small scheduling service works for one user but intermittently reports database busy during concurrent updates. Each request opens a transaction and then waits for a remote calendar API before committing. The team proposes a much larger connection pool.',
 ['14:00 — concurrent updates trigger busy errors.', '14:10 — write transactions last as long as remote API latency.', '14:25 — increasing connections increases contention rather than throughput.'],
 'Synthetic transaction trace\nBEGIN write\nupdate schedule\nawait remote calendar response\nCOMMIT\nDatabase: SQLite\nwrite duration: dominated by network wait',
 'Shorten the transaction and define consistency with the remote calendar. Explain bounded retries and why WAL is not multiple-writer support.',
 ['What is held while waiting on the network?', 'Which operations can be retried safely?', 'What state records a remote synchronization that needs retry?']),
'lost-update': (
 'Two warehouse service instances accept reservations for the last few items. Both read the same stock, compute a new value, and write it back. Each endpoint returns success, but the final stock no longer matches accepted quantities. A process-local mutex fixes the single-instance test only.',
 ['16:00 — two requests read stock 5.', '16:00 — each accepts a reservation of 4.', '16:01 — the stored stock is 1 although 8 items were accepted.'],
 'Synthetic interleaving\nA: SELECT stock -> 5\nB: SELECT stock -> 5\nA: UPDATE stock = 1\nB: UPDATE stock = 1\naccepted quantity: 8',
 'Replace the read-compute-write race with a database-enforced condition and explain exactly what a zero-row update means.',
 ['Where must the invariant hold across processes?', 'What other writes belong in the same transaction?', 'How will duplicate requests be prevented from reserving twice?']),
'flaky-order': (
 'A report snapshot fails in CI while local output looks correct. Every row and value is present, but ordering differs between executions. The report is assembled from a HashMap. Product says alphabetical order is part of the exported file format.',
 ['08:00 — CI snapshot differs after an unrelated change.', '08:12 — row contents compare equal as a multiset.', '08:25 — repeated fresh processes produce different row sequences.'],
 'Synthetic output A: blue, green, red\nSynthetic output B: red, blue, green\nsource collection: HashMap\nexport contract: alphabetical\nvalues: identical',
 'Fix the product behavior rather than weakening the assertion. Define stable tie-breaking where labels can compare equal.',
 ['Is ordering specified or irrelevant?', 'Should you sort at the boundary or use an ordered collection?', 'When would normalizing test output hide the actual defect?']),
'poisoned-lock': (
 'After one worker panic, unrelated requests begin failing when they acquire the same mutex. A quick patch calls into_inner on every poison error. You are reviewing it and need to decide whether the protected state is still valid after the original failure.',
 ['17:00 — an assertion fails between two state updates.', '17:02 — subsequent callers encounter PoisonError.', '17:10 — a patch proposes ignoring poison unconditionally.'],
 'Synthetic critical section\naccount.total -= amount;\nassert!(external_assumption);\naccount.entries.push(record);\n\nInvariant: total and ledger entries agree',
 'Find the initiating defect, choose a recovery policy, and show how your test detects an inconsistent total/ledger pair.',
 ['Which invariant may be broken at the panic point?', 'Does recovering the guard repair the data?', 'Can state be reconstructed from a durable source?']),
'duplicate-dependency': (
 'A security update is merged, but the next dependency scan still reports the same crate. The manifest shows the new version. An older plugin pins a separate dependency path, and the deployed image may not be the image produced by the latest pipeline.',
 ['13:00 — direct dependency update passes unit tests.', '13:20 — audit still finds a vulnerable version.', '13:40 — reverse dependency inspection identifies another path.'],
 'Synthetic dependency graph\napp -> client-new -> crate 0.4.fixed\napp -> legacy-plugin -> crate 0.3.affected\ndeployed image digest: not yet verified',
 'Trace every affected version to its parent, select a compatible remediation, and prove the corrected graph reached the running service.',
 ['Why can two versions coexist?', 'Which parent constrains the old branch?', 'What evidence distinguishes source remediation from deployment remediation?']),
}

def enrich(scenarios):
    for index,item in enumerate(scenarios,1):
        context,timeline,evidence,task,questions=BRIEFS[item['id']]
        item.update(ticket=f'RB-{index:03d}',context=context,timeline=timeline,evidence=evidence,task=task,investigation_questions=questions,
                    simulation='Fictional incident exercise. Timeline, metrics, and organization are invented for practice.' + (' The vulnerability mechanism and version guidance come from the linked advisory.' if item['kind']=='Documented advisory' else ' This is a general engineering failure scenario, not a reported outage.'))
