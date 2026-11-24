# Failure Handling and Recovery

## 1. General rule

A failure must be visible, scoped, and recoverable. Never silently skip a repository, evidence check, review gate, or human decision. Every failure report records the trigger, affected scope, state change, prohibited actions, user-visible output, and recovery path.

A failure in one independent repository may allow work on other repositories to continue, but it MUST NOT be hidden by an overall PASS. The run result is `PARTIAL` or `BLOCKED` when required coverage is incomplete.

## 2. Source inventory and mapping

| Scenario / trigger | State and allowed behavior | Prohibited behavior | Output and recovery |
|---|---|---|---|
| Submodule not initialized | Mark repository `inaccessible` / inventory `partial`; continue independent repositories | Do not infer its files, processes, or commits | Report path and expected pinned SHA; ask user to initialize or provide access |
| Repository inaccessible / permission denied | Mark affected repository blocked; retain known metadata only | Do not substitute a similarly named remote or another branch | Report exact repository/path and permission failure; retry only after access is restored |
| Checked-out commit differs from submodule pin | Mark source snapshot inconsistent; block ingestion for that repository | Do not silently analyze HEAD and claim it represents the pinned superproject revision | Report expected and actual full SHAs; user must restore pin or explicitly authorize a new snapshot |
| One repository contains multiple processes | Create separate candidate Process mappings | Do not equate repository = process | Record evidence for each mapping; request confirmation only for material ambiguity |
| One process spans repositories | Link all implementing repositories to one Process ID | Do not duplicate the process solely because it spans repositories | Record each repository's responsibility and evidence |
| Process boundary unclear | Keep mapping `candidate` or `unknown`; block unsupported integration edges | Do not invent process boundaries | Provide competing interpretations and evidence gaps for human confirmation |
| Profile evidence missing | Mark Process/Profile support `unknown` | Do not infer support from names, macros, directories, or build targets | Record which profile/source needs inspection |
| Only some profiles supported | Analyze confirmed profiles independently | Do not generalize one profile to others | Create pages only for confirmed/in-scope profiles; other profiles remain Unknown |

## 3. Evidence and generation

