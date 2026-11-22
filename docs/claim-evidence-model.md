# Claim, Evidence, and Page-Source Mapping

## 1. Purpose

This document defines the traceability model connecting a human-readable Wiki statement to the exact source revision and locator that supports it. A page-level bibliography alone is insufficient: material claims MUST map to specific evidence records.

## 2. Canonical storage

For v0.1.0, store:
- Source Manifest at `wiki/_meta/source-manifest.yaml`;
- each Claim at `wiki/_meta/claims/<claim-id>.yaml`;
- each Evidence record at `wiki/_meta/evidence/<evidence-id>.yaml`;
- Page-Source Map at `wiki/_meta/page-source-map.yaml`;
- Change Set and run reports under `wiki/_meta/changes/<change-id>/`.

Human-readable Wiki pages reference stable Claim IDs in frontmatter or inline metadata. Do not duplicate the full Claim/Evidence record into multiple pages; link to the canonical record.\n\nFor approval binding, compute `source_manifest_digest` as SHA-256 over the exact UTF-8 bytes (LF line endings) of the committed `wiki/_meta/source-manifest.yaml`. Compute `diff_digest` as SHA-256 over the exact patch bytes for the recorded base/candidate Wiki commits. Store both digests in the Change Set and Human Decision record; do not embed a self-referential digest inside the manifest.

## 3. Claim

A Claim is one atomic, reviewable statement. Split a paragraph when it contains independently verifiable facts.

Required fields:

| Field | Required | Meaning |
|---|---|---|
| `claim_id` | yes | Stable ID, unique within the Wiki |
| `statement` | yes | One factual statement, in Simplified Chinese by default |
| `scope_type` | yes | `system`, `repository`, `process`, `interface`, `workflow`, or `profile` |
| `scope_id` | yes | Stable ID of the scoped entity |
| `profile_ids` | yes | Explicit profile scope; use an empty list only for genuinely platform-neutral claims |
| `status` | yes | Claim status from docs/state-machine.md |
| `evidence_refs` | yes | One or more evidence IDs; empty only when status is unknown |
| `reasoning` | conditional | Required for inferred claims |
| `limitations` | conditional | Required when evidence is partial, indirect, or bounded |
| `last_verified_at` | recommended | Timestamp of the most recent evidence validation |

Claim IDs MUST remain stable when wording is refined. Create a new ID when the underlying fact or scope changes materially.

## 4. Evidence record

Required fields:

| Field | Required | Meaning |
|---|---|---|
| `evidence_id` | yes | Stable evidence identifier |
| `repository_id` | yes | Repository ID from Source Manifest |
| `commit` | yes | Full 40-character commit SHA |
| `path` | yes | Repository-relative path |
| `locator_type` | yes | `line_range`, `symbol`, `config_key`, `document_heading`, or `artifact` |
| `locator` | yes | Exact line range, symbol, key, heading, or artifact locator |
| `evidence_type` | yes | `implementation`, `declaration`, `configuration`, `build_graph`, `documentation`, `test`, or `history` |
| `profile_ids` | yes | Profiles for which the evidence was inspected |
| `status` | yes | Evidence status from docs/state-machine.md |
| `checked_at` | yes | When the locator was last resolved |
| `excerpt` | optional | Short supporting excerpt; omit or redact sensitive content |

An evidence-to-claim link MUST also state its role: `supports`, `contradicts`, or `qualifies`.

## 5. Claim-to-evidence rules

- The evidence must support the exact wording, not merely the general topic.
- Behavior claims should prefer implementation, configuration, and tests over comments or README text.
- A declaration proves that an interface is declared, not that it is invoked at runtime.
- A CMake DOT edge proves a configured build-target dependency only.
- Runtime dependency, IPC, and startup-order claims need evidence appropriate to those relationships.
- Profile-specific claims must be supported by evidence inspected for that profile.
- A common claim must be supported across every profile declared applicable to that claim.
- Negative claims require a bounded search scope and method. Prefer "No handler was found in the inspected paths at commit X" over a system-wide assertion.
- Inferred claims must expose the reasoning chain and assumptions.
- Unknown claims must identify the missing evidence or unresolved question.
- Do not copy secrets, tokens, private keys, personal data, or sensitive payloads into evidence excerpts. Preserve the locator and mark the evidence redacted where necessary.

## 6. Repository / Process / Profile mapping

Do not store platform applicability only at Repository level. A repository may contain multiple processes with different platform support.

Represent these separately:

1. Repository-to-Process mapping: `repository_id`, `process_id`, mapping status, evidence refs, notes.
2. Process-to-Profile mapping: `process_id`, `profile_id`, support status, evidence refs, notes.
3. Repository-to-Profile observation: optional inventory metadata; it does not by itself prove that every process in the repository supports that profile.

Mapping statuses:

- `confirmed`: direct evidence or explicit project-owner confirmation.
- `candidate`: plausible mapping awaiting confirmation.
- `unknown`: insufficient evidence.
- `rejected`: investigated and not applicable, with reason/evidence.

Process profile support statuses:

- `supported_verified`
- `present_unverified`
- `unsupported_verified`
- `unknown`

Never infer Process support from a repository name, folder, macro, or build option alone.

## 7. Page-source map

The Page-Source Map is the reverse index used by incremental update. It maps each Wiki page to the claims it contains, source repositories/revisions/paths, and dependent pages.

Required fields per page:

- `page_id`, `path`, `page_type`;
- `claim_ids`;
- `source_refs` containing repository ID, full commit SHA, and relevant paths/evidence IDs;
- `depends_on_pages`;
- `last_reviewed_change_id`;
- `content_status`.

A page-source map entry MUST be updated only after its page and cited sources have actually been inspected. It is not enough to update all commits globally.

## 8. Incremental invalidation

When a source repository changes:

1. Compare full old/new commit SHAs.
2. Identify changed paths.
3. Find evidence records and claims referencing those paths.
4. Mark affected evidence stale and affected claims stale until revalidated.
5. Traverse Page-Source Map dependencies to identify affected Interface, Workflow, and System pages.
6. Reinspect the changed source and surrounding context.
7. Revalidate both ends of affected interfaces and relationships where possible.
8. Update only affected pages; preserve unrelated human edits.
9. Rerun Lint and independent Review for the impact scope.
10. Require a new human decision for the new candidate snapshot.

If changed paths cannot be mapped reliably, mark the impact scope unknown and broaden review conservatively.

## 9. Example

```yaml
claims:
  - claim_id: process.telemetry.startup.qnx.001
    statement: "该进程在 QNX Profile 下由指定启动配置拉起。"
    scope_type: process
    scope_id: telemetry
    profile_ids: [qnx]
    status: verified
    evidence_refs:
      - evidence_id: ev.telemetry.init.001
        relation: supports
    limitations: "仅适用于记录的 QNX source revision。"

evidence:
  - evidence_id: ev.telemetry.init.001
    repository_id: telemetry-repo
    commit: "<40-character-full-commit-sha>"
    path: "etc/service.conf"
    locator_type: line_range
    locator: "12-24"
    evidence_type: configuration
    profile_ids: [qnx]
    status: valid
    checked_at: "YYYY-MM-DDThh:mm:ssZ"
```

The values above are illustrative placeholders, not claims about a real project.
