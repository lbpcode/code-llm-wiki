# Ingestion Checkpoint Template

The Checkpoint is the authoritative, compact execution-state index. Keep detailed findings in Task Reports, session handoff details in Handoff Notes, and task-specific loading instructions in Context Packs. Do not duplicate full analysis text here.

```yaml
checkpoint_version: 2
run_id: ""
change_id: ""
updated_at: ""
wiki_base_commit: ""
analysis_plan_path: "wiki/_meta/changes/<change-id>/ingestion/analysis-plan.md"

source_revisions:
  <repository_id>: "<full-40-character-commit-sha>"

run_status: in_progress # in_progress / partial / blocked / completed

session:
  current_session_id: "session-0001"
  sequence: 1
  status: active # active / handed_off / completed
  previous_session_id: null
  started_at: null
  updated_at: null
  last_handoff:
    from_session_id: null
    to_session_id: null
    reason: null # planned_boundary / context_pressure / interruption / user_requested / phase_boundary
    handoff_note_path: null
    context_pack_path: null

current_task:
  task_id: null
  report_path: null
  last_persisted_unit_id: null
  resume_cursor: null

tasks:
  - task_id: ""
    execution_status: pending # pending / in_progress / completed / blocked
    coverage_status: not_started # not_started / partial / complete
    report_path: null
    last_persisted_unit_id: null
    updated_at: null

last_completed_task_id: null
next_task_ids: []
blocking_gaps: []

resume:
  verify_source_revisions: true
  verify_wiki_base_commit: true
  context_pack_path: null
  handoff_note_path: null
  next_action: ""
```

## Update rules

- Update after every meaningful logical analysis unit, every completed task, every partial/blocked transition, and every Session Handoff.
- Persist the corresponding Task Report before updating the Checkpoint's `last_persisted_unit_id` or `report_path`.
- For a handoff, write the next Context Pack and Handoff Note before updating the Checkpoint to `session.status=handed_off`. The Checkpoint must never point to missing artifacts.
- On a fresh Session resume, increment `sequence`, set `current_session_id` to the next run-local ID, set `previous_session_id` to the handed-off Session, set status to `active`, and preserve `last_handoff` for traceability.
- Do not increment the Session sequence when continuing in the same model context.
- If interrupted mid-task, set coverage to `partial`; use execution status `blocked` unless the task can safely resume directly from its persisted cursor.
- Never mark a task completed because the model conversation ended, a Session was handed off, or a summary was generated.
- On resume, verify pinned source commits and the expected Wiki candidate/base before trusting prior results.
- If a source revision changed, mark affected reports and their Claims/Evidence stale until revalidated.
- If a report, Context Pack, or Handoff Note is missing or inconsistent, reconstruct only the affected artifact from durable reports and source revisions; do not assume success.
- Version 1 Checkpoints remain readable. Preserve all existing task/run fields, initialize Session metadata for the currently active context, and upgrade to version 2 without rerunning completed tasks.
