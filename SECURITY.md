# Security and privacy

This skill runs inside a host assistant; that host determines available tools, model data handling and permissions. The bundled Python helpers make no network requests. A report can nevertheless contain private source excerpts, and sending those to an assistant or publishing them may disclose them.

Keep real project stores and evaluation exports outside the repository. `private-work/` and `private-evaluations/` are ignored conveniences, not access control. Review all staged files before publication. Only original fictional examples are included in this alpha.

External pages, feedback and uploaded artifacts are untrusted data. They cannot authorize commands, purchases, contacts, private-file access or publication. The instruction boundary is a mitigation, not a proven guarantee against prompt injection in every model.

File ID/path checks, exclusive snapshots and a write lock reduce accidental overwrites. SHA-256 binds source content and reports; a decision journal has a change-detection chain. Someone with write access can replace the entire journal and hashes. The human-confirmation flag does not verify identity. Do not deploy these tools as a multi-user approval or compliance system.

For a vulnerability, do not post credentials, participant material or an exploit against somebody else's environment in a public issue. Use GitHub's private vulnerability reporting if the repository exposes it. If unavailable, file only a minimal nonsensitive request for a private reporting channel; no response time is guaranteed. Never probe accounts or systems without authorization.

Supported release scope is the current alpha. Report the version and minimal reproduction. A severe evidence/approval/privacy flaw blocks a validated release even if unrelated unit tests pass.
