# Architecture Decision Records

## ADR-001: Skill/Prompt-first implementation

**Status:** Accepted for v0.1.0

Use portable Agent Skills and Prompts as the complete implementation form for the initial workflow. Keep each operation focused and reusable. Do not introduce a separate application runtime or orchestration framework in phase one.

## ADR-002: Process-centric knowledge model

**Status:** Accepted for v0.1.0

Use Process as the primary knowledge entity and System as the cross-process synthesis layer. Repository and Process are distinct and have a many-to-many relationship. A repository may contain multiple processes; a process may span repositories.

## ADR-003: Atomic Platform Profiles

**Status:** Accepted for v0.1.0

Phase-one profiles are qnx, android, and linux-tbox. Bind OS and known deployment context in each profile. Do not generate an unrestricted OS × product matrix. QNX and Android product context must be discovered from the real project; do not assume IVI or TBOX. Linux-TBOX is one bound profile.

Process-to-Profile applicability is separate from Repository inventory because processes in one repository may have different platform support.

## ADR-004: Defer AST

**Status:** Accepted for v0.1.0

Do not introduce Tree-sitter, Clang AST, or other AST extraction in phase one. Reconsider only when concrete Wiki quality or engineering queries cannot be answered reliably from source/document inspection.

## ADR-005: Include optional CMake Graphviz DOT

**Status:** Accepted for v0.1.0

Support CMake Graphviz DOT as optional build-target dependency evidence when CMake is used and a representative configuration can be generated. DOT does not prove runtime dependencies, IPC, startup ordering, or call relationships. Failure/unavailability must not block unrelated ingestion.

## ADR-006: Strict knowledge quality gate

**Status:** Accepted for v0.1.0

Require source evidence, structural/provenance Lint, independent LLM review in a separate context, and human approval. BLOCKER or MAJOR findings prevent PASS. A numeric score cannot override critical factual/evidence failures. A missing required check is NOT RUN and blocks progression.

## ADR-007: Separate Private Engineering Wiki repository

**Status:** Accepted for v0.1.0

Store generated engineering knowledge in a separate Private Git repository. The source superproject remains the source of truth. Wiki updates are proposed as diffs and published only after human approval and explicit publication authorization.

## ADR-008: Separate knowledge and approval state domains

**Status:** Accepted for v0.1.0

Claim status, Evidence status, Change Set status, LLM Review decision, Human decision, and Publication status are independent. A verified claim is not necessarily approved; LLM PASS is not human approval; approval is not publication. See docs/state-machine.md.

## ADR-009: Atomic Claim-Evidence mapping

**Status:** Accepted for v0.1.0

Every material factual statement is an atomic Claim with explicit scope and links to specific Evidence records. Page-level bibliographies alone are insufficient. Evidence is pinned to repository, full commit SHA, path, locator, evidence type, and profile scope.

## ADR-010: Page-Source Map for incremental updates

**Status:** Accepted for v0.1.0

Maintain a reverse map from Wiki page to Claim IDs, source repositories/revisions/paths, and dependent pages. Source changes invalidate only affected claims/pages when impact can be demonstrated; otherwise broaden review conservatively.

## ADR-011: Approval binds to exact candidate snapshot

**Status:** Accepted for v0.1.0

Human approval binds to the exact candidate Wiki commit or diff digest, base commit, changed page scope, Source Manifest version/digest, relevant source revisions, Lint report, and independent Review report. Any material change invalidates approval. Publication is a separate explicitly authorized action.

## ADR-012: Preserve human edits and immutable audit history

**Status:** Accepted for v0.1.0

AI updates must not overwrite human edits. Overlapping semantic changes stop for human conflict resolution. Rejected candidates and prior review/decision records remain in audit history. Correct published content through a new change or revert commit, not history rewriting.

## ADR-013: Partial failure is explicit

**Status:** Accepted for v0.1.0

Independent repositories may be processed separately, but inaccessible or failed scopes must be reported. PARTIAL/BLOCKED runs cannot be treated as complete System knowledge or published. Optional CMake DOT failure alone does not block unrelated work.


## ADR-014: Bounded and resumable repository ingestion

**Status:** Accepted

Ingest MUST discover repository structure before deep source inspection, plan bounded Analysis Tasks by engineering concern, read only task-relevant source ranges, and persist Task Reports plus a compact Checkpoint. Tasks are not split mechanically by file. Resume verifies pinned source revisions and the Wiki candidate/base before reusing results. Process Integration consumes durable reports first and performs targeted source re-reads only when needed. Host-native isolated Subagents may execute independent Ingest tasks; sequential Checkpoint/Resume remains the portable fallback. This workflow does not introduce a custom runtime, token service, database, or AST dependency.
