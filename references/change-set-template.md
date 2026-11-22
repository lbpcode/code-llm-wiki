# Change Set Record Template

A Change Set groups one proposed Wiki update through Lint, independent Review, human decision, and publication. Keep each attempt immutable once rejected or published.

```yaml
change_id: <stable-change-id>
purpose: "<bounded change description>"
status: draft # canonical Change Set status from docs/state-machine.md; never use BLOCKED here
run_outcome: null # PASS | PARTIAL | BLOCKED | FAIL; execution-level, not Change Set status
review_execution_status: NOT_RUN # NOT_RUN | RUNNING | COMPLETED | INVALID
review_decision: null # PASS | REVISE | REJECT; null unless a valid review is COMPLETED
review_invocation_id: null # host-provided Subagent run ID, when available
created_at: <ISO-8601-timestamp>
updated_at: <ISO-8601-timestamp>
base_wiki_commit: <full-commit-sha>
candidate_wiki_commit: null
diff_digest: <digest-or-null>
changed_pages:
  - page_id: <page-id>
    path: wiki/processes/<process-id>/overview.md
changed_claim_ids:
  - <claim-id>
source_manifest:
  version: 1
  digest: <manifest-digest>
relevant_source_revisions:
  - repository_id: <repository-id>
    commit: <full-40-character-commit-sha>
impact:
  dependent_pages:
    - <page-id>
  impact_assessment: "<bounded impact summary>"
reports:
  init_report_id: null
  ingestion_report_ids: []
  integration_report_ids: []
  update_report_id: null
  lint_report_id: null
  review_report_id: null
human_decision_id: null
publication:
  authorized: false
  published_commit: null
  published_at: null
supersedes_change_id: null
```

## Rules

- Create a new Change Set for each materially new candidate attempt.
- Keep rejected Change Sets immutable; a retry gets a new ID and links to the rejected predecessor.
- Bind human approval to candidate/base revisions, diff digest, changed pages, Source Manifest, relevant source commits, and gate report IDs.
- `BLOCKED` is valid only for `run_outcome`; never write it to `status`, `review_execution_status`, or `review_decision`.
- If review cannot execute after Lint PASS, keep `status: pending_llm_review`, set `review_execution_status: NOT_RUN` (or `INVALID` for an invalid returned report), leave `review_decision: null`, and set `run_outcome: BLOCKED`.
- Any material post-approval change sets status to approval_stale.
- Do not set publication.authorized or published_commit until a human explicitly authorizes the publication action.
- A candidate is not accepted knowledge until publication is recorded.
