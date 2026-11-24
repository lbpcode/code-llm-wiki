# Workflow and State Model

## 1. State domains are separate

The workflow MUST NOT use one status field to represent both the truth of a claim and the approval state of a Wiki change.

| State domain | Applies to | Answers |
|---|---|---|
| Claim status | One atomic knowledge claim | How well is this statement supported by current evidence? |
| Evidence status | One source locator | Can this exact source reference be resolved and trusted at its pinned revision? |
| Page content status | One Wiki page | Is this page a candidate, accepted, stale, or superseded? |
| Change status | One proposed Wiki change set | Where is this candidate in the quality and approval workflow? |
| Review execution status | One independent LLM review attempt | Was the isolated reviewer launched and did it return a valid, snapshot-bound report? |
| Review decision | One valid, completed LLM review report | What is the independent review outcome? |
| Human decision | One human decision record | What did the authorized human decide? |
| Publication status | One accepted Wiki revision | Is this revision part of the accepted/published Wiki history? |
| Run outcome | One workflow execution | Did this execution pass, partially complete, become blocked, or fail? |

Never infer one state domain from another. A `verified` claim does not mean its page is approved. A `PASS` review does not mean a change is published.

## 2. Claim status

Canonical values:

- `verified`: current, resolvable evidence directly supports the exact claim and its declared scope.
- `inferred`: the statement is an explicit, bounded derivation from cited evidence; reasoning and assumptions are recorded.
- `unknown`: evidence is insufficient, unavailable, or ambiguous.
- `stale`: one or more material source revisions or locators changed and have not been revalidated.
- `contradicted`: current evidence conflicts with the claim and the conflict is unresolved.

Allowed transitions:

| From | To | Condition |
|---|---|---|
| unknown | inferred | A traceable derivation is recorded, but direct proof is unavailable |
| unknown | verified | Direct evidence is located and checked |
| inferred | verified | Direct evidence now supports the exact statement |
| verified / inferred | stale | A supporting source revision/locator changes or becomes inaccessible |
| verified / inferred | contradicted | New evidence conflicts with the statement |
| stale | verified / inferred / unknown / contradicted | Revalidation determines the new status |
| contradicted | verified / inferred / unknown | Conflict is resolved by inspecting authoritative evidence |

A status transition MUST preserve the previous value and its review history. Do not silently overwrite a previously reviewed claim.

## 3. Evidence status

Canonical values:

- `valid`: exact repository, commit, path, and locator were resolved.
- `unverified`: recorded but not yet resolved against the pinned revision.
- `stale`: the referenced source revision or locator changed.
- `inaccessible`: the source cannot currently be accessed.
- `conflicting`: sources disagree or the locator supports incompatible interpretations.
- `redacted`: sensitive source content was intentionally not copied; locator and redaction reason remain.

Evidence status is independent from Claim status. A claim may be `unknown` while its available evidence references are all `valid`, because those sources do not answer the question.

## 4. Page content status

Canonical values:

- `candidate`: generated or edited content not yet published.
- `accepted`: content included in the accepted Wiki revision after required gates and human approval.
- `stale`: one or more material claims/evidence references require revalidation.
- `superseded`: replaced by a later accepted page/revision; retain history and links.

A page's content status is not the same as a Change Set status. The candidate's workflow state is recorded by its Change Set; publication changes page content status to accepted. Source changes can make accepted pages stale without deleting their historical acceptance record.

Page content transitions:

| From | To | Condition |
|---|---|---|
| candidate | accepted | The owning Change Set is approved and explicitly published |
| accepted | stale | Supporting source evidence changes or becomes unavailable |
| accepted | superseded | A replacement page/change is accepted and published |
| stale | accepted | A new candidate revalidates affected claims, passes all gates, and is published |
| stale | superseded | A corrected replacement is published |

A rejected candidate never changes an already accepted page. A proposed deletion keeps the current accepted page until the deletion Change Set is approved and published; the old page then becomes superseded or is retained as a historical page.

## 5. Change-set status

Canonical values:

