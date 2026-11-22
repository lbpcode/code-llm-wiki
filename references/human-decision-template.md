# Human Review Decision Record

```yaml
human_decision_id: <stable-decision-id>
change_id: <candidate-change-id>
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
```

## Decision rules

- `approve` requires review of the exact diff and all required gate reports.
- `request_changes` requires actionable findings and returns the candidate to draft after acknowledgement.
- `reject` is terminal for this change ID; preserve the record and create a linked new ID for a new attempt.
- Waivers cannot override fabricated evidence, BLOCKER findings, or mandatory checks that did not run.
- Approval is invalid if its bound candidate, relevant source snapshot, or review scope changes.
- Publication is a separate explicit action and must record the resulting commit.
