# Independent Review Checklist

## A. Provenance

- [ ] Every material claim has a source reference.
- [ ] Repository IDs and full commit SHAs are valid.
- [ ] Paths and line/symbol/configuration locators resolve at the pinned revision.
- [ ] Evidence actually supports the exact claim.
- [ ] No fabricated files, symbols, commits, or line numbers.

## B. Process understanding

- [ ] Process responsibility and boundaries are clear.
- [ ] Repository-to-process mapping is evidence-based.
- [ ] Lifecycle covers startup, initialization, ready, shutdown, and recovery where applicable.
- [ ] Interfaces identify provider, consumer, mechanism, and contract.
- [ ] Runtime dependencies are not inferred from build dependencies.
- [ ] Important error paths, timeouts, and constraints are not omitted.

## C. Platform Profile

- [ ] Claims have the correct profile scope.
- [ ] QNX, Android, and Linux-TBOX are not treated as interchangeable.
- [ ] Deployment context is not guessed.
- [ ] Common claims are supported across every declared applicable profile.
- [ ] Uninspected profiles are marked Unknown.

## D. System integration

- [ ] Every cross-process edge has a relationship type.
- [ ] IPC claims have interface/configuration/implementation evidence.
- [ ] Startup ordering has startup configuration or runtime evidence.
- [ ] CMake DOT edges are labeled as build dependencies only.
- [ ] Conflicts between process pages and system pages are resolved or explicitly recorded.

## E. Quality

- [ ] No unsupported certainty or invented rationale.
- [ ] No stale source references presented as verified.
- [ ] No material contradiction with accepted Wiki knowledge.
- [ ] Unknowns and assumptions are explicit.
- [ ] Findings are classified BLOCKER, MAJOR, MINOR, or INFO.
- [ ] BLOCKER/MAJOR findings prevent PASS.

## F. Approval

- [ ] Independent LLM review was performed in a separate invocation/context.
- [ ] Review report is stored with the proposed change.
- [ ] Human reviewer inspected the diff and evidence.
- [ ] Human approval is recorded before merge.
