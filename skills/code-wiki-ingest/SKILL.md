---
name: code-wiki-ingest
description: Analyze one repository or bounded process scope and produce source-grounded Process Wiki knowledge through context-bounded, resumable Analysis Tasks.
---

# code-wiki-ingest

## Goal

Build accurate Process-level knowledge from pinned source revisions without loading an entire repository into one model context. Discover first, plan bounded Analysis Tasks, inspect only relevant source, persist each result, and integrate only evidence-backed findings.

## Normative references

Follow:
- docs/context-management.md
- docs/skill-contracts.md
- docs/independent-review-execution.md
- docs/wiki-schema.md
- docs/claim-evidence-model.md
- docs/source-evidence.md
- docs/state-machine.md
- docs/failure-handling.md
- docs/language-policy.md
- docs/wiki-maintenance.md

Use:
- references/process-template.md
- references/claim-template.md
- references/analysis-task-template.md
- references/checkpoint-template.md
- references/context-pack-template.md
- references/session-handoff-template.md
- references/ingestion-report-template.md

## Required inputs

- Source Manifest and selected repository ID(s).
- Exact pinned full commit SHA for each selected repository.
- Applicable parent and repository AGENTS.md files.
- Known or candidate Process ID(s).
- Process-to-Profile applicability and its evidence/status.
- Authorized Wiki destination and base revision.
- Existing accepted Wiki knowledge and any prior Checkpoint for a resumed run.

If the source commit does not match the manifest, stop ingestion for that repository. If process/profile mapping is uncertain, keep it candidate/unknown; do not guess.

## Procedure

### 1. Preflight and repository discovery

1. Confirm repository identity, working tree state, submodule pins, and exact source commits.
2. Read applicable AGENTS.md instructions once. Treat them as repository guidance, not as proof that implementation behavior matches the description.
3. Inventory repository paths and file names. Identify likely executable entry points, service/process definitions, build targets, public headers, deployment artifacts, startup configuration, security policy, and relevant tests.
4. Read key maintained documentation and only the build/service/configuration files needed to understand repository structure.
5. Do not bulk-read all source files. Discovery is an inventory and boundary-identification step, not deep implementation analysis.
6. Create a Repository Map with candidate Repository-to-Process mappings and Process-to-Profile support statuses. Attach evidence or keep mappings candidate/unknown.

Generated output, build directories, vendored dependencies, and unrelated test data are excluded by default. Include them only when a specific task requires them. Tests may be necessary evidence and must be selected when they demonstrate behavior.

### 2. Build an Analysis Plan before deep reading

1. Identify the Process or bounded Process scope selected for ingestion. Analyze multiple Processes separately even when they share one repository.
2. Break the work into Analysis Tasks by engineering concern, not by file. Typical concerns include process boundary/entry, startup/shutdown, suspend/resume, IPC/interface, data flow, concurrency/resource ownership, security/permissions, deployment, and profile differences.
3. Create only tasks relevant to the actual Process. Do not force every category or create one task per source file.
4. Each task must state its objective, Process/Profile/repository scope, pinned revisions, candidate input paths/symbols/configuration, dependencies, exclusions, and acceptance criteria.
5. Keep profile-specific behavior separate where implementations may differ. A common claim requires evidence across every applicable profile.
6. Order dependent tasks. Independent tasks may be delegated only when the host provides genuinely isolated Subagents.

Save the plan under the candidate Change Set using references/analysis-task-template.md and record its path in the Ingestion Report.

### 3. Execute bounded Analysis Tasks

For each task:

