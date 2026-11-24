# Publication Plan Template

Store this immutable YAML as `publication-plan.yaml` in the binding bundle and bind its digest before approval. It describes permitted effects, not human authorization. Follow docs/publication-recovery.md. Render narrative values in Simplified Chinese by default.

```yaml
schema_version: 1
plan_id: <stable-plan-id>
change_id: <change-id>
target:
  repository_id: <wiki-repository-id>
  branch: <exact-target-branch>
  expected_commit: <full-pre-publication-commit>
transitions:
  - path: wiki/processes/<process-id>/overview.md
    selector: frontmatter.content_status
    before: candidate
    after: accepted
  - path: wiki/_meta/changes/<change-id>/change-set.yaml
    selector: status
    before: <actual-frozen-change-status>
    after: published
  - path: wiki/_meta/changes/<change-id>/change-set.yaml
    selector: publication.published_commit
    before: null
    after_from: observed_content_commit
index_transitions:
  - path: wiki/index.md
    page_id: <page-id>
    before_content_status: candidate
    after_content_status: accepted
    before_change_status: <actual-frozen-change-status>
    after_change_status: published
    move_to: accepted-and-published # existing section; preserve link, scope, summary bytes
artifacts:
  - role: human_decision # lint_report | independent_review | human_decision | immutable_payload
    record_id: <preallocated-record-id>
    registry_path: <immutable-approval-or-report-relative-path>
    sha256: null # fixed digest if already written; otherwise resolved by publication authorization
    destination_path: <exact-wiki-archive-path>
```

Enumerate every additional required field transition, record-reference insertion, and artifact copy. An omitted path/field is not authorized by this template. For `publication_record_ref`, bind a stable locator allocated before side effects; `after_from` may resolve only `observed_content_commit` or named prebound IDs/locators. No arbitrary executable expressions or broad path wildcards. Index transitions preserve summaries and unrelated rows. Record any expected missing destination as such; conflicting existing bytes stop the operation.

Gate/approval artifacts created after candidate freeze are stored outside it. The plan may declare their exact destination and bound role/ID before bytes exist; resolve their digests in the separate immutable publication authorization record before publication. A null digest is permitted only for the declared lint_report, independent_review, or human_decision role, never for immutable_payload. Never use this provision for page bodies, claims, evidence, arbitrary file additions, the authorization's own digest, or mutable progress. Those later execution records remain external and may be mirrored in a subsequent audit operation. A changed destination/role or knowledge scope needs renewed review/approval.
