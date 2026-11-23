# Context-Bounded Ingestion

## 1. Purpose

Repository ingestion must remain accurate when a source repository is too large to inspect in one model context. This document defines a bounded, resumable analysis workflow for the existing Skill/Prompt implementation.

The objective is not to fit an entire repository into one context. The objective is to produce complete, evidence-backed knowledge for an explicitly bounded scope while keeping unfinished work visible and recoverable.

This is a workflow contract, not a new runtime. It does not require a database, vector store, indexing service, token-counting service, AST extractor, or orchestration framework.

## 2. Concepts

- **Analysis Plan:** the finite list of analysis tasks required for the selected Repository / Process / Profile scope.
- **Analysis Task:** one bounded engineering question or concern, such as process entry, startup lifecycle, suspend/resume, IPC contract, thread/resource ownership, security, or deployment.
- **Task Report:** the durable result of one task, including findings, exact evidence, unknowns, coverage, and follow-up work.
- **Checkpoint:** a compact, durable pointer to the plan, task states, source revisions, completed reports, and the next safe action.
- **Context Pack:** the minimum set of instructions, accepted Wiki knowledge, task inputs, and source excerpts required to execute one task.

Analysis Tasks are not files, classes, or arbitrary line ranges. A task is defined by an objective and acceptance criteria. Do not create one task per file. A small repository may need only a few tasks; a large or multi-process repository may need many.

A task should normally target one Process and one primary concern. Keep profile-specific behavior separate when evidence may differ. A deliberate cross-repository or cross-profile task is allowed when the relationship itself is the objective.

## 3. Discovery before source reading

Discovery builds an inventory and identifies likely analysis boundaries. It is not a full code review.

1. Verify repository identity, working tree state, and the exact pinned full commit SHA.
2. Read applicable parent and repository AGENTS.md instructions once, plus key maintained project documentation.
3. Inventory paths and file names; identify likely entry points, executable/service definitions, build targets, deployment files, configuration, public headers, and tests.
4. Inspect relevant build and service metadata such as CMake, Android.bp/Android.mk, QNX service/startup configuration, permissions, and package definitions.
5. Produce a Repository Map and candidate Repository-to-Process / Process-to-Profile mappings with explicit status and evidence.
6. Do not bulk-open all .cpp, .c, .h, or .hpp files during discovery.

Generated output, build directories, vendored dependencies, and unrelated test data are excluded by default. Include them only when the selected task requires them. Tests are valid evidence when they demonstrate behavior and should not be excluded categorically.

File names, directory names, build targets, comments, and AGENTS.md descriptions are discovery hints, not sufficient proof of runtime behavior or platform support.

## 4. Source-reading policy

For each Analysis Task:

1. Start from a concrete question and search for the relevant symbol, API, configuration key, message type, registration point, or entry point.
2. Read the smallest useful logical source units: the relevant implementation, declaration or type, caller/callee context, configuration, and tests as needed.
3. Expand to another file only when the current evidence identifies a dependency needed to answer the task.
4. Follow call paths only as far as required by the task's acceptance criteria. Record unresolved indirect calls, callbacks, function pointers, virtual dispatch, dynamic loading, macros, or generated-code boundaries as limitations when they cannot be resolved.
5. For large files, read targeted line ranges or logical function/class sections. Do not repeatedly dump the full file or repository.
6. Bound each tool response. Prefer search results and targeted excerpts over broad recursive output. If a tool truncates output, mark the affected inspection incomplete and re-read the exact missing range; never treat truncated output as complete evidence.
7. Record exact repository-relative paths, line ranges or stable symbols, repository IDs, and pinned commits while inspecting. Do not reconstruct locators from memory at the end.
8. Avoid rereading a source range already inspected in the same task unless a contradiction, missing context, or revision change requires it.
9. Stop expanding when the acceptance criteria are met. If the task reveals a separate engineering question, create a follow-up task rather than silently broadening the current one.

Do not impose a universal maximum file count or token count. File size and code complexity vary. If the task repeatedly expands, spans multiple independent concerns, or approaches the host's context limit, split it into smaller tasks.

CMake Graphviz DOT remains optional build-dependency evidence under docs/architecture.md. It does not replace source inspection. AST/Tree-sitter/Clang extraction remains deferred.

## 5. Analysis planning and task execution

Before deep source reading, create an Analysis Plan. Use references/analysis-task-template.md for each task.

The plan should:
- identify the selected Repository, Process, and applicable Profile scope;
- list task IDs, objectives, in-scope questions, exclusions, dependencies, candidate inputs, and acceptance criteria;
- order dependent tasks explicitly;
- separate independent concerns where doing so reduces context size;
- include only analysis dimensions relevant to the actual Process.

Typical task categories include process boundary and entry, startup/shutdown, suspend/resume, IPC/interface, data flow, concurrency/resource ownership, security/permissions, deployment, and platform differences. These are examples, not mandatory tasks for every Process.

