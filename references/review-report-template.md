# Independent LLM Review Report

## Review metadata

- Review ID:
- Execution status: NOT_RUN / RUNNING / COMPLETED / INVALID
- Run outcome: PASS / PARTIAL / BLOCKED / FAIL
- Change Status:
- Timestamp:
- Candidate change ID:
- Candidate Wiki commit / diff digest:
- Base Wiki commit:
- Source Manifest version/digest:
- Relevant source revisions:
- Reviewer Subagent invocation/run ID:
- Reviewer Skill revision:
- Reviewer model identifier (when available):
- Host-native delegation capability:
- Fresh context: true / false:
- Generator transcript inherited: true / false:
- Read-only: true / false:
- Review decision: PASS / REVISE / REJECT / null

## Independence declaration

Record whether the reviewer was launched by a host-native Subagent delegation in a fresh context, without inheriting the generator transcript, and with read-only access. If any mandatory condition is false or unverified, result is NOT RUN and no PASS is issued.

## Review scope

- Pages reviewed:
- Claims reviewed:
- Relationships/interfaces reviewed:
- Profiles reviewed:
- Excluded or inaccessible scope:

## Findings

| Finding ID | Severity | Page / Claim | Exact statement | Evidence inspected | Problem | Required correction |
|---|---|---|---|---|---|---|

Severity: BLOCKER / MAJOR / MINOR / INFO.

## Coverage assessment

- Factual correctness:
- Evidence traceability:
- Profile scope:
- Process boundaries:
- Interface and relationship correctness:
- Lifecycle / error-path completeness:
- Cross-page consistency:
- Unknowns and limitations:

## Unsupported / unknown claims

List each claim that cannot be verified, with the source inspection needed to resolve it.

## Review decision

Set a decision only when execution status is `COMPLETED` and the orchestrator has validated isolation and exact snapshot binding:

- `PASS`: no BLOCKER or MAJOR findings.
- `REVISE`: fixable issues remain.
- `REJECT`: fundamental reliability problems exist.

For `NOT_RUN` or `INVALID`, leave the review decision null. If review is blocked after Lint PASS, keep Change Status at `pending_llm_review` and set Run outcome to `BLOCKED`. `BLOCKED` is a run outcome, not a review decision.

## Reviewer limitations

State unavailable repositories, source paths, tools, profile coverage, or context limitations. This report is advisory and does not constitute human approval.
