# Publication Progress Record

Mutable execution metadata outside the candidate, stored at `publications/<publication-id>/progress.yaml` in the durable registry. Persist before side effects and update atomically. It does not add a canonical workflow status. Follow docs/publication-recovery.md; never treat booleans or a prior command response as proof without inspecting Git/artifacts.

```yaml
schema_version: 1
publication_id: <stable-publication-id>
change_id: <change-id>
snapshot_binding_ref:
  registry_id: <registry-id>
  binding_id: <binding-id>
  record_path: bindings/<binding-id>/binding.yaml
snapshot_binding_sha256: <expected-binding-bytes-digest>
plan_ref: <binding-bundle-relative-plan-path>
plan_sha256: <expected-plan-bytes-digest>
human_decision_ref: <registry-relative-immutable-decision-path>
human_decision_sha256: <decision-bytes-digest>
publication_authorization_ref: <registry-relative-authorization-path>
publication_authorization_sha256: <authorization-bytes-digest>
target:
  repository_id: <wiki-repository-id>
  branch: <target-branch>
  expected_start_commit: <full-commit-sha>
prepared_content_commit: null
observed_content_commit: null
prepared_finalization_commit: null
observed_finalization_commit: null
last_verified_target_commit: null
event_id: <publication-id>.publish
event_ref: publications/<publication-id>/publish-event.yaml
event_written: false
completed: false
attempt_report_refs: []
updated_at: <ISO-8601-with-timezone>
```

The reference stored in the Change Set and supplied to resumed sessions is:

```yaml
publication_record_ref:
  registry_id: <registry-id>
  publication_id: <publication-id>
  record_path: publications/<publication-id>/progress.yaml
```

Authorize and check a concrete target and binding, not a branch name alone. `completed` becomes true only after target verification and the unique event write. Missing/altered records, revoked authorization, divergent target, or unplanned knowledge differences stop recovery. Repeated successful resume returns the recorded result without new commits/events. Keep preallocated IDs and verified observations across attempts.

## Separate immutable publication authorization

Record an actual human authorization without modifying the already bound Human Decision. This record's exact bytes are hashed in progress, not inside itself. The same human instruction may approve knowledge and authorize publication; preserve its actual scope rather than asking again.

```yaml
schema_version: 1
authorization_id: <authorization-id>
change_id: <change-id>
human_authorizer: <authorized-human>
authorized_at: <actual-ISO-8601-timestamp>
human_decision_ref: <registry-relative-decision-path>
human_decision_sha256: <decision-digest>
snapshot_binding_ref:
  registry_id: <registry-id>
  binding_id: <binding-id>
  record_path: bindings/<binding-id>/binding.yaml
snapshot_binding_sha256: <binding-digest>
plan_sha256: <reviewed-plan-digest>
target:
  repository_id: <wiki-repository-id>
  branch: <target-branch>
  expected_commit: <approved-target-base>
resolved_artifacts:
  - record_id: <preallocated-plan-artifact-id>
    sha256: <actual-immutable-record-bytes-digest>
constraints: [] # actual human constraints only; do not invent expiry or approval
```

Resolve every deferred artifact from the plan by exact ID/path/role; reject missing, duplicated, or extra entries. This authorization record and mutable progress are not copied by a plan that would need their own digest, avoiding a self-reference cycle.
