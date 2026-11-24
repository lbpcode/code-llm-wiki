# Wiki Operation Log Template

Create `wiki/log.md` with a short introduction explaining append-only operational history. Render prose in Simplified Chinese. Append one entry per observed operation outcome; do not populate fictional history at initialization.

```markdown
## [<ISO-8601 timestamp with timezone>] <operation> | <short description>

- Event ID: <unique-stable-event-id>
- Run / Change ID: <actual-ID-or-none>
- Outcome: <observed-run-outcome-and-specific-operation-result>
- Scope: <repository/process/profile/page-scope>
- Wiki snapshot: <actual-revision-or-uncommitted-worktree-identifier>
- Source revisions: <relevant-repository-IDs-and-full-commits-or-manifest-reference>
- Pages / reports: <relative-links-to-existing-artifacts-or-explicitly-not-persisted>
- Summary: <what-completed-what-remains-unknown-and-next-action>
- Corrects event: <prior-event-id-only-for-a-correction>
```

Operations: `init`, `ingest`, `integrate`, `query`, `capture`, `update`, `lint`, `review`, `publish`. Use actual outcomes: a returned answer is not proof of a published change, and a review launch is not a completed PASS.

Do not change old entries. Deduplicate an append by Event ID; append a correction rather than editing history. For deferred events retain the actual event timestamp and record when it was later persisted. If no authorized write location is available, return the event without claiming it is saved. Query logging and frozen-snapshot handling follow docs/wiki-maintenance.md.
