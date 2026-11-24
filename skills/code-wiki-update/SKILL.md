---
name: code-wiki-update
description: Update Code LLM Wiki after source changes or explicitly requested query writeback, preserving evidence, human edits, navigation, and approval validity.
---

# code-wiki-update

## Goal

Refresh affected knowledge or retain a requested query finding as a candidate change, keeping every accepted Claim tied to the exact revision that supports it.

## Normative references

Follow docs/skill-contracts.md, docs/independent-review-execution.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/human-review.md, docs/failure-handling.md, and docs/language-policy.md. Use references/page-source-map-template.md and references/update-report-template.md.

Follow docs/wiki-maintenance.md for navigation, logging, and query capture. Use references/query-capture-template.md for requested answer writeback.

## Modes

- **Source update:** compare old/new source revisions and revalidate affected knowledge.
- **Query capture:** the user requests saving an answer or new finding. Source revisions may be unchanged; inspect the finding and create a reviewed knowledge diff. A normal question does not authorize capture.

Both modes use a candidate branch/worktree and the shared finish below. If the Wiki has no prior initialized manifest/base, route to Init before attempting capture; do not invent a baseline.

Respect an explicit candidate-only or no-Review request under docs/skill-contracts.md. Prepare the requested diff and record later gates as not run; candidate delivery is not publication readiness. Snapshot binding, including uncommitted candidates, follows docs/human-review.md section 4.

## Preconditions

- Previous Source Manifest and Page-Source Map exist.
- Current superproject and relevant repository revisions can be inspected.
- Accepted Wiki base and human-edited working state are available.
- No unresolved user changes will be overwritten.

If the previous mapping is missing or incomplete, report impact analysis as PARTIAL and broaden the review scope.

## Source-update procedure

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
14. Continue through the shared finish.

## Query-capture procedure

1. Confirm the authorized finding/scope from the user's request; read the destination entry point, accepted index/pages, manifest/map, exact source revisions, and human edits.
2. Locate the best existing page to extend. Create a new page only when its scope is distinct, using an existing entity type. Report a no-op if the requested knowledge is already represented accurately.
3. Create a new draft Change Set with origin query_capture and a query-capture.md record using references/query-capture-template.md. Record the question as a bounded summary; do not persist the full chat.
4. Reuse existing Claim IDs and original Evidence where they support the same fact. Inspect evidence for new conclusions; create new atomic Claims with justified verified/inferred/unknown status. Neither a prior answer nor a Wiki summary substitutes for original source evidence. Use bounded Ingest for authorized missing source inspection.
5. Prepare candidate page/Claim/Evidence changes and update Page-Source Map dependencies. Preserve human edits and accepted knowledge. Record unchanged source revisions honestly; assess approval invalidation from the new knowledge diff even without a source diff.
6. Continue through the shared finish. Capture has no shortcut to accepted/published knowledge.

## Shared finish

1. Synchronize contextual page links and wiki/index.md in the candidate diff. Include actual content/change state and keep unpublished findings out of accepted navigation. Record changed administrative paths as well as knowledge pages.
2. Persist the update report and an observed update or capture event. Freeze the candidate snapshot; Lint/Review and later publication events are returned to the orchestrator and persisted outside that frozen snapshot under docs/wiki-maintenance.md.
3. Run Lint on changed pages and their dependencies. If Lint PASS, the orchestrator MUST automatically delegate a fresh host-native Review Subagent using references/review-agent-task-template.md and skills/code-wiki-review/SKILL.md. Wait for a completed, snapshot-bound report. Do not ask the user to open a second conversation. If Subagent delegation/isolation is unavailable, set Review execution status to NOT_RUN, leave Review decision null, keep Change Status at pending_llm_review, and set Run outcome to BLOCKED.
4. Present the source revision summary, impact/capture report, actual diff, findings, and open questions for a human decision. Retain existing approval/publication boundaries.

## Required outputs

- Old/new source revision summary.
- Changed repository/path inventory.
- Affected Evidence, Claims, pages, and dependent pages.
- Stale claims not yet revalidated.
- Human-edit conflict report, if any.
- Approval invalidation assessment.
- Lint and independent Review results; if delegation is blocked, record Review execution status, null Review decision, unchanged Change Status, and Run outcome BLOCKED.
- Proposed Git diff and update report.
- Update origin (source_update or query_capture), capture record when applicable, synchronized index/cross-links, and operation event persistence status.

## Failure behavior

Follow docs/failure-handling.md. If source commits cannot be established, do not update accepted claims. If impact cannot be bounded, report PARTIAL and broaden review conservatively. If human edits conflict, pause the affected page for human resolution.

## Safety

Do not silently overwrite human-edited Wiki content. Preserve prior history. Do not mark a claim verified merely because its source commit changed; reopen the evidence and validate it. Do not publish or merge without explicit human authorization.
