---
name: code-wiki-lint
description: Validate Code LLM Wiki structure, metadata, mappings, links, Claim-Evidence records, Page-Source Map, profile scopes, state consistency, and stale references before semantic review or human approval.
---

# code-wiki-lint

## Goal

Perform a rule-driven structural and provenance audit. This Skill does not require a custom TypeScript/Python runtime. Use available file listing, search, read, and Git operations.

## Normative references

Follow docs/skill-contracts.md, docs/independent-review-execution.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/quality-gate.md, docs/failure-handling.md, and docs/language-policy.md. Use references/lint-report-template.md.

Follow docs/wiki-maintenance.md for maintenance-file validation. Administrative files do not require fabricated Claim/Evidence or Page-Source Map entries.

## Inputs

- Candidate Wiki tree and base revision.
- Source Manifest.
- Claim-Evidence records.
- Page-Source Map.
- Available pinned source repositories or source locator access.
- Change ID and declared review scope.

If a required input is missing, report the affected checks as FAIL or NOT RUN/PARTIAL according to whether the missing input is itself a schema violation or an unavailable capability.

## Checks

### 1. Repository and manifest

- Required manifest exists and schema is valid.
- Every in-scope repository has stable ID and full pinned commit SHA.
- Submodule paths and pins match the inspected superproject state.
- Checkout mismatch/uninitialized/inaccessible states are explicit.
- AGENTS.md inventory and read status are recorded.
- No credentials, tokens, private keys, or sensitive payloads are copied.
- Only approved phase-one profiles are used.

### 2. Mapping integrity

- Repository-to-Process mappings are explicit and many-to-many.
- Process-to-Profile mappings are separate from Repository inventory.
- Mapping status and evidence are present.
- Unsupported or unknown mappings are not represented as confirmed.
- Every referenced repository/process/profile ID resolves.

### 3. Page metadata and schema

- Every substantive page has stable ID, title, type, status, and source manifest/revision metadata.
- Process/profile pages reference valid IDs and correct scope.
- Common pages do not contain unsupported profile assumptions.
- Claim IDs and relationship IDs are unique and resolve.
- Change and approval metadata use canonical status values.

### 4. Claim-Evidence integrity

- Every material claim has a stable ID, atomic statement, scope, profile IDs, and status.
- Every non-unknown material claim has one or more evidence references.
- Evidence has repository ID, full commit SHA, path, locator, type, profile scope, status, and checked timestamp.
- Evidence-to-claim relation is supports/contradicts/qualifies.
- Inferred claims include reasoning and assumptions.
- Unknown claims identify evidence gaps.
- Evidence locators resolve at the pinned revision where the host can verify them.
- Build graph evidence is not used as runtime/IPC/startup evidence.

### 5. Page-Source Map and incremental update

- Every substantive page has a Page-Source Map entry.
- Claim IDs and evidence/source references match the page.
- Repository commits and changed paths are recorded at the inspected revision.
- Dependent pages resolve.
- Stale evidence propagates to affected claims/pages.
- Approval binding matches the candidate diff, Wiki revision, Source Manifest, and relevant source revisions.

### 6. Links and consistency

- Internal Markdown links resolve.
- IDs are unique.
- No broken or orphaned high-value pages.
- Relationship types are explicit and direction is supported.
- Duplicate or contradictory claims are reported.
- Query-visible/published content does not include draft, rejected, stale, or contradicted claims as current facts.

### 7. Platform scope

- Profile IDs are qnx, android, or linux-tbox in v0.1.0.
- Linux-TBOX remains one bound profile.
- QNX/Android deployment context is not guessed.
- Unsupported profiles are not generated.
- Claims are not generalized across uninspected profiles.

### 8. Navigation, operation history, and capture

- The destination-root AGENTS.md contains actual paths, self-contained query rules, a reproducible package locator/provenance, and an explicit query logging policy. Existing human instructions are preserved; unresolved placeholders or contradictory instructions are findings.
- The selected snapshot's index covers every substantive page once with working links, summaries, scope, and accurate page/change state. Candidate/stale/history entries are distinguished from accepted/published knowledge. Missing entries and falsely trusted status fail the check.
- Related pages have meaningful contextual links. Report index-only orphan pages, missing cross-references, and important unrepresented concepts; accept an explicit standalone-page rationale rather than forcing empty pages.
- Existing log content is an unchanged prefix of the new log relative to the base snapshot. New event IDs are unique; outcomes, revisions, and report links reflect observed operations. Corrections append rather than rewrite. No future PASS/publication is pre-recorded.
- Read-only queries have no required log event when query logging is disabled. Deferred gate events outside the frozen snapshot are explicitly reported; do not require editing the candidate to log its own Lint result.
- Query capture has an authorized scope, duplication check, original evidence, candidate status, and ordinary gate bindings. Unchanged source commits do not exempt new claims from review.

## Result semantics

- PASS: all required checks ran and passed.
- FAIL: a required deterministic check found an unresolved violation.
- PARTIAL: one or more checks could not execute or source coverage is incomplete.
- NOT RUN: an individual check was unavailable; this must be explained and blocks the gate when the check is required.

A required NOT RUN check cannot be treated as PASS. A PARTIAL Lint result cannot advance to independent Review or human approval.

## Output

Return the complete references/lint-report-template.md structure: result, checks passed/failed/NOT RUN, exact paths/locators, findings, limitations, and remediation.

Return the observed lint event to the orchestrator. Lint does not append the log or repair the index it is checking.

## Capability honesty

If file listing, Git revision inspection, source locator resolution, link checking, or secret scanning is unavailable, report that check as NOT RUN. Do not claim deterministic validation passed when the required operation was unavailable.

When the required Lint scope returns PASS, hand control to the orchestrator, which MUST automatically delegate the independent Review Subagent as specified in docs/independent-review-execution.md. This Skill does not ask the user to create another session and does not perform same-context semantic self-review.

This Skill is a rule-driven prompt workflow, not a compiled linter. A future optional script may automate repeatable checks, but it is out of scope for v0.1.0.
