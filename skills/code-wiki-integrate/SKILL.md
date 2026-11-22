---
name: code-wiki-integrate
description: Synthesize reviewed process-level knowledge from multiple repositories into system-level architecture, interfaces, runtime dependencies, data flows, startup sequences, and platform-specific workflows.
---

# code-wiki-integrate

## Goal

Build the system-level view across independent processes and repositories without inventing relationships that individual repositories do not prove.

## Normative references

Follow docs/skill-contracts.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/failure-handling.md, and docs/language-policy.md. Use references/system-template.md, references/interface-template.md, references/workflow-template.md, and references/integration-report-template.md.

## Preconditions

- Source Manifest pins the relevant repositories.
- Repository-to-Process and Process-to-Profile mappings have explicit status.
- Process pages exist for the in-scope processes.
- Each input page has a content/review status and Claim-Evidence mapping.
- Required source revisions and relevant interface evidence are accessible.

If prerequisites are missing, produce an integration gap report rather than presenting a complete System architecture.

Candidate Process pages may be used to draft candidate System pages only if their unapproved status is preserved and every derived claim remains traceable. Published/reviewed Process pages are preferred inputs.

## Procedure

1. Read the System inventory, Source Manifest, Page-Source Map, and all relevant Process pages.
2. Resolve each Process ID to its implementing repositories and pinned commits.
3. Verify Repository-to-Process and Process-to-Profile mappings; do not infer profile support from repository inventory.
4. Compare interface providers and consumers. Verify both sides where possible.
5. Classify each relationship precisely: build_depends_on, runtime_depends_on, communicates_with, provides_interface/consumes_interface, starts_before, or runs_on.
6. Create a relationship only when evidence supports its type, direction, endpoints, and profile scope. Otherwise record it as candidate/unknown.
7. Build System architecture and process maps with Claim-Evidence references.
8. Analyze startup, shutdown, suspend/resume, recovery, and data-flow workflows separately for each applicable Platform Profile.
9. Compare QNX, Android, and Linux-TBOX only where both sides of the comparison have been inspected.
10. Identify contradictions between Process pages, source configuration, interface definitions, and System-level claims.
11. Update System pages, relationship records, Interface/Workflow pages, and Page-Source Map dependencies.
12. Run Lint and independent Review. Keep results as a proposed diff until human approval.

## Outputs

- System overview and Process inventory.
- Evidence-backed architecture and relationship map.
- Interface catalog with provider/consumer evidence.
- Profile-specific startup/lifecycle workflows.
- Cross-profile differences and explicit unknowns.
- Integration conflicts and open questions.
- Integration report and proposed diff.

## Failure behavior

Follow docs/failure-handling.md. Missing Process pages, inaccessible repositories, one-sided interfaces, unresolved mappings, or contradictory evidence must appear in the report. Continue only independent scopes; return PARTIAL/BLOCKED when coverage is incomplete. Never infer a complete System architecture from partial inputs.

## Critical rule

A CMake target edge is a build dependency, not proof that one runtime process calls or communicates with another. Never convert it into a runtime relationship.
