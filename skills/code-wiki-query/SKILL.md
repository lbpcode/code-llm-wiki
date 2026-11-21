---
name: code-wiki-query
description: Answer engineering questions using the Code LLM Wiki, preserving source provenance, Process boundaries, and Platform Profile scope.
---

# code-wiki-query

## Goal

Answer engineering questions from the accepted Wiki without silently turning incomplete knowledge into certainty.


## Output language

Follow `docs/language-policy.md`. Unless the user explicitly requests another language, write generated Wiki pages, query answers, review findings, and deliverables in **Simplified Chinese**. Preserve source identifiers, API names, paths, commands, configuration keys, and source excerpts verbatim. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English.

## Procedure

1. Classify the question as system-level, process-level, interface, workflow, security, deployment, or platform comparison.
2. Identify the relevant Process IDs and Platform Profile(s).
3. Read the relevant Wiki pages and their source references.
4. Check page status and source revision freshness. Do not rely on stale pages as current facts.
5. Answer with the applicable profile scope and distinguish verified facts from inferences.
6. Cite repository, commit, path, and line/symbol/configuration locator for important claims.
7. If the Wiki does not contain enough evidence, say exactly what is unknown and identify the source that must be inspected.
8. Do not modify the Wiki during a query unless the user explicitly requests an update.

## Cross-platform questions

Compare QNX, Android, and Linux-TBOX only for profiles represented in the source manifest and backed by reviewed pages. Never assume an uninspected profile behaves like another profile.

## Output format

- Direct answer.
- Relevant Process/Profile scope.
- Evidence.
- Constraints, exceptions, and unknowns.
- Optional follow-up investigation.

Do not cite a Wiki summary as if it were the original source. Preserve the underlying source evidence.
