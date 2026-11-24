# Publication Progress and Safe Retry

Use after valid Lint, independent Review, and human approval of the exact snapshot and publication plan, with explicit authorization for the target repository/branch. This contract uses files and Git; it introduces no service or new Change/Publication status enums. Operational progress is separate from canonical knowledge state.

## 1. Durable plan and progress before side effects

Use references/publication-plan-template.md for the immutable plan included in the binding/review package. It names the target repository/branch, expected starting commit, exact paths/fields permitted to change, exact before/after values (or explicitly defined substitutions), and archives to copy by digest. A general "metadata files may change" allowance is insufficient.

Create external `publications/<publication-id>/progress.yaml` using references/publication-progress-template.md **before** changing the target. Record the Change ID, binding reference/digest, approval and authorization references/digests, plan reference/digest, target identity and expected commit, prepared/observed commit IDs, and a stable publication event ID. Authorization must name or unambiguously cover the target and operation; reusing the same valid authorization on retry does not require asking again. Changed/revoked authorization or an expired constraint blocks the affected action.

Use one publisher for the target and progress record. Persist checkpoints atomically; retain immutable attempt reports. If exclusive ownership cannot be established, stop instead of letting concurrent Agents overwrite progress. Commit/remote writes remain limited to the user's authorization.

Keep attempt reports in the publication's registry directory. Add existing report references to `attempt_report_refs` when next writing a progress checkpoint; do not list an unwritten report as completed. A completed operation's read-only retry may return a separate immutable attempt-report reference without rewriting the completed receipt.

## 2. Incorporate once, with a write-ahead commit identity

1. Verify the snapshot under docs/snapshot-binding.md, gate/approval/authorization records, target ref, and expected base. Prepare the exact content commit in isolation and save its SHA as `prepared_content_commit` before updating the target. For an existing candidate commit reuse its identity; for a patch, the prepared commit must reproduce the verified candidate tree. Do not include new knowledge or unrelated target changes.
2. Inspect the target's actual history. If it already contains the recorded prepared content commit, verify its tree/binding and record `observed_content_commit`; do not merge/apply it again. This covers a crash after target incorporation but before the checkpoint write.
3. Otherwise update the target only from the expected previous commit, using a compare-and-swap/local ref update or an equivalent checked, non-history-rewriting remote update. Record the observed commit after success. A failed command or lost response is not proof of failure: reread the target before retrying.

At this intermediate point the new pages remain candidate and the change is not published. Do not expose it as accepted knowledge simply because its commit is on the target branch.

## 3. Finalize only approved metadata, atomically

Build finalization from the verified content commit in isolation. Apply only the bound plan's exact transformations: page publication metadata; Change Set publication fields and record references; index placement/status without changing summaries; byte-for-byte copies of listed evidence/decision/report artifacts. Predetermined substitutions are limited to the observed content commit and the already bound IDs/record locators. Anything outside the allowlist, or different before-values, stops finalization for a new candidate/review.

Verify all non-allowlisted bytes/blobs are identical to the reviewed content, including page bodies, Claims/Evidence, source manifest/revisions, and index summary wording. Check page/change/index consistency and archival digests. Prepare one finalization commit containing all required metadata transitions and stable `publication_record_ref`; save its SHA in progress **before** updating the target. This avoids exposing partially updated page/change/index files on the target.

If the target already contains that prepared finalization commit, verify and record it instead of producing another commit. Otherwise advance from the recorded content commit with a checked update. An unexpected target change is not silently merged: stop, assess the new target/knowledge diff, and re-review where the approved binding or scope changed. Recovery must not rewrite target history.

Keep `completed: false` until the observed finalization commit and all planned transitions have been verified against the actual target. After successful verification, write the publication event once using its preallocated ID; an existing identical event is reused, while a conflicting event blocks completion. Store the observed finalization SHA/event reference and set `completed: true` **last**, atomically. A crash after the target update or event write is recovered by observing those artifacts, not repeating them. The progress record lives outside the finalization commit, so recording that commit's SHA creates no self-reference.

## 4. Resume and visibility

Every retry or new session loads progress from its stable registry-relative `publication_record_ref`, then revalidates binding, plan, human approval, authorization, target identity/history, and the current target's relevant content. Checkpoints guide inspection; Git and artifact bytes prove which actions completed. Missing/corrupt progress or conflicting prepared/observed SHAs blocks automatic retry; reconstruct only from verifiable records, never create a new publication ID to bypass uncertainty.

- If neither prepared commit is present, perform only the still-authorized missing action from its expected base.
- If the content commit is present but finalization is not, finish metadata only.
- If finalization is present but event/completion checkpoint is missing, verify it, append/reuse the one event, and complete the checkpoint only.
- If completion is recorded, verify the existing result and return it without new commits, events, or merges.

New publication records require Query to check `publication_record_ref`, matching binding, `completed: true`, and a verified observed finalization commit in the selected target history, in addition to accepted page/published change state. Until then, withhold this change's new knowledge and disclose incomplete publication; previously published unaffected knowledge remains queryable. A historical published Wiki revision is checked against its own bound receipt; unrelated later history is not proof that its completion failed. Legacy published changes without this reference retain their prior trust rules; do not fabricate retrospective receipts.

On a conflict, altered reviewed knowledge, mismatched plan/digest, missing authorization, or divergent target, stop with `run_outcome: BLOCKED`; keep the change unexposed, use `approval_stale` when the approval binding is invalid, and require a new reviewed candidate for knowledge/scope differences. Do not reinterpret these failures as permission to finish publication.

## 5. Retention

Keep the immutable binding/plan, approvals, reports, attempt records, progress and publication event in the durable registry. Archive completed records under a verified registry mirror using docs/snapshot-binding.md; preserve reference identities and original bytes. The Wiki may retain a reference to the external completion receipt instead of embedding a commit SHA into the same commit. Mirroring a completed receipt is a later authorized audit action, never a reason to repeat publication or change the frozen candidate.
