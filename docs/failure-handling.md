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
| Sensitive information detected | Redact content; evidence may be `redacted`; stop copying affected excerpt | Never write credentials, tokens, private keys, or sensitive payloads into Wiki/reports | Report locator and redaction reason without exposing value; follow project secret-handling procedure |

## 4. Quality gates and review

| Scenario / trigger | State and allowed behavior | Prohibited behavior | Output and recovery |
|---|---|---|---|
| Lint finds blocking structural/provenance errors | Change `lint_failed`; fix and rerun | Do not invoke human approval as a bypass | Lint findings with exact paths/locations; return to draft |
| Lint cannot execute a required check | Result `PARTIAL` / check `NOT RUN`; candidate remains blocked | Do not convert unavailable checks to PASS | Record capability limitation; restore capability or obtain an explicit scope decision if the check is truly out of scope |
| Host lacks native Subagent delegation / isolation cannot be proven | Review `NOT RUN`; Change Set remains `BLOCKED` | Do not ask the user to open a manual second session; do not fall back to same-context review | Report the missing host capability; enable native Subagent delegation before retrying |
| Subagent invocation fails, times out, or returns no completed report | Review `NOT RUN`; Change Set remains `BLOCKED` | Do not treat an accepted/running invocation as a completed review; do not use same-context fallback | Preserve invocation error/run ID; retry with a new isolated Subagent after the host issue is resolved |\n| Subagent report snapshot binding does not match candidate/source revisions | Reject report as invalid; Review `NOT RUN`; Change Set remains `BLOCKED` | Do not reuse report against another candidate or source snapshot | Rebuild immutable Review Package and launch a new Subagent invocation |\n| LLM Review returns REVISE | Change `llm_changes_requested` | Do not proceed to human approval | Preserve report; fix findings; rerun Lint and automatically delegate a new independent Review Subagent |
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

Use one overall run outcome:

- `PASS`: all required in-scope work and checks completed with no blocking findings.
- `PARTIAL`: some independent scopes or optional checks could not complete; limitations are explicit.
- `BLOCKED`: a required prerequisite or quality gate prevents safe continuation.
- `FAIL`: a required deterministic check found a violation that has not been corrected.

A PARTIAL or BLOCKED run cannot create accepted Wiki knowledge. A failed optional CMake DOT attempt alone does not make an otherwise complete ingestion fail.
