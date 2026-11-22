---
name: code-wiki-review
description: Independently audit Code LLM Wiki claims against pinned source code and configuration, checking factual accuracy, Claim-Evidence fit, profile scope, process relationships, completeness, state consistency, and contradictions.
---

# code-wiki-review

## Goal

Act as an adversarial, independent reviewer. Find unsupported, incorrect, incomplete, or overgeneralized claims; do not defend the generation output.

## Normative references

Follow docs/skill-contracts.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/quality-gate.md, docs/human-review.md, docs/failure-handling.md, and docs/language-policy.md. Use references/review-report-template.md and references/review-checklist.md.

## Independence requirement

Use a separate model invocation and fresh context from the generation step. Prefer a different model when available.

Provide the reviewer with:
- exact candidate Wiki snapshot/diff and base commit;
- Source Manifest and relevant full source revisions;
- Claim-Evidence mapping and Page-Source Map;
- relevant source excerpts/locators;
- prior accepted pages and previous findings;
- this review procedure and checklist.

Do not treat the generator's conclusions as trusted facts. If an independent context cannot be established, report NOT RUN and block the quality gate. A second pass in the same context is not independent.

## Procedure

1. Declare reviewer context/model and independence limitations.
2. Read the Source Manifest, Page-Source Map, changed Wiki pages, related accepted pages, and candidate diff.
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
15. Return findings with exact Claim ID, page/locator, evidence, problem, severity, and required correction.

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

Do not approve, merge, publish, or alter the candidate. Human approval is a separate mandatory gate.
