# Source Evidence and Provenance

## 1. Purpose

The Wiki is a derived knowledge layer. Source code, build/configuration files, deployment definitions, and maintained engineering documents remain authoritative. Every important claim must be traceable to the exact source revision from which it was derived.

## 2. Required provenance

Record for each source repository:
- stable repository_id;
- submodule path or source path in the superproject;
- canonical repository identity when available;
- pinned full commit SHA;
- branch/tag as informational metadata only;
- AGENTS.md paths that were read;
- associated process IDs;
- associated Platform Profile IDs;
- ingestion timestamp.

Never store credentials, access tokens, private keys, or secret values in the manifest or Wiki.

## 3. Evidence locator

Preferred locators:
1. Repository-relative path plus line range at a pinned commit.
2. Stable symbol/function/type plus file path and commit.
3. Configuration key or XML/JSON/YAML path plus file path and commit.
4. Document heading/section plus file path and commit.

A path without a commit is insufficient for a reviewed claim. A line number without a path is insufficient.

## 4. Evidence types

- implementation: executable source code;
- declaration: interface/header/type declaration;
- configuration: startup, permission, service, build, or deployment configuration;
- build_graph: CMake DOT or other generated build dependency data;
- documentation: maintained technical documentation or README;
- test: test code or test result that demonstrates behavior;
- history: commit or change record.

Prefer implementation/configuration evidence for behavior claims. Comments and README descriptions are useful context but do not override contradictory implementation evidence.

## 5. Claim-to-evidence mapping

Every important claim must map to one or more specific evidence references. Avoid attaching a large generic source list to a page without showing which source supports which claim.

For each claim ask:
- Does the cited source support this exact statement?
- Is the source from the correct repository and commit?
- Does the evidence apply to the stated Platform Profile?
- Does it prove behavior, or only a declaration/build dependency?
- Are relevant conditions, compile flags, feature guards, or error paths omitted?

## 6. Negative claims

Claims such as "the process does not support suspend" or "there is no authentication" require a defined search scope and strong evidence. Absence from one file is not proof of absence from the system.

Prefer bounded wording: "No suspend handler was found in the inspected source paths at commit X" rather than "The process does not support suspend."

## 7. Generated artifacts

CMake DOT is evidence of CMake target/build dependencies for the recorded configure context. Record source commit, CMake version if known, generator, toolchain file and relevant options (without secrets), configure success/failure, and DOT artifact path.

Do not treat DOT edges as runtime dependencies or IPC. AST artifacts are out of scope for v0.1.0.

## 8. Source revision changes

When a repository commit changes:
- mark claims sourced from changed files as requiring revalidation;
- mark affected page-source mappings stale until checked;
- revalidate downstream interface/workflow/system claims when supporting evidence or relationship endpoints change;
- preserve previous reviewed Wiki history.

Do not silently update the recorded source commit while leaving old evidence locators marked verified.

## 9. Evidence quality

A strong evidence record is specific, reproducible, profile-scoped, and sufficient to support the claim. If evidence is indirect, mark the claim inferred and explain the reasoning. If the source cannot be inspected, mark unknown.