1. Build a minimal Context Pack from applicable instructions, relevant accepted Wiki knowledge, task definition, and only the source inputs needed for the objective.
2. Search for relevant symbols, APIs, configuration keys, message types, entry points, and callers before opening implementation files.
3. Read targeted logical source units: relevant implementation, declaration/type, caller/callee context, configuration, and tests as needed. For large files, inspect specific functions or line ranges rather than dumping the whole file.
4. Expand to additional files only when the current evidence shows they are needed to satisfy the task's acceptance criteria.
5. Bound tool output. If output is truncated, record the gap and re-read the missing range. Never treat truncated output as complete evidence.
6. Avoid repeated reads of the same source range. Record evidence locators at the time of inspection, tied to the exact repository commit.
7. Stop when acceptance criteria are met. If the investigation expands into another independent concern, create a follow-up task instead of broadening the current task indefinitely.
8. Split a task when it spans multiple independent outcomes, repeatedly expands, or approaches the host context limit. Do not rely on automatic context compaction to preserve facts.
9. Create a Task Report using references/analysis-task-template.md. Record verified findings, inferred findings with reasoning, unknowns, contradictions, inspected scope, limitations, and evidence.
10. After each meaningful logical analysis unit, persist its findings and Evidence locators to the Task Report, then update the Checkpoint's last persisted unit/cursor. Also update after task completion, partial/blocked transitions, and before any context/session handoff. Do not wait until the entire Task is complete to persist all findings.

Use execution_status pending/in_progress/completed/blocked and coverage_status not_started/partial/complete as workflow metadata only. These are not Wiki Claim or Change Set states.

### 4. Sequential Session Handoff (no Subagent required)

Use Session Handoff when the current model context should be retired before the Ingest run is complete. This is a sequential execution mechanism and does not require or invoke Subagents.

1. Prefer safe boundaries: after Discovery/Planning, after one or a small number of related Analysis Tasks, or before Process Integration. Do not create a new Session after every small task.
2. If the host exposes a trustworthy context-usage indicator, follow the configured handoff threshold. Do not invent an exact percentage. Without an indicator, use host warnings, repeated output truncation, scope expansion, and planned phase boundaries.
3. Persist the current Task Report at logical-unit granularity. If the active task is unfinished, record partial coverage, the last persisted unit, exact resume cursor, unresolved questions, and verified Evidence only.
4. Create the next Session's Context Pack using references/context-pack-template.md. Include only the next task's required instructions, task definition, necessary report sections/Claim/Evidence references, pinned source revisions, and source locators.
5. Create a Handoff Note using references/session-handoff-template.md.
6. Update the Checkpoint last, mark the current Session handed_off, and record the Handoff Note, Context Pack, handoff reason, and next action. Verify that both referenced artifacts exist.
7. Stop the current Session. Do not continue reading source or claim that the context has been reset.

A Skill cannot open a new IDE/chat conversation unless the host explicitly exposes that operation. If it does not, output the exact resume instruction and ask the user to start a fresh conversation. The next conversation resumes from the Context Pack and Checkpoint, not the old chat transcript.

Do not use this mechanism as a fallback for the independent Review gate. Review still requires automatic host-native isolated Subagent delegation under docs/independent-review-execution.md.

### 5. Optional Subagent delegation

If the host supports isolated Subagents, delegate independent Analysis Tasks with a bounded task packet containing:
- exact objective and acceptance criteria;
- Process/Profile scope and allowed repositories/paths;
- full pinned source revisions;
- required Claim/Evidence locator format;
- explicit exclusions and read-only boundaries;
- required Task Report output.

Prefer a small number of independent, high-value tasks. Do not parallelize dependent tasks or allow workers to edit the same canonical Wiki files. The orchestrator must validate returned evidence locators, reconcile conflicts, and write canonical candidate artifacts.

Subagent delegation is optional for Ingest. If unavailable, execute tasks sequentially with Checkpoint/Resume. This does not change the mandatory isolated Subagent requirement for the later independent Review gate.

### 6. Resume interrupted ingestion

When resuming in a fresh Session, read the Checkpoint, referenced Handoff Note, and next Context Pack first. Verify the Source Manifest, Wiki base revision, and all relevant source commits before trusting prior results. If the Checkpoint is version 1, preserve its task states and upgrade it to version 2 without redoing completed work.

Load only the current task definition, required policy instructions, relevant sections of Task Reports, necessary Claims/Evidence, and source locators listed in the Context Pack. Do not load the full prior conversation or every completed report. Continue pending tasks and resume blocked/in-progress tasks only after their blocker or interruption is resolved. Do not repeat completed tasks or reread completed source ranges unless a revision changed, evidence no longer resolves, or a conflict requires revalidation.

Increment the logical Session sequence only when this is a genuinely new model context. If continuing in the same context, retain the current Session ID.

If the Checkpoint is missing or inconsistent, reconstruct task state from durable reports and pinned source revisions. Mark uncertain work partial; never guess that a task completed.

