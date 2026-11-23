# Ingestion Checkpoint Template

The Checkpoint is a compact recovery index. Keep detailed findings in Task Reports and reference them here; do not duplicate full analysis text.

```yaml
checkpoint_version: 1
run_id: ""
change_id: ""
updated_at: ""
wiki_base_commit: ""
analysis_plan_path: "wiki/_meta/changes/<change-id>/ingestion/analysis-plan.md"

source_revisions:
  <repository_id>: "<full-40-character-commit-sha>"

run_status: in_progress # in_progress / partial / blocked / completed

tasks:
  - task_id: ""
    execution_status: pending # pending / in_progress / completed / blocked
    coverage_status: not_started # not_started / partial / complete
    report_path: null
    updated_at: null

last_completed_task_id: null
next_task_ids: []
blocking_gaps: []

resume:
  verify_source_revisions: true
  verify_wiki_base_commit: true
  load_completed_reports_by_reference: true
  next_action: ""
```

## Update rules

- Update after every completed task and before every context/session handoff.
- If interrupted mid-task, set coverage_status to partial. Use execution_status=blocked when work cannot safely continue now, or in_progress only when it remains safely resumable; record the next action in the Checkpoint.
- Never mark a task completed because the model conversation ended or because a summary was generated.
- On resume, verify pinned source commits and the expected Wiki candidate/base before trusting prior results.
- If a source revision changed, mark affected reports and their Claims/Evidence stale until revalidated.
- If a report is missing, incomplete, or inconsistent with the Checkpoint, reconstruct only the affected task; do not assume success.
