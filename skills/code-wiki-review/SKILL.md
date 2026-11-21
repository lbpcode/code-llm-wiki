---
name: code-wiki-review
description: Independently audit Code LLM Wiki claims against pinned source code and configuration, checking factual accuracy, evidence, profile scope, process relationships, completeness, and contradictions.
---

# code-wiki-review

## Role

Act as an adversarial, independent reviewer. Your job is to find unsupported or incorrect claims, not to defend the generation output.


## Output language

Follow `docs/language-policy.md`. Unless the user explicitly requests another language, write generated Wiki pages, query answers, review findings, and deliverables in **Simplified Chinese**. Preserve source identifiers, API names, paths, commands, configuration keys, and source excerpts verbatim. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English.

## Independence requirement

Use a separate model invocation and fresh context from the generation step. Prefer a different model. If only one model endpoint exists, use a new session and provide the source excerpts, exact revisions, Wiki pages, and this review procedure. Do not treat a generator self-review as independent.

## Procedure

1. Read the source manifest, page-source map, changed Wiki pages, and related accepted pages.
2. Enumerate material claims and relationships.
3. Resolve each cited source against the exact pinned commit.
4. Verify that the evidence supports the exact wording and profile scope.
5. Challenge claims that use broad terms such as always, never, all platforms, required, or guaranteed.
6. Inspect relevant feature guards, compile options, runtime configuration, error paths, and platform-specific branches.
7. Check repository-to-process mapping and process boundaries.
8. Check that build dependencies, runtime dependencies, IPC relationships, and startup ordering are not conflated.
9. Check QNX, Android, and Linux-TBOX scope independently.
10. Check lifecycle, security, deployment, suspend/resume, and interface completeness where applicable.
11. Compare related pages for contradictions, duplicate concepts, and stale claims.
12. Return findings with exact claim, evidence, problem, severity, and required correction.

## Severity

- BLOCKER: fabricated evidence, major false architecture, unsupported security assertion, or false runtime/IPC relationship.
- MAJOR: material claim without adequate evidence, wrong profile scope, major omission, or build/runtime confusion.
- MINOR: weak locator, small inconsistency, or missing non-critical detail.
- INFO: optional improvement.

## Decision

- PASS: no BLOCKER or MAJOR findings; material claims are supported and correctly scoped.
- REVISE: fixable issues remain.
- REJECT: fundamental reliability problems exist.

A numeric score cannot override a BLOCKER or MAJOR finding.

## Report format

1. Review metadata and source revisions.
2. Independence declaration.
3. Pages and claims reviewed.
4. Findings table with severity and evidence.
5. Unsupported or unknown claims.
6. Cross-profile and cross-process consistency.
7. PASS / REVISE / REJECT recommendation.
8. Reviewer limitations.

Do not approve or merge the Wiki. Human approval is a separate mandatory gate.