| Status | Meaning | Allowed next states |
|---|---|---|
| `draft` | Candidate is being generated or revised | `lint_failed`, `pending_llm_review`, `rejected` |
| `lint_failed` | Deterministic checks found blocking errors | `draft`, `rejected` |
| `pending_llm_review` | Lint passed; awaiting a valid independent review result. If review cannot run, the Change Set stays here while the run outcome is BLOCKED. | `llm_changes_requested`, `pending_human_review`, `rejected` |
| `llm_changes_requested` | Reviewer returned REVISE | `draft`, `rejected` |
| `pending_human_review` | Independent review returned PASS; awaiting a human | `human_changes_requested`, `approved`, `rejected` |
| `human_changes_requested` | Human requested changes | `draft`, `rejected` |
| `approved` | Human approved the exact candidate snapshot | `published`, `approval_stale` |
| `approval_stale` | Approved snapshot no longer matches its approval binding | `draft`, `pending_llm_review`, `rejected` |
| `published` | Approved candidate was explicitly incorporated into accepted Wiki history | `superseded` |
| `rejected` | Candidate was rejected; it is immutable audit history | terminal |
| `superseded` | A later accepted revision replaces this published revision | terminal |

### Transition guards:

| Transition | Required condition |
|---|---|
| draft → lint_failed | Lint reports an unresolved required failure |
| draft → pending_llm_review | Full required Lint scope returns PASS |
| lint_failed → draft | Blocking Lint findings have been corrected |
| pending_llm_review → llm_changes_requested | Review execution status is COMPLETED; the report is valid and bound to the exact candidate/source snapshot; reviewer returns REVISE |
| pending_llm_review → pending_human_review | Review execution status is COMPLETED; the report is valid and bound to the exact candidate/source snapshot; reviewer returns PASS with no BLOCKER/MAJOR findings |
| pending_llm_review → rejected | Review execution status is COMPLETED; the report is valid and bound to the exact candidate/source snapshot; reviewer returns REJECT |
| llm_changes_requested → draft | Findings are acknowledged and a revised candidate is prepared |
| pending_human_review → human_changes_requested | Human records request_changes |
| pending_human_review → approved | Human records approve for the exact snapshot |
| pending_human_review → rejected | Human records reject |
| human_changes_requested → draft | Requested changes are accepted for implementation |
| approved → published | Human explicitly authorizes publication and the exact approved candidate is published |
| approved → approval_stale | A bound revision, diff, scope, or relevant source changes |
| approval_stale → draft | Impact is re-evaluated and a new candidate is prepared |
| published → superseded | A later accepted revision replaces it |

### Review execution status and run outcome

Review execution status is separate from both Change Set status and the LLM review decision. Use exactly:

- `NOT_RUN`: no valid isolated Review Subagent execution completed. This includes an unavailable host capability, failed/timed-out invocation, or no completed report.
- `RUNNING`: the host has launched the isolated Subagent and the invocation has not completed.
- `COMPLETED`: a report was returned and the orchestrator validated reviewer isolation, required scope, and exact candidate/source snapshot binding.
- `INVALID`: a report was returned but failed validation (for example, wrong snapshot, unproven isolation, reviewer write access, or missing mandatory scope).

The LLM review decision is a separate field and has exactly `PASS`, `REVISE`, or `REJECT`. It MUST be null unless Review execution status is `COMPLETED` with a valid report. `NOT_RUN`, `RUNNING`, and `INVALID` are not review decisions.

Review execution transitions:

| From | To | Condition |
|---|---|---|
| `NOT_RUN` | `RUNNING` | The host successfully launches a fresh, isolated Subagent invocation. |
| `RUNNING` | `COMPLETED` | A report is returned and the orchestrator validates isolation, required scope, and exact candidate/source snapshot binding. |
| `RUNNING` | `NOT_RUN` | The invocation fails or times out, or no completed report is returned. |
| `RUNNING` | `INVALID` | A report is returned but fails isolation, scope, read-only, or snapshot validation. |
| `INVALID` | `RUNNING` | A new invocation starts after the review package or host issue is corrected. |

A materially changed candidate or source snapshot requires a new review attempt; reset the current execution status to `NOT_RUN` and clear the current decision while retaining prior reports in audit history.

Run outcome is execution-level and has exactly `PASS`, `PARTIAL`, `BLOCKED`, or `FAIL`, as defined in docs/failure-handling.md. `BLOCKED` means a required prerequisite or gate prevents safe continuation; it is never a Change Set status or an LLM review decision.

