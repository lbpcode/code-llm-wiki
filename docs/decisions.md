# Architecture Decision Records

## ADR-001: Skill/Prompt-first implementation

**Status:** Accepted for v0.1.0

Use portable Agent Skills and prompts as the product interface. The Skills are loaded and executed by an IDE AI plugin / host agent. Reuse the host's existing model and workspace capabilities rather than introducing a separate application runtime.

Do not add a TypeScript runtime, LangChain/LangGraph, MCP server, vector database, custom agent framework, or model orchestration backend in phase one. The host environment must provide the required file, terminal, and Git capabilities.

## ADR-002: Process-centric knowledge model

**Status:** Accepted for v0.1.0

Use Process as the primary knowledge entity and System as the cross-process synthesis layer. Repository and Process are distinct and have a many-to-many relationship. This fits systems assembled from independent process/service repositories better than a module-centric monorepo model.

## ADR-003: Atomic Platform Profiles

**Status:** Accepted for v0.1.0

Phase-one profiles are qnx, android, and linux-tbox. Bind OS and known deployment context in each profile. Do not generate an unrestricted OS × product matrix.

QNX and Android product context must be discovered from the real project; do not assume IVI or TBOX. Linux-TBOX is one bound profile.

## ADR-004: Defer AST

**Status:** Accepted for v0.1.0

Do not introduce Tree-sitter, Clang AST, or other AST extraction in phase one. Reconsider only when concrete Wiki quality or engineering queries cannot be answered reliably from source/document inspection.

## ADR-005: Include optional CMake Graphviz DOT

**Status:** Accepted for v0.1.0

Support CMake Graphviz DOT as optional build-target dependency evidence when CMake is used and a representative configuration can be generated. DOT does not prove runtime dependencies, IPC, startup ordering, or call relationships. Failure/unavailability must not block ingestion.

## ADR-006: Strict knowledge quality gate

**Status:** Accepted for v0.1.0

Require source evidence, independent LLM review in a separate invocation/context, and human approval. BLOCKER or MAJOR findings prevent PASS. A numeric score cannot override critical factual/evidence failures.

## ADR-007: Separate Private Engineering Wiki repository

**Status:** Accepted for v0.1.0

Store generated engineering knowledge in a separate Private Git repository. The source superproject remains the source of truth. Wiki updates are proposed as diffs and merged only after human approval.

## ADR-008: IDE plugin as model execution host

**Status:** Accepted for v0.1.0

Use the user's IDE AI plugin / host agent to load Skills, invoke the configured model, and access the source and destination workspaces. The specific IDE, plugin, model, and provider are not fixed by Code LLM Wiki.

Do not implement direct model API calls, API clients, provider adapters, or inference services in this project. Model selection, authentication, and invocation remain the responsibility of the IDE plugin and the organization's AI environment.

## ADR-009: Mandatory IDE agent capabilities

**Status:** Accepted for v0.1.0

The IDE AI plugin / host agent must satisfy the mandatory requirements in docs/ide-plugin-requirements.md before the real-repository POC. These include Skill loading, simultaneous access to the source superproject and separate Wiki worktree, file operations, terminal/Git/CMake command execution where applicable, isolated independent review sessions, and human-controlled approval.

These capabilities are acceptance requirements, not optional experiments. If the selected plugin cannot satisfy them, choose or configure a compatible IDE agent. Do not weaken the quality gate or introduce direct model API integration as a workaround.
