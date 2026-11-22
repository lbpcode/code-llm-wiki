# Workflow and State Model

## 1. State domains are separate

The workflow MUST NOT use one status field to represent both the truth of a claim and the approval state of a Wiki change.

| State domain | Applies to | Answers |
|---|---|---|
| Claim status | One atomic knowledge claim | How well is this statement supported by current evidence? |
| Evidence status | One source locator | Can this exact source reference be resolved and trusted at its pinned revision? |
| Change status | One proposed Wiki change set | Where is this candidate in the quality and approval workflow? |
| Review decision | One LLM review run | What is the independent review outcome? |
| Human decision | One human decision record | What did the authorized human decide? |
| Publication status | One accepted Wiki revision | Is this revision part of the accepted/published Wiki history? |

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
| verified | stale | A supporting source revision/locator changes or becomes inaccessible |
| inferred | stale | A supporting source revision/locator changes or becomes inaccessible |
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

Evidence status is independent from claim status. For example, a claim may be `unknown` while its available evidence references are all `valid`, because those sources do not answer the question.

## 4. Change-set status

Canonical values:

| Status | Meaning | Allowed next states |
|---|---|---|
| `draft` | Candidate is being generated or revised | `lint_failed`, `pending_llm_review`, `rejected` |
| `lint_failed` | Deterministic checks found blocking errors | `draft`, `rejected` |
| `pending_llm_review` | Lint passed and independent review is requested | `llm_changes_requested`, `pending_human_review`, `rejected` |
| `llm_changes_requested` | Reviewer returned REVISE | `draft`, `rejected` |
| `pending_human_review` | Independent review returned PASS; awaiting a human | `human_changes_requested`, `approved`, `rejected` |
| `human_changes_requested` | Human requested changes | `draft`, `rejected` |
| `approved` | Human approved the exact candidate snapshot | `published`, `approval_stale` |
| `approval_stale` | Approved snapshot no longer matches its approval binding | `draft`, `pending_llm_review`, `rejected` |
| `published` | Approved candidate was explicitly incorporated into accepted Wiki history | `superseded` |
| `rejected` | Candidate was rejected; it is immutable audit history | terminal |
| `superseded` | A later accepted revision replaces this published revision | terminal |

A failed or unavailable check MUST NOT be represented as PASS. If a required check cannot run, the candidate remains blocked or the check result is PARTIAL; it cannot advance to human approval.

## 5. Review decisions

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

## 6. Gate order and invariants

The required order is:

1. Generate candidate pages and reports.
2. Run structural/provenance Lint.
3. Resolve all blocking Lint findings.
4. Run independent LLM Review in a fresh context.
5. Resolve REVISE findings and repeat Lint + independent Review for the affected scope.
6. Present the exact candidate snapshot and review materials to a human.
7. Record a human decision bound to the candidate snapshot.
8. Publish only after explicit human approval and authorization for the publication action.

Invariants:

- No candidate content is treated as accepted knowledge before publication.
- Query defaults to published knowledge only.
- Rejected candidates and prior reports are retained as immutable audit history.
- Every review/approval is bound to exact revisions and scope.
- Any material change after approval invalidates that approval.
- No Skill may approve its own generated content or silently publish/merge it.
- A missing independent review session is NOT RUN/BLOCKED, never PASS.

## 7. Approval binding and invalidation

Each approval record MUST bind:

- change_id;
- candidate Wiki commit (or exact patch/diff digest when no commit exists);
- base Wiki commit;
- changed page IDs and paths;
- source manifest version/digest;
- relevant source repository IDs and full commit SHAs;
- Lint report ID/digest;
- independent Review report ID/digest;
- human decision, reviewer, timestamp, and rationale.

Approval becomes stale if any of the following changes after approval:

- approved Wiki diff or candidate commit;
- approved base commit in a way that changes the reviewed result;
- source manifest data relevant to the approved claims;
- any relevant source repository commit or evidence locator;
- review report or finding disposition;
- changed-page scope or dependency impact set.

An unrelated source repository update need not invalidate an approval if the approved scope's source snapshot and page dependencies are demonstrably unchanged. Record that impact assessment. When uncertain, invalidate conservatively.

## 8. Re-review scope

After a change request or stale approval:

- rerun Lint over the complete candidate Wiki structure and all affected references;
- rerun independent Review over changed claims/pages plus dependent pages, interfaces, workflows, and System relationships;
- include prior findings and their disposition;
- obtain a new human decision for the new exact snapshot.

Do not reuse a previous PASS as if it reviewed changed content.
