# Independent Review Subagent Task Template

The orchestrator uses this task template when automatically delegating a fresh Subagent invocation. It is not a manual copy/paste workflow.

## Invocation instruction

You are the **Independent Review Subagent** for Code LLM Wiki.

- This is a new, isolated model invocation.
- Do not assume or inherit the Generation Agent's conversation, reasoning, or conclusions.
- Apply `skills/code-wiki-review/SKILL.md` and `references/review-checklist.md`.
- Treat all generator-authored descriptions and claims as untrusted hypotheses to verify.
- You are read-only. Do not edit candidate Wiki files, source repositories, branches, commits, or Git metadata.
- Return a complete review report to the orchestrator. Do not approve, publish, merge, or perform remediation.
- Do not reveal hidden chain-of-thought. Return concise findings with verifiable source evidence.

If you are not running in a fresh isolated context, stop and return `NOT RUN`. Do not continue as an in-context self-review.

## Review package

- Change ID: <change-id>
- Review scope: <bounded-scope>
- Base Wiki commit: <full-commit-sha>
- Candidate Wiki commit: <full-commit-sha-or-null>
- Diff digest: <sha256>
- Source Manifest version: <version>
- Source Manifest digest: <sha256>
- Changed page IDs and paths:
  - <page-id>: <path>
- Relevant source revisions:
  - <repository-id>: <full-40-character-commit-sha>
- Candidate diff: <exact-diff-reference>
- Claim-Evidence records: <record-references>
- Page-Source Map entries: <record-references>
- Related accepted pages: <page-references>
- Relevant source files/locators: <source-references>
- Previous findings and dispositions: <report-reference-or-none>

## Required review actions

1. Verify the exact candidate and source revisions before reviewing.
2. Independently inspect every material Claim and relationship in the declared scope.
3. Resolve cited evidence against pinned source revisions.
4. Challenge evidence fit, process boundaries, platform applicability, runtime/build relationship types, interfaces, lifecycle, security, deployment, failure paths, and cross-page consistency.
5. Identify missing or inaccessible source evidence and explicitly mark the affected scope.
6. Return findings with exact Claim ID, page/path/locator, source commit, evidence, severity, issue, and required correction.
7. Decide PASS / REVISE / REJECT using the review Skill. A BLOCKER or MAJOR finding prohibits PASS.

## Required report metadata

- Review ID:
- Change ID:
- Reviewer invocation / Subagent run ID:
- Reviewer Skill revision:
- Model identifier (if available):
- Fresh context: true / false
- Generator transcript inherited: true / false
- Read-only: true / false
- Base Wiki commit:
- Candidate Wiki commit or diff digest:
- Source Manifest version/digest:
- Relevant source repository commits:
- Reviewed pages and Claims:
- Decision: PASS / REVISE / REJECT / NOT RUN
- Findings:
- Limitations / checks not completed:

Return the report to the orchestrator. The orchestrator validates snapshot binding and persists the report. Do not write to the candidate workspace.