If Lint has not returned a full required-scope PASS, do not transition the Change Set to `pending_llm_review`: keep it `draft` (or `lint_failed` when blocking Lint findings exist) and set the run outcome to `PARTIAL` or `BLOCKED` as appropriate. After Lint PASS, the Change Set enters `pending_llm_review`. If the Review Subagent cannot be launched or a valid report cannot be obtained, keep Change Status at `pending_llm_review`, set Review execution status to `NOT_RUN` or `INVALID`, set Review decision to null, and set Run outcome to `BLOCKED`. Do not advance to human review.

A required check that is NOT RUN or PARTIAL cannot satisfy the Lint PASS guard. LLM Review must run independently; a missing independent context leaves the run blocked, not the Change Set status. Human approval is never inferred from an LLM decision.

A failed or unavailable check MUST NOT be represented as PASS. If a required check cannot run, the candidate remains at its current Change Set status and the run is `PARTIAL` or `BLOCKED`; it cannot advance to human approval.

## 6. Review decisions

LLM review uses exactly:

- `PASS`: no BLOCKER or MAJOR finding; material claims, evidence, scope, and completeness are acceptable.
- `REVISE`: one or more fixable findings remain.
- `REJECT`: fundamental reliability problems, fabricated evidence, or repeated critical errors make the candidate unsuitable.

Severity values are `BLOCKER`, `MAJOR`, `MINOR`, and `INFO`. Any BLOCKER or MAJOR finding prohibits PASS. A score never overrides a blocking finding.

Human decisions use exactly:

- `approve`
- `request_changes`
- `reject`

Only an authorized human can create a human decision. LLM PASS is a recommendation, not an approval.

## 7. Gate order and invariants

1. Generate candidate pages and reports.
2. Run structural/provenance Lint.
3. Resolve all blocking Lint findings.
4. After Lint PASS, the orchestrator automatically delegates a fresh host-native Review Subagent and waits for its completed, snapshot-bound report.
5. Resolve REVISE findings and repeat Lint + a new independent Subagent invocation for the affected scope.
6. Present the exact candidate snapshot and review materials to a human.
7. Record a human decision bound to the candidate snapshot.
8. Publish only after explicit human approval and authorization for the publication action.

Invariants:
- No candidate content is treated as accepted knowledge before publication.
- Query defaults to accepted/published knowledge only.
- Query capture is a new draft Change Set using the same gates, including when source commits are unchanged. Index visibility reflects page/change state; a log event never grants approval or publication. See docs/wiki-maintenance.md for read-only query logging and frozen-snapshot handling.
- Rejected candidates and prior reports are retained as immutable audit history.
- Every review/approval is bound to exact revisions and scope.
- Frozen candidate records are snapshots; live state progress and post-freeze reports use the external binding/execution record until archival. Publication metadata finalization follows docs/human-review.md and cannot change reviewed knowledge content.
- Any material change after approval invalidates that approval.
- No Skill may approve its own generated content or silently publish/merge it.
- A missing, failed, or non-isolated automatic Review Subagent invocation sets Review execution status to `NOT_RUN` or `INVALID`, Review decision to null, and Run outcome to `BLOCKED`; Change Status remains `pending_llm_review`. There is no manual-session or same-context fallback.

## 8. Approval binding and invalidation

Each approval record MUST bind:
- change_id;
- candidate Wiki commit (or exact patch/diff digest when no commit exists);
- base Wiki commit;
- changed page IDs and paths;
- Source Manifest version/digest;
- relevant source repository IDs and full commit SHAs;
- Lint report ID/digest;
- independent Review report ID/digest;
- human decision, reviewer, timestamp, and rationale.

Approval becomes stale if the approved Wiki diff/candidate commit, reviewed page scope, relevant source revision, relevant manifest mapping, review report, or impact set changes. An unrelated source repository update need not invalidate approval if the approved scope's source snapshot and dependencies are demonstrably unchanged. Record that impact assessment; when uncertain, invalidate conservatively.

## 9. Re-review scope

After a change request or stale approval:
- rerun Lint over the complete candidate Wiki structure and all affected references;
- rerun independent Review over changed claims/pages plus dependent pages, interfaces, workflows, and System relationships;
- include prior findings and their disposition;
- obtain a new human decision for the new exact snapshot.

Do not reuse a previous PASS as if it reviewed changed content.