### 7. Process integration and Wiki generation

1. Integrate Task Reports, Claims/Evidence, Repository Map, and relevant existing Wiki knowledge.
2. Do not reread the entire repository during integration. Reopen source only to validate evidence, resolve conflicts, inspect both sides of an interface, or answer a specific cross-module/cross-repository question.
3. If substantial new source analysis is required, create a focused follow-up Analysis Task and checkpoint it.
4. Analyze responsibility, boundaries, lifecycle, interfaces, runtime dependencies, data flow, security, deployment, resource constraints, and failure behavior only to the extent supported by the task coverage.
5. Inspect QNX, Android, and Linux-TBOX separately, but only for profiles present or explicitly in scope. Record Process-to-Profile support status and evidence.
6. Treat CMake Graphviz DOT only as optional build-target dependency evidence. It does not prove runtime dependencies, IPC, startup order, or call flow. AST/Tree-sitter/Clang extraction remains deferred.
7. Split material statements into atomic Claims. Map each Claim to exact Evidence records with repository, full commit, path, locator, evidence type, profile scope, and supports/contradicts/qualifies relation.
8. Mark claims verified, inferred, unknown, stale, or contradicted. Inferred claims require explicit reasoning; unknown claims require a gap description.
9. Inspect both sides of interfaces when possible. A one-sided interface remains candidate/unknown.
10. Update Page-Source Map entries only for pages and sources actually inspected. Preserve human edits and all existing candidate/accepted state boundaries.
11. Add contextual links between related knowledge pages and synchronize wiki/index.md with candidate pages and actual page/change status. Persist the ingestion report and append the observed ingest event before freezing the candidate; deferred gate events follow docs/wiki-maintenance.md.

### 8. Quality gates

Run Lint. If Lint PASS, the orchestrator MUST automatically delegate a fresh host-native Review Subagent using references/review-agent-task-template.md and skills/code-wiki-review/SKILL.md. Wait for a completed, snapshot-bound report.

Do not ask the user to open a second conversation or copy a prompt. If Subagent delegation/isolation is unavailable, set Review execution status to NOT_RUN, leave Review decision null, keep Change Status at pending_llm_review, and set Run outcome to BLOCKED. There is no manual-session or same-context fallback for independent Review.

Keep all generated content as a candidate diff until human approval and explicit publication authorization.

## Required outputs

- Repository Map and candidate Repository-to-Process / Process-to-Profile mappings.
- Analysis Plan and per-task reports.
- Checkpoint with source revisions, task states, logical-unit cursor, and Session metadata.
- Session Handoff Note and next Context Pack whenever execution is handed to a fresh context.
- Process overview and boundary, with coverage status.
- Profile-specific sections/pages for confirmed or explicitly in-scope profiles.
- Atomic Claim-Evidence records.
- Interface/Workflow candidates where evidence supports them.
- Page-Source Map entries for inspected sources only.
- Ingestion report with planned/completed/partial/blocked tasks, coverage, failures, unknowns, and open questions.
- Proposed Wiki diff.
- Synchronized index, contextual page links, and ingestion event or explicit deferred-event location.
- Lint report and independent Review report; if delegation is blocked, record Review execution status, null Review decision, unchanged Change Status, and Run outcome BLOCKED.

## Failure behavior

Follow docs/failure-handling.md and docs/context-management.md. A failure in one repository or task may allow independent scopes to continue, but the report must be PARTIAL/BLOCKED as appropriate. A commit mismatch, missing required context, unresolved conflict, or sensitive-data exposure blocks the affected scope. Do not summarize only README or a subset of files and call the Process complete.

## Prohibited shortcuts

- Do not equate one repository with one process.
- Do not equate one task or one inspected file set with complete Process coverage.
- Do not bulk-read an entire repository into one context.
- Do not invent completion after context truncation, compaction, interruption, or missing reports.
- Do not infer platform support from names, directories, macros, or build targets.
- Do not infer runtime relationships from CMake.
- Do not invent startup order, IPC semantics, permission behavior, or suspend/resume support.
- Do not copy secrets into Wiki pages or evidence excerpts.
- Do not overwrite human-authored content or self-approve the candidate.
