# Strict Quality Gate

## 1. Approval policy

No generated Wiki content becomes accepted knowledge until it passes:
1. source-evidence and structural validation (Lint);
2. automatic delegation to an independent LLM Review Subagent through the host's native Agent/Subagent capability;
3. human Review and approval of the exact candidate snapshot;
4. explicit publication authorization/action.

A high aggregate score cannot override a critical factual error or missing evidence. An LLM PASS is not human approval. Approval is not publication.

## 2. Separate state domains

Do not mix Claim status, Evidence status, Change status, LLM Review decision, Human decision, and Publication status. Their canonical values and transitions are defined in docs/state-machine.md.

## 3. Gate states

- PASS: no BLOCKER or MAJOR findings; evidence and scope are adequate; ready for human review.
- REVISE: fixable factual, evidence, completeness, or consistency problems remain.
- REJECT: fundamental unsupported architecture, fabricated evidence, or repeated/critical inaccuracies make the candidate unsuitable.

PASS is not the same as approved or published. A required check that did not run is NOT RUN and blocks progression; it must never be reported as PASS.

## 4. Review dimensions

| Dimension | Suggested weight |
|---|---:|
| Factual correctness | 30% |
| Evidence traceability | 25% |
| Completeness | 20% |
| Cross-page consistency | 15% |
| Clarity | 10% |

A critical finding in factual correctness or evidence traceability blocks PASS regardless of score.

## 5. Lint gate

Lint is a rule-driven structural/provenance audit, not a compiled linter in v0.1.0. It checks:
- required files, metadata, stable IDs, and schema;
- Source Manifest and exact pinned commits;
- Repository/Process/Profile mappings;
- Claim-Evidence references and locator resolution where the host can verify;
- Page-Source Map coverage and dependencies;
- internal links and relationship types;
- stale, contradictory, or overgeneralized claims;
- sensitive-data leakage.

Lint result is PASS / FAIL / PARTIAL. Every check is PASS / FAIL / NOT RUN with scope and reason. Required NOT RUN checks block progression. See references/lint-report-template.md.

## 6. Automatic Independent LLM Review

After Lint PASS, the orchestrator MUST automatically delegate a fresh Subagent invocation using `references/review-agent-task-template.md` and `skills/code-wiki-review/SKILL.md`. The reviewer must be a separate model invocation and fresh context from generation. Prefer a different model when available.

The host must expose native Subagent/Agent delegation and return a completed result. The Skill package does not create a new model context by itself. The reviewer must not inherit the Generation Agent transcript or hidden reasoning. There is no manual new-session or same-context fallback. If the host cannot launch the Subagent or prove isolation, set Review execution status to `NOT_RUN` (or `INVALID` for a returned but invalid report), keep Review decision null, leave Change Status at `pending_llm_review`, and set Run outcome to `BLOCKED`.

The reviewer must:
- receive exact source revisions, relevant source excerpts, candidate pages, Claim-Evidence mapping, Page-Source Map, and prior findings;
- enumerate material claims and verify evidence fit;
- check profile scope, process boundaries, interface direction, relationship types, lifecycle, failure paths, security, and deployment where applicable;
- challenge broad terms such as always, never, all platforms, required, and guaranteed;
- report exact claim, evidence, problem, severity, and correction.

If independent context cannot be established, report Review execution status `NOT_RUN` and Review decision null; keep Change Status at `pending_llm_review` and set Run outcome to `BLOCKED` before human approval. Generator self-review is not independent. The orchestrator must wait for the completed Subagent report and validate its candidate/source snapshot binding. See docs/independent-review-execution.md, references/review-agent-task-template.md, and references/review-report-template.md.

## 7. Severity

- BLOCKER: fabricated source/commit, material false architecture claim, unsafe security claim, or unsupported cross-process/runtime relationship.
- MAJOR: important claim lacks evidence, wrong profile scope, significant lifecycle/interface omission, or build/runtime confusion.
- MINOR: incomplete detail, weak locator, small inconsistency, or unclear wording.
- INFO: optional improvement or follow-up investigation.

BLOCKER or MAJOR findings prohibit PASS. A waiver cannot override fabricated evidence, BLOCKER, or a mandatory check that did not run.

## 8. Human approval

Human decisions are approve / request_changes / reject. Prepare the review package with references/human-review-summary-template.md before presenting it to the human reviewer.

The human reviewer must inspect:
- exact Wiki Diff and changed pages;
- Source Manifest and relevant source commits;
- Claim-Evidence mapping;
- Lint and independent Review reports;
- unresolved/unknown claims and impact pages;
- prior requests, findings, and waivers.

Approval MUST bind to the candidate Wiki commit or diff digest, base commit, changed page scope, Source Manifest version/digest, relevant source revisions, and report IDs. Any material change invalidates approval. Full rules and the decision record are in docs/human-review.md and references/human-decision-template.md.

## 9. Publication

Only the human may authorize publication/merge. The publication record links the resulting Wiki commit to the approval decision. Do not push, merge, or publish without explicit authorization. If a published change is wrong, create a corrective change or revert commit; do not rewrite published history.

## 10. Required reports

Each run stores the appropriate Init, Ingestion, Integration, or Update report, plus Lint report, independent Review report, and human decision record when those gates apply. Reports include exact source revisions, scope, checks not run, limitations, findings, and recovery actions.

Templates:
- references/init-report-template.md
- references/ingestion-report-template.md
- references/integration-report-template.md
- references/update-report-template.md
- references/lint-report-template.md
- references/review-agent-task-template.md
- references/review-report-template.md
- references/human-review-summary-template.md
- references/human-decision-template.md
