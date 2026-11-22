# Human Review, Approval, and Publication

## 1. Responsibility boundary

The three quality gates have different responsibilities. Independent LLM Review is automatically delegated to a fresh, read-only Subagent by the orchestrator; it is not a manual second-session workflow:

| Gate | Owner | Responsibility | Can approve publication? |
|---|---|---|---|
| Source-evidence / Lint | Workflow Skill / available deterministic checks | Structure, provenance, locator, schema, link, and consistency checks | No |
| Independent LLM Review | Automatically delegated host-native Subagent with fresh context | Challenge factual claims, evidence fit, scope, omissions, and contradictions | No |
| Human Review | Authorized human reviewer | Judge engineering correctness, usefulness, unresolved risk, and exact proposed diff | Yes, for the reviewed snapshot |

An LLM PASS is not a human approval. A human approval does not excuse missing required evidence or a skipped independent review. The orchestrator must automatically launch and await the Subagent; the user is not asked to manually open another conversation. If the host cannot delegate an isolated Subagent, set Review execution status to NOT_RUN, leave Review decision null, keep Change Status at pending_llm_review, and set Run outcome to BLOCKED; do not present the candidate for human approval.

## 2. Required review package

Before human review, present one immutable candidate package using references/human-review-summary-template.md. It must contain:

- change ID and purpose;
- base Wiki commit and candidate Wiki commit, or exact patch digest;
- changed page list and page IDs;
- Source Manifest version/digest;
- relevant source repository IDs and full commit SHAs;
- Claim-Evidence mapping for all material changed claims;
- Lint report and checks not executable;
- independent LLM Review report;
- unresolved questions, unknowns, stale evidence, and contradictions;
- impact analysis for dependent pages;
- prior human decisions and change-request dispositions, if any.

Do not ask a human to approve a summary without access to the actual diff and supporting evidence.

## 3. Human decisions

### Approve

Use only when the reviewer has inspected the exact diff and review package, all required gates have passed, and remaining limitations are explicitly accepted.

Record the approval binding described in docs/state-machine.md. Approval applies only to that exact snapshot and scope.

### Request Changes

Use when the candidate is potentially acceptable but needs correction or more evidence.

The decision record MUST include actionable findings, affected pages/claims, expected correction, and whether source investigation is required. Return the change set to `draft`; retain the request and previous reports. After changes, rerun Lint and independent Review for the impact scope and request a new human decision.

### Reject

Use when the candidate is unsuitable, the underlying analysis is unreliable, or the proposed scope should not be accepted.

A rejected candidate is immutable audit history. Do not silently reopen or rewrite it. A materially new attempt gets a new change ID and links to the rejected predecessor.

## 4. Approval binding

A human approval record MUST include:

- `human_decision_id`;
- `change_id`;
- `decision`;
- `reviewer` (human identity as configured by the project);
- `timestamp`;
- `base_wiki_commit`;
- `candidate_wiki_commit` or `diff_digest`;
- `changed_page_ids`;
- `source_manifest_version` and `source_manifest_digest`;
- relevant `source_revisions` (repository IDs and full commit SHAs);
- `lint_report_id` and `review_report_id`;
- `comments`;
- `waivers` with explicit reason, scope, and expiry/revalidation condition where applicable.

A waiver cannot override fabricated evidence, a BLOCKER, or a mandatory gate that did not run.

For reproducible binding, compute `source_manifest_digest` as SHA-256 over the exact UTF-8 bytes (LF line endings) of the committed `wiki/_meta/source-manifest.yaml`. Compute `diff_digest` as SHA-256 over the exact output bytes of `git diff --binary --no-ext-diff --no-renames <base_wiki_commit> <candidate_wiki_commit>`. The Change Set and Human Decision record must store the same values.

## 5. Approval invalidation

Set change status to `approval_stale` if:

- candidate content, diff digest, or candidate commit changes;
- a changed page is added/removed or the reviewed scope changes;
- a relevant source commit or evidence locator changes;
- relevant Source Manifest mappings change;
- a new contradiction or blocking finding appears;
- the base revision changes in a way that alters the reviewed result.

If only unrelated repositories change, preserve approval only after recording a dependency-impact assessment proving that the approved pages and their source snapshot are unaffected. When uncertain, invalidate conservatively.

An approval is never transferred to a new commit merely because the text appears similar.

## 6. AI edits and human edits

- AI-generated changes MUST be prepared as a proposed diff on a separate Wiki branch/worktree.
- Never overwrite uncommitted human changes.
- Never discard a human-authored section merely because it is absent from generated output.
- Before applying an update, compare the current page with the last accepted base and identify human modifications.
- If AI and human edits touch the same semantic section or claim, stop automatic application and report a merge conflict.
- If edits are disjoint, a three-way merge may be proposed, but the resulting diff must be reviewed as a new candidate.
- Preserve human wording and decisions unless the human explicitly authorizes replacement.
- Record the origin of substantive human edits in the page-source map or decision history when it affects future update behavior.

## 7. Publication and rollback

Approval and publication are separate events.

- Approval means the exact candidate is accepted by a human.
- Publication means the approved candidate is explicitly incorporated into the accepted Wiki branch.
- No Skill may push, merge, or publish without explicit authorization for that action.
- Record the publication commit and link it to the approval decision.
- If a published change is later found incorrect, create a corrective change or revert commit. Do not rewrite published Git history.
- Mark the previous published change as superseded only after the replacement/revert is accepted.

## 8. Audit retention

Keep rejected candidates, review reports, request-change decisions, approvals, waivers, and publication records. Do not delete failed history to make the current Wiki appear clean. Apply the repository's Private visibility and secret-redaction rules to all audit artifacts.
