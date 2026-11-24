---
name: code-wiki-init
description: Initialize a Code LLM Wiki from a source superproject containing multiple Git repositories or submodules. Inventory repositories, AGENTS.md files, pinned commits, Repository/Process mappings, and phase-one Platform Profiles.
---

# code-wiki-init

## Goal

Create the initial source inventory and Wiki skeleton for a multi-repository software system. Do not write substantive architecture claims before inspecting source repositories.

## Normative references

Follow docs/skill-contracts.md, docs/wiki-schema.md, docs/claim-evidence-model.md, docs/state-machine.md, docs/failure-handling.md, and docs/language-policy.md. Use references/source-manifest-template.md, references/repository-template.md, references/page-source-map-template.md, and references/init-report-template.md.

Follow docs/wiki-maintenance.md for the destination entry point, navigation, and log. Use references/wiki-agents-template.md, references/wiki-index-template.md, and references/wiki-log-template.md.

## Inputs

Required:
- Source superproject path/workspace.
- Destination Engineering Wiki repository/worktree.
- Permission to read the source workspace and write to the designated Wiki workspace.

Optional:
- System name/ID.
- Explicitly confirmed process and profile mappings.
- Prior Source Manifest and Wiki inventory for reinitialization.

## Preconditions

- Confirm the source root and Wiki destination are distinct authorized workspaces.
- Inspect Git status before any write; do not overwrite uncommitted user changes.
- If a previous manifest exists, preserve it and compare rather than silently replacing it.
- Confirm which source revision is intended. A submodule mismatch blocks ingestion for that repository.

## Procedure

1. Inspect superproject root, Git status, current full commit SHA, and .gitmodules.
2. Read top-level AGENTS.md and applicable parent instructions.
3. Enumerate submodules and record path, repository identity when available, expected pinned SHA, actual checkout SHA, and checkout status.
4. Discover AGENTS.md files in each accessible repository and read them before analyzing that repository.
5. Record inaccessible, uninitialized, permission-denied, and mismatched repositories explicitly.
6. Identify candidate processes from executable entry points, service definitions, init/service configuration, build targets, documentation, and explicit project metadata.
7. Create Repository-to-Process mappings with status confirmed/candidate/unknown/rejected and evidence refs. Do not equate repository = process.
8. Create Process-to-Platform Profile mappings separately with support status supported_verified/present_unverified/unsupported_verified/unknown.
9. Ask the human only where a materially ambiguous mapping cannot be resolved from source evidence. Preserve unresolved mappings as Unknown until answered.
10. Register only qnx, android, and linux-tbox. QNX/Android deployment context remains unknown unless confirmed.
11. Create the Source Manifest from references/source-manifest-template.md. Pin full commit SHAs for the superproject and every repository.
12. Create the Wiki skeleton from docs/wiki-schema.md and its index. Index only existing substantive pages, with summaries and explicit page/change status; state when published knowledge is empty. Do not create substantive architecture pages or verified Claims during inventory.
13. Create or propose a managed Code LLM Wiki section in the destination-root AGENTS.md. Preserve existing content and record any conflicts. Include self-contained query rules, actual artifact paths, query_logging disabled by default unless an existing authorized policy says otherwise, and a reproducible full-package locator/revision. Do not substitute the source repository's AGENTS.md for this destination entry point.
14. Initialize log.md without replacing existing history. Create an initialization report recording scope, successful/failed/skipped repositories, mapping confidence, maintenance artifacts, and open questions; append an observed init event in the authorized workspace. Do not invent earlier events.

## Outputs

- Source Manifest.
- Repository inventory with checkout status and AGENTS.md inventory; create repository pages using references/repository-template.md when they add durable value.
- Repository-to-Process mapping table.
- Process-to-Profile applicability table.
- Wiki directory skeleton and index.
- Destination-root AGENTS.md maintenance section and package provenance.
- Append-only operation log and init event.
- Initialization report and open questions.

## Acceptance checks

- Every accessible/checked-out repository has its exact full commit recorded.
- Submodule expected and actual commits are compared.
- AGENTS.md files are inventoried and read or explicitly marked inaccessible.
- Repository and Process are modeled separately.
- Profile applicability is attached to Process, not blindly inherited from Repository.
- No unsupported process/profile relationship or architecture Claim is asserted.
- No secrets are copied into the Wiki.
- The destination entry point, index, and log resolve; existing human instructions/history are preserved, and no candidate is listed as published.

## Failure behavior

Follow docs/failure-handling.md. Continue independent repositories where safe, but return PARTIAL when any in-scope repository is skipped/inaccessible. Return BLOCKED for an unsafe or inconsistent source snapshot. Never report incomplete inventory as PASS.

## Safety

Do not change source code, submodule pins, repository configuration, or Git remotes. Do not delete or replace existing Wiki history. Do not commit, push, create a PR, or merge without explicit authorization.
