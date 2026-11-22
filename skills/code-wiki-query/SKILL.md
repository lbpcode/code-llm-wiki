---
name: code-wiki-query
description: Answer engineering questions using the accepted Code LLM Wiki, preserving source provenance, Process boundaries, Platform Profile scope, and uncertainty.
---

# code-wiki-query

## Goal

Answer engineering questions from accepted Wiki knowledge without silently turning incomplete, stale, or unreviewed content into certainty.

## Normative references

Follow docs/skill-contracts.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, and docs/language-policy.md.

## Default trust policy

- Query pages with `content_status: accepted` whose owning Change Set is `published` by default.
- Exclude draft, pending, rejected, superseded, stale, and contradicted claims from unqualified factual answers.
- Do not treat a verified Claim as proof that its page/change is approved; check page/change publication status separately.
- If the user explicitly asks to inspect candidate or historical content, label its state and revision clearly.
- Distinguish verified facts, inferences, unknowns, and conflicts.

## Procedure

1. Classify the question as system-level, process-level, interface, workflow, security, deployment, or platform comparison.
2. Identify relevant Process IDs and Platform Profile(s).
3. Read the relevant published Wiki pages, Claim-Evidence records, and source references.
4. Check page/change publication status, Claim status, Evidence status, and source revision freshness.
5. Answer with applicable scope and distinguish facts from inference.
6. Cite repository, full commit, path, and line/symbol/configuration locator for material claims.
7. If evidence is insufficient, say exactly what is unknown and identify the source or profile that must be inspected.
8. If sources conflict, disclose the conflict; do not choose a side without a documented resolution.
9. Do not modify the Wiki during a query unless the user explicitly requests an update.

## Cross-platform questions

Compare QNX, Android, and Linux-TBOX only for profiles represented in the Source Manifest and backed by reviewed/published pages. Never assume an uninspected profile behaves like another profile.

## Output format

- Direct answer.
- Relevant Process/Profile scope.
- Verified evidence and source locators.
- Inferences and assumptions.
- Constraints, exceptions, conflicts, and unknowns.
- Optional follow-up investigation.

Do not cite a Wiki summary as if it were the original source. Preserve underlying source provenance.
