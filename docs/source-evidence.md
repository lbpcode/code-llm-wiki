# Source Evidence and Provenance

## 1. Purpose

The Wiki is a derived knowledge layer. Source code, build/configuration files, deployment definitions, tests, and maintained engineering documents remain authoritative. Every material claim must be traceable to the exact source revision from which it was derived.

The normative Claim, Evidence, and Page-Source Map data model is defined in docs/claim-evidence-model.md. Reusable record formats are in references/claim-template.md and references/page-source-map-template.md.

## 2. Required provenance

Record for each source repository:
- stable repository_id;
- submodule path or source path in the superproject;
- canonical repository identity when available;
- pinned full commit SHA;
- branch/tag as informational metadata only;
- AGENTS.md paths that were read;
- repository-to-process mappings and their evidence/status;
- ingestion timestamp.

Record Process-to-Platform Profile applicability separately. Do not assume all processes in one repository share the same platform support.

Never store credentials, access tokens, private keys, or secret values in the manifest or Wiki.

## 3. Evidence locator

Preferred locators:
1. Repository-relative path plus line range at a pinned commit.
2. Stable symbol/function/type plus file path and commit.
3. Configuration key or XML/JSON/YAML path plus file path and commit.
4. Document heading/section plus file path and commit.
5. Generated artifact path plus generation context and source commit.

A path without a commit is insufficient for a reviewed claim. A line number without a path is insufficient. A branch name is not a source revision.

## 4. Evidence types and status

Evidence types:
- implementation: executable source code;
- declaration: interface/header/type declaration;
- configuration: startup, permission, service, build, or deployment configuration;
- build_graph: CMake DOT or other generated build dependency data;
- documentation: maintained technical documentation or README;
- test: test code or test result that demonstrates behavior;
- history: commit or change record.

Evidence status is separate from Claim status:
- valid;
- unverified;
- stale;
- inaccessible;
- conflicting;
- redacted.

Prefer implementation/configuration evidence for behavior claims. Comments and README descriptions are context but do not override contradictory implementation evidence.

## 5. Claim-to-evidence mapping

Every material claim maps to one or more specific evidence records. Each link states whether the evidence supports, contradicts, or qualifies the claim. Avoid attaching a large generic source list to a page without showing which source supports which claim.

For each claim ask:
- Does the cited source support this exact statement?
- Is the source from the correct repository and commit?
- Does the evidence apply to the stated Platform Profile?
- Does it prove behavior, or only a declaration/build dependency?
- Are relevant conditions, compile flags, feature guards, error paths, and configuration branches omitted?
- Is the statement atomic and bounded?

Inferred claims must include reasoning and assumptions. Unknown claims must identify the missing evidence. Negative claims must define the inspected scope and method.

## 6. Sensitive information

Do not copy credentials, tokens, private keys, personal data, or sensitive payloads into Wiki pages, reports, examples, or review artifacts.

When sensitive material is encountered:
- stop copying the excerpt;
- retain only a safe source locator and evidence metadata;
- set evidence status to redacted and record a non-sensitive reason;
- report the affected path and required handling without echoing the secret;
- follow the source project's incident/secret-handling procedure.

## 7. Generated artifacts

CMake DOT is evidence of CMake target/build dependencies for the recorded configure context. Record source commit, CMake version if known, generator, toolchain file and relevant options (without secrets), configure success/failure, and DOT artifact path.

Do not treat DOT edges as runtime dependencies or IPC. AST artifacts are out of scope for v0.1.0.

## 8. Source revision changes

When a repository commit changes:
- compare full old/new commit SHAs;
- identify changed paths;
- mark evidence sourced from changed paths stale until revalidated;
- mark dependent claims and pages stale;
- use Page-Source Map to identify downstream Interface, Workflow, and System pages;
- revalidate both sides of affected interfaces/relationships where possible;
- preserve previous reviewed Wiki history.

Do not silently update the recorded source commit while leaving old evidence locators marked verified. If impact cannot be mapped reliably, mark it unknown and broaden review conservatively.

## 9. Evidence quality

A strong evidence record is specific, reproducible, profile-scoped, and sufficient to support the exact claim. If evidence is indirect, mark the claim inferred and explain the reasoning. If the source cannot be inspected, mark unknown or inaccessible; never fabricate a locator.
