---
name: code-wiki-update
description: Incrementally update Code LLM Wiki pages after source repository or submodule revisions change, preserving provenance, human edits, and approval validity.
---

# code-wiki-update

## Goal

Refresh only the knowledge affected by source changes while keeping every accepted Claim tied to the exact revision that supports it.

## Normative references

Follow docs/skill-contracts.md, docs/independent-review-execution.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/human-review.md, docs/failure-handling.md, and docs/language-policy.md. Use references/page-source-map-template.md and references/update-report-template.md.

## Preconditions

- Previous Source Manifest and Page-Source Map exist.
- Current superproject and relevant repository revisions can be inspected.
- Accepted Wiki base and human-edited working state are available.
- No unresolved user changes will be overwritten.

If the previous mapping is missing or incomplete, report impact analysis as PARTIAL and broaden the review scope.

## Procedure

1. Read the previous Source Manifest, Page-Source Map, accepted Wiki revision, and pending user edits.
2. Inspect current superproject commit and every relevant submodule pin.
3. Compare old/new full commit SHAs. Do not rely on branch names alone.
4. Identify changed repositories and paths from Git history/diff where available.
5. Map changed paths to Evidence IDs, Claims, Process/Profile pages, Interface, Workflow, and System pages.
6. Mark evidence and claims sourced from changed locations stale until revalidated.
7. Re-read changed source and relevant surrounding context; inspect both sides of changed interfaces when possible.
8. Revalidate downstream cross-process relationships and workflows if endpoints, contracts, startup configuration, or platform behavior changed.
9. Compare candidate output with current Wiki and last accepted base. Preserve human changes.
10. If AI and human edits overlap semantically, stop and report a conflict; do not overwrite either side.
11. Update only affected pages. Do not regenerate unrelated pages.
12. Update Source Manifest and Page-Source Map only for source revisions and pages actually inspected.
13. Assess whether prior approvals are invalidated. Any relevant source, diff, manifest mapping, or scope change makes the approval stale.
14. Run Lint on changed pages and their dependencies. If Lint PASS, the orchestrator MUST automatically delegate a fresh host-native Review Subagent using references/review-agent-task-template.md and skills/code-wiki-review/SKILL.md. Wait for a completed, snapshot-bound report. Do not ask the user to open a second conversation. If Subagent delegation/isolation is unavailable, set Review execution status to NOT_RUN, leave Review decision null, keep Change Status at pending_llm_review, and set Run outcome to BLOCKED.
15. Present old/new revisions, impact report, diff, findings, and open questions for a new human decision.

## Required outputs

- Old/new source revision summary.
- Changed repository/path inventory.
- Affected Evidence, Claims, pages, and dependent pages.
- Stale claims not yet revalidated.
- Human-edit conflict report, if any.
- Approval invalidation assessment.
- Lint and independent Review results; if delegation is blocked, record Review execution status, null Review decision, unchanged Change Status, and Run outcome BLOCKED.
- Proposed Git diff and update report.

## Failure behavior

Follow docs/failure-handling.md. If source commits cannot be established, do not update accepted claims. If impact cannot be bounded, report PARTIAL and broaden review conservatively. If human edits conflict, pause the affected page for human resolution.

## Safety

Do not silently overwrite human-edited Wiki content. Preserve prior history. Do not mark a claim verified merely because its source commit changed; reopen the evidence and validate it. Do not publish or merge without explicit human authorization.
