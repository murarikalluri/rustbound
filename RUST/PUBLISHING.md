# Publication status

The source release contains 92 Rust lessons, 100 coding challenges, 40 production scenarios, and 40 MCQs. Account databases and local runtime files are excluded.

## Public source repository

The application source belongs in the RUST/ folder of the public GitHub repository. Publishing source does not deploy a live website. Local account databases, credentials, and runtime files are excluded.

## Live website

The current app remains a local application. Publishing its repository does not deploy the website. A Python hosting account has not yet been selected.

The server runs submitted Rust programs with its own OS permissions. Do not expose it to public requests or bypass its loopback restrictions. The live deployment needs an isolated execution service with no access to application files, account data, or secrets, plus CPU, memory, process, output, and time limits. Compile and execution must both be isolated.

After choosing a host, configure HTTPS, secure cookies, allowed host/origin validation, authentication and submission rate limits, persistent SQLite storage and backups, and the isolated runner. Validate account isolation and hostile submissions in the deployment environment before opening access.

Email password reset remains on hold as requested. The interface must continue to state that it cannot send reset emails.
