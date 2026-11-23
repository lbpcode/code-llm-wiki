# Analysis Task Template

Use one task per bounded engineering question or concern, not one task per file. Keep the objective narrow enough to complete and verify within a manageable context.

## Task definition

- Task ID:
- Objective:
- Repository IDs:
- Process ID:
- Platform Profile IDs:
- Pinned source revisions:
- Dependencies:
- In-scope questions:
- Explicit exclusions:
- Candidate input paths / symbols / configuration keys:
- Acceptance criteria:

## Execution

- Execution status: pending / in_progress / completed / blocked
- Coverage status: not_started / partial / complete
- Started / completed:
- Context handoff / Subagent invocation (if applicable):
- Tool/output limitations:

## Progress ledger

Record each meaningful logical analysis unit when its result and evidence have been persisted. Do not create one row per file or trivial tool call.

| Unit ID | Question / symbol / behavior traced | Status | Durable findings / Evidence IDs | Resume cursor |
|---|---|---|---|---|

Statuses are workflow metadata: not_started / partial / completed.

## Findings

| Claim ID / finding | Statement | Status | Evidence IDs | Limitations |
|---|---|---|---|---|

## Evidence inspected

| Evidence ID | Repository | Commit | Path | Locator | Evidence type | Role |
|---|---|---|---|---|---|---|

Use exact pinned revisions and resolvable locators. Do not invent line numbers or infer runtime behavior from declarations/build relationships alone.

## Coverage

- Questions answered:
- Questions partially answered:
- Questions not inspected:
- Profiles actually inspected:
- Relevant callers/callees or interface counterpart not inspected:
- Generated/vendor/test sources included or excluded and why:

## Unknowns and follow-up

| Unknown / conflict | Why unresolved | Required source or decision | Follow-up task ID |
|---|---|---|---|

## Handoff

- Durable output path:
- Checkpoint updated: yes / no
- Next task IDs:
- Resume instruction:
- Overall task conclusion:

A task report records only the declared scope. It must not claim that the whole Process or Repository is complete unless the plan's required coverage has been satisfied.
