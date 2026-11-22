# Architecture Decision Records

## ADR-001: Skill/Prompt-first implementation

**Status:** Accepted for v0.1.0

Use portable Agent Skills and Prompts as the complete implementation form for the initial workflow. Keep each operation focused and reusable. Do not introduce a separate application runtime or orchestration framework in phase one.

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

Require source evidence, independent LLM review in a separate context, and human approval. BLOCKER or MAJOR findings prevent PASS. A numeric score cannot override critical factual/evidence failures.

## ADR-007: Separate Private Engineering Wiki repository

**Status:** Accepted for v0.1.0

Store generated engineering knowledge in a separate Private Git repository. The source superproject remains the source of truth. Wiki updates are proposed as diffs and merged only after human approval.
