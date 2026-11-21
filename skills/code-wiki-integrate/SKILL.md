---
name: code-wiki-integrate
description: Synthesize reviewed process-level knowledge from multiple repositories into system-level architecture, interfaces, runtime dependencies, data flows, startup sequences, and platform-specific workflows.
---

# code-wiki-integrate


## Mandatory IDE host precondition

Before running this workflow, confirm that the selected IDE AI plugin / host agent has passed the project-wide compatibility gate documented in docs/ide-plugin-requirements.md. The required capabilities are mandatory project requirements, not optional POC experiments.

If there is no recorded PASS for the compatibility gate, or a required capability is unavailable, stop and report the exact gap. Do not bypass the requirement by directly calling a model API or silently skipping the affected workflow.

## Goal

Build the system-level view across independent processes and repositories without inventing relationships that individual repositories do not prove.


## Output language

Follow `docs/language-policy.md`. Unless the user explicitly requests another language, write generated Wiki pages, analysis notes, and deliverables in **Simplified Chinese**. Preserve source identifiers, API names, paths, commands, configuration keys, and source excerpts verbatim. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English.

## Preconditions

- Source manifest exists and pins all relevant repositories.
- Process pages exist for the processes in scope.
- Each process page has source evidence and a review status.
- Platform Profile applicability is known or explicitly marked Unknown.

If these conditions are not met, produce an integration gap report instead of presenting a complete system architecture.

## Procedure

1. Read the system inventory and all relevant Process pages.
2. Resolve each process ID to its implementing repositories and pinned commits.
3. Compare interface providers and consumers. Verify both sides where possible.
4. Classify each relationship precisely: build_depends_on, runtime_depends_on, communicates_with, provides_interface/consumes_interface, or starts_before.
5. Create a relationship only when evidence supports its type and direction. Otherwise record a candidate relationship as unverified or an open question.
6. Build system architecture and process maps.
7. Analyze startup, shutdown, suspend/resume, recovery, and data-flow workflows separately for each applicable Platform Profile.
8. Compare QNX, Android, and Linux-TBOX only where both sides of the comparison have been inspected.
9. Identify contradictions between process pages, configuration, interface definitions, and system-level claims.
10. Update system pages and cross-page references.
11. Run lint and independent review. Keep the result as a proposed change until human approval.

## Output

- System overview and process inventory.
- Evidence-backed architecture and relationship map.
- Interface catalog.
- Profile-specific startup/lifecycle workflows.
- Cross-profile differences and unknowns.
- Integration conflicts and open questions.

## Critical rule

A CMake target edge is a build dependency, not proof that one runtime process calls or communicates with another. Never convert it into a runtime relationship.
