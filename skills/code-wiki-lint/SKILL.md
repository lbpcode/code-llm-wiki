---
name: code-wiki-lint
description: Validate Code LLM Wiki structure, metadata, links, source manifest, evidence locators, profile scopes, and stale references before semantic review or human approval.
---

# code-wiki-lint


## Goal

Perform a rule-based structural and provenance audit. This Skill does not require a custom TypeScript/Python runtime. Use available file listing, search, read, and Git operations.


## Output language

Follow `docs/language-policy.md`. Unless the user explicitly requests another language, write generated Wiki pages, query answers, review findings, and deliverables in **Simplified Chinese**. Preserve source identifiers, API names, paths, commands, configuration keys, and source excerpts verbatim. Keep schema keys, stable IDs, profile IDs, relationship types, and status enums in canonical English.

## Checks

### 1. Repository and manifest

- Required manifest exists.
- Every repository has a stable ID and full pinned commit SHA.
- Submodule paths and pins match the inspected superproject state.
- AGENTS.md inventory is recorded.
- No credentials or secrets are present.
- Only approved phase-one profiles are used unless explicitly authorized.

### 2. Page metadata

- Every substantive page has stable ID, title, type, and status.
- Process/profile pages reference valid IDs.
- Source revisions are recorded.
- Profile-specific pages use the correct profile ID.
- Common pages do not contain unsupported profile assumptions.

### 3. Evidence

- Every material claim has an evidence locator.
- Repository ID and commit resolve.
- Paths and line/symbol/configuration locators exist at the pinned revision where the host can verify them.
- Evidence type is appropriate to the claim.
- Stale evidence is not marked verified.
- Build graph evidence is not used as runtime evidence.

### 4. Links and consistency

- Internal Markdown links resolve.
- IDs are unique.
- No broken or orphaned high-value pages.
- Process and repository references resolve.
- Relationship types are explicit.
- Duplicate or contradictory claims are reported.

### 5. Platform scope

- Profile IDs are qnx, android, or linux-tbox in v0.1.0.
- Linux-TBOX remains one bound profile.
- QNX/Android deployment context is not guessed.
- Unsupported profiles are not generated.
- Claims are not generalized across uninspected profiles.

## Output

Return PASS / FAIL / PARTIAL, checks performed and checks not executable, findings with file path and exact location, stale/unresolved evidence, and recommended fixes.

## Capability honesty

If file listing, Git revision inspection, or source locator resolution is unavailable, report those checks as NOT RUN. Do not claim a deterministic check passed when the required operation was unavailable.

This Skill is a rule-driven prompt workflow, not a compiled linter. A future optional script may automate repeatable checks, but it is out of scope for v0.1.0.
