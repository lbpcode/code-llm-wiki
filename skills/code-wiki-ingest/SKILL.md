---
name: code-wiki-ingest
description: Analyze one repository or independent process and produce source-grounded Process Wiki pages with lifecycle, interfaces, dependencies, security, deployment, and Platform Profile differences.
---

# code-wiki-ingest

## Goal

Build accurate process-level knowledge from one repository at a time. Prefer understanding the process boundary and behavior over exhaustively cataloguing internal classes.


## Output language

Follow `docs/language-policy.md`. Unless the user explicitly requests another language, write generated Wiki pages, analysis notes, and deliverables in **Simplified Chinese**. Preserve source identifiers, API names, paths, commands, configuration keys, and source excerpts verbatim. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English.

## Required context

- Source manifest and selected repository ID.
- Pinned repository commit.
- Repository AGENTS.md files and applicable parent instructions.
- Known process ID(s) and applicable Platform Profile(s).

If the commit or profile scope is missing, stop and report the gap rather than guessing.

## Procedure

1. Read all applicable AGENTS.md files and key project documentation.
2. Confirm the source repository and commit match the manifest.
3. Identify executable entry points, process/service definitions, startup configuration, build targets, public interfaces, and deployment artifacts.
4. Establish which process or processes the repository implements. A repository may contain multiple executables or services.
5. Analyze process responsibility, boundaries, lifecycle, interfaces, runtime dependencies, data flow, security, deployment, and constraints.
6. Inspect profile-specific source/configuration separately for QNX, Android, and Linux-TBOX. Only analyze profiles that are present or explicitly in scope.
7. Separate common behavior from profile-specific behavior. A claim is common only when evidence supports every applicable profile.
8. Inspect CMake usage. If the repository uses CMake and the host environment can configure it with a representative existing toolchain/configuration, generate CMake Graphviz DOT. Record commit and configure context. If configuration is unavailable, report that; continue without DOT.
9. Treat DOT only as build-target dependency evidence. Do not infer runtime dependencies, IPC, or startup order from it.
10. Do not run AST/Tree-sitter/Clang extraction in v0.1.0.
11. Draft pages using references/process-template.md and docs/wiki-schema.md.
12. Attach source evidence to every material claim. Mark inferences and unknowns explicitly.
13. Update the page-source map and source manifest only for sources actually inspected.
14. Run code-wiki-lint and request independent code-wiki-review before proposing acceptance.

## Required output

- Process overview.
- Common knowledge, if genuinely common.
- One profile-specific section/page for each confirmed profile.
- Interface and workflow pages where cross-component contracts are substantial.
- Evidence index and unresolved questions.
- Proposed diff; do not self-approve or merge.

## Prohibited shortcuts

- Do not summarize only README and call it complete.
- Do not infer one process from one repository.
- Do not infer runtime relationships from CMake.
- Do not assume a process runs on a profile because a directory or macro name suggests it.
- Do not invent startup order, IPC semantics, permission behavior, or suspend/resume support.
