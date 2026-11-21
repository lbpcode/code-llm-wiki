# Code LLM Wiki

A source-grounded engineering knowledge workflow for multi-repository, process-oriented software systems.

## v0.1.0

- Process-centric knowledge model with System-level synthesis.
- Phase-one Platform Profiles: QNX, Android, and Linux (TBOX).
- Deployment context is bound to each Platform Profile.
- Portable Agent Skills and prompts, loaded and executed by an IDE AI plugin / host agent.
- No model API client, inference service, or model-provider integration is implemented by this project; model selection, authentication, and invocation remain the responsibility of the IDE plugin and the organization's AI environment.
- Markdown knowledge stored in a separate Git repository.
- Optional CMake Graphviz DOT for build dependencies only.
- AST deferred.
- Strict quality gate: source evidence, independent LLM review, and human approval.
- English Skill instructions with Simplified Chinese as the default generated Wiki/report language.

## Repository layout

- `SKILL.md`: entry point and workflow router.
- `skills/`: init, ingest, integrate, query, update, review, and lint.
- `docs/`: architecture, schema, evidence, quality gate, language policy, and decisions.
- `references/`: profile definitions, templates, and checklists.
- `examples/`: illustrative examples only.

## Quick start

1. Install or expose the root Skill and individual Skills to the IDE AI plugin / host agent.
2. Open the source superproject containing Git submodules in the IDE workspace.
3. Ensure the plugin can read the workspace, inspect Git state, and write to the separate Engineering Wiki repository.
4. Run `code-wiki-init` to inventory repositories, AGENTS.md files, pinned commits, and profiles.
5. Run `code-wiki-ingest` per repository/process.
6. Run `code-wiki-integrate` for cross-process knowledge.
7. Run `code-wiki-lint` and an independent `code-wiki-review`.
8. Obtain human approval before merging into the Engineering Wiki repository.

The IDE plugin / host agent supplies model execution and workspace capabilities. A Skill is an instruction package; it does not itself grant filesystem, terminal, Git, or repository write permissions. This project does not add a TypeScript runtime, LangChain, MCP, a vector database, a custom agent framework, or a model API client.

## Key rules

- Repository and Process are distinct; their relationship can be many-to-many.
- Build dependencies, runtime dependencies, IPC, and startup ordering are different relationship types.
- CMake DOT is build-graph evidence, not runtime architecture evidence.
- Claims must be scoped to the applicable Platform Profile and pinned source commit.
- Unknown information stays Unknown; no invented facts.
- Generated knowledge is provisional until independent review and human approval.
- Generated human-readable Wiki content defaults to Simplified Chinese; source identifiers and machine-readable metadata remain unchanged.

See `docs/architecture.md`, `docs/wiki-schema.md`, and `docs/language-policy.md`.
