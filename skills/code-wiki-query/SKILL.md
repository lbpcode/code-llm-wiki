---
name: code-wiki-query
description: Answer engineering questions from the accepted Code LLM Wiki with source citations and uncertainty; route explicitly requested answer writeback to a reviewed candidate update.
---

# code-wiki-query

## Goal

Answer engineering questions from accepted Wiki knowledge without silently turning incomplete, stale, or unreviewed content into certainty.

## Normative references

Follow docs/skill-contracts.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, and docs/language-policy.md.

Follow docs/wiki-maintenance.md for index-first navigation, optional query logging, and requested knowledge capture.

## Default trust policy

- Query pages with `content_status: accepted` whose owning Change Set is `published` by default.
- Exclude draft, pending, rejected, superseded, stale, and contradicted claims from unqualified factual answers.
- Do not treat a verified Claim as proof that its page/change is approved; check page/change publication status separately.
- If the user explicitly asks to inspect candidate or historical content, label its state and revision clearly.
- Distinguish verified facts, inferences, unknowns, and conflicts.
- For a new publication with publication_record_ref, verify its completed receipt, binding, and observed finalization commit under docs/publication-recovery.md before exposing that change's new knowledge. Accepted/published labels alone cannot bypass an incomplete or corrupt receipt. Legacy changes without this mechanism retain their prior checks.

## Procedure

1. Read the destination Wiki's AGENTS.md and wiki/index.md at the selected accepted snapshot. Use the index to locate relevant knowledge, then classify the question as system-level, process-level, interface, workflow, security, deployment, or platform comparison. If the index is missing or incomplete, use scoped page discovery and disclose the navigation gap without editing it.
2. Identify relevant Process IDs and Platform Profile(s).
3. Read the relevant published Wiki pages, Claim-Evidence records, and source references.
4. Check page/change publication status, Claim status, Evidence status, and source revision freshness.
5. Answer with applicable scope and distinguish facts from inference.
6. Cite repository, full commit, path, and line/symbol/configuration locator for material claims.
7. If evidence is insufficient, say exactly what is unknown and identify the source or profile that must be inspected.
8. If sources conflict, disclose the conflict; do not choose a side without a documented resolution.
9. Keep ordinary queries read-only, including the log. Append a redacted query event only when an explicit request or existing local query_logging policy authorizes log-only writes; a strict read-only request overrides that policy. Do not update pages, index, Claims, or publication state as a logging side effect.
10. If the user requests saving useful findings, use the query-capture mode in skills/code-wiki-update/SKILL.md and references/query-capture-template.md. Preserve the request's scope and existing authorization. Capture is a separate candidate write with ordinary quality gates, not immediate acceptance of this answer. Without a save request, suggest a concrete knowledge gap only when useful and create no capture file.

## Cross-platform questions

Compare QNX, Android, and Linux-TBOX only for profiles represented in the Source Manifest and backed by reviewed/published pages. Never assume an uninspected profile behaves like another profile.

## Output format

- Direct answer.
- Relevant Process/Profile scope.
- Verified evidence and source locators.
- Inferences and assumptions.
- Constraints, exceptions, conflicts, and unknowns.
- Optional follow-up investigation.
- Query log event reference only if persisted, or an explicit not-persisted status when a requested event could not be saved.
- If capture was requested, candidate Change ID, affected pages, and actual gate status; keep the direct answer distinct from the writeback result.

Do not cite a Wiki summary as if it were the original source. Preserve underlying source provenance.
