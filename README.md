# Code LLM Wiki

A source-grounded engineering knowledge workflow for multi-repository, process-oriented software systems.

## v0.1.0

- Process-centric knowledge model with System-level synthesis.
- Phase-one Platform Profiles: QNX, Android, and Linux (TBOX).
- Deployment context is bound to each Platform Profile.
- Portable Agent Skills and prompts; reuse the host agent and existing OpenAI-compatible API.
- Markdown knowledge stored in a separate Git repository.
- Optional CMake Graphviz DOT for build dependencies only.
- AST deferred.
- Strict quality gate: source evidence, independent LLM review, and human approval.

## Repository layout

- `SKILL.md`: entry point and workflow router.
- `skills/`: init, ingest, integrate, query, update, review, and lint.
- `docs/`: architecture, schema, evidence, and quality gate.
- `references/`: profile definitions, templates, and checklists.
- `examples/`: illustrative examples only.

## Quick start

1. Expose the root skill and individual skills to the host agent.
2. Open the source superproject containing Git submodules.
3. Run `code-wiki-init` to inventory repositories, AGENTS.md files, pinned commits, and profiles.
4. Run `code-wiki-ingest` per repository/process.
5. Run `code-wiki-integrate` for cross-process knowledge.
6. Run `code-wiki-lint` and an independent `code-wiki-review`.
7. Obtain human approval before merging into the Engineering Wiki repository.

The host agent must provide repository/file access and write access to the destination Wiki. A model API alone cannot read local files or persist Git commits. This project does not add TypeScript Runtime, LangChain, MCP, a vector database, or a custom agent framework.

## Key rules

- Repository and Process are distinct; their relationship can be many-to-many.
- Build dependencies, runtime dependencies, IPC, and startup ordering are different relationship types.
- CMake DOT is build-graph evidence, not runtime architecture evidence.
- Claims must be scoped to the applicable Platform Profile and pinned source commit.
- Unknown information stays Unknown; no invented facts.
- Generated knowledge is provisional until independent review and human approval.

See `docs/architecture.md` and `docs/wiki-schema.md`.
