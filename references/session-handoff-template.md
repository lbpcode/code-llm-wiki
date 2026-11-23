# Session Handoff Template

A Handoff Note is a concise navigation record for a fresh Session. The Checkpoint is authoritative for execution state; Task Reports are authoritative for findings; the Context Pack defines what the next Session should load.

## Handoff metadata

- Run ID:
- Change ID:
- Current Session ID:
- Next Session ID:
- Handoff reason: planned_boundary / context_pressure / interruption / user_requested / phase_boundary
- Handoff timestamp:
- Checkpoint path:
- Next Context Pack path:

## Durable state summary

- Source repository IDs and full pinned commits:
- Wiki base commit:
- Last completed task:
- Current task ID:
- Current task execution status:
- Current task coverage status:
- Last persisted logical unit ID:
- Resume cursor:
- Completed task IDs:
- Pending / blocked task IDs:
- Blocking gaps:

Keep this summary concise. Do not duplicate Task Report findings or Evidence excerpts.

## Exact next action

Describe one concrete action for the next Session, including the task ID and the first artifact/source locator to inspect.

## Resume instruction

Copy this resume instruction into a genuinely fresh conversation:

> Resume Code LLM Wiki Ingest from the Checkpoint at `<checkpoint path>` and Context Pack at `<next context pack path>`. Verify the Source Manifest, pinned source commits, and Wiki base/candidate revision, then continue from the recorded resume cursor without redoing completed work.

In the new model context:
1. read the Checkpoint at the path above;
2. read this Handoff Note and the referenced Context Pack;
3. verify the Source Manifest, pinned source commits, and Wiki base/candidate revision;
4. load only the artifacts and source locators listed in the Context Pack;
5. continue from the recorded resume cursor.

Do not resume from the previous chat transcript. Do not claim a fresh Session if the host kept the same model context.

## Completion and limitations

- Persisted outputs:
- Unpersisted work (must be empty; otherwise describe as unknown/partial):
- Known limitations:
- Handoff committed to Checkpoint: yes / no

The current Session must stop after the handoff is committed. If the host cannot create a new conversation automatically, ask the user to open one and provide the resume instruction above. This Ingest handoff is not a manual-session fallback for independent Review.