| Scenario / trigger | State and allowed behavior | Prohibited behavior | Output and recovery |
|---|---|---|---|
| Evidence locator does not resolve | Evidence `unverified` or `inaccessible`; claim cannot be verified | Do not fabricate line numbers or silently cite nearby code | Report repository, commit, path, locator; re-open exact pinned revision |
| Conflicting source evidence | Mark evidence `conflicting`; claim `contradicted` or `unknown` | Do not choose the more convenient source without rationale | List both sources, scope, revision, and unresolved interpretation; request engineering decision |
| Only one side of an interface is found | Mark interface/relationship candidate or unknown | Do not assert confirmed provider-consumer behavior or direction | Report inspected side and missing counterpart; inspect other repository/configuration |
| Relationship direction unclear | Keep relationship unverified | Do not reverse or infer direction from naming alone | Record candidate endpoints and required evidence |
| CMake configure unavailable/fails | Record DOT as unavailable with environment/error context; continue other analysis | Do not block unrelated ingestion or invent a graph | Report command/configuration/toolchain limitation; retry only with representative setup |
| Graphviz generation fails | Record failure; build-graph check NOT RUN | Do not infer target graph from incomplete logs | Report CMake configure status and Graphviz error; optional unless target dependency is essential to the task |
| Generation interrupted | Keep candidate `draft`; persist completed artifacts and run checkpoint | Do not mark partial pages accepted | Report completed/unfinished repositories and artifacts; resume from last verified checkpoint |
| Some repositories fail | Mark run `PARTIAL`; continue independent scopes | Do not claim complete System architecture | List successful, failed, skipped repositories; retry failed scopes |
| Sensitive information detected | Redact content; evidence may be redacted; stop copying affected excerpt | Never write credentials, tokens, private keys, or sensitive payloads into Wiki/reports | Report locator and redaction reason without exposing value; follow project secret-handling procedure |
| Context pressure approaches the host limit | Stop expanding scope; finish only a safely completable atomic task; persist its report and Checkpoint; continue in a fresh context when available | Do not rely on automatic compaction as lossless memory; do not keep loading unrelated files | Record the last completed task, current task status, source revisions, and next action; resume from the Checkpoint |
| Context is exhausted before a task completes | Set coverage_status=partial and execution_status=blocked (or in_progress only when safely resumable); preserve verified findings and unresolved questions | Do not mark the task or Process complete; do not reconstruct missing details from memory | Save a partial Task Report and Checkpoint; split remaining work into a focused follow-up task |
| Tool output is truncated or clipped | Mark the affected inspection incomplete and fetch the exact missing source range | Do not cite truncated output as complete evidence | Record the path/range and retry with smaller targeted reads; keep dependent claims unknown until resolved |
| An Analysis Task expands into multiple independent concerns | Stop scope expansion and create follow-up tasks with explicit objectives and dependencies | Do not keep broadening one task or create one task per source file | Update the Analysis Plan and Checkpoint; retain the original task's bounded coverage |
| Ingestion is interrupted or the session ends | Resume from durable Task Reports and Checkpoint after verifying source revisions and Wiki base | Do not assume an in-progress task completed; do not rerun all completed tasks by default | Reconstruct only missing/inconsistent task state; mark uncertain coverage partial |
| Host cannot create a fresh Session automatically | For sequential Ingest only, persist the Context Pack, Handoff Note, and Checkpoint; print a resume instruction and stop for the user to open a fresh conversation | Do not claim the context was reset; do not continue the same conversation as if it were a fresh Session; do not apply this as a Review fallback | Resume in the new conversation from the Context Pack and Checkpoint; independent Review still requires native isolated Subagent delegation |
| Handoff Note or Context Pack is missing / inconsistent | Treat the Checkpoint as authoritative; reconstruct only the missing artifact from Task Reports and pinned revisions | Do not trust a handoff summary that conflicts with the Checkpoint; do not mark unpersisted work complete | Rebuild the minimal Context Pack/Handoff Note, update the Checkpoint last, and resume from the last verified logical unit |
| Context Pack is too large or loads unrelated history | Reduce it to the active task, required instructions, selected prior report sections, and exact source locators | Do not solve a large pack by loading every Task Report or the full conversation transcript | Split the task or create a smaller pack; record excluded context and remaining coverage explicitly |
| Source revision changes during ingestion | Mark task reports and evidence tied to affected paths/revisions stale; revalidate before integration | Do not combine findings from mixed revisions as if they describe one snapshot | Refresh the Source Manifest under an authorized change, re-plan affected tasks, and record old/new full SHAs |

## 4. Quality gates and review

| Scenario / trigger | State and allowed behavior | Prohibited behavior | Output and recovery |
|---|---|---|---|
| Lint finds blocking structural/provenance errors | Change `lint_failed`; fix and rerun | Do not invoke human approval as a bypass | Lint findings with exact paths/locations; return to draft |
| Lint cannot execute a required check | Lint result `PARTIAL` / check `NOT RUN`; do not enter `pending_llm_review`; Change Status remains `draft` (or `lint_failed` if blocking findings exist); Run outcome `PARTIAL` or `BLOCKED` | Do not convert unavailable checks to PASS or write `BLOCKED` into Change Status | Record capability limitation; restore capability or obtain an explicit scope decision if the check is truly out of scope |
| Host lacks native Subagent delegation / isolation cannot be proven | Review execution status `NOT_RUN`; Review decision null; Change Status remains `pending_llm_review`; Run outcome `BLOCKED` | Do not write `BLOCKED` into Change Status; do not ask the user to open a manual second session or fall back to same-context review | Report the missing host capability; enable native Subagent delegation before retrying |
| Subagent invocation fails, times out, or returns no completed report | Review execution status `NOT_RUN`; Review decision null; Change Status remains `pending_llm_review`; Run outcome `BLOCKED` | Do not write `BLOCKED` into Change Status; do not treat an accepted/running invocation as a completed review or use same-context fallback | Preserve invocation error/run ID; retry with a new isolated Subagent after the host issue is resolved |
| Subagent report snapshot binding does not match candidate/source revisions | Review execution status `INVALID`; Review decision null; Change Status remains `pending_llm_review`; Run outcome `BLOCKED` | Do not write `BLOCKED` into Change Status or reuse the report against another candidate/source snapshot | Rebuild immutable Review Package and launch a new Subagent invocation |
| LLM Review returns REVISE | Change `llm_changes_requested` | Do not proceed to human approval | Preserve report; fix findings; rerun Lint and automatically delegate a new independent Review Subagent |
| LLM Review returns REJECT | Change `rejected` | Do not relabel the same candidate PASS | Preserve rejection report; a new attempt requires a new change ID |
| BLOCKER or MAJOR finding exists | PASS prohibited | Do not override with numeric score or waiver | Resolve finding or reject candidate |
| Human requests changes | Change `human_changes_requested`, then draft after acknowledgement | Do not publish or reuse prior approval | Record actionable requests; rerun affected gates and obtain a new decision |
| Human rejects | Change `rejected` (terminal) | Do not silently reopen or erase history | Preserve decision; create a new linked change ID for a materially new attempt |

