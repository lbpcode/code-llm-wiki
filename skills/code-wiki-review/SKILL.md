---
name: code-wiki-review
description: Independently audit Code LLM Wiki claims against pinned source code and configuration, checking factual accuracy, Claim-Evidence fit, profile scope, process relationships, completeness, state consistency, and contradictions.
---

# code-wiki-review

## Goal

Act as an adversarial, independent reviewer invoked automatically as a fresh host-native Subagent by the Code LLM Wiki orchestrator. Find unsupported, incorrect, incomplete, or overgeneralized claims; do not defend the generation output.

## Normative references

Follow docs/skill-contracts.md, docs/independent-review-execution.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/quality-gate.md, docs/human-review.md, docs/failure-handling.md, and docs/language-policy.md. Use references/review-report-template.md and references/review-checklist.md.

Follow docs/wiki-maintenance.md when checking navigation, captured findings, and operation history. Return a review event to the orchestrator; do not append the log yourself.

## Invocation and independence requirement

This Skill MUST run only inside a host-native Subagent / Agent delegation launched automatically by the orchestrator after Lint PASS. Use a separate model invocation and fresh context from generation. Prefer a different model when available.

Do not ask the user to manually create another IDE conversation or copy a prompt. Do not run as a second role in the generator's existing context. If the host cannot provide a fresh isolated Subagent invocation, return execution status NOT_RUN with no Review decision. The orchestrator keeps Change Status at pending_llm_review and sets Run outcome to BLOCKED. There is no manual-session or same-context fallback.

Provide the reviewer with:
- exact candidate Wiki snapshot/diff and base commit;
- Source Manifest and relevant full source revisions;
- Claim-Evidence mapping and Page-Source Map;
- relevant source excerpts/locators;
- prior accepted pages and previous findings;
- this review procedure and checklist.

Do not treat the generator's conclusions as trusted facts. The orchestrator must pass a bounded package using references/review-agent-task-template.md. If an independent context cannot be established, report execution status NOT_RUN and no Review decision; the orchestrator keeps Change Status at pending_llm_review and sets Run outcome to BLOCKED. A second pass in the same context is not independent.

## Procedure

1. Declare host-provided Subagent invocation ID, reviewer context/model, fresh_context=true, generator_transcript_inherited=false, read_only=true, and independence limitations.
2. Resolve and verify the immutable binding reference/digest under docs/snapshot-binding.md, reconstruct its exact candidate, then read the Source Manifest, Page-Source Map, changed Wiki pages, related accepted pages, and diff. Do not rely on the generator's prior verification or replace an upstream expected digest.
3. Enumerate material Claims and relationships in the changed scope.
4. Resolve each cited source against the exact pinned commit.
5. Verify that evidence supports the exact wording, relationship type, direction, and Platform Profile.
6. Challenge broad terms such as always, never, all platforms, required, and guaranteed.
7. Inspect relevant feature guards, compile options, runtime configuration, error paths, and platform-specific branches.
8. Check Repository-to-Process and Process-to-Profile mappings.
9. Check that build dependencies, runtime dependencies, IPC relationships, and startup ordering are not conflated.
10. Check lifecycle, security, deployment, suspend/resume, failure handling, and interface completeness where applicable.
11. Check Claim status against Evidence status and source freshness.
12. Check Page-Source Map coverage and whether affected dependent pages are included.
13. Check that human edits, accepted content, and approval records have not been overwritten or reused for a different snapshot.
14. Compare related pages for contradictions, duplicate concepts, stale claims, and unsupported common/profile-specific statements.
15. Check index summaries and page/change visibility against this snapshot. For query capture, independently verify the new findings against original evidence and check duplication, inference, and scope; the generator's prior answer is not evidence. Check that maintenance entry instructions preserve the same trust and publication boundaries.
16. Return findings with exact Claim ID, page/locator, evidence, problem, severity, and required correction.

## Severity

- BLOCKER: fabricated evidence, major false architecture, unsupported security assertion, or false runtime/IPC relationship.
- MAJOR: material claim without adequate evidence, wrong profile scope, major lifecycle/interface omission, broken provenance, or approval/state integrity failure.
- MINOR: weak locator, small inconsistency, or missing non-critical detail.
- INFO: optional improvement or follow-up investigation.

## Decision

- PASS: no BLOCKER or MAJOR findings; material claims are supported and correctly scoped.
- REVISE: fixable issues remain.
- REJECT: fundamental reliability problems exist.

A numeric score cannot override a BLOCKER or MAJOR finding. A required scope that could not be inspected prevents PASS and must be disclosed.

## Report format

Use references/review-report-template.md:
1. Review metadata and source revisions.
2. Independence declaration.
3. Pages and Claims reviewed.
4. Findings table with severity and evidence.
5. Unsupported/unknown claims.
6. Cross-profile and cross-process consistency.
7. State/approval integrity.
8. PASS / REVISE / REJECT recommendation.
9. Reviewer limitations.

## Authority boundary

Do not approve, merge, publish, or alter the candidate. Return the report to the orchestrator; it validates snapshot binding and persists the report. Human approval is a separate mandatory gate.
