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
- **Context Pack:** the minimum set of instructions, accepted Wiki knowledge, task inputs, and source locators required to execute one task in a fresh Session.
- **Session:** one sequential execution segment backed by one fresh model context; it is not a Subagent or a provider-specific conversation ID.
- **Session Handoff:** the durable transfer of execution state from the current Session to a later fresh Session through a Checkpoint, Handoff Note, and Context Pack.

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

## 6. Context budget and sequential session handoff

### 6.1 Context budget

Use the host's context-usage indicator when available. Do not claim an exact token count or percentage when the host does not expose it.

Keep sufficient room for reasoning, tool results, report generation, and a safe handoff. Reduce context growth by:
- loading only the Context Pack for the active task;
- limiting tool output and avoiding bulk file dumps;
- not pasting entire previous Task Reports when their paths/IDs and relevant sections suffice;
- writing durable findings to Task Reports instead of carrying them only in conversation history;
- avoiding repeated source reads and duplicate summaries.

Do not rely on automatic context compaction as a lossless memory mechanism. Session handoff reduces dependence on the current conversation context; it does not prevent the host from compacting context before the handoff occurs.

### 6.2 Session model

A **Session** is one sequential execution segment for an Ingest run, backed by one fresh model context. It is a workflow concept, not a provider-specific conversation ID, a Subagent, or a new runtime.

