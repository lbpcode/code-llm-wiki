# Independent Review Checklist

## A. Provenance and Claim-Evidence

- [ ] Every material claim is atomic and has a stable Claim ID.
- [ ] Every material claim maps to specific supporting/contradicting/qualifying evidence.
- [ ] Repository IDs and full commit SHAs are valid.
- [ ] Paths and line/symbol/configuration locators resolve at the pinned revision.
- [ ] Evidence supports the exact claim, profile, and relationship type.
- [ ] No fabricated files, symbols, commits, or line numbers.
- [ ] Sensitive source excerpts are omitted or safely redacted.

## B. Process understanding

- [ ] Process responsibility and boundaries are clear.
- [ ] Repository-to-Process mapping is evidence-based and many-to-many.
- [ ] Process-to-Profile support is recorded separately from repository inventory.
- [ ] Lifecycle covers startup, initialization, ready, shutdown, and recovery where applicable.
- [ ] Interfaces identify provider, consumer, mechanism, contract, and profile variants.
- [ ] Runtime dependencies are not inferred from build dependencies.
- [ ] Important error paths, timeouts, and constraints are not omitted.

## C. Platform Profile

- [ ] Claims have the correct profile scope.
- [ ] QNX, Android, and Linux-TBOX are not treated as interchangeable.
- [ ] Deployment context is not guessed.
- [ ] Common claims are supported across every declared applicable profile.
- [ ] Uninspected profiles are marked Unknown.

## D. System integration

- [ ] Every cross-process edge has a relationship type and evidence.
- [ ] IPC claims have interface/configuration/implementation evidence.
- [ ] Startup ordering has startup configuration or runtime evidence.
- [ ] CMake DOT edges are labeled as build dependencies only.
- [ ] Both sides of important interfaces are checked where possible.
- [ ] Conflicts between Process pages and System pages are resolved or explicitly recorded.

## E. State and incremental update

- [ ] Claim and Evidence statuses are not confused with approval status.
- [ ] Page-Source Map links pages to claims, source paths/revisions, and dependent pages.
- [ ] Stale evidence invalidates affected claims/pages until revalidated.
- [ ] Approval is bound to the exact candidate diff/commit and relevant source snapshot.
- [ ] Any material post-approval change invalidates approval.
- [ ] AI updates preserve human edits and stop on overlapping conflicts.

## F. Quality and independence

- [ ] Lint checks and NOT RUN checks are explicitly reported.
- [ ] Independent LLM review used a separate invocation and fresh context.
- [ ] Reviewer independently inspected source evidence.
- [ ] No unsupported certainty, invented rationale, or material contradiction.
- [ ] Findings are classified BLOCKER, MAJOR, MINOR, or INFO.
- [ ] BLOCKER/MAJOR findings prevent PASS.
- [ ] Reviewer limitations and uninspected scope are explicit.

## G. Human approval and publication

Check completed steps only; before human review, approval/publication items below are pending rather than prerequisites for the independent reviewer's PASS.

- [ ] Human reviewer inspected exact Wiki Diff and changed pages.
- [ ] Source Manifest and relevant source revisions were inspected.
- [ ] Claim-Evidence mapping and both gate reports were inspected.
- [ ] Human decision is approve / request_changes / reject.
- [ ] Decision record binds reviewer, timestamp, diff/Wiki commit, source snapshot, reports, comments, and waivers.
- [ ] Publication waits for explicit human authorization.
- [ ] Rejected candidates and prior decisions remain in audit history.

## H. Maintenance and captured knowledge

- [ ] Destination instructions locate the Wiki and full workflow package and preserve the same trust/publication boundaries.
- [ ] Index summaries add no unsupported claims; page/change visibility matches the reviewed snapshot.
- [ ] Related knowledge pages are navigable through contextual links, with intentional standalone pages explained.
- [ ] Operation history preserves prior entries and does not claim unobserved outcomes or modify frozen snapshots.
- [ ] Captured query findings have an authorized scope, avoid duplicate pages, and use original evidence rather than treating the prior answer as proof.
- [ ] Query-capture changes retain ordinary candidate/review/publication states even when source commits are unchanged.
