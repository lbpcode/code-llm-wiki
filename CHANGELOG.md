# Changelog

## v0.1.0

- Establish a Process-centric, multi-repository Code LLM Wiki.
- Define QNX, Android, and Linux-TBOX as the first-phase Platform Profiles.
- Bind deployment context to Platform Profile instead of creating an unrestricted OS/product matrix.
- Define separate System-level and Process-level knowledge and Repository ↔ Process many-to-many mapping.
- Add explicit Process-to-Profile applicability records.
- Add atomic Claim-Evidence mapping and Page-Source Map for source provenance and incremental impact analysis.
- Define separate Claim, Evidence, Page, Change Set, Review, Human Decision, and Publication state domains.
- Define Lint → automatically delegated independent Review Subagent → Human Review → explicitly authorized Publication gates.
- Bind human approval to the exact candidate diff/Wiki revision and relevant Source Manifest/source revisions; define approval invalidation.
- Define automatic host-native Subagent delegation, fresh-context isolation, read-only review, snapshot-bound reports, and blocked behavior when delegation is unavailable. No manual-session or same-context fallback.\n- Define failure handling for partial repository failures, commit mismatches, inaccessible sources, evidence conflicts, review failures, human edits, stale claims, and sensitive data.
- Add Change Set, Init, Ingestion, Integration, Update, Lint, Independent Review, Independent Review Subagent Task, Human Review Summary, Human Decision, Repository, Claim, Evidence, Page-Source Map, Interface, Workflow, Platform Profile, and Architecture Decision templates.
- Include optional CMake Graphviz DOT as build-dependency evidence; defer AST extraction.
- Provide portable Skill/Prompt workflows without a custom TypeScript runtime.
- Define English Skill instructions and Simplified Chinese as the default generated Wiki/report language, preserving source identifiers and machine-readable metadata.
- Real business repository end-to-end POC remains out of scope for Phase 0.
