# Wiki Schema

## 1. Design principles

- Process is the primary knowledge entity; System is the cross-process synthesis layer.
- Repository is a source container, not a synonym for Process.
- Repository ↔ Process is many-to-many.
- Process ↔ Platform Profile applicability is recorded independently from Repository inventory.
- Claims are atomic and mapped to exact evidence records.
- Page-Source Map supports reverse impact analysis for incremental updates.
- Claim truth status, Evidence status, Page content status, Change approval status, and Publication status are separate domains.
- Unknown, inferred, stale, and contradicted information remains explicit.
- Human edits and accepted history are preserved.

## 2. Entities

| Entity | Stable identity | Purpose |
|---|---|---|
| System | system_id | Complete software system assembled from repositories/processes |
| Repository | repository_id | Git repository and pinned source revision |
| Process | process_id | Independent process/service and its responsibility boundary |
| Interface | interface_id | Contract between processes or with an external system |
| Workflow | workflow_id | Multi-step or lifecycle behavior |
| Platform Profile | profile_id | Atomic OS/deployment scope |
| Architecture Decision | adr_id | Recorded architecture or engineering decision |
| Claim | claim_id | Atomic factual statement with scope and evidence |
| Evidence | evidence_id | Exact source locator at a pinned revision |
| Change Set | change_id | Proposed set of Wiki changes moving through quality gates |
| Review Report | review_id | Lint or independent LLM review result |
| Human Decision | human_decision_id | Immutable human approval/change-request/rejection record |
| Page-Source Map Entry | page_id | Reverse mapping from Wiki page to claims and source revisions |

## 3. Repository / Process / Profile mapping

Do not represent all applicability using a Repository-level profile list.

### Repository-to-Process mapping

Each mapping records repository_id, process_id, status (confirmed / candidate / unknown / rejected), evidence_refs, responsibility_note, and confirmed_by/confirmed_at when human-confirmed.

### Process-to-Profile mapping

Each mapping records process_id, profile_id, support_status (supported_verified / present_unverified / unsupported_verified / unknown), evidence_refs, and constraints.

A repository can implement several processes with different profile support. A process can span repositories. Repository-level profile observations are inventory hints, not proof that every process in the repository supports that profile.

## 4. Relationship semantics

Use explicit relationship types:
- implements: Repository implements Process.
- build_depends_on: build target depends on another target/library.
- runtime_depends_on: process requires another process/service at runtime.
- communicates_with: processes exchange information through an identified interface.
- starts_before: startup ordering is explicitly configured or evidenced.
- provides_interface / consumes_interface: interface roles.
- runs_on: Process is supported by a Platform Profile.

Every relationship record includes relationship_id, from_id, relationship_type, to_id, profile_ids, evidence_refs, status, constraints, and notes. Never infer one relationship type from another. A CMake target edge is build_depends_on only.

## 5. Page organization

The destination repository root also contains `AGENTS.md`, the Wiki-local maintenance entry point. Its paths and package provenance follow docs/wiki-maintenance.md.

    wiki/
      index.md
      log.md
      system/
      processes/<process-id>/
        overview.md
        common/
        profiles/<profile-id>/
      repositories/
      interfaces/
      workflows/
      platform-profiles/
      decisions/

Only create profile pages for confirmed/in-scope profiles. Do not create empty pages for unsupported combinations. The common directory is only for claims supported across every applicable profile.

## 6. Page metadata

Every substantive page begins with metadata equivalent to the following. Root AGENTS.md, wiki/index.md, and wiki/log.md are administrative files exempt from knowledge-page metadata and Claim/Evidence mapping; validate them under docs/wiki-maintenance.md.

    ---
    id: process.telemetry.overview
    title: 遥测进程概览
    type: process
    process_id: telemetry
    profile_ids: [qnx, android]
    content_status: candidate
    change_id: change-2026-001
    source_manifest_version: 1
    source_revisions:
      - repository_id: telemetry-repo
        commit: <full-40-character-commit-sha>
    claim_ids:
      - telemetry.responsibility.001
    last_reviewed: null
    ---

Use stable IDs. `content_status` is candidate / accepted / stale / superseded. Change Set status is tracked separately. Keep machine-readable keys, IDs, profile IDs, relationship types, and status enums in canonical English. Human-readable titles and descriptions use Simplified Chinese by default.

