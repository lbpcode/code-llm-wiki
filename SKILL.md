---
name: code-llm-wiki
description: Build and maintain a source-grounded engineering Wiki for multi-repository, process-oriented software systems. Use to initialize, ingest, integrate, query, update, review, or validate knowledge across a superproject and Git submodules.
---

# Code LLM Wiki — entry skill

Use this repository as a portable Skill/Prompt workflow loaded and executed by an IDE AI plugin or host agent. Do not assume a custom runtime, TypeScript application, model API client, LangChain, MCP server, vector database, or AST indexer.

## Project invariants

1. The primary knowledge entity is **Process**, not an internal source-code module.
2. The upper knowledge layer is **System**, describing cross-process architecture and behavior.
3. Repository and Process are distinct entities with a many-to-many relationship.
4. Phase-one Platform Profiles are **qnx**, **android**, and **linux-tbox**.
5. Deployment context is bound into each Platform Profile. Do not create an unrestricted OS × product matrix.
6. A process may have common knowledge and profile-specific knowledge. Mark content common only when evidence supports that scope.
7. Important claims require source evidence tied to a repository commit.
8. Build dependency, runtime dependency, IPC relationship, and startup ordering must never be conflated.
9. CMake DOT is optional build-dependency evidence only. AST is deferred.
10. No generated page is accepted without independent LLM review and human approval.

## Execution environment

The IDE AI plugin / host agent is responsible for loading this Skill, invoking its configured model, reading the source workspace, inspecting Git state, and writing to the separate Engineering Wiki repository. The IDE, plugin, model, and provider are not fixed by this project.

Code LLM Wiki does not directly call model APIs and does not provide a model API client, provider adapter, or inference service. The plugin must supply the required file, terminal, Git, and destination-repository permissions. If a capability is missing, report it explicitly; do not claim the operation succeeded.

## Output language policy

Unless the user explicitly requests another language, all generated Wiki pages, architecture documentation, analysis/integration reports, update summaries, query answers, and review reports MUST use **Simplified Chinese**.

Keep Skill instructions and reusable prompt templates in this repository in English. Preserve source identifiers, API names, symbols, paths, commands, configuration keys, enum values, commit SHAs, and source excerpts exactly as they appear in the source. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English. Use Chinese for human-readable explanations and titles, retaining established English technical terms where appropriate.

See docs/language-policy.md for the complete rules. Every individual workflow Skill must follow this language policy even when invoked without the root Skill.

## Route the task

- Initialize a source superproject/Wiki pair: use skills/code-wiki-init/SKILL.md.
- Analyze one repository or process: use skills/code-wiki-ingest/SKILL.md.
- Synthesize multiple processes: use skills/code-wiki-integrate/SKILL.md.
- Answer an engineering question: use skills/code-wiki-query/SKILL.md.
- Refresh knowledge after source changes: use skills/code-wiki-update/SKILL.md.
- Perform strict semantic review: use skills/code-wiki-review/SKILL.md.
- Check structure, links, manifests, and stale evidence: use skills/code-wiki-lint/SKILL.md.

## Required workflow

Init → Ingest per repository/process → Integrate → Lint → Independent Review → Human Approval → Git merge.

Query is read-only by default. Update produces a proposed diff and must pass the same quality gate.
