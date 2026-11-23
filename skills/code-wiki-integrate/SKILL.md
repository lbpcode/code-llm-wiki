---
name: code-wiki-integrate
description: Synthesize reviewed process-level knowledge from multiple repositories into system-level architecture, interfaces, runtime dependencies, data flows, startup sequences, and platform-specific workflows.
---

# code-wiki-integrate

## Goal

Build the system-level view across independent processes and repositories without inventing relationships that individual repositories do not prove.

## Normative references

Follow docs/skill-contracts.md, docs/independent-review-execution.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/failure-handling.md, and docs/language-policy.md. Use references/system-template.md, references/interface-template.md, references/workflow-template.md, and references/integration-report-template.md.

## Preconditions

- Source Manifest pins the relevant repositories.
- Ingestion Plans and Task Reports are available for the selected Process scope, or their absence is explicitly reported as a coverage gap. Legacy Process pages without task artifacts may still be used as candidate inputs, but their ingestion coverage MUST remain unverified/partial.
- Repository-to-Process and Process-to-Profile mappings have explicit status.
- Process pages exist for the in-scope processes.
- Each input page has a content/review status and Claim-Evidence mapping.
- Required source revisions and relevant interface evidence are accessible.

If prerequisites are missing, produce an integration gap report rather than presenting a complete System architecture. Missing, partial, or blocked Analysis Tasks must remain visible; do not infer complete Process coverage from a Process page alone.

Candidate Process pages may be used to draft candidate System pages only if their unapproved status is preserved and every derived claim remains traceable. Published/reviewed Process pages are preferred inputs.

## Procedure

1. Read the System inventory, Source Manifest, Page-Source Map, relevant Process pages, and the Ingestion Plans/Task Reports for the selected scope.
2. Resolve each Process ID to its implementing repositories and pinned commits; confirm that Task Reports refer to the same revisions.
3. Verify Repository-to-Process and Process-to-Profile mappings; do not infer profile support from repository inventory.
4. Build the initial integration view from Process pages, atomic Claims, Evidence records, and completed Task Reports. Preserve candidate, partial, stale, and unknown states.
5. Do not reread entire repositories or repeat completed Ingest analysis. Reopen only the exact source ranges needed to validate evidence, resolve contradictions, inspect both sides of an interface, or answer a specific cross-process question.
6. If a missing relationship requires substantial new source analysis, define a focused follow-up Analysis Task under the current Change Set, execute it with the context-bounded Ingest rules, and checkpoint the result.
7. Compare interface providers and consumers. Verify both sides where possible.
8. Classify each relationship precisely: build_depends_on, runtime_depends_on, communicates_with, provides_interface/consumes_interface, starts_before, or runs_on.
9. Create a relationship only when evidence supports its type, direction, endpoints, and profile scope. Otherwise record it as candidate/unknown.
10. Build System architecture and process maps with Claim-Evidence references.
11. Analyze startup, shutdown, suspend/resume, recovery, and data-flow workflows separately for each applicable Platform Profile.
12. Compare QNX, Android, and Linux-TBOX only where both sides of the comparison have been inspected.
13. Identify contradictions between Process pages, Task Reports, source configuration, interface definitions, and System-level claims.
14. Update System pages, relationship records, Interface/Workflow pages, and Page-Source Map dependencies.
15. Run Lint. If Lint PASS, the orchestrator MUST automatically delegate a fresh host-native Review Subagent using references/review-agent-task-template.md and skills/code-wiki-review/SKILL.md. Wait for a completed, snapshot-bound report. Do not ask the user to open a second conversation. If Subagent delegation/isolation is unavailable, set Review execution status to NOT_RUN, leave Review decision null, keep Change Status at pending_llm_review, and set Run outcome to BLOCKED. Keep results as a proposed diff until human approval.

## Outputs

- System overview and Process inventory.
- Evidence-backed architecture and relationship map.
- Interface catalog with provider/consumer evidence.
- Profile-specific startup/lifecycle workflows.
- Cross-profile differences and explicit unknowns.
- Integration conflicts and open questions.
- Integration report and proposed diff.
- Lint report and independent Review report; if delegation is blocked, record Review execution status, null Review decision, unchanged Change Status, and Run outcome BLOCKED.

## Failure behavior

Follow docs/failure-handling.md. Missing Process pages, inaccessible repositories, one-sided interfaces, unresolved mappings, or contradictory evidence must appear in the report. Continue only independent scopes; return PARTIAL/BLOCKED when coverage is incomplete. Never infer a complete System architecture from partial inputs.

## Critical rule

A CMake target edge is a build dependency, not proof that one runtime process calls or communicates with another. Never convert it into a runtime relationship.
