# Strict Quality Gate

## 1. Approval policy

No generated Wiki content becomes accepted knowledge until it passes:
1. source-evidence validation;
2. independent LLM review;
3. human approval.

A high aggregate score cannot override a critical factual error or missing evidence.

## 2. Gate states

- PASS: no blocking or major findings; evidence and scope are adequate; ready for human approval.
- REVISE: fixable factual, evidence, completeness, or consistency problems remain.
- REJECT: fundamental unsupported architecture, fabricated evidence, or repeated/critical inaccuracies make the page unsuitable for acceptance.

PASS is not the same as merged. Human approval is still mandatory.

## 3. Review dimensions

| Dimension | Suggested weight |
|---|---:|
| Factual correctness | 30% |
| Evidence traceability | 25% |
| Completeness | 20% |
| Cross-page consistency | 15% |
| Clarity | 10% |

A critical finding in factual correctness or evidence traceability blocks PASS regardless of the score.

## 4. Independent LLM review

The reviewer must be a separate model invocation and a fresh context from generation. Prefer a different model when available.

If only one model endpoint exists:
- use a new session/context;
- provide original source excerpts and source revision metadata;
- provide generated Wiki pages and review criteria;
- instruct the reviewer to distrust the generator's conclusions and independently verify each claim;
- do not pass the generator's self-review as independent review.

The reviewer must not approve claims merely because they are confidently written or cited.

## 5. Review procedure

1. Enumerate material claims in the changed pages.
2. Resolve every evidence reference against the exact repository commit.
3. Check that each source supports the associated claim.
4. Verify profile scope and deployment context.
5. Check relationship types: build dependency vs runtime dependency vs IPC vs startup ordering.
6. Check lifecycle, failure paths, constraints, and relevant feature/configuration guards.
7. Compare claims with related pages and previous reviewed knowledge.
8. Identify missing, contradictory, stale, or overgeneralized statements.
9. Return findings and a PASS/REVISE/REJECT recommendation.

## 6. Severity

- BLOCKER: fabricated source/commit, material false architecture claim, unsafe security claim, or unsupported cross-process/runtime relationship.
- MAJOR: important claim lacks evidence, wrong profile scope, significant lifecycle/interface omission, or a build edge presented as runtime behavior.
- MINOR: incomplete detail, weak locator, small inconsistency, or unclear wording.
- INFO: optional improvement or follow-up investigation.

BLOCKER or MAJOR findings prohibit PASS.

## 7. Human approval

The human reviewer checks changed pages and diffs, the independent review report, unresolved/unknown claims, source revision changes, platform/profile applicability, and engineering usefulness.

Only the human may approve/merge the change into the accepted Wiki branch.

## 8. Required review report

Each report records review ID and timestamp, Wiki commit/branch, source repository commits, reviewer model identifier when available, independence declaration, pages/claims reviewed, findings with severity and evidence, recommendation, and human approval status.

Do not expose private source content in public review artifacts. The Engineering Wiki repository is expected to be Private.
