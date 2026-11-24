# Lint Report

## Metadata

- Report ID:
- Timestamp:
- Candidate change ID:
- Snapshot binding reference (registry ID / binding ID / record path):
- Expected binding record SHA-256:
- Binding verification result and reconstructed tree:
- Wiki base/candidate commit:
- Source Manifest version/digest:
- Scope:
- Overall result: PASS / FAIL / PARTIAL

## Check results

| Check ID | Check | Result | Scope | Evidence / exact location | Finding |
|---|---|---|---|---|---|
| LINT-001 | Required files and schema | PASS / FAIL / NOT RUN | | | |
| LINT-002 | Stable IDs and metadata | PASS / FAIL / NOT RUN | | | |
| LINT-003 | Manifest and pinned commits | PASS / FAIL / NOT RUN | | | |
| LINT-004 | Claim-Evidence mapping | PASS / FAIL / NOT RUN | | | |
| LINT-005 | Locator resolution | PASS / FAIL / NOT RUN | | | |
| LINT-006 | Page-source map consistency | PASS / FAIL / NOT RUN | | | |
| LINT-007 | Internal links and references | PASS / FAIL / NOT RUN | | | |
| LINT-008 | Profile and relationship scope | PASS / FAIL / NOT RUN | | | |
| LINT-009 | Stale / conflicting claims | PASS / FAIL / NOT RUN | | | |
| LINT-010 | Secret / sensitive-data scan | PASS / FAIL / NOT RUN | | | |
| LINT-011 | Wiki-local entry paths, policy, and package provenance | PASS / FAIL / NOT RUN | | | |
| LINT-012 | Index coverage, summaries, page/change visibility, cross-links | PASS / FAIL / NOT RUN | | | |
| LINT-013 | Append-only log, unique events, observed outcomes, snapshot isolation | PASS / FAIL / NOT RUN | | | |
| LINT-014 | Query-capture scope, deduplication, original evidence, and candidate gates | PASS / FAIL / NOT RUN | | | |

For LINT-014, PASS may mean verified not applicable when this is not a query-capture change; record that scope decision. Do not invent a capture record. For LINT-013, absence of a disabled query log or a disclosed deferred post-freeze event is not a missing required event. Lint returns its own event to the orchestrator without changing this snapshot.

## Findings

| ID | Severity | File / locator | Problem | Required correction |
|---|---|---|---|---|

## Checks not executable

For every NOT RUN check, state why it could not run and whether it blocks progression.

## Recommendation

- PASS: all required checks ran and passed.
- FAIL: a required deterministic check found an unresolved violation.
- PARTIAL: one or more checks could not execute or coverage is incomplete.

For a frozen candidate, verify and record the binding under docs/snapshot-binding.md. Missing or mismatched binding data blocks the gate. Lint is not semantic approval. A Lint PASS permits independent LLM Review only when Review is within the requested scope.