## 7. Claim representation

For each material statement record:
- claim_id;
- atomic statement;
- scope_type and scope_id;
- profile_ids;
- status: verified / inferred / unknown / stale / contradicted;
- evidence_refs with supports / contradicts / qualifies relation;
- reasoning and assumptions for inferred claims;
- limitations and last_verified_at.

A page-level source list does not replace Claim-Evidence mapping. See docs/claim-evidence-model.md and references/claim-template.md.

## 8. Evidence reference

Each evidence record identifies repository_id, full commit SHA, repository-relative path, locator type/value, profile scope, evidence type, evidence status, and checked timestamp. Excerpts are optional and must be redacted if sensitive.

See docs/source-evidence.md and docs/claim-evidence-model.md.

## 9. Page-Source Map

Every substantive page is mapped to:
- page_id and path;
- claim_ids;
- source repository IDs, full commit SHAs, relevant paths, and evidence IDs;
- dependent page IDs;
- last reviewed change and Wiki commit.

This reverse index is required for reliable incremental updates. See references/page-source-map-template.md.

## 10. Canonical metadata storage

Use the following default layout in the Engineering Wiki repository:

    wiki/
      index.md
      log.md
      _meta/
        source-manifest.yaml
        page-source-map.yaml
        claims/<claim-id>.yaml
        evidence/<evidence-id>.yaml
        changes/<change-id>/
          change-set.yaml
          init-report.md
          ingestion-report.md
          integration-report.md
          update-report.md
          query-capture.md
          lint-report.md
          independent-review.md
          human-review-summary.md
          human-decision.md
      system/
      processes/
      repositories/
      interfaces/
      workflows/
      platform-profiles/
      decisions/

Keep human-readable knowledge pages under their entity directories. Keep machine-readable provenance and workflow records under `wiki/_meta/`. Store only the reports applicable to a change. This layout is the v0.1.0 default; a different layout requires an explicit schema decision and corresponding template updates.

## 11. State domains

Keep these independent:
- Claim status: verified / inferred / unknown / stale / contradicted.
- Evidence status: valid / unverified / stale / inaccessible / conflicting / redacted.
- Page content status: candidate / accepted / stale / superseded.
- Change status: draft / lint_failed / pending_llm_review / llm_changes_requested / pending_human_review / human_changes_requested / approved / approval_stale / published / rejected / superseded.
- Review execution status: NOT_RUN / RUNNING / COMPLETED / INVALID.
- LLM review decision: PASS / REVISE / REJECT (only for a valid COMPLETED review; otherwise null).
- Human decision: approve / request_changes / reject.
- Run outcome: PASS / PARTIAL / BLOCKED / FAIL (execution-level; BLOCKED is not a Change status).

See docs/state-machine.md for transition rules and invariants.

## 12. Cross-profile rules

- A profile-specific claim must name its profile.
- A common claim must be supported in every applicable profile.
- If behavior differs, record the difference instead of forcing a common statement.
- If a profile has not been inspected, its behavior is unknown.
- Do not create profiles outside qnx, android, linux-tbox without an explicit project decision.

## 13. Change and approval metadata

Each candidate Change Set records change_id, base_wiki_commit, candidate_wiki_commit or diff_digest, changed pages/claims, source manifest version/digest, relevant source revisions, Lint report, independent Review report, current change status, review_execution_status, review_decision (null unless a valid review completed), review_invocation_id when available, run_outcome, and human_decision_id. `BLOCKED` belongs only to run_outcome; it MUST NOT be written to the Change Set `status` field.

New records also identify `origin` (init / ingest / integrate / source_update / query_capture / maintenance), `changed_artifact_paths` for administrative changes, and `query_capture_path` when applicable. These describe scope and provenance, not new states. Legacy records may omit them; preserve history and identify the origin from inspected reports only when needed. Administrative edits remain in the actual candidate diff even though they have no page/Claim IDs.

`snapshot_binding_ref` may locate an immutable external candidate binding record. Resolve its base/candidate revision or complete patch digest, manifest digest, scope, and source revisions before gate decisions; null inline self-referential fields are not missing evidence when the external binding is valid. Storage, live progress, and publication finalization follow docs/human-review.md sections 4 and 7.

Human approval binds to the exact candidate snapshot. Any material change invalidates the approval. See docs/human-review.md and references/human-decision-template.md.
