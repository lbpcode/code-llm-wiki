---
name: code-wiki-ingest
description: Analyze one repository or independent process and produce source-grounded Process Wiki pages with atomic claims, evidence mappings, lifecycle, interfaces, dependencies, security, deployment, and Platform Profile differences.
---

# code-wiki-ingest

## Goal

Build accurate process-level knowledge from pinned source revisions. Prefer understanding process boundaries and behavior over exhaustively cataloguing internal classes.

## Normative references

Follow docs/skill-contracts.md, docs/independent-review-execution.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/source-evidence.md, docs/state-machine.md, docs/failure-handling.md, and docs/language-policy.md. Use references/process-template.md, references/claim-template.md, and references/ingestion-report-template.md.

## Required inputs

- Source Manifest and selected repository ID(s).
- Exact pinned full commit SHA for each selected repository.
- Repository AGENTS.md files and applicable parent instructions.
- Known or candidate Process ID(s).
- Process-to-Profile applicability and its evidence/status.
- Authorized Wiki destination and base revision.

If the source commit does not match the manifest, stop ingestion for that repository. If process/profile mapping is uncertain, keep it candidate/unknown; do not guess.

## Procedure

1. Read all applicable AGENTS.md files and key maintained project documentation.
2. Confirm repository identity, working tree state, and exact source commit against the manifest.
3. Identify executable entry points, process/service definitions, startup configuration, build targets, public interfaces, and deployment artifacts.
4. Establish which process or processes the repository implements. Analyze each Process separately even if several live in one repository.
5. Analyze responsibility, boundaries, lifecycle, interfaces, runtime dependencies, data flow, security, deployment, resource constraints, and failure behavior.
6. Inspect QNX, Android, and Linux-TBOX separately, but only for profiles present or explicitly in scope. Record Process-to-Profile support status and evidence.
7. Separate common behavior from profile-specific behavior. A claim is common only when evidence supports every applicable profile.
8. Inspect CMake usage. If CMake is used and a representative existing toolchain/configuration is available, generate Graphviz DOT. Record commit and configure context. If unavailable or generation fails, record the reason and continue unrelated analysis.
9. Treat DOT only as build-target dependency evidence. Never infer runtime dependencies, IPC, startup order, or call flow from it.
10. Do not run AST/Tree-sitter/Clang extraction in v0.1.0.
11. Split material statements into atomic Claims. Map each Claim to exact Evidence records with repository, full commit, path, locator, evidence type, profile scope, and supports/contradicts/qualifies relation.
12. Mark each Claim verified, inferred, unknown, stale, or contradicted. Inferred claims require explicit reasoning; unknown claims require a gap description.
13. Inspect both sides of interfaces when possible. A one-sided interface remains candidate/unknown.
14. Create Process pages and substantial Interface/Workflow candidates using the templates. Update Page-Source Map entries only for sources actually inspected.
15. Run Lint. If Lint PASS, the orchestrator MUST automatically delegate a fresh host-native Review Subagent using references/review-agent-task-template.md and skills/code-wiki-review/SKILL.md. Wait for a completed, snapshot-bound report. Do not ask the user to open a second conversation. If Subagent delegation/isolation is unavailable, set Review execution status to NOT_RUN, leave Review decision null, keep Change Status at pending_llm_review, and set Run outcome to BLOCKED. Keep all generated content as a candidate diff until human approval.

## Required outputs

- Process overview and boundary.
- Profile-specific sections/pages for confirmed or explicitly in-scope profiles.
- Atomic Claim-Evidence records.
- Interface/Workflow candidates where needed.
- Page-Source Map entries.
- Ingestion report with coverage, failures, unknowns, and open questions.
- Proposed Wiki diff.
- Lint report and independent Review report; if delegation is blocked, record Review execution status, null Review decision, unchanged Change Status, and Run outcome BLOCKED.

## Failure behavior

Follow docs/failure-handling.md. A failure in one repository may allow independent repositories to continue, but the report must be PARTIAL. A commit mismatch, missing required context, unresolved conflict, or sensitive-data exposure blocks the affected scope. Do not summarize only README and call it complete.

## Prohibited shortcuts

- Do not equate one repository with one process.
- Do not infer platform support from names, directories, macros, or build targets.
- Do not infer runtime relationships from CMake.
- Do not invent startup order, IPC semantics, permission behavior, or suspend/resume support.
- Do not copy secrets into Wiki pages or evidence excerpts.
- Do not overwrite human-authored content or self-approve the candidate.
