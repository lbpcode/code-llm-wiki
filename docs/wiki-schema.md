# Wiki Schema

## 1. Design principles

- Process is the primary knowledge entity.
- System is the cross-process synthesis layer.
- Repository is a source container, not a synonym for Process.
- Platform Profile is an atomic OS/deployment scope.
- Claims must be traceable to a pinned source revision.
- Shared/common claims require evidence that supports every profile in their declared scope.
- Unknown, inferred, stale, and contradicted information must remain distinguishable.

## 2. Entities

| Entity | Required identity | Description |
|---|---|---|
| System | system_id | Complete software system |
| Repository | repository_id | Git repository and pinned revision |
| Process | process_id | Independent process/service |
| Interface | interface_id | Contract or communication boundary |
| Workflow | workflow_id | Multi-step or lifecycle behavior |
| Platform Profile | profile_id | Atomic OS/deployment configuration |
| Decision | decision_id | Recorded architecture or technical decision |
| Claim | claim_id | Atomic factual statement with evidence |

## 3. Relationships

A Repository can implement multiple Processes. A Process can span multiple Repositories. A Process can run on one or more explicitly declared Platform Profiles.

System relationships must distinguish build dependencies, runtime dependencies, communication relationships, startup ordering, and interface provision/consumption.

Never infer one relationship type from another.

## 4. Page organization

    wiki/
      index.md
      system/
      processes/
        <process-id>/
          overview.md
          common/
          profiles/
            <profile-id>/
      interfaces/
      workflows/
      platform-profiles/
      decisions/

The common directory is only for claims proven to apply across all profiles listed for that process. Otherwise, put the claim under a specific profile.

## 5. Page metadata

Every substantive page should begin with metadata equivalent to:

    ---
    id: process-a.lifecycle.qnx
    title: Process A lifecycle on QNX
    type: process-profile
    process_id: process-a
    profile_id: qnx
    status: draft
    source_revisions:
      - repository_id: process-a-repo
        commit: <full-commit-sha>
    last_reviewed: YYYY-MM-DD
    ---

Use stable IDs. Do not use branch names as source identity; record full commit SHAs.

## 6. Claim representation

For important claims, include:
- Claim ID.
- Statement.
- Scope: system, process, interface, workflow, or profile.
- Status: verified, inferred, unknown, stale, or contradicted.
- Evidence references.
- Assumptions and limitations, if any.

Keep claims atomic. A paragraph containing several independent facts should be split or have evidence mapped to each claim.

## 7. Evidence reference

A source reference must identify:
- repository_id;
- full commit SHA;
- repository-relative path;
- line range, symbol, configuration key, or document heading;
- profile scope;
- evidence type.

See docs/source-evidence.md.

## 8. Status semantics

| Status | Meaning |
|---|---|
| verified | Direct source evidence supports the claim |
| inferred | Explicit derivation from cited evidence |
| unknown | Insufficient evidence to decide |
| stale | Source revision changed and claim has not been revalidated |
| contradicted | Available evidence conflicts with the claim |

Do not convert inferred or unknown claims into verified claims through repeated summarization.

## 9. Cross-profile rules

- A profile-specific claim must name its profile.
- A common claim must be supported in every applicable profile.
- If behavior differs, record the difference instead of forcing a common statement.
- If a profile has not been inspected, its behavior is unknown, not identical.
- Do not create profiles outside the approved phase-one list without an explicit project decision.

## 10. Relationship record

A relationship should include from entity, relationship type, to entity, profile scope, evidence references, confidence/status, and constraints.

A build graph edge must be represented as build_depends_on, never runtime_depends_on.