## 5. Approval, update, and publication

| Scenario / trigger | State and allowed behavior | Prohibited behavior | Output and recovery |
|---|---|---|---|
| Wiki Diff changes after approval | Mark `approval_stale` | Do not reuse approval | Recompute diff digest; rerun affected gates and obtain new approval |
| Relevant source commit changes during review | Mark affected claims/evidence stale and approval stale if already granted | Do not publish against mixed source snapshots | Refresh manifest, revalidate affected claims, rerun gates |
| Unrelated source commit changes | Perform dependency-impact assessment | Do not invalidate or preserve approval without checking scope | Record proof of unaffected dependencies; otherwise invalidate conservatively |
| AI update conflicts with human edit | Pause affected page; report conflict | Do not overwrite or drop human text | Offer three-way merge proposal; human resolves; new diff must pass gates |
| Page deletion is proposed | Keep the current page accepted and represent the proposed deletion in a draft Change Set | Do not delete accepted knowledge automatically | Show references, dependent pages, source reason, and migration/redirect proposal for human decision |
| Process appears removed or renamed | Set lifecycle_status to deprecated_candidate pending human confirmation | Do not erase historical Process page or ID automatically | Confirm replacement/retirement with owner; only then set lifecycle_status to retired_confirmed, preserve the old Process ID, and link its successor |
| Evidence becomes stale | Mark evidence and dependent claims/pages stale | Do not present stale claims as current | Run impact analysis and revalidate |
| Query finds draft/unreviewed content | Exclude by default; optionally report a knowledge gap | Do not answer as accepted fact | Query only published knowledge by default; identify missing/unknown evidence |
| Query finds stale or contradicted claim | Exclude from unqualified factual answer; disclose status if useful | Do not silently use it as current verified knowledge | Cite the status and recommend revalidation |
| Publication action fails | Keep approved change unpublished; record failure | Do not claim published | Retry only after inspecting current branch and approval binding |
| Published content later found incorrect | Create corrective change or revert commit | Do not rewrite published history | Preserve audit chain and require normal quality/approval gates |

## 6. Run outcome

Binding and publication recovery failures follow docs/snapshot-binding.md and docs/publication-recovery.md. Missing/corrupt records or altered patches block automatic continuation; do not refresh expected hashes or reuse approval for a different snapshot. On interrupted publication, inspect prepared/observed commit IDs and the actual target before acting; reuse the original publication/event IDs, withhold incomplete new knowledge, and never repeat incorporation merely because the last command response/checkpoint is absent.

Maintenance-specific recovery follows docs/wiki-maintenance.md. A missing/incomplete index allows a disclosed read-only discovery fallback, but must be repaired before a new knowledge change passes required maintenance checks. Preserve existing AGENTS.md and log history on conflicts. If the full workflow package cannot be located, use the Wiki-local rules for read-only questions and report the missing dependency before knowledge mutation. If a log write is unauthorized or would alter a frozen snapshot, return/defer the event and report its persistence status; never fabricate a saved event or silently modify approved content.

Use one overall run outcome, stored separately from Change Set status:

- `PASS`: all required in-scope work and checks completed with no blocking findings.
- `PARTIAL`: some independent scopes or optional checks could not complete; limitations are explicit.
- `BLOCKED`: a required prerequisite or quality gate prevents safe continuation. The Change Set retains its current canonical status; for a post-Lint Review block this is `pending_llm_review`.
- `FAIL`: a required deterministic check found a violation that has not been corrected.

`BLOCKED` is not a Change Set status, Review execution status, or LLM review decision. A PARTIAL or BLOCKED run cannot create accepted Wiki knowledge. A failed optional CMake DOT attempt alone does not make an otherwise complete ingestion fail.