Execute one bounded task at a time unless the host supports genuinely isolated Subagents and the tasks are independent. When Subagents are available, provide each worker with an exact task packet, pinned source revisions, allowed scope, required evidence format, and read-only boundaries. Workers return Task Reports; the orchestrator validates evidence locators, reconciles findings, and performs canonical Wiki writes. Do not let concurrent workers overwrite the same Wiki page or metadata file.

Subagent use is optional for Ingest. If the host does not support isolated Subagents, execute tasks sequentially and checkpoint between them. This does not weaken the separate mandatory independent-review requirement in docs/independent-review-execution.md.

A task is complete only when:
- its stated acceptance criteria have been addressed;
- material findings are atomic and linked to evidence at the pinned commit;
- evidence locators have been resolved, not guessed;
- unresolved questions and analysis limitations are explicit;
- its Task Report is saved.

Do not mark an entire Process complete merely because one task or one group of files was inspected.

## 6. Context budget and handoff

Use the host's context-usage indicator when available. Do not claim an exact token count when the host does not expose one.

Keep sufficient room for reasoning, report generation, tool results, and the next handoff. Reduce context growth by:
- loading only the Context Pack for the active task;
- limiting tool output and avoiding bulk file dumps;
- not pasting entire previous Task Reports when their paths/IDs and relevant sections suffice;
- writing durable findings to Task Reports instead of carrying them only in conversation history;
- avoiding repeated source reads and duplicate summaries.

Do not rely on automatic context compaction as a lossless memory mechanism. When the host indicates context pressure, tool output becomes unwieldy, or the current task starts accumulating unrelated concerns:
1. stop expanding the source scope;
2. finish the current atomic unit only if it can be completed safely;
3. save its Task Report with coverage_status=partial when the task is not complete;
4. update the Checkpoint;
5. continue in a fresh isolated context/session when available, loading only the Checkpoint, relevant Task Reports, and the next Context Pack.

If there is not enough context to finish safely, stop and checkpoint the task with coverage_status=partial and execution_status=blocked (or in_progress only when it remains safely resumable). Never manufacture a complete result from a partial read.

## 7. Durable artifacts and resume

Store working artifacts under the candidate Change Set, not in accepted Wiki pages:

- wiki/_meta/changes/<change-id>/ingestion/analysis-plan.md
- wiki/_meta/changes/<change-id>/ingestion/tasks/<task-id>.md
- wiki/_meta/changes/<change-id>/ingestion/checkpoint.yaml

Use the exact paths available in the authorized Wiki workspace if its layout differs, and record that layout in the Ingestion Report.

Update the Checkpoint:
- after each completed task;
- whenever task coverage becomes partial or task execution becomes blocked;
- before handing work to another context or Subagent;
- before stopping because of context pressure or interruption.

Keep the Checkpoint compact. Store task details and evidence in Task Reports; reference those artifacts by path rather than copying their contents into the Checkpoint.

On resume:
1. read the Source Manifest, current candidate Change Set, Analysis Plan, and Checkpoint;
2. verify that every relevant repository still matches its pinned full commit SHA and that the Wiki base/candidate workspace is the expected one;
3. load only the Task Reports needed by the next task, including relevant completed or partial reports, plus the minimal Context Pack;
4. continue pending tasks without repeating completed tasks;
5. if a source revision or relevant candidate artifact changed, mark affected task results stale and revalidate before using them.

If the Checkpoint is missing or inconsistent, do not guess where execution stopped. Reconstruct the affected task state from durable Task Reports and source revisions; mark uncertain work partial and repeat only the necessary inspection.

## 8. Process integration handoff

Process integration should consume the Analysis Plan, Task Reports, Claim/Evidence records, Repository Map, Source Manifest, and relevant Page-Source Map entries.

Do not reload every source file already analyzed. Reopen source only to:
- validate a cited locator;
- resolve conflicting or incomplete findings;
- inspect both sides of an interface;
- verify a cross-module or cross-repository relationship;
- answer a specific integration question not covered by the Task Reports.

If a missing relationship requires substantial additional source analysis, create a focused follow-up Analysis Task and checkpoint it. Integration must preserve partial coverage and unknowns; it must not turn a set of partial reports into a complete Process description.

## 9. Coverage and state boundaries

Task execution status and coverage status are workflow metadata, not Claim, Evidence, Change Set, Review, Human Decision, or Publication states.

Use:
- execution_status: pending, in_progress, completed, or blocked;
- coverage_status: not_started, partial, or complete.

A completed task may have complete coverage only for its declared scope. Process-level coverage is derived from all required tasks and relevant profiles. Repository-level coverage must not be inferred from a single Process result.

A run with unfinished required tasks is PARTIAL or BLOCKED according to the cause. Candidate Wiki content remains subject to the existing Lint, independent Review, Human Review, and explicit Publication gates.