- A new Session exists only when execution actually continues in a fresh model context. Sending another message in the same conversation does not create a new Session.
- Sessions execute sequentially in this workflow. Session Handoff does not require, imply, or create parallel Subagents.
- Each Session consumes a bounded Context Pack and writes durable Task Reports and Checkpoint updates.
- Session IDs are run-local logical IDs such as \`session-0001\`; do not invent host conversation IDs.
- Increment the session sequence only after a genuinely fresh context has been opened.

### 6.3 Handoff triggers

Prefer handoff at a safe task or phase boundary. Handoff is useful when:
- the host reports context usage at or above a configured project/host threshold;
- the host warns that context is nearing its limit;
- repeated large tool outputs or truncation indicate that the remaining work cannot be completed safely in the current context;
- Discovery and Analysis Planning are complete and deep source analysis is about to begin;
- the current task or a small group of related tasks is complete and the next work has a materially different focus;
- Process Integration is about to begin after a large set of Ingest tasks;
- the user requests a pause or the work must be resumed later.

Do not impose a universal utilization percentage. Use a configured threshold only when the host exposes a trustworthy usage indicator. If no indicator exists, use phase boundaries and qualitative warning signs; never claim to know the exact remaining budget.

Do not create a new Session after every small task. Keep a small number of closely related tasks together when their combined Context Pack and expected tool output remain safely bounded.

### 6.4 Handoff protocol

When a handoff is warranted:

1. Stop expanding the source scope. Finish the current logical analysis unit only if it can be completed safely.
2. Persist the current Task Report, including verified findings, exact Evidence locators, completed logical units, unresolved questions, and the next safe cursor. If the task is unfinished, set coverage to \`partial\`; use execution status \`blocked\` unless it is safe to resume directly from the recorded cursor.
3. Build a Context Pack for the next Session using \`references/context-pack-template.md\`. Include only the next task's objective, acceptance criteria, pinned revisions, necessary policy instructions, relevant prior report references, and exact source locators. Do not copy the full conversation or all prior reports.
4. Write a concise Handoff Note using \`references/session-handoff-template.md\`. The note points to the authoritative Checkpoint and next Context Pack; it does not duplicate the full Task Reports.
5. Update the Checkpoint last: mark the current Session \`handed_off\`, record the handoff reason and artifact paths, and set the next action. The Checkpoint must not point to a missing or unwritten artifact.
6. Stop the current Session after the handoff is committed. Do not continue source inspection in the same context while claiming a fresh Session has started.

If context pressure is urgent and a full Task Report cannot be completed, persist a partial report and the last verified logical unit. Never manufacture a complete task result from unsaved reasoning.

### 6.5 Resume protocol

At the start of a genuinely new Session:

1. Read the Checkpoint and the Handoff Note it references.
2. Read the Context Pack for the new Session. Treat the Checkpoint as the authoritative execution state, the Task Reports as the authoritative analysis record, and the Context Pack as a selective loading plan.
3. Verify the Source Manifest revisions and Wiki base/candidate revision before trusting prior findings.
4. Load only the task definition, required instructions, explicitly referenced Task Report sections, relevant Claims/Evidence, and source ranges needed for the next action.
5. Increment the logical Session sequence and mark the new Session \`active\`. Preserve the previous Session ID and last Handoff Note path.
6. Continue from the recorded cursor. Do not repeat completed tasks or reread completed source ranges unless a revision change, unresolved conflict, or evidence-validation requirement makes it necessary.

If the current conversation is continuing in the same model context, do not increment the Session sequence or pretend a rollover occurred.

### 6.6 Host capability boundary

A Skill can prepare handoff artifacts and a resume instruction, but it cannot create a new IDE/chat conversation unless the host explicitly provides that capability. When no such host operation exists, the Skill MUST save the handoff artifacts, print a concise instruction for opening a fresh conversation and resuming from the Context Pack, then stop. The user starts the new conversation.

This manual fresh-session handoff is supported for sequential Ingest work only. It is not a fallback for the independent Review gate: \`docs/independent-review-execution.md\` still requires automatic host-native isolated Subagent delegation and explicitly prohibits manual-session or same-context Review.

## 7. Durable artifacts and resume

Store working artifacts under the candidate Change Set, not in accepted Wiki pages:

- wiki/_meta/changes/<change-id>/ingestion/analysis-plan.md
- wiki/_meta/changes/<change-id>/ingestion/tasks/<task-id>.md
- wiki/_meta/changes/<change-id>/ingestion/checkpoint.yaml
- wiki/_meta/changes/<change-id>/ingestion/sessions/session-<sequence>-handoff.md
- wiki/_meta/changes/<change-id>/ingestion/sessions/session-<next-sequence>-context-pack.md

Use the exact paths available in the authorized Wiki workspace if its layout differs, and record that layout in the Ingestion Report.

Update the Checkpoint:
- after each meaningful logical analysis unit has been persisted to its Task Report;
- after each completed task;
- whenever task coverage becomes partial or task execution becomes blocked;
- before handing work to another context or Subagent;
- before stopping because of context pressure or interruption.

For a Session Handoff, write the Task Report first, then the next Session's Context Pack, then the Handoff Note, and update the Checkpoint last. The Checkpoint is the commit marker and MUST NOT reference an artifact that has not been written.

Keep the Checkpoint compact. Store task details and evidence in Task Reports; reference those artifacts by path rather than copying their contents into the Checkpoint.

On resume:
1. read the Checkpoint, referenced Handoff Note, and Context Pack for the new Session;
2. verify the Source Manifest, every relevant full source commit SHA, and the expected Wiki base/candidate workspace;
3. load only the task definition and Task Report sections, Claims/Evidence, instructions, and source locators named by the Context Pack;
4. continue from the recorded logical-unit cursor without repeating completed tasks or source reads;
5. if a source revision or relevant candidate artifact changed, mark affected task results stale and revalidate before using them.

A Checkpoint created by version 1 of this template may be resumed. Preserve its existing task state, initialize Session metadata as a migrated active Session, and upgrade it to version 2 on the next write; do not rerun completed tasks solely because the Checkpoint was upgraded.

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

Task execution status, coverage status, and Session metadata are workflow metadata, not Claim, Evidence, Change Set, Review, Human Decision, or Publication states.

Use:
- execution_status: pending, in_progress, completed, or blocked;
- coverage_status: not_started, partial, or complete.

A completed task may have complete coverage only for its declared scope. Process-level coverage is derived from all required tasks and relevant profiles. Repository-level coverage must not be inferred from a single Process result.

A run with unfinished required tasks is PARTIAL or BLOCKED according to the cause. Candidate Wiki content remains subject to the existing Lint, independent Review, Human Review, and explicit Publication gates.
