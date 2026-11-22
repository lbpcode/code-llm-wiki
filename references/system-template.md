# System Wiki Page Template

## Metadata

- System ID:
- Source superproject and full commit:
- Source Manifest version/digest:
- Source revisions:
- Platform Profiles covered:
- Content status:
- Change ID:
- Last reviewed:

## 1. System Overview

Describe system purpose and major responsibilities. Avoid unsupported product assumptions. Map material statements to Claim IDs.

## 2. Process Inventory

List processes with stable Process IDs, implementing repositories, Repository-to-Process mapping status, and confirmed Process-to-Profile support.

## 3. System Architecture

Describe process boundaries and high-level relationships. Every edge must have:
- relationship ID;
- from entity;
- explicit relationship type;
- to entity;
- profile scope;
- evidence references;
- status and constraints.

## 4. Runtime Dependencies

Record only dependencies that affect runtime behavior. Identify startup, availability, timeout, and failure semantics where evidence exists. Do not infer from build linkage.

## 5. Inter-process Interfaces

Describe providers, consumers, protocols, data contracts, versioning, error semantics, and profile-specific variants. Check both sides where possible; one-sided evidence remains a candidate/unknown.

## 6. Startup and Shutdown

Create a profile-specific sequence. Include actor, action, precondition, expected result, timeout, failure path, and evidence. Do not combine sequences across profiles unless equivalence is proven.

## 7. Suspend and Resume

Record participating processes, ordering, state persistence, wake sources, timeout constraints, and failure behavior for each applicable profile. Mark uninspected behavior Unknown.

## 8. Data Flow

Describe system-level data movement and ownership. Distinguish control plane from data plane where useful. Map material claims to evidence.

## 9. Platform Differences

Compare QNX, Android, and Linux-TBOX only where the relevant Process/Profile source repositories have been inspected. Mark uninspected areas Unknown.

## 10. Deployment and Security

Summarize process composition, startup configuration, permissions, and security boundaries per profile.

## 11. Contradictions, Risks, and Open Questions

Track source conflicts, unverified relationships, missing repositories, unknown platform behavior, and engineering decisions required.

## 12. Claim-Evidence and Page-Source Index

Every material architecture statement must link to exact evidence at pinned commits. Maintain Page-Source Map dependencies to affected Process, Interface, and Workflow pages.
