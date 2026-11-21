---
name: code-wiki-update
description: Incrementally update Code LLM Wiki pages after source repository or submodule revisions change, preserving provenance and triggering re-review of affected claims.
---

# code-wiki-update


## Mandatory IDE host precondition

Before running this workflow, confirm that the selected IDE AI plugin / host agent has passed the project-wide compatibility gate documented in docs/ide-plugin-requirements.md. The required capabilities are mandatory project requirements, not optional POC experiments.

If there is no recorded PASS for the compatibility gate, or a required capability is unavailable, stop and report the exact gap. Do not bypass the requirement by directly calling a model API or silently skipping the affected workflow.

## Goal

Refresh only the knowledge affected by source changes while keeping every accepted claim tied to the exact revision that supports it.


## Output language

Follow `docs/language-policy.md`. Unless the user explicitly requests another language, write generated Wiki pages, query answers, review findings, and deliverables in **Simplified Chinese**. Preserve source identifiers, API names, paths, commands, configuration keys, and source excerpts verbatim. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English.

## Procedure

1. Read the previous source manifest and page-source map.
2. Inspect the current superproject commit and every relevant submodule pin.
3. Compare old and new full commit SHAs. Do not rely on branch names alone.
4. Identify changed repositories and changed paths from Git history/diff where available.
5. Map changed paths to affected Process, Interface, Workflow, Platform Profile, and System pages.
6. Mark claims sourced from changed locations stale until revalidated.
7. Re-read changed source and relevant surrounding context; inspect both sides of changed interfaces when possible.
8. Revalidate downstream cross-process relationships and workflows if an endpoint, contract, startup configuration, or platform behavior changed.
9. Update only affected pages. Do not regenerate unrelated pages.
10. Update source manifest and page-source map to the inspected revisions.
11. Run lint and independent review on changed pages and their dependencies.
12. Present a diff and review report for human approval.

## Required output

- Old/new source revision summary.
- Changed repository/path inventory.
- Affected pages and reason for impact.
- Updated claims and evidence.
- Stale claims not yet revalidated.
- Lint and independent review results.
- Proposed Git diff.

## Safety

Do not silently overwrite human-edited Wiki content. Preserve prior history. Do not mark a claim verified merely because its source commit has changed; re-open the evidence and validate it.
