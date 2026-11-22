# Automatic Independent Review Execution

## 1. Policy

v0.1.0 supports exactly one independent-review execution mode:

**Automatic delegation to a host-native Subagent / independent Agent invocation.**

The workflow MUST NOT ask the user to manually open a second IDE conversation, copy a prompt, or transfer a review package. Manual-session execution is not a supported fallback.

A Skill or Prompt cannot create a new model context by itself. The IDE/Agent host must expose a native delegation capability that can start a separate model invocation with a fresh context and return its result to the orchestrator. This is a host capability requirement, not a custom runtime requirement of Code LLM Wiki.

If the host does not provide this capability, or the invocation cannot prove context isolation, independent Review is `NOT RUN` and the Change Set is `BLOCKED`. Do not claim PASS, proceed to human approval, or silently fall back to same-context self-review.

## 2. Roles

- **Orchestrator / Generation Agent**: generates the candidate, runs Lint, packages the exact review scope, delegates the reviewer, handles findings, and controls the Change Set state.
- **Independent Review Subagent**: receives a fresh context, independently checks the candidate against pinned source evidence, and returns a read-only review report.
- **Human reviewer**: reviews the final candidate and reports after all required automated gates pass.

The reviewer is a separate invocation, not merely a different role prompt in the generator's existing conversation. A different model is preferred when the host supports model selection, but a different model is not mandatory; fresh isolated context is mandatory.

## 3. Required host capability

The host must provide all of the following:

1. A native Subagent / Agent delegation operation.
2. A new model invocation with a fresh context.
3. No inherited generator conversation transcript, hidden reasoning, or unshared intermediate conclusions.
4. Ability to pass a bounded task instruction and explicit input references to the reviewer.
5. Ability for the reviewer to read the exact candidate snapshot and pinned source repositories.
6. Ability to return the review result to the orchestrator.
7. Read-only access for the reviewer to source and candidate Wiki content.

The host may expose these capabilities under any native name. This specification does not mandate a particular IDE, plugin, API, or tool name.

## 4. Automatic invocation sequence

After a candidate-producing workflow (Ingest, Integrate, or Update):

1. The orchestrator runs the required Lint scope.
2. If Lint is FAIL, fix findings before proceeding. If Lint is PARTIAL or a required check is NOT RUN, block the Change Set.
3. If Lint is PASS, the orchestrator creates an immutable Review Package for the exact candidate snapshot.
4. The orchestrator automatically delegates a new Subagent invocation using the task contract in `references/review-agent-task-template.md` and the `code-wiki-review` Skill.
5. The orchestrator waits for the Subagent to finish. It must not treat an invocation request/accepted state as a completed review.
6. The reviewer returns a structured report. The orchestrator validates its Change ID, candidate Wiki commit/diff digest, Source Manifest digest, source revisions, reviewer invocation identity, and decision.
7. The orchestrator persists the report under `wiki/_meta/changes/<change-id>/independent-review.md` and binds its ID/digest to the Change Set.
8. Only a valid PASS proceeds to Human Review.
9. REVISE returns the Change Set to draft. The Generation Agent addresses findings, reruns Lint, and delegates a **new** independent Subagent invocation against the new exact snapshot.
10. REJECT terminates the Change Set. Preserve the report and audit history.

No reviewer may edit the candidate. All corrections are applied by the Generation Agent as a new candidate snapshot.

## 5. Review Package

The orchestrator passes only the material needed for independent verification:

- Change ID and bounded review scope.
- Base Wiki commit and exact candidate Wiki commit, or exact diff digest.
- Candidate diff and changed page paths/IDs.
- Source Manifest content and digest.
- Relevant source repository IDs and full pinned commit SHAs.
- Claim-Evidence records for changed material claims.
- Page-Source Map entries and dependent pages in scope.
- Relevant source files/locators or read access to the exact pinned revisions.
- Related accepted pages needed to check consistency.
- Previous review findings and their disposition, if this is a re-review.
- The review Skill and review checklist.

Do not pass the generator's private reasoning or ask the reviewer to trust its conclusions. The reviewer must independently inspect the evidence. Redact secrets and unnecessary sensitive content.

## 6. Isolation and report validation

The reviewer report MUST record:
- `review_id` and `change_id`;
- host-provided reviewer invocation / Subagent run identifier;
- reviewer Skill revision;
- model identifier when available;
- `fresh_context: true`;
- `generator_transcript_inherited: false`;
- `read_only: true`;
- base/candidate Wiki revision or diff digest;
- Source Manifest version/digest;
- relevant source repository IDs and full commit SHAs;
- pages and Claims reviewed;
- findings, severity, evidence, and PASS / REVISE / REJECT decision;
- limitations and checks not completed.

Do not include hidden chain-of-thought. Provide concise findings and verifiable evidence only.

The orchestrator MUST reject a report as invalid / NOT RUN if:
- the host cannot establish a fresh independent invocation;
- the report is missing or identifies the wrong candidate/source snapshot;
- the reviewer modified the candidate or source;
- the report omits mandatory scope without declaring a limitation;
- the invocation failed, timed out, or returned no completed result.

## 7. Retry and state rules

- Each materially changed candidate requires a new reviewer invocation.
- Never reuse a PASS report for a changed candidate, changed source snapshot, or changed review scope.
- A reviewer REVISE result returns the Change Set to draft; Lint and independent Review both run again after correction.
- A reviewer REJECT result is terminal for that Change Set; a new attempt receives a new Change ID.
- If the host cannot launch the Subagent, returns an error, or cannot prove isolation, record `NOT RUN` and keep the Change Set blocked.
- There is no manual new-session fallback and no same-context fallback.

## 8. Boundary

This document defines the host-independent delegation contract. The Skill package does not implement an IDE's Subagent API, create a model runtime, call a model API directly, or install a custom orchestration service. The host's native Agent delegation capability performs the actual isolated invocation.
