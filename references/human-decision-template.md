# Human Review Decision Record

```yaml
human_decision_id: <stable-decision-id>
change_id: <candidate-change-id>
snapshot_binding_ref:
  registry_id: <registry-id>
  binding_id: <binding-id>
  record_path: bindings/<binding-id>/binding.yaml
snapshot_binding_sha256: <verified-binding-record-digest>
decision: approve # approve | request_changes | reject
reviewer: <authorized-human-identity>
timestamp: <ISO-8601-timestamp>
base_wiki_commit: <full-commit-sha>
candidate_wiki_commit: <full-commit-sha-or-null>
diff_digest: <digest-of-exact-diff>
changed_page_ids:
  - <page-id>
source_manifest_version: <version>
source_manifest_digest: <digest>
source_revisions:
  - repository_id: <repository-id>
    commit: <full-40-character-commit-sha>
lint_report_id: <report-id>
review_report_id: <report-id>
comments: "<decision rationale>"
requested_changes: []
waivers:
  - finding_id: <finding-id>
    reason: "<explicit rationale>"
    scope: "<bounded scope>"
    revalidation_condition: "<when this waiver must be revisited>"
publication:
  authorized: false
  published_commit: null
  timestamp: null
  authorization_ref: null # separate immutable authorization matching the reviewed plan and target
```

## Decision rules

- `approve` requires review of the exact diff and all required gate reports.
- `request_changes` requires actionable findings and returns the candidate to draft after acknowledgement.
- `reject` is terminal for this change ID; preserve the record and create a linked new ID for a new attempt.
- Waivers cannot override fabricated evidence, BLOCKER findings, or mandatory checks that did not run.
- Approval is invalid if its bound candidate, relevant source snapshot, or review scope changes.
- Publication is a separate explicit action and must record the resulting commit.
- Verify the binding under docs/snapshot-binding.md and match the same reference/digest in the Review report. Publication authorization and progress follow docs/publication-recovery.md and references/publication-progress-template.md; they must not introduce self-digests into this decision record.
